# コマンド作成ガイド

## 概要

コマンドは Markdown ファイルとして定義されるスラッシュコマンド（例: `/my-command`）です。

## 配置場所

```text
plugins/{plugin-name}/commands/{command-name}.md
```

## ファイル形式

```markdown
## コマンド名

このコマンドの説明。

### 使い方

/command-name [オプション]

### 例

/command-name --option value

### Claude への指示

このコマンドが呼び出されたときに Claude が実行する手順。
```

## 命名規則

- 小文字とハイフンを使用: `my-command.md`
- コマンド名はファイル名から（`.md` を除く）

## 例

ファイル: `plugins/common/commands/hello.md`

```markdown
## Hello

ユーザーに挨拶します。

### 使い方

/hello [名前]

### Claude への指示

1. 名前が指定されていれば「こんにちは、{名前}さん！」と挨拶
2. そうでなければ「こんにちは！」と挨拶
```
