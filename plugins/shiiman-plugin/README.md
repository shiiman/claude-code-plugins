# shiiman-plugin

プラグイン管理用プラグイン - 一覧表示、詳細表示、インストール、アンインストール、有効化、無効化、アップデート、Issue報告機能を提供します。

## インストール

```bash
# マーケットプレイスを追加（初回のみ）
/plugin marketplace add shiiman/claude-code-plugins

# プラグインをインストール
/plugin install shiiman-plugin@shiiman-claude-code-plugins
```

## 機能一覧

| 機能 | コマンド | スキル | 説明 |
|------|----------|--------|------|
| 一覧表示 | `/shiiman-plugin:list` | lister | 利用可能なプラグインの一覧を表示 |
| 詳細表示 | `/shiiman-plugin:show` | shower | プラグインの詳細情報を表示 |
| インストール | `/shiiman-plugin:install` | installer | プラグインをインストール |
| アンインストール | `/shiiman-plugin:uninstall` | uninstaller | プラグインをアンインストール |
| 有効化 | - | enabler | プラグインを有効化 |
| 無効化 | - | disabler | プラグインを無効化 |
| アップデート | - | updater | プラグインを最新版に更新 |
| Issue報告 | `/shiiman-plugin:report` | reporter | プラグインに関する要望・改善・バグを報告 |

## コマンド

### `/shiiman-plugin:list`

利用可能なプラグインの一覧を表示します。

```bash
/shiiman-plugin:list
```

表示内容:

- プラグイン名
- 説明
- 最新バージョン
- 現在バージョン
- インストール状態

### `/shiiman-plugin:show [plugin-name]`

指定したプラグインの詳細情報を表示します。

```bash
/shiiman-plugin:show shiiman-common
```

表示内容:

- 基本情報（名前、説明、バージョン）
- コマンド一覧
- スキル一覧
- エージェント一覧
- フック一覧
- README

### `/shiiman-plugin:install [plugin-name]`

指定したプラグインをインストールします。

```bash
/shiiman-plugin:install shiiman-common
```

### `/shiiman-plugin:uninstall [plugin-name]`

指定したプラグインをアンインストールします。

```bash
/shiiman-plugin:uninstall shiiman-common
```

### `/shiiman-plugin:report`

プラグインに関する要望、改善提案、バグ報告を shiiman/claude-code-plugins リポジトリに Issue として投稿します。

```bash
/shiiman-plugin:report
```

報告の種類:

- 要望（新機能の追加）→ `enhancement` ラベル
- 改善（既存機能の改善）→ `improvement` ラベル
- バグ（不具合の報告）→ `bug` ラベル

## スキル（自然言語トリガー）

以下のような自然言語でスキルを起動できます：

| スキル | トリガー例 |
|--------|------------|
| lister | 「プラグイン一覧」「どんなプラグインがある？」 |
| shower | 「〇〇プラグインについて教えて」「プラグインの詳細」 |
| installer | 「〇〇をインストールして」「プラグインを追加」 |
| uninstaller | 「〇〇を削除して」「プラグインをアンインストール」 |
| enabler | 「〇〇を有効にして」「プラグインをオンに」 |
| disabler | 「〇〇を無効にして」「プラグインをオフに」 |
| updater | 「〇〇をアップデート」「プラグインを最新に」 |
| reporter | 「バグを報告」「要望を送りたい」「改善提案」 |

## 使用する CLI コマンド

このプラグインは以下の Claude Code CLI コマンドを使用します：

```bash
claude plugin install <plugin>    # インストール
claude plugin uninstall <plugin>  # アンインストール
claude plugin enable <plugin>     # 有効化
claude plugin disable <plugin>    # 無効化
claude plugin update <plugin>     # アップデート

# Issue報告では gh コマンドを使用
gh issue create --repo shiiman/claude-code-plugins ...
```

## ライセンス

MIT
