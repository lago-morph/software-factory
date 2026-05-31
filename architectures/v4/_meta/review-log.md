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
- **XC-8 — Phase-0 capability enforcement is detection-only.** C02-B "kill on capability breach" and
  related controls have no enforcement teeth until C43 isolation (unbuilt, G31/G21). Several Track-B
  "prevention" claims are really detection at Phase 0; adversary softened wording. Real fix = sequence
  C43 earlier or accept detection-only Phase 0. Owner: C43 + integrator.
- **XC-9 — `[rigs]`/`[[rig]]` spelling inconsistent** across C01/C03/C42. Pick canonical. Owner: C07/integrator.
- **XC-3 — G18 numeric policy ownership.** C20 provides boundable schema slots
  (`attempt_no`/`max_attempts`/`escalated`/`closes`); the numeric policy (N attempts → escalate, F52
  oscillation detection, L5 ship authorization) is deferred to C39 (and possibly C18). Confirm C39 owns it.

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
- C04:OQ-4 — Provider-kind selection criterion (tmux vs k8s/subprocess/exec) unstated; inferred config-driven via C03, policy open.
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
- C42:OQ-3 — is the judge a third partition, or does it read `code` + scenario outputs role-isolated from the worker (D-1)?
- C42:OQ-4 — canonical `[rigs]` vs `[[rig]]` spelling inconsistent across C01/C03/C42 (XC-9).
