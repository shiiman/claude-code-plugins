# shiiman-terraform

Terraform リソース import を支援するプラグインです。

## 概要

既存の AWS/GCP/Azure リソースを Terraform の管理下に取り込むワークフローを提供します。

## 提供機能

### Skills

| スキル    | トリガー例                                       | 説明                                                          |
| --------- | ------------------------------------------------ | ------------------------------------------------------------- |
| tf-import | 「import して」「terraform import」「tf import」 | 既存リソースの import 支援（空定義生成 → import → plan 同期） |

## インストール

```bash
claude plugin install shiiman-terraform@shiiman-claude-code-plugins
```

## 使用方法

```bash
# 既存リソースを Terraform に import
「EC2 を import して」
```

## 特化機能

- import ワークフローのステップバイステップ案内
- 空リソース定義の自動生成
- 主要 AWS リソースの import コマンド例
- import 後の plan 差分確認と設定同期

## 必要条件

- Terraform CLI（1.0+）

## カスタマイズ

このプラグインは拡張可能です。詳細は [プラグイン作成ガイド](../../docs/plugin.md) を参照してください。
