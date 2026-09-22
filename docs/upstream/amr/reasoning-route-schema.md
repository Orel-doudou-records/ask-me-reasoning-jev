# Reasoning Route Schema

The route is the episode source of truth. It can be serialized as Markdown/YAML or held inline, but its logical fields and invariants are identical.

```yaml
schema_version: "1.0"
route_id: <stable-id>
status: active|blocked|awaiting_verification|closed
storage: inline|persisted
owner: <person-or-system>
goal:
  outcome: <text>
  success_tests: [<test>]
risk: low|medium|high|critical
active_gate: R0-SCOPE|R1-PROFILE|R2-STEP|R3-ACCEPT
bottleneck: <one missing condition>
capabilities:
  persistence: true|false
  retrieval: true|false
  code: true|false
  tools: [<tool-class>]
  parallelism: true|false
profile:
  version: <integer>
  preset: direct|grounded|analytic|exploratory|causal|agentic|high-assurance
  policy_tier: compact|extended
  mode: [deductive|inductive|abductive|analogical|causal|counterfactual|probabilistic|simulation|mixed]
  topology: linear|chain|tree|graph|parallel|recursive
  grounding: [parametric|working_memory|episodic_memory|semantic_memory|retrieval|knowledge_graph|web|code|tool|environment]
  collective: single|self_consistency|ensemble|debate|multi_agent
  domain: [logical|mathematical|commonsense|causal|spatial|temporal|visual|social|code|multilingual|other]
  control: [route|allocate_budget|branch|prune|backtrack|retry|checkpoint|escalate|stop]
  verifier: [semantic|citation|code|test|schema|solver|constraint|human]
  output_contract: <name>
current_state: OBSERVE|ORIENT|ACQUIRE|REASON|PLAN|DECIDE|EXECUTE|EVALUATE|ADAPT|CONSOLIDATE|DONE
allowed_expert: <exact skill name>
expected_output: <typed contract name>
evidence: [<refs>]
candidates: [<refs>]
uncertainty: low|medium|high
budget:
  class: micro|standard|bounded-search|long-horizon|critical
  branches: <nonnegative integer>
  depth: <nonnegative integer>
  tool_rounds: <nonnegative integer>
  adaptation_rounds: <nonnegative integer>
stop:
  max_residual_uncertainty: low|medium|high
  on_exhaustion: best_effort|escalate|fail_closed
checkpoints: [<refs>]
transitions: [<typed transition refs>]
review_at: <date or condition>
```

## Invariants

1. Exactly one `allowed_expert` exists while active.
2. Every expert input matches `route_id`, active gate, profile version and current state.
3. The profile changes only after a fail/uncertain verdict and an adaptation proposal applied by the router.
4. Budget counters never increase except through an accepted adaptation patch.
5. `DONE` requires declared success tests and required verification.
6. No field stores private chain-of-thought.
