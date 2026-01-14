#!/usr/bin/env python3
"""Slack メッセージ送信スクリプト。

チャンネルにメッセージを投稿します。
User Token（SLACK_USER_TOKEN）が設定されている場合はユーザーとして投稿し、
設定されていない場合は Bot として投稿します。
"""

import argparse
import sys

from slack_utils import (
    get_effective_client,
    get_slack_client,
    handle_api_error,
    has_user_token,
    print_error,
    print_json,
)


@handle_api_error
def post_message(
    channel_id: str,
    text: str,
    as_user: bool = True,
) -> None:
    """メッセージを投稿する。

    Args:
        channel_id: チャンネルID
        text: メッセージテキスト
        as_user: ユーザーとして投稿するか（User Token がある場合のみ有効）
    """
    # ユーザートークンがあり、as_user が True の場合はユーザーとして投稿
    client, is_user = get_effective_client(prefer_user=as_user)

    result = client.chat_postMessage(
        channel=channel_id,
        text=text,
    )

    message = result["message"]
    channel = result["channel"]

    if is_user:
        print("ユーザーとしてメッセージを送信しました。")
    else:
        print("Bot としてメッセージを送信しました。")
    print("")
    print(f"  チャンネル: {channel}")
    print(f"  タイムスタンプ: {message.get('ts', '')}")
    print(f"  テキスト: {message.get('text', '')[:50]}...")


@handle_api_error
def post_message_as_bot(channel_id: str, text: str) -> None:
    """Bot としてメッセージを投稿する。

    Args:
        channel_id: チャンネルID
        text: メッセージテキスト
    """
    client = get_slack_client()

    result = client.chat_postMessage(
        channel=channel_id,
        text=text,
    )

    message = result["message"]
    channel = result["channel"]

    print("Bot としてメッセージを送信しました。")
    print("")
    print(f"  チャンネル: {channel}")
    print(f"  タイムスタンプ: {message.get('ts', '')}")
    print(f"  テキスト: {message.get('text', '')[:50]}...")


def check_token_status() -> None:
    """トークンの状態を確認して表示する。"""
    if has_user_token():
        print("User Token が設定されています。")
        print("デフォルトではユーザーとしてメッセージを投稿します。")
        print("")
        print("オプション:")
        print("  --as-bot    Bot として投稿する")
    else:
        print("User Token が設定されていません。")
        print("Bot としてメッセージを投稿します。")
        print("")
        print("ユーザーとして投稿するには SLACK_USER_TOKEN を設定してください。")
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
        description="Slack にメッセージを投稿します"
    )
    subparsers = parser.add_subparsers(dest="command", help="コマンド")

    # post コマンド
    post_parser = subparsers.add_parser("post", help="メッセージを投稿")
    post_parser.add_argument(
        "--channel",
        "-c",
        required=True,
        help="チャンネルID",
    )
    post_parser.add_argument(
        "--text",
        "-t",
        required=True,
        help="メッセージテキスト",
    )
    post_parser.add_argument(
        "--as-bot",
        action="store_true",
        help="Bot として投稿する（User Token がある場合でも）",
    )

    # status コマンド
    subparsers.add_parser("status", help="トークンの状態を確認")

    args = parser.parse_args()

    if args.command == "post":
        # --as-bot が指定された場合は Bot として投稿
        if args.as_bot:
            post_message_as_bot(args.channel, args.text)
        else:
            post_message(args.channel, args.text, as_user=True)
    elif args.command == "status":
        check_token_status()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
