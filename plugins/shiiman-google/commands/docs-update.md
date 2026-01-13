---
name: docs-update
description: Google Docs ドキュメントにテキストを追加する
allowed-tools: [Bash]
---

# Docs Update

Google Docs ドキュメントにテキストを追加します。

## 引数

- `$ARGUMENTS` (必須): ドキュメントID

## オプション

- `--content <text>` (必須): 追加するテキスト
- `--append`: 末尾に追加（省略時は先頭に挿入）

## 実行

```bash
python plugins/shiiman-google/skills/docs-list/scripts/google_docs.py update --doc-id "$ARGUMENTS" --content "$CONTENT" ${APPEND:+--append}
```

## 使用例

```
/shiiman-google:docs-update 1abc...xyz --content "追加テキスト"
/shiiman-google:docs-update 1abc...xyz --content "末尾に追加" --append
```
