---
name: pr-review-check
description: PRのレビューコメントを確認し、指摘事項に対応する
allowed-tools: [Read, Edit, Write, Bash, Glob, Grep]
---

# PR Review Check

PRに付いたレビューコメントを確認し、指摘事項に対して修正を実行します。

## 引数

- `$ARGUMENTS`: PR番号（省略時は現在のブランチのPRを自動検出）

## オプション

- `--fix`: 指摘事項を修正する（指定しない場合は確認のみ）
- `--reply`: 修正後にレビューコメントへ返信を投稿する
- `--help`: このヘルプを表示する

## 使い方

```
/pr-review-check --help
/pr-review-check                    # 現在のブランチのPRのコメントを確認
/pr-review-check 25                 # PR #25 のコメントを確認
/pr-review-check --fix              # 現在のブランチのPRの指摘を修正
/pr-review-check 25 --fix           # PR #25 の指摘を修正
/pr-review-check --fix --reply      # 修正して返信も投稿
```

## 実行手順

### 1. PR番号の特定

PR番号が指定されていない場合、現在のブランチに関連するPRを検出:

```bash
gh pr view --json number,title,url
```

### 2. レビューコメントの取得

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews
```

### 3. コメントの分類と表示

取得したコメントを分類して表示:

| プレフィックス | 種別 | 対応 |
|--------------|------|-----|
| must. | 修正必須 | 必ず修正 |
| imo. | 改善提案 | 基本的に修正 |
| nits. | 軽微 | 修正 |
| q. | 質問 | 返信で回答 |

### 4. 修正の実行（--fix 指定時）

各指摘事項について:
1. 対象ファイルを特定
2. 指摘内容を理解
3. 適切な修正を実行
4. 修正内容を記録

### 5. 返信の投稿（--reply 指定時）

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -X POST -f body="修正しました。"
```

## 出力例

```
=== PR #25: feat: shiiman-google プラグインを追加 ===

【must.】修正必須 (2件)
1. [plugin.json:3] バージョンは 1.0.0 から始めてください
2. [README.md:45] インストール手順が不足しています

【imo.】改善提案 (1件)
1. [google_calendar.py:120] エラーハンドリングの追加を推奨

【nits.】軽微 (1件)
1. [SKILL.md:15] タイポ: "取得る" → "取得する"

【q.】質問 (1件)
1. [google_gmail.py:50] この実装の意図を教えてください

--fix オプションで修正を実行できます。
```

## 注意事項

- `--fix` なしの場合は確認のみで修正は実行しない
- 修正できない指摘がある場合はその旨を報告
- 質問（q.）には返信で回答する（--reply 必要）
