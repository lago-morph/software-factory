# Adversarial review — C20 Bead schema registry (Track B, sweep 1)

Reviewer persona: Subsystem Adversary (Persistence & Memory)
Target: spec-optimized/C20-bead-schema.md (+ plan-optimized/C20-bead-schema.md)

Track B attacks the **design**: correctness, hidden coupling, failure handling, cost, simplicity,
scalability, security. Each delta is tested for justification.

## Findings

### RC20B-01 — blocker — Bundle-id collision compounded by a direct *ownership contradiction* with C22-B: both specs claim to author the per-type bead payload schema
Evidence: C20-B DELTA-07 / §1 NOT-list: "Two registries, **one mapping**" — C20 *owns* bead-type schemas and
merely *binds* each to a CXDB `{bundle_id,type,version}`; §4.2 lists full per-type payload fields for
`override`/`fix_task`/`factory_build`. **C22-B DELTA-04 / §1 / §4.2 asserts the opposite**: "**one registry,
two namespaces**" — C22 is "the single source of truth for both bead types *and* CXDB payload types," owns
bead-type schemas as `kind: bead`, and itself registers `fix_task`/`override`/`factory_build` with viewpoints.
Both specs define the `fix_task` payload schema. Mutually exclusive architectures. On top: the *bundle string*
is 4-way inconsistent — C20-B `v4.beads.v1`, C21-B `softwarefactory.trajectory.v1`, C22-A `softwarefactory.v4`,
C22-B `strongdm.factory.v4`.
Reasoning: §8 AC-6 ("a bead payload registered under its `{bundle_id,type,version}` is replayable as a C21
turn") cannot pass — the round-trip needs one root and one owner. Two foundational Batch-1 specs disagreeing
on who authors `fix_task`'s schema is an unbuildable seam (XC-4: "must be fixed in both specs before any
bundle-authoring task").
Suggested fix: **Applied (C20 side, loud deferral):** added a DELTA-07 DEFERRED block in §4.4 and rewrote OQ3
to name *both* the string collision and the ownership fork, marking `v4.beads.v1` non-canonical and stating
C20-B's recommended canonical (C20 authors schemas; C22 hosts registration only; root
`softwarefactory.v4.beads`). C22-B is not mine to edit — **DEFERRED to the integrator**. **Recommended
canonical (to integrator): C20 owns/authors bead-type schemas; C22 owns the registration *mechanism* + CXDB-
turn types only; roots `softwarefactory.v4.beads` (beads) + `softwarefactory.v4.trajectory` (CXDB).** Favours
the store-owner authoring its own schemas (C20-B's model); rejects C22-B's single-registry claim over beads.

### RC20B-02 — major — DELTA-04 overclaims G18 closure: `attempt_no ≤ max_attempts` bounds *within-anomaly* retries but NOT the cross-anomaly oscillation F52 actually describes
Evidence (pre-fix): §3 invariant + §6 "An unbounded/**oscillating** chain is unrepresentable"; §6 F52 row
"the `max_attempts`+`escalated` invariant is the **direct guard**." But F52 ("more controller patches") is
*cross-chain*: fix-A causes anomaly-B, fix-B causes anomaly-C, … Each is a **distinct** anomaly with a
**fresh** `attempt_no`, so the per-chain bound never trips. The invariant guards single-anomaly retry runaway
only.
Reasoning: This is the "G18 truly resolved vs merely relocated" question. DELTA-04 *partially* resolves G18
(single-chain termination is a real, auditable schema invariant — a genuine win over v4) but "oscillating
chain unrepresentable" / "F52 direct guard" overclaim. Cross-anomaly oscillation detection needs C39/C18 to
walk `caused_by` across chains — that half is *relocated*, not resolved.
Suggested fix: Scope to within-anomaly; route cross-anomaly oscillation to C39/C18 over `caused_by`.
**Applied** — §3 invariant, §6 G18 row, §6 F52 row now state within-anomaly scope and relocate cross-anomaly
oscillation to C39; DELTA-04 retitled "*partially* resolves G18."

### RC20B-03 — major — DELTA-02 breaks the literal §16 cold-start query; the OQ1 shim is load-bearing, unspecified, and pushes a C20 modeling choice onto C19's query layer (XC-2)
Evidence: DELTA-02 folds `factory_build_in_progress` into `factory_build` + `state=in_progress`; §4.2
"redefines" the literal `gc bd find --type factory_build_in_progress` query (hard-coded §16). OQ1 offers (a) a
C19 alias or (b) patching §16's command. The delta is justified (one stable `id` across the build life — real
operability win) but imposes a compat burden on C19 (the alias) or silently rewrites a cold-start command.
Reasoning: Sound delta, unresolved cross-component cost. If C19's `gc bd find` lacks a `--state` predicate
(G11 — unverified), option (a) is unbuildable and the fallback (b) changes a memorized command.
Suggested fix: Keep DELTA-02; make shim ownership explicit and spike C19 `--state` before advertising the enum
(the plan's T8 does — good). **Not applied** (delta defensible, plan de-risks it) — flagged as the top
cross-component cost; DEFERRED to the C19/C20 freeze.

### RC20B-04 — major — `validate` sold as O(fields)-local, but DELTA-05 (actor existence) + DELTA-07 (CXDB forward on write) imply runtime fan-out on the hot write path
Evidence: §7 "validation is O(fields) at write; no runtime registry lookups." But §3 "`created_by` non-null
actor (DELTA-05)" + §1 "points it at C41's actor type" — checking the actor *exists* is a runtime C41 lookup;
and §5 "payload registered/forwarded under its CXDBTypeBinding" on the write path is a runtime C22/C21 call.
So `validate` potentially fans out to C41 and C22/C21, not O(fields)-local.
Reasoning: Cost/coupling mismatch — cheap-and-local claim vs invariants implying network fan-out per write.
Suggested fix: Pin which checks are local (presence/shape/enum/lifecycle) vs deferred (actor-existence →
C41 audit; CXDB-forward → async, non-blocking). **Not applied** (needs C41 + C22 seam contracts) — DEFERRED;
recommend `validate` be local-only with actor-existence + CXDB-forward async, preserving the O(fields) cost.

### RC20B-05 — minor — Closed-catalog invariant presupposes Gas City enforces a closed type set (G11); should rest on C19's writer, not native gc
Evidence: §3 "a bead whose `type` ∉ catalog cannot be written"; §6 G17 RESOLVED. Native Gas City type-set
enforcement is unverified (G11). DELTA-06 already routes enforcement through C19's *writer* `validate` seam —
which makes it G11-independent.
Suggested fix: State the enforcement point is C19's writer (DELTA-06), not native gc. **Not applied** (largely
covered by DELTA-06) — flagged so the integrator confirms the writer-seam is the enforcement point.

### RC20B-06 — minor — `override` lifecycle bakes C35's loop policy into the schema, breaking symmetry with the (correctly-deferred) `fix_task`/C39 split
Evidence: §4.3 `override` lifecycle includes `pattern_surfaced`/`rule_proposed`/`rule_adopted` — these are C35
override-loop stages, not intrinsic record states. `fix_task`'s control policy is correctly deferred to C39
(OQ2); `override`'s is embedded here un-flagged.
Suggested fix: Note `override`'s post-`logged` states are C35-driven (schema reserves states; C35 owns
transitions), mirroring the `fix_task`/C39 split. **Not applied** (sweep-2 lifecycle detail) — flagged for
symmetry with OQ2.

## Cross-component resolutions recommended to the integrator
- **Bundle-id (XC-4) [load-bearing]:** roots `softwarefactory.v4.beads` (beads) + `softwarefactory.v4.trajectory`
  (CXDB). **Ownership: C20 authors bead-type schemas; C22 owns registration mechanism + CXDB-turn types only.**
  Reject C22-B's "single registry owns bead schemas" model (RC20B-01).
- **C19↔C20 direction (XC-1):** **C20 depends on C19**; production write path is a hard cycle broken by the
  interface freeze + a no-op `validate` stub (C19-B RC19B-01).
- **G18 ownership (XC-3):** C20 owns the *schema slots* + the *within-anomaly* bound; **C39/C18 own the
  cross-anomaly oscillation policy + numeric thresholds.** G18 *partially* resolved at C20, relocated for the
  oscillation half (RC20B-02). Confirm C39.

## Verdict
**accept-with-fixes.** The catalog (DELTA-03), versioned registry (DELTA-01), and within-anomaly loop-closure
invariant (DELTA-04) are strong, well-justified deltas that materially improve on v4's G17/G18 silence. Two
issues are load-bearing: the **bundle-id ownership fork with C22-B (RC20B-01, blocker)** must be reconciled
before any bundle-authoring task, and **DELTA-04's G18 claim overclaimed** (RC20B-02 — bounds within-anomaly
retries, not F52 cross-anomaly oscillation). Both now scoped/flagged in place; the binding ruling and the
C41/C22 validation fan-out (RC20B-04) are DEFERRED to the integrator.
</content>
