"""Small transparent evaluation harness for AMR-Jev v0."""

import argparse
import json
import os
from pathlib import Path

from amr_jev import FALSE_AT, SIGNALS, TRUE_AT, reduce_orient_answers
from typesafe_adapter import route_orient

DEFAULT_CASES = Path("evaluation/cases.json")
ROUTE_KEYS = (
    "status",
    "base_preset",
    "preset",
    "topology",
    "external_evidence_needed",
)


def load_cases(path=DEFAULT_CASES):
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        raise ValueError("Evaluation corpus must be a JSON array")
    return cases


def classify_probability(value):
    if value >= TRUE_AT:
        return "true"
    if value <= FALSE_AT:
        return "false"
    return "ambiguous"


def _answers_from_labels(labels):
    values = {"true": 1.0, "false": 0.0, "ambiguous": 0.5}
    try:
        return {name: {"noul": values[labels[name]]} for name in SIGNALS}
    except KeyError as exc:
        raise ValueError(f"Invalid or missing signal label: {exc.args[0]}") from exc


def _route_matches(result, expected):
    return all(result.get(key) == expected.get(key) for key in ROUTE_KEYS)


def evaluate_offline(cases):
    failures = []
    route_correct = 0
    escalation_expected = 0
    escalation_correct = 0

    for case in cases:
        result = reduce_orient_answers(_answers_from_labels(case["expected_signals"]))
        expected = case["expected_route"]
        matches = _route_matches(result, expected)
        route_correct += int(matches)

        if expected["status"] == "ESCALATE":
            escalation_expected += 1
            escalation_correct += int(result["status"] == "ESCALATE")

        if not matches:
            failures.append(
                {"id": case["id"], "expected": expected, "actual": {k: result[k] for k in ROUTE_KEYS}}
            )

    total = len(cases)
    return {
        "mode": "offline-oracle",
        "cases": total,
        "route_correct": route_correct,
        "route_accuracy": route_correct / total if total else 0.0,
        "escalation_expected": escalation_expected,
        "escalation_correct": escalation_correct,
        "failures": failures,
    }


def evaluate_live(cases, api_key, model="jev-latest"):
    details = []
    signal_total = 0
    signal_correct = 0
    ambiguity_target_total = 0
    ambiguity_target_correct = 0
    route_correct = 0
    escalation_expected = 0
    escalation_correct = 0
    escalation_false_positive = 0
    provider_errors = 0

    for case in cases:
        expected_route = case["expected_route"]
        if expected_route["status"] == "ESCALATE":
            escalation_expected += 1

        try:
            result = route_orient(case["state"], api_key, model=model)
        except (RuntimeError, ValueError) as exc:
            provider_errors += 1
            details.append({"id": case["id"], "error": str(exc)})
            continue

        signal_results = {}
        for name in SIGNALS:
            expected = case["expected_signals"][name]
            actual = classify_probability(result["signal_probabilities"][name])
            correct = actual == expected
            if expected == "ambiguous":
                ambiguity_target_total += 1
                ambiguity_target_correct += int(correct)
            else:
                signal_total += 1
                signal_correct += int(correct)
            signal_results[name] = {
                "expected": expected,
                "actual": actual,
                "probability": result["signal_probabilities"][name],
                "correct": correct,
            }

        route_match = _route_matches(result, expected_route)
        route_correct += int(route_match)

        if expected_route["status"] == "ESCALATE":
            escalation_correct += int(result["status"] == "ESCALATE")
        elif result["status"] == "ESCALATE":
            escalation_false_positive += 1

        details.append(
            {
                "id": case["id"],
                "route_correct": route_match,
                "expected_route": expected_route,
                "actual_route": {key: result[key] for key in ROUTE_KEYS},
                "signals": signal_results,
            }
        )

    total = len(cases)
    completed = total - provider_errors
    return {
        "mode": "live",
        "model": model,
        "cases": total,
        "completed_cases": completed,
        "provider_errors": provider_errors,
        "signal_total": signal_total,
        "signal_correct": signal_correct,
        "signal_accuracy": signal_correct / signal_total if signal_total else 0.0,
        "ambiguity_target_total": ambiguity_target_total,
        "ambiguity_target_correct": ambiguity_target_correct,
        "ambiguity_target_accuracy": (
            ambiguity_target_correct / ambiguity_target_total if ambiguity_target_total else 0.0
        ),
        "route_correct": route_correct,
        "route_accuracy": route_correct / completed if completed else 0.0,
        "escalation_expected": escalation_expected,
        "escalation_correct": escalation_correct,
        "escalation_false_positive": escalation_false_positive,
        "details": details,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate AMR-Jev v0 routing.")
    parser.add_argument("--live", action="store_true", help="Call TypeSafe instead of using labeled oracle signals.")
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--model", default="jev-latest")
    args = parser.parse_args()

    cases = load_cases(args.cases)
    if args.live:
        api_key = os.environ.get("TYPESAFE_API_KEY", "")
        if not api_key:
            raise SystemExit("TYPESAFE_API_KEY is required for --live")
        report = evaluate_live(cases, api_key, model=args.model)
    else:
        report = evaluate_offline(cases)

    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
