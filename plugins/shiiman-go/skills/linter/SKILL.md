# Linter

Go コードの静的解析を実行するスキル。

## トリガー

- 「lint して」「静的解析」「golangci-lint」
- 「コードチェック」「lint 実行」「警告を確認」「lint エラー確認」

## 実行内容

`/shiiman-go:lint` コマンドを実行します。

## Claude への指示

### 実行手順

1. **コマンド実行**

   `/shiiman-go:lint` コマンドの内容に従って実行:

   - タスクランナー検出（Taskfile.yml, Makefile）
   - 設定ファイル検出（.golangci.yml）
   - 静的解析実行（golangci-lint run --fix）
   - 結果レポート

2. **出力形式**

   lint.md の「結果レポート」形式に従う

### 注意事項

- プロジェクトの既存設定を優先
- 自動修正可能な問題は修正
- 手動修正が必要な問題は詳細を報告
