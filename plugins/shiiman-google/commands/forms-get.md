---
name: forms-get
description: Google Forms フォームの内容を取得する
allowed-tools: [Bash]
---

# Forms Get

Google Forms フォームの内容を取得します。

## 引数

- `$ARGUMENTS` (必須): フォームID

## 実行

```bash
python plugins/shiiman-google/skills/forms-list/scripts/google_forms.py get --form-id "$ARGUMENTS"
```

## 使用例

```
/shiiman-google:forms-get 1abc...xyz
```
