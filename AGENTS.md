# AGENTS.md

## Purpose

This repository adds the smallest useful Jev integration to Ask Me Reasoning (AMR), with a bias toward compact-model reliability.

## Authority

- AMR owns routing policy, state-machine semantics, budgets, verification, acceptance, and side-effect authority.
- Jev supplies bounded semantic judgments only.
- Deterministic facts, permissions, calculations, schemas, tests, and runtime observations stay in code.
- Generative models execute bounded work; they do not silently rewrite the route.

## Working method

Use the established Ask Matt flow for every non-trivial brick:

1. `to-spec`: define the seam, scope, non-goals, contracts, acceptance proofs, and dependencies.
2. Challenge the spec before ticketing.
3. `to-tickets`: create vertical, independently testable tracer bullets with explicit blockers.
4. Implement TDD: red check -> minimum implementation -> green check.
5. Review against the spec and standards.
6. Run a Ponytail challenge on every ticket and diff.
7. Squash-merge only when checks and review are green.

Do not skip directly from idea to framework.

## Ponytail rules

Before adding code, stop at the first rung that holds:

1. Do we need it?
2. Does AMR already have the concept?
3. Does the implementation language's standard library already cover it?
4. Does the platform or TypeSafe API already cover it?
5. Does an installed dependency cover it?
6. Can the same behavior be expressed with less code?
7. Only then add the minimum implementation.

No speculative abstractions, one-implementation interfaces, generic managers, duplicate route models, or configuration nobody sets.

## Repository constraints

- Documentation and contracts are written in English.
- Prefer small pure functions and closed typed choices.
- One brick per PR.
- No new runtime layer parallel to the AMR Reasoning Route.
- No profile change without the AMR verification/adaptation contract.
- No Jev-selected side effect can bypass existing authorization.
- Ambiguous semantic routing escalates; it must not silently widen search.
- Every non-trivial behavior leaves one runnable check behind.

## Current roadmap

- v0: Jev-assisted `ORIENT` only.
- Later work is evidence-driven. Do not implement dynamic next-state routing or speculative target heads until v0 evaluation shows that post-orientation drift remains a material problem.
