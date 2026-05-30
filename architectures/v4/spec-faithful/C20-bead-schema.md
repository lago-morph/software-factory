# C20 — Bead schema registry  (Spec, Track A)

> Source: AI-CONTEXT §3.2 ("nine concepts" #2 — "Bead Store: Durable typed **work-graph** (Dolt or file)"); AI-CONTEXT §16 cold-start procedure (lines 694–699: "Find its bead with `gc bd find --type factory_build_in_progress` … `transfused_from` attribution … `gc converge resume <bead_id>`"); README Part 4 P8 ("Gas City beads with type `override`"), P9 ("beads … native `created_by`"), P10 ("Persistent task graph — Tasks with **dependencies**"), P11 ("diagnosis agent writes bead of type `fix_task`", "Loop closure tracking — Custom bead chain: anomaly → diagnosis → fix → resolution … Bead schema"); README Phase 3b ("Fix-task bead schema"); component-inventory C20 row (maps `A90, A91, A92, A58b, B37-schema`; depends on C19; gaps G17, G18; foundational: yes); ambiguities-and-gaps G17 (blocker — "no schema for any of the core stores", names `override`/`fix_task`/`factory_build_in_progress`/`factory_build`), G18 (blocker — self-healing loop has no termination / loop-closure contract).
> Inventory ID: C20   Kind: data-store   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C20 is the **canonical schema registry for every bead type** in the factory. A *bead* is one node in
the durable typed work-graph (C19); C20 defines **what the type tag means**, **what fields each type
carries**, and **how typed beads chain to each other** so that the cold-start, override, self-healing,
and bootstrap-resume flows that v4 references by *bead type name* actually resolve to a defined record
shape. Where C19 owns the **graph** (nodes, edges, durability, the `gc bd` store), C20 owns the
**vocabulary of node types** that flow through it.

This component exists because v4 instructs agents to query bead **types that are never defined**:
AI-CONTEXT §16 tells a cold agent to run `gc bd find --type factory_build_in_progress`, README P8/P11
reference `override`, `fix_task`, `factory_build`, and Phase 3b lists "Fix-task bead schema" as a
deliverable — but no schema is given anywhere (gap G17, blocker). C20 is the place those type
definitions live.

**Responsibilities**
- Define the **bead-type registry**: the closed (Phase-relative) set of `type` values v4 names, plus the
  per-type field set. Faithful v4 types: `override`, `fix_task`, `factory_build`,
  `factory_build_in_progress` (G17 §49; README P8/P11; AI-CONTEXT §16).
- Define the **common bead envelope** every type shares — the fields v4 asserts are present on *all*
  beads: `id`, `type`, `created_by` (P9: "every bead … native `created_by`"), and dependency edges
  (P10: "Tasks with dependencies").
- Define the **typed bead-chain shapes** v4 references by name: the override-discipline chain (P8) and
  the self-heal closure chain `anomaly → diagnosis → fix → resolution` (P11 "Loop closure tracking").
- Carry the **loop-closure / termination contract** fields that the self-heal chain needs to be
  *bounded* — attempt counters, terminal states, escalation markers — because G18 (blocker) flags that
  the chain as described has no stated bound. (See §4 + the G18 AMBIGUITY block.)
- Provide the **resume contract**: the fields C52/self-bootstrap and `gc converge resume` read to pick up
  an in-progress build (`factory_build_in_progress`, `transfused_from`, spec/scenario pointers;
  AI-CONTEXT §16 lines 695–698).

**Explicitly NOT**
- NOT the bead **store** (C19). C19 owns persistence, the file/Dolt backend, the graph edges, and the
  `gc bd` query surface. C20 owns *type definitions and field schemas* that ride inside C19's nodes.
- NOT the CXDB type registry (C22). C22 is the `{bundle_id, type, version}` system for **trajectory
  turns** in CXDB (AI-CONTEXT §5.3). C20 is the **bead** type system in Gas City. They are different
  stores with different type systems; C20 ≠ C22 (the inventory lists both as distinct foundational rows).
- NOT the loop **logic** (C35 override loop, C39 fix-task loop-closure). C20 defines the *bead shapes and
  the termination fields* those loops read/write; the control-loop behavior (when to escalate, how to
  detect oscillation) is C39/C35. C20 supplies the schema slots; the loops supply the policy.
- NOT identity/attribution (C41). C41 owns *who can act* and the `created_by` provenance semantics; C20
  merely declares `created_by` as a required envelope field (faithful to P9).
- NOT a new bead **type system** of v4's invention. Track-A faithfulness limits C20 to the types v4
  actually names; it does not add speculative types (those would be Track-B deltas).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C19** Bead store / work-graph | C20 types are stored as C19 nodes; C20 has no persistence of its own. Inventory: C20 `depends on C19`. |
| Upstream (concept) | **C01** Gas City substrate | Beads + `created_by` + the `gc bd` CLI are Gas City native (AI-CONTEXT §3.2 #2; README P9). |
| Downstream (consumes) | **C35** Override→pattern→rule loop | Reads/writes `override` beads (README P8: "Gas City beads with type `override`"). Inventory: C35 `depends on C20`. |
| Downstream (consumes) | **C39** Fix-task generation & loop-closure | Writes `fix_task` beads; reads the anomaly→diagnosis→fix→resolution chain + closure fields (README P11; Phase 3b "Fix-task bead schema"). Inventory: C39 `depends on C20`. |
| Downstream (consumes) | **C51** Gene-transfusion discipline | Reads/writes `transfused_from` on `factory_build*` beads (AI-CONTEXT §16 step 2). Inventory: C51 `depends on C20`. |
| Downstream (consumes) | **C52** Self-bootstrap recursion | Resumes via `factory_build_in_progress` beads (AI-CONTEXT §16 lines 695–699). |
| Sibling (not dependency) | **C41** Identity/attribution | Supplies the meaning of `created_by`; C20 declares the field, C41 owns provenance. |

C20 is **foundational** (inventory: yes), in **Batch 1**, authored in parallel with C19 — it is the
load-bearing schema the override loop, the self-heal loop, and bootstrap-resume all reference by type
name. Per the inventory's critical-path note #2, G17/G18 make C20 a **blocker** for those downstream
tiers until its types are defined.

## 3. Interfaces / contracts

Sweep 1 — interfaces named and described (concrete field signatures / JSON schemas deferred to sweep 2).

1. **Bead-type registry** — the enumerated set of `type` values v4 recognizes, each with a field
   schema. The contract every downstream component queries when it does `gc bd find --type <T>`.
2. **Common envelope contract** — the fields *every* bead carries regardless of type (`id`, `type`,
   `created_by`, dependency edges, status). Downstream code may rely on these on any bead.
3. **Per-type field contract** — for each named type, the additional fields it carries (e.g. `override`
   carries a "why" field; `fix_task` carries the diagnosis pointer; `factory_build_in_progress` carries
   `transfused_from` + spec/scenario pointers).
4. **Chain-shape contract** — the directed type-to-type edges that form the v4-named chains: the override
   chain (P8) and the closure chain `anomaly → diagnosis → fix → resolution` (P11). Defines which type
   may depend-on / resolve which.
5. **Termination/closure contract** — the fields on the self-heal chain that make it *bounded*: an
   attempt count, a terminal-state enum (`resolved` / `escalated` / `abandoned`), and an escalation
   marker. (Faithful elaboration forced by G18 — see §4.)

**Invariants**
- **Every bead has a type** drawn from the registry; an untyped or unknown-typed bead is invalid
  (otherwise `gc bd find --type <T>` cannot be well-defined, which is exactly the G17 failure).
- **Every bead carries `created_by`** (P9: "every bead and event carries `created_by`" — AI-CONTEXT §3.1
  row 9 "automatic everywhere"; README P9).
- **Chains are acyclic and typed**: a closure chain instance has at most one `resolution` terminal, and
  every `fix_task` traces back to the `diagnosis`/anomaly that produced it (faithful to "Custom bead
  chain: anomaly → diagnosis → fix → resolution", README P11).
- **Resume-completeness**: a `factory_build_in_progress` bead carries enough (`transfused_from`, spec
  pointer, scenario pointer, workflow handle) for `gc converge resume <bead_id>` to continue without
  out-of-band state (AI-CONTEXT §16 lines 695–699).

## 4. Data model / state

C20 owns the **bead-type definitions** (schema), not bead instances (those live in C19). The model has
three parts: the common envelope, the named types, and the named chains.

### 4.1 Common envelope (every bead)

| Field | Meaning | v4 source |
|---|---|---|
| `id` | bead identifier; target of `gc bd find` / `gc converge resume <bead_id>` | AI-CONTEXT §16 line 699 |
| `type` | the registry type tag queried by `gc bd find --type <T>` | AI-CONTEXT §16 line 695; G17 |
| `created_by` | actor attribution, present on every bead | README P9; AI-CONTEXT §3.1 row 9 |
| `dependencies` | edges to other beads (the "dependency-aware" work-graph) | README P10 "Tasks with dependencies"; AI-CONTEXT §3.2 #2 "work-graph" |
| `status` | lifecycle state of the bead | > [FAITHFUL-FILL] below |

> [FAITHFUL-FILL] **`status` field.** v4 never names a status field, yet it refers to a
> `factory_build_in_progress` type *and* a plain `factory_build` type (G17 §49). The minimal consistent
> reading is that "in progress" is a **lifecycle state of a build bead**, so beads carry a `status`. The
> smallest faithful choice is a single `status` field on the envelope rather than encoding lifecycle into
> the `type` string — except where v4 *itself* encodes it in the type (`factory_build` vs
> `factory_build_in_progress`), which is preserved verbatim (see the AMBIGUITY block). Concrete enum
> values deferred to sweep 2.

### 4.2 Named bead types (faithful enumeration)

| `type` | Purpose | Type-specific fields (sweep-1, described) | v4 source |
|---|---|---|---|
| `override` | durable record of an operator override + *why* | a "why"/rationale field; reference to the overridden action | README P8 ("beads with type `override`", "Override log storage") |
| `fix_task` | a diagnosis-generated unit of repair work re-entering the build flow | pointer to the diagnosis/anomaly that produced it; closure-chain fields (§4.3) | README P11 ("diagnosis agent writes bead of type `fix_task`"); Phase 3b "Fix-task bead schema" |
| `factory_build` | a factory-built-component build record | `transfused_from` (gene-transfusion attribution); spec pointer (`packs/*/spec.md`); scenario pointer (`scenarios/<component>/`) | AI-CONTEXT §16 steps 2–4; README P11 transfusion |
| `factory_build_in_progress` | a build that is mid-flight and resumable | the `factory_build` fields **plus** a workflow handle resumable by `gc converge resume <bead_id>` | AI-CONTEXT §16 lines 695–699 |

> [FAITHFUL-FILL] **Beyond these four, what other types exist?** v4 names exactly these four by string.
> The P11 closure chain ("anomaly → diagnosis → fix → resolution", README P11) implies **anomaly**,
> **diagnosis**, and **resolution** as further bead types (the "fix" node = `fix_task`). The minimal
> faithful elaboration is to register `anomaly`, `diagnosis`, and `resolution` as the chain's other
> nodes, because the chain is named explicitly and cannot be a "bead chain" unless its links are beads.
> They are marked as *chain-derived* types, distinct from the four v4 names by literal string. No other
> types are invented.

### 4.3 Named chains

**Override-discipline chain (P8).** `override` beads accumulate; periodic surfacing reads them; recurring
patterns convert to rules (README P8 "Periodic pattern surfacing", "Rule conversion"). Faithful shape:
`override` is a leaf-record type, not a multi-link chain; its only edge is `created_by` + a reference to
the overridden action.

**Self-heal closure chain (P11).** The v4-named chain:

```
anomaly  ──diagnosed_by──▶  diagnosis  ──produces──▶  fix_task  ──resolved_by──▶  resolution
```

This is the "Custom bead chain: anomaly → diagnosis → fix → resolution" that README P11 calls "Loop
closure tracking … Did the fix actually fix it?" and that Phase 3b lists as the "Fix-task bead schema"
deliverable. The `resolution` node is what proves the fix worked; its existence + a positive verdict is
loop closure.

> [AMBIGUITY: G18] **Where does the termination/escalation bound live — and does it exist at all?**
> Reading A (no bound): v4 describes the chain as a pure data lineage (anomaly→diagnosis→fix→resolution)
> and states the loop runs "without human intervention" (README P11/README:246). On this reading C20 just
> records the chain and *no* bound exists — which is exactly the F52 "more controller patches" trap the
> docs themselves warn about (F-MODE-COVERAGE §8; G18 §51).
> Reading B (bounded): G18 (blocker) and the F52 caution mean a *faithful* schema must at least carry the
> **fields a bound would be expressed in**, even though v4 states no numeric policy. The closure chain
> needs: an **attempt counter** (Nth fix for the same anomaly), a **terminal-state** enum
> (`resolved` | `escalated` | `abandoned`), and an **escalation marker** (who/what to escalate to at L5).
> **Pick: Reading B for the *schema*, Reading A for the *policy*.** Faithful to v4, C20 **adds the slots**
> (attempt count, terminal state, escalation marker) because the chain is named and the docs warn about
> unbounded patching, but C20 **does not set the threshold values** — the actual "N attempts then
> escalate" policy and oscillation detection are C39's contract (inventory: C39 owns loop-closure;
> G18/G35). This is the smallest consistent choice: it makes the loop *boundable* (so C39 has somewhere to
> write the bound) without inventing a policy number v4 never states. The numeric bound is flagged as an
> open question routed to C39 (§9).

### 4.4 Persistence & consistency

C20 stores *schema definitions*, not instances. Bead instances persist in C19 (file or Dolt;
AI-CONTEXT §3.2 #2). C20's only consistency requirement is **registry/store agreement**: every `type`
the C19 store accepts must be a type C20 defines, and the field set C19 enforces must match C20's schema
(otherwise `gc bd find --type <T>` is ill-defined — the G17 failure). Schema-version drift is a real
risk (AI-CONTEXT §3.5: "1-2 breaking pack-schema … changes per quarter"); a faithful schema-version pin
is a sweep-2 deliverable.

## 5. Behavior

C20 has no control loop of its own; its behavior is **definitional** and **validation-time**:

- **Definition-time**: the registry declares the envelope + named types + chain shapes above.
- **Write-time validation**: when a component writes a bead (C35 writes `override`, C38/C39 write
  `diagnosis`/`fix_task`/`resolution`, C52 writes `factory_build_in_progress`), the write is valid only
  if `type` is registered and the required envelope + type-specific fields are present.
- **Query-time resolution**: `gc bd find --type <T>` (AI-CONTEXT §16) resolves against the registry; an
  unregistered `<T>` is the G17 bug C20 exists to prevent.
- **Chain-progression**: the self-heal loop (C39) advances a closure-chain instance node by node and
  writes the terminal-state field; C20 only guarantees the *slots* exist and the chain stays acyclic with
  ≤1 `resolution`.

(Sequence/state diagrams for the closure-chain lifecycle and the resume flow are deferred to sweep 2 per
BUILDER-BRIEF altitude.)

## 6. Failure modes & handling

| F-mode / gap | Relevance | Handling in C20 (faithful) |
|---|---|---|
| **G17** (blocker) — no schema for bead types; cold-start queries `factory_build_in_progress`, a type the docs never define | C20 is the component that *closes* G17 by defining the types. | Resolved at sweep-1 altitude: §4 registers `override`, `fix_task`, `factory_build`, `factory_build_in_progress` (verbatim v4 names) + the chain-derived `anomaly`/`diagnosis`/`resolution`, with the common envelope. Concrete field schemas → sweep 2. |
| **G18** (blocker) — self-heal loop has no termination/loop-closure bound (F52 "more controller patches") | The closure chain `anomaly→diagnosis→fix→resolution` is a C20 schema. | **Partially addressed** (schema slots only): C20 adds attempt-count / terminal-state / escalation-marker fields so the loop is *boundable* (AMBIGUITY block §4.3). The *policy* (threshold N, oscillation detection, L5 ship authorization) is **deferred to C39** (inventory: C39 owns loop-closure; G18/G35) — setting it here would exceed C20's data-store scope. |
| **F52** "more controller patches" (oscillation; F-MODE-COVERAGE §8) | A fix that creates a new anomaly spawns a new chain unboundedly. | Faithful: C20 provides the attempt-counter + escalation slot that make oscillation *detectable*; detection logic is C39. C20 cannot itself stop oscillation (it is schema, not control). Flagged §9. |
| Unknown/missing `type` on write | A typo'd or new type would silently break `gc bd find` | Faithful posture: invalid (invariant §3). v4's registry is closed to the named set; adding a type is a schema change, not a free-form write. |
| Attribution gap (`created_by` absent) | P9 asserts it is "automatic everywhere"; G36 notes verification is optional/deferred | C20 *requires* `created_by` as an envelope field (faithful to P9) but does **not** require signed/verified provenance (G36: "optional, deferred", README:229). Verification is C41's optional pack, not C20. |

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security**: `created_by` is required but **self-asserted** — C20 faithfully records the field without
  mandating signatures (G36; README:229 "Identity verification … optional, deferred"). Signed provenance
  is C41's optional pack, surfaced as residual risk (§9).
- **Cost**: negligible; C20 is schema, not runtime. Its leverage is correctness — a defined schema is what
  lets the cold-start, override, and self-heal queries resolve at all.
- **Scale**: bounded by C19's store (file or Dolt). C20 adds no scale concern beyond keeping the registry
  small and closed.
- **Observability**: the bead type + `created_by` + chain edges *are* the audit trail (README P9 "Audit
  trail — Gas City event bus + bead history"). C20's typed chains are what make "did the fix work?"
  answerable (P11 loop-closure).
- **Ops**: schema changes ride normal git review (beads/packs are version-controlled). AI-CONTEXT §3.5's
  "1-2 breaking pack-schema changes per quarter" means C20 needs a schema-version pin (sweep 2) so the
  store and registry don't drift.

## 8. Acceptance criteria & test strategy

1. **Cold-start resolves (G17 closed)**: `gc bd find --type factory_build_in_progress` (and `override`,
   `fix_task`, `factory_build`) resolves against the registry — every type AI-CONTEXT §16 / README P8/P11
   names is defined, with no "queries a type that doesn't exist" gap.
2. **Envelope present on every type**: every registered type carries `id`, `type`, `created_by`,
   `dependencies`, `status`; a bead missing `created_by` is rejected (faithful to P9).
3. **Resume-completeness**: a `factory_build_in_progress` bead carries `transfused_from` + spec pointer +
   scenario pointer + workflow handle sufficient for `gc converge resume <bead_id>` (AI-CONTEXT §16
   695–699) with no out-of-band state.
4. **Closure chain is well-formed (G18 slots)**: a self-heal instance forms the typed chain
   `anomaly→diagnosis→fix_task→resolution`, acyclic, ≤1 `resolution`, and carries the attempt-count +
   terminal-state + escalation-marker fields — so C39 *can* express a bound (even though C20 sets none).
5. **Registry closed**: writing a bead whose `type` is not registered is rejected (no silent free-form
   types — the G17 prevention).
(Concrete JSON/TOML field schemas, the terminal-state enum, and registry-vs-store conformance test
vectors are sweep-2 deliverables.)

## 9. Open questions

- **OQ-C20-1** (→ review-log): **G18 numeric bound ownership.** C20 adds the *slots* (attempt count,
  terminal state, escalation marker) but defers the *policy* (how many fix attempts before escalation,
  oscillation/F52 detection, who authorizes a Healer fix to ship at L5) to **C39**. Confirm C39 is the
  right owner and that the slot set C20 provides is sufficient for C39's bound — else C20's schema needs
  more fields. This is the top open question.
- **OQ-C20-2** (→ review-log): **Chain-derived types (`anomaly`/`diagnosis`/`resolution`) are inferred**
  (§4.2 FAITHFUL-FILL). v4 names the *chain* but only `fix_task` by type string. Are the other three real
  bead types, or are anomaly/diagnosis/resolution stored elsewhere (e.g. CXDB turns, C21/C22) with only
  `fix_task` as a bead? Needs the actual C19/C39 read to confirm the type boundary.
- **OQ-C20-3** (→ review-log): **`status` vs type-encoded lifecycle.** v4 encodes lifecycle in the type
  string for builds (`factory_build` vs `factory_build_in_progress`) but C20's faithful elaboration also
  adds an envelope `status`. Is the dual representation intended, or should one be canonical? (AMBIGUITY
  §4.1.) Resolving this affects whether `factory_build_in_progress` is a distinct type or
  `factory_build` + `status=in_progress`.
- **OQ-C20-4** (→ review-log): **Registry/store authority (G11).** C20 assumes the C19 store enforces the
  C20 registry, but Gas City's actual bead-type enforcement is unverified (G11 — Gas City behavior is
  asserted, not run). Confirm whether Gas City beads enforce a closed type set or accept arbitrary `type`
  strings before sweep-2 schema can be authoritative.
