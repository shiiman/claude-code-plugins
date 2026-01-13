---
name: sheets-update
description: Google Sheets スプレッドシートのセルを更新する
allowed-tools: [Bash]
---

# Sheets Update

Google Sheets スプレッドシートのセルを更新します。

## 引数

- `$ARGUMENTS` (必須): スプレッドシートID

## オプション

- `--range <range>` (必須): 更新範囲（例: A1, A1:B2）
- `--values <json>` (必須): 書き込む値（JSON配列）

## 実行

```bash
python plugins/shiiman-google/skills/sheets-list/scripts/google_sheets.py update --sheet-id "$ARGUMENTS" --range "$RANGE" --values "$VALUES"
```

## 使用例

```
/shiiman-google:sheets-update 1abc...xyz --range "A1" --values '["Hello", "World"]'
/shiiman-google:sheets-update 1abc...xyz --range "A1:B2" --values '[["A1","B1"],["A2","B2"]]'
```
