---
name: shiiman-workflow:multi
description: MCP マルチエージェントで Issue/PR なしに並列実行する軽量フロー。「マルチフロー」「workflow-multi」「並列軽量フロー」「マルチエージェント実行」「複数人で実行」「並列フロー」「マルチ軽量」などで起動。複数 Worker でタスクを並列実行しコミットメッセージを出力。
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
argument-hint: "[タスク説明] [--plan|--no-git|--help]"
---

# Multi Flow

MCP マルチエージェントで Issue/PR なしに並列実行する軽量フロー。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-workflow:multi - MCP マルチエージェント軽量フロー

概要:
  MCP マルチエージェントで Issue/PR なしに並列実行する。
  ブランチ作成 → MCP 初期化 → Admin/Worker 並列実行 → コミットメッセージ出力。

使用方法:
  /shiiman-workflow:multi [タスク説明] [オプション]

オプション:
  --plan    plan mode で計画書を新規作成してから実行
  --no-git  git を使わず no-git モードで実行
  --help    このヘルプを表示

例:
  /shiiman-workflow:multi                        # 既存計画書から実行
  /shiiman-workflow:multi --plan                 # 計画書を作成してから実行
  /shiiman-workflow:multi "API リファクタリング"  # タスク説明から直接実行
  /shiiman-workflow:multi --no-git               # git なしモードで実行
```

## 前提条件

- multi-agent-mcp がインストール済み（**必須**）
- tmux がインストール済み（**必須**）
- `gh` コマンドが利用可能
- `gh auth status` が成功する（GitHub CLI 認証済み）

## 実行モード判定（重要）

優先順位は以下。

1. `--no-git` 指定あり: 常に no-git モード
2. `--no-git` 指定なし + `git rev-parse --is-inside-work-tree` 成功: git モード
3. それ以外: no-git モード

判定コマンド:

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1
```

## セッション ID / slug ルール

- slug はタスク内容から簡潔な英語キーワードで作成
- no-git モードでも `session_id` として slug を使用
- slug を生成できない場合は `no-git-task` を使用

## 環境変数

モデルプロファイルは環境変数で設定（`.env` または `export`）:

```bash
MCP_MODEL_PROFILE_ACTIVE=performance  # standard または performance
```

## 実行フロー

```text
git モード:
Phase 1: Owner → ブランチ作成 → MCP 初期化 → Admin 起動 → 計画書送信
Phase 2-4: Admin/Worker が自律実行（MCP が自動制御）
Phase 5: Owner → 結果確認 → 承認/修正依頼 → クリーンアップ → コミットメッセージ出力

no-git モード:
Phase 1: Owner → MCP 初期化(enable_git=false) → Admin 起動 → 計画書送信
Phase 2-4: Admin/Worker が自律実行（MCP が自動制御）
Phase 5: Owner → 結果確認（Admin 報告）→ 承認/修正依頼 → クリーンアップ
```

## ⚠️ caller_agent_id について（重要）

**全ての MCP ツールには `caller_agent_id` パラメータが必須です。**

- `create_agent()` の戻り値から自分の ID を取得
- 以降の全ツール呼び出しで `caller_agent_id="{owner_id}"` を指定

---

## Phase 1: セットアップ + Admin 起動

### ステップ 1: 実行モード判定

```bash
if [ "{no_git_flag}" = "true" ]; then
  FLOW_MODE="no-git"
elif git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  FLOW_MODE="git"
else
  FLOW_MODE="no-git"
fi
```

### ステップ 2: slug を決定

```text
slug = {task_slug}
if slug が空なら slug = "no-git-task"
```

### ステップ 3: git モード時のみブランチ作成

Skill ツールで `shiiman-github:branch-create` を呼び出す。

no-git モードではこのステップをスキップする。
ユーザーがベースブランチを明示した場合は、そちらを優先する。

### ステップ 4: Owner エージェント作成

```
owner_result = mcp__multi-agent-mcp__create_agent(role="owner", working_dir="パス")
# owner_result["agent"]["id"] を {owner_id} として保存
```

### ステップ 5: Owner の役割を取得（🔴 必須）

**Owner として行動する前に、必ずロールガイドを取得してください。**

```
mcp__multi-agent-mcp__get_role_guide(role="owner", caller_agent_id="{owner_id}")
```

### ステップ 6: MCP ワークスペース初期化

git モード:

```
mcp__multi-agent-mcp__init_tmux_workspace(
    working_dir="プロジェクトのルートパス",
    open_terminal=true,
    auto_setup_gtr=true,
    session_id="{slug}",
    caller_agent_id="{owner_id}"
)
```

no-git モード:

```
mcp__multi-agent-mcp__init_tmux_workspace(
    working_dir="プロジェクトのルートパス",
    open_terminal=true,
    auto_setup_gtr=true,
    session_id="{slug}",
    enable_git=false,
    caller_agent_id="{owner_id}"
)
```

**重要**: no-git モードでは `enable_git=false` を必ず渡す。

### ステップ 7: Admin エージェント作成

```
admin_result = mcp__multi-agent-mcp__create_agent(
    role="admin",
    working_dir="パス",
    caller_agent_id="{owner_id}"
)
# admin_result["agent"]["id"] を {admin_id} として保存
```

### ステップ 8: Admin に計画書を送信

git モード:

```
mcp__multi-agent-mcp__send_task(
    agent_id="{admin_id}",
    task_content="計画書またはタスク説明",
    session_id="{slug}",
    branch_name="feature/{slug}",
    caller_agent_id="{owner_id}"
)
```

no-git モード:

```
mcp__multi-agent-mcp__send_task(
    agent_id="{admin_id}",
    task_content="計画書またはタスク説明",
    session_id="{slug}",
    caller_agent_id="{owner_id}"
)
```

**重要**: no-git モードでは `branch_name` を渡さない。

### ステップ 9: Admin の完了を待機

**待機中**: macOS 通知で Admin からの完了報告が届きます。ユーザーから「Admin から完了通知来てるか確認して」と指示されたら Phase 5 へ進みます。

```
mcp__multi-agent-mcp__get_dashboard_summary(caller_agent_id="{owner_id}")
mcp__multi-agent-mcp__read_messages(agent_id="{owner_id}", caller_agent_id="{owner_id}")
```

---

## Phase 2-4: Admin/Worker の自律実行

**MCP が自動制御。Owner は待機のみ。**

---

## Phase 5: 結果確認 + ユーザー承認 + クリーンアップ

### ステップ 0: Admin からの完了報告を確認

```
mcp__multi-agent-mcp__read_messages(
    agent_id="{owner_id}",
    caller_agent_id="{owner_id}"
)
```

### ステップ 1: 変更内容をユーザーに表示

git モード:

```bash
git status --short --branch
git diff
git diff --cached
```

no-git モード:

- Admin の最終報告（実装サマリー・変更ファイル・テスト結果・残課題）をユーザーに表示
- `mcp__multi-agent-mcp__get_dashboard_summary` と `read_messages` の結果を確認対象にする

### ステップ 2: ユーザー確認（🔴 必須）

**⚠️ クリーンアップの前に必ずユーザー確認を行う**

`AskUserQuestion` でユーザーに確認を求める:

```
AskUserQuestion:
  question: "実装内容を確認しました。承認しますか？"
  options:
    - label: "OK（承認）"
      description: "クリーンアップして完了"
    - label: "NG（修正依頼）"
      description: "修正内容を指定して Admin に再指示"
    - label: "保留"
      description: "手動で確認してから判断"
```

### OK（承認）の場合

#### ステップ 3: Admin に承認通知を送信

```
mcp__multi-agent-mcp__send_message(
    sender_id="{owner_id}",
    receiver_id="{admin_id}",
    message_type="task_approved",
    content="ユーザー確認完了。実装を承認します。",
    caller_agent_id="{owner_id}"
)
```

### NG（修正依頼）の場合

1. 修正内容をユーザーに確認
2. Admin に再指示を送信

```
mcp__multi-agent-mcp__send_message(
    sender_id="{owner_id}",
    receiver_id="{admin_id}",
    message_type="request",
    content="修正依頼: {ユーザーからの修正内容}",
    caller_agent_id="{owner_id}"
)
```

3. Phase 2-4 に戻り、Admin が修正タスクを実行

#### ステップ 4: クリーンアップ

```
mcp__multi-agent-mcp__check_all_tasks_completed(caller_agent_id="{owner_id}")
mcp__multi-agent-mcp__cleanup_on_completion(caller_agent_id="{owner_id}")
```

#### ステップ 5: セキュリティチェック

git モード:

```bash
git status  # .env*, *.pem, credentials.json を検出したら警告
```

no-git モード:

```bash
find . -maxdepth 3 \( -name ".env*" -o -name "*.pem" -o -name "credentials.json" \)
```

#### ステップ 6: 完了出力

git モード:

**重要: このフローではコミット・プッシュ・PR作成を行いません。**

```text
## 実装完了

### 推奨コミットメッセージ
{Conventional Commits 形式}

### 次のステップ

プッシュするには以下を実行:

git push -u origin feature/{slug}

必要に応じて gh pr create
```

no-git モード:

```text
## 実装完了（no-git モード）

### 実装サマリー
- 変更ファイル: {admin_report_files}
- テスト結果: {admin_report_tests}
- 残課題: {admin_report_todos}

### 次のステップ
- 必要に応じてユーザー環境の手順に沿って成果物を反映
```
