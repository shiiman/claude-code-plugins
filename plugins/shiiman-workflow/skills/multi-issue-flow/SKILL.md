---
name: multi-issue-flow
description: MCP マルチエージェントで Issue から PR まで並列実行する開発フロー。「マルチ Issue フロー」「multi-issue-flow」「並列 Issue 開発」「マルチエージェント Issue」「複数人で Issue」「並列 Issue フロー」「マルチフロー Issue」などで起動。複数 Worker でタスクを並列実行。
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, EnterPlanMode, TodoWrite, Task]
context: fork
user-invocable: true
argument-hint: "[タスク説明] [--plan|--help]"
---

# Multi Issue Flow

MCP マルチエージェントで Issue から PR まで並列実行する開発フロー。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/multi-issue-flow - MCP マルチエージェント Issue 開発フロー

概要:
  MCP マルチエージェントで Issue 作成から PR 作成まで並列実行する。
  Issue 作成 → MCP 初期化 → Admin/Worker 並列実行 → コミット → PR 作成。

使用方法:
  /multi-issue-flow [タスク説明] [オプション]

オプション:
  --plan  plan mode で計画書を新規作成してから実行
  --help  このヘルプを表示

例:
  /multi-issue-flow                        # 既存計画書から実行
  /multi-issue-flow --plan                 # 計画書を作成してから実行
  /multi-issue-flow "認証機能を並列実装"    # タスク説明から直接実行
```

## 前提条件

- multi-agent-mcp がインストール済み（**必須**）
- tmux がインストール済み（**必須**）

## 環境変数

モデルプロファイルは環境変数で設定（`.env` または `export`）:

```bash
MCP_MODEL_PROFILE_ACTIVE=performance  # standard または performance
```

## 実行フロー

```
Phase 1: Owner  → Issue 作成 → ブランチ作成 → MCP 初期化 → Admin 起動 → 計画書送信
Phase 2-4: Admin/Worker が自律実行（MCP が自動制御）
Phase 5: Owner  → 結果確認 → ユーザー承認 → クリーンアップ → コミット → PR 作成
```

## ⚠️ caller_agent_id について（重要）

**全ての MCP ツールには `caller_agent_id` パラメータが必須です。**

- `create_agent()` の戻り値から自分の ID を取得
- 以降の全ツール呼び出しで `caller_agent_id="{owner_id}"` を指定

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

### ステップ 3: Owner エージェント作成

```
owner_result = mcp__multi-agent-mcp__create_agent(role="owner", working_dir="パス")
# owner_result["agent"]["id"] を {owner_id} として保存
```

### ステップ 4: Owner の役割を取得（🔴 必須）

**Owner として行動する前に、必ずロールガイドを取得してください。**

```
mcp__multi-agent-mcp__get_role_guide(role="owner", caller_agent_id="{owner_id}")
```

このガイドには Owner の責務、禁止事項、ワークフローが記載されています。

### ステップ 5: MCP ワークスペース初期化

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

### ステップ 6: Admin エージェント作成

```
admin_result = mcp__multi-agent-mcp__create_agent(
    role="admin",
    working_dir="パス",
    caller_agent_id="{owner_id}"
)
# admin_result["agent"]["id"] を {admin_id} として保存
```

### ステップ 7: Admin に計画書を送信

```
mcp__multi-agent-mcp__send_task(
    agent_id="{admin_id}",
    task_content="計画書またはタスク説明",
    session_id="Issue 番号",
    branch_name="feature/{issue番号}",
    caller_agent_id="{owner_id}"
)
```

### ステップ 8: Admin の完了を待機

**待機中**: macOS 通知で Admin からの完了報告が届きます。ユーザーから「Admin から完了通知来てるか確認して」と指示されたら Phase 5 へ進みます。

```
mcp__multi-agent-mcp__get_dashboard_summary(caller_agent_id="{owner_id}")
mcp__multi-agent-mcp__read_messages(agent_id="{owner_id}", caller_agent_id="{owner_id}")
```

---

## Phase 2-4: Admin/Worker の自律実行

**MCP が自動制御。Owner は待機のみ。**

---

## Phase 5: 結果確認 + ユーザー承認 + PR 作成

### ステップ 0: Admin からの完了報告を確認

macOS 通知が届いたら、ユーザーから「Admin から完了通知来てるか確認して」と指示されます。

```
mcp__multi-agent-mcp__read_messages(
    agent_id="{owner_id}",
    caller_agent_id="{owner_id}"
)
```

### ステップ 1: 変更内容をユーザーに表示

```bash
git status --short --branch
git diff
git diff --cached
```

変更内容、品質チェック結果（Admin からの報告）をユーザーに表示。

### ステップ 2: ユーザー確認（🔴 必須）

**⚠️ クリーンアップの前に必ずユーザー確認を行う**

`AskUserQuestion` でユーザーに確認を求める：

```
AskUserQuestion:
  question: "実装内容を確認しました。承認しますか？"
  options:
    - label: "OK（承認）"
      description: "クリーンアップして PR 作成へ進む"
    - label: "NG（修正依頼）"
      description: "修正内容を指定して Admin に再指示"
    - label: "保留"
      description: "手動で確認してから判断"
```

---

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

---

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

---

#### ステップ 4: クリーンアップ

```
mcp__multi-agent-mcp__check_all_tasks_completed(caller_agent_id="{owner_id}")
mcp__multi-agent-mcp__cleanup_on_completion(caller_agent_id="{owner_id}")
```

#### ステップ 5: セキュリティチェック

```bash
git status  # .env*, *.pem, credentials.json を検出したら警告
```

#### ステップ 6: Issue チェックボックス更新

Issue の全てのチェックボックスを完了状態に更新。

#### ステップ 7: コミット・プッシュ

```bash
git add .
git commit -m "{コミットメッセージ}"
git push origin feature/{issue番号}
```

#### ステップ 8: PR 作成

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

#### ステップ 9: 完了報告

```
## 開発フロー完了

### 作成された Issue
- #{issue番号}: {タイトル}

### 作成された PR
- PR #{pr番号}: {タイトル}
- URL: {pr_url}

PR がマージされると Issue #{issue番号} は自動的にクローズされます。
```
