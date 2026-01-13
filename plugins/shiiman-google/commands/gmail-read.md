# Gmail Read

Gmail メッセージ本文を表示します。

## 使い方

```bash
/shiiman-google:gmail-read <message-id>
/shiiman-google:gmail-read --help
```

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--help`   | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### 実行手順

1. `message-id` を受け取る
2. `~/.config/shiiman-google/active-profile` を読み取り、使用プロファイルを特定
3. トークン未作成なら `/shiiman-google:auth-login` を案内
4. `plugins/shiiman-google/skills/gmail-unread/scripts/google_gmail.py` を実行して本文を取得

### 実行例

```bash
python plugins/shiiman-google/skills/gmail-unread/scripts/google_gmail.py \
  --token ~/.config/shiiman-google/tokens/{profile}.json \
  read --id <message-id>
```
