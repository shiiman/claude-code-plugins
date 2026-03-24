---
name: shiiman-workflow:agent-team
description: Agent Team で Issue/PR なしの並列実装を実行する軽量フロー。「workflow-agent-team」「エージェントチームフロー」「チーム並列実装」「Agent Team で実装」「チーム軽量フロー」「並列チーム開発」「Agent Team 軽量」などで起動。workflow-multi の MCP 使用部分を Agent Team に置き換えて実行。
allowed-tools:
  [
    Read,
    Write,
    Edit,
    Bash,
    Glob,
    Grep,
    AskUserQuestion,
    EnterPlanMode,
    TodoWrite,
    Skill,
  ]
context: fork
user-invocable: true
argument-hint: "[タスク説明] [--plan|--branch|--no-git|--help]"
---

# Agent Team Flow

Agent Team で Issue/PR なしに並列実装を進める軽量フロー。
`workflow-multi` のうち MCP 依存部分を Agent Team 実行に置き換えます。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-workflow:agent-team - Agent Team 軽量フロー

概要:
  Agent Team で Issue/PR なしに並列実装を実行する。
  worktree/ブランチ作成 → tmux + Claude 起動 → Agent Team 並列実行 → コミットメッセージ出力。

使用方法:
  /shiiman-workflow:agent-team [タスク説明] [オプション]

オプション:
  --plan    plan mode で計画書を新規作成してから実行
  --branch  worktree の代わりにブランチを作成
  --no-git  git を使わず no-git モードで実行
  --help    このヘルプを表示

例:
  /shiiman-workflow:agent-team                        # 既存計画書から実行（worktree）
  /shiiman-workflow:agent-team --plan                 # 計画書を作成してから実行
  /shiiman-workflow:agent-team --branch               # ブランチ作成モードで実行
  /shiiman-workflow:agent-team "API リファクタリング"  # タスク説明から直接実行
  /shiiman-workflow:agent-team --no-git               # git なしモードで実行
```

## 前提条件

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` が設定済み（必須）
- `claude` コマンドが利用可能
- `tmux` が利用可能
- `gh` コマンドが利用可能
- `gh auth status` が成功する（GitHub CLI 認証済み）
- macOS で `cmux`、`Ghostty`、または `iTerm2` を推奨（未導入時は `Terminal.app` / 現在端末へフォールバック）

## 実行モード判定（重要）

優先順位は以下。

1. `--no-git` 指定あり: 常に no-git モード
2. `--no-git` 指定なし + `git rev-parse --is-inside-work-tree` 成功: git モード
3. それ以外: no-git モード

判定コマンド:

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1
```

## セッション名 / slug ルール

- slug はタスク内容から簡潔な英語キーワードで作成
- slug を生成できない場合は `no-git-task` を使用
- tmux セッション名は `agent-team-{slug}` を使用

## 実行フロー

```text
git モード:
Phase 1: ブランチ作成 → ターミナル + tmux 起動 → claude 起動 → 計画書送信
Phase 2-4: Agent Team が計画書を読み取り自律実装
Phase 5: 結果確認 → 承認/修正依頼 → クリーンアップ → コミットメッセージ出力

no-git モード:
Phase 1: ターミナル + tmux 起動 → claude 起動 → 計画書送信
Phase 2-4: Agent Team が計画書を読み取り自律実装
Phase 5: 結果確認（Agent Team 報告）→ 承認/修正依頼 → クリーンアップ
```

## Phase 1: セットアップと Agent Team 起動

### ステップ 1: 実行モード判定

```bash
if [ "{no_git_flag}" = "true" ]; then
  FLOW_MODE="no-git"
elif git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  FLOW_MODE="git"
else
  FLOW_MODE="no-git"
fi
```

### ステップ 2: slug を決定

```text
slug = {task_slug}
if slug が空なら slug = "no-git-task"
```

### ステップ 3: git モード時のみ worktree / ブランチ作成

**デフォルト（`--branch` なし）**:

Skill ツールで `shiiman-github:worktree-create` を呼び出す。

**`--branch` 指定時**:

Skill ツールで `shiiman-github:branch-create` を呼び出す。

no-git モードではこのステップをスキップする。
ユーザーがベースブランチを明示した場合は、そちらを優先する。

### ステップ 4: 共通スクリプトで tmux セッションを起動

```bash
SESSION="agent-team-{slug}"
REPO_ROOT="$(pwd)"
OPEN_TMUX_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/open_tmux_terminal.sh"
CLEANUP_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/cleanup_tmux_terminal.sh"
TERMINAL_STATE_FILE="$(mktemp)"

bash "$OPEN_TMUX_SCRIPT" \
  --session "$SESSION" \
  --repo-root "$REPO_ROOT" \
  --terminal auto \
  --state-file "$TERMINAL_STATE_FILE"
```

### ステップ 5: tmux 内で Claude Code を起動

```bash
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude --dangerously-skip-permissions --teammate-mode tmux
```

### ステップ 6: 送信スクリプトを設定（multi-agent-mcp の送信方式）

```bash
TARGET="$(tmux display-message -p -t "$SESSION" '#{session_name}:#{window_index}.#{pane_index}' 2>/dev/null || true)"
if [ -z "$TARGET" ]; then
  TARGET="$(tmux list-panes -t "$SESSION" -F '#{session_name}:#{window_index}.#{pane_index}' | head -n 1)"
fi
if [ -z "$TARGET" ]; then
  echo "ERROR: tmux target を解決できませんでした (session: $SESSION)" >&2
  exit 1
fi

PANE_CMD="$(tmux display-message -p -t "$TARGET" '#{pane_current_command}' 2>/dev/null || true)"
if [ "$PANE_CMD" != "claude" ]; then
  echo "WARN: target pane is not claude (target: $TARGET, current: ${PANE_CMD:-unknown})"
  echo "必要に応じて Step 5 の claude 起動をやり直してください。"
fi

SEND_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/send_claude_tmux_message.sh"
```

- `TARGET` は固定値（`0.0`）を使わず tmux 実値で解決する
- `base-index` / `pane-base-index` が `1` の環境でも同じ手順で動作する

### ステップ 7: 計画書を送信して Agent Team 実行を開始

送信スクリプトは、本文貼り付け後に 2 通目の Enter を自動送信する。

```bash
REPO_ROOT="$(pwd)"
COMMIT_NOTICE=""
if [ "$FLOW_MODE" = "git" ]; then
  COMMIT_NOTICE="コミット（git add / commit / push）は行わないでください。"
fi

# 計画書をファイルに保存
TS="$(date +%Y%m%d-%H%M%S)"
PLAN_FILE="${REPO_ROOT}/.claude/tmp/${TS}-${slug}-plan.md"
mkdir -p "${REPO_ROOT}/.claude/tmp"
cat >| "$PLAN_FILE" <<EOF
{plan_or_task}
EOF

# パス参照のみを送信
REQUEST_FILE="$(mktemp)"
cat >| "$REQUEST_FILE" <<EOF
TeamCreate ツールを使って Agent Team を作成し、計画書に従って実装を開始してください。
並列実行には必ず TeamCreate ツールを使用してください（Agent ツールではなく TeamCreate です）。
報告書などのアウトプットがある場合は "${REPO_ROOT}/.claude/tmp" に出力してください。
${COMMIT_NOTICE}

計画書ファイル: ${PLAN_FILE}
Read ツールで上記ファイルを読み込んでから実装を進めてください。

完了時は以下を報告してください。
- 実装サマリー
- 変更ファイル
- テスト結果
- 残課題

完了時は以下コマンドを実行して macOS 通知を送ってください。
osascript -e 'display notification "Agent Team 実装が完了しました" with title "workflow-agent-team" sound name "default"'
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$REQUEST_FILE"
rm -f "$REQUEST_FILE"
```

### ステップ 8: macOS 通知を待機

- Agent Team 側の処理が完了すると通知が届く想定
- 進捗確認が必要な場合は tmux 出力を確認

```bash
CAPTURE_TARGET="$(tmux display-message -p -t "$SESSION" '#{session_name}:#{window_index}.#{pane_index}' 2>/dev/null || tmux list-panes -t "$SESSION" -F '#{session_name}:#{window_index}.#{pane_index}' | head -n 1)"
tmux capture-pane -pt "$CAPTURE_TARGET" | tail -n 120
```

## Phase 2-4: Agent Team の自律実行

Agent Team が計画書を分解して実装を進める。呼び出し元は待機する。

## Phase 5: 結果確認と承認フロー

### ステップ 1: 変更内容を確認

git モード:

```bash
git status --short --branch
git diff
git diff --cached
```

no-git モード:

- Agent Team の最終報告（実装サマリー・変更ファイル・テスト結果・残課題）を確認
- 必要に応じて以下で tmux 出力を再確認

```bash
CAPTURE_TARGET="$(tmux display-message -p -t "$SESSION" '#{session_name}:#{window_index}.#{pane_index}' 2>/dev/null || tmux list-panes -t "$SESSION" -F '#{session_name}:#{window_index}.#{pane_index}' | head -n 1)"
tmux capture-pane -pt "$CAPTURE_TARGET" | tail -n 200
```

### ステップ 2: ユーザー承認を取得（必須）

`AskUserQuestion` で次を確認する。

```text
question: "実装内容を承認しますか？"
options:
  - OK（承認）: クリーンアップして完了
  - NG（修正依頼）: 修正内容を送って再実行
  - 保留: 手動確認後に再開
```

### OK（承認）の場合

1. 実行側でクリーンアップスクリプトを実行（tmux は常に終了、window 起動時のみ terminal をクローズ）

```bash
bash "$CLEANUP_SCRIPT" --session "$SESSION" --state-file "$TERMINAL_STATE_FILE"
rm -f "$TERMINAL_STATE_FILE"
```

- `OPEN_MODE=tab` / `OPEN_MODE=current_shell` の場合、terminal は閉じない
- terminal window クローズ失敗時は `WARN` を出して継続（best-effort）

2. セキュリティチェック

git モード:

```bash
git status  # .env*, *.pem, credentials.json を検出したら警告
```

no-git モード:

```bash
find . -maxdepth 3 \( -name ".env*" -o -name "*.pem" -o -name "credentials.json" \)
```

3. 完了出力

git モード:

```text
## 実装完了

### 作成されたブランチ / worktree
- {ブランチ名}
- パス: {worktree のパス}（worktree モード時のみ）

### 推奨コミットメッセージ
{Conventional Commits 形式}

### 次のステップ

プッシュするには以下を実行:

git push -u origin feature/{slug}

必要に応じて gh pr create

### worktree クリーンアップ（worktree モード時のみ）

PR マージ後、不要になった worktree を削除してください:
`/shiiman-git:worktree` で gtr rm または gtr clean を実行
```

no-git モード:

```text
## 実装完了（no-git モード）

### 実装サマリー
- 変更ファイル: {agent_team_files}
- テスト結果: {agent_team_tests}
- 残課題: {agent_team_todos}

### 次のステップ
- 必要に応じてユーザー環境の手順に沿って成果物を反映
```

### NG（修正依頼）の場合

1. 修正内容を変数に入れて送信スクリプトで再送

```bash
USER_FEEDBACK="{user_feedback}"
REPO_ROOT="$(pwd)"
COMMIT_NOTICE=""
if [ "$FLOW_MODE" = "git" ]; then
  COMMIT_NOTICE="コミット（git add / commit / push）は行わないでください。"
fi

# 修正依頼をファイルに保存
TS="$(date +%Y%m%d-%H%M%S)"
FIX_REQUEST_FILE="${REPO_ROOT}/.claude/tmp/${TS}-${slug}-fix-request.md"
mkdir -p "${REPO_ROOT}/.claude/tmp"
cat >| "$FIX_REQUEST_FILE" <<EOF
${USER_FEEDBACK}
EOF

# パス参照のみを送信
FIX_FILE="$(mktemp)"
cat >| "$FIX_FILE" <<EOF
TeamCreate ツールを使って Agent Team を作成し、修正指示に従って実装を開始してください。
並列実行には必ず TeamCreate ツールを使用してください（Agent ツールではなく TeamCreate です）。
報告書などのアウトプットがある場合は "${REPO_ROOT}/.claude/tmp" に出力してください。
${COMMIT_NOTICE}

修正依頼ファイル: ${FIX_REQUEST_FILE}
Read ツールで上記ファイルを読み込んでから修正を進めてください。

上記を反映し、完了時は実装サマリー・変更ファイル・テスト結果・残課題を再報告してください。
完了時は以下コマンドを実行して macOS 通知を送ってください。
osascript -e 'display notification "Agent Team 修正対応が完了しました" with title "workflow-agent-team" sound name "default"'
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$FIX_FILE"
rm -f "$FIX_FILE"
```

2. Phase 2-4 に戻って再実行

### 保留の場合

- 必要に応じて待機指示を送信スクリプトで送信

```bash
HOLD_FILE="$(mktemp)"
cat >| "$HOLD_FILE" <<'EOF'
現在は保留です。追加指示があるまで待機してください。
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$HOLD_FILE"
rm -f "$HOLD_FILE"
```

- tmux セッションを維持して待機
- 明示的な再開指示が来るまでクリーンアップしない

## 失敗時の対応

- `claude` 未インストール: インストール後に再実行
- `tmux` 未インストール: `tmux` 導入後に再実行
- Agent Team 側で部分失敗: 失敗タスクのみを再指示してループ
