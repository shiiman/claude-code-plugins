# フック作成ガイド

## 概要

フックは特定のイベント（ツール実行前後、セッション開始時など）で自動的に実行されるスクリプトです。

## 配置場所

フックは `settings.json` の `hooks` セクションに設定します。

### プラグインの場合

```text
plugins/{plugin-name}/.claude/settings.json
```

### プロジェクト固有の場合

```text
.claude/settings.json
```

## Hook イベント

| イベント           | 説明                         | matcher |
| ------------------ | ---------------------------- | ------- |
| `PreToolUse`       | ツール実行前（ブロック可能） | 必須    |
| `PostToolUse`      | ツール実行後                 | 必須    |
| `UserPromptSubmit` | ユーザープロンプト送信時     | 不要    |
| `Notification`     | 通知時                       | 不要    |
| `Stop`             | レスポンス完了時             | 不要    |
| `SubagentStop`     | サブエージェント完了時       | 不要    |
| `PreCompact`       | Compact 操作前               | 不要    |
| `SessionStart`     | セッション開始時             | 不要    |
| `SessionEnd`       | セッション終了時             | 不要    |

## Hook タイプ

| タイプ    | 説明                |
| --------- | ------------------- |
| `command` | Bash コマンドを実行 |
| `prompt`  | LLM（Haiku）で評価  |

## 設定形式

### settings.json に設定する場合

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "ツール名またはパターン",
        "hooks": [
          {
            "type": "command",
            "command": "実行するコマンド",
            "timeout": 60
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'セッション開始'"
          }
        ]
      }
    ]
  }
}
```

## マッチャーパターン

| パターン       | 説明                 | 例                          |
| -------------- | -------------------- | --------------------------- |
| 完全一致       | 正確なツール名       | `Bash`, `Write`             |
| ワイルドカード | すべてのツール       | `*` または `""`             |
| 正規表現       | OR / パターンマッチ  | `Edit\|Write`, `Notebook.*` |
| MCP ツール     | MCP サーバーのツール | `mcp__github__.*`           |

## 利用可能なツール名

```
Bash, Glob, Grep, Read, Edit, Write, Task,
WebFetch, WebSearch, SlashCommand, Notebook, ...
```

## 例

### PreToolUse: Bash 実行前チェック

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo '実行前チェック'"
          }
        ]
      }
    ]
  }
}
```

### PostToolUse: ファイル書き込み後の処理

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'ファイル変更完了'"
          }
        ]
      }
    ]
  }
}
```

### SessionStart: セッション開始時の処理

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'セッション開始'"
          }
        ]
      }
    ]
  }
}
```

## ユースケース

- ツール実行前のセキュリティチェック
- ファイル保存後のフォーマット/リント
- セッション開始時の環境セットアップ
- レスポンス完了時の通知
