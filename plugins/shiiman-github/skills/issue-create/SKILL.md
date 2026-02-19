---
name: shiiman-github:issue-create
description: タスクを細かい単位に分割して GitHub Issue を作成する。「Issue 作成」「Issue を作って」「タスクを Issue に」「Issue 追加」「チケット作成」「Issue を切る」「タスクを分割して Issue」などで起動。実装可能な粒度にタスクを分割して複数 Issue を生成。--branch でブランチも自動作成。
allowed-tools: [Read, Bash, Glob, Grep]
argument-hint: "[--branch|--help]"
context: fork
---

# Create Issue

タスクを細かい単位に分割して GitHub Issue を作成します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-github:issue-create - Create Issue

概要:
  タスクを細かい単位に分割して GitHub Issue を作成します。
  --branch で Issue 作成後にブランチも自動作成。

使用方法:
  /shiiman-github:issue-create [オプション]

オプション:
  --branch  Issue 作成後にブランチを自動作成
  --help    このヘルプを表示

例:
  /shiiman-github:issue-create              # Issue を作成
  /shiiman-github:issue-create --branch     # Issue 作成後にブランチも作成
```

## ワークフロー

### 1. タスクの確認

ユーザーから作成したいタスクの概要を聞く。

### 2. タスクの分割

タスクを実装可能な粒度に分割:

- 1 Issue = 1-2 時間で完了できる作業単位
- 依存関係がある場合は明記
- 各 Issue は独立してテスト可能

**タスク分割のルール**:

- 1つのタスクは 1ファイル or 1機能単位
- 具体的なアクションを記述（「〜を追加」「〜を修正」「〜を削除」）
- 依存関係がある場合は順番に並べる
- テストやドキュメント更新も個別タスクとして記載

### 3. Issue 内容の確認

分割した Issue 一覧をユーザーに提示して確認:

```
以下の Issue を作成します:

1. [機能A] 基本実装
   - 説明: ...
   - ラベル: enhancement

2. [機能A] テスト追加
   - 説明: ...
   - ラベル: enhancement
   - 依存: #1

3. [機能A] ドキュメント更新
   - 説明: ...
   - ラベル: documentation
   - 依存: #1

よろしいですか？
```

### 4. Issue 作成

承認後、`gh issue create` で各 Issue を作成。

**コマンドテンプレート**:

```bash
gh issue create \
  --title "[{scope}] {title}" \
  --body "## 概要

{description}

## タスク

- [ ] {task1}
- [ ] {task2}
- [ ] {task3}

## 完了条件

- {condition1}
- {condition2}

## 依存関係

{dependencies または「なし」}
" \
  --label "{labels}"
```

### 5. 結果報告

作成した Issue の一覧を報告:

```
以下の Issue を作成しました:

| # | タイトル | ラベル |
|---|----------|--------|
| #10 | [機能A] 基本実装 | enhancement |
| #11 | [機能A] テスト追加 | enhancement |
| #12 | [機能A] ドキュメント更新 | documentation |

推奨作業順序: #10 → #11 → #12
```

### 6. ブランチ作成の提案

**`--branch` 指定時**:

最初に作成した Issue の番号で `branch-create` の手順に従いブランチを自動作成する。

**`--branch` なし**:

ユーザーに「ブランチを作成しますか？」と確認:

- はい → 最初に作成した Issue の番号で `branch-create` の手順に従いブランチを作成
- いいえ → スキップ

## Issue タイトルの形式

`[{scope}] {title}`

- scope: 機能名や対象コンポーネント
- title: 具体的なタスク内容

## ラベルの自動判定

| 内容             | ラベル          |
| ---------------- | --------------- |
| 新機能           | `enhancement`   |
| バグ修正         | `bug`           |
| テスト           | `enhancement`   |
| ドキュメント     | `documentation` |
| リファクタリング | `improvement`   |

## 重要な注意事項

- ✅ 1-2 時間で完了できる粒度に分割
- ✅ 依存関係を明記
- ✅ 完了条件を明確にする
- ❌ 巨大な Issue を作成しない
- ❌ 曖昧なタスク記述
