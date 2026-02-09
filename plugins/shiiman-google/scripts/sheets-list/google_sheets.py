#!/usr/bin/env python3
"""Google Sheets API操作スクリプト

スプレッドシートの作成・取得・更新・エクスポートを行う。

使用例:
    # スプレッドシート作成
    python google_sheets.py create --name "新規シート"
    python google_sheets.py create --name "テスト" --folder-id "xxx"

    # シート（タブ）一覧取得
    python google_sheets.py sheets --sheet-id "xxx"

    # データ取得
    python google_sheets.py get --sheet-id "xxx"
    python google_sheets.py get --sheet-id "xxx" --range "A1:C10"
    python google_sheets.py get --sheet-id "xxx" --sheet "売上データ"

    # データ更新
    python google_sheets.py update --sheet-id "xxx" --range "A1" --values '["Hello", "World"]'
    python google_sheets.py update --sheet-id "xxx" --range "A1:B2" --values '[["A1","B1"],["A2","B2"]]'

    # CSVエクスポート
    python google_sheets.py export --sheet-id "xxx" --output "data.csv"
    python google_sheets.py export --sheet-id "xxx" --output "data.xlsx" --type xlsx
    python google_sheets.py export --sheet-id "xxx" --output "data.csv" --sheet "売上データ"
"""

import os
import sys
import argparse
import json

# lib/ ディレクトリをパスに追加
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib")
sys.path.insert(0, lib_dir)

from google_utils import (
    CONFIG_DIR,
    TOKENS_DIR,
    load_credentials,
    print_error,
    print_json,
    print_profile_header,
    print_table,
    handle_api_error,
    get_token_path,
    retry_with_backoff,
)

try:
    from googleapiclient.discovery import build
except ImportError:
    print_error("google-api-python-client がインストールされていません。pip install google-api-python-client を実行してください。")
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@handle_api_error
def list_sheets(token_path: str, sheet_id: str) -> dict:
    """スプレッドシートのシート（タブ）一覧を取得する

    Args:
        token_path: トークンファイルのパス
        sheet_id: スプレッドシートID

    Returns:
        シート一覧情報
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("sheets", "v4", credentials=creds)

    spreadsheet = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    title = spreadsheet.get("properties", {}).get("title", "")

    sheets = []
    for sheet in spreadsheet.get("sheets", []):
        props = sheet.get("properties", {})
        grid_props = props.get("gridProperties", {})
        sheets.append({
            "index": props.get("index", 0),
            "title": props.get("title", ""),
            "sheetId": props.get("sheetId", 0),
            "rowCount": grid_props.get("rowCount", 0),
            "columnCount": grid_props.get("columnCount", 0),
        })

    return {
        "id": sheet_id,
        "title": title,
        "sheetCount": len(sheets),
        "sheets": sheets,
        "url": f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    }


def _find_sheet_by_spec(sheets: list, sheet_spec: str) -> dict:
    """シート指定からシートを検索する共通ヘルパー関数

    Args:
        sheets: シート情報のリスト
        sheet_spec: シート指定（名前、インデックス番号）

    Returns:
        見つかったシート情報

    Raises:
        ValueError: シートが見つからない場合
    """
    if not sheets:
        raise ValueError("スプレッドシートにシートがありません。")

    # 数値の場合はインデックスとして扱う
    if sheet_spec.isdigit():
        index = int(sheet_spec)
        for sheet in sheets:
            if sheet["index"] == index:
                return sheet
        raise ValueError(f"インデックス {index} のシートが見つかりません。")

    # 名前で検索（完全一致）
    for sheet in sheets:
        if sheet["title"] == sheet_spec:
            return sheet

    # 名前で検索（部分一致、大文字小文字無視）
    sheet_spec_lower = sheet_spec.lower()
    for sheet in sheets:
        if sheet_spec_lower in sheet["title"].lower():
            return sheet

    # 見つからない場合
    sheet_names = [s["title"] for s in sheets]
    raise ValueError(f"シート '{sheet_spec}' が見つかりません。利用可能なシート: {', '.join(sheet_names)}")


def resolve_sheet_name(token_path: str, sheet_id: str, sheet_spec: str) -> str:
    """シート指定をシート名に解決する

    Args:
        token_path: トークンファイルのパス
        sheet_id: スプレッドシートID
        sheet_spec: シート指定（名前、インデックス番号、またはGID）

    Returns:
        シート名

    Raises:
        ValueError: シートが見つからない場合
    """
    sheets_info = list_sheets(token_path, sheet_id)
    sheets = sheets_info.get("sheets", [])
    sheet = _find_sheet_by_spec(sheets, sheet_spec)
    return sheet["title"]


def get_sheet_gid(token_path: str, sheet_id: str, sheet_spec: str) -> int:
    """シート指定からGIDを取得する

    Args:
        token_path: トークンファイルのパス
        sheet_id: スプレッドシートID
        sheet_spec: シート指定（名前、インデックス番号）

    Returns:
        シートのGID

    Raises:
        ValueError: シートが見つからない場合
    """
    sheets_info = list_sheets(token_path, sheet_id)
    sheets = sheets_info.get("sheets", [])
    sheet = _find_sheet_by_spec(sheets, sheet_spec)
    return sheet["sheetId"]


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


@retry_with_backoff()
@handle_api_error
def export_spreadsheet(
    token_path: str,
    sheet_id: str,
    output_path: str,
    mime_type: str = "text/csv",
    sheet_gid: int = None,
) -> dict:
    """スプレッドシートをエクスポートする

    Args:
        token_path: トークンファイルのパス
        sheet_id: スプレッドシートID
        output_path: 出力ファイルパス
        mime_type: 出力形式のMIMEタイプ
            - text/csv: CSV
            - application/vnd.openxmlformats-officedocument.spreadsheetml.sheet: Excel
            - application/pdf: PDF
            - application/vnd.oasis.opendocument.spreadsheet: ODS
            - text/tab-separated-values: TSV
        sheet_gid: エクスポートするシートのGID（CSV/TSVの場合のみ有効、省略時は最初のシート）

    Returns:
        エクスポート結果
    """
    import requests

    creds = load_credentials(token_path, SCOPES)
    drive_service = build("drive", "v3", credentials=creds)
    sheets_service = build("sheets", "v4", credentials=creds)

    # スプレッドシート名を取得
    spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    title = spreadsheet.get("properties", {}).get("title", "spreadsheet")

    # CSV/TSV で GID 指定がある場合は URL ベースでエクスポート
    if sheet_gid is not None and mime_type in ["text/csv", "text/tab-separated-values"]:
        # フォーマットを決定
        export_format = "csv" if mime_type == "text/csv" else "tsv"
        export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format={export_format}&gid={sheet_gid}"
        headers = {"Authorization": f"Bearer {creds.token}"}
        response = requests.get(export_url, headers=headers)
        response.raise_for_status()
        content = response.content
    else:
        # 通常の Drive API エクスポート
        content = drive_service.files().export(
            fileId=sheet_id,
            mimeType=mime_type
        ).execute()

    # ファイルに保存
    output_path = os.path.expanduser(output_path)
    with open(output_path, "wb") as f:
        f.write(content)

    # MIMEタイプからフォーマット名を判定
    format_name = {
        "text/csv": "CSV",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "Excel",
        "application/pdf": "PDF",
        "application/vnd.oasis.opendocument.spreadsheet": "ODS",
        "text/tab-separated-values": "TSV",
    }.get(mime_type, mime_type)

    return {
        "id": sheet_id,
        "title": title,
        "format": format_name,
        "outputPath": output_path,
        "fileSize": os.path.getsize(output_path),
    }


def main():
    # プロファイルヘッダーを表示
    print_profile_header()

    parser = argparse.ArgumentParser(description="Google Sheets 操作")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="出力形式")
    parser.add_argument("--token", help="トークンファイルパス（省略時はアクティブプロファイル）")

    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")

    # create コマンド
    create_parser = subparsers.add_parser("create", help="スプレッドシート作成")
    create_parser.add_argument("--name", required=True, help="スプレッドシート名")
    create_parser.add_argument("--folder-id", help="親フォルダID")

    # sheets コマンド（シート一覧取得）
    sheets_parser = subparsers.add_parser("sheets", help="シート（タブ）一覧取得")
    sheets_parser.add_argument("--sheet-id", required=True, help="スプレッドシートID")

    # get コマンド
    get_parser = subparsers.add_parser("get", help="データ取得")
    get_parser.add_argument("--sheet-id", required=True, help="スプレッドシートID")
    get_parser.add_argument("--range", help="取得範囲（例: A1:C10）")
    get_parser.add_argument("--sheet", help="シート名またはインデックス（例: '売上データ' または '0'）")

    # update コマンド
    update_parser = subparsers.add_parser("update", help="データ更新")
    update_parser.add_argument("--sheet-id", required=True, help="スプレッドシートID")
    update_parser.add_argument("--range", required=True, help="更新範囲（例: A1:B2）")
    update_parser.add_argument("--values", required=True, help="書き込むデータ（JSON配列）")
    update_parser.add_argument("--sheet", help="シート名またはインデックス（例: '売上データ' または '0'）")

    # append コマンド
    append_parser = subparsers.add_parser("append", help="行を末尾に追加")
    append_parser.add_argument("--sheet-id", required=True, help="スプレッドシートID")
    append_parser.add_argument("--range", default="Sheet1", help="追加先シート（デフォルト: Sheet1）")
    append_parser.add_argument("--values", required=True, help="追加するデータ（JSON配列）")
    append_parser.add_argument("--sheet", help="シート名またはインデックス（例: '売上データ' または '0'）")

    # export コマンド
    export_parser = subparsers.add_parser("export", help="スプレッドシートをエクスポート")
    export_parser.add_argument("--sheet-id", required=True, help="スプレッドシートID")
    export_parser.add_argument("--output", required=True, help="出力ファイルパス")
    export_parser.add_argument(
        "--type",
        choices=["csv", "xlsx", "pdf", "ods", "tsv"],
        default="csv",
        help="出力形式（デフォルト: csv）"
    )
    export_parser.add_argument("--sheet", help="エクスポートするシート名またはインデックス（CSV/TSVのみ有効）")

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

    elif args.command == "sheets":
        result = list_sheets(token_path, args.sheet_id)
        if args.format == "json":
            print_json([result])
        else:
            print(f"タイトル: {result['title']}")
            print(f"シート数: {result['sheetCount']}")
            print(f"URL: {result['url']}")
            print("-" * 40)
            for sheet in result['sheets']:
                print(f"  [{sheet['index']}] {sheet['title']} (GID: {sheet['sheetId']}, {sheet['rowCount']}行 x {sheet['columnCount']}列)")

    elif args.command == "get":
        # --sheet オプションがある場合、シート名を解決して範囲に追加
        range_str = args.range
        if hasattr(args, 'sheet') and args.sheet:
            try:
                sheet_name = resolve_sheet_name(token_path, args.sheet_id, args.sheet)
                if range_str:
                    # 範囲が指定されている場合、シート名を前に付ける
                    if '!' not in range_str:
                        range_str = f"'{sheet_name}'!{range_str}"
                else:
                    # 範囲が指定されていない場合、シート全体を取得
                    range_str = f"'{sheet_name}'"
            except ValueError as e:
                print_error(str(e))
                sys.exit(1)

        result = get_spreadsheet(token_path, args.sheet_id, range_str)
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

        # --sheet オプションがある場合、シート名を解決して範囲に追加
        range_str = args.range
        if hasattr(args, 'sheet') and args.sheet:
            try:
                sheet_name = resolve_sheet_name(token_path, args.sheet_id, args.sheet)
                if '!' not in range_str:
                    range_str = f"'{sheet_name}'!{range_str}"
            except ValueError as e:
                print_error(str(e))
                sys.exit(1)

        result = update_spreadsheet(token_path, args.sheet_id, range_str, values)
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

        # --sheet オプションがある場合、シート名を解決して範囲に追加
        range_str = args.range
        if hasattr(args, 'sheet') and args.sheet:
            try:
                sheet_name = resolve_sheet_name(token_path, args.sheet_id, args.sheet)
                range_str = f"'{sheet_name}'"
            except ValueError as e:
                print_error(str(e))
                sys.exit(1)

        result = append_spreadsheet(token_path, args.sheet_id, range_str, values)
        if args.format == "json":
            print_json([result])
        else:
            print(f"行を追加しました:")
            print(f"  追加先: {result['updatedRange']}")
            print(f"  追加行数: {result['updatedRows']}")
            print(f"  追加セル数: {result['updatedCells']}")
            print(f"  URL: {result['url']}")

    elif args.command == "export":
        # MIMEタイプのマッピング
        mime_types = {
            "csv": "text/csv",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "pdf": "application/pdf",
            "ods": "application/vnd.oasis.opendocument.spreadsheet",
            "tsv": "text/tab-separated-values",
        }
        mime_type = mime_types.get(args.type, "text/csv")

        # --sheet オプションがある場合、GIDを取得してURLに追加（CSV/TSVのみ）
        sheet_gid = None
        if hasattr(args, 'sheet') and args.sheet and args.type in ["csv", "tsv"]:
            try:
                sheet_gid = get_sheet_gid(token_path, args.sheet_id, args.sheet)
            except ValueError as e:
                print_error(str(e))
                sys.exit(1)

        result = export_spreadsheet(token_path, args.sheet_id, args.output, mime_type, sheet_gid)
        if args.format == "json":
            print_json([result])
        else:
            print(f"スプレッドシートをエクスポートしました:")
            print(f"  タイトル: {result['title']}")
            print(f"  形式: {result['format']}")
            print(f"  出力先: {result['outputPath']}")
            print(f"  ファイルサイズ: {result['fileSize']} bytes")


if __name__ == "__main__":
    main()
