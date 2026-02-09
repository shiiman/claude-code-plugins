#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  send_claude_tmux_message.sh --target <session:window.pane> --file <message_file> [--enter]

Options:
  --target <value>   tmux target (e.g. agent-team-foo:0.0)
  --file <path>      message text file path
  --enter            press Enter after pasting message
  --sleep-ms <ms>    wait before Enter (default: 150)
  --no-verify        skip pane_current_command == claude check
USAGE
}

TARGET=""
MESSAGE_FILE=""
SEND_ENTER=0
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
    --enter)
      SEND_ENTER=1
      shift
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

if [[ ! -f "$MESSAGE_FILE" ]]; then
  echo "message file not found: $MESSAGE_FILE" >&2
  exit 2
fi

if [[ "$VERIFY_PANE" -eq 1 ]]; then
  pane_cmd="$(tmux display-message -p -t "$TARGET" '#{pane_current_command}' 2>/dev/null || true)"
  if [[ "$pane_cmd" != "claude" ]]; then
    echo "ERROR: target pane is not claude (current: ${pane_cmd:-unknown}, target: $TARGET)" >&2
    exit 1
  fi
fi

buffer_name="claude-msg-$$-$(date +%s)"
trap 'tmux delete-buffer -b "$buffer_name" >/dev/null 2>&1 || true' EXIT

# 1回目: メッセージ本文を送信（Enterなし）
tmux load-buffer -b "$buffer_name" "$MESSAGE_FILE"
tmux paste-buffer -d -b "$buffer_name" -t "$TARGET"

# 2回目: 必要な場合のみ Enter を送信
if [[ "$SEND_ENTER" -eq 1 ]]; then
  sleep "$(awk "BEGIN { printf \"%.3f\", ${SLEEP_MS}/1000 }")"
  tmux send-keys -t "$TARGET" C-m 2>/dev/null || tmux send-keys -t "$TARGET" Enter
fi
