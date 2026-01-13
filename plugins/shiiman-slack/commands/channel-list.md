---
name: channel-list
description: Slack チャンネル一覧を取得する
allowed-tools: [FetchMcpResource]
---

# Channel List

Slack チャンネル一覧を取得します。

## 引数

なし

## オプション

なし（公式MCPのデフォルト動作）

## 実行

公式Slack MCPの `slack_list_channels` ツールを使用:

```
slack_list_channels()
```

## 使用例

```
/shiiman-slack:channel-list
```

## 出力

チャンネル一覧（ID、名前、トピック、メンバー数など）
