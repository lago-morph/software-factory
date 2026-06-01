# C42 — Rig / agent-role partitioning  (Spec, canonical track)

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
> Inventory ID: C42   Kind: agent-role   Status: sweep-2
> Track: A (faithful)
> Binding decisions obeyed: **D-1** (same-provider judge → holdout rests on partition+role isolation),
> **D-13** (C34 enforces+audits; C43 blast-radius; C42 PROVIDES — not enforces), **D-17** (joint C42/C34/C32
> Sweep-2 partition-shape freeze), **D-30** (prevent/block required for unattended; watcher design deferred
> to D-23 spike), **D-31** (multiple rigs per city — partition contract operates over N rigs; worker-rig ≠
> judge-rig), **D-32** (rig config spelling is file-split — `.gc/site.toml` uses `[[rig]]` with `path`;
> `city.toml` spelling is needs-pinned-gc-run G11; `[[rigs]] path =` is a PackV2 error).

> [D-23 substrate-verified — gascity-prototype@b14c278, 2026-05-25] Two substrate facts directly underwrite
> this spec: **(F1)** `[[rig]]` (singular) is the canonical block spelling; `[[rigs]] path=` is a PackV2
> error; path bindings live in `.gc/site.toml` (entrypoint-written). The city.toml `[[rig]]`/`[[rigs]]`
> spelling divergence between F1's "canonical `[[rig]]`" ruling and the prototype's `city.toml.example`
> using `[[rigs]]` is the **anchor contradiction** — see §4.2 spelling note and OQ-C42-4 resolution.
> **(F10)** Bead prefix is the **partition scoping mechanism** (agents on rig1 see/write only `r1-` beads;
> explicit `prefix=` required to avoid auto-derived collisions). Enforcement *strength* (prevent vs detect)
> was **not tested** and remains OPEN (D-23 spike Test A).

## 1. Purpose & responsibility

C42 is the **rig / agent-role partitioning layer**: it defines the closed set of **agent roles** the
factory runs (worker, scenario-author, judge) and the **read/write partitions** each role is confined to,
plus the **per-run worktree isolation** that keeps parallel runs from colliding. It is the *authorization*
half of the security model — where C41 says **who acted**, C42 says **what that actor's role is allowed to
read and write**. In v4 vocabulary a **rig** is "an agent worker role" (AI-CONTEXT §3.3); C42 owns the
`[[rig]]` partition declarations (AI-CONTEXT §13.3) and the policy that the **implementer/worker rig's
`read_partition` does NOT include `scenarios`** — the mechanism behind Principle 5's "the agent cannot see
[scenarios] during work" (README:166). (Faithful precision per G10: this makes the worker rig
*policy-denied* read of the scenario partition — filesystem perms + rig config — **not** a hard physical
control until C43 lands; see §6/G21.)

**[D-31 ADOPTED 2026-06-01 — Multiple rigs per city; partition contract operates over N rigs]**

> "A *city* (one Gas City install / the `gc` substrate, C01) hosts **multiple rigs** (C42) — not one.
> The `[[rig]]`/`[[rigs]]` array-of-tables declares N rig partitions inside a single city;
> **rig partitioning (C42) is the isolation of these N co-resident rigs from one another** (e.g. a
> worker rig and a separate judge rig living in the same city — the D-17 holdout read-surface depends
> on worker-rig ≠ judge-rig). Specs MUST model multiple-rigs-per-city explicitly and MUST NOT assume
> one-rig-per-city."
> — review-log D-31 (Sweep-2 spine-run decisions, 2026-06-01)

**C42's partition contract therefore operates over N rigs per city** — not a singleton. The `[[rig]]`/`[[rigs]]` array-of-tables in a city's config declares all N co-resident rig partitions; the partition isolation this component defines is fundamentally *between* multiple rigs sharing the same Gas City install. The D-17 holdout design (worker-rig ≠ judge-rig) is the canonical instance: both rigs reside in the same city, and the partition boundary between them is exactly what C42 provides. All contracts in this spec (§3, §4, §5) are stated over the set of N rigs, not a single rig.

C42 is **load-bearing for holdout integrity (C34)**. Per review-log **D-1**, the judge runs on the *same
provider/family* as the coder (cross-family judging is deferred to FE-1), so the holdout guarantee that
the implementer never trained-against / read the scenarios it is judged on **cannot** rest on model-family
diversity. It rests on exactly two things: (1) **rig partitioning** (this component — the worker rig is
*policy-denied* read of the scenario partition; a hard physical control awaits C43, G21) and (2)
**role/prompt isolation** (the worker, judge,
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
- State **which** of the v4-named mechanisms is authoritative (gap G28) — a *one-line authority note*, not
  a formal composition stack: (a) separate git repo for scenarios, (b) filesystem permissions
  (read-only-from-implementer), (c) Gas City rig `read_partition` config, (d) OPA policy "for finer control
  later" (README:171/425; AI-CONTEXT §13.3/§6.2). C42 names the rig `read_partition` the authoritative
  declarative unit and perms/repo its on-disk realization. (Per the capability-for-principle bar, DELTA-01
  "partition model + composition order" was dropped; the KEEP is the 3-role taxonomy + holdout invariant —
  this is a clarifying note, not a partition-composition primitive.)
- Supply the **partition labels** that **C34 (holdout integrity & isolation enforcement)** enforces and
  audits against ("log audit checking agent reads vs scenario paths", README:173). C42 defines *what the
  partitions are*; C34 *enforces and audits* them. C42 also names the residual gap (G21): against a worker
  with broad tool access, the realized boundary is filesystem perms + config + prompt discipline, so the
  read-escape that C34's enforcement cannot itself shut is the part that stays **detect-after-the-fact**
  until C43's lethal-trifecta isolation lands (G31).

**Explicitly NOT**
- NOT the **scenario store** (C30). C30 owns the scenario authoring DSL, the separate repo, and the
  scenario bytes; C42 owns the *partition/role policy* that makes that store unreadable by the worker rig.
  (Inventory: C30 depends on C42; C30 = "Inspect AI scenario DSL authored in an isolated rig".)
- NOT the **holdout-integrity enforcement + audit** (C34). Per inventory, C34 = "Holdout integrity &
  isolation **enforcement** … Read-isolation policy (perms + OPA + rig partition) + after-the-fact audit;
  … enforcement". C34 *owns* enforcing the holdout read-isolation and auditing reads vs scenario paths
  (README:173); C42 *declares* the partition labels/invariant that C34 enforces and audits against. The
  policy declaration is C42; the **enforcement + audit is C34**. (C42 does not over-claim that this
  enforcement is C43's — see the C43 bullet for the *distinct* lethal-trifecta boundary.) **This boundary
  is settled by D-13 — see §6.**
- NOT the **identity / actor model** (C41). C41 supplies the *actor* (who acted, the `created_by`); C42
  writes the read/write *policy against* that actor's role. C42 consumes C41 identity; it does not define
  it. (C41 §1 states the reverse boundary: "NOT authorization / partitioning (C42).")
- NOT the **isolation & lethal-trifecta boundary** (C43). C43 owns the Bash/network/filesystem security
  posture and twin isolation (G31) — the boundary that bounds blast radius when an agent has *broad tool
  access*. This is **distinct from** holdout read-isolation enforcement (C34's charter): C43 closes the
  residual read-escape that broad tool access opens, which neither C42's policy nor C34's enforcement can
  themselves shut (XC-8, G21, G31 — see §6). C42 declares the partitions; C43 bounds the trifecta blast
  radius. (Inventory: C43 depends on C42.)
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
| Upstream (substrate) | **C01** Gas City substrate | > [FAITHFUL-FILL] — **dependency not declared in inventory** (inventory C42 `depends on` = C04 only); faithful fill. `[[rig]]` blocks, `read_partition`/`write_partition`, and worktree isolation are the Gas City config/native primitive C42 elaborates (AI-CONTEXT §13.3; F17 "native"); C42 does not build a new substrate. |
| Downstream (consumes partitions) | **C30** Scenario authoring & store (read-isolation) | The scenario store lives in the `scenarios` partition and the `scenario_authoring` rig; the worker rig cannot read it. C30 `depends on C42`. |
| Downstream (holdout enforcement + audit) | **C34** Holdout integrity & isolation **enforcement** | Per inventory C34 = "Read-isolation policy (perms + OPA + rig partition) + after-the-fact audit; … **enforcement**". C34 *owns* holdout read-isolation enforcement+audit; it consumes C42's partition labels (the declarative unit) as the policy it enforces and audits reads against (D-1: the guarantee rests on partitioning + role isolation, not model family). C42 supplies the labels; **C34 enforces and audits** them. (D-13) |
| Downstream (broad-tool-access blast radius) | **C43** Isolation & lethal-trifecta boundary | Distinct boundary: C43 owns the Bash/network/fs security posture + twin isolation (G31). It backstops *any* partition once an agent has broad tool access — the residual read-escape C42's policy + C34's enforcement cannot themselves close. Without C43 the broad-tool-access escape stays open (XC-8). C43 `depends on C42`. |
| Downstream (judge tier) | **C32** Judge harness | Runs as the **judge** rig — a distinct *role* from the worker (one of the three KEEP roles). Same provider as coder (D-1), so separation is by rig/role, not family. Judge partition read-surface shape is the **joint C42/C34/C32 freeze** under D-17 (in progress this run — see §9 OQ-C42-3). |

C42 is **not foundational** (inventory: no) and is in **Batch 2** (built in parallel with C04/C05/C28/C29
etc.). It is **load-bearing for the evaluation tier's holdout claim** even though it is not on the Batch-1
critical path: per D-1, C34's holdout integrity has *no* model-family fallback, so the entire weight of
"the implementer did not see the scenarios" sits on C42's partition invariant plus role isolation.

## 3. Interfaces / contracts

Sweep 1 — interfaces **named and described**; Sweep 2 — concrete TOML grammar, partition-record schemas,
sequence diagram, E-codes, and AC-codes added below.

1. **Rig / role declaration contract** — the closed vocabulary of agent **roles** (worker/implementer,
   scenario-author, judge) and the shape of a `[[rig]]` declaration: a `name`, a `read_partition`, a
   `write_partition`, and (city.toml only) a bead `prefix` (F10; the scoping mechanism). Any component can
   resolve a running agent to its rig and thus to its allowed partitions and bead prefix.
2. **Partition model contract** — what a *partition* is (a named, label-addressed region of the
   read/write surface: at minimum `code` and `scenarios`, AI-CONTEXT §13.3) and the rule that a rig may
   only read its `read_partition` and only write its `write_partition`. The **holdout invariant** —
   `scenarios ∉ read_partition(worker)` — is the load-bearing clause.
3. **Worktree-isolation contract** — the guarantee that each run/session executes in an isolated worktree
   scoped to its rig's partitions, so parallel runs neither read nor clobber each other (F17). Named here;
   the session/worktree mechanism is C04's, the partition scoping is C42's.
4. **Holdout-policy feed contract** — the named surface C42 exposes to **C34 (holdout integrity &
   isolation enforcement)**: the set of partition labels + the read/write policy per rig, so C34 can
   enforce and compare *actual agent reads vs the declared partition* (README:173). C42 publishes the
   policy; C34 consumes it to enforce and audit it. Against a broad-tool-access worker the residual
   read-escape this feed cannot itself close is **detect-after-the-fact** until C43 (G21, G31).
5. **Composition / authority note (G28 — not a frozen contract)** — a *one-line* sweep-1 clarification of
   which of the named mechanisms is the declarative unit (rig `read_partition`), with filesystem perms +
   separate repo as its on-disk realization and OPA explicitly deferred (see §4.3 + the G28 AMBIGUITY in
   §6). This answers the G28 gap; it is **not** a formal partition-composition stack and not a separate
   interface downstream components freeze against (per the capability-for-principle bar: C42 DELTA-01
   "composition order" was dropped — KEEP is the 3-role taxonomy/holdout invariant only). Downstream
   components read it to know *what is authoritative today* vs *what is deferred*.

**Invariants**
- **Holdout invariant (load-bearing).** The worker/implementer rig's `read_partition` never includes
  `scenarios` (AI-CONTEXT §13.3). A worker rig configured with `scenarios` in its read set is an invalid
  configuration. This is the clause F28 ("Holdout leakage", Addressed) and C34 rest on.
- **Role closure.** Every running agent maps to exactly one rig/role; an agent with no rig, or a rig
  outside the named role set, is invalid. (> [FAITHFUL-FILL] — see §4.)
- **Partition confinement.** A rig reads only its `read_partition` and writes only its `write_partition`;
  cross-partition read/write is denied by policy (and, once C43 lands, enforced — G31).
- **Prefix uniqueness.** Each rig's bead prefix (`r1-`, `r2-`, etc.) must be *explicitly declared* in
  `city.toml`; relying on auto-derivation from the rig name is a misconfiguration — rig names with shared
  prefixes (e.g. `rig1`/`rig2` both derive `"ri"`) collide at startup (F10).
- **Worktree disjointness.** Two concurrent runs never share a writable worktree path (F17).
- **Detect-after-the-fact-by-default (residual).** The holdout invariant is upheld by filesystem
  permissions + rig config + prompt discipline and **enforced + verified by C34** (holdout integrity &
  isolation enforcement); against a broad-tool-access worker the residual read-escape is *not prevented*
  at tool-call time until C43's lethal-trifecta isolation lands (G21, G31). C42 records this so no
  downstream component over-trusts the boundary.

### 3.1 Concrete signatures (Sweep-2)

C42 is **config + policy**, not a service, so its "signatures" are the **config contract** (TOML shape)
and the **partition-record type** C34/C32/C43 freeze against.

**Partition record** — the typed artifact C34/C32 consume to enforce and audit (F-mode and AC-code
cross-refs in §4.1 and §8):

```
PartitionRecord {
  rig_name:       string          // must match [[rig]] name in city.toml; non-empty
                                  // NOTE: rig_name is the TOML config key value (e.g. "implementer", "worker");
                                  // role_kind is the ABSTRACT role class (e.g. worker). These are DISTINCT:
                                  // a [[rig]] with name="implementer" maps to role_kind=worker (OQ-C42-2 RESOLVED).
                                  // C34/C32 consumers: match on role_kind for policy logic; use rig_name for
                                  // config lookup and bead-prefix scoping. Do NOT conflate rig_name with role_kind.
  role_kind:      RoleKind        // enum: worker | scenario_author | judge
                                  // "worker" covers both Phase-0 "worker" and Phase-2 "implementer" rig names
                                  // (OQ-C42-2 RESOLVED — same role, different TOML name by phase)
  read_partition: set<string>     // partition labels this rig may read; validated holdout invariant
  write_partition: set<string>    // partition labels this rig may write
  bead_prefix:    string          // the scoping mechanism (F10); e.g. "r1", "r2" (explicit, no auto-derive)
}
```

**Config-load result** — returned (or error) when `city.toml` is loaded:

```
validate_partition_config(city_toml: CityToml) -> Result<[PartitionRecord], ConfigError>
  // raises E-C42-01 if any rig has scenarios in read_partition (holdout invariant violation)
  // raises E-C42-02 if two rigs have the same bead_prefix (prefix collision)
  // raises E-C42-03 if a rig has no role_kind (role-unmapped)
  // returns the closed set of PartitionRecord for the configured role set
```

**Holdout-policy feed** — the surface C34 calls:

```
get_partition_policy() -> [PartitionRecord]
  // C34 calls this to get the current partition policy for enforcement and audit
  // Returns the validated partition set; never includes a worker rig with scenarios in read_partition
```

**Worktree-isolation contract** — invoked by C04/Gas City at run setup:

```
assign_worktree(session_id: string, rig_name: string, partition_record: PartitionRecord)
  -> Result<WorktreePath, ConfigError>
  // Each session gets one isolated writable worktree path scoped to its rig's partitions
  // Two concurrent sessions with the same rig must receive disjoint WorktreePaths (F17 invariant)
```

## 4. Data model / state

C42 owns **policy/configuration definitions**, not instance state. The rig declarations live in
`city.toml` `[[rig]]` blocks (Gas City config, AI-CONTEXT §13.3); the scenario bytes live in C30; the
worktrees are C04/Gas-City-managed filesystem state. C42 defines the *meaning and invariants* of these.

### 4.1 Partition record — field table (Sweep-2)

The **partition record** is the unit of policy C34 and C32 freeze against. Every field is derived from
the `[[rig]]`/`[[rigs]]` block in `city.toml` at config-load.

| Field | Type | Req? | Semantics | R/W by |
|---|---|---|---|---|
| `rig_name` | `string` | R | Identifier matching the `name =` key in the `[[rig]]` block; non-empty; must be unique per city.toml. | C42 reads from city.toml; C34/C32/C43 read via `get_partition_policy()` |
| `role_kind` | `enum{worker, scenario_author, judge}` | R | The abstract role class (resolved role set — OQ-C42-2 resolves `worker`=`implementer`, see §9). Out-of-set → E-C42-03. | C42 classifies; C34/C32 consume |
| `read_partition` | `set<string>` | R | Partition labels this rig may read. **Holdout invariant:** `"scenarios" ∉ read_partition` when `role_kind=worker`. Violation → E-C42-01. | C42 reads; C34 enforces; C43 backstops |
| `write_partition` | `set<string>` | R | Partition labels this rig may write. Typically the same as the roles it authors. | C42 reads; C34 enforces |
| `bead_prefix` | `string` | R | Explicit prefix for bead IDs scoped to this rig (the scoping mechanism, F10). Must be unique across all rigs in this city; duplicate prefix → E-C42-02. Auto-derived prefix from rig name is a misconfiguration (F10 collision risk). | C42 validates; C01/Gas City runtime applies |

### 4.2 `city.toml` rig-block config surface (Sweep-2)

**[D-32 ADOPTED 2026-06-01 — Rig config spelling is file-split]**

> "Rig **path** bindings live in **`.gc/site.toml`** as **`[[rig]]`** (singular array-of-tables,
> `name` + `path`) — harvest-verified. The **`city.toml`** rig block (partition / `prefix` / role
> semantics, **no `path`**) is spelled **`[[rigs]]`** (plural) in the prototype's actual
> `city.toml.example`, contradicting D-23 F1's blanket "`[[rig]]` singular canonical" — so the
> **`city.toml` rig-block spelling is `needs-pinned-gc-run (G11)`** and specs MUST NOT assert a
> single canonical `city.toml` spelling. `[[rigs]] path =` (a `path` in `city.toml`) is an
> unambiguous PackV2 error."
> — review-log D-32 (Sweep-2 spine-run decisions, 2026-06-01)

> **DRIFT-CRITICAL SPELLING NOTE (from gascity-config-anchor §3, applies verbatim here).**
> The harvest's F1 states "canonical spelling is `[[rig]]` (singular)". The prototype **primary sources
> show the spelling is file-dependent**:
> - **`.gc/site.toml`** uses **`[[rig]]`** (singular) with `name` + `path` — harvest-verified
>   (entrypoint.sh:70–76).
> - **`city.toml`** in the prototype uses **`[[rigs]]`** (plural) with `name` + `prefix` — verbatim in
>   `city.toml.example:49–56`.
> The invariant that holds in both and is the real anti-drift rule: **a rig `path` belongs ONLY in
> `.gc/site.toml`; `city.toml` rig blocks carry `prefix`/partition/role and never `path`.**
> Whether `city.toml` uses `[[rig]]` or `[[rigs]]` is **`needs-pinned-gc-run (G11)`** — see
> OQ-C42-4 (updated in §9). `[[rigs]] path =` is unambiguously a PackV2 error (F1).

**city.toml partition/role blocks** — the canonical Gas City surface for partition declarations.
Fields `read_partition` and `write_partition` are v4-named (AI-CONTEXT §13.3) and are `needs-pinned-gc-run (G11)` for exact TOML grammar; the field *names* are grounded in v4 (AI-CONTEXT §13.3) and confirmed in the config-anchor table (C03:105, C42:133).

```toml
# city.toml — rig partition / role blocks
# Spelling: [[rig]] (F1 canonical) vs [[rigs]] (prototype city.toml.example) — needs-pinned-gc-run (G11)
# PATH belongs in .gc/site.toml, NOT here (F1 — PackV2 error otherwise)

# Worker / implementer rig (roles: code generation, build, test)
# OQ-C42-2 RESOLVED: "worker" (Phase-0) and "implementer" (Phase-2) are the same role — see §9
[[rig]]   # [needs G11 verification] — city.toml spelling may be [[rigs]] per prototype example
name     = "implementer"
prefix   = "r1"                  # EXPLICIT required (F10: avoid auto-derive collision)
# read_partition / write_partition grammar: needs-pinned-gc-run (G11); field names from AI-CONTEXT §13.3
read_partition  = ["code"]       # MUST NOT include "scenarios" — holdout invariant
write_partition = ["code"]

# Scenario-authoring rig (role: scenario authoring, isolated from implementer)
[[rig]]   # [needs G11 verification]
name     = "scenario_authoring"
prefix   = "r2"                  # EXPLICIT; different prefix from implementer to avoid collision
read_partition  = ["scenarios", "code"]
write_partition = ["scenarios"]

# Judge rig — reads trajectories + scenarios to score; MUST NOT share context with worker
# Partition shape: D-17 joint freeze (C42/C34/C32) in progress this run — see OQ-C42-3
[[rig]]   # [needs G11 verification]
name     = "judge"
prefix   = "gj"                  # EXPLICIT; distinct prefix
read_partition  = ["code", "scenarios", "trajectories"]  # [D-17 freeze in progress — see OQ-C42-3]
write_partition = ["judgments"]                          # [D-17 freeze in progress]
```

```toml
# .gc/site.toml — machine-local, entrypoint-written; DIFFERENT FILE from city.toml
# Path bindings only (F1 harvest-verified: entrypoint.sh:70–76)
[[rig]]
name = "implementer"
path = "/workspace/rigs/implementer/"   # actual filesystem path; written at container-start

[[rig]]
name = "scenario_authoring"
path = "/workspace/rigs/scenario_authoring/"

[[rig]]
name = "judge"
path = "/workspace/rigs/judge/"
```

### 4.3 Which mechanism is authoritative (G28) — sweep-1 note, not a composition primitive

> **Scope note (capability-for-principle bar).** This subsection answers the G28 gap with a *one-line
> authority statement*; it is deliberately **not** a formal partition-composition stack (C42 DELTA-01
> "partition model + composition order" was dropped — the KEEP is the 3-role taxonomy + holdout invariant
> only). The table below is an *explanatory* sweep-1 illustration of how the v4-named mechanisms relate;
> it is not a binding composition contract downstream components freeze against.

v4 names four mechanisms for the one holdout boundary: **(a)** separate git repo for scenarios
(README:171/425), **(b)** filesystem permissions / read-only-from-implementer (README:171/425), **(c)**
Gas City rig `read_partition` config (AI-CONTEXT §13.3), **(d)** OPA policy "for finer control **later**"
(README:425). Authority note (sweep-1; see G28 AMBIGUITY in §6):

| Layer | Mechanism | Role today | v4 source |
|---|---|---|---|
| 1 (primary, present) | Gas City rig `read_partition` excludes `scenarios` | the **authoritative policy declaration** — the partition is the unit of authorization | AI-CONTEXT §13.3 |
| 2 (substrate, present) | filesystem permissions (read-only-from-implementer) + separate git repo | the **physical backstop** that realizes the partition on disk | README:171/425 |
| 3 (deferred) | OPA policy | **finer-grained control, later** — not Phase-2 baseline | README:425 ("for finer control later") |
| enforce + audit | Holdout integrity & isolation **enforcement** (C34) | **enforces** the read-isolation policy and **audits** reads vs scenario paths (inventory C34); the broad-tool-access read-escape it cannot itself shut is detect-after-the-fact until C43 (G31) | README:173; G21; inventory C34 |

Authority note (one line, G28): the **rig `read_partition` is the authoritative declarative policy** (it
is the named *partition* primitive and the inventory's framing), realized on disk by filesystem perms +
repo separation, with OPA explicitly deferred. C42 owns the *declaration* (the labels + invariant);
**enforcement + audit of the holdout read-isolation is C34's** (inventory: "isolation enforcement + …
audit"), and the broad-tool-access blast-radius bound is C43's (G31). This is the smallest faithful
resolution of G28 — a one-line authority statement, not a composition stack (see §6).

### 4.4 Persistence & consistency

C42 holds **no instance state of its own**. Rig/partition policy is sourced from `city.toml` `[[rig]]`
blocks under git review (AI-CONTEXT §13.3); worktrees are C04/Gas-City filesystem state; scenario bytes are
C30. C42's only consistency requirement is the **holdout invariant** (§3): every config in which a
worker/implementer rig can read `scenarios` is invalid and must be rejected at config-load (faithful:
whether Gas City *rejects* such a config or merely *permits* it is the G21/OQ-C42-1 enforcement question —
§6).

### 4.5 Partition label registry (Sweep-2)

The v4-named partition labels (AI-CONTEXT §13.3). The label space is open (new partitions may be added),
but these are the two mandatory labels the holdout invariant is fixed on:

| Label | Meaning | Owner | Worker may read? | Judge may read? |
|---|---|---|---|---|
| `code` | source code, build artifacts, test results | implementer rig writes; all may read | Yes | Yes |
| `scenarios` | held-out evaluation scenario files (C30) | scenario_authoring rig writes | **NO** (holdout invariant) | Yes (D-17 default) |
| `trajectories` | agent session traces / CXDB turns (C21/C23) | Gas City session manager writes | Yes (own) | Yes (for scoring) |
| `judgments` | judge scores, ScoreRecords (C32/C33) | judge rig writes | No | Yes (own) |

> [FAITHFUL-FILL] — `trajectories` and `judgments` are inferred partition labels for the judge read surface (D-17
> joint freeze in progress). v4 names `code` and `scenarios` verbatim (AI-CONTEXT §13.3); `trajectories`
> and `judgments` are the minimal faithful extensions for a judge that must score without sharing a context
> window with the worker. The D-17 joint C42/C34/C32 freeze will either confirm or replace these labels.
> Until that freeze completes (C34/C32 must land), mark `[D-17 freeze in progress]`.

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

### 5.1 Partitioned read attempt — sequence diagram (Sweep-2)

The diagram shows the partitioned read path for a **worker** attempting to access the bead store, scoped
by the bead prefix mechanism (F10). C42 PROVIDES the partition contract at config-load; the worker's
runtime reads are scoped by Gas City's prefix routing; C34 audits after the fact; whether Gas City
PREVENTS out-of-prefix access is the D-30/D-23 open gate.

```mermaid
sequenceDiagram
    participant W as Worker (implementer rig, prefix r1-)
    participant GC as Gas City / bd (bead store)
    participant C34 as C34 holdout-integrity audit
    participant C43 as C43 isolation fence (D-30 gate — not yet enforced)

    Note over W,C43: Config-load phase (C42 provides the policy)
    W->>GC: city.toml [[rig]] name=implementer prefix=r1 read_partition=[code]
    GC-->>W: PartitionRecord validated (E-C42-01 if scenarios in read_partition)

    Note over W,GC: Worker reads bead store (runtime — prefix scoping)
    W->>GC: bd get r1-<bead-id>  (in-partition read)
    GC-->>W: bead data (prefix matches rig scope)

    Note over W,GC: Attempted out-of-partition read
    W->>GC: bd get r2-<bead-id>  (out-of-partition)
    alt Gas City PREVENTS (prevent-vs-detect-OPEN — D-23 spike)
        GC-->>W: BLOCKED (E-C42-04 partition-violation-detected; C43 fence active)
    else Gas City permits (detect-only path until D-23 spike + C43)
        GC-->>W: bead data returned (partition violation NOT blocked)
        GC->>C34: event: out-of-partition read observed (prefix r2 from rig r1)
        C34-->>C34: audit log: violation detected after the fact (G21 residual)
    end

    Note over C43: D-30: prevent required for unattended (P2/P3b)
    Note over C43: D-23 spike decides: watcher needed or native prevent sufficient
```

> **D-30 prevent-gate note:** The "Gas City PREVENTS" branch is the D-30 required end-state for P2/P3b.
> Until the D-23 spike (Test A) confirms whether `gc`/`bd` natively block out-of-prefix reads, this
> branch is UNVERIFIED. If the spike shows only detect, an enforcement watcher WILL be added (D-30 — sanctioned
> design deferred). Unattended operation is human-in-the-loop until prevention is established.

## 6. Failure modes & handling

| F-mode / gap | Relevance | Handling in C42 (faithful) |
|---|---|---|
| **F28** Holdout leakage (F-MODE §1 marks "Addressed") | The core mode C42's invariant targets: the implementer reading the scenarios it is judged on. | **Addressed-on-paper / detect-after-the-fact only** until OQ-C42-1 resolves and C43 lands — *lead with the caveat*: F-MODE-COVERAGE marks F28 "Addressed", but C42's contribution is the holdout invariant (§3) `scenarios ∉ read_partition(worker)`, realized by filesystem perms + repo separation (§4.3) and **enforced/audited by C34**. *Caveat (G21):* firm only if the worker subprocess cannot read outside its partition. The implementer runs as a Claude Code subprocess with broad Bash/Read tool access; nothing in faithful v4 *prevents* an out-of-partition read at tool-call time until C43 isolation lands (G31). So the realized boundary is **config + filesystem + discipline** with detect-after-the-fact audit (C34), not tool-call-time prevention. Per D-1 there is no model-family fallback, so this caveat is load-bearing — downstream (C57 register, C34) must lift the caveat with the status, not the bare "Addressed". |
| **F17** Parallel agents on shared dirs lose data (F-MODE §3, "Addressed") | Concurrent runs clobbering each other. | **Addressed** by worktree-per-run isolation (§3 contract 3); Gas City native (F17). C42 owns the policy "one isolated writable worktree per run, scoped to the rig's partitions"; the worktree substrate is C04/Gas City. |
| **G21** Holdout-integrity enforcement has no real mechanism (major) | Read-isolation is filesystem perms + rig config + "agent-prompt discipline"; the audit is detection, not prevention. | See the AMBIGUITY block below. Faithful resolution: C42 **declares** the partition policy and the holdout invariant and names the **primary mechanism** (rig `read_partition` + filesystem perms); enforcement + audit of the holdout read-isolation is **C34's** charter (inventory). C42 faithfully records that, against a broad-tool-access worker, the realized boundary is config + discipline with the read-escape detect-after-the-fact until C43's lethal-trifecta isolation lands. *(**RESOLVED by D-13** — review RC42-01/02: holdout-integrity **enforcement + audit is C34's** charter; the distinct lethal-trifecta blast-radius bound is **C43's** (G31); **C42 provides** the partition C34 enforces and does not enforce. Pre-constrains unbuilt C34 (Batch 3) + C43 (Batch 4).)* Routed to C34 + C43 + review-log as residual risk. |
| **G28** Three/four mechanisms, no authority statement (major) | Separate repo / filesystem perms / rig `read_partition` / OPA-later named for one boundary with no composition rule. | **Resolved (faithful)** by the §4.3 *one-line authority note* (not a formal composition stack — DELTA-01 dropped): rig `read_partition` is the authoritative declarative unit, filesystem perms + repo realize it on disk, OPA explicitly deferred ("for finer control later", README:425); enforcement+audit is C34's. See the §6 AMBIGUITY block for both readings. |
| **G10** "held-out" implies a guarantee the mechanism doesn't provide (minor) | The term "held-out" overstates a discipline-based boundary. | **Acknowledged**: C42 states the boundary is config + filesystem + (until C43) discipline, enforced + audited by C34 detect-after-the-fact — so "held-out" is a *policy intent verified after the fact*, not a hard guarantee, until G31/C43 closes the broad-tool-access read-escape. Surfaced as residual risk, not silently absorbed. |
| **G31** Lethal-trifecta boundary unbuilt/last (blocker, C43) | The broad-tool-access agent has no twin isolation Phase 0→3b; the read-escape broad tool access opens is unbounded. | **Deferred to C43 (faithful — not C42's to build)**: C43 owns the lethal-trifecta blast-radius bound (a *distinct* boundary from C34's holdout enforcement — see §1/§2). C42 *declares* the partitions; against a broad-tool-access worker the realized read-escape is detect-after-the-fact / discipline-backed until C43 lands (recorded here + §7 + §9). This is the XC-8 "detection-only at Phase 0" finding applied to the broad-tool-access read-escape. *(**RESOLVED by D-13** — RC42-01: the C34-enforcement-vs-C43-blast-radius split is settled — C34 owns holdout enforcement + audit, C43 owns the distinct lethal-trifecta blast-radius bound, C42 provides the partition.)* |

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
> Canonical-track faithfulness is binding: v4 says "discipline + audit logging" and "OPA … later" in plain words
> (README:177/425), so C42 **cannot make the boundary a hard enforced control** — enforcing the holdout
> read-isolation is **C34's** charter and bounding the residual broad-tool-access escape is **C43's** (D-13),
> neither a C42 canonical-track decision. The smallest faithful choice is to
> (1) declare the partition policy + holdout invariant (which v4 does mandate — `scenarios ∉
> read_partition(worker)`), (2) name the authoritative mechanism (§4.3 — rig `read_partition` + filesystem
> perms), (3) publish the partition policy to **C34**, which owns holdout-integrity **enforcement + audit**
> (**D-13**), and (4) record the residual broad-tool-access read-escape (§7, §9) that **C43**'s
> lethal-trifecta blast-radius bound closes (G31) — a *distinct* boundary from C34's holdout enforcement
> (**D-13**). C42 **provides** the partition; it does not enforce. Per D-13 the prevention/enforcement of
> the holdout read-isolation is C34's charter (not C43's); C43 only bounds the residual blast radius once a
> worker has broad tool access. On the canonical track this ownership split is settled by D-13; the
> remaining "does Gas City actively reject vs. permit-with-review" sub-question is OQ-C42-1.

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

### 6.1 Error taxonomy (Sweep-2)

Component-scoped E-codes for partition-level failures. The enforcement-strength of E-C42-04 (whether it
results in a hard block or an audit event) is the D-23 spike question; the code is defined regardless.

| E-code | Condition | Surfaced-as | Caller recovery |
|---|---|---|---|
| **E-C42-01** | `partition-violation-misconfig` — worker/implementer rig declares `scenarios` in `read_partition` in city.toml | Config-load error: `validate_partition_config` returns `ConfigError` at startup; `gc start` refuses to run | Fix city.toml: remove `scenarios` from the worker rig's `read_partition`; re-run `gc start` |
| **E-C42-02** | `prefix-collision` — two rigs in city.toml have the same `bead_prefix` value (auto-derived or explicit) | Config-load error: startup refusal with duplicate-prefix diagnostic (F10 — e.g. `rig1`/`rig2` both derive `"ri"`) | Add explicit `prefix = "<unique>"` to each rig's city.toml block; restart |
| **E-C42-03** | `role-unmapped` — a running agent references a `rig_name` not present in the validated `[PartitionRecord]` set | Runtime error: `assign_worktree` returns `ConfigError`; the session cannot start | Declare the missing `[[rig]]` block in city.toml and restart; or remap the agent to a declared rig |
| **E-C42-04** | `partition-violation-detected` — a runtime bead/filesystem access crosses a partition boundary (out-of-prefix bead access or out-of-partition file read) | **If prevent active (D-30 / D-23 spike): hard block** at tool-call boundary (E-C42-04 `BLOCKED`). **If detect-only** (current Phase-0 state): C34 audit event emitted; access may succeed (prevent-vs-detect-OPEN) | Investigate agent prompt + partition config; if repeated → escalate to human review; prevent mode: agent sees access denied error |

> **D-30 note on E-C42-04.** Per D-30 (verbatim from review-log):
>
> > "unattended operation (P2) and self-modification (P3b) require the substrate to BLOCK (prevent at the
> > tool-call/process boundary) — not merely detect — out-of-boundary access on the relevant blast-radius
> > face."
>
> E-C42-04 MUST be a hard block before P2/P3b is permitted. Whether Gas City natively provides this block
> (making E-C42-04 a tool-call-level rejection) or requires an enforcement watcher is the D-23 spike Test A
> outcome. Until that outcome is known, E-C42-04's "surfaced-as" row has two branches (above). Do NOT treat
> the detect-only branch as the permanent end-state.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security (the central concern).** C42 is the **authorization-declaration** layer of the security model
  and, per **D-1**, the load-bearing mechanism for holdout integrity now that model-family diversity is
  deferred (FE-1). The holdout invariant (`scenarios ∉ read_partition(worker)`) is declared and realized by
  rig config + filesystem perms; **enforcement + audit of that invariant is C34's** (inventory: "Holdout
  integrity & isolation enforcement"). Against a broad-tool-access worker the realized boundary is
  detect-after-the-fact / discipline-backed until C43's lethal-trifecta isolation closes the read-escape
  (G21, G31, XC-8). C42 guarantees the *policy is declared and auditable*; it does **not** itself prevent an
  out-of-partition read at tool-call time. This residual risk is the load-bearing caveat on F28's
  "Addressed" and is surfaced to C34, C43, and review-log (§9). *(**RESOLVED by D-13** — RC42-01/02: the C34-enforcement
  vs C43-blast-radius ownership split is settled — C34 owns holdout enforcement + audit, C43 owns the distinct lethal-trifecta blast-radius bound, C42 provides the partition.)*
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
  (AI-CONTEXT §13.3). *Spelling caveat (XC-9 resolved by D-23/F1 for `.gc/site.toml`; city.toml spelling
  needs-pinned-gc-run G11):* C42 uses the per-rig `[[rig]]` block form from §13.3 as F1's canonical
  recommendation, but the prototype's `city.toml.example` uses `[[rigs]]` — see §4.2 spelling note and
  OQ-C42-4. Enabling OPA later is an additive pack at the deferred layer-3 seam (§4.3) — additive, not a
  migration.

## 8. Acceptance criteria & test strategy

1. **Holdout invariant declared & rejected on violation (F28)**: a `city.toml` in which the
   worker/implementer rig's `read_partition` includes `scenarios` is an **invalid configuration**; the
   scenario_authoring rig may read/write `scenarios`; the implementer rig reads/writes only `code`
   (AI-CONTEXT §13.3). *(Whether Gas City actively rejects or merely permits-with-review is OQ-C42-1 / G21
   — the test asserts the *policy*; enforcement+audit is C34's, the broad-tool-access read-escape is C43's,
   and the exact split is **RESOLVED by D-13** — C42 provides the partition C34 enforces.)*
2. **Role closure**: every running agent resolves to exactly one rig in the closed role set
   {worker/implementer, scenario-author, judge}; an agent with no rig or an out-of-set role is invalid.
3. **Partition confinement**: a rig's declared `read_partition`/`write_partition` is the only surface it is
   *policy-authorized* to read/write; cross-partition access is denied by policy (and, once C43 lands,
   enforced — G31).
4. **Worktree disjointness (F17)**: two concurrent runs are assigned disjoint writable worktrees; neither
   can clobber the other's working files.
5. **Holdout-policy feed present (C34 seam)**: C42 publishes, per rig, its role + partition labels + r/w
   policy, and **C34 (holdout integrity & isolation enforcement)** can enforce and compare actual agent
   reads against the declared `scenarios` partition (README:173). The policy feed exists; the residual
   broad-tool-access read-escape is gated on C43 (the test records this, per G21/G31).
6. **G28 authority note is explicit (one line, not a composition stack)**: the v4-named mechanisms are
   documented with the rig `read_partition` named the authoritative declarative unit, filesystem perms +
   repo as on-disk realization, OPA deferred, and enforcement+audit identified as C34's — so downstream
   components (C30, C34, C43) know what is authoritative today vs what is deferred. (Per the
   capability-for-principle bar this is a *note*, not a frozen partition-composition contract — DELTA-01
   dropped.)
7. **Residual-risk caveat is discoverable (G21/G31)**: downstream consumers of the holdout guarantee (C34,
   C30, the F-mode owner C57) can discover that, against a broad-tool-access worker, the boundary is config
   + filesystem + discipline with detect-after-the-fact audit until C43 lands, so they do not over-trust
   "held-out".
8. **Prefix uniqueness enforced at config-load (F10)**: the config-load validator rejects any city.toml
   with two rigs having the same `bead_prefix`, whether explicit or auto-derived (E-C42-02). *(The same
   G11-gated question as E-C42-01: whether Gas City itself rejects this or the validator is a C42-supplied
   pack tool.)*

### 8.1 Concrete acceptance tests (Sweep-2)

Each is an executable check. `assert reject(...)` = validation refuses startup; `assert pass(...)` = valid
config accepted. E-codes cross-referenced per SWEEP2-DISPATCH rubric.

**Config-load validation — partition invariant (E-C42-01)**
- **AC-C42-01** — Given a `city.toml` with the implementer rig's `read_partition = ["code", "scenarios"]`,
  `validate_partition_config` returns E-C42-01 and `gc start` refuses to proceed. (Asserts the holdout
  invariant and E-C42-01.)
- **AC-C42-02** — Given a valid city.toml with the implementer rig's `read_partition = ["code"]` and
  scenario_authoring rig's `read_partition = ["scenarios", "code"]`, `validate_partition_config` returns a
  `[PartitionRecord]` with all three roles present. (Positive case — holdout invariant holds.)

**Prefix uniqueness (E-C42-02)**
- **AC-C42-03** — Given a city.toml where two rigs share the same explicit `prefix = "r1"`, startup is
  rejected with E-C42-02. (F10 collision; asserts E-C42-02.)
- **AC-C42-04** — Given rig names `rig1` and `rig2` with NO explicit `prefix`, startup is rejected with
  E-C42-02 (auto-derived `"ri"` collision, F10). *(Marked G11-gated: passes natively iff Gas City detects
  prefix collisions at config-load; else this is a C42 validator-pack check.)*

**Role-unmapped (E-C42-03)**
- **AC-C42-05** — Given an agent session referencing `rig_name = "unknown_rig"` not in the validated
  `[PartitionRecord]`, `assign_worktree` returns E-C42-03 and the session cannot start.

**Partition-violation detection (E-C42-04, D-23 gate)**
- **AC-C42-06** — Given a worker (prefix `r1-`) attempting to read a bead with prefix `r2-` (belonging to
  the scenario_authoring rig): **(a)** if prevent is active (D-23 spike confirms native block or watcher in
  place): the access is BLOCKED and E-C42-04 is surfaced as an access-denied error; **(b)** if detect-only
  (current Phase-0): C34 receives an audit event for the out-of-partition read; the test records which
  branch occurred. *(D-23 Test A gates the (a) branch. Asserts E-C42-04.)*
- **AC-C42-07** — An implementer-rig worker cannot access scenario files in the scenario partition via
  filesystem path traversal (`../scenario_authoring/…`); either the OS sandbox (C43) or filesystem
  permissions block the access. *(G21/G31 — this is the lethal-trifecta test; blocked until C43 lands.
  Recorded here as a forward test vector for C43's acceptance suite.)*

**Worktree isolation (F17)**
- **AC-C42-08** — Two concurrent implementer-rig sessions are assigned disjoint writable worktree paths;
  writing to session-1's worktree does not appear in session-2's worktree. (Asserts the worktree
  disjointness invariant; §3 contract 3.)

**Partition-policy feed (C34 seam)**
- **AC-C42-09** — `get_partition_policy()` returns one `PartitionRecord` per configured rig, each carrying
  the `rig_name`, `role_kind`, `read_partition`, `write_partition`, and `bead_prefix`; C34 can consume this
  set to enforce the holdout invariant without reading city.toml directly.

## 9. Open questions

- **OQ-C42-1** — **RESOLVED (Sweep-2, partial): D-13 settles ownership; substrate fact remains open (D-23 spike).**
  RESOLVED (Sweep-2): the *ownership* half of this OQ is closed by D-13 — C34 owns holdout-integrity
  enforcement + audit; C43 owns the lethal-trifecta blast-radius; C42 provides the partition. The verbatim
  D-13 ruling:

  > "C34 owns holdout-integrity ENFORCEMENT + after-the-fact AUDIT (read-isolation policy, independence
  > checks under D-1, `scenarios ∉ read_partition(worker)`). C43 owns the distinct lethal-trifecta
  > blast-radius bound (Bash/net/fs typing, twin isolation; G31). C42 PROVIDES the role partition C34
  > enforces; C42 does not enforce."

  Residual (still open): does Gas City *prevent* at tool-call time (the D-23 spike Test A question; G11/G21)?
  This is the substrate fact the empirical spike must answer. Conformance check: Test A1 (bead-layer:
  `bd get r2-… from rig1 cwd`) + Test A2 (OS/Bash: `cat ../rig2/…` from implementer session). Until the
  spike runs, E-C42-04 has two branches and AC-C42-06 has two outcomes. **D-30 is adopted:** prevent is
  required for P2/P3b regardless of the spike outcome.

- **OQ-C42-2** — **RESOLVED (Sweep-2): `worker` and `implementer` are the same role.**
  v4 Phase-0 uses `worker` (AI-CONTEXT §13.1); Phase-2 uses `implementer` (AI-CONTEXT §13.3). The faithful
  resolution: they are **the same role** — the Phase-0 `worker` rig evolves into the `implementer` rig
  name once the scenario-partition is established (v4 never runs both simultaneously; §13.1 is the
  Phase-0 single-rig config, §13.3 is the Phase-2 multi-role config). In the `role_kind` enum (§4.1)
  `worker` and `implementer` map to `role_kind = worker`; the partition-record `rig_name` field takes the
  verbatim name from city.toml (either `"worker"` in Phase-0 configs or `"implementer"` in Phase-2 configs).
  C42 does **not** require both names to coexist. The holdout invariant applies to whichever name is used.

- **OQ-C42-3** — **SCOPED BY D-17; joint freeze in progress this run.**
  The judge rig's exact `read_partition` / `write_partition` shape is the **unified OQ-C42-3 + OQ-C34-3 +
  C32-OQ5** question, to be frozen jointly by C42 (provides partition) + C34 (enforces+audits) + C32
  (judge) at Sweep-2. The D-17 verbatim ruling:

  > "D-17 — Judge read-surface: Sweep-1 default + joint C42/C34/C32 Sweep-2 freeze. Sweep-1 default:
  > the judge (C32) MAY read the worker's trajectories + the held-out scenarios (to score); the worker
  > MUST NOT read the judge rig or the scenarios (holdout). The exact judge-partition SHAPE (separate rig
  > vs shared scenario partition; precise read-surface) is settled jointly by C42 (provides partition)
  > + C34 (enforces+audits) + C32 (judge) at Sweep-2 — unifies OQ-C42-3 + OQ-C34-3 + C32-OQ5."

  C42's PROVIDING side is specced in §4.2 and §4.5 with the D-17 default applied. The freeze COMPLETES when
  C34 and C32 land their Sweep-2 specs and confirm or revise the judge partition labels (`trajectories`,
  `judgments` in §4.5 are marked `[D-17 freeze in progress]`).

- **OQ-C42-4** — **RESOLVED (D-23 harvest F1) + NUANCED by config anchor.**
  RESOLVED by D-23 harvest: `.gc/site.toml` uses `[[rig]]` (singular) with `name` + `path` —
  harvest-verified (entrypoint.sh:70–76). This closes XC-9 for the `.gc/site.toml` spelling.
  NUANCE: the config anchor (gascity-config-anchor §3) establishes that `city.toml` spelling is
  **`needs-pinned-gc-run (G11)`** — F1's "canonical `[[rig]]`" and the prototype's `city.toml.example`
  `[[rigs]]` disagree. The invariant that resolves both: **`path` belongs ONLY in `.gc/site.toml`**
  (a `[[rigs]] path=` in city.toml is a PackV2 error regardless of spelling). City.toml block spelling
  (`[[rig]]` vs `[[rigs]]`) must be confirmed against a pinned `gc` run (G11). C42 exemplars in §4.2 use
  `[[rig]]` (F1 canonical recommendation) and annotate `[needs G11 verification]`.

---

**[D-30 ADOPTED 2026-06-01 — prevent/block required for unattended]**

C42 provides the partition this decision enforces *prevention* over: the blast-radius face this gate refers to is the rig/partition boundary C42 defines.

> The operator has adopted the auto-001 rubric and re-adopted D-20 as **conditional on prevention**: unattended operation (P2) and self-modification (P3b) require the substrate to **BLOCK (prevent at the tool-call/process boundary)** — not merely detect — out-of-boundary access on the relevant blast-radius face. **Discharge:** if Gas City does not prevent natively (per the [D-23 spike](../_meta/D-23-gas-city-spike-protocol.md)), an **enforcement watcher that blocks WILL be added** (sanctioned in principle); its **design is DEFERRED until the spike confirms the substrate does not already prevent** — do not design what we may not need, and the watcher's design must still pass the bar when built. Until prevention is established (native or watcher), unattended operation is **blocked** (human-in-the-loop). The per-rig-class "structurally-safe parts may run unattended" optimization remains available but secondary. See the [auto-001 decision brief](../_meta/decisions/auto-001-detect-only-binding-gate.md) and review-log D-30.

The D-30 verbatim requirement, cited from review-log:

> "unattended operation (P2) and self-modification (P3b) require the substrate to BLOCK (prevent at the
> tool-call/process boundary) — not merely detect — out-of-boundary access on the relevant blast-radius
> face."

---

**[D-23 substrate-verified — gascity-prototype@b14c278, 2026-05-25]**

**F1 — `[[rig]]` path bindings and canonical spelling (RESOLVES OQ-C42-4 / XC-9):**
Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
the canonical spelling is `[[rig]]` (singular). `[[rigs]] path =` is a PackV2 validation error;
path bindings for a rig's working directory live in `.gc/site.toml` as `[[rig]]` entries, written
at container-start time by the entrypoint (which knows the runtime filesystem paths). `city.toml`
carries `[[rig]]` blocks for partition/role semantics only, without a `path` field. This resolves
XC-9 in favour of `[[rig]]` and makes the spelling in C01/C03/C42 canonical.

**F10 — Bead scope enforced by bead prefix; explicit `prefix=` required to avoid collision (NEW-INFO operational caveat):**
Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
**Bead scope is implemented as bead prefix.** Prefixes `gp-` (city HQ), `r1-` (rig1), `r2-`
(rig2) are the real scoping mechanism — agents scoped to rig1 see/write only `r1-` prefixed
beads. **Operational constraint:** rig names `rig1` and `rig2` both auto-derive prefix `"ri"` and
collide at startup; explicit `prefix = "r1"` and `prefix = "r2"` in `city.toml` are required.
Naming rigs to avoid short-prefix collisions is a production authoring concern, not a framework
safeguard.

**OPEN — prevent-vs-detect (C34:OQ-C34-1 / C43:OQ-C43-1 / D-23 spike):** The prototype proved
that prefix is the MECHANISM for scoping. It did NOT verify whether `gc` PREVENTS an
out-of-prefix bead access at the tool-call level or merely scopes-by-convention with
detect-after-the-fact. The end-to-end smoke test (which would test this path) was deferred.
This boundary remains the D-23 spike target and must NOT be treated as resolved by this harvest.
