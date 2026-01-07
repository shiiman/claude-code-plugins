---
name: slides-export
description: Google Slides をエクスポートする。「Slides を PDF で」「プレゼンをエクスポート」「Slides をダウンロード」「PowerPoint で保存」「プレゼンを PDF に」などで起動。`/shiiman-google:slides-export` を実行してエクスポートする。
allowed-tools: [Read, Bash]
---

# Slides Export

Google Slides をファイルにエクスポートします。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:slides-export` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:slides-export` に委譲します（SSOT として扱う）。
