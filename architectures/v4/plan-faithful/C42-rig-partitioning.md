# C42 — Rig / agent-role partitioning  (Build Plan, canonical track)

> Source / Spec ref: [C42 spec (faithful)](../spec/C42-rig-partitioning.md)
> Track: A (faithful)   Status: sweep-2

C42 is **policy/config**, not a service: it defines the closed role set (worker/scenario-author/judge),
the read/write partition model with the holdout invariant (`scenarios ∉ read_partition(worker)`), the
per-run worktree-isolation policy, and the composition of the four named isolation mechanisms. The plan is
correspondingly small; the load-bearing work is **freezing contracts** that C30/C34/C43 build against and
**retiring the enforcement-strength uncertainty** (G21/OQ-C42-1).

**Sweep-2 additions to this plan:** The Sweep-2 deepening adds (a) the partition-record type + field
table, (b) the TOML config exemplars per the config-anchor file-split, (c) the `sequenceDiagram` for a
partitioned read attempt, (d) the E-code taxonomy (E-C42-01..04) and AC-code table (AC-C42-01..09),
and (e) inline OQ resolutions for OQ-C42-1 (partial), OQ-C42-2 (resolved), OQ-C42-3 (D-17 scoped),
OQ-C42-4 (resolved+nuanced). Tasks below are updated to reflect this depth.

## 1. Work breakdown

| Task | Description | Size | Prereqs | Sweep |
|---|---|---|---|---|
| **T1** | **Freeze the rig/role-declaration contract** — closed role set {worker/implementer, scenario-author, judge}, `[[rig]]` shape (`name`, `read_partition`, `write_partition`, `prefix`). (Spec §3.1, §4.1) | S | C01 partition primitive confirmed | 1 |
| **T2** | **Freeze the partition model + holdout invariant** — partition = label-addressed r/w region; named `code`/`scenarios`; `scenarios ∉ read_partition(worker)`; partition-label registry (§4.5). (Spec §3.2, §4.2) | S | T1 | 1 |
| **T3** | **Freeze the worktree-isolation contract** — one isolated writable worktree per run, scoped to rig partitions (F17); `assign_worktree` signature. (Spec §3.1, §3.3) | S | C04 session/worktree seam | 1/2 |
| **T4** | **Freeze the holdout-policy feed contract** — per-rig role + partition labels + r/w policy published for **C34 (holdout integrity & isolation enforcement)** to enforce + audit; `get_partition_policy()` signature; residual broad-tool-access read-escape detect-after-the-fact until C43. (Spec §3.1, §3.4) | S | T1, T2 | 1/2 |
| **T5** | **Write the one-line G28 authority note** — which mechanism is the declarative unit (rig `read_partition`); filesystem perms + repo realize it on disk; OPA deferred; enforcement+audit is C34's. A sweep-1 clarification, **not** a frozen composition contract (DELTA-01 "composition order" was dropped). (Spec §4.3) | S | T2 | 1 |
| **T6** | **Author `[[rig]]` config exemplars** — `scenario_authoring` + `implementer` + `judge` blocks per AI-CONTEXT §13.3 + config-anchor file-split; includes `.gc/site.toml` path-binding pattern; invalid (worker-reads-scenarios) negative example; prefix-collision negative example (F10). (Spec §4.2) | S | T1, T2, config-anchor | 2 |
| **T7** | **Author partition-record field table** — `PartitionRecord` type + R/W-by annotations (§4.1). Sweep-2 schema deliverable. | S | T1, T2 | 2 |
| **T8** | **Author E-code taxonomy** — E-C42-01..04 covering misconfig / prefix-collision / role-unmapped / partition-violation-detected; D-30 two-branch note on E-C42-04. (Spec §6.1) | S | T2, T4 | 2 |
| **T9** | **Author AC-code table** — AC-C42-01..09; cross-reference each failure-path AC to its E-code; include D-23-gated and C43-gated forward vectors. (Spec §8.1) | S | T8 | 2 |
| **T10** | **Author sequence diagram** — `sequenceDiagram` for a partitioned worker read attempt: config-load → in-partition read → out-of-partition attempt (prevent/detect branches). (Spec §5.1) | S | T4, T8 | 2 |
| **T11** | **Resolve enforcement-strength OQ (G21/OQ-C42-1)** — spike: does Gas City *reject* a config where worker `read_partition` includes `scenarios`, or merely permit-with-review? Does the worker subprocess get *prevented* from out-of-partition reads, or is it discipline + C34 detect? Feeds the C43 hand-off. D-30 makes BLOCK required regardless of spike outcome for P2/P3b. | M | T2; G11-class `gc` availability | 2 spike |
| **T12** | **Resolve role-naming + judge-partition OQs** — OQ-C42-2 (worker≡implementer — RESOLVED Sweep-2), OQ-C42-3 (judge partition — D-17 joint freeze, completion gated on C34/C32), OQ-C42-4 (`[[rig]]`/`[[rigs]]` spelling — RESOLVED+NUANCED by config anchor; city.toml spelling needs G11). (Spec §9) | S | T1 | 2 |

## 2. Dependency graph

```
C01 (partition primitive) ─┐
                           ├─► T1 ─► T2 ─► {T4, T5, T6, T7}
C04 (session/worktree) ────┴─► T3
config-anchor (file-split) ────► T6 (exemplars)
                           T2 ─► T8 (E-codes) ─► T9 (ACs)
                           T4,T8 ─► T10 (diagram)
                           T2 ─► T11 (spike) ──► C43 hand-off
                           T1 ─► T12 (OQs) ───► review-log / C34 / C32 / C43
```

- **Critical path:** T1 → T2 → (T4 + T5). These freeze the holdout invariant and the audit/composition
  contracts that C30/C34/C43 all build against. Sweep-2 adds T6+T7+T8+T9+T10 as implementation-ready
  depth that must land before C34/C32 build against the partition record.
- **Upstream blockers:** T1 needs C01's `[[rig]]`/partition primitive confirmed (G11-class — is the
  partition real in `gc`?); T3 needs C04's worktree-per-session seam. T11's spike is gated on `gc` being
  runnable end-to-end (the same G11 assumption that blocks C01/C41).
- **D-17 freeze completion gate:** T12's OQ-C42-3 completion is gated on C34 and C32 landing their
  Sweep-2 specs. C42's PROVIDING side is already specced (§4.2, §4.5 with `[D-17 freeze in progress]`
  annotations); the joint freeze completes when those sibling specs confirm or revise the judge partition
  labels.
- **Downstream consumers waiting on these freezes:** C30 (scenario store in `scenarios` partition), C34
  (holdout-integrity **enforcement + audit** reads the partition labels — D-13), C43 (bounds the residual
  broad-tool-access blast radius — the distinct lethal-trifecta boundary, D-13), C32 (judge partition
  shape — D-17).

## 3. Parallelization

- **Independent once T1+T2 land:** T4 (policy feed + signatures), T5 (composition statement), T6 (config
  exemplars), T7 (field table), T12 (OQ resolution) are all disjoint and can be authored concurrently
  once T1+T2 are frozen.
- **T8+T9+T10 are a sequential chain but independent of T5/T6/T7:** E-codes (T8) → ACs cross-refing them
  (T9) → diagram (T10). This chain can run in parallel with T5/T6/T7.
- **The one serial spike:** T11 (enforcement-strength) is the long pole and gates the C43 hand-off; start
  it as soon as T2's invariant is frozen and `gc` is available — do not let it block T4/T5/T6.
- **Cross-component parallelism:** because C42 is Batch-2 config, C30 and C34 can build against **stubbed**
  partition labels the moment T2+T4 freeze, before T11 resolves enforcement strength.

## 4. Interfaces-first / contract milestones

| Milestone | Freezes | Unblocks |
|---|---|---|
| **M1 (earliest, load-bearing)** | Holdout invariant + partition model (T2) — `scenarios ∉ read_partition(worker)`, named partitions `code`/`scenarios` | C30 (scenario partition), C34 (what "violation" means) |
| **M2** | Holdout-audit feed contract (T4) + `get_partition_policy()` signature — per-rig partition policy surface | C34 builds its detector against the published labels and signature |
| **M3** | Worktree-isolation contract (T3) + `assign_worktree` signature | C04 ↔ C42 boundary on worktree-per-run scoping |
| **M4** | One-line G28 authority note (T5) | C57 (residual-risk register). *(Not "what C43 must enforce" — holdout enforcement+audit is C34's per inventory; C43 owns the lethal-trifecta blast-radius bound. See spec review RC42-01.)* |
| **M5 (Sweep-2)** | Partition-record field table (T7) + E-codes (T8) + ACs (T9) + sequence diagram (T10) — implementation-ready depth | C34/C32 can build against the typed `PartitionRecord`; the AC suite defines the test vectors for the joint holdout-integrity test run |
| **M6 (D-17 joint freeze)** | Judge partition shape (T12 OQ-C42-3) — when C34/C32 Sweep-2 land | C32 judge harness can bind to the `judge` rig's partition labels as final, not `[D-17 freeze in progress]` |

Freeze M1 first: it is the clause F28/C34/D-1 all rest on. M2 and M4 let C34 and C43 start without waiting
on the T11 enforcement spike. M5 is the Sweep-2 gate: C34/C32 must not build against C42 stubs past this point.

## 5. Risks & de-risking order

1. **(Highest) Enforcement is discipline-only, not a real control (G21/G31/OQ-C42-1).** Per D-1 there is no
   model-family fallback, so a detect-only holdout boundary is the *sole* integrity guarantee. **De-risk
   first via T11's spike**: establish whether the worker subprocess is *prevented* from out-of-partition
   reads or only *audited after the fact*. If discipline-only, the residual risk must be loud in C34/C57.
   Per **D-30 (ADOPTED)**: prevent is *required* for P2/P3b regardless — the spike determines whether a
   watcher must be built, not whether prevention is required.
   *(Ownership of the prevention seam — **RESOLVED by D-13**: holdout-integrity enforcement + audit is
   **C34's** charter; the broad-tool-access read-escape is **C43's** distinct lethal-trifecta blast-radius
   bound; **C42 provides** the partition C34 enforces. The residual *substrate* question — does Gas City
   prevent the out-of-partition read at tool-call time, or only audit after the fact (G11) — stays for the
   spike.)*
2. **`gc` partition primitive may not exist as described (G11-class).** T1/T11 assume `[[rig]]`
   `read_partition`/`write_partition` and worktree isolation are real Gas City behavior (AI-CONTEXT §13.3 /
   F17 "native"), but this is asserted-not-run. Spike `gc` config-load with the §13.3 `[[rig]]` blocks early
   (T11) — same uncertainty that blocks C01/C41. The `read_partition`/`write_partition` field grammar is
   `needs-pinned-gc-run (G11)` per the config-anchor (§3, row "[[rig]] read_partition / write_partition").
3. **city.toml `[[rig]]` vs `[[rigs]]` spelling (OQ-C42-4 nuance).** The config anchor establishes a
   genuine contradiction between F1's "canonical `[[rig]]`" and the prototype's `city.toml.example`
   `[[rigs]]`. C42 exemplars use `[[rig]]` with `[needs G11 verification]` annotations; the city.toml
   spelling must be confirmed before C42's TOML exemplars are deployed. **Do NOT use `[[rigs]] path=`
   under any circumstances** (PackV2 error regardless of which array form is used).
4. **D-17 joint judge-partition freeze depends on C34/C32 landing.** The judge partition labels in §4.5
   are marked `[D-17 freeze in progress]` and will be revised when C34/C32 Sweep-2 specs land. C42's
   PROVIDING side is ready; the completion gate is external.
5. **Mechanism-authority ambiguity (G28) leaves downstream unsure what is authoritative today.** De-risk
   via T5's one-line authority note (rig `read_partition` = declarative unit; perms/repo realize it; OPA
   deferred; enforcement+audit is C34's) before C30/C34/C43 build — a note, not a composition stack.
6. **Role-naming drift (worker vs implementer).** OQ-C42-2 RESOLVED (Sweep-2): `worker` = `implementer`
   = same `role_kind`. Low residual risk; the `rig_name` field takes the verbatim city.toml name.

## 6. Definition of done

**Per-task:** each contract task (T1–T5, T7–T10) is done when its spec section is frozen and a downstream
consumer (C30/C34/C43/C32) can build a stub against it; T6 is done when the §4.2 TOML exemplars (incl.
both negative cases) exist with the config-anchor spelling note applied; T11/T12 are done when the OQ is
answered in review-log (or explicitly carried forward with owner + reason).

**Per-component (tied to spec §8 acceptance criteria):**
- The holdout invariant is declared and a worker-reads-`scenarios` config is documented as **invalid**
  (AC-C42-01); enforcement *strength* is recorded (T11). Holdout enforcement+audit is C34's charter; the
  broad-tool-access read-escape is C43's blast-radius bound — the split is **RESOLVED by D-13** (C42 provides
  the partition C34 enforces).
- Role closure (§8.2), partition confinement (§8.3), and worktree disjointness (§8.4, F17) hold.
- C34's holdout-integrity audit can consume C42's published partition policy (`get_partition_policy()`)
  to *detect* a `scenarios`-read violation (AC-C42-09, §8.5).
- The G28 one-line authority note and the G21/G31 detect-after-the-fact residual-risk caveat are explicit
  and discoverable by C30/C34/C43/C57 (§8.6, §8.7).
- The Sweep-2 depth deliverables are all present: partition-record field table (§4.1), TOML exemplars
  (§4.2), `sequenceDiagram` (§5.1), E-code table (§6.1), AC-code table (§8.1).
- All four OQs are resolved or explicitly scoped with owners:
  - OQ-C42-1: ownership RESOLVED (D-13); substrate question open (D-23 spike).
  - OQ-C42-2: RESOLVED (worker = implementer, same `role_kind`).
  - OQ-C42-3: SCOPED (D-17; joint freeze in progress; completes when C34/C32 land).
  - OQ-C42-4: RESOLVED (F1: `.gc/site.toml` uses `[[rig]]`) + NUANCED (city.toml spelling needs G11).
