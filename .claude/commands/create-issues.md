# Create Issues

計画から複数の Issue をまとめて作成します。

## 使い方

```bash
/create-issues
/create-issues --help
```

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--help`   | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### ステップ 1: 計画の確認

ユーザーに計画を聞く、または既存の計画ファイルを確認:

1. **計画の内容**
   - 作成するプラグイン、コマンド、スキル、サブエージェント、フックの一覧
   - 各項目の説明

2. **計画ファイルがある場合**
   - `~/.claude/plans/` 内の最新ファイルを読み込む

### ステップ 2: Issue 一覧の生成

計画から必要な Issue のみを抽出し、一覧を表示:

- 計画に含まれる項目だけを Issue として作成
- 不要な項目は含めない

```text
以下の Issue を作成します:

1. [Plugin] shiiman-common - 汎用ユーティリティプラグイン
2. [Command] shiiman-common:commit - コミットメッセージ生成

作成しますか？ (y/n)
```

**例**: 計画が「プラグインとコマンド1つ」のみの場合、上記のように2つだけ作成。

### ステップ 3: Issue 作成

`gh issue create` コマンドで計画に含まれる Issue のみを作成。

**コマンドリファレンス**（必要なものだけ使用）:

```bash
# プラグイン作成
gh issue create \
  --title "[Plugin] shiiman-common" \
  --body "## プラグイン名
common

## 説明
汎用ユーティリティコマンドを提供" \
  --label "enhancement,plugin"

# コマンド追加
gh issue create \
  --title "[Command] shiiman-common:commit" \
  --body "## 対象プラグイン
shiiman-common

## コマンド名
commit

## 説明
コミットメッセージを生成" \
  --label "enhancement,command"

# スキル追加
gh issue create \
  --title "[Skill] shiiman-common:code-reviewer" \
  --body "## 対象プラグイン
shiiman-common

## スキル名
code-reviewer

## 説明
コードレビューを行うスキル。
トリガー: 「レビューして」「コードチェック」" \
  --label "enhancement,skill"

# サブエージェント追加
gh issue create \
  --title "[Subagent] shiiman-common:test-runner" \
  --body "## 対象プラグイン
shiiman-common

## サブエージェント名
test-runner

## 説明
テストを実行して結果を報告するサブエージェント。
使用ツール: Bash, Read, Grep" \
  --label "enhancement,subagent"

# フック追加
gh issue create \
  --title "[Hook] shiiman-common:PreToolUse:Bash" \
  --body "## 対象プラグイン
shiiman-common

## イベント
PreToolUse

## マッチャー
Bash

## 説明
Bash コマンド実行前にセキュリティチェックを行う。" \
  --label "enhancement,hook"
```

### ステップ 4: 報告

作成された Issue の一覧を表示（計画に含まれたもののみ）:

```text
Issue を作成しました:

- #1 [Plugin] shiiman-common
- #2 [Command] shiiman-common:commit

次のステップ:
- 各 Issue の実装を開始
- 実装完了後は /create-pr で PR を作成
```

## Issue タイプと対応するラベル

| タイプ | タイトルプレフィックス | ラベル |
|--------|------------------------|--------|
| プラグイン | `[Plugin]` | enhancement, plugin |
| コマンド | `[Command]` | enhancement, command |
| スキル | `[Skill]` | enhancement, skill |
| サブエージェント | `[Subagent]` | enhancement, subagent |
| フック | `[Hook]` | enhancement, hook |
