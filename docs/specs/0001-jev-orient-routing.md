# Spec 0001 — Jev-assisted ORIENT routing

Status: **Ready for ticketing**  
Parent: #1

## Problem

Ask Me Reasoning already has a bounded routing policy, a cognitive state machine, compact-model constraints, verification, and adaptation. Compact models can still fail before those controls help because they must semantically classify a request while also deciding how to reason about it.

The smallest useful Jev integration is therefore at `ORIENT`: move narrow semantic routing judgments out of the compact generative model, while keeping AMR policy and execution authority unchanged.

## Goal

Given a normalized AMR request, obtain a small set of atomic Jev judgments and deterministically apply the existing AMR selection policy.

A successful v0 makes compact-model routing more stable without creating a second route model or a new reasoning runtime.

## Authority boundary

AMR remains authoritative for:

- the Reasoning Route;
- preset/profile policy;
- state-machine legality;
- capabilities and permissions;
- budgets and stop behavior;
- verification and acceptance;
- tool execution and side effects.

Jev is authoritative for nothing beyond the returned bounded semantic judgments.

The reducer may consume Jev results. Jev may not directly mutate a Reasoning Route.

## Existing AMR concepts reused

v0 reuses the current AMR concepts rather than introducing equivalents:

- `Reasoning Route`
- `selection-policy.md`
- `model-capability-policy.md`
- `state-machine.md`
- `frame_delta`
- `verification_verdict`
- `adaptation_proposal`

No new persistent `TaskSnapshot`, `Affordance`, `DecisionPacket`, `BoundedDecision`, or `ObservationReceipt` type is introduced.

## Input seam

The Jev call receives a minimal projection of already-normalized AMR state:

```yaml
request:
  outcome: <normalized requested outcome>
  constraints: [<material constraints only>]
  supplied_context: <only context needed for routing judgments>
capabilities:
  retrieval: true|false
  code: true|false
  tools: [<available tool classes>]
```

Known capability values are code-owned state. Jev must not infer whether a tool or permission exists.

Do not send the full conversation or full route history by default.

## Jev judgments

v0 asks independent questions over the same state in one TypeSafe request.

All seven are `Noul` judgments because the conditions may co-exist.

### `external_evidence_needed`

Instruction:

> Does satisfying `request.outcome` require factual information that is not already supplied in `request.supplied_context` and therefore needs external or retrieved evidence?

True means missing factual evidence is required.  
False means the supplied context is sufficient for factual support.

### `material_action_needed`

Instruction:

> Does satisfying `request.outcome` require changing external state, rather than only returning information, analysis, a draft, or a plan?

True means an external side effect is part of success.  
False means no external mutation is required.

### `multiple_plausible_paths`

Instruction:

> Does solving `request.outcome` require comparing more than one materially different hypothesis, solution, or candidate before committing?

True means bounded branching is useful.  
False means one primary trajectory is sufficient.

### `ordered_dependencies`

Instruction:

> Does solving `request.outcome` require multiple dependent reasoning steps where a later step materially depends on an earlier result?

True means an ordered multi-step trajectory is required.  
False means no dependent chain is required.

### `shared_cross_dependencies`

Instruction:

> Do multiple parts of `request.outcome` share dependencies or constraints whose interactions would be missed by treating the work as a simple sequence?

True means graph-like coupling is present.  
False means no material cross-coupling is required.

### `causal_reasoning_needed`

Instruction:

> Does `request.outcome` require reasoning about a mechanism, intervention, or counterfactual rather than only description, lookup, transformation, or comparison?

True means causal/counterfactual reasoning is required.  
False means it is not.

### `high_consequence`

Instruction:

> Could a materially wrong answer or action for `request.outcome` reasonably cause significant safety, legal, financial, security, or irreversible harm?

True means the AMR high-assurance wrapper is required.  
False means normal assurance is sufficient unless another AMR rule escalates.

## Ambiguity

Do not add a separate `material_ambiguity` question.

Jev already returns a Noul probability. v0 treats the probability distribution as the ambiguity signal.

Initial prototype bands are deliberately conservative and must be evaluated on labeled cases before being treated as calibrated:

- `p >= 0.70`: true
- `p <= 0.30`: false
- otherwise: ambiguous

If an ambiguous judgment could change the selected preset, topology, grounding requirement, or assurance level, v0 returns `ESCALATE` instead of guessing.

The thresholds are implementation constants for the prototype, not user configuration and not universal TypeSafe recommendations.

## Deterministic reduction

The reducer applies AMR policy; it does not ask Jev to choose a preset.

### Base preset

Use the strongest task-shape requirement:

1. `material_action_needed` -> `agentic`
2. `causal_reasoning_needed` -> `causal`
3. `multiple_plausible_paths` -> `exploratory`
4. `ordered_dependencies || shared_cross_dependencies` -> `analytic`
5. `external_evidence_needed` -> `grounded`
6. otherwise -> `direct`

External evidence remains orthogonal: when `external_evidence_needed` is true, the resulting profile must include retrieval/source grounding even if the base preset is `agentic`, `causal`, `exploratory`, or `analytic`.

### Topology

- `causal_reasoning_needed || shared_cross_dependencies` -> `graph`
- else `multiple_plausible_paths` -> `tree`
- else `ordered_dependencies` -> `chain`
- else -> `linear`

### Assurance

If `high_consequence` is true, apply the existing AMR `high-assurance` wrapper semantics around the minimal adequate route. v0 does not add a new Reasoning Route field to represent the wrapped base preset.

### Deterministic oracle rule

A known runtime, test, schema, solver, or calculation requirement remains code-owned. It is not a Jev question and it does not become weaker because Jev selected a semantic route.

## Output seam

The v0 reducer returns an ephemeral orientation result:

```yaml
status: ROUTED|ESCALATE
preset: direct|grounded|analytic|exploratory|causal|agentic|high-assurance
topology: linear|chain|tree|graph
external_evidence_needed: true|false
signal_probabilities:
  <signal>: <0..1>
ambiguous_signals: [<signal>]
```

This is an adapter result, not a replacement for the Reasoning Route schema.

The AMR router applies it to the existing profile representation.

## Failure behavior

- Missing or malformed TypeSafe answer -> no route mutation; escalate/fallback.
- Missing API credential -> no guessed semantic classification.
- Ambiguous material signal -> `ESCALATE`.
- TypeSafe service failure -> no partial route mutation.
- Unsupported/unknown returned field -> reject the response.
- Existing deterministic policy conflict -> deterministic AMR policy wins.

## Non-goals

v0 does **not** implement:

- Jev selection of the next cognitive state after `ORIENT`;
- speculative operation-specific target heads;
- Jev-selected tools or side effects;
- a new Reasoning Route schema;
- a new persistent decision object;
- dynamic recursion;
- multi-agent routing;
- verification replacement;
- acceptance replacement;
- a generalized policy framework.

Those remain deferred until evaluation proves a concrete need.

## Acceptance proofs

The first implementation brick is complete only when runnable checks prove:

1. all seven Jev questions are generated in one request over one shared state;
2. no question asks Jev to choose an AMR preset directly;
3. the reducer follows the deterministic priority above;
4. external evidence remains active when another preset wins;
5. graph/tree/chain/linear topology follows the stated rules;
6. a material ambiguous signal returns `ESCALATE`;
7. malformed Jev output cannot mutate a route;
8. no network call is required for unit tests.

A later live smoke test may call TypeSafe, but CI must remain deterministic and offline.

## Dependency order

```text
contract tests
    ->
pure question builder + response validator + reducer
    ->
TypeSafe HTTP adapter
    ->
labeled routing evaluation
    ->
decision: stop at v0 OR justify a v1
```

No v1 dynamic routing ticket may start before the labeled evaluation.

## Ask Matt review

**KEEP**

The spec has one explicit seam: Jev semantic judgments at `ORIENT`. Inputs, outputs, authority boundaries, failure behavior, acceptance proofs, and dependency order are explicit. The existing AMR route model remains canonical.

The implementation must be ticketed as vertical observable slices, not as infrastructure layers.

## Ponytail challenge

**KEEP, reduced**

Cuts applied before implementation:

- deleted the proposed duplicate `material_ambiguity` judgment;
- deleted new persistent routing types;
- deleted an `AffordanceCompiler` class in favor of a small function;
- deferred dynamic next-state routing and speculative target heads;
- avoided a threshold configuration system; prototype thresholds are constants until labeled evaluation proves otherwise.

Upgrade only when a failing evaluation demonstrates the need.
