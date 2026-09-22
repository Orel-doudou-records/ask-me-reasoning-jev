import json
import unittest
from pathlib import Path

import evaluate


CASES = Path("evaluation/cases.json")


class EvaluationTests(unittest.TestCase):
    def test_offline_corpus_is_self_consistent(self):
        report = evaluate.evaluate_offline(evaluate.load_cases(CASES))
        self.assertEqual(report["cases"], report["route_correct"])
        self.assertEqual(report["route_accuracy"], 1.0)
        self.assertEqual(report["escalation_expected"], report["escalation_correct"])

    def test_corpus_covers_required_shapes(self):
        cases = evaluate.load_cases(CASES)
        base_presets = {case["expected_route"]["base_preset"] for case in cases}
        topologies = {case["expected_route"]["topology"] for case in cases}
        tags = {tag for case in cases for tag in case["tags"]}

        self.assertEqual(
            base_presets,
            {"direct", "grounded", "analytic", "exploratory", "causal", "agentic"},
        )
        self.assertEqual(topologies, {"linear", "chain", "tree", "graph"})
        self.assertIn("high-assurance", tags)
        self.assertIn("mixed", tags)
        self.assertIn("ambiguous", tags)
        self.assertIn("adversarial", tags)

    def test_signal_labels_use_only_supported_values(self):
        cases = evaluate.load_cases(CASES)
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(set(case["expected_signals"]), set(evaluate.SIGNALS))
                self.assertTrue(
                    set(case["expected_signals"].values())
                    <= {"true", "false", "ambiguous"}
                )


if __name__ == "__main__":
    unittest.main()
