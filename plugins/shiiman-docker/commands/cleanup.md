# Cleanup

未使用の Docker リソースを安全にクリーンアップします。

## 使い方

```bash
/shiiman-docker:cleanup              # 安全なクリーンアップを実行
/shiiman-docker:cleanup --dry-run    # 削除せずに対象を表示
/shiiman-docker:cleanup --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `--dry-run` | 削除せずに対象を表示（実行前確認用） |
| `--help` | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

---

### 削除対象（安全な範囲のみ）

以下のリソースのみ削除します:

| 種類 | 対象 | コマンド |
|------|------|----------|
| コンテナ | 停止中のコンテナ | `docker container prune -f` |
| イメージ | dangling イメージ（タグなし） | `docker image prune -f` |
| ネットワーク | 未使用ネットワーク | `docker network prune -f` |

### 削除しないもの（安全のため）

- ✅ 実行中のコンテナ
- ✅ タグ付きイメージ（使用中でなくても）
- ✅ ボリューム（データ保護のため）
- ✅ ビルドキャッシュ

---

### 実行手順

#### 1. 現在のディスク使用量を確認

```bash
docker system df
```

#### 2. 削除対象の確認

**停止コンテナ**:

```bash
docker ps -a --filter "status=exited" --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}"
```

**dangling イメージ**:

```bash
docker images -f "dangling=true" --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

**未使用ネットワーク**:

```bash
docker network ls --filter "dangling=true" --format "table {{.ID}}\t{{.Name}}\t{{.Driver}}"
```

#### 3. `--dry-run` の場合

削除対象を表示して終了:

```
## クリーンアップ対象（dry-run）

### 停止コンテナ
{コンテナ一覧}

### dangling イメージ
{イメージ一覧}

### 未使用ネットワーク
{ネットワーク一覧}

---
実際に削除するには `--dry-run` なしで実行してください。
```

#### 4. ユーザー確認

**重要**: 削除前に必ずユーザーに確認を求める。

```
## クリーンアップ確認

以下のリソースを削除します:

- 停止コンテナ: {N} 個
- dangling イメージ: {N} 個
- 未使用ネットワーク: {N} 個

削除を実行してよろしいですか？
```

#### 5. クリーンアップ実行

```bash
docker container prune -f
docker image prune -f
docker network prune -f
```

#### 6. 結果レポート

```bash
docker system df
```

```
## クリーンアップ完了

| 種類 | 削除数 | 解放容量 |
|------|--------|----------|
| コンテナ | {N} | {size} |
| イメージ | {N} | {size} |
| ネットワーク | {N} | - |

**合計解放容量**: {total}

### 現在のディスク使用量
{docker system df の出力}
```

---

### 完全クリーンアップが必要な場合

以下の操作は危険なため、このコマンドでは実行しません:

| コマンド | リスク |
|----------|--------|
| `docker system prune -a` | すべての未使用リソース削除 |
| `docker volume prune` | ボリューム削除（データ消失） |
| `docker builder prune -a` | 全ビルドキャッシュ削除 |

必要な場合はユーザーに手動実行を案内:

```
完全なクリーンアップが必要な場合は、以下を手動で実行してください:

# 未使用ボリュームを削除（データ消失注意）
docker volume prune

# ビルドキャッシュを削除
docker builder prune

# すべての未使用リソースを削除（要注意）
docker system prune -a
```

## 重要な注意事項

- ✅ 削除前に必ずユーザー確認を行う
- ✅ `--dry-run` で事前に対象を確認することを推奨
- ❌ ボリュームは削除しない（データ保護）
- ❌ タグ付きイメージは削除しない
- ❌ ユーザー確認なしで削除を実行しない
