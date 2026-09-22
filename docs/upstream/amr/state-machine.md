# Cognitive State Machine

The ten states form a cyclic graph, not a mandatory chain.

| State | Function | Common next states |
|---|---|---|
| `OBSERVE` | Normalize a new user/tool/worker/environment event | ORIENT |
| `ORIENT` | Frame goal, context, gaps, risk and task shape | ACQUIRE, REASON, PLAN, DECIDE, EVALUATE |
| `ACQUIRE` | Reduce an information deficit with provenance | ORIENT, REASON, EVALUATE, ADAPT |
| `REASON` | Produce hypotheses, derivations, models or candidates | ACQUIRE, REASON, PLAN, DECIDE, EVALUATE |
| `PLAN` | Produce executable actions, dependencies and contingencies | ACQUIRE, REASON, DECIDE, EVALUATE |
| `DECIDE` | Commit to a candidate, action, stop or escalation | EXECUTE, EVALUATE, ACQUIRE, ADAPT, DONE |
| `EXECUTE` | Perform one authorized action and capture its receipt | OBSERVE, EVALUATE, ADAPT |
| `EVALUATE` | Judge fit, correctness, evidence, progress or uncertainty | DECIDE, ACQUIRE, ADAPT, CONSOLIDATE, DONE |
| `ADAPT` | Propose/apply a bounded trajectory change after verdict | ORIENT, ACQUIRE, REASON, PLAN, DECIDE, EXECUTE, CONSOLIDATE |
| `CONSOLIDATE` | Create a durable lesson candidate | DONE, ORIENT for a new episode |

`DONE` is a terminal pseudo-state. Stopping is a control policy, not a cognitive state.

## Required loops

- Evidence gap: `REASON→ACQUIRE→REASON`.
- Tool loop: `DECIDE→EXECUTE→OBSERVE→EVALUATE`.
- Recovery: `EVALUATE(fail)→ADAPT→<rollback target>`.
- Profile change: `EVALUATE→ADAPT→ask-me-reasoning`, which increments the version.
