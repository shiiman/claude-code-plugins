#!/usr/bin/env python3
"""Slack リアクション追加スクリプト。

メッセージにリアクション（絵文字）を追加します。
"""

import os
import sys
import argparse
# lib/ ディレクトリをパスに追加
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib")
sys.path.insert(0, lib_dir)

from slack_utils import (
    get_slack_client,
    handle_api_error,
)


# よく使う絵文字のマッピング
COMMON_EMOJI = {
    "thumbsup": "👍",
    "+1": "👍",
    "heart": "❤️",
    "eyes": "👀",
    "fire": "🔥",
    "100": "💯",
    "tada": "🎉",
    "rocket": "🚀",
    "white_check_mark": "✅",
    "x": "❌",
    "thinking_face": "🤔",
    "raised_hands": "🙌",
    "clap": "👏",
    "pray": "🙏",
    "sparkles": "✨",
}


def normalize_emoji(emoji: str) -> str:
    """絵文字名を正規化する（コロンを削除）。

    Args:
        emoji: 絵文字名（:thumbsup: または thumbsup）

    Returns:
        正規化された絵文字名（thumbsup）
    """
    return emoji.strip().strip(":")


@handle_api_error
def add_reaction(
    channel_id: str,
    timestamp: str,
    emoji: str,
) -> None:
    """メッセージにリアクションを追加する。

    Args:
        channel_id: チャンネルID
        timestamp: メッセージのタイムスタンプ
        emoji: 絵文字名（コロンなし）
    """
    emoji = normalize_emoji(emoji)
    client = get_slack_client()

    client.reactions_add(
        channel=channel_id,
        timestamp=timestamp,
        name=emoji,
    )

    emoji_display = COMMON_EMOJI.get(emoji, f":{emoji}:")

    print(f"リアクション {emoji_display} を追加しました。")
    print("")
    print(f"  チャンネル: {channel_id}")
    print(f"  メッセージ: {timestamp}")
    print(f"  絵文字: {emoji_display} (:{emoji}:)")


def list_common_emoji() -> None:
    """よく使う絵文字の一覧を表示する。"""
    print("よく使う絵文字:")
    print("")
    for name, emoji in COMMON_EMOJI.items():
        print(f"  :{name}: - {emoji}")


def main() -> None:
    """メイン関数。"""
    parser = argparse.ArgumentParser(
        description="Slack メッセージにリアクションを追加します"
    )
    subparsers = parser.add_subparsers(dest="command", help="コマンド")

    # add コマンド
    add_parser = subparsers.add_parser("add", help="リアクションを追加")
    add_parser.add_argument(
        "--channel",
        "-c",
        required=True,
        help="チャンネルID",
    )
    add_parser.add_argument(
        "--timestamp",
        "-t",
        required=True,
        help="メッセージのタイムスタンプ",
    )
    add_parser.add_argument(
        "--emoji",
        "-e",
        required=True,
        help="絵文字名（例: thumbsup, :heart:）",
    )

    # list コマンド
    subparsers.add_parser("list", help="よく使う絵文字の一覧を表示")

    args = parser.parse_args()

    if args.command == "add":
        add_reaction(args.channel, args.timestamp, args.emoji)
    elif args.command == "list":
        list_common_emoji()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
