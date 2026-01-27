---
name: create-pr
description: 現在のブランチから PR を作成し関連 Issue を参照する。「PR 作成」「PR を作って」「プルリク作成」「pull request」「PR 出して」「プルリクエスト」「レビュー依頼したい」などで起動。変更内容を分析し適切な PR を生成。
allowed-tools: [Read, Bash, Glob, Grep]
context: fork
---

# Create PR

現在のブランチから PR を作成し、関連 Issue を参照します。

## ワークフロー

### 1. 変更内容の確認

```bash
git status
git diff --staged
git diff
git log main..HEAD --oneline
```

### 2. 関連 Issue の特定

以下から関連 Issue を判定:

- ブランチ名（`feature/5` → #5）
- コミットメッセージ
- ユーザーへの確認

### 3. PR 内容の作成

**タイトル**: Conventional Commits 形式

| タイプ | 説明 | 例 |
|--------|------|-----|
| feat | 新機能 | `feat: shiiman-git プラグインを追加` |
| fix | バグ修正 | `fix: Issue 番号の取得を修正` |
| docs | ドキュメント | `docs: README を更新` |
| refactor | リファクタリング | `refactor: スキル構造を整理` |
| chore | その他の変更 | `chore: 依存関係を更新` |

### 4. PR 作成

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

## テスト計画

- [ ] {テスト項目1}
- [ ] {テスト項目2}

## チェックリスト

- [x] 命名規則に従っている
- [x] README.md を更新した（必要な場合）
- [x] 動作確認済み"
```

### 5. 結果報告

```
PR を作成しました:

- URL: {pr_url}
- タイトル: {title}
- 関連 Issue: #{issue番号}

マージ後、Issue #{issue番号} は自動的にクローズされます。
```

## 重要な注意事項

- ✅ Conventional Commits 形式のタイトル
- ✅ 関連 Issue を `Closes #N` で参照
- ✅ 変更内容を箇条書きで記載
- ✅ PR タイトルと本文は日本語
- ❌ Issue の自動クローズを忘れない
