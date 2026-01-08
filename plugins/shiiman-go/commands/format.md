# Format

Go プロジェクトのコードをフォーマットします。プロジェクトのタスクランナー設定（Makefile、Taskfile.yml など）を最優先で使用し、設定がない場合は Go 標準のフォーマットツールを実行します。

## 使い方

```bash
/shiiman-go:format
/shiiman-go:format --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `--help` | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### フォーマット実行の優先順位

1. **プロジェクトのタスクランナー設定**（最優先）
   - `Taskfile.yml` (Task/go-task) - フォーマットツールを実行するタスクを自動検出
   - `Makefile` (Make) - フォーマットツールを実行するターゲットを自動検出
   - `Justfile` (Just) - フォーマットツールを実行するレシピを自動検出

2. **プロジェクト設定ファイル**
   - `.golangci.yml` の設定に基づく `golangci-lint run --fix`

3. **Go 標準ツール**（フォールバック）
   - `goimports` (import 文の整理 + フォーマット)
   - `gofmt` (標準フォーマッター)

### 実行手順

#### 1. タスクランナー検出

プロジェクトルートで設定ファイルを確認:

```bash
ls -la Taskfile.yml Makefile Justfile 2>/dev/null
```

**検出されるタスク名の例**:
- `fmt`, `format`, `format-go`, `gofmt`, `go-fmt`
- `imports`, `goimports`, `format-imports`

#### 2. フォーマット実行

検出されたタスクを実行:

```bash
# Taskfile の場合
task fmt

# Makefile の場合
make fmt

# タスクランナー設定がない場合
goimports -w .
# または
gofmt -w .
```

#### 3. 結果レポート

```
✅ フォーマット完了

使用したツール: {ツール名}
フォーマットされたファイル:
- {ファイル1}
- {ファイル2}
```

### 対応フォーマットツール

| ツール | 説明 | インストール |
|--------|------|-------------|
| gofmt | Go 標準フォーマッター | 標準搭載 |
| goimports | import 文の整理 + gofmt | `go install golang.org/x/tools/cmd/goimports@latest` |
| gofumpt | gofmt の厳密版 | `go install mvdan.cc/gofumpt@latest` |
| golangci-lint | 複数リンター + フォーマッター | `go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest` |

### 注意事項

- **変更前にコミット**: フォーマット実行前に未コミットの変更をコミットまたはスタッシュすることを推奨
- **CI/CD との整合性**: プロジェクトの CI/CD で使用されているフォーマットツールと同じものを使用
- **外部パッケージの除外**: `vendor` や `third_party` ディレクトリは除外される
