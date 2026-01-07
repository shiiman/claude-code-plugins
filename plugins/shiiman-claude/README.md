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

| 機能 | コマンド | スキル | 説明 |
|------|----------|--------|------|
| コマンド追加 | `/shiiman-claude:create-command` | command-creator | `.claude/commands/` にファイル作成 |
| スキル追加 | `/shiiman-claude:create-skill` | skill-creator | `.claude/skills/` にファイル作成 |
| エージェント追加 | `/shiiman-claude:create-subagent` | subagent-creator | `.claude/agents/` にファイル作成 |
| フック追加 | `/shiiman-claude:create-hook` | hook-creator | `.claude/settings.json` に hooks 追加 |
| リソース一覧 | `/shiiman-claude:list` | resource-lister | プロジェクトリソースを一覧表示 |
| 設定表示 | - | settings-viewer | 現在の設定を整形表示 |
| フック一覧 | - | hook-lister | 設定済みフックを一覧表示 |
| フック削除 | - | hook-remover | フックを削除 |
| MCP 一覧 | - | mcp-lister | MCP サーバー一覧を表示 |
| MCP 追加 | - | mcp-installer | MCP サーバーをインストール |
| MCP 削除 | - | mcp-remover | MCP サーバーを削除 |
| 設定更新 | - | settings-updater | `.claude/settings.json` を編集 |
| ローカル設定更新 | - | local-settings-updater | `.claude/settings.local.json` を編集 |
| ドキュメント更新 | - | docs-updater | `CLAUDE.md` を編集 |
| モデル切り替え | - | model-switcher | タスク種類に応じて自動切り替え |
| コンテキスト管理 | - | context-manager | 自動 compact 実行 |
| ultrathink | - | ultrathink | 深思考モード自動切り替え |

## コマンド

### `/shiiman-claude:create-command`

プロジェクトの `.claude/commands/` に新しいコマンドを作成します。

```bash
/shiiman-claude:create-command
```

### `/shiiman-claude:create-skill`

プロジェクトの `.claude/skills/` に新しいスキルを作成します。

```bash
/shiiman-claude:create-skill
```

### `/shiiman-claude:create-subagent`

プロジェクトの `.claude/agents/` に新しいサブエージェントを作成します。

```bash
/shiiman-claude:create-subagent
```

### `/shiiman-claude:create-hook`

プロジェクトの `.claude/settings.json` に新しいフックを追加します。

```bash
/shiiman-claude:create-hook
```

### `/shiiman-claude:list`

プロジェクトの Claude Code リソース（コマンド/スキル/エージェント/フック）を一覧表示します。

```bash
/shiiman-claude:list              # すべて表示
/shiiman-claude:list --commands   # コマンドのみ
/shiiman-claude:list --skills     # スキルのみ
/shiiman-claude:list --agents     # エージェントのみ
/shiiman-claude:list --hooks      # フックのみ
```

## スキル（自然言語トリガー）

以下のような自然言語でスキルを起動できます：

### リソース作成

| スキル | トリガー例 |
|--------|------------|
| command-creator | 「コマンドを追加して」「新しいコマンドを作って」 |
| skill-creator | 「スキルを追加して」「新しいスキルを作って」 |
| subagent-creator | 「エージェントを追加して」「サブエージェントを作って」 |
| hook-creator | 「フックを追加して」「新しいフックを作って」 |

### 情報表示

| スキル | トリガー例 |
|--------|------------|
| resource-lister | 「リソース一覧」「コマンド一覧」「スキル一覧」 |
| settings-viewer | 「設定を見せて」「現在の設定」「settings 確認」 |
| hook-lister | 「フック一覧」「設定済みフック」 |
| mcp-lister | 「MCP 一覧」「MCP サーバー確認」 |

### 設定管理

| スキル | トリガー例 |
|--------|------------|
| settings-updater | 「設定を更新して」「permissions を追加して」 |
| local-settings-updater | 「ローカル設定を更新して」「個人用設定を変更」 |
| docs-updater | 「CLAUDE.md を更新して」「ルールを追加して」 |
| hook-remover | 「フック削除」「フックを消して」 |
| mcp-installer | 「MCP インストール」「MCP を追加」 |
| mcp-remover | 「MCP 削除」「MCP を外して」 |

### 自動機能

| スキル | 説明 |
|--------|------|
| model-switcher | タスクの複雑さに応じて自動切り替え |
| context-manager | タスクの区切りで自動 compact |
| ultrathink | 複雑な問題で自動的に深思考モード |

## ライセンス

MIT
