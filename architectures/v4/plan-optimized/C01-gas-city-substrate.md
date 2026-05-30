# C01 — Gas City runtime substrate  (Build Plan, Track B)

> Source / Spec ref: spec-optimized/C01-gas-city-substrate.md

## 1. Work breakdown

| id | description | size | prerequisites |
|---|---|---|---|
| T1 | **Spike: obtain + run Gas City.** Clone `github.com/gastownhall/gascity`, build `gc`, run the §13.1 Phase-0 skeleton end-to-end (cold start → one agent dispatch → attributed event). This retires G11. | M | none (de-risk first) |
| T2 | **Define the `RuntimeSubstrate` interface (DELTA-01).** The thin contract every dependent codes against: `LoadConfig`, `RunFormula`, `Dispatch`, `Tick`, `Persist`, lifecycle (`Start/Reload/Drain/Shutdown/Health`). Name + signature only. | M | T1 (know real surface) |
| T3 | **Version pin + conformance suite (DELTA-02).** Pin `gc` version; author the conformance test set (provider lifecycle, dispatch, reconciler tick, event append+ordering, attribution stamp) that gates "Native" claims. | M | T2 |
| T4 | **Config-load integration (C03 seam).** Wire C01's `LoadConfig` to C03's loader; capability registry derived from `EffectiveConfig`; fail-closed activation. | S | T2, C03 contract |
| T5 | **Dispatch primitive + provider boundary (C04 seam).** `Dispatch(work_unit, target)` routing to agent-session (→C04) vs tool-node subprocess (→C02 ABI); attribution stamp on every dispatch. | M | T2, C04 + C02 contracts |
| T6 | **Reconciler primitive + bounded-tick invariant (DELTA-05).** `Tick`, per-node iteration cap, escalation to `stuck`/`needs_human`. | M | T2 |
| T7 | **Persistence mounts + attribution stamp (C41).** Storage lifecycle for bead store (C19) + event bus (C23); `created_by` injection; event-append-as-linearization-point. | M | T2, C19/C23/C41 contracts |
| T8 | **Formula execution path.** `RunFormula` → C12 parse → C13 molecule instantiation → hand to reconciler. Gated on `[formulas]`. | M | T6, C12/C13 contracts |
| T9 | **Coverage manifest (DELTA-03 / G03).** Machine-checked assertion: 5 native at Phase-0, P3 `[formulas]`-gated; CI artifact, not prose. | S | T3, T4 |
| T10 | **Degraded mode + supervised restart (DELTA-06).** Quiesce store-dependent capabilities on downstream outage; park molecules; replay-on-restart from event bus. | L | T6, T7 |
| T11 | **Conformance against a stub substrate (DELTA-01 proof).** No-op implementation passes the same suite, proving interface-not-internals coding. | S | T2, T3 |

## 2. Dependency graph

- **Upstream contracts C01 needs (interfaces, not full builds):** C03 (config loader contract), C04 (provider/session boundary), C02 (tool-node subprocess ABI), C19/C20 (bead storage + schema), C23 (event record), C41 (actor/`created_by`), C12/C13 (formula/molecule format). C01 can start the moment these are *named* (sweep-1 specs), building against stubs.
- **Critical path:** **T1 → T2 → T3** is the spine. T1 retires the project-killing G11 bet; T2 is the interface every dependent waits on; T3 makes the dependency trustworthy. Everything else hangs off T2.
- **C01 is the root of the system DAG** — almost every other component waits on T2's frozen interface. Freezing it early is the single highest-leverage scheduling act in the whole architecture.

## 3. Parallelization

Once **T2 (interface)** is frozen, these proceed as independent workstreams:
- Stream A: T4 (config seam) + T9 (coverage manifest).
- Stream B: T5 (dispatch + provider/tool-node seams).
- Stream C: T6 (reconciler + bounded tick) → T8 (formula path).
- Stream D: T7 (persistence mounts + attribution).
- Stream E: T10 (degraded/restart) — starts after T6+T7, can run alongside T8.
- T3 conformance suite (Stream F) grows continuously as A–D land, and T11 closes it.

## 4. Interfaces-first / contract milestones

Freeze in this order so the rest of the architecture unblocks:
1. **`RuntimeSubstrate` interface (T2)** — the load-bearing freeze; every dependent stubs against it.
2. **Tool-node subprocess ABI existence (T5/DELTA-04)** — co-frozen with C02; C02 owns the wire format, C01 owns "the seam exists + is conformance-tested."
3. **Provider boundary (T5)** — co-frozen with C04.
4. **Attribution stamp shape (T7)** — co-frozen with C41 so `created_by` threads cleanly.
5. **Bounded-tick contract (T6/DELTA-05)** — co-frozen with C18 so the reconciler specialization inherits termination.

## 5. Risks & de-risking order

1. **T1 first, always.** G11 is a blocker: nobody has run `gc`, the repo URL is asserted. If Gas City doesn't build/run as described, DELTA-01's portability contract is what lets the project pivot — but we must learn this in week 1, not week 12.
2. **OQ1 — interface thickness.** Spike T2 against the real Gas City surface (AI-CONTEXT §3.6: ~20 Go files for the runtime). If a thin portability contract is infeasible, DELTA-01 degrades to "document the lock-in" — decide explicitly, don't drift.
3. **DELTA-05 ownership (OQ2).** Prototype whether Gas City's reconciler already bounds iteration; determines whether T6 is "wrap" or "describe."
4. **Conformance suite as the trust anchor.** Until T3 passes on the pinned version, treat every "Native" coverage claim downstream as provisional.

## 6. Definition of done

- **Per-component:** §13.1 Phase-0 skeleton cold-starts and dispatches an attributed unit of work on a pinned `gc` (acceptance #2); conformance suite green on that version (acceptance #1); stub substrate also passes it (acceptance #6); coverage manifest asserts 5-native/P3-gated (acceptance #3).
- **Invariants proven:** attribution-total (acceptance #4), bounded reconciliation (acceptance #5), degraded-mode + supervised-restart replay with no lost committed events (acceptance #7).
- **Interface frozen + published** so all downstream components build against the `RuntimeSubstrate` contract rather than Gas City internals.
- **Open questions OQ1–OQ4 logged** to `_meta/review-log.md` with OQ1 (interface thickness) flagged as the top risk and acceptance #2 named as the G11 de-risking action.
