---
name: calendar-add
description: Google Calendar に予定を追加する
allowed-tools: [Bash]
---

# Calendar Add

Google Calendar に予定を追加します。

## 引数

- `$ARGUMENTS` (必須): 予定タイトル

## オプション

- `--start <datetime>` (必須): 開始日時 (ISO 8601形式: 2025-01-08T14:00:00)
- `--end <datetime>` (必須): 終了日時 (ISO 8601形式: 2025-01-08T15:00:00)
- `--calendar <id>`: カレンダーID（デフォルト: primary）
- `--color <1-11>`: 色ID（1:ラベンダー, 2:セージ, 3:ぶどう, 4:フラミンゴ, 5:バナナ, 6:みかん, 7:ピーコック, 8:グラファイト, 9:ブルーベリー, 10:バジル, 11:トマト）
- `--location <place>`: 場所
- `--description <text>`: 説明
- `--all-day`: 終日イベント

## 実行

```bash
python plugins/shiiman-google/scripts/google_calendar.py add --summary "$ARGUMENTS" --start "$START" --end "$END" ${CALENDAR:+--calendar "$CALENDAR"} ${COLOR:+--color "$COLOR"} ${LOCATION:+--location "$LOCATION"} ${DESCRIPTION:+--description "$DESCRIPTION"} ${ALL_DAY:+--all-day}
```

## 使用例

```
/shiiman-google:calendar-add 会議 --start 2025-01-08T14:00:00 --end 2025-01-08T15:00:00
/shiiman-google:calendar-add ランチ --start 2025-01-08T12:00:00 --end 2025-01-08T13:00:00 --color 6 --location "レストラン"
```
