---
name: calendar-delete
description: Google Calendar の予定を削除する
allowed-tools: [Bash]
---

# Calendar Delete

Google Calendar の予定を削除します。

## 引数

- `$ARGUMENTS` (必須): イベントID

## オプション

- `--calendar <id>`: カレンダーID（デフォルト: primary）

## 実行

```bash
python plugins/shiiman-google/scripts/google_calendar.py delete --event-id "$ARGUMENTS" ${CALENDAR:+--calendar "$CALENDAR"}
```

## 使用例

```
/shiiman-google:calendar-delete abc123xyz
/shiiman-google:calendar-delete abc123xyz --calendar work@group.calendar.google.com
```
