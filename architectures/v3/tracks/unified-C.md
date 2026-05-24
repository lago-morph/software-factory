---
track: unified-no-axis-C
axis: distance-from-frozen-anchor (a graph-distance axis: every work unit is parameterised by how far its proposed change is from a load-bearing immutable anchor)
mandate-scope: unified
based-on-commit: 96a949430b5c356f8b4e688b1d427348a68db468
based-on-date: 2026-05-24
---

# Unified track C — Anchor-Distance Factory

## §0 Axis declaration and defense

**Chosen axis: distance-from-frozen-anchor.** Every factory work unit is parameterised by a single scalar: the graph distance between the change the work unit proposes and the nearest *frozen anchor* the architecture recognises. The same axis runs both mandates because the mandates differ only in *which anchor is frozen*, not in *whether* an anchor exists.

- For **greenfield** (per [`brief §0 glossary`](../00-brief-v3.md), `Greenfield (mandate)`): the frozen anchor is the **intent block** in the sense of El Kaim's 9-field typed object (report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §4.1) — its `invariants` field is the explicit "non-negotiable conditions any valid realization must preserve." UC4's "spec-malleable" claim ([`constraints-extracted §UC4`](../constraints-extracted.md)) operates *downstream* of the intent block: spec is malleable, intent invariants are not. This is the CTR-B6 reading (the register's MISSED-3 entry, see [`contradictions §CTR-B6`](../contradictions.md)).
- For **brownfield** (per `Brownfield (mandate)`): the frozen anchor is the **existing codebase's observable behaviour and slow-layer invariants** — Brier's "Architecture" and "Standards" pace-layers (followup [`12`](../../../research/followup/12-brier-pace-layers.md) §4; F34 cross-layer-drift) plus the live test suite and runtime telemetry.
- For both: each cycle's work unit names its anchor explicitly, declares its proposed change, and the substrate measures distance.

**Why this axis is unified-defensible (not a mandate-axis in disguise).** The mandate becomes a *parameter* — the anchor's content — rather than the organising distinction. The architecture's primitives (anchor declaration, distance measurement, distance-keyed gates and watchdogs) are identical across mandates. UC4's hypothesis ([`constraints-extracted §UC4`](../constraints-extracted.md), formalised as [`decisions-captured §D1`](../decisions-captured.md)) is falsified at the architecture-shape level by exactly this move: the difference between mandates is *where the freezing happens in the artifact stack*, not whether the same primitives can drive both. The corpus already supplies the unifying observation indirectly: Brier's pace-layers (followup [`12`](../../../research/followup/12-brier-pace-layers.md)) explicitly frames every artifact — code, plan, spec, architecture, standards — as living on a velocity gradient with slow layers anchoring fast ones. Anchor-distance is the operationalisation of that gradient.

**Pre-response to Phase-3 adversarial passes** (anticipating the four predictable attacks):

1. *"You are just renaming Brier's pace-layers."* Partial yes; the contribution is treating distance as the substrate's first-class scalar (not an analytic frame), and supplying explicit primitives — anchor-declaration object, distance estimator, distance-gated dispatch — so the brief's "lights-out vs L5" tension (§2.1) gets a concrete answer: lights-out operates at low distance from anchor; high-distance changes escalate. This is option (b)+(c) per brief §2.1.
2. *"Distance is unmeasurable; you have hand-waved the metric."* The estimator is a typed multi-component object, not a real-valued scalar pretending to objectivity. Components: graph distance to an intent invariant (greenfield: count of intent-block fields touched); blast radius in the codebase dependency graph (brownfield: transitive symbol-reach × test-coverage gap); pace-layer crossing count (Brier layers crossed). The substrate stores the estimator output as a typed tuple; the regime classifier is a substrate decision table; the metric's accuracy is itself watchdog-monitored.
3. *"This collapses to substrate-heavy + thin-methodology and is therefore CTR-C2-vulnerable."* Yes — and that is the load-bearing claim being defended. The axis predicts CTR-C2 ([`contradictions §CTR-C2`](../contradictions.md)) dissolves on the substrate-side because anchor-distance is the methodology layer expressed in a single substrate primitive. It does not dissolve on the *operating mode* side; that requires the regime-classification work below.
4. *"Frozen anchors will not stay frozen; the architecture pretends an asymmetry that does not exist."* The architecture explicitly models anchor *modification* as a separate work-unit class (`anchor-edit`) whose distance is undefined (it is the change *to* the anchor) and which is always L4-classified, never lights-out. This is the explicit re-entry mechanism per OQ-B3 ([`brief §8`](../00-brief-v3.md)).

**Why I did not pick more obvious axes** (anticipating the D7 blind-axis test, [`decisions-captured §D7`](../decisions-captured.md)): substrate/methodology layering (likely an A or B choice), regime-classification by L3/L4/L5 (corpus-default, Round-2-anchored), and work-unit-class taxonomy (D2 already names that, so leaning on it would be derivative). Anchor-distance is a fourth-quadrant axis the corpus implies (Brier + El Kaim invariants + UC4 spec-malleability framing) but never names.

**Falsifiability declaration.** If the corpus shows that what humans call "the same kind of change" routinely lives at very different anchor-distances depending on minor framing, the metric is post-hoc and the axis fails. CTR-B6 and CTR-F4 are the corpus' nearest counter-anchors; they suggest invariant-stability is achievable when discipline is enforced upstream.

---

## §1 Architecture sketch

**Name.** *Anchor-Distance Factory* (ADF).

**Five primitives** (substrate-layer):

1. **Anchor object** — a typed declaration carrying: `kind` ∈ {`intent-invariant`, `architecture-rule`, `standards-rule`, `live-test`, `runtime-trace`}; `content` (the immutable text/rule/test); `frozen-since` timestamp; `owning-mandate` ∈ {`greenfield`, `brownfield`, `both`}; `mutation-protocol` (the explicit policy for changing this anchor — always L4 with named-human approval). El Kaim's 9-field intent block (report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §4.1) is the canonical greenfield shape; Brier's ARCHITECTURE.md (followup [`12`](../../../research/followup/12-brier-pace-layers.md) §6) is the canonical brownfield shape.

2. **Distance estimator** — a substrate function `distance(work-unit, anchor-set) → (intent-fields-touched, blast-radius, pace-layers-crossed, contradiction-flag)`. The contradiction-flag is set when the work unit's proposed change implies anchor mutation; this is the F37 (silent contradictory-prompt collapse, [`failure-modes-v3 §F37`](../failure-modes-v3.md)) hard catch.

3. **Distance-gated dispatcher** — substrate routes work units to one of three regimes based on distance:
   - **Near-anchor (distance ≤ τ_low)**: lights-out by default; substrate-enforced gates (acceptance criteria, holdout discipline per [`brief §4.1 D-4`](../00-brief-v3.md)) are sufficient; this is where the Jaymin "Automation Mode" thresholds (K=5 ≥90%, [`brief §0 glossary`](../00-brief-v3.md)) apply.
   - **Mid-distance (τ_low < d ≤ τ_high)**: Augmentation Mode (per Jaymin, report [`09`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5); cross-model judge required (F46 mitigation per CJ Hess kevin/carl, report [`34`](../../../research/34-lenny-howiai-personal-harnesses.md) §6.2); single-judge architecture (per Anthropic followup [`07`](../../../research/followup/07-evals-deepdive.md)) is explicitly *not* sufficient at this distance.
   - **Far-anchor or anchor-edit**: human-in-loop, always; protocol matches OQ-B3 ([`brief §8`](../00-brief-v3.md)) re-entry mechanism; this is where Caremark/RSI exposure ([`31`](../../../research/31-caremark-rsi-board-exposure.md), F43) requires structured board reporting.

4. **Anchor mutation queue** — separate substrate queue for `anchor-edit` work units. These are always far-anchor by definition; they carry mandatory cooling-off windows, multi-author requirement, and Caremark-style immutable logging (followup [`10`](../../../research/followup/10-governance.md) §A, AILCCP).

5. **Distance-keyed trajectory storage** — D-7 trajectory capture (per [`brief §4.1 D-7`](../00-brief-v3.md); OpenHands V1 sub-ms persist per report [`11`](../../../research/11-openhands-substrate-audit.md)) is enriched with the distance tuple at write time. Patrol-tier watchdog ([`brief §0 glossary`](../00-brief-v3.md)) monitors the empirical distribution: if too many work units are landing just under τ_low, the dispatcher is being gamed (F47 Goodhart, [`failure-modes-v3 §F47`](../failure-modes-v3.md)).

**Methodology layer (thin).** Per-cycle process is generic: agent receives a work unit + the anchor set + the distance tuple + the dispatched-regime. Different mandates pick different anchor-sources (intent block vs. existing codebase) but the per-cycle loop is identical. The Compound Engineering loop (plan → work → review → compound, report [`03`](../../../research/03-every-compound-engineering.md)) is the default per-cycle methodology; Atelier-style queues and Attractor-style DOT pipelines (reports [`02`](../../../research/02-strongdm-attractor.md), [`27`](../../../research/27-dotfile-pipelines-as-product.md)) are alternative methodologies that can be plugged in without changing substrate primitives.

**What the architecture explicitly is**: a substrate-heavy, thin-methodology unified architecture organised by anchor-distance. CTR-C2 ([`contradictions §CTR-C2`](../contradictions.md)) calls this shape out as one option; this track defends it.

---

## §2 How this addresses each load-bearing concern

### Lights-out / L5 tension (brief §2.1, OQ-B1, CTR-A1/A4/H10)

Combines brief §2.1 options (b) and (c). **"Lights-out" maps to "automation-eligible work units defined by low anchor-distance,"** not to L5 in Jaymin's sense (report [`09`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §7). The vocabulary-mapping test (CTR-A4, [`contradictions`](../contradictions.md)) resolves: lights-out ≠ L5 because lights-out is a *per-work-unit predicate parametrised by distance*, not a system-wide regime. Jaymin's empirical anti-pattern claim (CTR-A1; the CodeRabbit 1.4× / Veracode 45% / METR 19% triple) applies to high-distance work; the corpus does not refute lights-out on *low-distance* work units, and the dispatcher enforces the boundary mechanically. Jaymin's Automation thresholds (K=5 ≥90%, prompt-paraphrase 5/5) are credited as the near-anchor bar.

### UC4 working hypothesis (brief §3)

**Hypothesis falsified at the architecture-shape level, not at the work-unit-level.** UC4 ([`constraints-extracted §UC4`](../constraints-extracted.md)) says greenfield-spec-malleable vs brownfield-code-archaeological imply incompatible architectures. ADF says: spec-malleable is *near-anchor on greenfield*; code-archaeological is *near-anchor on brownfield*; in both cases the agent operates close to its mandate-specific anchor, and the primitives serving that operation are identical. CTR-B6 (El Kaim intent invariants vs UC4 spec-malleable, [`contradictions`](../contradictions.md)) is the strongest counter-evidence: it says greenfield does have upstream stability if intent-block discipline is applied. ADF takes that side of CTR-B6 explicitly.

### Cold-start (greenfield mandate, brief §5)

See §5 below.

### OQ-B2 (greenfield/brownfield boundary at substrate vs methodology, brief §8)

**The boundary falls inside the anchor object's `kind` field**, not at the substrate/methodology seam. Substrate carries anchor-machinery for both mandates; the anchor's `kind` parameterises mandate. This is a third position relative to CTR-C2 ([`contradictions`](../contradictions.md)).

### OQ-B3 (human re-entry, brief §8)

Explicit and mechanical: re-entry triggers are (1) distance > τ_high, (2) `anchor-edit` work unit, (3) watchdog patrol-tier escalation (per D-6, [`brief §4.1`](../00-brief-v3.md); F42 Cognitive-Escrow Negligence, [`failure-modes-v3`](../failure-modes-v3.md)). Hand-back protocol: the operator's verdict on an escalated unit is itself logged as a distance-zero anchor-bearing artifact.

### OQ-B4 (brownfield unit of work, brief §8)

The unit of work is a *distance-typed proposed change* whose anchor set is the codebase + its slow layers. Issue-style (Atelier, glossary §0) and change-request-style (Refinery) are both representable as distance-typed changes; the dispatcher does not care which front-end was used.

### OQ-B6 (which empirical bars, brief §8)

ADF accepts Jaymin's K=5 / paraphrase / safety-incident bars (report [`09`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5) *for near-anchor work only*. Far-anchor work clears no automation bar; mid-distance work uses Augmentation bars (K=5 ≥70%, paraphrase ≥3/5). This is option (d) per brief §2.1.

### OQ-B7 (alternative organising axes, brief §8)

ADF *is* a candidate alternative axis. If Phase-3 accepts it, the D2 mandate-fit matrix ([`decisions-captured §D2`](../decisions-captured.md)) gains a row labelled `Anchor-Distance Factory` and the work-unit-class columns (initial-spec, refactor, mvp, post-mvp-evolution, regression-fix) re-interpret as *typical-distance ranges* rather than independent dimensions.

### OQ-B8 (provider-property requirements, brief §8)

ADF requires the substrate's provider-routing layer to support model-family diversity *at mid-distance and far-anchor* (F46 mitigation, [`failure-modes-v3`](../failure-modes-v3.md)). Near-anchor work is permitted single-family (allowing Anthropic's single-judge finding per followup [`07`](../../../research/followup/07-evals-deepdive.md) to apply where its conditions are met). RouterLLM-equivalent (report [`11`](../../../research/11-openhands-substrate-audit.md) §6) is sufficient; Attractor-style per-provider profiles (report [`02`](../../../research/02-strongdm-attractor.md)) are an acceptable alternative. CTR-C4 ([`contradictions`](../contradictions.md)) does not need resolution at architecture time.

### F-mode coverage (selected)

- **F1 / F27 (Hallucination Loop, Circularity, [`failure-modes-v3`](../failure-modes-v3.md))** — mitigated by distance-gated cross-model judging; near-anchor allows single-judge per followup/07, mid-distance enforces cross-model per F46.
- **F12 / F44 (Lethal Trifecta, [`failure-modes-v3`](../failure-modes-v3.md))** — anchor object's `mutation-protocol` field forces production-scissors prohibition for any anchor whose content includes production-touch; CaMeL-style closure (followup [`08`](../../../research/followup/08-security-primitives.md) §3) sits at the distance estimator's contradiction-flag interlock.
- **F20 (maintenance asymmetry, [`failure-modes-v3`](../failure-modes-v3.md))** — directly addressed by brownfield-anchored work being first-class; ADF is not greenfield-leaning by construction.
- **F25 (design starvation, [`failure-modes-v3`](../failure-modes-v3.md))** — the anchor's `kind=intent-invariant` provides the spec scaffolding that addresses the cold-start regime; see §5.
- **F34 (cross-layer drift, [`failure-modes-v3`](../failure-modes-v3.md))** — anchor object explicitly enumerates pace-layers via `kind`; cross-layer drift is detected at distance-tuple computation time.
- **F36 / F37 (instruction-following ceiling, contradictory-prompt collapse, [`failure-modes-v3`](../failure-modes-v3.md))** — distance estimator's contradiction-flag is the architecture's F37 mitigation; spec chunking by anchor proximity is the F36 mitigation.
- **F43 (RSI board-visibility, [`failure-modes-v3`](../failure-modes-v3.md))** — anchor mutation queue produces the structured class declarations Caremark/RSI requires (followup [`10`](../../../research/followup/10-governance.md), report [`31`](../../../research/31-caremark-rsi-board-exposure.md)).
- **F51 (Ashby-deficient probabilistic guard, [`failure-modes-v3`](../failure-modes-v3.md))** — distance-gated regime ensures probabilistic guards are only relied on near-anchor where requisite variety is lowest; far-anchor work uses deterministic perimeter (anchor mutation protocol) and human review.
- **F53 (voluntary-discipline fragility, [`failure-modes-v3`](../failure-modes-v3.md))** — anchor object + dispatcher are *structural* controls; ADF deliberately moves discipline out of operator-voluntary into substrate-enforced (Kahana's "fragile dependency" framing, report [`30`](../../../research/30-cognitive-escrow.md) §3).

---

## §3 Citations and grounding

Load-bearing claims map to the corpus as follows:

- **Anchor object as primitive**: El Kaim 9-field intent block, report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §4.1; Brier ARCHITECTURE.md per repo, followup [`12`](../../../research/followup/12-brier-pace-layers.md) §6. Corresponds to contradiction CTR-B6 (taking the El-Kaim side).
- **Distance as load-bearing scalar**: Brier pace-layers, followup [`12`](../../../research/followup/12-brier-pace-layers.md) §4; F34 cross-layer drift, [`failure-modes-v3 §F34`](../failure-modes-v3.md).
- **Distance-gated dispatch & regime mapping**: Jaymin Augmentation/Automation thresholds, report [`09`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5; brief §2.1 options (b)+(c).
- **Substrate-heavy, thin-methodology**: Round-2 framing per [`brief §4.1`](../00-brief-v3.md); CTR-C2 ([`contradictions`](../contradictions.md)).
- **Cross-model judging at mid-distance**: CJ Hess kevin/carl, report [`34`](../../../research/34-lenny-howiai-personal-harnesses.md) §6.2; F46 [`failure-modes-v3`](../failure-modes-v3.md).
- **Anchor-mutation Caremark protocol**: report [`31`](../../../research/31-caremark-rsi-board-exposure.md), followup [`10`](../../../research/followup/10-governance.md) (AILCCP). F43 [`failure-modes-v3`](../failure-modes-v3.md).
- **F37 contradiction-flag**: report [`26`](../../../research/26-prompt-underspecification-academic.md) §6.1–6.2 (Larbi et al., 73.8%→6.7% on contradictory HumanEval).
- **Structural over voluntary discipline**: Kahana cognitive-escrow, report [`30`](../../../research/30-cognitive-escrow.md); F53 [`failure-modes-v3`](../failure-modes-v3.md).
- **Trajectory storage cheap**: D-7 brief default; report [`11`](../../../research/11-openhands-substrate-audit.md).
- **Anchor `kind=runtime-trace` for brownfield**: StrongDM scenarios-as-tokens, report [`01`](../../../research/01-strongdm-factory.md) §1 (CTR-B5 WEAK-3 sharpening); D-2 fragile-default ([`brief §4.1`](../00-brief-v3.md)).
- **Per-employee fleet shape compatible with ADF (out of scope but consistent)**: reports [`32`](../../../research/32-shapiro-completion-chat-agent-claw.md), [`35`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md), [`36`](../../../research/36-sendbird-quests-token-tiers.md).

Inventory anchors used: corpus-inventory entries for reports 14, 09, 11, 30, 31, 32, 34, 38; followups 10, 12, 07, 08.

---

## §4 §4 defaults: accepted vs challenged (all 7 marked)

Defaults from [`brief §4.1`](../00-brief-v3.md):

- **D-1 (Specs are durable, version-controlled, human-curated)** — **`accepted with justification`**. The anchor object is itself a typed spec; its `frozen-since` and `mutation-protocol` fields are the durable-versioning discipline. ADF agrees with D-1; it sharpens *which part of the spec* is durable (the invariants/anchor) vs. malleable (the rest).
- **D-2 (Scenarios live outside the codebase as a holdout set)** — **`challenged`**. ADF treats scenarios as `anchor.kind ∈ {live-test, runtime-trace}` and explicitly admits brownfield anchors that live *inside* the codebase (production traces, existing test suites). Cite CTR-B5 ([`contradictions`](../contradictions.md), including the WEAK-3 sharpening showing StrongDM's own primary docs already permit in-tree scenarios via incident replays / agentic simulation, report [`01`](../../../research/01-strongdm-factory.md) §1). Cite brief §4.1 fragile-default flag.
- **D-3 (Agent = Model + Harness)** — **`challenged`**. CTR-C10 ([`contradictions`](../contradictions.md)) supplies the natural-language register evidence (report [`37`](../../../research/37-academic-llm-agent-collusion.md) §5); CTR-C1 supplies the graph-node/population case. ADF additionally needs *anchor-set context* as a first-class harness-adjacent input that "Model + Harness" does not name. ADF proposes: `Agent = Model + Harness + Anchor-Context`.
- **D-4 (Holdout discipline substrate-enforced)** — **`accepted with justification`**. Distance-gated dispatcher is the substrate-enforced holdout boundary; near-anchor work has acceptance criteria withheld by the dispatcher itself. F28 mitigation aligns ([`failure-modes-v3 §F28`](../failure-modes-v3.md)).
- **D-5 (Hard cost ceilings non-optional in CI)** — **`accepted with justification`**. Anchor mutation queue carries its own cost ceiling (high); near-anchor work has lower ceilings; ADF accepts D-5 and parameterises it by distance. CTR-E1 cost-variance is addressed by per-distance ceilings.
- **D-6 (Tiered watchdog Daemon/Triage/Patrol)** — **`accepted with justification`**. Patrol-tier specifically monitors the dispatched-regime distribution to detect F47 Goodhart (gaming the distance estimator) and F49 discussion-as-amplification.
- **D-7 (Trajectory capture cheap)** — **`accepted with justification`**. Distance tuple is appended to every trajectory event at sub-ms cost (report [`11`](../../../research/11-openhands-substrate-audit.md) measurement context applies).

---

## §5 Cold-start (MANDATORY for unified-touching-greenfield)

**Day 0 of a greenfield ADF instance** has no codebase, no test suite, no `docs/solutions/`, no prior runs — but it does have anchor-machinery and a mandate to populate the anchor set.

**Step 0 (anchor authoring, operator-led).** Operator authors the initial **intent block** per El Kaim's 9-field shape (report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §4.1), with explicit population of the `invariants` field. This is required reading per [`brief §5.1`](../00-brief-v3.md) and is the asymmetric mitigation against F36 (instruction-following ceiling, report [`26`](../../../research/26-prompt-underspecification-academic.md) §3.4) and F37 (silent contradictory-prompt collapse, ibid §6.1–6.2). Operator is supported by an RE/SE-grounded prompt scaffold derived from INCOSE GtWR C1–C15 (report [`25`](../../../research/25-requirements-engineering-foundations.md) §"Implications") and EARS (ibid). The intent block is the day-0 frozen anchor.

**Step 1 (priors absorption).** Per the revised greenfield definition ([`brief §0 glossary`](../00-brief-v3.md), Skeptic #6): priors from adjacent domains, exemplar projects, library docs, and operator-curated knowledge from *other* factory runs are *permitted and expected*. The substrate ingests these as `anchor.kind=standards-rule` entries (citing F8 stale-knowledge inversion, [`failure-modes-v3`](../failure-modes-v3.md), as a discipline reminder — these priors are subject to F8 staleness even though they enter as anchors).

**Step 2 (cold-start dispatched cycles).** First cycles are by construction far-anchor (no near-anchor anchors exist beyond the intent block itself, so most proposed code is far from any architecture/standards anchor). ADF says: this is correct, and the dispatcher routes accordingly — cold-start is **L4 by construction**, lights-out cannot apply until anchors thicken. This is the trajectory from day 0 → day N: the system *earns* its lights-out regime by accumulating anchors. Anchors accumulate by:

  - **Pattern → standard promotion** (Brier pace-layers, followup [`12`](../../../research/followup/12-brier-pace-layers.md) §6: "project doc → Skill → enforced standard"). Each cycle's repeatable pattern is candidate for promotion to `anchor.kind=standards-rule`. Promotion is an `anchor-edit` work unit (always L4).
  - **First-passing tests** become `anchor.kind=live-test` once they have stabilised across N cycles.
  - **Architecture decisions** (ADRs) become `anchor.kind=architecture-rule`.

**Step 3 (bootstrap silent-failure protection).** Cold-start is the regime most exposed to F1/F27 (no holdout codebase exists, [`failure-modes-v3`](../failure-modes-v3.md) F1 greenfield-severity = critical) and F25 (design starvation). ADF's protection:

  - The intent block's `invariants` are themselves a non-trivial holdout — they are spec, not code, and judges can be asked to verify code against invariants. This is the *invariants-as-day-0-holdout* claim, drawing on report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §4.1 + report [`25`](../../../research/25-requirements-engineering-foundations.md) §"Implications" (Ashby variety arg).
  - F25 (design starvation, [`failure-modes-v3`](../failure-modes-v3.md) — greenfield-critical) is addressed by ADF's regime declaration: in cold-start, work-unit throughput is *expected* to be human-bottlenecked because all work is far-anchor; no lights-out promise is made. This is honest scope rather than mitigation, and the brief's mandatory cold-start section permits this honesty.
  - Cognitive escrow per Kahana (report [`30`](../../../research/30-cognitive-escrow.md), F42) is structurally present at cold-start: every cycle's output goes back to the operator, and the substrate exposes the prompt→response interval as a designed surface (per Schillace's Attention Firewall, report [`28`](../../../research/28-schillace-sunday-letters.md); Nystrom's standup pre-read, report [`35`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)).
  - Caremark/RSI board exposure (report [`31`](../../../research/31-caremark-rsi-board-exposure.md), F43) is honoured: cold-start cycles are logged with immutable AILCCP records (followup [`10`](../../../research/followup/10-governance.md) §A); the deploying organisation receives the class declaration the brief §5.1 reading list explicitly mandates.

**Trajectory from day 0 → day N.** ADF's transition to steady-state is not a date but a *distance-distribution shift*: the empirical distance distribution of work units shifts leftward (toward near-anchor) as the anchor set thickens. The transition criterion is mechanical — when ≥X% of work-unit distance distribution sits at d ≤ τ_low for K consecutive cycles, the dispatcher begins to route those work units lights-out. The architecture refuses to commit to a calendar transition; it commits to a distance-distribution transition.

---

## §6 What this track is NOT trying to be

- **Not comprehensive.** ADF's organising axis is anchor-distance; other axes (regime, stakes, synchronicity, per-employee fleet shape) are left to other tracks (greenfield-G/brownfield-B, unified-A/B, Phase-3 merge).
- **Not a complete substrate spec.** Phase 4 owns substrate-vs-methodology extraction; ADF describes substrate primitives only at the level needed to ground the axis defense.
- **Not a refutation of UC4.** UC4 is taken as a falsifiable hypothesis per D1; ADF is one falsification candidate, not a proof.
- **Not a coordination-layer proposal.** Coordination medium choice (mail bus vs GitHub-issues, CTR-C7) is methodology-layer detail; ADF is agnostic.
- **Not an `Agent = Model + Harness` rebuttal.** ADF challenges D-3 but does not replace it — proposes the extension `+ Anchor-Context` and leaves the rebuttal scope to Phase 3.
- **Not a metaphor stance.** Brier's software-factory-vs-company critique (CTR-F1, followup [`12`](../../../research/followup/12-brier-pace-layers.md)) is acknowledged; ADF takes no position on the metaphor because the architecture works under either framing.

---

## §7 Open questions surfaced by this track

1. **Is the distance estimator robust to adversarial gaming?** F47 Goodhart-on-Tokens ([`failure-modes-v3`](../failure-modes-v3.md)) applies: agents authoring work-unit descriptions may learn to phrase changes to land just below τ_low. The patrol-tier watchdog is the proposed catch; whether it is sufficient is empirically open. Concrete next action: design an adversarial-pass evaluation where one subagent attempts to author work units that land under τ_low while smuggling far-anchor changes.
2. **Does the contradiction-flag close F37, or merely narrow it?** F33/F51 (Ashby-deficient probabilistic guard, [`failure-modes-v3`](../failure-modes-v3.md)) suggests probabilistic detection has variety limits. Concrete next action: characterise the contradiction-flag's required variety against the regulated system's disturbance-variety (Ashby), and decide whether deterministic perimeter is required for `anchor-edit` detection.
3. **How are anchor invariants kept honest over a multi-month cold-start?** F8 stale-knowledge inversion + F35 federation-as-family drift ([`failure-modes-v3`](../failure-modes-v3.md)) both apply. The `anchor-edit` queue is the mechanical answer; the open question is whether the queue's cooling-off windows are themselves vulnerable to F53 (voluntary discipline fragility).
4. **Does anchor-distance correctly subsume Brier's pace-layers, or is it a strictly weaker re-encoding?** Phase-3 adversarial pass should test this: read Brier's five-layer framing (followup [`12`](../../../research/followup/12-brier-pace-layers.md)) and check whether anchor-distance preserves what Brier's framing predicts (e.g., that patterns sift downward through the layers).
5. **The biggest single open question — can the distance estimator be made operator-legible at the moment of dispatch?** If the operator cannot see why a work unit was routed to lights-out (vs Augmentation / human), the substrate is opaque in exactly the way F42 (cognitive-escrow negligence) names. Concrete next action: design a lean evaluation where the distance-tuple is exposed alongside every dispatch decision and operators rate the legibility.

---

*End of unified-C.md.*
