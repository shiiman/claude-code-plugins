---
name: docs-get
description: Google Docs ドキュメントの内容を取得する
allowed-tools: [Bash]
---

# Docs Get

Google Docs ドキュメントの内容を取得します。

## 引数

- `$ARGUMENTS` (必須): ドキュメントID

## 実行

```bash
python plugins/shiiman-google/scripts/google_docs.py get --doc-id "$ARGUMENTS"
```

## 使用例

```
/shiiman-google:docs-get 1abc...xyz
```
