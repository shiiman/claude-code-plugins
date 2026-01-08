# Lint

Dockerfile の静的解析を行い、ベストプラクティスに基づいた提案をします。

## 使い方

```bash
/shiiman-docker:lint                    # ./Dockerfile を解析
/shiiman-docker:lint --file ./docker/Dockerfile.prod
/shiiman-docker:lint --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `--file <path>` | Dockerfile のパスを指定（デフォルト: ./Dockerfile） |
| `--help` | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

---

### 実行手順

#### 1. Dockerfile の存在確認

```bash
ls Dockerfile* docker/Dockerfile* 2>/dev/null
```

指定パスまたはデフォルトの Dockerfile が存在するか確認。

#### 2. Dockerfile を読み込み

Read ツールで Dockerfile の内容を取得。

#### 3. ベストプラクティスに基づいてチェック

以下の観点で解析を行う:

---

### チェック項目

#### セキュリティ（重要度: 高）

| チェック | 問題 | 推奨 |
|----------|------|------|
| `USER` 指定 | root で実行 | 非 root ユーザーを指定 |
| 機密情報 | ハードコードされた秘密 | ARG/ENV + ビルド時注入 |
| `ADD` vs `COPY` | リモート URL や tar 展開 | `COPY` を優先 |
| `apt-get` | キャッシュ残存 | `rm -rf /var/lib/apt/lists/*` |

#### パフォーマンス（重要度: 中）

| チェック | 問題 | 推奨 |
|----------|------|------|
| マルチステージ | 単一ステージで大きいイメージ | マルチステージビルド |
| レイヤー最適化 | 複数の `RUN` | 1つの `RUN` に結合 |
| `.dockerignore` | 不要ファイルのコピー | `.dockerignore` を作成 |
| ベースイメージ | フルイメージ使用 | alpine/slim を検討 |

#### メンテナンス性（重要度: 低）

| チェック | 問題 | 推奨 |
|----------|------|------|
| タグ固定 | `FROM node:latest` | `FROM node:20-alpine` |
| `LABEL` | メタデータなし | `LABEL` で情報追加 |
| `WORKDIR` | 相対パス使用 | 絶対パスを指定 |

---

### 出力フォーマット

```
## Dockerfile 解析結果

**ファイル**: {path}
**ベースイメージ**: {base_image}
**ステージ数**: {stages}

---

### 問題点

| 重要度 | 行 | カテゴリ | 内容 | 推奨 |
|--------|-----|----------|------|------|
| 🔴 高 | 1 | セキュリティ | `FROM node:latest` | タグを固定: `FROM node:20-alpine` |
| 🔴 高 | 25 | セキュリティ | root ユーザーで実行 | `USER node` を追加 |
| 🟡 中 | 10-15 | パフォーマンス | 複数の RUN 命令 | 1つの RUN に結合 |
| 🟢 低 | - | メンテナンス | LABEL がない | メタデータを追加 |

---

### 改善提案

#### 1. セキュリティ改善

{具体的な修正例}

#### 2. パフォーマンス改善

{具体的な修正例}

#### 3. その他の推奨事項

{.dockerignore の作成など}

---

### 改善版 Dockerfile（参考）

{最適化された Dockerfile の例}
```

---

### 言語別の推奨パターン

#### Node.js

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER app
EXPOSE 3000
CMD ["node", "index.js"]
```

#### Go

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/main

FROM scratch
COPY --from=builder /app/main /main
ENTRYPOINT ["/main"]
```

#### Python

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
RUN useradd -m app
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
USER app
CMD ["python", "main.py"]
```

---

## 重要な注意事項

- ✅ Claude の知識ベースでチェック（外部ツール不要）
- ✅ 具体的な修正例を提示
- ✅ 重要度に応じた優先順位付け
- ❌ 自動修正は行わない（提案のみ）
