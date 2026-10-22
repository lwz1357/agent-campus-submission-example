import copy
import json
import unittest
from pathlib import Path
from src.main import run

ROOT = Path(__file__).resolve().parents[1]

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.request = json.loads((ROOT / "examples/normal.input.json").read_text())

    def test_normal(self):
        result = run(self.request)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["mode"], "offline_mock")
        self.assertEqual(result["shots"][0]["source_id"], result["evidence"][0]["source_id"])
        self.assertEqual(result["estimated_duration_seconds"], 30)

    def test_missing(self):
        del self.request["platform"]
        self.assertEqual(run(self.request)["missing"], ["platform"])

    def test_no_evidence(self):
        self.request["product_id"] = "unknown"
        result = run(self.request)
        self.assertEqual(result["status"], "insufficient_evidence")
        self.assertEqual(result["shots"], [])

    def test_tool_failure(self):
        self.request["simulate_tool_failure"] = True
        self.assertEqual(run(self.request)["status"], "tool_error")

    def test_duration_validation(self):
        for value in [0, -1, 121, True, "30"]:
            with self.subTest(value=value):
                self.request["duration_seconds"] = value
                with self.assertRaises(ValueError): run(self.request)

    def test_invalid_object(self):
        with self.assertRaises(ValueError): run([])

    def test_invalid_field(self):
        self.request["topic"] = ["bad"]
        with self.assertRaises(ValueError): run(self.request)

    def test_does_not_mutate_input(self):
        previous = copy.deepcopy(self.request)
        run(self.request)
        self.assertEqual(self.request, previous)

if __name__ == "__main__":
    unittest.main()
