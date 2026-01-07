# Gmail Mark Read

Gmail の未読メッセージを既読化します（単体/一括）。

## 使い方

```bash
/shiiman-google:gmail-mark-read <message-id>
/shiiman-google:gmail-mark-read --all
/shiiman-google:gmail-mark-read --help
```

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--all`    | 未読を一括で既読化         |
| `--help`   | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### 実行手順

1. `message-id` か `--all` を判定
2. `~/.config/shiiman-google/active-profile` を読み取り、使用プロファイルを特定
3. トークン未作成なら `/shiiman-google:auth-login` を案内
4. `plugins/shiiman-google/scripts/google_gmail.py` を実行して既読化
5. 完了メッセージを出力

### 実行例

```bash
python plugins/shiiman-google/scripts/google_gmail.py \
  --token ~/.config/shiiman-google/tokens/{profile}.json \
  mark-read --all
```
