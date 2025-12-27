# shiiman-plugin

プラグイン管理用プラグイン - 一覧表示、詳細表示、インストール、アンインストール、有効化、無効化、アップデート機能を提供します。

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

## 使用する CLI コマンド

このプラグインは以下の Claude Code CLI コマンドを使用します：

```bash
claude plugin install <plugin>    # インストール
claude plugin uninstall <plugin>  # アンインストール
claude plugin enable <plugin>     # 有効化
claude plugin disable <plugin>    # 無効化
claude plugin update <plugin>     # アップデート
```

## ライセンス

MIT
