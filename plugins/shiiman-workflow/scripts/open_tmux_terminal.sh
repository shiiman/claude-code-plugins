#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  open_tmux_terminal.sh --session <name> --repo-root <path> [--terminal <auto|ghostty|iterm2|terminal>] [--state-file <path>] [--dry-run]

Options:
  --session <name>      tmux session name (allowed: [A-Za-z0-9._:-])
  --repo-root <path>    repository root path
  --terminal <value>    auto | ghostty | iterm2 | terminal (default: auto)
  --state-file <path>   write launch metadata for cleanup script
  --dry-run             print selected behavior without opening terminals
  -h, --help            show this help
USAGE
}

SESSION=""
REPO_ROOT=""
TERMINAL="auto"
STATE_FILE=""
DRY_RUN=0

STATE_TERMINAL_BACKEND=""
STATE_OPEN_MODE=""
STATE_WINDOW_CLOSE_SUPPORTED="0"
STATE_ITERM_WINDOW_ID=""
STATE_TERMINAL_WINDOW_ID=""
STATE_GHOSTTY_PID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --session)
      SESSION="${2:-}"
      shift 2
      ;;
    --repo-root)
      REPO_ROOT="${2:-}"
      shift 2
      ;;
    --terminal)
      TERMINAL="${2:-}"
      shift 2
      ;;
    --state-file)
      STATE_FILE="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
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

if [[ -z "$SESSION" || -z "$REPO_ROOT" ]]; then
  echo "--session and --repo-root are required" >&2
  usage >&2
  exit 2
fi

if [[ ! "$SESSION" =~ ^[A-Za-z0-9._:-]+$ ]]; then
  echo "invalid session name: $SESSION" >&2
  exit 2
fi

if [[ ! -d "$REPO_ROOT" ]]; then
  echo "repo root is not a directory: $REPO_ROOT" >&2
  exit 2
fi
REPO_ROOT="$(cd "$REPO_ROOT" && pwd)"

if [[ -n "$STATE_FILE" ]]; then
  STATE_DIR="$(dirname "$STATE_FILE")"
  if [[ ! -d "$STATE_DIR" ]]; then
    echo "state file directory does not exist: $STATE_DIR" >&2
    exit 2
  fi
fi

case "$TERMINAL" in
  auto|ghostty|iterm2|terminal)
    ;;
  *)
    echo "invalid --terminal value: $TERMINAL" >&2
    exit 2
    ;;
esac

printf -v TMUX_CMD 'tmux new-session -A -s %q -c %q' "$SESSION" "$REPO_ROOT"

log() {
  echo "[open_tmux_terminal] $*" >&2
}

record_state() {
  STATE_TERMINAL_BACKEND="$1"
  STATE_OPEN_MODE="$2"
  STATE_WINDOW_CLOSE_SUPPORTED="${3:-0}"
  STATE_ITERM_WINDOW_ID="${4:-}"
  STATE_TERMINAL_WINDOW_ID="${5:-}"
  STATE_GHOSTTY_PID="${6:-}"
}

write_state_file() {
  if [[ -z "$STATE_FILE" ]]; then
    return 0
  fi

  cat >| "$STATE_FILE" <<EOF
SESSION=$SESSION
TERMINAL_BACKEND=$STATE_TERMINAL_BACKEND
OPEN_MODE=$STATE_OPEN_MODE
WINDOW_CLOSE_SUPPORTED=$STATE_WINDOW_CLOSE_SUPPORTED
ITERM_WINDOW_ID=$STATE_ITERM_WINDOW_ID
TERMINAL_WINDOW_ID=$STATE_TERMINAL_WINDOW_ID
GHOSTTY_PID=$STATE_GHOSTTY_PID
EOF
}

session_exists_exact() {
  local name="$1"
  tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -Fxq "$name"
}

wait_for_tmux_session() {
  local retries="${1:-20}"
  local delay="${2:-0.2}"
  local i
  for ((i = 1; i <= retries; i++)); do
    if session_exists_exact "$SESSION"; then
      return 0
    fi
    sleep "$delay"
  done
  return 1
}

escape_applescript() {
  local value="${1:-}"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  printf '%s' "$value"
}

collect_ghostty_pids() {
  {
    pgrep -x Ghostty 2>/dev/null || true
    pgrep -x ghostty 2>/dev/null || true
  } | awk 'NF { print $0 }' | sort -u
}

pick_new_ghostty_pid() {
  local before="$1"
  local after="$2"
  local pid
  while IFS= read -r pid; do
    [[ -n "$pid" ]] || continue
    if ! printf '%s\n' "$before" | grep -Fxq "$pid"; then
      printf '%s' "$pid"
      return 0
    fi
  done <<< "$after"
  return 1
}

is_ghostty_available() {
  [[ -d "/Applications/Ghostty.app" ]] || command -v ghostty >/dev/null 2>&1
}

is_iterm2_available() {
  osascript -e 'application "iTerm" exists' >/dev/null 2>&1
}

is_ghostty_running() {
  local stdout
  local applescript
  applescript=$(
    cat <<'EOF'
if application "Ghostty" is running then
    return "true"
else
    return "false"
end if
EOF
  )
  if stdout="$(osascript -e "$applescript" 2>/dev/null)"; then
    [[ "$stdout" == "true" ]]
    return
  fi
  pgrep -x Ghostty >/dev/null 2>&1 || pgrep -x ghostty >/dev/null 2>&1
}

open_in_running_ghostty_tab() {
  local escaped_cmd
  escaped_cmd="$(escape_applescript "$TMUX_CMD")"
  local applescript
  applescript=$(cat <<EOF
set the clipboard to "$escaped_cmd"
tell application "Ghostty"
    activate
end tell
tell application "System Events"
    if exists process "Ghostty" then
        tell process "Ghostty"
            keystroke "t" using command down
            delay 0.5
            keystroke "v" using command down
            delay 0.1
            keystroke return
        end tell
    else if exists process "ghostty" then
        tell process "ghostty"
            keystroke "t" using command down
            delay 0.5
            keystroke "v" using command down
            delay 0.1
            keystroke return
        end tell
    else
        error "Ghostty process not found"
    end if
end tell
EOF
)
  osascript -e "$applescript" >/dev/null 2>&1
}

open_in_ghostty() {
  local before_pids=""
  local after_pids=""
  local ghostty_pid=""

  if ! is_ghostty_available; then
    return 1
  fi

  if is_ghostty_running; then
    if [[ "$DRY_RUN" -eq 1 ]]; then
      echo "[DRY-RUN] Ghostty is running: open new tab and run: $TMUX_CMD"
      record_state "ghostty" "tab" "0"
      return 0
    fi
    if open_in_running_ghostty_tab; then
      if wait_for_tmux_session 15 0.2; then
        echo "Opened tmux in a new Ghostty tab."
        record_state "ghostty" "tab" "0"
        return 0
      fi
      log "Ghostty tab command was sent, but tmux session '$SESSION' was not created."
    else
      log "Ghostty tab open failed."
    fi
    log "Falling back to a new Ghostty window."
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY-RUN] Ghostty is not running: open new window first tab and run: $TMUX_CMD"
    record_state "ghostty" "window" "0"
    return 0
  fi

  before_pids="$(collect_ghostty_pids)"
  if ! open -na Ghostty.app --args -e tmux new-session -A -s "$SESSION" -c "$REPO_ROOT" >/dev/null 2>&1; then
    log "Ghostty new-window launch failed."
    return 1
  fi
  if ! wait_for_tmux_session 25 0.2; then
    log "Ghostty new-window command finished, but tmux session '$SESSION' was not created."
    return 1
  fi

  after_pids="$(collect_ghostty_pids)"
  ghostty_pid="$(pick_new_ghostty_pid "$before_pids" "$after_pids" || true)"
  if [[ -n "$ghostty_pid" ]]; then
    record_state "ghostty" "window" "1" "" "" "$ghostty_pid"
  else
    log "WARN: Ghostty window PID could not be identified. window cleanup will be skipped."
    record_state "ghostty" "window" "0"
  fi

  echo "Opened tmux in a new Ghostty window."
  return 0
}

open_in_iterm2() {
  local escaped_cmd
  local applescript
  local stdout
  local mode
  local window_id

  if ! is_iterm2_available; then
    return 1
  fi

  escaped_cmd="$(escape_applescript "$TMUX_CMD")"
  applescript=$(cat <<EOF
tell application "iTerm"
    activate
    if (count of windows) > 0 then
        tell current window
            create tab with default profile
            tell current session
                write text "$escaped_cmd"
            end tell
            return "tab|"
        end tell
    else
        set newWindow to (create window with default profile)
        tell current session of newWindow
            write text "$escaped_cmd"
        end tell
        return "window|" & (id of newWindow as text)
    end if
end tell
EOF
)

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY-RUN] iTerm2: existing window -> new tab, otherwise new window first tab. Command: $TMUX_CMD"
    record_state "iterm2" "tab" "0"
    return 0
  fi

  if ! stdout="$(osascript -e "$applescript" 2>/dev/null)"; then
    return 1
  fi
  stdout="${stdout//$'\r'/}"
  stdout="${stdout//$'\n'/}"

  mode="${stdout%%|*}"
  window_id=""
  if [[ "$stdout" == *"|"* ]]; then
    window_id="${stdout#*|}"
  fi

  if [[ "$mode" == "window" && "$window_id" =~ ^[0-9]+$ ]]; then
    record_state "iterm2" "window" "1" "$window_id"
  elif [[ "$mode" == "window" ]]; then
    log "WARN: iTerm2 window opened but window id was not resolved."
    record_state "iterm2" "window" "0"
  else
    record_state "iterm2" "tab" "0"
  fi

  echo "Opened tmux in iTerm2."
  return 0
}

open_in_terminal_app() {
  local applescript
  local escaped_cmd
  local stdout
  local mode
  local window_id

  escaped_cmd="$(escape_applescript "$TMUX_CMD")"
  applescript=$(cat <<EOF
tell application "Terminal"
    activate
    if (count of windows) > 0 then
        tell front window
            do script "$escaped_cmd"
        end tell
        return "tab|"
    else
        do script "$escaped_cmd"
        delay 0.1
        set newWindow to front window
        return "window|" & (id of newWindow as text)
    end if
end tell
EOF
)

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY-RUN] Terminal.app: existing window -> new tab, otherwise new window first tab. Command: $TMUX_CMD"
    record_state "terminal" "tab" "0"
    return 0
  fi

  if ! stdout="$(osascript -e "$applescript" 2>/dev/null)"; then
    return 1
  fi
  stdout="${stdout//$'\r'/}"
  stdout="${stdout//$'\n'/}"

  mode="${stdout%%|*}"
  window_id=""
  if [[ "$stdout" == *"|"* ]]; then
    window_id="${stdout#*|}"
  fi

  if [[ "$mode" == "window" && "$window_id" =~ ^[0-9]+$ ]]; then
    record_state "terminal" "window" "1" "" "$window_id"
  elif [[ "$mode" == "window" ]]; then
    log "WARN: Terminal.app window opened but window id was not resolved."
    record_state "terminal" "window" "0"
  else
    record_state "terminal" "tab" "0"
  fi

  echo "Opened tmux in Terminal.app."
  return 0
}

open_in_current_shell() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY-RUN] Current shell fallback: $TMUX_CMD"
    record_state "current_shell" "current_shell" "0"
    return 0
  fi
  tmux new-session -A -s "$SESSION" -c "$REPO_ROOT"
  record_state "current_shell" "current_shell" "0"
}

OPENED=0

case "$TERMINAL" in
  ghostty)
    if open_in_ghostty; then
      OPENED=1
    else
      echo "failed to open in Ghostty" >&2
      exit 1
    fi
    ;;
  iterm2)
    if open_in_iterm2; then
      OPENED=1
    else
      echo "failed to open in iTerm2" >&2
      exit 1
    fi
    ;;
  terminal)
    if open_in_terminal_app; then
      OPENED=1
    else
      echo "failed to open in Terminal.app" >&2
      exit 1
    fi
    ;;
  auto)
    if open_in_ghostty; then
      OPENED=1
    elif open_in_iterm2; then
      OPENED=1
    elif open_in_terminal_app; then
      OPENED=1
    else
      echo "Ghostty/iTerm2/Terminal.app unavailable. Falling back to current shell."
      if open_in_current_shell; then
        OPENED=1
      fi
    fi
    ;;
esac

if [[ "$OPENED" -ne 1 ]]; then
  echo "failed to open terminal for tmux session: $SESSION" >&2
  exit 1
fi

write_state_file
