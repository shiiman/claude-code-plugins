---
name: message-history
description: Slack チャンネルの履歴を取得する
allowed-tools: [FetchMcpResource]
---

# Message History

Slack チャンネルの会話履歴を取得します。

## 引数

- `$CHANNEL_ID` (必須): チャンネルID（例: C01234567）

## オプション

- `--limit <number>`: 取得件数（デフォルト: 20）

## 実行

公式Slack MCPの `slack_get_channel_history` ツールを使用:

```
slack_get_channel_history(
  channel_id="$CHANNEL_ID",
  limit=${LIMIT:-20}
)
```

## 使用例

```
/shiiman-slack:message-history C01234567
/shiiman-slack:message-history C01234567 --limit 50
```

## 出力

チャンネルのメッセージ履歴（タイムスタンプ、ユーザー、テキストなど）
