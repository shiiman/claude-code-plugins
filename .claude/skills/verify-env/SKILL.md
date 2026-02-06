---
name: verify-env
description: MCP マルチエージェント実行環境を事前検証するプリフライトチェック。「環境チェック」「verify-env」「MCP 環境確認」「環境検証」「プリフライト」「セットアップ確認」「tmux チェック」などで起動。tmux/MCP/gtr の状態確認を実行。
allowed-tools: [Read, Bash, Glob, Grep]
user-invocable: true
---

# MCP 環境プリフライトチェック

MCP マルチエージェント実行に必要な環境を事前検証します。

## ワークフロー

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

### 6. サマリーレポート出力

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

## 重要な注意事項

- ✅ 読み取り専用の確認のみ実行（環境を変更しない）
- ✅ 問題がある場合は具体的な解決策を提示
- ❌ 環境の自動修正は行わない（ユーザーに判断を委ねる）
