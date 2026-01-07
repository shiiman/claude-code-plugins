"""Gmail helpers for shiiman-google."""

import argparse
import base64
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

from googleapiclient.discovery import build

from google_utils import (
    TOKENS_DIR,
    format_output,
    get_token_path,
    handle_api_error,
    list_profiles,
    load_credentials,
    print_error,
)

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
]


def _get_service(token_path: str):
    """Gmail サービスを取得する。"""
    creds = load_credentials(token_path, DEFAULT_SCOPES)
    return build("gmail", "v1", credentials=creds)


def _fetch_all_message_ids(
    service,
    query: str,
    max_results: Optional[int] = None,
) -> List[str]:
    """クエリに一致する全メッセージIDを取得する（ページネーション対応）。

    Args:
        service: Gmail サービス
        query: 検索クエリ
        max_results: 最大取得件数（None の場合は全件）

    Returns:
        メッセージIDのリスト
    """
    message_ids = []
    page_token = None

    while True:
        # 1回の API 呼び出しで取得する件数
        page_size = 100
        if max_results is not None:
            remaining = max_results - len(message_ids)
            if remaining <= 0:
                break
            page_size = min(page_size, remaining)

        response = (
            service.users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=page_size,
                pageToken=page_token,
            )
            .execute()
        )

        messages = response.get("messages", [])
        message_ids.extend([msg["id"] for msg in messages])

        page_token = response.get("nextPageToken")
        if not page_token:
            break

        if max_results is not None and len(message_ids) >= max_results:
            break

    return message_ids


def _get_message_metadata(service, message_ids: List[str]) -> List[dict]:
    """メッセージのメタデータを取得する。"""
    results = []
    for message_id in message_ids:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=message_id, format="metadata")
            .execute()
        )
        headers = {
            h["name"].lower(): h["value"]
            for h in msg.get("payload", {}).get("headers", [])
        }
        results.append(
            {
                "id": message_id,
                "subject": headers.get("subject", ""),
                "from": headers.get("from", ""),
                "date": headers.get("date", ""),
            }
        )
    return results


def list_unread(token_path: str, max_results: int = 20) -> List[dict]:
    """未読メッセージ一覧を取得する。"""
    service = _get_service(token_path)
    message_ids = _fetch_all_message_ids(service, "is:unread", max_results)
    return _get_message_metadata(service, message_ids)


def list_starred(token_path: str, max_results: int = 20) -> List[dict]:
    """スター付きメッセージ一覧を取得する。"""
    service = _get_service(token_path)
    message_ids = _fetch_all_message_ids(service, "is:starred", max_results)
    return _get_message_metadata(service, message_ids)


def read_message(token_path: str, message_id: str) -> str:
    """メッセージ本文を取得する。"""
    service = _get_service(token_path)
    msg = (
        service.users()
        .messages()
        .get(userId="me", id=message_id, format="full")
        .execute()
    )
    payload = msg.get("payload", {})
    parts = payload.get("parts", [])
    data = payload.get("body", {}).get("data")

    if not data:
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data")
                break

    if not data:
        return ""

    decoded = base64.urlsafe_b64decode(data.encode("utf-8"))
    return decoded.decode("utf-8", errors="replace")


def mark_read(token_path: str, message_ids: List[str]) -> int:
    """メッセージを既読にする。

    Returns:
        既読にしたメッセージ数
    """
    if not message_ids:
        return 0

    service = _get_service(token_path)

    # 500件ずつバッチ処理
    batch_size = 500
    total = 0

    for i in range(0, len(message_ids), batch_size):
        batch_ids = message_ids[i : i + batch_size]
        service.users().messages().batchModify(
            userId="me",
            body={"ids": batch_ids, "removeLabelIds": ["UNREAD"]},
        ).execute()
        total += len(batch_ids)

    return total


def star_messages(token_path: str, message_ids: List[str]) -> int:
    """メッセージにスターを付ける。

    Returns:
        スターを付けたメッセージ数
    """
    if not message_ids:
        return 0

    service = _get_service(token_path)
    service.users().messages().batchModify(
        userId="me",
        body={"ids": message_ids, "addLabelIds": ["STARRED"]},
    ).execute()
    return len(message_ids)


def unstar_messages(token_path: str, message_ids: List[str]) -> int:
    """メッセージのスターを外す。

    Returns:
        スターを外したメッセージ数
    """
    if not message_ids:
        return 0

    service = _get_service(token_path)
    service.users().messages().batchModify(
        userId="me",
        body={"ids": message_ids, "removeLabelIds": ["STARRED"]},
    ).execute()
    return len(message_ids)


def _create_message(
    to: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    html: bool = False,
) -> dict:
    """MIMEメッセージを作成する。"""
    if html:
        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(body, "plain", "utf-8"))
        msg.attach(MIMEText(body, "html", "utf-8"))
    else:
        msg = MIMEText(body, "plain", "utf-8")

    msg["to"] = to
    msg["subject"] = subject
    if cc:
        msg["cc"] = cc
    if bcc:
        msg["bcc"] = bcc

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    return {"raw": raw}


def send_message(
    token_path: str,
    to: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    html: bool = False,
) -> dict:
    """メールを送信する。

    Args:
        token_path: トークンファイルパス
        to: 宛先メールアドレス
        subject: 件名
        body: 本文
        cc: CC（カンマ区切り）
        bcc: BCC（カンマ区切り）
        html: HTMLメールとして送信

    Returns:
        送信結果（id, threadId）
    """
    service = _get_service(token_path)
    message = _create_message(to, subject, body, cc, bcc, html)
    result = service.users().messages().send(userId="me", body=message).execute()
    return {
        "id": result["id"],
        "threadId": result.get("threadId", ""),
        "to": to,
        "subject": subject,
        "url": f"https://mail.google.com/mail/u/0/#sent/{result['id']}",
    }


def create_draft(
    token_path: str,
    to: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    html: bool = False,
) -> dict:
    """下書きを作成する。

    Args:
        token_path: トークンファイルパス
        to: 宛先メールアドレス
        subject: 件名
        body: 本文
        cc: CC（カンマ区切り）
        bcc: BCC（カンマ区切り）
        html: HTMLメールとして送信

    Returns:
        下書き情報（id, message.id）
    """
    service = _get_service(token_path)
    message = _create_message(to, subject, body, cc, bcc, html)
    result = (
        service.users()
        .drafts()
        .create(userId="me", body={"message": message})
        .execute()
    )
    return {
        "id": result["id"],
        "messageId": result["message"]["id"],
        "to": to,
        "subject": subject,
        "url": f"https://mail.google.com/mail/u/0/#drafts?compose={result['id']}",
    }


def list_unread_all_profiles(max_results: int = 20) -> dict:
    """全プロファイルの未読メッセージを取得する。

    Returns:
        プロファイル名をキー、未読メッセージリストを値とする辞書
    """
    profiles = list_profiles()
    if not profiles:
        return {}

    results = {}
    for profile in profiles:
        token_path = get_token_path(profile)
        try:
            items = list_unread(token_path, max_results)
            results[profile] = items
        except Exception as e:
            results[profile] = {"error": str(e)}

    return results


def mark_read_all_profiles() -> dict:
    """全プロファイルの未読メッセージを既読にする。

    Returns:
        プロファイル名をキー、既読にしたメッセージ数を値とする辞書
    """
    profiles = list_profiles()
    if not profiles:
        return {}

    results = {}
    for profile in profiles:
        token_path = get_token_path(profile)
        try:
            service = _get_service(token_path)
            # 全未読メッセージを取得
            message_ids = _fetch_all_message_ids(service, "is:unread", max_results=None)
            count = mark_read(token_path, message_ids)
            results[profile] = {"count": count}
        except Exception as e:
            results[profile] = {"error": str(e)}

    return results


@handle_api_error
def main() -> None:
    parser = argparse.ArgumentParser(description="Gmail 操作ツール")
    parser.add_argument("--token", help="トークンファイルパス")
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="出力形式 (デフォルト: table)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # unread サブコマンド
    unread_parser = subparsers.add_parser("unread", help="未読メッセージ一覧")
    unread_parser.add_argument("--max", type=int, default=20, help="最大取得件数")

    # starred サブコマンド
    starred_parser = subparsers.add_parser("starred", help="スター付きメッセージ一覧")
    starred_parser.add_argument("--max", type=int, default=20, help="最大取得件数")

    # read サブコマンド
    read_parser = subparsers.add_parser("read", help="メッセージ本文表示")
    read_parser.add_argument("--id", required=True, help="メッセージID")

    # mark-read サブコマンド
    mark_parser = subparsers.add_parser("mark-read", help="既読化")
    mark_parser.add_argument("--ids", nargs="+", help="メッセージID（複数可）")
    mark_parser.add_argument("--all", action="store_true", help="全未読を既読化")

    # star サブコマンド
    star_parser = subparsers.add_parser("star", help="スター操作")
    star_parser.add_argument("--ids", nargs="+", required=True, help="メッセージID（複数可）")
    star_parser.add_argument("--remove", action="store_true", help="スターを外す")

    # unread-all サブコマンド（全プロファイル）
    unread_all_parser = subparsers.add_parser(
        "unread-all", help="全プロファイルの未読メッセージ一覧"
    )
    unread_all_parser.add_argument("--max", type=int, default=20, help="各プロファイルの最大取得件数")

    # mark-read-all サブコマンド（全プロファイル）
    subparsers.add_parser("mark-read-all", help="全プロファイルの未読を既読化")

    # send サブコマンド
    send_parser = subparsers.add_parser("send", help="メールを送信")
    send_parser.add_argument("--to", required=True, help="宛先メールアドレス")
    send_parser.add_argument("--subject", required=True, help="件名")
    send_parser.add_argument("--body", required=True, help="本文")
    send_parser.add_argument("--cc", help="CC（カンマ区切り）")
    send_parser.add_argument("--bcc", help="BCC（カンマ区切り）")
    send_parser.add_argument("--html", action="store_true", help="HTMLメールとして送信")

    # draft サブコマンド
    draft_parser = subparsers.add_parser("draft", help="下書きを作成")
    draft_parser.add_argument("--to", required=True, help="宛先メールアドレス")
    draft_parser.add_argument("--subject", required=True, help="件名")
    draft_parser.add_argument("--body", required=True, help="本文")
    draft_parser.add_argument("--cc", help="CC（カンマ区切り）")
    draft_parser.add_argument("--bcc", help="BCC（カンマ区切り）")
    draft_parser.add_argument("--html", action="store_true", help="HTMLメールとして送信")

    args = parser.parse_args()

    # トークンパスの決定
    if args.token:
        token_path = args.token
    else:
        token_path = get_token_path()

    headers = ["id", "subject", "from", "date"]

    if args.command == "unread":
        items = list_unread(token_path, args.max)
        format_output(items, headers, args.format)

    elif args.command == "starred":
        items = list_starred(token_path, args.max)
        format_output(items, headers, args.format)

    elif args.command == "read":
        content = read_message(token_path, args.id)
        print(content)

    elif args.command == "mark-read":
        if args.all:
            # 全未読を取得して既読化
            service = _get_service(token_path)
            message_ids = _fetch_all_message_ids(service, "is:unread", max_results=None)
            count = mark_read(token_path, message_ids)
            print(f"{count} 件のメッセージを既読にしました。")
        elif args.ids:
            count = mark_read(token_path, args.ids)
            print(f"{count} 件のメッセージを既読にしました。")
        else:
            print_error("--ids または --all を指定してください。")
            sys.exit(1)

    elif args.command == "star":
        if args.remove:
            count = unstar_messages(token_path, args.ids)
            print(f"{count} 件のメッセージのスターを外しました。")
        else:
            count = star_messages(token_path, args.ids)
            print(f"{count} 件のメッセージにスターを付けました。")

    elif args.command == "unread-all":
        results = list_unread_all_profiles(args.max)
        if args.format == "json":
            format_output(results, output_format="json")
        else:
            for profile, items in results.items():
                print(f"\n=== {profile} ===")
                if isinstance(items, dict) and "error" in items:
                    print(f"エラー: {items['error']}")
                elif items:
                    format_output(items, headers, "table")
                else:
                    print("未読メッセージはありません。")

    elif args.command == "mark-read-all":
        results = mark_read_all_profiles()
        if args.format == "json":
            format_output(results, output_format="json")
        else:
            for profile, result in results.items():
                if "error" in result:
                    print(f"{profile}: エラー - {result['error']}")
                else:
                    print(f"{profile}: {result['count']} 件を既読にしました。")

    elif args.command == "send":
        result = send_message(
            token_path,
            args.to,
            args.subject,
            args.body,
            cc=args.cc,
            bcc=args.bcc,
            html=args.html,
        )
        if args.format == "json":
            format_output(result, output_format="json")
        else:
            print("メールを送信しました。")
            print(f"  宛先: {result['to']}")
            print(f"  件名: {result['subject']}")
            print(f"  メッセージID: {result['id']}")
            print(f"  URL: {result['url']}")

    elif args.command == "draft":
        result = create_draft(
            token_path,
            args.to,
            args.subject,
            args.body,
            cc=args.cc,
            bcc=args.bcc,
            html=args.html,
        )
        if args.format == "json":
            format_output(result, output_format="json")
        else:
            print("下書きを作成しました。")
            print(f"  宛先: {result['to']}")
            print(f"  件名: {result['subject']}")
            print(f"  下書きID: {result['id']}")
            print(f"  URL: {result['url']}")


if __name__ == "__main__":
    main()
