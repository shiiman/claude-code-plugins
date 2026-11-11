---
name: shiiman-github:pr-create
description: 現在のブランチから PR を作成または更新する。「PR 作成」「PR を作って」「プルリク作成」「pull request」「PR 出して」「プルリクエスト」「レビュー依頼したい」「PR 更新」などで起動。変更内容を分析し適切な PR を生成。「ドラフトで」「develop 向けに」などは発話から判断する。
allowed-tools: [Read, Bash, Glob, Grep, Skill]
argument-hint: "[タイトル]"
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
  /shiiman-github:pr-create [タイトル]

オプション:
  --help  このヘルプを表示

指定の伝え方:
  「ドラフトで」「draft で」      → ドラフト PR として作成
  「develop 向けに」「base は X」  → 宛先ブランチを指定（既定: リポジトリのデフォルトブランチ）

例:
  /shiiman-github:pr-create               # PR を作成または更新
  /shiiman-github:pr-create "タイトル"     # タイトルを指定して PR 作成
  「ドラフトで PR を作って」        # ドラフト PR を作成
  「develop 向けに PR を作成」      # develop ブランチ向けに PR 作成

内部呼び出し用:
  --no-confirm  許可済みワークフローからの呼び出し用の互換オプション
```

## 許可と確認の方針

グローバルの許可方針と現在の依頼から実行範囲を判断する。このスキルの操作を明示的に依頼されていれば、それを許可として扱い、生成した文面の承認や `--no-confirm` の指定を改めて求めない。このオプションは許可済みの呼び出しとの互換用であり、指定自体が許可を与えるものではない。セキュリティチェックは維持し、許可不足、重要な範囲変更、許可範囲外の具体的なリスクがある場合だけ確認する。

## 起動時の自動判断

引数・発話から PR の作成条件を判定する。明示がなければ既定を採用する。

| 項目         | 既定                   | 判断ルール                                        |
| ------------ | ---------------------- | ------------------------------------------------- |
| 宛先ブランチ | リポジトリのデフォルト | 「develop 向けに」「base は X」等の発話があれば X |
| ドラフト     | 通常 PR                | 「ドラフトで」「draft で」「WIP」等あれば draft   |

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

- 未コミットの変更と未 push のコミットを確認する。feature branch が未 push という理由だけで終了しない。
- PR 作成の依頼には、対象の feature branch のコミットを公開するために必要な通常の push を含む。remote・送信先・送信する差分を確認し、この許可だけで force-push やデフォルトブランチへの push は行わない。
- 対象変更のコミットが必要なら、その変更からの PR 作成依頼には検証後の必要なコミットも含む。`shiiman-git:add-commit` を使い、対象パスや hunk だけをコミットして無関係な編集・ステージ済みの内容を保護する。
- 対象範囲を安全に判断できない場合や、許可されていない内容を公開してしまう場合だけ確認する。「コミットしない」「push しない」などの制約を優先し、実行できない場合は阻害要因を報告して PR 完了を主張しない。

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
- 関連 Issue を特定できなければリンクを省略する。リンクが必須で対象が曖昧な場合だけ確認する。

### 5. 破壊的変更の検出

コミットと公開 API の変更から破壊的変更の有無を確認する。確認できた場合は Conventional Commits のタイトルに明示し、影響を説明する。タイトルに記号を付けるかの追加確認はしない。PR 作成の許可はデプロイやマージの許可を含まない。

### 6. PR 内容の作成

**タイトル**: Conventional Commits 形式

| タイプ   | 説明             | 例                                   |
| -------- | ---------------- | ------------------------------------ |
| feat     | 新機能           | `feat: shiiman-git プラグインを追加` |
| fix      | バグ修正         | `fix: Issue 番号の取得を修正`        |
| docs     | ドキュメント     | `docs: README を更新`                |
| refactor | リファクタリング | `refactor: スキル構造を整理`         |
| chore    | その他の変更     | `chore: 依存関係を更新`              |

検証した差分、リポジトリのテンプレート、実際の検証結果から日本語のタイトルと本文を作成する。PR 作成・更新が許可済みなら、文面の再承認を求めず進める。`--no-confirm` は任意であり、許可範囲を広げない。

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

ドラフトと判定した場合は `gh pr create --draft` を使用。宛先ブランチを判定した場合は `gh pr create --base {branch}` を付与する（既定はリポジトリのデフォルトブランチ）。

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
- 確認済みの関連 Issue がある場合は `Closes #N` で参照し、なければ該当セクションを省略する。
- ✅ PR タイトルと本文は日本語
- PR 作成前に、許可されたコミットと通常の feature branch push を完了し、無関係な作業を保護する。
- 存在しない Issue を記載したり、未実行のチェックが成功したと主張したりしない。
