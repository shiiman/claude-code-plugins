---
name: pr-creator
description: 実装完了後に PR を作成し関連 Issue をクローズする。「PR 作成」「PR を作って」「プルリク作成」「pull request」「PR 出して」「プルリクエスト」「PR を出したい」などで起動。変更内容を分析し適切な PR を生成。
allowed-tools: [Read, Bash, Glob, Grep]
---

# PR Creator

実装完了後に PR を作成し、関連 Issue をクローズします。

## ワークフロー

### 1. ドキュメント参照

`docs/pr.md` を Read ツールで参照（SSOT として扱う）。

### 2. コマンド実行

`/create-pr` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/create-pr` に委譲します（SSOT として扱う）。

`/create-pr` コマンドは以下を行う:

- 変更内容を確認（git status, git diff）
- 関連 Issue を自動判定
- ブランチを作成（必要な場合）
- `gh pr create` で PR を作成
- 作成された PR の URL を報告

## PR タイトルの命名規則

Conventional Commits 形式:

| タイプ   | 説明               |
|----------|--------------------|
| feat     | 新機能             |
| fix      | バグ修正           |
| docs     | ドキュメント       |
| refactor | リファクタリング   |
| chore    | その他の変更       |

## 重要な注意事項

- ✅ Conventional Commits 形式に従う
- ✅ 関連 Issue を `Closes #N` で参照
- ✅ 変更内容を箇条書きで記載
- ❌ Issue の自動クローズを忘れない
