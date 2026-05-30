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
| T5 | **`crossFamilyRule`.** Enforce `family(judge) ≠ family(coder)`; **fail closed** when no compliant family registered (I2). This is the load-bearing cross-family deliverable (README:427). | M | T2, T4 |
| T6 | **Dispatch integration seam.** Expose resolution to C05/C28/C32 at node dispatch; record chosen model for attribution (C41/C23). | M | T4, T5 |
| T7 | **Lint/audit hook.** Deterministic check that every satisfaction-measuring formula's judge/coder pair is cross-family-valid (lintable like other v4 deterministic rules). | S | T5 |

## 2. Dependency graph

```
C28 (floor adapter) ──▶ T1 ──▶ T2 ──▶ T3 ──▶ T4 ──▶ T6
                                          └──▶ T5 ──▶ T6, T7
C03 (config shape) ─────────────────▶ T3
```

**Critical path:** T1 → T2 → T3 → T4 → T5 → T6. T5 (cross-family) is the load-bearing gate: it is *consumed by C32/C34* and sits on the inventory critical path (note 3 — cross-family vs single-adapter tension). C32 (judge harness) cannot be acceptance-tested until T5 + its **upstream G20 dependency** (a registered non-Claude family) both exist.

**Hard external blocker (G20):** acceptance of T5's *positive* path (a judge actually running on a different family) is gated on an upstream decision that sources a non-Claude provider + credentials. C29 builds the *constraint and fail-closed path* without it; the *satisfied* path waits on G20.

## 3. Parallelization

- T1 + (C03 shape read) can start immediately and in parallel.
- T2 (registry) and the T3 **schema** half can be drafted concurrently once T1 fixes the floor identity.
- T5 (`crossFamilyRule` logic) can be developed against a **stubbed registry** in parallel with T4 (resolution cascade), then joined at T6.
- T7 (lint) can be authored against the frozen interfaces (§4) before T6 wiring lands.

## 4. Interfaces-first / contract milestones (freeze early)

1. **`modeldb` entry shape** `{id, family, cost_tier}` with **family at provider granularity** (resolves G08 reading (a)). Freeze first — C32/C34 compare on this.
2. **`resolveModel(node) → modelIdentity`** signature + the floor-clamp postcondition (I1).
3. **`crossFamilyRule` contract** including the **fail-closed-when-no-compliant-family** behavior (I2). C32/C34 build against this stub immediately.
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
