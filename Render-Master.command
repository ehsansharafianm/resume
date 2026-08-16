#!/bin/bash
# Rebuild the master resume on macOS and Linux.
# Double-click in Finder (macOS) or run from a terminal.
# Builds the HTML and opens it in your browser; use Print (Cmd+P) > Save as PDF.
# The Windows equivalent (Render-Master.cmd) writes the PDF directly.

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
  -SkipPdf -Open "$@"

exit $?
