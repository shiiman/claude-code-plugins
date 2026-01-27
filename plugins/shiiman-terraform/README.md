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
| exec-tf | 「terraform plan」「tf apply」「validate」 | Terraform コマンド実行（plan/apply/validate 統合） |
| exec-tg | 「terragrunt run-all」「tg plan」 | Terragrunt コマンド実行 |
| init | 「init して」「terraform init」 | 初期化処理 |
| import | 「import して」「リソース import」 | import 支援 |
| analyze-state | 「state list」「state show」 | state 分析・操作 |
| manage-version | 「tfenv」「バージョン切り替え」 | バージョン管理 |
| generate-module | 「モジュール作成」「モジュール生成」 | モジュール構造生成 |
| check-security | 「セキュリティチェック」「シークレット検出」 | セキュリティ監査 |

### Agents（4）

| エージェント | 説明 |
|-------------|------|
| plan-reviewer | plan 結果のレビュー・要約 |
| state-troubleshooter | state 関連問題の診断・解決 |
| module-designer | モジュール設計・構造提案 |
| drift-detector | ドリフト検出・修正提案 |

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
  - tf-executor → exec-tf（plan/apply/validate 統合）
  - tg-executor → exec-tg
  - init-runner → init
  - import-helper → import
  - state-analyzer → analyze-state
  - version-manager → manage-version
  - module-generator → generate-module
  - security-checker → check-security

### 1.1.0

- Agents 追加: plan-reviewer, state-troubleshooter, module-designer, drift-detector

### 1.0.0

- 初回リリース
- Commands: plan, apply, validate
- Skills: tf-executor, tg-executor, init-runner, import-helper, state-analyzer, version-manager, module-generator, security-checker
