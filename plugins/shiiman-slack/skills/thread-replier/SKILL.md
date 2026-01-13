---
name: thread-replier
description: Slack スレッドに返信する。「スレッドに返信」「スレッド返信して」「このスレッドに返信」「スレッドで返信」「スレッドに投稿」「スレッドに書き込み」「返信をスレッドで」などで起動。公式Slack MCPの `slack_reply_to_thread` を使用。
allowed-tools: [FetchMcpResource]
---

# Thread Replier

Slack スレッドに返信します。

## ワークフロー

### 1. スレッド情報の確認

以下を確認:
- チャンネルID
- スレッドのタイムスタンプ（親メッセージのts）
- 返信内容

### 2. 送信前の確認

送信前に必ずユーザーに確認を取る:

```
以下の内容でスレッドに返信してよろしいですか？

チャンネル: #general
スレッド: 1234567890.123456
返信: 了解しました！

[はい/いいえ]
```

### 3. スレッド返信

公式Slack MCPの `slack_reply_to_thread` ツールを使用:

```
slack_reply_to_thread(
  channel_id="C01234567",
  thread_ts="1234567890.123456",
  text="了解しました！"
)
```

### 4. 送信結果の報告

送信した返信のタイムスタンプとスレッド情報を表示

## コマンド連携

実際の処理は `/shiiman-slack:thread-reply` に委譲します（SSOT として扱う）。
