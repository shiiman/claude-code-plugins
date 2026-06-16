---
name: shiiman-workflow:single
description: シングルエージェントで計画書/タスクを順次実装する開発フロー。「シングルフロー」「shiiman-workflow:single」「1 人で実装」「順次実装」「シングルで実装して」「一人で開発」などで起動。Issue/PR まで作るかは発話・引数から判断し、曖昧なら確認する。
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
    Skill,
  ]
context: fork
user-invocable: true
argument-hint: "[タスク説明]"
---

# Single Flow

シングルエージェントで計画書またはタスク説明を順次実装する開発フロー。

フラグは不要。タスクを伝えれば、git の状態・発話内容から実行条件を自動判断し、曖昧な点だけ確認する。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-workflow:single - シングルエージェント開発フロー

概要:
  計画書またはタスク説明を 1 エージェントで順次実装する。
  実装条件（Issue/PR・計画書・ブランチ・git）はフラグ不要で自動判断し、
  曖昧な点だけ AskUserQuestion で確認する。

使用方法:
  /shiiman-workflow:single [タスク説明]
  /shiiman-workflow:single --help

オプション:
  --help  このヘルプを表示

例:
  /shiiman-workflow:single                          # 既存計画書から実装（あれば）
  /shiiman-workflow:single "ログイン機能を追加"      # タスク説明から実装
  /shiiman-workflow:single "認証を実装して PR まで"  # Issue/PR 連携ありで実装
  /shiiman-workflow:single --help                   # ヘルプを表示

指定の伝え方（フラグの代わり）:
  - 「計画を立ててから」  → plan mode で計画書を作成してから実装
  - 「ブランチで」        → worktree ではなくブランチを作成
  - 「Issue / PR まで」   → Issue 作成・PR 作成まで実施
  - 「コミットだけ」      → Issue/PR を作らずコミットメッセージ出力で終了
```

## 前提条件

- `gh` コマンドが利用可能
- `gh auth status` が成功する（GitHub CLI 認証済み）

## 起動時の自動判断（フラグの代わり）

ユーザーにフラグを入力させない。以下を順に決定する。**引数・発話に明示があればそれを最優先**し、明示がなければ自動判断、それでも曖昧な項目だけ後述の手順で確認する。

| 項目              | 既定       | 判断ルール                                                                                                      |
| ----------------- | ---------- | --------------------------------------------------------------------------------------------------------------- |
| git / no-git      | 自動       | `git rev-parse --is-inside-work-tree` 成功なら git。失敗なら no-git（ブランチ作成を省略）                       |
| worktree / branch | worktree   | 「ブランチで」「worktree なし」等の発話があれば branch                                                          |
| 計画書の扱い      | 後述の判定 | 「計画を立てて」「plan で」→ plan mode。引数にタスク説明あり → 直接。なし → 既存計画書を探索                    |
| Issue/PR 連携     | **要確認** | 「Issue」「PR」「プルリク」等あり → 連携あり。「コミットだけ」「Issue 不要」等 → 連携なし。どちらも無ければ確認 |

### Issue/PR 連携の確認

発話・引数から判断できない場合のみ、`AskUserQuestion` で 1 回だけ確認する。

```text
question: "どこまで実施しますか？"
options:
  - 軽量（コミットメッセージ出力のみ）: Issue/PR を作らず、変更とコミットメッセージの提示で終了
  - Issue/PR まで作成: Issue 作成 → 実装 → コミット → PR 作成まで実施
```

- **軽量** を選択 → 「実行フロー（共通）」のみ実施し、最後にコミットメッセージを出力（コミット・PR はしない）
- **Issue/PR まで作成** を選択 → 「実行フロー（共通）」に Issue/PR 連携ステップを追加

### git の状態判定

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1
```

- 成功 → git モード（ブランチ/worktree を作成）
- 失敗 → no-git モード（ブランチ作成を省略し、実装とサマリー出力のみ）

### 計画書の扱いの判定

1. 「計画を立ててから」等の依頼がある → **plan mode**: `EnterPlanMode` で計画書を作成・承認してから実装フェーズへ
2. 引数にタスク説明がある → **直接実行**: タスク説明をそのまま実装の指針にする（plan mode を使わない）
3. 引数なし → **既存計画書**: 最新の計画書を読み込む

```bash
ls -t ~/.claude/plans/*.md 2>/dev/null | head -1
```

計画書が見つからなければ「タスク説明を教えてください。または計画を立ててから実装することもできます」と案内して終了。

## 実行フロー（共通）

```text
[Issue/PR 連携あり] Issue 作成 →
ブランチ/worktree 作成 → 実装 → セキュリティチェック＆自己レビュー → ユーザー確認 →
[連携あり] コミット → プッシュ案内 → PR 作成 → 完了報告
[連携なし] コミットメッセージ出力で終了
```

### ステップ A: Issue 作成（Issue/PR 連携ありのときのみ）

Skill ツールで `shiiman-github:issue-create --no-confirm` を呼び出す。タスク内容を 50 文字以内のタイトルにし、本文は「## 概要 / ## タスク（チェックボックス）/ ## 完了条件」で構成する。ラベルは内容に応じて `enhancement` / `bug` / `documentation` / `improvement` を付与。

作成された Issue 番号を後続ステップで使う。

### ステップ 1: ブランチ / worktree 作成

git モードのみ実施（no-git モードはスキップ）。

- worktree（既定）: Skill ツールで `shiiman-github:worktree-create` を呼び出す
- ブランチ: Skill ツールで `shiiman-github:branch-create` を呼び出す
- Issue/PR 連携ありの場合は Issue 番号を引数に渡す（例: `shiiman-github:worktree-create {issue番号}`）

ユーザーがベースブランチを明示した場合はそちらを優先する。

### ステップ 2: 実装

計画書またはタスク説明に基づいて実装する。

1. 必要なファイルを特定
2. コード変更を実施
3. 動作確認（可能な場合）
4. Issue/PR 連携ありの場合、サブタスク完了時に Issue のチェックボックスを更新

### ステップ 3: セキュリティチェック＆自己レビュー

```bash
git status
git diff
```

- 機密ファイルを検出したら警告: `.env*`（環境変数）、`*.pem` / `*.key`（秘密鍵）、`credentials.json`（認証情報）、`node_modules/` / `vendor/`（依存）
- 自己レビュー観点: コード品質・命名規則 / セキュリティ（OWASP Top 10）/ パフォーマンス（N+1・メモリリーク）

### ステップ 4: ユーザー確認（必須）

変更内容を提示して確認を取る。

```text
## 変更内容の確認

{git diff --stat}

### 変更ファイル一覧
{変更ファイル}

### 自己レビュー結果
{サマリー}

### コミットメッセージ（案）
{Conventional Commits 形式}

この内容で進めてよろしいですか？
```

## 仕上げ

### Issue/PR 連携あり

ユーザー確認後、以下を実施する。

1. Issue の残りチェックボックスを全て完了に更新
2. コミット: Skill ツールで `shiiman-git:add-commit --no-confirm` を呼び出す
3. プッシュ案内（自動実行しない）:

   ```bash
   git push -u origin {ブランチ名}
   ```

4. PR 作成: Skill ツールで `shiiman-github:pr-create --no-confirm` を呼び出す。本文は「## 概要 / ## 変更内容 / ## 関連 Issue（`Closes #{issue番号}`）/ ## テスト計画」で構成
5. 完了報告:

   ```text
   ## 開発フロー完了

   ### 作成された Issue
   - #{issue番号}: {タイトル}

   ### 作成されたブランチ / worktree
   - {ブランチ名}
   - パス: {worktree のパス}（worktree モード時のみ）

   ### 作成された PR
   - PR #{pr番号}: {タイトル} / {pr_url}

   PR がマージされると Issue #{issue番号} は自動的にクローズされます。

   ### worktree クリーンアップ（worktree モード時のみ）
   PR マージ後、`/shiiman-git:worktree` で gtr rm または gtr clean を実行してください。
   ```

### Issue/PR 連携なし（軽量）

**コミット・プッシュ・PR 作成は行わない。** 推奨コミットメッセージを出力して終了する。

```text
## 実装完了

### 作成されたブランチ / worktree（git モード時のみ）
- {ブランチ名}
- パス: {worktree のパス}（worktree モード時のみ）

### 変更サマリー
{git diff --stat}

### 推奨コミットメッセージ
{Conventional Commits 形式（`.claude/settings.json` の git.commitMessage 設定があればそれに従う）}

### 次のステップ
git push -u origin {ブランチ名}
必要に応じて PR 作成: gh pr create
```

## 重要な注意事項

- ✅ ユーザーにフラグを入力させない（git・worktree/branch・計画書・Issue/PR を自動判断、曖昧なら確認）
- ✅ plan mode は「計画を立ててから」と依頼されたときのみ使用
- ✅ コミット前に必ずユーザー確認を行う
- ✅ 機密ファイルを警告・除外する
- ✅ コミットメッセージは `.claude/settings.json` の設定に従う（なければ Conventional Commits）
- ❌ デフォルトブランチで直接作業・コミットしない
- ❌ Issue/PR 連携なしのときは自動でコミット・プッシュ・PR を作らない
