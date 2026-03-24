---
name: shiiman-github:issue-create
description: GitHub Issue を作成する。タスクは Issue 本文内でチェックボックスに分割。「Issue 作成」「Issue を作って」「タスクを Issue に」「Issue 追加」「チケット作成」「Issue を切る」「タスクを分割して Issue」などで起動。--branch でブランチ、--worktree で worktree も自動作成。
allowed-tools: [Read, Bash, Glob, Grep]
argument-hint: "[--branch|--worktree|--no-confirm|--help]"
context: fork
---

# Create Issue

GitHub Issue を作成します。タスクは Issue 本文内でチェックボックスに分割します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-github:issue-create - Create Issue

概要:
  GitHub Issue を作成します。
  タスクは Issue 本文内でチェックボックスに分割します。
  --branch で Issue 作成後にブランチ、--worktree で worktree も自動作成。

使用方法:
  /shiiman-github:issue-create [オプション]

オプション:
  --branch      Issue 作成後にブランチを自動作成
  --worktree    Issue 作成後に worktree を自動作成（gtr 使用）
  --no-confirm  ユーザー確認をスキップして即座に Issue を作成
  --help        このヘルプを表示

例:
  /shiiman-github:issue-create              # Issue を作成
  /shiiman-github:issue-create --branch     # Issue 作成後にブランチも作成
  /shiiman-github:issue-create --worktree   # Issue 作成後に worktree も作成
  /shiiman-github:issue-create --no-confirm # 確認なしで Issue を作成
```

## ワークフロー

### 1. タスクの確認

ユーザーから作成したいタスクの概要を聞く。

### 2. タスクの分割

タスクを Issue 本文内のチェックボックスに分割:

- 1 タスク = 具体的なアクション（「〜を追加」「〜を修正」「〜を削除」）
- 依存関係がある場合は順番に並べる
- テストやドキュメント更新も個別タスクとして記載

### 3. Issue 内容の確認

**`--no-confirm` なしの場合**:

作成する Issue の内容をユーザーに提示して確認:

```
以下の Issue を作成します:

タイトル: [{scope}] {title}
ラベル: {labels}

本文:
## 概要
{description}

## タスク
- [ ] {task1}
- [ ] {task2}
- [ ] {task3}

## 完了条件
- {condition1}
- {condition2}

よろしいですか？
```

**`--no-confirm` 指定時**:

ユーザー確認をスキップして即座に Issue を作成する。

### 4. Issue 作成

承認後（または `--no-confirm` 指定時は即座に）、`gh issue create` で Issue を作成。

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
" \
  --label "{labels}"
```

### 5. 結果報告

作成した Issue の結果を報告:

```
Issue を作成しました:

- 番号: #{number}
- タイトル: [{scope}] {title}
- ラベル: {labels}
- URL: {issue_url}
```

### 6. ブランチもしくは worktree 作成の提案

**`--branch` 指定時**:

作成した Issue の番号で `branch-create` の手順に従いブランチを自動作成する。

**`--worktree` 指定時**:

作成した Issue の番号で `worktree-create` の手順に従い worktree を自動作成する。

**`--branch` / `--worktree` なし**:

ユーザーに「ブランチまたは worktree を作成しますか？」と確認:

- ブランチ → 作成した Issue の番号で `branch-create` の手順に従いブランチを作成
- worktree → 作成した Issue の番号で `worktree-create` の手順に従い worktree を作成
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

- ✅ タスクは Issue 本文内のチェックボックスで管理
- ✅ 完了条件を明確にする
- ✅ 具体的なアクションを記述
- ❌ 曖昧なタスク記述
- ❌ `--branch` と `--worktree` の同時指定不可（同時指定時はエラーを表示して終了）
