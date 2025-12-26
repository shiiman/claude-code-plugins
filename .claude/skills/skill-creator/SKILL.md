---
name: skill-creator
description: プラグインに新しいスキルを作成する。「スキル作成」「新しいスキル」「スキルを作って」「スキル追加」「skill 作成」「スキルを追加したい」「新規スキル」などで起動。自然言語トリガーで起動するスキルを生成。
allowed-tools: [Read, Write, Bash, Glob]
---

# Skill Creator

プラグインに新しいスキルを作成します。

## ワークフロー

### 1. ドキュメント参照

`docs/skill.md` を Read ツールで参照（SSOT として扱う）。

### 2. コマンド実行

`/create-skill` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/create-skill` に委譲します（SSOT として扱う）。

`/create-skill` コマンドは以下を行う:

- 対象プラグインを聞く
- スキル名と説明を聞く
- トリガーフレーズを 7 つ設定
- 許可するツールを設定
- スキルファイル（SKILL.md）を作成
- プラグイン README を更新

## description の書き方

**重要**: description は Claude が Skill を自動起動するための唯一の情報源。

- 7 つのトリガーワードを含める
- 形式: `{機能説明}。「トリガー1」「トリガー2」...「トリガー7」などで起動。{詳細説明}。`
- 最大 1024 文字

## 重要な注意事項

- ✅ 小文字・ハイフン区切りを使用
- ✅ description に 7 つのトリガーワードを含める
- ✅ SSOT パターンまたは独自実装パターンを選択
- ❌ トリガーワードが不足している description は避ける
