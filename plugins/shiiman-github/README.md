# shiiman-github

GitHub 操作プラグイン

## 概要

GitHub API / gh CLI を使った GitHub 操作スキル集。Issue 管理、PR 管理、GitHub Actions デバッグ、リポジトリ設定などを提供します。

## インストール

```bash
claude plugin install shiiman-github@shiiman-claude-code-plugins
```

## 機能

### スキル

| スキル                 | トリガー例                    | 説明                                          |
| ---------------------- | ----------------------------- | --------------------------------------------- |
| github-branch-create   | 「ブランチ作成」              | Issue 番号に基づいた feature ブランチ自動作成 |
| github-setup           | 「GitHub 設定をセットアップ」 | GitHub リポジトリ設定ファイルのセットアップ   |
| github-issue-create    | 「Issue 作成」                | タスクを分割して GitHub Issue を作成          |
| github-issue-update    | 「Issue 更新」                | Issue の状態を更新                            |
| github-issue-list      | 「Issue 一覧」                | オープン Issue の一覧を優先順位付きで表示     |
| github-pr-create       | 「PR 作成」                   | PR を作成または更新                           |
| github-pr-review       | 「PR レビュー」               | PR をレビュー                                 |
| github-pr-review-check | 「レビュー対応」              | PR に付いたレビューコメントを確認し対応       |
| github-pr-list         | 「PR 一覧」                   | オープン PR の一覧を表示                      |
| github-pr-approve      | 「PR 承認」                   | PR を承認                                     |
| github-actions-debug   | 「Actions エラー」            | GitHub Actions のエラーを調査                 |

### エージェント

| Agent             | 説明                                              |
| ----------------- | ------------------------------------------------- |
| reviewer          | PR の全体レビュー（品質、設計、可読性）           |
| security-check    | セキュリティ脆弱性チェック（OWASP Top 10）        |
| performance-check | パフォーマンス問題チェック（N+1、メモリリーク）   |
| issue-manager     | Issue 管理全般（作成、更新、検索）                |
| pr-manager        | PR 管理全般（作成、レビュー依頼、マージ）         |
| debugger          | GitHub Actions ワークフローエラーの調査・修正提案 |

## 必要条件

- GitHub CLI (`gh`) がインストール済み
- `gh auth login` で認証済み

## 権限設定

このプラグインは以下のコマンドを許可・拒否します：

**許可:**

- `gh issue`, `gh pr`, `gh repo view`, `gh api`
- `gh workflow`, `gh run`
- `git status`, `git log`, `git diff`, `git branch`, `git show`
- `git fetch`, `git pull`, `git add`, `git commit`
- `git checkout`, `git switch`

**拒否（危険なコマンド）:**

- `git push --force`, `git push -f`
- `git reset --hard`
- `git clean -fd`
- `gh repo delete`

## トラブルシューティング

### GitHub API レート制限

エラー: `API rate limit exceeded`

**対処法:**

1. 待機: 制限リセットまで待つ（通常1時間）
2. 確認: `gh api rate_limit` でリセット時間を確認
3. 認証: Personal Access Token を使用してレート制限を緩和

### 認証エラー

エラー: `gh: Not logged in`

**対処法:**

```bash
gh auth login
gh auth status  # 認証状態確認
```

### 権限エラー

エラー: `Resource not accessible by integration`

**対処法:**

- リポジトリへの適切な権限があるか確認
- Organization リポジトリの場合は SSO 認証を確認
