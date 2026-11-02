import json
import subprocess
import sys
import unittest
from pathlib import Path

from engine import evaluate


def example():
    return json.loads(Path(__file__).with_name("example.json").read_text(encoding="utf-8"))


class AcceptanceTests(unittest.TestCase):
    def test_example_cli(self):
        proc = subprocess.run([sys.executable, "cli.py", "example.json"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), evaluate(example()))

    def test_overlap_is_subtracted_once(self):
        result = evaluate(example())
        self.assertEqual(result["exclusive"]["request"], 6)
        self.assertEqual(result["largest_self_time"], "db")
        self.assertEqual(result["incomplete"], ["pending"])

    def test_unfinished_child_suppresses_parent_estimate(self):
        data = example()
        data["spans"][1]["end"] = None
        self.assertNotIn("request", evaluate(data)["exclusive"])

    def test_invalid_hierarchy(self):
        data = example()
        data["spans"][0]["parent"] = "db"
        with self.assertRaisesRegex(ValueError, "cycle"):
            evaluate(data)
