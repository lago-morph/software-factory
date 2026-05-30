# C42 — Rig / agent-role partitioning  (Build Plan, Track B)

> Source / Spec ref: spec-optimized/C42-rig-partitioning.md

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Role taxonomy + access matrix (DELTA-03).** Define the closed role set `{worker, scenario-author, judge}` and the `default-deny` `(role × partition) → {read, write}` matrix as canonical config. The `worker`→`scenarios` deny is the load-bearing cell. | S | — |
| T2 | **Partition + `[[rig]]` config schema (G28, DELTA-01).** Map the matrix onto Gas City `[[rig]] read_partition/write_partition` TOML (AI-CONTEXT §13.3); define `Partition` (incl. `scenarios` = separate git repo) and the authoritative composition order. | S | T1, C03 |
| T3 | **`PartitionBinding` contract (DELTA-05).** Freeze the typed binding object C04 enforces / C34 audits (the prevent-then-detect join). | M | T1 |
| T4 | **`bind_partition` / `resolve_matrix` API.** Deterministic resolution of `(role, run_id, matrix) → PartitionBinding`; matrix read model for audit/visualization. | M | T2, T3 |
| T5 | **`RunPartition` lifecycle (DELTA-04, F17).** `provision_run_partition` / `reap_run_partition`; git-worktree-per-run; no-shared-writable invariant + GC backstop. | M | T2 |
| T6 | **C04 enforcement integration (I1 teeth).** Wire `PartitionBinding` into C04's `CapabilityBinding` so C04 confines the process at spawn; co-define the partition-half/capability-half composition with C43. | L | T3, C04, C43-freeze |
| T7 | **C41 attribution wiring.** Register each rig as an `Actor` of class `rig`; attribute `bind_partition` + every partition-access (incl. denied) event. | S | T3, C41 |
| T8 | **Reconcile-time invariant checks.** Reject configs that violate I1 (`worker` granted `scenarios` read) or I3 at C18 reconcile / C42 self-check. | S | T2, T4 |
| T9 | **C34 audit surface (DELTA-05).** Emit the `PartitionBinding` manifest + access events for C34's prevent-then-detect audit; cross-check binding ≡ enforcement ≡ audit (I4). | M | T4, T7 |
| T10 | **(Optional) OPA intra-partition refinement (DELTA-06).** Position OPA strictly as intra-partition refinement; prove the coarse boundary holds with OPA disabled. | M | T6 |
| T11 | **Acceptance test battery.** Especially AC-1 (worker cannot read `scenarios`, verified at OS boundary) and AC-3 (judge sees only frozen output). | M | T6, T5, T8 |

## 2. Dependency graph

- **Must precede C42 (build-order dep):** **C04** (the enforcement seam — C42 has no teeth without it), **C03** (config substrate for `[[rig]]`/partitions), **C41** (Actor registration/attribution).
- **Co-design freezes (parallel, not strictly upstream):** **C43** (capability-half of the combined spawn binding) and **C04** (partition-half) must agree the `CapabilityBinding` shape — name this the **C42↔C04↔C43 binding freeze** (see §4).
- **C42 must precede / unblocks:** **C30** (scenario store lives in the `scenarios` partition; `depends C30 → C17, C42`), **C31/C32** (judge role binding), **C34** (audits C42's manifest), **C28** (runs as `worker` inside the partition).
- **Critical path:** T1 → T2/T3 → T4 → **T6 (C04 enforcement)** → T11. T6 is the critical node: it is where "declared" becomes "enforced" and thus where the D-1 holdout mandate is actually delivered. Everything else (T5, T7, T9, T10) hangs off the binding contract and can proceed in parallel once T3 is frozen.

## 3. Parallelization

Once **T3 (`PartitionBinding`) is frozen**, fan out independently:
- **Stream A (enforcement):** T6 (C04 integration) → T11 (AC tests). *The load-bearing stream.*
- **Stream B (worktree):** T5 (`RunPartition` lifecycle + GC).
- **Stream C (attribution/audit):** T7 (C41 wiring) → T9 (C34 surface).
- **Stream D (config safety):** T8 (reconcile invariant checks).
- **Stream E (optional):** T10 (OPA refinement) — last, gated on proving it is *not* load-bearing.

T1/T2/T3 are the only serial front-load; they are small/medium and define the contracts every stream consumes.

## 4. Interfaces-first / contract milestones

Freeze early so dependents build against stubs:
1. **`AccessMatrix` + role taxonomy (T1)** — C34/C57 audit against it; C30 reads which partition it lives in. Freeze first.
2. **`PartitionBinding` shape (T3)** — the join object across C04 (enforce), C41 (attribute), C34 (audit). The single most-shared contract; freeze before any stream forks.
3. **C42↔C04↔C43 combined `CapabilityBinding` (T6 design)** — agree the partition-half (C42) + capability-half (C43) composition C04 applies at spawn. This freeze de-risks the highest-uncertainty seam (OQ-1: the OS primitive that gives I1 teeth). Hold it jointly with the C04 and C43 builders.
4. **`RunPartition` interface (T5)** — provision/reap signatures so C28/C04 can target a worktree path against a stub.

## 5. Risks & de-risking order

1. **Spike OQ-1 first (the OS enforcement primitive).** Prototype the actual mechanism C04 uses to make `scenarios` bytes unreachable to a `worker` (mount namespace vs uid perms vs container fs view). The entire D-1 mandate rests on I1 being real; a bare chmod is too weak. Build the AC-1 attempted-access test against the prototype *before* committing the binding contract. **Highest-priority spike.**
2. **De-risk the C42↔C43 composition** (partition axis vs capability axis at one spawn seam) early — a muddled combined binding is where a leak hides.
3. **Prove OPA-optionality (T10/AC-6)** to retire the G28 ambiguity: demonstrate the worker/scenario boundary holds with OPA off, so no one is tempted to make the coarse boundary depend on the unbuilt OPA layer.
4. **`scenario-author`→`code` read path (OQ-2)** — design the gated/audited read before scenario authoring goes live, so the legitimate author-reads-code path doesn't become a scenario-intent backchannel.

## 6. Definition of done

**Per-component:**
- The closed role taxonomy + `default-deny` `AccessMatrix` exist as reconciled config; `worker`→`scenarios` deny is an asserted, reconcile-enforced invariant (I1/I2).
- `bind_partition` deterministically emits a `PartitionBinding` that C04 enforces at spawn and C34 audits — same object, no drift (I4).
- A `worker` session provably **cannot** read the `scenarios`/`judge` partition, verified by an attempted-access test failing at the OS boundary (AC-1) — the D-1 holdout mandate delivered as prevention, not discipline.
- Each run gets an isolated `RunPartition` worktree; no shared writable across parallel runs (I3/AC-4); reaped on completion with GC backstop.
- The same-provider judge reads only the frozen produced-work trajectory + scenarios, never the live worker worktree (AC-3, D-1).
- OPA (if built) refines only intra-partition rules; the coarse boundary holds with OPA disabled (AC-6, DELTA-06).
- Every partition bind + access attempt (incl. denied) is attributed (C41) and audit-visible (C34).

**Per-task:** each Txx ships its named artifact (matrix / schema / contract / lifecycle / wiring) with the corresponding acceptance criterion from spec §8 passing.

**Gaps:** **G21** (detect-only) and **G10** (discipline≠enforcement) closed by spawn-time enforcement; **G28** (composition ambiguity) closed by the authoritative order with OPA optional. **OQ-4 deferred:** residual same-provider model-prior bias is FE-1 (cross-family) territory — C42 bounds read-leakage, not correlated priors, and is not credited with closing it.
