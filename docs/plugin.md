# プラグイン作成ガイド

## 構造

```text
plugins/{plugin-name}/
├── .claude-plugin/
│   └── plugin.json       # 必須: プラグインメタデータ
├── skills/               # スキル定義
├── agents/               # エージェント定義
├── hooks/                # フック設定
├── scripts/              # オプション: plugin 全体で共有する実行スクリプト
└── README.md             # プラグイン説明
```

## scripts パス規約

plugin 内の scripts は、Skill 固有か共通処理かで配置先を分けます。

- 標準配置（Skill 固有）: `plugins/{plugin-name}/skills/{skill-name}/scripts/{script-file}`
- 標準呼び出し: `${CLAUDE_PLUGIN_ROOT}/skills/{skill-name}/scripts/{script-file}`
- 共通配置（複数 Skill で再利用）: `plugins/{plugin-name}/scripts/{script-file}`
- 共通呼び出し: `${CLAUDE_PLUGIN_ROOT}/scripts/{script-file}`
- 共通化の運用基準: 2 つ以上の `SKILL.md` から参照される script を plugin ルートへ配置

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/example-skill/scripts/example.py"
bash "${CLAUDE_PLUGIN_ROOT}/scripts/example.sh"
python "${CLAUDE_PLUGIN_ROOT}/scripts/example.py"
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
  "source": "./plugins/plugin-name",
  "category": "development"
}
```

## プラグインの更新手順

プラグインを更新する際は、以下の手順に従ってください。

### 1. plugin.json のバージョン更新

`plugins/{plugin-name}/.claude-plugin/plugin.json` の `version` フィールドを更新します。

**バージョニングルール**（[Semantic Versioning](https://semver.org/) に準拠）:

| 変更内容 | バージョンアップ | 例 |
|---------|----------------|-----|
| 破壊的変更 | MAJOR | 1.0.0 → 2.0.0 |
| 新機能追加（後方互換） | MINOR | 1.0.0 → 1.1.0 |
| バグ修正（後方互換） | PATCH | 1.0.0 → 1.0.1 |

**更新例**:

```json
{
  "name": "plugin-name",
  "version": "1.1.0",  // 1.0.0 から更新
  "description": "プラグインの説明",
  "author": {
    "name": "shiiman"
  }
}
```

### 2. README.md の更新

`plugins/{plugin-name}/README.md` を更新します（必要に応じて）。

- 新機能の説明を追加
- 変更履歴を追記
- 使い方の更新

### 3. marketplace.json のバージョン更新

`.claude-plugin/marketplace.json` の該当プラグインエントリの `version` フィールドを更新します。

**重要**: `plugin.json` のバージョンと `marketplace.json` のバージョンは一致させる必要があります。

**更新例**:

```json
{
  "name": "plugin-name",
  "description": "プラグインの説明",
  "version": "1.1.0",  // 1.0.0 から更新（plugin.json と一致させる）
  "source": "./plugins/plugin-name",
  "category": "development"
}
```

### 更新手順のまとめ

1. ✅ `plugins/{plugin-name}/.claude-plugin/plugin.json` の `version` を更新
2. ✅ `plugins/{plugin-name}/README.md` を更新（必要に応じて）
3. ✅ `.claude-plugin/marketplace.json` の該当エントリの `version` を更新（plugin.json と一致させる）

## 命名規則

**重要**: 他のマーケットプレイスとの競合を避けるため、プラグイン名には必ず `shiiman-` プレフィックスを付ける。

| ルール | 例 |
|--------|-----|
| プレフィックス必須 | `shiiman-` |
| 小文字のみ | `shiiman-common` ✅ / `shiiman-Common` ❌ |
| ハイフン区切り | `shiiman-code-review` ✅ / `shiiman_code_review` ❌ |
| コロン禁止 | `shiiman:common` ❌（コマンド区切りと競合） |
| 簡潔な名前 | `shiiman-plugin` ✅ / `shiiman-plugin-manager` ❌ |

**呼び出し形式**: `/shiiman-common:commit`

### 良い命名の例

```bash
# ✅ 良い例: 簡潔で分かりやすい
shiiman-plugin      # プラグイン管理
shiiman-git         # Git 操作
shiiman-react       # React 開発

# ❌ 悪い例: 冗長
shiiman-plugin-manager
shiiman-git-operations
shiiman-react-development-tools
```

## プラグイン管理コマンド

Claude Code CLI でプラグインを管理できます：

```bash
claude plugin install <plugin>    # インストール（plugin@marketplace 形式も可）
claude plugin uninstall <plugin>  # アンインストール
claude plugin enable <plugin>     # 有効化
claude plugin disable <plugin>    # 無効化
claude plugin update <plugin>     # アップデート
```
