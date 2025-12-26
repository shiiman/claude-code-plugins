---
name: issues-creator
description: 計画から複数の GitHub Issue をまとめて作成する。「Issue 作成」「Issue を作って」「issues 作成」「計画から Issue」「Issue 追加」「Issue を追加したい」「まとめて Issue」などで起動。計画を Issue に分解して一括作成。
allowed-tools: [Read, Bash, Glob]
---

# Issues Creator

計画から複数の GitHub Issue をまとめて作成します。

## ワークフロー

### 1. ドキュメント参照

`docs/issues.md` を Read ツールで参照（SSOT として扱う）。

### 2. コマンド実行

`/create-issues` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/create-issues` に委譲します（SSOT として扱う）。

`/create-issues` コマンドは以下を行う:

- 計画ファイルまたはユーザー入力から Issue 一覧を抽出
- Issue タイプ（Plugin/Command/Skill/Subagent/Hook）を判定
- `gh issue create` で Issue を作成
- 作成された Issue の一覧を報告

## Issue タイプ

| タイプ           | プレフィックス | ラベル                |
|------------------|----------------|-----------------------|
| プラグイン       | `[Plugin]`     | enhancement, plugin   |
| コマンド         | `[Command]`    | enhancement, command  |
| スキル           | `[Skill]`      | enhancement, skill    |
| サブエージェント | `[Subagent]`   | enhancement, subagent |
| フック           | `[Hook]`       | enhancement, hook     |

## 重要な注意事項

- ✅ 計画に含まれる項目のみを Issue として作成
- ✅ 適切なラベルを付与
- ❌ 不要な Issue を含めない
