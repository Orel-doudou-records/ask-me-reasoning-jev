# Internal module contracts

These modules are roles within the single `ask-me-reasoning` skill. They are not separate skills or tools. The router authorizes one module and one cognitive state at a time, validates the returned typed artifact, updates the route, and then selects the next state.

## Advance

Use for one authorized `ACQUIRE`, `REASON`, `PLAN`, `DECIDE`, or `EXECUTE` step. Apply the active profile without changing it or choosing the next module.

```yaml
frame_delta:
  route_id: <id>
  profile_version: <integer>
  state: <authorized-state>
  inputs_used: [<refs>]
  outputs: <typed payload>
  evidence_refs: [<refs>]
  assumptions: [<explicit assumptions>]
  uncertainty: low|medium|high
  budget_used: {branches: 0, depth: 0, tool_rounds: 0}
  requested_transition: <state or DONE>
```

State requirements:

- `ACQUIRE`: information need, real grounding, provenance, missing evidence, uncertainty delta.
- `REASON`: candidates or derivations, concise rationale, assumptions, uncertainty; no hidden thought trace.
- `PLAN`: executable steps or DAG, dependencies, preconditions, observations, and failure conditions.
- `DECIDE`: selected option, criteria/evidence references, and rejected risks.
- `EXECUTE`: one authorized action request and its actual observation, or a pending status.

The requested transition is advisory; the router applies it.

## Verify

Use in `EVALUATE`. Judge the target without repairing it. Prefer the strongest applicable oracle: runtime/test/schema/solver, authoritative source, constraint check, then semantic critic. A semantic critic can judge coherence but cannot create factual support.

Check only relevant dimensions: profile fit, evidence coverage, correctness, constraints, action state, and residual uncertainty.

```yaml
verification_verdict:
  route_id: <id>
  profile_version: <integer>
  target_ref: <ref>
  criteria_checked: [<criteria>]
  oracle: <runtime|test|schema|source|constraint|semantic|human>
  verdict: pass|fail|uncertain|blocked
  evidence_refs: [<refs>]
  defects: [<localized defects>]
  residual_uncertainty: low|medium|high
  recommended_transition: DECIDE|ACQUIRE|ADAPT|DONE
```

Do not rewrite the target, patch the profile, turn preference into correctness, or claim verification from memory when grounding was required.

## Adapt

Use only after a verifier verdict, observed execution failure, profile drift, or budget exhaustion. Diagnose one primary failure locus and propose the smallest bounded change; the router alone applies it.

Failure loci: `observation`, `orientation`, `acquisition`, `reasoning`, `planning`, `decision`, `execution`, `verification`, `profile`, or `budget`.

Prefer, in order: narrower evidence acquisition; corrected framing/domain; inference-mode repair; topology widening only when branching or coupling is evidenced; deterministic oracle for calculation; safe/idempotent action retry; rollback on drift; declared best-effort, escalation, or fail-closed on exhaustion.

```yaml
adaptation_proposal:
  route_id: <id>
  from_profile_version: <integer>
  failure_locus: <enum>
  evidence_refs: [<refs>]
  rollback_to: <checkpoint-ref>
  profile_patch: <minimal diff>
  requested_state: <state>
  added_budget: <bounded diff>
  risk_if_wrong: <text>
  stop_if_failed: <best_effort|escalate|fail_closed>
```

Do not retry irreversible actions or repeat adaptation beyond the route budget.

## Consolidate

Use only when a completed episode has a reusable, supported routing/verification/recovery lesson and memory is permitted. Produce a candidate, never an automatic memory write. If novelty, generality, evidence, privacy, or retention requirements fail, return `no_consolidation`.

```yaml
memory_candidate:
  lesson: <one operational statement>
  applies_when: <signals>
  do_not_apply_when: <boundaries>
  source_refs: [<episode evidence>]
  confidence: low|medium|high
  privacy: public|internal|private
  review_at: <date or condition>
  revocation_key: <stable id>
```

Store neither private chain-of-thought, secrets, personal data, nor full transcripts. Do not generalize one failure without a narrow scope.
