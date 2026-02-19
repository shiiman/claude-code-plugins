---
name: shiiman-workflow:issue-branch-pr-create
description: 既存変更から Issue → ブランチ → コミット・プッシュ（コマンド提示）→ PR を作成する Backward フロー。「変更から Issue と PR」「既存変更を PR に」「diff から Issue」「変更を Issue 化」「Backward フロー」などで起動。
allowed-tools: [Read, Bash, Glob, Grep, Skill, AskUserQuestion]
context: fork
user-invocable: true
argument-hint: "[--help]"
---

# Issue Branch PR Create（Backward フロー）

既存の変更内容から Issue → ブランチ → コミット → プッシュ提示 → PR を作成する Backward フロー。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-workflow:issue-branch-pr-create - 既存変更から Issue・PR を作成する Backward フロー

概要:
  ワーキングツリーの変更やコミット済み未プッシュの変更から
  Issue → ブランチ → コミット → プッシュ提示 → PR を自動作成する。

使用方法:
  /shiiman-workflow:issue-branch-pr-create [オプション]

オプション:
  --help  このヘルプを表示

例:
  /shiiman-workflow:issue-branch-pr-create    # 既存変更から Issue・PR を作成
```

## フロー概要

```
既存変更 → 確認 → Issue 作成 → ブランチ作成 → コミット → プッシュ提示 → PR 作成
```

## 状態分岐テーブル

| ブランチ | 変更状態           | Issue      | Branch   | Commit   | Push | PR   |
| -------- | ------------------ | ---------- | -------- | -------- | ---- | ---- |
| default  | 未コミットあり     | 実行       | 実行     | 実行     | 提示 | 実行 |
| default  | コミット済み未push | 実行       | 実行     | スキップ | 提示 | 実行 |
| feature  | 未コミットあり     | 実行       | スキップ | 実行     | 提示 | 実行 |
| feature  | コミット済み未push | 実行       | スキップ | スキップ | 提示 | 実行 |
| any      | 変更なし           | エラー終了 | -        | -        | -    | -    |

## 実行フロー

### ステップ 1: 変更確認

Bash で現在の変更状態を確認する。

```bash
git status
git diff
git diff --cached
```

未プッシュコミットの確認:

```bash
git log @{u}..HEAD --oneline 2>/dev/null || git log origin/$(git rev-parse --abbrev-ref HEAD)..HEAD --oneline 2>/dev/null
```

**判定ロジック**:

1. ステージング済み変更・未ステージング変更・未プッシュコミットのいずれもない場合 → エラー終了:

```
## エラー: 変更がありません

コミット対象の変更が見つかりませんでした。
変更を加えてから再度実行してください。
```

2. デフォルトブランチ（main/master）か feature ブランチかを判定:

```bash
DEFAULT_BRANCH="$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')"
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
```

- `CURRENT_BRANCH` が `DEFAULT_BRANCH` と一致 → デフォルトブランチ上
- それ以外 → feature ブランチ上

3. 未コミット変更があるか、コミット済み未プッシュのみかを判定

### ステップ 2: Issue 作成

Skill ツールで Issue を作成する。変更内容のサマリーを引数に渡す。

```
Skill: shiiman-github:issue-create
Args: --no-confirm {変更内容のサマリー}
```

作成された Issue 番号を記録する。

### ステップ 3: ブランチ作成

**デフォルトブランチ上の場合のみ実行**。feature ブランチ上ならスキップ。

Skill ツールで Issue 番号からブランチを作成する。

```
Skill: shiiman-github:branch-create
Args: {issue番号}
```

### ステップ 4: コミット

**未コミット変更がある場合のみ実行**。コミット済みならスキップ。

Skill ツールでコミットを実行する。

```
Skill: shiiman-git:add-commit
Args: --no-confirm
```

### ステップ 5: プッシュコマンド提示

**重要**: プッシュは自動実行しない。コマンドを表示するのみ。

```
## プッシュコマンド

以下のコマンドでリモートにプッシュしてください:

\`\`\`bash
git push -u origin {branch}
\`\`\`
```

### ステップ 6: PR 作成

Skill ツールで PR を作成する。

```
Skill: shiiman-github:pr-create
Args: --no-confirm
```

### ステップ 7: 完了報告

```
## Backward フロー完了

### 作成された Issue
- #{issue番号}: {タイトル}

### ブランチ
- {ブランチ名}

### 作成された PR
- PR #{pr番号}: {タイトル}
- URL: {pr_url}

PR がマージされると Issue #{issue番号} は自動的にクローズされます。
```

## 重要な注意事項

- ✅ プッシュは自動実行せず、コマンドを提示するのみ
- ✅ 変更がない場合はエラー終了する
- ✅ デフォルトブランチ上の場合のみブランチを作成する
- ✅ 未コミット変更がある場合のみコミットを実行する
- ✅ Issue 作成・コミット・PR 作成は Skill ツール経由で実行する
- ❌ 変更がないまま Issue や PR を作成しない
- ❌ プッシュを自動実行しない
