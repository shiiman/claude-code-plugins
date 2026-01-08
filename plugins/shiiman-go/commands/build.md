# Build

Go プロジェクトをビルドします。クロスコンパイル、再現可能ビルド、リンカーフラグによるバージョン埋め込みに対応。

## 使い方

```bash
/shiiman-go:build
/shiiman-go:build --os linux --arch amd64
/shiiman-go:build --trimpath
/shiiman-go:build --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `--os <os>` | ターゲット OS を指定 (linux, darwin, windows) |
| `--arch <arch>` | ターゲットアーキテクチャを指定 (amd64, arm64) |
| `--trimpath` | 再現可能ビルドのため絶対パスを削除 |
| `--help` | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### 実行手順

#### 1. タスクランナー検出

```bash
ls -la Taskfile.yml Makefile 2>/dev/null
```

**検出されるタスク名の例**:
- `build`, `compile`, `go-build`
- `build:linux`, `build:windows`

#### 2. ビルド実行

```bash
# タスクランナーがある場合
task build
make build

# 基本的なビルド
go build ./...

# 特定のエントリーポイントをビルド
go build -o bin/app ./cmd/app

# クロスコンパイル
GOOS=linux GOARCH=amd64 go build -o bin/app-linux ./cmd/app
GOOS=darwin GOARCH=arm64 go build -o bin/app-darwin ./cmd/app
GOOS=windows GOARCH=amd64 go build -o bin/app.exe ./cmd/app

# 再現可能ビルド
go build -trimpath -o bin/app ./cmd/app

# バージョン情報埋め込み
go build -ldflags "-X main.version=1.0.0 -X main.commit=$(git rev-parse HEAD)" -o bin/app ./cmd/app
```

#### 3. 結果レポート

```
✅ ビルド完了

出力ファイル: bin/app
ターゲット: {GOOS}/{GOARCH}
サイズ: {SIZE} MB

ビルドオプション:
- trimpath: {有効/無効}
- ldflags: {フラグ内容}
```

### クロスコンパイル対応表

| OS | GOOS | サポートアーキテクチャ |
|----|------|---------------------|
| Linux | linux | amd64, arm64, arm |
| macOS | darwin | amd64, arm64 |
| Windows | windows | amd64, arm64 |

### リンカーフラグ (-ldflags)

| フラグ | 説明 |
|--------|------|
| `-X main.version=1.0.0` | バージョン情報を埋め込み |
| `-X main.commit=abc123` | コミットハッシュを埋め込み |
| `-s` | シンボルテーブルを削除（バイナリサイズ削減） |
| `-w` | DWARF デバッグ情報を削除（バイナリサイズ削減） |

### ビルドタグ

```bash
# 特定のビルドタグを有効化
go build -tags "production" ./...

# 複数のタグを指定
go build -tags "production,netgo" ./...
```

### 注意事項

- **CGO**: クロスコンパイル時は `CGO_ENABLED=0` を設定する必要がある場合がある
- **再現可能ビルド**: リリースビルドでは `-trimpath` を使用して絶対パスを削除
- **バイナリサイズ**: `-ldflags "-s -w"` でデバッグ情報を削除してサイズ削減可能
- **PGO**: Profile-Guided Optimization で 2-14% の性能向上が期待できる（Go 1.22+）
