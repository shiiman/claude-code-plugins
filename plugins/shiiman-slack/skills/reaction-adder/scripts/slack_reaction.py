#!/usr/bin/env python3
"""Slack リアクション追加スクリプト。

メッセージにリアクション（絵文字）を追加します。
User Token（SLACK_USER_TOKEN）が設定されている場合はユーザーとしてリアクションし、
設定されていない場合は Bot としてリアクションします。
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
    as_user: bool = True,
) -> None:
    """メッセージにリアクションを追加する。

    Args:
        channel_id: チャンネルID
        timestamp: メッセージのタイムスタンプ
        emoji: 絵文字名（コロンなし）
        as_user: ユーザーとしてリアクションするか（User Token がある場合のみ有効）
    """
    emoji = normalize_emoji(emoji)

    # ユーザートークンがあり、as_user が True の場合はユーザーとしてリアクション
    client, is_user = get_effective_client(prefer_user=as_user)

    client.reactions_add(
        channel=channel_id,
        timestamp=timestamp,
        name=emoji,
    )

    emoji_display = COMMON_EMOJI.get(emoji, f":{emoji}:")

    if is_user:
        print(f"ユーザーとしてリアクション {emoji_display} を追加しました。")
    else:
        print(f"Bot としてリアクション {emoji_display} を追加しました。")
    print("")
    print(f"  チャンネル: {channel_id}")
    print(f"  メッセージ: {timestamp}")
    print(f"  絵文字: {emoji_display} (:{emoji}:)")


@handle_api_error
def add_reaction_as_bot(channel_id: str, timestamp: str, emoji: str) -> None:
    """Bot としてリアクションを追加する。

    Args:
        channel_id: チャンネルID
        timestamp: メッセージのタイムスタンプ
        emoji: 絵文字名
    """
    emoji = normalize_emoji(emoji)
    client = get_slack_client()

    client.reactions_add(
        channel=channel_id,
        timestamp=timestamp,
        name=emoji,
    )

    emoji_display = COMMON_EMOJI.get(emoji, f":{emoji}:")

    print(f"Bot としてリアクション {emoji_display} を追加しました。")
    print("")
    print(f"  チャンネル: {channel_id}")
    print(f"  メッセージ: {timestamp}")
    print(f"  絵文字: {emoji_display} (:{emoji}:)")


def check_token_status() -> None:
    """トークンの状態を確認して表示する。"""
    if has_user_token():
        print("User Token が設定されています。")
        print("デフォルトではユーザーとしてリアクションを追加します。")
        print("")
        print("オプション:")
        print("  --as-bot    Bot としてリアクションする")
    else:
        print("User Token が設定されていません。")
        print("Bot としてリアクションを追加します。")
        print("")
        print("ユーザーとしてリアクションするには SLACK_USER_TOKEN を設定してください。")
        print("")
        print("設定例（.claude/settings.local.json）:")
        print('  "mcpServers": {')
        print('    "slack": {')
        print('      "env": {')
        print('        "SLACK_USER_TOKEN": "xoxp-your-user-token"')
        print('      }')
        print('    }')
        print('  }')


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
    add_parser.add_argument(
        "--as-bot",
        action="store_true",
        help="Bot としてリアクション（User Token がある場合でも）",
    )

    # status コマンド
    subparsers.add_parser("status", help="トークンの状態を確認")

    # list コマンド
    subparsers.add_parser("list", help="よく使う絵文字の一覧を表示")

    args = parser.parse_args()

    if args.command == "add":
        # --as-bot が指定された場合は Bot としてリアクション
        if args.as_bot:
            add_reaction_as_bot(args.channel, args.timestamp, args.emoji)
        else:
            add_reaction(args.channel, args.timestamp, args.emoji, as_user=True)
    elif args.command == "status":
        check_token_status()
    elif args.command == "list":
        list_common_emoji()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
