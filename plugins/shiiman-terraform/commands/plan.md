# Plan

terraform plan を実行し、変更内容を解析・要約します。

## 使い方

```bash
/shiiman-terraform:plan                    # 標準 plan
/shiiman-terraform:plan --target <resource> # 特定リソースのみ
/shiiman-terraform:plan --out plan.tfplan  # plan ファイル出力
/shiiman-terraform:plan --destroy          # destroy plan
/shiiman-terraform:plan --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `--target <resource>` | 特定リソースのみ plan |
| `--out <file>` | plan ファイルを出力 |
| `--destroy` | destroy plan を実行 |
| `--help` | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

---

### 実行手順

#### 1. 事前確認

```bash
# .tf ファイルの存在確認
ls *.tf 2>/dev/null || ls **/*.tf 2>/dev/null
```

`.tf` ファイルがない場合はエラーメッセージを表示して終了。

#### 2. 初期化状態確認

```bash
# .terraform ディレクトリの存在確認
ls -la .terraform 2>/dev/null
```

`.terraform` がない場合:

```
⚠️ Terraform が初期化されていません。
先に `terraform init` を実行してください。

「init して」と言うか、以下を実行:
terraform init
```

#### 3. terraform plan 実行

**標準 plan**:

```bash
terraform plan -no-color
```

**オプション付き**:

```bash
# 特定リソースのみ
terraform plan -target=<resource> -no-color

# plan ファイル出力
terraform plan -out=<file> -no-color

# destroy plan
terraform plan -destroy -no-color
```

#### 4. 結果解析

plan 出力を解析し、以下の情報を抽出:

- 追加されるリソース（`+`）
- 変更されるリソース（`~`）
- 削除されるリソース（`-`）
- 再作成されるリソース（`-/+` または `+/-`）

#### 5. 出力フォーマット

```
## Plan 結果

| 種類 | 数 | リソース |
|------|-----|----------|
| 🟢 追加 | {N} | {リソース一覧} |
| 🟡 変更 | {N} | {リソース一覧} |
| 🔴 削除 | {N} | {リソース一覧} |
| ⚠️ 再作成 | {N} | {リソース一覧} |

### 変更サマリー

Plan: {add} to add, {change} to change, {destroy} to destroy.

### 破壊的変更（要注意）

{force replacement が発生するリソースがあれば警告}

- `aws_db_instance.main` - force replacement（engine_version の変更）
- ...

### 詳細

{terraform plan の出力（必要に応じて抜粋）}
```

#### 6. 破壊的変更の検出

以下のパターンを検出して警告:

- `# ... must be replaced` - リソースの再作成
- `# ... will be destroyed` - リソースの削除
- `forces replacement` - 属性変更による再作成

```
⚠️ 破壊的変更が検出されました

以下のリソースが再作成または削除されます:
- {リソース名}: {理由}

apply 前に内容を確認してください。
```

---

### 注意事項

- ✅ plan は読み取り専用で安全な操作
- ✅ 破壊的変更がある場合は警告を表示
- ✅ `--out` で plan ファイルを保存すると apply 時に同じ変更が適用される
- ❌ plan 結果を見ずに apply しない
