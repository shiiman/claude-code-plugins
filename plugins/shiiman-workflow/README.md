# shiiman-workflow

開発ワークフロー自動化プラグイン

## 概要

シングル / マルチエージェント / Agent Team での開発フローを提供します。

**フラグは不要です。** タスクを伝えれば、git の状態・発話内容から実行条件（Issue/PR 連携・計画書・ブランチ・git）を自動判断し、軽微な点は判断して進め、重要な範囲・リスクの判断だけ確認します。実行スタイル（順次 / MCP 並列 / Agent Team 並列）はスキルの選択で決めます。

## インストール

```bash
claude plugin install shiiman-workflow@shiiman-claude-code-plugins
```

## スキル一覧

| スキル                 | 実行スタイル     | Issue/PR 連携      | 用途                                          |
| ---------------------- | ---------------- | ------------------ | --------------------------------------------- |
| single                 | シングル（順次） | 発話・引数から自動 | 1 エージェントで順次実装                      |
| multi                  | MCP マルチ       | 発話・引数から自動 | Owner/Admin/Worker で並列実装（大規模）       |
| agent-team             | Agent Team       | 発話・引数から自動 | tmux + TeamCreate で並列実装                  |
| issue-branch-pr-create | シングル         | 必須（Backward）   | 既存変更から Issue・PR を作成する逆方向フロー |

> **v5.0.0 で `*-issue` 系を統合**: `single-issue` / `multi-issue` / `agent-team-issue` は廃止され、それぞれ `single` / `multi` / `agent-team` に統合されました。現在は発話から操作ごとの許可を判断し、明示がなければ実装・検証のみで終了します。「コミットだけ」はコミットまで、「PR まで」は必要なコミット・通常の push・PR 作成まで進めます。Issue は依頼済みの場合だけ作成します。

## フラグ廃止と自動判断

旧バージョンのフラグは、以下のルールで自動判断します（ユーザーは何も覚える必要がありません）。

| 旧フラグ        | 新しい決め方                                                                                    |
| --------------- | ----------------------------------------------------------------------------------------------- |
| `--no-git`      | `git rev-parse --is-inside-work-tree` で git/no-git を完全自動判定                              |
| `--branch`      | 既定は worktree。「ブランチで」等の発話で branch に切替                                         |
| `--plan`        | 「計画を立てて」等で plan mode / タスク説明あり → 直接 / なし → 既存計画書探索                  |
| `--no-review`   | 既定はレビュー実行。「レビュー不要」等でスキップ（agent-team）                                  |
| `-issue` の有無 | 実装のみが既定。「コミットだけ」「PR まで」「Issue と PR まで」を区別し、許可された操作だけ実行 |

## スキル

### single

1 エージェントで計画書またはタスク説明を順次実装するフロー。

**トリガー例**: 「シングルフロー」「1 人で実装」「順次実装」

**フロー**:

```
[Issue 作成が依頼済みの場合のみ] Issue 作成 →
ブランチ/worktree 作成 → 実装 → セキュリティ＆自己レビュー → 検証 →
[許可された操作だけ] コミット → 通常の push → PR 作成 → 結果報告
```

### multi

multi-agent-mcp の Owner/Admin/Worker で並列実装するフロー。

**トリガー例**: 「マルチフロー」「マルチエージェントで実装」「並列で実装」

**前提条件**: multi-agent-mcp / tmux がインストール済み

**階層**:

- Owner（呼び出し元）: 全体を統括
- Admin（1）: タスク分配と Worker 管理
- Worker（最大 16）: 各サブタスクを並列実行

### agent-team

Agent Team（tmux + TeamCreate）で並列実装するフロー。`multi` の MCP 依存部分を Agent Team 実行に置き換えたもの。

**トリガー例**: 「エージェントチームフロー」「Agent Team で実装」「チームで実装」

**前提条件**: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` / `claude` / `tmux`

**特徴**:

- 並列実行には必ず TeamCreate ツールを使用（Agent ツールではない）
- ターミナル起動は `scripts/open_tmux_terminal.sh`、クリーンアップは `scripts/cleanup_tmux_terminal.sh`、メッセージ送信は `scripts/send_claude_tmux_message.sh` を使用
- ターミナル選択順は `cmux → Ghostty → iTerm2 → Terminal.app → current shell`
- tmux メッセージ送信先 target は固定値ではなく tmux 実値から動的解決
- 既定で完了報告前に `/shiiman-common:review` を実行（「レビュー不要」でスキップ）

### issue-branch-pr-create

既存の変更内容から Issue と PR を作成する Backward（逆方向）フロー。

**トリガー例**: 「変更から Issue と PR」「既存変更を PR に」「Backward フロー」

**フロー**:

```
変更検出 → Issue 作成 → ブランチ/worktree 作成 → コミット → 通常の push → PR 作成
```

**特徴**:

- ワーキングツリーの変更やコミット済み未プッシュの変更から自動で Issue と PR を作成
- 通常フローと逆方向で、既に実装済みの変更を Issue/PR 化する
- 既定はブランチ。「worktree で」の発話で worktree（既存変更は stash 経由で移動）
- PR 作成に必要な通常の feature branch push は実行する。force-push やデフォルトブランチへの push は別の許可が必要

## 依存プラグイン

- **shiiman-git**: コミット操作（`shiiman-git:add-commit`）、worktree の一覧・削除・クリーンアップ（`shiiman-git:worktree`）
- **shiiman-github**: Issue 作成・worktree/ブランチ作成・PR 作成（`shiiman-github:issue-create`、`shiiman-github:worktree-create`、`shiiman-github:branch-create`、`shiiman-github:pr-create`）
- **shiiman-common**: 完了前レビュー（`shiiman-common:review`、agent-team で使用）

## 必要条件

### 全スキル共通

- GitHub CLI (`gh`) がインストール済み
- `gh auth login` で認証済み

### multi の追加要件

- multi-agent-mcp がインストール済み
- tmux がインストール済み

### agent-team の追加要件

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` を有効化
- `CLAUDE_PLUGIN_ROOT` が利用可能なプラグイン実行コンテキストで実行
- `claude` コマンドが利用可能
- tmux がインストール済み
- macOS で cmux、Ghostty、または iTerm2 を推奨（未導入時は Terminal.app / 現在端末にフォールバック）

## バージョン履歴

- v6.0.0: 実装のみ・コミットのみ・PR 作成までの範囲を分離し、不要な Issue 作成・完了承認・手動 push 待ちを廃止。許可済みの操作を検証後に続行（承認・push 動作の変更）

- v5.0.0: `single-issue` / `multi-issue` / `agent-team-issue` を `single` / `multi` / `agent-team` に統合（7→4 スキル）。全フラグ（`--plan` / `--branch` / `--issue` / `--no-git` / `--no-review`）を廃止し、git・worktree/branch・計画書・レビュー・Issue/PR 連携を発話・引数から自動判断する方式へ変更（破壊的変更）
- v4.1.0: cmux をターミナル最優先として追加（cmux → Ghostty → iTerm2 → Terminal.app → Current Shell）、全ターミナルで tab/workspace/window クローズに対応
- v4.0.0: git/GitHub 操作を Skill 呼び出しに置き換え、issue-branch-pr-create スキルを追加、push を自動実行からコマンド提示に変更（破壊的変更）
- v3.0.0: 全スキルから `workflow-` プレフィックスを除去しリネーム（破壊的変更）
- v2.0.0: 全スキルを `workflow-*` 形式にリネーム（破壊的変更）
- v1.8.0: マルチ / Agent Team 軽量フローに `--no-git` と git/no-git 自動分岐を追加（非git ディレクトリ対応）
- v1.5.0: SKILL.md を約 60% スリム化。MCP 側で Admin/Worker 指示を自動生成
- v1.4.0: Worker 数をデフォルト 6、最大 16 に変更。MCP 自動機能（ペルソナ、メモリ、7 セクション構造）を統合
- v1.0.0: 初期リリース（shiiman-git の dev-flow から移行）
