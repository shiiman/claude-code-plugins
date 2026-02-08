# shiiman-claude

Claude Code プロジェクト設定管理プラグイン - スキル/エージェント/フックの追加、設定更新、ドキュメント更新、モデル切り替え、コンテキスト管理、MCP サーバー管理機能を提供します。

## インストール

```bash
# マーケットプレイスを追加（初回のみ）
/plugin marketplace add shiiman/claude-code-plugins

# プラグインをインストール
/plugin install shiiman-claude@shiiman-claude-code-plugins
```

## 機能一覧

| 機能 | スキル | 説明 |
|------|--------|------|
| スキル追加 | skill-create | `.claude/skills/` にファイル作成 |
| エージェント追加 | subagent-create | `.claude/agents/` にファイル作成 |
| フック追加 | hook-create | `.claude/settings.json` に hooks 追加 |
| リソース一覧 | resource-list | プロジェクトリソースを一覧表示 |
| 設定表示 | settings-view | 現在の設定を整形表示 |
| フック一覧 | hook-list | 設定済みフックを一覧表示 |
| フック削除 | hook-remove | フックを削除 |
| MCP 一覧 | mcp-list | MCP サーバー一覧を表示 |
| MCP 追加 | mcp-install | MCP サーバーをインストール |
| MCP 削除 | mcp-remove | MCP サーバーを削除 |
| 設定更新 | settings-update | `.claude/settings.json` を編集 |
| ローカル設定更新 | settings-local-update | `.claude/settings.local.json` を編集 |
| ドキュメント更新 | docs-update | `CLAUDE.md` を編集 |
| モデル切り替え | model-switch | タスク種類に応じて自動切り替え |
| コンテキスト管理 | context-manage | 自動 compact 実行 |
| ultrathink | ultrathink | 深思考モード自動切り替え |

## スキル（自然言語トリガー）

以下のような自然言語でスキルを起動できます：

### リソース作成

| スキル | トリガー例 |
|--------|------------|
| skill-create | 「スキルを追加して」「新しいスキルを作って」 |
| subagent-create | 「エージェントを追加して」「サブエージェントを作って」 |
| hook-create | 「フックを追加して」「新しいフックを作って」 |

### 情報表示

| スキル | トリガー例 |
|--------|------------|
| resource-list | 「リソース一覧」「スキル一覧」「エージェント一覧」 |
| settings-view | 「設定を見せて」「現在の設定」「settings 確認」 |
| hook-list | 「フック一覧」「設定済みフック」 |
| mcp-list | 「MCP 一覧」「MCP サーバー確認」 |

### 設定管理

| スキル | トリガー例 |
|--------|------------|
| settings-update | 「設定を更新して」「permissions を追加して」 |
| settings-local-update | 「ローカル設定を更新して」「個人用設定を変更」 |
| docs-update | 「CLAUDE.md を更新して」「ルールを追加して」 |
| hook-remove | 「フック削除」「フックを消して」 |
| mcp-install | 「MCP インストール」「MCP を追加」 |
| mcp-remove | 「MCP 削除」「MCP を外して」 |

### 自動機能

| スキル | 説明 |
|--------|------|
| model-switch | タスクの複雑さに応じて自動切り替え |
| context-manage | タスクの区切りで自動 compact |
| ultrathink | 複雑な問題で自動的に深思考モード |

## ライセンス

MIT
