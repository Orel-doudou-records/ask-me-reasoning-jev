import json
import unittest
from urllib.error import URLError

import typesafe_adapter


SIGNALS = {
    "external_evidence_needed",
    "material_action_needed",
    "multiple_plausible_paths",
    "ordered_dependencies",
    "shared_cross_dependencies",
    "causal_reasoning_needed",
    "high_consequence",
}


def provider_result(**values):
    answers = {name: {"noul": 0.0} for name in SIGNALS}
    for name, value in values.items():
        answers[name] = {"noul": value}
    return {"model": "jev-test", "answers": answers, "usage": {}}


class FakeResponse:
    def __init__(self, payload, status=200):
        self.payload = json.dumps(payload).encode()
        self.status = status

    def read(self):
        return self.payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False


class TypeSafeAdapterTests(unittest.TestCase):
    def setUp(self):
        self.state = {
            "request": {
                "outcome": "Compare two approaches",
                "constraints": [],
                "supplied_context": "",
            },
            "capabilities": {"retrieval": True, "code": True, "tools": []},
        }

    def test_one_post_contains_shared_state_and_all_questions_without_key(self):
        calls = []

        def opener(request, timeout):
            calls.append((request, timeout))
            return FakeResponse(provider_result(multiple_plausible_paths=0.95))

        result = typesafe_adapter.route_orient(
            self.state,
            "secret-key",
            opener=opener,
            timeout=7,
        )

        self.assertEqual(len(calls), 1)
        request, timeout = calls[0]
        self.assertEqual(timeout, 7)
        self.assertEqual(request.full_url, typesafe_adapter.SYSTEM_ONE_URL)
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Authorization"), "Bearer secret-key")

        body = json.loads(request.data)
        self.assertEqual(body["state"], self.state)
        self.assertEqual(set(body["questions"]), SIGNALS)
        self.assertEqual(body["model"], "jev-latest")
        self.assertNotIn("secret-key", request.data.decode())

        self.assertEqual(result["status"], "ROUTED")
        self.assertEqual(result["base_preset"], "exploratory")
        self.assertEqual(result["topology"], "tree")

    def test_missing_key_stops_before_network(self):
        called = False

        def opener(_request, timeout):
            nonlocal called
            called = True
            raise AssertionError("network must not be called")

        with self.assertRaises(ValueError):
            typesafe_adapter.route_orient(self.state, "", opener=opener)

        self.assertFalse(called)

    def test_provider_failure_returns_no_route(self):
        def opener(_request, timeout):
            raise URLError("unavailable")

        with self.assertRaises(RuntimeError):
            typesafe_adapter.route_orient(self.state, "secret", opener=opener)

    def test_non_success_status_returns_no_route(self):
        def opener(_request, timeout):
            return FakeResponse({"error": "busy"}, status=503)

        with self.assertRaises(RuntimeError):
            typesafe_adapter.route_orient(self.state, "secret", opener=opener)

    def test_malformed_response_is_rejected_by_existing_contract(self):
        def opener(_request, timeout):
            return FakeResponse({"answers": {}})

        with self.assertRaises(ValueError):
            typesafe_adapter.route_orient(self.state, "secret", opener=opener)


if __name__ == "__main__":
    unittest.main()
