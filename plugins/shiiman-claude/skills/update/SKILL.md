---
name: shiiman-claude:update
description: Claude Code CLI 本体のバージョン確認・更新と、インストール済みプラグインの一括更新を実行する。「Claude Code を更新」「claude update」「Claude のバージョン確認」「Claude 本体更新」「プラグイン更新」「plugin update」などで起動。引数があれば優先し、なければ発話内容から version/update/plugin-update を判定。brew での AI CLI 一括更新は shiiman-common:brew-upgrade-ai。
allowed-tools: [Bash, AskUserQuestion]
argument-hint: "[version|update|plugin-update] [--help]"
---

# Claude Update

Claude Code CLI のバージョン確認と更新を行います。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-claude:update - Claude Code 更新

概要:
  Claude Code CLI のバージョン確認・更新、プラグイン一括更新を実行する。
  Homebrew 管理の場合は brew upgrade を使用。

使用方法:
  /shiiman-claude:update [操作] [オプション]

操作:
  version        現在のバージョンを確認
  update         Claude Code CLI を更新
  plugin-update  インストール済みプラグインを一括更新

オプション:
  --help         このヘルプを表示

例:
  /shiiman-claude:update                # 発話内容から操作を判定
  /shiiman-claude:update version        # バージョン確認
  /shiiman-claude:update update         # Claude Code を更新
  /shiiman-claude:update plugin-update  # プラグインを一括更新
```

## 実行手順

### 1. 操作種別の決定

- 引数が指定されていれば引数を優先
- 引数がない場合は発話内容から以下を判定:
  - 確認系: version
  - 更新系: update
  - プラグイン更新系: plugin-update

### 2. 操作の実行

#### version

1. `claude --version` で現在のバージョンを表示
2. `claude update` に check 専用オプションがないことを明示
3. 更新したい場合は `update` モード実行を案内

#### update

1. `claude --version` で更新前バージョンを取得
2. 実行前にユーザー確認を行う
3. インストール方法を判定:
   - macOS かつ `brew list --versions claude-code` が成功する場合: `brew upgrade claude-code`
   - それ以外: `claude update`
4. `claude --version` で更新後バージョンを確認
5. 結果と必要な次アクション（再起動など）を報告

#### plugin-update

1. marketplace キャッシュを最新化:

```bash
# known_marketplaces.json から marketplace 一覧と installLocation を取得
cat ~/.claude/plugins/known_marketplaces.json
```

各 marketplace の `installLocation` で `git pull` を実行:

```bash
git -C <installLocation> pull 2>&1
```

2. `~/.claude/settings.json` の `enabledPlugins` から有効プラグイン一覧を取得:

```bash
cat ~/.claude/settings.json
```

`enabledPlugins` のキーは `<plugin>@<marketplace>` 形式。値が `true` のもののみ対象。

3. 各プラグインの更新前バージョンを記録:

`~/.claude/plugins/cache/<marketplace>/<plugin>/` 配下のバージョンディレクトリ名から現在のバージョンを特定（最も新しいもの）。

4. 実行前にユーザー確認を行う
5. 各プラグインに対して `claude plugin install <plugin>@<marketplace>` を実行
6. 更新後のバージョンを確認し、更新前後のバージョンを比較して結果を報告
7. 更新があった場合「Claude CLI を再起動すると反映されます」と案内

## 出力フォーマット

```markdown
## Claude Code 更新

### 実行モード

- version / update / plugin-update

### 結果

- 更新前: x.y.z
- 更新後: x.y.z（version 時は省略可）
- ステータス: 成功 / 失敗
- 補足: 必要に応じて再起動案内

### plugin-update 時の結果

| プラグイン | 更新前 | 更新後 | ステータス |
| ---------- | ------ | ------ | ---------- |
```

## 重要な注意事項

- ✅ update 実行前に必ず確認する
- ✅ Homebrew 管理の Claude Code は `brew upgrade claude-code` を使う
- ✅ 更新前後のバージョン差分を明示する
- ✅ plugin-update では各プラグインの更新前後バージョンを比較する
- ✅ 失敗時はエラーメッセージをそのまま報告する
- ❌ 失敗を推測で補完しない
