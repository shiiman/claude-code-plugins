# shiiman-git

Git ローカル操作プラグイン

## 概要

Git のローカル操作に特化したスキルを提供します。
GitHub API や gh CLI を使用する操作は [`shiiman-github`](../shiiman-github/) プラグインをご利用ください。

## インストール

```bash
claude plugin install shiiman-git@shiiman-claude-code-plugins
```

## 機能

### スキル

| スキル | トリガー例 | 説明 |
|--------|------------|------|
| git-commit | 「コミット」「コミットして」 | 変更をコミットしてプッシュ |
| git-worktree | 「worktree 作成」「gtr list」 | gtr で worktree を管理 |
| git-gitignore-check | 「gitignore チェック」 | .gitignore に追加すべきファイルを確認 |
| git-commit-message-setup | 「コミットメッセージ設定」 | コミットメッセージ命名規則を設定 |
| git-gtrconfig-setup | 「gtrconfig 設定」 | .gtrconfig を生成 |

## 必要条件

- git がインストール済み

### git-worktree / git-gtrconfig-setup スキル

- gtr (git-worktree-runner) がインストール済み
  - インストール: https://github.com/coderabbitai/git-worktree-runner
  - worktree スキルは gtr 固有の機能（`--editor`, `--ai`, `.gtrconfig` など）を利用するため、`git worktree` 単体では完全に代替できません

## GitHub 操作について

Issue 管理、PR 管理、GitHub Actions デバッグ、ブランチ作成（Issue連携）等の GitHub API / gh CLI を使用する操作は `shiiman-github` プラグインをご利用ください。

```bash
claude plugin install shiiman-github@shiiman-claude-code-plugins
```

## バージョン履歴

- v2.0.0: shiiman-github プラグインへのスキル分離に伴い、GitHub 操作スキルを移動。全スキルを `git-` プレフィックス付きにリネーム（破壊的変更）
- v1.9.2: worktree / gtrconfig スキル追加
- v1.9.1: `branch-create` と `pr-create` のベースブランチ解決を `main` 固定から `gh repo view --json defaultBranchRef` 方式へ変更。`commit` の注意事項もデフォルトブランチ基準へ更新
