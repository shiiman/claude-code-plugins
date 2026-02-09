---
name: reaction-add
description: Slack メッセージにリアクションを追加する。「リアクション追加」「リアクションつけて」「👍つけて」「絵文字で反応」「リアクションで返信」「いいねして」「リアクション送って」などで起動。User Token があればユーザーとしてリアクション、なければ Bot としてリアクション。
allowed-tools: [Bash]
---

# Reaction Adder

Slack メッセージにリアクション（絵文字）を追加します。

## トークンについて

| トークン | リアクション元 | 表示 |
| -------- | -------------- | ---- |
| User Token（xoxp-） | ユーザー本人 | 自分のアイコンでリアクション |
| Bot Token（xoxb-） | Bot | Bot のアイコンでリアクション |

**User Token が設定されていない場合**:
Bot としてリアクションを追加します。ユーザーに「Bot としてリアクションしてよいか」を確認してから実行してください。

## ワークフロー

### 1. リアクション情報の確認

以下を確認:

- チャンネルID
- メッセージのタイムスタンプ
- 絵文字名（コロンなし、またはコロン付き）

### 2. トークン状態の確認

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/reaction-adder/slack_reaction.py status
```

User Token の有無を確認し、リアクション元を決定。

### 3. リアクション前の確認

リアクション前に必ずユーザーに確認を取る:

**User Token がある場合:**

```
以下のリアクションをユーザーとして追加してよろしいですか？

チャンネル: #general (C01234567)
メッセージ: 1234567890.123456
絵文字: 👍 (:thumbsup:)
リアクション元: あなた

[はい/いいえ]
```

**User Token がない場合:**

```
User Token が設定されていないため、Bot としてリアクションします。

チャンネル: #general (C01234567)
メッセージ: 1234567890.123456
絵文字: 👍 (:thumbsup:)
リアクション元: Bot

Bot としてリアクションしてよろしいですか？
[はい/いいえ]
```

### 4. リアクション追加

```bash
# ユーザーとしてリアクション（User Token がある場合のデフォルト）
python ${CLAUDE_PLUGIN_ROOT}/scripts/reaction-adder/slack_reaction.py add \
  --channel "C01234567" \
  --timestamp "1234567890.123456" \
  --emoji "thumbsup"

# Bot としてリアクション（明示的に指定）
python ${CLAUDE_PLUGIN_ROOT}/scripts/reaction-adder/slack_reaction.py add \
  --channel "C01234567" \
  --timestamp "1234567890.123456" \
  --emoji ":heart:" \
  --as-bot
```

### 5. 結果の報告

リアクション追加の成功を報告。

## コマンドオプション

| オプション | 必須 | 説明 |
| ---------- | ---- | ---- |
| `--channel`, `-c` | Yes | チャンネルID |
| `--timestamp`, `-t` | Yes | メッセージのタイムスタンプ |
| `--emoji`, `-e` | Yes | 絵文字名（例: thumbsup, :heart:） |
| `--as-bot` | No | Bot としてリアクション（User Token があっても） |

## よく使う絵文字

一覧を表示:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/reaction-adder/slack_reaction.py list
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
