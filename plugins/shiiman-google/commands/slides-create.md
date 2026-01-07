---
name: slides-create
description: Google Slides プレゼンテーションを新規作成する
allowed-tools: [Bash]
---

# Slides Create

Google Slides プレゼンテーションを新規作成します。

## 引数

- `$ARGUMENTS` (必須): プレゼンテーション名

## オプション

- `--folder-id <id>`: 作成先フォルダID

## 実行

```bash
python plugins/shiiman-google/scripts/google_slides.py create --name "$ARGUMENTS" ${FOLDER_ID:+--folder-id "$FOLDER_ID"}
```

## 使用例

```
/shiiman-google:slides-create 新規提案資料
/shiiman-google:slides-create プロジェクト報告 --folder-id xxx
```
