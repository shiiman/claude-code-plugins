# Apply

terraform apply を実行し、インフラに変更を適用します。

## 使い方

```bash
/shiiman-terraform:apply                   # plan 確認後に apply
/shiiman-terraform:apply plan.tfplan       # plan ファイルから apply
/shiiman-terraform:apply --target <resource> # 特定リソースのみ
/shiiman-terraform:apply --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `<plan-file>` | plan ファイルを指定して apply |
| `--target <resource>` | 特定リソースのみ apply |
| `--help` | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

---

### 重要な安全規則

- ❌ **`-auto-approve` は絶対に使用しない**
- ✅ 必ずユーザー確認を取ってから apply を実行
- ✅ 破壊的変更がある場合は特に注意を促す

---

### 実行手順

#### 1. 事前確認

```bash
# .tf ファイルの存在確認
ls *.tf 2>/dev/null || ls **/*.tf 2>/dev/null

# 初期化状態確認
ls -la .terraform 2>/dev/null
```

#### 2. plan 実行（plan ファイルがない場合）

plan ファイルが指定されていない場合、先に plan を実行:

```bash
terraform plan -no-color
```

#### 3. 変更内容の確認と警告

plan 結果を解析し、以下を表示:

```
## Apply 確認

### 変更内容

| 種類 | 数 | リソース |
|------|-----|----------|
| 🟢 追加 | {N} | {リソース一覧} |
| 🟡 変更 | {N} | {リソース一覧} |
| 🔴 削除 | {N} | {リソース一覧} |
| ⚠️ 再作成 | {N} | {リソース一覧} |

{破壊的変更がある場合}
### ⚠️ 警告: 破壊的変更

以下のリソースが削除または再作成されます:
- {リソース名}: {理由}

データ損失の可能性があります。十分に確認してください。
```

#### 4. ユーザー確認

**必ずユーザーに確認を求める**:

```
上記の変更を適用してよろしいですか？

- 「はい」または「apply して」で実行
- 「いいえ」または「キャンセル」で中止
```

#### 5. apply 実行

ユーザーの承認後のみ実行:

**plan ファイルなし**:

```bash
terraform apply -no-color
```

インタラクティブに `yes` を入力する必要があるため、ユーザーに案内:

```
terraform apply を実行します。
確認プロンプトで「yes」を入力してください。
```

**plan ファイルあり**:

```bash
terraform apply -no-color <plan-file>
```

plan ファイルからの apply は確認プロンプトなしで実行される。

#### 6. 結果レポート

```
## Apply 完了

### 適用結果

| 種類 | 数 |
|------|-----|
| 追加 | {N} |
| 変更 | {N} |
| 削除 | {N} |

### 出力値

{terraform output の結果（あれば）}

### 次のステップ

- `terraform state list` で作成されたリソースを確認
- `terraform output` で出力値を確認
```

---

### エラー時の対応

#### State ロックエラー

```
Error: Error acquiring the state lock
```

対応:

```
⚠️ State がロックされています

別のプロセスが terraform を実行中の可能性があります。
- 他のターミナルで terraform が実行中でないか確認
- CI/CD パイプラインが実行中でないか確認

どうしても解除が必要な場合:
terraform force-unlock <LOCK_ID>

※ force-unlock は危険な操作です。必ず原因を確認してから実行してください。
```

#### リソース競合エラー

```
Error: Resource already exists
```

対応:

```
⚠️ リソースが既に存在します

対処方法:
1. import で既存リソースを取り込む
2. リソース名を変更して新規作成
3. 既存リソースを削除してから apply

「import して」と言うと import の手順を案内します。
```

---

### 注意事項

- ✅ apply 前に必ず plan で変更内容を確認
- ✅ 破壊的変更がある場合は特に慎重に
- ✅ 本番環境への apply は十分な確認の上で実行
- ❌ `-auto-approve` は使用しない
- ❌ 確認なしで apply を実行しない
