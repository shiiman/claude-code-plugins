---
name: slides-get
description: Google Slides プレゼンテーションの内容を取得する
allowed-tools: [Bash]
---

# Slides Get

Google Slides プレゼンテーションの内容を取得します。

## 引数

- `$ARGUMENTS` (必須): プレゼンテーションID

## 実行

```bash
python plugins/shiiman-google/scripts/google_slides.py get --presentation-id "$ARGUMENTS"
```

## 使用例

```
/shiiman-google:slides-get 1abc...xyz
```
