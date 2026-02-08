# shiiman-go プラグイン

Go 言語開発を支援するプラグインです。

## 概要

Go 言語のベストプラクティスに基づいた開発支援を提供します。

## 対象技術

- Go 言語
- 標準パッケージ
- テーブル駆動テスト
- golangci-lint
- govulncheck

## 提供機能

### Skills

| スキル | トリガー例 | 説明 |
|--------|-----------|------|
| build | 「ビルドして」「go build」 | ビルド実行（クロスコンパイル対応） |
| format | 「フォーマットして」「gofmt して」 | フォーマット実行 |
| lint | 「lint して」「静的解析」 | lint 実行・自動修正 |
| test | 「テスト実行」「go test」 | テスト実行（カバレッジ対応） |
| mod-manage | 「依存関係を更新」「go mod」 | モジュール・バージョン管理 |
| perf-analyze | 「パフォーマンス計測」「ベンチマーク」 | パフォーマンス分析・最適化 |
| vuln-scan | 「脆弱性スキャン」「govulncheck」 | 脆弱性検出 |
| test-create | 「テストを作って」「テスト追加」 | テストコード自動生成 |
| error-fix | 「エラーを直して」「ビルドエラー修正」 | エラー診断・修正 |
| code-review | 「コードレビューして」「Go のレビュー」 | コードレビュー |

### Agents

| エージェント | 説明 |
|-------------|------|
| test-writer | テストコード専門家（テーブル駆動テスト、t.Parallel()、モック対応） |
| performance-optimizer | パフォーマンス最適化専門家（ベンチマーク、pprof、PGO） |
| command-runner | Go コマンド実行専門家（タスクランナー連携） |
| error-analyzer | エラー分析・修正専門家（コンパイル/lint/ランタイムエラー） |
| code-reviewer | コードレビュー専門家（Effective Go、Go Code Review Comments 準拠）|

## インストール

```bash
claude plugin install shiiman-go@shiiman-claude-code-plugins
```

## 使用方法

```bash
# コードのフォーマット
「フォーマットして」

# 静的解析の実行
「lint して」

# テストの実行
「テスト実行」

# 依存関係の更新
「依存関係を更新」

# 脆弱性スキャン
「脆弱性スキャン」
```

## 特化機能

- Go コーディング規約準拠
- 標準パッケージ活用
- エラーハンドリングパターン
- 並行処理のベストプラクティス
- テーブル駆動テスト
- Profile-Guided Optimization (PGO)

## カスタマイズ

このプラグインは拡張可能です。詳細は [プラグイン作成ガイド](../../docs/plugin.md) を参照してください。
