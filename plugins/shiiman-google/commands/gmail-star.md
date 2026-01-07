# Gmail Star

Gmail のメッセージをスター化/解除します。

## 使い方

```bash
/shiiman-google:gmail-star <message-id>
/shiiman-google:gmail-star --remove <message-id>
/shiiman-google:gmail-star --help
```

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--remove` | スターを解除               |
| `--help`   | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### 実行手順

1. `message-id` と `--remove` を判定
2. `~/.config/shiiman-google/active-profile` を読み取り、使用プロファイルを特定
3. トークン未作成なら `/shiiman-google:auth-login` を案内
4. `plugins/shiiman-google/scripts/google_gmail.py` を実行してスター化/解除
5. 完了メッセージを出力

### 実行例

```bash
python plugins/shiiman-google/scripts/google_gmail.py \
  --token ~/.config/shiiman-google/tokens/{profile}.json \
  star --ids <message-id>
```
