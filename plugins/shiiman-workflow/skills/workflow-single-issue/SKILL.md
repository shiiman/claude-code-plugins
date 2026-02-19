---
name: workflow-single-issue
description: Issue 作成から PR 作成まで自動実行するシングルエージェント開発フロー。「シングル Issue フロー」「workflow-single-issue」「Issue から PR まで」「Issue ベース開発」「シングルフロー Issue」「1人で Issue 開発」「Issue 付きフロー」などで起動。計画書に基づいた自動実装を実行。
allowed-tools:
  [
    Read,
    Write,
    Edit,
    Bash,
    Glob,
    Grep,
    AskUserQuestion,
    EnterPlanMode,
    TodoWrite,
    Task,
  ]
context: fork
user-invocable: true
argument-hint: "[タスク説明] [--plan|--help]"
---

# Single Issue Flow

Issue 作成から PR 作成まで自動実行するシングルエージェント開発フロー。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/workflow-single-issue - シングルエージェント Issue 開発フロー

概要:
  Issue 作成から PR 作成まで自動実行する。
  Issue 作成 → ブランチ作成 → 実装 → コミット → PR 作成。

使用方法:
  /workflow-single-issue [タスク説明] [オプション]

オプション:
  --plan  plan mode で計画書を新規作成してから実行
  --help  このヘルプを表示

例:
  /workflow-single-issue                        # 既存計画書から実行
  /workflow-single-issue --plan                 # 計画書を作成してから実行
  /workflow-single-issue "ログイン機能を追加"    # タスク説明から直接実行
```

## 3つの実行モード

### モード 1: 計画書実行モード（デフォルト）

引数なしで実行。既存の承認済み計画書から直接実行。

```
[既存計画書] → Issue作成 → ブランチ作成 → 実装 → ... → PR作成
```

### モード 2: 計画書作成モード（--plan）

plan mode を使って計画書を作成・承認してから実行。

```
[ユーザー入力] → plan mode → 計画書作成 → 承認 → Issue作成 → ... → PR作成
```

### モード 3: 直接実行モード（タスク説明あり）

計画書を作らず、タスク説明から直接実行。簡単なタスク向け。

```
[タスク説明] → Issue作成 → ブランチ作成 → 実装 → ... → PR作成
```

## 実行フロー

```
Issue作成 → ブランチ作成 → 実装 → 自己レビュー → [確認] → Issue更新 → コミット → プッシュ → PR作成
```

## モード判定

1. **先頭引数が `--plan` の場合** → モード 2（計画書作成モード）
2. **引数が1つ以上あり、`--plan` / `--help` 以外の文字列の場合** → モード 3（直接実行モード）
3. **引数なしの場合** → モード 1（計画書実行モード）

## モード 1: 計画書実行モード（デフォルト）

**重要: このモードでは plan mode を使用しません。**

- `EnterPlanMode` ツールを使用しないでください
- 計画の承認を求めないでください
- 直接フローを実行してください

### ステップ 0: 計画書の読み込み

`.claude/plans/` ディレクトリから最新の計画ファイルを読み込みます。

```bash
ls -t ~/.claude/plans/*.md | head -1
```

**計画書が見つからない場合**:

```
## 計画書が見つかりません

計画書が見つかりませんでした。

### 代替手段
- `workflow-single-issue --plan` で新しい計画を作成
- `workflow-single-issue タスク説明` で直接実行
```

計画書が見つかったら、ステップ 1 から実行。

## モード 2: 計画書作成モード（--plan）

**`EnterPlanMode` ツールを使用して plan mode に入ります。**

1. ユーザーに実装したい内容を確認
2. `EnterPlanMode` を実行して plan mode に入る
3. 計画書を作成（`.claude/plans/` に保存される）
4. ユーザーが計画を承認したら、自動的に workflow-single-issue の実行フェーズに進む

## モード 3: 直接実行モード（タスク説明あり）

**重要: このモードでは plan mode を使用しません。**

- `EnterPlanMode` ツールを使用しないでください
- 計画書を作成しないでください
- タスク説明を Issue の内容として使用してください

タスク説明を確認し、直接ステップ 1 から実行。

## 共通ステップ（全モード共通）

### ステップ 1: Issue 作成

`gh issue create` で Issue を作成:

```bash
gh repo view --json owner,name
gh issue create --title "{タイトル}" --body "{本文}" --label "{ラベル}"
```

**Issue タイトル**: タスク内容を簡潔に（50文字以内）

**Issue ラベル**:

- `enhancement`: 新機能
- `bug`: バグ修正
- `documentation`: ドキュメント
- `improvement`: リファクタリング

**Issue 本文フォーマット**:

```markdown
## 概要

{タスクの目的・背景}

## タスク

- [ ] {サブタスク1}
- [ ] {サブタスク2}
- [ ] {サブタスク3}

## 完了条件

- {達成すべき条件1}
- {達成すべき条件2}
```

### ステップ 2: ブランチ作成

```bash
DEFAULT_BRANCH="$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')"
if [ -z "$DEFAULT_BRANCH" ]; then
  echo "ERROR: デフォルトブランチを取得できませんでした。" >&2
  exit 1
fi

git fetch origin "$DEFAULT_BRANCH"
git checkout "$DEFAULT_BRANCH"
git pull origin "$DEFAULT_BRANCH"
git checkout -b feature/{issue番号}
```

ユーザーがベースブランチを明示した場合は、そちらを優先する。

**ブランチ名プレフィックス**:

- `enhancement` → `feature/{issue番号}`
- `bug` → `fix/{issue番号}`
- `documentation` → `docs/{issue番号}`
- `improvement` → `refactor/{issue番号}`

### ステップ 3: 実装

Issue の内容に基づいてコードを実装:

1. 必要なファイルを特定
2. コード変更を実施
3. 動作確認（可能な場合）
4. **サブタスク完了時に Issue を更新（バックグラウンド）**

### ステップ 4: セキュリティチェック＆自己レビュー

**セキュリティチェック**:

```bash
git status
```

以下のパターンを検出したら警告:

- `.env*` - 環境変数
- `*.pem`, `*.key` - 秘密鍵
- `credentials.json` - 認証情報
- `node_modules/`, `vendor/` - 依存パッケージ

**自己レビュー**:

```bash
git diff
```

以下の観点でチェック:

- コード品質・命名規則
- セキュリティ（OWASP Top 10）
- パフォーマンス（N+1、メモリリーク）

### ステップ 5: ユーザー確認

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

### ステップ 6: Issue チェックボックス完了更新

ユーザー確認後、コミット前に Issue の残りのチェックボックスを含め、全てを完了状態に更新します。

### ステップ 7: コミット

```bash
git add .
git commit -m "{コミットメッセージ}"
```

**コミットメッセージ形式**:

1. まず `.claude/settings.json` の `git.commitMessage` 設定を確認
2. 設定がある場合はその形式に従う
3. 設定がない場合は Conventional Commits（日本語）を使用

### ステップ 8: プッシュ

```bash
git push -u origin {ブランチ名}
```

### ステップ 9: PR 作成

```bash
gh pr create --title "{PRタイトル}" --body "{PR本文}"
```

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

### ステップ 10: 完了報告

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

- ✅ モード 2 のみ `EnterPlanMode` を使用
- ✅ モード 1, 3 では plan mode を使用しない
- ✅ コミット前に必ずユーザー確認を行う
- ✅ 機密ファイルをコミットしない
- ✅ `.claude/settings.json` のコミットメッセージ設定に従う（設定がなければ Conventional Commits）
- ✅ PR で `Closes #N` を使用して Issue を参照
- ❌ ユーザー確認なしでコミット・プッシュしない
- ❌ デフォルトブランチに直接コミットしない
