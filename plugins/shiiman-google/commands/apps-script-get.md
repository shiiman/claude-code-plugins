---
name: apps-script-get
description: Google Apps Script プロジェクトの内容を取得する
allowed-tools: [Bash]
---

# Apps Script Get

Google Apps Script プロジェクトの内容を取得します。

## 引数

- `$ARGUMENTS` (必須): スクリプトID

## 実行

```bash
python plugins/shiiman-google/scripts/google_apps_script.py get --script-id "$ARGUMENTS"
```

## 使用例

```
/shiiman-google:apps-script-get 1abc...xyz
```
