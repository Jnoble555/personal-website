"""Checks the edge cases represented by the synthetic example."""

import datetime as dt
import unittest
from pathlib import Path

from sample import read_runs, summarize


EXAMPLES = Path(__file__).parent / "examples"


class PipelineExampleTest(unittest.TestCase):
    def test_duplicate_metric_columns_and_race_exclusion(self):
        result = summarize(
            read_runs(EXAMPLES / "activities.csv"),
            dt.date(2025, 11, 22),
            EXAMPLES / "plan.csv",
        )
        self.assertEqual(result["training_runs"], 4)
        self.assertEqual(result["training_miles"], 29.0)
        self.assertEqual(result["race_miles"], 50.0)
        self.assertIn({"week": "2025-10-06", "miles": 0.0}, result["weekly_training"])

    def test_overnight_run_is_flagged_for_review(self):
        result = summarize(
            read_runs(EXAMPLES / "activities.csv"),
            dt.date(2025, 11, 22),
            EXAMPLES / "plan.csv",
        )
        self.assertEqual(result["possible_overnight_plan_matches"], ["2025-10-02"])


if __name__ == "__main__":
    unittest.main()
