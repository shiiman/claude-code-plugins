---
name: shiiman-slack:unread-check
description: Slack の未読メッセージを確認する（全チャンネル横断確認対応）。「Slack未読確認」「未読メッセージ」「未読ある？」「Slackの未読」「未読を見せて」「未読チェック」「未読メール確認」「全チャンネルの未読」「未読サマリー」などで起動。Pythonスクリプト `slack_message.py unread` を使用。
allowed-tools: [Bash]
argument-hint: "[--help]"
---

# Unread Checker

Slack の未読メッセージを確認します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-slack:unread-check - Unread Checker

概要:
  Slack の未読メッセージを確認します。

使用方法:
  /shiiman-slack:unread-check [オプション]

オプション:
  --help  このヘルプを表示
```

## ワークフロー

### 1. 未読メッセージ取得

Pythonスクリプトで未読メッセージ一覧を取得。3パターンのコマンドがある:

#### 全チャンネル詳細（チャンネル省略時）

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_message.py --format table unread
```

#### 全チャンネルサマリー（高速）

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_message.py unread --summary
```

`--summary` オプション: 各チャンネルの未読件数のみを一覧表示する。メッセージ本文は取得しないため高速。

#### 単一チャンネル指定

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_message.py --format table unread \
  --channel <CHANNEL_ID>
```

オプション:

- `--channel <CHANNEL_ID>`: チャンネルID（省略時は全チャンネルを横断確認）
- `--summary`: 未読件数のみのサマリー表示（高速）
- `--max <number>`: 最大取得件数（デフォルト: 20）
- `--format <table|json>`: 出力形式（デフォルト: table）※サブコマンドの前に指定

### 2. 結果の整形

チャンネルごとに未読メッセージをグループ化して表示:

```
# Slack 未読メッセージ

## #general (5件)
**山田太郎** (10:30)
今日のミーティングは15時からです

**佐藤花子** (10:32)
了解しました！

## #project-alpha (3件)
**田中一郎** (09:15)
PRレビューお願いします
```

### 3. 優先度の提示

未読メッセージの優先度を判断:

- メンション付き: 高優先度
- DMやプライベートチャンネル: 中優先度
- パブリックチャンネル: 通常優先度

### 4. 既読化の提案

未読メッセージ表示後、既読にするか確認する:

```
確認した未読を既読にしますか？（unread-mark で既読化できます）
```

## トークン設定

`/shiiman-slack:user-setup` でトークンを設定してください。

## 必要なスコープ

- `channels:read`
- `channels:history`
- `groups:read`
- `groups:history`
- `users:read`
