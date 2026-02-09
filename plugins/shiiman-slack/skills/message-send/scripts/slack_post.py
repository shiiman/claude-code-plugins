#!/usr/bin/env python3
"""Slack メッセージ送信スクリプト。

チャンネルにメッセージを投稿します。
"""

import os
import sys
import argparse
# lib/ ディレクトリをパスに追加
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib")
sys.path.insert(0, lib_dir)

from slack_utils import (
    get_slack_client,
    handle_api_error,
    print_error,
    print_json,
)


@handle_api_error
def post_message(
    channel_id: str,
    text: str,
) -> None:
    """メッセージを投稿する。

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

    print("メッセージを送信しました。")
    print("")
    print(f"  チャンネル: {channel}")
    print(f"  タイムスタンプ: {message.get('ts', '')}")
    print(f"  テキスト: {message.get('text', '')[:50]}...")


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

    args = parser.parse_args()

    if args.command == "post":
        post_message(args.channel, args.text)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
