---
name: google-forms
description: Google Forms フォームを新規作成・質問追加する。「フォーム作成」「Forms 作成」「新しいフォーム」「アンケート作成」「質問追加」「Forms 更新」「フォームに質問を追加」「アンケート項目追加」などで起動。
allowed-tools: [Read, Bash]
---

# Forms Editor

Google Forms フォームの新規作成・質問追加を行います。

## ワークフロー

### 新規作成

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_forms.py create \
  --name "フォーム名" \
  --description "フォームの説明"
```

| オプション | 必須 | 説明 |
|-----------|------|------|
| `--name` | Yes | フォーム名 |
| `--description` | No | フォームの説明 |

### 質問追加

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_forms.py add-question \
  --form-id "フォームID" \
  --question "質問文" \
  --type RADIO \
  --options "選択肢1,選択肢2,選択肢3" \
  --required
```

| オプション | 必須 | 説明 |
|-----------|------|------|
| `--form-id` | Yes | フォームID |
| `--question` | Yes | 質問文 |
| `--type` | Yes | 質問タイプ（TEXT, PARAGRAPH, RADIO, CHECKBOX, DROP_DOWN, SCALE, DATE, TIME） |
| `--options` | No | 選択肢（カンマ区切り、RADIO/CHECKBOX/DROP_DOWN 時） |
| `--required` | No | 必須フラグ |
