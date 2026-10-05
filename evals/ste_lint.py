#!/usr/bin/env python3
"""Run the STE linter as a self-test.

The linter is a regex pass. It is not a full parser. This test verifies
the core regexes work on known inputs.

This module also provides the mechanical linter itself, so that the
self-test and the linter cannot drift apart. Word choice is out of scope
here; the Issue 9 word lists live in tools/ste-dictionary.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evals"))

# Sentence word limits. ASD-STE100 rule 1.2 sets 20 words for procedural
# text and 25 words for descriptive text.
SENTENCE_LIMITS = {"procedural": 20, "descriptive": 25}

# The flags the published reply counts group under. The reply profile is
# descriptive, so it uses the 25-word limit.
REPLY_PROFILE = "descriptive"

# Each rule is (category, compiled pattern). The categories are the names
# the self-test and the evals use.
RULES = [
 # A possessive is not a contraction: "the server's config" is correct
 # English. The clitic forms are limited to the words that actually take
 # them, so a possessive ending in 's is not reported. "it's" and "don't"
 # are contractions; "server's" and "O'Donnell" are not.
 ("contraction", re.compile(
    r"\b(?:it|that|there|here|what|who|he|she|we|you|i|they)[’']"
    r"(?:s|t|re|ve|ll|d|m)\b"
    r"|\b(?:do|does|did|is|are|was|were|has|have|had|can|could|will|would|"
    r"should|must|need)[’'](?:n[’']t|t)\b", re.I)),
 ("present_perfect", re.compile(
    r"\b(?:has|have|had)\s+(?:been\s+)?(?:\w+ed|installed|completed|"
    r"configured|created|made|done|written|set|run)\b", re.I)),
 ("dangling_ing", re.compile(r",\s+\w+ing\b", re.I)),
 ("semicolon", re.compile(r";")),
 ("em_dash", re.compile(r"\u2014")),
 ("modal_should", re.compile(r"\byou\s+should\b", re.I)),
 ("modal_may", re.compile(r"\bwe\s+may\b", re.I)),
]

SLOP_TSV = ROOT / "evals" / "slop.tsv"

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")


def _slop_tables():
 """Read evals/slop.tsv into (single words, phrases).

 The TSV is the committed vocabulary. One entry per line, an optional
 "(...)" note giving the sense to use the word in, and a few entries are
 multi-word phrases. An entry with more than one word is a phrase, because
 _WORD cannot match a multi-word entry anyway. This module measures
 mechanical rules only; the per-word ASD not-approved counts are out of
 scope and live in tools/ste-dictionary.
 """
 words, phrases = set(), []
 try:
  raw = SLOP_TSV.read_text(encoding="utf-8")
 except OSError:
  return words, phrases
 for line in raw.splitlines():
  entry = line.split("#", 1)[0].strip()
  if not entry:
   continue
  # Drop the annotation, e.g. "simplify (as marketing)" -> "simplify".
  note = entry.find("(")
  if note != -1:
   entry = entry[:note].strip()
  if not entry:
   continue
  if len(_WORD.findall(entry)) > 1:
   phrases.append(entry)
  else:
   words.add(entry.lower())
 return words, phrases


SLOP_WORDS, SLOP_PHRASES = _slop_tables()


def strip_code(text):
 """Remove code, URLs, and heading lines. The rules do not govern them."""
 text = re.sub(r"```.*?```", " ", text, flags=re.S)
 text = re.sub(r"`[^`\n]+`", " ", text)
 text = re.sub(r"https?://\S+", " ", text)
 text = re.sub(r"^#+\s.*$", " ", text, flags=re.M)
 return text


def sentences(text):
 """Split text into sentences."""
 body = strip_code(text).strip()
 if not body:
  return []
 return [s.strip() for s in _SENTENCE_SPLIT.split(body) if s.strip()]


def sentences_over_limit(text, profile=REPLY_PROFILE):
 """Count the sentences that exceed the word limit for the profile."""
 limit = SENTENCE_LIMITS.get(profile, SENTENCE_LIMITS[REPLY_PROFILE])
 return sum(1 for s in sentences(text) if len(_WORD.findall(s)) > limit)


def lint(text, profile=REPLY_PROFILE):
 """Return the mechanical STE violations in the text.

 The report has the shape the evals and the self-test expect:
 {"violations": {"all": [{"category": ..., "text": ...}]},
  "sentences_over_limit": int}
 """
 body = strip_code(text)
 hits = []
 for category, pattern in RULES:
  for match in pattern.finditer(body):
   hits.append({"category": category, "text": match.group(0).strip()})
 for word in _WORD.findall(body):
  if word.lower() in SLOP_WORDS:
   hits.append({"category": "slop_word", "text": word})
 for phrase in SLOP_PHRASES:
  pattern = re.compile(r"\b" + r"\s+".join(re.escape(w) for w in phrase.split()) + r"\b", re.I)
  for match in pattern.finditer(body):
   hits.append({"category": "slop_phrase", "text": match.group(0)})
 by_category = {}
 for hit in hits:
  by_category.setdefault(hit["category"], []).append(hit)
 return {
  "violations": {"all": hits, **by_category},
  "sentences_over_limit": sentences_over_limit(text, profile),
  "profile": profile,
 }


def test_mechanical_rules():
 """Test that the linter catches the mechanical STE violations."""
 cases = [
 ("The system has completed the installation.", "present_perfect"),
 ("Do not run this command, making sure that files are saved.", "dangling_ing"),
 ("If the flag is set; the system fails.", "semicolon"),
 ("Make sure that the config is correct — or the system fails.", "em_dash"),
 ("You should check the logs.", "modal_should"),
 ("We may need to restart.", "modal_may"),
 ("This is crucial for your success.", "slop_word"),
 ("It's been installed.", "contraction"),
 ]
 for text, expected_category in cases:
  result = lint(text, "descriptive")
  violations = result.get("violations", {})
  found = any(expected_category in v.get("category", "") for v in violations.get("all", []))
  if not found:
   print(f"FAIL: expected {expected_category} in: {text}")
   print(f" violations: {violations}")
   return False
 return True

def test_no_false_positives():
 """Valid text must not be flagged.

 A linter that flags correct text trains the writer to ignore it, so the
 rules have to stay quiet on clean sentences. Each case is text a reviewer
 would accept.
 """
 cases = [
 "Check the logs.",
 "Run the test suite before you commit.",
 "The server sends one request per second.",
 "It sends the request to the host.",
 "The files are in the docs directory.",
 "Set the flag in the config file.",
 "This is a test of the parser and the tokenizer.",
 "Use the tool, then read the output.",
 ]
 for text in cases:
  result = lint(text, "descriptive")
  hits = result.get("violations", {}).get("all", [])
  if hits:
   print(f"FAIL: false positive in: {text}")
   print(f" violations: {hits}")
   return False
  if result.get("sentences_over_limit", 0):
   print(f"FAIL: short text reported as over-limit: {text}")
   return False
 return True

def test_sentence_length():
 """Test sentence length counting against the profile limits."""
 # Each case states the real word count of the sentence. The counts are
 # written as LITERALS and compared against the module limits, not derived
 # from them: a test that computes its expectation from the same constant it
 # is checking passes when the constant is wrong. These cases pin all four
 # boundaries: 20/21 for procedural and 25/26 for descriptive.
 def words(n):
  return " ".join("w%d" % i for i in range(n)) + "."
 cases = [
 # (text, word count, over procedural?, over descriptive?)
 (words(1), 1, False, False),
 (words(20), 20, False, False),
 (words(21), 21, True, False),
 (words(25), 25, True, False),
 (words(26), 26, True, True),
 ]
 for text, word_count, over_proc, over_desc in cases:
  measured = len(_WORD.findall(text))
  if measured != word_count:
   print(f"FAIL: expected {word_count} words, measured {measured}")
   return False
  if SENTENCE_LIMITS["procedural"] != 20:
   print(f"FAIL: procedural limit is {SENTENCE_LIMITS['procedural']}, expected 20")
   return False
  if SENTENCE_LIMITS["descriptive"] != 25:
   print(f"FAIL: descriptive limit is {SENTENCE_LIMITS['descriptive']}, expected 25")
   return False
  for profile, expect_over in (("procedural", over_proc),
                               ("descriptive", over_desc)):
   over = sentences_over_limit(text, profile)
   if expect_over and not over:
    print(f"FAIL: {profile} expected over-limit at {word_count} words")
    return False
   if not expect_over and over:
    print(f"FAIL: {profile} expected within limit at {word_count} words")
    return False
 return True

def test_edge_cases():
 """Pin the rules whose behaviour a weaker test would not notice.

 Each case is (text, category that MUST appear, category that must NOT).
 The negative half matters most: a rule that matches too much is a false
 positive, and a suite that only checks for hits cannot see it.
 """
 cases = [
 # a multi-word slop phrase, and the single word that is not inside it
 ("We did it in order to finish.", "slop_phrase", None),
 # a hyphen is not an em-dash
 ("The value is set - one - then read it.", None, "em_dash"),
 # an em-dash is an em-dash
 ("The value is set \u2014 then read it.", "em_dash", None),
 # a possessive apostrophe is not a contraction
 ("It reads the server's config file.", None, "contraction"),
 ("O'Donnell wrote it.", None, "contraction"),
 # a plain sentence with "has" is not present perfect
 ("The server has five worker threads.", None, "present_perfect"),
 # code spans are not prose
 ("Run `you should; utilize` first.", None, "modal_should"),
 ("Set `crucial` in the config.", None, "slop_word"),
 # a fenced block is not prose either
 ("```\nyou should; utilize\n```", None, "modal_should"),
 ("Text before.\n\n```\nutilize\n```\n", None, "slop_word"),
 # a heading line is a heading, not prose to lint
 ("# you should utilize\n", None, "modal_should"),
 # a URL is not prose
 ("See https://example.com/you-should-utilize now.", None, "modal_should"),
 ]
 for text, want, unwanted in cases:
  hits = lint(text, "descriptive").get("violations", {}).get("all", [])
  categories = {h["category"] for h in hits}
  if want and want not in categories:
   print(f"FAIL: expected {want} in: {text}")
   print(f" got: {sorted(categories)}")
   return False
  if unwanted and unwanted in categories:
   print(f"FAIL: {unwanted} must not fire on: {text}")
   print(f" got: {sorted(categories)}")
   return False
 return True

def main():
 """Run all self-tests."""
 print("Running STE linter self-tests...")
 tests = [
 ("Mechanical rules", test_mechanical_rules),
 ("No false positives", test_no_false_positives),
 ("Edge cases", test_edge_cases),
 ("Sentence length", test_sentence_length),
 ]
 all_passed = True
 for name, fn in tests:
  print(f"\nTesting: {name}...")
  try:
   if fn():
    print(f" PASS: {name}")
   else:
    print(f" FAIL: {name}")
    all_passed = False
  except Exception as e:
   print(f" ERROR: {name}: {e}")
   all_passed = False
 if all_passed:
  print("\nAll self-tests passed.")
  return 0
 else:
  print("\nSome self-tests failed.")
  return 1

if __name__ == "__main__":
 # README.md documents `python3 evals/ste_lint.py --self-test` as the
 # pre-push check. Accept the flag and also run the tests with no argument,
 # so the documented command and a bare run behave the same.
 if "--self-test" not in sys.argv[1:] and len(sys.argv) > 1:
  print("usage: ste_lint.py [--self-test]")
  sys.exit(2)
 sys.exit(main())
