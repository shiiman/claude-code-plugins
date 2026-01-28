"""共通ユーティリティモジュール for shiiman-slack."""

import functools
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# 設定ディレクトリ
CONFIG_DIR = os.path.expanduser("~/.config/shiiman-slack")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


# ======================================
# 設定管理関数
# ======================================


def load_config() -> Dict[str, Any]:
    """設定ファイルを読み込む。

    設定ファイル（~/.config/shiiman-slack/config.json）から設定を読み込みます。
    ファイルが存在しない場合は空の辞書を返します。

    Returns:
        設定データの辞書
    """
    if not os.path.exists(CONFIG_FILE):
        return {}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_config(config: Dict[str, Any]) -> None:
    """設定ファイルに保存する。

    設定データを ~/.config/shiiman-slack/config.json に保存します。
    ディレクトリが存在しない場合は自動的に作成されます。

    Args:
        config: 保存する設定データ
    """
    # ディレクトリがなければ作成（権限 700: 所有者のみアクセス可能）
    os.makedirs(CONFIG_DIR, mode=0o700, exist_ok=True)

    # タイムスタンプを更新
    now = datetime.now(timezone.utc).isoformat() + "Z"
    if "created_at" not in config:
        config["created_at"] = now
    config["updated_at"] = now

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    # ファイル権限を 600 に設定（所有者のみ読み書き可能）
    os.chmod(CONFIG_FILE, 0o600)


# ======================================
# トークン管理関数
# ======================================


def get_slack_token() -> Optional[str]:
    """Slack トークンを取得する。

    config.json から slack_token を取得します。

    Returns:
        Slack User Token（未設定の場合は None）
    """
    config = load_config()
    return config.get("slack_token")


def set_slack_token(token: str) -> None:
    """Slack トークンを設定する。

    config.json に slack_token を保存します。

    Args:
        token: Slack User Token (xoxp-...)

    Raises:
        ValueError: トークン形式が不正な場合
    """
    if not token.startswith("xoxp-"):
        raise ValueError(
            "無効なトークン形式です。User Token (xoxp-...) を指定してください。"
        )

    config = load_config()
    config["slack_token"] = token
    save_config(config)


def get_slack_client() -> WebClient:
    """Slack Web API クライアントを取得する。

    config.json から slack_token を取得してクライアントを作成します。

    Returns:
        WebClient インスタンス

    Raises:
        ValueError: slack_token が設定されていない場合
    """
    token = get_slack_token()
    if not token:
        raise ValueError(
            "Slack トークンが設定されていません。\n"
            "以下のコマンドでトークンを設定してください:\n"
            "  /shiiman-slack:user-setup --token xoxp-your-token\n"
            "\n"
            "または config.json を直接編集:\n"
            f"  {CONFIG_FILE}"
        )
    return WebClient(token=token)


def get_slack_team_id() -> Optional[str]:
    """Slack Team ID を取得する。

    config.json から team_id を取得します。

    Returns:
        Team ID（未設定の場合は None）
    """
    config = load_config()
    return config.get("team_id")


def get_default_user_id() -> Optional[str]:
    """デフォルトユーザーIDを取得する。

    設定ファイルから default_user_id を取得します。
    設定されていない場合は None を返します。

    Returns:
        デフォルトユーザーID（未設定の場合は None）
    """
    config = load_config()
    return config.get("default_user_id")


# ======================================
# 出力ユーティリティ関数
# ======================================


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


def handle_api_error(func: Callable) -> Callable:
    """Slack API 呼び出しのエラーハンドリングデコレータ。

    使用例:
        @handle_api_error
        def call_slack_api():
            ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print_error(str(e))
            sys.exit(1)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown")
            if error_code == "channel_not_found":
                print_error(
                    "チャンネルが見つかりません。\n"
                    "チャンネルIDが正しいか確認してください。"
                )
            elif error_code == "not_authed":
                print_error(
                    "認証エラー: トークンが無効です。\n"
                    "/shiiman-slack:user-setup --token でトークンを再設定してください。"
                )
            elif error_code == "missing_scope":
                print_error(
                    f"権限エラー: この操作を実行する権限がありません。\n"
                    f"必要なスコープを Slack App に追加してください。\n"
                    f"詳細: {e.response.get('needed', 'unknown')}"
                )
            elif error_code == "rate_limited":
                print_error(
                    "API レート制限に達しました。しばらく待ってから再試行してください。"
                )
            elif error_code == "message_not_found":
                print_error("メッセージが見つかりません。")
            elif error_code == "cant_update_message":
                print_error("メッセージを更新できません。")
            elif error_code == "cant_delete_message":
                print_error("メッセージを削除できません。")
            else:
                print_error(f"Slack API エラー: {error_code}\n詳細: {e.response}")
            sys.exit(1)
        except Exception as e:
            print_error(f"予期しないエラーが発生しました: {e}")
            sys.exit(1)

    return wrapper


# ======================================
# ユーザー情報ユーティリティ
# ======================================


def get_user_name(client: WebClient, user_id: str) -> str:
    """ユーザーIDからユーザー名を取得する。

    Args:
        client: Slack Web API クライアント
        user_id: ユーザーID

    Returns:
        ユーザー名（取得失敗時はuser_idをそのまま返す）
    """
    try:
        result = client.users_info(user=user_id)
        user = result["user"]
        return user.get("real_name") or user.get("name") or user_id
    except SlackApiError:
        return user_id


def resolve_user_names(client: WebClient, messages: List[Dict]) -> List[Dict]:
    """メッセージリスト内のユーザーIDをユーザー名に解決する。

    Args:
        client: Slack Web API クライアント
        messages: メッセージリスト（user キーを含む辞書のリスト）

    Returns:
        ユーザー名が解決されたメッセージリスト
    """
    # ユーザーIDを収集
    user_ids = set()
    for msg in messages:
        if "user" in msg and msg["user"]:
            user_ids.add(msg["user"])

    # ユーザー名マップを作成
    user_map = {}
    for user_id in user_ids:
        user_map[user_id] = get_user_name(client, user_id)

    # メッセージにユーザー名を追加
    result = []
    for msg in messages:
        msg_copy = msg.copy()
        if "user" in msg_copy and msg_copy["user"]:
            msg_copy["user_name"] = user_map.get(msg_copy["user"], msg_copy["user"])
        result.append(msg_copy)

    return result
