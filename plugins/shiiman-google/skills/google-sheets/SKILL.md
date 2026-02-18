---
name: google-sheets
description: Google Sheets スプレッドシートを新規作成・更新する。「スプレッドシート作成」「Sheets 作成」「新しいシート」「スプレッドシート更新」「Sheets 更新」「シートに書き込み」「セルを更新」などで起動。
allowed-tools: [Read, Bash]
---

# Sheets Editor

Google Sheets スプレッドシートの新規作成・セル更新を行います。

## ワークフロー

### 新規作成

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_sheets.py create \
  --name "スプレッドシート名" \
  --folder-id "フォルダID"
```

| オプション | 必須 | 説明 |
|-----------|------|------|
| `--name` | Yes | スプレッドシート名 |
| `--folder-id` | No | 保存先フォルダID |

### セル更新

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_sheets.py update \
  --sheet-id "シートID" \
  --range "A1:B2" \
  --values '[["値1","値2"],["値3","値4"]]'
```

| オプション | 必須 | 説明 |
|-----------|------|------|
| `--sheet-id` | Yes | スプレッドシートID |
| `--range` | Yes | セル範囲（例: A1, A1:B2） |
| `--values` | Yes | 値（JSON 配列形式） |

### 行追加

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_sheets.py append \
  --sheet-id "シートID" \
  --range "A1" \
  --values '[["値1","値2"]]'
```
