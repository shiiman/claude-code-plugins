---
name: shiiman-github:pr-review
description: GitHub の PR をレビューしてローカル表示または GitHub に投稿する。「PR レビュー」「PR をレビュー」「PR のセキュリティレビュー」「PR のパフォーマンスレビュー」「PR 承認」「approve して」「LGTM」などで起動。対象は GitHub 上の PR（手元の変更は shiiman-common:review）。既定はローカル表示のみで、投稿・承認は発話から判断し実行前に必ず確認する。
allowed-tools: [Read, Bash, Glob, Grep, AskUserQuestion]
argument-hint: "[PR番号]"
context: fork
agent: shiiman-github:reviewer
---

# Review PR

PR をレビューし、結果をローカル表示または GitHub に投稿します。

> **注意**: 自分の PR に付いたレビューコメントに対応する場合は `pr-review-check` を使用してください。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-github:pr-review - PR レビュー

概要:
  PR をレビューし、結果をローカル表示または GitHub に投稿する。
  既定はローカル表示のみ。投稿・承認は発話から判断し、実行前に必ず確認する。

使用方法:
  /shiiman-github:pr-review [PR番号]

オプション:
  --help  このヘルプを表示

出力先・レビュー結果の伝え方（フラグの代わり）:
  指定なし                  → ローカル表示のみ（GitHub には投稿しない）
  「GitHub に投稿して」      → レビューコメントを GitHub に投稿
  「approve」「承認」「LGTM」 → Approve として投稿
  「要修正」「変更要求」      → Request Changes として投稿

例:
  /shiiman-github:pr-review        # 現在のブランチの PR をレビュー（ローカル表示）
  /shiiman-github:pr-review 123    # PR #123 をレビュー（ローカル表示）
  「PR #123 をレビューして投稿して」 # レビューして GitHub に投稿
  「PR #123 を approve して」       # PR #123 を承認
```

## 起動時の自動判断（フラグの代わり）

引数・発話から出力先とレビュー結果を判定する。**明示がなければローカル表示のみ**（誤投稿防止の安全側）とする。

| 項目         | 既定         | 判断ルール                                                        |
| ------------ | ------------ | ----------------------------------------------------------------- |
| 出力先       | ローカル表示 | 「投稿して」「GitHub に」「approve」「要修正」等あれば投稿        |
| レビュー結果 | コメント     | 「approve」「承認」「LGTM」→ Approve／「要修正」→ Request Changes |

**GitHub への投稿・承認・変更要求は取り消しにくい外部操作のため、実行前に必ず `AskUserQuestion` で確認する**（後述のステップ 6）。判断に迷う場合はローカル表示にとどめる。

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

**ローカル表示のみ（既定）**: ローカルに結果を表示し、ここで終了する

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

**投稿と判定した場合**: GitHub に投稿する前に、`AskUserQuestion` で必ず確認する（外部・不可逆操作）。

```text
question: "レビュー結果を GitHub に投稿しますか？"
options:
  - コメントとして投稿: gh pr review --comment で投稿
  - Approve として投稿: gh pr review --approve で承認
  - Request Changes として投稿: gh pr review --request-changes で変更要求
  - 投稿しない: ローカル表示のみで終了
```

確認で投稿が選ばれた場合のみ、対応するコマンドを実行する。

```bash
# コメントとして投稿
gh pr review {pr番号} --comment --body "{レビュー内容}"

# Approve として投稿
gh pr review {pr番号} --approve --body "{レビュー内容}"

# Request Changes として投稿
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

## 簡易承認フロー（「approve」「LGTM」のみ伝えられた場合）

レビュー依頼なしで「approve」「承認」「LGTM」だけ伝えられた場合、詳細レビューをスキップして承認のみ行う。承認は GitHub への外部・不可逆操作のため、実行前に必ず `AskUserQuestion` で確認する。

### 1. PR 状態の確認

```bash
gh pr view {pr番号} --json title,state,reviews,mergeable,statusCheckRollup
```

以下を確認:

- 未対応の必須修正がないか
- CI が通っているか
- マージ可能な状態か

### 2. 承認実行（確認後）

`AskUserQuestion` で承認の実行可否を確認し、承認が選ばれた場合のみ実行する。

```bash
gh pr review {pr番号} --approve --body "{承認コメント}"
```

### 3. 結果報告

```
PR #{pr番号} を承認しました。

ステータス: ✅ Approved
マージ可能: {mergeable}

マージする場合:
gh pr merge {pr番号}
```

### 承認コメントテンプレート

**シンプル**:

```
LGTM! 🎉
```

**詳細**:

```markdown
## Approved

{approval_comment}

### 確認済み項目

- [x] コード品質
- [x] テスト
- [x] ドキュメント

LGTM! 🎉
```

## 重要な注意事項

- ✅ 投稿の意図が明示されない場合はローカル表示のみ（誤投稿防止の安全側）
- ✅ GitHub への投稿・承認・変更要求は実行前に必ず AskUserQuestion で確認する
- ✅ 「approve」「LGTM」のみの場合は簡易承認フローへ（確認後に承認）
- ✅ 具体的な改善提案を含める
- ✅ 良い点も指摘する
- ✅ 重要度を明確にする
- ❌ 曖昧なコメントを避ける
- ❌ 個人攻撃的なコメントは禁止
