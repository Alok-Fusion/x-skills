#!/usr/bin/env bash
# Install the x-skills pack for any agent that reads Agent Skills (SKILL.md).
#
#   ./install.sh                 # ~/.agents/skills and ~/.claude/skills
#   ./install.sh --target agents # Codex, Gemini CLI, GitHub Copilot
#   ./install.sh --target claude # Claude Code, Cursor, GitHub Copilot
#   ./install.sh --target DIR    # any other skills folder
#   ./install.sh --uninstall     # remove what this script installed
#   ./install.sh --force         # also replace x-* skills it didn't install
#
# It only replaces a skill folder that it installed before (marked with a
# .x-skills file), so your own skills with the same name are left alone.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/skills"
TARGET="all"
UNINSTALL=0
FORCE=0
VERSION="$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$HERE/.claude-plugin/plugin.json" | head -1)"

while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="${2:?--target needs a value}"; shift 2 ;;
    --target=*) TARGET="${1#*=}"; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    --force) FORCE=1; shift ;;
    -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

case "$TARGET" in
  all)    DIRS=("$HOME/.agents/skills" "$HOME/.claude/skills") ;;
  agents) DIRS=("$HOME/.agents/skills") ;;
  claude) DIRS=("$HOME/.claude/skills") ;;
  *)      DIRS=("$TARGET") ;;
esac

installed=0
skipped=0
for dir in "${DIRS[@]}"; do
  mkdir -p "$dir"
  for skill in "$SRC"/*/; do
    name="$(basename "$skill")"
    dest="$dir/$name"
    if [ "$UNINSTALL" -eq 1 ]; then
      if [ -f "$dest/.x-skills" ]; then rm -rf "$dest"; installed=$((installed + 1)); fi
      continue
    fi
    if [ -e "$dest" ] && [ ! -f "$dest/.x-skills" ] && [ "$FORCE" -ne 1 ]; then
      echo "skip  $dest (not installed by x-skills; use --force to replace)"
      skipped=$((skipped + 1))
      continue
    fi
    rm -rf "$dest"
    cp -R "$skill" "$dest"
    echo "x-skills $VERSION" > "$dest/.x-skills"
    installed=$((installed + 1))
  done
  echo "$([ "$UNINSTALL" -eq 1 ] && echo removed || echo installed) -> $dir"
done

if [ "$UNINSTALL" -eq 1 ]; then
  echo "Removed $installed skill folders. Your ~/.x-skills/ files were kept."
  exit 0
fi

# The voice file every skill reads. Never overwrite one that exists.
mkdir -p "$HOME/.x-skills/drafts"
if [ ! -f "$HOME/.x-skills/voice.md" ]; then
  cp "$SRC/x-post/assets/voice-template.md" "$HOME/.x-skills/voice.md"
  echo "created ~/.x-skills/voice.md (fill it in, or let x-post ask you)"
fi

if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
  echo "note: Python 3.8+ is needed for the x-human checker (scripts/xcheck.py)."
fi
echo "Done: $installed skill folders installed, $skipped skipped."
