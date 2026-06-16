---
name: shiiman-workflow:agent-team
description: Agent Team（tmux + TeamCreate）で並列実装する開発フロー。「エージェントチームフロー」「workflow-agent-team」「Agent Team で実装」「チームで実装」「チーム並列開発」などで起動。Issue/PR まで作るかは発話・引数から判断し、曖昧なら確認する。
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
argument-hint: "[タスク説明]"
---

# Agent Team Flow

Agent Team（tmux + TeamCreate）で並列実装する開発フロー。
`workflow-multi` の MCP 依存部分を Agent Team 実行に置き換えたもの。

フラグは不要。タスクを伝えれば、git の状態・発話内容から実行条件を自動判断し、曖昧な点だけ確認する。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-workflow:agent-team - Agent Team 開発フロー

概要:
  Agent Team（tmux + TeamCreate）で並列実装する。
  実装条件（Issue/PR・計画書・ブランチ・git・レビュー）はフラグ不要で自動判断し、
  曖昧な点だけ AskUserQuestion で確認する。

使用方法:
  /shiiman-workflow:agent-team [タスク説明]
  /shiiman-workflow:agent-team --help

オプション:
  --help  このヘルプを表示

例:
  /shiiman-workflow:agent-team                          # 既存計画書から並列実装（あれば）
  /shiiman-workflow:agent-team "API を並列リファクタ"    # タスク説明から並列実装
  /shiiman-workflow:agent-team "認証を実装して PR まで"  # Issue/PR 連携ありで並列実装
  /shiiman-workflow:agent-team --help                   # ヘルプを表示

指定の伝え方（フラグの代わり）:
  - 「計画を立ててから」  → plan mode で計画書を作成してから実装
  - 「ブランチで」        → worktree ではなくブランチを作成
  - 「Issue / PR まで」   → Issue 作成・PR 作成まで実施
  - 「コミットだけ」      → Issue/PR を作らずコミットメッセージ出力で終了
  - 「レビュー不要」      → 完了報告前の /shiiman-common:review をスキップ
```

## 前提条件

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` が設定済み（必須）
- `claude` / `tmux` / `gh` コマンドが利用可能
- `gh auth status` が成功する（GitHub CLI 認証済み）
- macOS で `cmux` / `Ghostty` / `iTerm2` を推奨（未導入時は `Terminal.app` / 現在端末へフォールバック）

## 起動時の自動判断（フラグの代わり）

ユーザーにフラグを入力させない。以下を順に決定する。**引数・発話に明示があればそれを最優先**し、明示がなければ自動判断、それでも曖昧な項目だけ後述の手順で確認する。

| 項目              | 既定       | 判断ルール                                                                                                      |
| ----------------- | ---------- | --------------------------------------------------------------------------------------------------------------- |
| git / no-git      | 自動       | `git rev-parse --is-inside-work-tree` 成功なら git。失敗なら no-git（ブランチ作成を省略）                       |
| worktree / branch | worktree   | 「ブランチで」「worktree なし」等の発話があれば branch                                                          |
| 計画書の扱い      | 後述の判定 | 「計画を立てて」「plan で」→ plan mode。引数にタスク説明あり → 直接。なし → 既存計画書を探索                    |
| レビュー          | 実行する   | 「レビュー不要」「レビューなし」等の発話があればスキップ                                                        |
| Issue/PR 連携     | **要確認** | 「Issue」「PR」「プルリク」等あり → 連携あり。「コミットだけ」「Issue 不要」等 → 連携なし。どちらも無ければ確認 |

### Issue/PR 連携の確認

発話・引数から判断できない場合のみ、`AskUserQuestion` で 1 回だけ確認する。

```text
question: "どこまで実施しますか？"
options:
  - 軽量（コミットメッセージ出力のみ）: Issue/PR を作らず、変更とコミットメッセージの提示で終了
  - Issue/PR まで作成: Issue 作成 → 並列実装 → コミット → PR 作成まで実施
```

### git の状態判定

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1
```

- 成功 → git モード（ブランチ/worktree を作成）
- 失敗 → no-git モード（ブランチ作成を省略し、実装とサマリー出力のみ）

### 計画書の扱いの判定

1. 「計画を立ててから」等の依頼がある → **plan mode**: `EnterPlanMode` で計画書を作成・承認してから実装フェーズへ
2. 引数にタスク説明がある → **直接実行**: タスク説明をそのまま実装の指針にする
3. 引数なし → **既存計画書**: 最新の計画書を読み込む（`ls -t ~/.claude/plans/*.md | head -1`）。見つからなければタスク説明を促して終了

### session 名 / slug ルール

- Issue/PR 連携あり → `agent-team-issue-{issue番号}`
- 連携なし → `agent-team-{slug}`（slug はタスク内容から英語キーワード。生成できなければ `no-git-task`）

## Phase 1: セットアップと Agent Team 起動

### ステップ A: Issue 作成（Issue/PR 連携ありのときのみ）

Skill ツールで `shiiman-github:issue-create --no-confirm` を呼び出す。本文は「## 概要 / ## タスク一覧（チェックボックス）/ ## 完了条件」で構成。作成された Issue 番号を session 名と後続に使う。

### ステップ 1: ブランチ / worktree 作成

git モードのみ実施（no-git はスキップ）。

- worktree（既定）: Skill ツールで `shiiman-github:worktree-create` を呼び出す
- ブランチ: Skill ツールで `shiiman-github:branch-create` を呼び出す
- Issue/PR 連携ありの場合は Issue 番号を引数に渡す

> **Note:** `shiiman-github:worktree-create` は `mise trust` を自動実行する（`mise.toml` がなければスキップ）。

### ステップ 2: 共通スクリプトで tmux セッションを起動

```bash
SESSION="{session名}"
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

### ステップ 3: tmux 内で Claude Code を起動

```bash
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude --dangerously-skip-permissions --teammate-mode tmux
```

### ステップ 4: 送信スクリプトを設定

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
  echo "必要に応じて Step 3 の claude 起動をやり直してください。"
fi

SEND_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/send_claude_tmux_message.sh"
```

- `TARGET` は固定値（`0.0`）を使わず tmux 実値で解決する（`base-index` / `pane-base-index` が `1` の環境でも動作）

### ステップ 5: 計画書を送信して Agent Team 実行を開始

送信スクリプトは、本文貼り付け後に 2 通目の Enter を自動送信する。

```bash
REPO_ROOT="$(pwd)"
COMMIT_NOTICE="コミット（git add / commit / push）は行わないでください。"
REVIEW_NOTICE=""
if [ "{レビュー実行}" = "true" ]; then
  REVIEW_NOTICE="/shiiman-common:review を実行して指摘内容をすべて自動修正し、"
fi
ISSUE_NOTICE=""
if [ "{Issue連携あり}" = "true" ]; then
  ISSUE_NOTICE="Issue #{issue番号} の対応として、"
fi

# 計画書をファイルに保存
TS="$(date +%Y%m%d-%H%M%S)"
PLAN_FILE="${REPO_ROOT}/.claude/tmp/${TS}-${SESSION}-plan.md"
mkdir -p "${REPO_ROOT}/.claude/tmp"
cat >| "$PLAN_FILE" <<EOF
{plan_or_task}
EOF

# パス参照のみを送信
REQUEST_FILE="$(mktemp)"
cat >| "$REQUEST_FILE" <<EOF
TeamCreate ツールを使って Agent Team を作成し、${ISSUE_NOTICE}計画書に従って実装を開始してください。
並列実行には必ず TeamCreate ツールを使用してください（Agent ツールではなく TeamCreate です）。
報告書などのアウトプットがある場合は "${REPO_ROOT}/.claude/tmp" に出力してください。
${COMMIT_NOTICE}

計画書ファイル: ${PLAN_FILE}
Read ツールで上記ファイルを読み込んでから実装を進めてください。

実装完了後、${REVIEW_NOTICE}以下を報告してください。
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

### ステップ 6: macOS 通知を待機

完了通知が届く想定。進捗確認が必要なら tmux 出力を確認:

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

no-git モード: Agent Team の最終報告（実装サマリー・変更ファイル・テスト結果・残課題）を確認。

### ステップ 2: ユーザー承認を取得（🔴 必須）

```text
AskUserQuestion:
  question: "実装内容を承認しますか？"
  options:
    - OK（承認）: 後続処理へ進む
    - NG（修正依頼）: 修正内容を送って再実行
    - 保留: 手動確認後に再開
```

### NG（修正依頼）の場合

修正内容を変数に入れて送信スクリプトで再送（`{レビュー実行}` / `COMMIT_NOTICE` はステップ 5 と同じ規則）:

```bash
USER_FEEDBACK="{user_feedback}"
TS="$(date +%Y%m%d-%H%M%S)"
FIX_REQUEST_FILE="${REPO_ROOT}/.claude/tmp/${TS}-fix-request.md"
mkdir -p "${REPO_ROOT}/.claude/tmp"
cat >| "$FIX_REQUEST_FILE" <<EOF
${USER_FEEDBACK}
EOF

FIX_FILE="$(mktemp)"
cat >| "$FIX_FILE" <<EOF
TeamCreate ツールを使って Agent Team を作成し、修正指示に従って実装を開始してください。
並列実行には必ず TeamCreate ツールを使用してください（Agent ツールではなく TeamCreate です）。
${COMMIT_NOTICE}

修正依頼ファイル: ${FIX_REQUEST_FILE}
Read ツールで上記ファイルを読み込んでから修正を進めてください。

上記を反映し、${REVIEW_NOTICE}実装サマリー・変更ファイル・テスト結果・残課題を再報告してください。
完了時は osascript で macOS 通知を送ってください。
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$FIX_FILE"
rm -f "$FIX_FILE"
```

→ Phase 2-4 に戻って再実行。

### 保留の場合

tmux セッションを維持して待機。明示的な再開指示が来るまでクリーンアップしない。

### OK（承認）の場合

1. クリーンアップ（tmux は常に終了、window 起動時のみ terminal をクローズ）:

   ```bash
   bash "$CLEANUP_SCRIPT" --session "$SESSION" --state-file "$TERMINAL_STATE_FILE"
   rm -f "$TERMINAL_STATE_FILE"
   ```

2. セキュリティチェック: 機密ファイル（`.env*` / `*.pem` / `credentials.json`）を検出したら警告

   ```bash
   git status   # git モード
   find . -maxdepth 3 \( -name ".env*" -o -name "*.pem" -o -name "credentials.json" \)  # no-git モード
   ```

3. 「仕上げ」へ進む

## 仕上げ

### Issue/PR 連携あり

1. Issue の全チェックボックスを完了に更新:

   ```bash
   gh issue edit {issue番号} --body "$(gh issue view {issue番号} --json body -q '.body' | sed 's/- \[ \]/- [x]/g')"
   ```

2. コミット: Skill ツールで `shiiman-git:add-commit --no-confirm` を呼び出す
3. プッシュ案内（自動実行しない）: `git push -u origin feature/{issue番号}`
4. PR 作成: Skill ツールで `shiiman-github:pr-create --no-confirm` を呼び出す。本文は「## 概要 / ## 並列実行サマリー（チームメイト×タスクの表）/ ## 関連 Issue（`Closes #{issue番号}`）/ ## テスト計画」
5. 完了報告（Issue 番号・ブランチ/worktree・PR 番号/URL・worktree クリーンアップ案内）

### Issue/PR 連携なし（軽量）

**コミット・プッシュ・PR 作成は行わない。** 推奨コミットメッセージを出力して終了する。

```text
## 実装完了

### 作成されたブランチ / worktree（git モード時のみ）
- {ブランチ名} / パス: {worktree のパス}（worktree モード時のみ）

### 推奨コミットメッセージ
{Conventional Commits 形式（`.claude/settings.json` の git.commitMessage 設定があればそれに従う）}

### 次のステップ
git push -u origin feature/{slug}
必要に応じて gh pr create

### worktree クリーンアップ（worktree モード時のみ）
PR マージ後、`/shiiman-git:worktree` で gtr rm または gtr clean を実行してください。
```

## 失敗時の対応

- `gh` 認証失敗: `gh auth login` 実施後に再開
- `claude` / `tmux` 未インストール: 導入後に再実行
- Agent Team 側で部分失敗: 失敗タスクのみを再指示してループ

## 重要な注意事項

- ✅ ユーザーにフラグを入力させない（git・worktree/branch・計画書・レビュー・Issue/PR を自動判断、曖昧なら確認）
- ✅ 並列実行には必ず TeamCreate ツールを使う（Agent ツールではない）
- ✅ クリーンアップ前に必ずユーザー確認を行う
- ✅ コミットメッセージは `.claude/settings.json` の設定に従う（なければ Conventional Commits）
- ❌ Issue/PR 連携なしのときは自動でコミット・プッシュ・PR を作らない
