---
name: subagent-creator
description: 新しいサブエージェントを作成。「サブエージェント作成」「新しいエージェント」「エージェントを作って」「subagent 作成」でトリガー。
allowed-tools: [Read, Write, Bash, Glob]
---

# Subagent Creator

プラグインに新しいサブエージェントを作成します。

## 手順

トリガーされたら `/create-subagent` コマンドを実行。

1. `docs/subagent.md` を参照として読む
2. `/create-subagent` を実行してユーザーをサブエージェント作成にガイド

`/create-subagent` コマンドは以下を行う:

- 対象プラグインを聞く
- サブエージェント名と説明を聞く
- サブエージェントファイルを作成
- プラグイン README を更新
