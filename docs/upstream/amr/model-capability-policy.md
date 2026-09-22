# Model Capability Policy

Route by observed capabilities and harness affordances, not provider names.

| Dimension | Compact policy | Extended policy |
|---|---|---|
| Profile representation | Closed enums, one primary mode, one topology | Mixed modes and richer topology when justified |
| Context | Minimal frame + evidence refs; no full history | Larger working context with checkpoints/compaction |
| Decomposition | ≤3 explicit subproblems by default | Adaptive DAG/recursive decomposition with cap |
| Search | Beam 2, depth 2, ≤4 candidates | Wider beam only when verifier value exceeds cost |
| Tools | One action/request at a time, strict schema | Multiple tools/task graph if harness supports state |
| Verification | External deterministic checks favored | Same; additional indepent judge when stakes justify |
| Collective | Single by default; small self-consistency only for objective answers | Ensemble/multi-agent only with real diversity/division |
| Recovery | One minimal adaptation before escalation | Multiple checkpointed adaptations within explicit budget |

## Compact-model rules

1. Normalize the request into fields before solving.
2. Choose from fixed presets and enums; avoid open-ended self-routing prose.
3. Externalize facts, arithmetic, search and tests whenever available.
4. Ask for one typed delta per call.
5. Keep assumptions explicit and few.
6. Verify independently; do not trust self-reported confidence.
7. Escalate ambiguous classification instead of silently widening the search.

If the model/harness cannot persist a route, include the compact route header in every turn. If it cannot call tools, return a typed `ActionRequest` for the harness.
