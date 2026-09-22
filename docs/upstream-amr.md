# Upstream Ask Me Reasoning contracts

This repository integrates with Ask Me Reasoning (AMR) but does not own AMR policy.

## Source status

As of 2026-09-22, no canonical `Orel-doudou-records/ask-me-reasoning` repository is accessible from GitHub. To keep this repository self-contained for agents, it vendors only the AMR contracts that this integration directly consumes.

The snapshot below was copied byte-for-byte from the Ask Me Reasoning skill artifact dated 2026-09-01.

These files are an **integration dependency snapshot**, not a fork of AMR. Do not edit them to make AMR-Jev easier to implement.

## Vendored contracts

| Local snapshot | AMR role | SHA-256 |
| --- | --- | --- |
| `docs/upstream/amr/selection-policy.md` | preset/profile selection authority | `47820fe3b9f0b8776ca671a3ddd5476ef455c53395d6e035bb9794c9542f2999` |
| `docs/upstream/amr/model-capability-policy.md` | compact/extended model constraints | `ef95647119fe0260dc5d535e172c09a6f4d90e7641407ad11cf5ab6bd0d56194` |
| `docs/upstream/amr/state-machine.md` | legal cognitive states and transitions | `411020dbf7dcbb6f0ccda7cf76267c73e9ac464b58236c9917ad439712a0527e` |
| `docs/upstream/amr/modules.md` | `frame_delta`, `verification_verdict`, and `adaptation_proposal` contracts | `d1696ef9509f8c30b95b816c50643e7ed4eee4c6178e88c058e5013c57cd22d0` |
| `docs/upstream/amr/reasoning-route-schema.md` | Reasoning Route fields and invariants | `b0a647b830b887060501e42ca76483b34241c1b8a77e3d29b07633e0898994a2` |

## Authority rule

When AMR-Jev code conflicts with a vendored AMR contract, the AMR contract wins unless a newer upstream AMR artifact explicitly changes it.

AMR-Jev may interpret or adapt those contracts at its integration seam, but it must not silently redefine them.

## Refresh protocol

Refresh this snapshot only from a newer canonical AMR artifact.

1. Replace the affected vendored files byte-for-byte.
2. Update the artifact date and SHA-256 values in this document.
3. Review the upstream diff before changing AMR-Jev behavior.
4. If the upstream change alters the integration seam, open a new Ask Matt spec before implementation.
5. Do not mix an upstream snapshot refresh with unrelated feature work.

If a canonical AMR repository becomes available, replace this snapshot locator with a pinned upstream repository reference rather than maintaining two editable sources of truth.
