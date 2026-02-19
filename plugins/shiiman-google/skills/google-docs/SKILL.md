---
name: google-docs
description: Google Docs ドキュメントを新規作成・更新する。「ドキュメント作成」「Docs 作成」「新しいドキュメント」「ドキュメント更新」「Docs 更新」「ドキュメントに追加」「ドキュメントを編集」などで起動。
allowed-tools: [Read, Bash]
argument-hint: "[--help]"
---

# Docs Editor

Google Docs ドキュメントの新規作成・テキスト追加を行います。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/google-docs - Docs Editor

概要:
  Google Docs ドキュメントの新規作成・テキスト追加を行います。

使用方法:
  /google-docs [オプション]

オプション:
  --help  このヘルプを表示
```

## ワークフロー

### 新規作成

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_docs.py create \
  --name "ドキュメント名" \
  --folder-id "フォルダID" \
  --content "初期テキスト"
```

| オプション    | 必須 | 説明             |
| ------------- | ---- | ---------------- |
| `--name`      | Yes  | ドキュメント名   |
| `--folder-id` | No   | 保存先フォルダID |
| `--content`   | No   | 初期テキスト     |

### テキスト追加

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_docs.py update \
  --doc-id "ドキュメントID" \
  --content "追加テキスト" \
  --append
```

| オプション  | 必須 | 説明                             |
| ----------- | ---- | -------------------------------- |
| `--doc-id`  | Yes  | ドキュメントID                   |
| `--content` | Yes  | 追加テキスト                     |
| `--append`  | No   | 末尾に追加（省略時は先頭に挿入） |
