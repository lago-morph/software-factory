---
based-on-commit: 9a205b6
based-on-date: 2026-05-24
track: greenfield-methodology-first
axis: methodology-first
mandate-scope: greenfield
---

# Greenfield methodology-first track

**One-line stance.** For greenfield, the per-cycle process — its work-unit, its gates, the way it accumulates knowledge, and the way it classifies and recovers from failure — is the load-bearing design surface; substrate is whatever the chosen cycle *forces into existence*. The cycle this track defends is a **typed-intent → narrow-scope cycle → holdout-judged increment → curated promotion** loop with a hard regime-classification gate at the front and structural (not voluntary-discipline) controls everywhere. Substrate is derived in §1.4, not pre-decided.

---

## §0 Axis declaration, glossary, and defense

### §0.1 Mini-glossary (track-local)

These re-use brief §0 glossary terms unless redefined. Track-local terms:

| Term | Definition (track-local) |
|---|---|
| **Work-unit** | A single bounded delivery the cycle commits to: ≤N requirements (per F36 budget), one typed intent block, one acceptance-region (per F39 shape diagnosis), one judged increment. Granularity is methodology-set, not operator-chosen per cycle. |
| **Typed intent block** | El Kaim Ch 3 §4.1 9-field object with non-negotiable `invariants` ([`research/14-el-kaim-book-intent-and-spec-authorship.md`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)). Treated here as **the durable upstream anchor**, distinct from the spec (which is malleable downstream of intent). |
| **Spec layer** | Layer-3 EARS-mandated ([`research/25-requirements-engineering-foundations.md`](../../../research/25-requirements-engineering-foundations.md) §2) acceptance-criteria block; free prose only in `statement`/`rationale`. **Malleable; intent is not.** This is the track's reconciliation of UC4 spec-malleability with MISSED-3. |
| **Regime gate** | Pre-cycle classifier that routes a work-unit to L3 (augmented), L4 (lights-out with sample audit), or `escalate` (human-required). Uses Jaymin K=5 / paraphrase-robustness ([`research/09-jaymin-book-harnesses-practices-mental-models.md`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5) but treats thresholds as per-work-unit-class parameters, not global bars. |
| **Promotion** | Explicit post-cycle act of moving an insight from the trajectory into a typed-and-curated artifact (skill, scenario, intent invariant, decision record). Promotion is **structural** (substrate refuses to forget) — not a voluntary post-hoc discipline (defeats F53). |
| **Discovery decomposition** | Anti-F59 design: decomposition of a work-unit is **revisable inside the cycle**, not frozen at a phase gate. The cycle has a `redecompose` action; F59 is mitigated by making decomposition a soft commit. |

### §0.2 The axis and why it fits greenfield

Methodology-first means: the per-cycle process is decided first; substrate primitives are then enumerated as *what the process forces into existence*. For greenfield, this is the right primary axis for four reasons that the corpus anchors:

1. **No codebase = the process is the only artifact at day 0.** A greenfield factory's first 100 cycles produce more *cycle-shape* than they produce code. Compare brownfield, where the codebase + tests + telemetry are themselves a substrate the methodology must respect (the brownfield-primary corpus — reports 03, 22, followup/11 per CHALLENGE-6/7/8 — assumes a queue of issues against an existing system). Greenfield has no such queue; the cycle *constructs* the queue.
2. **The cold-start risk (brief §5) is a methodology risk.** Reports 25, 26, 30, 31, followup/10 — the §5.1 required reading — name the cold-start risk in *process* terms (spec-authorship discipline, prompt-contradiction detection, interval-as-design-site, RSI-class objective stability, runtime-compliance evidence). None of these is solved by substrate primitives alone.
3. **Spec-malleability (UC4) is a methodology constraint, not a substrate one.** UC4's "architecture moves during spec refinement" is the *cycle* being non-monotonic. A substrate-first design treats malleability as a storage problem (versioning); a methodology-first design treats it as a *promotion problem* (when do we let intent freeze; when do we let the spec move; what acceptance-region pins the work-unit; F39).
4. **The failure surface that bites greenfield is methodology-shaped.** Greenfield-critical F-modes in [`failure-modes-v3.md`](../failure-modes-v3.md) — F1, F2, F3, F9, F15, F25, F27, F28, F36, F37, F39, F40, F41, F55 — are overwhelmingly *cycle-shape* failures, not substrate failures. F52 (Tempting-Wrong-Hybrid, [`failure-modes-v3.md`](../failure-modes-v3.md) §5a / [`research/28-schillace-sunday-letters.md`](../../../research/28-schillace-sunday-letters.md) §6 Letter 11) is the explicit warning against the substrate-first reflex.

### §0.3 Pre-respond to the strongest critique

The Phase-3 adversarial likely attacks on three fronts; each is pre-answered.

**Critique A: "You're inheriting the worst of waterfall — you put process first, you'll re-create the phase-gated architecture report 28's Letter 11 names as the Tempting-Wrong-Hybrid (F52), and you'll trip F59 (premature decomposition)."**

Response. Methodology-first ≠ waterfall-first. The cycle in §1 is *short* (single work-unit, one acceptance-region, one judged increment), *non-monotonic* (intent freezes; spec is malleable downstream; decomposition is revisable inside the cycle per the `redecompose` action), and *recursive* (the cycle's own outputs feed back into the regime classifier). What the cycle freezes is the **typed intent block's `invariants` field** (per MISSED-3, El Kaim Ch 3 §4.1 [`research/14-el-kaim-book-intent-and-spec-authorship.md`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)), not the spec, not the architecture, not the decomposition. This is the structural reconciliation of UC4 with MISSED-3 the brief flags. F59 is mitigated by making decomposition *revisable* mid-cycle, not by removing decomposition (Overstory STEELMAN risk 5/11 per [`failure-modes-v3.md`](../failure-modes-v3.md) §5a F59).

**Critique B: "You're underspecifying substrate — methodology-first defers the real engineering. Round-2 §8 turned this project from 'design a methodology' into 'configure a methodology on top of an existing substrate' (CTR-C2). You're regressing."**

Response. Substrate isn't underspecified; it's **derived** in §1.4. The cycle in §1 *forces into existence* a specific minimum set: typed-intent store with `invariants` immutability, EARS-validated spec store, scenario holdout with substrate-enforced isolation (D-4), trajectory capture (D-7), tiered watchdog (D-6), cost ceiling (D-5), regime classifier as a substrate component (not operator discipline; this is the F53 mitigation), promotion enforcer (substrate refuses to discard cycle outputs without classification), and a cross-model judge router (sized to F1/F27/F46 not F1 alone; addresses WEAK-5 third position). The substrate-first tracks may surface more primitives; this track *enumerates the minimum the cycle requires*, no more. Round-2's framing is a corpus claim worth challenging — the brief explicitly relaxes its defaults to challengeable (D3).

**Critique C: "The spec-malleable phase doesn't have a stable methodology to inherit. You're attempting to apply RE/SE discipline (reports 25/26) to a regime UC4 explicitly says is in flux."**

Response. This is precisely the MISSED-3 finding the bias-guard surfaced. The track's answer: **split the artifact stack into intent (stable) + spec (malleable) + code (regenerable)**. RE/SE discipline applies to the intent layer (where INCOSE GtWR C1-C15 / EARS / Complexity Primer have 30+ year history per [`research/25-requirements-engineering-foundations.md`](../../../research/25-requirements-engineering-foundations.md) §2-5). The spec layer is the malleable one (UC4); RE/SE discipline is applied as *lint* (R7/R8/R9 vocabulary, [`research/25-requirements-engineering-foundations.md`](../../../research/25-requirements-engineering-foundations.md) §3.4 mapping; F38) — a deterministic gate, not a freeze. Brier's pace-layers ([`research/followup/12-brier-pace-layers.md`](../../../research/followup/12-brier-pace-layers.md)) and Nystrom's spec-git-history-as-changelog ([`research/35-lenny-howiai-spec-driven-and-team-ops.md`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)) are *both* compatible with this split: Brier predicts intent-stability (we agree); Nystrom predicts spec-velocity (we agree). CTR-B7 dissolves under the intent/spec split.

---

## §1 Architecture sketch — the methodology in detail

### §1.1 Cycle shape

The work-unit is a **single regime-classified, intent-anchored, spec-bounded, judge-gated, promotion-closed cycle**. One cycle delivers one increment. Cycles do not chain agents in sustained dialogue (F26 mitigation); they hand off through durable artifacts (intent block, spec block, scenario, decision record).

```
[1] REGIME GATE        → classify(work-unit) → {L3-augmented | L4-lights-out | escalate}
[2] INTENT FREEZE      → typed intent block with non-negotiable invariants checked in (Git)
[3] SPEC DRAFT         → EARS-mandated Layer-3 acceptance criteria; R7/R8/R9 lint must pass
[4] DECOMP             → soft commit; cycle may `redecompose` if implementation discovers shape (F59)
[5] BUILD              → builder agent(s); scenario acceptance withheld (D-4 substrate-enforced)
[6] JUDGE              → cross-model panel (F1/F27/F46/F48 mitigation per WEAK-5 third position)
                          + deterministic perimeter (F33/F51 mitigation per Ashby framing)
[7] HOLDOUT            → scenario suite run on shipped artifact, not on builder context (F28)
[8] PROMOTION          → substrate-enforced classification of cycle outputs:
                          insight | playbook | correction | pattern | intent-invariant | scenario | dead
                          (typed per followup/11 Compound Knowledge; "dead" is explicit, not silent)
[9] DRIFT CHECK        → pace-layer audit against ARCHITECTURE.md invariants (F34, Brier followup/12)
```

Steps 2 (intent freeze) and 8 (promotion) are **structural** — the substrate refuses to advance without them. This is the F53 mitigation: no voluntary-discipline step in the inner loop. Steps 4 (decomp) and 5/6 (build/judge) are revisable inside the cycle (F59 mitigation).

### §1.2 Work-unit sizing (F36/F39-anchored)

Per F36 ([`failure-modes-v3.md`](../failure-modes-v3.md) §4; Yang et al. [`research/26-prompt-underspecification-academic.md`](../../../research/26-prompt-underspecification-academic.md)) the empirical model-capability ceiling is ~10-20 simultaneously-specified requirements before quality collapses (gpt-4o 98.7%→85.0% as specs grow 1→19). The methodology fixes the work-unit at **≤7 EARS-form requirements per cycle**, with hard substrate enforcement at 12. This is the most expensive single methodology decision in the track because it bounds per-cycle throughput — but unbounded work-units sink F36 and F37 (Larbi silent contradictory-prompt collapse, 73.8%→6.7%). Per F39 ([`failure-modes-v3.md`](../failure-modes-v3.md) §4) every work-unit declares whether the acceptance criterion is a **point spec** (closed-form, ≤7 EARS clauses) or an **acceptance region** (Complexity Primer principle 12, [`research/25-requirements-engineering-foundations.md`](../../../research/25-requirements-engineering-foundations.md) §5). Region-shape work-units are routed to a different judge panel that scores acceptable variance, not point-correctness. The shape-choice itself is a regime-gate output; the operator does not pick per-cycle.

### §1.3 Knowledge accumulation and dreaming

The promotion step (step 8) is the inverse of F10 ([`failure-modes-v3.md`](../failure-modes-v3.md) §1, "findings disappear into chat"). Cycle outputs are typed per followup/11 Compound Knowledge ([`research/followup/11-compound-knowledge.md`](../../../research/followup/11-compound-knowledge.md)): `insight | playbook | correction | pattern`. The track adds two greenfield-specific types: `intent-invariant` (a promoted invariant pulled into the typed intent block, which then becomes immutable for future cycles) and `scenario` (a promoted holdout scenario added to the substrate-held scenario set, never visible to future builders per D-4).

Knowledge accumulation has two failure surfaces. F8 (stale-knowledge inversion) and F55 (behavioural drift / self-reference loop). The mitigation chain:
- **Confidence-checked at write** ([`research/followup/11-compound-knowledge.md`](../../../research/followup/11-compound-knowledge.md), `kw:confidence` first-class skill); knowledge enters with stated confidence and a re-verify cadence.
- **Pace-layered** ([`research/followup/12-brier-pace-layers.md`](../../../research/followup/12-brier-pace-layers.md)) — `pattern`s sift down toward `standard` only after N cycles of consistent use; this is the structural rate-limit on the self-reference loop F55 names.
- **Grounded-against-human-data periodically** — every M cycles the regime gate forces a `cold-recheck` run that bypasses the accumulated knowledge store and re-derives from intent+spec alone. Discrepancies are F55 signals.

Dreaming ([`research/32-shapiro-completion-chat-agent-claw.md`](../../../research/32-shapiro-completion-chat-agent-claw.md), Jesse Vincent's overnight research Claw exemplar) is permitted as an **off-cycle** activity targeting the knowledge store, not the inner loop. The MISSED-5 contradiction (Anthropic Skills no-network vs Claw dreaming) is dissolved by scope: dreaming runs in a separate harness with network access; in-cycle skill discovery runs in the Anthropic Skills sandbox. Two surfaces, not one.

### §1.4 Substrate primitives derived from the cycle (minimum set)

The cycle in §1.1 forces into existence the following primitives. This is **not a substrate-first enumeration**; it is the smallest set the cycle cannot run without. Substrate-first tracks should be the place richer enumeration happens.

| # | Primitive | Forced by which cycle step | Failure-mode the primitive closes |
|---|---|---|---|
| 1 | **Typed intent store with immutability on `invariants`** | Step 2 | MISSED-3 (UC4 vs El Kaim); F41 |
| 2 | **EARS-validated spec store + R7/R8/R9 lint** | Step 3 | F18, F38 |
| 3 | **Substrate-enforced acceptance-region shape declaration** | Steps 1, 4, 7 | F39, F51 |
| 4 | **Scenarios in holdout with substrate-enforced builder isolation** | Steps 5, 7 | D-4; F28 |
| 5 | **Trajectory capture + replay (D-7 / OpenHands-class)** | Steps 6, 8, 9 | F10, F16, F22 |
| 6 | **Tiered watchdog (Daemon/Triage/Patrol — D-6 / C14)** | Steps 5, 6 | F22, F23 |
| 7 | **Hard cost ceiling (D-5 / C15)** | All steps | F47 surface, CTR-E1 |
| 8 | **Regime-classifier substrate component** | Step 1 | F53 (voluntary-discipline mitigation); F57 |
| 9 | **Promotion enforcer (substrate refuses cycle close without classification)** | Step 8 | F10, F55, F53 |
| 10 | **Cross-model judge router (not single-router; per WEAK-5 three positions)** | Step 6 | F1, F27, F46, F48 |
| 11 | **Deterministic perimeter on tools (CaMeL-class, accepted with ~7pt utility tax per MISSED-9)** | Step 5 | F12, F33, F44, F51 |
| 12 | **Pace-layer drift detector against ARCHITECTURE.md** | Step 9 | F34, F35, F57 |
| 13 | **Off-cycle dreaming harness (separate sandbox; network-permitted; no in-cycle write)** | Knowledge accumulation | MISSED-5 reconciliation |

The track is **silent on**: choice of substrate stack (OpenHands+Overstory vs Gas City — CTR-C5); coordination medium (mail bus vs GitHub issues — CTR-C7); language choice (F45 / [`research/33-language-choice-as-harness.md`](../../../research/33-language-choice-as-harness.md)); per-provider routing details (CTR-C4). Those are substrate-first decisions.

### §1.5 Error handling and regime classification

The regime gate (step 1) classifies each work-unit. The classification is **not operator-discretionary** — it is computed from work-unit shape (number of EARS clauses, region-vs-point shape per F39, declared invariant count, judge-confidence on similar prior cycles, drift signals from step 9 last cycle). This addresses F57 (design-authority erosion — convenience reclassifies stakes): reclassification requires an explicit policy change with audit trail, not an operator's per-cycle convenience.

Three regime outcomes:

- **L3-augmented.** Human in the inner loop per cycle. Used for: first N cycles of any new intent invariant set; any work-unit with declared `acceptance-region` shape; any cycle following a step-9 drift alert.
- **L4-lights-out with sample audit.** No human in inner loop; trajectory + judge output + promotion record go to a sampled-audit queue. Used for: well-characterized intent invariant sets with ≥M consecutive clean cycles, point-spec shape, sub-threshold drift.
- **escalate.** Routed to human spec-author and not run. Used for: contradiction detected in intent invariants (F37 mitigation, structural); declared region-shape with no acceptance-region tooling available; pace-layer alert from prior cycle.

This is the brief §2.1 option (c)+(b) combination — declare a regime classification scheme that names where the factory operates at L4 vs L5 and which work units flow to which. **The track does not claim L5 anywhere.** Lights-out = L4-with-sample-audit per glossary §0. Jaymin's K=5 / paraphrase-robustness thresholds ([`research/09-jaymin-book-harnesses-practices-mental-models.md`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5) parameterize the classifier; OQ-B6 is engaged but not resolved here (the corpus' bars are one input among several — see WEAK-1 instability flag).

### §1.6 How knowledge accumulates without re-creating waterfall

The trajectory from day 0 to day N (the question §5 requires answering) is methodology-driven, not waterfall-driven:

- Day 0-N: every work-unit runs L3-augmented; intent invariants are *discovered* in human-augmented cycles and promoted to immutable status (step 8) when the human commits to them. The spec layer churns (Nystrom's spec-git-history-as-changelog); the intent layer accumulates slowly (Brier pace-layer 3+).
- Day N-2N: the regime gate begins routing well-characterized intent sets to L4-lights-out. Sample-audit results re-tune the classifier.
- Day 2N+: steady-state. L3-augmented becomes the exception (new intent, region-shape work, drift-flagged cycles); L4-lights-out is the default for everything else.

Waterfall would lock the spec at day N. This methodology locks only the *intent invariants* (and only by promotion, not by phase gate); the spec moves throughout.

---

## §2 Load-bearing concerns

### §2.1 OQ-B1 (lights-out / L5 / regime tension)

Addressed at §1.5. Stance: brief §2.1 option (c) + (b). Lights-out maps to **L4-with-sample-audit per work-unit-class**, not to L5. The vocabulary mapping test (CTR-A4) is resolved by definitional alignment: this track's "lights-out" = no human in the per-cycle inner loop for L4-classified work-units, with humans setting policy (intent invariants), sample-auditing post-hoc, intervening on watchdog escalation, and re-entering on declared trigger conditions (regime-gate `escalate`). This is the brief §0 glossary definition; the track does not redefine it.

The Jaymin Ch 9 §7 anti-pattern claim ([`research/09-jaymin-book-harnesses-practices-mental-models.md`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §2c; CTR-A1) is not engaged as decisive *against* lights-out because (a) the corpus citations (CodeRabbit 1.4×, Veracode 45%, METR 19%) are scope-caveated in brief §2.1 footnotes (CTR-E3); (b) WEAK-1 surfaces Jaymin's *internal* contradiction (anti-L5 alongside "this time it works"); (c) this track does not claim L5. OQ-B6 (which bar set) is engaged but not resolved here — the regime classifier is parameterized on Jaymin's thresholds *and* on per-architecture sample-audit results, with explicit auditable thresholds per work-unit-class.

### §2.2 UC4 spec-malleable hypothesis

Engaged at §0.3 critique C and §1.4 primitive 1. The track **partly accepts and partly reframes** UC4. Accept: the spec layer is malleable, per UC4 (and per Nystrom's spec-git-history-as-changelog, [`research/35-lenny-howiai-spec-driven-and-team-ops.md`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)). Reframe: the intent layer is *not* malleable; per MISSED-3 / El Kaim Ch 3 §4.1, intent invariants are non-negotiable and substrate-enforced (primitive 1). This is the track's first-class engagement with the MISSED-3 finding the bias-guard surfaced as "at minimum on par with CTR-A4 as a v3-foundational tension." If UC4 is read maximally (everything malleable, including intent), the track challenges UC4 with corpus evidence (D3). If UC4 is read narrowly (the spec moves; intent freezes at promotion), the track is fully compatible.

### §2.3 Cold-start summary

See §5 below for the dedicated treatment. Short form: day 0 starts in L3-augmented for all work-units; the human authors typed intent blocks per [`research/14-el-kaim-book-intent-and-spec-authorship.md`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) + EARS specs per [`research/25-requirements-engineering-foundations.md`](../../../research/25-requirements-engineering-foundations.md); the regime classifier is bootstrapped on Jaymin-style K=5 + cross-model-judge measurements from the first M cycles; promotion of any `pattern` to `standard` is forbidden in the first N cycles (anti-F55 hard rate-limit).

### §2.4 Other OQ-B2..B10

- **OQ-B2** (where greenfield/brownfield boundary falls). Lead-agent question; track stance: the boundary falls at *methodology*, not substrate. The substrate primitives in §1.4 are mostly substrate-shareable with a brownfield track; the cycle shape (especially intent-freeze + EARS spec + region-shape declaration + promotion-as-typed-classification) is greenfield-specific. Brownfield's natural cycle (issue from queue, [`research/03-every-compound-engineering.md`](../../../research/03-every-compound-engineering.md) per CHALLENGE-6) doesn't need most of these.
- **OQ-B3** (human re-entry). The regime gate `escalate` outcome + watchdog Patrol escalations + sampled-audit findings are the three re-entry conditions. Substrate protocol: trajectory + intent + spec + judge output go to a human queue; human re-enters by editing the typed intent block (which forces re-promotion).
- **OQ-B4** (brownfield only).
- **OQ-B5** (now §5).
- **OQ-B6** (which empirical bars). Engaged §1.5, §2.1. Jaymin's bars used as parameters, not as universal gates; per-work-unit-class thresholds; WEAK-1 instability flagged.
- **OQ-B7** (organizing axes beyond mandate). The regime axis is load-bearing here (lights-out is per work-unit-class, not architecture-global). Stakes axis is engaged through F57 (design-authority erosion). Synchronicity is not engaged here.
- **OQ-B8** (provider-property requirements). Substrate-deferred. The track requires a *cross-model judge router* (primitive 10) — this implies provider diversity for the judge population (per WEAK-5 three positions) but does not require RouterLLM-shaped abstraction (CTR-C4 unresolved here).
- **OQ-B9** (methodology evolution). The track's pace-layer drift detector (primitive 12) and promotion enforcer (primitive 9) implement methodology evolution as substrate-supported but methodology-driven. Patterns sift to standards over N cycles; the cycle shape itself is revisable through the ADR mechanism, not auto-evolved.
- **OQ-B10** (process discipline).

### §2.5 Bias-guard load-bearing engagements

- **MISSED-3** (El Kaim intent vs UC4): central to §1.4 primitive 1 and §2.2.
- **WEAK-2** (CTR-C6 bitter-lesson vs scaffold-substrate): the track sits on the *scaffold-substrate* side (EARS specs, typed intent, promoted skills, ARCHITECTURE.md drift detection). This is a defensible position per [`research/23-anthropic-engineering-trilogy.md`](../../../research/23-anthropic-engineering-trilogy.md) (Anthropic Skills), [`research/35-lenny-howiai-spec-driven-and-team-ops.md`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md) (Nystrom Markdown specs), [`research/14-el-kaim-book-intent-and-spec-authorship.md`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) (Codex). The bitter-lesson camp (Jaymin Manifesto Rule 2, Gas City [`research/38-gas-systems-substrate.md`](../../../research/38-gas-systems-substrate.md)) is a coherent corpus position; this track diverges from it explicitly because the §1.4 primitives 1-3 *are* scaffold-substrate. The bitter-lesson critique applies to the spec and intent layers; the track's defense is that LLM-authored specs without EARS/GtWR lint trip F18/F36/F37/F38 at measured rates.
- **WEAK-5** (F1 mitigation third position — Anthropic same-model-different-role): incorporated in primitive 10 (cross-model judge router is *one* mitigation; same-model-different-role specialist critics in the panel is *another*; the track uses both).
- **MISSED-9** (CaMeL ~7-point utility tax): accepted in primitive 11 — the track explicitly buys the safety primitive at its measured cost.
- **CANDIDATE-2 / F53 voluntary-discipline fragility**: the cycle has *zero* steps that depend on operator voluntary discipline in the inner loop (regime gate is computed; intent freeze is substrate-enforced; EARS lint is deterministic; judge panel is substrate-routed; promotion is substrate-required; pace-layer drift is substrate-detected). Operator discipline is required only at *escalate* and at *promotion classification editing* — both out-of-cycle.

---

## §3 Citations and grounding

Every load-bearing claim in §1-§2 cites a corpus anchor. Anchor table:

| Claim | Anchor |
|---|---|
| Intent invariants are non-negotiable upstream | [`research/14-el-kaim-book-intent-and-spec-authorship.md`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) Ch 3 §4.1; MISSED-3 |
| Spec is malleable, version-controlled, durable | UC4 + [`research/35-lenny-howiai-spec-driven-and-team-ops.md`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md) (Nystrom); D-1 |
| EARS for Layer-3 acceptance criteria | [`research/25-requirements-engineering-foundations.md`](../../../research/25-requirements-engineering-foundations.md) §2 |
| GtWR R7/R8/R9 lint as deterministic gate | [`research/25-requirements-engineering-foundations.md`](../../../research/25-requirements-engineering-foundations.md) §3.4; F38 |
| ≤7 requirements per cycle (12 hard cap) | [`failure-modes-v3.md`](../failure-modes-v3.md) F36 (Yang et al.) |
| Acceptance-region vs point-spec shape declaration | [`research/25-requirements-engineering-foundations.md`](../../../research/25-requirements-engineering-foundations.md) §5 (Complexity Primer p12); F39 |
| Silent contradictory-prompt detection at intent layer | [`failure-modes-v3.md`](../failure-modes-v3.md) F37 (Larbi et al.) |
| Cross-model + same-model-different-role judge panel | [`research/34-lenny-howiai-personal-harnesses.md`](../../../research/34-lenny-howiai-personal-harnesses.md) F46; [`research/23-anthropic-engineering-trilogy.md`](../../../research/23-anthropic-engineering-trilogy.md) Auto-Review; WEAK-5 |
| Deterministic perimeter (CaMeL) with utility tax accepted | [`research/followup/08-security-primitives.md`](../../../research/followup/08-security-primitives.md) §3; MISSED-9 |
| Scenarios held out, substrate-enforced | D-4; [`research/01-strongdm-factory.md`](../../../research/01-strongdm-factory.md); F28 |
| Trajectory capture cheap & production-tested | D-7; [`research/11-openhands-substrate-audit.md`](../../../research/11-openhands-substrate-audit.md) |
| Tiered watchdog | D-6 / C14 |
| Cost ceiling | D-5 / C15 |
| Promotion as substrate-required typed classification | [`research/followup/11-compound-knowledge.md`](../../../research/followup/11-compound-knowledge.md) (insight/playbook/correction/pattern); F10 mitigation |
| Pace-layer drift detection against ARCHITECTURE.md | [`research/followup/12-brier-pace-layers.md`](../../../research/followup/12-brier-pace-layers.md); F34 |
| Regime classification per work-unit-class (not global) | Brief §2.1 option (c); D2; [`research/09-jaymin-book-harnesses-practices-mental-models.md`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5 |
| Dreaming as off-cycle harness | [`research/32-shapiro-completion-chat-agent-claw.md`](../../../research/32-shapiro-completion-chat-agent-claw.md); MISSED-5 reconciliation |
| Cycle hands off through artifacts (no sustained dialogue) | F26; [`research/09-jaymin-book-harnesses-practices-mental-models.md`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) Manifesto Rule 5 |
| Decomposition revisable inside cycle | F59 ([`research/10-overstory-substrate-audit.md`](../../../research/10-overstory-substrate-audit.md) STEELMAN risk 5/11) |
| Voluntary-discipline avoidance throughout cycle | F53 / CANDIDATE-2 ([`research/30-cognitive-escrow.md`](../../../research/30-cognitive-escrow.md)) |
| Pattern→standard rate-limit anti-self-reference | F55 ([`research/31-caremark-rsi-board-exposure.md`](../../../research/31-caremark-rsi-board-exposure.md)) |
| Tempting-Wrong-Hybrid warning shapes substrate-derivation discipline | F52 ([`research/28-schillace-sunday-letters.md`](../../../research/28-schillace-sunday-letters.md) Letter 11) |

**Most-cited corpus anchors in this track:** report 25 (EARS / GtWR / Complexity Primer — RE/SE bootstrapping); report 14 (El Kaim typed intent); F36/F37/F38/F39 (Yang/Larbi/vocab-lint/point-spec — the four greenfield-critical methodology F-modes); F53 (voluntary-discipline fragility — the structural-controls mandate).

---

## §4 Defaults: accepted vs challenged

All 7 marked per D3.

- **D-1 (Specs are the durable, version-controlled, human-curated artifact).** `accepted with refinement` — the track splits the durable artifact into **intent (immutable invariants) + spec (malleable, version-controlled per Nystrom)**. Both are durable; both are version-controlled; intent is human-curated upstream and substrate-frozen on promotion; spec is malleable downstream of intent. This is the methodology-most-relevant default and the track engages it deeply per MISSED-3. Justification: UC4 + Nystrom give the malleable side; El Kaim Ch 3 §4.1 gives the immutable side; their reconciliation is the layer split.

- **D-2 (Scenarios live outside the codebase as a holdout set).** `accepted with justification` — greenfield has no codebase to inherit scenarios from at day 0 (this is the cold-start problem). Scenarios live in substrate-enforced holdout (primitive 4) and are promoted from cycle outputs at step 8. WEAK-3 sharpening (StrongDM's own primary pages permit incident-replays / agentic-simulation inside the runtime) doesn't apply to greenfield at day 0 because there is no runtime to capture from. After day N the runtime begins to produce scenarios; they still live in substrate-enforced holdout.

- **D-3 (Agent = Model + Harness).** `accepted with caveat` — the cycle uses agents in this decomposition for steps 5 (build) and 6 (judge). Caveat: MISSED-8 / CTR-C10 (report 37 Portuguese-vs-English language effect on policy) implies "Agent = Model + Harness + Natural-Language-Register"; the track flags this as an open vocabulary question (§7) but does not redesign the cycle around it. Population/graph-node architectures (the fragility flag) are not used here — the cycle is queue-of-cycles, not population-of-agents.

- **D-4 (Holdout discipline is substrate-enforced).** `accepted with justification` — primitive 4. F28 is critical for greenfield; the only ground-truth signal in greenfield comes from holdout, so substrate-enforcement is non-negotiable.

- **D-5 (Hard cost ceilings non-optional in CI).** `accepted with justification` — primitive 7. F47 (Goodhart-on-tokens) is a separate concern; cost ceiling is a per-cycle bound, not an operator-leaderboard metric.

- **D-6 (Tiered watchdog Daemon/Triage/Patrol substrate primitive).** `accepted with justification` — primitive 6. F22 (zombie agents) and F23 (stalled-vs-thinking) are directly mitigated. Patrol escalations feed the regime gate (§1.5).

- **D-7 (Trajectory capture cheap and production-tested).** `accepted with justification` — primitive 5. The track relies on trajectory capture for steps 6, 8, 9 and for sample-auditing of L4 cycles.

---

## §5 Cold-start (MANDATORY)

The greenfield cold-start problem (brief §5): how does the factory bootstrap on day 0 with no scenarios, no issue queue, no `docs/solutions/`, no prior runs? Below uses the required reading (reports 25, 26, 30, 31, followup/10 — per brief §5.1).

### §5.1 Day-0 state and priors

Day 0 inputs (the priors greenfield is permitted, per brief §0 redefinition):

- **Operator-authored typed intent blocks** for the initial work-units. Authored per [`research/14-el-kaim-book-intent-and-spec-authorship.md`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) Ch 3 §4.1 9-field schema; `invariants` field is the one that becomes immutable on promotion.
- **EARS-validated initial spec(s)** for the first work-unit. Per [`research/25-requirements-engineering-foundations.md`](../../../research/25-requirements-engineering-foundations.md) §2. Authored by operator; lint-passed deterministically.
- **Adjacent-domain skills and library docs.** Standard scaffold-side priors (Anthropic Skills, Every SKILL.md, [`research/04-every-skill-libraries.md`](../../../research/04-every-skill-libraries.md)). The bitter-lesson camp would reject these; the track per WEAK-2 accepts them as scaffold-substrate.
- **Operator-curated knowledge from other factory runs.** Per UC1 / brief §0 — explicitly permitted as priors. The cold-start factory inherits typed knowledge from prior factories, if any; if not (truly cold), it operates only on intent + spec + skills.
- **A regime classifier seeded with Jaymin K=5 / paraphrase-robustness defaults** ([`research/09-jaymin-book-harnesses-practices-mental-models.md`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5). These thresholds are *initial parameters*, not load-bearing bars; per WEAK-1 instability they will be re-tuned from the first M cycles.

### §5.2 What day-0 lacks (and how the methodology covers)

- **No scenarios.** Day-0 has no holdout set. Mitigation: every day-0 work-unit runs L3-augmented (human in inner loop), and step 8 promotion includes *scenario authoring as a first-class output type*. By day N every shipped increment has produced ≥1 substrate-held scenario. Scenarios are added to holdout, never visible to builders (D-4).
- **No track record for the regime classifier.** Mitigation: regime gate forces all work-units to L3-augmented for the first N cycles. After N cycles with stable judge-confidence, the classifier begins routing point-spec work-units with characterized intent to L4-lights-out. The transition is *gradual and per-work-unit-class*, not a phase flip.
- **No `docs/solutions/` accumulated.** Mitigation: knowledge accumulation starts at cycle 1, typed per followup/11. Pattern → standard sift is forbidden in the first N cycles (anti-F55 hard rate-limit; see §1.3).
- **No baseline against which to detect drift.** Mitigation: ARCHITECTURE.md ([`research/followup/12-brier-pace-layers.md`](../../../research/followup/12-brier-pace-layers.md)) is authored at day 0 by the operator as part of the seed intent block. Drift detection at step 9 measures against this seed; the *baseline itself* is human-authored, not factory-generated (this is the anti-F55 anchor).
- **No prior cost data for ceilings.** Mitigation: cost ceilings start at operator-defined conservative values; cycle telemetry re-calibrates them after M cycles.

### §5.3 Required-reading anchors specific to cold-start

- **Report 25** ([`research/25-requirements-engineering-foundations.md`](../../../research/25-requirements-engineering-foundations.md)). Cold-start uses EARS for the first specs and GtWR for the first lint pass. The Complexity Primer (§5) is used by the operator to declare initial work-unit shapes (point vs region). AFIS strategy-3 (per [`research/35-lenny-howiai-spec-driven-and-team-ops.md`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md) update note) is the destination state — Markdown specs in `agent specs/` subfolder; spec git-history is the changelog after day N.
- **Report 26** ([`research/26-prompt-underspecification-academic.md`](../../../research/26-prompt-underspecification-academic.md)). Yang et al. and Larbi et al. give the empirical model-capability ceilings the cold-start cycle must respect from day 0. ≤7 EARS clauses per cycle (F36). Substrate-side contradiction detection (F37) starts deterministic, escalates to LLM-judge only with cross-model panel (MCC ≤0.55 alone is insufficient).
- **Report 30** ([`research/30-cognitive-escrow.md`](../../../research/30-cognitive-escrow.md)). The Day-0 L3-augmented cycle is the high-cognitive-load regime; cognitive-escrow design (F42) at the operator side is load-bearing. The methodology requires the operator-side harness to surface re-engagement prompts between cycles (Attention Firewall, [`research/28-schillace-sunday-letters.md`](../../../research/28-schillace-sunday-letters.md) §"Surprises") — this is **not** a voluntary-discipline ask (avoids F53); it is a substrate-side prompt the harness emits.
- **Report 31** ([`research/31-caremark-rsi-board-exposure.md`](../../../research/31-caremark-rsi-board-exposure.md)). At day 0 the factory declares its RSI class explicitly (F43 mitigation). The three RSI failure modes (F54 goal subversion, F55 behavioural drift, behavioural-drift-via-intent-modification) are surfaced at day 0 as named risks the cold-start regime classifier hedges against (no L4 routing in first N cycles; pattern→standard rate-limit; ARCHITECTURE.md as human-authored anchor).
- **Followup 10** ([`research/followup/10-governance.md`](../../../research/followup/10-governance.md)). AILCCP controls (Human Approval Gate, sandboxing, immutable logging) map to cycle steps 1 (regime gate), 5/11 (deterministic perimeter), 5 (trajectory capture). Replit DB wipe (F56 / G14) is the canonical reason the cold-start factory does **not** get production-scissors anywhere near the cycle until well past day N. The runtime/design-time compliance split (F58 / G9) is acknowledged but not load-bearing for a greenfield application not yet inside a regulated perimeter.

### §5.4 Trajectory from day 0 to day N (steady-state transition)

| Phase | Cycle count | Regime | Knowledge state | Drift baseline |
|---|---|---|---|---|
| Bootstrap | 0–N₁ | All L3-augmented | Empty → first cycles' insights at step 8; no pattern→standard sift | Human-authored ARCHITECTURE.md only |
| Maturation | N₁–N₂ | L3 default; L4 for well-characterized point-spec work-units only | Pattern→standard sift permitted with confidence-check gate | ARCHITECTURE.md + first standards |
| Steady-state | N₂+ | L4 default; L3 for new intent, region-shape, drift-flagged | Full Compound-Knowledge typed accumulation; periodic `cold-recheck` | Full pace-layer stack |

N₁ and N₂ are not fixed — they are reached when **measurable per-work-unit-class criteria** are met: cycle count, K=5 consistency at substrate-measured thresholds, prompt-paraphrase robustness, zero medium-or-high safety incidents in the trajectory (per [`research/09-jaymin-book-harnesses-practices-mental-models.md`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5 Automation Mode bars, parameterized not fixed per WEAK-1).

### §5.5 Anti-silent-failure mechanisms specific to cold-start

The cold-start factory has no track record to evaluate it against. Specific protections:

- **Daily `cold-recheck` cycle** in the bootstrap phase: a random work-unit from yesterday's queue re-runs from scratch, ignoring the accumulated knowledge store, and the output is compared. Divergence is F55 / F8 signal.
- **Human spec author re-authors a seed intent block monthly** for the first N₂ cycles. Re-authored intent is compared to the substrate-stored intent; drift between them is F54 / goal-subversion signal.
- **All promotions in the bootstrap phase are operator-confirmed**, not auto-classified. Substrate refuses to advance step 8 without operator classification. This *is* a voluntary-discipline step, but it is at *cycle close*, not the inner loop, and is the cold-start trade-off (F53 mitigation is structural for the inner loop; promotion classification is operator-confirmed because the classifier has no track record yet).
- **No L4 routing until N₁** cycles of clean L3 with the specific intent set.

---

## §6 What this track is NOT

- **Not a substrate enumeration.** §1.4 lists the minimum primitives the cycle forces. Substrate-first tracks should surface CTR-C5 (substrate stack choice), CTR-C7 (coordination medium), CTR-C4 (provider abstraction), F45 (language choice). This track is silent on all four.
- **Not a cold-start architecture.** §5 covers cold-start because the brief makes it mandatory; the cold-start-first track is the place for deeper treatment of the Stanford CodeX / AILCCP governance literature and the bootstrap-vs-priors design space.
- **Not a brownfield-applicable design.** The cycle assumes no codebase, no issue queue at day 0; brownfield's natural cycle ([`research/03-every-compound-engineering.md`](../../../research/03-every-compound-engineering.md) per CHALLENGE-6) is different in kind. Substrate primitives 1-13 are mostly shareable; the cycle shape isn't.
- **Not a comprehensive engagement with every corpus contradiction.** The track engages the contradictions load-bearing for methodology-first: MISSED-3 (deeply); CTR-C2 (substrate-heavy vs methodology-dominates — track sides with methodology-dominates for greenfield); CTR-A4 + CTR-A1 (regime tension — track resolves at L4-with-sample-audit per work-unit-class); CTR-B2/B3/B7 (spec velocity / spec-stack ordering — track resolves with intent/spec split); CTR-C6 / WEAK-2 (scaffold-substrate — track sides with scaffold-substrate camp explicitly). Other contradictions are noted, not resolved.
- **Not a Phase-4 substrate boundary call.** OQ-B2 is engaged at §2.4 but not resolved.
- **Not an L5 design.** The track explicitly does not claim L5 anywhere; lights-out = L4-with-sample-audit per glossary §0.
- **Not committed on F45 (language-as-harness).** Substrate-first concern.

---

## §7 Open questions surfaced

1. **Q-MF1 — How fast can intent invariants safely accumulate?** The promotion-to-immutable step is the structural F55 mitigation, but premature invariant freezing recreates the waterfall trap critique A pre-responds to. The track says "human-confirmed in bootstrap phase," but the post-bootstrap rate is unspecified. *Action:* corpus-grounded study of intent-invariant churn rates in Notion (Nystrom) and El Kaim Codex; if no anchor, defer to lean-eval (Phase 8).
2. **Q-MF2 — Does the ≤7 EARS-clauses bound generalize beyond Yang et al.'s benchmark population?** F36 is anchored on gpt-4o + Llama-3.3-70B; the empirical bar may shift on newer models. The bound is load-bearing for cycle throughput. *Action:* lean-eval measurement on the target model set.
3. **Q-MF3 — How does the cycle handle work-units that genuinely span multiple intent-invariant sets?** §1.2 requires per-cycle alignment with one intent set; cross-set work-units are not addressed. *Action:* per-architecture decomposition discipline; possibly a "joint-invariant" type added to the intent schema.
4. **Q-MF4 — Is the operator-side cognitive-escrow harness itself voluntary-discipline?** §1.6 / §5.3 claims the Attention Firewall harness emits substrate-side prompts to avoid F53, but the operator can still ignore them. The track may be smuggling voluntary-discipline at the operator-input edge. *Action:* Phase-3 adversarial check; if confirmed, the cycle's L3-augmented mode needs a stricter operator-engagement model.
5. **Q-MF5 — How is the regime classifier itself audited?** Primitive 8 (regime-classifier substrate component) closes F53 by removing operator discretion, but the classifier's own quality is unaudited. A bad classifier silently misroutes work-units to L4 that should be L3. *Action:* the cold-recheck cycle (§5.5) catches some of this; the rest is OQ-B6 (which bars) + OQ-B9 (methodology evolution).
6. **Q-MF6 — Does the intent/spec split survive UC4 read maximally?** §2.2 acknowledges that if UC4 is read to include intent malleability, the track challenges UC4. Lead-agent / user clarification of UC4's scope would resolve this. *Action:* surface as DECISIONS-PENDING in Phase 3.
7. **Q-MF7 — Where does the natural-language-register axis (CTR-C10 / MISSED-8) fit?** D-3 caveat in §4 flags this; report 37's empirical finding implies the agent vocabulary is incomplete. The track does not redesign around it. *Action:* substrate-first tracks engagement; this track will inherit whatever vocabulary they settle on.

---

*End of greenfield-methodology-first.md.*
