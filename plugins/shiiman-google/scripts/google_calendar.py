"""Calendar helpers for shiiman-google."""

import argparse
import datetime as dt
import json
from typing import List, Tuple

from googleapiclient.discovery import build

from google_utils import (
    format_output,
    get_token_path,
    handle_api_error,
    load_credentials,
    print_json,
    retry_with_backoff,
)

# 読み書き両方可能なスコープに変更
DEFAULT_SCOPES = ["https://www.googleapis.com/auth/calendar"]

# カレンダーイベントの色ID
COLOR_MAP = {
    1: "ラベンダー",
    2: "セージ",
    3: "ぶどう",
    4: "フラミンゴ",
    5: "バナナ",
    6: "みかん",
    7: "ピーコック",
    8: "グラファイト",
    9: "ブルーベリー",
    10: "バジル",
    11: "トマト",
}


def _get_service(token_path: str):
    """Calendar サービスを取得する。"""
    creds = load_credentials(token_path, DEFAULT_SCOPES)
    return build("calendar", "v3", credentials=creds)


def _range_for(period: str) -> Tuple[str, str]:
    """期間文字列から開始・終了日時を取得する。

    Args:
        period: "today", "week", "month"

    Returns:
        (time_min, time_max) のタプル（ISO形式文字列）
    """
    now = dt.datetime.now(dt.timezone.utc)

    if period == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + dt.timedelta(days=1)
    elif period == "week":
        # 週の始まりを月曜日に
        start = now - dt.timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + dt.timedelta(days=7)
    elif period == "month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # 翌月の初日を計算
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1)
        else:
            end = start.replace(month=start.month + 1)
    else:
        # デフォルトは今日
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + dt.timedelta(days=1)

    return start.isoformat(), end.isoformat()


def list_events(
    token_path: str,
    period: str = "today",
    calendar_id: str = "primary",
    max_results: int = 50,
) -> List[dict]:
    """指定期間のイベント一覧を取得する。

    Args:
        token_path: トークンファイルパス
        period: 期間 ("today", "week", "month")
        calendar_id: カレンダーID（デフォルト: primary）
        max_results: 最大取得件数

    Returns:
        イベントのリスト
    """
    service = _get_service(token_path)
    time_min, time_max = _range_for(period)

    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    results = []
    for event in events:
        start = event.get("start", {})
        end = event.get("end", {})

        # 終日イベントは date、時間指定は dateTime
        start_str = start.get("dateTime", start.get("date", ""))
        end_str = end.get("dateTime", end.get("date", ""))

        results.append(
            {
                "id": event.get("id", ""),
                "start": start_str,
                "end": end_str,
                "summary": event.get("summary", ""),
                "location": event.get("location", ""),
                "url": event.get("htmlLink", ""),
            }
        )

    return results


@retry_with_backoff()
@handle_api_error
def list_all_events(
    token_path: str,
    period: str = "today",
    max_results: int = 50,
) -> List[dict]:
    """全カレンダーから指定期間のイベント一覧を取得する。

    Args:
        token_path: トークンファイルパス
        period: 期間 ("today", "week", "month")
        max_results: 最大取得件数（カレンダーごと）

    Returns:
        イベントのリスト（開始時間順にソート）
    """
    calendars = list_calendars(token_path)
    all_events = []

    for cal in calendars:
        # owner または writer 権限のカレンダーのみ取得
        if cal["accessRole"] in ["owner", "writer"]:
            events = list_events(token_path, period, cal["id"], max_results)
            for event in events:
                event["calendar"] = cal["summary"]
                all_events.append(event)

    # 開始時間でソート
    all_events.sort(key=lambda x: x["start"])

    return all_events


def list_calendars(token_path: str) -> List[dict]:
    """利用可能なカレンダー一覧を取得する。

    Args:
        token_path: トークンファイルパス

    Returns:
        カレンダーのリスト
    """
    service = _get_service(token_path)

    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get("items", [])

    results = []
    for cal in calendars:
        results.append(
            {
                "id": cal.get("id", ""),
                "summary": cal.get("summary", ""),
                "primary": cal.get("primary", False),
                "accessRole": cal.get("accessRole", ""),
                "backgroundColor": cal.get("backgroundColor", ""),
            }
        )

    return results


@retry_with_backoff()
@handle_api_error
def get_event(
    token_path: str,
    event_id: str,
    calendar_id: str = "primary",
) -> dict:
    """イベントの詳細を取得する。

    Args:
        token_path: トークンファイルパス
        event_id: イベントID
        calendar_id: カレンダーID（デフォルト: primary）

    Returns:
        イベント情報
    """
    service = _get_service(token_path)

    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

    start = event.get("start", {})
    end = event.get("end", {})
    start_str = start.get("dateTime", start.get("date", ""))
    end_str = end.get("dateTime", end.get("date", ""))

    return {
        "id": event.get("id", ""),
        "summary": event.get("summary", ""),
        "start": start_str,
        "end": end_str,
        "location": event.get("location", ""),
        "description": event.get("description", ""),
        "url": event.get("htmlLink", ""),
    }


def create_event(
    token_path: str,
    summary: str,
    start: str,
    end: str,
    calendar_id: str = "primary",
    color_id: int = None,
    location: str = None,
    description: str = None,
    all_day: bool = False,
) -> dict:
    """カレンダーに予定を追加する。

    Args:
        token_path: トークンファイルパス
        summary: 予定タイトル
        start: 開始日時（ISO 8601形式: 2025-01-08T14:00:00 または 2025-01-08）
        end: 終了日時（ISO 8601形式: 2025-01-08T15:00:00 または 2025-01-08）
        calendar_id: カレンダーID（デフォルト: primary）
        color_id: 色ID（1-11）
        location: 場所
        description: 説明
        all_day: 終日イベントかどうか

    Returns:
        作成したイベント情報
    """
    service = _get_service(token_path)

    # イベントボディを構築
    event_body = {
        "summary": summary,
    }

    # 終日イベントの場合
    if all_day or "T" not in start:
        event_body["start"] = {"date": start.split("T")[0]}
        event_body["end"] = {"date": end.split("T")[0]}
    else:
        # タイムゾーンを取得（ローカルタイムゾーン）
        local_tz = dt.datetime.now().astimezone().tzinfo
        tz_name = str(local_tz)

        event_body["start"] = {"dateTime": start, "timeZone": tz_name}
        event_body["end"] = {"dateTime": end, "timeZone": tz_name}

    if color_id and 1 <= color_id <= 11:
        event_body["colorId"] = str(color_id)

    if location:
        event_body["location"] = location

    if description:
        event_body["description"] = description

    event = service.events().insert(calendarId=calendar_id, body=event_body).execute()

    return {
        "id": event.get("id", ""),
        "summary": event.get("summary", ""),
        "start": event.get("start", {}).get("dateTime", event.get("start", {}).get("date", "")),
        "end": event.get("end", {}).get("dateTime", event.get("end", {}).get("date", "")),
        "location": event.get("location", ""),
        "url": event.get("htmlLink", ""),
        "status": "created",
    }


@retry_with_backoff()
@handle_api_error
def update_event(
    token_path: str,
    event_id: str,
    calendar_id: str = "primary",
    summary: str = None,
    start: str = None,
    end: str = None,
    location: str = None,
    description: str = None,
    color_id: int = None,
) -> dict:
    """イベントを更新する。

    Args:
        token_path: トークンファイルパス
        event_id: イベントID
        calendar_id: カレンダーID（デフォルト: primary）
        summary: 新しいタイトル（省略時は変更なし）
        start: 新しい開始日時（省略時は変更なし）
        end: 新しい終了日時（省略時は変更なし）
        location: 新しい場所（省略時は変更なし）
        description: 新しい説明（省略時は変更なし）
        color_id: 新しい色ID（省略時は変更なし）

    Returns:
        更新されたイベント情報
    """
    service = _get_service(token_path)

    # 現在のイベント情報を取得
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

    # 更新する項目だけ変更
    if summary is not None:
        event["summary"] = summary

    if location is not None:
        event["location"] = location

    if description is not None:
        event["description"] = description

    if color_id is not None and 1 <= color_id <= 11:
        event["colorId"] = str(color_id)

    # 日時の更新
    if start is not None:
        # 終日イベントかどうか判定
        if "T" not in start:
            event["start"] = {"date": start.split("T")[0]}
        else:
            local_tz = dt.datetime.now().astimezone().tzinfo
            tz_name = str(local_tz)
            event["start"] = {"dateTime": start, "timeZone": tz_name}

    if end is not None:
        if "T" not in end:
            event["end"] = {"date": end.split("T")[0]}
        else:
            local_tz = dt.datetime.now().astimezone().tzinfo
            tz_name = str(local_tz)
            event["end"] = {"dateTime": end, "timeZone": tz_name}

    # 更新を実行
    updated_event = (
        service.events()
        .update(calendarId=calendar_id, eventId=event_id, body=event)
        .execute()
    )

    return {
        "id": updated_event.get("id", ""),
        "summary": updated_event.get("summary", ""),
        "start": updated_event.get("start", {}).get("dateTime", updated_event.get("start", {}).get("date", "")),
        "end": updated_event.get("end", {}).get("dateTime", updated_event.get("end", {}).get("date", "")),
        "location": updated_event.get("location", ""),
        "url": updated_event.get("htmlLink", ""),
        "status": "updated",
    }


@retry_with_backoff()
@handle_api_error
def delete_event(
    token_path: str,
    event_id: str,
    calendar_id: str = "primary",
) -> dict:
    """イベントを削除する。

    Args:
        token_path: トークンファイルパス
        event_id: イベントID
        calendar_id: カレンダーID（デフォルト: primary）

    Returns:
        削除結果
    """
    service = _get_service(token_path)

    # まずイベント情報を取得（削除前に情報を保存）
    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        event_summary = event.get("summary", "")
    except Exception:
        event_summary = ""

    # 削除を実行
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

    return {
        "id": event_id,
        "summary": event_summary,
        "status": "deleted",
    }


@handle_api_error
def main() -> None:
    parser = argparse.ArgumentParser(description="Google Calendar 操作ツール")
    parser.add_argument("--token", help="トークンファイルパス")
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="出力形式 (デフォルト: table)",
    )

    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")

    # events サブコマンド（デフォルト動作）
    events_parser = subparsers.add_parser("events", help="予定一覧を取得")
    events_parser.add_argument(
        "--range",
        choices=["today", "week", "month"],
        default="today",
        help="期間 (デフォルト: today)",
    )
    events_parser.add_argument(
        "--calendar",
        default="all",
        help="カレンダーID (デフォルト: all=全カレンダー, primary=メインのみ)",
    )
    events_parser.add_argument(
        "--max",
        type=int,
        default=50,
        help="最大取得件数 (デフォルト: 50)",
    )

    # calendars サブコマンド
    calendars_parser = subparsers.add_parser("calendars", help="カレンダー一覧を取得")

    # add サブコマンド
    add_parser = subparsers.add_parser("add", help="予定を追加")
    add_parser.add_argument("--summary", required=True, help="予定タイトル")
    add_parser.add_argument("--start", required=True, help="開始日時 (ISO 8601形式)")
    add_parser.add_argument("--end", required=True, help="終了日時 (ISO 8601形式)")
    add_parser.add_argument("--calendar", default="primary", help="カレンダーID")
    add_parser.add_argument("--color", type=int, choices=range(1, 12), help="色ID (1-11)")
    add_parser.add_argument("--location", help="場所")
    add_parser.add_argument("--description", help="説明")
    add_parser.add_argument("--all-day", action="store_true", help="終日イベント")

    # colors サブコマンド
    colors_parser = subparsers.add_parser("colors", help="使用可能な色一覧を表示")

    # update サブコマンド
    update_parser = subparsers.add_parser("update", help="予定を更新")
    update_parser.add_argument("--event-id", required=True, help="イベントID")
    update_parser.add_argument("--calendar", default="primary", help="カレンダーID")
    update_parser.add_argument("--summary", help="新しいタイトル")
    update_parser.add_argument("--start", help="新しい開始日時 (ISO 8601形式)")
    update_parser.add_argument("--end", help="新しい終了日時 (ISO 8601形式)")
    update_parser.add_argument("--location", help="新しい場所")
    update_parser.add_argument("--description", help="新しい説明")
    update_parser.add_argument("--color", type=int, choices=range(1, 12), help="新しい色ID (1-11)")

    # delete サブコマンド
    delete_parser = subparsers.add_parser("delete", help="予定を削除")
    delete_parser.add_argument("--event-id", required=True, help="イベントID")
    delete_parser.add_argument("--calendar", default="primary", help="カレンダーID")

    # get サブコマンド
    get_parser = subparsers.add_parser("get", help="予定の詳細を取得")
    get_parser.add_argument("--event-id", required=True, help="イベントID")
    get_parser.add_argument("--calendar", default="primary", help="カレンダーID")

    # 後方互換性のための引数（サブコマンドなしの場合）
    parser.add_argument(
        "--range",
        choices=["today", "week", "month"],
        default="today",
        help="期間 (デフォルト: today)",
    )
    parser.add_argument(
        "--calendar",
        default="all",
        help="カレンダーID (デフォルト: all=全カレンダー, primary=メインのみ)",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=50,
        help="最大取得件数 (デフォルト: 50)",
    )

    args = parser.parse_args()

    # トークンパスの決定
    if args.token:
        token_path = args.token
    else:
        token_path = get_token_path()

    # コマンド実行
    if args.command == "calendars":
        calendars = list_calendars(token_path)
        if args.format == "json":
            print_json(calendars)
        else:
            print("利用可能なカレンダー:")
            for cal in calendars:
                primary_mark = " (primary)" if cal["primary"] else ""
                print(f"  {cal['summary']}{primary_mark}")
                print(f"    ID: {cal['id']}")
                print(f"    権限: {cal['accessRole']}")
                print()

    elif args.command == "add":
        result = create_event(
            token_path,
            args.summary,
            args.start,
            args.end,
            args.calendar,
            args.color,
            args.location,
            args.description,
            args.all_day,
        )
        if args.format == "json":
            print_json([result])
        else:
            print("予定を追加しました:")
            print(f"  タイトル: {result['summary']}")
            print(f"  開始: {result['start']}")
            print(f"  終了: {result['end']}")
            if result['location']:
                print(f"  場所: {result['location']}")
            print(f"  URL: {result['url']}")

    elif args.command == "colors":
        if args.format == "json":
            colors = [{"id": k, "name": v} for k, v in COLOR_MAP.items()]
            print_json(colors)
        else:
            print("使用可能な色:")
            for color_id, color_name in COLOR_MAP.items():
                print(f"  {color_id}: {color_name}")

    elif args.command == "update":
        result = update_event(
            token_path,
            args.event_id,
            args.calendar,
            args.summary,
            args.start,
            args.end,
            args.location,
            args.description,
            args.color,
        )
        if args.format == "json":
            print_json([result])
        else:
            print("予定を更新しました:")
            print(f"  タイトル: {result['summary']}")
            print(f"  開始: {result['start']}")
            print(f"  終了: {result['end']}")
            if result['location']:
                print(f"  場所: {result['location']}")
            print(f"  URL: {result['url']}")

    elif args.command == "delete":
        result = delete_event(token_path, args.event_id, args.calendar)
        if args.format == "json":
            print_json([result])
        else:
            print("予定を削除しました:")
            print(f"  イベントID: {result['id']}")
            if result['summary']:
                print(f"  タイトル: {result['summary']}")

    elif args.command == "get":
        result = get_event(token_path, args.event_id, args.calendar)
        if args.format == "json":
            print_json([result])
        else:
            print(f"タイトル: {result['summary']}")
            print(f"開始: {result['start']}")
            print(f"終了: {result['end']}")
            if result['location']:
                print(f"場所: {result['location']}")
            if result['description']:
                print(f"説明: {result['description']}")
            print(f"URL: {result['url']}")

    else:
        # サブコマンドなし or events サブコマンド
        period = args.range
        calendar_id = args.calendar
        max_results = args.max

        if calendar_id == "all":
            events = list_all_events(token_path, period, max_results)
            headers = ["start", "end", "summary", "calendar", "location"]
        else:
            events = list_events(token_path, period, calendar_id, max_results)
            headers = ["start", "end", "summary", "location", "url"]

        format_output(events, headers, args.format)


if __name__ == "__main__":
    main()
