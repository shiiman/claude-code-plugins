# shiiman-claude

Claude Code プロジェクト設定管理プラグイン - コマンド/スキル/エージェント/フックの追加、設定更新、ドキュメント更新、モデル切り替え、コンテキスト管理機能を提供します。

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
| 設定更新 | - | settings-updater | `.claude/settings.json` を編集 |
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

## スキル（自然言語トリガー）

以下のような自然言語でスキルを起動できます：

| スキル | トリガー例 |
|--------|------------|
| command-creator | 「コマンドを追加して」「新しいコマンドを作って」 |
| skill-creator | 「スキルを追加して」「新しいスキルを作って」 |
| subagent-creator | 「エージェントを追加して」「サブエージェントを作って」 |
| hook-creator | 「フックを追加して」「新しいフックを作って」 |
| settings-updater | 「設定を更新して」「permissions を追加して」 |
| docs-updater | 「CLAUDE.md を更新して」「ルールを追加して」 |
| model-switcher | （タスクの複雑さに応じて自動切り替え） |
| context-manager | （タスクの区切りで自動 compact） |
| ultrathink | （複雑な問題で自動的に深思考モード） |

## ライセンス

MIT
