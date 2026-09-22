"""Offline AMR-Jev ORIENT contract.

Jev supplies seven narrow semantic judgments. AMR policy stays deterministic here.
No network or Reasoning Route mutation lives in this module.
"""

from math import isfinite

TRUE_AT = 0.70
FALSE_AT = 0.30

QUESTION_SPECS = {
    "external_evidence_needed": (
        "Does satisfying `request.outcome` require factual information that is not already supplied "
        "in `request.supplied_context` and therefore needs external or retrieved evidence?",
        "Missing factual evidence is required.",
        "The supplied context is sufficient for factual support.",
    ),
    "material_action_needed": (
        "Does satisfying `request.outcome` require changing external state, rather than only returning "
        "information, analysis, a draft, or a plan?",
        "An external side effect is part of success.",
        "No external mutation is required.",
    ),
    "multiple_plausible_paths": (
        "Does solving `request.outcome` require comparing more than one materially different "
        "hypothesis, solution, or candidate before committing?",
        "Bounded branching is useful.",
        "One primary trajectory is sufficient.",
    ),
    "ordered_dependencies": (
        "Does solving `request.outcome` require multiple dependent reasoning steps where a later step "
        "materially depends on an earlier result?",
        "An ordered multi-step trajectory is required.",
        "No dependent chain is required.",
    ),
    "shared_cross_dependencies": (
        "Do multiple parts of `request.outcome` share dependencies or constraints whose interactions "
        "would be missed by treating the work as a simple sequence?",
        "Graph-like coupling is present.",
        "No material cross-coupling is required.",
    ),
    "causal_reasoning_needed": (
        "Does `request.outcome` require reasoning about a mechanism, intervention, or counterfactual "
        "rather than only description, lookup, transformation, or comparison?",
        "Causal or counterfactual reasoning is required.",
        "Causal or counterfactual reasoning is not required.",
    ),
    "high_consequence": (
        "Could a materially wrong answer or action for `request.outcome` reasonably cause significant "
        "safety, legal, financial, security, or irreversible harm?",
        "Stronger assurance is required.",
        "Normal assurance is sufficient unless another AMR rule escalates.",
    ),
}

SIGNALS = tuple(QUESTION_SPECS)


def build_orient_request(state, model="jev-latest"):
    """Build one TypeSafe request containing all independent ORIENT judgments."""
    questions = {}
    for name, (instruction, true_meaning, false_meaning) in QUESTION_SPECS.items():
        questions[name] = {
            "type": "noul",
            "instructions": instruction,
            "criteria": {
                "true": {"what": true_meaning},
                "false": {"what": false_meaning},
            },
        }
    return {"model": model, "state": state, "questions": questions}


def _validated_probabilities(answers):
    if not isinstance(answers, dict) or set(answers) != set(SIGNALS):
        raise ValueError("TypeSafe answers must contain exactly the seven ORIENT signals")

    probabilities = {}
    for name in SIGNALS:
        answer = answers[name]
        if not isinstance(answer, dict) or "noul" not in answer:
            raise ValueError(f"Missing Noul value for {name}")
        value = answer["noul"]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Invalid Noul value for {name}")
        value = float(value)
        if not isfinite(value) or not 0 <= value <= 1:
            raise ValueError(f"Invalid Noul value for {name}")
        probabilities[name] = value
    return probabilities


def _route(signals):
    if signals["material_action_needed"]:
        base_preset = "agentic"
    elif signals["causal_reasoning_needed"]:
        base_preset = "causal"
    elif signals["multiple_plausible_paths"]:
        base_preset = "exploratory"
    elif signals["ordered_dependencies"] or signals["shared_cross_dependencies"]:
        base_preset = "analytic"
    elif signals["external_evidence_needed"]:
        base_preset = "grounded"
    else:
        base_preset = "direct"

    if signals["causal_reasoning_needed"] or signals["shared_cross_dependencies"]:
        topology = "graph"
    elif signals["multiple_plausible_paths"]:
        topology = "tree"
    elif signals["ordered_dependencies"]:
        topology = "chain"
    else:
        topology = "linear"

    return {
        "base_preset": base_preset,
        "preset": "high-assurance" if signals["high_consequence"] else base_preset,
        "topology": topology,
        "external_evidence_needed": signals["external_evidence_needed"],
    }


def reduce_orient_answers(answers):
    """Validate Jev answers and reduce them through AMR's deterministic ORIENT policy."""
    probabilities = _validated_probabilities(answers)
    resolved = {}
    ambiguous = []

    for name, probability in probabilities.items():
        if probability >= TRUE_AT:
            resolved[name] = True
        elif probability <= FALSE_AT:
            resolved[name] = False
        else:
            resolved[name] = False
            ambiguous.append(name)

    baseline = _route(resolved)
    material_ambiguity = []
    for name in ambiguous:
        counterfactual = dict(resolved)
        counterfactual[name] = True
        if _route(counterfactual) != baseline:
            material_ambiguity.append(name)

    return {
        "status": "ESCALATE" if material_ambiguity else "ROUTED",
        **baseline,
        "signal_probabilities": probabilities,
        "ambiguous_signals": ambiguous,
    }
