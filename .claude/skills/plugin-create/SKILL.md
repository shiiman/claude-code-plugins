---
name: plugin-create
description: 新しい Claude Code プラグインを作成する。「プラグイン作成」「新しいプラグイン」「プラグインを作って」「プラグイン追加」「plugin 作成」「プラグインを追加したい」「新規プラグイン」などで起動。必要なディレクトリ構造とファイルを持つプラグインを生成。
allowed-tools: [Read, Write, Bash, Glob]
---

# Create Plugin

必要なディレクトリ構造とファイルを持つ新しい Claude Code プラグインを作成します。

## ワークフロー

### 1. 情報収集

ユーザーに以下を聞く:

1. **プラグイン名**
   - 例: `common`, `react`, `code-review`
   - `shiiman-` プレフィックスは省略可（自動付与される）

2. **説明**（1-2 文）

### 2. 名前の正規化と検証

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

### 3. 構造を作成

以下のファイルを作成:

```text
plugins/{plugin-name}/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── .gitkeep
├── agents/
│   └── .gitkeep
├── hooks/
│   └── .gitkeep
├── scripts/
│   └── .gitkeep
└── README.md
```

**scripts パス規約**:

- 標準: Skill 固有 script は `plugins/{plugin-name}/skills/{skill-name}/scripts/` に配置
- 標準参照: `${CLAUDE_PLUGIN_ROOT}/skills/{skill-name}/scripts/{script-file}`
- 共通処理のみ `plugins/{plugin-name}/scripts/` に配置
- 共通参照: `${CLAUDE_PLUGIN_ROOT}/scripts/{script-file}`
- 共通化基準（運用）: 2 つ以上の `SKILL.md` から参照される script を plugin ルートへ配置

### 4. plugin.json を生成

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

### 5. README.md を生成

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

## スキル

（まだありません）

## ライセンス

MIT
````

### 6. marketplace.json を更新

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

### 7. 報告

作成されたファイルと次のステップを表示:

```text
プラグインを作成しました: {plugin-name}

ファイル:
- plugins/{plugin-name}/.claude-plugin/plugin.json
- plugins/{plugin-name}/README.md
- plugins/{plugin-name}/skills/.gitkeep
- plugins/{plugin-name}/agents/.gitkeep
- plugins/{plugin-name}/hooks/.gitkeep
- plugins/{plugin-name}/scripts/.gitkeep

更新:
- .claude-plugin/marketplace.json

次のステップ:
- /create-skill でスキルを追加
- /create-subagent でサブエージェントを追加
- /create-hook でフックを追加
```

## 重要な注意事項

- ✅ shiiman- プレフィックスを必ず付与
- ✅ 小文字・ハイフン区切りを使用
- ✅ README にインストール方法を必ず記載
- ✅ scripts は原則 `skills/{skill}/scripts/`、共通処理のみ `scripts/` を使用
- ❌ アンダースコアやキャメルケースは使用しない
- ❌ コロンは使用しない
