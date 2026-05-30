# C42 — Rig / agent-role partitioning  (Spec, Track B)

> Source: component-inventory.md C42 row (Security & Governance, agent-role, NOT foundational; maps A22i "Rig — agent worker role with read/write partitions" / A22k Polecat / A22l Mayor / B85 worktree-per-run; depends C04; gaps **G21/G28**); AI-CONTEXT §3.3 vocab (l.99–101 city/rig/agent), **§13.3 rig partitions** (l.584–608: the `[[rig]]` `read_partition`/`write_partition` TOML, the `# explicitly does NOT include scenarios in read_partition` comment, and the `[[tool]] … work_partition` sketch); README **P5** (l.164–177: "The agent cannot see them during work"; scenario storage row l.171 "Separate git repo + file permissions + Gas City rig partition"; l.177 "Holdout enforcement is filesystem permissions + agent-prompt **discipline** + audit logging"), README l.425 ("separate git repo + filesystem permissions enforcing read-only-from-implementer; OPA policy for finer control later"); F-MODE-COVERAGE **F28** ("Holdout leakage — read-isolation: perms + OPA + rig partition — Addressed", l.22), **F17** ("Parallel agents on shared dirs — Gas City worktree isolation per session (native) + OPA — Addressed", l.86); _meta **review-log D-1 / FUTURE-ENHANCEMENTS FE-1** (user 2026-05-30: Phase-0 judge is **same-provider** as coder; "holdout integrity comes from rig partitioning + role/prompt isolation"); _meta gaps **G21** (holdout enforcement is detect-only, no real prevention), **G28** (three named mechanisms — git repo + perms + rig partition + "OPA later" — with no authoritative composition), **G10** (held-out "discipline" ≠ enforcement); related specs C04 §3 (DELTA-05 isolation-at-spawn; C04 is the enforcement seam C42 declares the partition for), C41 (rig is an `Actor`; C42 enforces what C41 attributes), C28 (the worker agent with Bash/Read that must be confined), C43 (capability profile co-seam), C30 (`scenario-store`, `depends C30→C17,C42`), C34 (holdout-integrity audit).
> Inventory ID: C42   Kind: agent-role (component: the rig partition model + its enforcement contract)   Status: sweep-1
> Deltas: DELTA-01 (C42 is **the partition *model + enforcement contract*, with a single authoritative composition order** — resolves G28: the three named mechanisms become one ordered defense stack `process-confinement (mandatory floor) → filesystem perms → declared partition manifest → OPA (finer, optional)`, with process-confinement at spawn as the load-bearing layer, *not* four co-equal half-mechanisms); DELTA-02 (**read-isolation is enforced at the OS/process boundary, not by agent-prompt discipline** — closes G21/G10: the worker session is spawned inside a partition that *physically cannot* open the scenario partition's bytes; "discipline" is demoted to defense-in-depth, never the guarantee); DELTA-03 (**roles are a closed, typed taxonomy `worker | scenario-author | judge` with a declared partition-access matrix** — the corpus lists rig as one loose role; D-1 makes the *worker↔scenario/judge* read-isolation the primary holdout mechanism, so the matrix is the load-bearing artifact and is `default-deny`); DELTA-04 (**worktree-per-run is a first-class, lifecycle-managed isolation unit** — B85/F17 "native worktree" is promoted to a `RunPartition` with explicit create/confine/reap and a no-shared-writable invariant, so parallel runs cannot clobber *or* read across each other); DELTA-05 (**C42 emits a verifiable `PartitionBinding` that C04 enforces and C34 audits** — the partition is a typed, attributed object, so holdout integrity is *prevent-then-detect*: enforced at spawn (C04), continuously attributable (C41), and audited after the fact (C34) against the *same* declared manifest — closing the G21 "detect-only" gap); DELTA-06 (**OPA is positioned precisely as the finer-grained, optional layer for intra-partition rules, never the boundary itself** — resolves the G28 "OPA later" ambiguity: the coarse worker/scenario boundary never depends on OPA being built; OPA only refines *within* an already-confined partition).

## 1. Purpose & responsibility

C42 is **the rig / agent-role partitioning model and its enforcement contract**: it defines the closed set of worker roles (`worker`, `scenario-author`, `judge`), the **read/write partitions** each role is bound to, and the **mechanism that physically prevents a role from reading or writing outside its partition** — applied at process spawn, not asserted in a prompt. It is AI-CONTEXT §3.3's one-line "rig = agent worker role" (l.100) and §13.3's `[[rig]] read_partition/write_partition` TOML (l.586–597) promoted into the load-bearing security boundary of the evaluation tier.

**C42 carries the holdout-integrity weight (the D-1 mandate).** With the Phase-0 judge running on the **same provider** as the coder (D-1 / FE-1 defers cross-family judging), the cross-family independence argument is unavailable. The only thing that keeps the evaluation honest is that **the implementer worker never sees the scenarios it is being judged against**. That read-isolation *is* C42. So C42 must spec it to carry that weight: read-isolation between the `worker` partition and the `scenario`/`judge` partitions, **enforced (process-level, default-deny) not merely declared** (filesystem-permission hint + agent-prompt discipline, which is what the corpus had).

C42 owns:
- **The role taxonomy (DELTA-03).** A closed, typed set of rig roles — `worker` (the implementer; C28 runs as this), `scenario-author` (authors/edits scenarios; C30/B22), `judge` (scores trajectories; C32) — each an `Actor` of class `rig` (C41 DELTA-02). No ad-hoc roles; adding one is a config + matrix change, reviewed.
- **The partition model + access matrix (DELTA-03).** Named partitions (`code`, `scenarios`, `judge`, plus per-run `RunPartition`s) and a **default-deny access matrix** mapping `(role) → {readable partitions, writable partitions}`. The load-bearing cell: `worker` has **no** read access to `scenarios` or `judge` (AI-CONTEXT §13.3 l.596 `# explicitly does NOT include scenarios in read_partition`).
- **The `PartitionBinding` contract (DELTA-05).** The typed, attributed object handed to C04 at spawn declaring which partitions a session may read/write — the thing C04 enforces, C41 attributes, and C34 audits, all against one manifest.
- **The composition order (DELTA-01).** The single authoritative ordering of the previously-loose mechanisms (process-confinement → filesystem perms → declared manifest → OPA), with process-confinement as the mandatory floor and OPA as optional refinement (DELTA-06). This is the answer to G28.
- **Worktree-per-run isolation (DELTA-04).** The `RunPartition` lifecycle (create-confine-reap) that gives each run an isolated writable worktree so parallel agents neither clobber nor read across runs (F17/B85).

What C42 is **NOT**:
- **Not the process-spawn enforcer itself.** **C04** owns process creation and *applies* the `PartitionBinding` at spawn (C04 DELTA-05, "isolation-at-spawn"). C42 *defines and emits* the binding and the matrix; C04 is the seam that makes the OS confine the process to it. (Clean split: C42 says "the `worker` role may read `code`, never `scenarios`"; C04 launches the process inside a filesystem/namespace view where `scenarios` bytes are unreachable.)
- **Not the capability / lethal-trifecta boundary.** **C43** owns the *capability profile* (which Bash commands, which network egress, twin-vs-production target) — the axis of "what dangerous things can the agent do." C42 owns the *partition* axis — "which workspace bytes can the agent see/touch." They are co-applied at the same C04 spawn seam but are orthogonal concerns; C42 does **not** define network/Bash policy.
- **Not identity or attribution.** **C41** defines that a rig *is* an `Actor` and attributes every action. C42 enforces what that actor may read/write. C41 *labels* a cross-partition read; C42 *prevents* it.
- **Not the holdout audit.** **C34** runs the after-the-fact audit (agent reads vs scenario paths). C42 makes that audit *prevent-first* by enforcing at spawn and emitting the manifest C34 audits against; C42 is the prevention half of the prevent-then-detect pair, C34 the detection half.
- **Not the scenario store.** **C30** owns the scenario DSL + storage (separate git repo). C42 owns the *partition that store lives in* and the worker's exclusion from it. (C30 `depends C42`.)
- **Not Gas City rig vocabulary itself.** AI-CONTEXT names `rig`/`polecat`/`mayor` (A22i/k/l); `polecat`/`mayor` are Gas-Town-pack-only role names (vocab, not interface). C42 specifies the *v4-relevant role/partition semantics*, mapping onto Gas City `[[rig]]` config where it exists, not the full Gas Town role catalog.

## 2. Context & dependencies

- **Depends on (declared in inventory):**
  - **C04 (session/provider).** *The enforcement seam.* C42 emits a `PartitionBinding`; C04 applies it at process spawn (C04 DELTA-05 "isolation-at-spawn"; C04 §3 `CapabilityBinding = C43 profile + C42 partition/worktree"). C42 cannot enforce by itself — it has no process; it declares what C04 confines. This is the load-bearing dependency.
- **Co-design seams (not build-order deps, but contracts that must align):**
  - **C43 (isolation boundary).** Co-applied at the C04 spawn seam. C43 = capability/egress axis; C42 = partition/filesystem axis. They compose into the single `CapabilityBinding` C04 enforces. C42↔C43 freeze the combined binding shape early (plan §4).
  - **C41 (identity/attribution).** A rig is an `Actor` of class `rig` (C41 DELTA-02); every partition-scoped action is attributed (`created_by` = rig actor). C41 *labels* `boundary_class`; C42 supplies the partition fact that makes a cross-boundary read attributable.
  - **C03 (config/feature-flags).** The `[[rig]]` blocks and partition definitions live in layered TOML (AI-CONTEXT §13.3); section presence enables a rig/partition (C03 model). The access matrix is config, reconciled.
  - **C34 (holdout integrity).** Consumes the `PartitionBinding` manifest + emitted partition-access events to run the prevent-then-detect audit (DELTA-05). C42 is the prevention; C34 the detection.
- **Consumed by (downstream):**
  - **C28 (agent loop)** runs as a `worker` rig; its session is spawned inside the `worker` partition (excludes `scenarios`/`judge`). C28's Bash/Read tool surface is the *threat C42 contains*.
  - **C30 (scenario store)** lives in the `scenarios` partition; its authoring rig is `scenario-author`. C30 `depends C30 → C17, C42`.
  - **C31/C32 (scenario runner / judge harness)** run as the `judge` role; the runner reads `scenarios` + the *produced work trajectory*, never the worker's live worktree mid-run.
  - **C57 (failure-mode coverage)** derives F28/F17 status from C42's enforcement guarantee, not from "discipline."
- **Sits at:** the **Security & Governance** subsystem; **Batch 2** of the build order (parallel with C04/C05/C28/C29). Promoted in priority by D-1: it is now *the* holdout-integrity mechanism, so although the inventory marks it "not foundational," it is on the critical path for a trustworthy evaluation tier (C30–C34).

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete TOML schema, the `PartitionBinding` byte-shape, the full access matrix, the OPA refinement contract, and a Mermaid spawn/enforce sequence land in sweep 2). The defining move (DELTA-01/02) is that C42 specifies an **enforced** partition model with one authoritative composition order, not four co-equal hints.

**The role taxonomy (DELTA-03) — closed set:**
- `worker` — the implementer (C28). Reads/writes `code`; reads its own `RunPartition`; **denied** read on `scenarios` and `judge`.
- `scenario-author` — authors scenarios (C30/B22). Reads/writes `scenarios`; **denied** write on `code`; reads `code` only via review-gated, attributed paths (scenarios "cite original exemplar behavior", README l.428 — read of code-under-test is legitimate *for the author*, never for the worker).
- `judge` — scores trajectories (C31/C32). Reads `scenarios` + the *frozen produced-work trajectory* (the worker's *output*, not its live worktree); **denied** write on `code` and `scenarios`.

**The access matrix (DELTA-03) — `default-deny`:**

| Role | read `code` | read `scenarios` | read `judge` | write `code` | write `scenarios` | own `RunPartition` |
|---|---|---|---|---|---|---|
| `worker` | ✔ | **✘ (load-bearing)** | ✘ | ✔ | ✘ | rw |
| `scenario-author` | gated/audited | ✔ | ✘ | ✘ | ✔ | rw |
| `judge` | ✘ (reads frozen trajectory only) | ✔ | ✔ | ✘ | ✘ | ro |

The `worker`-cannot-read-`scenarios` cell is the holdout invariant that D-1 makes primary. Everything else is supporting.

**Inbound — what C42 offers:**
- `bind_partition(role, run_id) → PartitionBinding` — resolves a role + run to its concrete partition binding (readable/writable partition roots + the per-run worktree), `default-deny`, ready for C04 to enforce at spawn. **Pre:** role ∈ taxonomy; the named partitions exist (C03). **Post:** a binding whose readable set provably excludes any partition not granted in the matrix.
- `provision_run_partition(run_id, role) → RunPartition` / `reap_run_partition(run_id)` — create/destroy an isolated worktree for a run (DELTA-04). **Invariant:** no two live `RunPartition`s share a writable path.
- `resolve_matrix() → AccessMatrix` — the reconciled, config-derived matrix for audit/visualization (C34, C57 read this).

**Outbound — what C42 requires:**
- **C04 `CapabilityBinding` input (→ C04 DELTA-05):** C42's `PartitionBinding` is one half (the partition/filesystem axis) of the binding C04 applies at spawn; C43's capability profile is the other. C42 hands C04 the partition half.
- **C03 config:** `[[rig]]` blocks + partition root definitions (AI-CONTEXT §13.3 l.586–597).
- **C41 attribution:** each rig is registered as an `Actor`; bindings and partition-access events are attributed.
- **(Optional, DELTA-06) OPA policy input:** finer-grained *intra-partition* rules (e.g., which files within `code` a sub-role may touch); never the coarse worker/scenario boundary.

**Invariants:**
- **I1 — Holdout read-isolation (DELTA-02, the D-1 load-bearer):** a `worker` session, on its first and every subsequent command, **cannot read the bytes of the `scenarios` or `judge` partition**. Enforced at the OS/process boundary by C04, not by prompt. F28's "Addressed" rests on *this*, not on discipline.
- **I2 — Default-deny (DELTA-03):** any partition not explicitly granted in the matrix is unreadable and unwritable to that role. Adding access is an explicit, reviewed matrix edit.
- **I3 — No-shared-writable across runs (DELTA-04, F17):** two concurrent runs never share a writable path; each has its own `RunPartition` worktree.
- **I4 — Binding ≡ enforcement ≡ audit (DELTA-05):** the manifest C42 emits, the confinement C04 applies, and the surface C34 audits are the **same declared object** — no drift between "what was declared," "what was enforced," and "what is audited."
- **I5 — Composition order is authoritative (DELTA-01):** process-confinement is the mandatory floor; filesystem perms and the declared manifest reinforce it; OPA only refines within a confined partition. No boundary depends on OPA existing (DELTA-06).
- **I6 — Prevention precedes detection (DELTA-05):** holdout integrity is enforced *before* the worker's first read (prevent), and *also* audited after (detect) — the corpus had only detect.

## 4. Data model / state

C42 owns the **partition/role declaration + binding state**, not workspace contents:

- **`Rig` (durable, config-derived):** `{ rig_id, role ∈ {worker, scenario-author, judge}, actor_ref (C41), read_partitions[], write_partitions[], city_ref }`. Sourced from `[[rig]]` TOML (C03/AI-CONTEXT §13.3); each rig is registered as a C41 `Actor` of class `rig`.
- **`Partition` (durable, config-derived):** `{ partition_id ∈ {code, scenarios, judge, …}, root_path / git_repo_ref, kind ∈ {shared, per-run}, default_access = deny }`. `scenarios` maps to the **separate git repo** (README l.171/425) — repo separation is one layer of the stack, not the whole boundary.
- **`AccessMatrix` (durable, derived):** the reconciled `(role × partition) → {read, write}` matrix; the single artifact C34/C57 audit against and the visualizer renders. `default-deny`; explicit grants only.
- **`PartitionBinding` (per spawn, emitted to C04, DELTA-05):** `{ run_id, role, actor_ref, readable_roots[], writable_roots[], run_partition_worktree, composition = [process-confine, fs-perms, manifest, opa?], emitted_at, attribution }`. The typed object C04 enforces and C34 audits — *the* prevent-then-detect join.
- **`RunPartition` (per run, ephemeral, DELTA-04):** `{ run_id, role, worktree_path, state ∈ {provisioned, live, reaped}, created_by }`. Lifecycle-bound to the run; reaped on completion. No two live ones share a writable path (I3).
- **Not owned:** scenario contents (C30), code/work-graph (C19), the capability profile (C43), the process itself (C04), the audit results (C34). C42 references and emits into these; it stores none of their schemas.

**Consistency:** the `AccessMatrix` and partition roots are reconciled config (C03/C18 reconciler); a `PartitionBinding` is computed deterministically from `(role, run_id, matrix)` so the same role always binds the same way — making I4 (binding ≡ enforcement ≡ audit) a checkable identity, not a hope.

## 5. Behavior

**Spawn-with-partition (the holdout-critical path):** C05 dispatches work for role `worker` → C42 `bind_partition(worker, run_id)` resolves the binding (readable = `{code, run_partition}`, **excludes** `scenarios`/`judge`) and `provision_run_partition` materializes the worktree → C42 hands the `PartitionBinding` to C04 → C04 composes it with C43's capability profile into one `CapabilityBinding` and **applies it at process creation** (C04 DELTA-05) → the worker process exists in a filesystem view where `scenarios` bytes are unreachable, *before its first tool call*. The worker's later `Read`/`Bash` against a scenario path fails at the OS boundary — not because a prompt told it not to.

**Judge run (same-provider, D-1):** C32 judge dispatched as role `judge` → binds `{readable: scenarios + frozen produced-work trajectory; writable: judge}` → reads the worker's *output trajectory* (frozen, from C21/C19), never the worker's live worktree. The same-provider judge is acceptable *because* the worker never saw the scenarios — the integrity comes from the partition, exactly as D-1 states.

**Parallel runs (DELTA-04, F17):** N worker runs each get a distinct `RunPartition` worktree; no shared writable path (I3). On completion each is reaped; its trajectory is frozen for the judge.

**Prevent-then-detect (DELTA-05 → C34):** C42 enforces at spawn (prevent). C34 separately audits the emitted `PartitionBinding` manifest against actual partition-access events (detect). A divergence (an enforced binding that *should* have blocked a read that nonetheless appears) is a high-severity C34 finding — and, because of I4, it points at a concrete enforcement bug, not a discipline lapse.

**Mechanism-composition (DELTA-01, resolves G28):** for any boundary, the stack applies in order: (1) **process-confinement** at spawn (mandatory floor; C04) → (2) **filesystem permissions** (read-only mounts / uid perms; reinforcement) → (3) **declared partition manifest** (the matrix; the source of truth all layers derive from) → (4) **OPA** (optional, intra-partition refinement only; DELTA-06). The coarse worker/scenario boundary is held by (1)+(2)+(3) and never waits on (4).

## 6. Failure modes & handling

| F-mode | C42 role | Handling |
|---|---|---|
| **F28 Holdout leakage** (Addressed) | **Primary owner under D-1** | I1: `worker` cannot read `scenarios`/`judge` — enforced at the OS/process boundary by C04 (DELTA-02), not "agent-prompt discipline." With the same-provider judge (D-1), this is *the* mechanism keeping evaluation honest; the spec carries that weight. C34 audits it after the fact (prevent-then-detect, DELTA-05). **This converts F28's "Addressed" from resting on detect-only discipline (G21) to resting on spawn-time prevention.** |
| **F17 Parallel agents on shared dirs** (Addressed) | Owner (partition axis) | I3: each run gets its own `RunPartition` worktree (DELTA-04); no two live runs share a writable path. Promotes the corpus's "native worktree" to a lifecycle-managed, invariant-checked unit. |
| **G21 Holdout enforcement detect-only** | Closes | DELTA-02 + DELTA-05: enforcement moves to spawn-time process confinement; detection (C34) is retained as defense-in-depth, not the guarantee. The "discipline is not enforcement" objection (G10) is answered. |
| **G28 Three-mechanism composition ambiguity** | Closes | DELTA-01: one authoritative order (process-confine → perms → manifest → OPA), with process-confinement load-bearing and OPA optional (DELTA-06). No more "four co-equal half-mechanisms." |
| **G10 "held-out" = discipline** | Closes | I1 makes "held-out" a process-enforced guarantee, matching the term's promise. |
| Worker attempts cross-partition read (e.g., `cat scenarios/...`) | Detected + denied | Denied at OS boundary (prevent, C04); the attempt is an attributed event (C41) and a C34 audit signal — a leak *attempt* is visible even though the read fails. |
| Misconfigured matrix grants `worker` read on `scenarios` | Caught at reconcile | The `worker`→`scenarios` deny is an asserted invariant (I1); a config that violates it is rejected by C18 reconcile / a C42 self-check, not silently applied. |
| `RunPartition` not reaped (leak) | Bounded | Reap is lifecycle-bound to run completion; orphaned worktrees are garbage-collected; an unreaped writable worktree is flagged (I3 health check). |
| Lethal-trifecta exfiltration *within* an allowed command (G31) | Out of scope (C43) | C42 confines *which bytes* the worker sees, not *what dangerous commands* it can run. A Bash agent could still exfiltrate `code` it legitimately reads — that network/egress axis is **C43**'s capability profile, co-applied at the same C04 seam. C42 narrows the readable surface (smaller blast radius) but does not own egress. |

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security (the point of this component):** C42 is the holdout-integrity primary mechanism under D-1. Read-isolation is enforced at the process boundary (DELTA-02), default-deny (I2), with one authoritative composition order (DELTA-01) and prevent-then-detect coverage (DELTA-05). The separate-git-repo for `scenarios` (README l.171) is *one layer* (repo separation limits accidental checkout), not the boundary — the boundary is process confinement. OPA is optional refinement, never load-bearing (DELTA-06).
- **Cost:** negligible direct cost; the `RunPartition` worktree adds disk per concurrent run (bounded by C28's seat-pool ceiling). No model tokens. Avoiding a *second provider* (D-1's whole point) is the cost saving this component underwrites — same-provider judging is only safe *because* C42 holds the line.
- **Scale:** `RunPartition` provisioning must keep up with the parallel-run fan-out (C28 seat pool, C04 multi-session DELTA-06). Worktree create/reap is cheap (git worktree); the matrix is static config, O(1) to bind.
- **Observability:** every `bind_partition` and partition-access attempt is an attributed event (C41) on C23; the `AccessMatrix` and live `RunPartition`s are a queryable read model for C34 audit and C57 coverage. A cross-partition read *attempt* (denied) is visible — you can see someone tried.
- **Ops:** partitions/roles are reconciled config (C03/C18); adding a role or grant is a reviewed matrix edit, not code. The worktree lifecycle (provision/reap) is a substrate operation with a GC backstop.

## 8. Acceptance criteria & test strategy

1. **Holdout read-isolation is enforced, not declared (I1, DELTA-02, F28 — the load-bearing test).** A `worker` session spawned with the standard binding **cannot** read a known file in the `scenarios` partition: an explicit `Read`/`cat`/`Bash` against a scenario path **fails at the OS boundary**, verified by attempted-access (not by inspecting the prompt or trusting an audit log). *This is the single test that proves the D-1 mandate.* Mirror test: it *can* read `code`.
2. **Default-deny holds (I2).** A role with no grant on partition X cannot read or write X; granting requires an explicit matrix edit that passes review/reconcile.
3. **Same-provider judge sees only frozen output (D-1).** A `judge` session can read the frozen produced-work trajectory + scenarios but **cannot** read the worker's live `RunPartition` worktree mid-run.
4. **No shared writable across parallel runs (I3, DELTA-04, F17).** N concurrent worker runs each get a distinct writable worktree; a write in run A is invisible/unwritable to run B's path.
5. **Binding ≡ enforcement ≡ audit (I4, DELTA-05).** The `PartitionBinding` C42 emits, the confinement C04 applies, and the manifest C34 audits are byte-identical; an injected enforcement bug (binding allows what manifest forbids) is caught by the cross-check.
6. **Composition order is real (I5, DELTA-01, resolves G28).** With OPA *disabled*, the worker/scenario boundary still holds (process-confinement floor); enabling OPA only refines intra-partition rules — proving OPA is not load-bearing.
7. **Misconfiguration rejected.** A `[[rig]]` config that grants `worker` read on `scenarios` is rejected at reconcile (violates I1), not silently applied.
8. **Leak-attempt is attributable (C41/C34).** A denied cross-partition read produces an attributed event a C34 audit query surfaces.

## 9. Open questions

- **OQ-1 (enforcement primitive depth, → C04/C43 co-design):** *what* OS mechanism does C04 use to make `scenarios` bytes unreachable to a `worker` (filesystem namespace / mount-namespace / uid perms / container)? The strength of I1 depends entirely on this primitive, which C04 owns. A bare chmod is weaker than a mount-namespace. C42 declares the binding; the *teeth* are C04's — this freeze (C42↔C04) is the highest-risk seam. → review-log.
- **OQ-2 (scenario-author reads `code`, legitimately — how gated?):** scenarios "cite original exemplar behavior" (README l.428), so the *author* must read code-under-test, but the *worker* must never read scenarios. The asymmetry is real and correct, but the `scenario-author`→`code` read path needs a gated, audited contract so it isn't a backchannel that leaks scenario *intent* back into `code`. → review-log.
- **OQ-3 (judge reads the trajectory, which lives near code):** the frozen produced-work trajectory (C21) is what the judge scores; ensuring the judge reads only the *frozen* artifact and not a path that aliases into the live worker worktree is a partition-boundary detail to nail in sweep 2. → review-log.
- **OQ-4 (residual same-provider bias under D-1):** C42 guarantees the worker didn't *read* the scenarios, but same-provider judge+coder can still share *training-distribution* blind spots (the FE-1 concern). C42 cannot close that — it bounds *information leakage via reads*, not *correlated model priors*. FE-1 (cross-family) remains the only fix for the latter; C42 should not be credited with closing it. → review-log.
