# Discipline: Three-loop (ingestion / work / maintenance)

A brownfield factory operates three distinct loops over a single durable artifact (the *codebase model*): **ingestion** (deep, slow, run once per codebase + refresh on declared triggers) builds the model; **work** (per-cycle, methodology-shaped) queries the model and proposes changes; **maintenance** (continuous, low-cadence) reconciles the model with reality as code, runtime patterns, and conventions drift. Each loop has different cost ceilings, judge profiles, and watchdog cadences. The discipline operationalises F20 (maintenance-vs-greenfield asymmetry, brownfield-critical) and treats UC4's *"analyzing what is there and growing it"* as constitutive rather than as a side condition.

## Named-by

- `BF-L` — entire architecture: *"The architecture has three loops over a single durable artifact."* (Loop 1: Ingestion deep-slow-one-time-plus-deltas; Loop 2: Work per-cycle methodology-shaped; Loop 3: Maintenance continuous low-cadence). [brownfield-legacy-ingestion-first.md](../tracks/brownfield-legacy-ingestion-first.md) §1.
- `BF-S` — `inferable`. Legacy-ingestion-as-one-time substrate setup is named; maintenance is incremental-on-every-commit, framed as substrate operation not as a separate loop. *"Per-cycle methodology cost is reduced. This is the brownfield analog of the greenfield cold-start problem (CTR-G3); this track explicitly does not treat them as symmetric."* [brownfield-substrate-first.md](../tracks/brownfield-substrate-first.md) §1.1 / §5.
- `BF-M` — `inferable`. Stage 2 (Comprehension) treated as stage-cost, not separate meta-stage; *"If Phase-3 or Phase-4 decide legacy-ingestion deserves equal weight, that would shift this track's stage-2 description to a stage-0/stage-1 split."* [brownfield-methodology-first.md](../tracks/brownfield-methodology-first.md) §5.
- Greenfield tracks (`silent`) — no codebase to ingest yet; greenfield cold-start is structurally different.
- `U-A`, `U-B`, `U-C`, `D7-U-1` (`inferable` but not load-bearing) — brownfield ingestion treated as interval-kind / pace-layer / FC-catalog warming, not as a distinct loop.

## Corpus motivation

- **F20** in [failure-modes-v3.md](../failure-modes-v3.md) — maintenance-vs-greenfield asymmetry, brownfield-critical. Primary source El Kaim per [archive/synthesis-v1-v2/00-synthesis.md §4].
- **F34** — cross-layer drift, brownfield-critical; primary source [followup 12](../../../research/followup/12-brier-pace-layers.md) (Brier pace-layers).
- **F55** — behavioural drift / self-reference loop.
- **F57** — design-authority erosion (the failure mode if model is not maintained).
- **UC4** ([constraints-extracted.md](../constraints-extracted.md)) — "analyzing what is there and growing it."
- **CTR-G3** ([contradictions.md](../contradictions.md)) — legacy-ingestion symmetry question.
- **Report 38** — Beads `discovered-from` edge (candidate knowledge primitive at the engine level).

## Open questions

- **Is legacy-ingestion symmetric to greenfield cold-start?** CTR-G3 is the named tension. BF-S says no (one-time setup vs recurring methodology problem); BF-L flags it as deserving parallel-section discipline (§7 OQ-2).
- **Is ingestion substrate or methodology?** BF-L §7 OQ-1 — *"If substrate, then a shared substrate primitive (codebase model) must be provided cross-architecture; if methodology, then per-architecture ingestion is acceptable."*
- **What's the maintenance-loop cadence?** BF-L §7 OQ-3: *"Too slow → F34 (cross-layer drift) bites; too fast → cost ceiling pressure (D-5) bites. Open: what's the empirical anchor for cadence?"*
- **Recurring legacy-ingestion events** (vendored libraries, acquired-company code). BF-S §7 OQ-T6: *"The architecture has not declared whether these re-trigger the full S-1..S-4 bootstrap or are handled incrementally."*

## Substrate-enforcement options

- `BF-L` `Codebase Model` — versioned, queryable, multi-view representation. Primary substrate primitive of the architecture.
- `BF-S` `S-1 Codebase Index + S-2 Dependency-and-Impact Graph + S-3 Runtime/Telemetry Ingestor + S-4 Change-History/Attribution Store + S-5 Perimeter/Trifecta-Closure Layer`. The five primitives implicitly span the three loops without naming the loops.

Disciplines are distinct from primitives; the three-loop discipline is *how the loops divide labour over these primitives* and is the brownfield analog of the greenfield cold-start discipline.
