---
name: docs-create
description: Google Docs ドキュメントを新規作成する
allowed-tools: [Bash]
---

# Docs Create

Google Docs ドキュメントを新規作成します。

## 引数

- `$ARGUMENTS` (必須): ドキュメント名

## オプション

- `--folder-id <id>`: 作成先フォルダID
- `--content <text>`: 初期内容

## 実行

```bash
python plugins/shiiman-google/scripts/google_docs.py create --name "$ARGUMENTS" ${FOLDER_ID:+--folder-id "$FOLDER_ID"} ${CONTENT:+--content "$CONTENT"}
```

## 使用例

```
/shiiman-google:docs-create 会議議事録
/shiiman-google:docs-create 企画書 --folder-id xxx --content "# 概要"
```
