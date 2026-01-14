---
name: profile-update
description: 自分の Slack プロフィールを更新する
allowed-tools: [Bash]
---

# Profile Update

自分の Slack プロフィールを更新します。User Token（SLACK_USER_TOKEN）が必要です。

## 引数

なし（オプションで指定）

## オプション

- `--show`: 現在のプロフィールを表示
- `--display-name`: 表示名を変更
- `--status-text`: ステータステキストを設定
- `--status-emoji`: ステータス絵文字を設定
- `--clear-status`: ステータスをクリア

## 実行

```bash
# 現在のプロフィールを表示
python plugins/shiiman-slack/skills/profile-updater/scripts/slack_profile.py show

# 表示名を変更
python plugins/shiiman-slack/skills/profile-updater/scripts/slack_profile.py update --display-name "新しい表示名"

# ステータスを設定
python plugins/shiiman-slack/skills/profile-updater/scripts/slack_profile.py update --status-text "会議中" --status-emoji ":calendar:"

# ステータスをクリア
python plugins/shiiman-slack/skills/profile-updater/scripts/slack_profile.py clear-status
```

## 使用例

```
# プロフィールを表示
/shiiman-slack:profile-update --show

# 表示名を変更
/shiiman-slack:profile-update --display-name "田中 太郎"

# ステータスを設定
/shiiman-slack:profile-update --status-text "休憩中" --status-emoji ":coffee:"

# ステータスをクリア
/shiiman-slack:profile-update --clear-status
```

## 出力

更新結果（変更されたフィールドの情報）

## 注意

このコマンドには `SLACK_USER_TOKEN`（xoxp-で始まるトークン）が必要です。
Bot Token のみでは実行できません。
