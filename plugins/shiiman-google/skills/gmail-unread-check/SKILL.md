---
name: shiiman-google:gmail-unread-check
description: Gmail の未読メッセージ一覧を取得する。「未読メール」「Gmail 未読」「未読一覧」「未読メールを見たい」「未読メッセージ」「メールの未読」「全アカウントの未読」などで起動。
allowed-tools: [Read, Bash]
argument-hint: "[--help]"
---

# Gmail Unread

Gmail の未読メッセージ一覧を取得します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-google:gmail-unread-check - Gmail Unread

概要:
  Gmail の未読メッセージ一覧を取得します。

使用方法:
  /shiiman-google:gmail-unread-check [オプション]

オプション:
  --help  このヘルプを表示
```

## 実行方法

### アクティブプロファイルの未読一覧

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py unread
```

### 最大件数を指定

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py unread --max 50
```

### 全プロファイルの未読一覧

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py unread-all
```

### 未読が100件を超えるか確認

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py unread-all --show-has-more
```

### JSON 形式で出力

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py --format json unread
```

## 出力項目

- id: メッセージID
- subject: 件名
- from: 送信者
- date: 受信日時

## 追加取得について

デフォルトでは最大100件を取得します。

### 追加取得の確認方法

`--show-has-more` オプションを使用すると、指定した件数（デフォルト100件）を超える未読があるかどうかが表示されます。
出力に「※ まだ未読があります」と表示された場合は、ユーザーに追加取得するか確認してください。

### 追加取得の実行方法

続きを取得する場合は `--max 200` のように件数を増やして再実行します。

## 既読化の提案

未読メッセージ表示後、既読にするか確認する:

```
確認した未読を既読にしますか？（shiiman-google:gmail-unread-mark で既読化できます）
```
