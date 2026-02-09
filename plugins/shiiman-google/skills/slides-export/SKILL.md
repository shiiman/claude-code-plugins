---
name: slides-export
description: Google Slides をエクスポートする。「Slides を PDF で」「プレゼンをエクスポート」「Slides をダウンロード」「PowerPoint で保存」「プレゼンを PDF に」などで起動。
allowed-tools: [Read, Bash]
---

# Slides Export

Google Slides をファイルにエクスポートします。

## 引数

- プレゼンテーションID (必須): エクスポートするプレゼンテーションのID

## オプション

- `--output <path>` (必須): 出力ファイルパス
- `--type <format>`: 出力形式（pdf, pptx, odp, txt）デフォルト: pdf

## 実行方法

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slides-list/google_slides.py export --presentation-id <presentation-id> --output ~/Downloads/presentation.pdf
```

### PowerPoint形式でエクスポート

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slides-list/google_slides.py export --presentation-id <presentation-id> --output ~/Downloads/presentation.pptx --type pptx
```
