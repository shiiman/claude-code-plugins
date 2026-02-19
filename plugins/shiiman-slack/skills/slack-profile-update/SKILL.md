---
name: slack-profile-update
description: Slack プロフィールを更新する。「プロフィール更新」「ステータス変更」「表示名を変更」「自分のステータス」「プロフィールを変更」「ステータス設定」などで起動。ユーザートークン（SLACK_USER_TOKEN）が必要。
allowed-tools: [Bash]
argument-hint: "[--help]"
---

# Profile Updater

Slack のプロフィールを更新します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/slack-profile-update - Profile Updater

概要:
  Slack のプロフィールを更新します。

使用方法:
  /slack-profile-update [オプション]

オプション:
  --help  このヘルプを表示
```

## 前提条件

このスキルは **User Token（SLACK_USER_TOKEN）** が必要です。
User Token がない場合はエラーになります。

### User Token の設定

`.claude/settings.local.json` または環境変数で設定：

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

### 必要なスコープ

User Token に以下のスコープが必要：

- `users.profile:write` - プロフィール更新

## ワークフロー

### 1. 現在のプロフィールを確認

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/slack-profile-update/scripts/slack_profile.py show
```

### 2. 表示名を変更

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/slack-profile-update/scripts/slack_profile.py update --display-name "新しい表示名"
```

### 3. ステータスを設定

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/slack-profile-update/scripts/slack_profile.py update \
  --status-text "会議中" \
  --status-emoji ":calendar:"
```

### 4. ステータスをクリア

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/slack-profile-update/scripts/slack_profile.py clear-status
```

## 更新可能なフィールド

| フィールド | オプション       | 説明                     |
| ---------- | ---------------- | ------------------------ |
| 表示名     | `--display-name` | Slack に表示される名前   |
| ステータス | `--status-text`  | 現在の状態を示すテキスト |
| 絵文字     | `--status-emoji` | ステータスに付く絵文字   |
| 役職       | `--title`        | 役職・肩書き             |
| 電話番号   | `--phone`        | 連絡先電話番号           |
| 名         | `--first-name`   | 名前（名）               |
| 姓         | `--last-name`    | 名前（姓）               |

## 使用例

### 表示名とステータスを同時に変更

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/slack-profile-update/scripts/slack_profile.py update \
  --display-name "山田太郎 - リモート" \
  --status-text "在宅勤務中" \
  --status-emoji ":house:"
```

### 役職を変更

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/slack-profile-update/scripts/slack_profile.py update \
  --title "シニアエンジニア"
```

## 注意事項

- User Token がないとこのスキルは使用できません
- ワークスペースの設定によっては一部フィールドが変更できない場合があります
- ステータス絵文字は `:emoji_name:` 形式で指定します
