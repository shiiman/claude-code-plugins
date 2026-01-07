#!/usr/bin/env python3
"""Google Slides API操作スクリプト

プレゼンテーションの作成・取得・更新を行う。

使用例:
    # プレゼンテーション作成
    python google_slides.py create --name "新規プレゼン"
    python google_slides.py create --name "テスト" --folder-id "xxx"

    # プレゼンテーション取得
    python google_slides.py get --presentation-id "xxx"

    # スライド追加
    python google_slides.py add-slide --presentation-id "xxx" --title "新しいスライド" --body "本文テキスト"
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
)

try:
    from googleapiclient.discovery import build
except ImportError:
    print_error("google-api-python-client がインストールされていません。pip install google-api-python-client を実行してください。")
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive.file",
]


@handle_api_error
def create_presentation(token_path: str, name: str, folder_id: str = None) -> dict:
    """新規プレゼンテーションを作成する

    Args:
        token_path: トークンファイルのパス
        name: プレゼンテーション名
        folder_id: 親フォルダID（省略時はマイドライブ）

    Returns:
        作成したプレゼンテーション情報
    """
    creds = load_credentials(token_path, SCOPES)
    slides_service = build("slides", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    # プレゼンテーション作成
    presentation = slides_service.presentations().create(
        body={"title": name}
    ).execute()
    presentation_id = presentation["presentationId"]

    # フォルダに移動（指定がある場合）
    if folder_id:
        file = drive_service.files().get(fileId=presentation_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents", []))
        drive_service.files().update(
            fileId=presentation_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields="id, parents"
        ).execute()

    return {
        "id": presentation_id,
        "name": name,
        "url": f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    }


@handle_api_error
def get_presentation(token_path: str, presentation_id: str) -> dict:
    """プレゼンテーションの情報を取得する

    Args:
        token_path: トークンファイルのパス
        presentation_id: プレゼンテーションID

    Returns:
        プレゼンテーション情報
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("slides", "v1", credentials=creds)

    presentation = service.presentations().get(presentationId=presentation_id).execute()

    slides = []
    for slide in presentation.get("slides", []):
        slide_info = {
            "objectId": slide.get("objectId"),
            "texts": []
        }
        # テキスト内容を抽出
        for element in slide.get("pageElements", []):
            if "shape" in element and "text" in element.get("shape", {}):
                text_content = ""
                for text_element in element["shape"]["text"].get("textElements", []):
                    if "textRun" in text_element:
                        text_content += text_element["textRun"].get("content", "")
                if text_content.strip():
                    slide_info["texts"].append(text_content.strip())
        slides.append(slide_info)

    return {
        "id": presentation_id,
        "title": presentation.get("title", ""),
        "slideCount": len(slides),
        "slides": slides,
        "url": f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    }


@handle_api_error
def add_slide(token_path: str, presentation_id: str, title: str = None, body: str = None, layout: str = "BLANK") -> dict:
    """プレゼンテーションにスライドを追加する

    Args:
        token_path: トークンファイルのパス
        presentation_id: プレゼンテーションID
        title: スライドタイトル
        body: スライド本文
        layout: レイアウト種別（BLANK, TITLE, TITLE_AND_BODY など）

    Returns:
        追加結果
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("slides", "v1", credentials=creds)

    # スライドを追加
    requests = [
        {
            "createSlide": {
                "slideLayoutReference": {
                    "predefinedLayout": layout
                }
            }
        }
    ]

    result = service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests}
    ).execute()

    slide_id = result.get("replies", [{}])[0].get("createSlide", {}).get("objectId")

    # テキストを追加（タイトルまたは本文がある場合）
    if slide_id and (title or body):
        # スライドの情報を取得してテキストボックスのIDを特定
        presentation = service.presentations().get(presentationId=presentation_id).execute()

        text_requests = []
        for slide in presentation.get("slides", []):
            if slide.get("objectId") == slide_id:
                for element in slide.get("pageElements", []):
                    shape = element.get("shape", {})
                    placeholder = shape.get("placeholder", {})
                    element_id = element.get("objectId")

                    if placeholder.get("type") == "TITLE" and title:
                        text_requests.append({
                            "insertText": {
                                "objectId": element_id,
                                "text": title
                            }
                        })
                    elif placeholder.get("type") == "BODY" and body:
                        text_requests.append({
                            "insertText": {
                                "objectId": element_id,
                                "text": body
                            }
                        })

        if text_requests:
            service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={"requests": text_requests}
            ).execute()

    return {
        "id": presentation_id,
        "slideId": slide_id,
        "status": "slide_added",
        "url": f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    }


def main():
    parser = argparse.ArgumentParser(description="Google Slides 操作")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="出力形式")
    parser.add_argument("--token", help="トークンファイルパス（省略時はアクティブプロファイル）")

    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")

    # create コマンド
    create_parser = subparsers.add_parser("create", help="プレゼンテーション作成")
    create_parser.add_argument("--name", required=True, help="プレゼンテーション名")
    create_parser.add_argument("--folder-id", help="親フォルダID")

    # get コマンド
    get_parser = subparsers.add_parser("get", help="プレゼンテーション取得")
    get_parser.add_argument("--presentation-id", required=True, help="プレゼンテーションID")

    # add-slide コマンド
    add_slide_parser = subparsers.add_parser("add-slide", help="スライド追加")
    add_slide_parser.add_argument("--presentation-id", required=True, help="プレゼンテーションID")
    add_slide_parser.add_argument("--title", help="スライドタイトル")
    add_slide_parser.add_argument("--body", help="スライド本文")
    add_slide_parser.add_argument("--layout", default="TITLE_AND_BODY",
                                   choices=["BLANK", "TITLE", "TITLE_AND_BODY", "TITLE_AND_TWO_COLUMNS"],
                                   help="レイアウト種別")

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
        result = create_presentation(token_path, args.name, args.folder_id)
        if args.format == "json":
            print_json([result])
        else:
            print(f"プレゼンテーションを作成しました:")
            print(f"  ID: {result['id']}")
            print(f"  名前: {result['name']}")
            print(f"  URL: {result['url']}")

    elif args.command == "get":
        result = get_presentation(token_path, args.presentation_id)
        if args.format == "json":
            print_json([result])
        else:
            print(f"タイトル: {result['title']}")
            print(f"スライド数: {result['slideCount']}")
            print(f"URL: {result['url']}")
            print("-" * 40)
            for i, slide in enumerate(result['slides'], 1):
                print(f"スライド {i} (ID: {slide['objectId']}):")
                for text in slide['texts']:
                    print(f"  - {text[:100]}{'...' if len(text) > 100 else ''}")
                if not slide['texts']:
                    print("  (テキストなし)")

    elif args.command == "add-slide":
        result = add_slide(token_path, args.presentation_id, args.title, args.body, args.layout)
        if args.format == "json":
            print_json([result])
        else:
            print(f"スライドを追加しました:")
            print(f"  プレゼンテーションID: {result['id']}")
            print(f"  スライドID: {result['slideId']}")
            print(f"  URL: {result['url']}")


if __name__ == "__main__":
    main()
