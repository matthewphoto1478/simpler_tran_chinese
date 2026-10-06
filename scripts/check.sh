#!/bin/sh
# Local equivalent of `.github/workflows/check.yml` (removed when the push
# token lacked the `workflow` scope). Run this before pushing to reproduce
# CI's seven checks. `python3` is preferred; `python` is the fallback on
# Windows, where the Microsoft Store alias stub is on PATH but fails.
if python3 -c "" >/dev/null 2>&1; then
  PY=python3
else
  PY=python
fi
set -e
node --test src/hooks/simple-english-activate.test.js
"$PY" src/hooks/test_lint_hook.py
"$PY" src/hooks/test_reply_rules.py
"$PY" tools/ste-dictionary/ste_dict_lint.py --self-test
"$PY" evals/ste_lint.py --self-test
"$PY" evals/check_numbers.py
"$PY" -m unittest evals.test_run_pi_bench
