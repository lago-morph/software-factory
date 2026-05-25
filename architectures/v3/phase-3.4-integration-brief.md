---
artifact: phase-3.4-integration-brief
phase: 3.4
based-on-commit: 6f0a3cf
based-on-date: 2026-05-25
inputs:
  - draft-greenfield-synthesis.md
  - draft-brownfield-synthesis.md
  - draft-unified-synthesis.md
  - bias-guards/phase-3/greenfield/*.md (6 critiques)
  - bias-guards/phase-3/brownfield/*.md (6 critiques)
  - bias-guards/phase-3/unified/*.md (6 critiques)
  - bias-guards/phase-3/cross-mandate/*.md (4 falsification tests)
  - bias-guards/phase-3/d7-blind-axis/*.md (2 blind-axis tests)
---

# Phase 3.4 Integration Brief

**Status.** All 24 Phase-3.2 + Phase-3.3 + D7 subagents have landed. This brief compiles the integrated findings and the user-decision items required before the three `*-synthesis-v1.md` files can be written. Per the [`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) §Phase-3.4 checkpoint, **every DECISIONS-PENDING item is surfaced before integration writes the final syntheses**.

## §1 The Phase-3.3 cross-mandate verdict is sharply split

Four cross-mandate subagents reached three structurally distinct verdicts:

| Subagent | Verdict | Recommended Phase-4 shape |
|---|---|---|
| [`X_UNM_G`](bias-guards/phase-3/cross-mandate/x-unm-g.md) (unified-fails-greenfield) | **PARTIAL FAIL** — unified survives greenfield artefact-wise but DPU-1 must resolve first; DPU-5 EscrowSurface compounds F42/F53 under mixed mandates | Greenfield day-0 primitives remain mandate-specific even under unified envelope |
| [`X_UNM_B`](bias-guards/phase-3/cross-mandate/x-unm-b.md) (unified-fails-brownfield) | **FAILS** — unified substrate has NO equivalent to ROBUST-B3/B4 CodebaseModel; F21, F28, F34, F58 unmitigated | UC4 holds on brownfield side; CodebaseModel is the missing primitive |
| [`X_GFB_A`](bias-guards/phase-3/cross-mandate/x-gfb-a.md) (unify-advocate) | **UC4 FALSIFIED** — 8 of 8 splitter-cluster substrate primitives are shared; methodology divergences are work-unit-class variations on one cycle | One unified architecture with parameter atlas |
| [`X_GFB_X`](bias-guards/phase-3/cross-mandate/x-gfb-x.md) (cannot-unify) | **UC4 SURVIVES** — greenfield primitives have no brownfield analog and vice versa; sharing tactical primitives is not architectural unity | Two architectures sharing tactical-substrate stratum |

**Synthesis of the verdicts.** The advocate (X_GFB_A) and the cannot-unify attacker (X_GFB_X) reach genuinely opposite conclusions about whether the drafts collapse. Critically, both agree on what is *empirically* shared (the 8 splitter clusters: judge, watchdog, log, sandbox, holdout-discipline, spec-lint, perimeter, cost ceiling) and what *empirically* differs (cold-start vs. legacy-ingestion per CTR-G3; codebase-model substrate vs. intent-crucible substrate). They disagree on the *naming* — is this "one architecture with parameters" or "two architectures sharing tactical substrate"? — and the *Phase-4 shape*.

The X_UNM_B verdict adds a hard constraint: if Phase-4 picks "one architecture," the unified draft must add a `CodebaseModel` substrate primitive (with five sub-stores) before it can claim brownfield-fit. Currently the unified draft does not name this primitive at all.

## §2 The D7-U-1 blind-axis test partially confirms F-ANCHOR-2 / F-ANCHOR-3

[`D7-U-1`](bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) (cognitive-escrow / interval-as-substrate-primitive PROHIBITED) **produced a defensible alternative**: "Unified-D — Adversarial-Falsification Topology" (FTF), an architecture organised around typed Falsification Commitments. This means the unified-track convergence on escrow framing was *at least partially brief-anchored*; a different reading-list weighting produces a different convergence.

**The subagent's honest concession:** FTF does *not* close F42 (cognitive-escrow negligence) at the substrate layer. The operator-as-opposing-side cold-start regime relies on methodology-layer attention-surface design, where escrow-flavoured architectures are stronger.

**The subagent's recommendation:** treat the unified-track set as needing **both** an escrow-flavoured architecture and an opposing-side-flavoured architecture in the v3 final set, not one chosen over the other. The corpus supplies signal for both clusters:
- **Cluster (a):** cross-family / opposing-side cluster (F1/F27/F46/F48, multi-voice, no single primary source).
- **Cluster (b):** interval / attention-surface cluster (Kahana-anchored, secondarily Schillace / Anthropic / AILCCP).

## §3 The D7-G-1 blind-axis test produces partial alternative to brief §2.1 option (c)+(b)

[`D7-G-1`](bias-guards/phase-3/d7-blind-axis/d7-g-1-prohibit-c-b.md) (option (c)+(b) PROHIBITED) defends option (d): Husain/Shankar evals-FAQ + Anthropic Auto-Review TPR/TNR discipline as the primary empirical-bar source, with Jaymin's K=5 / paraphrase-5/5 / safety-severity matrix demoted to one corpus-derived candidate.

**Honest finding:** (c)+(b) survives as the *regime layer*, but option (d) should be co-adopted at the *empirical-bar layer*. The (c)+(b) convergence was *partially* brief-anchored — ROBUST-G1 / G2 should demote slightly.

## §4 Cross-cutting Phase-3.2 critique findings

The 18 persona-adversarial critiques converge on shared recommendations:

### §4.1 ROBUST-claim demotions (from red-team critiques across all three drafts)

| Original | Recommended demotion | Reason |
|---|---|---|
| ROBUST-G1 (day-0 = L3-Augmentation) | DECISIONS-PENDING new-DPG | Convergence on (c)+(b) is brief-anchored per F-ANCHOR-1 |
| ROBUST-G5 (≥3 region-shaped scenarios) | drop numeric bar | `≥3` is invented threshold; GF-C says 5-10 |
| ROBUST-G10 (cross-model judge mandatory) | per-cell rule | CTR-D7 (Anthropic same-model-fine) + CTR-D8 + CTR-D4 split |
| ROBUST-G14 (EscrowSurface substrate) | DECISIONS-PENDING contingent on D7 | Single-source Kahana promotion |
| ROBUST-G19 (RSI declaration day-0) | narrow scope | Kahana three-part test is steady-state; day-0 timing not corpus-warranted |
| ROBUST-B7 (in-codebase scenarios) | DPB-11 new | Role-partitioning is theoretical; leaks via S-2 dependency edges |
| ROBUST-B8 (cross-model judge brownfield default) | per-cell rule | Same CTR-D7/D8/D4 split |
| ROBUST-B10 (AttributedEventLog) | split U-9a + U-9b | OpenHands measurement does not scale to industrial brownfield |
| ROBUST-U1 (mandate as parameter) | reframe to envelope-only | 95% is at framing; 55% at substrate-primitive-content |
| ROBUST-U10 (EscrowSurface unified) | contingent on D7-U-1 | Single-source promotion; alternative axis exists |
| ROBUST-U13 (typed bootstrap output) | split U13-G + U13-B | Greenfield-flavoured smuggled into unified |

### §4.2 New ADR candidates (from regulator + on-call + CFO critiques)

- **AILCCP three-controls coverage attestation at graduation events** (regulator) — Phase-5 wave-1
- **AttributedEventLog engineering specification** (regulator, brownfield + unified) — retention horizon, WORM attestation, jurisdictional residency, reconstruction protocol; Phase-5 wave-1
- **Inherited-compliance-obligations register as 6th codebase-model sub-store** (brownfield regulator)
- **Per-view freshness primitive** (brownfield on-call) — Phase-5 wave-1
- **Acquired-codebase merge as named substrate event class** (brownfield on-call)
- **Intent-block amendment audit** (greenfield on-call) — invariant amendments cross-family-judged
- **Patrol-threshold immutability discipline** (greenfield on-call) — threshold-tuning events as audit-class
- **Cognitive-escrow engagement audit** (greenfield on-call) — STIR-cascade dismissals logged
- **Cost-per-graduation specification** (greenfield + brownfield + unified CFO) — Phase-5 wave-1
- **ClassifierInputPopulationAudit substrate primitive** (unified on-call) — proposed ROBUST-U15
- **Deliverable-bounded substrate partitioning** (unified regulator) — proposed DPU-9

### §4.3 New F-mode candidates

- **F62 — Inherited-Certification Lapse** (brownfield regulator): agent-modified codebase silently invalidates a design-time certification
- **F62/F63 — Cross-mandate substrate accountability collapse** (unified regulator): deliverable-level Caremark/SB 53/IAC accountability is undermined when one substrate concurrently runs deliverables of differing regulatory regimes
- **Severity re-rank for F48 / F55 / F57 / F8 at the unified architecture specifically** (unified on-call): these compose multiplicatively across mandates

### §4.4 Newcomer-readability recommendations (from all three newcomer critiques)

- Add a §0 reader's preamble to each synthesis-v1 file
- Add a §0.5 reference card / "see X" pointer header
- Inline-gloss F-mode IDs, CTR IDs, splitter/lumper cluster IDs, F-ANCHOR IDs on first mention
- Disambiguate the "D" namespace (D-1..D-7 defaults / D1..D7 decisions / D7-* blind-axis / DPU-* decisions-pending)
- Work one cycle three ways for DPU-1 (a worked example under U-A / U-B / U-C)

## §5 The Phase-3.4 user-decision queue

The decisions below are listed in approximate dependency order: top items must resolve before bottom items can be answered. Items in **bold** are *architectural*; the rest are downstream specifications.

### Tier 1 — load-bearing architectural shape (must resolve at this checkpoint)

1. **DEC-1 (unification verdict).** Given the split cross-mandate verdicts, what is v3's Phase-4 shape?
   - Option A: One unified architecture with mandate-parameter atlas (per `X_GFB_A`)
   - Option B: Two architectures sharing tactical-substrate stratum (per `X_GFB_X`)
   - Option C: Two unified candidates — one escrow-flavoured (current U-A/U-B/U-C) + one opposing-side-flavoured (D7-U-1's FTF) — picked per work-unit-class in D2 matrix
   - Option D: Both A *and* the brownfield draft retains its own architecture (in case A doesn't reach brownfield-fit)

2. **DEC-2 (EscrowSurface placement).** Given the partial F-ANCHOR-2 confirmation by D7-U-1, what is the EscrowSurface's status?
   - Option A: Substrate primitive (current ROBUST-G14/U10 stance)
   - Option B: Methodology-layer convention enabled by D-6 Patrol + D-7 trajectory but not substrate-typed
   - Option C: Contingent — substrate primitive *only if* DEC-1 picks option A or D (one unified architecture), methodology if DEC-1 picks B or C

3. **DEC-3 (methodology shape per greenfield draft, DPG-2).**
   - Option A: GF-S substrate-thin (deliberately empty methodology)
   - Option B: GF-M two-regime (spec-discovery / spec-anchored, reversible-commitment unit-of-work)
   - Option C: GF-C three-sub-phase Bootstrap-Bench (graduation protocol)
   - Option D: Combination — GF-C bootstrap + GF-M Regime A/B steady-state + GF-S substrate-stack underneath

4. **DEC-4 (methodology shape per brownfield draft, DPB-3).**
   - Option A: BF-S substrate-continuous-with-thin-methodology
   - Option B: BF-M 8-stage methodology-cycle-as-architecture
   - Option C: BF-L 3-loop architecture (ingestion / work / maintenance over codebase model)

### Tier 2 — substrate / methodology boundary (depend on Tier 1)

5. **DEC-5 (eligibility classifier placement, DPG-3 / DPB-7 / DPU-3).** Substrate primitive or methodology / per-architecture-spec?
6. **DEC-6 (typed-object granularity for unified, DPU-1).** Interval (U-A) / layer (U-B) / anchor (U-C) / multi-primitive coexistence — if DEC-1 picks A or D.
7. **DEC-7 (codebase-model maintenance cadence, DPB-4).** Continuous / per-cycle-reconstructed / refresh-on-trigger / human-anchored-refresh-trigger.
8. **DEC-8 (regime granularity, DPB-6).** Per-work-unit-class / per-(work-unit-class × code-region).
9. **DEC-9 (D-3 decomposition, DPG-1 / DPB-2 / DPU-2).** Agent = Model + Harness + {natural-language-register / interval-kind / anchor-context / opposing-side-declaration}.

### Tier 3 — operational specifications (Phase-5 ADRs)

10. DEC-10 (cost-per-graduation specification + cost-ceiling under stacked guards)
11. DEC-11 (AttributedEventLog engineering: retention, WORM attestation, jurisdictional residency)
12. DEC-12 (judge sub-shape policy per work-unit-class × evidence-density cell)
13. DEC-13 (primary durable artifact for brownfield, DPB-1): codebase / change-intent block / codebase model
14. DEC-14 (work-unit-class taxonomy source, DPB-5): D2 default / per-deployment / model-derived
15. DEC-15 (Compound knowledge store placement, DPB-10 / DPU-7)
16. DEC-16 (spec-format commitment, DPG-5): agnostic / malleable / EARS-mandated
17. DEC-17 (empirical bars source, DPG-6 / OQ-B6): Jaymin defaults / Husain-Shankar TPR-TNR / per-architecture / bench-derived
18. DEC-18 (cognitive-escrow primitives status, DPG-7 / DPU-5): substrate / methodology (see DEC-2)
19. DEC-19 (cold-start exit criteria, DPG-4): GF-C four criteria adopted as default / open Phase-5 parameter

## §6 What Phase-3.4 produces if all decisions resolve

Three `*-synthesis-v1.md` files per the plan's §6 schema:

- `architectures/v3/greenfield-synthesis-v1.md` — ROBUST claims (filtered through critique demotions) + DECISIONS-RESOLVED appendix + objections-and-responses appendix pointing at the 6 greenfield critiques + 2 cross-mandate critiques + D7-G-1
- `architectures/v3/brownfield-synthesis-v1.md` — same structure with brownfield critiques + cross-mandate + (no D7 specific to brownfield)
- `architectures/v3/unified-synthesis-v1.md` — same structure with unified critiques + cross-mandate + D7-U-1; *or* if DEC-1 resolves to "no unified survives," the file is renamed/removed per Phase-4

Plus updated brief §6 outputs:
- F-mode catalog gains F62 (Inherited-Certification Lapse) and re-ranked severities
- Splitter cluster recommendations are absorbed into Phase-4 substrate enumeration prep
- New ADR candidates (from §4.2) are queued for Phase-5 waves

## §7 What Phase-3.4 cannot do without user input

The integration cannot proceed with the current draft text intact because:
- Three ROBUST claims rest on contingent D7 outcomes
- The cross-mandate verdict is split four ways
- The methodology shape is open per mandate
- The substrate/methodology boundary depends on the unification choice

**The Phase-3.4 user checkpoint surfaces DEC-1 through DEC-4 (Tier 1) at minimum.** Tier 2 and Tier 3 items can either be resolved here or carried to Phase-5 as ADR questions, depending on user appetite.
