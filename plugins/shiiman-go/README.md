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

### Commands

| コマンド | 説明 |
|----------|------|
| `/shiiman-go:format` | コードのフォーマット（gofmt/goimports/gofumpt） |
| `/shiiman-go:lint` | 静的解析を実行し、自動修正可能な問題を修正 |
| `/shiiman-go:test` | ユニットテストの実行（カバレッジ計測対応） |
| `/shiiman-go:mod-update` | go.mod の依存関係を更新 |
| `/shiiman-go:mod-version` | go.mod の Go バージョンを管理 |
| `/shiiman-go:build` | プロジェクトのビルド（クロスコンパイル対応） |
| `/shiiman-go:perf` | パフォーマンス計測・最適化 |
| `/shiiman-go:vuln` | govulncheck で脆弱性スキャン |

### Skills

| スキル | トリガー例 | 説明 |
|--------|-----------|------|
| test-creator | 「テストを作って」「テスト追加」 | テストコード自動生成 |
| error-fixer | 「エラーを直して」「ビルドエラー修正」 | エラー診断・修正 |
| code-reviewer | 「コードレビューして」「Go のレビュー」 | コードレビュー |
| formatter | 「フォーマットして」「gofmt して」 | フォーマット実行 |
| linter | 「lint して」「静的解析」 | lint 実行 |
| mod-manager | 「依存関係を更新」「go mod」 | モジュール管理 |
| builder | 「ビルドして」「go build」 | ビルド実行 |

### Agents

| エージェント | 説明 |
|-------------|------|
| test-writer | テストコード専門家（テーブル駆動テスト、t.Parallel()、モック対応） |
| performance-optimizer | パフォーマンス最適化専門家（ベンチマーク、pprof、PGO） |
| command-runner | Go コマンド実行専門家（タスクランナー連携） |
| error-analyzer | エラー分析・修正専門家（コンパイル/lint/ランタイムエラー） |

## インストール

```bash
claude plugin install shiiman-go@shiiman-claude-code-plugins
```

## 使用方法

```bash
# コードのフォーマット
/shiiman-go:format

# 静的解析の実行
/shiiman-go:lint

# テストの実行
/shiiman-go:test

# 依存関係の更新
/shiiman-go:mod-update

# 脆弱性スキャン
/shiiman-go:vuln
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
