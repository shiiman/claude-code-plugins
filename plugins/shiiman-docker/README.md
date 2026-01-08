# shiiman-docker

Docker/Docker Compose の操作を支援するプラグインです。

## 概要

コンテナ、イメージ、ネットワーク、ボリュームの管理をシンプルなコマンドと自然言語で実現します。危険な操作は自動的にブロックされ、安全に Docker 環境を管理できます。

## インストール

```bash
claude plugin install shiiman-docker@shiiman-claude-code-plugins
```

## 機能

### Commands

| コマンド | 説明 |
|----------|------|
| `/shiiman-docker:logs` | コンテナ/サービスのログを表示 |
| `/shiiman-docker:cleanup` | 未使用リソースを安全にクリーンアップ |
| `/shiiman-docker:lint` | Dockerfile の静的解析 |

### Skills

| スキル | トリガー例 | 説明 |
|--------|-----------|------|
| container-manager | 「コンテナ一覧」「docker ps」「コンテナ止めて」 | コンテナ管理（ps, start, stop, exec, stats, inspect） |
| image-manager | 「イメージ一覧」「ビルドして」「イメージ取得」 | イメージ管理（images, build, pull） |
| compose-manager | 「compose 起動」「サービス停止」「compose ログ」 | Compose 管理（up, down, ps, logs） |
| resource-manager | 「ネットワーク確認」「ボリューム一覧」「ディスク確認」 | リソース管理（network, volume, disk） |
| dockerfile-helper | 「Dockerfile 作成」「Dockerfile 改善」 | Dockerfile 作成・改善支援 |

### Agents

| エージェント | 説明 |
|-------------|------|
| troubleshooter | 起動エラー、ネットワーク問題、パフォーマンス問題の診断・解決 |
| dockerfile-reviewer | Dockerfile のセキュリティ、パフォーマンス、ベストプラクティスレビュー |

## 使用例

### コンテナ管理

```bash
# コンテナ一覧
「コンテナ一覧」

# ログ確認
/shiiman-docker:logs my-container --tail 100

# コンテナに入る
「app コンテナに入って」
```

### Docker Compose

```bash
# サービス起動
「compose 起動」

# サービス停止
「compose 停止」

# リアルタイムログ
/shiiman-docker:logs --compose --follow
```

### イメージ管理

```bash
# イメージ一覧
「イメージ一覧」

# ビルド
「ビルドして」

# イメージ取得
「node:20-alpine を pull して」
```

### Dockerfile

```bash
# Dockerfile 作成
「Dockerfile を作って」

# Dockerfile レビュー
/shiiman-docker:lint

# 最適化
「Dockerfile を alpine 化して」
```

### クリーンアップ

```bash
# 削除対象を確認
/shiiman-docker:cleanup --dry-run

# クリーンアップ実行
/shiiman-docker:cleanup
```

### トラブルシューティング

```bash
# 問題診断
「コンテナが起動しない」

# パフォーマンス問題
「コンテナが遅い」
```

## セキュリティ

このプラグインは以下の危険な操作を自動的にブロックします:

### 許可される操作

- 読み取り系: `docker ps`, `docker logs`, `docker images`, `docker inspect`, `docker stats`
- 制御系: `docker start`, `docker stop`, `docker restart`, `docker exec`
- ビルド系: `docker build`, `docker pull`, `docker compose build`
- Compose 系: `docker compose up`, `docker compose down`, `docker compose ps`
- 安全なクリーンアップ: `docker container prune -f`, `docker image prune -f`

### ブロックされる操作

- 強制削除: `docker rm -f`, `docker rmi -f`
- 強制終了: `docker kill`
- データ消失リスク: `docker volume prune`, `docker volume rm`
- 完全クリーンアップ: `docker system prune -a`
- Compose 強制: `docker compose kill`, `docker compose rm -f`

## 必要条件

- Docker Desktop または Docker Engine
- Docker Compose v2

## バージョン履歴

### v1.0.0

- 初回リリース
- 3 コマンド（logs, cleanup, lint）
- 5 スキル（container-manager, image-manager, compose-manager, resource-manager, dockerfile-helper）
- 2 エージェント（troubleshooter, dockerfile-reviewer）
