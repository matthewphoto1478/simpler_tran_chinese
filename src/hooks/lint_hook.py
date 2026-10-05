#!/usr/bin/env python3
"""Advisory writing checks for Claude Code hooks. Never blocks.

PostToolUse (Write|Edit on a .md file): lint the file with evals/ste_lint.py
and, when it has violations, print the offending text and line number for
each hit (capped at MAX_HOOK_HITS) to stderr and exit 2 so the model sees
it. Exit 2 on PostToolUse is advisory: the tool already ran. Agent-internal
Markdown, such as memory files under the Claude configuration directory, is
skipped. The writing rules do not govern it, and a summary of its
violations only spends tokens. Set SIMPLE_ENGLISH_LINT_EXCLUDE to skip more
paths.

Stop: read `last_assistant_message`, check the reply register (no headers,
bullets, bold, or em-dashes), and return a systemMessage only when the reply
breaks it. Always exit 0, so the session never loops.
"""
import fnmatch
import inspect
import json
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "evals"))

MAX_HOOK_HITS = 12
CLAUDE_DIR = ".claude"
_UNSET = object()
OPENERS = re.compile(r"^\s*(certainly|great question|you're absolutely right|sure[,!]|absolutely[,!])", re.I)
CLOSERS = re.compile(r"(i hope this helps|let me know if|feel free to)", re.I)

def load_linter():
 """Return a module exposing lint(text, profile) -> report, or None.

 The linter lives in tools/ste-dictionary. evals/ste_lint.py is only a self-test
 wrapper, so it must not shadow the real implementation on sys.path.
 """
 for candidate in (str(ROOT / "tools" / "ste-dictionary"), str(ROOT / "evals")):
  if candidate not in sys.path:
   sys.path.insert(0, candidate)
 try:
  import ste_dict_lint as linter
 except Exception: # noqa: BLE001
  try:
   import ste_lint as linter # noqa: N813
  except Exception: # noqa: BLE001
   return None
 return _compat(linter)

def _compat(linter):
 """Give the linter the API the hooks call, degrading when a method is absent."""
 if not hasattr(linter, "lint_detail"):
  def lint_detail(text, profile):
   """One entry per hit, with the line number when the linter reports one.

   The two linters take different arguments. ste_dict_lint.lint is
   (text, table=None, slop=None) and returns {"hits", "slop_hits"};
   ste_lint.lint is (text, profile=...) and returns {"violations": {"all"}}.
   Calling either with the other's signature raises TypeError, so dispatch on
   the real parameters instead of assuming one shape.
   """
   params = inspect.signature(linter.lint).parameters
   if "table" in params:
    try:
     report = linter.lint(text, table=None)
    except FileNotFoundError:
     # The dictionary files are intentionally absent, so the dictionary rules
     # cannot run. Report no hits instead of propagating: the caller still
     # applies the mechanical rules, and the hook must never raise.
     return []
    hits = []
    for item in report.get("hits", []):
     hits.append({"category": "not_approved", "line": None, "text": item.get("used", "")})
    for item in report.get("slop_hits", []):
     hits.append({"category": "slop", "line": None, "text": item.get("used", "")})
   else:
    report = linter.lint(text)
    hits = [{"category": item.get("category", ""), "line": item.get("line"),
             "text": item.get("text", "")}
            for item in report.get("violations", {}).get("all", [])]
   hits.sort(key=lambda hit: hit["line"] or 0)
   return hits
  linter.lint_detail = lint_detail
 if not hasattr(linter, "reader_check"):
  def reader_check(reply):
   """Counts the hook reports on. The linter reads text, not layout."""
   lines = reply.splitlines()
   return {"counts": {
    "em_dash": reply.count("—") + reply.count(" - "),
    "bold_spans": reply.count("**") // 2,
    "headers": sum(1 for line in lines if line.startswith("#")),
    "bullets": sum(1 for line in lines
                   if line.lstrip().startswith(("- ", "* ", "+ ")))}}
  linter.reader_check = reader_check
 return linter

def strip_code(text):
 text = re.sub(r"```.*?```", " ", text, flags=re.S)
 return re.sub(r"`[^`]*`", " ", text)

def absolute(path, cwd=None):
 """Make the path absolute. The harness can send it relative to the session directory."""
 return pathlib.Path(cwd or ".", pathlib.Path(path).expanduser()).absolute()

def variants(path):
 """The path as written and the path with symlinks resolved. An exclusion matches either form.

 A symlink hides a directory name in both directions. `notes.md` can point into `.claude`,
 and `.claude` itself can point at a dotfiles repository. Both forms must miss for the
 file to reach the linter.
 """
 return {pathlib.Path(os.path.normpath(path)), path.resolve()}

def excluded(target):
 """True for agent-internal Markdown and for the paths the user excludes."""
 config_dirs = variants(absolute(os.environ.get("CLAUDE_CONFIG_DIR") or f"~/{CLAUDE_DIR}"))
 raw = os.environ.get("SIMPLE_ENGLISH_LINT_EXCLUDE", "").split(os.pathsep)
 patterns = [os.path.expanduser(p) for p in raw if p]
 for form in variants(target):
  if CLAUDE_DIR in form.parts or any(form.is_relative_to(d) for d in config_dirs):
   return True
  if any(fnmatch.fnmatch(str(form), p) for p in patterns):
   return True
 return False

def post_tool_use(event):
 path = (event.get("tool_input") or {}).get("file_path") or ""
 if not path.endswith(".md"):
  return 0
 target = absolute(path, event.get("cwd"))
 if excluded(target):
  return 0
 lint = load_linter()
 if lint is None:
  return 0
 try:
  text = target.read_text(encoding="utf-8")
 except OSError:
  return 0
 # The dictionary linter raises FileNotFoundError when the Issue 9 word lists
 # are absent, which is the default state of a fresh install, and the
 # mechanical linter needs no data files at all. Try the dictionary first and
 # fall back to the mechanical result, so a missing list degrades the report
 # rather than aborting it.
 try:
  report = lint.lint(text)
  na = report.get("not_approved", 0) or 0
  slop = report.get("slop", 0) or 0
 except Exception: # noqa: BLE001
  na = 0
  slop = 0
 if not na and not slop:
  # _mechanical_detail returns EVERY category, so a file whose only hits are
  # contraction, modal, semicolon or present perfect is reported too. Counting
  # slop alone here would call such a file clean while the detail below had
  # rows ready to print.
  if not _mechanical_detail(text):
   return 0
  na = 1
 try:
  detail = lint.lint_detail(text, "descriptive")
 except Exception: # noqa: BLE001
  detail = []
 if not detail:
  # The dictionary linter found nothing, so its detail is empty even when the
  # mechanical rules have hits. Fall back to those, or the file would be
  # reported as clean.
  detail = _mechanical_detail(text)
 if not detail:
  return 0
 violations_total = len(detail)
 lines = [f"simple-english: {target.name} has {violations_total} STE violations."]
 for hit in detail[:MAX_HOOK_HITS]:
  lines.append("  line {line}, {cat}: {text}".format(
   line=hit.get("line"), cat=hit.get("category", ""), text=hit.get("text", "")))
 if len(detail) > MAX_HOOK_HITS:
  lines.append(f"  and {len(detail) - MAX_HOOK_HITS} more hit(s).")
 lines.append("Fix these hits in the file you just wrote, then continue.")
 sys.stderr.write("\n".join(lines) + "\n")
 return 2

def stop(event):
 reply = event.get("last_assistant_message") or ""
 problems = []
 lint = load_linter()
 if lint is not None:
  counts = lint.reader_check(reply)["counts"]
  for key, label in (("em_dash", "em-dash"), ("bold_spans", "bold span"),
                      ("headers", "header"), ("bullets", "list item")):
   if counts[key]:
    problems.append(f"{counts[key]} {label}(s)")
  # The Issue 9 word lists are not in this repository, so lint() raises when
  # they are missing. The layout counts above do not need a dictionary, and the
  # reply rules are the default mode, so a missing dictionary must not discard
  # them. Keep the counts only when the linter can actually run.
  try:
   lint_result = lint.lint(strip_code(reply))
   slop = lint_result.get("slop", 0)
   not_approved = lint_result.get("not_approved", 0)
  except Exception: # noqa: BLE001
   slop = 0
   not_approved = 0
  # The dictionary linter counts words from the Issue 9 lists, which are not in
  # this repository. Without them it reports 0, which would silently drop every
  # slop hit. The mechanical linter needs no dictionary and reads the committed
  # evals/slop.tsv, so merge its hits in as a floor rather than losing them.
  for category, count in _mechanical_counts(reply):
   if category == "slop":
    slop = max(slop, count)
   else:
    not_approved = max(not_approved, count)
  if slop:
   problems.append(f"{slop} slop word(s)")
  if not_approved:
   problems.append(f"{not_approved} word(s) not approved in STE")
 if OPENERS.search(reply):
  problems.append("a filler opener")
 if CLOSERS.search(reply):
  problems.append("a filler closer")
 if problems:
  print(json.dumps({"systemMessage": "simple-english reply check: "
                   + "; ".join(problems) + ". Answer in prose."}))
 return 0

def _mechanical():
 """Return the mechanical linter module, or None if it cannot be imported.

 evals/ste_lint.py needs no word-list data files, so it still works when the
 Issue 9 dictionaries are absent. The import is cached and both call sites
 share this one accessor, so they cannot drift apart.
 """
 if _mechanical.module is _UNSET:
  try:
   if str(ROOT / "evals") not in sys.path:
    sys.path.insert(0, str(ROOT / "evals"))
   import ste_lint as mechanical
  except Exception: # noqa: BLE001
   mechanical = None
  _mechanical.module = mechanical
 return _mechanical.module


_mechanical.module = _UNSET

def _mechanical_hits(text):
 """Return the mechanical linter's violation hits, or [].

 Every category is returned, not only slop. A caller that filtered to slop
 alone would report a file whose only hits are contraction, modal or semicolon
 as clean, which is the same silent-drop this function exists to prevent.
 """
 mechanical = _mechanical()
 if mechanical is None or not hasattr(mechanical, "lint"):
  return []
 try:
  report = mechanical.lint(strip_code(text))
  return report.get("violations", {}).get("all", [])
 except Exception: # noqa: BLE001
  return []

def _mechanical_counts(reply):
 """Return (category, count) pairs for the reply summary.

 Only slop is summarised. src/hooks/README.md defines the Stop message as
 layout defects, filler openers and closers, and redundant words, so the
 mechanical grammar rules are not part of the reply summary.
 """
 hits = _mechanical_hits(reply)
 slop = sum(1 for hit in hits if hit.get("category", "").startswith("slop"))
 return [("slop", slop)] if slop else []

def _mechanical_detail(text):
 """Return file-check detail rows, shaped like lint_detail() output."""
 rows = [{"category": hit.get("category", ""), "line": None,
          "text": hit.get("text", "")} for hit in _mechanical_hits(text)]
 rows.sort(key=lambda row: row["text"])
 return rows

def main():
 try:
  event = json.load(sys.stdin)
 except Exception: # noqa: BLE001
  return 0
 try:
  name = event.get("hook_event_name", "")
  if name == "PostToolUse":
   return post_tool_use(event)
  if name == "Stop":
   return stop(event)
 except Exception: # noqa: BLE001 advisory hook: a crash must never block or loop the session
  return 0
 return 0

if __name__ == "__main__":
 sys.exit(main())
