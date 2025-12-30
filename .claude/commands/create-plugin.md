# Create Plugin

新しい Claude Code プラグインを必要な構造で作成します。

## 使い方

```bash
/create-plugin
/create-plugin --help
```

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--help`   | このコマンドのヘルプを表示 |

## 実行例

```bash
# 基本的な使用
/create-plugin
→ プラグイン名: common
→ 説明: 汎用ユーティリティコマンドを提供

# 結果: plugins/shiiman-common/ が作成される
```

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### ステップ 1: 情報収集

ユーザーに以下を聞く:

1. **プラグイン名**
   - 例: `common`, `react`, `code-review`
   - `shiiman-` プレフィックスは省略可（自動付与される）

2. **説明**（1-2 文）

### ステップ 2: 名前の正規化と検証

1. **プレフィックス自動付与**
   - ユーザー入力が `shiiman-` で始まっていなければ自動で付与
   - 例: `common` → `shiiman-common`
   - 例: `shiiman-react` → `shiiman-react`（そのまま）

2. **検証**
   - 小文字、ハイフンのみかチェック（アンダースコア、コロン禁止）
   - `plugins/` ディレクトリに既存のプラグインがないか確認

### 命名規則

**重要**: 他のマーケットプレイスとの競合を避けるため、プラグイン名には必ず `shiiman-` プレフィックスを付ける。

| ルール                 | 例                                                  |
|------------------------|-----------------------------------------------------|
| プレフィックス自動付与 | `common` → `shiiman-common`                         |
| 小文字のみ             | `shiiman-common` ✅ / `shiiman-Common` ❌           |
| ハイフン区切り         | `shiiman-code-review` ✅ / `shiiman_code_review` ❌ |
| コロン禁止             | `shiiman:common` ❌（コマンド区切りと競合）         |

**呼び出し形式**: `/shiiman-common:commit`

### ステップ 3: 構造を作成

以下のファイルを作成:

```text
plugins/{plugin-name}/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── .gitkeep
├── skills/
│   └── .gitkeep
├── agents/
│   └── .gitkeep
├── hooks/
│   └── .gitkeep
└── README.md
```

### ステップ 4: plugin.json を生成

```json
{
  "name": "{plugin-name}",
  "version": "1.0.0",
  "description": "{説明}",
  "author": {
    "name": "shiiman"
  }
}
```

### ステップ 5: README.md を生成

**重要**: README には必ずインストール方法を含める。

````markdown
# {plugin-name}

{説明}

## インストール

```bash
# マーケットプレイスを追加（初回のみ）
/plugin marketplace add shiiman/claude-code-plugins

# プラグインをインストール
/plugin install {plugin-name}@shiiman-claude-code-plugins
```

## コマンド

（まだありません）

## スキル

（まだありません）

## ライセンス

MIT
````

### ステップ 6: marketplace.json を更新

`.claude-plugin/marketplace.json` の plugins 配列に追加:

```json
{
  "name": "{plugin-name}",
  "description": "{説明}",
  "version": "1.0.0",
  "author": { "name": "shiiman" },
  "source": "./plugins/{plugin-name}",
  "category": "development"
}
```

### ステップ 7: 報告

作成されたファイルと次のステップを表示:

```text
プラグインを作成しました: {plugin-name}

ファイル:
- plugins/{plugin-name}/.claude-plugin/plugin.json
- plugins/{plugin-name}/README.md
- plugins/{plugin-name}/commands/.gitkeep
- plugins/{plugin-name}/skills/.gitkeep
- plugins/{plugin-name}/agents/.gitkeep
- plugins/{plugin-name}/hooks/.gitkeep

更新:
- .claude-plugin/marketplace.json

次のステップ:
- /create-command でコマンドを追加
- /create-skill でスキルを追加
- /create-subagent でサブエージェントを追加
- /create-hook でフックを追加
```
