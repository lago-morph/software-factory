# P-32 — Distance estimator (multi-component, typed)

**Dispatch tier.** per-primitive (designed-system, with research-grade-uncertainty sub-flag on calibration).
**Claimed by.** [U-C Anchor-Distance Factory](../tracks/unified-C.md) (load-bearing primitive #2 of the ADF substrate).
**Depends on.** [P-22 polyglot codebase index](P-22-polyglot-codebase-index.md), [P-23 dependency-and-impact graph](../tracks/brownfield-substrate-first.md) (per [primitives/index.md](index.md)).

## Contract restatement

A substrate function `distance(work-unit, anchor-set) → DistanceTuple` where `DistanceTuple` is a **typed decomposed record**, not a real-valued scalar. Three named components per [unified-C §1 primitive #2](../tracks/unified-C.md):

1. **`graph_distance`** — shortest-path length in P-23's dependency-impact graph from the work-unit's touched symbol(s) to the anchor's grounding symbol(s). Integer ≥ 0; ∞ if disconnected.
2. **`pace_layer_crossings`** — count of Brier pace-layer boundaries crossed between work-unit and anchor, derived from the anchor's typed `kind` field ({`intent-invariant`, `architecture-rule`, `standards-rule`, `live-test`, `runtime-trace`}) and the work-unit's classified layer. Integer 0–4.
3. **`intent_field_touches`** — count of El-Kaim 9-field intent-block fields the work-unit's diff cross-references or modifies (greenfield) / spec-anchored requirement IDs touched (brownfield variant). Integer ≥ 0.

Plus a derived **`contradiction_flag: bool`** set when the change *implies* anchor mutation (F37 mitigation per [unified-C §1](../tracks/unified-C.md)). **Tuple is canonical**; scalar aggregation is dispatcher-local. Determinism: `graph_distance` fully deterministic (BFS); `pace_layer_crossings` deterministic given typed `kind` + layer classifier; `intent_field_touches` deterministic for explicit cross-references, **partly LLM-judged** for implicit semantic touches.

## Construction path

**Graph distance.** Composes P-23's blast-radius graph. Substrate resolves the diff to touched symbols via P-22's `index.symbols_at(file, byte-range)`, resolves the anchor to its `grounding_symbols` (carried at declaration time), then runs **BFS** (unit weights) or **Dijkstra** (when P-23 weights edges by call-frequency). Tools: **Glean** via Angle (`derive distance(W, A) = path(W, A, references)`); **CodeQL** via a custom QL predicate; **Stack Graphs** via partial-path stitching. *Integration:* in the Glean realisation the substrate emits `python.Distance { source = W, target = A, hops = N }` and reads `N` as `graph_distance` — Glean's derived-predicate compilation handles the BFS internally.

**Pace-layer crossings.** Anchor's `kind` maps deterministically into Brier's pace-layer ordinal (`intent-invariant`=0 slowest → `runtime-trace`=4 fastest). Work-unit's layer is classified by the file/artifact it touches (e.g., `ARCHITECTURE.md` = layer 1; `tests/*` = layer 3; production source = layer 3–4). *Integration:* substrate computes `pace_layer_crossings = |layer(work-unit) - layer(anchor)|` using a substrate decision table — the same artifact P-19 (regime classifier) uses for layer classification, so the two primitives share one source of truth.

**Intent-field-touch count.** Two paths: (1) **explicit cross-references** — diff contains `intent-field:<field-id>` markers (P-15 / P-17 perimeter-enforced) and substrate counts them; (2) **implicit semantic touches** — a P-14-routed LLM judge reads the diff against the El-Kaim 9-field intent block and emits a boolean per field. *Integration:* substrate composes P-22's `index.symbols_in_diff(work-unit)` with a stored `symbol → intent-field` map (built at intent-block authoring, maintained as a P-13 reconciliation artifact) for the deterministic half, falling back to `judge.intent_field_touches(diff, intent-block) → {field-id: bool}` for unmapped symbols.

## Multi-component aggregation

Dispatcher (P-19 variant) consumes the tuple under named weights `(w_g, w_p, w_i)`: `composite = w_g · graph_distance + w_p · pace_layer_crossings + w_i · intent_field_touches`. **Tuple canonical; scalar dispatcher-local.** Different dispatchers (per work-unit class, per region) may apply different weights; substrate commits to no single weighting. Thresholds `τ_low` / `τ_high` per [unified-C §1.3](../tracks/unified-C.md) apply to the composite; the P-05 distance-keyed trajectory log retains the decomposed tuple so post-hoc analysis can re-weight. **Open weighting question:** no corpus recipe selects `(w_g, w_p, w_i)` — weights are dispatcher-empirical.

## Goodhart resistance

[U-C OQ-1 / §7-1](../tracks/unified-C.md): agents may game work-unit descriptions to land under `τ_low`. The multi-component structure provides **partial structural resistance, not closure.** Gaming `graph_distance` requires limiting actual symbol reach (a real cost on the change, not a description trick); gaming `pace_layer_crossings` requires mis-typing the anchor at declaration, which is a separate `anchor-edit` class always routed L4 ([unified-C §1 primitive #4](../tracks/unified-C.md)); gaming `intent_field_touches` is the weakest leg — agents can avoid `intent-field:` markers, and the implicit semantic-touch judge inherits F33/F51 Ashby-deficiency. Net: **two of three legs structurally resistant; third probabilistically guarded and brittle.** The U-C patrol-tier watchdog (P-06) catches distributional gaming post-hoc but is not preventive. **Not closure of F47** — reduces the gameable surface from three legs to one plus a patrol detector on the residual.

## Calibration uncertainty

Distance values must be **calibrated against actual difficulty / risk** for `τ_low` / `τ_high` to be meaningful. U-C §7-5 names this: operator legibility presupposes the tuple tracks an operator's intuitive sense of risk. Corpus offers **no calibration recipe**. Plausible paths (historical-incident → distance-tuple regression; operator-rated calibration sample) need empirical study that has not been done. **Calibration is open.**

## Corpus-why citation

Load-bearing corpus problems: **[U-C §1 primitive #2 + §7-1](../tracks/unified-C.md)** (distance is the substrate's first-class scalar operationalising Brier's pace-layer gradient, parameterising lights-out vs Augmentation vs human per [brief §2.1](../00-brief-v3.md)); **[F47 Visible-Metric Drift](../failure-modes-v3.md#f47--visible-metric-drift-goodhart-on-tokens)** (any dispatch-driving metric becomes a target); **[F33 Adversarial-prompt defeat of LLM-based security analysis](../failure-modes-v3.md#f33--adversarial-prompt-defeat-of-llm-based-security-analysis)** (the LLM-judged half of `intent_field_touches`); **[F51 Ashby-deficient probabilistic guard](../failure-modes-v3.md#f51--ashby-deficient-probabilistic-guard)** (broader framing for the same probabilistic component). Secondary: [F37 silent contradictory-prompt collapse](../failure-modes-v3.md#f37--silent-contradictory-prompt-collapse) (the `contradiction_flag` is U-C's F37 catch).

## Research-grade-uncertainty flag

**Flagged on two sub-axes**: (a) **calibration** — no corpus recipe maps the tuple to operator-meaningful risk; thresholds and weights empirical-only; (b) **Goodhart resistance of the LLM-judged third leg** — F33/F51 apply; structure mitigates but does not close. **Not flagged on construction.**

## Buildability verdict — decomposed

- **Construction:** `designed-system`. Each component has a named-tool construction path; integration composes over P-22 and P-23 (both `designed-system`, registry High).
- **Calibration:** `research-grade-uncertainty`. No corpus recipe; thresholds and weights are empirical-only.
- **Goodhart resistance:** `designed-system with partial research-grade residue`. Structural resistance on two of three components; LLM-judged third leg + patrol detector is the open residue.

**Overall:** `designed-system` for construction, with a mandatory `research-grade-uncertainty` flag on calibration that Phase-4.2 methodology-matching must carry forward as an open risk against U-C.
