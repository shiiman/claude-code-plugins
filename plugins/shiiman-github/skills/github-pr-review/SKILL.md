---
name: shiiman-github:github-pr-review
description: PR をレビューしてローカル表示または GitHub に投稿する。「PR レビュー」「PR をレビュー」「コードレビュー」「レビューして」「セキュリティレビュー」「パフォーマンスレビュー」などで起動。
allowed-tools: [Read, Bash, Glob, Grep]
argument-hint: "[PR番号] [--submit|--approve|--request-changes|--help]"
context: fork
agent: shiiman-github:reviewer
---

# Review PR

PR をレビューし、結果をローカル表示または GitHub に投稿します。

> **注意**: 自分の PR に付いたレビューコメントに対応する場合は `github-pr-review-check` を使用してください。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-github:github-pr-review - PR レビュー

概要:
  PR をレビューし、結果をローカル表示または GitHub に投稿する。
  デフォルトはローカル表示のみ。--submit で GitHub に投稿。

使用方法:
  /shiiman-github:github-pr-review [PR番号] [オプション]

オプション:
  --help             このヘルプを表示
  --submit           GitHub にレビューコメントを投稿
  --approve          Approve としてレビュー投稿（--submit 必須）
  --request-changes  Request Changes としてレビュー投稿（--submit 必須）

例:
  /shiiman-github:github-pr-review                           # 現在のブランチの PR をレビュー（ローカル表示）
  /shiiman-github:github-pr-review 123                       # PR #123 をレビュー（ローカル表示）
  /shiiman-github:github-pr-review --submit                  # レビュー結果を GitHub に投稿
  /shiiman-github:github-pr-review 123 --submit --approve    # PR #123 をレビューして Approve
```

## ワークフロー

### 1. 対象 PR の特定

- PR 番号が指定されている場合: その PR をレビュー
- PR 番号が指定されていない場合: 現在のブランチの PR を自動検出

```bash
# PR 番号未指定時の自動検出
gh pr view --json number,title,url
```

### 2. レビュータイプの確認

ユーザーにレビュータイプを確認（複数選択可）:

| タイプ        | 説明           | チェック観点                        |
| ------------- | -------------- | ----------------------------------- |
| `general`     | 全体レビュー   | コード品質、設計、テスト            |
| `security`    | セキュリティ   | OWASP Top 10、入力検証、認証・認可  |
| `performance` | パフォーマンス | N+1、メモリリーク、アルゴリズム効率 |

デフォルト: `general`

### 3. PR 内容の取得

```bash
# PR 情報取得
gh pr view {pr番号} --json title,body,files,additions,deletions

# 変更差分取得
gh pr diff {pr番号}
```

### 4. レビュー実行

**全体レビュー（general）**:

- コードスタイル・命名規則
- 設計パターン・責務分離
- エラーハンドリング
- テストカバレッジ
- ドキュメント

**セキュリティレビュー（security）**:

- インジェクション（SQL, XSS, Command）
- 認証・認可の実装
- 機密情報の扱い
- 入力検証
- セッション管理

**パフォーマンスレビュー（performance）**:

- N+1 クエリ
- メモリリーク
- 不要なループ・計算
- キャッシュ戦略
- 非同期処理

### 5. 重要度の分類

| レベル   | 説明                                   |
| -------- | -------------------------------------- |
| Critical | セキュリティリスク、アーキテクチャ違反 |
| High     | パフォーマンス問題、重要な規約違反     |
| Medium   | コード品質向上                         |
| Low      | スタイル提案                           |

### 6. 結果の出力

**`--submit` なし（デフォルト）**: ローカルに結果を表示

```
## コードレビュー結果

### サマリー
{overall_assessment}

### 良い点
- {good_point_1}

### 改善提案
- [ ] {suggestion_1}

### 重要度: 高
{high_priority_issues}

### 重要度: 中
{medium_priority_issues}

### 重要度: 低
{low_priority_issues}
```

**`--submit` あり**: GitHub にコメント投稿

```bash
# --approve も --request-changes もない場合
gh pr review {pr番号} --comment --body "{レビュー内容}"

# --approve の場合
gh pr review {pr番号} --approve --body "{レビュー内容}"

# --request-changes の場合
gh pr review {pr番号} --request-changes --body "{レビュー内容}"
```

### 7. 結果報告

```
PR #{pr番号} のレビューを完了しました。

レビュータイプ: {types}
出力先: {ローカル表示|GitHub 投稿}
重要な指摘: {high_priority_count}件
改善提案: {suggestion_count}件
```

## 重要な注意事項

- ✅ `--submit` がない場合はローカルに結果を表示するだけ（誤投稿防止）
- ✅ `--approve` または `--request-changes` は `--submit` が必須
- ✅ 具体的な改善提案を含める
- ✅ 良い点も指摘する
- ✅ 重要度を明確にする
- ❌ 曖昧なコメントを避ける
- ❌ 個人攻撃的なコメントは禁止
