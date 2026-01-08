# Logs

Docker コンテナまたは Docker Compose サービスのログを表示します。

## 使い方

```bash
/shiiman-docker:logs                    # コンテナ一覧から選択
/shiiman-docker:logs <container>        # 特定のコンテナのログ
/shiiman-docker:logs --follow           # リアルタイムでログを追跡
/shiiman-docker:logs --tail 100         # 最新100行を表示
/shiiman-docker:logs --since 1h         # 過去1時間のログ
/shiiman-docker:logs --compose          # docker compose logs を使用
/shiiman-docker:logs --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `--follow`, `-f` | ログをリアルタイムで追跡 |
| `--tail <n>` | 最新 n 行を表示（デフォルト: 100） |
| `--since <time>` | 指定時刻以降のログ（例: 1h, 30m, 2024-01-01） |
| `--compose` | docker compose logs を使用 |
| `--service <name>` | Compose の特定サービスのみ（--compose と併用） |
| `--help` | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

---

### 実行手順

#### 1. Docker 環境確認

```bash
docker version --format '{{.Server.Version}}' 2>/dev/null || echo "Docker is not running"
```

Docker が起動していない場合はエラーメッセージを表示して終了。

#### 2. コンテナ/サービスの特定

**コンテナ名が指定されている場合**:
そのコンテナのログを表示。

**`--compose` が指定されている場合**:

```bash
docker compose ps --format "table {{.Name}}\t{{.Service}}\t{{.Status}}"
```

**指定がない場合**:

```bash
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}"
```

一覧を表示し、ユーザーに選択を促す。

#### 3. ログ取得

**Docker コンテナのログ**:

```bash
docker logs [--follow] [--tail N] [--since TIME] <container>
```

**Docker Compose のログ**:

```bash
docker compose logs [--follow] [--tail N] [--since TIME] [service]
```

### 出力フォーマット

```
## コンテナログ: {container_name}

{ログ出力}

---
表示行数: {N} 行
期間: {since} から現在まで
```

### 注意事項

- `--follow` 使用時は `Ctrl+C` で停止することを案内
- 大量ログの場合は `--tail` を推奨
- タイムスタンプ付きで表示
