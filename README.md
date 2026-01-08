# shiiman-claude-code-plugins

個人用 Claude Code プラグインマーケットプレイス。

## インストール

### 方法 1: プロジェクト設定（推奨）

プロジェクトの `.claude/settings.json` にマーケットプレイスを設定すると、プロジェクトを開くたびに自動的にプラグインを利用できるようになります。

```json
{
  "extraKnownMarketplaces": {
    "shiiman-claude-code-plugins": {
      "source": {
        "source": "git",
        "url": "git@github.com:shiiman/claude-code-plugins.git"
      }
    }
  },
  "enabledPlugins": {
    "shiiman-plugin@shiiman-claude-code-plugins": true,
    "shiiman-claude@shiiman-claude-code-plugins": true,
    "shiiman-git@shiiman-claude-code-plugins": true,
    "shiiman-google@shiiman-claude-code-plugins": true,
    "shiiman-go@shiiman-claude-code-plugins": true,
    "shiiman-docker@shiiman-claude-code-plugins": true
  }
}
```

**メリット**:

- プロジェクトを開くと自動的にインストール
- プラグインのバージョン管理が容易
- 設定を共有して同じプラグイン環境を維持

### 方法 2: 個別インストール

#### 1. マーケットプレイスを追加

```bash
/plugin marketplace add shiiman/claude-code-plugins
```

#### 2. プラグインをインストール

| プラグイン | 説明 | インストールコマンド |
| ---------- | ---- | -------------------- |
| [`shiiman-plugin`](plugins/shiiman-plugin/) | プラグイン管理用プラグイン - 一覧表示、詳細表示、インストール、アンインストール、有効化、無効化、アップデート機能を提供 | `/plugin install shiiman-plugin@shiiman-claude-code-plugins` |
| [`shiiman-claude`](plugins/shiiman-claude/) | Claude Code プロジェクト設定管理プラグイン - コマンド/スキル/エージェント/フックの追加、設定更新、ドキュメント更新、モデル切り替え、コンテキスト管理機能を提供 | `/plugin install shiiman-claude@shiiman-claude-code-plugins` |
| [`shiiman-git`](plugins/shiiman-git/) | Git/GitHub ワークフロー管理 - セットアップ、コミット、Issue、PR、Actions 管理機能を提供 | `/plugin install shiiman-git@shiiman-claude-code-plugins` |
| [`shiiman-google`](plugins/shiiman-google/) | Google Workspace 操作 - 認証、Drive/Docs/Sheets/Slides/Forms/Apps Script、Calendar、Gmail 機能を提供 | `/plugin install shiiman-google@shiiman-claude-code-plugins` |
| [`shiiman-go`](plugins/shiiman-go/) | Go 言語開発支援 - フォーマット、静的解析、テスト、依存関係管理、ビルド、パフォーマンス計測、脆弱性スキャン | `/plugin install shiiman-go@shiiman-claude-code-plugins` |
| [`shiiman-docker`](plugins/shiiman-docker/) | Docker/Docker Compose 管理 - コンテナ、イメージ、ネットワーク、ボリューム、Dockerfile の操作を支援 | `/plugin install shiiman-docker@shiiman-claude-code-plugins` |

**インストール例**:

```bash
# すべてのプラグインをインストール
/plugin install shiiman-plugin@shiiman-claude-code-plugins
/plugin install shiiman-claude@shiiman-claude-code-plugins
/plugin install shiiman-git@shiiman-claude-code-plugins
/plugin install shiiman-google@shiiman-claude-code-plugins
/plugin install shiiman-go@shiiman-claude-code-plugins
/plugin install shiiman-docker@shiiman-claude-code-plugins
```

## 構造

```text
.
├── .claude-plugin/
│   └── marketplace.json    # マーケットプレイス定義
├── .claude/
│   ├── commands/           # リポジトリ用コマンド
│   └── skills/             # リポジトリ用スキル
├── plugins/                # プラグインディレクトリ
├── docs/                   # ドキュメント
└── README.md
```

## 利用可能なコマンド

| コマンド | 説明 |
|----------|------|
| `/create-plugin` | 新しいプラグインを作成 |
| `/create-command` | プラグインにコマンドを追加 |
| `/create-skill` | プラグインにスキルを追加 |
| `/create-subagent` | プラグインにサブエージェントを追加 |
| `/create-hook` | プラグインにフックを追加 |

## 利用可能なスキル

自然言語で呼び出せるスキル:

| スキル           | トリガー例                                   | 説明                               |
|------------------|----------------------------------------------|------------------------------------|
| plugin-creator   | 「プラグイン作成」「新しいプラグイン」       | 新しいプラグインを作成             |
| command-creator  | 「コマンド作成」「新しいコマンド」           | プラグインにコマンドを追加         |
| skill-creator    | 「スキル作成」「新しいスキル」               | プラグインにスキルを追加           |
| subagent-creator | 「サブエージェント作成」「エージェント作成」 | プラグインにサブエージェントを追加 |
| hook-creator     | 「フック作成」「新しいフック」               | プラグインにフックを追加           |
| issue-creator    | 「Issue 作成」「Issue を作って」             | 計画から複数の Issue を作成        |
| pr-creator       | 「PR 作成」「PR を作って」                   | PR を作成し Issue をクローズ       |

## ドキュメント

- [docs/plugin.md](docs/plugin.md) - プラグイン作成ガイド
- [docs/command.md](docs/command.md) - コマンド作成ガイド
- [docs/skill.md](docs/skill.md) - スキル作成ガイド
- [docs/subagent.md](docs/subagent.md) - サブエージェント作成ガイド
- [docs/hook.md](docs/hook.md) - フック作成ガイド

## プラグインの追加

`plugins/` 配下に以下の構造でディレクトリを作成:

```text
plugins/my-plugin/
├── .claude-plugin/
│   └── plugin.json         # プラグインメタデータ
├── commands/               # スラッシュコマンド
├── skills/                 # スキル定義
├── agents/                 # サブエージェント定義
├── hooks/                  # フック設定
└── README.md
```

その後 `.claude-plugin/marketplace.json` にエントリを追加:

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin",
  "description": "プラグインの説明",
  "version": "1.0.0",
  "author": { "name": "shiiman" },
  "category": "development"
}
```

## プラグインの更新

プラグインを更新する際は、以下のファイルを更新してください:

1. `plugins/{plugin-name}/.claude-plugin/plugin.json` - バージョンを更新
2. `plugins/{plugin-name}/README.md` - 必要に応じて更新
3. `.claude-plugin/marketplace.json` - 該当エントリのバージョンを更新（plugin.json と一致させる）

詳細な手順は [docs/plugin.md](docs/plugin.md) の「プラグインの更新手順」を参照してください。
