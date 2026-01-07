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
| `/shiiman-git:dev-flow` | **Issue → 実装 → PR を自動実行** |
| `/shiiman-git:setup` | GitHub 設定ファイルを一括生成 |
| `/shiiman-git:commit-message` | コミットメッセージ命名規則の設定・表示 |
| `/shiiman-git:issue-list` | オープン Issue 一覧を優先順位付きで表示 |
| `/shiiman-git:pr-list` | オープン PR 一覧を優先順位付きで表示 |

### スキル

| スキル | トリガー例 | 説明 |
|--------|------------|------|
| setup-runner | 「GitHub 設定をセットアップ」 | .github 設定ファイルを一括生成 |
| commit-messenger | 「コミットメッセージ設定」 | コミットメッセージ命名規則を設定 |
| committer | 「コミット」「コミットして」 | 変更をコミットしてプッシュ |
| branch-creator | 「ブランチ作成」 | feature/[issue番号] ブランチを作成 |
| gitignore-checker | 「gitignore チェック」 | .gitignore に追加すべきファイルを確認 |
| issue-creator | 「Issue 作成」 | タスクを分割して Issue を作成 |
| issue-updater | 「Issue 更新」 | Issue の状態を更新 |
| issue-lister | 「Issue 一覧」 | オープン Issue を表示 |
| pr-creator | 「PR 作成」 | PR を作成し関連 Issue を参照 |
| pr-reviewer | 「PR レビュー」 | **他者の PR** をレビューしてコメント投稿 |
| pr-review-checker | 「レビュー対応」 | **自分の PR** に付いたコメントを確認・修正 |
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

## ワークフローガイド

### 自動開発フロー（推奨）

`/shiiman-git:dev-flow` を使うと、以下のフローを自動実行します:

```
Issue作成 → ブランチ作成 → 実装（進捗をIssueに反映）→ 自己レビュー → [確認] → コミット → プッシュ → PR作成
```

**サブタスク進捗管理**: 実装中、サブタスク完了時にバックグラウンドで Issue のチェックボックスを自動更新します。

**3つの実行モード:**

| モード | コマンド | 説明 |
|--------|----------|------|
| 計画書実行 | `/shiiman-git:dev-flow` | 最新の計画書から直接実行（デフォルト） |
| 計画書作成 | `/shiiman-git:dev-flow --plan` | plan mode で計画書を新規作成してから実行 |
| 直接実行 | `/shiiman-git:dev-flow タスク説明` | 計画書なしで直接実行（簡単なタスク用） |

### 手動フロー

個別のスキルを使う場合:

1. **作業開始時**
   - `issue-creator` → タスクを Issue 化
   - `branch-creator` → Issue 番号でブランチ作成

2. **コミット時**
   - `gitignore-checker` → 機密ファイルチェック
   - `committer` → コミット＆プッシュ

3. **PR 作成時**
   - `pr-creator` → PR 作成

4. **レビュー時**
   - `pr-reviewer` → **他者の PR** をレビュー（レビュアーとして）
   - `pr-review-checker` → **自分の PR** のレビューコメントに対応（作成者として）

5. **完了時**
   - `pr-approver` → PR 承認

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
