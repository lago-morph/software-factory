# C29 — Model floor & stylesheet routing  (Build Plan, canonical track)

> Source / Spec ref: [`spec/C29-model-floor-stylesheet.md`](../spec/C29-model-floor-stylesheet.md)
> Canonical track, sweep-2. Plan altitude: workstreams + contract milestones + concrete interface freeze order for the new sweep-2 depth.

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Floor declaration.** Encode "Claude Code @ Max = capability floor" as the single sanctioned coder adapter; this is the artifact that makes F19/F31 "Addressed by declaration". | S | C28 model identity known |
| T2 | **Model registry (`modeldb`-shaped).** `{id, family, cost_tier}` per model (D-10: binding, no `independence_class`); the `family` label is the cross-family comparison key. **Per D-1, Phase-0 is the same-provider judge — G08 reading (b)**; the provider-granularity reading (a) is the cross-provider/FE-1 form, not the Phase-0 contract (see T5). Transfusion: Kilroy `modeldb` (AI-CONTEXT §6.3). | S | T1 |
| T3 | **Stylesheet schema + parser.** CSS-like (selector → declaration), layered TOML under C03. Transfusion: Fabro CSS model stylesheet (AI-CONTEXT §6.2). Sweep-2: implement the concrete TOML grammar (§3.3), specificity ranking, and first-match tiebreak. Validate `model_id` references against registry at load time (E-C29-03, E-C29-05, E-C29-06). | M | C03 config shape; T2 |
| T4 | **`resolveModel(node)` cascade.** CSS specificity resolution → winning model; clamp coder nodes to floor (I1, E-C29-02). Sweep-2: concrete signature (§3.2), specificity algorithm (§3.3), floor-clamp logic. | M | T3 |
| T5 | **`crossFamilyRule` (seam) — Phase-0 same-provider baseline per D-1/FE-1.** Phase 0 routes a same-provider judge that is rig/role/prompt-isolated from the coder and emits `IndependenceConstraint{level:L1, cross_family_required:false}`. Keep the `family` registry field + constraint emitter as the clean seam; the literal `family(judge) ≠ family(coder)` cross-provider enforcement is **FE-1 (future)**, switched on when `judge_policy.cross_family_enforce=true` (E-C29-04). | M | T2, T4 |
| T6 | **Dispatch integration seam.** Expose resolution to C05/C28/C32 at node dispatch; record chosen model for attribution (C41/C23). | M | T4, T5 |
| T7 | **Lint/audit hook.** Deterministic check that every satisfaction-measuring formula's judge/coder pair carries a resolvable independence constraint (Phase-0: same-provider isolation present; FE-1: cross-family-valid). Lintable like other v4 deterministic rules. Sweep-2: also lints for sub-floor declarations (E-C29-02 static detection). | S | T5 |
| T8 (sweep-2 new) | **Acceptance test suite.** Implement AC-C29-01 through AC-C29-10 (§8.2) as executable checks. Particularly: the cascade specificity tests (AC-C29-01), floor-clamp (AC-C29-02), determinism (AC-C29-03), Phase-0 advisory constraint (AC-C29-04), cost-tier preference (AC-C29-05), error paths (AC-C29-06–08). AC-C29-09 (FE-1 family-enforce) marked as integration-gated. | S | T7 |

## 2. Dependency graph

```
C28 (floor adapter) ──▶ T1 ──▶ T2 ──▶ T3 ──▶ T4 ──▶ T6
                                          └──▶ T5 ──▶ T6, T7
C03 (config shape) ─────────────────▶ T3
T4, T5, T7 ──▶ T8 (test suite)
```

**Critical path:** T1 → T2 → T3 → T4 → T5 → T6. T5 (independence seam) is the load-bearing gate consumed by C32/C34. **Per D-1/FE-1 the Phase-0 cross-family/single-adapter tension is RESOLVED:** the Phase-0 baseline is the same-provider judge (isolated by rig/role/prompt), so C32 can be acceptance-tested at Phase 0 *without* a registered non-Claude family. The literal cross-provider judge is FE-1.

**G20 — RESOLVED by D-1/FE-1 (no longer a Phase-0 blocker):** Phase 0 runs the same-provider judge, so no second-provider credential is required to stand up the evaluation tier. Sourcing a non-Claude provider + credentials is **FE-1 (future)**, revisited when a second-provider credential path exists; C29 keeps the `family` label + constraint emitter as the seam FE-1 switches on.

## 3. Parallelization

- T1 + (C03 shape read) can start immediately and in parallel.
- T2 (registry) and the T3 **schema** half can be drafted concurrently once T1 fixes the floor identity.
- T5 (independence-seam logic — Phase-0 same-provider isolation per D-1/FE-1) can be developed against a **stubbed registry** in parallel with T4 (resolution cascade), then joined at T6.
- T7 (lint) can be authored against the frozen interfaces (§4) before T6 wiring lands.
- T8 (test suite) can be stubbed out (AC skeleton) once T3's grammar is frozen, then filled in as T4/T5 implement the behavior.

## 4. Interfaces-first / contract milestones (freeze early)

1. **`modeldb` entry shape** `{id, family, cost_tier}` (D-10 frozen). The `family` label is frozen first — C32/C34 compare on it. **Per D-1, Phase-0 resolves G08 to reading (b)** (same-provider judge; independence from rig/role/prompt isolation, not family diversity); **provider-granularity cross-family/cross-provider enforcement is FE-1**, not the Phase-0 contract. The field is the clean FE-1 seam.
2. **`resolveModel(node: NodeAttrs) → ModelIdentity`** concrete signature (§3.2) + the floor-clamp postcondition (I1) + E-C29-01/02 error contracts. Freeze before C05/C32 build against it.
3. **Stylesheet grammar** (§3.3) — the `[[model_rule]]` TOML shape, `[model_floor]`, and `[judge_policy]` sections. Freeze before T7 lint is authored.
4. **Independence-constraint contract** (the `crossFamilyRule` seam + `IndependenceConstraint` type, §3.2). Phase-0 (D-1/FE-1): emit the active same-provider isolation constraint; I2 is advisory/relaxed at Phase 0. The fail-closed cross-provider form (E-C29-04) is FE-1. C32/C34 build against this stub immediately.
5. **Floor declaration** identity string (`"claude-code@max"`, `family="claude"`, `cost_tier="standard"`). Downstream attribution (C41) and F19/F31 coverage cite it.

Freezing 1–5 lets C32 (judge harness) and C34 (holdout integrity / cross-family + independence enforcement) build against stubs in parallel with C29's internals.

## 5. Risks & de-risking order

| Risk | De-risk first by |
|---|---|
| **G08/G20 — no second family available — RESOLVED by D-1/FE-1.** | No longer a top risk: Phase-0 baseline is the same-provider judge (rig/role/prompt isolation), so the evaluation tier stands up without a second provider. Build the `family` label + constraint emitter as the FE-1 seam. |
| Floor-clamp semantics ("⩾ floor") under a single-adapter world (degenerate: only one model). | Prototype T4 with a 1-entry registry to confirm clamp is a no-op-but-correct, then with ≥2 to confirm ordering. Covered by AC-C29-02. |
| Cost-tier expressiveness vs absent v4 cost model (G32). | Keep cost-tier a *preference label* only; do NOT build a cost model here (defer to C46). Prototype tier-preference selection (A5) with synthetic tiers. Covered by AC-C29-05. |
| Stylesheet round-trip / CSS-cascade fidelity to Fabro pattern. | T3 implements and T8 verifies cascade specificity (AC-C29-01); determinism tested by AC-C29-03. |
| Registry-miss at rule-load vs resolution time. | T3 validates `model_id` references at stylesheet load, not deferred to resolution (E-C29-03, AC-C29-07). |

## 6. Definition of done

### Sweep-1 (preserved)

- Spec acceptance A1–A5 each have a named owning task: A1→T4, A2→T5, A3→T4, A4→T1, A5→T3/T4.
- Floor declaration exists and names exactly one coder adapter (F19/F31 "Addressed by declaration" is backed by a real artifact, not just prose).
- The independence-constraint contract (`crossFamilyRule` seam) is frozen; **Phase-0 emits the same-provider isolation constraint (I2 relaxed per D-1/FE-1), the cross-provider fail-closed form is FE-1**; C32/C34 can build against it.
- The deferred items are recorded with reasons: G08/G20 **RESOLVED by D-1/FE-1** (same-provider Phase-0 baseline; cross-family/cross-provider = FE-1); G32 = C46 owns cost model.
- Per-component exit: resolution is deterministic, lintable (T7), and every interface in §4 is frozen for dependents.

### Sweep-2 additions

- Concrete stylesheet grammar (§3.3) is implemented and validated: TOML `[[model_rule]]` / `[model_floor]` / `[judge_policy]` sections parse and round-trip.
- `resolveModel` concrete signature (§3.2) is implemented with the specificity cascade algorithm and floor-clamp.
- `crossFamilyRule` emits typed `IndependenceConstraint` with the correct Phase-0 values per D-1.
- All E-codes E-C29-01 through E-C29-06 are handled and surface with the documented error message.
- AC-C29-01 through AC-C29-10 are implemented as executable tests; AC-C29-09 (FE-1 path) may be gated by feature flag (`cross_family_enforce=true`).
- T7 lint hook statically detects sub-floor declarations (E-C29-02 at lint time) and missing-floor-declaration (E-C29-05).
- The worked routing example (§5.3) is a passing test vector.
- `modeldb` schema table with R/W-by column (§4.2) is frozen; downstream components (C32, C34, C46) cite only these three fields.
