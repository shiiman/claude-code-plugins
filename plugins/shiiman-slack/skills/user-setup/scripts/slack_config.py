#!/usr/bin/env python3
"""Slack ユーザー設定管理スクリプト。

デフォルトユーザーIDの設定・表示・削除を行います。
"""

import argparse
import sys

from slack_utils import (
    CONFIG_FILE,
    get_default_user_id,
    get_slack_client,
    get_user_name,
    handle_api_error,
    load_config,
    print_error,
    print_json,
    save_config,
)


def validate_user_id(user_id: str) -> bool:
    """ユーザーID の形式を検証する。

    Args:
        user_id: 検証するユーザーID

    Returns:
        有効な形式の場合は True
    """
    # Slack ユーザーID は通常 U で始まる11文字程度
    if not user_id:
        return False
    if not user_id.startswith("U") and not user_id.startswith("W"):
        return False
    if len(user_id) < 9 or len(user_id) > 15:
        return False
    return True


@handle_api_error
def set_user(user_id: str) -> None:
    """デフォルトユーザーID を設定する。

    Args:
        user_id: 設定するユーザーID
    """
    # ユーザーID の形式チェック
    if not validate_user_id(user_id):
        print_error(
            f"無効なユーザーID形式です: {user_id}\n"
            "ユーザーID は U または W で始まる9〜15文字の文字列です。\n"
            "Slack でプロフィールを開き「メンバーIDをコピー」で確認できます。"
        )
        sys.exit(1)

    # Slack API でユーザーの存在を確認
    client = get_slack_client()
    try:
        result = client.users_info(user=user_id)
        user = result["user"]
        user_name = user.get("real_name") or user.get("name") or user_id
        team_id = user.get("team_id", "")

        # ワークスペース情報を取得
        team_name = ""
        try:
            team_result = client.team_info()
            team_name = team_result["team"]["name"]
        except Exception:
            pass

    except Exception as e:
        print_error(
            f"ユーザー {user_id} が見つかりません。\n"
            "ユーザーID が正しいか確認してください。"
        )
        sys.exit(1)

    # 設定を保存
    config = load_config()
    config["default_user_id"] = user_id
    config["workspace"] = {
        "team_id": team_id,
        "team_name": team_name,
    }
    save_config(config)

    print(f"デフォルトユーザーを設定しました。")
    print(f"")
    print(f"  ユーザーID: {user_id}")
    print(f"  ユーザー名: {user_name}")
    if team_name:
        print(f"  ワークスペース: {team_name}")
    print(f"")
    print(f"設定ファイル: {CONFIG_FILE}")


@handle_api_error
def show_config() -> None:
    """現在の設定を表示する。"""
    config = load_config()

    if not config:
        print("設定が見つかりません。")
        print("")
        print("ユーザーを設定するには:")
        print("  「自分を設定して U01234567」と指示してください。")
        return

    user_id = config.get("default_user_id")
    if not user_id:
        print("デフォルトユーザーが設定されていません。")
        print("")
        print("ユーザーを設定するには:")
        print("  「自分を設定して U01234567」と指示してください。")
        return

    # ユーザー名を取得
    client = get_slack_client()
    user_name = get_user_name(client, user_id)

    workspace = config.get("workspace", {})

    print("現在の設定:")
    print("")
    print(f"  デフォルトユーザーID: {user_id}")
    print(f"  ユーザー名: {user_name}")
    if workspace.get("team_name"):
        print(f"  ワークスペース: {workspace['team_name']}")
    print("")
    print(f"  作成日時: {config.get('created_at', '不明')}")
    print(f"  更新日時: {config.get('updated_at', '不明')}")
    print("")
    print(f"設定ファイル: {CONFIG_FILE}")


def clear_config() -> None:
    """設定をクリアする。"""
    config = load_config()

    if not config:
        print("クリアする設定がありません。")
        return

    # default_user_id と workspace をクリア
    if "default_user_id" in config:
        del config["default_user_id"]
    if "workspace" in config:
        del config["workspace"]

    save_config(config)

    print("デフォルトユーザー設定をクリアしました。")
    print(f"設定ファイル: {CONFIG_FILE}")


def main() -> None:
    """メイン関数。"""
    parser = argparse.ArgumentParser(
        description="Slack ユーザー設定を管理します"
    )
    subparsers = parser.add_subparsers(dest="command", help="コマンド")

    # set-user コマンド
    set_parser = subparsers.add_parser(
        "set-user", help="デフォルトユーザーを設定"
    )
    set_parser.add_argument(
        "--user-id",
        required=True,
        help="設定するユーザーID（例: U01234567）",
    )

    # show コマンド
    subparsers.add_parser("show", help="現在の設定を表示")

    # clear コマンド
    subparsers.add_parser("clear", help="設定をクリア")

    # json コマンド（デバッグ用）
    subparsers.add_parser("json", help="設定を JSON 形式で表示")

    args = parser.parse_args()

    if args.command == "set-user":
        set_user(args.user_id)
    elif args.command == "show":
        show_config()
    elif args.command == "clear":
        clear_config()
    elif args.command == "json":
        config = load_config()
        print_json(config)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
