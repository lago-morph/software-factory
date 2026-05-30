# C13 — Molecule (instantiated workflow) / runtime state  (Build Plan, Track B)

> Source / Spec ref: [`spec-optimized/C13-molecule-runtime-state.md`](../spec-optimized/C13-molecule-runtime-state.md)

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| **T1** | Define the **`molecule` root-bead payload schema** (fields per spec §4: `molecule_id`, `formula_identity`, `params`, `lifecycle_state`, `bound`/`bound_remaining`, `branched_from`) and submit it to C20 for registration via the C20↔C22 seam (D-3). | M | C20 envelope + register mechanism; C12 `FormulaIdentity` shape |
| **T2** | Freeze the **molecule lifecycle state machine** (`instantiating → running → {converged\|failed\|escalated\|abandoned}`, `paused/resuming`) as the C20 lifecycle states for the `molecule` type. | S | T1 |
| **T3** | Implement **`instantiate(parsed_formula, params, owner_actor) → Molecule`** — the bind→materialize→seal transform (DELTA-02): create root, map each node→`child_of` bead, project edges→`blocks`, assert §3 invariants, transactional seal. | L | T1, T2, C12 `ParsedFormula`/`NodeBinding`, C19 `create`/`add_edge` |
| **T4** | Implement the **run-state query contract** (`ready_frontier`, `state`, `node_for`/`formula_node_for`) over C19. Freeze early (M1) so C05/C18/C33/C49 build against stubs. | M | C19 `ready_frontier`/`walk`/`find` |
| **T5** | Implement **`resume(molecule_id)`** — pure-read reconstruction from C19 (root + `child_of` subtree + per-node state); the `gc converge resume` substrate (§16). | M | T3, C19 `find`/`walk` |
| **T6** | Implement **`record_node_outcome` + frontier recompute + `bound` decrement/escalation** (DELTA-05; slot+signal only, numerics deferred to C18/C39 per XC-3). | M | T3, T4 |
| **T7** | Implement **`branch(molecule_id, from_node, overrides)`** re-instantiation (DELTA-07): shared history + diverging sibling, `branched_from` lineage. The C49/C55 hook. | L | T3, T5 |
| **T8** | Tree-shape **invariant assertions** (rooted / total+injective mapping / edge-projection fidelity / sealed-before-runnable) as reusable seal-time checks. Share fixtures with C12 well-formedness + C19 acyclicity. | M | T3 |
| **T9** | **Vocabulary authority** wiring (G06): author the canonical molecule/bead-tree/wisp definition text, link C07 glossary here; document the C12(template)↔C13(instance) boundary as a testable contract. | S | spec §1 frozen |
| **T10** | Acceptance test suite (spec §8 AC1–AC9), incl. crash/resume fidelity, all-or-nothing seal, bound-escalation (F52), branch comparability, and the C18-absent dependency-direction proof (AC9). | M | T3–T8 |

## 2. Dependency graph

```
C12 (ParsedFormula, FormulaIdentity, bound)  ─┐
C19 (BeadStore: create/add_edge/walk/find/    ─┼─► C13.T3 instantiate ─► T5 resume ─► T7 branch
     ready_frontier)                          │        │
C20 (molecule payload schema + lifecycle) ◄── T1,T2 ──┘        └─► T6 record/bound
C41 (created_by actor)  ───────────────────────────────────────► (inherited via C19)
C03 ([formulas] flag gates existence)
```

- **Critical path:** C12 + C19 interface freeze → **T1/T2 (schema+lifecycle)** → **T3 (instantiate)** → T5/T6 → T7 → T10. T3 is the long pole; everything runtime hangs off a correct seal.
- **C13 is NOT on C18's build path.** Per spec DELTA-06/OQ2, C18 (reconciler) is a *runtime collaborator*; C13 builds and tests against C19 + stubs with C18 absent (AC9). This is the dependency-direction correction the integrator must confirm (the inventory's `Depends on: C12, C18` is wrong on the C18 leg).
- **Upstream blockers:** C12 must expose `ParsedFormula`/`NodeBinding`/gate-`bound`; C19 must freeze `create`/`add_edge`/`ready_frontier`/`walk`; C20 must accept the `molecule` type registration. These are Batch-1/early-Batch-2 freezes already in flight.

## 3. Parallelization

Independent workstreams after the C12+C19+C20 interface freeze (M1):
- **WS-A (schema/lifecycle):** T1, T2, T9 — pure data/definition; no runtime code; can land first and unblock everyone.
- **WS-B (instantiation core):** T3, T8 — the seal transform + invariants; the long pole.
- **WS-C (query/run-state):** T4, T6 — the read/progress surface; depends only on C19 + the frozen `state` shape, *not* on T3's internals, so it can develop against a hand-built fixture molecule in parallel with WS-B.
- **WS-D (resume/branch):** T5, T7 — depends on T3's persisted shape; starts once T3's bead layout is frozen (not its full impl).
- **WS-E (tests):** T10 — fixtures authored in parallel; executed as WS-B/C/D land.

Fan-out: WS-A ∥ WS-C ∥ (WS-E fixture authoring) immediately after M1; WS-B leads; WS-D follows WS-B's layout freeze.

## 4. Interfaces-first / contract milestones

- **M1 (freeze first):** the **`MoleculeState` query contract** (`ready_frontier`, `state`, `node_for`) + the **`molecule` root-bead field schema** (T1) + the **lifecycle state-name set** (T2). These three let C05/C18/C33/C49/C55 and C20 build against C13 stubs before `instantiate` exists. This mirrors C19's "freeze the query contract early" (DELTA-07).
- **M2:** the **`instantiate` signature + seal semantics** (all-or-nothing, sealed-before-runnable) + the **node↔bead mapping** rule — so C12 hand-off and C39 fix-task injection (`caused_by` into a live tree) are stable.
- **M3:** the **`resume` contract** (`gc converge resume <molecule_root>` → live molecule) — the §16 cold-start anchor C52 self-bootstrap resume depends on.
- **M4:** the **`branch` contract + `branched_from` lineage** — co-frozen with C49/C55 (defer arbitrary-midpoint vs gate-boundary granularity to those specs, spec OQ5).

## 5. Risks & de-risking order

1. **Gas City native molecule model (spec OQ1 / G11) — highest uncertainty.** Spike: confirm whether `gc converge` exposes a native run/molecule object with its own state, or whether "molecule" is purely v4's name for the bead-tree under a root. Retire **before** finalizing T1/T3 — if native, C13's root-bead must conform-or-wrap; if not, C13's root-bead *is* the molecule. Same blocker as C12 OQ1.
2. **Dependency-direction correction (spec OQ2 / DELTA-06).** Confirm C19 (not C18) as the build-time substrate dep at the integrator pass *before* committing the build order; AC9 (instantiate+resume with C18 absent) is the falsifiable proof. Low effort, high clarifying value — do early.
3. **Transactional seal over a non-transactional file store (DELTA-02 vs C19 file provider).** C19's file backend is append+fsync+atomic-rename, not a multi-row transaction. Spike the rollback/`instantiation_failed`-marking strategy so a mid-instantiation crash never yields a runnable torn molecule. Retire with the T8 invariant + a crash-injection fixture (AC2).
4. **Branch/checkpoint granularity for C49 (spec OQ5 / G19).** The hardest, admittedly-unsolved invention. De-risk by shipping **gate-boundary branching first** (cheap, sufficient for C55 methodology A/B) and deferring arbitrary-midpoint branching to co-design with C49. Do not block T3–T6 on this.
5. **`sub_formula` = nested molecule vs flattened (spec OQ4).** Affects whether resume/branch operate on a forest. Co-specify with C12 OQ3; pick nested-child-molecule provisionally (matches the bead-tree forest reading) but keep T5/T7 agnostic until confirmed.

## 6. Definition of done

- **Per-task:** each Tn meets its spec §8 acceptance criterion (T3→AC1/AC2/AC3; T5→AC4; T6→AC5; T7→AC6; T2/identity→AC7; T9→AC8; dependency-direction→AC9).
- **Per-component:**
  - The README "3-step minimum" formula instantiates to a sealed 3-node + root molecule (AC1), runs to `converged`, survives a simulated crash via `resume` with identical run-state (AC4), and a bound-exceeding variant `escalates` instead of looping (AC5).
  - All §3 tree-shape invariants hold at seal; a torn/half-built molecule never appears in any frontier (AC2/AC3).
  - `branch` produces an independently-runnable, identity-comparable sibling (AC6); methodology identity is immutable post-seal (AC7).
  - C07 glossary links to C13 for molecule/bead-tree/wisp; the C12↔C13 template-vs-instance boundary is a documented, testable contract (AC8).
  - Instantiate + resume demonstrably work with C18 (reconciler) absent (AC9), proving the C19-not-C18 substrate dependency.
  - The five open questions (OQ1 Gas City model, OQ2 dep-direction, OQ3 bound-policy owner, OQ4 sub_formula nesting, OQ5 branch granularity) are mirrored to [`_meta/review-log.md`](../_meta/review-log.md) with owners.
