---
name: sheets-export
description: Google Sheets をエクスポートする
allowed-tools: [Bash]
---

# Sheets Export

Google Sheets をファイルにエクスポートします。

## 引数

- `$ARGUMENTS` (必須): スプレッドシートID

## オプション

- `--output <path>` (必須): 出力ファイルパス
- `--type <format>`: 出力形式（csv, xlsx, pdf, ods, tsv）デフォルト: csv

## 実行

```bash
python plugins/shiiman-google/skills/sheets-list/scripts/google_sheets.py export --sheet-id "$ARGUMENTS" --output "$OUTPUT" ${TYPE:+--type "$TYPE"}
```

## 使用例

```
/shiiman-google:sheets-export 1abc...xyz --output ~/Downloads/data.csv
/shiiman-google:sheets-export 1abc...xyz --output ~/Downloads/data.xlsx --type xlsx
```
