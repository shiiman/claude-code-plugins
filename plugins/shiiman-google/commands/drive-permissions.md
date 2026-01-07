---
name: drive-permissions
description: Google Drive のファイルの共有設定を確認する
allowed-tools: [Bash]
---

# Drive Permissions

Google Drive のファイルの共有設定を確認します。

## 引数

- `$ARGUMENTS` (必須): ファイルID

## 実行

```bash
python plugins/shiiman-google/scripts/google_drive.py permissions --file-id "$ARGUMENTS"
```

## 使用例

```
/shiiman-google:drive-permissions 1abc...xyz
```
