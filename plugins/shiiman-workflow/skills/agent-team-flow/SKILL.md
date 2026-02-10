---
name: agent-team-flow
description: Agent Team で Issue/PR なしの並列実装を実行する軽量フロー。「agent-team-flow」「エージェントチームフロー」「チーム並列実装」「Agent Team で実装」「チーム軽量フロー」「並列チーム開発」「Agent Team 軽量」などで起動。multi-flow の MCP 使用部分を Agent Team に置き換えて実行。
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, EnterPlanMode, TodoWrite]
context: fork
user-invocable: true
---

# Agent Team Flow

Agent Team で Issue/PR なしに並列実装を進める軽量フロー。
`multi-flow` のうち MCP 依存部分を Agent Team 実行に置き換えます。

## 前提条件

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` が設定済み（必須）
- `claude` コマンドが利用可能
- `tmux` が利用可能
- macOS で `Ghostty` または `iTerm2` が利用可能（Ghostty 優先）

## 引数

- `--plan`: plan mode で計画書を新規作成してから実行
- `--no-git`: git を使わず no-git モードで実行（強制）
- `--help`: ヘルプを表示
- `[タスク説明]`: 計画書なしで直接実行

## 実行モード判定（重要）

優先順位は以下。

1. `--no-git` 指定あり: 常に no-git モード
2. `--no-git` 指定なし + `git rev-parse --is-inside-work-tree` 成功: git モード
3. それ以外: git モード

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
Phase 1: ブランチ作成 → Ghostty/iTerm2 + tmux 起動 → claude 起動 → 計画書送信
Phase 2-4: Agent Team が計画書を読み取り自律実装
Phase 5: 結果確認 → 承認/修正依頼 → クリーンアップ → コミットメッセージ出力

no-git モード:
Phase 1: Ghostty/iTerm2 + tmux 起動 → claude 起動 → 計画書送信
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

### ステップ 3: git モード時のみブランチ作成

```bash
git fetch origin main
git checkout main
git pull origin main
git checkout -b feature/{slug}
```

no-git モードではこのステップをスキップする。

### ステップ 4: Ghostty (なければ iTerm2) を起動して tmux セッションを用意

```bash
SESSION="agent-team-{slug}"
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

### ステップ 5: tmux 内で Claude Code を起動

```bash
claude --dangerously-skip-permissions
```

### ステップ 6: 送信スクリプトを設定（multi-agent-mcp の送信方式）

```bash
TARGET="$SESSION:0.0"

SEND_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/send_claude_tmux_message.sh"
```

### ステップ 7: 計画書を送信して Agent Team 実行を開始

送信スクリプトは、本文貼り付け後に 2 通目の Enter を自動送信する。

```bash
REQUEST_FILE="$(mktemp)"
NO_COMMIT_LINE=""
if [ "$FLOW_MODE" = "git" ]; then
  NO_COMMIT_LINE="git add / commit / push は実行しないでください。"
fi
cat > "$REQUEST_FILE" <<EOF
Agent Team を作成して、以下の計画書に従って実装を開始してください。
${NO_COMMIT_LINE}

計画書:
{plan_or_task}

完了時は、実装サマリー・変更ファイル・テスト結果・残課題を報告してください。
完了時は以下コマンドを実行して macOS 通知を送ってください。
osascript -e 'display notification "Agent Team 実装が完了しました" with title "agent-team-flow" sound name "default"'
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$REQUEST_FILE"
rm -f "$REQUEST_FILE"
```

### ステップ 8: macOS 通知を待機

- Agent Team 側の処理が完了すると通知が届く想定
- 進捗確認が必要な場合は tmux 出力を確認

```bash
tmux capture-pane -pt "$SESSION":0.0 | tail -n 120
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
tmux capture-pane -pt "$SESSION":0.0 | tail -n 200
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

1. 送信スクリプトで Claude Code へクリーンアップ指示を送信

```bash
APPROVAL_FILE="$(mktemp)"
cat > "$APPROVAL_FILE" <<'EOF'
実装を承認します。Agent Team をクリーンアップして、最終サマリーを出してください。
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$APPROVAL_FILE"
rm -f "$APPROVAL_FILE"
```

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

### 推奨コミットメッセージ
{Conventional Commits 形式}

### 次のステップ（手動）
1. git add .
2. git commit -m "{メッセージ}"
3. git push origin feature/{slug}
4. 必要に応じて gh pr create
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
FIX_FILE="$(mktemp)"
NO_COMMIT_FIX_LINE=""
if [ "$FLOW_MODE" = "git" ]; then
  NO_COMMIT_FIX_LINE="コミット（git add / commit / push）は行わないでください。"
fi
cat > "$FIX_FILE" <<EOF
Agent Team を作成して、以下の修正指示に従って実装を開始してください。
${NO_COMMIT_FIX_LINE}

修正依頼: ${USER_FEEDBACK}

上記を反映し、完了時は実装サマリー・変更ファイル・テスト結果・残課題を再報告してください。
完了時は以下コマンドを実行して macOS 通知を送ってください。
osascript -e 'display notification "Agent Team 修正対応が完了しました" with title "agent-team-flow" sound name "default"'
EOF
bash "$SEND_SCRIPT" --target "$TARGET" --file "$FIX_FILE"
rm -f "$FIX_FILE"
```

2. Phase 2-4 に戻って再実行

### 保留の場合

- 必要に応じて待機指示を送信スクリプトで送信

```bash
HOLD_FILE="$(mktemp)"
cat > "$HOLD_FILE" <<'EOF'
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
- Ghostty/iTerm2 なし: 現在のターミナルで tmux を起動して継続
- Agent Team 側で部分失敗: 失敗タスクのみを再指示してループ
