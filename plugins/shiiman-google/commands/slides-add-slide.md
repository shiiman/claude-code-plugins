---
name: slides-add-slide
description: Google Slides にスライドを追加する
allowed-tools: [Bash]
---

# Slides Add Slide

Google Slides プレゼンテーションにスライドを追加します。

## 引数

- `$ARGUMENTS` (必須): プレゼンテーションID

## オプション

- `--title <text>`: スライドタイトル
- `--body <text>`: スライド本文
- `--layout <type>`: レイアウト（BLANK, TITLE, TITLE_AND_BODY, TITLE_AND_TWO_COLUMNS）

## 実行

```bash
python plugins/shiiman-google/scripts/google_slides.py add-slide --presentation-id "$ARGUMENTS" ${TITLE:+--title "$TITLE"} ${BODY:+--body "$BODY"} ${LAYOUT:+--layout "$LAYOUT"}
```

## 使用例

```
/shiiman-google:slides-add-slide 1abc...xyz --title "新機能紹介" --body "詳細説明"
/shiiman-google:slides-add-slide 1abc...xyz --layout BLANK
```
