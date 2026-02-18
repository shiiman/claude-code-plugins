# サブエージェント作成ガイド

このガイドでは、Claude Code プラグイン用のサブエージェントを作成する方法を説明します。

## 概要

エージェントは、特定の役割や専門知識を持った AI アシスタントとして動作し、Markdown ファイル (`.md`) として定義されます。`plugins/{plugin-name}/agents/` ディレクトリに配置されます。

## サブエージェントとは

エージェントは以下の特徴を持ちます：

- **役割ベース**: 特定の専門分野（例: コードレビュー、パフォーマンス分析）を担当
- **自律的実行**: 与えられたタスクを自律的に実行
- **コンテキスト保持**: 会話全体のコンテキストを理解して対応
- **ツール利用**: Read, Edit, Bash などのツールを活用

## 配置場所

```text
plugins/{plugin-name}/agents/{subagent-name}.md
```

## エージェントファイルの構造

### 基本テンプレート

```markdown
# エージェントの役割（1 行で簡潔に）

エージェントの詳細な説明。専門分野、得意な領域、提供する価値を記述します。

## 実行内容

このエージェントが実行する具体的なタスク：

- タスク 1
- タスク 2
- タスク 3

## 使用タイミング

どのような場面で使用するべきか：

- ケース 1: 説明
- ケース 2: 説明
- ケース 3: 説明

## 専門知識

このエージェントが持つ専門知識や参照する基準：

- 知識 1（例: OWASP Top 10）
- 知識 2（例: Clean Code 原則）
- 知識 3（例: パフォーマンスベストプラクティス）

## 使用例

\`\`\`bash
# 基本的な使用
プロジェクトで {role} を実行してください

# 特定のファイルを対象
src/ 配下のコードを {role} でレビューしてください
\`\`\`
```

### ポイント

- **役割を明確に**: 1 行目で役割を端的に表現
- **具体的な実行内容**: 何をするのか明確に記述
- **使用タイミングを明示**: いつ使うべきか分かりやすく
- **専門知識を記載**: どのような基準で判断するか明記

## 命名規則

### 基本ルール

- 小文字とハイフンを使用: `code-reviewer.md`
- 役割を明確に表す名前にする
- プラグイン内で一貫した命名

### サブエージェント特有のパターン

サブエージェントでは役割と専門性を組み合わせた命名が一般的です：

```bash
# 役割ベース
reviewer              # コードレビュアー
analyzer              # 分析担当

# 専門分野付き
code-reviewer         # コードレビュー専門
performance-analyzer  # パフォーマンス分析専門
security-auditor      # セキュリティ監査専門

# ドメイン固有
frontend-specialist   # フロントエンド専門家
backend-developer     # バックエンド開発者
```

## サブエージェントの種類

### 1. Review Agents（レビュー系）

コードやドキュメントのレビューを担当：

```bash
code-reviewer         # コードレビュー
architecture-reviewer # アーキテクチャレビュー
doc-reviewer          # ドキュメントレビュー
```

**特徴**:

- コーディング規約の確認
- ベストプラクティスの適用
- 潜在的な問題の指摘

### 2. Analysis Agents（分析系）

コードやシステムの分析を担当：

```bash
performance-analyzer  # パフォーマンス分析
security-analyzer     # セキュリティ分析
dependency-analyzer   # 依存関係分析
```

**特徴**:

- メトリクスの収集
- 問題点の特定
- 改善提案の提示

### 3. Specialist Agents（専門家系）

特定の技術領域の専門家：

```bash
frontend-specialist   # フロントエンド専門
backend-specialist    # バックエンド専門
mobile-specialist     # モバイル専門
```

**特徴**:

- 領域特化の深い知識
- 技術スタック固有のアドバイス
- 最新のベストプラクティス

### 4. Role Agents（役割系）

開発プロセスにおける特定の役割：

```bash
architect             # システムアーキテクト
qa-engineer           # QA エンジニア
devops-engineer       # DevOps エンジニア
```

**特徴**:

- 役割に応じた視点
- プロセス全体の理解
- チーム協働の促進

## 実装ガイドライン

### 1. 明確な役割定義

```markdown
# ✅ 良い例

# コードレビュー専門エージェント

Clean Code 原則、SOLID 原則に基づいてコードレビューを実施します。
バグの検出、可読性の向上、パフォーマンス改善を提案します。

# ❌ 悪い例

# レビュー

コードをレビューします。
```

### 2. 具体的な実行内容

```markdown
# ✅ 良い例

## 実行内容

- コーディング規約の確認
- Clean Code 原則の適用状況チェック
- 潜在的なバグの検出
- パフォーマンス上の問題点の指摘
- セキュリティリスクの評価

# ❌ 悪い例

## 実行内容

- コードを見る
- 問題があれば指摘する
```

### 3. 明示的な使用タイミング

```markdown
# ✅ 良い例

## 使用タイミング

- PR 作成前の最終チェック
- 複雑なロジックを実装した後
- パフォーマンスが重要な機能の実装時
- セキュリティが関わる機能の実装時

# ❌ 悪い例

## 使用タイミング

- 必要な時
```

### 4. 専門知識の明記

```markdown
# ✅ 良い例

## 専門知識

- Clean Code 原則（Robert C. Martin）
- SOLID 原則
- OWASP Top 10（セキュリティ）
- Google JavaScript Style Guide
- React ベストプラクティス

# ❌ 悪い例

## 専門知識

- いろいろな知識
```

## ベストプラクティス

### 単一責任の原則

```bash
# ✅ 良い設計
code-reviewer          # コードレビューのみ
performance-analyzer   # パフォーマンス分析のみ
security-auditor       # セキュリティ監査のみ

# ❌ 悪い設計
all-in-one-reviewer    # すべてを担当（責任が不明確）
```

### 一貫した命名

```bash
# ✅ プラグイン内で統一
code-reviewer
architecture-reviewer
doc-reviewer

# ❌ 不統一
code-reviewer
analyze-architecture
documentChecker
```

### 適切な粒度

```bash
# ✅ 適切な粒度
frontend-specialist    # フロントエンド全般
react-specialist       # React 特化（必要に応じて）

# ❌ 細かすぎる
react-hooks-specialist
react-state-specialist
```

## 実装例

ファイル: `plugins/shiiman-git/agents/reviewer.md`

```markdown
# コードレビュー専門エージェント

Clean Code 原則、SOLID 原則に基づいてコードレビューを実施します。
バグの検出、可読性の向上、パフォーマンス改善を提案します。

## 実行内容

- コーディング規約の確認
- Clean Code 原則の適用状況チェック
- 潜在的なバグの検出
- パフォーマンス上の問題点の指摘
- セキュリティリスクの評価

## 使用タイミング

- PR 作成前の最終チェック
- 複雑なロジックを実装した後
- パフォーマンスが重要な機能の実装時
- セキュリティが関わる機能の実装時

## 専門知識

- Clean Code 原則（Robert C. Martin）
- SOLID 原則
- OWASP Top 10（セキュリティ）
- Google JavaScript Style Guide

## 出力形式

### 問題点

| 重要度 | ファイル | 行 | 問題                   |
| ------ | -------- | -- | ---------------------- |
| 高     | foo.ts   | 42 | SQL インジェクションの可能性 |
| 中     | bar.ts   | 15 | 未使用の変数           |

### 改善提案

1. **foo.ts:42** - パラメータ化されたクエリを使用してください
2. **bar.ts:15** - 未使用の変数 `temp` を削除してください

## 使用例

\`\`\`bash
# 基本的な使用
プロジェクト全体をコードレビューしてください

# 特定のファイルを対象
src/services/ 配下のコードをレビューしてください
\`\`\`
```

## トラブルシューティング

### サブエージェント名が既に存在する

```bash
# エラー: Agent 'code-reviewer' already exists in plugin 'shiiman-git'

# 解決策
ls plugins/shiiman-git/agents/  # 既存エージェントを確認
# 別の名前を検討（例: advanced-code-reviewer, senior-code-reviewer）
```

### 命名規則違反

```bash
# エラー: Invalid agent name 'CodeReviewer'

# 解決策
# 小文字・ハイフン区切りに修正
code-reviewer  # ✅
```

## 参考資料

公式ドキュメント:

- [Claude Code Plugins 公式ドキュメント](https://docs.anthropic.com/en/docs/claude-code/plugins)
- [Claude Code Agents](https://docs.anthropic.com/en/docs/claude-code/agents)
