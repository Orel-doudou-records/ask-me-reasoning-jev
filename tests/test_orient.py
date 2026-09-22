import math
import unittest

import amr_jev


SIGNALS = {
    "external_evidence_needed",
    "material_action_needed",
    "multiple_plausible_paths",
    "ordered_dependencies",
    "shared_cross_dependencies",
    "causal_reasoning_needed",
    "high_consequence",
}


def answers(**values):
    base = {name: {"noul": 0.0} for name in SIGNALS}
    for name, value in values.items():
        base[name] = {"noul": value}
    return base


class OrientContractTests(unittest.TestCase):
    def test_builds_all_atomic_noul_questions_in_one_request(self):
        state = {
            "request": {"outcome": "Compare two approaches", "constraints": [], "supplied_context": ""},
            "capabilities": {"retrieval": True, "code": True, "tools": []},
        }
        request = amr_jev.build_orient_request(state)
        self.assertEqual(set(request["questions"]), SIGNALS)
        self.assertIs(request["state"], state)
        self.assertTrue(all(q["type"] == "noul" for q in request["questions"].values()))
        self.assertNotIn("preset", " ".join(str(q).lower() for q in request["questions"].values()))

    def test_reducer_uses_task_shape_priority_and_keeps_external_grounding(self):
        result = amr_jev.reduce_orient_answers(
            answers(
                external_evidence_needed=0.95,
                ordered_dependencies=0.95,
                multiple_plausible_paths=0.95,
                causal_reasoning_needed=0.95,
                material_action_needed=0.95,
            )
        )
        self.assertEqual(result["status"], "ROUTED")
        self.assertEqual(result["base_preset"], "agentic")
        self.assertEqual(result["preset"], "agentic")
        self.assertEqual(result["topology"], "graph")
        self.assertTrue(result["external_evidence_needed"])

    def test_topology_rules(self):
        cases = [
            ({"shared_cross_dependencies": 0.95}, "graph"),
            ({"multiple_plausible_paths": 0.95}, "tree"),
            ({"ordered_dependencies": 0.95}, "chain"),
            ({}, "linear"),
        ]
        for values, expected in cases:
            with self.subTest(values=values):
                self.assertEqual(amr_jev.reduce_orient_answers(answers(**values))["topology"], expected)

    def test_high_assurance_preserves_base_preset(self):
        result = amr_jev.reduce_orient_answers(
            answers(material_action_needed=0.95, high_consequence=0.95)
        )
        self.assertEqual(result["base_preset"], "agentic")
        self.assertEqual(result["preset"], "high-assurance")

    def test_material_ambiguity_escalates(self):
        result = amr_jev.reduce_orient_answers(answers(material_action_needed=0.50))
        self.assertEqual(result["status"], "ESCALATE")
        self.assertIn("material_action_needed", result["ambiguous_signals"])

    def test_irrelevant_ambiguity_does_not_escalate(self):
        result = amr_jev.reduce_orient_answers(
            answers(causal_reasoning_needed=0.95, ordered_dependencies=0.50)
        )
        self.assertEqual(result["status"], "ROUTED")
        self.assertEqual(result["base_preset"], "causal")
        self.assertEqual(result["topology"], "graph")
        self.assertIn("ordered_dependencies", result["ambiguous_signals"])

    def test_rejects_malformed_answers(self):
        bad = answers()
        bad.pop("high_consequence")
        with self.assertRaises(ValueError):
            amr_jev.reduce_orient_answers(bad)

        for value in (-0.1, 1.1, math.nan, True, "0.8"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    amr_jev.reduce_orient_answers(answers(high_consequence=value))

        bad = answers()
        bad["unknown_signal"] = {"noul": 0.2}
        with self.assertRaises(ValueError):
            amr_jev.reduce_orient_answers(bad)


if __name__ == "__main__":
    unittest.main()
