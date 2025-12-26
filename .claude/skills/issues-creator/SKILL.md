---
name: issues-creator
description: 計画から複数の Issue を作成。「Issue 作成」「Issue を作って」「issues 作成」「計画から Issue」でトリガー。
allowed-tools: [Read, Bash, Glob]
---

# Issues Creator

計画から複数の GitHub Issue をまとめて作成します。

## 手順

トリガーされたら `/create-issues` コマンドを実行。

1. `docs/issues.md` を参照として読む
2. `/create-issues` を実行してユーザーを Issue 作成にガイド

`/create-issues` コマンドは以下を行う:

- 計画ファイルまたはユーザー入力から Issue 一覧を抽出
- Issue タイプ（Plugin/Command/Skill/Subagent/Hook）を判定
- `gh issue create` で Issue を作成
- 作成された Issue の一覧を報告

## Issue タイプ

| タイプ | プレフィックス | ラベル |
|--------|----------------|--------|
| プラグイン | `[Plugin]` | enhancement, plugin |
| コマンド | `[Command]` | enhancement, command |
| スキル | `[Skill]` | enhancement, skill |
| サブエージェント | `[Subagent]` | enhancement, subagent |
| フック | `[Hook]` | enhancement, hook |
