# shiiman-workflow

開発ワークフロー自動化プラグイン

## 概要

シングルエージェント/マルチエージェントでの開発フローを提供します。
Issue 管理付き・なしの両方のパターンに対応。

## インストール

```bash
claude plugin install shiiman-workflow@shiiman-claude-code-plugins
```

## 機能比較

| スキル                    | Issue | ブランチ | PR  | エージェント | 用途                                                        |
| ------------------------- | ----- | -------- | --- | ------------ | ----------------------------------------------------------- |
| workflow-single-issue     | ✅    | ✅       | ✅  | シングル     | 標準的な開発フロー                                          |
| workflow-single           | ❌    | ✅       | ❌  | シングル     | 軽量な実装タスク                                            |
| workflow-multi-issue      | ✅    | ✅       | ✅  | マルチ       | 大規模な開発タスク                                          |
| workflow-multi            | ❌    | ✅/❌    | ❌  | マルチ       | 並列実装タスク（`--no-git` / 自動判定で非git対応）          |
| workflow-agent-team-issue | ✅    | ✅       | ✅  | Agent Team   | Agent Team で Issue から PR まで                            |
| workflow-agent-team       | ❌    | ✅/❌    | ❌  | Agent Team   | Agent Team 軽量並列実装（`--no-git` / 自動判定で非git対応） |

## スキル

### workflow-single-issue

Issue から PR まで自動実行するシングルエージェントフロー。

**トリガー例**: 「シングル Issue フロー」「Issue から PR まで」「workflow-single-issue」

**フロー**:

```
計画書 → Issue → ブランチ → 実装 → レビュー → コミット → PR
```

**実行モード**:

- 引数なし: 既存の計画書から実行
- `--plan`: 計画書を作成してから実行
- `タスク説明`: 計画書なしで直接実行

### workflow-single

Issue/PR なしで軽量に実行するフロー。

**トリガー例**: 「シングルフロー」「軽量フロー」「workflow-single」

**フロー**:

```
計画書 → ブランチ → 実装 → レビュー → コミットメッセージ出力
```

**特徴**:

- Issue を作成しない
- ブランチを作成する（feature/{slug} 形式）
- PR を作成しない
- コミットメッセージを出力して終了（手動でコミット）

### workflow-multi-issue

MCP マルチエージェントで並列実行する開発フロー。

**トリガー例**: 「マルチ Issue フロー」「並列 Issue 開発」「workflow-multi-issue」

**前提条件**:

- multi-agent-mcp インストール済み
- tmux インストール済み

**フロー**:

```
計画書 → Issue → MCP初期化 → 並列実行 → 統合 → レビュー → コミット → PR
```

**階層**:

- Owner（呼び出し元）: 全体を統括
- Admin（1）: タスク分配と Worker 管理
- Worker（max 16）: 各サブタスクを並列実行

### workflow-multi

MCP マルチエージェントで並列実行する軽量フロー。

**トリガー例**: 「マルチフロー」「並列フロー」「workflow-multi」

**前提条件**:

- multi-agent-mcp インストール済み
- tmux インストール済み

**フロー**:

```
git モード: 計画書 → ブランチ → MCP初期化 → 並列実行 → 統合 → レビュー → コミットメッセージ出力
no-git モード: 計画書 → MCP初期化(enable_git=false) → 並列実行 → 統合 → レビュー
```

**特徴**:

- Issue を作成しない
- git 管理プロジェクトではブランチを作成する（feature/{slug} 形式）
- `--no-git` 指定時、または `git rev-parse --is-inside-work-tree` 失敗時は no-git モードへ切替
- no-git モードでは `init_tmux_workspace(..., enable_git=false)` で実行
- PR を作成しない
- 複数 Worker が並列実行
- git モードでは統合後にコミットメッセージを出力

### workflow-agent-team-issue

Agent Team で Issue から PR まで並列実行する開発フロー。

**トリガー例**: 「workflow-agent-team-issue」「エージェントチーム Issue フロー」「Agent Team Issue」

**フロー**:

```text
計画書 → Issue → ブランチ → ターミナル + tmux 起動 → Agent Team 実装 → レビュー → コミット → PR
```

**特徴**:

- `workflow-multi-issue` の MCP 使用部分を Agent Team 実行に置き換え
- `claude --dangerously-skip-permissions` で Agent Team 実行
- ターミナル起動は `plugins/shiiman-workflow/scripts/open_tmux_terminal.sh` を使用（既存起動時は新規タブ、未起動時は新規ウィンドウ先頭タブ）
- 承認時クリーンアップは `plugins/shiiman-workflow/scripts/cleanup_tmux_terminal.sh` を使用（tmux は常に終了、window 起動時のみ terminal をクローズ）
- ターミナル選択順は `ghostty -> iterm2 -> Terminal.app -> current shell`
- tmux メッセージ送信先 target は固定値ではなく tmux 実値から動的解決
- 2 つの Agent Team スキルで共通利用する送信スクリプトは `plugins/shiiman-workflow/scripts/send_claude_tmux_message.sh` を使用

### workflow-agent-team

Agent Team で Issue/PR なしに並列実行する軽量フロー。

**トリガー例**: 「workflow-agent-team」「エージェントチームフロー」「Agent Team で実装」

**フロー**:

```text
git モード: 計画書 → ブランチ → ターミナル + tmux 起動 → Agent Team 実装 → レビュー → コミットメッセージ出力
no-git モード: 計画書 → ターミナル + tmux 起動 → Agent Team 実装 → レビュー
```

**特徴**:

- `workflow-multi` の MCP 使用部分を Agent Team 実行に置き換え
- `claude --dangerously-skip-permissions` で Agent Team 実行
- `--no-git` 指定時、または `git rev-parse --is-inside-work-tree` 失敗時は no-git モードへ切替
- no-git モードではブランチ作成と push 前提手順を行わない
- 問題時は Agent Team に再指示してループ可能
- ターミナル起動は `plugins/shiiman-workflow/scripts/open_tmux_terminal.sh` を使用（既存起動時は新規タブ、未起動時は新規ウィンドウ先頭タブ）
- 承認時クリーンアップは `plugins/shiiman-workflow/scripts/cleanup_tmux_terminal.sh` を使用（tmux は常に終了、window 起動時のみ terminal をクローズ）
- ターミナル選択順は `ghostty -> iterm2 -> Terminal.app -> current shell`
- tmux メッセージ送信先 target は固定値ではなく tmux 実値から動的解決
- 2 つの Agent Team スキルで共通利用する送信スクリプトは `plugins/shiiman-workflow/scripts/send_claude_tmux_message.sh` を使用

## 必要条件

### 全スキル共通

- GitHub CLI (`gh`) がインストール済み
- `gh auth login` で認証済み

### マルチエージェントスキル（workflow-multi-\*）

- multi-agent-mcp がインストール済み
- tmux がインストール済み

### Agent Team スキル（workflow-agent-team-\*）

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` を有効化
- `CLAUDE_PLUGIN_ROOT` が利用可能なプラグイン実行コンテキストで実行
- `claude` コマンドが利用可能
- tmux がインストール済み
- macOS で Ghostty または iTerm2 を推奨（未導入時は Terminal.app / 現在端末にフォールバック）

## バージョン履歴

- v2.0.0: 全スキルを `workflow-*` 形式にリネーム（破壊的変更）
- v1.8.7: ブランチ作成手順を `main` 固定から `gh repo view --json defaultBranchRef` によるデフォルトブランチ取得へ変更
- v1.8.6: Agent Team Issue の Step 6 送信テンプレート先頭を `Agent Team を作成して` へ修正し、実行意図を明確化
- v1.8.5: `open_tmux_terminal.sh` に `--state-file` を追加し、`cleanup_tmux_terminal.sh` を新規追加。Agent Team 承認時は tmux を常に終了し、window 起動時のみ terminal をクローズする仕様へ変更
- v1.8.4: Agent Team スキルの送信テンプレートを `>|` に統一して `zsh noclobber` を回避。`send_claude_tmux_message.sh` に空ファイルガードを追加
- v1.8.3: Agent Team 承認時のクリーンアップを「送信指示」から「実行側の直接実行」に変更し、依頼テンプレート形式を統一
- v1.8.2: Ghostty 起動フォールバックと tmux target 解決を修正（`0.0` 固定を廃止し実値解決へ変更）
- v1.8.1: Agent Team スキルのターミナル起動を共通化し、既存起動時の新規タブ化と文字化け対策を修正
- v1.8.0: マルチ / Agent Team 軽量フローに `--no-git` と git/no-git 自動分岐を追加（非gitディレクトリ対応）
- v1.7.4: Phase 5 の変更確認手順を統一（`git status --short --branch` + `git diff` + `git diff --cached`）
- v1.7.1: Agent Team スキルを仕様準拠に修正（Ghostty/iTerm2 + tmux + Agent Team 実行フローへ統一）
- v1.5.0: SKILL.md を約 60% スリム化。MCP 側で Admin/Worker 指示を自動生成
- v1.4.0: Worker 数をデフォルト 6、最大 16 に変更。MCP 自動機能（ペルソナ、メモリ、7セクション構造）を統合
- v1.0.0: 初期リリース（shiiman-git の dev-flow から移行）
