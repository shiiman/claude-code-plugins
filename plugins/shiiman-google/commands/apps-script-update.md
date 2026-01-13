---
name: apps-script-update
description: Google Apps Script のコードを更新する
allowed-tools: [Bash]
---

# Apps Script Update

Google Apps Script プロジェクトのコードを更新します。

## 引数

- `$ARGUMENTS` (必須): スクリプトID

## オプション

- `--filename <name>` (必須): ファイル名（例: Code.gs, Utils.gs）
- `--code <code>` (必須): ソースコード

## 実行

```bash
python plugins/shiiman-google/skills/apps-script-list/scripts/google_apps_script.py update --script-id "$ARGUMENTS" --filename "$FILENAME" --code "$CODE"
```

## 使用例

```
/shiiman-google:apps-script-update 1abc --filename "Code.gs" --code "function myFunc() { Logger.log('Hello'); }"
```
