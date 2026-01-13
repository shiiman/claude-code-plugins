---
name: slides-export
description: Google Slides をエクスポートする
allowed-tools: [Bash]
---

# Slides Export

Google Slides をファイルにエクスポートします。

## 引数

- `$ARGUMENTS` (必須): プレゼンテーションID

## オプション

- `--output <path>` (必須): 出力ファイルパス
- `--type <format>`: 出力形式（pdf, pptx, odp, txt）デフォルト: pdf

## 実行

```bash
python plugins/shiiman-google/skills/slides-list/scripts/google_slides.py export --presentation-id "$ARGUMENTS" --output "$OUTPUT" ${TYPE:+--type "$TYPE"}
```

## 使用例

```
/shiiman-google:slides-export 1abc...xyz --output ~/Downloads/presentation.pdf
/shiiman-google:slides-export 1abc...xyz --output ~/Downloads/presentation.pptx --type pptx
```
