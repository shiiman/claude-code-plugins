---
name: hook-creator
description: プロジェクトの .claude/settings.json に新しいフックを追加する。「フック作成」「新しいフック」「フックを作って」「フック追加」「hook 作成」「フックを追加したい」「新規フック」などで起動。ツール実行前後やセッションイベントで実行されるフックを設定。
allowed-tools: [Read, Write, Bash, Glob]
---

# Hook Creator

プロジェクトの `.claude/settings.json` に新しいフックを追加します。

## ワークフロー

### 1. コマンド実行

`/shiiman-claude:create-hook` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-claude:create-hook` に委譲します（SSOT として扱う）。

`/shiiman-claude:create-hook` コマンドは以下を行う:

- イベントを聞く（PreToolUse, PostToolUse, SessionStart 等）
- マッチャーを聞く（PreToolUse / PostToolUse の場合のみ）
- フックタイプを聞く（command または prompt）
- 実行するコマンドを聞く
- settings.json の hooks セクションを更新

## Hook イベント

| イベント           | 説明                 | matcher |
|--------------------|----------------------|---------|
| `PreToolUse`       | ツール実行前         | 必須    |
| `PostToolUse`      | ツール実行後         | 必須    |
| `UserPromptSubmit` | プロンプト送信時     | 不要    |
| `Notification`     | 通知時               | 不要    |
| `Stop`             | レスポンス完了時     | 不要    |
| `SubagentStop`     | サブエージェント完了 | 不要    |
| `PreCompact`       | Compact 操作前       | 不要    |
| `SessionStart`     | セッション開始時     | 不要    |
| `SessionEnd`       | セッション終了時     | 不要    |

## 重要な注意事項

- ✅ PreToolUse / PostToolUse には必ず matcher を指定
- ✅ `.claude/settings.json` の hooks セクションに設定
- ❌ matcher が必要なイベントで matcher を省略しない
- ❌ 別ファイル（hooks.json）は使用しない
