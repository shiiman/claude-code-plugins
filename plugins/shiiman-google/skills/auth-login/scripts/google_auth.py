"""OAuth login and token storage for shiiman-google."""

import argparse
import json
import os
import pathlib
import sys
from typing import Iterable, List

from google_auth_oauthlib.flow import InstalledAppFlow

from google_utils import (
    ACTIVE_PROFILE_FILE,
    CLIENTS_DIR,
    CONFIG_DIR,
    TOKENS_DIR,
    expand_path,
    list_profiles,
    print_error,
)

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/script.projects",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
]


def _load_client(path: str) -> dict:
    """クライアント設定を読み込む。"""
    expanded_path = expand_path(path)
    if not os.path.exists(expanded_path):
        raise FileNotFoundError(
            f"クライアント設定ファイルが見つかりません: {expanded_path}\n"
            "Google Cloud Console で OAuth クライアント ID を作成し、\n"
            f"{CLIENTS_DIR}/default.json に保存してください。"
        )
    with open(expanded_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dir(path: str) -> None:
    """ディレクトリを作成する。"""
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def _save_json(path: str, payload: dict) -> None:
    """JSON をファイルに保存する（セキュリティ考慮）。"""
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
    # セキュリティ: ファイルパーミッションを制限
    os.chmod(path, 0o600)


def login(client_path: str, token_path: str, scopes: Iterable[str]) -> None:
    """OAuth ログインを実行してトークンを保存する。

    Args:
        client_path: クライアント設定ファイルのパス
        token_path: トークン保存先のパス
        scopes: 要求するスコープ
    """
    client = _load_client(client_path)
    flow = InstalledAppFlow.from_client_config(client, scopes)

    print("ブラウザで Google 認証画面が開きます...")
    print("認証が完了するまでお待ちください。")

    try:
        creds = flow.run_local_server(port=0, timeout_seconds=300)
    except Exception as e:
        raise RuntimeError(
            f"認証に失敗しました: {e}\n"
            "ブラウザで認証を完了してください。"
        ) from e

    _ensure_dir(os.path.dirname(token_path))
    _save_json(
        token_path,
        {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": list(creds.scopes) if creds.scopes else [],
        },
    )

    print(f"認証完了！トークンを保存しました: {token_path}")


def set_active_profile(profile: str) -> None:
    """アクティブなプロファイルを設定する。"""
    _ensure_dir(CONFIG_DIR)
    with open(ACTIVE_PROFILE_FILE, "w", encoding="utf-8") as f:
        f.write(profile)
    print(f"アクティブプロファイルを '{profile}' に設定しました。")


def show_profiles() -> None:
    """登録済みプロファイル一覧を表示する。"""
    profiles = list_profiles()
    if not profiles:
        print("登録済みのプロファイルはありません。")
        return

    # アクティブプロファイルを取得
    active = ""
    if os.path.exists(ACTIVE_PROFILE_FILE):
        with open(ACTIVE_PROFILE_FILE, "r", encoding="utf-8") as f:
            active = f.read().strip()

    print("登録済みプロファイル:")
    for profile in profiles:
        marker = " (active)" if profile == active else ""
        print(f"  - {profile}{marker}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Google OAuth 認証ツール")

    subparsers = parser.add_subparsers(dest="command")

    # login サブコマンド
    login_parser = subparsers.add_parser("login", help="認証を実行")
    login_parser.add_argument(
        "--client",
        default=os.path.join(CLIENTS_DIR, "default.json"),
        help="クライアント設定ファイル",
    )
    login_parser.add_argument(
        "--profile",
        default="default",
        help="プロファイル名 (デフォルト: default)",
    )
    login_parser.add_argument("--scopes", nargs="*", default=DEFAULT_SCOPES)

    # profiles サブコマンド
    subparsers.add_parser("profiles", help="プロファイル一覧を表示")

    # switch サブコマンド
    switch_parser = subparsers.add_parser("switch", help="プロファイルを切り替え")
    switch_parser.add_argument("profile", help="切り替え先のプロファイル名")

    args = parser.parse_args()

    try:
        # 後方互換性: 旧形式の引数をサポート
        if args.command is None:
            legacy_parser = argparse.ArgumentParser()
            legacy_parser.add_argument("--client", required=True)
            legacy_parser.add_argument("--token", required=True)
            legacy_parser.add_argument("--scopes", nargs="*", default=DEFAULT_SCOPES)
            legacy_args, _ = legacy_parser.parse_known_args()

            client_path = expand_path(legacy_args.client)
            token_path = expand_path(legacy_args.token)
            login(client_path, token_path, legacy_args.scopes)
            return

        if args.command == "login":
            client_path = expand_path(args.client)
            token_path = os.path.join(TOKENS_DIR, f"{args.profile}.json")
            login(client_path, token_path, args.scopes)
            # ログイン後、アクティブプロファイルを設定
            set_active_profile(args.profile)

        elif args.command == "profiles":
            show_profiles()

        elif args.command == "switch":
            profiles = list_profiles()
            if args.profile not in profiles:
                print_error(
                    f"プロファイル '{args.profile}' が見つかりません。\n"
                    f"利用可能なプロファイル: {', '.join(profiles)}"
                )
                sys.exit(1)
            set_active_profile(args.profile)

    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)
    except RuntimeError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
