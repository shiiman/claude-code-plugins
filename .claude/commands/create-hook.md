# Create Hook

プラグインに新しいフックを作成します。

## 使い方

```bash
/create-hook
```

## Claude への指示

### ステップ 1: 情報収集

ユーザーに以下を聞く:

1. **対象プラグイン** - どのプラグインにフックを追加するか
   - `plugins/` ディレクトリから既存プラグインを一覧表示

2. **イベント** - いつ実行するか
   - `PreToolUse`: ツール実行前（ブロック可能、matcher 必須）
   - `PostToolUse`: ツール実行後（matcher 必須）
   - `UserPromptSubmit`: ユーザープロンプト送信時
   - `SessionStart`: セッション開始時
   - `SessionEnd`: セッション終了時
   - `Stop`: レスポンス完了時
   - `Notification`: 通知時

3. **マッチャー**（PreToolUse / PostToolUse の場合のみ）
   - 例: `Bash`, `Write`, `Edit|Write`, `*`（すべて）

4. **フックタイプ**
   - `command`: Bash コマンドを実行
   - `prompt`: LLM（Haiku）で評価

5. **実行するコマンド**（type: command の場合）
   - 例: `npm run lint`, `echo "完了"`

### ステップ 2: 検証

- プラグインが存在するか確認
- イベントが有効か確認
- PreToolUse / PostToolUse の場合、マッチャーが指定されているか確認

### ステップ 3: hooks.json を作成または更新

`plugins/{plugin-name}/hooks/hooks.json` を作成または更新:

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

既存の hooks.json がある場合は、適切なイベントに追加する。

### ステップ 4: プラグイン README を更新

`plugins/{plugin-name}/README.md` のフックセクションにフックを追加。

### ステップ 5: 報告

作成されたファイルと次のステップを表示:

```text
フックを作成しました: {イベント} {マッチャー（あれば）}

ファイル:
- plugins/{plugin-name}/hooks/hooks.json

更新:
- plugins/{plugin-name}/README.md

次のステップ:
- /create-hook で別のフックを追加
- /create-command でコマンドを追加
- /create-skill で別のスキルを追加
- /create-subagent でサブエージェントを追加
```
