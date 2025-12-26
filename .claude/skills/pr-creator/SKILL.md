---
name: pr-creator
description: 実装完了後に PR を作成し関連 Issue をクローズする。「PR 作成」「PR を作って」「プルリク作成」「pull request」「PR 出して」「プルリクエスト」「PR を出したい」などで起動。変更内容を分析し適切な PR を生成。
allowed-tools: [Read, Bash, Glob, Grep]
---

# PR Creator

実装完了後に PR を作成し、関連 Issue をクローズします。

## ワークフロー

### 1. 変更内容の確認

```bash
git status
git diff --staged
git diff
```

### 2. 関連 Issue の特定

以下から関連 Issue を判定：

- コミットメッセージ
- ブランチ名
- ユーザーへの確認

### 3. ブランチの準備

必要に応じて新しいブランチを作成：

```bash
# 現在のブランチ確認
git branch --show-current

# 必要ならブランチ作成
git checkout -b feature/xxx
```

### 4. PR 作成

`gh pr create` で PR を作成。

**PR タイトルの命名規則**（Conventional Commits 形式）:

| タイプ   | 説明             | 例                                       |
|----------|------------------|------------------------------------------|
| feat     | 新機能           | `feat: shiiman-common プラグインを追加`  |
| fix      | バグ修正         | `fix: コマンド名の typo を修正`          |
| docs     | ドキュメント     | `docs: README を更新`                    |
| refactor | リファクタリング | `refactor: スキル構造を整理`             |
| chore    | その他の変更     | `chore: 依存関係を更新`                  |

**PR 作成コマンド**:

```bash
gh pr create \
  --title "feat: {変更内容の要約}" \
  --body "## 概要

{変更内容の説明}

## 変更内容

- {変更点1}
- {変更点2}
- {変更点3}

## 関連 Issue

Closes #{issue番号}

## チェックリスト

- [x] 命名規則に従っている
- [x] README.md を更新した
- [x] 動作確認済み"
```

### 5. 結果報告

作成された PR の URL を報告。

## Issue の自動クローズ

PR 説明に以下のキーワードを含めると、マージ時に Issue が自動クローズ：

- `Closes #1`
- `Fixes #1`
- `Resolves #1`

複数 Issue をクローズする場合:

```text
Closes #1, #2, #3
```

## 重要な注意事項

- ✅ Conventional Commits 形式に従う
- ✅ 関連 Issue を `Closes #N` で参照
- ✅ 変更内容を箇条書きで記載
- ✅ PR タイトルと本文は日本語で記載
- ❌ Issue の自動クローズを忘れない
- ❌ 変更内容と無関係な Issue を参照しない
