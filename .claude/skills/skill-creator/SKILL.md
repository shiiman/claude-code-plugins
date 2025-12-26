---
name: skill-creator
description: 新しいスキルを作成。「スキル作成」「新しいスキル」「スキルを作って」「skill 作成」でトリガー。
allowed-tools: [Read, Write, Bash, Glob]
---

# Skill Creator

プラグインに新しいスキルを作成します。

## 手順

トリガーされたら `/create-skill` コマンドを実行。

1. `docs/skill.md` を参照として読む
2. `/create-skill` を実行してユーザーをスキル作成にガイド

`/create-skill` コマンドは以下を行う:

- 対象プラグインを聞く
- スキル名と説明を聞く
- トリガーフレーズを設定
- スキルファイルを作成
- プラグイン README を更新
