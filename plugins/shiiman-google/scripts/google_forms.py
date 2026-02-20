#!/usr/bin/env python3
"""Google Forms API操作スクリプト

フォームの作成・取得・更新・回答取得を行う。

使用例:
    # フォーム作成
    python google_forms.py create --name "新規フォーム"
    python google_forms.py create --name "テスト" --description "テスト用フォーム"

    # フォーム取得
    python google_forms.py get --form-id "xxx"

    # 質問追加
    python google_forms.py add-question --form-id "xxx" --question "お名前は？" --type TEXT
    python google_forms.py add-question --form-id "xxx" --question "好きな色は？" --type RADIO --options "赤,青,緑"

    # 回答取得
    python google_forms.py responses --form-id "xxx"
    python google_forms.py responses --form-id "xxx" --max 100
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
    retry_with_backoff,
)

try:
    from googleapiclient.discovery import build
except ImportError:
    print_error("google-api-python-client がインストールされていません。pip install google-api-python-client を実行してください。")
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/drive",
]


@handle_api_error
def create_form(token_path: str, name: str, description: str = None) -> dict:
    """新規フォームを作成する

    Args:
        token_path: トークンファイルのパス
        name: フォーム名
        description: フォームの説明

    Returns:
        作成したフォーム情報
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("forms", "v1", credentials=creds)

    # フォーム作成
    form = service.forms().create(
        body={"info": {"title": name}}
    ).execute()
    form_id = form["formId"]

    # 説明を追加
    if description:
        service.forms().batchUpdate(
            formId=form_id,
            body={
                "requests": [{
                    "updateFormInfo": {
                        "info": {"description": description},
                        "updateMask": "description"
                    }
                }]
            }
        ).execute()

    return {
        "id": form_id,
        "name": name,
        "description": description or "",
        "editUrl": f"https://docs.google.com/forms/d/{form_id}/edit",
        "responseUrl": f"https://docs.google.com/forms/d/{form_id}/viewform"
    }


@handle_api_error
def get_form(token_path: str, form_id: str) -> dict:
    """フォームの情報を取得する

    Args:
        token_path: トークンファイルのパス
        form_id: フォームID

    Returns:
        フォーム情報
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("forms", "v1", credentials=creds)

    form = service.forms().get(formId=form_id).execute()

    questions = []
    for item in form.get("items", []):
        question_info = {
            "itemId": item.get("itemId"),
            "title": item.get("title", ""),
        }
        if "questionItem" in item:
            question = item["questionItem"].get("question", {})
            question_info["required"] = question.get("required", False)
            if "textQuestion" in question:
                question_info["type"] = "TEXT"
            elif "choiceQuestion" in question:
                choice = question["choiceQuestion"]
                question_info["type"] = choice.get("type", "RADIO")
                question_info["options"] = [opt.get("value", "") for opt in choice.get("options", [])]
            elif "scaleQuestion" in question:
                question_info["type"] = "SCALE"
            elif "dateQuestion" in question:
                question_info["type"] = "DATE"
            elif "timeQuestion" in question:
                question_info["type"] = "TIME"
        questions.append(question_info)

    return {
        "id": form_id,
        "title": form.get("info", {}).get("title", ""),
        "description": form.get("info", {}).get("description", ""),
        "questionCount": len(questions),
        "questions": questions,
        "editUrl": f"https://docs.google.com/forms/d/{form_id}/edit",
        "responseUrl": f"https://docs.google.com/forms/d/{form_id}/viewform"
    }


@handle_api_error
def add_question(token_path: str, form_id: str, question: str, question_type: str,
                 options: list = None, required: bool = False) -> dict:
    """フォームに質問を追加する

    Args:
        token_path: トークンファイルのパス
        form_id: フォームID
        question: 質問文
        question_type: 質問タイプ（TEXT, RADIO, CHECKBOX, DROP_DOWN, SCALE, DATE, TIME）
        options: 選択肢（RADIO, CHECKBOX, DROP_DOWN の場合）
        required: 必須かどうか

    Returns:
        追加結果
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("forms", "v1", credentials=creds)

    # 質問アイテム構築
    question_item = {
        "question": {
            "required": required
        }
    }

    normalized_type = "DROP_DOWN" if question_type == "DROPDOWN" else question_type

    if normalized_type == "TEXT":
        question_item["question"]["textQuestion"] = {"paragraph": False}
    elif normalized_type == "PARAGRAPH":
        question_item["question"]["textQuestion"] = {"paragraph": True}
    elif normalized_type in ["RADIO", "CHECKBOX", "DROP_DOWN"]:
        if not options:
            print_error(f"{normalized_type} タイプには --options が必要です")
            sys.exit(1)
        question_item["question"]["choiceQuestion"] = {
            "type": normalized_type,
            "options": [{"value": opt} for opt in options]
        }
    elif normalized_type == "SCALE":
        question_item["question"]["scaleQuestion"] = {
            "low": 1,
            "high": 5
        }
    elif normalized_type == "DATE":
        question_item["question"]["dateQuestion"] = {}
    elif normalized_type == "TIME":
        question_item["question"]["timeQuestion"] = {}
    else:
        print_error(f"不明な質問タイプ: {question_type}")
        sys.exit(1)

    # フォーム更新
    result = service.forms().batchUpdate(
        formId=form_id,
        body={
            "requests": [{
                "createItem": {
                    "item": {
                        "title": question,
                        "questionItem": question_item
                    },
                    "location": {"index": 0}
                }
            }]
        }
    ).execute()

    return {
        "id": form_id,
        "status": "question_added",
        "question": question,
        "type": normalized_type,
        "editUrl": f"https://docs.google.com/forms/d/{form_id}/edit"
    }


@retry_with_backoff()
@handle_api_error
def get_responses(token_path: str, form_id: str, max_results: int = 50) -> dict:
    """フォームの回答を取得する

    Args:
        token_path: トークンファイルのパス
        form_id: フォームID
        max_results: 最大取得件数

    Returns:
        回答情報
    """
    creds = load_credentials(token_path, SCOPES)
    service = build("forms", "v1", credentials=creds)

    # フォーム情報を取得
    form = service.forms().get(formId=form_id).execute()
    form_title = form.get("info", {}).get("title", "")

    # 質問IDと質問文のマッピングを作成
    question_map = {}
    for item in form.get("items", []):
        if "questionItem" in item:
            question_id = item["questionItem"]["question"].get("questionId")
            if question_id:
                question_map[question_id] = item.get("title", "")

    # 回答を取得
    responses_result = service.forms().responses().list(
        formId=form_id,
        pageSize=max_results
    ).execute()

    responses = []
    for response in responses_result.get("responses", []):
        response_data = {
            "responseId": response.get("responseId"),
            "createTime": response.get("createTime"),
            "lastSubmittedTime": response.get("lastSubmittedTime"),
            "answers": []
        }

        # 各回答を処理
        for question_id, answer_data in response.get("answers", {}).items():
            question_text = question_map.get(question_id, question_id)
            text_answers = answer_data.get("textAnswers", {}).get("answers", [])
            answer_values = [a.get("value", "") for a in text_answers]

            response_data["answers"].append({
                "question": question_text,
                "questionId": question_id,
                "values": answer_values
            })

        responses.append(response_data)

    return {
        "formId": form_id,
        "formTitle": form_title,
        "responseCount": len(responses),
        "responses": responses,
        "editUrl": f"https://docs.google.com/forms/d/{form_id}/edit",
        "responsesUrl": f"https://docs.google.com/forms/d/{form_id}/edit#responses"
    }


def main():
    # プロファイルヘッダーを表示
    print_profile_header()

    parser = argparse.ArgumentParser(description="Google Forms 操作")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="出力形式")
    parser.add_argument("--token", help="トークンファイルパス（省略時はアクティブプロファイル）")
    parser.add_argument("--profile", help="認証プロファイル名（デフォルト: アクティブプロファイル）")

    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")

    # create コマンド
    create_parser = subparsers.add_parser("create", help="フォーム作成")
    create_parser.add_argument("--name", required=True, help="フォーム名")
    create_parser.add_argument("--description", help="フォームの説明")

    # get コマンド
    get_parser = subparsers.add_parser("get", help="フォーム取得")
    get_parser.add_argument("--form-id", required=True, help="フォームID")

    # add-question コマンド
    add_question_parser = subparsers.add_parser("add-question", help="質問追加")
    add_question_parser.add_argument("--form-id", required=True, help="フォームID")
    add_question_parser.add_argument("--question", required=True, help="質問文")
    add_question_parser.add_argument("--type", required=True,
                                      choices=["TEXT", "PARAGRAPH", "RADIO", "CHECKBOX", "DROP_DOWN", "DROPDOWN", "SCALE", "DATE", "TIME"],
                                      help="質問タイプ")
    add_question_parser.add_argument("--options", help="選択肢（カンマ区切り）")
    add_question_parser.add_argument("--required", action="store_true", help="必須にする")

    # responses コマンド
    responses_parser = subparsers.add_parser("responses", help="回答取得")
    responses_parser.add_argument("--form-id", required=True, help="フォームID")
    responses_parser.add_argument("--max", type=int, default=50, help="最大取得件数（デフォルト: 50）")

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
        result = create_form(token_path, args.name, args.description)
        if args.format == "json":
            print_json([result])
        else:
            print(f"フォームを作成しました:")
            print(f"  ID: {result['id']}")
            print(f"  名前: {result['name']}")
            print(f"  編集URL: {result['editUrl']}")
            print(f"  回答URL: {result['responseUrl']}")

    elif args.command == "get":
        result = get_form(token_path, args.form_id)
        if args.format == "json":
            print_json([result])
        else:
            print(f"タイトル: {result['title']}")
            print(f"説明: {result['description']}")
            print(f"質問数: {result['questionCount']}")
            print(f"編集URL: {result['editUrl']}")
            print(f"回答URL: {result['responseUrl']}")
            print("-" * 40)
            for i, q in enumerate(result['questions'], 1):
                required = "（必須）" if q.get('required') else ""
                print(f"{i}. {q['title']} [{q.get('type', 'N/A')}]{required}")
                if 'options' in q:
                    for opt in q['options']:
                        print(f"   - {opt}")

    elif args.command == "add-question":
        options = args.options.split(",") if args.options else None
        result = add_question(token_path, args.form_id, args.question, args.type, options, args.required)
        if args.format == "json":
            print_json([result])
        else:
            print(f"質問を追加しました:")
            print(f"  フォームID: {result['id']}")
            print(f"  質問: {result['question']}")
            print(f"  タイプ: {result['type']}")
            print(f"  編集URL: {result['editUrl']}")

    elif args.command == "responses":
        result = get_responses(token_path, args.form_id, args.max)
        if args.format == "json":
            print_json([result])
        else:
            print(f"フォーム: {result['formTitle']}")
            print(f"回答数: {result['responseCount']}")
            print(f"回答URL: {result['responsesUrl']}")
            print("-" * 40)
            for i, response in enumerate(result['responses'], 1):
                print(f"\n回答 {i} ({response['lastSubmittedTime']}):")
                for answer in response['answers']:
                    values = ", ".join(answer['values']) if answer['values'] else "(未回答)"
                    print(f"  Q: {answer['question']}")
                    print(f"  A: {values}")


if __name__ == "__main__":
    main()
