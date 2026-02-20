---
name: shiiman-google:gmail-unread-mark
description: Gmail の未読を既読化する。「既読にする」「未読を既読」「メールを既読化」「Gmail 既読化」「未読を消す」「メールを開封扱い」「一括既読」などで起動。
allowed-tools: [Read, Bash]
argument-hint: "[--help]"
---

# Gmail Mark Read

Gmail の未読メッセージを既読化します（単体/一括）。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-google:gmail-unread-mark - Gmail Mark Read

概要:
  Gmail の未読メッセージを既読化します（単体/一括）。

使用方法:
  /shiiman-google:gmail-unread-mark [オプション]

オプション:
  --help  このヘルプを表示
```

## 実行方法

### 特定メッセージを既読化

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py mark-read --ids <message-id>
```

### 複数メッセージを一括で既読化

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py mark-read --ids <id1> <id2> <id3>
```

### 未読メッセージを一括で既読化

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py mark-read --all
```

### プロファイル指定

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py --profile <profile-name> mark-read --all
```

## オプション

- `--ids <id1> <id2> ...`: 既読化するメッセージIDのリスト（スペース区切り）
- `--all`: 全ての未読メッセージを既読化

## 関連操作

- 未読一覧を確認: `shiiman-google:gmail-unread-check` を実行

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
- `--all` オプションは全ての未読を既読化するため、慎重に使用してください
