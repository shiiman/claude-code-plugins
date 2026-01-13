# Forms Search

Google Forms を検索します。

## 使い方

```bash
/shiiman-google:forms-search <query>
/shiiman-google:forms-search --help
```

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--help`   | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### 実行手順

1. `query` を受け取る（例: `name contains 'spec'`）
2. `~/.config/shiiman-google/active-profile` を読み取り、使用プロファイルを特定
3. トークン未作成なら `/shiiman-google:auth-login` を案内
4. Drive API で Forms のみに絞って検索
5. 表形式で出力

### 実行例

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py \
  --token ~/.config/shiiman-google/tokens/{profile}.json \
  --query "mimeType='application/vnd.google-apps.form' and name contains 'spec'"
```
