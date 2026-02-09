---
name: message-send
description: Slack にメッセージを送信する。「メッセージ送信」「Slackに投稿」「#channel に送って」「メッセージを送る」「投稿して」「Slackに書き込み」「チャンネルに送信」などで起動。
allowed-tools: [Bash]
---

# Message Sender

Slack にメッセージを送信します。

## トークンについて

| トークン | 投稿者 | 表示名 |
|---------|--------|--------|
| User Token（xoxp-） | ユーザー本人 | 自分の名前とアイコン |

## ワークフロー

### 1. 送信先と内容の確認

ユーザーに以下を確認:
- 送信先チャンネル（チャンネル名を指定された場合は ID を調べる）
- メッセージ内容

### 2. トークン状態の確認

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_config.py token-show
```

User Token が設定済みかを確認。未設定の場合は先に `token-set` を実行する。

### 3. 送信前の確認

送信前に必ずユーザーに確認を取る:

**確認例:**
```
以下の内容でユーザーとして送信してよろしいですか？

チャンネル: #general (C01234567)
メッセージ: お疲れ様です。本日の作業完了しました。
投稿者: あなた（ユーザー名）

[はい/いいえ]
```

### 4. メッセージ送信

```bash
# メッセージ投稿
python ${CLAUDE_PLUGIN_ROOT}/skills/message-send/scripts/slack_post.py post \
  --channel "C01234567" \
  --text "お疲れ様です。本日の作業完了しました。"
```

### 5. 送信結果の報告

送信したメッセージのタイムスタンプとチャンネル情報を表示。

## コマンドオプション

| オプション | 必須 | 説明 |
|-----------|------|------|
| `--channel`, `-c` | Yes | チャンネルID |
| `--text`, `-t` | Yes | メッセージテキスト |

## User Token の設定方法

ユーザーとして投稿するには、`.claude/settings.local.json` に `SLACK_USER_TOKEN` を設定:

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
