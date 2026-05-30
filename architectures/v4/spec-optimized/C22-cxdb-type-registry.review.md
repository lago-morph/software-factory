# Adversarial review — C22 CXDB Type Registry & Viewpoint Tagging (Track B, sweep 1)

Reviewer persona: Subsystem Adversary — Persistence & Memory
Target: spec-optimized/C22-cxdb-type-registry.md
Charter: Track B → attack the DESIGN hard. Are the [DELTA]s justified, or hidden coupling / taste?

## Findings

### RC22B-01 — blocker — Bundle-id `strongdm.factory.v4` collides across four foundational specs AND contradicts C20-B's own binding (XC-4)
**Claim.** DELTA-01 names the concrete bundle `strongdm.factory.v4`; types are namespaced
`strongdm.factory:factory_build_in_progress` (§4 table). **Evidence.** Four foundational specs name this
namespace incompatibly: C22-B `strongdm.factory.v4`, C22-A `softwarefactory.v4`, C21-B
`softwarefactory.trajectory.v1`, C20-B `v4.beads.v1`. Worse than a cosmetic clash: **C22-B's own
DELTA-04 claims one registry serves BOTH bead-type and CXDB-payload-type namespaces** and registers
`fix_task`/`override`/`factory_build` under `strongdm.factory.v4` (§4 table, kind=`bead`) — but **C20-B
DELTA-07 independently binds those exact same bead types to `v4.beads.v1` / `v4:fix_task`**. So the two
optimized specs register the *same* bead types under *two different bundle-ids*. A cold-agent
`gc bd find --type factory_build_in_progress` (the G17 query DELTA-01 exists to satisfy) resolves
against whichever bundle wins — and the bead-payload→CXDB round-trip (C20-B AC "CXDB binding
round-trip") fails because the binding points at a bundle C22 didn't register under that id. This is the
must-fix XC-4 collision, and C22-B is the spec that most concretely entrenches it. Also note `strongdm.`
is a *vendor* reverse-DNS (the upstream CXDB author) — pinning the factory's own bundle under the
vendor's namespace is a lock-in smell, not a neutral choice. **Fix (DEFERRED — integrator ruling).**
Flagged the collision + the C20-B contradiction in the spec; recommended canonical ruling below. C22 and
C20 must agree on the bead-type bundle-id before any bundle-authoring task.

### RC22B-02 — major — DELTA-04 "one registry, two namespaces" is hidden coupling between C20 (bead schema) and C22 (CXDB types) that the inventory keeps separate
**Claim.** DELTA-04 makes C22 the single source of truth for *both* bead types and CXDB payload types.
**Evidence.** The inventory keeps C20 (bead schema registry) and C22 (CXDB type registry) as distinct
components on distinct stores (C19 vs C21). DELTA-04 collapses them, which (a) makes C22 a hard
dependency of C19/C20's cold-start path (`gc bd find` now routes through CXDB's `registry/`), coupling
the bead work-graph's queryability to the CXDB process being up — a Phase-1 component the bead store
(Phase 0) must not depend on; and (b) contradicts C20-B, which keeps its *own* bead-type schemas and
only *binds* to a CXDB bundle (DELTA-07). The "single source of truth" goal is sound, but routing bead
cold-start through CXDB inverts the dependency direction (C20 is more foundational than C21/C22). **Fix
(applied).** Annotated DELTA-04 in the spec: the *registry-of-record for bead types* should stay with
C20 (Phase-0, no CXDB dependency); C22 may *import/mirror* the bead-type vocabulary for projection, but
bead cold-start MUST NOT require the CXDB process. Flagged the C20-B contradiction explicitly.

### RC22B-03 — major — `Resolve(version?) → latest` is a non-determinism footgun on the replay path; OQ-1 raises it but the API still ships it
**Claim.** `Resolve(bundle_id, type, version?)` returns the highest version when `version` is omitted
(§3), with a "callers needing determinism MUST pin" caveat. **Evidence.** C49 counterfactual replay and
C37 clustering read *historical* turns whose correct schema is the version they were *written* under, not
"latest." A resolve-latest default means the easy/ergonomic call is the *wrong* one for every replay
consumer — a classic footgun where the safe path requires every caller to remember to opt out. DELTA-03's
whole point is replay determinism; a latest-defaulting resolver undercuts it. **Fix (applied).** Changed
the contract so replay/read paths resolve against the *turn's recorded version* (the turn already carries
`{bundle_id,type,version}` — C21 stores it), and `version?`-omitted resolve is permitted only on the
*live-write* path. Made "resolve the version the payload was written under" the default for reads.

### RC22B-04 — major — Validation-on-every-append puts a JSON-Schema check on C21's p50<1ms hot path with no cost budget
**Claim.** §5 flow 2 + I2: C21's ingest calls `Validate` (full JSON-Schema check) on *every* append;
§7 says "schemas must stay cheap (compile at load)." **Evidence.** C21's performance target is p50<1ms
append (AI-CONTEXT §5.5); a synchronous JSON-Schema validation per turn — especially for large
raw-API-body payloads (whole model responses) — can dominate that budget. The spec acknowledges the
tension but resolves it only with "compile schemas at load," which bounds *compilation* cost, not
*validation* cost over a multi-KB payload. For the highest-volume payload class (trajectory turns from
C24), per-append deep validation may be the single biggest ingest cost. **Fix (applied).** Added a
tiered-validation note: cheap structural checks (triple resolves, required envelope fields) on the hot
path; deep body-schema validation either sampled, async, or restricted to control-plane types (beads,
verdicts) — NOT mandatory deep-validation of every high-volume trajectory turn inline. Flagged exact
policy as sweep-2 with a cost budget.

### RC22B-05 — minor — Closed five-value viewpoint enum frozen now, but three of five values are inferred (C24/C37/C38 not consulted)
**Claim.** I3 freezes `viewpoint ∈ {architecture, spec, trajectory, telemetry, control}`; OQ-2 admits
three are inferred. **Evidence.** A *closed* enum that's wrong is a breaking registry migration (the
spec says so). Freezing it before the downstream owners (C24 telemetry, C37/C38 self-heal) confirm their
payload classes risks an expensive migration. **Fix (applied).** Downgraded the enum from "frozen" to
"provisional/extensible-until-sweep-2-sign-off" and required C24/C37/C38 confirmation before the close,
matching OQ-2.

### RC22B-06 — minor — `architecture_doc` / `spec_artifact` as CXDB payload types overreaches C22's scope into C08
**Claim.** §4 registers `spec_artifact` (viewpoint=spec) and `architecture_doc` (viewpoint=architecture)
as CXDB payload types. **Evidence.** The spec artifact is C08's owned format (a version-controlled
Markdown source-of-truth), not a CXDB trajectory payload. Registering it as a CXDB payload type implies
specs flow through CXDB, which isn't v4's model (specs are git artifacts; CXDB holds trajectories). These
two rows look added only to give F50's architecture-vs-spec distinction a concrete pair, but they may not
correspond to real stored CXDB payloads. **Fix (applied).** Noted that `spec_artifact`/`architecture_doc`
as CXDB types must be justified by an actual stored payload class (e.g. a *reference/pointer* turn) or
moved to viewpoint-tags-on-references rather than full payload types; flagged for sweep-2 with C08.

## Verdict
**needs-rework** (one DEFERRED blocker + two majors that change the component's coupling). The viewpoint
enforcement (DELTA-02) and append-only/version-monotonic registry (DELTA-03) are good, well-motivated
improvements. But (1) the **bundle-id collision (XC-4)** is entrenched here and directly contradicts
C20-B; (2) **DELTA-04's registry unification inverts the C20→C21 dependency** and couples bead cold-start
to the CXDB process; and (3) **resolve-latest is a replay-determinism footgun**. The namespace ruling is
deferred to the integrator; the coupling and resolver fixes are applied. Re-review after XC-4 is ruled.
