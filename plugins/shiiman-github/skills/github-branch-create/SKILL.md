---
name: shiiman-github:github-branch-create
description: Issue 番号に基づいて feature ブランチを自動作成する。「ブランチ作成」「ブランチを作って」「新しいブランチ」「feature ブランチ」「Issue からブランチ」「作業ブランチを作成」「ブランチ切って」などで起動。feature/[issue番号] 形式でブランチを作成。
allowed-tools: [Read, Bash]
argument-hint: "[--help]"
---

# Create Branch

Issue 番号に基づいて feature ブランチを自動作成します。


## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-github:github-branch-create - Create Branch

概要:
  Issue 番号に基づいて feature ブランチを自動作成します。

使用方法:
  /shiiman-github:github-branch-create [オプション]

オプション:
  --help  このヘルプを表示
```

## ワークフロー

### 1. Issue 番号の確認

ユーザーに Issue 番号を確認。または以下から推測:

- 直前の会話コンテキスト
- 「Issue #5 のブランチを作って」のような指示

### 2. Issue 情報の取得

```bash
gh issue view {issue番号} --json title,labels
```

### 3. ブランチ名の決定

**命名規則**:

| Issue タイプ | ブランチ形式 |
|--------------|--------------|
| 機能追加（enhancement） | `feature/{issue番号}` |
| バグ修正（bug） | `fix/{issue番号}` |
| ドキュメント（documentation） | `docs/{issue番号}` |
| リファクタリング | `refactor/{issue番号}` |
| その他 | `feature/{issue番号}` |

### 4. ブランチ作成

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
git checkout -b feature/{issue番号}
```

ユーザーがベースブランチを明示した場合は、そちらを優先する。

### 5. 結果報告

```
ブランチ `feature/{issue番号}` を作成しました。

関連 Issue: #{issue番号} - {issue タイトル}

作業を開始できます。
```

## 重要な注意事項

- ✅ デフォルトブランチから派生（ユーザー指定があればそちらを優先）
- ✅ Issue 番号をブランチ名に含める
- ✅ Issue タイプに応じたプレフィックス
- ❌ 既存ブランチを上書きしない
- ❌ ユーザー指定なしでデフォルトブランチ以外から派生しない
