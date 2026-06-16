---
name: shiiman-slack:unread-mark
description: Slack チャンネルを既読にする（全チャンネル一括既読化対応）。「Slack を既読にして」「Slack 既読化」「Slack チャンネル既読」「Slack の未読を消す」「Slack 既読マーク」「Slack を全部読んだことにして」「Slack 全部既読」「Slack を一括既読」などで起動。Pythonスクリプト `slack_message.py mark-read` を使用。
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
（チャンネル省略の場合: 全未読チャンネルを一括既読化しますか？）

[はい/いいえ]
```

### 3. 既読化実行

Pythonスクリプトを実行:

#### 全未読チャンネルを一括既読化（チャンネル省略時）

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_message.py mark-read
```

#### 単一チャンネル既読化

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_message.py mark-read \
  --channel C01234567
```

### 4. 結果の報告

既読化したチャンネル情報を表示
