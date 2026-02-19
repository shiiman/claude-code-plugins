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
| git-add-commit | 「コミット」「コミットして」 | セキュリティチェック + ステージング + コミット |
| git-worktree | 「worktree 作成」「gtr list」 | gtr で worktree を管理 |
| git-worktree-setup | 「worktree セットアップ」「gtr 設定」 | gtr インストールと .gtrconfig 設定 |

## 必要条件

- git がインストール済み

### git-worktree / git-worktree-setup スキル

- gtr (git-worktree-runner) がインストール済み
  - インストール: https://github.com/coderabbitai/git-worktree-runner
  - worktree スキルは gtr 固有の機能（`--editor`, `--ai`, `.gtrconfig` など）を利用するため、`git worktree` 単体では完全に代替できません

## GitHub 操作について

Issue 管理、PR 管理、GitHub Actions デバッグ、ブランチ作成（Issue連携）等の GitHub API / gh CLI を使用する操作は `shiiman-github` プラグインをご利用ください。

```bash
claude plugin install shiiman-github@shiiman-claude-code-plugins
```

## バージョン履歴

- v3.0.0: git-commit → git-add-commit にリネーム、git-gitignore-check を統合、git-commit-message-setup を削除、git-worktree を gtr v2.1.0 対応に更新、git-gtrconfig-setup → git-worktree-setup にリネーム（破壊的変更）
- v2.0.0: shiiman-github プラグインへのスキル分離に伴い、GitHub 操作スキルを移動。全スキルを `git-` プレフィックス付きにリネーム（破壊的変更）
- v1.9.2: worktree / gtrconfig スキル追加
- v1.9.1: `branch-create` と `pr-create` のベースブランチ解決を `main` 固定から `gh repo view --json defaultBranchRef` 方式へ変更。`commit` の注意事項もデフォルトブランチ基準へ更新
