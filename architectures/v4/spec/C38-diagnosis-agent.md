# C38 — Diagnosis Agent (Healer)  (Spec, canonical track)

> Source: README §"Principle 11 — Self-healing loop" (L248 "Observability → anomaly → diagnosis → fix →
> ship, without human intervention."; the P11 component table — **"Diagnosis agent | LLM-driven
> root-cause analysis | Custom Claude Code agent with CXDB query tools; transfusion source: Tracker's
> `Diagnose`/`Audit`/`Doctor` programmatic APIs | License of Tracker: verify (likely MIT) | Specialized
> Gas City agent pack"**, README:256; "**Fix-task generation | Diagnosis → bead | Custom: diagnosis agent
> writes bead of type `fix_task`**", README:257; L261 "the diagnosis agent is the focused work …
> **Mammoth/Tracker's diagnosis APIs are the strongest LLM-pipeline-runner transfusion target for this
> layer**"); README §Phase 3b "Healer in pieces" (L459–466: L462 "**Diagnosis agent (transfusion from
> Tracker's `Diagnose`/`Audit`/`Doctor` shape + Anthropic's investigation patterns visible in Claude Code
> itself)**"; L466 "save the diagnosis agent for after the substrate is proven"); AI-CONTEXT §6.4 Mammoth
> (L276 "Layer 4 **DIAGNOSIS** — Tracker's `Diagnose` / `DiagnoseMostRecent` / `Audit` / `Doctor`
> programmatic APIs **returning JSON-serializable failure reports** — strongest Layer 4 source in survey";
> L278 "**Tracker's Diagnose/Audit/Doctor shape for the Healer agent**"); AI-CONTEXT §7 layer map (L331
> "**Diagnosis agent | None — strongest exemplar is Tracker's Diagnose API | TBD verify | DIY with strong
> gene-transfusion source**"); AI-CONTEXT §11 transfusion sources (L407 "**Diagnosis agent**: Tracker's
> `Diagnose`/`Audit`/`Doctor` (strongest LLM-pipeline transfusion target), **Anthropic's Claude Code
> investigation patterns**, Sentry Performance Insights, Honeycomb BubbleUp"); AI-CONTEXT §14 risk (L625
> "Tracker license is non-permissive | … | Verify before adoption; **if restrictive, transfuse pattern
> without adopting code**"); F-MODE-COVERAGE §1/§8 (F22 "Zombie agents — … **Tracker-style diagnosis**";
> **F23** "Stalled-vs-thinking ambiguity — **Tracker `Diagnose`/`Audit`/`Doctor` APIs as gene transfusion
> source for Healer**" — Addressed; F4 "Code-quality teardown — Healer agent recognizes degradation
> patterns" — Partial); component-inventory C38 row (subsystem Self-Healing Loop; kind agent-role;
> "LLM root-cause analysis over clustered failures (Tracker Diagnose/Audit/Doctor transfusion)";
> maps **A57/B24**; **depends on C37, C21**; gaps **G30, G07**; foundational: no; Batch 4);
> review-log **D-1** (the diagnosis LLM = **Claude Code, same provider** as the coder), **D-6** (canonical
> track), **XC-3** (the heal-loop **numeric** termination/escalation policy is **C39**'s, not C38's);
> the C40 spec (`spec/C40-durable-orders.md` §1/§6 — "no Healer agent shipped"; the anomaly→diagnosis→fix
> *content* is C36/C37/C38/C39, C40 is only the durable carrier), and the C37/C39 inventory contracts
> (C37 supplies the failure **clusters**; C39 consumes the **diagnosis** to mint the `fix_task` bead +
> owns loop-closure). **Gene-transfusion correctness predicate + license framework are C51's** (G07/G30
> framework); C38 addresses only its local part.
> Inventory ID: C38   Kind: agent-role   Status: sweep-1
> Track: canonical (faithful posture — elaborate v4 exactly; mark inferred fills `[FAITHFUL-FILL]`,
> v4 ambiguities `[AMBIGUITY: Gxx]`).

## 1. Purpose & responsibility

C38 is the factory's **diagnosis agent** — the **"Healer's" reasoning step**: given a **cluster of similar
failures** (from C37) and the **trajectory context** behind them (from CXDB, C21), it runs **LLM-driven
root-cause analysis** and emits a structured **diagnosis** — "*why* did this class of trajectories fail,
and what is the proposed remedy?" — that the fix-task loop (C39) turns into actionable work. It is v4's
mechanism for the **diagnosis** node in **Principle 11 — self-healing loop**: "Observability → anomaly →
**diagnosis** → fix → ship" (README:248). It is the *focused custom work* of P11 ("the diagnosis agent is
the focused work", README:261) — the one node in the loop the existing stack does not supply turnkey
("Diagnosis agent | **None** — strongest exemplar is Tracker's Diagnose API | DIY with strong
gene-transfusion source", AI-CONTEXT:331).

The agent is built **on the existing stack, not from scratch**. The *investigator* is **Claude Code
itself** — the same provider/family as the coder (review-log **D-1**), driven by C28's multi-turn
reasoning + tool-dispatch loop with read access to CXDB query tools ("Custom **Claude Code agent** with
CXDB query tools", README:256). C38's own genuine deliverable is the thin glue the stack does not provide:
**(a) the diagnosis prompt/agent role** — what to investigate, over which cluster, with which read tools,
under which output contract — and **(b) the `Diagnosis` record + the diagnosis→C39 handoff**. The
investigation *capability* is Claude Code's; the **diagnostic discipline and report shape** are
**gene-transfused from Tracker's `Diagnose`/`Audit`/`Doctor` programmatic APIs** — "JSON-serializable
failure reports … the **strongest Layer-4 source in survey**" (AI-CONTEXT:276) — plus "Anthropic's Claude
Code investigation patterns visible in Claude Code itself" (README:462).

**Responsibilities (what C38 is the spec-of-record for):**
- **Root-cause analysis over one failure cluster.** Take a cluster of similar failures (C37) + its
  representative/exemplar trajectories and produce a **root-cause diagnosis**: the probable cause of the
  failure class, the evidence (CXDB turns/spans) supporting it, and a proposed remedy direction. This is
  "**LLM-driven root-cause analysis**" verbatim (README:256, inventory C38).
- **Driving Claude Code as the `diagnosis`/healer role.** C38 runs the investigation as a **Claude Code
  agent loop** (C28) with a **diagnosis-role prompt** and **read-only CXDB query tools** (C21), scoped to
  the cluster under investigation. At Phase 0 the investigator is **Claude Code, same provider as the
  coder** (D-1) — a distinct *role* (healer), not a distinct provider.
- **The diagnosis prompt = the Tracker `Diagnose`/`Audit`/`Doctor` discipline, transfused.** C38 owns the
  prompt/role that makes the LLM behave like Tracker's diagnostic APIs: produce a **JSON-serializable
  failure report** (cause, evidence, confidence, suggested action) rather than free prose. The *shape* and
  *discipline* are transfused; the *engine* is Claude Code. `> [FAITHFUL-FILL]` — v4 names the transfusion
  *source* and the *report-is-JSON-serializable* property (AI-CONTEXT:276) but does not enumerate
  `Diagnose`-vs-`Audit`-vs-`Doctor` field-by-field; the minimal consistent reading is **one `Diagnosis`
  record per cluster carrying {root-cause, evidence refs, confidence, proposed remedy}**, modeled on the
  Tracker report shape. Concrete schema is sweep-2 (and pinned against the verified Tracker API, G30).
- **Emitting a typed, attributed `Diagnosis` for C39.** Write the diagnosis as a structured record
  (per-cluster, carrying the cause/evidence/confidence/remedy + the cluster id it explains), attributed
  (C41 `created_by` = the healer role) onto a bead / CXDB turn, so **C39** can mint the `fix_task` bead and
  carry it into the build flow. C38 produces the **diagnosis**; "**diagnosis agent writes bead of type
  `fix_task`**" (README:257) is the *next* node — see boundary below. The diagnosis→C39 handoff is the seam
  C38 owns.

**Explicitly NOT (boundaries):**
- **NOT fix-task generation / loop-closure / termination (C39) — the load-bearing downstream boundary.**
  Turning a diagnosis into a `fix_task` bead, re-entering the build flow, proving the fix worked via the
  bead chain, and — critically — the **numeric termination/escalation policy** (how many fix attempts
  before escalation, oscillation detection when a fix *creates* a new anomaly, who authorizes a fix to ship
  at L5) are **C39's** (inventory C39; G18/G35; review-log **XC-3** routes the numeric heal-loop policy to
  C39, not the diagnosis step). C38 *emits a diagnosis*; it does **not** write `fix_task`, does **not**
  decide attempt budgets, does **not** authorize shipping. `> [AMBIGUITY: G07-adjacent]` — README:257 says
  "**diagnosis agent writes bead of type `fix_task`**", which reads as C38 writing the bead; but the
  inventory splits C38 (diagnosis) from **C39** (fix-task generation & loop-closure, which *depends on
  C38*). Minimal consistent reading with the inventory + C39's deps: **C38 emits the `Diagnosis`; C39 mints
  the `fix_task` from it.** The README "writes" is the loop *as a whole*; the inventory's C38/C39 split is
  authoritative for the seam. (See §9 OQ1.)
- **NOT clustering / embedding / anomaly detection (C37, C36).** *Embedding trajectories and grouping
  similar failures* is **C37** (sentence-transformers + HDBSCAN); *numeric anomaly detection* is **C36**
  (PyOD). C38 *consumes* a finished cluster; it neither embeds nor clusters nor detects the anomaly.
  (Inventory: C38 depends on C37.)
- **NOT the agent-loop / investigation engine / CXDB query tooling (C28, C21).** The multi-turn reasoning,
  tool dispatch, and the provider abstraction are **C28** ("the implementer worker; hooks/skills/subagents/
  MCP surface"); the CXDB turn-DAG + its HTTP/binary query APIs are **C21**. **Per the bar, C38 builds none
  of these** — Anthropic's "Claude Code investigation patterns visible in Claude Code itself" (README:462)
  are *the stack*, not C38's code. C38 *configures* a diagnosis role over them. (Capability-for-principle:
  the investigation loop is what the stack already does → DROP.)
- **NOT the gene-transfusion correctness predicate or license framework (C51).** *Whether a transfusion is
  "correct/complete"* (G07) and *the license-hygiene framework for transfused exemplars* (G30 framework)
  are **C51's** (inventory C51 "needs a correctness/completeness predicate + license handling"; the brief
  binds the predicate/license framework to C51). C38 records *what it transfused from* (`transfused_from =
  Tracker Diagnose/Audit/Doctor`) and flags the **C38-local** license question (is Tracker permissive
  enough to port code, or pattern-only?), but routes the *framework* to C51. (See §6 gap handling.)
- **NOT the durable carrier (C40).** *Surviving crashes / event-triggered re-launch* of the heal workflow
  is **C40** (Gas City Orders). An Order may *drive* a diagnosis run, but the durability/retry of the
  workflow is C40's; C38 is the diagnosis *content* ("no Healer agent shipped … the anomaly→diagnosis→fix
  *content* is C36/C37/C38/C39", C40 spec §1).
- **NOT Healer governance / authorization (deferred).** "Healer governance | OPA" (AI-CONTEXT:335) — who is
  allowed to *act* on a diagnosis, and the L5 ship authorization — is **not** C38's; it sits with C39's
  loop-closure (ship authorization) and the autonomy ladder (C56). C38 only *diagnoses*; it never deploys.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Depends on | **C37** Trajectory clustering | Supplies the **failure cluster** C38 diagnoses: a group of similar failing trajectories (HDBSCAN over sentence-transformer embeddings) + their representative/exemplar members. C38 reads a cluster; it does not form it. |
| Depends on / reads | **C21** CXDB trajectory store | The **trajectory context** behind a cluster — the recorded turn-DAGs C38's investigation queries for evidence (read-only "CXDB query tools", README:256). Read-only. |
| Runs on | **C28** Claude Code agent loop | The **investigator**: multi-turn reasoning + tool dispatch + provider abstraction. C38 runs as a diagnosis-role agent loop here (D-1: same provider as the coder). C38 supplies the prompt/role + read tools; C28 supplies the loop. |
| Constrained by | **C29** Model floor & stylesheet | Supplies the diagnosis-role model identity (`resolveModel(diagnosis/healer node)`). Phase-0 default = Claude Code (D-1). `> [FAITHFUL-FILL]` — inventory names only C37/C21 as deps, but a Claude-Code agent role needs a model identity; C29 is the model-routing owner (minimal, consistent with C28/C32). |
| Consumed by | **C39** Fix-task generation & loop-closure | Reads C38's **`Diagnosis`** record and mints the `fix_task` bead, re-enters the build flow, and owns the termination/escalation contract (G18/G35; XC-3). The diagnosis→C39 handoff is the seam C38 owns the *emitting* half of. |
| May be driven by | **C40** Durable workflow (Orders) | An event-triggered Order (crash/anomaly/cluster-formed) may *launch* a diagnosis run durably (C40's inferred P11 consumer is C39; the diagnosis step sits in the same chain). C40 = durable carrier; C38 = content. (Downstream wiring; not a build dep of C38.) |
| Attribution | **C41** Identity / actor model | Every `Diagnosis` is attributed (`created_by` = the healer rig/role). No unattributed diagnosis. |
| Records transfusion | **C51** Gene-transfusion discipline | C38 stamps `transfused_from = Tracker Diagnose/Audit/Doctor` (+ Claude Code investigation patterns) on the build; C51 owns the *correctness predicate* (G07) + *license framework* (G30) that judges/records the transfusion. |
| Realized over | **C17/C02** Tool-node / pack ABI | The diagnosis agent ships as a **"Specialized Gas City agent pack"** (README:256) — prompt + role + tool wiring, no Go fork. |

## 3. Interfaces / contracts (sweep-1: named + described)

**Inbound:**
1. **Cluster-to-diagnose contract (from C37).** A reference to a **failure cluster**: its id, its member
   trajectories (or representative exemplars), and whatever cluster-level features C37 attaches (size,
   centroid/exemplar, the shared-failure signal). C38 reads this as the *unit of diagnosis* — one
   `Diagnosis` per cluster. *Precondition:* the cluster is resolvable and its member trajectory refs
   dereference to CXDB. Concrete cluster schema is C37's (sweep-2 seam).
2. **Trajectory-read contract (from C21).** Read-only access to the cluster's trajectory turn-DAGs (CXDB
   query tools) so the investigation can gather evidence (which turn/tool/span the failure originates in).
   Read-only; the diagnosis agent never mutates trajectories.
3. **Diagnosis-model contract (from C29/C28).** The diagnosis-role model identity (`resolveModel`,
   Phase-0 Claude Code, D-1) and the C28 agent-loop the role runs in. C38 *honors* the routed identity; it
   does not pick the model.

**Outbound:**
4. **`diagnoseCluster(clusterRef) → Diagnosis` (primary entry).** The agent's core operation: given a
   failure cluster, run the Claude Code diagnosis-role investigation over its trajectories (CXDB evidence)
   and produce a structured root-cause **`Diagnosis`**. *Postcondition:* exactly one attributed `Diagnosis`
   is emitted + persisted (bead/CXDB turn) for the cluster, consumable by C39. Concrete signature/schema is
   sweep-2.
5. **`Diagnosis` emission (to C39).** A structured per-cluster record — modeled on the **Tracker
   `Diagnose`/`Audit`/`Doctor` JSON failure-report shape** (AI-CONTEXT:276) — carrying: the **cluster id**
   it explains, the **root cause** (the failure-class hypothesis), **evidence references** (CXDB turn/span
   ids the cause rests on), a **confidence** signal, and a **proposed remedy direction**. This is the seam
   C39 reads to mint a `fix_task`. `> [FAITHFUL-FILL]` schema — v4 fixes only "JSON-serializable failure
   report" + the transfusion source; the fields above are the minimal set C39 needs to act and a human can
   review (README:466 "after the substrate is proven"); concrete schema sweep-2, pinned to the verified
   Tracker API (G30).

**Invariants:**
- **I1 (evidence-bound, no free-floating cause).** Every `Diagnosis` cites **evidence references** into
  CXDB (turns/spans) supporting its root cause — the Tracker discipline of a *JSON failure report*, not a
  prose opinion (AI-CONTEXT:276). A diagnosis with no evidence ref is invalid. This is what lets a human
  reviewer (README:466) and the loop-closure (C39) check the diagnosis against the actual trajectories.
- **I2 (diagnose-don't-fix).** C38 emits a **diagnosis + proposed remedy**; it never writes the `fix_task`
  bead, never re-enters the build flow, and never authorizes a ship. The action boundary is C39's
  (XC-3/G18/G35). A `Diagnosis` is a *recommendation*, not a mutation.
- **I3 (read-only over trajectories).** The investigation has **read-only** access to CXDB + the cluster
  (query tools, not write tools); it cannot mutate the trajectories it diagnoses. (Prevents the diagnosis
  step from contaminating the evidence it reasons over.)
- **I4 (attributed, no silent diagnosis).** Every `Diagnosis` is attributed (C41 `created_by` = healer
  role) and recorded — there is no unlogged diagnosis. This is what makes the heal loop auditable and
  feeds loop-closure (C39) and the goal-drift audit (F54/RSI residual, G35 — owned downstream).
- **I5 (one diagnosis per cluster).** `diagnoseCluster` is deterministic in its *bookkeeping* (one
  `Diagnosis` per cluster-run); the *root-cause reasoning itself* is probabilistic (an LLM) — which is
  exactly why it carries a **confidence** and **evidence refs** a downstream gate/human can check, rather
  than being treated as ground truth.
- **I6 (transfusion recorded, pattern-vs-code routed to C51).** The build records `transfused_from =
  Tracker Diagnose/Audit/Doctor`; whether the transfusion is *code-port* or *pattern-reimplementation*
  depends on the Tracker license verdict (G30), and the *correctness* of the transfusion is judged by
  C51's predicate (G07). C38 stamps the provenance; C51 owns the framework.

## 4. Data model / state

C38 owns **little durable state** — it is an *agent-role/investigator*, not a store. Clusters live in C37,
trajectories in C21, the `fix_task` + loop-closure chain in C39/C20.

| Datum | Shape (sweep-1) | Owner | Notes |
|---|---|---|---|
| `Diagnosis` (per cluster) | `{cluster_id, root_cause, evidence_refs[] (CXDB turn/span), confidence, proposed_remedy, transfused_from}` | C38 (emits) → persisted on bead/CXDB | The record C39 consumes to mint a `fix_task`. `> [FAITHFUL-FILL]` — minimal field set, modeled on the Tracker JSON failure-report shape; sweep-2 fixes schema vs the verified Tracker API. |
| Diagnosis-agent pack | Claude Code diagnosis-role **prompt + role + read-tool wiring**, shipped as a "Specialized Gas City agent pack" (README:256) | C02/C17 + C38 | Declarative; the investigation engine (C28) + CXDB tools (C21) are adopted, not authored. **This prompt/role is C38's primary deliverable.** |
| Cluster + trajectory context (transient) | the cluster + its CXDB turn-DAGs, loaded read-only for one run | C37 / C21 | Held only for the duration of a diagnosis run. |
| Diagnosis-model identity (transient) | from C29 per run (Phase-0 Claude Code, D-1) | C29 | Recorded into the `Diagnosis`/attribution; not owned. |

C38 is **restart-safe**: a diagnosis run is re-runnable (idempotent at the bookkeeping level, I5) because
its inputs (cluster, trajectories) are durable elsewhere; a lost in-flight diagnosis is simply re-run
(durability/re-launch of the run is C40's, not C38's).

## 5. Behavior

**Diagnosing one cluster (the core flow):**
1. A failure **cluster** becomes diagnoseable (C37 finishes clustering; an Order/event may trigger the run,
   C40). The cluster is the **unit** of diagnosis (one `Diagnosis` per cluster).
2. C38 obtains the **diagnosis-role model** (C29, Phase-0 Claude Code, D-1) and runs a **Claude Code agent
   loop** (C28) with the **diagnosis prompt** (the transfused Tracker `Diagnose`/`Audit`/`Doctor`
   discipline) and **read-only CXDB query tools** (C21), scoped to the cluster's trajectories.
3. The agent investigates: reads the cluster's representative trajectories, queries CXDB for the failing
   turns/spans, and forms a **root-cause hypothesis** with **supporting evidence refs** (I1).
4. C38 emits a structured **`Diagnosis`** (root cause + evidence refs + confidence + proposed remedy +
   `transfused_from`), attributed (C41), to a bead / CXDB turn → consumed by **C39** to mint a `fix_task`
   and carry it into the build flow.

**Degraded behavior:** if the diagnosis model is unavailable (C29 cannot resolve / auth fails) the cluster
is left *undiagnosed* and surfaced as a bead/gate event (visible to the operator / the rest of the heal
loop) — C38 never silently substitutes a fabricated diagnosis (I4). If the investigation cannot reach a
confident root cause, it emits a **low-confidence `Diagnosis`** (or an explicit "**inconclusive**" verdict
with whatever partial evidence it gathered) rather than inventing a cause — the confidence signal (I5) is
what lets C39 / a human decide whether to act, escalate, or gather more data. If trajectory evidence is
unresolvable (CXDB miss), the diagnosis fails closed (no fabricated cause) and reports the missing evidence.

Sequence/state diagrams, the concrete diagnosis prompt, and the evidence-gathering algorithm are
**sweep-2/3**; this sweep fixes the named flow + invariants + the transfusion source.

## 6. Failure modes & handling

| F-mode | Source | C38's role | Status per v4 |
|---|---|---|---|
| **F23** Stalled-vs-thinking ambiguity | FM:45 | The **Tracker `Diagnose`/`Audit`/`Doctor` discipline** transfused into the diagnosis prompt — the named v4 mechanism for telling a stalled agent from a thinking one via root-cause analysis over the trajectory | Addressed (C38 *is* the F23 mechanism) |
| **F22** Zombie agents | FM:44 | After C36 anomaly-detects a non-live session, **Tracker-style diagnosis** (C38) explains *why* (the root-cause step); detection is C36, diagnosis is C38 | Addressed (diagnosis half is C38) |
| **F4** Code-quality teardown | FM:42 | C38 performs the **root-cause analysis** when C36/C37 flag a degradation cluster ("Healer agent recognizes degradation patterns") — but quality-metric *definition* is the hard part v4 marks Partial | Partial (per v4 — metric definition is the residual, not the diagnosis step) |
| **F54** Goal subversion (RSI drift over cycles) | FM:93 | Every `Diagnosis` is **attributed + evidence-bound + recorded** (I1/I4) into CXDB content-addressed history — the audit substrate the F54 guard relies on; C38 does not *resolve* F54 (weakest acknowledged mechanism, G35) but its records feed the audit | Partial (significant residual; audit discipline owned downstream — G35) |

**Gap handling (G30 + G07) — C38-local part addressed; framework routed to C51:**

> [AMBIGUITY: G30 — diagnosis-agent ↔ Tracker transfusion seam; **framework owned by C51**] **Tracker's
> license is unverified** (README:292,335; AI-CONTEXT:440,508,625) and Tracker is wrapped by Mammoth. If
> Tracker is **non-permissive**, the *strongest Layer-4 exemplar* is unusable for **code** transfusion —
> only **pattern** transfusion (reimplement the `Diagnose`/`Audit`/`Doctor` *shape* from the documented
> behavior, port no code). Reading (a): *port Tracker's code* (fastest, but blocked if non-permissive).
> Reading (b): *reimplement the pattern* (always legal; the JSON-failure-report shape is described, not
> copyrightable as an idea). **C38-local resolution (the canonical track):** treat the transfusion as
> **pattern-by-default** — the diagnosis prompt reproduces the *discipline* (produce a structured,
> evidence-bound, JSON-serializable failure report with cause/confidence/remedy), which is **legal
> regardless of Tracker's license**, and only upgrades to code-port **iff** the license is verified
> permissive (AI-CONTEXT:625 "if restrictive, transfuse pattern without adopting code"). The *framework*
> that decides the verdict and records license hygiene — the **transfusion license-handling framework — is
> C51's** (inventory C51; G30 framework). C38 records `transfused_from = Tracker Diagnose/Audit/Doctor`
> and the pattern-vs-code flag; it does **not** own the license-clearance machinery. (See §9 OQ2.)

> [AMBIGUITY: G07 — diagnosis correctness; **predicate owned by C51**] **There is no acceptance criterion
> for when a transfusion (here, of the Tracker diagnosis discipline) is "correct/complete"** (G07). v4
> gives the *adversarial-scenario* shape for the Healer's own evaluation: "**feed it failure trajectories
> that the team has manually clustered, ensure its clusters match**" (README:499) — i.e., the diagnosis
> agent is validated by **its own held-out scenarios** (the evaluation tier, C30–C33), scoring whether its
> diagnoses match a human's on known failure classes. **C38-local resolution:** C38's correctness is
> *measured*, not asserted — its acceptance is "**diagnoses match the human root-cause on a held-out
> failure-cluster scenario set**" (AC2/AC4; README:499), exactly the factory's own evaluation mechanism
> turned on the Healer. But the **general transfusion-correctness predicate** (the contract for "behaves
> like the exemplar") is **C51's** (inventory C51 "needs a correctness/completeness predicate"; the brief
> binds the predicate to C51). C38 supplies the *diagnosis-specific* acceptance (match-the-human scenarios)
> and routes the *general predicate* to C51. (See §9 OQ3.)

**Other detection/recovery:** diagnosis-model-unavailable / inconclusive / CXDB-evidence-miss are surfaced
as bead/gate events (visible to the operator + the rest of the C36–C39 loop), never as silent or fabricated
diagnoses (I4). **No fix is ever applied by C38** — the *act* on a diagnosis (and its termination/
oscillation/ship-authorization safety, the F52 "more controller patches" trap, G18) is **C39's** (XC-3).

## 7. Cross-cutting

- **Security / isolation.** The diagnosis agent has **read-only** access to CXDB + clusters (I3) — it
  cannot mutate the trajectories it reasons over, and it cannot write `fix_task` beads or ship (I2). Its
  Claude Code auth is the same Max-OAuth path as C28 (no separate credential at Phase 0, D-1; a
  second-provider diagnosis model would be FE-1-adjacent + G37 secrets, deferred). The healer runs as a
  distinct **role** (not a distinct provider), kept off the write path of the system it diagnoses.
- **Cost (G32).** v4's only anchor is "$200/month Max" (AI-CONTEXT §4.1); there is **no cost model** for
  running an LLM root-cause investigation per failure cluster. At Phase 0 the diagnosis investigation
  consumes the **same single Max seat** as the coder/judge, so diagnosis volume competes with build + judge
  volume for the shared seat ceiling (cf. C28 G13/G34) — flagged. Cost-per-satisfaction is **C46's**;
  deferred here (G32, noted not resolved — §9). v4 deliberately sequences C38 *last* in P11 ("save the
  diagnosis agent for after the substrate is proven", README:466), partly bounding when this cost lands.
- **Scale.** Same single-seat throughput ceiling as the rest of the agent loop; the diagnosis step runs
  **per cluster** (not per trajectory), which is the natural rate-limiter C37's clustering provides —
  diagnosing *one cluster of many failures* is far cheaper than diagnosing each failure. (This is the
  point of putting clustering, C37, *before* diagnosis.)
- **Observability.** Every `Diagnosis` is attributed (C41) and recorded (bead/CXDB) — the diagnosis agent's
  own trajectory is itself captured by the C25→C27 telemetry tier (it is a Claude Code loop). This is what
  makes loop-closure (C39) and the goal-drift audit (F54/G35) computable.
- **Ops.** The agent ships off-the-shelf engine (Claude Code, C28) + transfused discipline as a **"Specialized
  Gas City agent pack"** (README:256) — prompt + role + read-tool wiring, no Go fork; the Tracker discipline
  is transfused pattern-first (G30), upgraded to code-port only on a verified-permissive license.

## 8. Acceptance criteria & test strategy (sweep-1, high level)

- **AC1 (diagnoses a cluster → a structured `Diagnosis`).** Given a failure cluster (C37) and its CXDB
  trajectory context (C21), `diagnoseCluster` runs the Claude Code diagnosis role and emits exactly one
  attributed `Diagnosis` carrying root-cause + **evidence refs** + confidence + proposed remedy (README:256;
  AI-CONTEXT:276; inventory C38). *Test:* one cluster → one persisted, attributed, evidence-bound `Diagnosis`
  consumable by C39.
- **AC2 (diagnoses match the human on held-out failure clusters — the G07 acceptance).** On the **adversarial
  Healer scenario set** — "feed it failure trajectories that the team has manually clustered, ensure its
  clusters match" (README:499) — C38's root-cause diagnoses **match the human-assigned root cause** for known
  failure classes (scored by the evaluation tier, C30–C33). *Test:* a labelled failure-cluster scenario set
  → C38's diagnoses agree with the human labels above a bar (bar/threshold owned by the evaluation tier /
  C53, not C38). *(This is how G07 "is the diagnosis correct?" is operationalized for C38; the general
  transfusion predicate is C51's.)*
- **AC3 (evidence-bound, not free prose — Tracker discipline).** Every `Diagnosis` cites CXDB evidence refs
  for its root cause (I1) — a diagnosis with no evidence ref fails validation. *Test:* a `Diagnosis` with an
  empty evidence set is rejected by the contract.
- **AC4 (inconclusive is a first-class verdict).** When the investigation cannot reach a confident root
  cause, C38 emits a **low-confidence / inconclusive** `Diagnosis` (with partial evidence), never a
  fabricated cause (degraded behavior, I5). *Test:* a cluster with insufficient signal → an explicit
  inconclusive/low-confidence verdict, not an invented cause.
- **AC5 (diagnose-don't-fix).** C38 emits a `Diagnosis` + proposed remedy but **never** writes a `fix_task`
  bead, re-enters the build flow, or authorizes a ship (I2; XC-3 → C39). *Test:* a diagnosis run produces a
  `Diagnosis` and **no** `fix_task` / deploy side-effect; the `fix_task` is minted only when C39 consumes it.
- **AC6 (read-only over trajectories).** The diagnosis investigation cannot mutate CXDB / the cluster (I3).
  *Test:* the diagnosis role has only read tools; a write attempt is unavailable/denied.
- **AC7 (transfusion recorded; pattern-by-default).** The build stamps `transfused_from = Tracker
  Diagnose/Audit/Doctor` and the **pattern-vs-code** flag; absent a verified-permissive Tracker license the
  diagnosis discipline is **reimplemented pattern**, not ported code (G30; AI-CONTEXT:625). *Test:* provenance
  is recorded; with license unverified, no Tracker code is vendored. *(The license verdict + correctness
  predicate are exercised in C51's suite, not C38's.)*
- **AC8 (no silent diagnosis on failure).** Diagnosis-model-unavailable / CXDB-evidence-miss leaves the
  cluster undiagnosed + surfaced as a bead/gate event; no fabricated `Diagnosis` is ever emitted (I4).
  *Test:* induce diagnosis-model auth failure → no `Diagnosis`, a gate event instead.

Concrete `Diagnosis` schema (pinned to the verified Tracker API), the diagnosis prompt, the evidence-gathering
flow, and the Healer scenario fixtures are **sweep-2**.

## 9. Open questions (→ review-log)

- **OQ1 (C38↔C39 seam — who writes `fix_task`?, top).** README:257 reads as "**diagnosis agent writes bead
  of type `fix_task`**", but the inventory splits **C38 (diagnosis)** from **C39 (fix-task generation &
  loop-closure, depends on C38)**. Sweep-1 takes the **inventory split** as authoritative: **C38 emits the
  `Diagnosis`; C39 mints the `fix_task`** from it (the README "writes" is the loop as a whole). Confirm the
  exact handoff contract (does C39 *poll* C38's `Diagnosis` beads, or does C38 *hand* the `Diagnosis` to a
  C39 entry?) at sweep-2 (overlaps C39, whose spec is not yet on disk). *This is the load-bearing downstream
  seam.*
- **OQ2 (G30 — Tracker license verdict, framework C51).** The Tracker license is **unverified** (likely MIT
  by 2389 convention, but "verify before adoption", README:292). Until verified, C38 transfuses the
  diagnosis discipline **pattern-only** (legal regardless). The *verdict* + the license-hygiene framework are
  **C51's** (G30 framework). Open: confirm Tracker's actual license so C38 can decide pattern-vs-code at
  sweep-2; route the framework to C51.
- **OQ3 (G07 — diagnosis-correctness predicate, framework C51).** C38's *local* acceptance is "diagnoses
  match the human on a held-out failure-cluster scenario set" (AC2; README:499) — but the **bar/threshold**
  ("how close a match is correct?") and the **general transfusion-correctness predicate** ("behaves like the
  exemplar") are **C51's** (predicate) + the evaluation tier's (threshold, C53). Confirm the C38 Healer
  scenario set + its pass bar with C51/C53 at sweep-2.
- **OQ4 (`Diagnosis` schema seam).** v4 fixes only "JSON-serializable failure report" + the Tracker
  transfusion source (AI-CONTEXT:276). The concrete `Diagnosis` schema is the contract **C39** binds to (to
  mint a `fix_task`) and a **human** reviews (README:466) — freeze it early (sweep-2), pinned against the
  verified Tracker `Diagnose`/`Audit`/`Doctor` field shape. `[FAITHFUL-FILL]` here; needs a canonical schema
  ruling.
- **OQ5 (cost/throughput, shared with C28 G13/G34, G32).** No token-budget/cost model exists for an LLM
  root-cause investigation per cluster on the **single Phase-0 Max seat** the diagnosis agent shares with the
  coder + judge. Per-cluster (not per-trajectory) is the natural rate-limiter, but v4 gives no numbers; needs
  quantification (→ C46) before throughput claims hold.
