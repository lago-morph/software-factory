# C17 — Tool-Node Abstraction  (Build Plan, canonical track)

> Source / Spec ref: [`spec/C17-tool-node-abstraction.md`](../spec/C17-tool-node-abstraction.md)
> Depends on: [`spec/C02-pack-extension-abi.md`](../spec/C02-pack-extension-abi.md) (ABI), C01 (substrate), C12/C13 (formula/molecule consumers), C16 (discipline linter consumer).
> Sweep-2 update (2026-06-01): T1 (C17↔C02 split) is RESOLVED; T2–T7 are implementation-ready; T8 is concrete. New tasks T9 (G11 spike) and T10 (C12/C16 node-kind freeze) added for Sweep-3 gating.

## 1. Work breakdown (updated for Sweep-2)

| Task | Description | Size | Status | Prerequisites |
|---|---|---|---|---|
| T1 | **Freeze C17↔C02 split.** Resolves [AMBIGUITY: G29]; Reading A confirmed (C02 = wire bytes; C17 = typed abstraction). | S | **DONE (Sweep-2)** | C02 §3.2 ABI frozen |
| T2 | **Define the node-definition shape.** `ToolNodeRef` + `ToolNodeResult` concrete typed signatures (spec §3.4). | M | **DONE (Sweep-2)** | T1 |
| T3 | **Define the formula/molecule reference contract.** `BindToolNode` + `MoleculeContext` + `PackRegistry` interface (spec §3.4). | M | **DONE (Sweep-2)** | T2; C12/C13 node shape |
| T4 | **Define the node-kind tag.** D-7 binding: `kind="tool"` is C12's vocabulary; `DeterminismTag="deterministic"` is C17's typed mapping (spec §3.1, §3.4). | S | **DONE (Sweep-2)** | T2 |
| T5 | **Define the determinism / safe-re-run invariant** and its test posture (spec §3.1, §6, AC-C17-09/10). | S | **DONE (Sweep-2)** | T2 |
| T6 | **Define status/output surfacing to the work graph.** `ToolNodeResult` carries `ExitCode`, `OutputFiles`, `CreatedBy` (D-29 wire format); bead/event attribution chain (spec §3.5, §7). | M | **DONE (Sweep-2)** | T1, T3 |
| T7 | **Cross-language exemplar validation.** `BindToolNode` + `InvokeToolNode` used identically for Go/Python/CLI tool nodes; AC-C17-12 is the test vector (spec §8.1). | S | **DONE (Sweep-2)** | T2, T3 |
| T8 | **Concrete acceptance tests** (13 AC-codes, §8.1). Includes E↔AC cross-refs for E-C17-01 through E-C17-05. | M | **DONE (Sweep-2)** | T2–T7 |
| T9 | **G11 spike: Gas City tool-bead runtime API verification.** Confirm `PackRegistry.LookupTool`, subprocess env vars, stdin behavior, and working-dir contract against a pinned `gc` install. Unblocks `[needs G11 verification]` annotations in spec §3.4/§3.6. | M | **Sweep-3 / G11 spike** | D-23 spike protocol |
| T10 | **C12/C16 node-kind field name freeze.** Joint freeze of the on-disk TOML key spelling for `kind` across C12 (formula schema), C16 (discipline linter), and C17 (typed mapping). Resolves C12:OQ-4 residual. | S | **Sweep-3 / joint C12+C16+C17 pass** | C12:OQ-4 resolved |

## 2. Dependency graph (Sweep-2 view)

- **T1 DONE** — the C17↔C02 split is settled; every downstream component can build against C17's typed
  surface (`ToolNodeRef` / `ToolNodeResult` / `BindToolNode` / `InvokeToolNode`).
- **T2–T8 DONE** — implementation-ready; C24, C30, C31, C33, C44 can build against the spec-frozen stubs.
- **Remaining critical path:** T9 (G11 spike) → unblocks `[needs G11 verification]` annotations; T10
  (joint C12/C16/C17 field-name freeze) → closes the node-kind tag residual.
- **T9 and T10 are independent** and can run in parallel in Sweep-3.

## 3. Parallelization (Sweep-3 targets)

- **T9** (G11 spike) and **T10** (node-kind field freeze) run concurrently — no dependency between them.
- All Sweep-2 work is done and stub-consumable; Sweep-3 deepening is pure verification and naming
  finalization, not new design.

## 4. Interfaces-first / contract milestones

1. **M1 — C17↔C02 split (T1). COMPLETE.** Reading A confirmed. Downstream unblocked.
2. **M2 — Typed signatures (T2+T3). COMPLETE.** `ToolNodeRef`, `ToolNodeResult`, `BindToolNode`,
   `InvokeToolNode`, `PackRegistry` are implementation-ready. C24/C30/C31/C33/C44 can build against stubs.
3. **M3 — Node-kind tag binding (T4). COMPLETE.** D-7 binding: `kind="tool"` (C12) maps to
   `DeterminismTag="deterministic"` (C17). C16's discipline linter can implement F52 against this surface.
4. **M4 — E-codes + AC-codes (T8). COMPLETE.** 6 E-codes, 13 AC-codes with E↔AC cross-refs.
5. **M5 (Sweep-3) — G11 spike verification (T9).** Confirms or adjusts `PackRegistry` / subprocess shape.
6. **M6 (Sweep-3) — On-disk `kind` field name (T10).** Joint freeze across C12/C16/C17.

## 5. Risks & de-risking order (Sweep-2 view)

1. **G11 (top remaining risk).** `PackRegistry.LookupTool` and the subprocess lifecycle are `[needs G11
   verification]`. C17's abstraction layer is designed to absorb impedance — the formula/molecule surface
   is stable; only `BoundToolNode.Command/Args` and the env-var/stdin details may shift. T9 is the resolver.
2. **Node-kind field drift (C17/C12/C16).** Partially mitigated by D-7 (taxonomy home = C12) and C17's
   typed `DeterminismTag`. Residual: the on-disk TOML key name. T10 resolves it. Low risk because D-7 is
   binding and the C17 abstraction maps `kind="tool"` uniformly.
3. **Hidden non-determinism in "deterministic" nodes.** AC-C17-09 (same inputs → same outputs test) is
   the Sweep-2 test floor. Runtime enforcement remains declared-and-tested discipline (C16/F52). Sweep-3
   may add a sandbox option but it is not in v4 scope (OQ-C17-3).
4. **`[[service]]` vs tool-node boundary for C24/C44.** C02:OQ5 notes that long-lived work (C24 directory
   watch, C44 twin) may belong on the `[[service]]` side, not under `InvokeToolNode`. C17 holds the
   spawn-per-step invariant as the faithful floor; if C24/C44 resolve to `[[service]]`, they simply do NOT
   use C17's `InvokeToolNode` — the abstraction is unchanged. Resolved at C24/C44 build time. No C17 churn.

## 6. Definition of done (Sweep-2 — achieved)

**Spec-level (achieved this sweep):**
- 6 E-codes (E-C17-01..E-C17-06) with condition/surfaced-as/caller-recovery.
- 13 AC-codes (AC-C17-01..AC-C17-13) with given/when/then; E↔AC cross-refs for all failure paths.
- 2 field tables (ToolNodeRef, ToolNodeResult) with R/W-by column.
- Concrete typed signatures: `ToolNodeRef`, `ToolNodeResult`, `BoundToolNode`, `BindToolNode`,
  `InvokeToolNode`, `PackRegistry`, `MoleculeContext`, `ToolDecl`.
- 1 `sequenceDiagram` (typed invocation through the C17 abstraction, §3.6).
- D-7 cited verbatim in spec §3.1; OQ-C17-1, OQ-C17-2, OQ-C17-4 resolved in spec §9.
- Sweep-1 content, FAITHFUL-FILL annotations, and OQs preserved in place.

**Sweep-3 gates (open):**
- T9 (G11 spike) — verify `PackRegistry` shape and subprocess lifecycle against pinned `gc`.
- T10 (C12/C16/C17 joint freeze) — finalize on-disk `kind` field name.
