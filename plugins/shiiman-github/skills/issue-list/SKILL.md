---
name: shiiman-github:issue-list
description: オープン Issue の一覧を優先順位付きで表示する。「Issue 一覧」「Issue リスト」「オープン Issue」「Issue を見せて」「チケット一覧」「未解決 Issue」「Issue 確認」などで起動。優先度順にソートして表示。「クローズ済みも」「自分の Issue」などの絞り込みは発話から判断する。
allowed-tools: [Bash]
argument-hint: "[--help]"
---

# List Issues

オープン Issue の一覧を優先順位付きで表示します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-github:issue-list - Issue 一覧表示

概要:
  オープン Issue の一覧を優先順位付きで表示する。
  ラベルに基づく優先度ソートに対応。

使用方法:
  /shiiman-github:issue-list

オプション:
  --help  このヘルプを表示

絞り込みの伝え方（フラグの代わり）:
  「クローズ済みも」「全部」  → クローズ済みも含めて表示
  「自分の」「自分担当」      → 自分がアサインされた Issue のみ

例:
  /shiiman-github:issue-list       # オープン Issue を表示
  「クローズした Issue も見せて」   # 全 Issue を表示
  「自分の Issue 一覧」             # 自分担当の Issue を表示
```

## 実行手順

### 1. 表示範囲を判定（フラグの代わり）

引数・発話から表示範囲を決める。明示がなければ既定（オープンのみ・全担当）とする。読み取り専用のため確認は不要。

| 項目 | 既定     | 判断ルール                                       |
| ---- | -------- | ------------------------------------------------ |
| 状態 | オープン | 「クローズ済みも」「全部」→ 全状態               |
| 担当 | 全員     | 「自分の」「自分担当」→ 自分がアサインされたもの |

### 2. Issue 一覧を取得

判定した範囲に応じて `gh issue list` を実行する。

```bash
# オープンのみ（既定）
gh issue list --json number,title,labels,assignees,createdAt --limit 50

# クローズ済みも含める（「クローズ済みも」と判定した場合）
gh issue list --state all --json number,title,labels,assignees,createdAt,state --limit 50

# 自分がアサインされたもの（「自分の」と判定した場合）
gh issue list --assignee @me --json number,title,labels,assignees,createdAt --limit 50
```

### 3. 優先順位でソート（ラベル: priority-high > priority-medium > priority-low）

### 4. 以下の形式で表示

## 出力フォーマット

```
## オープン Issue 一覧

| 優先度 | # | タイトル | ラベル | 担当者 | 作成日 |
|:------:|---|----------|--------|--------|--------|
| 🔴 | #5 | バグ修正 | bug, priority: high | @user | 2024-01-01 |
| 🟡 | #3 | 機能追加 | enhancement | - | 2024-01-02 |
| 🟢 | #1 | ドキュメント | docs, priority: low | @user | 2024-01-03 |

合計: 3 件のオープン Issue
```

## 優先度の判定

| 優先度 | アイコン | 条件                                                 |
| ------ | -------- | ---------------------------------------------------- |
| 高     | 🔴       | `priority: high` ラベル または `bug` ラベル          |
| 中     | 🟡       | `priority: medium` ラベル または ラベルなし          |
| 低     | 🟢       | `priority: low` ラベル または `documentation` ラベル |

## 重要な注意事項

- ✅ 優先度順にソートして表示
- ✅ 担当者がいない場合は `-` で表示
- ✅ ラベルはカンマ区切りで表示
- ❌ Issue の内容は表示しない（一覧のみ）
