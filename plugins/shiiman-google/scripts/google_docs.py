#!/usr/bin/env python3
"""Google Docs API操作スクリプト

ドキュメントの作成・取得・更新・エクスポートを行う。

使用例:
    # ドキュメント作成
    python google_docs.py create --name "新規ドキュメント"
    python google_docs.py create --name "テスト" --folder-id "xxx" --content "初期内容"

    # ドキュメント取得（テキスト形式）
    python google_docs.py get --doc-id "xxx"

    # ドキュメント更新
    python google_docs.py update --doc-id "xxx" --content "追加テキスト"
    python google_docs.py update --doc-id "xxx" --content "追加テキスト" --append

    # PDFエクスポート
    python google_docs.py export --doc-id "xxx" --output "document.pdf"
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
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]


@handle_api_error
def create_document(token_path: str, name: str, folder_id: str = None, content: str = None) -> dict:
    """新規ドキュメントを作成する

    Args:
        token_path: トークンファイルのパス
        name: ドキュメント名
        folder_id: 親フォルダID（省略時はマイドライブ）
        content: 初期内容（省略時は空）

    Returns:
        作成したドキュメント情報
    """
    creds = load_credentials(token_path, SCOPES)
    docs_service = build("docs", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    # ドキュメント作成
    doc = docs_service.documents().create(body={"title": name}).execute()
    doc_id = doc["documentId"]

    # フォルダに移動（指定がある場合）
    if folder_id:
        file = drive_service.files().get(fileId=doc_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents", []))
        drive_service.files().update(
            fileId=doc_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields="id, parents"
        ).execute()

    # 初期内容を挿入
    if content:
        requests = [
            {
                "insertText": {
                    "location": {"index": 1},
                    "text": content
                }
            }
        ]
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": requests}
        ).execute()

    return {
        "id": doc_id,
        "name": name,
        "url": f"https://docs.google.com/document/d/{doc_id}/edit"
    }


@handle_api_error
def get_document(token_path: str, doc_id: str) -> dict:
    """ドキュメントの内容を取得する

    Args:
        token_path: トークンファイルのパス
        doc_id: ドキュメントID

    Returns:
        ドキュメント情報とテキスト内容
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("docs", "v1", credentials=creds)

    doc = service.documents().get(documentId=doc_id).execute()

    # テキスト内容を抽出
    content_text = ""
    for element in doc.get("body", {}).get("content", []):
        if "paragraph" in element:
            for text_run in element["paragraph"].get("elements", []):
                if "textRun" in text_run:
                    content_text += text_run["textRun"].get("content", "")

    return {
        "id": doc_id,
        "title": doc.get("title", ""),
        "content": content_text,
        "url": f"https://docs.google.com/document/d/{doc_id}/edit"
    }


@handle_api_error
def update_document(token_path: str, doc_id: str, content: str, append: bool = False) -> dict:
    """ドキュメントを更新する

    Args:
        token_path: トークンファイルのパス
        doc_id: ドキュメントID
        content: 挿入するテキスト
        append: True の場合は末尾に追加、False の場合は先頭に挿入

    Returns:
        更新結果
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("docs", "v1", credentials=creds)

    if append:
        # 末尾に追加する場合、まずドキュメントの長さを取得
        doc = service.documents().get(documentId=doc_id).execute()
        end_index = doc.get("body", {}).get("content", [{}])[-1].get("endIndex", 1) - 1

        requests = [
            {
                "insertText": {
                    "location": {"index": end_index},
                    "text": content
                }
            }
        ]
    else:
        # 先頭に挿入
        requests = [
            {
                "insertText": {
                    "location": {"index": 1},
                    "text": content
                }
            }
        ]

    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": requests}
    ).execute()

    return {
        "id": doc_id,
        "status": "updated",
        "mode": "append" if append else "prepend",
        "url": f"https://docs.google.com/document/d/{doc_id}/edit"
    }


@retry_with_backoff()
@handle_api_error
def export_document(token_path: str, doc_id: str, output_path: str, mime_type: str = "application/pdf") -> dict:
    """ドキュメントをエクスポートする

    Args:
        token_path: トークンファイルのパス
        doc_id: ドキュメントID
        output_path: 出力ファイルパス
        mime_type: 出力形式のMIMEタイプ
            - application/pdf: PDF
            - application/vnd.openxmlformats-officedocument.wordprocessingml.document: Word
            - text/plain: プレーンテキスト
            - text/html: HTML
            - application/rtf: RTF
            - application/epub+zip: EPUB

    Returns:
        エクスポート結果
    """
    creds = load_credentials(token_path, SCOPES)
    drive_service = build("drive", "v3", credentials=creds)
    docs_service = build("docs", "v1", credentials=creds)

    # ドキュメント名を取得
    doc = docs_service.documents().get(documentId=doc_id).execute()
    doc_title = doc.get("title", "document")

    # エクスポート実行
    content = drive_service.files().export(
        fileId=doc_id,
        mimeType=mime_type
    ).execute()

    # ファイルに保存
    output_path = os.path.expanduser(output_path)
    with open(output_path, "wb") as f:
        f.write(content)

    # MIMEタイプから拡張子を判定
    format_name = {
        "application/pdf": "PDF",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "Word",
        "text/plain": "テキスト",
        "text/html": "HTML",
        "application/rtf": "RTF",
        "application/epub+zip": "EPUB",
    }.get(mime_type, mime_type)

    return {
        "id": doc_id,
        "title": doc_title,
        "format": format_name,
        "outputPath": output_path,
        "fileSize": os.path.getsize(output_path),
    }


def main():
    parser = argparse.ArgumentParser(description="Google Docs 操作")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="出力形式")
    parser.add_argument("--token", help="トークンファイルパス（省略時はアクティブプロファイル）")

    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")

    # create コマンド
    create_parser = subparsers.add_parser("create", help="ドキュメント作成")
    create_parser.add_argument("--name", required=True, help="ドキュメント名")
    create_parser.add_argument("--folder-id", help="親フォルダID")
    create_parser.add_argument("--content", help="初期内容")

    # get コマンド
    get_parser = subparsers.add_parser("get", help="ドキュメント取得")
    get_parser.add_argument("--doc-id", required=True, help="ドキュメントID")

    # update コマンド
    update_parser = subparsers.add_parser("update", help="ドキュメント更新")
    update_parser.add_argument("--doc-id", required=True, help="ドキュメントID")
    update_parser.add_argument("--content", required=True, help="挿入するテキスト")
    update_parser.add_argument("--append", action="store_true", help="末尾に追加（省略時は先頭に挿入）")

    # export コマンド
    export_parser = subparsers.add_parser("export", help="ドキュメントをエクスポート")
    export_parser.add_argument("--doc-id", required=True, help="ドキュメントID")
    export_parser.add_argument("--output", required=True, help="出力ファイルパス")
    export_parser.add_argument(
        "--type",
        choices=["pdf", "docx", "txt", "html", "rtf", "epub"],
        default="pdf",
        help="出力形式（デフォルト: pdf）"
    )

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
        result = create_document(token_path, args.name, args.folder_id, args.content)
        if args.format == "json":
            print_json([result])
        else:
            print(f"ドキュメントを作成しました:")
            print(f"  ID: {result['id']}")
            print(f"  名前: {result['name']}")
            print(f"  URL: {result['url']}")

    elif args.command == "get":
        result = get_document(token_path, args.doc_id)
        if args.format == "json":
            print_json([result])
        else:
            print(f"タイトル: {result['title']}")
            print(f"URL: {result['url']}")
            print("-" * 40)
            print(result['content'])

    elif args.command == "update":
        result = update_document(token_path, args.doc_id, args.content, args.append)
        if args.format == "json":
            print_json([result])
        else:
            print(f"ドキュメントを更新しました:")
            print(f"  ID: {result['id']}")
            print(f"  モード: {'末尾追加' if result['mode'] == 'append' else '先頭挿入'}")
            print(f"  URL: {result['url']}")

    elif args.command == "export":
        # MIMEタイプのマッピング
        mime_types = {
            "pdf": "application/pdf",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "txt": "text/plain",
            "html": "text/html",
            "rtf": "application/rtf",
            "epub": "application/epub+zip",
        }
        mime_type = mime_types.get(args.type, "application/pdf")

        result = export_document(token_path, args.doc_id, args.output, mime_type)
        if args.format == "json":
            print_json([result])
        else:
            print(f"ドキュメントをエクスポートしました:")
            print(f"  タイトル: {result['title']}")
            print(f"  形式: {result['format']}")
            print(f"  出力先: {result['outputPath']}")
            print(f"  ファイルサイズ: {result['fileSize']} bytes")


if __name__ == "__main__":
    main()
