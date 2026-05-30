# C29 — Model floor & stylesheet routing  (Build Plan, Track A)

> Source / Spec ref: [`spec-faithful/C29-model-floor-stylesheet.md`](../spec-faithful/C29-model-floor-stylesheet.md)
> Track A, sweep-1. Plan altitude matches sweep-1 spec: workstreams + contract milestones, not task-level pseudocode.

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Floor declaration.** Encode "Claude Code @ Max = capability floor" as the single sanctioned coder adapter; this is the artifact that makes F19/F31 "Addressed by declaration". | S | C28 model identity known |
| T2 | **Model registry (`modeldb`-shaped).** `{id, family(provider-level), cost_tier}` per model; family label is the cross-family comparison key. Transfusion: Kilroy `modeldb` (AI-CONTEXT §6.3). | S | T1 |
| T3 | **Stylesheet schema + parser.** CSS-like (selector → declaration), layered TOML under C03. Transfusion: Fabro CSS model stylesheet (AI-CONTEXT §6.2). | M | C03 config shape; T2 |
| T4 | **`resolveModel(node)` cascade.** CSS specificity resolution → winning model; clamp coder nodes to floor (I1). | M | T3 |
| T5 | **`crossFamilyRule` (seam) — Phase-0 same-provider baseline per D-1/FE-1.** Phase 0 routes a same-provider judge that is rig/role/prompt-isolated from the coder and emits the active independence constraint; I2 is **relaxed (advisory, not fail-closed)** at Phase 0. Keep the `family` registry field + constraint emitter as the clean seam; the literal `family(judge) ≠ family(coder)` cross-provider enforcement (README:427) is **FE-1 (future)**, switched on when a second-provider family is registered. | M | T2, T4 |
| T6 | **Dispatch integration seam.** Expose resolution to C05/C28/C32 at node dispatch; record chosen model for attribution (C41/C23). | M | T4, T5 |
| T7 | **Lint/audit hook.** Deterministic check that every satisfaction-measuring formula's judge/coder pair carries a resolvable independence constraint (Phase-0: same-provider isolation present; FE-1: cross-family-valid). Lintable like other v4 deterministic rules. | S | T5 |

## 2. Dependency graph

```
C28 (floor adapter) ──▶ T1 ──▶ T2 ──▶ T3 ──▶ T4 ──▶ T6
                                          └──▶ T5 ──▶ T6, T7
C03 (config shape) ─────────────────▶ T3
```

**Critical path:** T1 → T2 → T3 → T4 → T5 → T6. T5 (independence seam) is the load-bearing gate consumed by C32/C34. **Per D-1/FE-1 the Phase-0 cross-family/single-adapter tension is RESOLVED:** the Phase-0 baseline is the same-provider judge (isolated by rig/role/prompt), so C32 can be acceptance-tested at Phase 0 *without* a registered non-Claude family. The literal cross-provider judge is FE-1.

**G20 — RESOLVED by D-1/FE-1 (no longer a Phase-0 blocker):** Phase 0 runs the same-provider judge, so no second-provider credential is required to stand up the evaluation tier. Sourcing a non-Claude provider + credentials is **FE-1 (future)**, revisited when a second-provider credential path exists; C29 keeps the `family` label + constraint emitter as the seam FE-1 switches on.

## 3. Parallelization

- T1 + (C03 shape read) can start immediately and in parallel.
- T2 (registry) and the T3 **schema** half can be drafted concurrently once T1 fixes the floor identity.
- T5 (independence-seam logic — Phase-0 same-provider isolation per D-1/FE-1) can be developed against a **stubbed registry** in parallel with T4 (resolution cascade), then joined at T6.
- T7 (lint) can be authored against the frozen interfaces (§4) before T6 wiring lands.

## 4. Interfaces-first / contract milestones (freeze early)

1. **`modeldb` entry shape** `{id, family, cost_tier}` with **family at provider granularity** (resolves G08 reading (a)). Freeze first — C32/C34 compare on this.
2. **`resolveModel(node) → modelIdentity`** signature + the floor-clamp postcondition (I1).
3. **Independence-constraint contract** (the `crossFamilyRule` seam). Phase-0 (D-1/FE-1): emit the active same-provider isolation constraint; I2 is advisory/relaxed at Phase 0. The fail-closed cross-provider form is FE-1. C32/C34 build against this stub immediately.
4. **Floor declaration** identity string. Downstream attribution (C41) and F19/F31 coverage cite it.

Freezing 1–4 lets C32 (judge harness) and C34 (holdout integrity / cross-family + independence enforcement) build against stubs in parallel with C29's internals.

## 5. Risks & de-risking order

| Risk | De-risk first by |
|---|---|
| **G08/G20 — no second family available** (highest). | Spike the **fail-closed** path (T5) and the registry's `family` label *before* the cascade, so the cross-family contract is proven independent of whether a second provider ever materializes. Surface G20 to the run/review-log as an upstream blocker. |
| Floor-clamp semantics ("⩾ floor") under a single-adapter world (degenerate: only one model). | Prototype T4 with a 1-entry registry to confirm clamp is a no-op-but-correct, then with ≥2 to confirm ordering. |
| Cost-tier expressiveness vs absent v4 cost model (G32). | Keep cost-tier a *preference label* only; do NOT build a cost model here (defer to C46). Prototype tier-preference selection (A5) with synthetic tiers. |
| Stylesheet round-trip / CSS-cascade fidelity to Fabro pattern. | Sweep-2 concern; sweep-1 only freezes selector/declaration shape. |

## 6. Definition of done (sweep-1)

- Spec acceptance A1–A5 each have a named owning task: A1→T4, A2→T5, A3→T4, A4→T1, A5→T3/T4.
- Floor declaration exists and names exactly one coder adapter (F19/F31 "Addressed by declaration" is backed by a real artifact, not just prose).
- `crossFamilyRule` contract is frozen and **fails closed**; C32/C34 can build against it.
- The three deferred/blocked items (G08 picked = provider-level; G20 = upstream sourcing; G32 = C46 owns cost model) are recorded in the review-log with their reasons.
- Per-component exit: resolution is deterministic, lintable (T7), and every interface in §4 is frozen for dependents.
