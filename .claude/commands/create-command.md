# Create Command

プラグインに新しいスラッシュコマンドを作成します。

## 使い方

```bash
/create-command
```

## Claude への指示

### ステップ 1: 情報収集

ユーザーに以下を聞く:

1. **対象プラグイン** - どのプラグインにコマンドを追加するか
   - `plugins/` ディレクトリから既存プラグインを一覧表示

2. **コマンド名**（小文字、ハイフン可）
   - 例: `lint`, `format-code`

3. **説明**（1文）

4. **このコマンドで何をする？**（詳細な指示）

### ステップ 2: 検証

- コマンド名の形式をチェック
- プラグインが存在するか確認
- コマンドが既に存在しないか確認

### ステップ 3: コマンドファイルを作成

`plugins/{plugin-name}/commands/{command-name}.md` を作成:

```markdown
# {コマンド名}

{説明}

## 使い方

/{command-name} [オプション]

## Claude への指示

{ユーザーからの詳細な指示}
```

### ステップ 4: プラグイン README を更新

`plugins/{plugin-name}/README.md` のコマンドセクションにコマンドを追加。

### ステップ 5: 報告

作成されたファイルと次のステップを表示:

```text
コマンドを作成しました: /{command-name}

ファイル:
- plugins/{plugin-name}/commands/{command-name}.md

更新:
- plugins/{plugin-name}/README.md

次のステップ:
- /create-command で別のコマンドを追加
- /create-skill でスキルを追加
- /create-subagent でサブエージェントを追加
- /create-hook でフックを追加
```
