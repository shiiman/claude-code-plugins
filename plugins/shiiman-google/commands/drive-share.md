---
name: drive-share
description: Google Drive のファイルを共有する
allowed-tools: [Bash]
---

# Drive Share

Google Drive のファイルを共有します。

## 引数

- `$ARGUMENTS` (必須): ファイルID

## オプション

- `--email <address>`: 共有先メールアドレス（user/group タイプの場合必須）
- `--role <role>`: 権限（reader=閲覧, writer=編集, commenter=コメント）デフォルト: reader
- `--type <type>`: 共有タイプ（user=個人, group=グループ, anyone=リンク共有）デフォルト: user
- `--no-notify`: 共有通知メールを送信しない

## 実行

```bash
python plugins/shiiman-google/scripts/google_drive.py share --file-id "$ARGUMENTS" ${EMAIL:+--email "$EMAIL"} ${ROLE:+--role "$ROLE"} ${TYPE:+--type "$TYPE"} ${NO_NOTIFY:+--no-notify}
```

## 使用例

```
/shiiman-google:drive-share 1abc...xyz --email user@example.com --role writer
/shiiman-google:drive-share 1abc...xyz --type anyone --role reader
```
