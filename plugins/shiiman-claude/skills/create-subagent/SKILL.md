---
name: create-subagent
description: プロジェクトの .claude/agents/ に新しいサブエージェントを作成する。「エージェント作成」「新しいエージェント」「エージェントを作って」「サブエージェント追加」「agent 作成」「エージェントを追加したい」「新規エージェント」などで起動。プロジェクト固有のサブエージェントファイルを生成。
allowed-tools: [Read, Write, Bash, Glob, AskUserQuestion]
---

# Create Subagent

プロジェクトの `.claude/agents/` に新しいサブエージェントを作成します。

## 引数

- `$ARGUMENTS`: `--help` でヘルプを表示

## 実行手順

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### ステップ 1: 情報収集

ユーザーに以下を聞く:

1. **サブエージェント名**（小文字、ハイフン可）
   - 例: `code-reviewer`, `test-writer`, `security-auditor`

2. **説明**（1-2 文）

3. **このサブエージェントで何をする？**（詳細な指示）

### ステップ 2: 検証

- サブエージェント名の形式をチェック（小文字、ハイフンのみ）
- `.claude/agents/` ディレクトリが存在するか確認（なければ作成）
- サブエージェントが既に存在しないか確認

### 命名規則

| パターン   | 例                                         | 説明               |
|------------|--------------------------------------------|--------------------|
| 役割ベース | `reviewer`, `analyzer`                     | 役割を表す         |
| 専門分野付 | `code-reviewer`, `performance-analyzer`    | 役割 + 専門分野    |
| ドメイン固 | `frontend-specialist`, `backend-developer` | 特定の領域の専門家 |

### サブエージェントの種類

- **Review Agents**: `code-reviewer`, `architecture-reviewer`
- **Analysis Agents**: `performance-analyzer`, `security-analyzer`
- **Specialist Agents**: `frontend-specialist`, `backend-specialist`
- **Role Agents**: `architect`, `qa-engineer`, `devops-engineer`

### ステップ 3: サブエージェントファイルを作成

`.claude/agents/{subagent-name}.md` を作成:

```markdown
# {サブエージェント名}

{説明}

## 実行内容

このサブエージェントが実行する具体的なタスク：

- タスク 1
- タスク 2
- タスク 3

## 使用タイミング

どのような場面で使用するべきか：

- ケース 1
- ケース 2

## 専門知識

このサブエージェントが持つ専門知識：

- 知識 1（例: Clean Code 原則）
- 知識 2（例: OWASP Top 10）

## 出力形式

### 問題点

| 重要度 | ファイル | 行 | 問題 |
|--------|----------|-----|------|
| 高     | foo.ts   | 42  | ...  |

### 改善提案

1. **foo.ts:42** - 改善内容
```

### ステップ 4: 報告

作成されたファイルと次のステップを表示:

```text
サブエージェントを作成しました: {subagent-name}

ファイル:
- .claude/agents/{subagent-name}.md

次のステップ:
- /shiiman-claude:create-subagent で別のサブエージェントを追加
- /shiiman-claude:create-skill でスキルを追加
- /shiiman-claude:create-command でコマンドを追加
- /shiiman-claude:create-hook でフックを追加
```

## 重要な注意事項

- ✅ 小文字・ハイフン区切りを使用
- ✅ `.claude/agents/{name}.md` に作成
- ❌ アンダースコアやキャメルケースは使用しない
