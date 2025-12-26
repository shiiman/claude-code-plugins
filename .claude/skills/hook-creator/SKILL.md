---
name: hook-creator
description: 新しいフックを作成。「フック作成」「新しいフック」「フックを作って」「hook 作成」でトリガー。
allowed-tools: [Read, Write, Bash, Glob]
---

# Hook Creator

プラグインに新しいフックを作成します。

## 手順

トリガーされたら `/create-hook` コマンドを実行。

1. `docs/hook.md` を参照として読む
2. `/create-hook` を実行してユーザーをフック作成にガイド

`/create-hook` コマンドは以下を行う:

- 対象プラグインを聞く
- イベントを聞く（PreToolUse, PostToolUse, SessionStart 等）
- マッチャーを聞く（PreToolUse / PostToolUse の場合のみ）
- フックタイプを聞く（command または prompt）
- 実行するコマンドを聞く
- hooks.json を作成または更新
- プラグイン README を更新

## Hook イベント

| イベント | 説明 | matcher |
|----------|------|---------|
| `PreToolUse` | ツール実行前 | 必須 |
| `PostToolUse` | ツール実行後 | 必須 |
| `SessionStart` | セッション開始時 | 不要 |
| `SessionEnd` | セッション終了時 | 不要 |
| `UserPromptSubmit` | プロンプト送信時 | 不要 |
| `Stop` | レスポンス完了時 | 不要 |
