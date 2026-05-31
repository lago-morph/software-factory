# C13 — Molecule (instantiated workflow / runtime state)  (Build Plan, Track A)

> Source / Spec ref: [`spec/C13-molecule-runtime-state.md`](C13-molecule-runtime-state.md)
> Track: A (faithful)   Sweep: 1 (architecture altitude)

C13 is the runtime-state join between three already-specced primitives — the formula (C12) it instantiates,
the beads (C19/C20) it is made of, and the reconciler (C18) that drives it. Almost all of C13's correctness is
*derived* from those contracts, so this plan is dominated by **contract-reconciliation** tasks, not net-new
build. The single hard de-risk is the same one the whole Workflow Engine carries: the real Gas City
molecule/`gc converge` model is unverified (G11).

## 1. Work breakdown

| ID | Task | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the molecule⇄formula instantiation contract** — define how a named formula + bound params maps to a bead-tree (one bead per node / per loop-occurrence; formula edges → bead dependency edges; provenance per node). | M | C12 spec frozen (§3.3 outbound) |
| T2 | **Freeze the molecule-state-on-beads model** — confirm the molecule is a *rooted C19 subgraph* (no shadow store); reconcile per-node `status` enum + loop-iteration counter against the C20 envelope `status` field (one field, not three across C12/C13/C20). | M | C19/C20 specs frozen; T1 |
| T3 | **Define the run identity / resume contract** — root-bead handle, `factory_build_in_progress` resume fields (C20), `gc converge resume <bead_id>` re-attach semantics from persisted bead state. | S | C20 resume contract; T2 |
| T4 | **Define the frontier / readiness computation** — runnable set = node-beads whose dependency edges are all `done`; the derived (not stored) topological-readiness over the formula DAG. | S | T1, T2 |
| T5 | **Define the wisp surface to Sling (C05)** — what a runnable frontier node exposes for routing (its formula-node binding: C17 tool node or C09 template name); confirm wisp = dispatch view of a node-bead (not a separate object). | S | T4; C05 contract (sweep 2) |
| T6 | **Define the molecule lifecycle state machine** — instantiated → converging → paused/resumable → converged / failed-escalated; the transition guards consumed by C18's tick. | M | T2, T3; C18 reconciler contract |
| T7 | **Bounded-loop termination handling** — track iteration counter vs formula-declared bound; terminate/escalate at the bound (policy is C39/C18, slots are here). | S | T1 (C12 loop construct), T6 |
| T8 | **Sweep-2 schema freeze against real `gc`** *(deferred — G11 gate)* — concrete molecule/`gc converge` signatures, `status` enum values, wisp shape, instantiation/resume test vectors. | L | G11 retired (an author has run `gc`); T1–T7 |

## 2. Dependency graph

```
C12 (formula spec) ──┐
C19/C20 (bead specs)─┼──▶ T1 ──▶ T2 ──▶ T3
C18 (reconciler) ····┘            │       │
                                  ├─▶ T4 ─▶ T5  (needs C05)
                                  └─▶ T6 ◀─ T3
                                       └─▶ T7
all of T1–T7 ──▶ T8 (gated on G11)
```

**Critical path:** C12/C19/C20 frozen → **T1 → T2 → T6** (instantiation → state-on-beads → lifecycle), because
the lifecycle state machine is what C18 (the driver) binds to and is the most contract-entangled piece. T3/T4
hang off T2; T5 additionally waits on the C05 wisp contract; T7 hangs off T1+T6.

**External blockers:** (a) **C18 has no spec at sweep-1** — its reconciler contract (tick cadence,
frontier-advance, gate evaluation, tick serialization) must land before T6 can be finalized (OQ-C13-2).
(b) **G11** (unverified Gas City molecule model) gates T8 and the concrete shape of T1–T7.

## 3. Parallelization

Within C13, after the upstream specs are frozen:
- **Stream A (structure):** T1 → T4 (instantiation topology → frontier computation) — pure derivation from the
  formula DAG; no external wait until T5.
- **Stream B (state):** T2 → T3 (state-on-beads → resume) — reconciliation against C19/C20 envelope; can run
  concurrently with Stream A once T1 lands.
- **Stream C (lifecycle):** T6 → T7 — depends on both streams' outputs (needs T2 state + T3 resume) and on the
  C18 contract; start its *interface stub* early, finalize last.

T5 (wisp surface) is the one task with a *cross-component* wait (C05); stub the wisp contract from C13's side
(frontier node → routable unit) so C05 can build against it in parallel.

## 4. Interfaces-first / contract milestones

Freeze these early so dependents build against stubs in parallel:

1. **Instantiation contract (T1)** — "formula name + params → rooted bead-tree" — the C12→C13 seam. Unblocks
   anyone reasoning about a run's shape.
2. **Molecule-state-on-beads invariant (T2)** — "a molecule is a rooted C19 subgraph; all run state is bead
   state; `status` is the C20 envelope field." This is the load-bearing decision; freezing it prevents a
   duplicate molecule store and pins the C13↔C19/C20 ownership line.
3. **Resume handle (T3)** — root-bead id + `gc converge resume` semantics — the C13↔C18 and C13↔C52 seam for
   cross-session continuity.
4. **Wisp contract (T5)** — "runnable frontier node → routable unit" — the C13→C05 seam. Stub from C13's side.
5. **Lifecycle/tick subject (T6)** — the desired-vs-actual subject the reconciler reads — the C13↔C18 seam.

## 5. Risks & de-risking order

| Order | Risk | De-risk action |
|---|---|---|
| 1 | **G11 — real Gas City molecule/`gc converge` model unverified.** Every concrete shape (instantiation verb, `status` enum, wisp, resume) is Gas City's, asserted not run. | Spike: obtain `gc`, instantiate a 3-step formula, inspect the resulting bead-tree + `gc converge resume`. This is the shared Workflow-Engine spike (C12 §9 OQ-1) — coordinate, don't duplicate. Until then, keep T1–T7 at named-contract altitude. |
| 2 | **C18 reconciler contract absent at sweep-1.** T6 (lifecycle) cannot finalize without the tick/frontier-advance/gate/serialization contract. | Co-design the C13 lifecycle state machine *with* the C18 author; treat the molecule lifecycle and the reconciler tick as one joint contract (the molecule is the subject; the tick is the verb). |
| 3 | **`status` / loop-counter field drift across C12/C13/C20.** Three specs could name three fields. | Reconciliation task T2 + the C12 §9 / C20 OQ cross-refs; pin ONE `status` field on the C20 envelope and ONE loop construct in C12, both reused verbatim by C13. |
| 4 | **Shadow-store temptation.** Implementers may add a separate molecule store, breaking resume + duplicating C19. | The T2 invariant ("rooted C19 subgraph, no separate store") is the explicit guard; AC-2 tests it. |
| 5 | **Wisp under-definition (C05 seam).** | Stub the wisp from C13's side (frontier node → routable unit) so C05 isn't blocked; finalize jointly at sweep 2. |

## 6. Definition of done

**Per-task DoD** — each of T1–T7 produces a named, sourced contract entry in the C13 spec (sweep-1 altitude:
named + described, no concrete `gc` signatures), with every cross-component field reconciled to a single owner
(no duplicate `status`/edge/type definitions vs C12/C19/C20). T8 is explicitly out-of-scope at sweep 1
(G11-gated) and listed as the sweep-2 entry condition.

**Per-component DoD (sweep 1)** — tied to the spec's §8 acceptance criteria:
1. Instantiation produces a bead-tree topologically identical to the formula DAG, params bound, nodes typed +
   attributed (AC-1). 
2. All molecule state is readable from C19 alone — no shadow store (AC-2). 
3. Frontier = beads whose deps are all `done`; no premature dispatch (AC-3). 
4. Paused run reconstructs identically via `gc converge resume <bead_id>` (AC-4). 
5. Bounded loop terminates/escalates at the formula bound; never unbounded (AC-5). 
6. Convergence/failure detection well-defined (AC-6). 
7. Frontier nodes presentable as wisps to Sling (AC-7). 
8. Per-node provenance enables judge (C33) + replay (C49) (AC-8).

**Exit to sweep 2:** G11 retired (an author has run `gc`) AND the C18 reconciler contract frozen — at which
point T8 concretizes the molecule/`gc converge` signatures, the `status` enum, the wisp shape, and the
instantiation/resume test vectors jointly with C12, C18, and C19/C20.
