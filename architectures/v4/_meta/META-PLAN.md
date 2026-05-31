# Meta-Plan: Detailed Spec & Plan for `architectures/v4`

> The plan for producing the plan. This document is the orchestration contract for
> the primary agent and every subagent. It is itself a deliverable and is kept current.

> **⚠ PARTIALLY SUPERSEDED (2026-05-31): tracks converged.** §1 ("two tracks") and the Phase-2
> wave structure (build × track) below describe the *original* parallel-track plan that produced
> the first 23 components. The run has since converged to a **single canonical track** — `spec/`
> (formerly `spec-faithful/`) and its build companion `plan-faithful/`. `spec-optimized/` and
> `plan-optimized/` are frozen reference. For the remaining 34 components, dispatch one builder
> per component, single-track, under the capability-for-principle bar. See
> [`HANDOFF.md`](./HANDOFF.md) §2 for the bar and [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md) for
> the convergence rationale. The phases, personas, parallelism model, and context-preservation
> protocol below remain in force.

## 0. Mandate (from the user)

- Produce an **incredibly detailed spec** and an **incredibly detailed plan** for **every
  single piece** described in `architectures/v4`.
- Exploit **parallelism to the max** — both *in the produced plan* (so the real build can run
  many concurrent workstreams) and *in the process of producing it* (massive subagent fan-out).
- **Cooperative AND adversarial** subagents scrutinize everything, at every step. Run multiple
  **distinct personas** on the **same** task in parallel (diversity-by-redundancy), then reconcile.
- **~2 hours, effectively unlimited tokens.** Quality foundation over a slapdash implementation-ready
  artifact with weak foundations. The user will cut the run off when the token window closes; until
  then, keep going — do not rush.
- **50+ subagents concurrently.** Ruthlessly preserve the primary agent's context window by pushing
  all reading and authoring into subagents that persist artifacts to disk and return short receipts.

## 1. The two tracks (run simultaneously)

| Track | Folder roots | Posture |
|---|---|---|
| **A — Faithful** | `spec/`, `plan-faithful/` | Treat the four v4 docs as a *fixed proof*. Elaborate exactly what is there. Adversarial agents flag risks but MUST NOT alter the architecture. |
| **B — Optimized** | `spec-optimized/`, `plan-optimized/` | v4 is the starting point but fair game. Ruthlessly improve the design on best judgment; every deviation from v4 is recorded as an explicit, justified **delta**. |

Both tracks are decomposed against the **same canonical component inventory** so they stay diffable.

## 2. Context-preservation protocol (non-negotiable)

1. The **primary agent never reads the large v4 docs in full.** Subagents read; they return ≤15-line
   receipts (paths written, headline findings, open questions).
2. **All real output goes to disk** under `architectures/v4/`. Receipts are for orchestration only.
3. The **only** large thing the primary keeps in context is the compact **component inventory**
   (numbered list, one line each) — the backbone for dispatch.
4. **Git is the primary's job.** Subagents only Write/Edit their own files (distinct paths, no races).
   The primary stages/commits/pushes **between waves**, never mid-wave.
5. Checkpoint commit + push after every wave so the ephemeral sandbox can die without data loss.

## 3. Phases

### Phase 0 — Grounding (this wave)
Redundant cooperative cartographers + an adversarial skeptic read all four v4 docs and produce, in `_meta/`:
- `component-inventory-A.md`, `component-inventory-B.md` — two independent exhaustive decompositions.
- `ambiguities-and-gaps.md` — contradictions, undefined terms, unstated assumptions, missing pieces.
A reconciler then emits the canonical `component-inventory.md` (stable IDs `C01..Cnn`, one-line desc,
source refs, dependencies). This list is the dispatch backbone.

### Phase 1 — Scaffolding & track charters
Write `spec/00-index.md`, `spec-optimized/00-index.md`, `plan-*/00-index.md`, each seeding the
component list and the per-doc template. Write the Track A and Track B charters (rules each track's
builders must obey).

### Phase 2 — Sweep 1: Architecture-level foundation (the big fan-out)
For each component C × each track T: a **builder** persona authors `spec-T/Cnn-*.md` at architecture
altitude (responsibilities, boundaries, interfaces named, key decisions, tradeoffs, dependencies,
failure modes referenced). In parallel an **adversary** persona authors `Cnn-*.review.md` attacking it.
A **reconciler** folds the review into the spec and logs unresolved issues to `_meta/review-log.md`.
Plan docs are authored in the same wave structure under `plan-T/`.

### Phase 3 — Sweep 2: Implementation-ready depth
Re-enter each component: concrete interfaces/signatures, data schemas, API contracts, sequence/state
diagrams, error taxonomies, acceptance criteria, test strategy. Same builder/adversary/reconciler trio.

### Phase 4 — Sweep 3: Exhaustive depth (as time allows)
Pseudocode/algorithms, representative skeletons, edge-case catalogs, perf/security/ops detail.

### Phase 5 — Cross-cutting integration & final adversarial pass
Whole-system consistency review (cross-component drift), critical-path/parallelism analysis of the
build plan, Track A vs Track B comparison memo, and an index/README tying it all together.

## 4. Subagent role catalog (personas)

- **Cartographer** (coop): decomposes, names, structures.
- **Skeptic / Red-team** (adversarial): attacks assumptions, hunts contradictions, asks "what breaks?".
- **Builder** (coop): authors a component spec/plan doc.
- **Adversary** (adversarial): reviews one doc, writes `.review.md`.
- **Reconciler** (coop): merges builder + adversary, logs open issues.
- **Optimizer** (Track B): proposes and justifies deltas from v4.
- **Integrator** (coop): cross-component consistency + parallelism analysis.

Each persona brief carries: the context-preservation protocol, its track charter, the target file
path(s), the inventory ID it owns, and the instruction to return a ≤15-line receipt only.

## 5. Parallelism model

- Waves of many concurrent `Agent` dispatches; each writes a distinct path → no write races.
- Builder and adversary for the *same* component run concurrently (adversary reviews the prior sweep's
  version, or co-develops against the same brief, depending on sweep).
- Both tracks fan out in the same wave.
- Target sustained concurrency ≥ the user's 50-subagent bar by batching across (components × tracks ×
  roles). Receipts keep the primary lean enough to sustain it.

## 6. Status ledger
See `_meta/STATUS.md` (updated every wave) for live phase/sweep/component completion state.
