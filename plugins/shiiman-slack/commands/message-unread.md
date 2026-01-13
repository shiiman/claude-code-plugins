---
name: message-unread
description: Slack の未読メッセージ一覧を取得する
allowed-tools: [Bash]
---

# Message Unread

Slack チャンネルの未読メッセージ一覧を取得します。

## 引数

- `$CHANNEL_ID` (必須): チャンネルID（例: C01234567）

## オプション

- `--max <number>`: 最大取得件数（デフォルト: 20）
- `--format <table|json>`: 出力形式（デフォルト: table）

## 実行

```bash
python plugins/shiiman-slack/skills/unread-checker/scripts/slack_message.py unread \
  --channel "$CHANNEL_ID" \
  ${MAX:+--max "$MAX"} \
  ${FORMAT:+--format "$FORMAT"}
```

## 使用例

```
/shiiman-slack:message-unread C01234567
/shiiman-slack:message-unread C01234567 --max 50
/shiiman-slack:message-unread C01234567 --format json
```

## 出力

未読メッセージ一覧（タイムスタンプ、ユーザー名、テキスト）

## 必要な環境変数

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
```

## 必要なスコープ

- `channels:read`
- `channels:history`
- `groups:read`
- `groups:history`
- `users:read`
