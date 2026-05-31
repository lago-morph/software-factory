# C17 — Tool-Node Abstraction  (Build Plan, Track A)

> Source / Spec ref: [`spec/C17-tool-node-abstraction.md`](../spec/C17-tool-node-abstraction.md)
> Depends on: [`spec/C02-pack-extension-abi.md`](../spec/C02-pack-extension-abi.md) (ABI), C01 (substrate), C12/C13 (formula/molecule consumers), C16 (discipline linter consumer).

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze C17↔C02 split.** Pin which of inputs/outputs/status is C02 (wire bytes) vs C17 (workflow-level declared inputs/outputs). Resolves the §3.2 [AMBIGUITY: G29] split for downstream. | S | C02 §3.2 ABI frozen |
| T2 | **Define the node-definition shape.** The logical record `name` → C02 `[[tool]]` + `kind=deterministic` + declared inputs/outputs + determinism contract (spec §3.1). | M | T1 |
| T3 | **Define the formula/molecule reference contract.** How a C12 DAG node references a deterministic node by name + declared inputs/outputs; how C13 binds + supplies context (spec §3.2). | M | T2; C12/C13 node shape |
| T4 | **Define the node-kind tag.** The `kind=deterministic` vs model/agent distinction, machine-readable for C16 (spec §3.1 fill). Reconcile field name with C12 + C16. | S | T2 |
| T5 | **Define the determinism / safe-re-run invariant** and its test posture (spec §3.1, §6, §8.4). | S | T2 |
| T6 | **Define status/output surfacing to the work graph.** Map C02 exit-code/outputs → molecule step product → bead (C19/C20) + event bus (C23) + `created_by` (C41) (spec §3.3, §5, §7). | M | T1, T3 |
| T7 | **Reference exemplar tool nodes** across languages (Go: CXDB bridge / aggregator; Python: PyOD/HDBSCAN; CLI: Inspect AI) to validate the uniform interface (spec §8.1). | S | T2, T3 |
| T8 | **Acceptance tests** for the six spec §8 criteria. | M | T2–T7 |

## 2. Dependency graph

- **Critical path:** C02 ABI frozen → **T1** → **T2** → {**T3**, **T6**} → **T8**.
- **T1 is the gate:** nothing C17-specific can freeze until the C02↔C17 ownership split is pinned, because
  every node element (inputs/outputs/status) either belongs to C02 (cited) or C17 (defined here).
- C17 is in **Batch 1** with C02/C01; its interface contracts (T2–T4) must land early so C12/C13/C16 and
  every "tool node" component (C24, C30/C31, C32/C33, C44) can build against C17 stubs in parallel.

## 3. Parallelization

Once **T2** (node-definition shape) is drafted, these run concurrently:
- **T4** (node-kind tag) — independent field; needs only T2 + a name-reconciliation handshake with C16/C12.
- **T5** (determinism invariant + test posture) — pure contract statement.
- **T6** (status/output surfacing) — depends on T1 + T3 but not on T4/T5.
- **T7** (cross-language exemplars) — can be drafted against the T2 shape while T3 firms up binding.

T3 (formula/molecule reference) and T6 (work-graph surfacing) are the two that must converge before T8.

## 4. Interfaces-first / contract milestones

Freeze early so dependents build against stubs:
1. **M1 — C17↔C02 split (T1).** The single most load-bearing milestone; unblocks every tool-node component.
2. **M2 — Node-definition shape + reference contract (T2+T3).** Lets C12/C13 place deterministic nodes and
   lets C24/C30/C31/C32/C33/C44 author themselves as C17 nodes against a stub.
3. **M3 — Node-kind tag (T4).** Unblocks C16/A36b discipline linter (F52).

## 5. Risks & de-risking order

1. **G29 / C17↔C02 ownership ambiguity (highest).** Spike T1 first: walk one concrete node (Inspect AI CLI)
   end-to-end and confirm declared-inputs→C02 args and declared-outputs→partition-files map cleanly. If the
   split is wrong, T2–T8 churn.
2. **Gas City "tool bead" reality (G11).** The "native unified interface" is unverified. De-risk by
   validating the native tool-bead shape before freezing T2's mapping; if Gas City's native shape differs,
   T2 absorbs the impedance rather than every downstream node.
3. **Node-kind tag drift across C17/C12/C16.** De-risk via the M3 handshake — one field name agreed across
   all three before any of them ship enforcement.
4. **Hidden non-determinism in "deterministic" nodes.** Lower risk at sweep-1 (contract-only); flag for
   sweep-2/sweep-3 whether a runtime guard is in v4 scope (spec §9 Q3).

## 6. Definition of done

**Per-component:**
- All six spec §8 acceptance criteria expressible as tests (uniform cross-language placement; deterministic
  run via C02; machine-readable node-kind; safe re-run; clean failure surfacing; no new on-disk artifact).
- The §3.2 [AMBIGUITY: G29] split is pinned (M1) and cited consistently with `spec/C02-pack-extension-abi.md` §3.2.
- The node-kind tag (M3) is reconciled with C12 (formula node schema) and C16 (discipline linter).
- Open questions in spec §9 are mirrored into [`_meta/review-log.md`](../_meta/review-log.md).

**Per-task:** each Tn done when its spec section is implementable (sweep-2 signatures) and its contract is
stub-consumable by the dependents named in §4.
