---
name: shiiman-git:git-gtrconfig-setup
description: .gtrconfig を生成。「gtrconfig 設定」「gtr 設定」「.gtrconfig 作成」などで起動。
allowed-tools: [Read, Write, Bash, Glob, AskUserQuestion]
argument-hint: "[--help]"
---

# GTR Config Setup

.gtrconfig ファイルを生成してプロジェクトの worktree 設定を構成するスキル。


## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-git:git-gtrconfig-setup - GTR Config Setup

概要:
  .gtrconfig ファイルを生成してプロジェクトの worktree 設定を構成するスキル。

使用方法:
  /shiiman-git:git-gtrconfig-setup [オプション]

オプション:
  --help  このヘルプを表示
```

## 前提条件

- gtr (git-worktree-runner) がインストール済み
- Git リポジトリ内で実行

## 実行フロー

### ステップ 1: 既存設定の確認

既に .gtrconfig が存在するか確認します。

```bash
cat .gtrconfig 2>/dev/null || echo "Not found"
```

**既存設定がある場合**:

```
既に .gtrconfig が存在します:

{既存設定の内容}

上書きしますか？
- はい: 既存設定をバックアップ (.gtrconfig.backup) して新規作成
- いいえ: 処理を中断
```

### ステップ 2: プロジェクトタイプの自動検出

パッケージファイルから自動判定します。

**検出ロジック**:

```bash
# Node.js
if [ -f "package.json" ]; then
  PROJECT_TYPE="nodejs"

# Python
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
  PROJECT_TYPE="python"

# Go
elif [ -f "go.mod" ]; then
  PROJECT_TYPE="go"

# Rust
elif [ -f "Cargo.toml" ]; then
  PROJECT_TYPE="rust"

# PHP
elif [ -f "composer.json" ]; then
  PROJECT_TYPE="php"

# その他
else
  PROJECT_TYPE="generic"
fi
```

### ステップ 3: ユーザー確認

AskUserQuestion ツールを使用して以下を確認:

1. **デフォルトエディタ**
   - Cursor (推奨)
   - VS Code
   - その他

2. **デフォルト AI ツール**
   - Claude (推奨)
   - その他

3. **カスタムコピールール**
   - デフォルトのまま
   - カスタマイズする

### ステップ 4: テンプレート生成

プロジェクトタイプに応じた .gtrconfig を生成します。

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

### ステップ 5: ファイル生成

.gtrconfig をプロジェクトルートに作成します。

```bash
# バックアップ（既存ファイルがある場合）
[ -f .gtrconfig ] && cp .gtrconfig .gtrconfig.backup

# 新規作成
cat > .gtrconfig << 'EOF'
{テンプレート内容}
EOF
```

### ステップ 6: 完了報告と次のステップ

```
## .gtrconfig を作成しました

### 生成された設定

プロジェクトタイプ: {PROJECT_TYPE}

{生成された .gtrconfig の内容}

### 次のステップ

1. **設定の確認**
   ```bash
   cat .gtrconfig
   ```

2. **.gitignore への追加（チーム設定の場合は追加しない）**

   個人用設定として使う場合:
   ```bash
   echo ".gtrconfig" >> .gitignore
   ```

   チーム全体で共有する場合:
   ```bash
   git add .gtrconfig
   git commit -m "feat: .gtrconfig を追加"
   ```

3. **worktree の作成**
   ```bash
   git gtr new feature/new-feature
   ```

4. **gtr コマンドのクイックリファレンス**
   ```bash
   git gtr new <branch>       # worktree 作成
   git gtr list               # worktree 一覧
   git gtr rm <branch>        # worktree 削除
   git gtr editor <branch>    # エディタで開く
   git gtr ai <branch>        # AI ツールで開く
   ```

### 関連リソース

- gtr 公式リポジトリ: https://github.com/coderabbitai/git-worktree-runner
- 関連スキル: `git-worktree` - gtr で worktree を管理
```

## .gtrconfig 設定項目の詳細

### [copy] セクション

worktree 作成時にコピーするファイルのルールを定義します。

| 設定項目 | 説明 | 例 |
|----------|------|-----|
| `include` | コピーする glob パターン | `**/.env.example` |
| `exclude` | 除外する glob パターン | `**/.env` |
| `includeDirs` | コピーするディレクトリ | `node_modules` |
| `excludeDirs` | 除外するディレクトリ | `node_modules/.cache` |

**glob パターン**:
- `**/*.txt` - すべての .txt ファイル
- `**/test/` - すべての test ディレクトリ
- `*.json` - ルートの .json ファイル

### [hooks] セクション

worktree 作成後に自動実行するコマンドを定義します。

| フック名 | 説明 | 例 |
|----------|------|-----|
| `postCreate` | worktree 作成後に実行 | `npm install` |

**複数コマンド**:

```ini
[hooks]
  postCreate = npm install && npm run build
```

### [defaults] セクション

デフォルトのエディタと AI ツールを定義します。

| 設定項目 | 説明 | 例 |
|----------|------|-----|
| `editor` | デフォルトエディタ | `cursor`, `code`, `vim` |
| `ai` | デフォルト AI ツール | `claude`, `other` |

## エラーハンドリング

### gtr がインストールされていない場合

```
gtr がインストールされていません。

`worktree` スキルでインストール手順を確認できます。
```

### Git リポジトリ外で実行された場合

```
Git リポジトリ内で実行してください。

現在のディレクトリ: {pwd}
```

### ファイル書き込み権限がない場合

```
.gtrconfig の作成に失敗しました。

書き込み権限を確認してください。
```

## カスタマイズ例

### 特定ファイルのみコピー

```ini
[copy]
  include = .env.example
  include = .nvmrc
  exclude = *
```

### 複数のディレクトリを除外

```ini
[copy]
  excludeDirs = node_modules
  excludeDirs = dist
  excludeDirs = .next
  excludeDirs = coverage
```

### postCreate で複数コマンド実行

```ini
[hooks]
  postCreate = npm install && npm run build && npm test
```

### 独自エディタの設定

```ini
[defaults]
  editor = vim
  ai = claude
```
