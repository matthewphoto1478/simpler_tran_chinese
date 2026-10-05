#!/usr/bin/env python3
"""Self-tests for the reply and file checks the hooks actually run.

`tools/ste-dictionary/ste_dict_lint.py` measures word choice. The reply rules
(`src/hooks/lint_hook.py`) are a separate concern: they count layout defects in
a chat reply, and check vocabulary on the text with code stripped.

These tests drive the two hook entry points -- `stop()` for a chat reply and
`post_tool_use()` for a written file -- so a regression in the rules the model
is shown fails the build instead of silently changing the feedback it gets.

The English mechanical rules (modal verbs, present perfect, dangling -ing) are
NOT covered here: no module in this repository implements them, so there is
nothing to test. The vocabulary linter is exercised by
`tools/ste-dictionary/ste_dict_lint.py --self-test`.

Usage:
 python3 src/hooks/test_reply_rules.py
"""
import importlib
import io
import json
import pathlib
import sys
from contextlib import redirect_stdout

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src" / "hooks"))

import lint_hook


def run_stop(reply):
 """Run the Stop hook and return the systemMessage it emits, or None."""
 buf = io.StringIO()
 with redirect_stdout(buf):
  lint_hook.stop({"hook_event_name": "Stop", "last_assistant_message": reply})
 out = buf.getvalue().strip()
 if not out:
  return None
 return json.loads(out).get("systemMessage", "")


def test_flagged_replies():
 """A reply carrying layout defects or filler is reported."""
 cases = [
  ("Certainly! Use the **bold** header here.", "bold span"),
  ("Check the logs — then restart.", "em-dash"),
  ("I hope this helps.", "filler closer"),
  ("Sure, here are the steps:\n- one\n- two", "list item"),
 ]
 for reply, expected in cases:
  message = run_stop(reply)
  if message is None:
   print(f"FAIL: expected a report for: {reply!r}")
   return False
  if expected not in message:
   print(f"FAIL: expected {expected!r} in report for {reply!r}")
   print(f" message: {message}")
   return False
 return True


def test_clean_reply():
 """A plain prose reply is not reported."""
 cases = [
  "Check the logs, then restart the service.",
  "The service stopped because the port was in use.",
  "Run the migration, then start the server.",
 ]
 for reply in cases:
  message = run_stop(reply)
  if message is not None:
   print(f"FAIL: unexpected report for: {reply!r}")
   print(f" message: {message}")
   return False
 return True


def test_strip_code():
 """Code spans and fences are removed before counting."""
 stripped = lint_hook.strip_code("Use `run --now` and:\n```\n--flag x\n```\n")
 if "run --now" in stripped or "--flag" in stripped:
  print(f"FAIL: code not stripped: {stripped!r}")
  return False
 if "Use" not in stripped:
  print(f"FAIL: prose was removed: {stripped!r}")
  return False
 return True


def test_load_linter():
 """The linter is found and exposes the API the hooks call."""
 linter = lint_hook.load_linter()
 # Assert the linter loads, not merely that loading cannot fail: the hooks all
 # no-op when this returns None, so a silent load failure would disable the
 # reply check entirely while this test still passed.
 if linter is None:
  print("FAIL: load_linter() returned None; the reply check would be disabled")
  return False
 for attr in ("lint", "reader_check", "lint_detail"):
  if not hasattr(linter, attr):
   print(f"FAIL: linter is missing {attr}()")
   return False
 return True


def test_lint_detail_runs():
 """lint_detail() is called, not merely present, and works on both linters.

 hasattr() is not enough: the compatibility shim used to call
 lint(text, table=None) unconditionally, which is the ste_dict_lint signature.
 On the ste_lint path that signature is (text, profile=...), so every call
 raised TypeError. The hook survived it because post_tool_use wraps the call
 in `except Exception` and falls back to the mechanical rules, so the tests
 above stayed green while the documented API was broken.

 Both modules are exercised deliberately. ste_dict_lint is what load_linter()
 returns, but its dictionary files are intentionally absent, so it can only be
 checked for a well-formed empty result; ste_lint is the path that actually
 produces hits, and it is the one the broken shim broke.
 """
 text = "This is crucial and robust for the team. You should utilize leverage."

 for name in ("ste_dict_lint", "ste_lint"):
  if name not in sys.path:
   sys.path.insert(0, str(ROOT / "tools" / "ste-dictionary") if name == "ste_dict_lint"
                   else str(ROOT / "evals"))
  linter = lint_hook._compat(importlib.import_module(name))
  try:
   detail = linter.lint_detail(text, "descriptive")
  except Exception as exc:
   print(f"FAIL: {name}.lint_detail() raised {type(exc).__name__}: {exc}")
   return False
  if not isinstance(detail, list):
   print(f"FAIL: {name}.lint_detail() returned {type(detail).__name__}, expected list")
   return False
  for row in detail:
   if not {"category", "line", "text"} <= set(row):
    print(f"FAIL: {name}.lint_detail() row missing keys: {row!r}")
    return False

 # ste_lint must actually report the mechanical violations above. An empty
 # result for every input would satisfy the shape checks while reporting
 # nothing, which is how the previous version failed unnoticed.
 if not detail:
  print("FAIL: ste_lint.lint_detail() returned no hits for text with known violations")
  return False
 categories = {row["category"] for row in detail}
 if "slop_word" not in categories:
  print(f"FAIL: expected a slop_word category, got {sorted(categories)}")
  return False

 # The live linter must also answer without raising, whatever it is.
 live = lint_hook.load_linter()
 if live is None:
  print("FAIL: load_linter() returned None")
  return False
 try:
  live.lint_detail(text, "descriptive")
 except Exception as exc:
  print(f"FAIL: loaded linter.lint_detail() raised {type(exc).__name__}: {exc}")
  return False
 return True


def test_reader_check_runs():
 """reader_check() returns the layout counts the Stop hook reports."""
 linter = lint_hook.load_linter()
 if linter is None:
  print("FAIL: load_linter() returned None")
  return False
 try:
  report = linter.reader_check("# Header\n- **bold** bullet\n")
 except Exception as exc:
  print(f"FAIL: reader_check() raised {type(exc).__name__}: {exc}")
  return False
 if not isinstance(report, dict) or "counts" not in report:
  print(f"FAIL: reader_check() returned {report!r}, expected a 'counts' dict")
  return False
 counts = report["counts"]
 for key in ("em_dash", "bold_spans", "headers", "bullets"):
  if key not in counts:
   print(f"FAIL: reader_check() counts missing {key!r}")
   return False
 if counts["headers"] != 1 or counts["bullets"] != 1 or counts["bold_spans"] != 1:
  print(f"FAIL: reader_check() miscounted: {counts}")
  return False
 return True


def main():
 print("Running reply-rule self-tests...")
 tests = [
  ("Flagged replies", test_flagged_replies),
  ("Clean replies", test_clean_reply),
  ("Strip code", test_strip_code),
  ("Load linter", test_load_linter),
  ("lint_detail runs", test_lint_detail_runs),
  ("reader_check runs", test_reader_check_runs),
 ]
 all_passed = True
 for name, fn in tests:
  try:
   if fn():
    print(f" PASS: {name}")
   else:
    print(f" FAIL: {name}")
    all_passed = False
  except Exception as exc:
   print(f" ERROR: {name}: {exc}")
   all_passed = False
 if all_passed:
  print("\nAll self-tests passed.")
  return 0
 print("\nSome self-tests failed.")
 return 1


if __name__ == "__main__":
 sys.exit(main())