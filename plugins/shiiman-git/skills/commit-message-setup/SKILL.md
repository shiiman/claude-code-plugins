---
name: commit-message-setup
description: コミットメッセージの命名規則を設定する。「コミットメッセージ設定」「コミット規則」「コミット形式を設定」「コミットメッセージルール」「commit message 設定」「コミットの書き方を設定」「コミットフォーマット」などで起動。プロジェクト固有のコミットメッセージルールを管理。
allowed-tools: [Read, Write, Bash, AskUserQuestion]
argument-hint: "[--set|--help]"
---

# Setup Commit Message

コミットメッセージの命名規則を設定・表示します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/commit-message-setup - コミットメッセージ設定

概要:
  コミットメッセージの命名規則を設定・表示する。
  Conventional Commits、日本語プレフィックス、カスタム形式に対応。

使用方法:
  /commit-message-setup [オプション]

オプション:
  --set   命名規則を対話的に設定
  --help  このヘルプを表示

例:
  /commit-message-setup          # 現在の設定を表示
  /commit-message-setup --set    # 命名規則を対話的に設定
```

## 実行手順

### `--set` オプションがある場合

1. プロジェクトの `.claude/settings.json` を読み込み
2. 以下を順番に聞く:

**コミットメッセージ形式**:

| 形式 | 例 |
|------|-----|
| Conventional Commits（日本語） | `feat: 新機能を追加` |
| 日本語プレフィックス | `新機能: ユーザー認証を追加` |
| カスタム | ユーザー定義 |

**言語・行数ルール**:

- **日本語で記述**
- **1行で簡潔に**（50文字以内推奨）

**使用するプレフィックス**（Conventional Commits の場合）:

- `feat` - 新機能
- `fix` - バグ修正
- `docs` - ドキュメント
- `refactor` - リファクタリング
- `chore` - その他
- `test` - テスト
- `style` - スタイル修正
- `perf` - パフォーマンス改善

**Issue 参照形式**:

| 形式 | 例 |
|------|-----|
| 末尾括弧 | `feat: 機能追加 (#123)` |
| 先頭 | `#123 feat: 機能追加` |
| なし | Issue 参照しない |

3. 設定を `.claude/settings.json` の `git.commitMessage` に保存

### オプションなしの場合

- 現在の設定を表示
- 設定がない場合はデフォルト設定を表示

## 設定ファイル形式

`.claude/settings.json`:

```json
{
  "git": {
    "commitMessage": {
      "format": "conventional",
      "language": "ja",
      "singleLine": true,
      "prefixes": ["feat", "fix", "docs", "refactor", "chore", "test"],
      "issueReference": true,
      "issueFormat": "(#N)"
    }
  }
}
```

## 出力フォーマット

```
## コミットメッセージ設定

形式: Conventional Commits
言語: 日本語
行数: 1行
プレフィックス: feat, fix, docs, refactor, chore, test
Issue 参照: あり (末尾括弧形式)

### 例

feat: ユーザー認証機能を追加 (#123)
fix: ログイン時のエラーを修正 (#124)
docs: READMEを更新
```

## 重要な注意事項

- ✅ プロジェクトごとに設定を保存
- ✅ チームで統一したルールを設定可能
- ❌ 設定なしでもコミットは可能（推奨設定を表示するのみ）
