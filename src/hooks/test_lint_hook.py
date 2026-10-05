#!/usr/bin/env python3
"""Test the lint hook functionality."""
import sys
import json
from pathlib import Path

# Add repo root to sys.path so `import src.hooks.lint_hook` works.
# When running `python file.py`, Python puts the script's directory as sys.path[0],
# which takes priority. We need the repo root (three levels up) ahead of it.
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_hook_imports():
 """Test that lint_hook can be imported."""
 import src.hooks.lint_hook
 assert hasattr(src.hooks.lint_hook, 'load_linter')
 assert hasattr(src.hooks.lint_hook, 'strip_code')
 assert hasattr(src.hooks.lint_hook, 'post_tool_use')
 assert hasattr(src.hooks.lint_hook, 'stop')
 return True

def test_strip_code():
 """Test code stripping functionality."""
 from src.hooks.lint_hook import strip_code
 text = "Some text with `code` and ```code block``` inside."
 result = strip_code(text)
 assert "`code`" not in result
 assert "code block" not in result
 return True

def test_load_linter():
 """Test linter loading."""
 from src.hooks.lint_hook import load_linter
 # Should return None or ste_lint module
 result = load_linter()
 # Result is either None or a module
 assert result is None or hasattr(result, 'lint')
 return True

def main():
 print("Running lint hook tests...")
 tests = [
 ("Import", test_hook_imports),
 ("Strip code", test_strip_code),
 ("Load linter", test_load_linter),
 ]
 passed = 0
 failed = 0
 for name, fn in tests:
  try:
   if fn():
    print(f" PASS: {name}")
    passed += 1
   else:
    print(f" FAIL: {name}")
    failed += 1
  except Exception as e:
   print(f" ERROR: {name}: {e}")
   failed += 1
 print(f"\nResults: {passed} passed, {failed} failed")
 return 0 if failed == 0 else 1

if __name__ == "__main__":
 sys.exit(main())
