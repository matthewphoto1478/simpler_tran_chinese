#!/bin/sh
# Portable launcher: use python3 when it actually runs, else fall back to python.
# Windows Python installs expose `python` but often only a non-functional
# Microsoft Store alias named `python3`; POSIX systems commonly have `python3`
# only. `command -v` is not enough on Windows, because the Store stub is on
# PATH yet fails when executed, so probe by running it.
if python3 -c "" >/dev/null 2>&1; then
  exec python3 "$@"
fi
exec python "$@"
