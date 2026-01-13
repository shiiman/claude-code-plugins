---
name: forms-responses
description: Google Forms の回答を取得する
allowed-tools: [Bash]
---

# Forms Responses

Google Forms の回答を取得します。

## 引数

- `$ARGUMENTS` (必須): フォームID

## オプション

- `--max <number>`: 最大取得件数（デフォルト: 50）

## 実行

```bash
python plugins/shiiman-google/skills/forms-list/scripts/google_forms.py responses --form-id "$ARGUMENTS" ${MAX:+--max "$MAX"}
```

## 使用例

```
/shiiman-google:forms-responses 1abc...xyz
/shiiman-google:forms-responses 1abc...xyz --max 100
```
