# C19 — Bead store / typed work-graph  (Build Plan, canonical track)

> Source / Spec ref: [`spec/C19-bead-work-graph.md`](../spec/C19-bead-work-graph.md)
> Status: sweep-2 (implementation-ready)

## 1. Work breakdown

Ordered tasks to build C19. Sizes: S/M/L. C19 is a *native Gas City capability* (AI-CONTEXT §3.2 #2),
so "build" work is primarily **adopt + verify + bind the contract**, not author-from-scratch.

**Sweep-1 tasks (now concrete with sweep-2 detail):**

| Task | Description | Size | Prereqs | Exit criterion |
|---|---|---|---|---|
| **T1** | **Freeze the M1 bead-record contract** (spec §3.1): ship the C19↔C20 field table (`id`, `type`, `created_by`, `depends_on`, `status`, `payload`, `history`), the no-op `validate` stub seam, and the write_bead/transition_status/find_by_* logical interface signatures (spec §3.2). This is the interfaces-first freeze that breaks the C19/C20 write-path cycle (D-4). | M | spec §3/§4 finalized; C20 stub available | C20 + C18 + C39 sign off that they can build against the frozen field set |
| **T2** | **Verify Gas City native bead store + `gc bd`** against an actual `gc` install (G11 spike — PF-1 first action): exercise `gc bd` create/find-by-type/by-id/by-creator, dependency edges, and cross-session durability against `gascity-prototype@b14c278`. Record what is native vs. must-be-packed. Confirm F9 dolt-push constraint (`--ref refs/heads/dolt-data`) in the Dolt path. | M | C01 live `gc` install | Filled-in native-vs-pack table; E-C19-1 enforce strength confirmed or flagged |
| **T3** | **Bind attribution-total + typed-total + durable-across-sessions invariants** as the adopted contract (spec §3 invariants). Ratify via AC-C19-A1, AC-C19-A2. | S | T1, T2 | AC-C19-A1 passes; AC-C19-A2 passes |
| **T4** | **Prove file-backend cold-start recipe** (AC-C19-R1): write a `factory_build_in_progress` bead with C20-required fields; kill process; restart; `gc bd find --type factory_build_in_progress`; `gc converge resume <id>`. End-to-end with C20 stub. | M | T2, T3, C20 M1 stub | AC-C19-R1 passes on file backend |
| **T5** | **Implement dependency-edge + cycle-detection** (spec §4.2 + §3.1 postconditions): write_bead with `depends_on` enforces referential integrity (E-C19-5) and acyclicity (E-C19-3). Passes AC-C19-W4 + AC-C19-W5. | M | T1 | AC-C19-W4 + AC-C19-W5 pass |
| **T6** | **Bind created_by attribution path** end-to-end (stamping, §3 FAITHFUL-FILL): every create stamps a non-empty actor from acting context. Surfaces G36 self-asserted limitation at C19↔C41 seam in ops docs. | S | T3 | AC-C19-A1 passes; G36 residual risk in review-log |

**Sweep-2 tasks (implementation-ready, interfaces-first):**

| Task | Description | Size | Prereqs | Exit criterion |
|---|---|---|---|---|
| **T7a** | **Freeze C19↔C20 seam interfaces first**: the `validate(type, payload)` stub replaced by real C20 validator call; E-C19-1 enforcement wired. Unblocks all C20 downstream consumers. **Freeze this seam before T7b.** | S | T1, C20 §3.1 real validator available | AC-C19-W2 passes (unknown type rejected) |
| **T7b** | **Freeze C19↔C41 seam**: `created_by` stamping confirmed against C41 actor model; optional C41 signature hook registered (no-op until C41 ships signed provenance). | S | T1, C41 M1 stub | C41 signs off; G36 residual noted |
| **T7c** | **Concrete bead node SQL schema** (spec §4.1): map each field in the node table to a Dolt SQL column type (F9: local SQL server); including `payload` as `JSON` column. Jointl with C20 — field types in the node table match C20's logical types (C20 §4.5). Round-trip test AC-C19-W3. | M | T1, T2, C20 §4.5 frozen | AC-C19-W3 passes on Dolt backend |
| **T7d** | **Concrete edge SQL schema** (spec §4.2): `(from_id, to_id)` edge table; foreign key to node table for referential integrity (E-C19-5). Cycle-check procedure implemented in SQL or app layer. | S | T7c | AC-C19-W4 + AC-C19-W5 on Dolt backend |
| **T8a** | **Dolt-backend persistence contract** (spec §4.3): dolt push config (`DOLT_REF=refs/heads/dolt-data`); push-failure alarm (E-C19-7); ops runbook for `--ref` constraint. AC-C19-D2 test written. | M | T2, T7c | AC-C19-D1 + AC-C19-D2 pass on Dolt backend |
| **T8b** | **Status transition table** (spec §6.1 E-C19-2): implement the lifecycle DAG `open→in_progress→closed` in I6; reject backward transitions. AC-C19-Q4 passes. | S | T7c | AC-C19-Q4 passes |
| **T8c** | **History / audit interface** (spec §3.2 I7): surface Dolt versioning as the `get_history(id)` call (Dolt native branch history); timestamps monotonic. AC-C19-Q5 passes. | M | T7c | AC-C19-Q5 passes |
| **T9** | **file→Dolt migration** + schema-version pin (AI-CONTEXT §3.5). OQ-C19-2 is the gate: is a faithful migration spec in scope or a Gas City internal? Deferred until OQ-C19-2 resolved by G11 verification. | L | T8a; OQ-C19-2 resolved | Backend-transparency AC-C19-BT1 passes |

## 2. Dependency graph

- **Upstream gates**: **C01** (live `gc` binary) must exist before T2; **C03** supplies `[beads] provider`.
  T1 (contract freeze) proceeds on spec text alone — no live `gc` needed.
- **C20 seam (co-foundational, D-4)**: T7a wires the C20 real validator; C20 must ship its M1 stub before
  T1, and its real validator before T7a. Both components share the §3.1 field table as the contract boundary.
- **C41 seam**: T7b wires the attribution path; C41 M1 stub needed first.
- **Downstream dependents**: **C05, C13, C18, C35, C39, C41, C33, C52** all build against the frozen M1
  contract from T1 + T3 invariants. T7a (real C20 seam) unblocks their validation-dependent paths.
- **Critical path**: T1 (M1 freeze) → T3 (invariants) → T4 (cold-start end-to-end) → T7a (C20 seam live)
  → T7c/T7d (SQL schema) → T8a (Dolt durability) → T9 (migration, gated on OQ-C19-2).

## 3. Parallelization

After **T1 (M1 freeze + T3 invariants)** are committed:

| Stream | Tasks | Prerequisite | Concurrent with |
|---|---|---|---|
| **A — Adopt/verify** | T2 → T4 | T3 | B, C |
| **B — Graph semantics** | T5 | T1 | A, C |
| **C — Attribution** | T6 → T7b | T3; C41 stub | A, B |
| **D — SQL schema** | T7c → T7d | T2, C20 §4.5 frozen | E |
| **E — Dolt persistence** | T8a → T8b → T8c | T7c | D (after T7c done) |
| **F — Migration** | T9 | T8a; OQ-C19-2 resolved | independent |

**C20 builds in lockstep against T1** as a sixth parallel stream owned by C20. The C19↔C20 seam (T7a) is
the join point between C19 Stream D and C20's real-validator delivery.

## 4. Interfaces-first / contract milestones

Freeze in this order to maximize downstream parallelism:

1. **M1 — Bead-record contract (T1)**: the §3.1 field table + no-op `validate` stub + logical I1–I7
   signatures (spec §3.2). *Freeze first* — breaks the C19/C20 write-path cycle (D-4) and unblocks C20,
   C18, C39, C41, C33, C52 simultaneously.
2. **M2 — Store invariants (T3)**: attribution-total, typed-total, durable-across-sessions,
   backend-transparent. Adopted by C41/C18/C05/C39 as their correctness assumptions.
3. **M3 — Query surface (T2/T4)**: find-by-id/type/creator/status; the end-to-end §16 cold-start recipe
   AC-C19-R1 confirmed against the file backend.
4. **M4 — Edge / chain model (T5)**: the `depends_on` directed edge + acyclicity + referential integrity;
   the integration target for C39 (chain walks) and C35 (override links).
5. **M5 — C20 real seam (T7a)** *(sweep-2 freeze)*: the no-op stub replaced by the real `C20.validate`
   call; E-C19-1 enforce wired. **Freeze before building the SQL schema (T7c)** — the SQL types must
   agree with C20's logical types.
6. **M6 — Dolt SQL schema (T7c+T7d)**: the concrete SQL column layout; enables AC-C19-W3 round-trip test
   and the Dolt-backend persistence suite.
7. **M7 — Dolt push contract (T8a)**: `DOLT_REF=refs/heads/dolt-data` ops runbook frozen; E-C19-7 surfaced.
   Gates AC-C19-D2.

## 5. Risks & de-risking order

Spike highest-uncertainty first:

1. **Gas City bead-store reality (G11 / PF-1)** — the entire "native" claim is unproven until a real
   `gc bd` is exercised. *De-risk first* (T2): confirm create/find-by-type/edges/`created_by`/cross-session
   on an actual install. The D-23 spike established F9 (Dolt = local SQL server) and the `refs/heads/*`
   constraint; T2 extends this to the full I1–I7 surface. If anything is not native, it becomes pack work.
2. **C19↔C20 seam / G17 (blocker)** — until M1 is frozen, neither store nor schema can build, and
   AC-C19-R1 cannot run. *De-risk second* (T1): freeze M1 with C20 in the same sitting. This is the
   single most important coordination point in Batch 1's persistence pair.
3. **E-C19-1 enforce strength (G11 / OQ-C20-4)** — the D-23 harvest showed bead-prefix is the scoping
   mechanism but enforcement strength was never tested. T2 must confirm whether `gc` natively rejects
   unknown type strings (prevent) or only records them (detect-only → C02 pack enforcement). This ruling
   changes the AC-C19-W2 test from G11-gated to either native or pack-enforced.
4. **Dolt `refs/heads/*` ops constraint (F9)** — T8a must wire the `DOLT_REF=refs/heads/dolt-data`
   constraint into the ops runbook and the E-C19-7 alert before the Dolt backend goes live. Any deployment
   without this fails in proxy-mediated environments (F9 — D-23 substrate-verified).
5. **`file` backend concurrency (OQ-C19-3)** — at L4/L5 fan-out, concurrent writes to the file backend
   are unspecified. Low risk at Phase 0 (low-concurrency); flag loudly to review-log and gate T9 (migration
   design) on resolving OQ-C19-3.
6. **Attribution integrity (G36)** — `created_by` is self-asserted; T7b reserves the C41 signing hook
   but does not build it (C41 optional/deferred). Surface as residual risk in ops docs.

## 6. Definition of done

**Sweep-2 exit (implementation-ready):**

The component is implementation-ready when:
- **M1 through M7 milestones** are committed (§4 above).
- **All AC-C19-*** tests pass** on the file backend (AC-C19-BT1 is Dolt-era / G11-gated — stated, not yet
  required at Phase 0 exit).
- **C20 seam wired (T7a)**: the no-op `validate` stub is replaced by the real C20 validator call; E-C19-1
  is enforced (or marked G11-pending-T2 if Gas City accepts free-form types natively).
- **Dolt SQL schema (T7c)** maps the §4.1 node table to concrete SQL columns, round-trip confirmed (AC-C19-W3).
- **Dolt push ops runbook (T8a)** names `DOLT_REF=refs/heads/dolt-data` as mandatory; E-C19-7 alert wired.
- **OQ-C19-2** (migration) and **OQ-C19-3** (concurrency) are in the review-log with T9 explicitly deferred
  pending their resolution.
- **G17** is fully closed: C19 stores every type C20 defines; `gc bd find --type factory_build_in_progress`
  runs end-to-end (AC-C19-Q1, AC-C19-R1).
- **G36** residual risk is in the review-log: `created_by` is self-asserted; C41 signing hook is reserved
  at T7b (no-op) and flagged as the open integrity gap.

**Per-task exit (sweep-2):** each task exits when its AC-code passes:
- T1↔M1 freeze signed off by C20+C18+C39; T2↔T2 native-vs-pack table + F9 confirmed; T3↔AC-C19-A1+A2;
  T4↔AC-C19-R1 (file); T5↔AC-C19-W4+W5; T6↔AC-C19-A1 + G36 in review-log; T7a↔AC-C19-W2;
  T7b↔C41 sign-off; T7c↔AC-C19-W3; T7d↔AC-C19-W4+W5 (Dolt); T8a↔AC-C19-D2; T8b↔AC-C19-Q4;
  T8c↔AC-C19-Q5; T9↔AC-C19-BT1 (deferred, OQ-C19-2 gated).
