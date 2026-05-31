# Adversarial review — C22 CXDB Type Registry & Viewpoint Tagging (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Persistence & Memory
Target: spec/C22-cxdb-type-registry.md
Charter: Track A → attack FIDELITY and COMPLETENESS only, not the design.

## Findings

### RC22A-01 — major — Bundle-id `softwarefactory.v4` is invented and collides with the other foundational specs (XC-4)
**Claim.** §1/§4 name the v4 bundle `softwarefactory.v4`. **Evidence.** v4 never states a v4 bundle-id
(G17 — "the v4-specific type bundle … is never specified"); CXDB's only example is the illustrative
`mycompany.agents.v1` (AI-CONTEXT §5.3). So `softwarefactory.v4` is a fill — but it is presented in §1/§4
as the bundle name without a `[FAITHFUL-FILL]` marker on the *identity string itself*, and it collides
with sibling specs: C21-B `softwarefactory.trajectory.v1`, C22-B `strongdm.factory.v4`, C20-B
`v4.beads.v1`. A faithful spec inventing a namespace string that disagrees with its own Track-B twin and
with C20/C21 is exactly the XC-4 hazard. **Fix (applied).** Marked the `softwarefactory.v4` literal as a
`[FAITHFUL-FILL]` placeholder and added the XC-4 pointer: the *existence* of a v4 bundle is faithfully
forced (reading (b), correctly argued in §4), but the literal *string* is deferred to the integrator's
canonical-namespace ruling, not asserted as fact.

### RC22A-02 — major — I3 "viewpoint totality" (mandatory tag) is a designed strengthening that Track A may not silently impose
**Claim.** I3 makes a viewpoint tag mandatory on *every* payload ("'untagged' is not a legal state").
**Evidence.** The spec itself concedes "v4 (F50) says viewpoint tagging exists but does not say it is
mandatory" and labels I3 a `[FAITHFUL-FILL]`. Making an optional v4 feature *total* is a real design
choice (it changes the ingest contract for every writer — C24, the event bus, Go clients — all of which
must now supply a viewpoint or be rejected). That is closer to a Track-B improvement than a minimal
faithful elaboration; the minimal faithful reading is "viewpoint tagging is available and is the F50
mechanism," not "every payload must carry one or be rejected." The fill is *defensible* (the F50
"Addressed" claim is hollow if tags are optional — the spec argues this well) but it is load-bearing
enough that it should be flagged as the smallest-choice-with-a-caveat, not stated as an invariant the
build must enforce. **Fix (applied).** Kept I3 but re-tagged it explicitly as the *minimal choice that
makes F50 hold* and cross-referenced OQ1 (detect-vs-prevent), noting that whether totality is enforced
at write-time vs audited is a Track-B/C57 decision — so a faithful builder doesn't hard-reject untagged
legacy writes without the integrator's sign-off.

### RC22A-03 — minor — Viewpoint enumeration (`architecture`/`spec`/`implementation`) is a fill that disagrees with C22-B's enum
**Claim.** §4 enumerates three viewpoints. **Evidence.** Correctly flagged `[FAITHFUL-FILL]` and well
argued (F50's title forces architecture+spec; implementation is the minimal third). But C22-B (Track B)
uses a *five*-value enum (`architecture | spec | trajectory | telemetry | control`). The faithful 3-set
and the optimized 5-set will not diff cleanly; a reader comparing tracks sees two different closed enums
for the "same" mechanism. This is acceptable for Track A (it stays minimal) but the divergence should be
surfaced. **Fix (applied).** Added a one-line note that the optimized track widens the enum and that the
canonical set is an integrator decision (a closed enum is a breaking migration to change later — C22-B
OQ2 raises the same point).

### RC22A-04 — minor — F50 marked "Addressed" but mechanism is detect-and-label only — correctly caveated; no fix needed
**Claim.** §6/OQ1 concede C22's mechanism is tagging + query separation, not enforcement that the
*correct* viewpoint is chosen at write time (a writer can mis-tag a spec as architecture). **Evidence.**
This is the right faithful caveat (mirrors the G21/G36 detect-vs-prevent pattern) and is already routed
to OQ1 / C57. **Fix.** None — accept as-is; the honesty is correct for Track A.

### RC22A-05 — minor — C20↔C22 "separate parallel registries" is the right faithful reading but the Track-B twin unifies them — flag the contradiction
**Claim.** §1/§4/OQ2 treat C20 (bead types) and C22 (CXDB payload types) as separate parallel
registries. **Evidence.** Faithful and minimal (v4 never unifies them). But C22-B DELTA-04 *unifies*
them into one registry with two namespaces, and C20-B DELTA-07 binds bead types into a CXDB bundle —
so the two tracks take opposite structural positions on the C20↔C22 relationship. Track A's choice is
correct for its charter; the cross-track contradiction needs the integrator. **Fix (applied).** Added
an XC-4-adjacent note in OQ2 that the optimized track unifies the two registries, so the integrator
sees both readings.

## Verdict
**accept-with-fixes.** The faithful core (reading (b): v4 *must* register its own bundle to make F50
"Addressed" and §5.5 projection real; immutable versioned schemas for replay-safety) is correct and
well-traced. The fidelity defects are (1) an invented bundle-id string asserted as fact and colliding
across specs — now marked a fill + deferred to XC-4 — and (2) the mandatory-viewpoint invariant being a
heavier-than-minimal fill — now caveated. No fidelity blockers; the namespace ruling is the integrator's.
