# Ask Me Reasoning Jev

A minimal Jev-assisted routing layer for Ask Me Reasoning (AMR), optimized for compact models.

## Design rule

**AMR owns policy. Jev supplies bounded semantic judgments. Code owns execution.**

This repository is intentionally incremental. The first validated slice uses Jev only at `ORIENT`; dynamic next-state routing is deferred until evaluation proves it is needed.

## Current brick

- Parent: [AMR-JEV-001](https://github.com/Orel-doudou-records/ask-me-reasoning-jev/issues/1)
- Spec: `docs/specs/0001-jev-orient-routing.md`
- Status: spec ready for ticketing

## Upstream references

- TypeSafe skill: https://github.com/typesafe-ai/skills/blob/main/skills/typesafe-ai/SKILL.md
- Jev engineering skill: https://github.com/dbreunig/building-with-jev-skill
- Jev Ultrafast reference architecture: https://github.com/browser-use/jev-ultrafast
- Ponytail: https://github.com/DietrichGebert/ponytail

## Minimal TypeSafe boundary

`typesafe_adapter.route_orient(state, api_key)` sends the existing ORIENT contract to TypeSafe System One and immediately passes the returned Noul answers to the provider-agnostic AMR reducer.

The adapter does not read environment variables, persist credentials, retry side effects, or own routing policy. The caller owns credential sourcing and fallback behavior.

See `AGENTS.md` before making changes.
