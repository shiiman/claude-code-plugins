# shiiman-terraform

Terraform/Terragrunt の操作を支援するプラグインです。

## 概要

Terraform/Terragrunt の主要操作をシンプルなスキルと自然言語で実現します。
危険な操作（destroy、auto-approve）は自動的にブロックされ、安全にインフラを管理できます。

## インストール

```bash
claude plugin install shiiman-terraform@shiiman/claude-code-plugins
```

## 機能

### Skills（8）

| スキル | トリガー例 | 説明 |
|--------|-----------|------|
| tf | 「terraform plan」「tf apply」「validate」 | Terraform コマンド実行（plan/apply/validate 統合） |
| tg | 「terragrunt run-all」「tg plan」 | Terragrunt コマンド実行 |
| tf-init | 「init して」「terraform init」 | 初期化処理 |
| resource-import | 「import して」「リソース import」 | import 支援 |
| state-analyze | 「state list」「state show」 | state 分析・操作 |
| version-manage | 「tfenv」「バージョン切り替え」 | バージョン管理 |
| module-generate | 「モジュール作成」「モジュール生成」 | モジュール構造生成 |
| security-check | 「セキュリティチェック」「シークレット検出」 | セキュリティ監査 |

### Agents（5）

| エージェント | 説明 |
|-------------|------|
| plan-reviewer | plan 結果のレビュー・要約 |
| state-troubleshooter | state 関連問題の診断・解決 |
| module-designer | モジュール設計・構造提案 |
| drift-detector | ドリフト検出・修正提案 |
| security-checker | セキュリティ監査・リスク検出 |

## セキュリティ

### 許可される操作

- 読み取り系: terraform version, show, state list, output
- 検証系: terraform fmt, validate
- 計画系: terraform init, plan

### ブロックされる操作

- 破壊系: terraform destroy, destroy-all
- 自動承認: apply -auto-approve
- state 変更: state rm, state mv（手動実行を案内）
- 強制操作: force-unlock, taint

## 必要条件

- Terraform CLI（1.0+）
- Terragrunt（オプション）
- tfenv（オプション、バージョン管理用）
- tgswitch（オプション、Terragrunt バージョン管理用）

## バージョン履歴

### 1.2.0

- コマンドをスキルに統合
- スキル名を CLI 命名規則に変更
  - tf-executor → tf（plan/apply/validate 統合）
  - tg-executor → tg
  - init-runner → tf-init
  - import-helper → resource-import
  - state-analyzer → state-analyze
  - version-manager → version-manage
  - module-generator → module-generate
  - security-checker → security-check

### 1.1.0

- Agents 追加: plan-reviewer, state-troubleshooter, module-designer, drift-detector

### 1.0.0

- 初回リリース
- Commands: plan, apply, validate
- Skills: tf-executor, tg-executor, init-runner, import-helper, state-analyzer, version-manager, module-generator, security-checker
