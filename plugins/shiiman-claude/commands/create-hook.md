# Create Hook

プロジェクトの `.claude/settings.json` に新しいフックを追加します。

## 使い方

```bash
/shiiman-claude:create-hook
/shiiman-claude:create-hook --help
```

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--help`   | このコマンドのヘルプを表示 |

## 実行例

```bash
# 基本的な使用
/shiiman-claude:create-hook
→ イベント: PreToolUse
→ マッチャー: Bash
→ フックタイプ: command
→ コマンド: echo "Bash コマンドを実行します"

# 結果: .claude/settings.json の hooks セクションが更新される
```

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### ステップ 1: 情報収集

ユーザーに以下を聞く:

1. **イベント** - いつ実行するか
   - `PreToolUse`: ツール実行前（ブロック可能、matcher 必須）
   - `PostToolUse`: ツール実行後（matcher 必須）
   - `UserPromptSubmit`: ユーザープロンプト送信時
   - `Notification`: 通知時
   - `Stop`: レスポンス完了時
   - `SubagentStop`: サブエージェント完了時
   - `PreCompact`: Compact 操作前
   - `SessionStart`: セッション開始時
   - `SessionEnd`: セッション終了時

2. **マッチャー**（PreToolUse / PostToolUse の場合のみ）
   - 例: `Bash`, `Write`, `Edit|Write`, `*`（すべて）

3. **フックタイプ**
   - `command`: Bash コマンドを実行
   - `prompt`: LLM（Haiku）で評価

4. **実行するコマンド**（type: command の場合）
   - 例: `npm run lint`, `echo "完了"`

### ステップ 2: 検証

- イベントが有効か確認
- PreToolUse / PostToolUse の場合、マッチャーが指定されているか確認
- `.claude/settings.json` が存在するか確認（なければ作成）

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

### ステップ 3: settings.json の hooks セクションを更新

`.claude/settings.json` の hooks セクションを更新:

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

### ステップ 4: 報告

作成されたファイルと次のステップを表示:

```text
フックを作成しました: {イベント} {マッチャー（あれば）}

更新:
- .claude/settings.json

次のステップ:
- /shiiman-claude:create-hook で別のフックを追加
- /shiiman-claude:create-command でコマンドを追加
- /shiiman-claude:create-skill でスキルを追加
- /shiiman-claude:create-subagent でサブエージェントを追加
```
