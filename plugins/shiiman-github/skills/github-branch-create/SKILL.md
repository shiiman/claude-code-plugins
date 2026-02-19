---
name: shiiman-github:github-branch-create
description: feature ブランチを作成する。「ブランチ作成」「ブランチを作って」「新しいブランチ」「feature ブランチ」「Issue からブランチ」「作業ブランチを作成」「ブランチ切って」などで起動。Issue 番号・ブランチ名の直接指定・コンテキストからの自動命名に対応。
allowed-tools: [Read, Bash]
argument-hint: "[Issue番号|ブランチ名] [--help]"
---

# Create Branch

feature ブランチを作成します。Issue 番号指定・ブランチ名直接指定・コンテキストからの自動命名に対応。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-github:github-branch-create - Create Branch

概要:
  feature ブランチを作成する。
  Issue 番号、ブランチ名の直接指定、コンテキストからの自動命名に対応。

使用方法:
  /shiiman-github:github-branch-create [Issue番号|ブランチ名] [オプション]

オプション:
  --help  このヘルプを表示

例:
  /shiiman-github:github-branch-create 5                   # Issue #5 から feature/5 を作成
  /shiiman-github:github-branch-create feature/add-auth     # ブランチ名を直接指定
  /shiiman-github:github-branch-create                      # コンテキストから自動命名
```

## ワークフロー

### 1. ブランチ名の決定

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

### 2. ブランチ作成

```bash
# デフォルトブランチから最新を取得
DEFAULT_BRANCH="$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')"
if [ -z "$DEFAULT_BRANCH" ]; then
  echo "ERROR: デフォルトブランチを取得できませんでした。" >&2
  exit 1
fi
git fetch origin "$DEFAULT_BRANCH"
git checkout "$DEFAULT_BRANCH"
git pull origin "$DEFAULT_BRANCH"

# 新しいブランチを作成
git checkout -b {ブランチ名}
```

ユーザーがベースブランチを明示した場合は、そちらを優先する。

### 3. 結果報告

**Issue 指定時**:

```
ブランチ `feature/{issue番号}` を作成しました。

関連 Issue: #{issue番号} - {issue タイトル}

作業を開始できます。
```

**Issue なし時**:

```
ブランチ `{ブランチ名}` を作成しました。

作業を開始できます。
```

## 重要な注意事項

- ✅ デフォルトブランチから派生（ユーザー指定があればそちらを優先）
- ✅ Issue タイプに応じたプレフィックス
- ✅ コンテキストから自動命名を試みる
- ❌ 既存ブランチを上書きしない
- ❌ ユーザー指定なしでデフォルトブランチ以外から派生しない
