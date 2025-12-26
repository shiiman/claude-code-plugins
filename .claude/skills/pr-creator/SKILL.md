---
name: pr-creator
description: PR を作成して Issue をクローズ。「PR 作成」「PR を作って」「プルリク作成」「pull request」でトリガー。
allowed-tools: [Read, Bash, Glob, Grep]
---

# PR Creator

実装完了後に PR を作成し、関連 Issue をクローズします。

## 手順

トリガーされたら `/create-pr` コマンドを実行。

1. `docs/pr.md` を参照として読む
2. `/create-pr` を実行してユーザーを PR 作成にガイド

`/create-pr` コマンドは以下を行う:

- 変更内容を確認（git status, git diff）
- クローズする Issue 番号を聞く
- ブランチを作成（必要な場合）
- `gh pr create` で PR を作成
- 作成された PR の URL を報告

## PR タイトルの命名規則

Conventional Commits 形式:

| タイプ | 説明 |
|--------|------|
| feat | 新機能 |
| fix | バグ修正 |
| docs | ドキュメント |
| refactor | リファクタリング |
