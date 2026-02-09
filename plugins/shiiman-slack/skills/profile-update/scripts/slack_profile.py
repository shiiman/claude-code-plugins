#!/usr/bin/env python3
"""Slack プロフィール管理スクリプト。

プロフィールの表示・更新を行います。
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
def show_profile() -> None:
    """現在のプロフィールを表示する。"""
    client = get_slack_client()
    result = client.users_profile_get()
    profile = result["profile"]

    print("現在のプロフィール:")
    print("")
    print(f"  表示名: {profile.get('display_name', '未設定')}")
    print(f"  本名: {profile.get('real_name', '未設定')}")
    print(f"  名: {profile.get('first_name', '未設定')}")
    print(f"  姓: {profile.get('last_name', '未設定')}")
    print(f"  役職: {profile.get('title', '未設定')}")
    print(f"  電話番号: {profile.get('phone', '未設定')}")
    print("")
    print("ステータス:")
    status_text = profile.get("status_text", "")
    status_emoji = profile.get("status_emoji", "")
    if status_text or status_emoji:
        print(f"  テキスト: {status_text or '(なし)'}")
        print(f"  絵文字: {status_emoji or '(なし)'}")
    else:
        print("  (ステータスは設定されていません)")


@handle_api_error
def update_profile(
    display_name: str = None,
    status_text: str = None,
    status_emoji: str = None,
    title: str = None,
    phone: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
    """プロフィールを更新する。

    Args:
        display_name: 表示名
        status_text: ステータステキスト
        status_emoji: ステータス絵文字
        title: 役職
        phone: 電話番号
        first_name: 名
        last_name: 姓
    """
    # 更新するフィールドを収集
    profile = {}
    if display_name is not None:
        profile["display_name"] = display_name
    if status_text is not None:
        profile["status_text"] = status_text
    if status_emoji is not None:
        profile["status_emoji"] = status_emoji
    if title is not None:
        profile["title"] = title
    if phone is not None:
        profile["phone"] = phone
    if first_name is not None:
        profile["first_name"] = first_name
    if last_name is not None:
        profile["last_name"] = last_name

    if not profile:
        print_error("更新するフィールドが指定されていません。")
        print("使用例:")
        print("  --display-name '新しい表示名'")
        print("  --status-text '会議中' --status-emoji ':calendar:'")
        sys.exit(1)

    client = get_slack_client()
    result = client.users_profile_set(profile=profile)
    updated_profile = result["profile"]

    print("プロフィールを更新しました。")
    print("")
    print("更新後のプロフィール:")
    if "display_name" in profile:
        print(f"  表示名: {updated_profile.get('display_name', '')}")
    if "status_text" in profile or "status_emoji" in profile:
        print(f"  ステータス: {updated_profile.get('status_emoji', '')} {updated_profile.get('status_text', '')}")
    if "title" in profile:
        print(f"  役職: {updated_profile.get('title', '')}")
    if "phone" in profile:
        print(f"  電話番号: {updated_profile.get('phone', '')}")
    if "first_name" in profile:
        print(f"  名: {updated_profile.get('first_name', '')}")
    if "last_name" in profile:
        print(f"  姓: {updated_profile.get('last_name', '')}")


@handle_api_error
def clear_status() -> None:
    """ステータスをクリアする。"""
    client = get_slack_client()
    client.users_profile_set(profile={
        "status_text": "",
        "status_emoji": "",
    })

    print("ステータスをクリアしました。")


def main() -> None:
    """メイン関数。"""
    parser = argparse.ArgumentParser(
        description="Slack プロフィールを管理します"
    )
    subparsers = parser.add_subparsers(dest="command", help="コマンド")

    # show コマンド
    subparsers.add_parser("show", help="現在のプロフィールを表示")

    # update コマンド
    update_parser = subparsers.add_parser("update", help="プロフィールを更新")
    update_parser.add_argument(
        "--display-name",
        help="表示名",
    )
    update_parser.add_argument(
        "--status-text",
        help="ステータステキスト",
    )
    update_parser.add_argument(
        "--status-emoji",
        help="ステータス絵文字（例: :calendar:）",
    )
    update_parser.add_argument(
        "--title",
        help="役職",
    )
    update_parser.add_argument(
        "--phone",
        help="電話番号",
    )
    update_parser.add_argument(
        "--first-name",
        help="名",
    )
    update_parser.add_argument(
        "--last-name",
        help="姓",
    )

    # clear-status コマンド
    subparsers.add_parser("clear-status", help="ステータスをクリア")

    # json コマンド（デバッグ用）
    subparsers.add_parser("json", help="プロフィールを JSON 形式で表示")

    args = parser.parse_args()

    if args.command == "show":
        show_profile()
    elif args.command == "update":
        update_profile(
            display_name=args.display_name,
            status_text=args.status_text,
            status_emoji=args.status_emoji,
            title=args.title,
            phone=args.phone,
            first_name=args.first_name,
            last_name=args.last_name,
        )
    elif args.command == "clear-status":
        clear_status()
    elif args.command == "json":
        client = get_slack_client()
        result = client.users_profile_get()
        print_json(result["profile"])
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
