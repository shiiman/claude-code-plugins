# shiiman-claude-code-plugins

個人用 Claude Code プラグインマーケットプレイス。

## 使い方

```bash
claude plugin marketplace add shiiman/claude-code-plugins
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
