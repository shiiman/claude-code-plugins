#!/usr/bin/env python3
"""Slack スレッド返信スクリプト。

スレッドに返信を投稿します。
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
)


@handle_api_error
def reply_to_thread(
    channel_id: str,
    thread_ts: str,
    text: str,
) -> None:
    """スレッドに返信する。

    Args:
        channel_id: チャンネルID
        thread_ts: スレッドのタイムスタンプ（親メッセージのts）
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

    print("スレッドに返信しました。")
    print("")
    print(f"  チャンネル: {channel}")
    print(f"  スレッド: {thread_ts}")
    print(f"  タイムスタンプ: {message.get('ts', '')}")
    print(f"  テキスト: {message.get('text', '')[:50]}...")


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

    args = parser.parse_args()

    if args.command == "reply":
        reply_to_thread(args.channel, args.thread_ts, args.text)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
