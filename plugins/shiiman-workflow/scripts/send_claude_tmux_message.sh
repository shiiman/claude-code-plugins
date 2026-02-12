#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  send_claude_tmux_message.sh --target <session:window.pane> --file <message_file>

Options:
  --target <value>   tmux target (e.g. agent-team-foo:1.1)
  --file <path>      message text file path
  --sleep-ms <ms>    wait before Enter (default: 150)
  --no-verify        skip pane_current_command == claude check
USAGE
}

TARGET=""
MESSAGE_FILE=""
SLEEP_MS=150
VERIFY_PANE=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --file)
      MESSAGE_FILE="${2:-}"
      shift 2
      ;;
    --sleep-ms)
      SLEEP_MS="${2:-150}"
      shift 2
      ;;
    --no-verify)
      VERIFY_PANE=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$TARGET" || -z "$MESSAGE_FILE" ]]; then
  echo "--target and --file are required" >&2
  usage >&2
  exit 2
fi

if [[ ! "$SLEEP_MS" =~ ^[0-9]+$ ]]; then
  echo "--sleep-ms must be a non-negative integer (milliseconds): $SLEEP_MS" >&2
  exit 2
fi

if [[ ! -f "$MESSAGE_FILE" ]]; then
  echo "message file not found: $MESSAGE_FILE" >&2
  exit 2
fi

if [[ ! -s "$MESSAGE_FILE" ]]; then
  echo "message file is empty: $MESSAGE_FILE" >&2
  echo "HINT: if zsh noclobber is enabled, write heredoc with >| (e.g. cat >| \"\$REQUEST_FILE\" <<EOF)." >&2
  exit 2
fi

target_session="${TARGET%%:*}"
if [[ -z "$target_session" || "$target_session" == "$TARGET" ]]; then
  echo "ERROR: invalid --target format (expected session:window.pane, got: $TARGET)" >&2
  exit 2
fi

session_exists_exact() {
  local name="$1"
  tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -Fxq "$name"
}

if ! session_exists_exact "$target_session"; then
  echo "ERROR: tmux session not found: $target_session" >&2
  echo "HINT: run open_tmux_terminal.sh for session '$target_session' before sending messages." >&2
  exit 1
fi

pane_inventory="$(tmux list-panes -t "$target_session" -F '#{session_name}:#{window_index}.#{pane_index} cmd=#{pane_current_command} active=#{pane_active}' 2>/dev/null || true)"
pane_targets="$(printf '%s\n' "$pane_inventory" | cut -d ' ' -f1)"

if ! printf '%s\n' "$pane_targets" | grep -Fxq "$TARGET"; then
  echo "ERROR: target pane not found in session '$target_session' (target: $TARGET)" >&2
  echo "Available panes:" >&2
  printf '  %s\n' "$pane_inventory" >&2
  exit 1
fi

if [[ "$VERIFY_PANE" -eq 1 ]]; then
  pane_cmd="$(tmux display-message -p -t "$TARGET" '#{pane_current_command}' 2>/dev/null || true)"
  if [[ "$pane_cmd" != "claude" ]]; then
    echo "ERROR: target pane is not claude (current: ${pane_cmd:-unknown}, target: $TARGET)" >&2
    echo "Available panes in session '$target_session':" >&2
    printf '  %s\n' "$pane_inventory" >&2
    echo "HINT: start 'claude --dangerously-skip-permissions' in the target pane, then retry." >&2
    exit 1
  fi
fi

buffer_name="claude-msg-$$-$(date +%s)"
trap 'tmux delete-buffer -b "$buffer_name" >/dev/null 2>&1 || true' EXIT

# 1回目: メッセージ本文を送信（Enterなし）
tmux load-buffer -b "$buffer_name" "$MESSAGE_FILE"
tmux paste-buffer -b "$buffer_name" -t "$TARGET"

# 2回目: Enter を自動送信
sleep "$(printf '%d.%03d' "$((SLEEP_MS / 1000))" "$((SLEEP_MS % 1000))")"
tmux send-keys -t "$TARGET" C-m 2>/dev/null || tmux send-keys -t "$TARGET" Enter
