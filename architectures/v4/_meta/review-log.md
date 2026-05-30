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
- **DECISION NEEDED — signing mandatory vs optional.** Track A holds README:229 "optional/deferred";
  Track B makes it graduated-mandatory. Integrator/human must settle; if mandatory, G37 + XC-5 must be
  pulled forward with it.

- **DECISION NEEDED — cross-family judge credential (critical path).** C29's "judge family ≠ coder
  family" constraint (consumed by C32/C34) has no *satisfiable* path: Max issues no second-provider API
  key (AI-CONTEXT §4.1). The whole evaluation/judge tier (C32–C34) is blocked until an upstream
  provider/credential decision lands (or the cross-family requirement is relaxed). Owner: human +
  integrator; gates Batch-3 evaluation components. (Gaps G20, G08.)

## Per-component open questions (harvested)
(Collector appends `C<ID>:OQ-n — text` rows here each pass. Initial seeds below.)
- C01: has anyone run `gc` end-to-end vs v4's Native claims? Pinned version+commit? (blocks on G11)
- C02: exact tool-node I/O channel (argv+files+exit vs stdin/stdout JSON) must be frozen vs real `gc`.
- C03: SecretResolver provider baseline under Max (env-injection vs Vault/SOPS); layer-merge precedence.
- C08: is "spec" collapsed into `prompt.template.md`, or a standalone target-system Markdown it references?
- C20: compat shim for hard-coded `factory_build_in_progress` query (see XC-2).
