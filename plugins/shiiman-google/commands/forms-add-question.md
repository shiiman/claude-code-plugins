---
name: forms-add-question
description: Google Forms に質問を追加する
allowed-tools: [Bash]
---

# Forms Add Question

Google Forms フォームに質問を追加します。

## 引数

- `$ARGUMENTS` (必須): フォームID

## オプション

- `--question <text>` (必須): 質問文
- `--type <type>` (必須): 質問タイプ（TEXT, PARAGRAPH, RADIO, CHECKBOX, DROP_DOWN, SCALE, DATE, TIME）
- `--options <values>`: 選択肢（カンマ区切り、RADIO/CHECKBOX/DROP_DOWN で使用）
- `--required`: 必須にする

## 実行

```bash
python plugins/shiiman-google/skills/forms-list/scripts/google_forms.py add-question --form-id "$ARGUMENTS" --question "$QUESTION" --type "$TYPE" ${OPTIONS:+--options "$OPTIONS"} ${REQUIRED:+--required}
```

## 使用例

```
/shiiman-google:forms-add-question 1abc --question "お名前" --type TEXT --required
/shiiman-google:forms-add-question 1abc --question "好きな色" --type RADIO --options "赤,青,緑"
```
