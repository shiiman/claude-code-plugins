---
name: pr-reviewer
description: 他者の PR をレビューして GitHub にコメントを投稿する（レビュアー向け）。「PR レビュー」「PR をレビュー」「コードレビュー」「レビューして」「セキュリティレビュー」「パフォーマンスレビュー」などで起動。
allowed-tools: [Read, Bash, Glob, Grep]
---

# PR Reviewer

**他者の PR** をレビューして GitHub にコメントを投稿します。

> **注意**: 自分の PR に付いたレビューコメントに対応する場合は `pr-review-checker` を使用してください。

## ワークフロー

### 1. 対象 PR の特定

以下から対象 PR を特定:

- ユーザーの指示（「#10 をレビュー」）
- PR URL
- 現在のブランチに関連する PR

### 2. レビュータイプの確認

ユーザーにレビュータイプを確認（複数選択可）:

| タイプ | 説明 | チェック観点 |
|--------|------|--------------|
| `general` | 全体レビュー | コード品質、設計、テスト |
| `security` | セキュリティ | OWASP Top 10、入力検証、認証・認可 |
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

### 5. GitHub コメント投稿

```bash
gh pr review {pr番号} --comment --body "$(cat <<'EOF'
## コードレビュー結果

### サマリー

{overall_assessment}

### 良い点

- {good_point_1}
- {good_point_2}

### 改善提案

- [ ] {suggestion_1}
- [ ] {suggestion_2}

### {タイプ}レビュー詳細

#### 重要度: 高

{high_priority_issues}

#### 重要度: 中

{medium_priority_issues}

#### 重要度: 低

{low_priority_issues}

---

レビュータイプ: {types}
EOF
)"
```

### 6. 結果報告

```
PR #{pr番号} のレビューを完了しました。

レビュータイプ: {types}
コメント URL: {comment_url}

重要な指摘: {high_priority_count}件
改善提案: {suggestion_count}件
```

## レビューコメントの種類

| 種類 | 説明 | アクション |
|------|------|------------|
| `COMMENT` | 一般コメント | 情報提供のみ |
| `REQUEST_CHANGES` | 変更要求 | 修正必須 |
| `APPROVE` | 承認 | マージ可能 |

## 重要な注意事項

- ✅ 具体的な改善提案を含める
- ✅ 良い点も指摘する
- ✅ 重要度を明確にする
- ❌ 曖昧なコメントを避ける
- ❌ 個人攻撃的なコメントは禁止
