---
name: shiiman-github:pr-create
description: 現在のブランチから PR を作成または更新する。「PR 作成」「PR を作って」「プルリク作成」「pull request」「PR 出して」「プルリクエスト」「レビュー依頼したい」「PR 更新」などで起動。変更内容を分析し適切な PR を生成。
allowed-tools: [Read, Bash, Glob, Grep]
argument-hint: "[タイトル] [--base <branch>|--draft|--help]"
context: fork
---

# Create PR

現在のブランチから PR を作成または更新します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-github:pr-create - PR 作成・更新

概要:
  現在のブランチから PR を作成または更新する。
  既存 PR がある場合は自動的に更新モードになる。
  ブランチ名から関連 Issue を自動検出し、PR テンプレートに従って本文を生成。

使用方法:
  /shiiman-github:pr-create [タイトル] [オプション]

オプション:
  --help           このヘルプを表示
  --base <branch>  宛先ブランチを指定（デフォルト: リポジトリのデフォルトブランチ）
  --draft          ドラフト PR として作成

例:
  /shiiman-github:pr-create                    # PR を作成または更新
  /shiiman-github:pr-create --draft            # ドラフト PR を作成
  /shiiman-github:pr-create "タイトル"          # タイトルを指定して PR 作成
  /shiiman-github:pr-create --base develop     # develop ブランチ向けに PR 作成
```

## ワークフロー

### 1. 事前チェック

```bash
DEFAULT_BRANCH="$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')"
CURRENT_BRANCH="$(git branch --show-current)"

# ブランチ状態確認
git status --short
git fetch origin
git log "origin/${CURRENT_BRANCH}..HEAD" --oneline 2>/dev/null
```

**ブランチ状態の検証**:

- ✅ 未コミットの変更がない
- ✅ プッシュされていないコミットがない
- ❌ いずれかがある場合は警告して処理を終了

### 2. 既存 PR の自動検出

```bash
gh pr list --head "${CURRENT_BRANCH}" --json number,title,url
```

- **既存 PR あり**: 更新モードに切替（タイトル・本文の更新を提案）
- **既存 PR なし**: 新規作成モード

### 3. 変更内容の確認

```bash
git log "origin/${DEFAULT_BRANCH}..HEAD" --oneline
git diff "origin/${DEFAULT_BRANCH}...HEAD" --stat
```

### 4. 関連 Issue の特定

以下から関連 Issue を判定:

- ブランチ名（`feature/5` → #5）
- コミットメッセージ
- ユーザーへの確認

### 5. 破壊的変更の検出

以下のパターンを検出した場合、PR タイトルに `!` を付与して警告:

- コミットメッセージに `BREAKING CHANGE:` または `!:` が含まれる
- 公開 API の削除・シグネチャ変更

```
⚠️ 破壊的変更が検出されました:
- コミット: feat!: 認証方式を変更

PR タイトルに破壊的変更を明示しますか？
```

### 6. PR 内容の作成

**タイトル**: Conventional Commits 形式

| タイプ   | 説明             | 例                                   |
| -------- | ---------------- | ------------------------------------ |
| feat     | 新機能           | `feat: shiiman-git プラグインを追加` |
| fix      | バグ修正         | `fix: Issue 番号の取得を修正`        |
| docs     | ドキュメント     | `docs: README を更新`                |
| refactor | リファクタリング | `refactor: スキル構造を整理`         |
| chore    | その他の変更     | `chore: 依存関係を更新`              |

### 7. PR 作成・更新

**新規作成の場合**:

```bash
gh pr create \
  --title "feat: {変更内容の要約}" \
  --body "## 概要

{変更内容の説明}

## 変更内容

- {変更点1}
- {変更点2}

## 関連 Issue

Closes #{issue番号}

## テスト計画

- [ ] {テスト項目1}
- [ ] {テスト項目2}

## チェックリスト

- [x] 命名規則に従っている
- [x] README.md を更新した（必要な場合）
- [x] 動作確認済み"
```

`--draft` 指定時は `gh pr create --draft` を使用。

**更新の場合**:

```bash
gh pr edit {pr番号} \
  --title "{更新タイトル}" \
  --body "{更新本文}"
```

### 8. 結果報告

```
PR を{作成|更新}しました:

- URL: {pr_url}
- タイトル: {title}
- 関連 Issue: #{issue番号}
- モード: {新規作成|更新}

マージ後、Issue #{issue番号} は自動的にクローズされます。
```

## 重要な注意事項

- ✅ 既存 PR がある場合は自動的に更新モードになる
- ✅ Conventional Commits 形式のタイトル
- ✅ 関連 Issue を `Closes #N` で参照
- ✅ PR タイトルと本文は日本語
- ✅ 未コミット・未プッシュの変更がある場合は警告して終了
- ❌ Issue の自動クローズを忘れない
