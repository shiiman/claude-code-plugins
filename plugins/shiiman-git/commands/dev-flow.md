# Dev Flow

Issue 作成から PR 作成まで自動実行する統合開発ワークフロー。

## 使い方

```bash
/shiiman-git:dev-flow              # 計画書から開始（デフォルト）
/shiiman-git:dev-flow タスクの説明  # タスク説明から開始
/shiiman-git:dev-flow --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `--help` | このコマンドのヘルプを表示 |

## 実行フロー

```
[計画書] → Issue作成 → ブランチ作成 → 実装 → 自己レビュー → [確認] → コミット → プッシュ → PR作成
```

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### ステップ 1: タスク内容の確認

**計画書がある場合（`--from-plan` または plan mode 直後）**:

1. `.claude/plans/` ディレクトリから最新の計画ファイルを読み込む
2. 計画書の内容を Issue の本文として使用
3. **実装を始めずに** Issue 作成に進む

```bash
# 計画ファイルを探す
ls -t ~/.claude/plans/*.md | head -1
```

**計画書がない場合**:

ユーザーが指定したタスクの説明を確認。不明確な場合は質問して明確化。

**重要**: 「実装しますか？」とは聞かない。タスク確認後は直接 Issue 作成に進む。

### ステップ 2: Issue 作成

`gh issue create` で Issue を作成:

```bash
# リポジトリ情報取得
gh repo view --json owner,name

# Issue 作成
gh issue create --title "{タイトル}" --body "{本文}" --label "{ラベル}"
```

**Issue タイトル**: タスク内容を簡潔に（50文字以内）
**Issue ラベル**: タスク種類に応じて自動選択

- `enhancement`: 新機能
- `bug`: バグ修正
- `documentation`: ドキュメント
- `improvement`: リファクタリング

### ステップ 3: ブランチ作成

Issue 番号でブランチを作成:

```bash
# main ブランチを最新化
git fetch origin main
git checkout main
git pull origin main

# ブランチ作成
git checkout -b feature/{issue番号}
```

**ブランチ名プレフィックス**（ラベルに応じて）:

- `enhancement` → `feature/{issue番号}`
- `bug` → `fix/{issue番号}`
- `documentation` → `docs/{issue番号}`
- `improvement` → `refactor/{issue番号}`

### ステップ 4: 実装

Issue の内容に基づいてコードを実装:

1. 必要なファイルを特定
2. コード変更を実施
3. 動作確認（可能な場合）

### ステップ 5: セキュリティチェック

コミット前に機密ファイルをチェック:

```bash
git status
```

以下のパターンを検出したら警告:

- `.env*` - 環境変数
- `*.pem`, `*.key` - 秘密鍵
- `credentials.json` - 認証情報
- `node_modules/`, `vendor/` - 依存パッケージ

### ステップ 6: 自己レビュー

実装完了後、自分でコードをレビュー:

1. 変更差分を取得
2. `pr-reviewer` と同様の観点でチェック:
   - コード品質・命名規則
   - セキュリティ（OWASP Top 10）
   - パフォーマンス（N+1、メモリリーク）
3. 問題があれば修正

```bash
# 変更差分を確認
git diff
```

### ステップ 7: ユーザー確認

**重要**: ここでユーザーに確認を求める。

```
## 変更内容の確認

以下の変更をコミットします:

{git diff --stat の出力}

### 変更ファイル一覧
{変更ファイルリスト}

### 自己レビュー結果
{レビューで確認した内容のサマリー}

### コミットメッセージ
{自動生成されたメッセージ}

この内容でコミット・プッシュ・PR作成を実行してよろしいですか？
```

**ユーザーが承認しない場合**: 追加の修正を行うか、中断。

### ステップ 8: コミット

```bash
git add .
git commit -m "{コミットメッセージ}"
```

**コミットメッセージ形式** (Conventional Commits):

- `feat: {説明}` - 新機能
- `fix: {説明}` - バグ修正
- `docs: {説明}` - ドキュメント
- `refactor: {説明}` - リファクタリング

### ステップ 9: プッシュ

```bash
git push -u origin {ブランチ名}
```

### ステップ 10: PR 作成

```bash
gh pr create --title "{PRタイトル}" --body "{PR本文}"
```

**PR タイトル**: コミットメッセージと同様の形式
**PR 本文**:

```markdown
## 概要

{変更内容の説明}

## 変更内容

- {変更点1}
- {変更点2}

## 関連 Issue

Closes #{issue番号}

## テスト計画

- [ ] {テスト項目}
```

### ステップ 11: 完了報告

```
## 開発フロー完了

### 作成された Issue
- #{issue番号}: {タイトル}

### 作成されたブランチ
- {ブランチ名}

### 作成された PR
- PR #{pr番号}: {タイトル}
- URL: {pr_url}

PR がマージされると Issue #{issue番号} は自動的にクローズされます。
```

## 重要な注意事項

- ✅ コミット前に必ずユーザー確認を行う
- ✅ 機密ファイルをコミットしない
- ✅ Conventional Commits 形式を使用
- ✅ PR で `Closes #N` を使用して Issue を参照
- ❌ ユーザー確認なしでコミット・プッシュしない
- ❌ main ブランチに直接コミットしない
