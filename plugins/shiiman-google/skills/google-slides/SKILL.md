---
name: google-slides
description: Google Slides プレゼンテーションを新規作成・スライド追加する。「プレゼン作成」「Slides 作成」「新しいスライド」「スライド追加」「Slides 更新」「スライドを追加して」「ページを追加」などで起動。
allowed-tools: [Read, Bash]
---

# Slides Editor

Google Slides プレゼンテーションの新規作成・スライド追加を行います。

## ワークフロー

### 新規作成

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_slides.py create \
  --name "プレゼンテーション名" \
  --folder-id "フォルダID"
```

| オプション | 必須 | 説明 |
|-----------|------|------|
| `--name` | Yes | プレゼンテーション名 |
| `--folder-id` | No | 保存先フォルダID |

### スライド追加

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_slides.py add-slide \
  --presentation-id "プレゼンテーションID" \
  --title "スライドタイトル" \
  --body "スライド本文" \
  --layout TITLE_AND_BODY
```

| オプション | 必須 | 説明 |
|-----------|------|------|
| `--presentation-id` | Yes | プレゼンテーションID |
| `--title` | No | スライドタイトル |
| `--body` | No | スライド本文 |
| `--layout` | No | レイアウト（BLANK, TITLE, TITLE_AND_BODY, TITLE_AND_TWO_COLUMNS） |
