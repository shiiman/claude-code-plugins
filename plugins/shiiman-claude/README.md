# shiiman-claude

Claude Code プロジェクト設定管理プラグイン - MCP サーバー管理、Claude 設定管理、Claude リソース一覧表示、Claude Code CLI 更新を提供します。

## インストール

```bash
# マーケットプレイスを追加（初回のみ）
/plugin marketplace add shiiman/claude-code-plugins

# プラグインをインストール
/plugin install shiiman-claude@shiiman-claude-code-plugins
```

## 機能一覧

| 機能         | スキル                       | 説明                                                                            |
| ------------ | ---------------------------- | ------------------------------------------------------------------------------- |
| MCP 管理     | shiiman-claude:mcp           | MCP サーバーの一覧・追加・削除を統合管理                                        |
| 設定管理     | shiiman-claude:settings      | `.claude/settings.json` と `.claude/settings.local.json` の表示・更新を統合管理 |
| リソース一覧 | shiiman-claude:resource-list | Claude リソース（skills/agents/hooks）を一覧表示                                |
| Claude 更新  | shiiman-claude:update        | Claude Code CLI のバージョン確認・更新、プラグイン一括更新を実行                |

## スキル（自然言語トリガー）

以下のような自然言語でスキルを起動できます：

### リソース一覧

| スキル                       | トリガー例                                                              |
| ---------------------------- | ----------------------------------------------------------------------- |
| shiiman-claude:resource-list | 「Claude リソース一覧」「スキル一覧」「エージェント一覧」「フック一覧」 |

### MCP 管理

| スキル             | トリガー例                                           |
| ------------------ | ---------------------------------------------------- |
| shiiman-claude:mcp | 「MCP 管理」「MCP 一覧」「MCP を追加」「MCP を削除」 |

### 設定管理

| スキル                  | トリガー例                                                                    |
| ----------------------- | ----------------------------------------------------------------------------- |
| shiiman-claude:settings | 「Claude 設定管理」「設定を表示」「settings を更新」「local settings を更新」 |

### Claude 更新

| スキル                | トリガー例                                                                                                          |
| --------------------- | ------------------------------------------------------------------------------------------------------------------- |
| shiiman-claude:update | 「Claude を更新」「claude update」「Claude のバージョン確認」「Claude を最新に」「プラグイン更新」「plugin update」 |

## ライセンス

MIT
