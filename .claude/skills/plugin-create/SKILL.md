---
name: plugin-create
description: 新しい Claude Code プラグインを作成する。「プラグイン作成」「新しいプラグイン」「プラグインを作って」「プラグイン追加」「plugin 作成」「プラグイン一括作成」「フル作成」などで起動。プラグインのみ作成と、スキル/サブエージェント/フックを含む一括作成の両方に対応。
allowed-tools: [Read, Write, Bash, Glob]
argument-hint: "[--help]"
---

# Create Plugin

必要なディレクトリ構造とファイルを持つ新しい Claude Code プラグインを作成します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/plugin-create - Create Plugin

概要:
  必要なディレクトリ構造とファイルを持つ新しい Claude Code プラグインを作成します。

使用方法:
  /plugin-create [オプション]

オプション:
  --help  このヘルプを表示
```

## ワークフロー

### 1. 情報収集

ユーザーに以下を聞く:

1. **プラグイン名**
   - 例: `common`, `react`, `code-review`
   - `shiiman-` プレフィックスは省略可（自動付与される）

2. **説明**（1-2 文）

### 2. 作成モードを確認

以下のどちらで作成するか確認する:

- **プラグインのみ**: ベース構造だけ作成
- **機能込み一括**: ベース構造作成後、スキル/サブエージェント/フックをまとめて追加

### 3. 機能込み一括の場合のみ、機能一覧を収集

モードが「機能込み一括」の場合、以下の形式で機能一覧を聞く:

```markdown
| #   | 機能     | スキル      | サブエージェント | フック      |
| --- | -------- | ----------- | ---------------- | ----------- |
| 1   | {機能名} | {名前 or -} | {名前 or -}      | {名前 or -} |
```

- 各列に名前を入力、不要なら `-`
- ファイル名にプラグイン名のプレフィックスは不要: `list` ✅ / `plugin-list` ❌

### 4. 名前の正規化と検証

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
| ---------------------- | --------------------------------------------------- |
| プレフィックス自動付与 | `common` → `shiiman-common`                         |
| 小文字のみ             | `shiiman-common` ✅ / `shiiman-Common` ❌           |
| ハイフン区切り         | `shiiman-code-review` ✅ / `shiiman_code_review` ❌ |
| コロン禁止             | `shiiman:common` ❌（コマンド区切りと競合）         |

**呼び出し形式**: `/shiiman-github:pr-create`

### 5. ベースプラグインを作成

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

### 6. plugin.json を生成

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

### 7. README.md を生成

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

### 8. marketplace.json を更新

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

### 9. 機能込み一括モードの場合、単体スキルに順次委譲

機能一覧を上から順に処理し、必要な列だけ作成する:

1. **スキル列**が `-` でなければ `skill-create` を呼び出す
2. **サブエージェント列**が `-` でなければ `subagent-create` を呼び出す
3. **フック列**が `-` でなければ `hook-create` を呼び出す

### 10. 報告

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
- /plugin-create で別のプラグインを作成
- /skill-create でスキルを追加
- /subagent-create でサブエージェントを追加
- /hook-create でフックを追加
```

## 重要な注意事項

- ✅ 作成開始時に必ずモード（プラグインのみ / 機能込み一括）を確認
- ✅ shiiman- プレフィックスを必ず付与
- ✅ 小文字・ハイフン区切りを使用
- ✅ README にインストール方法を必ず記載
- ✅ scripts は原則 `skills/{skill}/scripts/`、共通処理のみ `scripts/` を使用
- ❌ アンダースコアやキャメルケースは使用しない
- ❌ コロンは使用しない
