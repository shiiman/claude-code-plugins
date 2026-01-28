---
name: resource
description: Docker のリソースを管理する。「ネットワーク確認」「docker network」「ネットワーク一覧」「ボリューム確認」「docker volume」「ボリューム一覧」「ディスク確認」「docker system df」「ディスク使用量」「容量確認」「クリーンアップ」「docker cleanup」「docker prune」などで起動。
allowed-tools: [Bash]
---

# Manage Resource

Docker のネットワーク、ボリューム、ディスク使用量を管理します。

## 対応操作

| 操作 | トリガー例 | コマンド |
|------|-----------|----------|
| ネットワーク一覧 | 「ネットワーク確認」 | `docker network ls` |
| ネットワーク詳細 | 「ネットワーク詳細」 | `docker network inspect` |
| ボリューム一覧 | 「ボリューム確認」 | `docker volume ls` |
| ボリューム詳細 | 「ボリューム詳細」 | `docker volume inspect` |
| ディスク使用量 | 「ディスク確認」「容量」 | `docker system df` |
| クリーンアップ | 「クリーンアップ」「cleanup」 | `docker prune` |

## 実行手順

### 1. 意図の判定

ユーザーの発話から操作を判定:

- **ネットワーク系**: 「ネットワーク」「network」→ `docker network`
- **ボリューム系**: 「ボリューム」「volume」「永続化」→ `docker volume`
- **ディスク系**: 「ディスク」「容量」「使用量」「df」→ `docker system df`
- **クリーンアップ系**: 「クリーンアップ」「cleanup」「prune」「掃除」→ `docker prune`

### 2. ネットワーク操作

**一覧表示**:

```bash
docker network ls --format "table {{.ID}}\t{{.Name}}\t{{.Driver}}\t{{.Scope}}"
```

**詳細表示**:

```bash
docker network inspect <network> --format '{{json .}}' | jq '.'
```

接続中のコンテナを確認:

```bash
docker network inspect <network> --format '{{range .Containers}}{{.Name}} {{end}}'
```

### 3. ボリューム操作

**一覧表示**:

```bash
docker volume ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}"
```

**詳細表示**:

```bash
docker volume inspect <volume> --format '{{json .}}' | jq '.'
```

**使用量確認**:

```bash
docker system df -v | grep -A 100 "Local Volumes"
```

### 4. ディスク使用量

**概要**:

```bash
docker system df
```

**詳細**:

```bash
docker system df -v
```

### 5. 出力フォーマット

```
## ネットワーク一覧

| ID | 名前 | ドライバー | スコープ |
|----|------|-----------|----------|
| ... | ... | ... | ... |

合計: {N} ネットワーク
```

```
## ボリューム一覧

| 名前 | ドライバー | スコープ |
|------|-----------|----------|
| ... | ... | ... |

合計: {N} ボリューム
```

```
## Docker ディスク使用量

| タイプ | 総数 | アクティブ | サイズ | 回収可能 |
|--------|------|-----------|--------|----------|
| Images | ... | ... | ... | ... |
| Containers | ... | ... | ... | ... |
| Local Volumes | ... | ... | ... | ... |
| Build Cache | ... | ... | ... | ... |

**合計使用量**: {total}
**回収可能**: {reclaimable}

### 提案

{使用量が多い場合}
ディスク使用量が多くなっています。
「Docker のクリーンアップして」「削除対象を確認」などで不要リソースを削除できます。
```

### 6. クリーンアップ

未使用のリソースを安全にクリーンアップします。

#### 削除対象の確認

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

#### ユーザー確認

**重要**: 削除前に必ずユーザーに確認を求める。

```
## クリーンアップ確認

以下のリソースを削除します:

- 停止コンテナ: {N} 個
- dangling イメージ: {N} 個
- 未使用ネットワーク: {N} 個

削除を実行してよろしいですか？
```

#### クリーンアップ実行（安全な範囲のみ）

```bash
docker container prune -f
docker image prune -f
docker network prune -f
```

#### 削除しないもの（安全のため）

- ✅ 実行中のコンテナ
- ✅ タグ付きイメージ（使用中でなくても）
- ✅ ボリューム（データ保護のため）
- ✅ ビルドキャッシュ

#### 完全クリーンアップが必要な場合

以下の操作は危険なため、手動実行を案内:

```
完全なクリーンアップが必要な場合は、以下を手動で実行してください:

# 未使用ボリュームを削除（データ消失注意）
docker volume prune

# ビルドキャッシュを削除
docker builder prune

# すべての未使用リソースを削除（要注意）
docker system prune -a
```

## 注意事項

- ✅ ネットワーク/ボリュームの詳細は inspect で確認
- ✅ ディスク使用量が多い場合は cleanup を提案
- ✅ クリーンアップ前にユーザー確認を必ず行う
- ❌ `docker volume rm` は使用しない（データ保護）
- ❌ `docker volume prune` は使用しない（データ保護）
- ❌ ユーザー確認なしで削除を実行しない
