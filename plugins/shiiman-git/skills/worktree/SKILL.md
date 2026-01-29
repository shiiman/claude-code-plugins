---
name: worktree
description: gtr で worktree を管理。「worktree 作成」「gtr list」「gtr rm」などで起動。
allowed-tools: [Read, Bash, Glob, Grep]
---

# Worktree Management with gtr

gtr (git-worktree-runner) を使用して git worktree を管理するスキル。

## 前提条件

- gtr (git-worktree-runner) がインストール済み
  - インストール方法: https://github.com/coderabbitai/git-worktree-runner

## 機能

### 1. gtr インストール確認

最初に gtr がインストールされているか確認します。

```bash
git gtr --version
```

**未インストール時の対応**:

```
gtr がインストールされていません。以下の手順でインストールしてください:

## インストール方法

```bash
# リポジトリをクローン
git clone https://github.com/coderabbitai/git-worktree-runner.git
cd git-worktree-runner

# シンボリックリンクを作成
sudo ln -s "$(pwd)/bin/git-gtr" /usr/local/bin/git-gtr

# 確認
git gtr --version
```

## エイリアス設定（推奨）

```bash
# .bashrc または .zshrc に追加
alias gwr='git gtr'
```
```

### 2. worktree 作成 (gtr new)

ユーザー入力から以下を判定:
- 「worktree 作成」「gtr new」「新しい worktree」「ワークツリー作成」

**基本操作**:

```bash
git gtr new <branch-name>
```

**オプション**:

- `--from-current`: 現在のブランチから派生
- `--editor`: 作成後にエディタで開く
- `--ai`: 作成後に AI ツール（Claude Code）で開く

**実行例**:

```bash
# 基本
git gtr new feature/new-feature

# 現在のブランチから派生
git gtr new feature/bugfix --from-current

# 作成後にエディタで開く
git gtr new feature/ui-update --editor

# 作成後に Claude Code で開く
git gtr new feature/refactor --ai
```

**処理フロー**:

1. ブランチ名を確認（指定がない場合はユーザーに質問）
2. オプションの確認（--from-current, --editor, --ai）
3. `git gtr new` を実行
4. 成功メッセージを表示

### 3. worktree 一覧 (gtr list)

ユーザー入力から以下を判定:
- 「worktree 一覧」「gtr list」「ワークツリー一覧」「worktree 確認」

**基本操作**:

```bash
git gtr list
```

**詳細表示**:

```bash
git gtr list --porcelain
```

**実行結果の整形**:

一覧を見やすく整形して表示します:

```
## Worktree 一覧

| ブランチ | パス |
|----------|------|
| main | /path/to/main |
| feature/A | /path/to/feature-A |
| feature/B | /path/to/feature-B |
```

### 4. worktree 削除 (gtr rm)

ユーザー入力から以下を判定:
- 「worktree 削除」「gtr rm」「ワークツリー削除」「worktree を消す」

**基本操作**:

```bash
git gtr rm <branch-name>
```

**強制削除**:

```bash
git gtr rm <branch-name> --force
```

**処理フロー**:

1. 削除対象のブランチ名を確認
2. 未コミット変更がある場合は警告
3. ユーザー確認後に削除実行
4. 成功メッセージを表示

### 5. worktree をエディタで開く (gtr editor)

ユーザー入力から以下を判定:
- 「worktree を開く」「gtr editor」「エディタで開く」

**基本操作**:

```bash
git gtr editor <branch-name>
```

**処理フロー**:

1. ブランチ名を確認
2. .gtrconfig の defaults.editor 設定を使用
3. エディタで worktree を開く

### 6. worktree を AI ツールで開く (gtr ai)

ユーザー入力から以下を判定:
- 「worktree を AI で」「gtr ai」「Claude で開く」「AI ツールで開く」

**基本操作**:

```bash
git gtr ai <branch-name>
```

**処理フロー**:

1. ブランチ名を確認
2. .gtrconfig の defaults.ai 設定を使用（通常は claude）
3. Claude Code で worktree を開く

## エラーハンドリング

### gtr コマンドが失敗した場合

エラーメッセージを確認し、以下を提案:

1. gtr がインストールされているか確認
2. git リポジトリ内で実行しているか確認
3. .gtrconfig が正しく設定されているか確認

### worktree 作成時にブランチが既に存在する場合

gtr は自動的に既存ブランチの worktree を作成します。

### worktree 削除時に未コミット変更がある場合

警告を表示し、`--force` オプションの使用を提案します。

## 関連リソース

- gtr 公式リポジトリ: https://github.com/coderabbitai/git-worktree-runner
- Zenn 記事: https://zenn.dev/yumemi_inc/articles/20251213_gtr
- 関連スキル: `gtrconfig-setup` - .gtrconfig 設定ファイル生成
