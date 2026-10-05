#!/usr/bin/env python3
"""Check that every published number matches the raw files it came from.

Every number in README.md, SKILL.md, and RESULTS.md that claims to come from
an eval run is recomputed from the committed raw JSON files. A mismatch
fails the build. This script runs in CI on every push.

Usage:
 python3 evals/check_numbers.py
 python3 evals/check_numbers.py --verbose
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"

# Numbers in the source files, keyed by a unique tag.
# Values are (file, regex) pairs. The regex must have one capture group
# that is the number. The check recomputes the number from the raw files
# and asserts equality.
# The published sentence ends the number with a full-width ideographic stop,
# as in "218 → 11。". An earlier pattern expected an ASCII "(" here, so it
# never matched and every run skipped silently. Matching the real text lets
# the check report SKIP for the right reason when the raw files are absent.
PUBLISHED = {
 # README.md
 "reply_total_no_skill": ("README.md", r"(\d+)\s+→\s+\d+。"),
 "reply_total_with_skill": ("README.md", r"\d+\s+→\s+(\d+)。"),
 # SKILL.md (none currently)
 # CHANGELOG.md (none currently)
}

def load_raw(path):
 return json.loads(path.read_text(encoding="utf-8"))

def count_defects(replies):
 """Count visible defects in a list of reply strings.

 Counts: em-dashes, bold spans, headers, list items. Over-cap sentences are
 reported but NOT added to the total: CHANGELOG 2.1.0 removed the sentence
 limit and recomputed the published figures (218 -> 11) on these four
 categories alone. Including over_cap here would recompute a different
 quantity than the one the README publishes, and the check would fail on a
 correct tree.

 Returns a dict with counts and totals.
 """
 total = 0
 by_type = {}
 for reply in replies:
  if isinstance(reply, dict):
   text = reply.get("text") or ""
  else:
   text = reply or ""
  # A malformed raw entry must not crash the gate: normalise to a string
  # here so every count below sees one.
  text = text if isinstance(text, str) else ""
  # em-dashes
  dashes = len(re.findall(r"—", text))
  # bold
  bold = len(re.findall(r"\*\*.+?\*\*", text))
  # headers
  headers = len(re.findall(r"^#+\s+", text, re.MULTILINE))
  # bullets
  bullets = len(re.findall(r"^\s*[-*]\s+", text, re.MULTILINE))
  # over-cap sentences (>25 words), reported only
  sentences = re.split(r"[.!?]+", text)
  over_cap = sum(1 for s in sentences if len(s.split()) > 25)
  total += dashes + bold + headers + bullets
  by_type.setdefault("em_dash", 0)
  by_type["em_dash"] += dashes
  by_type.setdefault("bold", 0)
  by_type["bold"] += bold
  by_type.setdefault("headers", 0)
  by_type["headers"] += headers
  by_type.setdefault("bullets", 0)
  by_type["bullets"] += bullets
  by_type.setdefault("over_cap", 0)
  by_type["over_cap"] += over_cap
 return {"total": total, "by_type": by_type}

def compute_reply_stats(raw_dir):
 """Compute aggregate reply defect counts from raw JSON files."""
 raw_dir = pathlib.Path(raw_dir)
 replies = []
 for f in raw_dir.glob("*__reply__*.json"):
  data = load_raw(f)
  replies.extend(data.get("replies", []) if isinstance(data, dict) else data)
 if not replies:
  return None
 counts = count_defects(replies)
 return {
 "total_defects": counts["total"],
 "by_type": counts["by_type"],
 "num_replies": len(replies),
 }

def check(verbose=False):
 """Run all checks. Returns True if no check failed.

 Each check is PASS, FAIL, or SKIP. SKIP means the evidence needed to verify the
 number is not in the repository, so the number stays unverified -- it is not a
 pass, and it prints whether or not --verbose is set, so a green CI run is
 never mistaken for a verified number.
 """
 passed = True
 skipped = 0
 for tag, (file, regex) in PUBLISHED.items():
  path = ROOT / file
  text = path.read_text(encoding="utf-8")
  m = re.search(regex, text)
  if not m:
   skipped += 1
   print(f"SKIP: {tag}: no pattern in {file} to compare against. Number unverified.")
   continue
  published = int(m.group(1))
  # Compute from raw files
  if "reply" in tag:
   raw_dir = EVALS / "results" / "raw"
   stats = compute_reply_stats(raw_dir)
   if stats is None:
    skipped += 1
    print(f"SKIP: {tag}: no raw files in {raw_dir}. Number unverified.")
    continue
   computed = stats["total_defects"]
   if published != computed:
    print(f"FAIL: {tag}: published={published}, computed={computed}")
    passed = False
   else:
    print(f"PASS: {tag}={computed}")
 if skipped:
  print(f"note: {skipped} published number(s) unverified; see the README benchmark section.")
 return passed


if __name__ == "__main__":
 verbose = "--verbose" in sys.argv
 ok = check(verbose=verbose)
 sys.exit(0 if ok else 1)
