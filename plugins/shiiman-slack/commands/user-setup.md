---
name: user-setup
description: トークン設定・デフォルトユーザーIDを設定する
allowed-tools: [Bash]
---

# User Setup

Slack トークンとデフォルトユーザーIDを設定します。

## 引数

- `$USER_ID` (オプション): 設定するユーザーID（例: U01234567）

## オプション

- `--token <TOKEN>`: User Token (xoxp-...) を設定
- `--show`: 現在の設定を表示
- `--clear`: ユーザー設定をクリア
- `--auto`: トークンからユーザーを自動検出して設定

## 実行

```bash
# トークンを設定（初回セットアップ）
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py token-set --token "$TOKEN"

# トークンからユーザーを自動検出して設定
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py auto-detect

# ユーザーIDを手動で設定
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py set-user --user-id "$USER_ID"

# 設定を表示
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py show

# ユーザー設定をクリア
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py clear

# トークンをクリア
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py token-clear
```

## 使用例

```
# トークンを設定（初回セットアップ、必須）
/shiiman-slack:user-setup --token xoxp-your-user-token

# トークンから自動検出
/shiiman-slack:user-setup --auto

# ユーザーIDを手動で設定
/shiiman-slack:user-setup U01234567

# 現在の設定を表示
/shiiman-slack:user-setup --show

# ユーザー設定をクリア
/shiiman-slack:user-setup --clear
```

## 出力

設定結果（設定されたユーザーID、ワークスペース情報など）

## 設定ファイル

設定は `~/.config/shiiman-slack/config.json` に保存されます。
