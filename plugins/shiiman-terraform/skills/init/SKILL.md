---
name: init
description: Terraform/Terragrunt の初期化を実行する。「init して」「terraform init」「terragrunt init」「初期化して」「tf init」「tg init」「プロジェクト初期化」「モジュール初期化」などで起動。
allowed-tools: [Bash, Read]
---

# Init Runner

Terraform/Terragrunt の初期化を実行します。

## 対応操作

| 操作 | トリガー例 | コマンド |
|------|-----------|----------|
| Terraform 初期化 | 「init して」「terraform init」 | `terraform init` |
| アップグレード | 「upgrade」「更新」 | `terraform init -upgrade` |
| 再設定 | 「reconfigure」「再設定」 | `terraform init -reconfigure` |
| Terragrunt 初期化 | 「tg init」「terragrunt init」 | `terragrunt init` |

## 実行手順

### 1. ツールの判定

```bash
# terragrunt.hcl があれば Terragrunt
ls terragrunt.hcl 2>/dev/null && echo "terragrunt" || echo "terraform"
```

### 2. 現在の状態確認

```bash
# .terraform ディレクトリの存在確認
ls -la .terraform 2>/dev/null

# .terraform.lock.hcl の存在確認
ls -la .terraform.lock.hcl 2>/dev/null
```

### 3. init 実行

**Terraform**:

```bash
# 標準 init
terraform init

# プロバイダのアップグレード
terraform init -upgrade

# バックエンド再設定
terraform init -reconfigure
```

**Terragrunt**:

```bash
terragrunt init
```

### 4. バックエンド設定の確認

init 後、バックエンド設定を確認:

```bash
# backend 設定の確認
grep -A 10 'backend' *.tf 2>/dev/null
```

### 5. 出力フォーマット

```
## Init 完了

### バックエンド
{local / s3 / gcs / azurerm など}

### プロバイダ
| プロバイダ | バージョン |
|-----------|-----------|
| aws | 5.x.x |
| ... | ... |

### モジュール
{使用しているモジュール一覧}

### 次のステップ
- `terraform plan` で変更内容を確認
- `terraform apply` で適用
```

## よくあるエラーと対処

### バックエンド設定変更時

```
Error: Backend configuration changed
```

対処:

```bash
terraform init -reconfigure
```

### プロバイダバージョン不整合

```
Error: Failed to query available provider packages
```

対処:

```bash
terraform init -upgrade
```

### 認証エラー（S3 バックエンド）

```
Error: error configuring S3 Backend: no valid credential sources
```

対処:

```
AWS 認証情報を設定してください:
- 環境変数: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
- AWS CLI: aws configure
- IAM ロール（EC2/ECS の場合）
```

## 注意事項

- ✅ init は安全な操作で何度実行しても問題ない
- ✅ `-upgrade` はプロバイダを最新バージョンに更新
- ✅ `-reconfigure` はバックエンド設定を再初期化
- ⚠️ バックエンド変更時は state の移行に注意
