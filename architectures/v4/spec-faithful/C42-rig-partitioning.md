# C42 — Rig / agent-role partitioning  (Spec, Track A)

> Source: README §"Principle 5 — Scenarios as held-out test set" (L164–177: "The agent **cannot see**
> them during work"; the 4-row table — "Scenario storage with read-isolation" = "Prevents agent from
> reading scenarios during work" / "Separate git repo + file permissions + **Gas City rig partition**";
> "Holdout integrity audit" = "Detects if isolation has been violated"; placement summary L177 "Holdout
> enforcement is filesystem permissions + agent-prompt **discipline** + audit logging"); README §Phase 2
> (L417–442: L425 "scenario storage: separate git repo + filesystem permissions enforcing
> read-only-from-implementer; **OPA policy for finer control later**"; L442 "the harder parts are … the
> **scenario isolation policy**"); README §P9 (L226 "Gas City `actor` schema (cities, **rigs**, agents)");
> AI-CONTEXT §3.3 vocabulary (L100 "rig | agent worker role"); AI-CONTEXT §13.3 (L582–608: the `[[rig]]`
> blocks — `scenario_authoring`/`implementer` with `read_partition`/`write_partition`; the comment
> "explicitly does NOT include scenarios in read_partition"; the `inspect_eval` tool node with
> `work_partition`); AI-CONTEXT §6.2 "Holdout isolation … OPA + file permissions composition" (L303);
> AI-CONTEXT §7 "Holdout enforcement: ML training pipelines" (L394); F-MODE-COVERAGE §1 (F28 "Holdout
> leakage" → "Scenario storage with read-isolation (P5 component: file permissions + OPA + rig partition)"
> — "Addressed"), §3 (F17 "Parallel agents on shared dirs lose data" → "Gas City **worktree isolation per
> session** (native); OPA policy on shared partitions" — "Addressed"); component-inventory C42 row (subsystem
> Security & Governance; kind agent-role; "Worker/scenario/judge roles with read/write partitions; worktree
> isolation per run"; maps A22i/A22k/A22l/B85; depends on C04; gaps G21, G28; foundational: no; Batch 2);
> ambiguities-and-gaps **G21** (major — holdout-integrity enforcement has no real mechanism; read-isolation
> is "discipline" + config, audit is detect-after-the-fact), **G28** (major — three/four overlapping
> mechanisms named for one boundary with no authority/composition statement), **G10** (minor — "held-out"
> implies a guarantee the mechanism doesn't provide), **G31** (blocker, C43 — lethal-trifecta boundary
> unbuilt; partitions have no enforcement teeth until isolation lands); review-log **D-1** (judge uses SAME
> provider as coder ⇒ holdout integrity rests on THIS component + role/prompt isolation, making C42
> load-bearing for C34) and **FE-1**; review-log **XC-9** (`[rigs]`/`[[rig]]` spelling inconsistent across
> C01/C03/C42).
> Inventory ID: C42   Kind: agent-role   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C42 is the **rig / agent-role partitioning layer**: it defines the closed set of **agent roles** the
factory runs (worker, scenario-author, judge) and the **read/write partitions** each role is confined to,
plus the **per-run worktree isolation** that keeps parallel runs from colliding. It is the *authorization*
half of the security model — where C41 says **who acted**, C42 says **what that actor's role is allowed to
read and write**. In v4 vocabulary a **rig** is "an agent worker role" (AI-CONTEXT §3.3); C42 owns the
`[[rig]]` partition declarations (AI-CONTEXT §13.3) and the policy that the **implementer/worker rig's
`read_partition` does NOT include `scenarios`** — the mechanism behind Principle 5's "the agent cannot see
[scenarios] during work" (README:166).

C42 is **load-bearing for holdout integrity (C34)**. Per review-log **D-1**, the judge runs on the *same
provider/family* as the coder (cross-family judging is deferred to FE-1), so the holdout guarantee that
the implementer never trained-against / read the scenarios it is judged on **cannot** rest on model-family
diversity. It rests on exactly two things: (1) **rig partitioning** (this component — the worker rig
physically/policy-cannot-read the scenario partition) and (2) **role/prompt isolation** (the worker, judge,
and scenario-author run as distinct rigs with distinct prompts and distinct partitions). C42 owns (1) and
the *role* dimension of (2). This is why C30 (scenario store) and C34 (holdout integrity) both depend on
C42.

**Responsibilities**
- Define the **closed set of agent roles (rigs)** v4 names for the evaluation/holdout boundary —
  **worker/implementer**, **scenario-author**, **judge** — and that each is a distinct `[[rig]]` with its
  own partitions (component-inventory C42 "Worker/scenario/judge roles"; AI-CONTEXT §13.3
  `scenario_authoring` + `implementer` rigs; README:171 "rig partition").
- Own the **read/write partition model**: each rig declares a `read_partition` and a `write_partition`
  (AI-CONTEXT §13.3); the partition is the unit of authorization. Assert the **holdout invariant**: the
  worker/implementer rig's `read_partition` **excludes `scenarios`** (AI-CONTEXT §13.3 comment "explicitly
  does NOT include scenarios in read_partition"; README:166).
- Own the **per-run / per-session worktree isolation**: each run gets an isolated worktree so parallel
  agents on shared dirs do not lose each other's data (component-inventory C42 "worktree isolation per
  run"; F17 "Gas City worktree isolation per session (native)"). The *session* that the worktree hangs off
  is C04's; C42 owns the *isolation policy* (one worktree per run, per-partition).
- Compose the **named isolation mechanisms** into one stated, ordered boundary: (a) separate git repo for
  scenarios, (b) filesystem permissions (read-only-from-implementer), (c) Gas City rig `read_partition`
  config, (d) OPA policy "for finer control later" (README:171/425; AI-CONTEXT §13.3/§6.2). C42 must state
  **which is authoritative and how they compose** (gap G28) — at sweep-1 altitude, as a layered defense
  with a named primary, not just an enumeration.
- Supply the **partition labels** that the **Holdout integrity audit** (C34's detector / "log audit
  checking agent reads vs scenario paths", README:173) reads against. C42 defines *what the partitions are*;
  C34 *detects violations* of them after the fact. C42 also names the residual gap that this audit is
  **detect-only, not prevent** (G21).

**Explicitly NOT**
- NOT the **scenario store** (C30). C30 owns the scenario authoring DSL, the separate repo, and the
  scenario bytes; C42 owns the *partition/role policy* that makes that store unreadable by the worker rig.
  (Inventory: C30 depends on C42; C30 = "Inspect AI scenario DSL authored in an isolated rig".)
- NOT the **holdout-integrity audit / detector** (C34). C34 *detects* that isolation was violated by
  comparing agent reads vs scenario paths (README:173). C42 *declares* the partitions C34 audits against
  and asserts the prevention invariant. Detection is C34; the partition policy is C42.
- NOT the **identity / actor model** (C41). C41 supplies the *actor* (who acted, the `created_by`); C42
  writes the read/write *policy against* that actor's role. C42 consumes C41 identity; it does not define
  it. (C41 §1 states the reverse boundary: "NOT authorization / partitioning (C42).")
- NOT the **isolation & lethal-trifecta boundary** (C43). C43 owns the Bash/network/filesystem security
  posture and twin isolation that gives partitions *enforcement teeth* (G31). C42 declares the partitions;
  C43 is what actually bounds blast radius when an agent has broad tool access. C42 depends on its policy
  being *enforced* by C43 to be more than discipline (XC-8, G21, G31 — see §6). (Inventory: C43 depends on
  C42.)
- NOT the **session & provider runtime** (C04). C04 owns the session lifecycle and the worktree-per-session
  substrate; C42 owns the *partitioning policy applied to* those worktrees (one isolated worktree per run,
  scoped to a rig's partitions). C42 depends on C04.
- NOT the **cross-family judge enforcement** (C29/C32). Per D-1/FE-1 the judge is same-provider; the
  `judge_family` policy hook is FE-1's seam, not C42's. C42's contribution to judge independence is the
  *role/partition* separation, not the model family.
- NOT a **secrets / credential store** (G37, C03/C43). C42 references partitions by label; it does not store
  keys or tokens.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C04** Session & provider runtime | Worktree-per-run isolation hangs off C04's session/worktree substrate (F17 "worktree isolation per session"). Inventory: C42 `depends on C04`. C42 adds the *partition scoping* on top of C04's session. |
| Upstream (consumes identity) | **C41** Identity / actor model | Read/write policy is written *against* the rig/agent actor C41 defines. C41 supplies "who/which role"; C42 supplies "allowed to read/write what". (C41 §1/§2 names C42 the downstream policy consumer.) |
| Upstream (substrate) | **C01** Gas City substrate | `[[rig]]` blocks, `read_partition`/`write_partition`, and worktree isolation are Gas City config/native (AI-CONTEXT §13.3; F17 "native"). C42 elaborates the substrate's partition model; it does not build a new one. > [FAITHFUL-FILL] dependency — see note. |
| Downstream (consumes partitions) | **C30** Scenario authoring & store (read-isolation) | The scenario store lives in the `scenarios` partition and the `scenario_authoring` rig; the worker rig cannot read it. C30 `depends on C42`. |
| Downstream (consumes partitions) | **C34** Holdout integrity | Holdout integrity (D-1: rests on partitioning + role isolation, not model family) is the *guarantee* C42's partition invariant provides; C34 audits reads against C42's partition labels. |
| Downstream (enforcement) | **C43** Isolation & lethal-trifecta boundary | C43 gives C42's partitions real enforcement teeth (G31); without C43, partitions are config + discipline (XC-8). C43 `depends on C42`. |
| Downstream (judge tier) | **C32** Judge harness | Runs as the **judge** rig — a distinct role/partition from the worker. Same provider as coder (D-1), so separation is by rig/partition, not family. |

C42 is **not foundational** (inventory: no) and is in **Batch 2** (built in parallel with C04/C05/C28/C29
etc.). It is **load-bearing for the evaluation tier's holdout claim** even though it is not on the Batch-1
critical path: per D-1, C34's holdout integrity has *no* model-family fallback, so the entire weight of
"the implementer did not see the scenarios" sits on C42's partition invariant plus role isolation.

## 3. Interfaces / contracts

Sweep 1 — interfaces **named and described**; concrete TOML grammar, partition-label syntax, the
audit-feed schema, and the OPA policy contract are sweep-2 deliverables.

1. **Rig / role declaration contract** — the closed vocabulary of agent **roles** (worker/implementer,
   scenario-author, judge) and the shape of a `[[rig]]` declaration: a `name`, a `read_partition`, and a
   `write_partition` (AI-CONTEXT §13.3). Any component can resolve a running agent to its rig and thus to
   its allowed partitions.
2. **Partition model contract** — what a *partition* is (a named, label-addressed region of the
   read/write surface: at minimum `code` and `scenarios`, AI-CONTEXT §13.3) and the rule that a rig may
   only read its `read_partition` and only write its `write_partition`. The **holdout invariant** —
   `scenarios ∉ read_partition(worker)` — is the load-bearing clause.
3. **Worktree-isolation contract** — the guarantee that each run/session executes in an isolated worktree
   scoped to its rig's partitions, so parallel runs neither read nor clobber each other (F17). Named here;
   the session/worktree mechanism is C04's, the partition scoping is C42's.
4. **Holdout-audit feed contract** — the named surface C42 exposes to C34's holdout-integrity audit: the
   set of partition labels + the read/write policy per rig, so C34 can compare *actual agent reads vs the
   declared partition* (README:173). C42 publishes the policy; C34 consumes it to detect violations. This
   is the **detect-only** seam (G21).
5. **Composition / authority statement** — the named, ordered relationship among the four mechanisms
   (separate repo / filesystem perms / rig `read_partition` / OPA-later) declaring which is authoritative
   (see §4.3 + the G28 AMBIGUITY in §6). This is itself a *contract* downstream components rely on so they
   know *what enforces the boundary today* vs *what is deferred*.

**Invariants**
- **Holdout invariant (load-bearing).** The worker/implementer rig's `read_partition` never includes
  `scenarios` (AI-CONTEXT §13.3). A worker rig configured with `scenarios` in its read set is an invalid
  configuration. This is the clause F28 ("Holdout leakage", Addressed) and C34 rest on.
- **Role closure.** Every running agent maps to exactly one rig/role; an agent with no rig, or a rig
  outside the named role set, is invalid. (> [FAITHFUL-FILL] — see §4.)
- **Partition confinement.** A rig reads only its `read_partition` and writes only its `write_partition`;
  cross-partition read/write is denied by policy (and, once C43 lands, enforced — G31).
- **Worktree disjointness.** Two concurrent runs never share a writable worktree path (F17).
- **Detect-only-by-default (residual).** Absent C43 enforcement, the holdout invariant is upheld by
  filesystem permissions + rig config + prompt discipline and *verified after the fact* by C34's audit,
  not *prevented* at tool-call time (G21). C42 records this so no downstream component over-trusts the
  boundary.

## 4. Data model / state

C42 owns **policy/configuration definitions**, not instance state. The rig declarations live in
`city.toml` `[[rig]]` blocks (Gas City config, AI-CONTEXT §13.3); the scenario bytes live in C30; the
worktrees are C04/Gas-City-managed filesystem state. C42 defines the *meaning and invariants* of these.

### 4.1 Rig / role declaration (the unit of policy)

| Field | Meaning | v4 source |
|---|---|---|
| `name` | the rig name; identifies the role (`implementer`, `scenario_authoring`, judge) | AI-CONTEXT §13.3 |
| role *kind* | one of worker/implementer, scenario-author, judge | component-inventory C42 "Worker/scenario/judge roles" |
| `read_partition` | the partition label(s) this rig may read | AI-CONTEXT §13.3 |
| `write_partition` | the partition label(s) this rig may write | AI-CONTEXT §13.3 |

> [FAITHFUL-FILL] **Role set = exactly {worker/implementer, scenario-author, judge}.** v4 names the
> `implementer` and `scenario_authoring` rigs verbatim (AI-CONTEXT §13.3) and the inventory names
> "Worker/scenario/judge **roles**" (C42 one-liner). The minimal faithful choice is to treat this triple as
> the *closed* role set for the holdout boundary, because v4 names no fourth evaluation role and the
> role-closure invariant ("an agent outside the named role set is invalid") needs a closed set to be
> well-defined. Whether `worker` and `implementer` are the *same* role under two names (Phase-0 `worker`
> rig, AI-CONTEXT §13.1, vs Phase-2 `implementer` rig, §13.3) is OQ-C42-2; the smallest faithful reading is
> that they are the **same role** — the Phase-0 `worker` becomes the Phase-2 `implementer` once the
> scenario partition exists, since v4 never runs both simultaneously. Concrete role↔rig-name grammar
> deferred to sweep 2.

### 4.2 Partition (the unit of authorization)

A **partition** is a named, label-addressed region of the read/write surface. v4 names at least two:
`code` and `scenarios` (AI-CONTEXT §13.3), plus `work_partition = "scenarios"` on the `inspect_eval` tool
node (§13.3). The partition is what a `read_partition`/`write_partition` points at.

> [FAITHFUL-FILL] **Partition set is open, anchored by the named two (`code`, `scenarios`).** v4 names
> `code` and `scenarios` explicitly (AI-CONTEXT §13.3). The smallest faithful reading is that the partition
> *label space* is open (other partitions may exist for other boundaries) but the **two v4-named partitions
> are mandatory** and the holdout invariant is fixed on the `scenarios` label. The concrete mapping of a
> partition label to a filesystem path / git repo / OPA resource is sweep-2 (and is exactly the G28
> composition question — see §4.3).

### 4.3 Composition of the four named mechanisms (G28)

v4 names four mechanisms for the one holdout boundary: **(a)** separate git repo for scenarios
(README:171/425), **(b)** filesystem permissions / read-only-from-implementer (README:171/425), **(c)**
Gas City rig `read_partition` config (AI-CONTEXT §13.3), **(d)** OPA policy "for finer control **later**"
(README:425). Faithful composition statement (sweep-1 altitude; see G28 AMBIGUITY in §6):

| Layer | Mechanism | Role today | v4 source |
|---|---|---|---|
| 1 (primary, present) | Gas City rig `read_partition` excludes `scenarios` | the **authoritative policy declaration** — the partition is the unit of authorization | AI-CONTEXT §13.3 |
| 2 (substrate, present) | filesystem permissions (read-only-from-implementer) + separate git repo | the **physical backstop** that realizes the partition on disk | README:171/425 |
| 3 (deferred) | OPA policy | **finer-grained control, later** — not Phase-2 baseline | README:425 ("for finer control later") |
| audit (detect-only) | Holdout integrity audit (C34) | **detects** a layer-1/2 violation after the fact | README:173; G21 |

Faithful authority ruling: the **rig `read_partition` is the authoritative policy** (it is the named
*partition* primitive and the inventory's framing), realized physically by filesystem perms + repo
separation, with OPA explicitly deferred. C42 owns layer 1 and the *statement* of layers 2–3; the audit is
C34's. (This is the smallest faithful resolution of G28 — see §6.)

### 4.4 Persistence & consistency

C42 holds **no instance state of its own**. Rig/partition policy is sourced from `city.toml` `[[rig]]`
blocks under git review (AI-CONTEXT §13.3); worktrees are C04/Gas-City filesystem state; scenario bytes are
C30. C42's only consistency requirement is the **holdout invariant** (§3): every config in which a
worker/implementer rig can read `scenarios` is invalid and must be rejected at config-load (faithful:
whether Gas City *rejects* such a config or merely *permits* it is the G21/OQ-C42-1 enforcement question —
§6).

## 5. Behavior

C42 has no control loop; its behavior is **definitional** and **config-load / run-setup**-time:

- **Definition-time**: declares the role set (rigs), the partition model, the holdout invariant, and the
  four-mechanism composition (§4.3).
- **Config-load time**: when `city.toml` is loaded, each `[[rig]]` is validated against the partition
  model; a worker/implementer rig with `scenarios` in `read_partition` is an invalid config (whether this
  is *enforced* by the substrate or relies on review is OQ-C42-1 / G21).
- **Run-setup time**: when a run starts, it is assigned its rig and an **isolated worktree** scoped to that
  rig's partitions (F17 worktree-per-session). Parallel runs get disjoint writable worktrees.
- **Audit-time (C34, not C42)**: C34's holdout-integrity audit reads C42's published partition policy and
  compares it against actual agent reads (README:173) to *detect* a violation after the fact. C42 supplies
  the policy; it does not run the audit.

(Sequence/state diagrams for config-load validation and run-setup worktree assignment are deferred to
sweep 2 per BUILDER-BRIEF altitude.)

## 6. Failure modes & handling

| F-mode / gap | Relevance | Handling in C42 (faithful) |
|---|---|---|
| **F28** Holdout leakage (F-MODE §1, "Addressed") | The core mode C42 prevents: the implementer reading the scenarios it is judged on. | **Addressed conditional on OQ-C42-1 + G31** at sweep-1 altitude by the holdout invariant (§3): `scenarios ∉ read_partition(worker)`, realized by filesystem perms + repo separation (§4.3). *Caveat (G21):* this is firm only if the worker subprocess **cannot** read outside its partition. The implementer runs as a Claude Code subprocess with broad Bash/Read tool access; nothing in faithful v4 *prevents* a read outside the declared partition until C43 isolation lands (G31). So F28 is "Addressed" as a **config + filesystem + discipline** boundary with **detect-after-the-fact** audit (C34), not tool-call-time prevention. Per D-1 there is no model-family fallback, so this caveat is load-bearing. |
| **F17** Parallel agents on shared dirs lose data (F-MODE §3, "Addressed") | Concurrent runs clobbering each other. | **Addressed** by worktree-per-run isolation (§3 contract 3); Gas City native (F17). C42 owns the policy "one isolated writable worktree per run, scoped to the rig's partitions"; the worktree substrate is C04/Gas City. |
| **G21** Holdout-integrity enforcement has no real mechanism (major) | Read-isolation is filesystem perms + rig config + "agent-prompt discipline"; the audit is detection, not prevention. | See the AMBIGUITY block below. Faithful resolution: C42 **declares** the partition policy and the holdout invariant and names the **primary mechanism** (rig `read_partition` + filesystem perms), but **faithfully records that, absent C43, enforcement is config + discipline and the audit (C34) is detect-only** — it does not invent a prevention mechanism v4 lacks. Routed to C43 + review-log as residual risk. |
| **G28** Three/four mechanisms, no authority statement (major) | Separate repo / filesystem perms / rig `read_partition` / OPA-later named for one boundary with no composition rule. | **Resolved (faithful)** by the layered composition in §4.3: rig `read_partition` authoritative, filesystem perms + repo as physical backstop, OPA explicitly deferred ("for finer control later", README:425), audit detect-only. See the §6 AMBIGUITY block for both readings. |
| **G10** "held-out" implies a guarantee the mechanism doesn't provide (minor) | The term "held-out" overstates a discipline-based boundary. | **Acknowledged**: C42 states the boundary is config + filesystem + (until C43) discipline, with detect-only audit — so "held-out" is a *policy intent verified after the fact*, not a hard guarantee, until G31/C43 closes. Surfaced as residual risk, not silently absorbed. |
| **G31** Lethal-trifecta boundary unbuilt/last (blocker, C43) | The broad-tool-access agent has no twin isolation Phase 0→3b; partitions have no teeth. | **Deferred to C43 (faithful — not C42's to build)**: C42 *declares* the partitions and depends on C43 for enforcement. C42 records (here + §7 + §9) that the holdout invariant is detect-only / discipline-backed until C43 lands. This is the XC-8 "detection-only at Phase 0" finding applied to the holdout boundary. |

> [AMBIGUITY: G21] **Is the holdout boundary an enforced control, or a config + discipline + detect-only
> arrangement?**
> Reading A (faithful-literal — config + discipline + detect): README:177 states holdout enforcement is
> "filesystem permissions + agent-prompt **discipline** + audit logging"; README:173 makes the audit a
> *detector* ("Detects if isolation has been violated"); README:425 defers OPA ("for finer control
> later"). On this reading C42 declares the partition policy and the holdout invariant, the filesystem +
> rig config realize it, and **violation is caught after the fact** by C34's audit. The implementer
> subprocess has broad tool access (G21) and nothing in faithful v4 *prevents* an out-of-partition read at
> tool-call time before C43.
> Reading B (security-consistent — should be a hard control): the Skeptic's G21 finding (major) argues a
> discipline + detect-only boundary is not real holdout enforcement; F28 is marked "Addressed" on a
> mechanism that only detects. With D-1 removing the model-family fallback, a self-asserted/detect-only
> holdout boundary is the *sole* thing standing between the implementer and the scenarios — a single
> detect-only layer for a load-bearing integrity property.
> **Pick: Reading A for the *mechanism C42 declares*, with Reading B surfaced as named residual risk.**
> Track-A faithfulness is binding: v4 says "discipline + audit logging" and "OPA … later" in plain words
> (README:177/425), so C42 **cannot make the boundary a hard enforced control** without an architectural
> change (that is C43's job, and forbidden as a C42 Track-A decision). The smallest faithful choice is to
> (1) declare the partition policy + holdout invariant (which v4 does mandate — `scenarios ∉
> read_partition(worker)`), (2) name the authoritative mechanism (§4.3 — rig `read_partition` + filesystem
> perms), (3) publish the partition policy to C34's audit, and (4) record the detect-only / discipline-
> backed residual risk (§7, §9) and route the *prevention* requirement to C43 (G31). Making the boundary a
> hard tool-call-time control is exactly a Track-B `[DELTA]` candidate (e.g., enforce read-confinement in
> the agent loop / sequence C43 earlier); in Track A it is OQ-C42-1, not a decision C42 may take.

> [AMBIGUITY: G28] **Which of the four named mechanisms is authoritative, and how do they compose?**
> Reading A (rig-partition authoritative): the inventory frames C42 as "read/write **partitions**" and
> AI-CONTEXT §13.3 makes `read_partition`/`write_partition` the primitive; filesystem perms + separate repo
> are the *physical realization*, OPA is explicitly "**later**" (README:425). → §4.3 layering.
> Reading B (filesystem-perms authoritative): README:171/177 lead with "file permissions" and
> "**filesystem permissions** + agent-prompt discipline + audit logging", suggesting the OS is the real
> boundary and the rig config is a convenience label.
> **Pick: Reading A.** Most consistent with the rest of v4: the component is *named* `rig-partitioning`,
> the inventory's one-liner is "read/write **partitions**", and §13.3 makes the `[[rig]]` partition the
> declarative unit; filesystem perms are how the partition is *enforced on disk*, not a competing
> authority. OPA is unambiguously deferred. So the faithful composition is the §4.3 layering: **rig
> `read_partition` authoritative → filesystem perms + repo backstop → OPA later → audit detect-only**. The
> remaining real question is *enforcement strength*, which is the G21 ambiguity above, not G28.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security (the central concern).** C42 is the **authorization** layer of the security model and, per
  **D-1**, the load-bearing mechanism for holdout integrity (C34) now that model-family diversity is
  deferred (FE-1). The holdout invariant (`scenarios ∉ read_partition(worker)`) is declared and realized by
  rig config + filesystem perms, but is **detect-only / discipline-backed until C43 lands** (G21, G31,
  XC-8). C42 guarantees the *policy is declared and auditable*, not that an out-of-partition read is
  *prevented at tool-call time* — that prevention is C43's. This residual risk is the load-bearing caveat
  on F28's "Addressed" and is surfaced to C43, C34, and review-log (§9).
- **Cost.** Declaring partitions and one worktree per run is cheap — config + native worktree isolation
  (F17 "native"). OPA (deferred) would add policy-engine cost; v4 parks it (README:425), so the default-path
  cost is config-only.
- **Scale.** No new store; partitions are labels and worktrees are per-run filesystem state with their own
  scale story (C04). C42 adds no scale concern beyond keeping the role set closed and the partition set
  small.
- **Observability.** C42's partition policy is exactly what makes the **holdout integrity audit** (C34)
  possible — the audit compares actual reads against the declared partition labels (README:173). C42's
  published policy *is* the observability surface for holdout violations.
- **Ops.** Rig/partition policy is sourced from `city.toml` `[[rig]]` blocks under normal git review
  (AI-CONTEXT §13.3). *Spelling caveat (XC-9):* `[rigs]` (the config section, AI-CONTEXT §3.4 "explicitly
  off" list) vs `[[rig]]` (the per-rig block, §13.3) is inconsistent across C01/C03/C42; C42 uses the
  per-rig `[[rig]]` block form from §13.3 and flags the canonical-spelling ruling to C07/integrator
  (OQ-C42-4). Enabling OPA later is an additive pack at the deferred layer-3 seam (§4.3) — additive, not a
  migration.

## 8. Acceptance criteria & test strategy

1. **Holdout invariant declared & rejected on violation (F28)**: a `city.toml` in which the
   worker/implementer rig's `read_partition` includes `scenarios` is an **invalid configuration**; the
   scenario_authoring rig may read/write `scenarios`; the implementer rig reads/writes only `code`
   (AI-CONTEXT §13.3). *(Whether Gas City actively rejects or merely permits-with-review is OQ-C42-1 / G21
   — the test asserts the *policy*; enforcement strength is C43's.)*
2. **Role closure**: every running agent resolves to exactly one rig in the closed role set
   {worker/implementer, scenario-author, judge}; an agent with no rig or an out-of-set role is invalid.
3. **Partition confinement**: a rig's declared `read_partition`/`write_partition` is the only surface it is
   *policy-authorized* to read/write; cross-partition access is denied by policy (and, once C43 lands,
   enforced — G31).
4. **Worktree disjointness (F17)**: two concurrent runs are assigned disjoint writable worktrees; neither
   can clobber the other's working files.
5. **Holdout-audit feed present (C34 seam)**: C42 publishes, per rig, its role + partition labels + r/w
   policy, and C34's holdout-integrity audit can compare actual agent reads against the declared `scenarios`
   partition to *detect* a violation (README:173). The detection path exists; the *prevention* path is
   gated on C43 (the test records this, per G21).
6. **Composition/authority statement is explicit (G28)**: the four named mechanisms are documented as a
   layered defense with the rig `read_partition` named authoritative, filesystem perms as backstop, OPA
   deferred, and audit detect-only — so downstream components (C30, C34, C43) know what enforces the
   boundary today vs what is deferred.
7. **Residual-risk caveat is discoverable (G21/G31)**: downstream consumers of the holdout guarantee (C34,
   C30, the F-mode owner C57) can discover that, absent C43 enforcement, the boundary is config + filesystem
   + discipline with detect-only audit, so they do not over-trust "held-out".
(Concrete `[[rig]]`/partition-label TOML grammar, the audit-feed schema, the OPA policy contract, and
out-of-partition-read test vectors are sweep-2 deliverables — and for the *prevention* path, are
deliverables of C43, not C42's default build.)

## 9. Open questions

- **OQ-C42-1** (→ review-log): **Does Gas City *enforce* the holdout invariant, or only declare it? (G21,
  top open question).** This is the load-bearing security decision for C42: v4 says "filesystem permissions
  + agent-prompt **discipline** + audit logging" (README:177) and the audit is a *detector* (README:173).
  Confirm whether the worker rig subprocess is *prevented* from reading outside `read_partition` at
  tool-call time, or whether the boundary is config + filesystem + discipline with C34 detecting violations
  after the fact. Per D-1 there is **no model-family fallback**, so this single boundary carries the whole
  holdout guarantee — making this exactly a Track-B `[DELTA]` candidate (enforce read-confinement / sequence
  C43 earlier) and the cross-track reconciler's call. Track A cannot make the boundary a hard control
  without an architectural change (that is C43).
- **OQ-C42-2** (→ review-log): **Are `worker` and `implementer` the same role under two names?** Phase-0
  names a `worker` rig (AI-CONTEXT §13.1); Phase-2 names an `implementer` rig (§13.3). The faithful fill
  (§4.1) treats them as the same role (the Phase-0 worker *becomes* the implementer once the scenario
  partition exists). Confirm, and confirm the canonical role↔rig-name mapping for the closed role set.
- **OQ-C42-3** (→ review-log): **Is the judge a third partition, or does it read `code` + scenario
  *results*?** v4 names `scenario_authoring` and `implementer` rigs (§13.3) but does not give the judge
  rig's `read_partition` explicitly. The judge must read the trajectory/output to score it but must remain
  role-isolated from the worker (D-1). Confirm the judge rig's partition (and whether the same-provider
  judge per D-1 needs its own partition label distinct from `code`/`scenarios`).
- **OQ-C42-4** (→ review-log, XC-9): **Canonical `[rigs]` vs `[[rig]]` spelling.** Inconsistent across
  C01/C03/C42; C42 uses `[[rig]]` per AI-CONTEXT §13.3. Owner: C07/integrator — pick one and propagate.
