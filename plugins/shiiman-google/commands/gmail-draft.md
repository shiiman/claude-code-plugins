---
name: gmail-draft
description: Gmail で下書きを作成する
allowed-tools: [Bash]
---

# Gmail Draft

Gmail で下書きを作成します。

## 引数

- `$ARGUMENTS` (必須): 宛先メールアドレス

## オプション

- `--subject <text>` (必須): 件名
- `--body <text>` (必須): 本文
- `--cc <emails>`: CC（カンマ区切り）
- `--bcc <emails>`: BCC（カンマ区切り）
- `--html`: HTMLメールとして送信

## 実行

```bash
python plugins/shiiman-google/skills/gmail-unread/scripts/google_gmail.py draft --to "$ARGUMENTS" --subject "$SUBJECT" --body "$BODY" ${CC:+--cc "$CC"} ${BCC:+--bcc "$BCC"} ${HTML:+--html}
```

## 使用例

```
/shiiman-google:gmail-draft user@example.com --subject "件名" --body "本文です。"
/shiiman-google:gmail-draft user@example.com --subject "報告" --body "内容" --cc "cc1@example.com"
```
