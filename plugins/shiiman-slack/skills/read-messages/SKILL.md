---
name: read-messages
description: Slack チャンネルのメッセージ履歴を取得する。「メッセージ確認」「履歴を見せて」「最新メッセージ」「#channel のメッセージ」「会話履歴」「過去のメッセージ」「チャンネル履歴」などで起動。公式Slack MCPの `slack_get_channel_history` を使用。
allowed-tools: [FetchMcpResource]
---

# Message Reader

Slack チャンネルのメッセージ履歴を取得します。

## ワークフロー

### 1. チャンネル特定

ユーザーが指定したチャンネル名またはIDを特定

### 2. メッセージ履歴取得

公式Slack MCPの `slack_get_channel_history` ツールを呼び出す:

```
slack_get_channel_history(
  channel_id="C01234567",
  limit=20
)
```

オプション:
- `limit`: 取得件数（デフォルト: 20）

### 3. 結果の整形

メッセージを整形して表示:

```
# #general の最新メッセージ

**山田太郎** (10:30)
今日のミーティングは15時からです

**佐藤花子** (10:32)
了解しました！
```
