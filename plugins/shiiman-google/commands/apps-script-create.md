---
name: apps-script-create
description: Google Apps Script プロジェクトを新規作成する
allowed-tools: [Bash]
---

# Apps Script Create

Google Apps Script プロジェクトを新規作成します。

## 引数

- `$ARGUMENTS` (必須): スクリプト名

## オプション

- `--parent-id <id>`: 親ドキュメントID（スプレッドシート等に紐付ける場合）

## 実行

```bash
python plugins/shiiman-google/scripts/google_apps_script.py create --name "$ARGUMENTS" ${PARENT_ID:+--parent-id "$PARENT_ID"}
```

## 使用例

```
/shiiman-google:apps-script-create MyScript
/shiiman-google:apps-script-create マクロ --parent-id spreadsheet-id
```
