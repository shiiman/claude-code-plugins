#!/usr/bin/env python3
"""Slack ユーザー設定管理スクリプト。

トークン設定とデフォルトユーザーIDの設定・表示・削除を行います。
"""

import os
import sys
import argparse
# lib/ ディレクトリをパスに追加
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib")
sys.path.insert(0, lib_dir)

from slack_utils import (
    CONFIG_FILE,
    get_default_user_id,
    get_slack_client,
    get_slack_token,
    get_user_name,
    handle_api_error,
    load_config,
    print_error,
    print_json,
    save_config,
    set_slack_token,
)


# 定数: 共通メッセージ
MSG_USER_SETUP_HINT = (
    "ユーザーを設定するには:\n"
    "  「自分を設定して U01234567」と指示してください。"
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
def set_token(token: str) -> None:
    """Slack トークンを設定する。

    Args:
        token: 設定する User Token (xoxp-...)
    """
    # トークン形式の検証
    if not token.startswith("xoxp-"):
        print_error(
            "無効なトークン形式です。\n"
            "User Token (xoxp-...) を指定してください。"
        )
        sys.exit(1)

    # トークンを保存
    set_slack_token(token)

    # トークンの検証（auth.test で確認）
    try:
        from slack_sdk import WebClient
        client = WebClient(token=token)
        auth_result = client.auth_test()

        user_id = auth_result["user_id"]
        user_name = auth_result["user"]
        team_id = auth_result["team_id"]
        team_name = auth_result["team"]

        # ワークスペース情報も保存
        config = load_config()
        config["team_id"] = team_id
        config["workspace"] = {
            "team_id": team_id,
            "team_name": team_name,
        }
        save_config(config)

        print("トークンを設定しました。")
        print("")
        print(f"  ユーザーID: {user_id}")
        print(f"  ユーザー名: {user_name}")
        print(f"  ワークスペース: {team_name}")
        print("")
        print(f"設定ファイル: {CONFIG_FILE}")

    except Exception as e:
        print_error(f"トークンの検証に失敗しました: {e}")
        sys.exit(1)


def show_token() -> None:
    """トークンの設定状況を表示する（マスク表示）。"""
    token = get_slack_token()

    if not token:
        print("トークンが設定されていません。")
        print("")
        print("トークンを設定するには:")
        print("  /shiiman-slack:user-setup --token xoxp-your-token")
        return

    # トークンをマスク表示（最初と最後の4文字のみ表示）
    if len(token) > 12:
        masked = token[:8] + "..." + token[-4:]
    else:
        masked = token[:4] + "..."

    print("トークン設定状況:")
    print("")
    print(f"  トークン: {masked}")
    print(f"  形式: {'User Token' if token.startswith('xoxp-') else '不明'}")
    print("")
    print(f"設定ファイル: {CONFIG_FILE}")


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
        print("トークンを設定するには:")
        print("  /shiiman-slack:user-setup --token xoxp-your-token")
        return

    # トークン状況
    token = config.get("slack_token")
    if token:
        if len(token) > 12:
            masked = token[:8] + "..." + token[-4:]
        else:
            masked = token[:4] + "..."
        print(f"トークン: {masked}")
    else:
        print("トークン: (未設定)")

    # ユーザー情報
    user_id = config.get("default_user_id")
    if user_id:
        # ユーザー名を取得
        try:
            client = get_slack_client()
            user_name = get_user_name(client, user_id)
        except Exception:
            user_name = "(取得失敗)"
        print(f"デフォルトユーザー: {user_id} ({user_name})")
    else:
        print("デフォルトユーザー: (未設定)")

    # ワークスペース情報
    workspace = config.get("workspace", {})
    if workspace.get("team_name"):
        print(f"ワークスペース: {workspace['team_name']}")

    print("")
    print(f"作成日時: {config.get('created_at', '不明')}")
    print(f"更新日時: {config.get('updated_at', '不明')}")
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


def clear_token() -> None:
    """トークンをクリアする。"""
    config = load_config()

    if not config or "slack_token" not in config:
        print("クリアするトークンがありません。")
        return

    del config["slack_token"]
    save_config(config)

    print("トークンをクリアしました。")
    print(f"設定ファイル: {CONFIG_FILE}")


@handle_api_error
def auto_detect() -> None:
    """トークンからユーザーを自動検出して設定する。

    設定済みのトークンを使って auth.test API を呼び出し、
    トークンの所有者情報を取得してデフォルトユーザーとして設定します。
    """
    token = get_slack_token()
    if not token:
        print_error(
            "トークンが設定されていません。\n"
            "\n"
            "先にトークンを設定してください:\n"
            "  /shiiman-slack:user-setup --token xoxp-your-token\n"
            "\n"
            "または、手動でユーザーIDを指定:\n"
            "  python slack_config.py set-user --user-id U01234567"
        )
        sys.exit(1)

    # トークンで認証テスト（トークンの所有者情報を取得）
    client = get_slack_client()
    auth_result = client.auth_test()

    user_id = auth_result["user_id"]
    user_name = auth_result["user"]
    team_id = auth_result["team_id"]
    team_name = auth_result["team"]

    # ユーザーの詳細情報を取得（表示名など）
    try:
        user_result = client.users_info(user=user_id)
        user = user_result["user"]
        display_name = user.get("real_name") or user.get("name") or user_name
    except Exception:
        display_name = user_name

    # 設定を保存
    config = load_config()
    config["default_user_id"] = user_id
    config["team_id"] = team_id
    config["workspace"] = {
        "team_id": team_id,
        "team_name": team_name,
    }
    save_config(config)

    print("トークンからユーザーを自動検出しました。")
    print("")
    print(f"  ユーザーID: {user_id}")
    print(f"  ユーザー名: {display_name}")
    print(f"  ワークスペース: {team_name}")
    print("")
    print(f"設定ファイル: {CONFIG_FILE}")


def main() -> None:
    """メイン関数。"""
    parser = argparse.ArgumentParser(
        description="Slack ユーザー設定を管理します"
    )
    subparsers = parser.add_subparsers(dest="command", help="コマンド")

    # token-set コマンド
    token_set_parser = subparsers.add_parser(
        "token-set", help="トークンを設定"
    )
    token_set_parser.add_argument(
        "--token",
        required=True,
        help="User Token (xoxp-...)",
    )

    # token-show コマンド
    subparsers.add_parser("token-show", help="トークン設定状況を表示")

    # token-clear コマンド
    subparsers.add_parser("token-clear", help="トークンをクリア")

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
    subparsers.add_parser("clear", help="ユーザー設定をクリア")

    # auto-detect コマンド
    subparsers.add_parser(
        "auto-detect",
        help="トークンからユーザーを自動検出して設定"
    )

    # json コマンド（デバッグ用）
    subparsers.add_parser("json", help="設定を JSON 形式で表示")

    args = parser.parse_args()

    if args.command == "token-set":
        set_token(args.token)
    elif args.command == "token-show":
        show_token()
    elif args.command == "token-clear":
        clear_token()
    elif args.command == "set-user":
        set_user(args.user_id)
    elif args.command == "show":
        show_config()
    elif args.command == "clear":
        clear_config()
    elif args.command == "auto-detect":
        auto_detect()
    elif args.command == "json":
        config = load_config()
        print_json(config)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
