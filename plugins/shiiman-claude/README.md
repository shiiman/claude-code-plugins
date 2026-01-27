# shiiman-claude

Claude Code プロジェクト設定管理プラグイン - コマンド/スキル/エージェント/フックの追加、設定更新、ドキュメント更新、モデル切り替え、コンテキスト管理、MCP サーバー管理機能を提供します。

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
| コマンド追加 | create-command | `.claude/commands/` にファイル作成 |
| スキル追加 | create-skill | `.claude/skills/` にファイル作成 |
| エージェント追加 | create-subagent | `.claude/agents/` にファイル作成 |
| フック追加 | create-hook | `.claude/settings.json` に hooks 追加 |
| リソース一覧 | list-resources | プロジェクトリソースを一覧表示 |
| 設定表示 | view-settings | 現在の設定を整形表示 |
| フック一覧 | list-hooks | 設定済みフックを一覧表示 |
| フック削除 | remove-hook | フックを削除 |
| MCP 一覧 | list-mcp | MCP サーバー一覧を表示 |
| MCP 追加 | install-mcp | MCP サーバーをインストール |
| MCP 削除 | remove-mcp | MCP サーバーを削除 |
| 設定更新 | update-settings | `.claude/settings.json` を編集 |
| ローカル設定更新 | update-local-settings | `.claude/settings.local.json` を編集 |
| ドキュメント更新 | update-docs | `CLAUDE.md` を編集 |
| モデル切り替え | switch-model | タスク種類に応じて自動切り替え |
| コンテキスト管理 | manage-context | 自動 compact 実行 |
| ultrathink | ultrathink | 深思考モード自動切り替え |

## スキル（自然言語トリガー）

以下のような自然言語でスキルを起動できます：

### リソース作成

| スキル | トリガー例 |
|--------|------------|
| create-command | 「コマンドを追加して」「新しいコマンドを作って」 |
| create-skill | 「スキルを追加して」「新しいスキルを作って」 |
| create-subagent | 「エージェントを追加して」「サブエージェントを作って」 |
| create-hook | 「フックを追加して」「新しいフックを作って」 |

### 情報表示

| スキル | トリガー例 |
|--------|------------|
| list-resources | 「リソース一覧」「コマンド一覧」「スキル一覧」 |
| view-settings | 「設定を見せて」「現在の設定」「settings 確認」 |
| list-hooks | 「フック一覧」「設定済みフック」 |
| list-mcp | 「MCP 一覧」「MCP サーバー確認」 |

### 設定管理

| スキル | トリガー例 |
|--------|------------|
| update-settings | 「設定を更新して」「permissions を追加して」 |
| update-local-settings | 「ローカル設定を更新して」「個人用設定を変更」 |
| update-docs | 「CLAUDE.md を更新して」「ルールを追加して」 |
| remove-hook | 「フック削除」「フックを消して」 |
| install-mcp | 「MCP インストール」「MCP を追加」 |
| remove-mcp | 「MCP 削除」「MCP を外して」 |

### 自動機能

| スキル | 説明 |
|--------|------|
| switch-model | タスクの複雑さに応じて自動切り替え |
| manage-context | タスクの区切りで自動 compact |
| ultrathink | 複雑な問題で自動的に深思考モード |

## ライセンス

MIT
