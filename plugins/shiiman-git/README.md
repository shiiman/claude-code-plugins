# shiiman-git

Git/GitHub 管理プラグイン

## 概要

GitHub リポジトリのセットアップ、コミット管理、Issue 管理、PR 管理、Actions 管理を統合的にサポートします。

> **Note**: 開発ワークフロー（Issue → 実装 → PR）は `shiiman-workflow` プラグインに移行しました。

## インストール

```bash
claude plugin install shiiman-git@shiiman-claude-code-plugins
```

## 機能

### スキル

| スキル | トリガー例 | 説明 |
|--------|------------|------|
| github-setup | 「GitHub 設定をセットアップ」 | .github 設定ファイルを一括生成 |
| commit-message-setup | 「コミットメッセージ設定」 | コミットメッセージ命名規則を設定 |
| commit | 「コミット」「コミットして」 | 変更をコミットしてプッシュ |
| branch-create | 「ブランチ作成」 | `gh` で取得したデフォルトブランチから feature/[issue番号] ブランチを作成 |
| gitignore-check | 「gitignore チェック」 | .gitignore に追加すべきファイルを確認 |
| issue-create | 「Issue 作成」 | タスクを分割して Issue を作成 |
| issue-update | 「Issue 更新」 | Issue の状態を更新 |
| issue-list | 「Issue 一覧」 | オープン Issue を表示 |
| pr-create | 「PR 作成」 | デフォルトブランチとの差分を確認して PR を作成し関連 Issue を参照 |
| pr-review | 「PR レビュー」 | **他者の PR** をレビューしてコメント投稿 |
| pr-review-check | 「レビュー対応」 | **自分の PR** に付いたコメントを確認・修正 |
| pr-list | 「PR 一覧」 | オープン PR を表示 |
| pr-approve | 「PR 承認」 | PR を approve |
| actions-debug | 「Actions エラー」 | GitHub Actions のエラーを調査 |
| worktree | 「worktree 作成」「gtr list」 | gtr で worktree を管理 |
| gtrconfig-setup | 「gtrconfig 設定」 | .gtrconfig を生成 |

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

### worktree スキル

- gtr (git-worktree-runner) がインストール済み
  - インストール: https://github.com/coderabbitai/git-worktree-runner
  - worktree スキルは gtr 固有の機能（`--editor`, `--ai`, `.gtrconfig` など）を利用するため、`git worktree` 単体では完全に代替できません

## 権限設定

このプラグインは以下のコマンドを許可・拒否します：

**許可:**

- `git status`, `git log`, `git diff`, `git branch`, `git show`
- `git fetch`, `git pull`, `git add`, `git commit`
- `git checkout`, `git switch`
- `git gtr`, `git worktree` (worktree 管理)
- `gh issue`, `gh pr`, `gh repo view`, `gh api`
- `gh workflow`, `gh run`

**拒否（危険なコマンド）:**

- `git push --force`, `git push -f`
- `git reset --hard`
- `git clean -fd`
- `gh repo delete`

## ワークフローガイド

> **開発フローについて**: Issue → 実装 → PR の自動開発フローは `shiiman-workflow` プラグインをご利用ください。
> - `workflow-single-issue`: シングルエージェントで Issue から PR まで
> - `workflow-multi-issue`: マルチエージェントで並列実行
> - `workflow-single` / `workflow-multi`: Issue/PR なしの軽量フロー

### 手動フロー

個別のスキルを使う場合:

1. **作業開始時**
   - `issue-create` → タスクを Issue 化
   - `branch-create` → Issue 番号でブランチ作成

2. **コミット時**
   - `gitignore-check` → 機密ファイルチェック
   - `commit` → コミット＆プッシュ

3. **PR 作成時**
   - `pr-create` → PR 作成

4. **レビュー時**
   - `pr-review` → **他者の PR** をレビュー（レビュアーとして）
   - `pr-review-check` → **自分の PR** のレビューコメントに対応（作成者として）

5. **完了時**
   - `pr-approve` → PR 承認

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

## バージョン履歴

- v1.9.1: `branch-create` と `pr-create` のベースブランチ解決を `main` 固定から `gh repo view --json defaultBranchRef` 方式へ変更。`commit` の注意事項もデフォルトブランチ基準へ更新
