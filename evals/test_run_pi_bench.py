#!/usr/bin/env python3
"""Tests for run_pi_bench.py."""
import unittest
import sys
import pathlib

# Add parent to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

class TestRunPiBench(unittest.TestCase):
  """Test cases for PI benchmark runner."""

  def test_import(self):
   """Test that the module can be imported."""
   import evals.run_pi_bench
   self.assertTrue(hasattr(evals.run_pi_bench, 'main'))

if __name__ == "__main__":
 unittest.main()
