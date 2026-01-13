# Drive List

Google Drive のファイル一覧を取得します。

## 使い方

```bash
/shiiman-google:drive-list
/shiiman-google:drive-list --help
```

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--help`   | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### 実行手順

1. `~/.config/shiiman-google/active-profile` を読み取り、使用プロファイルを特定
2. トークン未作成なら `/shiiman-google:auth-login` を案内
3. `plugins/shiiman-google/skills/drive-list/scripts/google_drive.py` を実行して一覧を取得
4. 表形式で出力（名前、種類、更新日時、URL）

### 実行例

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py \
  --token ~/.config/shiiman-google/tokens/{profile}.json
```
