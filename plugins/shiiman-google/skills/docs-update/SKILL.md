---
name: docs-update
description: Google Docs ドキュメントにテキストを追加する。「ドキュメント更新」「Docs 更新」「ドキュメントに追加」「ドキュメントを編集」などで起動。
allowed-tools: [Read, Bash]
---

# Docs Update

Google Docs ドキュメントにテキストを追加します。

## 実行方法

### 先頭に挿入

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/docs-update/google_docs.py update --doc-id "ドキュメントID" --content "追加テキスト"
```

### 末尾に追加

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/docs-update/google_docs.py update --doc-id "ドキュメントID" --content "追加テキスト" --append
```

## ユーザー入力の解釈

- ドキュメントIDを聞き出すか、事前に docs-list/drive-search で検索
- 追加するテキストを確認
- 「末尾に」「最後に」などの指定があれば --append を使用

## 出力項目

- id: ドキュメントID
- status: 更新ステータス
- mode: 挿入モード（append/prepend）
- url: 編集URL
