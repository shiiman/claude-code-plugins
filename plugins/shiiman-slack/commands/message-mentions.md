---
name: message-mentions
description: 自分へのメンション一覧を取得する
allowed-tools: [Bash]
---

# Message Mentions

自分へのメンション一覧を取得します。

## 引数

なし

## オプション

- `--max <number>`: 最大取得件数（デフォルト: 20）
- `--format <table|json>`: 出力形式（デフォルト: table）

## 実行

```bash
python plugins/shiiman-slack/skills/mention-checker/scripts/slack_message.py mentions \
  ${MAX:+--max "$MAX"} \
  ${FORMAT:+--format "$FORMAT"}
```

## 使用例

```
/shiiman-slack:message-mentions
/shiiman-slack:message-mentions --max 50
/shiiman-slack:message-mentions --format json
```

## 出力

メンション一覧（チャンネル、ユーザー、テキスト、パーマリンク）

## 必要な環境変数

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
```

## 必要なスコープ

- `search:read`
- `users:read`

## 注意

Slack Search APIは検索履歴の制限があります（フリープランでは直近10,000メッセージ）。
