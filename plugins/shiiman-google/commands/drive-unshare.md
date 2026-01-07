---
name: drive-unshare
description: Google Drive のファイルの共有を解除する
allowed-tools: [Bash]
---

# Drive Unshare

Google Drive のファイルの共有を解除します。

## 引数

- `$ARGUMENTS` (必須): ファイルID

## オプション

- `--email <address>`: 共有解除するメールアドレス
- `--permission-id <id>`: パーミッションID（email より優先）

## 実行

```bash
python plugins/shiiman-google/scripts/google_drive.py unshare --file-id "$ARGUMENTS" ${EMAIL:+--email "$EMAIL"} ${PERMISSION_ID:+--permission-id "$PERMISSION_ID"}
```

## 使用例

```
/shiiman-google:drive-unshare 1abc...xyz --email user@example.com
/shiiman-google:drive-unshare 1abc...xyz --permission-id anyoneWithLink
```
