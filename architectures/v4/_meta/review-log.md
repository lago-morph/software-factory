# Review Log — open questions, deferrals, and cross-component issues

Central sink for open questions (OQs), deferred decisions, and adversarial findings that need an
orchestrator/human call. Per-component docs raise OQs inline; a periodic **collector** agent harvests
them here so the primary doesn't have to read every doc. Do not have many agents append concurrently —
this file is written by the primary or a single collector agent per pass.

## ✅ Resolved decisions (binding)

- **D-1 — Judge provider (resolves the cross-family critical-path blocker).** Decision (user,
  2026-05-30): **implement the judge with the SAME provider/family as the coder for now**; a
  different-provider judge moves to the **future-enhancements bucket** (`_meta/FUTURE-ENHANCEMENTS.md`).
  Impact: C29 cross-family rule becomes advisory/relaxed; C32/C34 build against same-provider judging
  with holdout-integrity provided by rig partitioning + prompt/role isolation rather than family
  diversity. Cross-family judging is a documented future enhancement, not a Phase-0 requirement.
- **D-2 (ADOPTED — both Persistence adversaries independently concur) — Bundle-id namespace.** One
  factory-owned reverse-DNS root with per-store sub-bundles: `softwarefactory.v4.beads` (bead types),
  `softwarefactory.v4.trajectory` (CXDB turn types), `softwarefactory.v4.packs` (pack ids). Drop vendor
  `strongdm.*` and the merged-single-bundle option. Apply across C02/C20/C21/C22.
- **D-3 (ADOPTED) — bead-type schema ownership (resolves RC20B-01 blocker + XC-4).** **C20 authors the
  bead-type payload schemas** (`fix_task`, `override`, `factory_build`, …); **C22 owns the registration
  *mechanism* + the CXDB-turn types only** and registers C20's bead types via a documented binding seam.
  Reject C22-B's single-registry-authors-beads claim.
- **D-4 (ADOPTED) — C19↔C20 direction (resolves XC-1).** Canonical: **C20 depends on C19** (schema layer
  over the graph store). They are co-foundational; the production write-path cycle is broken by the M1
  interface freeze + a no-op `validate` stub seam (the reversed dispatch arrow was only that call seam).
- **D-5 (ADOPTED) — C41↔C23 tamper-evidence (resolves XC-5 blocker).** **C41 owns the provenance
  hash-chain**, computed over C23-provided ordered `event_id`s. C23 provides gap-free ordered `event_id`s
  only; it does NOT provide the chain. Update both specs.

### Batch-2 review integration (2026-05-31) — D-6..D-14

- **D-6 — Nomenclature: "canonical track", not "Track A".** Post-convergence there is one track (`spec/` + `plan-faithful/`). Component specs/plans MUST NOT frame themselves as "Track A / faithful track" against a live "Track B". Relabel such references to "the canonical track" or drop the track framing. PRESERVE Track-A/B history in `_meta/` docs (SURVIVOR-PASS, META-PLAN, TRACK-CHARTERS, BUILDER/ADVERSARY briefs) — intentional. (from RC09-04)
- **D-7 — Formula node-kind taxonomy home = C12.** The node-kind set (agent/tool/gate/sub_formula) is named by C12 as the formula DAG's own vocabulary; C02 references C12's `tool` kind for the tool-node ABI but does not redefine the set. Sweep-1 FAITHFUL-FILL; authoritative list awaits real `gc` grammar (G11/Sweep-2). (from C12 deferred)
- **D-8 — Convoy → C05; Order → C40.** "Convoy" (atomic multi-bead dispatch) is a Gas City sling concept referenced by C05; "Order" (durable workflow) is owned by C40. C12 references both but defines neither; C07 carries glossary entries. (from C12 deferred)
- **D-9 — F38 (undefined-vocabulary detection) owner = C10.** Per F-MODE-COVERAGE:74 and C07's frozen spec, F38 is owned by C10's EARS linter. SURVIVOR-PASS DROP #04 dropped only the C07 machine-readable *registry*, not C10's F38 duty. C10 names F38 vocab-lint as a deterministic rule over specs (flag undefined/inconsistent terms) with NO C07 registry machinery — prose-glossary-based. (from RC10-01)
- **D-10 — `modeldb` fields = {id, family, cost_tier}.** Per the SURVIVOR-PASS apply outcome (binding). No separate `independence_class` field; judge independence is expressed by the L0–L3 policy (L1 same-family default, D-1), not a registry field. (from RC29-05)
- **D-11 — Observability seam: LangFuse ingests TRACES only.** Verified vs LangFuse OTel docs. C26 exports the trace signal to C27/LangFuse; metrics/events received by C26 are NOT asserted to appear in LangFuse (forwarded best-effort or not routed) and NEVER to CXDB (two-sink anti-edge holds). Seam transport = OTLP/HTTP + HTTP Basic auth (base64 `public:secret`); path → Sweep-2. (from RC26-01/RC27-01)
- **D-12 — Two-sink rule stays as cross-referenced per-spec notes.** Fork stated at C25 (source), Collector✗→CXDB anti-edge at C26, C24/C27 cross-referencing. No new shared subsystem doc (avoid scope creep). (from C26/C27 OQ-2)
- **D-13 — Holdout enforcement ownership.** C34 owns holdout-integrity ENFORCEMENT + after-the-fact AUDIT (read-isolation policy, independence checks under D-1, `scenarios ∉ read_partition(worker)`). C43 owns the distinct lethal-trifecta blast-radius bound (Bash/net/fs typing, twin isolation; G31). C42 PROVIDES the role partition C34 enforces; C42 does not enforce. Pre-constrains unbuilt C34 (Batch 3) + C43 (Batch 4). (from RC42-01/02)
- **D-14 — G37 (secrets) ≠ FE-3 (signing).** G37 = open secrets/credential-storage gap (owned by C03; plaintext `city.toml`/env today). FE-3 = graduated-mandatory signing, BLOCKED ON G37 but a distinct deferred enhancement. Specs deferring secrets cite **G37**, not FE-3. Signing stays deferred (Bet 2 → FE-3); resolves the old "signing mandatory vs optional" → optional/deferred (README:229), revisit at FE-3's trigger. (from RC27-03)

### Batch-3 review integration (2026-05-31) — D-15..D-17

- **D-15 — Satisfaction is HOLISTIC at Sweep-1 (FE-5 resolution).** C33 computes the satisfaction distribution by a graded judge (C32) over C08's existing free-form Definition-of-Done — NOT against enumerated per-criterion DoD. **FE-5 (enumerated per-criterion DoD inside the spec artifact) stays DEFERRED**; it is a coordinated C08+C32+C33 change whose primary beneficiary (C46 per-criterion diagnosis) is built last. Revisit at Sweep-2 / when C46 needs per-criterion granularity. (C33 builder + adversary concur.)
- **D-16 — Loop-primitive DOT encoding owned by C12; joint C12/C14/C15 Sweep-2 freeze.** The DOT encoding of a sanctioned bounded loop / back-edge marker (so C15 can distinguish a bounded loop from a raw cycle) is owned by C12 (formula grammar) and frozen jointly with C14 (translator) + C15 (linter) at Sweep-2, blocked on the real `gc` loop primitive (C12:OQ-2). Sweep-1: C14 names the back-edge marker as a seam element (interim fail-loud → end-state marked-back-edge); C15 consumes it; none invents the encoding. (C14↔C15 seam.)
- **D-17 — Judge read-surface: Sweep-1 default + joint C42/C34/C32 Sweep-2 freeze.** Sweep-1 default: the judge (C32) MAY read the worker's trajectories + the held-out scenarios (to score); the worker MUST NOT read the judge rig or the scenarios (holdout). The exact judge-partition SHAPE (separate rig vs shared scenario partition; precise read-surface) is settled jointly by C42 (provides partition) + C34 (enforces+audits) + C32 (judge) at Sweep-2 — unifies OQ-C42-3 + OQ-C34-3 + C32-OQ5. (C32 DEFERRED.)

### Batch-4 review integration (2026-05-31) — D-18..D-19 + XC-3 resolved

- **XC-3 RESOLVED — G18 numeric termination policy owned by C39.** C39 (fix-task-loop-closure) owns the numeric termination/escalation policy (N-attempts→escalate, F52 oscillation detection, L5 ship-authorization) over C20's bounded slots; **C18** owns the convergence loop + the bound-reached signal; **C20** owns the schema slots. Verified across the C16/C18/C20/C39 reviews and against C39's now-on-disk spec (§1/§3.2 contract 7/§6 "CRITICAL — XC-3"). Closes the XC-3 routing that C16/C18/C20 deferred to C39. (See the updated XC-3 entry in the Cross-component-issues section.)
- **D-18 (ADOPTED — operator confirmed 2026-05-31; see D-20) — C43 split-sequencing.** C43 (isolation-boundary) splits across phases: its **boundary-typing + blast-radius half** (depends only on C42 + the P4 deterministic-first reconciler/tool-node primitives, NOT twins) pulls forward to a **Phase-2 entry precondition**; its **twin-isolation half** (blocked on C44 twins) stays at **Phase 3c**. Rationale: the P0–P3b window scales the factory unattended (P2) and self-modifies (P3b) with only after-the-fact detection (C34) and no blast-radius bound — the XC-8/F12/F44 hazard; the boundary-typing half closes most of it without waiting on twins. Aligns with XC-8 + D-13. Security risk-tolerance call **confirmed by operator** (D-20 below): the fence is pulled forward; the detection-only-Phase-0 alternative was rejected. The faithful P3c manifest is preserved + annotated, not re-sequenced. (from C54 OQ-3 / RC54-05 + adversary split recommendation; confirmed via decisions-to-make.md item 1.)
- **D-19 — Methodology significance testing → C48.** C55 (methodology-experiment) computes per-(methodology × work-type) satisfaction distributions via the existing eval tier (C30/C32/C33) but does NOT perform statistical significance testing — routed to **C48** (Batch 5). C55 names the seam and withholds the significance claim (surfaces raw distributions + sample counts) until C48 lands; it does not reimplement stats. Mirrors C33's identical significance→C48 boundary; grounded in C48's inventory mandate ("determines whether a variant was actually better"). (from RC55-02 — was builder-asserted/adversary-softened, now logged.)

### Wrap-up operator decisions (2026-05-31) — D-20..D-25

Operator (jonathan@manton.com) reviewed [`decisions-to-make.md`](../../../decisions-to-make.md) on 2026-05-31 and **agreed with every recommendation**. Each item below is the corresponding binding ledger decision. Items map 1:1 to the six entries in that doc.

- **D-20 (ADOPTED — operator) — C43 fence split-sequencing confirmed (decisions-to-make item 1; confirms D-18).** Adopt Option A: pull the C43 **boundary-typing / blast-radius half** (the lethal-trifecta "fence") forward to a **Phase-2 entry precondition** — a gate the factory MUST pass before it runs unattended (P2) or self-modifies (P3b); the **twin-isolation half** stays at Phase 3c with C44. The "accept detection-only Phase 0" alternative (XC-8) is **rejected**. D-18 flips PROVISIONAL→ADOPTED. Affected: C43 spec/plan (the split is its own design, already authored — now binding, not provisional), C54 phase plan annotation, XC-8. Rewind: revert this entry + the C54/C43 annotation.
- **D-21 (ADOPTED — operator) — F54 objective-drift audit: register + human checkpoint now, detector before L5 (decisions-to-make item 2; resolves OQ-C57-3).** Adopt Option A: F54/objective-drift stays **registered-unbuilt** in the C57 residual register; mitigate now with a **cheap periodic human checkpoint** — "do the objectives still match intent?" — tied to each batched human-review point on the autonomy ladder (C56). A **real drift detector (Option B) is REQUIRED before L5 lights-out** and is a hard precondition on L5 promotion (C56). Affected: C57 register (record residual + the human-checkpoint mitigation + the L5 precondition), C56 (name the L5-gate dependency), C39:OQ3/C52:OQ6/C56:OQ-3 reciprocals resolved to this. NOT a Sweep-1 build.
- **D-22 (ADOPTED — operator) — Counterfactual replay: deterministic half now, LLM half experimental (decisions-to-make item 3; resolves C49:OQ-1 disposition).** Adopt Option A: the **deterministic-tool / twin slice** of a counterfactual replay is automated and reproducible (feeds C48/C50); the **LLM-step slice** ships **best-effort, variance-bounded, human-reviewed, NEVER auto-promoted on its own**. Calibration of the LLM half (Option B — N/variance-bound/judge-FP guard) is **deferred to later, as evidence accumulates**; the optimization loop is NOT gated on solving it (Option C rejected). C49's honest split-framing stands; this confirms it as the adopted posture. Affected: C49 (confirm disposition note), C48/C50 (consume only the deterministic slice automatically).
- **D-23 (ADOPTED — operator) — Prevent-vs-detect: Gas City reality check first (decisions-to-make item 4; scopes C34:OQ-C34-1 ≡ C43:OQ-C43-1, gated on G11).** Adopt Option A: **do NOT bind holdout-integrity (C34) or the fence (C43) to either "prevent" or "detect"** until a focused **Gas City reality-check spike** verifies what a real `gc` actually enforces at tool-call/config-load time. This spike is the **first move of the next pass (Sweep-2)** and the highest-leverage de-risking action (it underwrites every "Gas City does X natively" claim). Affected: C34/C43 keep both readings live with the spike named as the resolver; Sweep-2 entry checklist leads with it. Pairs with G11.
- **D-24 (ADOPTED — operator) — C46 dependency-edge wiring correction (decisions-to-make item 5; resolves OQ-6 / C46:OQ-6).** Accept the fix: C46's cost signal comes from the OTLP-metrics path (C25 emit → C26 collector) + the CXDB read seam (C21), with **C24 = writer/provenance only**. The pinned **inventory dependency edge for C46** is corrected to read **C21/C25** (in addition to C33), not "C33, C24". Affected: [`component-inventory.md`](component-inventory.md) C46 dep column (real edit, this pass). Typo-class; no behavior change.
- **D-25 (ADOPTED — operator) — Secrets deferred; flag-lib license pinned (decisions-to-make item 6; resolves G37 posture + Unleash license note).** Secrets: adopt Option A — keep config/env now, adopt a **minimal off-the-shelf secrets approach (env-injection or SOPS-encrypted files) at first real credential**; no premature secrets build. This is the **G37** posture (G37 ≠ FE-3 signing, per D-14). License: **pin a known-open (Apache-2.0) version of Unleash, or pick an unambiguously-open alternative**; resolution home = the **C57 license-hygiene register** + the Sweep-2 version-pin step (mirrors C27:OQ-3 LangFuse SPDX-drift). Affected: C03 (secrets posture note), C57 register (license census), C48/C27 (cite the pinned-open verdict). Sweep-2 application.

### Expert-panel follow-ups (2026-05-31) — PF-1..PF-3 (operator review at Sweep-2 entry)

The 5-expert panel ([verdict](panel/VERDICT.md)) returned **right-idea-but-change-X-before-building** — the v4 shape is sound; the build is gated on unverified substrate, not architecture. Three recommendations sit BEYOND the adopted decisions D-20..D-25. None blocks closing Sweep-1; all shape Sweep-2 / first implementation. NOT yet operator-decided — surfaced for review.

- **PF-1 — Broaden the D-23 spike into a full Gas City substrate-verification MILESTONE as the literal first implementation step.** D-23 scopes a prevent-vs-detect spike; the panel (5/5 flagged G11) wants every "Gas City does X natively" claim verified against a real `gc` install before any component binds to it — not just the prevent-vs-detect question. **Recommendation: make this the first implementation target** (see [HANDOFF](HANDOFF.md) / [STATUS](STATUS.md)).
- **PF-2 — Add a judge-calibration / false-positive-rate audit GATE before trusting satisfaction numbers.** Same-family LLM-judge (D-1) on the held-out stream may be a "hall of mirrors" (pragmatist + security + methodology). Relates to C32:OQ1 / FE-1. **Recommendation: gate the first reliance on satisfaction scores on a judge-FP audit** (C46 can measure it); do not auto-promote on uncalibrated satisfaction.
- **PF-3 — Define a minimum objective-drift tripwire even PRE-L5, not only at L5.** D-21 puts the real detector before L5 lights-out; the panel wants a cheap mechanical tripwire (not only the human checkpoint) active from the first self-modification (P3b), since drift can begin the moment the factory tunes itself. **Recommendation: a lightweight drift tripwire at P3b**, ahead of the full detector at L5.

### D-23 substrate harvest (2026-06-01) — Sweep-2 first action (protocol + harvest, no live run)

Per the operator's Sweep-2 decision (no live agents this run), the D-23 Gas City reality-check was executed as **(a)** a runnable spike protocol ([D-23 spike protocol](D-23-gas-city-spike-protocol.md)) and **(b)** a harvest of the substrate facts the Gas City prototype (`lago-morph/gascity-prototype@b14c278`, 2026-05-25) already proved ([D-23 substrate harvest](D-23-substrate-harvest.md), 12 facts F1–F12). Spec annotations applied this run carry the marker `[D-23 substrate-verified — gascity-prototype@b14c278, 2026-05-25]`.

- **OQs RESOLVED by the harvest:** **XC-9** + **C42:OQ-4** (canonical `[[rig]]`; path bindings in `.gc/site.toml`; F1); **C04:OQ-4** (Phase-0 Provider-kind = tmux, one interactive `claude` per pane; F7). **C28:OQ-4** partially informed (pack-import strictness; full pack contract still needs pinned-`gc` G11 verification; F3).
- **Contradiction scan — lead-verified 0 true contradictions.** The harvest flagged F2 (`convergence.max_iterations` not a real field), F4 (`gc init` interactive), F9 (dolt `--ref refs/heads/*`) as `CONTRADICTS-CLAIM`. Lead verification against the actual specs reclassified **all three to `NEW-INFO`**: C18/C39 never assert a `convergence.*` field (they defer numeric policy to C20 slots + G11), and no v4 spec references `gc init` or dolt refs at all. v4's deferral discipline held. Applied as operational caveats, not corrections. (Morning-review headline.)
- **Prevent-vs-detect remains OPEN.** The prototype proved bead-**prefix** is the scoping *mechanism* (F10) but **never tested enforcement strength** (smoke test deferred). **C34:OQ-C34-1 ≡ C43:OQ-C43-1 stay live**; the D-23 spike (Test A) is the resolver. No annotation closes this.

### Sweep-2 data-cluster cross-component decisions (2026-06-01) — D-26..D-29

Surfaced by the cross-cluster seam-consistency adversary review of the C19/C20/C21/C23/C41 Sweep-2 deepening (the panel's R4 integration-tax lens). Each is an adopted cross-component contract resolution, applied corpus-wide by a single integrator pass and propagated into the affected specs. Decided by the lead from the seam review; not to be re-litigated.

- **D-26 — `event_id` wire type = `EventId = {stream, seq}` (C23-canonical).** The seam review found a HIGH-severity drift: C23 §4.1 produces a structured `EventId = {stream, seq}` while C41 consumed a bare `uint64` at the D-5 chain seam (would collide across multiple streams). Canonical: C41 consumes C23's `EventId` struct. Applied: C41 §3.6 + §4.2 (`uint64` → `EventId`); C23 unchanged (already canonical).
- **D-27 — `payload_digest` is C41-computed, not C23-provided.** C41 implied `payload_digest` arrived on the incoming C23 `EventRecord`; C23 carries no such field. Canonical: C41 computes `payload_digest` over the C23 record bytes at chain-append time (chain-internal). Applied: C41 §3.4/§3.6/§4.2; C23 unchanged.
- **D-28 — dependency-edge field name = `depends_on` (C19 M1-freeze anchor).** C19 used `depends_on`, C20 used `dependencies` for the same edge. Canonical: `depends_on` (matches C19's M1 interface freeze). Applied: C20 §4.1 + §4.5.0 (`dependencies` → `depends_on`); C19 unchanged.
- **D-29 — `created_by` common wire type = colon-delimited `"kind:id"` string (resolves OQ-C41-4).** The wire type drifted (`string`/`actor`/`actor_id`/`ActorRef`). Canonical: the wire value is the `"kind:id"` string (e.g. `"rig:worker-1"`), parsed by C41's `resolve_actor` into the `ActorRef` struct (the in-memory/parsed form). Applied: C19/C20/C21/C23 normalize the `created_by` wire type note; C41 marks **OQ-C41-4 RESOLVED** and keeps `ActorRef` as the parsed form.

### Operator adoption of the prevent-gate (2026-06-01) — D-30 (closes auto-001 + both morning-review items)

- **D-30 (ADOPTED — operator, 2026-06-01) — Prevent/block is required for unattended; the watcher is the sanctioned discharge, its design deferred.** The operator re-adopts **D-20 as conditional on prevention** and adopts the [auto-001 rubric](decisions/auto-001-detect-only-binding-gate.md): unattended operation (P2) and self-modification (P3b) require the substrate to **BLOCK (prevent at the tool-call/process boundary)** — not merely detect — out-of-boundary access on the relevant blast-radius face. **Discharge:** if Gas City does not prevent natively (per the [D-23 spike](D-23-gas-city-spike-protocol.md)), an **enforcement watcher that blocks WILL be added** — sanctioned in principle; its **design is DEFERRED until the spike confirms the substrate does not already prevent** (don't design what we may not need; the watcher's design must still pass the bar when built). Until prevention is established (native or watcher), unattended operation is **blocked** (human-in-the-loop). The per-rig-class "structurally-safe parts may run unattended" optimization remains available but **secondary**. **Supersedes** the auto-001 Round-2 "prevent layer NOT pre-blessed / descope-to-L4 as the sole default discharge" wording — the prevent path is sanctioned, only its premature design is withheld. **Resolves morning-review item #1** (block: yes) **and #2** (per-rig-class: kept, secondary). Applied: auto-001 brief (adoption section); C43/C34/C42/C56/C57 spec annotations (`[D-30 ADOPTED …]`); STATUS; HANDOFF (binding constraint for the next run). The empirical prevent-vs-detect spike (C34:OQ-C34-1 ≡ C43:OQ-C43-1) stays the open input that decides whether the watcher is needed.

### Sweep-2 spine-run decisions (2026-06-01) — operator inputs + cross-component rulings

- **D-31 (ADOPTED — operator, 2026-06-01) — Multiple rigs per city.** A *city* (one Gas City install / the `gc` substrate, C01) hosts **multiple rigs** (C42) — not one. The `[[rig]]`/`[[rigs]]` array-of-tables declares N rig partitions inside a single city; **rig partitioning (C42) is the isolation of these N co-resident rigs from one another** (e.g. a worker rig and a separate judge rig living in the same city — the D-17 holdout read-surface depends on worker-rig ≠ judge-rig). Specs MUST model multiple-rigs-per-city explicitly and MUST NOT assume one-rig-per-city. Affected/applied: C42 (rig model + partition contract across N rigs), C01 (a city hosts many rigs), C03 (the rig config section is an array of rig blocks), [`gascity-config-anchor.md`](gascity-config-anchor.md) (rig facts), and the fence (C34 holdout / C43 blast-radius reason per-rig and across-rig). Operator input during the Sweep-2 Gas City builder wave. Rewind: revert this entry + the C42/C01/C03/anchor multi-rig annotations.

- **D-32 (ADOPTED — lead, from the config anchor grounded in `gascity-prototype@b14c278`; 2026-06-01) — Rig config spelling is file-split.** Rig **path** bindings live in **`.gc/site.toml`** as **`[[rig]]`** (singular array-of-tables, `name` + `path`) — harvest-verified. The **`city.toml`** rig block (partition / `prefix` / role semantics, **no `path`**) is spelled **`[[rigs]]`** (plural) in the prototype's actual `city.toml.example`, contradicting D-23 F1's blanket "`[[rig]]` singular canonical" — so the **`city.toml` rig-block spelling is `needs-pinned-gc-run (G11)`** and specs MUST NOT assert a single canonical `city.toml` spelling. `[[rigs]] path =` (a `path` in `city.toml`) is an unambiguous PackV2 error. **Partially re-opens C42:OQ-4 / XC-9** (the `.gc/site.toml` half stays closed; the `city.toml`-spelling half re-opens, gated on G11). Applied: C01 / C03 / C42 / [`gascity-config-anchor.md`](gascity-config-anchor.md). Rewind: revert this entry + the anchor §3 spelling note.
- **D-33 (ADOPTED — lead, converged C02+C03 builders; 2026-06-01) — XC-7 CapabilityDescriptor ownership resolved.** The C02 and C03 Sweep-2 builders independently converged: **C03 owns the CapabilityDescriptor registry** (the authored capability catalog — a `city.toml` / config-layer concern); **C02 carries only a `capability_id` reference** in the pack manifest, not the descriptor definition. Resolves **XC-7** (the C02↔C03 ownership straddle flagged in both Sweep-1 specs). Applied: C02 (manifest references `capability_id`), C03 (owns registry + descriptor schema). Rewind: revert this entry + the C02/C03 ownership annotations.
- **D-34 (ADOPTED — lead, from the Gas City seam review + config anchor; 2026-06-01) — Tool-node command-key field name is a source contradiction, G11-gated.** AI-CONTEXT §13.3's `[[tool]]` sketch uses **`command`**; the prototype `pack/pack.toml` (per [`gascity-config-anchor.md`](gascity-config-anchor.md) §3) uses **`cmd`**. The real `gc` field name is **needs-pinned-gc-run (G11)** — neither is "harvest-verified" as canonical. Specs MUST carry the spelling note (as C02 §field-table and C03 do) and MUST NOT claim either spelling as verified. Applied: C02 (the line-186 "harvest-verified" over-claim corrected; field-table spelling note stands), C03 (`cmd` + note). **Carried residual OQs** (not blocking; later freeze): BoundReachedSignal C18→C39 transport (native bead-write floor stated, exact mechanism G11) and CapabilityDescriptor exact field names (Sweep-3 freeze). Rewind: revert this entry + the C02 line-186 edit.
- **D-35 (ADOPTED — lead, from Spec-intake seam review RSI-SEAM-02; 2026-06-01) — C09 render-context variables come from the C05 `DispatchRequest`, not a new C13 interface.** C09's template variables (`{{.BeadId}}`, `{{.CreatedBy}}`) are sourced from the **C05 `DispatchRequest`** (which already carries `bead_id` + `created_by`, C05 §3.4) — NOT from a runtime C13 (molecule) fetch. **C13 is NOT pulled into the spine** (it stays a non-spine Gas City component). Keeps the render seam C09↔C05, both in-spine, and avoids scope creep. Applied: C09 §2 / §3.1 / §3.2a / §4 / §5.1. Rewind: revert this entry + the C09 render-var edits.

### Evaluation-tier seam decisions (2026-06-01) — D-36..D-39 (lead, pre-briefed to the C30/C31/C32/C33 builders to prevent drift; grounded in D-1/D-13/D-15/D-17/D-30/D-31 + the inventory's backbone closure)

- **D-36 — Eval-tier trajectory flow is the Inspect AI log, NOT CXDB.** C31 (runner) produces an **Inspect AI trajectory log**; C32 (judge) scores that log; C33 reduces. The spine eval tier does **NOT** read trajectories from CXDB (C21) — CXDB (C21/C22) + the bridge (C24) stay **non-spine** (the back-half self-heal/replay/self-optimization reads CXDB and is deferred per the backbone). C33 writes the satisfaction record to **C19 (beads)**, not CXDB. Resolves envelope decision-fork #2 (C24 not pulled in). Rewind: revert this entry + the eval-tier CXDB-scope annotations.
- **D-37 — C31↔C32 contract = post-hoc scoring.** C31 runs the held-out scenario against the freshly built component → a **trajectory log** (the single hand-off artifact); C32 scores **post-hoc off that log** (Inspect AI's scorer phase), NOT C31 invoking C32 inline. Resolves **C32:OQ4**. Rewind: revert this entry + the C31/C32 contract sections.
- **D-38 — Judge read-surface SHAPE = a separate judge rig (the D-17 joint C42/C34/C32 freeze).** Per D-31 (multiple rigs per city) + D-17: the judge runs in a **separate rig** from the worker (worker rig + judge rig, co-resident in the city). The judge MAY read the worker's trajectory log + the held-out scenario partition; the worker MUST NOT read the judge rig or the scenarios (the holdout — C34 enforces+audits, C42 provides the partition); **no shared context window**. Resolves the unified **OQ-C42-3 + OQ-C34-3 + C32-OQ5** (D-17 freeze). Prevent-vs-detect of the worker→scenario read remains the D-23 spike's open question (D-30). Rewind: revert this entry + the C42/C32/C34 judge-partition annotations.
- **D-39 — `ScoreRecord` schema is owned + frozen by C32.** C32 defines the per-scenario judge-output `ScoreRecord` schema; **C33** (aggregate), **C34** (audit), and C46 (FP-rate, non-spine) consume it. Frozen at Sweep-2. Resolves **C32:OQ2**. Rewind: revert this entry + the C32 ScoreRecord schema.

### Fence + Bootstrap seam decision (2026-06-01) — D-40 (lead, pre-briefed to the C20/C52/C53 builders)

- **D-40 (ADOPTED — lead, resolving XC-2 / C20:OQ-3 / C52:OQ3; 2026-06-01) — `factory_build` build-state is a STATUS transition, not a type-flip.** The in-progress → completed advance of a factory self-build is a **`status` field transition on a single `factory_build` bead type** (`status: in_progress → completed`), **NOT** a flip from a distinct `factory_build_in_progress` type to `factory_build`. The cold-start / resume query keys on `factory_build` + `status = in_progress` (resolving **XC-2**'s AI-CONTEXT §16 hard-coded `gc bd find --type factory_build_in_progress` to a `--type factory_build --status in_progress` query). **C20** owns the `factory_build` schema + the `status` slot; **C52** drives the transition; **C53** records the go/no-go on the same bead (C53:OQ-4). Applied: C20 (factory_build lifecycle + status slot), C52 (build-state advance), C53 (go/no-go record). Resolves XC-2 + C20:OQ-3 + C52:OQ3. Rewind: revert this entry + the C20/C52/C53 `factory_build` annotations.

### Sweep-2 opus-panel integration fixes (2026-06-01) — D-41

- **D-41 (ADOPTED — lead, from the Sweep-2 opus-panel integration adversary; 2026-06-01) — Four cross-product integration fixes.** The 5-expert opus panel's cross-product integration adversary found 4 seam contradictions that the per-cluster seam reviews missed (each cluster review trusted the *other* side of a seam crossing two reviews). All corrected without architectural change:
  1. **C52↔C53 circular hand-off (was a deadlock)** → **linearized**: C52 review-phase → `ReviewVerdict` → `C53.decide(satisfaction, review_verdict, transfusion_verdict) → GoNoGoDecision` → C52 deploy-phase. C53 runs AFTER C52's human review; its decision is C52's deploy trigger (one-directional, no cycle).
  2. **`factory_build` status enum collision** → the build-state terminal aligns to C20's bead-envelope `state = closed` (the `in_progress → closed` envelope lifecycle), **NOT** a new `completed` value (which collided with C20's `{open, in_progress, closed}`); the go/no-go outcome is the separate `milestone_verdict` field. **This CORRECTS D-40's stated `completed` terminal to `closed`.**
  3. **C09↔C05 ordering** → C09's sequence is **DispatchRequest-first** (C05 builds the `DispatchRequest`, calls C09; C09 reads `bead_id`/`created_by` from it — consistent with D-35). C09's self-contradicting diagram fixed.
  4. **C41 actor-kind enum** → add `tool` → `{city, rig, agent, tool}` (admits `tool:<name>` emitted by C17/C32; D-29 wire type).
  Applied: C52 / C53 / C20 / C09 / C41 (see [`panel-sweep2/INTEGRATION-FIXES.md`](panel-sweep2/INTEGRATION-FIXES.md)). Panel overall: 4/5 `right-idea-change-X-before-building`, 1/5 `sound-as-is` — the spine SHAPE is sound; these were the change-before-building corrections. Rewind: revert this entry + the integration-fix commit.

### Triangle evaluation invariant (2026-06-02) — D-42 (operator-adopted; ADR-0069)

- **D-42 (ADOPTED — operator, 2026-06-02) — the spec–scenarios–system triangle is the canonical evaluation framing; the judge is a diagnostician, not a scorer.** Every build is three representations — **Spec (S)**, hold-out **Scenarios (H)**, **System (I)** — joined by three independently-verified edges: **S↔H** (scenario builder + spec builder make the correspondence correct + complete), **S↔I** (the system's own unit/integration/e2e tests — implementer-written, therefore gameable), **H↔I** (the judge, evaluated independently — the anti-gaming check). The judge measures H↔I; a misalignment is a **non-specific signal** whose root cause is attributed across **{judge, spec, scenario, system}**; the judge surfaces the attribution and recommends **incremental-fix** vs **discard-and-reimplement-from-revised-spec**. A component is **complete only when all three edges align** — 100% hold-out pass is necessary, not sufficient. Spec/scenario correction is performed by an authoring path **independent of the implementing worker** (anti-gaming). Canonical statement: [ADR-0069](../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md). **This reframes C32 (scorer → diagnostician), supersedes the lone-distribution-gate reading of C53 (→ tri-alignment completion), and adds the repair router to C52.** Implementation plan: **HANDOFF §0★**. Refines D-15 / D-38 / D-39 and the `auto-002` gate (now understood as the H↔I edge of the triangle). Rewind: revert this entry + ADR-0069 + the §0★ plan + the eval-tier spec deltas.

### Triangle diagnosis contract (2026-06-02) — D-43 (lead, implementing D-42 / ADR-0069 §0★.2; pre-briefed to the C32 builder + the C52/C53/C30/C08/C34 dependent wave)

- **D-43 (ADOPTED — lead, 2026-06-02; implements D-42 / HANDOFF §0★.2.1) — the judge's diagnosis is a companion `DiagnosisRecord`, NOT a mutation of the frozen `ScoreRecord`; owned + frozen by C32.** Reifying the diagnostician (D-42) requires a new per-build judge output. Of the two §0★.2.1 options (additive optional fields on `ScoreRecord` with a bead-type version bump, vs. a companion record keyed to the `ScoreRecord`), the **companion `DiagnosisRecord` is adopted** — so the **D-39 `ScoreRecord` freeze is preserved verbatim** and C33/C34/C46 keep consuming `ScoreRecord` unchanged. Cardinality: `ScoreRecord` stays **per (trajectory, scenario, judge)** — the per-scenario H↔I signal, unchanged; `DiagnosisRecord` is **one per build/evaluation pass** (per component-under-evaluation), computed by C32 over the set of `ScoreRecord`s for that build. C32 gains a `diagnose()` method alongside the unchanged `score()`.

  **Bead type: `softwarefactory.v4.beads:diagnosis_record`. Canonical frozen schema = C32 §3.2a.** Field summary (the contract C52/C53/C34 build against):

  | Field | Type | Req | Semantics |
  |---|---|---|---|
  | `factory_build_ref` | `string` | R | The `factory_build` bead this diagnosis is for (D-40 status bead) |
  | `component_id` | `string` | R | The component under evaluation |
  | `scenario_set_version` | `string` | R | C30 hold-out corpus pin evaluated (C34 audits) |
  | `score_record_refs` | `list<string>` | R | The per-scenario `ScoreRecord`s (the H↔I evidence) this diagnosis is computed over |
  | `holdout_pass_rate` | `float` (0.0–1.0) | R | Fraction of scenarios with `score_label = satisfied` (H↔I gate input) |
  | `all_scenarios_satisfied` | `bool` | R | True iff **every** scenario `score_label = satisfied` (the **100% hold-out floor** — necessary, not sufficient) |
  | `misalignments` | `list<Misalignment>` | R | Per-scenario misalignment detail (empty iff `all_scenarios_satisfied`); each = `{scenario_id, score_record_ref, observed, expected, gap, attributed_cause ∈ {judge,spec,scenario,system}}` |
  | `root_cause` | `enum{judge,spec,scenario,system,none}` | R | Primary root-cause attribution of the misalignment; `none` iff aligned |
  | `root_cause_rationale` | `string` | R | The judge's reasoning for the attribution (human-review reads) |
  | `secondary_causes` | `list<enum{judge,spec,scenario,system}>` | O | Additional contributing corners when multi-source |
  | `spec_defect_class` | `enum{none,localized,structural}` | R | When `root_cause ∈ {spec}`: `localized` (ambiguity patchable in place) vs `structural` (system faithfully built the wrong target → discard); `none` otherwise |
  | `repair_recommendation` | `enum{incremental_fix,discard_and_reimplement,none}` | R | The repair mode the judge recommends; `none` iff aligned. C52 routes on (`root_cause`, `spec_defect_class`, this) |
  | `repair_rationale` | `string` | R | Justification for the repair recommendation |
  | `tri_alignment` | `enum{aligned,misaligned}` | R | All three edges judged aligned; `aligned` **requires** `all_scenarios_satisfied = true` AND `root_cause = none` |
  | `judge_self_trust` | `enum{calibrated,uncalibrated}` | O | Whether the judge's own verdicts are trusted yet (PF-2 calibration precondition); informs C53 oversight, never the 100% floor |
  | `judge_model_id` | `string` | R | Judge identity (D-10) — the diagnosis is itself an auditable judge output |
  | `diagnosis_prompt_hash` | `string` | R | SHA-256 of the diagnosis prompt (C34 audit reproducibility) |
  | `created_by` | `actor` | R | C41 attribution — the judge rig (`"rig:judge-N"`, D-29) |
  | `diagnosed_at` | `timestamp` | R | UTC timestamp |
  | `error_code` | `string` | O | E-code if diagnosis was degraded |

  **Attribution → repair semantics (the C52 router key):** `system` (clear spec, trajectory genuinely fails) → `incremental_fix` = **polish** (patch system + its own S↔I tests); `judge` (mis-run / inconsistent / high ensemble disagreement / can't justify its own grade) → `incremental_fix` but routed to **recalibrate-judge-then-re-eval** (no system/spec change); `scenario` (scenario misrepresents the spec — tests what the spec doesn't require, or is itself ambiguous/contradictory vs the spec) → `incremental_fix` routed to **independent scenario correction** (C30 scenario builder + spec builder, never the worker); `spec` + `localized` → `incremental_fix` routed to **independent spec correction** (C08 + future C10/C11); `spec` + `structural` → `discard_and_reimplement` (independent spec correction, then throw away the system and rebuild from the revised spec).

  **Anti-gaming invariants (load-bearing — D-42 / ADR-0069):** (i) the `DiagnosisRecord` is produced **only by the judge rig** (D-38), never by the implementing worker; (ii) every `spec`/`scenario` repair route is executed by the **independent authoring path** (C08 + future C10/C11; C30 scenario builder + spec builder), **never the implementing worker** — without this, "fix the spec" degenerates into "weaken the spec until my output passes"; (iii) `tri_alignment = aligned` is **necessary-and-the-100%-floor-is-non-negotiable**: 100% hold-out pass (`all_scenarios_satisfied`) is necessary but **not sufficient** for `aligned` — the spec/scenario edges must also be clean. The **100% floor never lowers**; only the human-review / judge-trust **oversight** relaxes as the judge earns calibration (`judge_self_trust`).

  **Scope (capability-bar, §0★.3):** the independent spec/scenario-correction path is named as a **SEAM** to C08 + the future non-spine C10/C11 + C30; this pass specs the *contracts* (the `DiagnosisRecord`, the repair router, the independence requirement) and does **NOT** build the intent crucible (C11) / EARS linter (C10).

  Owner: **C32** (freezes the schema; only C32 may change a required field, by a new binding decision). Consumers: **C52** (repair router keys on `root_cause`/`spec_defect_class`/`repair_recommendation`), **C53** (`tri_alignment` + `all_scenarios_satisfied` are conjunctive go terms), **C34** (audits the diagnosis as a judge output; audits `scenario_set_version` staleness + `created_by` independence), human review. Refines D-39 (additively — `ScoreRecord` untouched), D-15 (holistic grading still feeds `satisfaction_score`; diagnosis adds the attribution layer D-15 deferred to FE-5), D-38 (diagnosis runs in the judge rig). Rewind: revert this entry + C32 §3.2a/§3.1a + the C52/C53/C30/C08/C34 diagnosis deltas.

## Cross-component issues (raised during Sweep 1 builds)

- **XC-1 — C19↔C20 dependency direction contradiction.** The canonical inventory lists C20→C19
  (schema before graph), but the dispatch batching and C19's builder treat them as co-foundational with
  C19 owning the graph engine and C20 the type catalog. Resolved provisionally as a co-foundational pair
  with an interface freeze (M1). Needs a canonical ruling. Owner: integrator pass.
- **XC-2 — G17 cold-start query vs schema.** C20 DELTA-02 turns `factory_build_in_progress` from a bead
  *type* into a `factory_build` + `in_progress` lifecycle *state*; AI-CONTEXT §16 hard-codes
  `gc bd find --type factory_build_in_progress`. Track B needs a compat shim or the cold-start query
  must change. Owner: C20 (B) + C52 self-bootstrap resume.
- **XC-4 — C20↔C22 bundle-id collision (foundational, must-fix).** C20 binds bead payloads to
  `v4.beads.v1`; C22 registers bead types under `strongdm.factory.v4`. Two foundational specs disagree on
  the canonical bead `bundle_id` — the bead-payload round-trip fails until reconciled. Must be fixed in
  both specs before any bundle-authoring task. Owner: integrator + C20/C22 (B). Also note C21-B names its
  CXDB bundle `softwarefactory.trajectory.v1` — the whole bundle-id namespace needs one ruling.
- **XC-4b — identity-namespace sprawl (extends XC-4).** FOUR unreconciled reverse-DNS namespaces now
  exist: bead `v4.beads.v1` (C20), type-registry `strongdm.factory.v4` (C22), trajectory
  `softwarefactory.trajectory.v1` (C21-B), pack `pack_id` (C02). Need ONE namespace convention ruling
  across C02/C20/C21/C22. Owner: integrator.
- **XC-7 — CapabilityDescriptor ownership straddle.** Same concept declared in both C02 and C03 (both
  flagged OQ3). Rule one owner. Owner: integrator + C02/C03.
- **XC-8 — RESOLVED by D-20 (was: Phase-0 capability enforcement is detection-only).** C02-B "kill on
  capability breach" and related controls have no enforcement teeth until C43 isolation. The two options
  were "sequence C43 earlier" vs "accept detection-only Phase 0"; **operator chose the former (D-20):** the
  C43 boundary-typing/blast-radius fence is pulled forward to a Phase-2 entry precondition, so the
  unattended/self-modifying window is no longer detection-only. The residual prevent-vs-detect *strength*
  question (does `gc` prevent or only detect) is the distinct D-23 spike (G11). Owner: closed; C43 fence is
  a P2 gate.
- **XC-9 — `[rigs]`/`[[rig]]` spelling inconsistent** across C01/C03/C42. Pick canonical. Owner: C07/integrator.
- **XC-3 — RESOLVED by D-18-block (see "Batch-4 review integration" above: "XC-3 RESOLVED — G18 numeric
  termination policy owned by C39").** C20 provides boundable schema slots
  (`attempt_no`/`max_attempts`/`escalated`/`closes`); the numeric policy (N attempts → escalate, F52
  oscillation detection, L5 ship authorization) is owned by **C39** (confirmed against C39's on-disk spec);
  **C18** owns the convergence loop + emits the bound-reached signal (C39 injects the per-pass bound C18
  enforces), **C20** owns the slots. Was: "deferred to C39 (and possibly C18) — confirm C39 owns it" — now confirmed.

- **XC-5 — C41↔C23 tamper-evidence chain ownership (blocker, from adversary).** C41-B DELTA-04 claims
  tamper-evidence "anchored in C23," but C23-B defers record hash-chaining (its OQ3). F14 "RESOLVED" rests
  on a chain that may not exist. Resolution: C41 owns the hash-chain computed over C23 `event_id`s; C23
  provides ordered `event_id`s only. Confirm and update both specs. Owner: integrator + C41/C23 (B).
- **XC-6 — Phase-0 signing assurance vs unsolved secrets (G37).** C41-B `signed`/`attested` assurance is
  over-stated while G37 (key storage) is unsolved — plaintext keys in `city.toml` collapse the ladder.
  Signing is a mechanism, not yet a control, until C03's SecretResolver (OQ) lands. Owner: C41/C03 (B).
- **RESOLVED by D-14 (was: DECISION NEEDED — signing mandatory vs optional).** Settled **optional/deferred**
  (README:229). Graduated-mandatory signing is **FE-3** (a distinct deferred enhancement, blocked on the
  open secrets gap **G37**), not a Phase-0 requirement; revisit at FE-3's trigger. G37 (secrets) ≠ FE-3
  (signing) — specs deferring secrets cite G37, not FE-3.

- **RESOLVED by D-1 (was: DECISION NEEDED — cross-family judge credential, critical path).** Settled by
  D-1: the judge uses the **same provider/family as the coder** for Phase 0, so no second-provider API key
  is required; C29's "judge family ≠ coder family" constraint becomes **advisory/relaxed** (active
  cross-family/cross-provider enforcement = **FE-1**, future). C32–C34 build against same-provider judging
  with holdout-integrity from rig partitioning + prompt/role isolation. (Gaps G20, G08 → FE-1.)

## Per-component open questions (harvested)
(Collector appends `C<ID>:OQ-n — text` rows here each pass. Initial seeds below.)
- C01: has anyone run `gc` end-to-end vs v4's Native claims? Pinned version+commit? (blocks on G11)
- C02: exact tool-node I/O channel (argv+files+exit vs stdin/stdout JSON) must be frozen vs real `gc`.
- C03: SecretResolver provider baseline under Max (env-injection vs Vault/SOPS); layer-merge precedence.
- C08: is "spec" collapsed into `prompt.template.md`, or a standalone target-system Markdown it references?
- C20: compat shim for hard-coded `factory_build_in_progress` query (see XC-2).

_Batch-2 + tail review wave (2026-05-31 harvest):_
- C04:OQ-1 — Max revokes unattended subprocess automation: what Provider/auth swap lands behind C04's seam, before/after the Jun-15-2026 Agent-SDK-Max path? Fallback auth undesigned (G12). *Shared with C28:OQ-1.*
- C04:OQ-2 — resume modes unenumerated ("multi-mode resume"/Native); which modes in scope + resume-failure escalation (re-dispatch? operator gate?).
- C04:OQ-3 — multi-session/seat horizontal scale ownership: C04 (hosting) vs C05 (dispatch/pool) vs C29 (routing)? (G34) *Shared with C28:OQ-3.*
- C04:OQ-4 — **RESOLVED by D-23 harvest (F7, 2026-06-01):** Phase-0 Provider-kind = **tmux** — each agent is one interactive `claude` process in its own pane under a single tmux server, managed by the `gc start` controller. Verified against gascity-prototype@b14c278. (Was: selection criterion unstated; inferred config-driven.) Non-tmux providers (k8s/subprocess/exec) remain future/config-driven.
- C05:OQ-1 — routing-key authority: C05 vs C09 vs C12 (who resolves name→template/role). *Shared seam with C09:OQ-1.*
- C05:OQ-2 — pool member-selection policy is Gas City's, not C05's (round-robin/least-loaded/sticky); unspecified, sweep-2.
- C05:OQ-3 — back-pressure: Gas City native dispatch vs reconciler (C18) tick — never a C05 queue; verify vs pinned `gc` (G11).
- C09:OQ-1 — C08↔C09 boundary under the faithful collapse (template file = spec); if integrator adopts optimized split, C09 inbound gains `spec_id` resolution. *= C05:OQ-1 seam.*
- C09:OQ-2 — template-variable namespace: is there a canonical variable set (bead fields/run ids) or arbitrary? v4 enumerates none.
- C09:OQ-3 — binding registry vs naming convention: formula-node→template-name→role as implicit pack-layout convention vs a registry.
- C10:OQ-1 — F38/EARS findings disposition: blocking vs advisory (v4 calls the linter "optional"); which finding classes block.
- C10:OQ-2 — concrete INCOSE R7–R35 → detector mapping (range cited by number, not enumerated).
- C10:OQ-3 — requirement-statement extraction over C08's free-form Markdown body.
- C10:OQ-4 — findings serialization (JSON/SARIF/text) — equal candidates, constrained by C02 output ABI; pick sweep-2.
- C10:OQ-1-vocab — RESOLVED by D-9 (F38 stays in C10, prose-glossary, no C07 registry).
- C12:OQ-1 — real Gas City formula schema (node/edge/kind/loop/parameter key names, TOML shape) unverified (G11), sweep-2.
- C12:OQ-2 — loop primitive vs pure DAG: how Gas City expresses bounded iteration in a "DAG file" (drives C15/C14).
- C12:OQ-3 — convoy/order boundary — RESOLVED by D-8 (convoy→C05, order→C40).
- C12:OQ-4 — node-kind field — taxonomy home RESOLVED by D-7 (set `{agent,tool,gate,sub_formula}` is C12's); on-disk field name/shape sweep-2.
- C12:OQ-5 — parameter-binding syntax (`$slot`) formula↔molecule contract, sweep-2 vs real `gc`.
- C13:OQ-1 — real `gc` molecule / `gc converge` model (is molecule a first-class `gc` object?) unverified (G11), sweep-2.
- C13:OQ-2 — C13 dependency-set reconciliation (dispatch brief vs inventory); C18 reconciler lands Batch 3 (driver lag).
- C13:OQ-3 — molecule⇄first-class-object boundary with C19 (state on beads, no shadow store).
- C13:OQ-4 — wisp definition (dispatch view of a runnable node-bead) — joint with C05.
- C13:OQ-5 — loop-iteration / per-node `status` field reconciliation with C12, C20.
- C24:OQ-1 — G27 residual contradiction: raw-API-bodies path bound (reading b), event-subset promotion a future-track item. *Mirrors C23:OQ-1.*
- C24:OQ-2 — file-completeness detection (G26): how does the C25 escape hatch signal a body file is complete.
- C24:OQ-3 — exact `session.id`→parent-turn rule + head-map persistence (bridge-local map vs re-query CXDB on restart) (G26).
- C24:OQ-4 — inbox-capacity / durability ceiling (G33): max CXDB-outage window before the inbox fills (OS spool is the bound).
- C24:OQ-5 — HTTP (:9010) vs binary (:9009) ingest under load (G26 back-pressure). *Mirrors C21:OQ-4.*
- C25:OQ-1 — G04 two-sinks statement — RESOLVED by D-12 (cross-referenced per-spec notes; fork at C25).
- C25:OQ-2 — raw-body file protocol seam (naming/atomic-completion/retention), shared with C24 (G26).
- C25:OQ-3 — emit-side durability when C26 is down (G33): no C25 buffer; rely on native exporter.
- C26:OQ-1 — C26→C27 ingestion seam — signal coverage + transport RESOLVED by D-11 (traces-only; OTLP/HTTP+Basic auth); only path/header sweep-2.
- C26:OQ-2 — G04 two-sinks/anti-edge placement — RESOLVED by D-12 (anti-edge stated at C26; no new doc).
- C26:OQ-3 — export durability when LangFuse down (G33): no custom buffer; native sending-queue+retry.
- C27:OQ-1 — C26→C27 ingestion endpoint — RESOLVED by D-11 (traces-only; transport settled); path/version-header sweep-2.
- C27:OQ-2 — LangFuse as "weak L4 fallback" event substrate: NOT adopted (CXDB is L4); confirm nothing reads trajectories from LangFuse.
- C27:OQ-3 — LangFuse license/SPDX pin (README "MIT core" vs AI-CONTEXT "Apache 2.0"); pin at deploy.
- C27:OQ-4 — G37 secrets handling (config owner C03); G37≠FE-3 per D-14 (secrets=G37; signing=FE-3, blocked on G37).
- C27:OQ-5 — trace retention/rotation (LangFuse-config + ops); build none.
- C27:OQ-6 — LangFuse-down durability (G33; owned at C24, exporter-side shared with C26).
- C28:OQ-1 — Max→API-key fallback named but undesigned, contradicts no-API-key model (G12). *Shared with C04:OQ-1.*
- C28:OQ-2 — no token-budget/cost model for L5-volume runs on one Max seat (G13/G32); quantify before throughput claims.
- C28:OQ-3 — agent-side rate-limit ceiling on one Max sub; is multi-seat/multi-session scale in scope, who owns it (G34)? *Shared with C04:OQ-3.*
- C28:OQ-4 — Skills/Subagents/Hooks/MCP registration schemas inferred declarative ([FAITHFUL-FILL]); confirm pack-level contract. *(RC28-05: C28 OQ1–4 + C04 OQ1/OQ3 are the shared review-log items the orchestrator pass harvests.)*
- C29:G08 — "model family" undefined — RESOLVED by D-1/FE-1 (Phase-0 same-provider judge = reading (b); provider-level (a) = FE-1). `family` stays a label.
- C29:G20 — judge model unsourced — RESOLVED by D-1/FE-1 (no Phase-0 second-provider credential; sourcing = FE-1).
- C29:G32 — cost-per-satisfaction model deferred to C46 (C29 is cost-aware only).
- C29:OQ — concrete stylesheet "judge != coder" grammar (AI-CONTEXT:514) → named rule here, grammar sweep-2.
- C42:OQ-1 — holdout enforce vs declare ownership RESOLVED by D-13 (C34 enforces+audits; C43 blast-radius; C42 provides); residual = does Gas City prevent at tool-call time or audit-after (G11/G21).
- C42:OQ-2 — are `worker` and `implementer` the same role under two names (Phase-0 vs Phase-2 rigs)?
- C42:OQ-3 — judge partition shape — SCOPED BY D-17 (Sweep-1 read-default fixed; partition SHAPE = unified OQ-C42-3+OQ-C34-3+C32-OQ5, joint C42/C34/C32 Sweep-2 freeze).
- C42:OQ-4 — **RESOLVED by D-23 harvest (F1, 2026-06-01):** canonical spelling is **`[[rig]]`** (singular); path bindings live in `.gc/site.toml`, `city.toml` `[[rig]]` blocks carry partition/role semantics only. `[[rigs]] path=` is a PackV2 error. Verified against gascity-prototype@b14c278. Closes XC-9. (Was: spelling inconsistent across C01/C03/C42.)

_Batch-3 review wave (2026-05-31 harvest) — D-15/D-16/D-17 applied:_
- C06:OQ-1 — F32 "Addressed" but integrity half (HMAC mail signing) optional/deferred (G36→FE-3, blocked on G37); when does signing become mandatory? *(seam: signature attaches at C06 Mail envelope, binds to C41 provenance.)*
- C06:OQ-2 — Mail retention / dead-letter / expiry policy for a recipient that never returns — inherited from substrate or C06-defined? sweep-2.
- C06:OQ-3 — is Nudge independently feature-gated or always-on once coordination config present? v4 gates `[mail]`, silent on Nudge.
- C06:OQ-4 — addressing granularity: recipients by individual `session.id` vs C42 role vs broadcast? sweep-2.
- C11:OQ-1 — the 9 field NAMES are FAITHFUL-FILL; GF-C exemplar is undefined in all four docs (count-9 is the only anchor). Locate real GF-C, confirm field set/grouping at sweep-2. *(load-bearing for C11.)*
- C11:OQ-2 — crucible record vs C08 spec: one artifact or two (co-versioned)? Contingent on C08:OQ-1; integrator call.
- C11:G23 — bootstrap-validation success criteria subjective; C11 supplies the DoD field (#7), gate/threshold deferred to C53 (asserted from inventory routing; confirm vs C53 spec, later-batch).
- C14:OQ-1 — is `gc formula export --format dot` native `gc` or v4-supplied? Corpus two-sided (README:385 "Add" vs :133/:384 "Custom/Build"); resolve via `gc` G11 spike; bar default = wrap-not-reinvent.
- C14:OQ-2 — loop/back-edge DOT encoding — **RESOLVED-scoped by D-16** (encoding owned by C12:OQ-2; joint C12/C14/C15 Sweep-2 freeze; C14 names marker, interim fail-loud → end-state marked-back-edge).
- C14:OQ-3 — exact canonical form (normalization) that makes `import(export(f))=f` decidable — sweep-2.
- C14:OQ-4 — the C14 DOT-profile grammar (restricted DOT subset `import` accepts + exclusion list) vs Attractor/Mammoth-shaped DOT — sweep-2.
- C14:OQ-5 — DOT encoding of node bindings + formula parameters; tracks C12 on-disk field decisions (C12:OQ-4) — sweep-2.
- C15:OQ-2 (top) — does C15 lint the C14 DOT export or the C12 formula directly? Default DOT-in via C14; loop-marker encoding = C14:OQ-2 → C12:OQ-2 (**D-16** joint freeze).
- C15:OQ-1 — blocking vs advisory disposition (README "optional"); sweep-1 picks advisory-default/blocking-by-config (parity C10:OQ-1); confirm sweep-2.
- C15:OQ-3 — Mammoth license (unverified, likely-MIT by 2389 convention — README:301 "verify") + the 21-rule enumeration (G30 boundary inherited from C38 Tracker transfusion); code-port iff verified MIT, else pattern-reimplement.
- C15:OQ-4 — findings serialization JSON vs SARIF vs text (constrained by C02 output ABI) — sweep-2.
- C16:OQ-G18 (top) — confirm **C39** (not C16) owns the heal-loop numeric policy (G18 / XC-3); non-reverting fail-safe (if C39/C18 disclaim, G18 needs a new home, NOT C16). C39 spec absent on disk — confirm sweep-2. *(C39-ownership confirmation; shared with C18:OQ-1.)*
- C16:OQ-1 — blocking vs advisory disposition (P4 "small add"); advisory-default/blocking-by-config (mirrors C10:OQ-1).
- C16:OQ-2 — concrete LLM-where-tool heuristic table + false-positive measurement (README names property, not detectors) — sweep-2.
- C16:OQ-3 — justification-annotation ("why a model is required here") on-disk home, joint with C12 — sweep-2.
- C16:OQ-4 — findings serialization incl. `falsifying_scenario` field (JSON/SARIF/text) — sweep-2.
- C18:OQ-1 (top) — confirm **C39** owns numeric termination policy (G18/XC-3); C18 owns loop + bound-reached signal + injected-bound enforcement only; C39 spec absent — confirm sweep-2. *(C39-ownership confirmation; shared with C16:OQ-G18.)*
- C18:OQ-2 — reconciler→C05 (re)dispatch trigger is inferred not v4-stated (RC05-01); confirm with C05 author (alt: C12-formula-step drives dispatch); flag as inference until pinned.
- C18:OQ-3 — native Health Patrol internals unverified (G11); C18 specs the contract (deterministic-first ordering, bounded pass, bound-reached), not the engine — confirm vs pinned `gc`.
- C30:OQ-1 (top) — scenario record fields + corpus manifest (Task file under `scenarios/<component>/`, provenance = git commit identity; explicit `created_by`?); freeze sweep-2 before C31/C32/C34 build. *(signing NOT part of record — DEFERRED→FE-3/G37, D-14.)*
- C30:OQ-2 — D-13 storage/enforcement seam: confirm C30 stores/authors, C34 enforces+audits, C42 provides partition.
- C30:OQ-3 — scenario signing DEFERRED confirmed (FE-3/G37, D-14); Phase-0 integrity = git content-addressing + rig isolation.
- C30:OQ-4 — CXDB vs git for scenario metadata; sweep-1 keeps authoritative home in separate git repo; confirm metadata home sweep-2.
- C31:OQ-1 (top) — session-id adapter depth (G25): does Inspect AI let the caller set/propagate `session.id`? thin 1:1 vs thick id-map — spike.
- C31:OQ-2 — exact `session.id` injection mechanism (given OQ-1) — sweep-2.
- C31:OQ-3 — one scenario → one `session.id` granularity (does one `inspect eval` map to one parent-chained trajectory?) — C24 G26 seam.
- C31:OQ-4 — `inspect eval` CLI surface + trajectory-log schema (exact flags + log shape) — sweep-2.
- C31:OQ-5 — run target / twin selection: confirm scenario/task (C30), not C31, selects the run target/twin.
- C32:OQ1 (top) — same-family judge bias residual (D-1): F48 stays Partial; when does it trigger FE-1 (cross-family), and what measurement (judge-FP via C46?) makes the call?
- C32:OQ2 — `ScoreRecord` schema seam (C33 aggregate + C34 audit + C46 FP-rate all bind); freeze early sweep-2.
- C32:OQ3 — cost/throughput for judge-suite + ensemble on single Phase-0 Max seat (shared C28 G13/G34, G32); quantify (→C46) before throughput claims.
- C32:OQ4 — runner↔scorer split (C31 runner, C32 judge): does C31 invoke C32, or C32 score post-hoc from CXDB, or both? confirm C31↔C32 contract sweep-2.
- C32:OQ5 — judge partition read-surface — **SCOPED BY D-17** (Sweep-1 default: judge MAY read trajectories+scenarios, worker MUST NOT read judge rig/scenarios; partition SHAPE = joint C42/C34/C32 freeze, unifies OQ-C42-3+OQ-C34-3).
- C33:OQ-1 (top) — G09 threshold value + ownership: C33 is threshold-free; cutline lives at C50/C53/C39; confirm value is operator/integrator policy.
- C33:OQ-2 — distribution representation + statistic set (continuous vs binned; which quantiles/spread; streamed?); freeze sweep-2 with C46.
- C33:OQ-3 — FE-5 enumerated per-criterion DoD — **RESOLVED by D-15** (Sweep-1 = holistic against C08 free-form DoD; enumerated DoD DEFERRED to Sweep-2, beneficiary C46).
- C33:OQ-4 — score scale + ensemble-collapse-to-one-score is C32's contract; C33 normalisation (I2) frozen against C32 output shape sweep-2.
- C34:OQ-C34-1 (top) — does Gas City PREVENT the worker's out-of-partition read at tool-call time, or permit-with-detect (G21 enforcement-strength, gated on G11)? Reading A (config+perms+detect) is the build; Reading B (hard-control) = residual → C43.
- C34:OQ-C34-2 — is the read/tool-call trail complete enough to make the audit sound? source = C23 bus / C25 OTLP / CXDB / C41 attribution (C41 supplies attribution, not the read trail) — sweep-2.
- C34:OQ-C34-3 — independence predicate for same-provider judge (distinct rig+prompt+partition; no shared context window) — **judge read-surface SCOPED BY D-17** (partition SHAPE = unified OQ-C42-3+OQ-C34-3+C32-OQ5, joint Sweep-2 freeze); "no shared context window" detection still open.
- C34:OQ-C34-4 — when FE-1 lands, does the family-difference check move into C34 or stay advisory in C29? (today relaxed per D-1.)
- C35:OQ1 (top, G43) — P8 maturity disagreement across 4 docs; spec rules automated scope = detect→why→log→surface, conversion operator-gated; confirm F10 "Addressed" valid only from Phase 3a, no earlier phase relies on the loop.
- C35:OQ2 — override-recognition predicate boundary (operator deny? edit-against-gate? force past failing linter?) + hook event-payload fields — the lone custom piece; sweep-2.
- C35:OQ3 — is the recurring-pattern report persisted as a bead (new C20 type) or transient? sweep-1 transient; persisted type = C20 change request (D-3).
- C35:OQ4 — rule-conversion encoding per sink + **which sinks are in scope**: v4 names only the C30 Inspect-AI rubric (PRIMARY); C10 (EARS) + C15 (Mammoth) sinks are a FAITHFUL-FILL inference (not v4-named, not C35 deps). Confirm with orchestrator whether the loop converts to C10/C15 at all or only the rubric. *(C35 C10/C15 sink scope.)*
- C35:OQ5 — recurrence threshold + false-positive policy for the predicate (how many recurrences = a pattern) — unquantified; sweep-2.
- C40:OQ-1 (top) — the "Orders prove insufficient → Temporal" trigger is undefined (AI-CONTEXT:486 defers Temporal but states no falsifiable trigger); convert deferred-Temporal bet into a falsifiable condition.
- C40:OQ-2 — Order-definition syntax + trigger-predicate grammar (`{trigger,launches,retry}`; how a trigger matches a C23 event) must bind to pinned `gc` — sweep-2.
- C40:OQ-3 — durability-ceiling depth (G33) unverified: crash-resume mid-step or step-boundary? re-launch idempotent? default retry bound? — sweep-2.
- C40:OQ-4 — C40↔C39 launch seam: confirm the contract by which an Order *drives* a C39 fix-task chain (the coupling is C40's faithful inference; C39 deps don't list C40). *(C40/C39 launch-seam confirmation.)*

_Batch-4 review wave (2026-05-31 harvest) — D-18/D-19 applied; XC-3 resolved:_

- **RESOLVED-update (Batch-3 rows):** C16:OQ-G18 and C18:OQ-1 (above) — both deferred the G18 numeric-policy ownership to C39 with the fail-safe "if C39 disclaims, G18 needs a new home." **RESOLVED by the XC-3-resolution / D-18-block:** C39's on-disk spec (§1/§3.2 contract 7/§6) explicitly accepts ownership; C18 owns loop + bound-reached; C20 owns slots. No new home needed.
- **Cross-component OQ — prevent-vs-detect (C43:OQ-C43-1 ≡ C34:OQ-C34-1).** Does `gc`/the pack loader *PREVENT* an out-of-partition read / a production-typed surface at tool-call / config-load time, or only permit-with-detect (audit after)? Settles whether C43's typing is a *control* or a *declaration*. Gated on **G11** (real `gc`); ownership already settled by D-13. **Both components share this identical substrate question** — freeze jointly.
- **Cross-component OQ — C36↔C37 population seam (C36:OQ-2 / C37:OQ-1).** The *carrier* is settled (C36's `anomaly` signal, C36 I3); the open residual is **granularity/aggregation**: does C37 cluster exactly C36's flagged set (C36 selects the population) or a broader set read from C21 (C37 `depends on C21`) with C36 scoring per-trajectory? Joint **sweep-2 freeze** of the `anomaly`-record shape + the selector granularity (C36 OQ-2 carrier/shape ⋈ C37 OQ-1 granularity).
- **Cross-component OQ-5 — G14 class-level transfusion-failure hedge (C52:OQ5 / C51:OQ-C51-2 / C54:OQ-5).** If a whole P3 sub-phase's transfusion bet fails (Healer/P3b, twins/P3c, self-opt/P3d), does the phase plan re-sequence/defer that sub-phase, or hand-build it? C51 + C52 route it to **C54**; C54 records it as OQ-5 but flags G14 is **outside its four assigned gaps** (G01/G02/G03/G31) — DEFERRED, needs orchestrator to home G14 explicitly across C51/C52/C54.
- **Cross-component OQ — C52/XC-2 build-state transition (= C20:OQ-3).** The `factory_build_in_progress` → completed `factory_build` advance form — a `type`-flip on one record vs a `status` transition (which also decides whether `factory_build_in_progress` stays a distinct `type`) — is **C20:OQ-3**. C52 commits only to *reaching* the completed state, never the mechanism (RC52-01); co-owner of XC-2.
- C36:OQ-1 — metric-stream read seam (C24 = provenance/lands stream, C36 reads via C21; inventory lists both as deps); confirm watched-metric set (CXDB/C24 side vs OTLP C25/C26) + G33 ceiling inherited (no C36-side durability).
- C36:OQ-2 — detector selection per metric class + the `anomaly`-signal record shape + **C20-bead-vs-C23-event carrier** + thresholds / FP-recurrence policy (F52); freeze sweep-2 with C37/C38/C20/C23.
- C36:OQ-3 — LLM-trajectory/semantic anomaly boundary: confirm C36 is the numeric generic base only; semantic layer is a separate later P11 surface ("compose on generic", AI-CONTEXT:328).
- C36:OQ-4 — F4 quality-metric scope: which quality series exist for C36 to watch at P3b (defining new quality metrics is out of scope); F4 honestly Partial.
- C36:OQ-5 — C36↔C37 population seam (= C37:OQ-1) — see cross-component row above.
- C37:OQ-1 — C36↔C37 population seam granularity (carrier = C36 I3 settled) — see cross-component row above; co-owned with C36:OQ-2.
- C37:OQ-2 — trajectory representation (I2/G32: turn-text vs tool-call-seq vs error-sig) + embedding-model id + HDBSCAN parameter set; freeze sweep-2 with C38 against real trajectories.
- C37:OQ-3 — G32 cost-figure ownership → C46 (cost-per-embedding); confirm no embed-all background mode required (reading (b): bounded anomalous population).
- C37:OQ-4 — G33 OOM ceiling / batch size for a large anomalous window; durability seam = C40 Orders + C21 fail-open, not in-stage HA.
- C38:OQ1 — C38↔C39 seam: ownership split **confirmed on disk** (C38 emits `Diagnosis`, C39 mints `fix_task`); only the *handoff mechanism* (C39 polls vs C38 hands off) is the sweep-2 residual.
- C38:OQ2 — G30 Tracker license verdict unverified (pattern-only until verified); framework + verdict → C51.
- C38:OQ3 — G07 diagnosis-correctness predicate + bar: local AC = match-the-human (README:499); general predicate → C51, threshold → C53.
- C38:OQ4 — `Diagnosis` schema seam: concrete schema (the contract C39 binds to + a human reviews) is FAITHFUL-FILL; freeze sweep-2 vs verified Tracker field shape.
- C38:OQ5 — cost/throughput for LLM root-cause per cluster on the single Phase-0 Max seat (shared C28 G13/G34, G32); per-cluster rate-limiter; quantify → C46.
- C39:OQ1 — G18 ownership confirmation: **C39 accepts the numeric termination policy** over C20 slots, consuming C18's bound-reached (XC-3 RESOLVED); confirm C20's slot set is sufficient else C39 files a C20 change request.
- C39:OQ2 — G18 policy *values* (N, oscillation window, L4-vs-L5 cadence) unquantified by v4; shape fixed sweep-1, values are operator/integrator config (confirm home = C03).
- C39:OQ3 — G35 fix-authorization: ship-without-review gated on C56 level (L5 dark only); multi-cycle F54 drift audit = C56/C57; confirm C39 reads level from C56 (named, not hard dep). *(reciprocal of C56:OQ-3.)*
- C39:OQ4 — C40↔C39 launch seam (= C40:OQ-4): does an Order launch/retry the heal chain or only persist it? sweep-2.
- C39:OQ5 — closure-verdict source: does C39 read satisfaction (C33), judge (C32), anomaly detector (C36), or all three? + "anomaly no longer fires" detection mechanism; sweep-2.
- C43:OQ-C43-1 — prevent-vs-detect (≡ C34:OQ-C34-1) — see cross-component row above. **Top OQ.**
- C43:OQ-C43-2 — does the P0→P3b exposure window need an interim bound before C44 twins, or is detection-only the accepted Phase-0 posture? *(XC-8 applied; informs D-18 confirmation.)*
- C43:OQ-C43-3 — exact boundary between C43's `isolated` type and C42/C04 worktree/process scope (label-on-C42/C04 vs distinct C43 sandbox — the latter an over-build); sweep-2 with C42/C04.
- C43:OQ-C43-4 — production-scissors declaration grammar + where it attaches (pack/`city.toml`, C02/C03); NOT wired to the dropped capability-grant engine (C02-04); sweep-2.
- C44:OQ-1 — G22/G31 sibling cross-check (C45 owns fidelity bar, C43 owns blast-radius/isolation): both **on disk and confirm** C44's attribution; cross-check concrete I2/I8 vs C45 §3 + I1/I2 substitution vs C43 §3 at joint sweep-2 freeze.
- C44:OQ-2 — three-mode precedence (replay→stateful→OpenAPI) + request-match/merge rule (G22-adjacent); freeze sweep-2 with C45.
- C44:OQ-3 — twin session-state + reset granularity (per-scenario vs per-step; concurrent-scenario state isolation) — interacts with C42 run-isolation + throughput claim; sweep-2.
- C44:OQ-4 — per-twin packaging schema (`[[service]]` TOML + fixture/cassette format), constrained by VCR/WireMock/Prism + C02/C17 ABI; sweep-2.
- C44:OQ-5 — which engine per twin (record/replay + stateful + OpenAPI choice); Go-native bias (go-vcr/HoverFly) per the per-twin Go binary; per-instance at instantiation.
- C45:OQ-C45-1 — G22 bar: concrete default fidelity dimensions + tolerance values + per-service-class starter templates (shape fixed sweep-1); sweep-2 per first real twin (C44). **Top OQ.**
- C45:OQ-C45-2 — real-service reference capture + drift refresh: where stored (**C44's record/replay capture?** C30 corpus? CXDB?) + refresh cadence (stale reference ⇒ F55 residual). *(C44 I3 is the candidate source — C44:OQ-1.)*
- C45:OQ-C45-3 — does C45 invoke C31 to drive probes at the twin, or run the probe corpus itself as a pack tool node? (mirrors C31:OQ-5.)
- C45:OQ-C45-4 — is `fidelity_pass` a hard gate on twin substitution or advisory? differs for scenario-runs (C31) vs production-default substitution (F44/C43)?
- C51:OQ-C51-1 — "named exemplar behaviors" extraction (the completeness anchor): operator at C11 intake? exemplar tests/docs? FAITHFUL-FILL → sweep-2. Without an anchor, "complete" is subjective (residual edge of G07). **Top OQ.**
- C51:OQ-C51-2 — G14 class-level fallback ownership → C54 (= cross-component OQ-5 above).
- C51:OQ-C51-3 — numeric satisfaction bar/threshold owner (shared G09): cutline at C53/C50 as operator policy; same C33 statistic C51's predicate reads. (parity C33:OQ-1.)
- C51:OQ-C51-4 — license census authority + staleness (G30, shared with C57): confirm C57 owns the census + verification workflow; adding an exemplar's license is a pre-transfusion step; no Phase-0 SBOM scanner.
- C51:OQ-C51-5 — transfusion-record signing (G36/G37/FE-3): `transfused_from` + verdict self-asserted (D-14); confirm Phase-0-acceptable and signing is FE-3 (blocked on G37), not Phase-0.
- C52:OQ1 — G23: C52 owns loop + mandatory review gate; **C53 owns rubric/scenario-set/pass bar**; C11 supplies next-component intent — confirm C53 is the authoritative bootstrap-bar home.
- C52:OQ2 — `C52-gate` decomposition: the inventory `C52-gate` dep is the C52-internal design-review gate (rubric→C53, level→C56), not a separate component — confirm so it isn't mistaken for an unbuilt dep.
- C52:OQ3 — gate decision-record home (new `factory_build` slot = C20 change request / C53 record / review bead) + **build-state advance = C20:OQ-3** (RC52-01; = XC-2 cross-component row above); sweep-2.
- C52:OQ4 — resume-failure escalation: AI-CONTEXT §16 gives only the happy path; unrecoverable `factory_build_in_progress` (missing handle / dangling pointer) → restart-from-spec sweep-1; escalation contract sweep-2. *(parallels C04:OQ-2 + XC-2.)*
- C52:OQ5 — G14 class-level fallback (shared with C51) → C54 (= cross-component OQ-5 above).
- C52:OQ6 — F54 audit-pack ownership: confirm owner (C43 isolation / **C57** residual register / dedicated pack) of the multi-cycle goal-comparison audit (G35) so F54 residual is explicitly homed, not assumed-covered by C52's gate.
- C53:OQ-1 — G09/G23 milestone bar *value* + decision rule (single quantile? distribution-shape? multi-term predicate over C33?): cutline at C53 (not C33), value is policy (shared C33:OQ-1 / C51:OQ-C51-3 / C50); freeze sweep-2 with C33/C51. **Top OQ.**
- C53:OQ-2 — fail-branch attempt bound + "add substrate" authorizer (README:519 "after a few attempts" fixes no count/authorizer); C53 requires *a* bound, value+authorizer = operator policy (relates to C56 ladder); sweep-2.
- C53:OQ-3 — bootstrap scenario-set sufficiency: how many scenarios / what coverage make the go/no-go credible for bet #3 (too-small set meets bar but is weak evidence); minimum-evidence guideline sweep-2 with C30/C51.
- C53:OQ-4 — C52/C51/C53 seam: who records what on the `factory_build` bead (C51 verdict + C52 review record + C53 go/no-go); slot ownership + grain (one decision per first-component build) + C20 slot requests; sweep-2 with C20/C51/C52.
- C54:OQ-1 — G01: two "layer" vocabularies ("three-layer + persistence" vs "Layer 0–6") never reconciled corpus-wide; C54 resolves locally (Reading A); architecture-wide rename → integrator/C57.
- C54:OQ-2 — may a later phase's *authoring* pipeline while an earlier phase's *exit gate* is pending (overlap), or strict end-to-end (INV-1)? faithful pick strict; operability relaxation = integrator call.
- C54:OQ-3 — **RESOLVED (adopted) by D-18/D-20** — C43 split-sequencing (boundary-typing→P2 entry precondition; twin-isolation→P3c). Operator confirmed 2026-05-31; "accept detection-only Phase 0" alternative rejected.
- C54:OQ-5 — G14 class-level transfusion-failure hedge ownership (inbound from C52:OQ5 + C51:OQ-C51-2) — see cross-component OQ-5 above; G14 outside C54's four assigned gaps, DEFERRED to orchestrator.
- C55:OQ-1 — G05: confirm empirical per-work-type selection (not a soft GF-M pre-commitment), "GF-M first ≠ GF-M chosen"; absolute cutline is C50/operator, not C55. **Top OQ.**
- C55:OQ-2 — work-type taxonomy: v4 names the *dimension* (README:33) not the *values* (only F20 greenfield/brownfield axis named); freeze canonical `work_type` set sweep-2 (source = C30 scenario families? separate axis?).
- C55:OQ-3 — experiment fan-out cost vs single-seat throughput (G32/G34): ten candidates × work-types × suite is multiplicative on one Max seat, "cost amortizes" (README:512) has no number; quantify with C46 before full grid.
- C55:OQ-4 — C48 significance seam (forward dep): the significance→C48 *routing* is now **recorded as D-19**; the residual open item is the C55→C48 *consultation-contract freeze* at sweep-2 when C48 is authored (interim withheld-significance behavior).
- C56:OQ-1 — G15: is the one-operator spec-authoring bottleneck a precondition C56 merely documents, or does sustained L4/L5 need a design response? does C52 (factory-builds-factory) eventually relieve the load? → C57 + review-log. **Top OQ.**
- C56:OQ-2 — G11/sweep-2: where the current authorized level lives + read API (single C03-layered operator value, read at the gated action for downgrade-safe re-read); confirm representation (`[autonomy] level` vs C56 surface). *(shared seam with C39 §3 contract 4.)*
- C56:OQ-3 — G35 ownership split + F54 audit-pack home: C56 = ladder + which-level-auto-ships + L4-default + named F54 obligation; C43 = blast radius; C39 = per-fix ship-gate; **C57** = objective-drift audit register + mechanism (unbuilt, Batch 5). *(reciprocal of C39:OQ3.)*
- C56:OQ-4 — is L5 promotion gated by anything machine-checkable (F54 audit-pack present+green) or purely an operator decision (README:498 "P12 mature and trusted" is a judgment)? sweep-2.

_Batch-5 review wave (2026-05-31 harvest) — all six accept-with-fixes; no new D-ruling (fidelity/sourcing applied in place + OQs deferred). D-6/D-15/D-19 in force, not re-opened:_

- C46:OQ-1 — G32 cost-model **dollar dimension + price reference**: tokens/time exact, $ = modelled tokens×reference-price = operator/integrator policy under flat $200/mo Max (G13, no per-token price); confirm $ is operator-config (not C46-derived) + how set under flat sub (amortised/marginal-zero/notional-API). (shared G09 cutline-value with C33:OQ-1.) **Top OQ.**
- C46:OQ-2 — which meta-metrics beyond the three named (README:269) — AI-CONTEXT:516 "values question" leaves "which specifically" to operator; sweep-1 fixes the three + makes the set config-extensible; confirm operator additions sweep-2 + that C50's gate reads whatever set C46 records.
- C46:OQ-3 — per-criterion meta-metrics (FE-5/D-15 beneficiary): C46 reads C33 **holistic** satisfaction (D-15); FE-5 names C46 per-criterion diagnosis as primary beneficiary "built last"; confirm per-criterion is the Sweep-2 extension revisited when FE-5 lands. (shared C33:OQ-3 / D-15.)
- C46:OQ-4 — C46↔C48 compare-contract + C46↔C33 schema freeze: freeze (a) logged metric-record schema jointly with C33's distribution-record + (b) the read-surface C48 consumes (D-19), sweep-2.
- **C46:OQ-6 (NEW — dep-edge; integrator/sweep-2 call) — from RC46-01 (major, fixed in place).** C46's cost/usage signal is natively OTLP **metrics** (C25 emit → C26 collector; AI-CONTEXT:172, spec/C25 §3.3) + the CXDB **read seam is C21** (spec/C24 §1: "C36/C37/C38/C49 read from C21, not from C24") with **C24 = writer/provenance** — NOT C24's raw-conversation-bodies payload. Prose fixed across C46 §1/§2/§3-I2/§4/§5/§6 + plan to mirror sibling C36. **Residual RESOLVED by D-24:** C46's pinned **inventory dependency edge** now reads **C21/C25** (in addition to C33), with C24 = writer/provenance. `component-inventory.md` dep column **edited this pass** (D-24).
- C47:OQ-1 — the C46-objective definition (inherits G09/G32): C47 points its search at C46's meta-metric objective, only as well-defined as C46's still-open cost model. **Top OQ.**
- C47:OQ-2 — C47→C48 hand-off contract + variant-set carrier: canonical variant-set shape + whether carrier is a C20 bead type or a C23 event (parity with C36's OQ-2 carrier question). RC47-02 narrowed the old two-way seam: faithful reading = **C47 emits candidate list; experiment/routing design = C48** (C48 §3/§4 already owns routing-strategy + arm-mapping); residual reframed to "how much provenance/metadata C47 attaches per candidate." sweep-2.
- C47:OQ-3 — search trigger + engine selection (DSPy prompt vs Optuna/Ray-Tune hyperparam) + fan-out budget (cost vs single-seat throughput, G32 → C46); sweep-2 ops choice.
- C47:OQ-4 — variant-space declaration grammar + ownership: *what is optimizable* (which prompt slots / hyperparam ranges); sweep-2.
- C47:OQ-5 — methodology/topology variant search explicitly **excluded** (that is C55) — confirm the boundary holds (C55 spec:111 "discovery (DSPy/Optuna) is C47"). *(RC47-01: DSPy's second v4 capability "statistical comparison (prompt-programs)" AI-CONTEXT:377 reconciled in-place — DSPy = variant-ID half only; all significance = C48 per D-19.)*
- C48:OQ-1 — G32: the C46↔C48 cost-signal contract + cost model; C48 wires the signal + degrades-with-declaration when absent (INV-6); C46 owns the model (reading (b)). **Top OQ.**
- C48:OQ-2 — test selection + multiple-comparison correction: which scipy/statsmodels test(s) + α / FDR control; sweep-2.
- C48:OQ-3 — routing strategy default + the bandit reward (G32): fixed-split flags (Unleash) vs adaptive bandit (MABWiser); how C46's cost enters the reward (satisfaction-per-$ vs spend-cap) on a single $200/mo seat; sweep-2. *(RC48-02: bandit miscited to README:273 — fixed; README:273 names only Unleash/GrowthBook/Flagsmith, bandit lives at AI-CONTEXT:361 + A72c.)*
- C48:OQ-4 — the C48→C50 verdict contract + the C55 consultation seam (D-19): freeze the verdict record C50 consumes + the C55→C48 consultation contract (spec/C55 OQ-4) sweep-2 when C50 authored; C48 is the single significance home for both. *(RC48-01 major, fixed: C55 was mislabeled as a **routing-input** source — corrected to **significance-verdict consumer only**; C55 runs its own eval-tier experiment per D-19, C48 routes C47 variants only.)*
- C49:OQ-1 — **the unsolved core of G19 — when is an LLM-step counterfactual *trustworthy enough* (N / variance bound / judge-FP guard) to feed C48/C50, vs "deterministic-slice automated + LLM-slice human-reviewed-only"?** Deterministic-tool replay over C21's O(1) branch is tractable-now (reproducible control + attributable variant diff); the full LLM-step counterfactual ships **labeled best-effort, reproduction NOT claimed**, routed to v4's "heaviest human review" (README:470). **v4's riskiest open question.** **Top OQ.**
- C49:OQ-2 — replay-job/result persistence: bead (new C20 type) vs durable CXDB artifact (the leaner default); sweep-2.
- C49:OQ-3 — replay cost model + budget: v4 gives no cost model for counterfactual re-execution → C46 (the expensive deferred slice); sweep-2.
- C49:OQ-4 — variant-injection seam + result-record schema: exact mechanism binding a variant into the branched midpoint + the result record; sweep-2. *(RC49-03 fixed: the deterministic-vs-LLM step classifier is **C12 node-kinds + C16 discipline-check (D-7)** which C49 consumes — not a C49-owned classifier; RC49-04: "deterministic ⇒ pure" qualified to "deterministic **and input-closed**", borrowing the Temporal-replay determinism constraint.)*
- C49:OQ-5 — twin-fidelity dependence (G22 inherited): the external-state half of a replay is only as good as the twin; bar deferred to C45; sweep-2.
- C50:OQ-1 — G09 promotion **cutline values + guard-metric set**: C50 applies the satisfaction + guard cutlines at this decision site (D-15/G09); **values** + **which C46 metrics are guards** are operator policy v4 does not fix (AI-CONTEXT:516); confirm cutline lives at C50 (not C33), freeze guard set sweep-2 with C46/C33 (shared C33:OQ-1 / C53:OQ-1 / C51:OQ-C51-3). **Top OQ.** *(RC50-01 major, fixed: an un-sourced "held-out(-scenario) signal" was listed beside v4's three named C46 metrics — re-grounded to the three named {cost-per-satisfaction, time-to-threshold, judge-FP-rate}; the F9/held-out concern routed through **C48's significance term over held-out runs**, not a fourth C46 metric.)*
- C50:OQ-2 — the multi-metric decision rule shape: how "moving coherently" / "materially regressed" operationalise over C46's stats (per-metric bar vector? Pareto-dominance? weighted composite under no-regression) — must stay multi-metric (INV-1/F47); freeze sweep-2 with C46/C48.
- C50:OQ-3 — reversibility / regression-triggered rollback: INV-4 retains prior default for back-out; whether back-out is operator-manual or automated regression-triggered (on a later C46 measurement) is unfixed; freeze sweep-2, build no rollback engine sweep-1 (the bar).
- C50:OQ-4 — C56 autonomy gate on the default-flip: whether a `promote` auto-flips the live default or surfaces for human ratification is gated on C56's authorized level (README:498/527); confirm the C50↔C56 seam (parity C39 §3.2 L5 ship-gate) + who authorizes auto-flip; freeze sweep-2 with C56.
- C57:OQ-C57-1 — what is F15, and what is its status? F15 absent from the 60-distinct catalog (G38); C57 adds the row but marks status TBD pending F15's definition recovery from the v3 catalog source; sweep-2.
- C57:OQ-C57-2 — is C57 a point-in-time snapshot (re-authored each integration) or a living doc with a propagation discipline from owning components? faithful sweep-1 = hand-maintained snapshot updated at integration milestones (no automated sync = the dropped enforcement engine); cadence + edit-owner open; sweep-2.
- **C57:OQ-C57-3 — RESOLVED by D-21 (was: MORNING-REVIEW operator call) — F54 objective-drift audit ownership.** The F54 / objective-drift audit is **homed at C57, registered UNBUILT** — the loudest residual after G31. **Operator decision (D-21):** stays a registered residual now, mitigated by a **cheap periodic human checkpoint** at each batched autonomy-ladder review (C56); a **real drift detector is REQUIRED before L5 lights-out** and is a hard precondition on L5 promotion. C56:OQ-3's "register *+ mechanism*" wording is settled: register + human-checkpoint now, mechanism before L5. *(reciprocal of C56:OQ-3 / C39:OQ3 / C52:OQ6 — all resolve to D-21.)*
- C57:OQ-C57-4 — does the G39 re-tally (Reading A, §4.3) belong at sweep-2 as a pure editorial pass, or must each owning component re-confirm its mode's status first? Several statuses are themselves contested (prevent-vs-detect ⇒ F12/F28 "Addressed" contingent); confirm editorial-vs-per-owner-freeze. sweep-2.
- C57:OQ-C57-5 — where do the architecture-wide editorial residuals routed to "integrator/C57" actually land — C57 register entries vs a separate integrator edit pass? G01 (two "layer" vocabularies, C54:OQ-1), G44 (El Kaim principle-count), namespace-sprawl (XC-4/XC-4b) are routed "integrator/C57"; C57's faithful scope = *record* them, a corpus-wide rename is an integrator action a register cannot perform. sweep-2 / integrator.

**License contradiction (from C48 RC48-03 — route to C57 license-hygiene register + sweep-2 version-pin; NO unilateral rewrite — faithful citation of a v4-internal contradiction).** README:273 (P12 capability-table row) calls Unleash **"commercial-with-OSS-core"** while README:322 (license table) lists Unleash **Apache-2.0** (AI-CONTEXT:358 concurs Apache-2.0); README:273 likewise positions Flagsmith MIT vs README:324 BSD-3. This is **v4's own internal inconsistency**, not a builder error — C48 faithfully cited both and asserts no license of its own (the bar: preserve a source contradiction, do not silently "correct" it). Resolution home = **C57's license-hygiene register** (C51:OQ-C51-4 confirms C57 owns the license census) + the **sweep-2 version-pin** step. Mirrors C27:OQ-3 (LangFuse "MIT core" vs "Apache 2.0") — the corpus has a recurring capability-row-vs-license-table SPDX-drift pattern; sweep-2 license census reconciles both.

**RC57-04 (CORPUS-WIDE source-header style — sweep-2/style follow-up; do NOT unilaterally rewrite).** Component-spec `> Source:` headers refer to sibling docs (`F-MODE-COVERAGE.md`, `FUTURE-ENHANCEMENTS.md`, `README`, `AI-CONTEXT`, `component-inventory`, OQ ids) as **bare text**, not descriptive relative markdown links as AGENTS.md "Internal document references" requires. This is the **prevailing style across the entire v4 spec corpus** (every spec's Source block is bare-text + carries dense line-anchored citations), so unilaterally re-linking only one spec's header diverges from the corpus without fixing the systemic issue. **NOT a fidelity defect.** Logged as a **corpus-wide sweep-2/style editorial pass** (sibling to OQ-C57-5's "integrator edit pass" routing). NOTE: this is an AGENTS.md-convention follow-up — AGENTS.md NOT edited this pass.
