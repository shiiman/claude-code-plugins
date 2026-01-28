---
name: hook-create
description: プラグインに新しいフックを作成する。「フック作成」「新しいフック」「フックを作って」「フック追加」「hook 作成」「フックを追加したい」「新規フック」などで起動。ツール実行前後やセッションイベントで実行されるフックを生成。
allowed-tools: [Read, Write, Bash, Glob]
---

# Create Hook

プラグインに新しいフックを作成します。

## ワークフロー

### 1. 情報収集

ユーザーに以下を聞く:

1. **対象プラグイン** - どのプラグインにフックを追加するか
   - `plugins/` ディレクトリから既存プラグインを一覧表示

2. **イベント** - いつ実行するか
   - `PreToolUse`: ツール実行前（ブロック可能、matcher 必須）
   - `PostToolUse`: ツール実行後（matcher 必須）
   - `UserPromptSubmit`: ユーザープロンプト送信時
   - `Notification`: 通知時
   - `Stop`: レスポンス完了時
   - `SubagentStop`: サブエージェント完了時
   - `PreCompact`: Compact 操作前
   - `SessionStart`: セッション開始時
   - `SessionEnd`: セッション終了時

3. **マッチャー**（PreToolUse / PostToolUse の場合のみ）
   - 例: `Bash`, `Write`, `Edit|Write`, `*`（すべて）

4. **フックタイプ**
   - `command`: Bash コマンドを実行
   - `prompt`: LLM（Haiku）で評価

5. **実行するコマンド**（type: command の場合）
   - 例: `npm run lint`, `echo "完了"`

### 2. 検証

- プラグインが存在するか確認
- イベントが有効か確認
- PreToolUse / PostToolUse の場合、マッチャーが指定されているか確認

### イベント一覧

| イベント           | matcher | 説明                           |
|--------------------|---------|--------------------------------|
| `PreToolUse`       | 必須    | ツール実行前（ブロック可能）   |
| `PostToolUse`      | 必須    | ツール実行後                   |
| `UserPromptSubmit` | 不要    | ユーザープロンプト送信時       |
| `Notification`     | 不要    | 通知時                         |
| `Stop`             | 不要    | レスポンス完了時               |
| `SubagentStop`     | 不要    | サブエージェント完了時         |
| `PreCompact`       | 不要    | Compact 操作前                 |
| `SessionStart`     | 不要    | セッション開始時               |
| `SessionEnd`       | 不要    | セッション終了時               |

### 3. settings.json の hooks セクションを更新

`plugins/{plugin-name}/.claude/settings.json` の hooks セクションを更新（ファイルがなければ作成）:

**PreToolUse / PostToolUse の場合（matcher 必須）:**

```json
{
  "hooks": {
    "{イベント}": [
      {
        "matcher": "{マッチャー}",
        "hooks": [
          {
            "type": "command",
            "command": "{コマンド}"
          }
        ]
      }
    ]
  }
}
```

**その他のイベントの場合（matcher 不要）:**

```json
{
  "hooks": {
    "{イベント}": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "{コマンド}"
          }
        ]
      }
    ]
  }
}
```

既存の hooks セクションがある場合は、適切なイベントに追加する。

### 4. プラグイン README を更新

`plugins/{plugin-name}/README.md` のフックセクションにフックを追加。

### 5. 報告

作成されたファイルと次のステップを表示:

```text
フックを作成しました: {イベント} {マッチャー（あれば）}

更新:
- plugins/{plugin-name}/.claude/settings.json
- plugins/{plugin-name}/README.md

次のステップ:
- /create-hook で別のフックを追加
- /create-command でコマンドを追加
- /create-skill でスキルを追加
- /create-subagent でサブエージェントを追加
```

## 重要な注意事項

- ✅ PreToolUse / PostToolUse には必ず matcher を指定
- ✅ settings.json の hooks セクションに設定
- ❌ matcher が必要なイベントで matcher を省略しない
