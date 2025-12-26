---
name: command-creator
description: 新しいコマンドを作成。「コマンド作成」「新しいコマンド」「コマンドを作って」「command 作成」でトリガー。
allowed-tools: [Read, Write, Bash, Glob]
---

# Command Creator

プラグインに新しいスラッシュコマンドを作成します。

## 手順

トリガーされたら `/create-command` コマンドを実行。

1. `docs/command.md` を参照として読む
2. `/create-command` を実行してユーザーをコマンド作成にガイド

`/create-command` コマンドは以下を行う:

- 対象プラグインを聞く
- コマンド名と説明を聞く
- コマンドファイルを作成
- プラグイン README を更新
