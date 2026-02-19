# shiiman-common

共通開発ツールプラグイン

## 概要

ローカル変更の統合レビュー（Claude + Codex + セキュリティ）と AI CLI ツールの一括更新を提供するプラグインです。

## インストール

```bash
claude plugin install shiiman-common@shiiman-claude-code-plugins
```

## 機能

### スキル

| スキル          | トリガー例                     | 説明                                                                |
| --------------- | ------------------------------ | ------------------------------------------------------------------- |
| review          | 「レビュー」「コードレビュー」 | ローカル変更を Claude + Codex + セキュリティの 3 観点で並列レビュー |
| brew-upgrade-ai | 「AI ツール更新」              | AI 関連 CLI ツールを brew で一括アップグレード                      |

## スキル詳細

### review

ローカル変更を 3 つの観点で並列レビューし、統合結果を表示します。

**レビュー観点:**

1. **コード品質レビュー (Claude)** — 命名・設計・テスト・可読性を評価
2. **セキュリティレビュー** — OWASP Top 10 基準で脆弱性チェック
3. **Codex レビュー** — `codex review --uncommitted` を実行

レビュー後、指摘の修正をインタラクティブに実行可能。

### brew-upgrade-ai

AI 関連 CLI ツール（claude-code, codex, cursor-cli, gemini-cli）を brew で一括アップグレードします。

**対象ツール:**

- Claude Code (`claude-code`)
- Codex (`codex`)
- Cursor CLI (`cursor-cli`)
- Gemini CLI (`gemini-cli`)

未インストールのツールはスキップし、更新結果を表形式で出力します。

## 必要条件

- Homebrew がインストール済み（brew-upgrade-ai 用）
- codex CLI がインストール済み（review の Codex レビュー用、未インストールでもスキップ可）
