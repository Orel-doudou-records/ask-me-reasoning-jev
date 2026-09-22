# Ask Me Reasoning Jev

A minimal Jev-assisted routing layer for Ask Me Reasoning (AMR), optimized for compact models.

## Design rule

**AMR owns policy. Jev supplies bounded semantic judgments. Code owns execution.**

This repository is intentionally incremental. The first validated slice uses Jev only at `ORIENT`; dynamic next-state routing is deferred until evaluation proves it is needed.

## Project status

The dependency graph and current implementation status are tracked in [AMR-JEV-001](https://github.com/Orel-doudou-records/ask-me-reasoning-jev/issues/1). The canonical v0 contract is `docs/specs/0001-jev-orient-routing.md`.

## Upstream references

- TypeSafe skill: https://github.com/typesafe-ai/skills/blob/main/skills/typesafe-ai/SKILL.md
- Jev engineering skill: https://github.com/dbreunig/building-with-jev-skill
- Jev Ultrafast reference architecture: https://github.com/browser-use/jev-ultrafast
- Ponytail: https://github.com/DietrichGebert/ponytail

## Minimal TypeSafe boundary

`typesafe_adapter.route_orient(state, api_key)` sends the existing ORIENT contract to TypeSafe System One and immediately passes the returned Noul answers to the provider-agnostic AMR reducer.

The adapter does not read environment variables, persist credentials, retry side effects, or own routing policy. The caller owns credential sourcing and fallback behavior.

## Evaluation

The labeled corpus is `evaluation/cases.json`. It is intentionally readable and covers every v0 base preset, every topology, mixed signals, high-assurance wrapping, adversarial state, and ambiguity behavior.

Offline corpus/reducer check:

```bash
python evaluate.py
```

Live Jev evaluation:

```bash
TYPESAFE_API_KEY=... python evaluate.py --live
```

The live report keeps boolean signal accuracy, ambiguity-target behavior, route accuracy, escalation behavior, and provider errors separate. Do not tune the frozen v0 thresholds on this corpus and then present the same corpus as an independent final evaluation.

See `AGENTS.md` before making changes.
