---
name: shiiman-common:brew-upgrade-ai
description: AI 関連 CLI ツールを brew で一括アップグレードする。「AI ツール更新」「brew upgrade AI」「AI CLI 更新」「ツール一括更新」「claude/codex/cursor/gemini 更新」などで起動。
allowed-tools: [Bash]
argument-hint: "[--help]"
---

# Brew Upgrade AI

AI 関連 CLI ツールを brew で一括アップグレードします。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-common:brew-upgrade-ai - AI ツール一括更新

概要:
  AI 関連 CLI ツール（claude-code, codex, cursor-cli, gemini-cli）を
  brew で一括アップグレードします。

使用方法:
  /shiiman-common:brew-upgrade-ai [オプション]

オプション:
  --help    このヘルプを表示

例:
  /shiiman-common:brew-upgrade-ai     # AI ツールを一括更新
```

## 対象ツール

| brew パッケージ名 | ツール名    |
| ----------------- | ----------- |
| claude-code       | Claude Code |
| codex             | Codex       |
| cursor-cli        | Cursor CLI  |
| gemini-cli        | Gemini CLI  |

## ワークフロー

### 1. 現在のバージョン確認

Bash ツールで以下を**並列実行**し、各ツールのインストール状態と現在のバージョンを取得:

- `brew list --versions claude-code 2>/dev/null || echo "NOT_INSTALLED"`
- `brew list --versions codex 2>/dev/null || echo "NOT_INSTALLED"`
- `brew list --versions cursor-cli 2>/dev/null || echo "NOT_INSTALLED"`
- `brew list --versions gemini-cli 2>/dev/null || echo "NOT_INSTALLED"`

未インストール（`NOT_INSTALLED`）のツールはスキップ対象として記録。

### 2. アップグレード実行

インストール済みのツールのみ、Bash ツールで `brew upgrade` を**並列実行**:

- `brew upgrade claude-code 2>&1`
- `brew upgrade codex 2>&1`
- `brew upgrade cursor-cli 2>&1`
- `brew upgrade gemini-cli 2>&1`

各コマンドの出力から以下を判定:

- **更新済み**: バージョンが変わった場合
- **最新**: `already installed` や `already up-to-date` を含む場合
- **エラー**: その他のエラー出力

### 3. 新バージョン確認

更新が行われたツールのみ、Bash ツールで**並列実行**して新バージョンを取得:

- `brew list --versions {パッケージ名}`

### 4. 結果表示

以下のフォーマットで結果を出力:

```markdown
## AI ツール更新結果

| ツール      | 旧バージョン | 新バージョン | 状態           |
| ----------- | ------------ | ------------ | -------------- |
| claude-code | x.x.x        | y.y.y        | 更新済み       |
| codex       | x.x.x        | x.x.x        | 最新           |
| cursor-cli  | -            | -            | 未インストール |
| gemini-cli  | x.x.x        | y.y.y        | 更新済み       |
```

**状態の表記**:

| 状態           | 条件                                     |
| -------------- | ---------------------------------------- |
| 更新済み       | バージョンが変わった                     |
| 最新           | 既に最新バージョン                       |
| 未インストール | brew にパッケージが存在しない            |
| エラー         | upgrade コマンドが失敗（エラー詳細付記） |

## 重要な注意事項

- ✅ 未インストールのツールはスキップ（エラーにしない）
- ✅ 各 brew upgrade は並列実行して高速化
- ✅ 旧バージョン・新バージョンを比較して状態を判定
- ❌ 未インストールのツールを自動インストールしない
- ❌ brew 以外のパッケージマネージャは使用しない
