---
name: subagent-creator
description: プラグインに新しいサブエージェントを作成する。「サブエージェント作成」「新しいエージェント」「エージェントを作って」「エージェント追加」「subagent 作成」「エージェントを追加したい」「新規エージェント」などで起動。特定の役割を持つサブエージェントを生成。
allowed-tools: [Read, Write, Bash, Glob]
---

# Subagent Creator

プラグインに新しいサブエージェントを作成します。

## ワークフロー

### 1. ドキュメント参照

`docs/subagent.md` を Read ツールで参照（SSOT として扱う）。

### 2. コマンド実行

`/create-subagent` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/create-subagent` に委譲します（SSOT として扱う）。

`/create-subagent` コマンドは以下を行う:

- 対象プラグインを聞く
- サブエージェント名と説明を聞く
- サブエージェントの役割と専門知識を設定
- サブエージェントファイルを作成
- プラグイン README を更新

## サブエージェントの種類

- **Review Agents**: `code-reviewer`, `architecture-reviewer`
- **Analysis Agents**: `performance-analyzer`, `security-analyzer`
- **Specialist Agents**: `frontend-specialist`, `backend-specialist`
- **Role Agents**: `architect`, `qa-engineer`, `devops-engineer`

## 重要な注意事項

- ✅ 小文字・ハイフン区切りを使用
- ✅ 明確な役割定義を含める
- ✅ 具体的な実行内容と専門知識を記載
- ❌ 曖昧な役割定義は避ける
