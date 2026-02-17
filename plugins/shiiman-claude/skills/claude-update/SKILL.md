---
name: claude-update
description: Claude Code CLI のバージョン確認と更新を実行する。「Claude を更新」「Claude Code をアップデート」「claude update」「Claude のバージョン確認」「最新版にして」「Claude を最新に」「Claude 本体更新」などで起動。引数があれば優先し、なければ発話内容から version/update を判定。
allowed-tools: [Bash, AskUserQuestion]
---

# Claude Update

Claude Code CLI のバージョン確認と更新を行います。

## 引数

- `$ARGUMENTS`:
  - `--version`: 現在バージョンを確認
  - `--update`: Claude Code CLI を更新
  - `--help`: ヘルプを表示

## 実行手順

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### 1. 操作種別の決定

- 引数が指定されていれば引数を優先
- 引数がない場合は発話内容から以下を判定:
  - 確認系: version
  - 更新系: update

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

## 出力フォーマット

```markdown
## Claude Code 更新

### 実行モード
- version / update

### 結果
- 更新前: x.y.z
- 更新後: x.y.z（version 時は省略可）
- ステータス: 成功 / 失敗
- 補足: 必要に応じて再起動案内
```

## 重要な注意事項

- ✅ update 実行前に必ず確認する
- ✅ Homebrew 管理の Claude Code は `brew upgrade claude-code` を使う
- ✅ 更新前後のバージョン差分を明示する
- ✅ 失敗時はエラーメッセージをそのまま報告する
- ❌ 失敗を推測で補完しない
