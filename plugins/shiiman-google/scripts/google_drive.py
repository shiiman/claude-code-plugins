"""Drive list, search, move, and folder operations for shiiman-google."""

import argparse
from typing import List, Optional

from googleapiclient.discovery import build

from google_utils import (
    format_output,
    get_token_path,
    handle_api_error,
    load_credentials,
    print_json,
)

DEFAULT_SCOPES = ["https://www.googleapis.com/auth/drive"]


def _get_service(token_path: str):
    """Drive サービスを取得する。"""
    creds = load_credentials(token_path, DEFAULT_SCOPES)
    return build("drive", "v3", credentials=creds)


def list_files(token_path: str, page_size: int = 50) -> List[dict]:
    """ファイル一覧を取得する。"""
    service = _get_service(token_path)
    results = (
        service.files()
        .list(
            pageSize=page_size,
            fields="files(id,name,mimeType,modifiedTime,webViewLink)",
            orderBy="modifiedTime desc",
        )
        .execute()
    )
    return results.get("files", [])


def search_files(token_path: str, query: str, page_size: int = 50) -> List[dict]:
    """ファイルを検索する。"""
    service = _get_service(token_path)
    results = (
        service.files()
        .list(
            q=query,
            pageSize=page_size,
            fields="files(id,name,mimeType,modifiedTime,webViewLink)",
            orderBy="modifiedTime desc",
        )
        .execute()
    )
    return results.get("files", [])


def move_file(
    token_path: str,
    file_id: str,
    destination_folder_id: str,
) -> dict:
    """ファイルを別のフォルダに移動する。

    Args:
        token_path: トークンファイルパス
        file_id: 移動するファイルのID
        destination_folder_id: 移動先フォルダのID

    Returns:
        更新されたファイル情報
    """
    service = _get_service(token_path)

    # 現在の親フォルダを取得
    file = service.files().get(fileId=file_id, fields="parents").execute()
    previous_parents = ",".join(file.get("parents", []))

    # 移動を実行
    result = (
        service.files()
        .update(
            fileId=file_id,
            addParents=destination_folder_id,
            removeParents=previous_parents,
            fields="id,name,parents,webViewLink",
        )
        .execute()
    )
    return result


def create_folder(
    token_path: str,
    name: str,
    parent_folder_id: Optional[str] = None,
) -> dict:
    """フォルダを作成する。

    Args:
        token_path: トークンファイルパス
        name: フォルダ名
        parent_folder_id: 親フォルダのID（省略時はマイドライブ直下）

    Returns:
        作成されたフォルダ情報
    """
    service = _get_service(token_path)

    file_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }

    if parent_folder_id:
        file_metadata["parents"] = [parent_folder_id]

    result = (
        service.files()
        .create(body=file_metadata, fields="id,name,webViewLink")
        .execute()
    )
    return result


def copy_file(
    token_path: str,
    file_id: str,
    new_name: Optional[str] = None,
    destination_folder_id: Optional[str] = None,
) -> dict:
    """ファイルをコピーする。

    Args:
        token_path: トークンファイルパス
        file_id: コピー元ファイルのID
        new_name: 新しいファイル名（省略時は元のファイル名 + " のコピー"）
        destination_folder_id: コピー先フォルダのID（省略時は元と同じフォルダ）

    Returns:
        コピーされたファイル情報
    """
    service = _get_service(token_path)

    file_metadata = {}
    if new_name:
        file_metadata["name"] = new_name
    if destination_folder_id:
        file_metadata["parents"] = [destination_folder_id]

    result = (
        service.files()
        .copy(fileId=file_id, body=file_metadata, fields="id,name,webViewLink")
        .execute()
    )
    return result


def share_file(
    token_path: str,
    file_id: str,
    email: Optional[str] = None,
    role: str = "reader",
    share_type: str = "user",
    send_notification: bool = True,
) -> dict:
    """ファイルを共有する。

    Args:
        token_path: トークンファイルパス
        file_id: ファイルID
        email: 共有先メールアドレス（share_typeがuser/groupの場合必須）
        role: 権限（reader=閲覧, writer=編集, commenter=コメント）
        share_type: 共有タイプ（user=個人, group=グループ, anyone=リンク共有）
        send_notification: 共有通知メールを送信するか

    Returns:
        作成されたパーミッション情報
    """
    service = _get_service(token_path)

    permission = {
        "role": role,
        "type": share_type,
    }

    if share_type in ("user", "group"):
        if not email:
            raise ValueError(f"{share_type}タイプの共有にはメールアドレスが必要です")
        permission["emailAddress"] = email

    result = (
        service.permissions()
        .create(
            fileId=file_id,
            body=permission,
            sendNotificationEmail=send_notification,
            fields="id,type,role,emailAddress",
        )
        .execute()
    )

    # ファイル情報も取得して共有リンクを返す
    file_info = (
        service.files()
        .get(fileId=file_id, fields="name,webViewLink")
        .execute()
    )

    return {
        "permissionId": result.get("id"),
        "type": result.get("type"),
        "role": result.get("role"),
        "emailAddress": result.get("emailAddress", ""),
        "fileName": file_info.get("name"),
        "fileUrl": file_info.get("webViewLink"),
    }


def unshare_file(
    token_path: str,
    file_id: str,
    permission_id: Optional[str] = None,
    email: Optional[str] = None,
) -> dict:
    """ファイルの共有を解除する。

    Args:
        token_path: トークンファイルパス
        file_id: ファイルID
        permission_id: 解除するパーミッションID（優先）
        email: 解除するメールアドレス（permission_idがない場合に使用）

    Returns:
        削除結果
    """
    service = _get_service(token_path)

    # permission_idが指定されていない場合、emailから検索
    if not permission_id and email:
        permissions = get_permissions(token_path, file_id)
        for perm in permissions:
            if perm.get("emailAddress") == email:
                permission_id = perm.get("id")
                break

    if not permission_id:
        raise ValueError("permission_id または email を指定してください")

    service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()

    return {
        "status": "deleted",
        "fileId": file_id,
        "permissionId": permission_id,
    }


def get_permissions(
    token_path: str,
    file_id: str,
) -> List[dict]:
    """ファイルの共有設定一覧を取得する。

    Args:
        token_path: トークンファイルパス
        file_id: ファイルID

    Returns:
        パーミッション情報のリスト
    """
    service = _get_service(token_path)

    # ファイル情報を取得
    file_info = (
        service.files()
        .get(fileId=file_id, fields="name,webViewLink")
        .execute()
    )

    # パーミッション一覧を取得
    result = (
        service.permissions()
        .list(
            fileId=file_id,
            fields="permissions(id,type,role,emailAddress,displayName)",
        )
        .execute()
    )

    permissions = []
    for perm in result.get("permissions", []):
        permissions.append({
            "id": perm.get("id"),
            "type": perm.get("type"),
            "role": perm.get("role"),
            "emailAddress": perm.get("emailAddress", ""),
            "displayName": perm.get("displayName", ""),
        })

    return {
        "fileName": file_info.get("name"),
        "fileUrl": file_info.get("webViewLink"),
        "permissions": permissions,
    }


@handle_api_error
def main() -> None:
    parser = argparse.ArgumentParser(description="Google Drive 操作ツール")
    parser.add_argument("--token", help="トークンファイルパス")
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="出力形式 (デフォルト: table)",
    )

    subparsers = parser.add_subparsers(dest="command")

    # list サブコマンド
    list_parser = subparsers.add_parser("list", help="ファイル一覧")
    list_parser.add_argument("--page-size", type=int, default=50, help="取得件数")

    # search サブコマンド
    search_parser = subparsers.add_parser("search", help="ファイル検索")
    search_parser.add_argument("--query", required=True, help="検索クエリ")
    search_parser.add_argument("--page-size", type=int, default=50, help="取得件数")

    # move サブコマンド
    move_parser = subparsers.add_parser("move", help="ファイル移動")
    move_parser.add_argument("--file-id", required=True, help="ファイルID")
    move_parser.add_argument("--destination", required=True, help="移動先フォルダID")

    # create-folder サブコマンド
    folder_parser = subparsers.add_parser("create-folder", help="フォルダ作成")
    folder_parser.add_argument("--name", required=True, help="フォルダ名")
    folder_parser.add_argument("--parent", help="親フォルダID")

    # copy サブコマンド
    copy_parser = subparsers.add_parser("copy", help="ファイルコピー")
    copy_parser.add_argument("--file-id", required=True, help="ファイルID")
    copy_parser.add_argument("--name", help="新しいファイル名")
    copy_parser.add_argument("--destination", help="コピー先フォルダID")

    # share サブコマンド
    share_parser = subparsers.add_parser("share", help="ファイル共有")
    share_parser.add_argument("--file-id", required=True, help="ファイルID")
    share_parser.add_argument("--email", help="共有先メールアドレス")
    share_parser.add_argument(
        "--role",
        choices=["reader", "writer", "commenter"],
        default="reader",
        help="権限（reader=閲覧, writer=編集, commenter=コメント）",
    )
    share_parser.add_argument(
        "--type",
        choices=["user", "group", "anyone"],
        default="user",
        help="共有タイプ（user=個人, group=グループ, anyone=リンク共有）",
    )
    share_parser.add_argument(
        "--no-notify",
        action="store_true",
        help="共有通知メールを送信しない",
    )

    # unshare サブコマンド
    unshare_parser = subparsers.add_parser("unshare", help="共有解除")
    unshare_parser.add_argument("--file-id", required=True, help="ファイルID")
    unshare_parser.add_argument("--permission-id", help="パーミッションID")
    unshare_parser.add_argument("--email", help="解除するメールアドレス")

    # permissions サブコマンド
    permissions_parser = subparsers.add_parser("permissions", help="共有設定確認")
    permissions_parser.add_argument("--file-id", required=True, help="ファイルID")

    args = parser.parse_args()

    # トークンパスの決定
    if args.token:
        token_path = args.token
    else:
        token_path = get_token_path()

    headers = ["name", "mimeType", "modifiedTime", "webViewLink"]

    # デフォルト: list コマンド（後方互換性のため）
    if args.command is None:
        # 旧形式: --query オプションで検索
        legacy_parser = argparse.ArgumentParser()
        legacy_parser.add_argument("--token")
        legacy_parser.add_argument("--page-size", type=int, default=50)
        legacy_parser.add_argument("--query")
        legacy_parser.add_argument("--format", default="table")
        legacy_args, _ = legacy_parser.parse_known_args()

        if legacy_args.query:
            items = search_files(
                token_path, legacy_args.query, legacy_args.page_size
            )
        else:
            items = list_files(token_path, legacy_args.page_size)
        format_output(items, headers, legacy_args.format)
        return

    if args.command == "list":
        items = list_files(token_path, args.page_size)
        format_output(items, headers, args.format)

    elif args.command == "search":
        items = search_files(token_path, args.query, args.page_size)
        format_output(items, headers, args.format)

    elif args.command == "move":
        result = move_file(token_path, args.file_id, args.destination)
        print(f"ファイルを移動しました: {result.get('name')}")
        print(f"URL: {result.get('webViewLink')}")

    elif args.command == "create-folder":
        result = create_folder(token_path, args.name, args.parent)
        print(f"フォルダを作成しました: {result.get('name')}")
        print(f"ID: {result.get('id')}")
        print(f"URL: {result.get('webViewLink')}")

    elif args.command == "copy":
        result = copy_file(token_path, args.file_id, args.name, args.destination)
        print(f"ファイルをコピーしました: {result.get('name')}")
        print(f"ID: {result.get('id')}")
        print(f"URL: {result.get('webViewLink')}")

    elif args.command == "share":
        result = share_file(
            token_path,
            args.file_id,
            args.email,
            args.role,
            args.type,
            not args.no_notify,
        )
        if args.format == "json":
            print_json([result])
        else:
            role_ja = {"reader": "閲覧", "writer": "編集", "commenter": "コメント"}
            type_ja = {"user": "ユーザー", "group": "グループ", "anyone": "リンク共有"}
            print(f"ファイルを共有しました:")
            print(f"  ファイル: {result.get('fileName')}")
            print(f"  共有タイプ: {type_ja.get(result.get('type'), result.get('type'))}")
            print(f"  権限: {role_ja.get(result.get('role'), result.get('role'))}")
            if result.get("emailAddress"):
                print(f"  共有先: {result.get('emailAddress')}")
            print(f"  URL: {result.get('fileUrl')}")

    elif args.command == "unshare":
        result = unshare_file(
            token_path,
            args.file_id,
            args.permission_id,
            args.email,
        )
        if args.format == "json":
            print_json([result])
        else:
            print(f"共有を解除しました:")
            print(f"  ファイルID: {result.get('fileId')}")
            print(f"  パーミッションID: {result.get('permissionId')}")

    elif args.command == "permissions":
        result = get_permissions(token_path, args.file_id)
        if args.format == "json":
            print_json([result])
        else:
            print(f"ファイル: {result.get('fileName')}")
            print(f"URL: {result.get('fileUrl')}")
            print(f"共有設定:")
            role_ja = {"owner": "オーナー", "reader": "閲覧", "writer": "編集", "commenter": "コメント"}
            type_ja = {"user": "ユーザー", "group": "グループ", "anyone": "リンク共有"}
            for perm in result.get("permissions", []):
                perm_type = type_ja.get(perm.get("type"), perm.get("type"))
                perm_role = role_ja.get(perm.get("role"), perm.get("role"))
                email = perm.get("emailAddress") or perm.get("displayName") or ""
                print(f"  - {perm_type}: {email} ({perm_role})")


if __name__ == "__main__":
    main()
