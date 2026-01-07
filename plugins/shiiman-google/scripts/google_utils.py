"""共通ユーティリティモジュール for shiiman-google."""

import json
import os
import sys
from typing import Any, Dict, List, Optional

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# 設定ディレクトリ
CONFIG_DIR = os.path.expanduser("~/.config/shiiman-google")
TOKENS_DIR = os.path.join(CONFIG_DIR, "tokens")
CLIENTS_DIR = os.path.join(CONFIG_DIR, "clients")
ACTIVE_PROFILE_FILE = os.path.join(CONFIG_DIR, "active-profile")


def expand_path(path: str) -> str:
    """パスを展開する。"""
    return os.path.expanduser(path)


def get_active_profile() -> str:
    """アクティブなプロファイル名を取得する。"""
    if os.path.exists(ACTIVE_PROFILE_FILE):
        with open(ACTIVE_PROFILE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip() or "default"
    return "default"


def get_token_path(profile: Optional[str] = None) -> str:
    """トークンファイルのパスを取得する。"""
    if profile is None:
        profile = get_active_profile()
    return os.path.join(TOKENS_DIR, f"{profile}.json")


def list_profiles() -> List[str]:
    """登録済みの全プロファイル名を取得する。"""
    if not os.path.exists(TOKENS_DIR):
        return []
    profiles = []
    for filename in os.listdir(TOKENS_DIR):
        if filename.endswith(".json"):
            profiles.append(filename[:-5])  # .json を除去
    return sorted(profiles)


def load_credentials(
    token_path: str,
    scopes: List[str],
    auto_refresh: bool = True,
) -> Credentials:
    """認証情報を読み込み、必要に応じてリフレッシュする。

    Args:
        token_path: トークンファイルのパス
        scopes: 必要なスコープ
        auto_refresh: 期限切れ時に自動リフレッシュするか

    Returns:
        認証情報

    Raises:
        FileNotFoundError: トークンファイルが存在しない場合
        RefreshError: トークンのリフレッシュに失敗した場合
    """
    path = expand_path(token_path)

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"トークンファイルが見つかりません: {path}\n"
            "「Google 認証して」または「ログインして」と言って認証を行ってください。"
        )

    creds = Credentials.from_authorized_user_file(path, scopes=scopes)

    # 期限切れの場合はリフレッシュを試みる
    if auto_refresh and creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # リフレッシュ後のトークンを保存
            save_credentials(path, creds)
        except RefreshError as e:
            raise RefreshError(
                f"トークンのリフレッシュに失敗しました。再認証が必要です。\n"
                f"「Google 認証して」と言って再認証を行ってください。\n"
                f"詳細: {e}"
            ) from e

    return creds


def save_credentials(token_path: str, creds: Credentials) -> None:
    """認証情報をファイルに保存する。"""
    path = expand_path(token_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # セキュリティ: ファイルパーミッションを制限
    os.chmod(path, 0o600)


def print_error(message: str) -> None:
    """エラーメッセージを標準エラー出力に表示する。"""
    print(f"エラー: {message}", file=sys.stderr)


def print_table(items: List[Dict[str, Any]], headers: List[str]) -> None:
    """データをテーブル形式で出力する。

    Args:
        items: 出力するデータのリスト
        headers: ヘッダー（キー名）のリスト
    """
    if not items:
        print("データがありません。")
        return

    # ヘッダー出力
    print("\t".join(headers))

    # データ出力
    for item in items:
        row = []
        for header in headers:
            value = item.get(header, "")
            # 改行やタブを置換
            if isinstance(value, str):
                value = value.replace("\n", " ").replace("\t", " ")
            row.append(str(value))
        print("\t".join(row))


def print_json(items: Any) -> None:
    """データを JSON 形式で出力する。"""
    print(json.dumps(items, ensure_ascii=False, indent=2))


def format_output(
    items: Any,
    headers: Optional[List[str]] = None,
    output_format: str = "table",
) -> None:
    """指定されたフォーマットでデータを出力する。

    Args:
        items: 出力するデータ
        headers: テーブル形式の場合のヘッダー
        output_format: 出力形式 ("table" or "json")
    """
    if output_format == "json":
        print_json(items)
    else:
        if headers and isinstance(items, list):
            print_table(items, headers)
        else:
            print_json(items)


def handle_api_error(func):
    """API 呼び出しのエラーハンドリングデコレータ。"""
    from functools import wraps

    from googleapiclient.errors import HttpError

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print_error(str(e))
            sys.exit(1)
        except RefreshError as e:
            print_error(str(e))
            sys.exit(1)
        except HttpError as e:
            if e.resp.status == 401:
                print_error(
                    "認証エラー: トークンが無効です。\n"
                    "「Google 認証して」と言って再認証を行ってください。"
                )
            elif e.resp.status == 403:
                print_error(
                    f"権限エラー: この操作を実行する権限がありません。\n詳細: {e}"
                )
            elif e.resp.status == 404:
                print_error(f"リソースが見つかりません。\n詳細: {e}")
            elif e.resp.status == 429:
                print_error(
                    "API レート制限に達しました。しばらく待ってから再試行してください。"
                )
            else:
                print_error(f"API エラー: {e}")
            sys.exit(1)
        except Exception as e:
            print_error(f"予期しないエラーが発生しました: {e}")
            sys.exit(1)

    return wrapper
