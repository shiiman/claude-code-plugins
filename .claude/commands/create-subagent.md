# Create Subagent

プラグインに新しいサブエージェントを作成します。

## 使い方

```bash
/create-subagent
/create-subagent --help
```

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--help`   | このコマンドのヘルプを表示 |

## 実行例

```bash
# 基本的な使用
/create-subagent
→ 対象プラグイン: shiiman-common
→ サブエージェント名: code-reviewer
→ 説明: Clean Code 原則に基づいてコードレビューを実施
→ 何をする？: コーディング規約、潜在的バグ、セキュリティリスクをチェック

# 結果: plugins/shiiman-common/agents/code-reviewer.md が作成される
```

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### ステップ 1: 情報収集

ユーザーに以下を聞く:

1. **対象プラグイン** - どのプラグインにサブエージェントを追加するか
   - `plugins/` ディレクトリから既存プラグインを一覧表示

2. **サブエージェント名**（小文字、ハイフン可）
   - 例: `code-reviewer`, `test-writer`, `security-auditor`

3. **説明**（1-2 文）

4. **このサブエージェントで何をする？**（詳細な指示）

### ステップ 2: 検証

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

### ステップ 3: サブエージェントファイルを作成

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

### ステップ 4: プラグイン README を更新

`plugins/{plugin-name}/README.md` のエージェントセクションにサブエージェントを追加。

### ステップ 5: 報告

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
