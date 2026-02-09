---
name: message-edit
description: Slack メッセージを編集する。「メッセージ編集」「さっきのを修正」「メッセージ修正」「訂正して」「編集して」「メッセージを直す」「内容を変更」などで起動。
allowed-tools: [Bash]
---

# Message Editor

Slack メッセージを編集します。

## トークンについて

| トークン | 編集可能な投稿 |
| -------- | -------------- |
| User Token（xoxp-） | 自分の投稿 |

## ワークフロー

### 1. 編集対象の確認

以下を確認:

- チャンネルID
- メッセージのタイムスタンプ
- 新しいメッセージ内容

### 2. トークン状態の確認

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_config.py token-show
```

User Token が設定済みかを確認。未設定の場合は先に `token-set` を実行する。

### 3. 編集前の確認

編集前に必ずユーザーに確認を取る:

**確認例:**

```
以下のメッセージを編集してよろしいですか？

チャンネル: #general (C01234567)
タイムスタンプ: 1234567890.123456
新しい内容: 訂正: お疲れ様でした
編集者: あなた（ユーザー名）

[はい/いいえ]
```

### 4. メッセージ編集

```bash
# メッセージ編集
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_message.py edit \
  --channel C01234567 \
  --ts 1234567890.123456 \
  --text "訂正: お疲れ様でした"
```

### 5. 結果の報告

編集したメッセージの情報を表示。

## コマンドオプション

| オプション | 必須 | 説明 |
| ---------- | ---- | ---- |
| `--channel` | Yes | チャンネルID |
| `--ts` | Yes | メッセージのタイムスタンプ |
| `--text` | Yes | 新しいメッセージテキスト |

## User Token の設定方法

自分の投稿を編集するには、`.claude/settings.local.json` に `SLACK_USER_TOKEN` を設定:

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
