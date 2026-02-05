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
- `--help`: ヘルプを表示
- `[タスク説明]`: 計画書なしで直接実行（簡単なタスク用）

## 環境変数

モデルプロファイルは環境変数で設定（`.env` または `export`）:

```bash
MCP_MODEL_PROFILE_ACTIVE=performance  # standard または performance
```

## 実行フロー

```
Phase 1: Owner  → ブランチ作成 → MCP 初期化 → Admin 起動 → 計画書送信
Phase 2-4: Admin/Worker が自律実行（MCP が自動制御）
Phase 5: Owner  → 結果確認 → クリーンアップ → コミットメッセージ出力
```

## ⚠️ caller_agent_id について（重要）

**全ての MCP ツールには `caller_agent_id` パラメータが必須です。**

- `create_agent()` の戻り値から自分の ID を取得
- 以降の全ツール呼び出しで `caller_agent_id="{owner_id}"` を指定

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

### ステップ 2: Owner エージェント作成

```
owner_result = mcp__multi-agent-mcp__create_agent(role="owner", working_dir="パス")
# owner_result["agent"]["id"] を {owner_id} として保存
```

### ステップ 3: Owner の役割を取得（🔴 必須）

**Owner として行動する前に、必ずロールガイドを取得してください。**

```
mcp__multi-agent-mcp__get_role_guide(role="owner", caller_agent_id="{owner_id}")
```

このガイドには Owner の責務、禁止事項、ワークフローが記載されています。

### ステップ 4: MCP ワークスペース初期化

```
mcp__multi-agent-mcp__init_tmux_workspace(
    working_dir="プロジェクトのルートパス",
    open_terminal=true,
    auto_setup_gtr=true,
    session_id="{slug}",
    caller_agent_id="{owner_id}"
)
```

**重要**: `session_id` には Step 1 で作成したブランチの slug を指定。これにより MCP ディレクトリ（デフォルト: `.multi-agent-mcp`）の `{slug}/` 配下に全てのセッションデータが配置される。

### ステップ 5: Admin エージェント作成

```
admin_result = mcp__multi-agent-mcp__create_agent(
    role="admin",
    working_dir="パス",
    caller_agent_id="{owner_id}"
)
# admin_result["agent"]["id"] を {admin_id} として保存
```

### ステップ 6: Admin に計画書を送信

```
mcp__multi-agent-mcp__send_task(
    agent_id="{admin_id}",
    task_content="計画書またはタスク説明",
    session_id="ブランチの slug",
    worker_count=N,
    branch_name="feature/{slug}",
    caller_agent_id="{owner_id}"
)
```

### ステップ 7: Admin の完了を待機

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

macOS 通知が届いたら、ユーザーから「Admin から完了通知来てるか確認して」と指示されます。

```
mcp__multi-agent-mcp__read_messages(
    agent_id="{owner_id}",
    caller_agent_id="{owner_id}"
)
```

### ステップ 1: 結果統合確認

```bash
git checkout feature/{slug}
git pull origin feature/{slug}
```

### ステップ 2: 変更内容をユーザーに表示

```bash
git diff main...feature/{slug} --stat
git log main..feature/{slug} --oneline
```

変更内容、品質チェック結果（Admin からの報告）をユーザーに表示。

### ステップ 3: ユーザー確認（🔴 必須）

**⚠️ クリーンアップの前に必ずユーザー確認を行う**

`AskUserQuestion` でユーザーに確認を求める：

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

---

### OK（承認）の場合

#### ステップ 4: Admin に承認通知を送信

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

#### ステップ 5: クリーンアップ

```
mcp__multi-agent-mcp__check_all_tasks_completed(caller_agent_id="{owner_id}")
mcp__multi-agent-mcp__cleanup_on_completion(caller_agent_id="{owner_id}")
```

#### ステップ 6: セキュリティチェック

```bash
git status  # .env*, *.pem, credentials.json を検出したら警告
```

#### ステップ 7: コミットメッセージ出力

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
