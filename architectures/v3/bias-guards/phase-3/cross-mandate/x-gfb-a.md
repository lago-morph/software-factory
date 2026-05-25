---
guard: cross-mandate-unify-advocate
target: draft-greenfield-synthesis + draft-brownfield-synthesis vs draft-unified-synthesis
phase: 3.3
based-on-commit: 52f4fb9
based-on-date: 2026-05-25
---

# Phase-3.3 `X_GFB_A` — greenfield+brownfield unify advocate

## §1 Stance

The two mandate-specific drafts can — and should — collapse into the unified architecture, because the divergences between them are *parameter-data sitting in shared substrate primitives*, not differences of architecture-shape. Read structurally: the greenfield draft's 19 ROBUST claims and the brownfield draft's 14 ROBUST claims map onto the same substrate primitive set under different mandate-parameter content. The methodology divergences (DPG-2 vs. DPB-3) are not architecture-shape conflicts — they are different parameterizations of the same per-typed-object cycle. UC4 is falsified for the architecture's domain of applicability.

## §2 Top unification arguments

### Argument 1 — Eight of eight substrate primitives are shared; only the *parameter values* differ

| Primitive | Greenfield instance | Brownfield instance | What varies |
|---|---|---|---|
| `FrozenAnchor` | ROBUST-G4 El Kaim intent block, `invariants` mandatory | ROBUST-B4 invariant view extracted from tests/types | `provenance`: `operator-authored` vs. `inferred-from-codebase` |
| `RegimeClassifier` | ROBUST-G1/G17 day-0 L3 | ROBUST-B14 day-0 L3 per work-unit-class | classifier *features*, not identity |
| `TypedJudgeCall` | ROBUST-G10 cross-family | ROBUST-B8 cross-family | sub-shape distribution |
| `DeterministicSpecLinter` | ROBUST-G6 EARS/GtWR | implied at change-intent block | applied to different artifact, same lint |
| `PerimeterClosure` | ROBUST-G9 | ROBUST-B5 — *identical primitive* | nothing |
| `AttributedEventLog` | ROBUST-G12 | ROBUST-B10 + HMAC signing | metadata schema is extensible |
| `EscrowSurface` | ROBUST-G14 | implicit in ROBUST-B12 stage 8 | greenfield foregrounds; brownfield embeds |
| `HoldoutPartition` | ROBUST-G17 out-of-tree | ROBUST-B6 role-partitioned in-codebase | `location` parameter |

The splitter §4 ranks these as the single largest Phase-3 dividend. The two drafts' own §1 ROBUST sections are 80%+ parameter-renames of each other.

### Argument 2 — `CodebaseModel` is not a brownfield-only primitive; it is `FrozenAnchor.provenance=inferred-from-codebase`

The five sub-stores of `CodebaseModel` are not architecturally novel — they are the *prior population* of substrate primitives that already exist in greenfield in vacant form:

- Codebase index ↔ greenfield's `priors.in-tree` slot, populated empty at day 0.
- Dependency-and-impact graph ↔ greenfield's blast-radius slot.
- Runtime/telemetry view ↔ greenfield's `EvaluationSuite` populated by operator-curated scenarios.
- Change-history view ↔ `AttributedEventLog`, shared identically.
- Invariant/debt view ↔ `FrozenAnchor` with `provenance: inferred-from-codebase`.

Brownfield's "codebase model" is greenfield's `priors` slot filled in by an `ingestion`-class work unit.

### Argument 3 — Methodology divergences (DPG-2 vs. DPB-3) are work-unit-class variations on one cycle shape

- GF-S ↔ BF-S: the substrate-thick-thin-methodology pair. Both refuse to commit unit-of-work at architecture level.
- GF-M ↔ BF-M: the per-cycle named-stage pair. Both are `per-typed-object cycle` instances differing only in unit-of-work parameter.
- GF-C ↔ BF-L: the bootstrap-first / ingestion-first pair. Both treat day-0 as a distinguished phase with measurable graduation. CTR-G3 distinguishes them in phenomenon but not in architecture-shape.

### Argument 4 — UC4's "spec-malleable vs. code-archaeological" is the same traversal in opposite directions

U-B is the load-bearing piece of evidence. Greenfield = top-down traversal of L0→L4. Brownfield = bottom-up *inference* of L4→L0. The pace-layer stack is identical; the change-rate field is identical; the escrow-policy is identical. What varies is which layer the operator authors directly and which layers the substrate *infers from priors*.

### Argument 5 — The mandate-specific DECISIONS-PENDING items already fold into unified DPUs

- DPG-1 + DPB-2 → DPU-2.
- DPG-3 + DPB-7 → DPU-3.
- DPG-7 → DPU-5.
- DPB-10 → DPU-7.
- DPG-2 + DPB-3 → resolves to DPU-1.
- DPG-5 + DPB-1 → both resolve to the same `FrozenAnchor.provenance` axis.
- DPG-6 + DPB-8 → both resolve to per-`TypedJudgeCall` policy field.
- DPG-8 + DPB-4 → both resolve to substrate's promote-or-reverse policy on `EscrowInterval`.

Every per-mandate DECISIONS-PENDING resolves through a unified-draft DECISIONS-PENDING.

## §3 What the unified architecture must concede

CTR-G3 names a real asymmetry: greenfield's cold-start is a *methodology-creation* problem; brownfield's legacy-ingestion is a *substrate-setup* problem. The splitter explicitly preserves this in Cluster 9 ("PARTIAL UNIFY: unify the graduation protocol primitive, but do NOT unify cold-start with legacy-ingestion"). The unified architecture's `kind: bootstrap` interval must carry *two distinct content-handling protocols* — one for the day-0 operator-authoring case (greenfield), one for the day-0 codebase-ingesting case (brownfield). This is not an architecture-shape concession; it is a *content-handling protocol* concession.

Secondarily, the unified architecture must concede that the *day-0 operator labor cost* is genuinely asymmetric: greenfield demands operator-intent-illiteracy mitigation; brownfield demands codebase-fidelity-of-ingestion mitigation. These are different operator-side concerns.

## §4 Verdict for Phase-3.4

**Phase-4 shared/divergence extraction should treat the drafts as one architecture with mandate parameters, not two architectures.**

1. **Substrate enumeration is one.** Phase-4 produces *one* substrate document; the "divergence document" captures the *parameter-population differences* as a *parameter atlas*, not as architectural divergence.

2. **Methodology enumeration is one cycle shape with mandate-parameterized stages.** The per-typed-object cycle handles both mandates by varying which stages compress to zero.

3. **The mandate-fit matrix (D2) becomes one architecture's mandate-fit matrix.** The unified architecture produces a single 5-column matrix where each cell is either `both` (most cells) or notes mandate-specific parameter dependencies.

4. **CTR-G3 is preserved as a per-bootstrap-interval protocol distinction**, not an architecture-shape distinction.

5. **The cross-mandate adversarial outcome is therefore:** UC4 is falsified for the unified architecture's domain of applicability. The Phase-4 work is one architecture with a parameter atlas; the Phase-6 architecture-spec count drops by at least one.

The strongest counter-attacker move (`X_GFB_X`) will be CTR-G3 + the per-region regime classification asymmetry (DPB-6). The unify-advocate response is that both reduce to *parameter-population* differences inside one substrate primitive.
