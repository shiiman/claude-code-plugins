---
name: calendar-get
description: Google Calendar のイベント詳細を取得する
allowed-tools: [Bash]
---

# Calendar Get

Google Calendar のイベント詳細を取得します。

## 引数

- `$ARGUMENTS` (必須): イベントID

## オプション

- `--calendar <id>`: カレンダーID（デフォルト: primary）

## 実行

```bash
python plugins/shiiman-google/scripts/google_calendar.py get --event-id "$ARGUMENTS" ${CALENDAR:+--calendar "$CALENDAR"}
```

## 使用例

```
/shiiman-google:calendar-get abc123xyz
/shiiman-google:calendar-get abc123xyz --calendar work@group.calendar.google.com
```
