---
based-on-commit: 5c4deeb
based-on-date: 2026-05-24
---

# Phase-2 axis-divergence audit

**Method.** Read the §0 axis defenses of unified-A, unified-B, unified-C in full. Then grep the brief, the §C-bis unified-track must-read list, the failure-modes catalog, the contradictions register, the decisions log, and the three Phase-1 bias-guard reports for biasing language ("stakes", "tier", "risk-tier", "blast-radius", "reversibility"). For each candidate bias source, classify as `present` (the language is in material the unified-track subagents were instructed to read), `borderline`, or `absent`. Then test whether A and C are the same axis, judge whether convergence is honest corpus signal or contamination, and recommend a Phase-3 treatment.

---

## Section 1 — The axis selections in detail

### Track A axis: risk-tier (T0-T4)

- **Defining dimensions:** blast radius × reversibility × Kahana-RSI-exposure.
- **Tier set:** 5 tiers — T0-sandbox / T1-recoverable / T2-rollback / T3-production-scissors / T4-RSI-exposed.
- **Citations driving the choice** (A's §0.3 four-reason defense):
  1. CodeRabbit 1.4× / Veracode 45% / METR 19% (via report 09) + Replit DB wipe (followup 10, F56) — all framed as biting "at the production-scissors boundary, not at greenfield vs. brownfield."
  2. Shapiro R3 production-scissors rule (report 32 §8.2; F44) — framed as a tier rule.
  3. Kahana RSI three-part test (report 31) — framed as mandate-agnostic, tier-axis concept.
  4. Explicit rejection of Brier pace-layers (followup 12) as the primary frame, while borrowing the pattern-sift mechanism.
- **Distinguishing move:** RSI as its own discrete tier (T4); explicit tier ↔ Shapiro-level mapping (T0–T2 = lights-out, T3 = L4, T4 = Augmentation-with-Approval).

### Track B axis: Brier pace-layers

- **Defining dimensions:** artifact pace / churn cadence — five layers (Code / Plans / Specs / Architecture / Standards).
- **Citations driving the choice:** followup 12 (Brier) as the primary anchor, with report 14 (El Kaim invariant pack at Standards layer) and report 35 (Nystrom spec-git-history at Specs layer) as the per-layer fits; F34 (cross-layer drift) made first-class via a dedicated Sentinel judge.
- **Distinguishing move:** regime per layer (L5 only at Code under conditions); mandate becomes per-layer initial state + churn-gradient; the Sentinel is the architecture-level mitigation of F34.

### Track C axis: stakes-tier / blast-radius (T0-T3)

- **Defining dimensions:** reversibility × scope × regulatory-exposure (three orthogonal typed attributes; least-permissive wins).
- **Tier set:** 4 tiers — T0-sandboxed / T1-revertible / T2-production-touch / T3-regulated.
- **Citations driving the choice** (C's §0.2):
  - The F-mode catalog's greenfield→brownfield severity escalations (F12, F30, F33, F43, F44, F54, F56, F58) all reduce to "production proximity changed" — a stakes property.
  - CTR-C2 substrate-heavy/thin-methodology framing (Round-2 anchor) treated as the *expected* shape.
  - Report 31 (Kahana RSI) anchors T3 regulated overlay.
  - Report 38 (Beads `discovered-from`) + followup 11 (CK typed-classification) carry the cross-overlay unification claim.
- **Distinguishing move:** **the tier classifier is deterministic** (a typed-attribute policy table — explicitly NOT an LLM judgment, per §0.3 point 4 invoking the F51 Ashby-deficient lesson "one layer up"). Mandate is preserved as a *statistical distribution* over tiers, not eliminated.

---

## Section 2 — Are A and C "the same axis"?

Test on four dimensions:

| Test | Track A | Track C | Same? |
|---|---|---|---|
| Primary dimensions | blast-radius × reversibility × RSI-exposure | reversibility × scope × regulatory-exposure | **near-same** (RSI-exposure ≈ regulatory-exposure; blast-radius ≈ scope) |
| Tier count | 5 (T0–T4) | 4 (T0–T3) | **distinct** — A breaks out RSI as its own tier; C folds RSI under T3-regulated |
| Classifier type | deterministic floors + LLM-judge hybrid with confidence threshold | deterministic policy table, explicitly never an LLM call | **distinct** — different stance on F51 Ashby risk for the classifier itself |
| Downstream architectural moves | tier-overlay matrix selects per-tier (judges, cost, watchdog cadence, escrow shape); methodology shapes from v2 absorbed as tier-overlay choices | seven shared substrate primitives + four overlay bundles; explicit Discovery / Excavation / Production-touch / Regulated overlays | **same shape, different vocabulary** — both = "one substrate, tier-selected overlays" |
| Regime mapping (CTR-A4) | T0–T2 = lights-out; T3 = L4; T4 = Augmentation-with-Approval | T0–T1 = L5-equivalent post-bar-clearance; T2 = L4; T3 = L3 with Human Approval Gate | **same logic, off-by-one in tier-count** |
| Mandate handling | mandate as covariate; greenfield/brownfield feeds inject inputs before classification | mandate as statistical distribution over tiers; Discovery vs. Excavation overlays = mandate-shape at T0–T1 | **same logic, different overlay vocabulary** |
| Treatment of F57 (stakes-drift) | substrate-audited tier-emit event | substrate-monitored stakes-drift in Patrol watchdog | **same** |

**Verdict: borderline → same.** The dimensions overlap (blast-radius vs. scope is a vocabulary difference; RSI-exposure vs. regulatory-exposure is a near-synonym), the architectural shape is identical (substrate + tier-selected overlays), the regime mapping is the same logic at different granularity, and both explicitly cite the F-mode severity-gradient as the empirical anchor. The non-trivial distinctions are (a) classifier mechanism (A allows LLM-judge; C forbids it), (b) tier count (A=5 with RSI as its own tier; C=4 with RSI folded into T3), and (c) C's explicit Discovery/Excavation overlay bifurcation at low tiers that A handles via mandate-feed adapters before classification.

These are **implementation-level distinctions on the same axis**, not different axes. A reviewer reading the two §0s back-to-back would judge them as cousins, not strangers. If we count axes strictly, **the corpus produced 2 distinct axis selections from 3 subagents**: tier-class (A+C) and pace-layers (B).

---

## Section 3 — Prompt-bias test

Searched the prompt material for biasing language. Findings:

### 3.1 Brief §8 OQ-B7 explicitly names "stakes" as a candidate axis

> *"OQ-B7. **(New per Skeptic #1, partially resolved by D1.)** Beyond mandate, what organizing axes (regime, **stakes**, synchronicity, work-unit-class, codebase-lifecycle stage) deserve architectural-level treatment? The 3 both-mandates tracks (D1) have explicit authorization to surface alternative axes."* (00-brief-v3.md L217)

This is a **named candidate-axis list** in the brief. "stakes" is one of five examples. Two of three subagents picked it. Classification: **present, high-magnitude**. A subagent looking for "what axes are legitimate to pick" finds an explicit list in the brief; picking from that list is the path of least resistance, especially for "stakes" which is the most resonant with the corpus' F-mode anchoring.

### 3.2 decisions-captured.md repeats the list

> *"Also resolves Skeptic #1 (whether regime/**stakes**/synchronicity should be primary axes alongside mandate). The 3 no-axis-prescribed tracks have explicit authorization to find them; the corpus will surface them if they're load-bearing."* (decisions-captured.md L27)

Classification: **present**. Same list, restated in the decision log the unified-track subagents would consult.

### 3.3 F57 in failure-modes-v3.md presupposes tier-classification

> *"The factory classifies work units into automation-eligible vs human-required by **stakes / risk tier**. Over time, convenience pressure ... reclassifies higher-stakes decisions downward..."* (failure-modes-v3.md F57 mechanism, L528)

This is the **strongest single biasing source**. F57's mechanism description does not present tier-classification as one option — it presents it as a *given* of how the factory works. Both A and C cite F57 directly. A subagent reading F57 to understand the failure mode is also reading an implicit ontology in which tier-classification is the factory's organizing primitive. Classification: **present, high-magnitude**.

### 3.4 §C-bis unified-track must-read list

Re-reading the 12-item must-read list (corpus-inventory.md L364–L381):

- Followup 12 (Brier pace-layers) — explicit candidate axis (B picked it).
- Report 38 (Gas City substrate split) — substrate-vs-application axis.
- Reports 14, 18, 11, 38 — substrate primitives.
- Report 31 (Kahana RSI) — tier-relevant but mandate-agnostic.
- Report 30 (cognitive escrow) — interval-as-tier-property.

The list **does not disproportionately favor tier-based axes** — Brier (pace) and Gas City (substrate-split) are equally available. However, **the list's coverage observation** ("skews toward substrate reports rather than methodology reports... consistent with the lead-agent working stance that 'substrate-heavy + thin-methodology' may be how a unified architecture emerges") nudges toward "substrate + overlay" architectures. Both A and C produced exactly that shape. Classification: **borderline**. The list itself is neutral; the coverage observation gently biases toward substrate-overlay shapes (which tier-overlay matrices are a natural instance of).

### 3.5 Phase-1 bias-guard reports

- **missing-failure-modes-audit.md CANDIDATE-6** (which became F57): uses the exact phrase "stakes / risk tier" and frames factory work-unit classification *as* a stakes-tier operation. Classification: **present, high-magnitude**.
- **missing-failure-modes-audit.md** repeatedly references "blast radius" (F45, F56, etc.) and "production scissors" — both A and C cite these clusters as the anchor for tier-based axes.
- **uncomfortable-contradictions-audit.md MISSED-3** (El Kaim invariants vs. UC4 spec-malleability): does not bias toward tier specifically, but its resolution shape (invariants at one level, malleability at another) is structurally tier-like; both A and C absorbed it via tiered invariant ratchets. Classification: **borderline**.

### 3.6 Brief §2.1 option (c)

> *"(c) Declare a regime-classification scheme that names where the factory operates at L4 vs. L5 and which work units flow to which."* (00-brief-v3.md L86)

This is followed by the lead-agent working stance: *"option (c) plus (b) is the most likely shape."* This is a direct nudge toward classifying work units by something (regime or stakes), which is structurally a tier exercise. Classification: **present, medium-magnitude**.

### 3.7 Brief D-6 / glossary §0 "Daemon / Triage / Patrol"

The brief already establishes a tiered substrate (the watchdog). The vocabulary of "tiered substrate" is normalized. Classification: **borderline**.

### Convergence score

| Bias source | Magnitude |
|---|---|
| Brief OQ-B7 candidate-axis list including "stakes" | high |
| F57 framing factory as tier-classifier | high |
| CANDIDATE-6 / missing-failure-modes language | high |
| Brief §2.1 option (c) regime-classification nudge | medium |
| §C-bis coverage observation | borderline |
| decisions-captured.md restatement | medium (reinforcement, not independent) |
| MISSED-3 resolution shape | borderline |
| D-6 tiered watchdog precedent | borderline |

**Aggregate verdict: mixed → leaning contaminated.** The corpus does genuinely support a stakes/tier reading (the F-mode severity-gradient is real corpus signal). But the brief, the F-mode catalog, and the bias-guards repeatedly name "stakes / risk tier" as the candidate frame — making it the *named, available, low-friction choice* for any subagent looking for an axis outside mandate. The A/C convergence is not pure corpus signal; it is partly the brief's own candidate list working as a soft prompt.

---

## Section 4 — Honest corpus signal test

Despite the contamination, there *is* genuine independent corpus support for risk-tier:

1. **F-mode severity gradient is real.** F12, F30, F33, F43, F44, F54, F56, F58 all escalate greenfield→brownfield in a way that A and C both attribute to production-proximity (a stakes property), not to mandate. The catalog was authored *before* the unified tracks; the gradient is corpus signal, not subagent confabulation.

2. **Different anchors converge.** A leans heavily on Kahana RSI (report 31) + Shapiro R3 (report 32) + the Jaymin empirical-anchor cluster (CodeRabbit/Veracode/METR via report 09). C leans heavily on the F-mode-severity-pattern + CTR-C2 substrate-heavy framing + Beads/CK knowledge-graph (report 38, followup 11). The *only* overlapping primary citation is Kahana RSI (report 31). That's some independence: A and C converged on tier-shape from partially independent corpus walks.

3. **Brier (B) is the corpus' only explicit alternative.** Followup 12 is the only public counter-metaphor in the corpus. B picked it. That B exists at all and was defensible means the corpus does *not* uniformly point at tier — it admits at least one other architecture-level axis. If the corpus *only* supported tier, B would have failed; B's existence as a credible track is evidence the corpus supports multiple axes.

4. **What A and C reject is informative.** Both explicitly reject Brier pace-layers as the *primary* axis while accepting it as a per-layer property (A §0.3 point 4; C §0.2). Both also reject mandate-as-primary using the same F-mode-severity argument. The reject-pattern is consistent across A and C, which is corpus signal in itself.

Honest signal exists. The contamination is in the **magnitude** of A+C's convergence — 2/3 tracks naming the same axis is more than the independent corpus signal alone would predict; the brief's candidate-list and F57's framing closed the gap.

---

## Section 5 — Implication for D1's falsification work

D1's setup tested two distinct questions:

**Q1: Are unified architectures possible?** Answer: 3/3 yes (A: conditional yes; B: yes with falsifiable shape; C: yes if axis = stakes-tier). This is **converged** independent of axis choice. The unified-possibility hypothesis is **not falsified** — three defensible unified architectures exist.

**Q2: Does the corpus point uniquely at one organizing axis?** Answer: **partially**. The 2-of-3 tier convergence is *partly* honest corpus signal (the F-mode severity gradient is real and load-bearing) and *partly* prompt-bias contamination (the brief named "stakes" as a candidate axis, F57 presupposes tier-classification, the missing-FM audit used "stakes/risk tier" language). If contamination were removed, we'd expect the convergence to be weaker — perhaps 1.5-of-3 tier rather than 2-of-3.

This matters for Phase 3 as follows:

- **If A+C is treated as "the corpus genuinely points at tier"** → Phase 3 merges them into one unified architecture, treats tier as the load-bearing primitive, and treats B as a complementary layer-axis dimension. This risks locking in the contamination.
- **If A+C is treated as "the corpus admits tier as one defensible axis, with one fingerprint of prompt-bias"** → Phase 3 acknowledges the tier-axis is well-supported but does *not* treat it as uniquely-correct; B's pace-layer axis is preserved as a peer, and a Phase-2 supplement may be warranted to probe axes the brief did NOT name (synchronicity, knowledge-accumulation strategy, judge-architecture, language-as-harness) for under-coverage.

---

## Section 6 — Recommendation to Phase 3 lead agent

**Recommendation: Merge A+C as a single "stakes/tier" unified architecture, but explicitly preserve B as a peer and flag the contamination in the merge artifact.**

Specific actions:

1. **Treat A and C as the same axis at the merge layer.** They are cousins, not strangers; their differences (5-tier-with-RSI-broken-out vs. 4-tier-with-RSI-folded; LLM-judge-classifier vs. deterministic-classifier; mandate-feed-adapter vs. Discovery/Excavation overlays) are ADR-class implementation choices, not architecture-class choices. The merged unified-A+C should pick one tier count (recommend C's 4, with A's RSI-as-distinct-tier as an OQ for governance-exposed deployments), one classifier mechanism (recommend C's deterministic table per F51 Ashby argument, with A's confidence-threshold + LLM-judge as the *escalation path* for ambiguous cases), and one low-tier-mandate-handling mechanism (the Discovery/Excavation overlay split is more explicit than mandate-feed-adapters; recommend C's framing).

2. **Preserve B (pace-layers) as a peer unified architecture, not as a sub-component.** The 1/3-of-3 minority is a legitimate alternative axis with its own corpus anchor (Brier, the only public counter-metaphor). Folding B into A+C as "pace-layers is a per-tier property" loses B's positive claim that *regime should be per-layer not per-cycle*. The Phase 3 unified-synthesis-v1.md should produce **two unified architectures**, not one: U1 = stakes-tier (merged A+C) and U2 = pace-layered (B), with their differences explicit.

3. **Flag the contamination in writing.** The Phase 3 merge artifact should include a section titled something like "Why two unified architectures, not one" that explicitly notes: (a) A+C convergence is partly prompt-bias (brief OQ-B7's candidate list + F57 framing), (b) the corpus signal genuinely supports tier-axis but not uniquely, (c) B's pace-layer alternative is preserved precisely because eliminating it would lock in the contamination.

4. **Phase-2 supplement: probably warranted.** None of the three unified tracks picked a *non-named* axis. The brief named six candidate axes (mandate, regime, stakes, synchronicity, work-unit-class, codebase-lifecycle stage) plus Brier pace-layers, plus the lead-agent stance of substrate-vs-methodology — and 3/3 subagents picked from this list (B = pace-layers; A+C = stakes). **No subagent picked synchronicity, knowledge-accumulation strategy, judge-architecture, language-as-harness, or any wholly novel axis.** This is consistent with the named-list functioning as a soft prompt. A single supplementary unified track with an explicit "axis must be NOT on the brief's list" constraint would test whether the absence of these axes is honest under-support or pure list-anchoring. Recommend dispatching one such track before Phase 3 merge.

---

*End.*
