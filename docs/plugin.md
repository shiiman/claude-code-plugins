# プラグイン作成ガイド

## 構造

```text
plugins/{plugin-name}/
├── .claude-plugin/
│   └── plugin.json       # 必須: プラグインメタデータ
├── commands/             # スラッシュコマンド (.md)
├── skills/               # スキル定義
├── agents/               # エージェント定義
├── hooks/                # フック設定
└── README.md             # プラグイン説明
```

## plugin.json

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "プラグインの説明",
  "author": {
    "name": "shiiman"
  }
}
```

## marketplace.json への登録

`.claude-plugin/marketplace.json` に追加:

```json
{
  "name": "plugin-name",
  "description": "プラグインの説明",
  "version": "1.0.0",
  "author": { "name": "shiiman" },
  "source": "./plugins/plugin-name",
  "category": "development"
}
```

## 命名規則

**重要**: 他のマーケットプレイスとの競合を避けるため、プラグイン名には必ず `shiiman-` プレフィックスを付ける。

| ルール | 例 |
|--------|-----|
| プレフィックス必須 | `shiiman-` |
| 小文字のみ | `shiiman-common` ✅ / `shiiman-Common` ❌ |
| ハイフン区切り | `shiiman-code-review` ✅ / `shiiman_code_review` ❌ |
| コロン禁止 | `shiiman:common` ❌（コマンド区切りと競合） |

**呼び出し形式**: `/shiiman-common:commit`
