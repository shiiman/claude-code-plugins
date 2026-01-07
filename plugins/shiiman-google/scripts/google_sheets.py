#!/usr/bin/env python3
"""Google Sheets API操作スクリプト

スプレッドシートの作成・取得・更新を行う。

使用例:
    # スプレッドシート作成
    python google_sheets.py create --name "新規シート"
    python google_sheets.py create --name "テスト" --folder-id "xxx"

    # データ取得
    python google_sheets.py get --sheet-id "xxx"
    python google_sheets.py get --sheet-id "xxx" --range "A1:C10"

    # データ更新
    python google_sheets.py update --sheet-id "xxx" --range "A1" --values '["Hello", "World"]'
    python google_sheets.py update --sheet-id "xxx" --range "A1:B2" --values '[["A1","B1"],["A2","B2"]]'
"""

import argparse
import json
import os
import sys

# 共通モジュールのインポート
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from google_utils import (
    CONFIG_DIR,
    TOKENS_DIR,
    load_credentials,
    print_error,
    print_json,
    print_table,
    handle_api_error,
    get_token_path,
)

try:
    from googleapiclient.discovery import build
except ImportError:
    print_error("google-api-python-client がインストールされていません。pip install google-api-python-client を実行してください。")
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]


@handle_api_error
def create_spreadsheet(token_path: str, name: str, folder_id: str = None) -> dict:
    """新規スプレッドシートを作成する

    Args:
        token_path: トークンファイルのパス
        name: スプレッドシート名
        folder_id: 親フォルダID（省略時はマイドライブ）

    Returns:
        作成したスプレッドシート情報
    """
    creds = load_credentials(token_path, SCOPES)
    sheets_service = build("sheets", "v4", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    # スプレッドシート作成
    spreadsheet = sheets_service.spreadsheets().create(
        body={"properties": {"title": name}}
    ).execute()
    sheet_id = spreadsheet["spreadsheetId"]

    # フォルダに移動（指定がある場合）
    if folder_id:
        file = drive_service.files().get(fileId=sheet_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents", []))
        drive_service.files().update(
            fileId=sheet_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields="id, parents"
        ).execute()

    return {
        "id": sheet_id,
        "name": name,
        "url": f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    }


@handle_api_error
def get_spreadsheet(token_path: str, sheet_id: str, range_str: str = None) -> dict:
    """スプレッドシートのデータを取得する

    Args:
        token_path: トークンファイルのパス
        sheet_id: スプレッドシートID
        range_str: 取得範囲（例: "A1:C10", "Sheet1!A1:C10"）

    Returns:
        スプレッドシート情報とデータ
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("sheets", "v4", credentials=creds)

    # メタデータ取得
    spreadsheet = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    title = spreadsheet.get("properties", {}).get("title", "")
    sheets = [s.get("properties", {}).get("title", "") for s in spreadsheet.get("sheets", [])]

    # データ取得
    values = []
    if range_str:
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=range_str
        ).execute()
        values = result.get("values", [])
    else:
        # 範囲未指定の場合、最初のシートのデータを取得
        if sheets:
            result = service.spreadsheets().values().get(
                spreadsheetId=sheet_id,
                range=sheets[0]
            ).execute()
            values = result.get("values", [])

    return {
        "id": sheet_id,
        "title": title,
        "sheets": sheets,
        "range": range_str or (sheets[0] if sheets else ""),
        "values": values,
        "url": f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    }


@handle_api_error
def update_spreadsheet(token_path: str, sheet_id: str, range_str: str, values: list) -> dict:
    """スプレッドシートを更新する

    Args:
        token_path: トークンファイルのパス
        sheet_id: スプレッドシートID
        range_str: 更新範囲（例: "A1", "A1:B2"）
        values: 書き込むデータ（2次元配列）

    Returns:
        更新結果
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("sheets", "v4", credentials=creds)

    # 1次元配列の場合は2次元配列に変換
    if values and not isinstance(values[0], list):
        values = [values]

    result = service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range_str,
        valueInputOption="USER_ENTERED",
        body={"values": values}
    ).execute()

    return {
        "id": sheet_id,
        "status": "updated",
        "updatedRange": result.get("updatedRange", ""),
        "updatedRows": result.get("updatedRows", 0),
        "updatedColumns": result.get("updatedColumns", 0),
        "updatedCells": result.get("updatedCells", 0),
        "url": f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    }


@handle_api_error
def append_spreadsheet(token_path: str, sheet_id: str, range_str: str, values: list) -> dict:
    """スプレッドシートの末尾に行を追加する

    Args:
        token_path: トークンファイルのパス
        sheet_id: スプレッドシートID
        range_str: 追加先のシート範囲（例: "Sheet1"）
        values: 追加するデータ（2次元配列）

    Returns:
        追加結果
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("sheets", "v4", credentials=creds)

    # 1次元配列の場合は2次元配列に変換
    if values and not isinstance(values[0], list):
        values = [values]

    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=range_str,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": values}
    ).execute()

    updates = result.get("updates", {})
    return {
        "id": sheet_id,
        "status": "appended",
        "updatedRange": updates.get("updatedRange", ""),
        "updatedRows": updates.get("updatedRows", 0),
        "updatedCells": updates.get("updatedCells", 0),
        "url": f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    }


def main():
    parser = argparse.ArgumentParser(description="Google Sheets 操作")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="出力形式")
    parser.add_argument("--token", help="トークンファイルパス（省略時はアクティブプロファイル）")

    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")

    # create コマンド
    create_parser = subparsers.add_parser("create", help="スプレッドシート作成")
    create_parser.add_argument("--name", required=True, help="スプレッドシート名")
    create_parser.add_argument("--folder-id", help="親フォルダID")

    # get コマンド
    get_parser = subparsers.add_parser("get", help="データ取得")
    get_parser.add_argument("--sheet-id", required=True, help="スプレッドシートID")
    get_parser.add_argument("--range", help="取得範囲（例: A1:C10）")

    # update コマンド
    update_parser = subparsers.add_parser("update", help="データ更新")
    update_parser.add_argument("--sheet-id", required=True, help="スプレッドシートID")
    update_parser.add_argument("--range", required=True, help="更新範囲（例: A1:B2）")
    update_parser.add_argument("--values", required=True, help="書き込むデータ（JSON配列）")

    # append コマンド
    append_parser = subparsers.add_parser("append", help="行を末尾に追加")
    append_parser.add_argument("--sheet-id", required=True, help="スプレッドシートID")
    append_parser.add_argument("--range", default="Sheet1", help="追加先シート（デフォルト: Sheet1）")
    append_parser.add_argument("--values", required=True, help="追加するデータ（JSON配列）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # トークンパス決定
    token_path = args.token if args.token else get_token_path()
    if not token_path:
        print_error("アクティブなプロファイルがありません。'google_auth.py login' で認証してください。")
        sys.exit(1)

    # コマンド実行
    if args.command == "create":
        result = create_spreadsheet(token_path, args.name, args.folder_id)
        if args.format == "json":
            print_json([result])
        else:
            print(f"スプレッドシートを作成しました:")
            print(f"  ID: {result['id']}")
            print(f"  名前: {result['name']}")
            print(f"  URL: {result['url']}")

    elif args.command == "get":
        result = get_spreadsheet(token_path, args.sheet_id, args.range)
        if args.format == "json":
            print_json([result])
        else:
            print(f"タイトル: {result['title']}")
            print(f"シート: {', '.join(result['sheets'])}")
            print(f"範囲: {result['range']}")
            print(f"URL: {result['url']}")
            print("-" * 40)
            if result['values']:
                for row in result['values']:
                    print("\t".join(str(cell) for cell in row))
            else:
                print("データがありません")

    elif args.command == "update":
        try:
            values = json.loads(args.values)
        except json.JSONDecodeError:
            print_error("--values はJSON形式で指定してください（例: '[\"A\",\"B\"]' または '[[\"A1\",\"B1\"],[\"A2\",\"B2\"]]'）")
            sys.exit(1)

        result = update_spreadsheet(token_path, args.sheet_id, args.range, values)
        if args.format == "json":
            print_json([result])
        else:
            print(f"スプレッドシートを更新しました:")
            print(f"  更新範囲: {result['updatedRange']}")
            print(f"  更新行数: {result['updatedRows']}")
            print(f"  更新列数: {result['updatedColumns']}")
            print(f"  更新セル数: {result['updatedCells']}")
            print(f"  URL: {result['url']}")

    elif args.command == "append":
        try:
            values = json.loads(args.values)
        except json.JSONDecodeError:
            print_error("--values はJSON形式で指定してください（例: '[\"A\",\"B\"]' または '[[\"A1\",\"B1\"],[\"A2\",\"B2\"]]'）")
            sys.exit(1)

        result = append_spreadsheet(token_path, args.sheet_id, args.range, values)
        if args.format == "json":
            print_json([result])
        else:
            print(f"行を追加しました:")
            print(f"  追加先: {result['updatedRange']}")
            print(f"  追加行数: {result['updatedRows']}")
            print(f"  追加セル数: {result['updatedCells']}")
            print(f"  URL: {result['url']}")


if __name__ == "__main__":
    main()
