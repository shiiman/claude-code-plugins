---
name: message-delete
description: Slack メッセージを削除する。「メッセージ削除」「さっきのを消して」「メッセージを消す」「削除して」「メッセージ取り消し」「投稿を削除」「このメッセージ削除」などで起動。
allowed-tools: [Bash]
---

# Message Deleter

Slack メッセージを削除します。

## トークンについて

| トークン | 削除可能な投稿 |
| -------- | -------------- |
| User Token（xoxp-） | 自分の投稿 |

## ワークフロー

### 1. 削除対象の確認

以下を確認:

- チャンネルID
- メッセージのタイムスタンプ

### 2. トークン状態の確認

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_config.py token-show
```

User Token が設定済みかを確認。未設定の場合は先に `token-set` を実行する。

### 3. 削除前の確認

削除前に必ずユーザーに確認を取る:

**確認例:**

```
以下のメッセージを削除してよろしいですか？

チャンネル: #general (C01234567)
タイムスタンプ: 1234567890.123456
削除者: あなた（ユーザー名）

⚠️ 注意: 削除は取り消しできません

[はい/いいえ]
```

### 4. メッセージ削除

```bash
# メッセージ削除
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_message.py delete \
  --channel C01234567 \
  --ts 1234567890.123456
```

### 5. 結果の報告

削除したメッセージの情報を表示。

## コマンドオプション

| オプション | 必須 | 説明 |
| ---------- | ---- | ---- |
| `--channel` | Yes | チャンネルID |
| `--ts` | Yes | メッセージのタイムスタンプ |

## 注意事項

- 削除は取り消しできません
- 他のユーザーの投稿は削除できません

## User Token の設定方法

自分の投稿を削除するには、`.claude/settings.local.json` に `SLACK_USER_TOKEN` を設定:

```json
{
  "mcpServers": {
    "slack": {
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
        "SLACK_USER_TOKEN": "xoxp-your-user-token"
      }
    }
  }
}
```

User Token には `chat:write` スコープが必要です。
