---
name: spawn-admin
description: MCP Admin エージェントを標準化された手順で生成する。「Admin 起動」「spawn-admin」「管理エージェント作成」「Admin を作って」「Admin スポーン」「管理者エージェント起動」「MCP Admin 生成」などで起動。Owner/Admin の初期化を自動実行。
allowed-tools: [Bash, Read, Glob]
context: fork
user-invocable: true
---

# MCP Admin エージェント起動

MCP マルチエージェントの Admin を標準化された手順で起動します。

## 引数

- `--session-id`: セッション ID（省略時: 現在のブランチ名を使用）
- `--task`: Admin に送信するタスク概要（省略時: ユーザーに確認）

## ワークフロー

### 0. プリフライトチェック

verify-env と同等のチェックを実行:

1. `which tmux` で tmux の存在確認
2. `tmux ls` で既存セッションの確認
3. `.gtrconfig` の存在確認
4. MCP サーバー設定の確認

**いずれかが NG の場合**: 問題を報告して停止。`/verify-env` の実行を推奨。

### 1. session_id の決定

```bash
# ブランチ名から取得（デフォルト）
git branch --show-current
```

- ユーザー指定がある場合はそちらを優先
- ブランチ名が `main` や `master` の場合は警告し、ユーザーに確認

### 2. Owner エージェント作成

MCP ツール `create_agent` を使用:

- `caller_agent_id`: "owner"（固定）
- `session_id`: ステップ 1 で決定した値
- `role`: "owner"
- `name`: "owner"

### 3. tmux ワークスペース初期化

MCP ツール `init_tmux_workspace` を使用:

- `caller_agent_id`: "owner"
- `session_id`: ステップ 1 で決定した値

### 4. Admin エージェント作成

MCP ツール `create_agent` を使用:

- `caller_agent_id`: "owner"
- `session_id`: ステップ 1 で決定した値
- `role`: "admin"
- `name`: "admin"

### 5. ロールガイド取得

MCP ツール `get_role_guide` を使用:

- `role`: "admin"

取得したガイドを Admin への指示に含める。

### 6. Admin にタスク送信

MCP ツール `send_task` を使用:

- `caller_agent_id`: "owner"
- `session_id`: ステップ 1 で決定した値
- `agent_id`: ステップ 4 で作成した Admin の ID
- `task`: ユーザー指定のタスク概要 + ロールガイド

### 7. 状態確認

MCP ツール `get_dashboard` を使用してダッシュボードを表示:

```
## 起動完了

- Session ID: {session_id}
- Owner: 作成済み
- Admin: タスク送信済み
- ダッシュボード: {dashboard_url}

Admin がタスクを受信し、Worker の生成を開始します。
進捗は `get_dashboard` で確認できます。
```

## 重要な注意事項

- ✅ すべての MCP ツール呼び出しに `caller_agent_id` を必ず指定
- ✅ Admin↔Worker 通知はイベント駆動（ポーリング禁止）
- ✅ プリフライトチェックで環境問題を事前検知
- ❌ Admin 起動後にポーリングループで監視しない
- ❌ ブランチが main/master の場合は警告なしで進めない
