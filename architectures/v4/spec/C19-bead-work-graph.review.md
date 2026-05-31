# Adversarial review — C19 Bead store / typed work-graph (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Persistence & Memory
Target: spec/C19-bead-work-graph.md (+ plan-faithful/C19-bead-work-graph.md)
Charter: Track A — attack **fidelity & completeness**, not the design.

## Findings

### R19A-01 — major — `created_by`-without-config invariant overstates v4 vs C41 deferral
**Claim.** §3 invariant "Attribution-total" says a bead without `created_by` "is not well-formed" and §8 AC-1 says creating a bead without one *fails*. v4 says attribution is "automatic everywhere" / "native" (AI-CONTEXT §3.1 P9; README:227/371) — i.e. the runtime *always stamps* it — but never states the store *rejects* an un-attributed write. "Native/automatic" (the producer always supplies it) and "the store hard-fails on absence" (a validation gate) are different claims; the latter is a Track-B-style enforcement decision (it is exactly C19-B's DELTA-02).
**Evidence.** README:227 "every action carries identity… native `created_by`"; G36 explicitly notes attribution is *self-asserted and optional/deferred* at the verification layer. A faithful spec should assert *presence is native/total*, not invent a rejecting validation gate.
**Fix (applied).** Softened AC-1 and the invariant to "native/automatic — the create path always stamps a non-empty `created_by`" and moved the *reject-on-absence* enforcement to a FAITHFUL-FILL noting it is the minimal mechanism that makes "total" testable, flagged as the smallest consistent choice rather than a v4 fact.

### R19A-02 — major — bundle-id / CXDB-binding silence creates a latent cross-component contradiction
**Claim.** C19-A §1 ("NOT the CXDB trajectory store… A bead is not a CXDB turn") correctly separates the stores, but is silent on whether bead *payloads* are ever registered as CXDB types. The optimized siblings are not silent and they disagree: C20 binds beads to `v4.beads.v1`; C22-faithful registers under `softwarefactory.v4`; C22-optimized claims *one registry, two namespaces* under `strongdm.factory.v4`; C21-optimized names `softwarefactory.trajectory.v1`. C19-A's clean separation is the *correct faithful posture*, but it must say so explicitly so the integrator does not later read C19's silence as assent to C22-B owning the bead namespace.
**Evidence.** XC-4 in review-log; C22-B DELTA-04 ("single source of truth for both bead types and CXDB payload types"); C20-A/B `v4.beads.v1`.
**Fix (applied).** Added one sentence to §1 NOT-list and an OQ (OQ-C19-5) stating: faithfully, beads are a *separate* type space from CXDB turns (AI-CONTEXT §5 keeps them distinct stores); any bead↔CXDB binding is a C20/C22 concern and C19 asserts no shared bundle namespace. Flagged DEFERRED for the integrator (bundle-id collision).

### R19A-03 — minor — §2 "Bidirectional" dependency row contradicts the inventory it cites
**Claim.** §2 labels the C19↔C20 relationship "Bidirectional" and says "Faithful reading: a mutual foundational pair." The canonical inventory unambiguously lists **C20 depends on C19** (one direction). Track A may not silently re-scope a dependency the inventory states; a "mutual pair" is a *reading*, not what the source says.
**Evidence.** component-inventory C20 row: "Depends on: C19." XC-1 records the contradiction is between the inventory and the *dispatch brief*, not within the inventory.
**Fix (applied).** Relabeled the row "Upstream-of (C20 depends on C19, per inventory)" and moved the co-foundational "mutual pair" framing into OQ-C19-1 as the *proposed resolution* of XC-1, not as a faithful fact. The canonical inventory direction is stated first.

### R19A-04 — minor — §4 lists `history` as an owned field but v4 only names "bead history" as a query surface
**Claim.** The bead record table lists `history` as a stored field (cited README:228). README:228 pairs "event bus + bead history" as *audit sources*; it does not assert history is a denormalized field *on the bead record* (it may be derived from the event log / Dolt versioning).
**Evidence.** README:228; AI-CONTEXT §3.2 #2 (Dolt = versioned). Whether history is a stored field or a derived view is genuinely underspecified.
**Fix (applied).** Annotated the `history` row as `[FAITHFUL-FILL]` — "history is queryable (README:228); whether it is a stored field or derived from C23/Dolt is unspecified by v4 and deferred."

### R19A-05 — minor — §6 "reject unknown type" enforcement is asserted as the C19↔C20 contract but is unverified against Gas City (G11)
**Claim.** §6 row "Unknown/unregistered bead type" states the typed-total invariant is enforced at the C19↔C20 seam. Whether Gas City's native bead store enforces a *closed* type set or accepts free-form `type` strings is unverified (this is C20-A's own OQ-C20-4 / G11). C19-A asserts the enforcement without flagging that the substrate may not provide it.
**Fix (applied).** Cross-referenced OQ-C20-4 / G11 in the §6 row: "closed-type enforcement presupposes Gas City rejects unregistered types — unverified (G11); if the substrate accepts free-form types, enforcement becomes pack work (C02)."

## Cross-component note (for integrator, not fixed here)
- **C19↔C20 direction (XC-1):** recommend canonical = **C20 depends on C19** (inventory), built as a co-foundational pair behind a frozen `{id,type,created_by,edges,state}` envelope. C19 ships the generic container; C20 the catalog. The dispatch-brief's reversed arrow should be treated as "co-foundational," not a real reversal.

## Verdict
**accept-with-fixes.** Faithful and well-sourced; the only real fidelity defects are (a) over-claiming store-side rejection as a v4 fact (R19A-01) and (b) a dependency-direction label that contradicts the cited inventory (R19A-03). Both fixed in place. The bundle-id silence (R19A-02) is correct faithful posture but is DEFERRED to the integrator because the *optimized* siblings actively collide.

---

## Second-pass addendum (Subsystem Adversary, cross-component sweep)

A later subsystem-wide pass (C19+C20 both tracks, cross-checked against C21/C22) confirms the findings above
and adds the following. Where the first pass already tightened the attribution invariant (R19A-01), my
stamping-vs-rejection edit further sharpened the §3/§8 wording to say *stamping* explicitly; consistent, not
conflicting.

### R19A-06 — minor — Cold-start procedure cited "§16" here but "§13" in C20-A (same lines 694–699)
The same recipe is labelled AI-CONTEXT §16 in C19-A/C21-A/C22 but §13 in C20-A. Line numbers agree; the label
is the defect. C19-A matches the subsystem majority — **no edit to C19-A**; flagged in the C20-A review.

### R19A-07 — major — Edge model inconsistent across the faithful pair: C19-A implies one untyped depends-on edge while C20-A names three typed chain edges
C19-A §4/§8 AC-4 presume a single untyped "A depends on B"; C20-A §4.3 names `diagnosed_by`/`produces`/
`resolved_by` (typed). v4 says only "Tasks with dependencies" (untyped). The faithful pair states two edge
models. **Fix applied** — added an `[AMBIGUITY]` block to C19-A §4 recording both readings and routing
edge-kind ownership to the C19↔C20 freeze without inventing edge names.

### R19A-08 — minor — AC-6 backend transparency reads as sweep-1-testable but is Dolt-era / G11-gated
Phase 0 turns Dolt "explicitly off" (AI-CONTEXT §3.4); the Dolt backend is unverified (G11). **Fix applied** —
AC-6 annotated as sweep-2/Dolt-era and G11-gated.

### R19A-09 — major (escalation of R19A-02) — the bundle-id collision is an *ownership* fork, not just a string clash
Beyond the four conflicting strings (`v4.beads.v1` C20-B, `softwarefactory.trajectory.v1` C21-B,
`softwarefactory.v4` C22-A, `strongdm.factory.v4` C22-B), **C20-B and C22-B both claim to author the per-type
bead payload schema** (`fix_task`, `override`): C20-B says "two registries, one mapping" (C20 owns schemas,
binds to a CXDB bundle); C22-B says "one registry, two namespaces" (C22 is the single source of truth, owning
bead-type schemas as `kind: bead`). These are mutually exclusive architectures and both define the same
schemas today. **Fix applied** — extended OQ-C19-5 to name the ownership fork and C19's recommendation: C20
authors bead-type schemas; C22 hosts the registration *mechanism*. The string can't be pinned until ownership
is decided. DEFERRED to integrator.

### Recommended canonical resolutions (to integrator)
- **Bundle-id:** one reverse-DNS root, per-store sub-bundles — `softwarefactory.v4.beads` (C19/C20) and
  `softwarefactory.v4.trajectory` (C21/C22); **C20 authors bead-type schemas, C22 hosts registration.**
- **C19↔C20 direction:** **C20 depends on C19** (inventory); co-foundational, broken by the M1 envelope
  freeze. The reversed dispatch-brief arrow reflects the `validate` call seam, not a dependency reversal.

Updated verdict: **accept-with-fixes** (unchanged). No blockers in C19-A itself; the load-bearing residuals
(edge ownership, bundle-id ownership) are cross-component and DEFERRED to the integrator.
