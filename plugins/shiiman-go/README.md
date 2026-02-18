# shiiman-go プラグイン

Go 言語開発を支援するプラグインです。

## 概要

Go 言語のベストプラクティスに基づいた開発支援を提供します。

## 対象技術

- Go 言語
- 標準パッケージ
- golangci-lint
- govulncheck

## 提供機能

### Skills

| スキル | トリガー例 | 説明 |
|--------|-----------|------|
| lint | 「lint して」「静的解析」 | lint 実行・自動修正 |
| mod-manage | 「依存関係を更新」「go mod」 | モジュール・バージョン管理 |
| perf-analyze | 「パフォーマンス計測」「ベンチマーク」 | パフォーマンス分析・最適化 |
| vuln-scan | 「脆弱性スキャン」「govulncheck」 | 脆弱性検出 |

### Agents

| エージェント | 説明 |
|-------------|------|
| performance-optimizer | パフォーマンス最適化専門家（ベンチマーク、pprof、PGO） |

## インストール

```bash
claude plugin install shiiman-go@shiiman-claude-code-plugins
```

## 使用方法

```bash
# 静的解析の実行
「lint して」

# 依存関係の更新
「依存関係を更新」

# パフォーマンス計測
「ベンチマーク」

# 脆弱性スキャン
「脆弱性スキャン」
```

## 特化機能

- golangci-lint 統合（自動修正対応）
- 依存関係の危険度評価付き更新
- pprof / benchstat によるパフォーマンス分析
- govulncheck による脆弱性検出
- Profile-Guided Optimization (PGO)

## カスタマイズ

このプラグインは拡張可能です。詳細は [プラグイン作成ガイド](../../docs/plugin.md) を参照してください。
