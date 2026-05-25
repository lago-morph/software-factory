---
guard: cross-mandate-unified-fails-greenfield
target: draft-unified-synthesis
phase: 3.3
based-on-commit: 52f4fb9
based-on-date: 2026-05-25
---

# Phase-3.3 `X_UNM_G` — unified-fails-greenfield falsification test

## §1 Stance

The unified architecture cannot work for greenfield because its day-0 substrate is *under*-specified at exactly the moment greenfield is *over*-vulnerable. The unified draft trades the greenfield draft's authorable Intent-Crucible-shaped day-0 primitives (ROBUST-G4/G5/G6/G7/G8) for an abstract typed-object substrate whose **bootstrap shape is not yet authored by anyone in the room at day 0**. The unified draft openly concedes this in DPU-1 ("Pick one typed-object as the substrate-primitive granularity… Phase-5 wave-1 ADRs cannot proceed without this choice") and DPU-5 (cognitive-escrow promotion is single-source F-ANCHOR-2). The unified architecture's primitive is one level of abstraction too far from the El Kaim/EARS surface the corpus warrants for cold-start.

## §2 Top attack findings

**A. The typed-object primitive's bootstrap shape is not authorable at day 0 — and the unified draft admits it.** Yang et al. (report 26 §3.4, gpt-4o 98.7%→85.0% as requirements grow 1→19) and Larbi (MCC ≤ 0.55 for single-judge contradiction detection) together establish that operators cannot reliably specify 10–20 simultaneous requirements without **deterministic, format-bound scaffolding at the artifact surface**. The greenfield draft answers this with ROBUST-G6 (deterministic GtWR/EARS lint, fail-closed, *not* LLM-judge) and ROBUST-G7 (requirement-count budgeter chunking at Yang ceiling). The unified draft offers ROBUST-U7 *inside* an `EscrowInterval`/layer/anchor envelope whose shape DPU-1 explicitly defers. At day 0 the operator must author *two* things: the EARS spec *and* the typed-object choice that wraps it. The corpus warrant is for the *first* artifact only. **Severity: critical.**

**B. EscrowSurface promotion to substrate amplifies F42/F53 under unified factories.** Kahana (report 30 §1) describes the operator-attention-fragility problem for *one* factory operating against *one* codebase. A unified factory carrying both greenfield and brownfield work expands the multi-strand cognitive-escrow burden by adding **mandate-context-switching** to agent-count-switching. The greenfield operator at day 0 is uniquely vulnerable: authoring everything from scratch *and* receiving substrate-fired reflection questions *and* being context-switched into archaeology questions on a parallel codebase. U-B OQ-5 names exactly this verbatim ("the operator's *response* to substrate-fired escrow primitives is itself voluntary"). **Severity: high.**

**C. Graduation criteria are not measurable when the substrate is also handling brownfield.** ROBUST-U14 lists *three abstract* criteria. The greenfield draft DPG-4 lists *four concrete* criteria (bench saturation; Jaymin K=5 baseline; cross-model judge agreement; RSI-declaration cadence). Three of those four are *measured against the greenfield work-unit-class itself*. Under the unified architecture's mandate-as-parameter framing, the same substrate is concurrently producing brownfield work-units that exercise different feature inputs. **The graduation primitive is not load-bearing across mandates; it is theoretical.** Without measurable graduation, the cold-start protections of ROBUST-U12 cannot be safely lifted. **Severity: critical.**

**D. The cold-start required-reading set does not warrant a unified-architecture cold-start.** Report 30 (cognitive escrow) is greenfield-shaped — Kahana's worked examples are *lawyer/clinician operators authoring intent*, not maintaining a codebase model. Report 31 (Caremark RSI) is explicitly *mid-market-scope* — its three-part test is a *brownfield-RSI* test, not a greenfield-cold-start test. Followup/10 (governance, AILCCP) is brownfield-shaped — the AILCCP controls were drained against StrongDM, BCG, MacGregor. Only reports 25 + 26 have genuine greenfield-cold-start warrant. The unified draft inherits brief §5's reading list *as if* it applies symmetrically. **Severity: medium-high.**

**E. The four-default-challenge cluster D-2/D-3/DPU-2 is structurally heavier for greenfield day-0.** Greenfield's `priors.out-of-tree` slot is structurally vacuous at day 0 — the operator has no out-of-tree scenarios *yet*. The unified architecture's defense asserts a slot but does not *populate* it. **Severity: medium.**

## §3 What the unified architecture concedes

The unified draft is unusually honest about its day-0 exposure. ROBUST-U12 commits to the *same* day-0 conservatism as ROBUST-G1. ROBUST-U13 re-uses the El Kaim 9-field intent block — i.e., it has *not* invented a unified-bootstrap primitive; it has wrapped the greenfield-bootstrap primitive in a typed envelope. To that extent, the unified architecture inherits the corpus warrant the greenfield draft built. The attack lands not on the *artefact set* but on the *primitive that wraps it*: the unified draft owes a DPU-1 resolution before the wrapping primitive exists.

DPU-8 names the present test as the resolution mechanism for whether UC4 falsifies. The draft does not claim to have survived it pre-emptively.

## §4 Verdict for Phase-3.4

**Partial survival — requires modifications.** The unified architecture does not fail outright for greenfield: its day-0 artefact set is the greenfield draft's day-0 artefact set, and ROBUST-U12's L3-Augmentation commitment closes the most acute exposure. But it cannot survive *as currently specified* because:

(a) DPU-1 must resolve before any operator can author the bootstrap typed object,
(b) DPU-5's substrate-promotion of EscrowSurface compounds F42/F53 in the multi-mandate case,
(c) ROBUST-U14's three abstract graduation conditions cannot be operationally measured when the substrate is also producing brownfield work.

UC4 is **partially confirmed for greenfield**: the typed-object substrate can host the greenfield-bootstrap artefacts, but at the cost of an additional Phase-5 ADR (DPU-1) that the greenfield-only architecture does not need. If the unified architecture is to proceed, it owes Phase-3.4 (i) a default DPU-1 resolution selected *for greenfield day-0 specifically* (likely U-C's anchor-typed-object since `intent-block-invariants` is the only stable anchor at day 0), (ii) a `RegimeClassifier` feature-set explicitly separating greenfield-day-0 from brownfield work-units to prevent cross-mandate calibration leakage, and (iii) the four DPG-4 concrete graduation criteria adopted as defaults for greenfield work-unit-classes regardless of the unified envelope.

The substantive recommendation for Phase-4: greenfield day-0 primitives (intent block, EARS lint, Yang budgeter, paraphrase divergence) should remain *greenfield-mandate-specific* even under a unified envelope. The unification can hold at the AttributedEventLog/PerimeterClosure/TypedJudgeCall layer (ROBUST-U5/U8/U9 — these *are* mandate-neutral), but the cold-start cluster should be marked mandate-specific in the divergence document.
