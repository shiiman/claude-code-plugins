---
name: calendar-update
description: Google Calendar の予定を更新する
allowed-tools: [Bash]
---

# Calendar Update

Google Calendar の予定を更新します。

## 引数

- `$ARGUMENTS` (必須): イベントID

## オプション

- `--calendar <id>`: カレンダーID（デフォルト: primary）
- `--summary <title>`: 新しいタイトル
- `--start <datetime>`: 新しい開始日時 (ISO 8601形式)
- `--end <datetime>`: 新しい終了日時 (ISO 8601形式)
- `--location <place>`: 新しい場所
- `--description <text>`: 新しい説明
- `--color <1-11>`: 新しい色ID

## 実行

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py update --event-id "$ARGUMENTS" ${CALENDAR:+--calendar "$CALENDAR"} ${SUMMARY:+--summary "$SUMMARY"} ${START:+--start "$START"} ${END:+--end "$END"} ${LOCATION:+--location "$LOCATION"} ${DESCRIPTION:+--description "$DESCRIPTION"} ${COLOR:+--color "$COLOR"}
```

## 使用例

```
/shiiman-google:calendar-update abc123xyz --summary "新しいタイトル"
/shiiman-google:calendar-update abc123xyz --start 2025-01-08T15:00:00 --end 2025-01-08T16:00:00
```
