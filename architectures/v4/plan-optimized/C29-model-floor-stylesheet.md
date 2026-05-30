# C29 — Model floor & stylesheet routing  (Build Plan, Track B)

> Source / Spec ref: spec-optimized/C29-model-floor-stylesheet.md

## 1. Work breakdown

| id | description | size | prerequisites |
|---|---|---|---|
| T1 | **Freeze `model_registry` schema** — `{id, adapter, family, independence_class, cost_tier, capability_rank, status}`. The `family` ("shared-weights lineage") + `independence_class` fields are the G08 resolution. (DELTA-01) | S | C03 config shape |
| T2 | **Freeze `resolveSelection(node, ctx) → ModelSelection` contract** — inbound node/ctx; outbound `{adapter, model, family, independence_class, cost_class, floor_satisfied, independence_verdict, winning_rule_id}`. The interface C05/C28/C32 bind to. | M | T1, C28 selection shape (co-design) |
| T3 | **Stylesheet grammar + compiler** — CSS-like `(selector, declaration)` rules → compiled deterministic decision function; cascade/specificity resolution. Transfuse Fabro CSS stylesheet shape. (DELTA-04) | M | T1 |
| T4 | **Stylesheet lint pass** — reject unregistered-model references, undefined families, ambiguous cascades; CI gate. (DELTA-04) | S | T3 |
| T5 | **Floor clamp** — coder-node post-condition `capability(model) ⩾ capability(floor)`; read C28 conformance result so no non-conformed adapter wins a coder rule; log clamps. (DELTA-04, I1) | M | T2, C28 conformance suite (read) |
| T6 | **`judge_independence_policy` engine (L0–L3)** — evaluate `independence_verdict` against the configured level; the graded enforcement that replaces the binary cross-family rule. (DELTA-02, I2) | M | T1, T2 |
| T7 | **Credential gate `requireJudgeFamily()`** — for L≥2, require a valid judge-seat credential handle + a registered cross-family entry; else trigger fail-closed. (DELTA-03) | M | T6; OQ-2 judge-seat admissibility |
| T8 | **Fail-closed + `degraded_eval` escape valve** — refuse satisfaction-measuring dispatch when independence unmet; honor operator-signed `degraded_eval` acceptance, tag scores `independence_degraded`, log. (DELTA-06) | M | T6 |
| T9 | **Cost-tier live-budget selector** — among floor-or-above candidates pick cheapest meeting capability need, reading C46/C28 live budget; static `cost_tier` fallback when stream absent. (DELTA-05) | M | T2, C46 stream (read), C28 governor (read) |
| T10 | **Resolution-record emitter** — emit `{node, winning_rule_id, model, family, independence_verdict, clamp?}` to C23/C41 per resolution; makes routing auditable + replayable. (DELTA-04/06) | S | T2, C23/C41 |
| T11 | **Independence-level tagging on satisfaction outputs** — stamp `L1/L2/L3/independence_degraded` so C46/C50 can filter trust. (DELTA-06) | S | T6, T8 |
| T12 | **Config surface (C03)** — stylesheet TOML section, registry, `judge_independence_policy` level (default L1), judge-seat credential ref. | S | T1, T6 |
| T13 | **`crossFamilyConstraint` / `floorDeclaration` emitters** — outbound constraints consumed by C32/C34. | S | T6 |

## 2. Dependency graph

- **Upstream (must precede):** C03 (config/registry/policy section), C28 (the floor adapter + its conformance result + seat-governor budget — co-designed selection contract), C46 (live cost stream; optional/graceful at Phase 0/1).
- **Critical path:** T1 → T2 → T6 → T7/T8 (the independence policy + credential gate + fail-closed are the load-bearing chain; T7 is gated by **OQ-2**, judge-seat admissibility). T5 floor clamp depends on the C28 conformance seam (**OQ-4** co-design).
- **Downstream consumers:** C05 (dispatch resolves through C29), C28 (consumes `model_selection`), C32 (constrained judge identity), C34 (family-independence verdict input), C50/C46 (independence-tagged trust).
- **Concurrent with:** C28, C25, C26, C27, C24 (Batch 2); C29 may start in Batch 1 once C01/C03 shapes are fixed.

## 3. Parallelization

Once **T1 (registry) + T2 (selection contract)** freeze, fan out:
- **Stream A (stylesheet engine):** T3 compiler → T4 lint. Independent of judge logic.
- **Stream B (floor):** T5 clamp — depends only on the C28 conformance read.
- **Stream C (independence — the spine):** T6 policy engine → T7 credential gate → T8 fail-closed/escape-valve → T11 tagging.
- **Stream D (cost):** T9 live-budget selector — independent, builds against a stub budget stream.
- **Stream E (glue):** T10 emitter, T12 config, T13 constraint emitters — small, parallel against stubs.

Streams A–E build against the T1/T2 contracts + stubs concurrently.

## 4. Interfaces-first / contract milestones

Freeze early so dependents build against stubs:
1. **`model_registry` schema (T1)** — unblocks every selector/declaration and the C28 conformance/registry seam.
2. **`resolveSelection`/`ModelSelection` contract (T2)** — unblocks C05 (dispatch), C28 (selection consumer), C32 (judge identity).
3. **`judge_independence_policy` levels + `IndependenceConstraint` (T6/T13)** — unblocks C32/C34/C50 building their trust logic against the named levels before the engine lands.
4. **`degraded_eval` acceptance format (T8)** — unblocks the operator/promotion-gate (C50) workflow that consumes degraded-trust tags.

## 5. Risks & de-risking order

1. **OQ-1/OQ-2 — RESOLVED by D-1/FE-1 (no longer Phase-0 spikes).** D-1 ratifies **L1 (same-provider, prompt-independent) as the Phase-0 default** — holdout integrity from rig/role/prompt isolation, not family diversity. The metered-API judge seat (OQ-2/DELTA-03) and **L2/L3 (cross-family/cross-provider) are FE-1 (future)**, so judge-seat admissibility and the second-key/G37 question do **not** gate Phase 0; T7 stays off the Phase-0 critical path. Build T6/T7 as the clean FE-1 `judge_family` seam that switches on when a second-family credential lands. (FE-1 residual: minimum independence level per high-stakes class, revisited when a second-provider path exists.)
2. **OQ-4 — floor capability comparator (co-design with C28).** Spike the `capability_rank` metric jointly so "⩾ floor" is well-defined; without agreement T5's clamp is unverifiable.
3. **OQ-3 (FE-1-scoped) — does L2 (cross-family-same-provider) buy real independence** over L1, or collapse via shared training distribution (F48 residual)? Determines whether L2 is a real tier or dead config; an FE-1-time question (prototype a disagreement-rate measurement before committing L2 routing rules), not a Phase-0 blocker.
5. **Cascade-specificity correctness (T3/T4)** — CSS cascade is a classic source of surprising precedence bugs; lock the lint + determinism tests (spec A5) before exposing the stylesheet to operators.

## 6. Definition of done

- **Per-component:** spec acceptance criteria 1–7 all pass; floor clamp + conformance gate enforce I1; graded independence policy enforces I2 with fail-closed; resolution deterministic + replayable from the emitted record; cost routing prefers cheapest floor-or-above with graceful static fallback; every satisfaction score carries its independence level.
- **Per-task exits:** T1/T2 — schemas reviewed + frozen, C05/C28/C32 building against them. T3/T4 — stylesheet compiles, lint rejects unregistered models, cascade deterministic. T5 — sub-floor/non-conformed coder rule clamps + logs. T6 — each L0–L3 level evaluated correctly against a registry. T7 — L≥2 without a valid judge-seat credential is refused at the gate. T8 — independence-unmet dispatch fails closed unless a signed `degraded_eval` is present, which tags + logs. T9 — cheaper candidate selected under budget pressure; static fallback identical without C46. T10/T11 — resolution records emitted to C23/C41; satisfaction scores tagged.
- **Open-question gates:** OQ-1/OQ-2/OQ-3/OQ-4 resolved or explicitly carried into review-log before C29 is production-ready; **T7 not merged until OQ-2 (judge-seat admissibility) resolves**, and the default policy level documented as **L1** with the L2/L3 upgrade path costed.
