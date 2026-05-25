---
phase: 4.3
based-on-commit: 96a949430b5c356f8b4e688b1d427348a68db468
scope: track-driven discipline extraction (9 Phase-2 tracks + D7-U-1 blind-axis)
subagent: discipline-extraction-tracks
---

# Architecture-level disciplines (track-driven extraction)

This file inventories *architecture-level disciplines* — the meta-disciplines that govern *how a methodology calls into a substrate* and *what invariants are maintained at boundaries* — as named (explicitly or by pattern) across the 9 Phase-2 methodology tracks plus the D7-U-1 blind-axis file. Per the [working definitions](../phase-3.4-decisions-resolved.md#working-definitions-architecture-substrate-methodology), disciplines are *distinct from* substrate primitives (which are typed things with contracts + construction paths) and *distinct from* methodology choices (which fix per-cycle stages and unit-of-work).

Ordering is by claim-strength: the most-strongly-cross-referenced disciplines come first.

**Tag legend.**
- `explicit-named` — candidate names the discipline by name (or near-paraphrase) in the track.
- `inferable` — candidate uses the pattern in a load-bearing way without naming it as a discipline.
- `rejects` — candidate explicitly rejects or refuses this discipline.
- `silent` — candidate is silent on it within the read scope.

**Scope honesty.** The track files are the read surface. AGENTS.md-codified disciplines (real-subagent-review, three-layer citation, internal-document-references) may be only weakly inferable from tracks; flagged for lead-agent merge against Subagent-2 (registry / primitives) output.

---

## D-Bias-Guard — Bias-guard / adversarial-review discipline

- **One-line definition.** Every load-bearing artifact is subjected to an *opposing-side* attempt to refute it (cross-model judge, deterministic checker, named human, population vote) before downstream compounding is permitted.
- **Governing principle.** F1/F27/F46/F48 cascade is single-mechanism: no opposing side committed to falsifying the output. Same-model self-review inherits the author's blind spots. Independence is *measured*, not declared (D7-U-1's Patrol-tier independence auditor).
- **Candidates that name it (with claim strength).**
  - `D7-U-1` (`explicit-named`) — entire architecture is built around this discipline; primitive is the `FalsificationCommitment` ([d7-u-1-prohibit-interval-escrow.md §1](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md), "Adversarial-Falsification Topology").
  - `BF-M` (`explicit-named`) — Stage-6 cross-model review is constitutive ("Cross-family routing for reviewer", [brownfield-methodology-first.md §1.1](../tracks/brownfield-methodology-first.md) stage 6); §2.5 cites F46 directly.
  - `GF-M` (`explicit-named`) — paraphrase divergence as F37 defense, K=5 cross-model panel ([greenfield-methodology-first.md §1.1 / §1.2 / §2.9](../tracks/greenfield-methodology-first.md)).
  - `GF-C` (`explicit-named`) — Cold-Start Bench requires cross-model judge mandatory at first cycles ([greenfield-cold-start-first.md §1.2 / §5 "five protections" #2](../tracks/greenfield-cold-start-first.md)).
  - `U-A`, `U-B`, `U-C` (`explicit-named`) — judge-diversity is an explicit interval/layer/distance-policy slot ([unified-A.md §1 EscrowInterval.policies.judge-diversity](../tracks/unified-A.md); [unified-B.md §2.5](../tracks/unified-B.md); [unified-C.md §1 distance-gated dispatcher](../tracks/unified-C.md)).
  - `BF-S`, `BF-L` (`explicit-named`) — cross-model judge is a substrate-required cycle-step ([brownfield-substrate-first.md §1.3 step 5](../tracks/brownfield-substrate-first.md); [brownfield-legacy-ingestion-first.md §2.3 "Load-bearing F-modes" F46](../tracks/brownfield-legacy-ingestion-first.md)).
  - `GF-S` (`inferable`) — substrate primitive S6 (judge routing) types the judge-shape choice but does not adjudicate ([greenfield-substrate-first.md §1.S6](../tracks/greenfield-substrate-first.md)); related to discipline, not the discipline itself.
- **Anchored corpus sources.** Report 34 §6.2 (CJ Hess `kevin`/`carl`); Report 23 §3.5 (Anthropic five specialist critics); followup 07 §3.6 (Husain/Shankar same-model judging); Report 26 §6.1–6.2 (Larbi MCC ≤ 0.55); F46 in [failure-modes-v3.md](../failure-modes-v3.md).
- **Open questions / debates across candidates.** Same-model-different-role vs cross-model-different-family is unresolved across tracks ([CTR-D4 / D7 / D8](../contradictions.md) split). U-A treats it as per-interval policy; U-B treats it as per-layer policy; D7-U-1 treats opposing-side identity as a typed FC field. GF-M and BF-M insist on cross-family at stage-6; followup 07's "same-model is fine when the task differs" is acknowledged by U-A/U-B but not adopted as default.
- **Relation to substrate primitives.** GF-S `S6 judge routing`; U-A `judge router`; U-C `distance-gated dispatcher`; D7-U-1 `opposing-side router`. The discipline is enforced *by* these primitives; it is not identical to any of them.

---

## D-Substrate-Enforcement — Substrate-enforced (not voluntary) discipline

- **One-line definition.** Critical invariants are enforced by the substrate's refusal to advance, not by operator or methodology-layer voluntary compliance.
- **Governing principle.** F53 (voluntary-discipline fragility, Kahana). Any control assumed to be operator-applied or methodology-applied breaks under the time-pressure conditions where it is most needed. Replit-class incidents (followup 10 §3) are the empirical anchor.
- **Candidates that name it (with claim strength).**
  - All 10 tracks (`explicit-named`). Every track invokes F53 by name and uses it to justify substrate-typing of at least one control.
  - `GF-S` ([greenfield-substrate-first.md §1.S5 / §1.S8 / §1.S9 / §4 / §5.4](../tracks/greenfield-substrate-first.md)).
  - `GF-M` ([greenfield-methodology-first.md §2.9 F53 line](../tracks/greenfield-methodology-first.md)).
  - `GF-C` ([greenfield-cold-start-first.md §1.1 R1-R5 substrate-default; §5 "five protections"](../tracks/greenfield-cold-start-first.md)).
  - `BF-S` ([brownfield-substrate-first.md §0 reason 3; §1.1 S-5; §4 D-4 / D-6](../tracks/brownfield-substrate-first.md)).
  - `BF-M` ([brownfield-methodology-first.md §2.5 F53 line "cycle refuses to advance, not the operator refusing-to-skip"](../tracks/brownfield-methodology-first.md)).
  - `BF-L` ([brownfield-legacy-ingestion-first.md §2.3 F56 / F44; §3 F53 line](../tracks/brownfield-legacy-ingestion-first.md)).
  - `U-A` ([unified-A.md §0 reason 4; §5.3 bootstrap interval policies](../tracks/unified-A.md)).
  - `U-B` ([unified-B.md §0 reason 2; §1 escrow primitive "structural replacement for voluntary discipline"](../tracks/unified-B.md)).
  - `U-C` ([unified-C.md §2 F53 line; §5 Step 0](../tracks/unified-C.md)).
  - `D7-U-1` ([d7-u-1-prohibit-interval-escrow.md §0 reason 4; §1.3 Compounding gate](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)).
- **Anchored corpus sources.** Report 30 §3 (Kahana voluntary-discipline fragility); followup 10 §3 (Replit / Moltbook incidents); Report 32 §8.2 (Shapiro R1-R5 substrate-default scissors).
- **Open questions / debates across candidates.** U-B (§7 OQ-PLEF-5) surfaces the strongest residual: the *operator's response* to a substrate-fired prompt is itself voluntary. D7-U-1 sidesteps this by refusing to elevate attention-surface design to substrate; U-A/U-B make it constitutive. The disagreement is *which voluntary residual is tolerable*.
- **Relation to substrate primitives.** Cuts across most named primitives: S1 sandbox closure-default-off, S4 cost ceiling, S5 watchdog tiers, S8 guard mediator (GF-S); S-5 perimeter (BF-S); policy mediator (U-A); compounding gate (D7-U-1).

---

## D-Holdout — Holdout-partition discipline

- **One-line definition.** Builder agents cannot read the artifacts (scenarios, acceptance criteria, telemetry) used to judge their output; the substrate enforces the partition, not the methodology.
- **Governing principle.** D-4 from the brief; F28 holdout-leakage. The discipline survives the D-2 brownfield challenge (scenarios may live in-tree) by re-anchoring on *unseen-by-builder*, not *out-of-tree*.
- **Candidates that name it (with claim strength).**
  - All 10 tracks (`explicit-named`); every track marks D-4 `accepted-with-justification` (or `accepted-and-expanded`).
  - `GF-S` (substrate-typed holdout, S2 + S6, [greenfield-substrate-first.md §1.S2](../tracks/greenfield-substrate-first.md)).
  - `BF-S` (expanded to telemetry-as-scenario partitioned by role, S-3, [brownfield-substrate-first.md §1.1 / §4 D-4](../tracks/brownfield-substrate-first.md)).
  - `BF-L` (in-model partition enforcement; [brownfield-legacy-ingestion-first.md §1 scenarios + §4 D-4](../tracks/brownfield-legacy-ingestion-first.md)).
  - `U-A` (policy mediator refuses to close judge interval if leak detected; [unified-A.md §4 D-4](../tracks/unified-A.md)).
  - `D7-U-1` (generalized to *every* artifact boundary via the compounding gate; [d7-u-1-prohibit-interval-escrow.md §4 D-4](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)).
- **Anchored corpus sources.** F28 in [failure-modes-v3.md](../failure-modes-v3.md); Round-2 C13.
- **Open questions / debates across candidates.** Greenfield insists out-of-tree (no codebase); brownfield inverts (in-codebase, partitioned-by-role). The unified tracks accept both as policy choices on shared substrate. BF-S's `OQ-T5` flags that the D-2 challenge may cascade into D-4 with structural consequences for the substrate/methodology boundary.
- **Relation to substrate primitives.** GF-S `S2 scenario storage`; BF-S `S-3 runtime/telemetry ingestor`; BF-L `codebase-model in-model partition`; U-A `policy mediator`; D7-U-1 `compounding gate`.

---

## D-Cost-Ceiling — Cost-ceiling enforcement discipline

- **One-line definition.** Hard cost ceilings (tokens, wall-clock, tool-calls) are substrate-enforced, non-optional, declared up-front; the substrate kills cycles at ceiling.
- **Governing principle.** D-5. CTR-E1 10× variance (Cherny $100K/mo vs $500-5000/day) is configuration; the *non-optional* property survives. CTR-E6 CaMeL ~7-point utility tax is admitted, not hidden.
- **Candidates that name it (with claim strength).**
  - All 10 tracks (`explicit-named`); D-5 marked across the board.
  - `GF-S` (no graceful-degradation mode; explicit refusal to absorb CaMeL utility-tax silently, [greenfield-substrate-first.md §1.S4](../tracks/greenfield-substrate-first.md)).
  - `U-A` (cost-ceiling breach is a substrate-fired re-entry trigger, [unified-A.md §4 D-5](../tracks/unified-A.md)).
  - `U-C` (per-distance ceilings: anchor-mutation queue carries higher ceiling than near-anchor cycles, [unified-C.md §4 D-5](../tracks/unified-C.md)).
  - `GF-M` (Regime-A paraphrase fan-out is the primary cost multiplier, ceilinged, [greenfield-methodology-first.md §1.3 / OQ-T2](../tracks/greenfield-methodology-first.md)).
- **Anchored corpus sources.** D-5 in brief §4.1; CTR-E1 (cost variance); CTR-E6 (CaMeL utility tax, followup 08 §3).
- **Open questions / debates across candidates.** Per-cycle flat vs per-phase / per-distance / per-layer is unresolved. GF-M's OQ-T2 names paraphrase fan-out as load-bearing-but-ceilinged tension. U-A §7 OQ-6 flags combined cost of immutable logging + cross-family judging + STIR cascade as corpus-unmeasured.
- **Relation to substrate primitives.** GF-S `S4 cost ceilings`; U-A `policy mediator`; BF-S `S-5 perimeter`.

---

## D-Watchdog — Watchdog-tier escalation discipline (Daemon / Triage / Patrol)

- **One-line definition.** Three substrate-resident watchdog tiers monitor liveness (Daemon, seconds), agent-stall ambiguity (Triage, seconds-to-minutes), and strategic drift across cycles (Patrol, hours+); each escalates by typed event.
- **Governing principle.** D-6 + Round-2 C14. F22 (zombie agents), F23 (stalled-vs-thinking), F34 (cross-layer drift), F54 (goal subversion), F55 (behavioural drift), F57 (design-authority erosion) require distinct cadences.
- **Candidates that name it (with claim strength).** All 10 tracks (`explicit-named`).
  - `GF-S` ([greenfield-substrate-first.md §1.S5](../tracks/greenfield-substrate-first.md)) — patrol guards operator-declared invariants since no historical baseline yet.
  - `BF-L` — Triage parameterised by codebase model; Patrol checks model drift ([brownfield-legacy-ingestion-first.md §4 D-6](../tracks/brownfield-legacy-ingestion-first.md)).
  - `GF-C` (Patrol structurally muted at cold-start because no baselines, [greenfield-cold-start-first.md §4 D-6](../tracks/greenfield-cold-start-first.md)).
  - `U-A` (three tiers map onto interval-policy enforcement, [unified-A.md §4 D-6](../tracks/unified-A.md)).
- **Anchored corpus sources.** [Glossary §0](../00-brief-v3.md); Round-2 C14; F22/F23/F34/F54/F55/F57 in [failure-modes-v3.md](../failure-modes-v3.md).
- **Open questions / debates across candidates.** Patrol's reference set differs: GF-S guards invariants (no historical baseline); BF-L guards model-against-reality; GF-C says Patrol is structurally muted until cold-start graduates. U-B makes Patrol's primary signal cross-layer drift.
- **Relation to substrate primitives.** GF-S `S5 watchdog tiers`; BF-S `S-4 attribution + S-2 dependency graph` (Patrol input); U-A `Patrol monitors interval history`.

---

## D-Regime-Classification — Eligibility / regime-classification discipline

- **One-line definition.** Lights-out applies *only* over a declared automation-eligible work-unit / regime / interval / distance-bucket surface; the classifier itself is substrate-typed, audited, and re-entry-triggering on drift.
- **Governing principle.** Brief §2.1 option (c)+(b). Vocabulary discipline: "lights-out" ≠ L5 (CTR-A4). Classification *drift* (F57) is the failure mode if eligibility is policy not substrate.
- **Candidates that name it (with claim strength).** All 10 tracks (`explicit-named`); near-universally adopt option (c)+(b).
  - `GF-S` `S9 eligibility classifier` substrate primitive ([greenfield-substrate-first.md §1.S9 / §2.A](../tracks/greenfield-substrate-first.md)).
  - `BF-L` model-driven classifier per region ([brownfield-legacy-ingestion-first.md §1 regime + §2.1](../tracks/brownfield-legacy-ingestion-first.md)).
  - `U-A` classifier substrate-typed; runs inside an interval, audit-able ([unified-A.md §1 / §7 OQ-2](../tracks/unified-A.md)).
  - `U-C` distance-gated dispatcher routes near / mid / far ([unified-C.md §1 primitive 3](../tracks/unified-C.md)).
  - `GF-C` graduation protocol from L3-Augmentation to per-class L4 ([greenfield-cold-start-first.md §1.3](../tracks/greenfield-cold-start-first.md)).
  - `BF-M` per-(work-unit-class × stage) bar clearance ([brownfield-methodology-first.md §2.1](../tracks/brownfield-methodology-first.md)).
- **Anchored corpus sources.** Report 09 §5.5 (Jaymin Augmentation / Automation thresholds); [CTR-A1 / A4 / A5 / H10](../contradictions.md); brief §0 glossary.
- **Open questions / debates across candidates.** Eligibility *granularity* — per work-unit (BF-S), per region (BF-L), per interval (U-A), per layer (U-B), per anchor-distance (U-C), per artifact-kind (D7-U-1). The cross-track question is whether classifier accountability scales (U-A OQ-2: "classifier is the architecture's most powerful actor"; F57 amplified).
- **Relation to substrate primitives.** GF-S `S9 classifier`; U-A `classifier`; U-C `distance-gated dispatcher`; BF-L `model-driven classifier`. Substrate-enforcement of *the classifier's decisions being typed and audited* is consistent across; the *content* differs.

---

## D-Trifecta-Closure — Lethal-trifecta closure discipline (closure-first / production-scissors-default-off)

- **One-line definition.** Production credentials, network access, and tool surface are substrate-default-disabled; explicit declarations escalate to a more-restricted closure profile; perimeter typing (CaMeL-class) replaces probabilistic guards on cross-sandbox calls.
- **Governing principle.** Lethal trifecta (F12 / F33 / F44 / F56). Shapiro R1-R5 hardening rules (report 32 §8.2). CaMeL NORMAL / STRICT interpreter modes (followup 08).
- **Candidates that name it (with claim strength).** All 10 tracks (`explicit-named`).
  - `GF-S` `S1 sandbox closure-first` ([greenfield-substrate-first.md §1.S1](../tracks/greenfield-substrate-first.md)).
  - `BF-S` (lethal trifecta is *constitutive of brownfield*; §0 reason 3, [brownfield-substrate-first.md §0 / §1.1 S-5](../tracks/brownfield-substrate-first.md)).
  - `GF-C` production-scissors-off default at first cycles ([greenfield-cold-start-first.md §1.2 sub-phase C](../tracks/greenfield-cold-start-first.md)).
  - `BF-L` model's `production-access-surface` view + substrate-enforced scissors-off makes Replit failure shape structurally not-available ([brownfield-legacy-ingestion-first.md §2.3 F56](../tracks/brownfield-legacy-ingestion-first.md)).
  - `U-A` interval-policy `approval-gate: required` + `sandbox` on every production-touching interval ([unified-A.md §2 F12/F33/F44](../tracks/unified-A.md)).
- **Anchored corpus sources.** Report 32 §8.2 (Shapiro R1-R5); followup 08 §3 (CaMeL); followup 10 §3 (Replit incident G14); Report 05 (Willison lethal-trifecta framing).
- **Open questions / debates across candidates.** CTR-C9 (Anthropic zero-network closure vs "dreaming") — GF-S resolves by treating dreaming as separate capability profile; BF-M flags as Phase-5 unresolved (§7 OQ-8).
- **Relation to substrate primitives.** GF-S `S1` + `S8 guard mediator`; BF-S `S-5 perimeter`; U-A `sandbox + approval-gate policies`.

---

## D-Three-Loop — Three-loop discipline (ingestion / work / maintenance)

- **One-line definition.** A brownfield factory has three distinct loops over a single durable artifact: ingestion (deep, one-time + delta-triggered), work (per-cycle), maintenance (continuous, low-cadence); each has different cost ceiling, judge profile, and watchdog cadence.
- **Governing principle.** F20 (maintenance-vs-greenfield asymmetry, brownfield-critical); F34 (cross-layer drift); F55 (behavioural drift / self-reference loop); F57 (design-authority erosion). The codebase model drifts; a maintenance loop reconciles.
- **Candidates that name it (with claim strength).**
  - `BF-L` (`explicit-named`) — the entire architecture: "three loops over a single durable artifact" ([brownfield-legacy-ingestion-first.md §1](../tracks/brownfield-legacy-ingestion-first.md)).
  - `BF-S` (`inferable`) — legacy-ingestion-as-one-time substrate setup, but maintenance is incremental-on-every-commit, framed as substrate operation not separate loop ([brownfield-substrate-first.md §1.1 / §5](../tracks/brownfield-substrate-first.md)).
  - `BF-M` (`inferable`) — stage 2 (Comprehension) is the brownfield-analog of cold-start; legacy-ingestion treated as stage-2 cost not separate meta-stage ([brownfield-methodology-first.md §5](../tracks/brownfield-methodology-first.md)).
  - GF-* tracks: `silent` (no codebase to ingest yet).
  - U-A, U-B, U-C, D7-U-1: `inferable` but not load-bearing — they treat brownfield ingestion as a kind of interval / layer / FC-catalog warming, not as a distinct loop.
- **Anchored corpus sources.** F20 anchor: El Kaim per [archive/synthesis-v1-v2/00-synthesis.md §4]; CTR-G3 (legacy-ingestion symmetry question); Report 38 (Beads `discovered-from` edge); UC4.
- **Open questions / debates across candidates.** Is legacy-ingestion symmetric to greenfield cold-start (CTR-G3)? BF-S explicitly says no (one-time setup vs recurring methodology problem); BF-L explicitly says it might deserve parallel discipline. BF-L's `OQ-1` flags ingestion-as-substrate vs ingestion-as-methodology as a Phase-4 decision.
- **Relation to substrate primitives.** BF-L `codebase model`; BF-S `S-1 codebase index + S-2 dependency graph + S-3 telemetry + S-4 attribution + S-5 perimeter`. The discipline is *how the loops divide labour over those primitives*.

---

## D-Spec-Lint / D-Deterministic-Perimeter — Deterministic-perimeter-at-authoring discipline

- **One-line definition.** Spec / intent / acceptance-criteria pass through deterministic rule-based linters (EARS grammar, INCOSE GtWR R7/R8/R9, requirement-count budgeter) *before* any LLM-judge runs; deterministic checks where possible, probabilistic guards only when no deterministic option exists.
- **Governing principle.** F38 (vocabulary lint debt) is deterministically catchable. F51 (Ashby-deficient probabilistic guard) means LLM-judges have variety ceilings. F52 (Tempting-Wrong-Hybrid, Schillace Letter 11) caps the number of deterministic wrappers.
- **Candidates that name it (with claim strength).**
  - `GF-S` `S8 guard mediator` (four deterministic guards: GtWR lint, contradiction-detector, requirement-count budgeter, perimeter typing — [greenfield-substrate-first.md §1.S8](../tracks/greenfield-substrate-first.md)).
  - `GF-C` GtWR/EARS linter is deterministic rule engine, not LLM-as-judge ([greenfield-cold-start-first.md §1.1 primitive 2; §5 protection #1](../tracks/greenfield-cold-start-first.md)).
  - `GF-M` Phase-1 EARS/GtWR lint at substrate, single deterministic wrapper named explicitly to defend against F52 ([greenfield-methodology-first.md §1.1 phase 1; §2.9 F52 line](../tracks/greenfield-methodology-first.md)).
  - `BF-M` deterministic GtWR R7/R8/R9 lint on change-intent block ([brownfield-methodology-first.md §1.1 stage 3 / §2.5 F38 + F51](../tracks/brownfield-methodology-first.md)).
  - `U-A` `kind: spec-author` interval policy mandates EARS/GtWR lint ([unified-A.md §5.3 gate](../tracks/unified-A.md)).
  - `U-B` L2 layer is EARS-typed + GtWR-linted at substrate ([unified-B.md §2.5 F36/F37/F38/F39](../tracks/unified-B.md)).
  - `U-C` operator scaffolded by INCOSE GtWR C1-C15 + EARS at intent authoring ([unified-C.md §5 Step 0](../tracks/unified-C.md)).
  - `BF-S` `S-5 deterministic perimeter` ([brownfield-substrate-first.md §1.1 S-5](../tracks/brownfield-substrate-first.md)).
  - `BF-L` `inferable` (substrate enforces invariants extracted from tests/types but does not separately name an authoring linter).
  - `D7-U-1` deterministic-checker is one of four `opposing-side.kind` values; spec FCs include GtWR/EARS deterministic check ([d7-u-1-prohibit-interval-escrow.md §2 F36/F37/F38/F39](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)).
- **Anchored corpus sources.** Report 25 §2 / §3 (EARS, INCOSE GtWR); Report 26 §3.4 (Yang et al. 98.7→85.0% as 1→19 requirements); F36, F37, F38, F39, F51, F52.
- **Open questions / debates across candidates.** Schillace F52 imposes a hard cap (GF-S: "four guards full stop"; GF-M: "only one deterministic wrapper") on how many deterministic layers can accrete. U-B §7 OQ-PLEF-8 explicitly raises the F52-risk of the pace-layer-as-deterministic-wrapper. The disagreement is not whether to lint, but how far up the stack determinism can go without triggering Schillace.
- **Relation to substrate primitives.** GF-S `S8`; BF-S `S-5`; U-A `gate.deterministic` policy; U-C `contradiction-flag` in distance estimator.

---

## D-Cognitive-Escrow / D-Interval-as-Design-Site — Cognitive-escrow / interval-as-design-site discipline

- **One-line definition.** The interval between when an instruction leaves human possession and when consequences return is a first-class design surface; the substrate fires reflection prompts, success-criterion articulations, similar-past surfacing, STIR cascade, and delegation-level confirmations *structurally* (not voluntarily) at the interval.
- **Governing principle.** F42 (Cognitive Escrow negligence, Kahana); F53 (voluntary-discipline fragility). Same-mechanism as D-Substrate-Enforcement, but the *site* is specifically the prompt→response / handoff interval.
- **Candidates that name it (with claim strength).**
  - `U-A` (`explicit-named`, foundational — the entire architecture is built on `EscrowInterval` substrate-typed object, [unified-A.md §0 / §1](../tracks/unified-A.md)).
  - `U-B` (`explicit-named`, foundational — every layer transition IS an escrow interval, [unified-B.md §0 / §1 / §5.3](../tracks/unified-B.md)).
  - `GF-C` (`explicit-named` — Cognitive-Escrow-Aware Operator Surface is a day-0 substrate primitive, [greenfield-cold-start-first.md §1.1 primitive 4](../tracks/greenfield-cold-start-first.md)).
  - `GF-M` (`explicit-named` — Phase-1 and Phase-4 operator-touchpoints are escrow-interval design sites, [greenfield-methodology-first.md §1.3 cognitive escrow primitive](../tracks/greenfield-methodology-first.md)).
  - `BF-M` (`inferable` — F42 mitigation at stage 8: PR body bundles change-intent + brief + trajectory + failed line, [brownfield-methodology-first.md §2.5 F42](../tracks/brownfield-methodology-first.md)).
  - `GF-S` (`inferable` — STIR-in-the-interval is named as one direction in §7 open question 8, [greenfield-substrate-first.md §5.5 / §7.8](../tracks/greenfield-substrate-first.md)).
  - `U-C` (`inferable` — F42 acknowledged but at methodology, not primitive, [unified-C.md §5 step 3](../tracks/unified-C.md)).
  - `BF-S`, `BF-L`: `silent` to `inferable`.
  - `D7-U-1` (`rejects` — explicitly refuses to promote interval-as-substrate; "the substrate does not promote attention-surface design to a primitive"; methodology may still treat it as load-bearing, [d7-u-1-prohibit-interval-escrow.md §0 reason 4; §2 F42; "Honest assessment"](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)).
- **Anchored corpus sources.** Report 30 (Kahana cognitive escrow); F42, F53 in [failure-modes-v3.md](../failure-modes-v3.md); Report 28 §6 (Schillace Attention Firewall); Report 35 (Notion standup pre-read).
- **Open questions / debates across candidates.** The D7-U-1 blind-axis explicitly tests whether substrate-promotion of escrow is *load-bearing* or *one of two convergence patterns* (the other being opposing-side discipline). D7-U-1's "honest concession": opposing-side topology does *not* close F42 at substrate; escrow-flavoured architectures are *stronger* there. The "two-things-both-true" recommendation in D7-U-1 stands as the cross-candidate verdict: the corpus signals both clusters and the architecture set should carry both.
- **Relation to substrate primitives.** U-A `EscrowInterval object store + policy mediator + re-entry registrar`; U-B `escrow primitive at every layer transition`; GF-C `Cognitive-Escrow-Aware Operator Surface`; GF-M / GF-S name it as methodology / open-question primitive.

---

## D-Knowledge-Promotion — Knowledge-promotion / pattern-promotion discipline

- **One-line definition.** Patterns, insights, corrections, and skills accumulated per-cycle are *promoted* through typed gates (provisional → durable; pattern → standard; reversible → frozen-anchor) rather than committed silently.
- **Governing principle.** Compound-Knowledge four-way classification (insight / playbook / correction / pattern); F8 (stale-knowledge inversion); F55 (behavioural drift / self-reference loop) is acute when knowledge accumulates without explicit promotion gates.
- **Candidates that name it (with claim strength).**
  - `GF-M` `promote-or-reverse` is the cycle's Phase-4 gate; reversal is cheap by design ([greenfield-methodology-first.md §1.1 phase 4](../tracks/greenfield-methodology-first.md)).
  - `BF-S` "Knowledge promotion" is named methodology obligation; Beads `discovered-from` edge ([brownfield-substrate-first.md §1.2 / §1.3 step 8](../tracks/brownfield-substrate-first.md)).
  - `BF-M` knowledge typing (followup 11 four-way) with `kw:confidence`; stale-knowledge is *next reader's obligation*, not curator daemon ([brownfield-methodology-first.md §1.2](../tracks/brownfield-methodology-first.md)).
  - `U-B` pattern → Skill → enforced standard pace-layer promotion (Brier); each cycle's repeatable pattern is candidate for promotion to `anchor.kind=standards-rule` ([unified-B.md §1 knowledge store; §5 day-7-to-30](../tracks/unified-B.md)).
  - `U-C` (`explicit-named`) — "Pattern → standard promotion" is the explicit anchor-set growth mechanism; promotion is an `anchor-edit` work unit (always L4-classified, [unified-C.md §5 step 2](../tracks/unified-C.md)).
  - `GF-C` graduation protocol promotes work-unit-classes from Cold-Start (L3) to Steady-State (L4-eligible) ([greenfield-cold-start-first.md §1.3](../tracks/greenfield-cold-start-first.md)).
  - `D7-U-1` survival-window registrar — when a window expires, dependent artifacts are re-falsified ([d7-u-1-prohibit-interval-escrow.md §1.3 primitive 5](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)).
  - `GF-S` `inferable` — knowledge accumulation deferred to methodology layer ([greenfield-substrate-first.md §2.H OQ-B9](../tracks/greenfield-substrate-first.md)).
  - `BF-L` Loop-3 maintenance reconciles model with reality; promotion is methodology-side over substrate-stored knowledge.
- **Anchored corpus sources.** Followup 11 (Compound Knowledge typed-learnings); F8, F55 in [failure-modes-v3.md](../failure-modes-v3.md); Report 38 (Beads `discovered-from` edge); Brier followup 12 §6.
- **Open questions / debates across candidates.** Is promotion methodology or substrate? GF-S / BF-S / BF-M put it methodology-side; U-C makes anchor-edit a typed work-unit-class; D7-U-1 substrate-types it as survival-window. CTR-C3 (self-improvement as methodology pattern vs substrate primitive) is the broader name.
- **Relation to substrate primitives.** BF-S `S-4 attribution + Compound-Knowledge store`; U-C `anchor mutation queue`; D7-U-1 `survival-window registrar`.

---

## D-Honesty — Honesty / no-fabrication discipline (corpus + buildability + RG flags)

- **One-line definition.** Substrate primitives carry construction paths or are flagged research-grade; corpus citations are required for the *why*; tracks do not pretend evidence they lack ("the substrate cannot author the day-0 intent block; operator labour is irreducible").
- **Governing principle.** Phase-3.4 working-definitions rule 3 ("Buildability is mandatory. 'Just assume `CodebaseModel` exists' is handwaving and is rejected"). [phase-3.4-decisions-resolved.md "Refined two-part rule"](../phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive). Scoping principle. Bias-guard discipline carrying through.
- **Candidates that name it (with claim strength).**
  - `GF-C` (`explicit-named`) — "Honesty discipline: at cold-start the factory cannot claim to have cleared *any* empirical bar; the graduation protocol is the act of earning the claim" ([greenfield-cold-start-first.md §2 OQ-B6](../tracks/greenfield-cold-start-first.md)).
  - `U-C` (`explicit-named`) — "F25 (design starvation) is addressed by ADF's regime declaration: in cold-start, work-unit throughput is *expected* to be human-bottlenecked because all work is far-anchor; no lights-out promise is made. This is honest scope rather than mitigation" ([unified-C.md §5 step 3](../tracks/unified-C.md)).
  - All tracks (`inferable`) — every track explicitly section-§6 names what it is "not trying to be" and §7 surfaces open questions (corpus-grounded honesty about scope and gaps).
  - `GF-S` §5.5 "What cold-start does NOT solve" is structurally honest about F40 last-mile drift.
  - `D7-U-1` "Honest assessment" section: explicitly concedes its track does *not* close F42 at substrate, and recommends both architectures be carried ([d7-u-1-prohibit-interval-escrow.md "Honest assessment"](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)).
- **Anchored corpus sources.** Brief §0 (measurement vs normative dependency); [phase-3.4-decisions-resolved.md](../phase-3.4-decisions-resolved.md). This discipline is largely process-level (Phase-2 dispatch shape) rather than corpus-anchored, *and that is itself a candidate fact about its scope* — flag for lead-agent.
- **Open questions / debates across candidates.** No candidate disagrees; the discipline is process-level rather than design-level. Inferable consensus.
- **Relation to substrate primitives.** N/A. This discipline lives at the architecture / dispatch / authoring level. RG-flagging of substrate primitives is the closest substrate instance (handled in Subagent-2's primitives output).

---

## D-Scoping — Scoping-principle discipline (carry-every-defensible-candidate)

- **One-line definition.** Phase-3 does not eliminate candidates with defensible supporting arguments; pressure-testing happens at Phase-8 lean-eval and downstream simulation, not at end-of-Phase-3.
- **Governing principle.** [phase-3.4-decisions-resolved.md scoping principle](../phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief). User-declared, immutable. No public source has detailed a working software-factory architecture; narrowing forecloses crossover.
- **Candidates that name it (with claim strength).** This is a *process discipline*, not an architecture-level discipline named per-candidate. Tracks observe it by being authored at all and by §6 ("Not trying to be") + §7 ("Open questions") sections that surface adversarial-attack surfaces rather than defend against them.
  - `D7-U-1` (`explicit-named`) — the "two-things-both-true" / "carry both" recommendation IS an application of the scoping principle ([d7-u-1-prohibit-interval-escrow.md "Recommendation"](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)).
  - All other tracks (`inferable`).
- **Anchored corpus sources.** User direction (phase-3.4-decisions-resolved.md). Not corpus-derived; flag as project-level rather than research-anchored.
- **Open questions / debates across candidates.** None within scope.
- **Relation to substrate primitives.** N/A.

---

## Disciplines flagged for lead-agent attention (out-of-scope-here-but-architecture-level)

These disciplines are *named in AGENTS.md or the registry / brief but are weakly or not at all visible in the track scope*. Subagent-2 (registry / primitives) is the right surface to extract them. Flagged here so the lead-agent merge does not lose them:

- **D-Real-Subagent-Review** ([AGENTS.md "Adversarial review MUST be real subagents"](../../../AGENTS.md#adversarial-review-must-be-real-subagents)) — codified post-PR-#144; not in track scope; closest track surface is the bias-guard / adversarial-review discipline above, but that is *content* (judge diversity) not *process* (real-subagent dispatch vs lead-agent simulation).
- **D-Three-Layer-Citation** (corpus → candidate-claim → primitive). Tracks heavily cite the corpus and use load-bearing-claim mapping (§3 of every track) but do not name a "three-layer" discipline. The pattern is *inferable* from §3 ("Citations and grounding") structures; the *name* is not in scope here.
- **D-Concrete-Task** (each subagent gets concrete, bounded scope) — this dispatch-level discipline, named in [phase-3.4-integration-brief.md] and across phase-3.x decision docs. Tracks instantiate it (each is concretely scoped to mandate + axis) but do not articulate it as a discipline.
- **D-Internal-Document-References** ([AGENTS.md "Internal document references"](../../../AGENTS.md#internal-document-references)) — process discipline; tracks follow it (relative paths, descriptive link text) but do not articulate it.
- **D-Graceful-Degradation** (when an RG primitive falls back). GF-S explicitly *rejects* graceful degradation as silent absorption of CaMeL utility tax ([greenfield-substrate-first.md §1.S4](../tracks/greenfield-substrate-first.md)); other tracks are mostly silent. Whether this is a single cross-track discipline or a per-candidate choice is *unclear from track scope*; flag for lead-agent merge.

---

*End of track-driven discipline index.*

---

# Substrate-layer disciplines (merged in at Wave 4.6 from sketch/registry extraction)

The following disciplines surface predominantly at the substrate / decision-brief / cross-cutting layer rather than in candidate tracks. They were extracted by the parallel Wave-4.3 sketch-and-registry subagent (full extraction preserved in [`sketch-registry-extracted-disciplines.md`](sketch-registry-extracted-disciplines.md) for traceability). Each is named here with its substrate-layer surfaces, reconciliation note vs the track-driven disciplines above, and its relation to specific primitives.

## D-Construction-Path-Plus-Corpus-Why — Two-part rule for substrate primitive admission

- **One-line definition.** Every substrate primitive admitted to the catalog must ship (i) a construction path naming concrete tools/libraries with an integration sentence per primitive, and (ii) a corpus citation for *why* the primitive solves a corpus-named problem.
- **Governing principle.** Per [phase-3.4-decisions-resolved.md § Refined two-part rule](../phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive) (`binding-rule`). "It is handwaving to just assume something like `CodebaseModel` just exists."
- **Surfaces in.** Every per-primitive sketch (P-14–P-34) and cluster sketch (C1/C2/C3) is structured by this rule (`explicit-named`); [`auto-001` Round-2 amendments](../decisions/auto-001-phase-3.5-dispatch-shape.md#amendments-to-the-dispatch-brief-that-will-be-sent-to-subagents) sharpened it to "named tool + integration sentence + specific corpus problem."
- **Reconciliation with track-driven D-Honesty.** Partial overlap (both require evidence). This discipline is the *substrate-side enforcement mechanism* for D-Honesty's no-fabrication norm on construction paths. Track-driven D-Honesty extends to methodology-level scope claims; the two are *complementary not identical*.
- **Relation to specific primitives.** Universal — every P-NN sketch is an instance.

## D-RG-Primitive-Rule — Bounded-sub-track-or-accept-as-RG per RG-portion

- **One-line definition.** Any candidate carrying a load-bearing research-grade-uncertainty primitive must choose, per RG-portion, between (a) committing to a bounded authoring sub-track to convert RG content to designed-system, or (b) downgrading the dependent contract to accept-as-RG with substrate documenting the gap and methodology specifying graceful degradation.
- **Governing principle.** Symmetry across candidates; no per-candidate ad-hoc lifelines. Same toolkit (a/b with defaults) governs every RG primitive. Per [candidate-registry.md § Phase-3.5.5 RG-primitive rule](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25) (`binding-rule`, user-approved 2026-05-25).
- **Surfaces in.** [`auto-002 Round 2`](../decisions/auto-002-ub-path.md) (U-B P-31 smoke-test); [`auto-003 Round 2`](../decisions/auto-003-bfl-rg-view-choice.md) (BF-L per-view smoke-tests); [`P-34`](../primitives/P-34-independence-auditor.md) (A+C hybrid as combined a+b application). Wave-4.5 sub-track verdicts apply this rule.
- **Reconciliation with track-driven disciplines.** Substrate-only — born post-tracks at the Phase-3.5.5 close. Not in the track scope.
- **Relation to specific primitives.** P-26 (BF-L conventional + invariant views); P-31 (U-B); P-34 (D7-U-1); partial-RG on P-15, P-17, P-21, P-25, P-27, P-32.

## D-Same-vs-Distinct-Deferred — Substrate-matching is methodology-downstream

- **One-line definition.** Buildability-sketch subagents are forbidden from declaring whether two candidates' superficially-similar primitives are "the same." Each variant gets its own contract paragraph; collapse is reserved for the Phase-4.2 lead-agent diff.
- **Governing principle.** Substrate-matching is downstream-methodology work; premature collapse forecloses cross-candidate variety the scoping principle protects.
- **Surfaces in.** [`primitives/index.md` § Scope discipline](../primitives/index.md) (`binding-rule`); [`auto-001` Round-2 cluster-subagent constraints](../decisions/auto-001-phase-3.5-dispatch-shape.md#amendments-to-the-dispatch-brief-that-will-be-sent-to-subagents). Operationalized by Wave 4.2 [`overlap.md`](../primitives/overlap.md).
- **Reconciliation with track-driven disciplines.** Substrate-only — process discipline born of the Phase-3.5 sketch-dispatch shape. Tracks predate it.
- **Relation to specific primitives.** P-28, P-29, P-30, P-19 contested variants; P-08↔P-09 collapse; P-12↔P-16 absorption; P-14↔P-33 distinction.

## D-Real-Subagent-Review — Adversarial review MUST be real subagents

- **One-line definition.** Adversarial review of any lead-agent-authored decision brief, design proposal, plan, or artifact MUST use real subagent dispatches (the `Agent` tool), not inline-simulated reviewers written as prose.
- **Governing principle.** Per [AGENTS.md § Adversarial review MUST be real subagents](../../../AGENTS.md#adversarial-review-must-be-real-subagents) (`binding-rule`, codified PR #144 retrospective). Inline-simulated reviewers inherit the lead agent's anchoring on the chosen option; they look like adversarial pressure but exert none.
- **Surfaces in.** AGENTS.md; auto-001 Round 2; auto-002 Round 2; auto-003 Round 2; auto-004 Round 2 (every decision brief in the catalog applies this rule explicitly).
- **Reconciliation with track-driven D-Bias-Guard.** D-Bias-Guard is about *content* (opposing-side judge diversity within the architecture). D-Real-Subagent-Review is about *process* (how decision briefs are reviewed during the synthesis pipeline). Complementary, not identical.
- **Relation to specific primitives.** N/A — process discipline.

## D-Per-Role-Read-Filter — ABAC partition at the read API, not the filesystem

- **One-line definition.** Holdout enforcement, builder/judge separation, and role-based access are implemented as ABAC policy at the substrate read-API layer, not as filesystem permissions or directory layout.
- **Governing principle.** Substrate-enforcement applied to information-flow boundaries. Per the [cluster-C2 sketch § P-07](../primitives/cluster-C2.md) and [cluster-C3 § P-08](../primitives/cluster-C3.md): the storage half is commodity; the ABAC integration is the design content.
- **Surfaces in.** P-07 (telemetry ingestor); P-08 (scenario storage); BF-S B7 partition-leakage analysis (P-23 sketch's "rate-limited side channel" conclusion).
- **Reconciliation with track-driven D-Holdout.** D-Holdout is the *what* (training/holdout partition); D-Per-Role-Read-Filter is the *how* (ABAC mechanism). The new discipline tightens D-Holdout's substrate enforcement claim.
- **Relation to specific primitives.** P-07, P-08, P-25 (CaMeL perimeter).

## D-Typed-Envelope — Substrate-typed-store discipline

- **One-line definition.** Substrate stores (P-28 variants, P-10, P-11, P-18, P-24) carry a typed envelope with content-hash addressing + append-only discipline + typed-filter primary axis declared at admission time.
- **Governing principle.** The envelope schema is the integration contract; the storage is commodity. Multiple candidates' variants can coexist on one substrate provided their envelope namespaces are disjoint (per [Wave 4.2 overlap.md § P-28](../primitives/overlap.md#p-28-typed-object-store--four-contested-variants)).
- **Surfaces in.** P-28 (4 variants); P-10 coordination medium; P-11 Cold-Start Bench; P-18 RSI Ledger; P-24 attribution store.
- **Reconciliation with track-driven disciplines.** Substrate-only — tracks name their stores without articulating the typed-envelope discipline. Surfaced by the sketch-driven extraction.
- **Relation to specific primitives.** P-28 (load-bearing); P-10, P-11, P-18, P-24 (instances).

## D-Snapshot-Consistency-at-Version-Boundaries

- **One-line definition.** Versioned substrate artifacts (P-26 Codebase Model; P-08 scenario store; P-18 RSI Ledger) maintain snapshot consistency at version boundaries; per-cycle queries pin a version at dispatch; the cycle does not see mid-cycle changes.
- **Governing principle.** F34 (cross-layer drift) defence at the model level. Eventually-consistent within an ingestion pass; consistent across versions.
- **Surfaces in.** P-26 sketch (Integration discipline section); P-13 maintenance loop; P-08 scenario storage's append-only discipline.
- **Reconciliation with track-driven disciplines.** Substrate-only — sharpest in P-26 sketch; tracks observe it inferentially.
- **Relation to specific primitives.** P-26, P-13, P-08, P-18.

## D-Honest-RG-Flag — "Say so explicitly" honesty clause for RG primitives

- **One-line definition.** When a primitive or sub-component is research-grade-uncertain, the substrate documentation says so explicitly with named gaps; fabricated construction paths without corpus support do not count.
- **Governing principle.** Operationalizes track-driven D-Honesty at the substrate-primitive layer. Per [P-31 smoke-test § Honesty discipline](../primitives/P-31-smoke-test-invariants.md) (verbatim: "If a layer-pair has no corpus-citable non-trivial invariant, this report says so explicitly and names the gap — fabricated invariants without corpus support do not count").
- **Surfaces in.** P-26 sketch; P-31 sketch + smoke-test; P-34 sketch; P-32 sketch (partial-RG on calibration); auto-002 Round 2 + auto-003 Round 2 reviewers' enforcement.
- **Reconciliation with track-driven D-Honesty.** Substrate-layer specialization of D-Honesty. The track-driven discipline is the umbrella; this is the substrate-primitive-layer enforcement mechanism.
- **Relation to specific primitives.** P-26, P-31, P-32, P-34 (load-bearing RG); P-15, P-17, P-21, P-25, P-27 (partial-RG).

## D-Decision-Brief-Rewind-Pointer — Decisions are reversible

- **One-line definition.** Every `decisions/auto-NNN-*.md` brief carries an explicit rewind point (a named commit SHA or branch state) so any decision can be reverted without losing downstream work.
- **Governing principle.** "Make every decision rewindable." Per the project's unattended-mode discipline.
- **Surfaces in.** Every `auto-NNN` brief (auto-001 through auto-004); SESSION-HANDOFF docs; the overnight-summary.md.
- **Reconciliation with track-driven disciplines.** Substrate-only — process discipline born of the synthesis pipeline. Tracks don't observe it (tracks are not decision briefs).
- **Relation to specific primitives.** N/A — process discipline.

---

## Reconciliation summary (Wave 4.6 merge)

**21 disciplines total** in the canonical index: 13 track-driven + 8 substrate-layer (with 4 substrate-layer disciplines from the sketch-registry extraction reconciled as overlapping with track-driven entries and dropped: substrate-enforcement-not-operator-voluntary → matches D-Substrate-Enforcement; honest-RG-flag-flagging → folded into substrate-only D-Honest-RG-Flag (a specialization) above; cross-family-judge-diversity → matches D-Bias-Guard; graceful-degradation → moved to track-driven flagged-for-attention list as ambiguous-per-candidate).

**Dropped overlap notes (for Wave-5 ADR authors):**
- *Substrate-enforcement-not-operator-voluntary* and D-Substrate-Enforcement are the same discipline. Use D-Substrate-Enforcement.
- *Cross-family / opposing-side judge diversity* and D-Bias-Guard are the same discipline. Use D-Bias-Guard.

**Track-driven flagged-for-attention items resolved by the substrate-layer merge:**
- *D-Real-Subagent-Review* → captured here (substrate-layer).
- *D-Three-Layer-Citation* → not surfaced by either subagent's read scope; carries forward as an open discipline-extraction question (it exists in `phase-3.4-integration-brief.md` but neither subagent's read scope covered it deeply). Not landed at Wave 4.6; carries to Phase 5/6 as informal.
- *D-Concrete-Task* → process-level (dispatch); carries forward as informal.
- *D-Internal-Document-References* → process-level (codified in AGENTS.md); informal.
- *D-Graceful-Degradation* → substrate-layer extraction did not name it as a distinct discipline either; it is a per-candidate choice expressed via the (b) option of the RG-Primitive-Rule (see D-RG-Primitive-Rule above). NOT a separate cross-cutting discipline; carries forward as RG-Primitive-Rule application.

**Per-discipline stubs status.** Stubs for the 13 track-driven disciplines exist in this directory (`bias-guard.md`, `substrate-enforcement.md`, etc.). The 8 substrate-layer disciplines do not yet have stub files — the lead-agent merge intentionally left these as index-only entries (referencing the sketch-registry-extracted file for full content) per the Wave 4.6 cost discipline. Stubs can be authored at Phase 5 ADR dispatch time as needed.
