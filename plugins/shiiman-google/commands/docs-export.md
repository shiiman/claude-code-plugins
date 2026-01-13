---
name: docs-export
description: Google Docs をエクスポートする
allowed-tools: [Bash]
---

# Docs Export

Google Docs をファイルにエクスポートします。

## 引数

- `$ARGUMENTS` (必須): ドキュメントID

## オプション

- `--output <path>` (必須): 出力ファイルパス
- `--type <format>`: 出力形式（pdf, docx, txt, html, rtf, epub）デフォルト: pdf

## 実行

```bash
python plugins/shiiman-google/skills/docs-list/scripts/google_docs.py export --doc-id "$ARGUMENTS" --output "$OUTPUT" ${TYPE:+--type "$TYPE"}
```

## 使用例

```
/shiiman-google:docs-export 1abc...xyz --output ~/Downloads/document.pdf
/shiiman-google:docs-export 1abc...xyz --output ~/Downloads/document.docx --type docx
```
