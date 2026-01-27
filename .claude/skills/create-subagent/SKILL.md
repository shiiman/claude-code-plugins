---
name: create-subagent
description: プラグインに新しいサブエージェントを作成する。「サブエージェント作成」「新しいエージェント」「エージェントを作って」「エージェント追加」「subagent 作成」「エージェントを追加したい」「新規エージェント」などで起動。特定の役割を持つサブエージェントを生成。
allowed-tools: [Read, Write, Bash, Glob]
---

# Create Subagent

プラグインに新しいサブエージェントを作成します。

## ワークフロー

### 1. 情報収集

ユーザーに以下を聞く:

1. **対象プラグイン** - どのプラグインにサブエージェントを追加するか
   - `plugins/` ディレクトリから既存プラグインを一覧表示

2. **サブエージェント名**（小文字、ハイフン可）
   - 例: `code-reviewer`, `test-writer`, `security-auditor`

3. **説明**（1-2 文）

4. **このサブエージェントで何をする？**（詳細な指示）

### 2. 検証

- サブエージェント名の形式をチェック（小文字、ハイフンのみ）
- プラグインが存在するか確認
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

### 3. サブエージェントファイルを作成

`plugins/{plugin-name}/agents/{subagent-name}.md` を作成:

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

### 4. プラグイン README を更新

`plugins/{plugin-name}/README.md` のエージェントセクションにサブエージェントを追加。

### 5. 報告

作成されたファイルと次のステップを表示:

```text
サブエージェントを作成しました: {subagent-name}

ファイル:
- plugins/{plugin-name}/agents/{subagent-name}.md

更新:
- plugins/{plugin-name}/README.md

次のステップ:
- /create-subagent で別のサブエージェントを追加
- /create-skill でスキルを追加
- /create-command でコマンドを追加
- /create-hook でフックを追加
```

## 重要な注意事項

- ✅ 小文字・ハイフン区切りを使用
- ✅ 明確な役割定義を含める
- ✅ 具体的な実行内容と専門知識を記載
- ❌ 曖昧な役割定義は避ける
