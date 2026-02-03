---
name: multi-issue-flow
description: MCP マルチエージェントで Issue から PR まで並列実行する開発フロー。「マルチ Issue フロー」「multi-issue-flow」「並列 Issue 開発」「マルチエージェント Issue」「複数人で Issue」「並列 Issue フロー」「マルチフロー Issue」などで起動。複数 Worker でタスクを並列実行。
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, EnterPlanMode, TodoWrite, Task]
context: fork
user-invocable: true
---

# Multi Issue Flow

MCP マルチエージェントで Issue から PR まで並列実行する開発フロー。

## 前提条件

- multi-agent-mcp がインストール済み（**必須**）
- tmux がインストール済み（**必須**）

**確認方法**:

```bash
which tmux
claude mcp list | grep multi-agent-mcp
```

## 引数

- `--plan`: plan mode で計画書を新規作成してから実行
- `--workers N`: Worker 数を指定（省略時はプロファイル設定に従う）
- `--profile standard|performance`: モデルプロファイル選択
  - `standard`（デフォルト）: Sonnet、Worker 上限 6
  - `performance`: Opus、Worker 上限 16（複雑なタスク向け）
- `--help`: ヘルプを表示
- `[タスク説明]`: 計画書なしで直接実行（簡単なタスク用）

## アーキテクチャ

```
┌───────────────────────────────────────────────────────────────────┐
│                    tmux セッション (main)                          │
├─────────────────┬────────────┬────────────┬────────────┐
│     pane 0      │   pane 1   │   pane 3   │   pane 5   │
│     Admin       │    W1      │    W3      │    W5      │
│     (40%)       ├────────────┼────────────┼────────────┤
│ (タスク分割・   │   pane 2   │   pane 4   │   pane 6   │
│  管理)          │    W2      │    W4      │    W6      │
└─────────────────┴────────────┴────────────┴────────────┘
     左40%              右60% (Workers 1-6, 3列×2行)
```

**役割分担**:

| 役割   | 実行者                          | 責務                               |
| ------ | ------------------------------- | ---------------------------------- |
| Owner  | 起点 Claude Code（tmux なし）   | 全体指揮、Admin の管理、結果の確認 |
| Admin  | tmux pane 0                     | タスク分割、Worker 管理、進捗監視  |
| Worker | tmux pane 1-6+                  | タスク実行、worktree で作業        |

## 3つの実行モード

1. **計画書実行モード**（引数なし）: 既存の承認済み計画書から実行
2. **計画書作成モード**（`--plan`）: plan mode で計画書を作成してから実行
3. **直接実行モード**（タスク説明あり）: 計画書なしで直接実行

## 実行フロー概要

```
Phase 1: Owner  → Issue 作成 → ブランチ作成 → MCP 初期化 → Admin 起動 → 計画書送信
Phase 2: Admin  → タスク分割 → Worker 作成・管理（自律実行）
Phase 3: Worker → タスク実行 → Admin に報告（自律実行）
Phase 4: Owner  → 結果確認 → クリーンアップ → PR 作成 → Issue クローズ
```

---

## Phase 1: Issue 作成 + セットアップ + Admin 起動（Owner が実行）

### ステップ 1: Issue 作成

```bash
gh repo view --json owner,name
gh issue create --title "{タイトル}" --body "{本文}" --label "{ラベル}"
```

**Issue 本文フォーマット**:

```markdown
## 概要
{タスクの目的・背景}

## タスク一覧
- [ ] Task 1: {サブタスク1}
- [ ] Task 2: {サブタスク2}
...

## 完了条件
- 全てのTaskが完了していること
- テストが通過していること
```

### ステップ 2: ベースブランチ作成

```bash
git fetch origin main
git checkout main
git pull origin main
git checkout -b feature/{issue番号}
git push -u origin feature/{issue番号}
```

### ステップ 3: MCP ワークスペース初期化

```
mcp__multi-agent-mcp__init_workspace
```

- `workspace_path`: プロジェクト名

### ステップ 4: tmux ワークスペース作成

```
mcp__multi-agent-mcp__init_tmux_workspace
```

- `working_dir`: プロジェクトのルートパス
- `open_terminal`: true
- `auto_setup_gtr`: true（gtr 自動設定）

**自動作成**: `memory/`, `screenshot/` ディレクトリと `.env` テンプレートが自動生成されます。

### ステップ 4.5: モデルプロファイル設定（`--profile` 指定時）

```
mcp__multi-agent-mcp__switch_model_profile
```

- `profile`: "standard" または "performance"

**注意**: `--profile performance` 指定時のみ実行。Worker 上限 16、Opus モデルに切替。

### ステップ 5: Owner エージェント登録

```
mcp__multi-agent-mcp__create_agent
```

- `role`: "owner"
- `working_dir`: プロジェクトのルートパス

**注意**: Owner は tmux ペインなし。IPC 自動登録 + メトリクス記録開始。

### ステップ 6: Admin エージェント作成

```
mcp__multi-agent-mcp__create_agent
```

- `role`: "admin"
- `working_dir`: プロジェクトのルートパス

**注意**: tmux pane 0 に配置。IPC 自動登録 + メトリクス記録開始。

### ステップ 7: Admin に計画書を送信

```
mcp__multi-agent-mcp__send_task
```

- `agent_id`: Admin の ID
- `task_content`: 計画書またはタスク説明
- `session_id`: Issue 番号（例: "123"）
- `worker_count`: Worker 数（省略時はプロファイル設定、`--workers` 指定時はその値）
- `branch_name`: 作業ブランチ名（例: "feature/123"）

**自動処理**: MCP が Admin 用の指示テンプレートを自動生成（Worker 管理手順、メモリ検索結果を含む）

### ステップ 8: Admin の完了を待機

Admin が自律的に Worker を作成・管理。Owner は完了報告を待つ。

```
mcp__multi-agent-mcp__get_dashboard_summary  # 進捗確認（軽量）
mcp__multi-agent-mcp__read_messages          # Admin からのメッセージ確認
```

---

## Phase 2-3: Admin/Worker の自律実行

**Admin と Worker は自律的に動作します。Owner は実行しません。**

### Admin の役割

1. 計画書からサブタスクを抽出し Dashboard に登録
2. スクリーンショット確認（UI タスクの場合、`read_latest_screenshot` で視覚的問題を分析）
3. Worker 用 Worktree を作成
4. Worker エージェントを作成・タスク送信
5. 進捗を監視し、結果確認後 Owner に報告

### Worker の役割

1. 指示されたタスクを実装
2. コミット・プッシュし、ベースブランチにマージ
3. Admin に完了報告

**MCP 自動処理**:

- `send_task`: 7セクション構造、ペルソナ、メモリ検索を自動統合
- `report_task_completion`: メモリ保存、メトリクス更新を自動実行

---

## Phase 4: 結果確認 + PR 作成（Owner が実行）

### ステップ 1: 結果統合確認

```bash
git checkout feature/{issue番号}
git pull origin feature/{issue番号}
```

### ステップ 2: クリーンアップ

```
mcp__multi-agent-mcp__check_all_tasks_completed
mcp__multi-agent-mcp__cleanup_on_completion  # ターミナル自動終了
```

### ステップ 3: セキュリティチェック＆自己レビュー

```bash
git status  # .env*, *.pem, credentials.json を検出したら警告
git diff main...feature/{issue番号}
```

### ステップ 4: ユーザー確認

```
## 変更内容の確認

### 並列実行結果
- Worker 1: {Task 1} ✅ 完了
- Worker 2: {Task 2} ✅ 完了
...

### 変更サマリー
{git diff --stat}

### コミットメッセージ
{自動生成されたメッセージ}

この内容でコミット・プッシュ・PR作成を実行してよろしいですか？
```

### ステップ 5: Issue チェックボックス更新

ユーザー確認後、Issue の全てのチェックボックスを完了状態に更新。

### ステップ 6: コミット・プッシュ

```bash
git add .
git commit -m "{コミットメッセージ}"
git push origin feature/{issue番号}
```

### ステップ 7: PR 作成

```bash
gh pr create --title "{PRタイトル}" --body "{PR本文}"
```

**PR 本文**:

```markdown
## 概要
{変更内容の説明}

## 並列実行サマリー
| Worker | Task | 状態 |
|--------|------|------|
| Worker 1 | Task 1 | ✅ 完了 |
| Worker 2 | Task 2 | ✅ 完了 |
...

## 関連 Issue
Closes #{issue番号}

## テスト計画
- [ ] {テスト項目}
```

### ステップ 8: 完了報告

```
## 開発フロー完了

### 作成された Issue
- #{issue番号}: {タイトル}

### 作成された PR
- PR #{pr番号}: {タイトル}
- URL: {pr_url}

PR がマージされると Issue #{issue番号} は自動的にクローズされます。
```

---

## 重要な注意事項

### Owner がやること

- ✅ Issue 作成
- ✅ ブランチ作成
- ✅ MCP ワークスペース初期化
- ✅ tmux セッション作成
- ✅ Owner/Admin エージェント作成
- ✅ Admin に `send_task` で計画書送信
- ✅ Admin の完了を待機
- ✅ 結果確認・クリーンアップ
- ✅ PR 作成

### Owner がやらないこと

- ❌ Worker を直接作成（Admin の仕事）
- ❌ タスク分割（Admin の仕事）
- ❌ Worker にタスク直接送信（Admin の仕事）
- ❌ ユーザー確認なしでコミット・プッシュ
- ❌ main ブランチで直接作業

### MCP ツール使用ルール

- MCP ツールは `mcp__multi-agent-mcp__*` 形式で呼び出し
- Worker 数は最大 16
- 各 Worker は git worktree で独立したディレクトリで作業
- Dashboard でタスク進捗を管理
