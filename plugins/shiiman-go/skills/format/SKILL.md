---
name: format
description: Go コードをフォーマットする。「フォーマットして」「コード整形」「gofmt して」「コードを綺麗にして」「整形して」「フォーマット実行」「goimports」などで起動。タスクランナー設定を最優先で使用。
allowed-tools: [Read, Bash, Glob, Grep]
---

# Format

Go コードをフォーマットします。プロジェクトのタスクランナー設定（Makefile、Taskfile.yml など）を最優先で使用し、設定がない場合は Go 標準のフォーマットツールを実行。

## 引数

- `--help`: ヘルプを表示

## フォーマット実行の優先順位

1. **プロジェクトのタスクランナー設定**（最優先）
   - `Taskfile.yml` (Task/go-task)
   - `Makefile` (Make)
   - `Justfile` (Just)

2. **プロジェクト設定ファイル**
   - `.golangci.yml` の設定に基づく `golangci-lint run --fix`

3. **Go 標準ツール**（フォールバック）
   - `goimports` (import 文の整理 + フォーマット)
   - `gofmt` (標準フォーマッター)

## 実行手順

### 1. タスクランナー検出

```bash
ls -la Taskfile.yml Makefile Justfile 2>/dev/null
```

**検出されるタスク名の例**:
- `fmt`, `format`, `format-go`, `gofmt`, `go-fmt`
- `imports`, `goimports`, `format-imports`

### 2. フォーマット実行

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

### 3. 結果レポート

```
✅ フォーマット完了

使用したツール: {ツール名}
フォーマットされたファイル:
- {ファイル1}
- {ファイル2}
```

## 対応フォーマットツール

| ツール | 説明 | インストール |
|--------|------|-------------|
| gofmt | Go 標準フォーマッター | 標準搭載 |
| goimports | import 文の整理 + gofmt | `go install golang.org/x/tools/cmd/goimports@latest` |
| gofumpt | gofmt の厳密版 | `go install mvdan.cc/gofumpt@latest` |
| golangci-lint | 複数リンター + フォーマッター | `go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest` |

## 重要な注意事項

- ✅ プロジェクトの既存設定を優先
- ✅ タスクランナーがあれば使用
- ✅ 変更されたファイルを明示
- ❌ フォーマット実行前に未コミットの変更をコミットまたはスタッシュすることを推奨
