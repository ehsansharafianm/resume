#!/bin/bash
# Rebuild the master resume outputs on macOS and Linux.
# Double-click in Finder (macOS) or run from a terminal.
# The Windows equivalent is Render-Master.cmd.

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
"$PY" "$DIR/system/resume_tool.py" render \
  -Input "$DIR/master/Ehsan_Sharafian_Master.yaml" \
  -OutputHtml "$DIR/system/index.html" \
  -OutputPdf "$DIR/Ehsan-Sharafian-Resume.pdf" "$@"

exit $?
