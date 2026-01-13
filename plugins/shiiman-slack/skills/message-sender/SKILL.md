---
name: message-sender
description: Slack にメッセージを送信する。「メッセージ送信」「Slackに投稿」「#channel に送って」「メッセージを送る」「投稿して」「Slackに書き込み」「チャンネルに送信」などで起動。公式Slack MCPの `slack_post_message` を使用。
allowed-tools: [FetchMcpResource]
---

# Message Sender

Slack にメッセージを送信します。

## ワークフロー

### 1. 送信先と内容の確認

ユーザーに以下を確認:
- 送信先チャンネル
- メッセージ内容

### 2. 送信前の確認

送信前に必ずユーザーに確認を取る:

```
以下の内容で送信してよろしいですか？

チャンネル: #general
メッセージ: お疲れ様です。本日の作業完了しました。

[はい/いいえ]
```

### 3. メッセージ送信

公式Slack MCPの `slack_post_message` ツールを使用:

```
slack_post_message(
  channel_id="C01234567",
  text="お疲れ様です。本日の作業完了しました。"
)
```

### 4. 送信結果の報告

送信したメッセージのタイムスタンプとチャンネル情報を表示

## コマンド連携

実際の処理は `/shiiman-slack:message-send` に委譲します（SSOT として扱う）。
