# shiiman-common

共通開発ツールプラグイン

## 概要

ローカル変更の統合レビュー（Claude + Codex + セキュリティ + Simplify）と AI CLI ツールの一括更新を提供するプラグインです。

## インストール

```bash
claude plugin install shiiman-common@shiiman-claude-code-plugins
```

## 機能

### スキル

| スキル          | トリガー例                     | 説明                                                                            |
| --------------- | ------------------------------ | ------------------------------------------------------------------------------- |
| review          | 「レビュー」「コードレビュー」 | ローカル変更を Claude + Codex + セキュリティ + Simplify の 4 観点で並列レビュー |
| brew-upgrade-ai | 「AI ツール更新」              | AI 関連 CLI ツールを brew で一括アップグレード                                  |

## スキル詳細

### review

ローカル変更を 4 つの観点で並列レビューし、統合結果を表示します。

**レビュー観点:**

1. **コード品質レビュー (Claude / 8 観点並列)** — コード品質・設計・テスト・可読性・パフォーマンス・エラーハンドリング・ベストプラクティス・保守性
2. **セキュリティレビュー** — ビルトイン `/security-review` スキルによる脆弱性チェック
3. **Codex レビュー** — `codex exec --full-auto` で 8 観点の並列レビューを実行
4. **Simplify レビュー** — ビルトイン `/simplify` スキルによるコードの再利用性・品質・効率性チェック

レビュー後、指摘の修正をインタラクティブに実行可能。

### brew-upgrade-ai

AI 関連 CLI ツール（claude-code@latest, codex, cursor-cli, gemini-cli）を brew で一括アップグレードします。

**対象ツール:**

- Claude Code (`claude-code@latest`、fallback: `claude-code`)
- Codex (`codex`)
- Cursor CLI (`cursor-cli`)
- Gemini CLI (`gemini-cli`)

未インストールのツールはスキップし、更新結果を表形式で出力します。

## 必要条件

- Claude Code v2.1.56 以上（ビルトイン `/security-review` スキル使用のため）
- Homebrew がインストール済み（brew-upgrade-ai 用）
- codex CLI がインストール済み（review の Codex レビュー用、未インストールでもスキップ可）
