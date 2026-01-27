#!/usr/bin/env python3
"""Slack メッセージ操作スクリプト for shiiman-slack."""

import argparse
import sys
from typing import List, Dict, Optional

from slack_utils import (
    get_slack_client,
    handle_api_error,
    format_output,
    print_error,
    get_user_name,
    resolve_user_names,
)


@handle_api_error
def edit_message(channel: str, ts: str, text: str) -> None:
    """メッセージを編集する。
    
    Args:
        channel: チャンネルID
        ts: メッセージのタイムスタンプ
        text: 新しいメッセージテキスト
    """
    client = get_slack_client()
    result = client.chat_update(
        channel=channel,
        ts=ts,
        text=text,
    )
    print(f"メッセージを編集しました。")
    print(f"  チャンネル: {channel}")
    print(f"  タイムスタンプ: {result['ts']}")


@handle_api_error
def delete_message(channel: str, ts: str) -> None:
    """メッセージを削除する。
    
    Args:
        channel: チャンネルID
        ts: メッセージのタイムスタンプ
    """
    client = get_slack_client()
    client.chat_delete(
        channel=channel,
        ts=ts,
    )
    print(f"メッセージを削除しました。")
    print(f"  チャンネル: {channel}")
    print(f"  タイムスタンプ: {ts}")


@handle_api_error
def get_unread_messages(
    channel: str,
    max_results: int = 20,
    output_format: str = "table",
) -> None:
    """未読メッセージを取得する。
    
    Args:
        channel: チャンネルID
        max_results: 最大取得件数
        output_format: 出力形式 ("table" or "json")
    """
    client = get_slack_client()
    
    # チャンネル情報を取得（最終既読位置を含む）
    channel_info = client.conversations_info(channel=channel)
    last_read = channel_info["channel"].get("last_read")
    
    # メッセージ履歴を取得
    result = client.conversations_history(
        channel=channel,
        limit=max_results,
    )
    
    messages = result.get("messages", [])
    
    # 未読メッセージをフィルタ
    unread_messages = []
    for msg in messages:
        if not last_read or float(msg["ts"]) > float(last_read):
            unread_messages.append({
                "ts": msg["ts"],
                "user": msg.get("user", ""),
                "text": msg.get("text", ""),
            })
    
    # ユーザー名を解決
    unread_messages = resolve_user_names(client, unread_messages)
    
    if not unread_messages:
        print("未読メッセージはありません。")
        return
    
    print(f"未読メッセージ数: {len(unread_messages)}")
    headers = ["ts", "user_name", "text"]
    format_output(unread_messages, headers, output_format)


@handle_api_error
def mark_as_read(channel: str) -> None:
    """チャンネルを既読にする。
    
    Args:
        channel: チャンネルID
    """
    client = get_slack_client()
    
    # 最新メッセージのタイムスタンプを取得
    result = client.conversations_history(
        channel=channel,
        limit=1,
    )
    
    messages = result.get("messages", [])
    if not messages:
        print("メッセージがありません。")
        return
    
    latest_ts = messages[0]["ts"]
    
    # 既読マークを設定
    client.conversations_mark(
        channel=channel,
        ts=latest_ts,
    )
    
    print(f"チャンネルを既読にしました。")
    print(f"  チャンネル: {channel}")


@handle_api_error
def get_mentions(
    max_results: int = 20,
    output_format: str = "table",
) -> None:
    """自分へのメンションを取得する。
    
    Args:
        max_results: 最大取得件数
        output_format: 出力形式 ("table" or "json")
    """
    client = get_slack_client()
    
    # 自分のユーザーIDを取得
    auth_result = client.auth_test()
    user_id = auth_result["user_id"]
    
    # メンションを検索
    result = client.search_messages(
        query=f"<@{user_id}>",
        count=max_results,
    )
    
    matches = result.get("messages", {}).get("matches", [])
    
    if not matches:
        print("メンションはありません。")
        return
    
    mentions = []
    for match in matches:
        mentions.append({
            "channel": match.get("channel", {}).get("name", ""),
            "user": match.get("username", ""),
            "text": match.get("text", ""),
            "ts": match.get("ts", ""),
            "permalink": match.get("permalink", ""),
        })
    
    print(f"メンション数: {len(mentions)}")
    headers = ["channel", "user", "text", "permalink"]
    format_output(mentions, headers, output_format)


@handle_api_error
def get_thread_users(
    channel: str,
    thread_ts: str,
    output_format: str = "table",
) -> None:
    """スレッドの参加者一覧を取得する。
    
    Args:
        channel: チャンネルID
        thread_ts: スレッドのタイムスタンプ
        output_format: 出力形式 ("table" or "json")
    """
    client = get_slack_client()
    
    # スレッドの返信を取得
    result = client.conversations_replies(
        channel=channel,
        ts=thread_ts,
    )
    
    messages = result.get("messages", [])
    
    # ユーザーIDを収集
    user_ids = set()
    for msg in messages:
        if "user" in msg:
            user_ids.add(msg["user"])
    
    # ユーザー情報を取得
    users = []
    for user_id in user_ids:
        user_name = get_user_name(client, user_id)
        users.append({
            "user_id": user_id,
            "user_name": user_name,
        })
    
    print(f"スレッド参加者数: {len(users)}")
    headers = ["user_id", "user_name"]
    format_output(users, headers, output_format)


@handle_api_error
def summarize_messages(
    channel: str,
    thread_ts: Optional[str] = None,
    max_results: int = 50,
    output_format: str = "json",
) -> None:
    """メッセージを要約用に取得する（ユーザー名解決済み）。
    
    Args:
        channel: チャンネルID
        thread_ts: スレッドのタイムスタンプ（指定時はスレッド要約）
        max_results: 最大取得件数
        output_format: 出力形式 ("table" or "json")
    """
    client = get_slack_client()
    
    if thread_ts:
        # スレッド返信を取得
        result = client.conversations_replies(
            channel=channel,
            ts=thread_ts,
            limit=max_results,
        )
    else:
        # チャンネル履歴を取得
        result = client.conversations_history(
            channel=channel,
            limit=max_results,
        )
    
    messages = result.get("messages", [])
    
    # メッセージを整形
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "user": msg.get("user", ""),
            "text": msg.get("text", ""),
            "ts": msg["ts"],
        })
    
    # ユーザー名を解決
    formatted_messages = resolve_user_names(client, formatted_messages)
    
    # 要約用に整形
    summary_data = []
    for msg in formatted_messages:
        summary_data.append({
            "user": msg.get("user_name", msg.get("user", "")),
            "text": msg.get("text", ""),
            "ts": msg["ts"],
        })
    
    if output_format == "json":
        format_output(summary_data, output_format="json")
    else:
        # テーブル形式の場合
        headers = ["user", "text", "ts"]
        format_output(summary_data, headers, output_format)


@handle_api_error
def main() -> None:
    parser = argparse.ArgumentParser(description="Slack メッセージ操作ツール")
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="出力形式 (デフォルト: table)",
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # edit サブコマンド
    edit_parser = subparsers.add_parser("edit", help="メッセージ編集")
    edit_parser.add_argument("--channel", required=True, help="チャンネルID")
    edit_parser.add_argument("--ts", required=True, help="メッセージのタイムスタンプ")
    edit_parser.add_argument("--text", required=True, help="新しいメッセージテキスト")
    
    # delete サブコマンド
    delete_parser = subparsers.add_parser("delete", help="メッセージ削除")
    delete_parser.add_argument("--channel", required=True, help="チャンネルID")
    delete_parser.add_argument("--ts", required=True, help="メッセージのタイムスタンプ")
    
    # unread サブコマンド
    unread_parser = subparsers.add_parser("unread", help="未読メッセージ一覧")
    unread_parser.add_argument("--channel", required=True, help="チャンネルID")
    unread_parser.add_argument("--max", type=int, default=20, help="最大取得件数")
    
    # mark-read サブコマンド
    mark_parser = subparsers.add_parser("mark-read", help="既読化")
    mark_parser.add_argument("--channel", required=True, help="チャンネルID")
    
    # mentions サブコマンド
    mentions_parser = subparsers.add_parser("mentions", help="メンション一覧")
    mentions_parser.add_argument("--max", type=int, default=20, help="最大取得件数")
    
    # thread-users サブコマンド
    thread_users_parser = subparsers.add_parser("thread-users", help="スレッド参加者一覧")
    thread_users_parser.add_argument("--channel", required=True, help="チャンネルID")
    thread_users_parser.add_argument("--ts", required=True, help="スレッドのタイムスタンプ")
    
    # summarize サブコマンド
    summarize_parser = subparsers.add_parser("summarize", help="要約用メッセージ取得")
    summarize_parser.add_argument("--channel", required=True, help="チャンネルID")
    summarize_parser.add_argument("--ts", help="スレッドのタイムスタンプ（スレッド要約時）")
    summarize_parser.add_argument("--max", type=int, default=50, help="最大取得件数")
    
    args = parser.parse_args()
    
    if args.command == "edit":
        edit_message(args.channel, args.ts, args.text)
    
    elif args.command == "delete":
        delete_message(args.channel, args.ts)
    
    elif args.command == "unread":
        get_unread_messages(args.channel, args.max, args.format)
    
    elif args.command == "mark-read":
        mark_as_read(args.channel)
    
    elif args.command == "mentions":
        get_mentions(args.max, args.format)
    
    elif args.command == "thread-users":
        get_thread_users(args.channel, args.ts, args.format)
    
    elif args.command == "summarize":
        summarize_messages(args.channel, args.ts, args.max, args.format)


if __name__ == "__main__":
    main()
