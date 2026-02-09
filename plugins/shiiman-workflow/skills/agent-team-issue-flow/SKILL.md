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
- macOS で `Ghostty` または `iTerm2` が利用可能（Ghostty 優先）

## 引数

- `--plan`: plan mode で計画書を新規作成してから実行
- `--help`: ヘルプを表示
- `[タスク説明]`: 計画書なしで直接実行

## 実行フロー

```text
Phase 1: Issue 作成 → ブランチ作成 → Ghostty/iTerm2 + tmux 起動 → claude 起動 → 計画書送信
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
git push -u origin feature/{issue_number}
```

### ステップ 3: Ghostty (なければ iTerm2) を起動して tmux セッションを用意

```bash
SESSION="agent-team-issue-{issue_number}"
REPO_ROOT="$(pwd)"

if [ -d "/Applications/Ghostty.app" ]; then
  open -na Ghostty
  echo "Ghostty を起動。新しいウィンドウで: cd \"$REPO_ROOT\" && tmux new -As \"$SESSION\""
elif [ -d "/Applications/iTerm.app" ]; then
  open -na iTerm
  echo "iTerm2 を起動。新しいウィンドウで: cd \"$REPO_ROOT\" && tmux new -As \"$SESSION\""
else
  echo "Ghostty/iTerm2 が見つからないため、現在の端末で: cd \"$REPO_ROOT\" && tmux new -As \"$SESSION\""
fi
```

### ステップ 4: tmux 内で Claude Code を起動

```bash
claude --dangerously-skip-permissions
```

### ステップ 5: 送信スクリプトを設定（multi-agent-mcp の送信方式）

```bash
TARGET="$SESSION:0.0"

if [ -z "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  CLAUDE_PLUGIN_ROOT="$REPO_ROOT/plugins/shiiman-workflow"
fi

SEND_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/send_claude_tmux_message.sh"
test -x "$SEND_SCRIPT" || { echo "script not found: $SEND_SCRIPT" >&2; exit 1; }
```

### ステップ 6: 計画書を送信して Agent Team 実行を開始

メッセージは 2 回に分けて送る（1通目は Enter なし、2通目で Enter）。
- 1通目: 実行指示
- 2通目: 計画書本文（2回目も Enter で確定）

```bash
INSTRUCTION_FILE="$(mktemp)"
cat > "$INSTRUCTION_FILE" <<'EOF'
Issue #{issue_number} の対応を開始してください。次のメッセージで計画書本体を送ります。
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$INSTRUCTION_FILE"
rm -f "$INSTRUCTION_FILE"

PLAN_MSG_FILE="$(mktemp)"
cat > "$PLAN_MSG_FILE" <<'EOF'
計画書:
{plan_or_task}

- 完了条件: 実装、テスト、変更サマリー、残課題の報告
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$PLAN_MSG_FILE" --enter
rm -f "$PLAN_MSG_FILE"
```

### ステップ 7: macOS 通知を待機

- Agent Team 側の処理が完了すると通知が届く想定
- 進捗確認が必要な場合は tmux 出力を確認

```bash
tmux capture-pane -pt "$SESSION":0.0 | tail -n 120
```

## Phase 2-4: Agent Team の自律実行

Agent Team が計画書を分解して実装を進める。呼び出し元は待機し、必要時のみ追加指示を送る。

## Phase 5: 結果確認と承認フロー

### ステップ 1: 変更内容を確認

```bash
git checkout feature/{issue_number}
git pull origin feature/{issue_number}
git diff main...feature/{issue_number} --stat
git log main..feature/{issue_number} --oneline
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

1. 送信スクリプトで Claude Code へクリーンアップ指示を送信

```bash
APPROVAL_FILE="$(mktemp)"
cat > "$APPROVAL_FILE" <<'EOF'
実装を承認します。Agent Team をクリーンアップして、最終サマリーを出してください。
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$APPROVAL_FILE" --enter
rm -f "$APPROVAL_FILE"
```

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

1. 修正内容を変数に入れて送信スクリプトで再送（2通）

```bash
USER_FEEDBACK="{user_feedback}"
FIX_HEAD_FILE="$(mktemp)"
cat > "$FIX_HEAD_FILE" <<'EOF'
修正依頼を送ります。次のメッセージの内容を反映してください。
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$FIX_HEAD_FILE"
rm -f "$FIX_HEAD_FILE"

FIX_BODY_FILE="$(mktemp)"
cat > "$FIX_BODY_FILE" <<EOF
修正依頼: ${USER_FEEDBACK}

上記を反映し、完了後に差分とテスト結果を再報告してください。
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$FIX_BODY_FILE" --enter
rm -f "$FIX_BODY_FILE"
```

2. Phase 2-4 に戻って再実行

### 保留の場合

- 必要に応じて待機指示を送信スクリプトで送信

```bash
HOLD_FILE="$(mktemp)"
cat > "$HOLD_FILE" <<'EOF'
現在は保留です。追加指示があるまで待機してください。
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$HOLD_FILE" --enter
rm -f "$HOLD_FILE"
```

- tmux セッションを維持して待機
- 明示的な再開指示が来るまでクリーンアップしない

## 失敗時の対応

- `gh` 認証失敗: `gh auth login` 実施後に再開
- `claude` 未インストール: インストール後に再実行
- `tmux` 未インストール: `tmux` 導入後に再実行
- Ghostty/iTerm2 なし: 現在のターミナルで tmux を起動して継続
- Agent Team 側で部分失敗: 失敗タスクのみを再指示してループ
