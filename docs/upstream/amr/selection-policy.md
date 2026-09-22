# Selection Policy

Select the cheapest sufficient profile by checking hard requirements before subjective difficulty.

## Priority rules

1. Current/external fact → grounding before more reasoning.
2. Deterministic calculation/test → code, solver or schema oracle.
3. Material action → plan, permission gate, execution observation and verification.
4. Several plausible alternatives → bounded tree/search.
5. Shared cross-dependencies → graph, not merely a longer chain.
6. Self-similar large problem → recursive decomposition with base case and depth cap.
7. High stakes or unresolved high uncertainty → stronger verifier, ensemble diversity or human gate.
8. Otherwise use direct or analytic single-trajectory reasoning.

## Preset matrix

| Preset | Required signal | Default chain | Default verifier |
|---|---|---|---|
| `direct` | One-hop/transform, low risk, low uncertainty | `ORIENT→DECIDE→EVALUATE→DONE` | schema or semantic |
| `grounded` | External knowledge/evidence | `ORIENT→ACQUIRE→REASON→EVALUATE→DONE` | citation/source |
| `analytic` | Ordered multi-step dependencies | `ORIENT→REASON(chain)→DECIDE→EVALUATE` | code/test/semantic |
| `exploratory` | Multiple hypotheses/solutions | `ORIENT→REASON(tree)↔EVALUATE/prune→DECIDE→EVALUATE` | independent judge/oracle |
| `causal` | Mechanism/intervention/what-if | `ORIENT→ACQUIRE→REASON(graph)→EVALUATE→DECIDE` | data/code/source |
| `agentic` | Tools/actions with new observations | `ORIENT→PLAN→DECIDE→EXECUTE→OBSERVE→EVALUATE↔ADAPT` | environment/test |
| `high-assurance` | High consequence or critical uncertainty | Wrap the minimal adequate preset with stronger evidence, deterministic verifier and human/fail-closed gate | strongest available |

## Budget classes

| Class | Compact default | Extended allowance |
|---|---|---|
| `micro` | 1 trajectory, depth 1, no branch, no adaptation | Same unless an oracle forces one tool call |
| `standard` | ≤3 subproblems, depth 3, ≤2 tool rounds, 1 adaptation | Adaptive decomposition with explicit caps |
| `bounded-search` | beam 2, depth 2, ≤4 candidates, 1 adaptation | beam 3–5, depth set by value and verifier |
| `long-horizon` | Checkpoint every step, one action per loop, bounded retries | Task graph/parallel workers when divisible |
| `critical` | No unsupported conclusion; fail closed or human gate | Ensemble only for genuine error diversity; still bounded |

Multi-agent is never selected solely by difficulty. Require independent subproblems, distinct roles or demonstrably useful error diversity.
