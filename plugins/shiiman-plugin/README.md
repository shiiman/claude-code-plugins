# shiiman-plugin

プラグイン管理用プラグイン - 一覧表示、詳細表示、インストール、アンインストール、有効化、無効化、アップデート、検索、更新チェック、Issue報告機能を提供します。

## インストール

```bash
# マーケットプレイスを追加（初回のみ）
/plugin marketplace add shiiman/claude-code-plugins

# プラグインをインストール
/plugin install shiiman-plugin@shiiman-claude-code-plugins
```

## 機能一覧

| 機能 | スキル | 説明 |
|------|--------|------|
| 一覧表示 | list | 利用可能なプラグインの一覧を表示 |
| 詳細表示 | show | プラグインの詳細情報を表示 |
| インストール | install | プラグインをインストール |
| アンインストール | uninstall | プラグインをアンインストール |
| 有効化 | enable | プラグインを有効化 |
| 無効化 | disable | プラグインを無効化 |
| アップデート | update | プラグインを最新版に更新（--all で一括更新） |
| 検索 | search | キーワードでプラグインを検索 |
| 更新チェック | check-updates | 更新可能なプラグインを確認 |
| Issue報告 | report | プラグインに関する要望・改善・バグを報告 |

## スキル（自然言語トリガー）

以下のような自然言語でスキルを起動できます：

| スキル | トリガー例 |
|--------|------------|
| list | 「プラグイン一覧」「どんなプラグインがある？」 |
| show | 「〇〇プラグインについて教えて」「プラグインの詳細」 |
| install | 「〇〇をインストールして」「プラグインを追加」 |
| uninstall | 「〇〇を削除して」「プラグインをアンインストール」 |
| enable | 「〇〇を有効にして」「プラグインをオンに」 |
| disable | 「〇〇を無効にして」「プラグインをオフに」 |
| update | 「〇〇をアップデート」「プラグインを最新に」「全部アップデート」 |
| search | 「〇〇関連のプラグイン」「〇〇ができるプラグイン」 |
| check-updates | 「更新があるか確認」「アップデート確認」 |
| report | 「バグを報告」「要望を送りたい」「改善提案」 |

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
