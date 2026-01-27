# shiiman-git

Git/GitHub ワークフロー管理プラグイン

## 概要

GitHub リポジトリのセットアップ、コミット管理、Issue 管理、PR 管理、Actions 管理を統合的にサポートします。

## インストール

```bash
/shiiman-plugin:install shiiman-git
```

## 機能

### スキル

| スキル | トリガー例 | 説明 |
|--------|------------|------|
| run-dev-flow | 「開発フロー」「dev-flow」 | **Issue → 実装 → PR を自動実行** |
| setup-github | 「GitHub 設定をセットアップ」 | .github 設定ファイルを一括生成 |
| setup-commit-message | 「コミットメッセージ設定」 | コミットメッセージ命名規則を設定 |
| commit | 「コミット」「コミットして」 | 変更をコミットしてプッシュ |
| create-branch | 「ブランチ作成」 | feature/[issue番号] ブランチを作成 |
| check-gitignore | 「gitignore チェック」 | .gitignore に追加すべきファイルを確認 |
| create-issue | 「Issue 作成」 | タスクを分割して Issue を作成 |
| update-issue | 「Issue 更新」 | Issue の状態を更新 |
| list-issues | 「Issue 一覧」 | オープン Issue を表示 |
| create-pr | 「PR 作成」 | PR を作成し関連 Issue を参照 |
| review-pr | 「PR レビュー」 | **他者の PR** をレビューしてコメント投稿 |
| check-pr-review | 「レビュー対応」 | **自分の PR** に付いたコメントを確認・修正 |
| list-prs | 「PR 一覧」 | オープン PR を表示 |
| approve-pr | 「PR 承認」 | PR を approve |
| debug-actions | 「Actions エラー」 | GitHub Actions のエラーを調査 |

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

`run-dev-flow` スキルを使うと、以下のフローを自動実行します:

```
Issue作成 → ブランチ作成 → 実装 → 自己レビュー → [確認] → Issue更新 → コミット → プッシュ → PR作成
```

**Issue 進捗管理**:

- 実装中: サブタスク完了時にバックグラウンドで Issue のチェックボックスを更新（オプション）
- 確認後: 全チェックボックスを同期実行で確実に完了状態に更新

**3つの実行モード:**

| モード | 起動方法 | 説明 |
|--------|----------|------|
| 計画書実行 | 「開発フロー」 | 最新の計画書から直接実行（デフォルト） |
| 計画書作成 | 「開発フロー --plan」 | plan mode で計画書を新規作成してから実行 |
| 直接実行 | 「開発フロー タスク説明」 | 計画書なしで直接実行（簡単なタスク用） |

### 手動フロー

個別のスキルを使う場合:

1. **作業開始時**
   - `create-issue` → タスクを Issue 化
   - `create-branch` → Issue 番号でブランチ作成

2. **コミット時**
   - `check-gitignore` → 機密ファイルチェック
   - `commit` → コミット＆プッシュ

3. **PR 作成時**
   - `create-pr` → PR 作成

4. **レビュー時**
   - `review-pr` → **他者の PR** をレビュー（レビュアーとして）
   - `check-pr-review` → **自分の PR** のレビューコメントに対応（作成者として）

5. **完了時**
   - `approve-pr` → PR 承認

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
