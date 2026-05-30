# Review Log — open questions, deferrals, and cross-component issues

Central sink for open questions (OQs), deferred decisions, and adversarial findings that need an
orchestrator/human call. Per-component docs raise OQs inline; a periodic **collector** agent harvests
them here so the primary doesn't have to read every doc. Do not have many agents append concurrently —
this file is written by the primary or a single collector agent per pass.

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
- **XC-3 — G18 numeric policy ownership.** C20 provides boundable schema slots
  (`attempt_no`/`max_attempts`/`escalated`/`closes`); the numeric policy (N attempts → escalate, F52
  oscillation detection, L5 ship authorization) is deferred to C39 (and possibly C18). Confirm C39 owns it.

## Per-component open questions (harvested)
(Collector appends `C<ID>:OQ-n — text` rows here each pass. Initial seeds below.)
- C01: has anyone run `gc` end-to-end vs v4's Native claims? Pinned version+commit? (blocks on G11)
- C02: exact tool-node I/O channel (argv+files+exit vs stdin/stdout JSON) must be frozen vs real `gc`.
- C03: SecretResolver provider baseline under Max (env-injection vs Vault/SOPS); layer-merge precedence.
- C08: is "spec" collapsed into `prompt.template.md`, or a standalone target-system Markdown it references?
- C20: compat shim for hard-coded `factory_build_in_progress` query (see XC-2).
