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

## 引数

- `--plan`: plan mode で計画書を新規作成してから実行
- `--workers N`: Worker 数を指定（省略時はプロファイル設定に従う）
- `--profile standard|performance`: モデルプロファイル選択
- `--help`: ヘルプを表示
- `[タスク説明]`: 計画書なしで直接実行（簡単なタスク用）

## 実行フロー

```
Phase 1: Owner  → Issue 作成 → ブランチ作成 → MCP 初期化 → Admin 起動 → 計画書送信
Phase 2-4: Admin/Worker が自律実行（MCP が自動制御）
Phase 5: Owner  → 結果確認 → クリーンアップ → PR 作成 → Issue クローズ
```

## ⚠️ caller_agent_id について（重要）

**全ての MCP ツールには `caller_agent_id` パラメータが必須です。**

- `create_agent()` の戻り値から自分の ID を取得
- 以降の全ツール呼び出しで `caller_agent_id="{owner_id}"` を指定

## Owner の役割（MCP から取得）

```
mcp__multi-agent-mcp__get_role_guide(role="owner", caller_agent_id="{owner_id}")
```

---

## Phase 1: Issue 作成 + セットアップ + Admin 起動

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

### ステップ 3: tmux ワークスペース初期化

```
mcp__multi-agent-mcp__init_tmux_workspace(
    working_dir="プロジェクトのルートパス",
    open_terminal=true,
    auto_setup_gtr=true,
    session_id="{issue番号}",
    caller_agent_id="{owner_id}"
)
```

**重要**: `session_id` には Issue 番号を指定。これにより MCP ディレクトリ（デフォルト: `.multi-agent-mcp`）の `{issue番号}/` 配下に全てのセッションデータが配置される。

### ステップ 3.5: モデルプロファイル設定（`--profile` 指定時のみ）

```
mcp__multi-agent-mcp__switch_model_profile(
    profile="standard" or "performance",
    caller_agent_id="{owner_id}"
)
```

### ステップ 4: エージェント作成

```
owner_result = mcp__multi-agent-mcp__create_agent(role="owner", working_dir="パス")
# owner_result["agent_id"] を {owner_id} として保存

admin_result = mcp__multi-agent-mcp__create_agent(
    role="admin",
    working_dir="パス",
    caller_agent_id="{owner_id}"
)
# admin_result["agent_id"] を {admin_id} として保存
```

### ステップ 5: Admin に計画書を送信

```
mcp__multi-agent-mcp__send_task(
    agent_id="{admin_id}",
    task_content="計画書またはタスク説明",
    session_id="Issue 番号",
    worker_count=N,
    branch_name="feature/{issue番号}",
    caller_agent_id="{owner_id}"
)
```

### ステップ 6: Admin の完了を待機

```
mcp__multi-agent-mcp__get_dashboard_summary(caller_agent_id="{owner_id}")
mcp__multi-agent-mcp__read_messages(caller_agent_id="{owner_id}")
```

---

## Phase 2-4: Admin/Worker の自律実行

**MCP が自動制御。Owner は待機のみ。**

---

## Phase 5: 結果確認 + PR 作成

### ステップ 0: Admin からの完了報告を確認

```
mcp__multi-agent-mcp__read_messages(caller_agent_id="{owner_id}")
```

### ステップ 1: 結果統合確認

```bash
git checkout feature/{issue番号}
git pull origin feature/{issue番号}
```

### ステップ 2: クリーンアップ

```
mcp__multi-agent-mcp__check_all_tasks_completed(caller_agent_id="{owner_id}")
mcp__multi-agent-mcp__cleanup_on_completion(caller_agent_id="{owner_id}")
```

### ステップ 3: セキュリティチェック

```bash
git status  # .env*, *.pem, credentials.json を検出したら警告
git diff main...feature/{issue番号}
```

### ステップ 4: ユーザー確認

変更内容、並列実行結果、コミットメッセージを表示してユーザーに確認。

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
