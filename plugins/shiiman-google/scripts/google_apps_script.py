#!/usr/bin/env python3
"""Google Apps Script API操作スクリプト

スクリプトの作成・取得・更新を行う。

使用例:
    # スクリプト作成（スタンドアロン）
    python google_apps_script.py create --name "新規スクリプト"

    # スクリプト作成（スプレッドシートに紐付け）
    python google_apps_script.py create --name "マクロ" --parent-id "spreadsheet-id"

    # スクリプト取得
    python google_apps_script.py get --script-id "xxx"

    # コード更新
    python google_apps_script.py update --script-id "xxx" --filename "Code.gs" --code "function myFunc() {}"
"""

import os
import sys
import argparse
import json

# lib/ ディレクトリをパスに追加
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib")
sys.path.insert(0, lib_dir)

from google_utils import (
    CONFIG_DIR,
    TOKENS_DIR,
    load_credentials,
    print_error,
    print_json,
    print_profile_header,
    handle_api_error,
    get_token_path,
)

try:
    from googleapiclient.discovery import build
except ImportError:
    print_error("google-api-python-client がインストールされていません。pip install google-api-python-client を実行してください。")
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/script.projects",
    "https://www.googleapis.com/auth/drive",
]


@handle_api_error
def create_script(token_path: str, name: str, parent_id: str = None) -> dict:
    """新規スクリプトプロジェクトを作成する

    Args:
        token_path: トークンファイルのパス
        name: スクリプト名
        parent_id: 親ドキュメントID（スプレッドシート等に紐付ける場合）

    Returns:
        作成したスクリプト情報
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("script", "v1", credentials=creds)

    body = {"title": name}
    if parent_id:
        body["parentId"] = parent_id

    project = service.projects().create(body=body).execute()
    script_id = project["scriptId"]

    return {
        "id": script_id,
        "name": name,
        "parentId": parent_id,
        "url": f"https://script.google.com/d/{script_id}/edit"
    }


@handle_api_error
def get_script(token_path: str, script_id: str) -> dict:
    """スクリプトの内容を取得する

    Args:
        token_path: トークンファイルのパス
        script_id: スクリプトID

    Returns:
        スクリプト情報
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("script", "v1", credentials=creds)

    # プロジェクト情報取得
    project = service.projects().get(scriptId=script_id).execute()

    # コンテンツ取得
    content = service.projects().getContent(scriptId=script_id).execute()

    files = []
    for file in content.get("files", []):
        files.append({
            "name": file.get("name", ""),
            "type": file.get("type", ""),
            "source": file.get("source", ""),
        })

    return {
        "id": script_id,
        "title": project.get("title", ""),
        "parentId": project.get("parentId"),
        "files": files,
        "url": f"https://script.google.com/d/{script_id}/edit"
    }


@handle_api_error
def update_script(token_path: str, script_id: str, filename: str, code: str) -> dict:
    """スクリプトのコードを更新する

    Args:
        token_path: トークンファイルのパス
        script_id: スクリプトID
        filename: ファイル名（例: "Code.gs", "Utils.gs"）
        code: ソースコード

    Returns:
        更新結果
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("script", "v1", credentials=creds)

    # 現在のコンテンツ取得
    content = service.projects().getContent(scriptId=script_id).execute()
    files = content.get("files", [])

    # ファイルタイプ判定
    file_type = "SERVER_JS"
    if filename.endswith(".html"):
        file_type = "HTML"
    elif filename.endswith(".json"):
        file_type = "JSON"

    # ファイル名から拡張子を除去
    name = filename
    if name.endswith(".gs"):
        name = name[:-3]
    elif name.endswith(".html"):
        name = name[:-5]
    elif name.endswith(".json"):
        name = name[:-5]

    # ファイルを更新または追加
    found = False
    for f in files:
        if f.get("name") == name:
            f["source"] = code
            found = True
            break

    if not found:
        files.append({
            "name": name,
            "type": file_type,
            "source": code
        })

    # コンテンツ更新
    service.projects().updateContent(
        scriptId=script_id,
        body={"files": files}
    ).execute()

    return {
        "id": script_id,
        "status": "updated",
        "filename": filename,
        "url": f"https://script.google.com/d/{script_id}/edit"
    }


def main():
    # プロファイルヘッダーを表示
    print_profile_header()

    parser = argparse.ArgumentParser(description="Google Apps Script 操作")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="出力形式")
    parser.add_argument("--token", help="トークンファイルパス（省略時はアクティブプロファイル）")
    parser.add_argument("--profile", help="認証プロファイル名（デフォルト: アクティブプロファイル）")

    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")

    # create コマンド
    create_parser = subparsers.add_parser("create", help="スクリプト作成")
    create_parser.add_argument("--name", required=True, help="スクリプト名")
    create_parser.add_argument("--parent-id", help="親ドキュメントID（スプレッドシート等）")

    # get コマンド
    get_parser = subparsers.add_parser("get", help="スクリプト取得")
    get_parser.add_argument("--script-id", required=True, help="スクリプトID")

    # update コマンド
    update_parser = subparsers.add_parser("update", help="コード更新")
    update_parser.add_argument("--script-id", required=True, help="スクリプトID")
    update_parser.add_argument("--filename", required=True, help="ファイル名（例: Code.gs）")
    update_parser.add_argument("--code", required=True, help="ソースコード")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # トークンパス決定
    if args.token:
        token_path = args.token
    elif args.profile:
        token_path = get_token_path(args.profile)
    else:
        token_path = get_token_path()
    if not token_path:
        print_error("アクティブなプロファイルがありません。'google_auth.py login' で認証してください。")
        sys.exit(1)

    # コマンド実行
    if args.command == "create":
        result = create_script(token_path, args.name, args.parent_id)
        if args.format == "json":
            print_json([result])
        else:
            print(f"スクリプトを作成しました:")
            print(f"  ID: {result['id']}")
            print(f"  名前: {result['name']}")
            if result['parentId']:
                print(f"  親ID: {result['parentId']}")
            print(f"  URL: {result['url']}")

    elif args.command == "get":
        result = get_script(token_path, args.script_id)
        if args.format == "json":
            print_json([result])
        else:
            print(f"タイトル: {result['title']}")
            if result['parentId']:
                print(f"親ID: {result['parentId']}")
            print(f"URL: {result['url']}")
            print("-" * 40)
            for f in result['files']:
                print(f"ファイル: {f['name']} ({f['type']})")
                print("-" * 20)
                # ソースコードを表示（長い場合は省略）
                source = f['source']
                if len(source) > 500:
                    print(source[:500] + "...\n(省略)")
                else:
                    print(source)
                print()

    elif args.command == "update":
        result = update_script(token_path, args.script_id, args.filename, args.code)
        if args.format == "json":
            print_json([result])
        else:
            print(f"スクリプトを更新しました:")
            print(f"  スクリプトID: {result['id']}")
            print(f"  ファイル: {result['filename']}")
            print(f"  URL: {result['url']}")


if __name__ == "__main__":
    main()
