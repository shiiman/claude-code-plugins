---
name: subagent-creator
description: プロジェクトの .claude/agents/ に新しいサブエージェントを作成する。「エージェント作成」「新しいエージェント」「エージェントを作って」「サブエージェント追加」「agent 作成」「エージェントを追加したい」「新規エージェント」などで起動。プロジェクト固有のサブエージェントファイルを生成。
allowed-tools: [Read, Write, Bash, Glob]
---

# Subagent Creator

プロジェクトの `.claude/agents/` に新しいサブエージェントを作成します。

## ワークフロー

### 1. コマンド実行

`/shiiman-claude:create-subagent` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-claude:create-subagent` に委譲します（SSOT として扱う）。

`/shiiman-claude:create-subagent` コマンドは以下を行う:

- サブエージェント名と説明を聞く
- サブエージェントファイルを作成

## サブエージェントの種類

- **Review Agents**: `code-reviewer`, `architecture-reviewer`
- **Analysis Agents**: `performance-analyzer`, `security-analyzer`
- **Specialist Agents**: `frontend-specialist`, `backend-specialist`
- **Role Agents**: `architect`, `qa-engineer`, `devops-engineer`

## 重要な注意事項

- ✅ 小文字・ハイフン区切りを使用
- ✅ `.claude/agents/{name}.md` に作成
- ❌ アンダースコアやキャメルケースは使用しない
