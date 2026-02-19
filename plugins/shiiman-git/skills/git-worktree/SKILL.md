---
name: shiiman-git:git-worktree
description: gtr で worktree を管理。「worktree 作成」「gtr new」「gtr list」「gtr rm」「worktree 削除」「クリーンアップ」「マージ済み削除」「ワークツリー」などで起動。
allowed-tools: [Read, Bash, Glob, Grep]
argument-hint: "[--help]"
---

# Worktree Management with gtr

gtr (git-worktree-runner) を使用して git worktree を管理するスキル。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-git:git-worktree - Worktree Management with gtr

概要:
  gtr を使用して worktree の作成・一覧・削除・クリーンアップを行う。

使用方法:
  /shiiman-git:git-worktree [オプション]

オプション:
  --help  このヘルプを表示

対応コマンド:
  new     現在のブランチから worktree を作成
  list    worktree の一覧を表示
  rm      worktree をブランチごと削除
  clean   不要な worktree をクリーンアップ
```

## 前提条件

- gtr (git-worktree-runner) がインストール済み
  - 未インストールの場合は `git-worktree-setup` スキルを案内する

## 機能

ユーザーの発話内容から以下の 3 パターンを判定して実行する。

### 1. worktree 作成

トリガー: 「worktree 作成」「gtr new」「新しい worktree」「ワークツリー作成」

現在のブランチをベースに worktree を作成する。

```bash
git gtr new <branch> --from-current
```

**処理フロー**:

1. ブランチ名を確認（指定がない場合はユーザーに質問）
2. `git gtr new <branch> --from-current` を実行
3. 成功メッセージを表示

### 2. worktree 一覧

トリガー: 「worktree 一覧」「gtr list」「ワークツリー一覧」「worktree 確認」

```bash
git gtr list
```

結果をテーブル形式に整形して表示:

```
## Worktree 一覧

| ブランチ | パス |
|----------|------|
| main | /path/to/main |
| feature/A | /path/to/feature-A |
```

### 3. worktree 削除 + クリーンアップ

#### 個別削除

トリガー: 「worktree 削除」「gtr rm」「ワークツリー削除」「worktree を消す」

ブランチごと複数 worktree をまとめて削除する。

```bash
git gtr rm <branch1> <branch2> --delete-branch
```

**処理フロー**:

1. 削除対象のブランチ名を確認（`git gtr list` で一覧を提示）
2. ユーザー確認後に `--delete-branch` 付きで削除実行
3. 成功メッセージを表示

#### クリーンアップ

トリガー: 「クリーンアップ」「マージ済み削除」「不要な worktree を整理」

不要な worktree を一括削除する。

```bash
git gtr clean
```

**処理フロー**:

1. まず `git gtr clean --dry-run` でプレビューを表示
2. ユーザー確認後に `git gtr clean` を実行
3. 成功メッセージを表示

## エラーハンドリング

### gtr がインストールされていない場合

```
gtr がインストールされていません。
`/shiiman-git:git-worktree-setup` でインストールと設定ができます。
```

### worktree 削除時に未コミット変更がある場合

警告を表示し、`--force` オプションの使用を提案する。

## 関連リソース

- gtr 公式リポジトリ: https://github.com/coderabbitai/git-worktree-runner
- 関連スキル: `git-worktree-setup` - gtr のインストールと .gtrconfig 設定
