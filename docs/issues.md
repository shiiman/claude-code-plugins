# Issue 作成ガイド

## 概要

計画から複数の GitHub Issue をまとめて作成します。

## コマンド

```bash
/create-issues
```

## Issue タイプ

| タイプ | プレフィックス | ラベル |
|--------|----------------|--------|
| プラグイン | `[Plugin]` | enhancement, plugin |
| コマンド | `[Command]` | enhancement, command |
| スキル | `[Skill]` | enhancement, skill |
| サブエージェント | `[Subagent]` | enhancement, subagent |
| フック | `[Hook]` | enhancement, hook |
| その他 | `[Request]` | question |

## Issue 作成コマンド

```bash
# プラグイン
gh issue create \
  --title "[Plugin] shiiman-common" \
  --body "## プラグイン名
common

## 説明
汎用ユーティリティコマンドを提供" \
  --label "enhancement,plugin"

# コマンド
gh issue create \
  --title "[Command] shiiman-common:commit" \
  --body "## 対象プラグイン
shiiman-common

## コマンド名
commit

## 説明
コミットメッセージを生成" \
  --label "enhancement,command"

# スキル
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

# サブエージェント
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

# フック
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

## ワークフロー

```text
1. 計画を立てる（plan mode）
   ↓
2. /create-issues で Issue をまとめて作成
   ↓
3. 各 Issue の実装
   ↓
4. /create-pr で PR 作成（Issue をクローズ）
```

## 関連コマンド

- `/create-pr` - PR を作成して Issue をクローズ
