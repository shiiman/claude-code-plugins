---
name: docs-search
description: Google Docs を検索する。「Docs 検索」「ドキュメント検索」「Google Docs 検索」「Docs を探して」「ドキュメントを検索」「Google ドキュメント検索」「Docs を見つけたい」などで起動。`/shiiman-google:docs-search` を実行して検索する。
allowed-tools: [Read, Bash]
---

# Docs Search

Google Docs を検索します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:docs-search` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:docs-search` に委譲します（SSOT として扱う）。
