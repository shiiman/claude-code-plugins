# PR 作成ガイド

## 概要

実装完了後に PR を作成し、関連 Issue をクローズします。

## コマンド

```bash
/pr-create
```

## PR タイトルの命名規則

Conventional Commits 形式:

| タイプ | 説明 | 例 |
|--------|------|-----|
| feat | 新機能 | `feat: shiiman-common プラグインを追加` |
| fix | バグ修正 | `fix: コマンド名のtypoを修正` |
| docs | ドキュメント | `docs: README を更新` |
| refactor | リファクタリング | `refactor: スキル構造を整理` |

## PR 作成コマンド

```bash
gh pr create \
  --title "feat: shiiman-common プラグインを追加" \
  --body "## 概要

shiiman-common プラグインを追加しました。

## 変更内容

- プラグイン構造を作成
- commit コマンドを追加
- code-reviewer スキルを追加

## 関連 Issue

Closes #1, #2, #3

## チェックリスト

- [x] 命名規則に従っている
- [x] README.md を更新した
- [x] 動作確認済み"
```

## Issue のクローズ

PR 説明に以下のキーワードを含めると、マージ時に Issue が自動クローズされます:

- `Closes #1`
- `Fixes #1`
- `Resolves #1`

複数 Issue をクローズする場合:

```text
Closes #1, #2, #3
```

## ワークフロー

```text
1. /issue-create で Issue を作成
   ↓
2. 実装（/plugin-create, /skill-create 等）
   ↓
3. /pr-create で PR 作成
   ↓
4. レビュー & マージ
   ↓
5. Issue が自動クローズ
```

## 関連コマンド

- `/issue-create` - 計画から Issue をまとめて作成
