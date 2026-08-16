#!/bin/bash
# Interactive job-application wizard for macOS and Linux.
# Double-click in Finder (macOS) or run from a terminal.
# The Windows equivalent is New-Application.cmd.

DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Python 3 was not found. Install it from https://www.python.org/downloads/ and try again."
  read -n 1 -s -r -p "Press any key to close this window..."
  echo ""
  exit 1
fi

"$PY" "$DIR/system/resume_tool.py" migrate --quiet

if [ "$#" -eq 0 ]; then
  clear
  "$PY" "$DIR/system/resume_tool.py" wizard
else
  "$PY" "$DIR/system/resume_tool.py" create "$@"
fi

exit $?
