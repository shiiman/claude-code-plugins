---
name: shiiman-github:issue-create
description: GitHub Issue を作成する。タスクは Issue 本文内でチェックボックスに分割。「Issue 作成」「Issue を作って」「タスクを Issue に」「Issue 追加」「チケット作成」「Issue を切る」「タスクを分割して Issue」などで起動。「ブランチも」「worktree も」と伝えれば作成後にブランチ/worktree も用意する。
allowed-tools: [Read, Bash, Glob, Grep, AskUserQuestion]
argument-hint: "[タスク説明]"
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
  「ブランチも」「worktree も」と伝えれば作成後にブランチ/worktree も用意します。

使用方法:
  /shiiman-github:issue-create [タスク説明]

オプション:
  --help  このヘルプを表示

後続作成の伝え方:
  「ブランチも作って」    → Issue 作成後にブランチを作成
  「worktree も」         → Issue 作成後に worktree を作成（gtr 使用）
  指定なし                → Issue 作成のみで終了

例:
  /shiiman-github:issue-create                    # Issue を作成
  「Issue を作ってブランチも切って」        # Issue 作成後にブランチも作成
  「Issue を作って worktree も用意して」    # Issue 作成後に worktree も作成

内部呼び出し用:
  --no-confirm  許可済みワークフローからの呼び出し用の互換オプション
```

## 許可と確認の方針

グローバルの許可方針と現在の依頼から実行範囲を判断する。このスキルの操作を明示的に依頼されていれば、それを許可として扱い、生成した文面の承認や `--no-confirm` の指定を改めて求めない。このオプションは許可済みの呼び出しとの互換用であり、指定自体が許可を与えるものではない。セキュリティチェックは維持し、許可不足、重要な範囲変更、許可範囲外の具体的なリスクがある場合だけ確認する。

## ワークフロー

### 1. タスクの確認

タスク説明と会話の情報を優先する。既存の情報から作成対象の Issue を判断できない場合だけ概要を質問する。

### 2. タスクの分割

タスクを Issue 本文内のチェックボックスに分割:

- 1 タスク = 具体的なアクション（「〜を追加」「〜を修正」「〜を削除」）
- 依存関係がある場合は順番に並べる
- テストやドキュメント更新も個別タスクとして記載

### 3. Issue 内容の準備

依頼からタイトル・ラベル・タスクのチェックボックス・完了条件を用意する。明示的な Issue 作成依頼があれば文面を再承認せず作成する。重要な情報不足や未許可の範囲についてだけ確認する。`--no-confirm` 自体は許可を与えない。

### 4. Issue 作成

作成が許可され、内容を検証できたら `gh issue create` で Issue を作成する。

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

### 6. ブランチもしくは worktree 作成

引数・発話から後続作成の要否を判定する。

**「ブランチも」と判定した場合**:

作成した Issue の番号で `shiiman-github:branch-create` スキルのワークフローに従いブランチを自動作成する。

**「worktree も」と判定した場合**:

作成した Issue の番号で `shiiman-github:worktree-create` スキルのワークフローに従い worktree を自動作成する。

**後続の作成が依頼されていない場合**:

Issue の URL を報告して終了する。branch や worktree を作るかは質問しない。許可済みの親ワークフローで必要な場合は、その指定に従い追加確認せず進める。

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
- ❌ ブランチと worktree の同時作成はしない（どちらか一方のみ。両方求められた場合は worktree を優先して確認）
