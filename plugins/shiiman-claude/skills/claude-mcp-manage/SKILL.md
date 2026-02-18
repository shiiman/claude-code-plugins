---
name: claude-mcp-manage
description: MCP サーバーの一覧表示・追加・削除を一つのスキルで管理する。「MCP 管理」「MCP 一覧」「MCP を追加」「MCP を削除」「MCP サーバー管理」「MCP 設定」「MCP 操作」などで起動。引数があれば優先し、なければ発話内容から list/install/remove を判定。
allowed-tools: [Bash, AskUserQuestion]
argument-hint: "[list|install|remove] [--help]"
---

# Claude MCP Manage

MCP サーバーの一覧表示・追加・削除を統合して管理します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/claude-mcp-manage - MCP サーバー管理

概要:
  MCP サーバーの一覧表示・追加・削除を一つのスキルで管理する。
  引数があれば優先し、なければ発話内容から操作を判定。

使用方法:
  /claude-mcp-manage [操作] [オプション]

操作:
  list     MCP サーバー一覧を表示
  install  MCP サーバーを追加
  remove   MCP サーバーを削除

オプション:
  --help   このヘルプを表示

例:
  /claude-mcp-manage              # 発話内容から操作を判定
  /claude-mcp-manage list         # MCP サーバー一覧を表示
  /claude-mcp-manage install      # MCP サーバーを追加
  /claude-mcp-manage remove       # MCP サーバーを削除
```

## 実行手順

### 1. 操作種別の決定

- 引数が指定されていれば引数を優先
- 引数がない場合は発話内容から以下を判定:
  - 一覧系: list
  - 追加系: install
  - 削除系: remove

### 2. 操作の実行

#### list

1. `claude mcp list` を実行
2. 結果を整形して表示

#### install

1. ユーザーに以下を確認:
   - サーバー名（例: github, filesystem, puppeteer）
   - スコープ（`user` または `project`）
2. 実行内容を確認してから `claude mcp add <name> --scope <scope>` を実行
3. 必要な環境変数がある場合は案内

#### remove

1. `claude mcp list` で現在の一覧を表示
2. ユーザーに削除対象のサーバー名を確認
3. 実行内容を確認してから `claude mcp remove <name>` を実行

## 人気の MCP サーバー

| 名前 | 説明 | 必要な環境変数 |
|------|------|----------------|
| github | GitHub API 操作 | GITHUB_PERSONAL_ACCESS_TOKEN |
| filesystem | ファイルシステム操作 | なし |
| puppeteer | ブラウザ自動化 | なし |
| postgres | PostgreSQL 操作 | DATABASE_URL |
| sqlite | SQLite 操作 | なし |

## 出力フォーマット

```markdown
## MCP サーバー管理

### 実行モード
- list / install / remove

### 結果
- 実行コマンド: claude mcp ...
- ステータス: 成功 / 失敗
- 補足: 必要なら環境変数の案内
```

## 重要な注意事項

- ✅ install/remove は実行前に必ず確認する
- ✅ list ではサーバーが0件のケースを考慮する
- ✅ 必要な環境変数を案内する
- ❌ 環境変数の値そのものは設定しない
