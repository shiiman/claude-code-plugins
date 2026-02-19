---
name: shiiman-git:git-worktree-setup
description: gtr のインストールと .gtrconfig を設定する。「worktree セットアップ」「gtr 設定」「gtrconfig 設定」「.gtrconfig 作成」「gtr インストール」「worktree 設定」などで起動。
allowed-tools: [Read, Write, Bash, Glob, AskUserQuestion]
argument-hint: "[--help]"
---

# Worktree Setup

gtr (git-worktree-runner) のインストール確認と .gtrconfig の生成・更新を行うスキル。
実行するたびにプロジェクトの現状に合わせて .gtrconfig を更新する。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-git:git-worktree-setup - Worktree Setup

概要:
  gtr のインストール確認と .gtrconfig の生成・更新を行う。
  実行するたびにプロジェクトの現状に合わせて .gtrconfig を更新する。

使用方法:
  /shiiman-git:git-worktree-setup [オプション]

オプション:
  --help  このヘルプを表示
```

## 実行フロー

### ステップ 1: gtr インストール確認

```bash
git gtr --version
```

**未インストール時の対応**:

インストール手順を案内して処理を終了する。

```
gtr がインストールされていません。以下の手順でインストールしてください:

## インストール方法

# Homebrew（推奨）
brew install coderabbitai/gtr/git-gtr

# または手動インストール
git clone https://github.com/coderabbitai/git-worktree-runner.git
cd git-worktree-runner
sudo ln -s "$(pwd)/bin/git-gtr" /usr/local/bin/git-gtr

# 確認
git gtr --version
```

### ステップ 2: プロジェクト状態を分析

パッケージファイルからプロジェクトタイプを自動検出する。

```bash
# Node.js
[ -f "package.json" ] && PROJECT_TYPE="nodejs"

# Python
[ -f "pyproject.toml" ] || [ -f "requirements.txt" ] && PROJECT_TYPE="python"

# Go
[ -f "go.mod" ] && PROJECT_TYPE="go"

# Rust
[ -f "Cargo.toml" ] && PROJECT_TYPE="rust"

# PHP
[ -f "composer.json" ] && PROJECT_TYPE="php"

# その他
PROJECT_TYPE="generic"
```

既存の .gtrconfig があれば読み込む:

```bash
cat .gtrconfig 2>/dev/null
```

### ステップ 3: .gtrconfig を生成/更新

プロジェクトタイプに応じたテンプレートをベースに生成する。
既存設定がある場合は差分を提示してユーザーに確認する。

#### Node.js プロジェクト

```ini
[copy]
  include = **/.env.example
  include = **/.nvmrc
  include = **/tsconfig.json
  include = **/.prettierrc
  include = **/.eslintrc*
  exclude = **/.env
  exclude = **/.env.local
  excludeDirs = node_modules
  excludeDirs = dist
  excludeDirs = .next
  excludeDirs = build

[hooks]
  postCreate = npm install

[defaults]
  editor = cursor
  ai = claude
```

#### Python プロジェクト

```ini
[copy]
  include = **/.env.example
  include = **/pyproject.toml
  include = **/requirements*.txt
  include = **/.python-version
  exclude = **/.env
  exclude = **/.env.local
  excludeDirs = .venv
  excludeDirs = venv
  excludeDirs = __pycache__
  excludeDirs = .mypy_cache
  excludeDirs = .pytest_cache
  excludeDirs = *.egg-info

[hooks]
  postCreate = pip install -e ".[dev]"

[defaults]
  editor = cursor
  ai = claude
```

#### Go プロジェクト

```ini
[copy]
  include = **/.env.example
  include = **/go.mod
  include = **/go.sum
  exclude = **/.env
  exclude = **/.env.local
  excludeDirs = vendor
  excludeDirs = bin

[hooks]
  postCreate = go mod download

[defaults]
  editor = cursor
  ai = claude
```

#### Rust プロジェクト

```ini
[copy]
  include = **/.env.example
  include = **/Cargo.toml
  include = **/Cargo.lock
  exclude = **/.env
  exclude = **/.env.local
  excludeDirs = target
  excludeDirs = .cargo

[hooks]
  postCreate = cargo fetch

[defaults]
  editor = cursor
  ai = claude
```

#### PHP プロジェクト

```ini
[copy]
  include = **/.env.example
  include = **/composer.json
  include = **/composer.lock
  exclude = **/.env
  exclude = **/.env.local
  excludeDirs = vendor

[hooks]
  postCreate = composer install

[defaults]
  editor = cursor
  ai = claude
```

#### Generic プロジェクト

```ini
[copy]
  include = **/.env.example
  exclude = **/.env
  exclude = **/.env.local

[hooks]
  postCreate = echo "Worktree created successfully"

[defaults]
  editor = cursor
  ai = claude
```

### ステップ 4: ファイル書き込み

初回の場合はそのまま生成する。
既存ファイルがある場合はバックアップを作成し、差分を表示してユーザー確認後に更新する。

```bash
# バックアップ（既存ファイルがある場合）
[ -f .gtrconfig ] && cp .gtrconfig .gtrconfig.backup
```

### ステップ 5: 完了報告

```
## .gtrconfig を更新しました

プロジェクトタイプ: {PROJECT_TYPE}

{変更内容の差分 or 生成された内容}

### 次のステップ

- worktree を作成: `/shiiman-git:git-worktree`
```

## .gtrconfig 設定項目の詳細

### [copy] セクション

worktree 作成時にコピーするファイルのルールを定義する。

| 設定項目      | 説明                     | 例                    |
| ------------- | ------------------------ | --------------------- |
| `include`     | コピーする glob パターン | `**/.env.example`     |
| `exclude`     | 除外する glob パターン   | `**/.env`             |
| `includeDirs` | コピーするディレクトリ   | `node_modules`        |
| `excludeDirs` | 除外するディレクトリ     | `node_modules/.cache` |

### [hooks] セクション

worktree ライフサイクルで自動実行するコマンドを定義する。

| フック名     | 説明                          | 例               |
| ------------ | ----------------------------- | ---------------- |
| `postCreate` | worktree 作成後               | `npm install`    |
| `preRemove`  | worktree 削除前（失敗時中断） | `npm run clean`  |
| `postRemove` | worktree 削除後               | `echo "removed"` |

### [defaults] セクション

デフォルトのエディタと AI ツールを定義する。

| 設定項目 | 説明                 | 例                      |
| -------- | -------------------- | ----------------------- |
| `editor` | デフォルトエディタ   | `cursor`, `code`, `vim` |
| `ai`     | デフォルト AI ツール | `claude`, `other`       |

## 重要な注意事項

- ✅ 何度実行しても安全（冪等）
- ✅ 既存設定がある場合は差分を提示して確認
- ✅ バックアップを自動作成
- ❌ ユーザーの確認なしに既存設定を上書きしない

## 関連リソース

- gtr 公式リポジトリ: https://github.com/coderabbitai/git-worktree-runner
- 関連スキル: `git-worktree` - gtr で worktree を管理
