---
name: channel-search
description: チャンネルを名前で検索する
allowed-tools: [Bash]
---

# Channel Search

チャンネルを名前で検索します。

## 引数

- `$QUERY` (必須): 検索クエリ（チャンネル名の一部）

## オプション

- `--format <table|json>`: 出力形式（デフォルト: table）

## 実行

```bash
python plugins/shiiman-slack/skills/channel-lister/scripts/slack_channel.py search \
  --query "$QUERY" \
  ${FORMAT:+--format "$FORMAT"}
```

## 使用例

```
/shiiman-slack:channel-search project
/shiiman-slack:channel-search "team-" --format json
```

## 出力

検索結果のチャンネル一覧（ID、名前、プライベート/パブリック、トピック、メンバー数）

## 必要な環境変数

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
```

## 必要なスコープ

- `channels:read`
- `groups:read`

## 検索の仕様

- チャンネル名の部分一致で検索
- パブリックチャンネルとプライベートチャンネルの両方を検索
- 大文字小文字を区別しない
