---
name: shiiman-github:github-actions-debug
description: GitHub Actions のワークフロー実行エラーを調査し、原因を特定して解決策を提案する。「Actions エラー」「ワークフロー失敗」「CI が落ちた」「ビルド失敗」「テスト失敗」「Actions を調べて」「CI のエラーを見て」などで起動。失敗したジョブのログを分析し、具体的な修正方法を提示。
allowed-tools: [Read, Bash, Grep, Glob]
argument-hint: "[run番号] [--help]"
context: fork
agent: shiiman-github:debugger
---

# Debug Actions

GitHub Actions のワークフロー実行エラーを調査し、原因を特定して解決策を提案します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-github:github-actions-debug - GitHub Actions エラー調査

概要:
  GitHub Actions のワークフロー実行エラーを調査する。
  失敗ジョブの特定、ログ取得、原因分析、修正提案を実行。

使用方法:
  /shiiman-github:github-actions-debug [run番号] [オプション]

オプション:
  --help  このヘルプを表示

例:
  /shiiman-github:github-actions-debug                    # 最新の失敗 run を調査
  /shiiman-github:github-actions-debug 12345678901        # 指定 run 番号を調査
```

## ワークフロー

### 1. run 番号の特定

- `$ARGUMENTS` に run 番号が指定されている場合: その run を調査
- 指定がない場合: 最新の失敗 run を自動検出

```bash
# 最新の失敗 run を取得
gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId'

# 特定の PR に関連する Run を確認
gh pr checks {pr番号}
```

### 2. ワークフロー実行情報の取得

```bash
gh run view {run_id}
```

### 3. 失敗ジョブの特定

```bash
# 失敗したジョブのみ抽出
gh run view {run_id} --json jobs --jq '.jobs[] | select(.conclusion == "failure") | {name, conclusion}'
```

### 4. エラーログの取得・分析

```bash
# 失敗したステップのログを取得
gh run view {run_id} --log-failed
```

ログから以下を特定:

- エラーメッセージ
- 失敗したステップ
- 関連するファイル・行番号

### 5. 解決策の提案

エラーパターンに基づいて修正を提案:

- 具体的な修正コード
- 設定変更の提案
- ローカルでの再現方法

## よくあるエラーパターン

### テスト失敗

```bash
gh run view {run_id} --log-failed | grep -A 10 "FAIL"
```

**対処法**:

- 失敗したテストケースを特定
- ローカルで再現
- テストまたはコードを修正

### ビルドエラー

```bash
gh run view {run_id} --log-failed | grep -A 5 "error"
```

**対処法**:

- コンパイルエラーを特定
- 型エラーや構文エラーを修正
- 依存関係を確認

### 依存関係エラー

```bash
gh run view {run_id} --log-failed | grep -A 5 "npm ERR!"
```

**対処法**:

- `package-lock.json` を更新
- 依存関係のバージョンを確認
- キャッシュをクリア

### 権限エラー

**対処法**:

- workflow の permissions を確認
- GITHUB_TOKEN の権限を確認
- secrets の設定を確認

## 出力形式

```
## GitHub Actions エラー調査結果

**Run ID**: {run_id}
**ワークフロー**: {workflow_name}
**ステータス**: ❌ failure

### 失敗したジョブ

| ジョブ | ステップ | 原因 |
|--------|----------|------|
| test | Run tests | テスト失敗 |

### エラー詳細

{エラーログの抜粋}

### 修正提案

1. {具体的な修正方法}

### 参考コマンド

{ローカルでの再現コマンド}
```

## 重要な注意事項

- ✅ run 番号未指定時は最新の失敗 run を自動検出
- ✅ エラーログを詳細に分析
- ✅ 具体的な修正提案を含める
- ✅ ローカルでの再現方法を提示
- ✅ ログが長い場合は重要なエラー部分のみ抽出して報告
- ❌ 漠然とした提案を避ける
- ❌ 関係ないエラーを混同しない
