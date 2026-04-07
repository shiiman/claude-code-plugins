---
name: shiiman-github:worktree-create
description: worktree を作成する。「worktree 作成」「ワークツリー作成」「worktree を作って」「worktree 切って」「Issue から worktree」「作業用 worktree」「gtr new」などで起動。Issue 番号・ブランチ名の直接指定・コンテキストからの自動命名に対応。
allowed-tools: [Read, Bash]
argument-hint: "[Issue番号|ブランチ名] [--help]"
---

# Create Worktree

gtr (git-worktree-runner) を使用して worktree を作成します。Issue 番号指定・ブランチ名直接指定・コンテキストからの自動命名に対応。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-github:worktree-create - Create Worktree

概要:
  gtr を使用して worktree を作成する。
  Issue 番号、ブランチ名の直接指定、コンテキストからの自動命名に対応。

使用方法:
  /shiiman-github:worktree-create [Issue番号|ブランチ名] [オプション]

オプション:
  --help  このヘルプを表示

例:
  /shiiman-github:worktree-create 5                   # Issue #5 から feature/5 の worktree を作成
  /shiiman-github:worktree-create feature/add-auth     # ブランチ名を直接指定して worktree を作成
  /shiiman-github:worktree-create                      # コンテキストから自動命名
```

## 前提条件

- gtr (git-worktree-runner) がインストール済み
  - 未インストールの場合は `shiiman-git:worktree-setup` スキルを案内する

## ワークフロー

### 1. gtr の確認

```bash
git gtr --version
```

コマンドが失敗した場合:

```
gtr がインストールされていません。
`/shiiman-git:worktree-setup` でインストールと設定ができます。
```

### 2. ブランチ名の決定

引数の内容に応じて分岐:

**A) 引数が Issue 番号の場合**（数値のみ、例: `5`）:

1. Issue 情報を取得

```bash
gh issue view {issue番号} --json title,labels
```

2. Issue タイプに応じたブランチ名を決定

| Issue タイプ                  | ブランチ形式           |
| ----------------------------- | ---------------------- |
| 機能追加（enhancement）       | `feature/{issue番号}`  |
| バグ修正（bug）               | `fix/{issue番号}`      |
| ドキュメント（documentation） | `docs/{issue番号}`     |
| リファクタリング              | `refactor/{issue番号}` |
| その他                        | `feature/{issue番号}`  |

**B) 引数がブランチ名の場合**（数値以外、例: `feature/add-auth`）:

- そのまま使用

**C) 引数なしの場合**:

1. 会話コンテキスト（直前のタスク説明・指示内容）からブランチ名を自動命名
   - 例: 「認証機能を追加」→ `feature/add-auth`
   - 例: 「ログインバグを修正」→ `fix/login-bug`
2. 手がかりがない場合のみユーザーに確認

### 3. worktree 作成

```bash
# デフォルトブランチから最新を取得
DEFAULT_BRANCH="$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')"
if [ -z "$DEFAULT_BRANCH" ]; then
  echo "ERROR: デフォルトブランチを取得できませんでした。" >&2
  exit 1
fi
git fetch origin "$DEFAULT_BRANCH"

# gtr で worktree を作成
git gtr new {ブランチ名}
```

ユーザーがベースブランチを明示した場合は、`--from-current` オプションを使用:

```bash
git gtr new {ブランチ名} --from-current
```

### 4. worktree ディレクトリへ移動

作成した worktree のパスに `cd` で移動する。

```bash
cd {worktree のパス}
```

### 5. mise trust（mise.toml が存在する場合）

`mise` のセキュリティ仕様により、新しい worktree パスでは `mise.toml` が未信頼扱いになる。
`mise.toml` が存在する場合は信頼登録を実行する。

```bash
if [ -f "mise.toml" ]; then
  mise trust mise.toml
fi
```

失敗した場合はエラーを表示するが、処理は継続する（mise を使わない環境では不要なため）。

### 6. 結果報告

**Issue 指定時**:

```
worktree `feature/{issue番号}` を作成しました。

関連 Issue: #{issue番号} - {issue タイトル}
パス: {worktree のパス}

作業を開始できます。
```

**Issue なし時**:

```
worktree `{ブランチ名}` を作成しました。

パス: {worktree のパス}

作業を開始できます。
```

## 重要な注意事項

- ✅ デフォルトブランチから派生（ユーザー指定があればそちらを優先）
- ✅ Issue タイプに応じたプレフィックス
- ✅ コンテキストから自動命名を試みる
- ✅ gtr を使用して worktree を管理
- ❌ 既存ブランチを上書きしない
- ❌ ユーザー指定なしでデフォルトブランチ以外から派生しない

## エラーハンドリング

### gtr がインストールされていない場合

```
gtr がインストールされていません。
`/shiiman-git:worktree-setup` でインストールと設定ができます。
```

### worktree 作成に失敗した場合

エラーメッセージを表示し、原因と対処法を提案する。

## 関連リソース

- gtr 公式リポジトリ: https://github.com/coderabbitai/git-worktree-runner
- 関連スキル: `shiiman-git:worktree` - worktree の一覧・削除・クリーンアップ
- 関連スキル: `shiiman-git:worktree-setup` - gtr のインストールと .gtrconfig 設定
- 関連スキル: `shiiman-github:branch-create` - ブランチのみ作成（worktree なし）
