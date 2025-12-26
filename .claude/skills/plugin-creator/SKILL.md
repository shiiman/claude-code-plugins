---
name: plugin-creator
description: 新しい Claude Code プラグインを作成。「プラグイン作成」「新しいプラグイン」「プラグインを作って」「plugin 作成」でトリガー。
allowed-tools: [Read, Write, Bash, Glob]
---

# Plugin Creator

必要なディレクトリ構造とファイルを持つ新しい Claude Code プラグインを作成します。

## 手順

トリガーされたら `/create-plugin` コマンドを実行。

1. `docs/plugin.md` を参照として読む
2. `/create-plugin` を実行してユーザーをプラグイン作成にガイド

`/create-plugin` コマンドは以下を行う:

- プラグイン名と説明を聞く
- ディレクトリ構造を作成
- plugin.json を生成
- README.md を生成
- marketplace.json を更新

## 命名規則

プラグイン名には必ず `shiiman-` プレフィックスを付ける（他マーケットプレイスとの競合回避）。

- 形式: `shiiman-{name}`
- 小文字、ハイフン区切りのみ
- コロン（`:`）禁止（コマンド区切りと競合）
- 例: `shiiman-common`, `shiiman-react`, `shiiman-code-review`
