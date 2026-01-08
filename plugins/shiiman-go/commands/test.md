# Test

Go プロジェクトのユニットテストを実行します。カバレッジ計測、特定パッケージ/ファイルのテスト、レースコンディション検出に対応。

## 使い方

```bash
/shiiman-go:test
/shiiman-go:test ./internal/handler
/shiiman-go:test --cover
/shiiman-go:test --race
/shiiman-go:test --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `--cover` | カバレッジ計測を有効化 |
| `--race` | データレース検出を有効化 |
| `--help` | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### 実行手順

#### 1. タスクランナー検出

```bash
ls -la Taskfile.yml Makefile 2>/dev/null
```

**検出されるタスク名の例**:
- `test`, `test-unit`, `go-test`
- `test:unit`, `unit-test`

#### 2. テスト実行

```bash
# タスクランナーがある場合
task test
make test

# タスクランナーがない場合
go test ./...

# カバレッジ付き
go test -cover ./...

# カバレッジレポート生成
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out

# レースコンディション検出
go test -race ./...

# 特定パッケージのテスト
go test -v ./internal/handler

# 特定テストケースのみ
go test -v -run TestCreateUser ./internal/handler
```

#### 3. 結果レポート

```
✅ テスト完了

実行パッケージ数: {N}
実行テスト数: {M}
成功: {S}
失敗: {F}
スキップ: {K}
実行時間: {T}s

カバレッジ: {C}%

失敗したテスト:
- {パッケージ/テスト名}
  エラー: {エラーメッセージ}
```

### テスト作成支援

テストコードの作成が必要な場合は、test-writer エージェントが以下をサポート:

- テーブル駆動テストの作成
- t.Parallel() による並行テスト
- モック実装（testify/mock, gomock）
- テストデータ管理（testdata ディレクトリ）

### 段階的テスト実行戦略

効率的なデバッグのため、以下の順序でテストを実行:

1. **特定テストケース** - `go test -v -run TestXxx ./path`
2. **特定テストファイル** - 対象ファイルのみ
3. **特定パッケージ** - `go test -v ./internal/handler`
4. **プロジェクト全体** - `go test ./...`

### 注意事項

- **`-race` フラグ**: 実行速度が遅くなるため、開発時のみ使用推奨
- **テストキャッシュ**: キャッシュを無効化するには `-count=1` を使用
- **並行テスト**: `t.Parallel()` を使用して独立したテストを並行実行可能
