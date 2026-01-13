---
name: message-deleter
description: Slack メッセージを削除する。「メッセージ削除」「さっきのを消して」「メッセージを消す」「削除して」「メッセージ取り消し」「投稿を削除」「このメッセージ削除」などで起動。Pythonスクリプト `slack_message.py delete` を使用。
allowed-tools: [Bash]
---

# Message Deleter

Slack メッセージを削除します。

## ワークフロー

### 1. 削除対象の確認

以下を確認:
- チャンネルID
- メッセージのタイムスタンプ

### 2. 削除前の確認

削除前に必ずユーザーに確認を取る:

```
以下のメッセージを削除してよろしいですか？

チャンネル: #general
タイムスタンプ: 1234567890.123456

注意: 削除は取り消しできません

[はい/いいえ]
```

### 3. メッセージ削除

Pythonスクリプトを実行:

```bash
python plugins/shiiman-slack/skills/unread-checker/scripts/slack_message.py delete \
  --channel C01234567 \
  --ts 1234567890.123456
```

### 4. 結果の報告

削除したメッセージの情報を表示

## 注意事項

- Bot が投稿したメッセージのみ削除可能です
- 他のユーザーが投稿したメッセージは削除できません
- 削除は取り消しできません

## コマンド連携

実際の処理は `/shiiman-slack:message-delete` に委譲します（SSOT として扱う）。
