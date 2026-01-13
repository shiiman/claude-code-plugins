---
name: user-profile
description: Slack ユーザープロファイルを取得する
allowed-tools: [FetchMcpResource]
---

# User Profile

Slack ユーザーのプロファイル情報を取得します。

## 引数

- `$USER_ID` (必須): ユーザーID（例: U01234567）

## オプション

なし

## 実行

公式Slack MCPの `slack_get_user_profile` ツールを使用:

```
slack_get_user_profile(
  user_id="$USER_ID"
)
```

## 使用例

```
/shiiman-slack:user-profile U01234567
```

## 出力

ユーザープロファイル情報:
- 名前（real_name, display_name）
- メールアドレス
- タイトル
- ステータステキスト・絵文字
- その他プロファイル情報

## 注意

このコマンドは読み取り専用です。プロファイル情報の変更はできません。
