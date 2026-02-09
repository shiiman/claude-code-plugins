---
name: docs-search
description: Google Docs を検索する。「Docs 検索」「ドキュメント検索」「Google Docs 検索」「Docs を探して」「ドキュメントを検索」「Google ドキュメント検索」「Docs を見つけたい」などで起動。
allowed-tools: [Read, Bash]
---

# Docs Search

Google Docs を検索します。

## 引数

- 検索クエリ (必須): 名前の部分一致など（例: `spec`）

## 実行方法

### アクティブプロファイルで検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/drive-list/google_drive.py search --query "mimeType='application/vnd.google-apps.document' and name contains '<検索キーワード>'"
```

### プロファイル指定で検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/drive-list/google_drive.py search --profile <profile-name> --query "mimeType='application/vnd.google-apps.document' and name contains '<検索キーワード>'"
```

## 検索クエリ例

```bash
# 名前に "spec" を含む
--query "mimeType='application/vnd.google-apps.document' and name contains 'spec'"

# 名前に "議事録" を含む
--query "mimeType='application/vnd.google-apps.document' and name contains '議事録'"

# 最近更新された
--query "mimeType='application/vnd.google-apps.document' and modifiedTime > '2024-01-01'"
```

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
