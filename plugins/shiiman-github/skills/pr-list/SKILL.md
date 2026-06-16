---
name: shiiman-github:pr-list
description: オープン PR の一覧を優先順位付きで表示する。「PR 一覧」「PR リスト」「オープン PR」「PR を見せて」「プルリク一覧」「レビュー待ち PR」「PR 確認」などで起動。レビュー状態と優先度順にソートして表示。「マージ済みも」「自分の」などの絞り込みは発話から判断する。
allowed-tools: [Bash]
argument-hint: "[--help]"
---

# List PRs

オープン PR の一覧を優先順位付きで表示します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-github:pr-list - PR 一覧表示

概要:
  オープン PR の一覧をレビュー状態と優先順位付きで表示する。

使用方法:
  /shiiman-github:pr-list

オプション:
  --help  このヘルプを表示

絞り込みの伝え方（フラグの代わり）:
  「マージ済みも」「全部」  → マージ済みも含めて表示
  「自分の」「自分作成」    → 自分が作成した PR のみ

例:
  /shiiman-github:pr-list        # オープン PR を表示
  「マージ済みの PR も見せて」    # 全 PR を表示
  「自分の PR 一覧」              # 自分作成の PR を表示
```

## 実行手順

### 1. 表示範囲を判定（フラグの代わり）

引数・発話から表示範囲を決める。明示がなければ既定（オープンのみ・全作成者）とする。読み取り専用のため確認は不要。

| 項目   | 既定     | 判断ルール                             |
| ------ | -------- | -------------------------------------- |
| 状態   | オープン | 「マージ済みも」「全部」→ 全状態       |
| 作成者 | 全員     | 「自分の」「自分作成」→ 自分の PR のみ |

### 2. PR 一覧を取得

判定した範囲に応じて `gh pr list` を実行する。

```bash
# オープンのみ（既定）
gh pr list --json number,title,headRefName,author,reviewDecision,updatedAt --limit 50

# マージ済みも含める（「マージ済みも」と判定した場合）
gh pr list --state all --json number,title,headRefName,author,reviewDecision,updatedAt,state --limit 50

# 自分が作成したもの（「自分の」と判定した場合）
gh pr list --author @me --json number,title,headRefName,author,reviewDecision,updatedAt --limit 50
```

### 3. レビュー状態と優先順位でソート

### 4. 以下の形式で表示

## 出力フォーマット

```
## オープン PR 一覧

| 状態 | # | タイトル | ブランチ | レビュー | 作成者 | 更新日 |
|:----:|---|----------|----------|----------|--------|--------|
| 🔄 | #10 | feat: 新機能 | feature/5 | ⏳ 待機中 | @user | 2024-01-01 |
| ✅ | #8 | fix: バグ修正 | fix/bug | ✅ 承認済 | @user | 2024-01-02 |
| ⚠️ | #6 | docs: 更新 | docs/update | ❌ 要修正 | @user | 2024-01-03 |

合計: 3 件のオープン PR
```

## 状態アイコン

| アイコン | 状態         | 条件                                            |
| -------- | ------------ | ----------------------------------------------- |
| 🔄       | レビュー待ち | `reviewDecision` が null または REVIEW_REQUIRED |
| ✅       | 承認済み     | `reviewDecision` が APPROVED                    |
| ⚠️       | 変更要求あり | `reviewDecision` が CHANGES_REQUESTED           |
| 🚧       | ドラフト     | `isDraft` が true                               |

## レビュー状態アイコン

| アイコン  | 状態                           |
| --------- | ------------------------------ |
| ⏳ 待機中 | レビュー未依頼またはレビュー中 |
| ✅ 承認済 | 承認済み（マージ可能）         |
| ❌ 要修正 | 変更要求あり                   |

## 重要な注意事項

- ✅ レビュー状態順にソートして表示
- ✅ ブランチ名を表示して関連 Issue を推測可能に
- ✅ 更新日順でソート
- ❌ PR の内容は表示しない（一覧のみ）
