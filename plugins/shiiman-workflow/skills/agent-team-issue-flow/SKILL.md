---
name: agent-team-issue-flow
description: Agent Team で Issue から PR まで並列実行する開発フロー。「agent-team-issue-flow」「エージェントチーム Issue フロー」「チーム Issue 開発」「Agent Team Issue」「Issue から並列実装」「チームで PR 作成」「Agent Team で Issue 対応」などで起動。multi-issue-flow の MCP 使用部分を Agent Team に置き換えて実行。
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, EnterPlanMode, TodoWrite]
context: fork
user-invocable: true
---

# Agent Team Issue Flow

Agent Team で Issue 作成から PR 作成までを並列実行するフロー。
`multi-issue-flow` のうち MCP 依存部分を Agent Team 実行に置き換えます。

## 前提条件

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` が設定済み（必須）
- `claude` コマンドが利用可能
- `tmux` が利用可能
- `gh auth status` が成功する（GitHub CLI 認証済み）
- macOS で `Ghostty` または `iTerm2` を推奨（未導入時は `Terminal.app` / 現在端末へフォールバック）

## 引数

- `--plan`: plan mode で計画書を新規作成してから実行
- `--help`: ヘルプを表示
- `[タスク説明]`: 計画書なしで直接実行

## 実行フロー

```text
Phase 1: Issue 作成 → ブランチ作成 → ターミナル + tmux 起動 → claude 起動 → 計画書送信
Phase 2-4: Agent Team が計画書を読み取り自律実装
Phase 5: 結果確認 → 承認/修正依頼 → クリーンアップ → Issue 更新 → コミット/Push → PR 作成
```

## Phase 1: Issue 作成と Agent Team 起動

### ステップ 1: Issue 作成

```bash
gh repo view --json owner,name
gh issue create --title "{title}" --body "{body}" --label "{label}"
```

Issue 本文テンプレート:

```markdown
## 概要
{目的・背景}

## タスク一覧
- [ ] Task 1: {subtask}
- [ ] Task 2: {subtask}

## 完了条件
- 全 Task が完了
- テスト通過
```

### ステップ 2: ブランチ作成

```bash
git fetch origin main
git checkout main
git pull origin main
git checkout -b feature/{issue_number}
```

### ステップ 3: 共通スクリプトで tmux セッションを起動

```bash
SESSION="agent-team-issue-{issue_number}"
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

### ステップ 4: tmux 内で Claude Code を起動

```bash
claude --dangerously-skip-permissions
```

### ステップ 5: 送信スクリプトを設定（multi-agent-mcp の送信方式）

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
  echo "必要に応じて Step 4 の claude 起動をやり直してください。"
fi

SEND_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/send_claude_tmux_message.sh"
```

- `TARGET` は固定値（`0.0`）を使わず tmux 実値で解決する
- `base-index` / `pane-base-index` が `1` の環境でも同じ手順で動作する

### ステップ 6: 計画書を送信して Agent Team 実行を開始

送信スクリプトは、本文貼り付け後に 2 通目の Enter を自動送信する。

```bash
REPO_ROOT="$(pwd)"
REQUEST_FILE="$(mktemp)"
COMMIT_NOTICE="コミット（git add / commit / push）は行わないでください。"

cat >| "$REQUEST_FILE" <<EOF
Issue #{issue_number} の対応を開始してください。以下の計画書に従って実装してください。
報告書などのアウトプットがある場合は "${REPO_ROOT}/.claude/tmp" に出力してください。
${COMMIT_NOTICE}

計画書:
{plan_or_task}

完了時は以下を報告してください。
- 実装サマリー
- 変更ファイル
- テスト結果
- 残課題

完了時は以下コマンドを実行して macOS 通知を送ってください。
osascript -e 'display notification "Agent Team Issue 実装が完了しました" with title "agent-team-issue-flow" sound name "default"'
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$REQUEST_FILE"
rm -f "$REQUEST_FILE"
```

### ステップ 7: macOS 通知を待機

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

```bash
git status --short --branch
git diff
git diff --cached
```

### ステップ 2: ユーザー承認を取得（必須）

`AskUserQuestion` で次を確認する。

```text
question: "実装内容を承認しますか？"
options:
  - OK（承認）: PR 作成まで進む
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

```bash
git status  # .env*, *.pem, credentials.json を検出したら警告
```

3. Issue のチェックボックスを完了に更新

```bash
gh issue edit {issue_number} --body "$(gh issue view {issue_number} --json body -q '.body' | sed 's/- \[ \]/- [x]/g')"
```

4. コミットと push

```bash
git add .
git commit -m "{conventional_commit_message}"
git push origin feature/{issue_number}
```

5. PR 作成

```bash
gh pr create --title "{pr_title}" --body "{pr_body}"
```

PR 本文テンプレート:

```markdown
## 概要
{変更内容}

## 並列実行サマリー
| チームメイト | タスク | 状態 |
|-------------|--------|------|
| worker-1 | Task 1 | ✅ 完了 |

## 関連 Issue
Closes #{issue_number}

## テスト計画
- [ ] {test_item}
```

6. 完了報告

```text
## 開発フロー完了

### 作成された Issue
- #{issue_number}: {issue_title}

### 作成された PR
- PR #{pr_number}: {pr_title}
- URL: {pr_url}
```

### NG（修正依頼）の場合

1. 修正内容を変数に入れて送信スクリプトで再送

```bash
USER_FEEDBACK="{user_feedback}"
REPO_ROOT="$(pwd)"
FIX_FILE="$(mktemp)"
COMMIT_NOTICE="コミット（git add / commit / push）は行わないでください。"

cat >| "$FIX_FILE" <<EOF
Agent Team を作成して、以下の修正指示に従って実装を開始してください。
報告書などのアウトプットがある場合は "${REPO_ROOT}/.claude/tmp" に出力してください。
${COMMIT_NOTICE}

修正依頼: ${USER_FEEDBACK}

上記を反映し、完了時は実装サマリー・変更ファイル・テスト結果・残課題を再報告してください。
完了時は以下コマンドを実行して macOS 通知を送ってください。
osascript -e 'display notification "Agent Team Issue 修正対応が完了しました" with title "agent-team-issue-flow" sound name "default"'
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

- `gh` 認証失敗: `gh auth login` 実施後に再開
- `claude` 未インストール: インストール後に再実行
- `tmux` 未インストール: `tmux` 導入後に再実行
- Agent Team 側で部分失敗: 失敗タスクのみを再指示してループ
