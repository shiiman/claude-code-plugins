---
name: shiiman-slack:unread-mark
description: Slack チャンネルを既読にする。「既読にして」「既読化」「チャンネル既読」「未読を消す」「既読マーク」「全部読んだことにして」「既読にしたい」などで起動。Pythonスクリプト `slack_message.py mark-read` を使用。
allowed-tools: [Bash]
argument-hint: "[--help]"
---

# Mark Reader

Slack チャンネルを既読にします（一括既読化）。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-slack:unread-mark - Mark Reader

概要:
  Slack チャンネルを既読にします（一括既読化）。

使用方法:
  /shiiman-slack:unread-mark [オプション]

オプション:
  --help  このヘルプを表示
```

## ワークフロー

### 1. チャンネルの確認

既読にするチャンネルを確認

### 2. 既読化前の確認

既読化する前に必ずユーザーに確認を取る:

```
#general の未読を既読にしますか？

[はい/いいえ]
```

### 3. 既読化実行

Pythonスクリプトを実行:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_message.py mark-read \
  --channel C01234567
```

### 4. 結果の報告

既読化したチャンネル情報を表示
