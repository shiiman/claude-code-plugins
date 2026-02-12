#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  open_tmux_terminal.sh --session <name> --repo-root <path> [--terminal <auto|ghostty|iterm2|terminal>] [--dry-run]

Options:
  --session <name>      tmux session name (allowed: [A-Za-z0-9._:-])
  --repo-root <path>    repository root path
  --terminal <value>    auto | ghostty | iterm2 | terminal (default: auto)
  --dry-run             print selected behavior without opening terminals
  -h, --help            show this help
USAGE
}

SESSION=""
REPO_ROOT=""
TERMINAL="auto"
DRY_RUN=0

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

case "$TERMINAL" in
  auto|ghostty|iterm2|terminal)
    ;;
  *)
    echo "invalid --terminal value: $TERMINAL" >&2
    exit 2
    ;;
esac

printf -v TMUX_CMD 'tmux new-session -A -s %q -c %q' "$SESSION" "$REPO_ROOT"

escape_applescript() {
  local value="${1:-}"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  printf '%s' "$value"
}

is_ghostty_available() {
  [[ -d "/Applications/Ghostty.app" ]] || command -v ghostty >/dev/null 2>&1
}

is_iterm2_available() {
  osascript -e 'application "iTerm" exists' >/dev/null 2>&1
}

is_ghostty_running() {
  local stdout
  if stdout="$(osascript -e 'if application "Ghostty" is running then return "true" else return "false" end if' 2>/dev/null)"; then
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
  if ! is_ghostty_available; then
    return 1
  fi

  if is_ghostty_running; then
    if [[ "$DRY_RUN" -eq 1 ]]; then
      echo "[DRY-RUN] Ghostty is running: open new tab and run: $TMUX_CMD"
      return 0
    fi
    if open_in_running_ghostty_tab; then
      echo "Opened tmux in a new Ghostty tab."
      return 0
    fi
    echo "Ghostty tab open failed, falling back to new window." >&2
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY-RUN] Ghostty is not running: open new window first tab and run: $TMUX_CMD"
    return 0
  fi

  if ! open -a Ghostty.app --args -e /bin/bash -lc "$TMUX_CMD" >/dev/null 2>&1; then
    return 1
  fi
  echo "Opened tmux in a new Ghostty window."
  return 0
}

open_in_iterm2() {
  if ! is_iterm2_available; then
    return 1
  fi

  local escaped_cmd
  escaped_cmd="$(escape_applescript "$TMUX_CMD")"
  local applescript
  applescript=$(cat <<EOF
tell application "iTerm"
    activate
    if (count of windows) > 0 then
        tell current window
            create tab with default profile
            tell current session
                write text "$escaped_cmd"
            end tell
        end tell
    else
        create window with default profile
        tell current session of current window
            write text "$escaped_cmd"
        end tell
    end if
end tell
EOF
)

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY-RUN] iTerm2: existing window -> new tab, otherwise new window first tab. Command: $TMUX_CMD"
    return 0
  fi

  if ! osascript -e "$applescript" >/dev/null 2>&1; then
    return 1
  fi
  echo "Opened tmux in iTerm2."
  return 0
}

open_in_terminal_app() {
  local escaped_cmd
  escaped_cmd="$(escape_applescript "$TMUX_CMD")"
  local applescript
  applescript=$(cat <<EOF
tell application "Terminal"
    activate
    if (count of windows) > 0 then
        tell front window
            do script "$escaped_cmd"
        end tell
    else
        do script "$escaped_cmd"
    end if
end tell
EOF
)

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY-RUN] Terminal.app: existing window -> new tab, otherwise new window first tab. Command: $TMUX_CMD"
    return 0
  fi

  if ! osascript -e "$applescript" >/dev/null 2>&1; then
    return 1
  fi
  echo "Opened tmux in Terminal.app."
  return 0
}

open_in_current_shell() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY-RUN] Current shell fallback: $TMUX_CMD"
    return 0
  fi
  tmux new-session -A -s "$SESSION" -c "$REPO_ROOT"
}

case "$TERMINAL" in
  ghostty)
    if ! open_in_ghostty; then
      echo "failed to open in Ghostty" >&2
      exit 1
    fi
    ;;
  iterm2)
    if ! open_in_iterm2; then
      echo "failed to open in iTerm2" >&2
      exit 1
    fi
    ;;
  terminal)
    if ! open_in_terminal_app; then
      echo "failed to open in Terminal.app" >&2
      exit 1
    fi
    ;;
  auto)
    if open_in_ghostty; then
      exit 0
    fi
    if open_in_iterm2; then
      exit 0
    fi
    if open_in_terminal_app; then
      exit 0
    fi
    echo "Ghostty/iTerm2/Terminal.app unavailable. Falling back to current shell."
    open_in_current_shell
    ;;
esac
