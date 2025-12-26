# Create PR

実装完了後に PR を作成し、関連 Issue をクローズします。

## 使い方

```bash
/create-pr
/create-pr --help
```

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--help`   | このコマンドのヘルプを表示 |

## 実行例

```bash
# 基本的な使用
/create-pr
→ 変更内容を確認
→ 関連 Issue を自動判定
→ PR を作成

# 結果:
# https://github.com/shiiman/claude-code-plugins/pull/4
# Closes #1, #2, #3
```

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### ステップ 1: 変更内容の確認

以下を確認:

1. **git status** - 変更されたファイル一覧
2. **git diff** - 変更内容の詳細
3. **git log** - 最近のコミット（未プッシュ含む）

### ステップ 2: 関連 Issue の自動判定

1. `gh issue list --state open` で未クローズの Issue を取得
2. 変更内容（git diff）と Issue タイトル/内容を照合
3. 関連する Issue を自動で特定

**判定ロジック**:

- プラグイン名が一致する Issue
- コマンド名/スキル名/サブエージェント名が一致する Issue
- 変更ファイルパスから推測

### ステップ 3: PR 作成

```bash
gh pr create \
  --title "feat: shiiman-common プラグインを追加" \
  --body "## 概要

shiiman-common プラグインを追加しました。

## 変更内容

- プラグイン構造を作成
- commit コマンドを追加
- code-reviewer スキルを追加

## 関連 Issue

Closes #1, #2, #3

## チェックリスト

- [x] 命名規則に従っている
- [x] README.md を更新した
- [x] 動作確認済み"
```

### PR タイトルの命名規則

Conventional Commits 形式:

| タイプ   | 説明               | 例                                      |
|----------|--------------------|-----------------------------------------|
| feat     | 新機能             | `feat: shiiman-common プラグインを追加` |
| fix      | バグ修正           | `fix: コマンド名の typo を修正`         |
| docs     | ドキュメント       | `docs: README を更新`                   |
| refactor | リファクタリング   | `refactor: スキル構造を整理`            |
| chore    | その他の変更       | `chore: .gitignore を更新`              |

### ステップ 4: 報告

```text
PR を作成しました:

https://github.com/shiiman/claude-code-plugins/pull/4

クローズされる Issue:
- #1 [Plugin] shiiman-common
- #2 [Command] shiiman-common:commit
- #3 [Skill] shiiman-common:code-reviewer

次のステップ:
- PR をレビュー
- マージ後、Issue が自動でクローズされます
```
