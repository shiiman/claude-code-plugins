# Validate

terraform validate と fmt を実行し、設定ファイルを検証します。

## 使い方

```bash
/shiiman-terraform:validate               # validate + fmt check
/shiiman-terraform:validate --fix         # fmt -write で自動修正
/shiiman-terraform:validate --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `--fix` | フォーマットの自動修正を実行 |
| `--help` | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

---

### 実行手順

#### 1. フォーマットチェック

```bash
terraform fmt -check -recursive -diff
```

出力例:

```
main.tf
--- old/main.tf
+++ new/main.tf
@@ -1,3 +1,3 @@
-resource "aws_instance" "example" {
-ami           = "ami-12345678"
+resource "aws_instance" "example" {
+  ami = "ami-12345678"
```

#### 2. `--fix` 指定時のフォーマット修正

```bash
terraform fmt -recursive -write=true
```

```
## フォーマット修正

以下のファイルを修正しました:
- main.tf
- variables.tf

修正完了
```

#### 3. 構文検証

```bash
terraform validate
```

成功時:

```
Success! The configuration is valid.
```

エラー時:

```
Error: Missing required argument
  on main.tf line 2, in resource "aws_instance" "example":
   2: resource "aws_instance" "example" {

The argument "ami" is required, but no definition was found.
```

#### 4. 結果レポート

**成功時**:

```
## 検証結果: ✅ 成功

### フォーマット
{フォーマット問題なし / N 件の問題あり}

### 構文検証
✅ 設定は有効です

{--fix なしでフォーマット問題がある場合}
フォーマットを修正するには:
/shiiman-terraform:validate --fix
```

**エラー時**:

```
## 検証結果: ❌ エラー

### フォーマット
{フォーマットの差分}

### 構文検証
❌ {エラー数} 件のエラー

| ファイル | 行 | エラー |
|----------|-----|--------|
| main.tf | 2 | Missing required argument "ami" |
| ... | ... | ... |

### 修正方法

{エラーごとの修正方法を提案}
```

---

### よくあるエラーと修正方法

| エラー | 原因 | 修正方法 |
|--------|------|----------|
| Missing required argument | 必須属性がない | 属性を追加 |
| Reference to undeclared resource | リソース参照エラー | リソース名を確認 |
| Invalid reference | 参照構文エラー | 構文を確認 |
| Unsupported attribute | 存在しない属性 | プロバイダのドキュメントを確認 |
| Cycle detected | 循環参照 | depends_on を見直し |

---

### 注意事項

- ✅ validate は読み取り専用で安全な操作
- ✅ `--fix` はファイルを書き換えるが、内容の変更ではなくフォーマットのみ
- ✅ CI/CD パイプラインで validate を実行することを推奨
- ❌ validate が通っても plan でエラーになることがある（プロバイダ固有のバリデーション）
