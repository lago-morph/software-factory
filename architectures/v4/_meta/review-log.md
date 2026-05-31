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
- **D-18 (PROVISIONAL — operator confirmation requested; morning-review item) — C43 split-sequencing.** C43 (isolation-boundary) splits across phases: its **boundary-typing + blast-radius half** (depends only on C42 + the P4 deterministic-first reconciler/tool-node primitives, NOT twins) pulls forward to a **Phase-2 entry precondition**; its **twin-isolation half** (blocked on C44 twins) stays at **Phase 3c**. Rationale: the P0–P3b window scales the factory unattended (P2) and self-modifies (P3b) with only after-the-fact detection (C34) and no blast-radius bound — the XC-8/F12/F44 hazard; the boundary-typing half closes most of it without waiting on twins. Aligns with XC-8 + D-13. Security risk-tolerance call → operator confirms (or, per XC-8's alternative, explicitly "accept detection-only Phase 0"). The faithful P3c manifest is preserved + annotated, not re-sequenced. (from C54 OQ-3 / RC54-05 + adversary split recommendation.)
- **D-19 — Methodology significance testing → C48.** C55 (methodology-experiment) computes per-(methodology × work-type) satisfaction distributions via the existing eval tier (C30/C32/C33) but does NOT perform statistical significance testing — routed to **C48** (Batch 5). C55 names the seam and withholds the significance claim (surfaces raw distributions + sample counts) until C48 lands; it does not reimplement stats. Mirrors C33's identical significance→C48 boundary; grounded in C48's inventory mandate ("determines whether a variant was actually better"). (from RC55-02 — was builder-asserted/adversary-softened, now logged.)

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
- C42:OQ-3 — judge partition shape — SCOPED BY D-17 (Sweep-1 read-default fixed; partition SHAPE = unified OQ-C42-3+OQ-C34-3+C32-OQ5, joint C42/C34/C32 Sweep-2 freeze).
- C42:OQ-4 — canonical `[rigs]` vs `[[rig]]` spelling inconsistent across C01/C03/C42 (XC-9).

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
- C54:OQ-3 — **RESOLVED (provisional) by D-18** — C43 split-sequencing (boundary-typing→P2 entry precondition; twin-isolation→P3c). Operator-confirm pending (security risk-tolerance; or "accept detection-only Phase 0" per XC-8).
- C54:OQ-5 — G14 class-level transfusion-failure hedge ownership (inbound from C52:OQ5 + C51:OQ-C51-2) — see cross-component OQ-5 above; G14 outside C54's four assigned gaps, DEFERRED to orchestrator.
- C55:OQ-1 — G05: confirm empirical per-work-type selection (not a soft GF-M pre-commitment), "GF-M first ≠ GF-M chosen"; absolute cutline is C50/operator, not C55. **Top OQ.**
- C55:OQ-2 — work-type taxonomy: v4 names the *dimension* (README:33) not the *values* (only F20 greenfield/brownfield axis named); freeze canonical `work_type` set sweep-2 (source = C30 scenario families? separate axis?).
- C55:OQ-3 — experiment fan-out cost vs single-seat throughput (G32/G34): ten candidates × work-types × suite is multiplicative on one Max seat, "cost amortizes" (README:512) has no number; quantify with C46 before full grid.
- C55:OQ-4 — C48 significance seam (forward dep): the significance→C48 *routing* is now **recorded as D-19**; the residual open item is the C55→C48 *consultation-contract freeze* at sweep-2 when C48 is authored (interim withheld-significance behavior).
- C56:OQ-1 — G15: is the one-operator spec-authoring bottleneck a precondition C56 merely documents, or does sustained L4/L5 need a design response? does C52 (factory-builds-factory) eventually relieve the load? → C57 + review-log. **Top OQ.**
- C56:OQ-2 — G11/sweep-2: where the current authorized level lives + read API (single C03-layered operator value, read at the gated action for downgrade-safe re-read); confirm representation (`[autonomy] level` vs C56 surface). *(shared seam with C39 §3 contract 4.)*
- C56:OQ-3 — G35 ownership split + F54 audit-pack home: C56 = ladder + which-level-auto-ships + L4-default + named F54 obligation; C43 = blast radius; C39 = per-fix ship-gate; **C57** = objective-drift audit register + mechanism (unbuilt, Batch 5). *(reciprocal of C39:OQ3.)*
- C56:OQ-4 — is L5 promotion gated by anything machine-checkable (F54 audit-pack present+green) or purely an operator decision (README:498 "P12 mature and trusted" is a judgment)? sweep-2.
