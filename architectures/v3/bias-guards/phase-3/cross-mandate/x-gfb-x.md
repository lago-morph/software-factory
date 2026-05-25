---
guard: cross-mandate-cannot-unify-attacker
target: draft-greenfield-synthesis + draft-brownfield-synthesis vs draft-unified-synthesis
phase: 3.3
based-on-commit: 52f4fb9
based-on-date: 2026-05-25
---

# Phase-3.3 `X_GFB_X` — greenfield+brownfield cannot-unify attacker

## §1 Stance

The separate greenfield and brownfield drafts CANNOT collapse without losing the load-bearing mandate-specific primitives that the corpus *itself* distinguishes — most decisively at CTR-G3 (cold-start ≠ legacy-ingestion; lumper Cluster-4: corpus-supported SPLIT) and CTR-B5/CTR-G2 (scenario-locus inversion: out-of-tree for greenfield vs. in-tree for brownfield). The unified draft's "mandate is a parameter" claim achieves uniformity by *eliding* exactly those asymmetries the corpus has registered as contradictions. The advocate (`X_GFB_A`) confuses *family resemblance among tactical primitives* (judge, watchdog, log) with *architectural unity*.

## §2 Top cannot-unify arguments

### §2.1 — Greenfield day-0 substrate primitives have no brownfield analog

Greenfield ROBUST-G4 (operator-authored El Kaim 9-field intent block), ROBUST-G5 (≥3 region-shaped Kaner scenarios authored by the operator out-of-tree), ROBUST-G19 (RSI declaration *before* the first cycle), and the **Cold-Start Bench** are *constitutively* greenfield-shaped: they presuppose **the absence of inheritable artifacts**. The Intent Crucible is not a primitive that runs against a 1M-LOC codebase — there is no operator who authors a fresh 9-field intent block for an inherited system. Conversely, brownfield's ROBUST-B13 legacy-ingestion is the inverse: a *one-time + incremental ingestion pass over existing artifacts*.

CTR-G3 explicitly registers this asymmetry as unresolved. Lumper Cluster-4 says: *"three distinct day-0/recurring-day-0 phenomena: greenfield intent-bootstrap, brownfield code-archaeology, and intra-factory regime-change… brief §5 mandatory-section rule applies to greenfield intent-bootstrap only."*

### §2.2 — Brownfield substrate primitives have no greenfield analog

Brownfield ROBUST-B3/B4 mandates a **codebase model with five distinct sub-stores**. Per lumper Cluster-6 (corpus-canonical five-input split from brief §0), each requires a distinct substrate primitive with different cost, freshness, and maintenance cadence. **None of these primitives exists at greenfield day-0** — there is no codebase to index, no dependency graph to derive, no telemetry to ingest, no history to attribute, no invariant to extract. The unified draft's response (`priors.in-tree: []` for greenfield) is not a parameterization — it is an *empty slot*.

Symmetrically, ROBUST-B6 (in-codebase role-partitioned holdout) requires a substrate primitive that **partitions reads of the live codebase by agent role**. Per lumper Cluster-2, this is structurally distinct from out-of-tree-directory holdout. **D-4 is at minimum four distinct primitives** (out-of-tree / in-codebase-partition / telemetry-stream / co-authored-bench-temporal-partition).

### §2.3 — The "`priors.in-tree: []`" slot is vacuous, not uniform

A schema slot that one mandate populates with five-store load-bearing infrastructure and the other populates with `[]` is not a parameter — it is a *type union with degenerate cases*. Symmetrically, the unified draft's bootstrap-from-priors story for brownfield is incoherent: brownfield does not "bootstrap from priors" when there is a 1M-LOC inherited codebase. The first brownfield cycle reads an existing system; *that read operation is not a prior, it is the substrate's primary capability*. Priors are *inheritable context the substrate uses to seed cycles*; the codebase is *the artifact the substrate maintains a queryable model of*. These are different ontological categories.

### §2.4 — The 95% convergence on "mandate is a parameter" is F-ANCHOR-3 / brief-anchored

The axis-divergence-audit §3.3 *itself flags this*: *"the convergence 'could be either corpus signal (the design space is narrow) or shared contamination from the brief §3 framing (which explicitly invites unification). My judgment is corpus signal, but I cannot prove the negative."* The corpus-thinness becomes visible when you separate the *substrate-primitive-content* overlap (~55%) from the *unified-claim* overlap (~95%): the higher number is brief-induced rhetorical alignment, not corpus-grounded primitive sharing. Lumper Cluster-3 and Cluster-4 both note that the *splitter cluster unifications* are **tactical** (avoid duplicate ADRs), not strategic (one architecture).

### §2.5 — Critical mandate-specific F-modes have non-overlapping solution sets

Brownfield-critical F20 (maintenance asymmetry — *"the brownfield mandate stated as a failure-mode"*), F21 (context exhaustion — unsolvable without a codebase model returning slices), F34 (cross-layer drift — requires invariant view of codebase model) are **unsolvable without the codebase-model five-store substrate**. Greenfield-critical F25 (design starvation), F40 (last-mile drift), F41 (under-defined-intent debt) are **unsolvable without intent-authoring scaffolding**. A unified factory would have to *carry both substrate sets simultaneously*. This is not a parameterization — it is two architectures coexisting under one schema with a `mandate` discriminator.

## §3 What the unified architecture does correctly identify

The convergence is not *entirely* corpus-thin. There is a genuine and corpus-supported family of **tactical substrate primitives** that both mandates share: `TypedJudgeCall`, `PerimeterClosure`, `AttributedEventLog`, `DeterministicSpecLinter`, `HoldoutPartition` *as discipline* (D-4), the three-tier watchdog (D-6), trajectory capture (D-7), and hard cost ceilings (D-5). These appear in both ROBUST-G and ROBUST-B claims with substantially identical shape. The unified draft is right that Phase-4 substrate enumeration can de-duplicate these primitives.

But sharing tactical primitives is not architectural unity. Greenfield and brownfield can use the same logger, the same judge call, the same sandbox, the same watchdog — and still be two architectures. The unified draft's mistake is conflating "tactical primitives unify cleanly" (true) with "the architecture unifies" (the corpus does not support this leap).

## §4 Verdict for Phase-3.4

**Phase-4 should treat greenfield and brownfield as two architectures sharing a tactical-substrate stratum, not as one architecture parameterized by mandate.**

1. **Two architectures, one substrate-tactical layer.** Phase-4 produces **one shared tactical-primitive set** (the splitter Cluster 1-8 primitives) and **two mandate-specific substrate strata above it**:
   - Greenfield: Intent-Crucible primitive, Cold-Start-Bench primitive, RSI-declaration-at-day-0, requirement-count budgeter, paraphrase-divergence-at-spec.
   - Brownfield: `CodebaseModel` with five sub-stores, in-codebase role-partitioning, telemetry ingestor, change-history attribution store, legacy-ingestion-as-substrate-setup-operation, change-intent block (per-cycle).

2. **The "mandate" is not a parameter.** It is a *selector between substrate strata*. The unified draft's `priors.in-tree` schema field is the wrong abstraction.

3. **Minimum substrate-sharing the corpus actually supports.** Splitter Clusters 1–8 enumerate the genuinely shared primitives. Everything *above* these tactical primitives — methodology shape, cycle structure, bootstrap operation, durable-artifact identity, regime-classifier inputs — is mandate-specific. The 80%+ shared-primitive claim is true if scoped to *tactical primitives*; it is false if scoped to *architectural shape*.

4. **CTR-G3 is preserved as the architectural-shape distinction it actually is**, not collapsed into a per-bootstrap-protocol distinction.

**Concrete recommendation.** Phase-4 produces three documents: (i) `shared-tactical-substrate-v1.md` enumerating cross-mandate primitives; (ii) `greenfield-architecture-v1.md` with greenfield substrate stratum + methodology; (iii) `brownfield-architecture-v1.md` with brownfield substrate stratum + methodology. The unified draft is reframed as *the shared-tactical-substrate document plus a note that ROBUST-U1's stronger claim was not corpus-supported under cross-mandate adversarial test*. UC4 survives the falsification attempt of Phase-3.3.
