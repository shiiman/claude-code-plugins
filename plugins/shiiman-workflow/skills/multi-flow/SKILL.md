---
name: multi-flow
description: MCP マルチエージェントで Issue/PR なしに並列実行する軽量フロー。「マルチフロー」「multi-flow」「並列軽量フロー」「マルチエージェント実行」「複数人で実行」「並列フロー」「マルチ軽量」などで起動。複数 Worker でタスクを並列実行しコミットメッセージを出力。
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, EnterPlanMode, TodoWrite, Task]
context: fork
user-invocable: true
---

# Multi Flow

MCP マルチエージェントで Issue/PR なしに並列実行する軽量フロー。

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
Phase 1: Owner  → ブランチ作成 → MCP 初期化 → Admin 起動 → 計画書送信
Phase 2-4: Admin/Worker が自律実行（MCP が自動制御）
Phase 5: Owner  → 結果確認 → クリーンアップ → コミットメッセージ出力
```

## Owner の役割（MCP から取得）

```
mcp__multi-agent-mcp__get_role_guide(role="owner")
```

---

## Phase 1: セットアップ + Admin 起動

### ステップ 1: ブランチ作成

```bash
git fetch origin main
git checkout main
git pull origin main
git checkout -b feature/{slug}
git push -u origin feature/{slug}
```

**slug の生成ルール**: タスク内容から簡潔な英語キーワードに変換

### ステップ 2: MCP ワークスペース初期化

```
mcp__multi-agent-mcp__init_workspace(workspace_path="プロジェクト名")
```

### ステップ 3: tmux ワークスペース作成

```
mcp__multi-agent-mcp__init_tmux_workspace(
    working_dir="プロジェクトのルートパス",
    open_terminal=true,
    auto_setup_gtr=true
)
```

### ステップ 3.5: モデルプロファイル設定（`--profile` 指定時のみ）

```
mcp__multi-agent-mcp__switch_model_profile(profile="standard" or "performance")
```

### ステップ 4: エージェント作成

```
mcp__multi-agent-mcp__create_agent(role="owner", working_dir="パス")
mcp__multi-agent-mcp__create_agent(role="admin", working_dir="パス")
```

### ステップ 5: Admin に計画書を送信

```
mcp__multi-agent-mcp__send_task(
    agent_id="Admin の ID",
    task_content="計画書またはタスク説明",
    session_id="ブランチの slug",
    worker_count=N,
    branch_name="feature/{slug}"
)
```

### ステップ 6: Admin の完了を待機

```
mcp__multi-agent-mcp__get_dashboard_summary()
mcp__multi-agent-mcp__read_messages()
```

---

## Phase 2-4: Admin/Worker の自律実行

**MCP が自動制御。Owner は待機のみ。**

---

## Phase 5: 結果確認 + コミットメッセージ出力

### ステップ 0: Admin からの完了報告を確認

```
mcp__multi-agent-mcp__read_messages()
```

### ステップ 1: 結果統合確認

```bash
git checkout feature/{slug}
git pull origin feature/{slug}
```

### ステップ 2: クリーンアップ

```
mcp__multi-agent-mcp__check_all_tasks_completed()
mcp__multi-agent-mcp__cleanup_on_completion()
```

### ステップ 3: セキュリティチェック

```bash
git status  # .env*, *.pem, credentials.json を検出したら警告
git diff main...feature/{slug}
```

### ステップ 4: ユーザー確認

変更内容、並列実行結果、推奨コミットメッセージを表示してユーザーに確認。

### ステップ 5: コミットメッセージ出力

**重要: このフローではコミット・プッシュ・PR作成を行いません。**

```
## 実装完了

### 推奨コミットメッセージ
{Conventional Commits 形式}

### 次のステップ（手動）
1. git add .
2. git commit -m "{メッセージ}"
3. git push origin feature/{slug}
4. 必要に応じて gh pr create
```
