---
name: sheets-create
description: Google Sheets スプレッドシートを新規作成する
allowed-tools: [Bash]
---

# Sheets Create

Google Sheets スプレッドシートを新規作成します。

## 引数

- `$ARGUMENTS` (必須): スプレッドシート名

## オプション

- `--folder-id <id>`: 作成先フォルダID

## 実行

```bash
python plugins/shiiman-google/skills/sheets-list/scripts/google_sheets.py create --name "$ARGUMENTS" ${FOLDER_ID:+--folder-id "$FOLDER_ID"}
```

## 使用例

```
/shiiman-google:sheets-create 売上データ
/shiiman-google:sheets-create 顧客リスト --folder-id xxx
```
