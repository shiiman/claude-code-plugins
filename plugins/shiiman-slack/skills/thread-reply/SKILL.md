---
name: thread-reply
description: Slack スレッドに返信する。「スレッドに返信」「スレッド返信して」「このスレッドに返信」「スレッドで返信」「スレッドに投稿」「スレッドに書き込み」「返信をスレッドで」などで起動。
allowed-tools: [Bash]
---

# Thread Replier

Slack スレッドに返信します。

## トークンについて

| トークン | 返信者 | 表示名 |
| -------- | ------ | ------ |
| User Token（xoxp-） | ユーザー本人 | 自分の名前とアイコン |

## ワークフロー

### 1. スレッド情報の確認

以下を確認:

- チャンネルID
- スレッドのタイムスタンプ（親メッセージのts）
- 返信内容

### 2. トークン状態の確認

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_config.py token-show
```

User Token が設定済みかを確認。未設定の場合は先に `token-set` を実行する。

### 3. 送信前の確認

送信前に必ずユーザーに確認を取る:

**確認例:**

```
以下の内容でユーザーとしてスレッドに返信してよろしいですか？

チャンネル: #general (C01234567)
スレッド: 1234567890.123456
返信: 了解しました！
投稿者: あなた（ユーザー名）

[はい/いいえ]
```

### 4. スレッド返信

```bash
# スレッド返信
python ${CLAUDE_PLUGIN_ROOT}/skills/thread-reply/scripts/slack_thread.py reply \
  --channel "C01234567" \
  --thread-ts "1234567890.123456" \
  --text "了解しました！"
```

### 5. 送信結果の報告

送信した返信のタイムスタンプとスレッド情報を表示。

## コマンドオプション

| オプション | 必須 | 説明 |
| ---------- | ---- | ---- |
| `--channel`, `-c` | Yes | チャンネルID |
| `--thread-ts`, `-t` | Yes | スレッドのタイムスタンプ |
| `--text`, `-m` | Yes | 返信テキスト |

## User Token の設定方法

ユーザーとして返信するには、`.claude/settings.local.json` に `SLACK_USER_TOKEN` を設定:

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
