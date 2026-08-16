#!/bin/bash
# Re-render this application on macOS and Linux.
# Double-click in Finder (macOS) or run from a terminal.
# Builds the HTML and opens it in your browser; use Print (Cmd+P) >
# Save as PDF. The Windows equivalent (Render.cmd) writes the PDF directly.
DIR="$(cd "$(dirname "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Python 3 was not found. Install it from https://www.python.org/downloads/ and try again."
  exit 1
fi
"$PY" "$DIR/../../../system/resume_tool.py" render -Input "$DIR/resume.yaml" -OutputHtml "$DIR/index.html" -SkipPdf -Open "$@"
