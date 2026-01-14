---
name: user-setup
description: デフォルトユーザーIDを設定する
allowed-tools: [Bash]
---

# User Setup

デフォルトユーザーIDを設定します。設定したユーザーIDは各スキルで自動的に使用されます。

## 引数

- `$USER_ID` (オプション): 設定するユーザーID（例: U01234567）

## オプション

- `--show`: 現在の設定を表示
- `--clear`: 設定をクリア

## 実行

```bash
# ユーザーIDを設定
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py set-user --user-id "$USER_ID"

# 設定を表示
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py show

# 設定をクリア
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py clear
```

## 使用例

```
# ユーザーIDを設定
/shiiman-slack:user-setup U01234567

# 現在の設定を表示
/shiiman-slack:user-setup --show

# 設定をクリア
/shiiman-slack:user-setup --clear
```

## 出力

設定結果（設定されたユーザーID、ワークスペース情報など）

## 設定ファイル

設定は `~/.config/shiiman-slack/config.json` に保存されます。
