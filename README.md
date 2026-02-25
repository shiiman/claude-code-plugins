# shiiman-claude-code-plugins

個人用 Claude Code プラグインマーケットプレイス。

## 前提条件

- Python 3.10 以上
- Node.js（Prettier 用）
- 依存パッケージのインストール:

```bash
pip install -r requirements.txt
npm install
```

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
    "shiiman-claude@shiiman-claude-code-plugins": true,
    "shiiman-git@shiiman-claude-code-plugins": true,
    "shiiman-github@shiiman-claude-code-plugins": true,
    "shiiman-workflow@shiiman-claude-code-plugins": true,
    "shiiman-google@shiiman-claude-code-plugins": true,
    "shiiman-go@shiiman-claude-code-plugins": true,
    "shiiman-terraform@shiiman-claude-code-plugins": true,
    "shiiman-slack@shiiman-claude-code-plugins": true
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

| プラグイン                                        | 説明                                                                                                                                | インストールコマンド                                            |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [`shiiman-claude`](plugins/shiiman-claude/)       | Claude Code プロジェクト設定管理プラグイン - MCP サーバー管理、Claude 設定管理、Claude リソース一覧表示、Claude Code CLI 更新を提供 | `/plugin install shiiman-claude@shiiman-claude-code-plugins`    |
| [`shiiman-git`](plugins/shiiman-git/)             | Git ローカル操作 - コミット、worktree、gitignore チェック、コミットメッセージ設定、gtrconfig 生成を提供                             | `/plugin install shiiman-git@shiiman-claude-code-plugins`       |
| [`shiiman-github`](plugins/shiiman-github/)       | GitHub API / gh CLI 操作 - Issue、PR、ブランチ、GitHub Actions、リポジトリ設定管理を提供                                            | `/plugin install shiiman-github@shiiman-claude-code-plugins`    |
| [`shiiman-workflow`](plugins/shiiman-workflow/)   | 開発ワークフロー自動化 - シングル/マルチエージェント/Agent Team での Issue 管理付き・なしのフローを提供                             | `/plugin install shiiman-workflow@shiiman-claude-code-plugins`  |
| [`shiiman-google`](plugins/shiiman-google/)       | Google Workspace 操作 - 認証、Drive 検索、Docs/Sheets/Slides/Forms/Apps Script 編集、Calendar、Gmail 未読管理を提供                 | `/plugin install shiiman-google@shiiman-claude-code-plugins`    |
| [`shiiman-go`](plugins/shiiman-go/)               | Go 言語開発支援 - フォーマット、静的解析、テスト、依存関係管理、ビルド、パフォーマンス計測、脆弱性スキャン                          | `/plugin install shiiman-go@shiiman-claude-code-plugins`        |
| [`shiiman-terraform`](plugins/shiiman-terraform/) | Terraform/Terragrunt 管理 - コマンド実行、バージョン管理、モジュール管理、state 操作、import 支援、セキュリティ監査                 | `/plugin install shiiman-terraform@shiiman-claude-code-plugins` |
| [`shiiman-slack`](plugins/shiiman-slack/)         | Slack 通知管理 - 未読確認、既読化、メンション確認・返信、プロフィール更新を提供                                                     | `/plugin install shiiman-slack@shiiman-claude-code-plugins`     |

**インストール例**:

```bash
# すべてのプラグインをインストール
/plugin install shiiman-claude@shiiman-claude-code-plugins
/plugin install shiiman-git@shiiman-claude-code-plugins
/plugin install shiiman-github@shiiman-claude-code-plugins
/plugin install shiiman-workflow@shiiman-claude-code-plugins
/plugin install shiiman-google@shiiman-claude-code-plugins
/plugin install shiiman-go@shiiman-claude-code-plugins
/plugin install shiiman-terraform@shiiman-claude-code-plugins
/plugin install shiiman-slack@shiiman-claude-code-plugins
```

## 構造

```text
.
├── .claude-plugin/
│   └── marketplace.json    # マーケットプレイス定義
├── .claude/
│   └── skills/             # リポジトリ用スキル
├── plugins/                # プラグインディレクトリ
├── docs/                   # ドキュメント
└── README.md
```

## 利用可能なコマンド

| コマンド              | 説明                                                    |
| --------------------- | ------------------------------------------------------- |
| `/plugin-create`      | 新しいプラグインを作成（プラグインのみ / 機能込み一括） |
| `/skill-create`       | プラグインにスキルを追加                                |
| `/subagent-create`    | プラグインにサブエージェントを追加                      |
| `/hook-create`        | プラグインにフックを追加                                |
| `/marketplace-toggle` | マーケットプレイスを dev（symlink）/ prd（git）に切替   |

## 利用可能なスキル

自然言語で呼び出せるスキル:

### プラグイン管理

| スキル          | プラグイン | トリガー例                                   | 説明                                                    |
| --------------- | ---------- | -------------------------------------------- | ------------------------------------------------------- |
| plugin-create   | -          | 「プラグイン作成」「プラグイン一括作成」     | 新しいプラグインを作成（プラグインのみ / 機能込み一括） |
| skill-create    | -          | 「スキル作成」「新しいスキル」               | プラグインにスキルを追加                                |
| subagent-create | -          | 「サブエージェント作成」「エージェント作成」 | プラグインにサブエージェントを追加                      |
| hook-create     | -          | 「フック作成」「新しいフック」               | プラグインにフックを追加                                |

### ワークフロー

| スキル                    | プラグイン       | トリガー例                                              | 説明                                                             |
| ------------------------- | ---------------- | ------------------------------------------------------- | ---------------------------------------------------------------- |
| workflow-single-issue     | shiiman-workflow | 「シングル Issue フロー」「Issue から PR まで」         | Issue 作成から PR 作成まで自動実行するシングルエージェントフロー |
| workflow-multi-issue      | shiiman-workflow | 「マルチ Issue フロー」「並列 Issue 開発」              | MCP マルチエージェントで Issue から PR まで並列実行              |
| workflow-single           | shiiman-workflow | 「シングルフロー」「軽量フロー」                        | Issue/PR なしで計画書からタスク実行する軽量フロー                |
| workflow-multi            | shiiman-workflow | 「マルチフロー」「並列軽量フロー」                      | MCP マルチエージェントで Issue/PR なしに並列実行する軽量フロー   |
| workflow-agent-team-issue | shiiman-workflow | 「Agent Team Issue」「エージェントチーム Issue フロー」 | Agent Team で Issue から PR まで並列実行                         |
| workflow-agent-team       | shiiman-workflow | 「エージェントチームフロー」「Agent Team で実装」       | Agent Team で Issue/PR なしに並列実行する軽量フロー              |

### 開発ツール

| スキル             | プラグイン | トリガー例                               | 説明                                                      |
| ------------------ | ---------- | ---------------------------------------- | --------------------------------------------------------- |
| marketplace-toggle | -          | 「マーケットプレイス切替」「dev モード」 | installLocation を symlink（dev）/ git clone（prd）に切替 |

**dev モード**: `installLocation` をプロジェクトディレクトリへの symlink に差し替え。ローカルのプラグイン変更が即座に反映される（Claude Code の再起動は必要）。

**prd モード**: `installLocation` を元の git clone に復元し `git pull` で最新化。

```bash
/marketplace-toggle dev      # ローカル開発モードに切り替え
/marketplace-toggle prd      # git モードに戻す
/marketplace-toggle status   # 現在のモードを確認
```

GitHub の Issue/PR 操作は、このリポジトリのローカル `.claude` スキルではなく、`shiiman-github` プラグインのスキルを利用してください。
Git ローカル操作（コミット、worktree等）は `shiiman-git` プラグインのスキルを利用してください。

## ドキュメント

- [docs/plugin.md](docs/plugin.md) - プラグイン作成ガイド
- [docs/skill.md](docs/skill.md) - スキル作成ガイド
- [docs/subagent.md](docs/subagent.md) - サブエージェント作成ガイド
- [docs/hook.md](docs/hook.md) - フック作成ガイド
- [docs/issues.md](docs/issues.md) - GitHub Issue Template からの起票ガイド

## プラグインの追加

`plugins/` 配下に以下の構造でディレクトリを作成:

```text
plugins/my-plugin/
├── .claude-plugin/
│   └── plugin.json         # プラグインメタデータ
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

## Markdown フォーマット

Prettier で `.md` ファイルを統一フォーマットしています。

```bash
# フォーマット実行
npm run format

# フォーマットチェック（CI 用）
npm run format:check
```

設定: `.prettierrc`（`proseWrap: "preserve"` で日本語の折り返しを維持）
