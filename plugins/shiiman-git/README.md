# shiiman-git

Git/GitHub ワークフロー管理プラグイン

## 概要

GitHub リポジトリのセットアップ、コミット管理、Issue 管理、PR 管理、Actions 管理を統合的にサポートします。

## インストール

```bash
/shiiman-plugin:install shiiman-git
```

## 機能

### コマンド

| コマンド | 説明 |
|----------|------|
| `/shiiman-git:setup` | GitHub 設定ファイルを一括生成 |
| `/shiiman-git:commit-message` | コミットメッセージ命名規則の設定・表示 |
| `/shiiman-git:issue-list` | オープン Issue 一覧を優先順位付きで表示 |
| `/shiiman-git:pr-list` | オープン PR 一覧を優先順位付きで表示 |

### スキル

| スキル | トリガー例 | 説明 |
|--------|------------|------|
| setup-runner | 「GitHub 設定をセットアップ」 | .github 設定ファイルを一括生成 |
| commit-messenger | 「コミットメッセージ設定」 | コミットメッセージ命名規則を設定 |
| branch-creator | 「ブランチ作成」 | feature/[issue番号] ブランチを作成 |
| gitignore-checker | 「gitignore チェック」 | .gitignore に追加すべきファイルを確認 |
| issue-creator | 「Issue 作成」 | タスクを分割して Issue を作成 |
| issue-updater | 「Issue 更新」 | Issue の状態を更新 |
| issue-lister | 「Issue 一覧」 | オープン Issue を表示 |
| pr-creator | 「PR 作成」 | PR を作成し関連 Issue を参照 |
| pr-reviewer | 「PR レビュー」 | PR をレビューして GitHub にコメント |
| pr-review-responder | 「レビュー対応」 | レビュー指摘を修正 |
| pr-lister | 「PR 一覧」 | オープン PR を表示 |
| pr-approver | 「PR 承認」 | PR を approve |
| actions-debugger | 「Actions エラー」 | GitHub Actions のエラーを調査 |

### エージェント

| Agent | 説明 |
|-------|------|
| reviewer | PR の全体レビュー（品質、設計、可読性） |
| security-check | セキュリティ脆弱性チェック（OWASP Top 10） |
| performance-check | パフォーマンス問題チェック（N+1、メモリリーク） |
| issue-manager | Issue 管理全般（作成、更新、検索） |
| pr-manager | PR 管理全般（作成、レビュー依頼、マージ） |

## Setup で生成されるファイル

| ファイル | 説明 |
|----------|------|
| `.github/ISSUE_TEMPLATE/config.yml` | Issue テンプレート設定 |
| `.github/ISSUE_TEMPLATE/bug-report.yml` | バグ報告テンプレート |
| `.github/ISSUE_TEMPLATE/feature-request.yml` | 機能リクエストテンプレート |
| `.github/ISSUE_TEMPLATE/improvement.yml` | 改善提案テンプレート |
| `.github/pull_request_template.md` | PR テンプレート |
| `.github/copilot-instructions.md` | GitHub Copilot 設定 |
| `.github/labels.yml` | ラベル定義 |
| `.github/labeler.yml` | 自動ラベル付けルール |
| `.github/workflows/sync-labels.yml` | ラベル同期 workflow |
| `.github/workflows/labeler.yml` | 自動ラベル付け workflow |

## 必要条件

- GitHub CLI (`gh`) がインストール済み
- `gh auth login` で認証済み

## 権限設定

このプラグインは以下のコマンドを許可・拒否します：

**許可:**

- `git status`, `git log`, `git diff`, `git branch`, `git show`
- `git fetch`, `git pull`, `git add`, `git commit`
- `git checkout`, `git switch`
- `gh issue`, `gh pr`, `gh repo view`, `gh api`
- `gh workflow`, `gh run`

**拒否（危険なコマンド）:**

- `git push --force`, `git push -f`
- `git reset --hard`
- `git clean -fd`
- `gh repo delete`
