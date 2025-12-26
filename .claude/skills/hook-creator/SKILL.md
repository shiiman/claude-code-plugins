---
name: hook-creator
description: プラグインに新しいフックを作成する。「フック作成」「新しいフック」「フックを作って」「フック追加」「hook 作成」「フックを追加したい」「新規フック」などで起動。ツール実行前後やセッションイベントで実行されるフックを生成。
allowed-tools: [Read, Write, Bash, Glob]
---

# Hook Creator

プラグインに新しいフックを作成します。

## ワークフロー

### 1. ドキュメント参照

`docs/hook.md` を Read ツールで参照（SSOT として扱う）。

### 2. コマンド実行

`/create-hook` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/create-hook` に委譲します（SSOT として扱う）。

`/create-hook` コマンドは以下を行う:

- 対象プラグインを聞く
- イベントを聞く（PreToolUse, PostToolUse, SessionStart 等）
- マッチャーを聞く（PreToolUse / PostToolUse の場合のみ）
- フックタイプを聞く（command または prompt）
- 実行するコマンドを聞く
- hooks.json を作成または更新
- プラグイン README を更新

## Hook イベント

| イベント           | 説明                 | matcher |
|--------------------|----------------------|---------|
| `PreToolUse`       | ツール実行前         | 必須    |
| `PostToolUse`      | ツール実行後         | 必須    |
| `SessionStart`     | セッション開始時     | 不要    |
| `SessionEnd`       | セッション終了時     | 不要    |
| `UserPromptSubmit` | プロンプト送信時     | 不要    |
| `Stop`             | レスポンス完了時     | 不要    |
| `Notification`     | 通知時               | 不要    |

## 重要な注意事項

- ✅ PreToolUse / PostToolUse には必ず matcher を指定
- ✅ hooks.json 形式に従う
- ❌ matcher が必要なイベントで matcher を省略しない
