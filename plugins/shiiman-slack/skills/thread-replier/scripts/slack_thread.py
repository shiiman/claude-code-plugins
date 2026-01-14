#!/usr/bin/env python3
"""Slack スレッド返信スクリプト。

スレッドに返信を投稿します。
User Token（SLACK_USER_TOKEN）が設定されている場合はユーザーとして返信し、
設定されていない場合は Bot として返信します。
"""

import argparse
import sys

from slack_utils import (
    get_effective_client,
    get_slack_client,
    handle_api_error,
    has_user_token,
    print_error,
)


@handle_api_error
def reply_to_thread(
    channel_id: str,
    thread_ts: str,
    text: str,
    as_user: bool = True,
) -> None:
    """スレッドに返信する。

    Args:
        channel_id: チャンネルID
        thread_ts: スレッドのタイムスタンプ（親メッセージのts）
        text: 返信テキスト
        as_user: ユーザーとして返信するか（User Token がある場合のみ有効）
    """
    # ユーザートークンがあり、as_user が True の場合はユーザーとして返信
    client, is_user = get_effective_client(prefer_user=as_user)

    result = client.chat_postMessage(
        channel=channel_id,
        thread_ts=thread_ts,
        text=text,
    )

    message = result["message"]
    channel = result["channel"]

    if is_user:
        print("ユーザーとしてスレッドに返信しました。")
    else:
        print("Bot としてスレッドに返信しました。")
    print("")
    print(f"  チャンネル: {channel}")
    print(f"  スレッド: {thread_ts}")
    print(f"  タイムスタンプ: {message.get('ts', '')}")
    print(f"  テキスト: {message.get('text', '')[:50]}...")


@handle_api_error
def reply_to_thread_as_bot(channel_id: str, thread_ts: str, text: str) -> None:
    """Bot としてスレッドに返信する。

    Args:
        channel_id: チャンネルID
        thread_ts: スレッドのタイムスタンプ
        text: 返信テキスト
    """
    client = get_slack_client()

    result = client.chat_postMessage(
        channel=channel_id,
        thread_ts=thread_ts,
        text=text,
    )

    message = result["message"]
    channel = result["channel"]

    print("Bot としてスレッドに返信しました。")
    print("")
    print(f"  チャンネル: {channel}")
    print(f"  スレッド: {thread_ts}")
    print(f"  タイムスタンプ: {message.get('ts', '')}")
    print(f"  テキスト: {message.get('text', '')[:50]}...")


def check_token_status() -> None:
    """トークンの状態を確認して表示する。"""
    if has_user_token():
        print("User Token が設定されています。")
        print("デフォルトではユーザーとしてスレッドに返信します。")
        print("")
        print("オプション:")
        print("  --as-bot    Bot として返信する")
    else:
        print("User Token が設定されていません。")
        print("Bot としてスレッドに返信します。")
        print("")
        print("ユーザーとして返信するには SLACK_USER_TOKEN を設定してください。")
        print("")
        print("設定例（.claude/settings.local.json）:")
        print('  "mcpServers": {')
        print('    "slack": {')
        print('      "env": {')
        print('        "SLACK_USER_TOKEN": "xoxp-your-user-token"')
        print('      }')
        print('    }')
        print('  }')


def main() -> None:
    """メイン関数。"""
    parser = argparse.ArgumentParser(
        description="Slack スレッドに返信します"
    )
    subparsers = parser.add_subparsers(dest="command", help="コマンド")

    # reply コマンド
    reply_parser = subparsers.add_parser("reply", help="スレッドに返信")
    reply_parser.add_argument(
        "--channel",
        "-c",
        required=True,
        help="チャンネルID",
    )
    reply_parser.add_argument(
        "--thread-ts",
        "-t",
        required=True,
        help="スレッドのタイムスタンプ（親メッセージのts）",
    )
    reply_parser.add_argument(
        "--text",
        "-m",
        required=True,
        help="返信テキスト",
    )
    reply_parser.add_argument(
        "--as-bot",
        action="store_true",
        help="Bot として返信する（User Token がある場合でも）",
    )

    # status コマンド
    subparsers.add_parser("status", help="トークンの状態を確認")

    args = parser.parse_args()

    if args.command == "reply":
        # --as-bot が指定された場合は Bot として返信
        if args.as_bot:
            reply_to_thread_as_bot(args.channel, args.thread_ts, args.text)
        else:
            reply_to_thread(args.channel, args.thread_ts, args.text, as_user=True)
    elif args.command == "status":
        check_token_status()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
