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


def _load_mcp_env_from_settings() -> Dict[str, str]:
    """設定ファイルからMCP環境変数を読み込む。
    
    以下の順序で設定ファイルを読み込み、MCP設定のenvセクションから環境変数を取得:
    1. .claude/settings.local.json（プロジェクトローカル設定、最も優先）
    2. .claude/settings.json（プロジェクト設定）
    3. ~/.claude/settings.local.json（グローバルローカル設定）
    4. ~/.claude/settings.json（グローバル設定）
    
    Returns:
        MCP環境変数の辞書（mcpServers.slack.env から取得）
    """
    env_vars = {}
    settings_files = [
        Path(".claude/settings.local.json"),  # プロジェクトローカル（最優先）
        Path(".claude/settings.json"),        # プロジェクト設定
        Path.home() / ".claude/settings.local.json",  # グローバルローカル
        Path.home() / ".claude/settings.json",        # グローバル設定
    ]
    
    # 後から読み込んだファイルが優先される（逆順に読み込む）
    for settings_file in reversed(settings_files):
        if settings_file.exists():
            try:
                with open(settings_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    mcp_servers = settings.get("mcpServers", {})
                    slack_config = mcp_servers.get("slack", {})
                    slack_env = slack_config.get("env", {})
                    # 既存の値を上書き（後から読み込んだファイルが優先）
                    env_vars.update(slack_env)
            except (json.JSONDecodeError, IOError):
                # ファイル読み込みエラーは無視して続行
                continue
    
    return env_vars


def get_env_var(var_name: str, required: bool = True, default: Optional[str] = None) -> Optional[str]:
    """環境変数を取得する。
    
    以下の順序で環境変数を取得:
    1. os.environ（Claude Codeが設定した環境変数）
    2. 設定ファイルからMCP設定を読み込んで取得
    
    設定ファイルの読み込み順序:
    1. .claude/settings.local.json（プロジェクトローカル設定、最も優先）
    2. .claude/settings.json（プロジェクト設定）
    3. ~/.claude/settings.local.json（グローバルローカル設定）
    4. ~/.claude/settings.json（グローバル設定）
    
    MCP設定例（.claude/settings.local.json）:
    {
      "mcpServers": {
        "slack": {
          "env": {
            "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
            "SLACK_TEAM_ID": "T01234567"
          }
        }
      }
    }
    
    Args:
        var_name: 環境変数名
        required: 必須かどうか（Trueの場合、未設定時はエラー）
        default: デフォルト値（required=Falseの場合のみ有効）
        
    Returns:
        環境変数の値（未設定でrequired=Falseの場合はdefault）
        
    Raises:
        ValueError: required=Trueで環境変数が設定されていない場合
    """
    # まず環境変数から取得を試みる
    value = os.environ.get(var_name)
    
    # 環境変数がなければ設定ファイルから読み込む
    if not value:
        mcp_env = _load_mcp_env_from_settings()
        value = mcp_env.get(var_name, default)
    
    if required and not value:
        raise ValueError(
            f"環境変数 {var_name} が設定されていません。\n"
            "Claude Code の MCP 設定（.claude/settings.local.json など）で\n"
            f"{var_name} を設定してください。\n"
            "\n"
            "設定例:\n"
            '  "mcpServers": {\n'
            '    "slack": {\n'
            '      "env": {\n'
            f'        "{var_name}": "your-value"\n'
            '      }\n'
            '    }\n'
            '  }'
        )
    
    return value


def get_slack_client() -> WebClient:
    """Slack Web API クライアントを取得する。
    
    環境変数 SLACK_BOT_TOKEN から認証トークンを取得します。
    この環境変数は、Claude Code の MCP 設定（.claude/settings.local.json など）
    で設定した値と同じものを使用します。
    
    Returns:
        WebClient インスタンス
        
    Raises:
        ValueError: SLACK_BOT_TOKEN が設定されていない場合
    """
    token = get_env_var("SLACK_BOT_TOKEN", required=True)
    return WebClient(token=token)


def get_slack_team_id() -> Optional[str]:
    """Slack Team ID を取得する。

    環境変数 SLACK_TEAM_ID から取得します。
    この環境変数は、Claude Code の MCP 設定（.claude/settings.local.json など）
    で設定した値と同じものを使用します。

    Returns:
        Team ID（未設定の場合はNone）
    """
    return get_env_var("SLACK_TEAM_ID", required=False)


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


def get_default_user_id() -> Optional[str]:
    """デフォルトユーザーIDを取得する。

    設定ファイルから default_user_id を取得します。
    設定されていない場合は None を返します。

    Returns:
        デフォルトユーザーID（未設定の場合はNone）
    """
    config = load_config()
    return config.get("default_user_id")


# ======================================
# ユーザートークン関連関数
# ======================================


def has_user_token() -> bool:
    """ユーザートークン（SLACK_USER_TOKEN）が設定されているか確認する。

    Returns:
        ユーザートークンが設定されている場合は True
    """
    token = get_env_var("SLACK_USER_TOKEN", required=False)
    return token is not None and token.startswith("xoxp-")


def get_slack_user_client() -> WebClient:
    """ユーザートークン用の Slack Web API クライアントを取得する。

    環境変数 SLACK_USER_TOKEN から認証トークンを取得します。
    ユーザートークンを使用すると、Bot ではなくユーザーとして操作が実行されます。

    Returns:
        WebClient インスタンス（ユーザートークン使用）

    Raises:
        ValueError: SLACK_USER_TOKEN が設定されていない場合
    """
    token = get_env_var("SLACK_USER_TOKEN", required=True)
    return WebClient(token=token)


def get_effective_client(prefer_user: bool = True) -> tuple[WebClient, bool]:
    """状況に応じた Slack クライアントを取得する。

    ユーザートークンが設定されていて prefer_user が True の場合は
    ユーザートークンのクライアントを返し、それ以外は Bot クライアントを返します。

    Args:
        prefer_user: ユーザートークンを優先するか（デフォルト: True）

    Returns:
        (WebClient, is_user_client) のタプル
        - WebClient: Slack クライアント
        - is_user_client: ユーザートークンを使用している場合は True
    """
    if prefer_user and has_user_token():
        return get_slack_user_client(), True
    return get_slack_client(), False


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
                    "チャンネルIDが正しいか、Bot がチャンネルに招待されているか確認してください。"
                )
            elif error_code == "not_authed":
                print_error(
                    "認証エラー: トークンが無効です。\n"
                    "SLACK_BOT_TOKEN を確認してください。"
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
                print_error("メッセージを更新できません。Bot が投稿したメッセージのみ編集可能です。")
            elif error_code == "cant_delete_message":
                print_error("メッセージを削除できません。Bot が投稿したメッセージのみ削除可能です。")
            else:
                print_error(f"Slack API エラー: {error_code}\n詳細: {e.response}")
            sys.exit(1)
        except Exception as e:
            print_error(f"予期しないエラーが発生しました: {e}")
            sys.exit(1)
    
    return wrapper


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
