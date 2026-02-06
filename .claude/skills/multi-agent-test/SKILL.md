---
name: multi-agent-test
description: MCP マルチエージェント環境検証と Admin 起動を一括実行する。「マルチエージェントテスト」「multi-agent-test」「MCP テスト」「環境チェック」「Admin 起動」「マルチエージェント起動」「MCP 起動」などで起動。プリフライトチェック後に Admin を生成。
allowed-tools: [Read, Bash, Glob, Grep]
context: fork
user-invocable: true
---

# MCP マルチエージェント テスト & 起動

環境のプリフライトチェックを実行し、問題なければ Admin エージェントを起動します。

## 引数

- `--check-only`: 環境チェックのみ実行（Admin 起動をスキップ）
- `--session-id`: セッション ID（省略時: 現在のブランチ名を使用）
- `--task`: Admin に送信するタスク概要（省略時: ユーザーに確認）

## Phase 1: プリフライトチェック

### 1. tmux 確認

```bash
which tmux
tmux -V
```

- tmux がインストールされているか確認
- バージョンを表示

### 2. tmux セッション確認

```bash
tmux ls 2>/dev/null || echo "セッションなし"
```

- 既存の tmux セッションを一覧表示
- multi-agent-mcp 関連のセッションが残っていないか確認

### 3. .gtrconfig 確認

プロジェクトルートに `.gtrconfig` が存在するか確認。

- 存在する場合: 内容を簡易表示（copy/exclude 設定）
- 存在しない場合: NG として報告（`/shiiman-git:gtrconfig-setup` で作成可能と案内）

### 4. MCP サーバー設定確認

`~/.claude.json` または `~/.claude/settings.local.json` を読み込み、multi-agent-mcp の MCP サーバー設定が存在するか確認。

- `mcpServers` に `multi-agent-mcp` エントリがあるか
- コマンドパスが有効か

### 5. 残存セッションディレクトリ確認

```bash
ls -la .multi-agent-mcp/ 2>/dev/null || echo "残存なし"
```

- 前回のセッションディレクトリが残っていないか確認
- 残っている場合: クリーンアップを推奨

### 6. チェック結果レポート

以下の形式でレポートを出力:

```
## MCP 環境チェック結果

| チェック項目 | 状態 | 詳細 |
|-------------|------|------|
| tmux        | ✅/❌ | バージョン情報 |
| tmux セッション | ✅/⚠️ | 残存セッション数 |
| .gtrconfig  | ✅/❌ | 存在有無 |
| MCP サーバー設定 | ✅/❌ | 設定の有無 |
| 残存セッション | ✅/⚠️ | ディレクトリの有無 |

{問題がある場合の推奨アクション}
```

**❌ が1つでもある場合**: 問題を報告して停止。修正後に再実行を促す。
**`--check-only` の場合**: ここで終了。

---

## Phase 2: Admin エージェント起動

プリフライトチェックが全て OK の場合のみ実行。

### 7. session_id の決定

```bash
git branch --show-current
```

- ユーザー指定がある場合はそちらを優先
- ブランチ名が `main` や `master` の場合は警告し、ユーザーに確認

### 8. Owner エージェント作成

MCP ツール `create_agent` を使用:

- `caller_agent_id`: "owner"（固定）
- `session_id`: ステップ 7 で決定した値
- `role`: "owner"
- `name`: "owner"

### 9. tmux ワークスペース初期化

MCP ツール `init_tmux_workspace` を使用:

- `caller_agent_id`: "owner"
- `session_id`: ステップ 7 で決定した値

### 10. Admin エージェント作成

MCP ツール `create_agent` を使用:

- `caller_agent_id`: "owner"
- `session_id`: ステップ 7 で決定した値
- `role`: "admin"
- `name`: "admin"

### 11. ロールガイド取得

MCP ツール `get_role_guide` を使用:

- `role`: "admin"

取得したガイドを Admin への指示に含める。

### 12. Admin にタスク送信

MCP ツール `send_task` を使用:

- `caller_agent_id`: "owner"
- `session_id`: ステップ 7 で決定した値
- `agent_id`: ステップ 10 で作成した Admin の ID
- `task`: ユーザー指定のタスク概要 + ロールガイド

### 13. 起動完了レポート

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
- ✅ 読み取り専用チェックで環境を変更しない（Phase 1）
- ❌ Admin 起動後にポーリングループで監視しない
- ❌ ブランチが main/master の場合は警告なしで進めない
- ❌ プリフライトチェック NG のまま Admin を起動しない
