# C42 — Rig / agent-role partitioning  (Build Plan, Track A)

> Source / Spec ref: [C42 spec (faithful)](../spec/C42-rig-partitioning.md)
> Track: A (faithful)   Status: sweep-1

C42 is **policy/config**, not a service: it defines the closed role set (worker/scenario-author/judge),
the read/write partition model with the holdout invariant (`scenarios ∉ read_partition(worker)`), the
per-run worktree-isolation policy, and the composition of the four named isolation mechanisms. The plan is
correspondingly small; the load-bearing work is **freezing contracts** that C30/C34/C43 build against and
**retiring the enforcement-strength uncertainty** (G21/OQ-C42-1).

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** | **Freeze the rig/role-declaration contract** — closed role set {worker/implementer, scenario-author, judge}, `[[rig]]` shape (`name`, `read_partition`, `write_partition`). (Spec §3.1, §4.1) | S | C01 partition primitive confirmed |
| **T2** | **Freeze the partition model + holdout invariant** — partition = label-addressed r/w region; named `code`/`scenarios`; `scenarios ∉ read_partition(worker)`. (Spec §3.2, §4.2) | S | T1 |
| **T3** | **Freeze the worktree-isolation contract** — one isolated writable worktree per run, scoped to rig partitions (F17). (Spec §3.3) | S | C04 session/worktree seam |
| **T4** | **Freeze the holdout-audit feed contract** — per-rig role + partition labels + r/w policy published for C34's audit (detect-only seam). (Spec §3.4) | S | T1, T2 |
| **T5** | **Write the G28 composition/authority statement** — layered defense: rig `read_partition` authoritative → filesystem perms + repo backstop → OPA deferred → audit detect-only. (Spec §4.3) | S | T2 |
| **T6** | **Author `[[rig]]` config exemplars** — `scenario_authoring` + `implementer` blocks per AI-CONTEXT §13.3, plus the invalid (worker-reads-scenarios) negative example. | S | T1, T2 |
| **T7** | **Resolve enforcement-strength OQ (G21/OQ-C42-1)** — spike: does Gas City *reject* a config where worker `read_partition` includes `scenarios`, or merely permit-with-review? Does the worker subprocess get *prevented* from out-of-partition reads, or is it discipline + C34 detect? Feeds the C43 hand-off. | M | T2; G11-class `gc` availability |
| **T8** | **Resolve role-naming + judge-partition OQs** — OQ-C42-2 (worker≡implementer?), OQ-C42-3 (judge partition), OQ-C42-4 (`[rigs]`/`[[rig]]` spelling, XC-9). | S | T1 |

## 2. Dependency graph

```
C01 (partition primitive) ─┐
                           ├─► T1 ─► T2 ─► {T4, T5, T6}
C04 (session/worktree) ────┴─► T3
                                  T2 ─► T7 (spike) ──► C43 hand-off
                                  T1 ─► T8 (OQs) ────► review-log / C07 / C34 / C43
```

- **Critical path:** T1 → T2 → (T4 + T5). These freeze the holdout invariant and the audit/composition
  contracts that C30/C34/C43 all build against. Everything else hangs off them.
- **Upstream blockers:** T1 needs C01's `[[rig]]`/partition primitive confirmed (G11-class — is the
  partition real in `gc`?); T3 needs C04's worktree-per-session seam. T7's spike is gated on `gc` being
  runnable end-to-end (the same G11 assumption that blocks C01/C41).
- **Downstream consumers waiting on these freezes:** C30 (scenario store in `scenarios` partition), C34
  (holdout audit reads the partition labels), C43 (enforces partition confinement).

## 3. Parallelization

- **Independent once T1+T2 land:** T4 (audit feed), T5 (composition statement), T6 (config exemplars) are
  disjoint and can be authored concurrently by separate workstreams.
- **Independent of the contract path:** T8 (the naming/spelling/judge-partition OQs) only needs T1 and can
  run in parallel with the whole T2→T4/T5 chain.
- **The one serial spike:** T7 (enforcement-strength) is the long pole and gates the C43 hand-off; start it
  as soon as T2's invariant is frozen and `gc` is available — do not let it block T4/T5/T6.
- **Cross-component parallelism:** because C42 is Batch-2 config, C30 and C34 can build against **stubbed**
  partition labels the moment T2+T4 freeze, before T7 resolves enforcement strength.

## 4. Interfaces-first / contract milestones

| Milestone | Freezes | Unblocks |
|---|---|---|
| **M1 (earliest, load-bearing)** | Holdout invariant + partition model (T2) — `scenarios ∉ read_partition(worker)`, named partitions `code`/`scenarios` | C30 (scenario partition), C34 (what "violation" means) |
| **M2** | Holdout-audit feed contract (T4) — per-rig partition policy surface | C34 builds its detector against the published labels |
| **M3** | Worktree-isolation contract (T3) | C04 ↔ C42 boundary on worktree-per-run scoping |
| **M4** | Composition/authority statement (T5) | C43 (what it must *enforce*), C57 (residual-risk register) |

Freeze M1 first: it is the clause F28/C34/D-1 all rest on. M2 and M4 let C34 and C43 start without waiting
on the T7 enforcement spike.

## 5. Risks & de-risking order

1. **(Highest) Enforcement is discipline-only, not a real control (G21/G31/OQ-C42-1).** Per D-1 there is no
   model-family fallback, so a detect-only holdout boundary is the *sole* integrity guarantee. **De-risk
   first via T7's spike** + the C43 hand-off: establish whether the worker subprocess is *prevented* from
   out-of-partition reads or only *audited after the fact*. If discipline-only, the residual risk must be
   loud in C34/C57 and route the prevention requirement to C43 (a Track-B `[DELTA]` candidate).
2. **`gc` partition primitive may not exist as described (G11-class).** T1/T7 assume `[[rig]]`
   `read_partition`/`write_partition` and worktree isolation are real Gas City behavior (AI-CONTEXT §13.3 /
   F17 "native"), but this is asserted-not-run. Spike `gc` config-load with the §13.3 `[[rig]]` blocks early
   (T7) — same uncertainty that blocks C01/C41.
3. **Mechanism-composition ambiguity (G28) leaves downstream unsure what enforces the boundary.** De-risk
   via T5's explicit layered/authority statement before C30/C34/C43 build.
4. **Role-naming drift (worker vs implementer; `[rigs]` vs `[[rig]]`, XC-9).** Low impact but cheap to
   retire — T8 early so config exemplars (T6) and C07's glossary use one canonical spelling.

## 6. Definition of done

**Per-task:** each contract task (T1–T5) is done when its spec section is frozen and a downstream
consumer (C30/C34/C43) can build a stub against it; T6 is done when the §13.3-faithful exemplars (incl. the
invalid negative case) exist; T7/T8 are done when the OQ is answered in review-log (or explicitly carried
forward with owner + reason).

**Per-component (tied to spec §8 acceptance criteria):**
- The holdout invariant is declared and a worker-reads-`scenarios` config is documented as **invalid**
  (§8.1); enforcement *strength* is recorded (T7) and the prevention path handed to C43.
- Role closure (§8.2), partition confinement (§8.3), and worktree disjointness (§8.4, F17) hold.
- C34's holdout-integrity audit can consume C42's published partition policy to *detect* a `scenarios`-read
  violation (§8.5).
- The G28 composition/authority statement and the G21/G31 detect-only residual-risk caveat are explicit and
  discoverable by C30/C34/C43/C57 (§8.6, §8.7).
- All four OQs are in review-log with owners (OQ-C42-1 → reconciler/C43; OQ-C42-2/3 → C42+C34; OQ-C42-4 →
  C07/integrator).
