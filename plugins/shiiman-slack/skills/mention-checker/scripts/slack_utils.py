"""共通ユーティリティモジュール for shiiman-slack."""

import functools
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


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
