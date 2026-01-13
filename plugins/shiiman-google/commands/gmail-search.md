---
name: gmail-search
description: Gmail でメールを検索する
allowed-tools: [Bash]
---

# Gmail Search

Gmail でメールを検索します。Gmail の検索クエリ構文を使用できます。

## 引数

- `$ARGUMENTS` (必須): 検索クエリ

## オプション

- `--max <number>`: 最大取得件数（デフォルト: 20）
- `--include-body`: 本文プレビューを含める

## クエリ例

- `from:user@example.com` - 送信者で検索
- `to:user@example.com` - 宛先で検索
- `subject:会議` - 件名で検索
- `has:attachment` - 添付ファイル付き
- `after:2025/01/01` - 日付以降
- `before:2025/01/31` - 日付以前
- `is:unread` - 未読
- `is:starred` - スター付き
- `label:important` - ラベルで検索

## 実行

```bash
python plugins/shiiman-google/skills/gmail-unread/scripts/google_gmail.py search --query "$ARGUMENTS" ${MAX:+--max "$MAX"} ${INCLUDE_BODY:+--include-body}
```

## 使用例

```
/shiiman-google:gmail-search from:boss@company.com
/shiiman-google:gmail-search subject:会議 after:2025/01/01 --max 50
/shiiman-google:gmail-search has:attachment is:unread --include-body
```
