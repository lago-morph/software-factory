---
based-on-commit: HEAD
based-on-date: 2026-05-26
---

# Mandate-fit matrix — Phase 6.4

## Section 1 — TL;DR

This file is the Phase-6.4 cross-candidate mandate-fit matrix per [auto-006 Round 2](decisions/auto-006-phase-6-dispatch-shape.md) and the [DEC-2 schema](decisions-captured.md#d2--mandate-fit-is-per-architecture--work-unit-class-not-per-architecture). It composes the YAML `mandate-fit:` block from each of the 10 Phase-6 specs (`specs/<id>.md`) into a 10-row × 5-work-unit-class matrix using tokens `greenfield | brownfield | both | n/a | silent` (the `silent` token per the [R2 schema amendment](decisions/auto-006-phase-6-dispatch-shape.md#decision-round-2)). Per-cell rationale + falsifying scenario lives in Section 3, pulled from each spec's §5 Mandate fit prose. Per-candidate `both`-cell counts + a neutral DEC-1.a observation live in Section 4. References are in Section 5. The matrix is evidence for downstream pressure-testing; verdicts are not authored here.

## Section 2 — The matrix

| Candidate | initial-spec | refactor | mvp | post-mvp-evolution | regression-fix |
|---|---|---|---|---|---|
| GF-S | greenfield | greenfield | greenfield | greenfield | greenfield |
| GF-M | greenfield | silent | greenfield | greenfield | greenfield |
| GF-C | greenfield | silent | greenfield | silent | silent |
| BF-S | brownfield | brownfield | n/a | brownfield | brownfield |
| BF-M | n/a | brownfield | n/a | brownfield | brownfield |
| BF-L | brownfield | brownfield | n/a | brownfield | brownfield |
| U-A | both | both | greenfield | both | both |
| U-B | both | both | greenfield | both | both |
| U-C | brownfield | both | greenfield | both | both |
| D7-U-1 | both | both | both | both | both |

## Section 3 — Per-cell rationale

Per-cell rationale is provided for every `both` / `n/a` cell (the cells that load DEC-1.a pressure-testing) and a one-line note for every `silent` cell citing the spec section that establishes silence. `greenfield` / `brownfield` cells inherit natural mandate alignment and carry no per-cell rationale here (rationale is in each spec's §5).

### GF-S

All 5 cells are `greenfield`; no `both` / `n/a` / `silent` cells. Per [`specs/gf-s.md` §5](specs/gf-s.md#5-mandate-fit), GF-S is mandate-specific by construction; the substrate's S2 holdout-discipline + S9 work-unit-class feature source are only coherent at greenfield day-0 where no Codebase Model exists.

### GF-M

- **refactor: silent.** GF-M takes no position on `refactor`; refactor presupposes an existing codebase against which the proposed change is sized. Silence (not n/a) per [`specs/gf-m.md` §5](specs/gf-m.md#5-mandate-fit): "no claim, not a deliberate rejection." Established by [`tracks/greenfield-methodology-first.md` §6](tracks/greenfield-methodology-first.md).

### GF-C

- **refactor: silent.** Refactoring presupposes a steady-state codebase; GF-C's design centre is day 0 before code exists. [`specs/gf-c.md` §5](specs/gf-c.md#5-mandate-fit) explicitly states "silent, not n/a — silence is not a rejection."
- **post-mvp-evolution: silent.** GF-C does not claim a post-graduation methodology; the micro-cold-start re-entry mechanism is its only post-graduation surface ([`specs/gf-c.md` §5](specs/gf-c.md#5-mandate-fit)).
- **regression-fix: silent.** Regression-fix presupposes a failing test against an established test suite; not a canonical GF-C work-unit-class ([`specs/gf-c.md` §5](specs/gf-c.md#5-mandate-fit)).

### BF-S

- **mvp: n/a.** MVP authoring presupposes greenfield-leaning evolution (no pre-existing codebase to read); BF-S's load-bearing primitives (P-22 / P-23 / P-07 / P-24) all presuppose existing code. Per [`specs/bf-s.md` §5](specs/bf-s.md#5-mandate-fit): "n/a not silent — BF-S rejects MVP, it doesn't simply have no position." Falsifying scenario: if BF-S's substrate successfully ran an end-to-end MVP authoring against an empty repository, the brownfield-only construction would be wrong.

### BF-M

- **initial-spec: n/a.** BF-M is brownfield-only by construction; initial-spec authoring presupposes greenfield (no prior codebase). [`specs/bf-m.md` §5](specs/bf-m.md#5-mandate-fit): "n/a, not silent — the cycle's shape rejects this work-unit-class." Falsifying scenario: a successful run of stages 2-3 against an empty repository would refute the stage-2 brownfield-defining claim.
- **mvp: n/a.** MVP authoring presupposes greenfield cold-start; explicit out-of-scope per [`tracks/brownfield-methodology-first.md` §6](tracks/brownfield-methodology-first.md#6-what-this-track-is-not-trying-to-be) "Not a greenfield architecture." Falsifying scenario: end-to-end MVP authoring with no pre-existing codebase would refute the stage-2-brownfield-defining claim.

### BF-L

- **mvp: n/a.** MVP authoring presupposes greenfield-leaning evolution (no existing code, no model to ingest); BF-L's three loops are structurally tied to an existing codebase. [`specs/bf-l.md` §5](specs/bf-l.md#5-mandate-fit) cites [`tracks/brownfield-legacy-ingestion-first.md` §6](tracks/brownfield-legacy-ingestion-first.md#6-what-this-track-is-not-trying-to-be): brownfield-only by construction. Running Loop-1 on an empty repository produces an empty model with no features for Loop-2's classifier.

### U-A

Per [`specs/u-a.md` §5](specs/u-a.md#5-mandate-fit):

- **initial-spec: both.** Greenfield runs `kind: bootstrap`; brownfield runs `kind: archaeology` then `kind: spec-author`. Same substrate primitives (ADR 0050 / 0051 / 0052) with `priors` content varying. Falsifying scenario: if greenfield bootstrap graduates without threshold-bar measurement OR brownfield archaeology miscalibrates against held-out behaviour, mandate-as-parameter fails.
- **refactor: both.** `kind: refactor` interval; greenfield and brownfield share envelope shape, only `priors.in-tree` content differs. Falsifying scenario: systematically lower automation-eligibility on brownfield refactor with identical envelope features collapses substrate's mandate-symmetry.
- **post-mvp-evolution: both.** Steady-state cycles operate against accumulated in-tree priors on both mandates; same substrate. Falsifying scenario: if brownfield post-MVP requires an extraction primitive U-A does not carry (X_UNM_B gap), the unified claim retreats to greenfield-only.
- **regression-fix: both.** `kind: regression-fix`; failing test is the first `priors.in-tree` element; ADR 0050 dispatches `sample-audit`. Falsifying scenario: routine escalation to `human-required` because substrate cannot distinguish regression-fix from broader refactors refutes the per-`kind` regime structure.

### U-B

Per [`specs/u-b.md` §5](specs/u-b.md#5-mandate-fit):

- **initial-spec: both.** L2 spec authoring against El Kaim 9-field intent block regardless of mandate; greenfield constructs against seeded L0/L1; brownfield treats L2 spec as delta-spec against L4-inferred system. Falsifying scenario: if brownfield initial-spec requires substrate primitives not reducible to P-22 + P-23 + ADR-archaeology, the unified claim collapses.
- **refactor: both.** Layer-typed; greenfield runs L1→L2 under existing L0; brownfield pins L1 via inference then L2→L3→L4. Falsifying scenario: indistinguishable layer-pair distributions across mandates with identical gate fire-rates refutes mandate-as-parameter.
- **post-mvp-evolution: both.** Cycles operate against accumulated typed-object graph on either mandate; ADR 0055 + ADR 0056 are uniform. Falsifying scenario: if brownfield post-MVP requires fundamentally different layer-pair gates than greenfield, the unified claim collapses.
- **regression-fix: both.** L4 cycles with `expected-touch[]` scoped to failing test's call-graph closure. Falsifying scenario: routine L0/L1 traversal rather than L3/L4-bounded fixes refutes regression-as-L4-bounded.

### U-C

Per [`specs/u-c.md` §5](specs/u-c.md#5-mandate-fit):

- **refactor: both.** Distance-typed; greenfield uses architecture-rule anchors, brownfield uses live-test + Brier pace-layers driving `graph_distance` via P-22 + P-23. Falsifying scenario: indistinguishable distances on greenfield vs brownfield with identical regime distributions refutes mandate-as-parameter.
- **post-mvp-evolution: both.** Distance estimator uniform across mandates; anchor sets differ in source content not substrate. Falsifying scenario: if brownfield post-MVP requires fundamentally different primitives, the unified claim collapses.
- **regression-fix: both.** Near-anchor by construction; ADR 0058 contradiction-flag hard floor + ADR 0021 holdout. Falsifying scenario: routine routing to mid-distance / far-anchor regimes refutes regression-as-near-anchor.

### D7-U-1

Per [`specs/d7-u-1.md` §5](specs/d7-u-1.md#5-mandate-fit):

- **initial-spec: both.** Substrate is mandate-symmetric; day-0 FC defaults are strictest (operator + deterministic checker on greenfield; legacy wrapper-FCs on brownfield). Falsifying scenario: if greenfield initial-spec cannot survive day-0 FCs at non-trivial rate, the operator-as-opposing-side bootstrap is wrong.
- **refactor: both.** FC-typed; greenfield uses operator-attested + deterministic-checker FCs, brownfield uses legacy test suite. Falsifying scenario: routine failure of ADR 0061's trajectory-overlap auditor check refutes substrate-level independence.
- **mvp: both.** Brownfield MVP supported by legacy artifact catalog density; greenfield MVP by strictest-defaults cold-start regime. Falsifying scenario: if MVP cycles never accumulate enough survived FCs to leave the cold-start regime, the earned-replaceability claim is wrong.
- **post-mvp-evolution: both.** Substrate uniform across mandates; only FC catalog density at deployment differs. Falsifying scenario: if brownfield post-MVP requires fundamentally different FC-template defaults, the unified-attempt claim collapses.
- **regression-fix: both.** Close-to-anchor by construction; ADR 0063 compounding gate + ADR 0021 holdout. Falsifying scenario: routine routing to long-survival-window FCs refutes the substrate's FC-method-dispatch.

## Section 4 — DEC-1.a observation

Per-candidate `both`-cell count (computed from Section 2):

| Candidate | `both` cells | Cluster |
|---|---|---|
| GF-S | 0 | greenfield |
| GF-M | 0 | greenfield |
| GF-C | 0 | greenfield |
| BF-S | 0 | brownfield |
| BF-M | 0 | brownfield |
| BF-L | 0 | brownfield |
| U-A | 4 | unified-attempt |
| U-B | 4 | unified-attempt |
| U-C | 3 | unified-attempt |
| D7-U-1 | 5 | unified-attempt |

**Cross-mandate `both` distribution.** All 16 `both` cells (4 + 4 + 3 + 5) sit in the four unified-attempt candidates; zero in the six mandate-specific candidates. D7-U-1 claims `both` on every class; U-A and U-B on 4 of 5 (`mvp` carved out as `greenfield`); U-C on 3 of 5 (`initial-spec` as `brownfield`, `mvp` as `greenfield`).

**Observation re [DEC-1.a working hypothesis](decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8).** The distribution is structurally consistent with what the [9-track Phase-2 fanout](decisions-captured.md#d1--phase-2-fanout-9-parallel-tracks-3--3--3) would produce if mandate-specific tracks declined to claim cross-mandate fit and unified-attempt tracks made the unification claim their candidate is built around. Whether the unified-attempt `both` claims survive Phase-8 lean-eval — and in particular whether the falsifying scenarios named in Section 3 fire — determines whether DEC-1.a is upheld or falsified. This matrix is evidence for that pressure-testing, not a verdict on it.

## Section 5 — References

Architecture specs (10):

- [`specs/gf-s.md`](specs/gf-s.md)
- [`specs/gf-m.md`](specs/gf-m.md)
- [`specs/gf-c.md`](specs/gf-c.md)
- [`specs/bf-s.md`](specs/bf-s.md)
- [`specs/bf-m.md`](specs/bf-m.md)
- [`specs/bf-l.md`](specs/bf-l.md)
- [`specs/u-a.md`](specs/u-a.md)
- [`specs/u-b.md`](specs/u-b.md)
- [`specs/u-c.md`](specs/u-c.md)
- [`specs/d7-u-1.md`](specs/d7-u-1.md)

Decisions:

- [`decisions-captured.md` §D1 — Unification verdict / DEC-1.a working hypothesis](decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8)
- [`decisions-captured.md` §D2 — Mandate-fit schema](decisions-captured.md#d2--mandate-fit-is-per-architecture--work-unit-class-not-per-architecture)
- [`decisions/auto-006-phase-6-dispatch-shape.md` — Phase 6 dispatch shape (Round 2 schema amendment introducing `silent`)](decisions/auto-006-phase-6-dispatch-shape.md)

Supporting:

- [`candidate-registry.md`](candidate-registry.md)
