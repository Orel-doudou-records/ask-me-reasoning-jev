import unittest
from pathlib import Path
from unittest.mock import patch

import evaluate
from amr_jev import reduce_orient_answers


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

    def test_live_report_separates_boolean_signals_ambiguity_routes_and_escalation(self):
        cases = evaluate.load_cases(CASES)
        direct = next(case for case in cases if case["id"] == "direct_rewrite")
        ambiguous = next(case for case in cases if case["id"] == "ambiguous_material_action")

        direct_answers = {name: {"noul": 0.0} for name in evaluate.SIGNALS}
        ambiguous_answers = {name: {"noul": 0.0} for name in evaluate.SIGNALS}
        ambiguous_answers["material_action_needed"] = {"noul": 0.5}

        with patch(
            "evaluate.route_orient",
            side_effect=[
                reduce_orient_answers(direct_answers),
                reduce_orient_answers(ambiguous_answers),
            ],
        ):
            report = evaluate.evaluate_live([direct, ambiguous], "fake-key")

        self.assertEqual(report["completed_cases"], 2)
        self.assertEqual(report["signal_total"], 13)
        self.assertEqual(report["signal_correct"], 13)
        self.assertEqual(report["ambiguity_target_total"], 1)
        self.assertEqual(report["ambiguity_target_correct"], 1)
        self.assertEqual(report["route_correct"], 2)
        self.assertEqual(report["escalation_expected"], 1)
        self.assertEqual(report["escalation_correct"], 1)


if __name__ == "__main__":
    unittest.main()
