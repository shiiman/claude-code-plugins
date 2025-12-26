---
name: plugin-creator
description: 新しい Claude Code プラグインを作成する。「プラグイン作成」「新しいプラグイン」「プラグインを作って」「プラグイン追加」「plugin 作成」「プラグインを追加したい」「新規プラグイン」などで起動。必要なディレクトリ構造とファイルを持つプラグインを生成。
allowed-tools: [Read, Write, Bash, Glob]
---

# Plugin Creator

必要なディレクトリ構造とファイルを持つ新しい Claude Code プラグインを作成します。

## ワークフロー

### 1. ドキュメント参照

`docs/plugin.md` を Read ツールで参照（SSOT として扱う）。

### 2. コマンド実行

`/create-plugin` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/create-plugin` に委譲します（SSOT として扱う）。

`/create-plugin` コマンドは以下を行う:

- プラグイン名と説明を聞く
- shiiman- プレフィックスを自動付与
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

## 重要な注意事項

- ✅ shiiman- プレフィックスを必ず付与
- ✅ 小文字・ハイフン区切りを使用
- ❌ アンダースコアやキャメルケースは使用しない
- ❌ コロンは使用しない
