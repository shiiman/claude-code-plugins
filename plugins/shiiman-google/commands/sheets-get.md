---
name: sheets-get
description: Google Sheets スプレッドシートのデータを取得する
allowed-tools: [Bash]
---

# Sheets Get

Google Sheets スプレッドシートのデータを取得します。

## 引数

- `$ARGUMENTS` (必須): スプレッドシートID

## オプション

- `--range <range>`: 取得範囲（例: A1:C10, Sheet1!A1:B5）

## 実行

```bash
python plugins/shiiman-google/scripts/google_sheets.py get --sheet-id "$ARGUMENTS" ${RANGE:+--range "$RANGE"}
```

## 使用例

```
/shiiman-google:sheets-get 1abc...xyz
/shiiman-google:sheets-get 1abc...xyz --range "A1:C10"
```
