---
name: reaction-add
description: Slack メッセージにリアクションを追加する。「リアクション追加」「リアクションつけて」「👍つけて」「絵文字で反応」「リアクションで返信」「いいねして」「リアクション送って」などで起動。
allowed-tools: [Bash]
---

# Reaction Adder

Slack メッセージにリアクション（絵文字）を追加します。

## トークンについて

| トークン | リアクション元 | 表示 |
| -------- | -------------- | ---- |
| User Token（xoxp-） | ユーザー本人 | 自分のアイコンでリアクション |

## ワークフロー

### 1. リアクション情報の確認

以下を確認:

- チャンネルID
- メッセージのタイムスタンプ
- 絵文字名（コロンなし、またはコロン付き）

### 2. トークン状態の確認

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_config.py token-show
```

User Token が設定済みかを確認。未設定の場合は先に `token-set` を実行する。

### 3. リアクション前の確認

リアクション前に必ずユーザーに確認を取る:

**確認例:**

```
以下のリアクションをユーザーとして追加してよろしいですか？

チャンネル: #general (C01234567)
メッセージ: 1234567890.123456
絵文字: 👍 (:thumbsup:)
リアクション元: あなた

[はい/いいえ]
```

### 4. リアクション追加

```bash
# リアクション追加
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_reaction.py add \
  --channel "C01234567" \
  --timestamp "1234567890.123456" \
  --emoji "thumbsup"
```

### 5. 結果の報告

リアクション追加の成功を報告。

## コマンドオプション

| オプション | 必須 | 説明 |
| ---------- | ---- | ---- |
| `--channel`, `-c` | Yes | チャンネルID |
| `--timestamp`, `-t` | Yes | メッセージのタイムスタンプ |
| `--emoji`, `-e` | Yes | 絵文字名（例: thumbsup, :heart:） |

## よく使う絵文字

一覧を表示:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_reaction.py list
```

| 絵文字名 | 表示 |
| -------- | ---- |
| `thumbsup`, `+1` | 👍 |
| `heart` | ❤️ |
| `eyes` | 👀 |
| `fire` | 🔥 |
| `100` | 💯 |
| `tada` | 🎉 |
| `rocket` | 🚀 |
| `white_check_mark` | ✅ |
| `x` | ❌ |
| `thinking_face` | 🤔 |
| `raised_hands` | 🙌 |
| `clap` | 👏 |
| `pray` | 🙏 |
| `sparkles` | ✨ |

## User Token の設定方法

ユーザーとしてリアクションするには、`.claude/settings.local.json` に `SLACK_USER_TOKEN` を設定:

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

User Token には `reactions:write` スコープが必要です。
