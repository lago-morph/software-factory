# Adversarial review — C52 Self-bootstrap recursion & design review (canonical track, sweep 1)

Reviewer persona: Bootstrap Adversary — critic-fixer
Target: spec/C52-self-bootstrap.md + plan-faithful/C52-self-bootstrap.md
Posture (post-convergence single track): attack FIDELITY + COMPLETENESS, not design — PLUS the
capability-for-principle bar (flag hardening-on-existing-capability vs new P-recursion capability).

## Bar check (the KEEP)

The genuine P-recursion capability is correctly isolated and the over-builds are explicitly dropped:
- **Self-targeted spec-authoring + dispatch via the normal build flow** (C08 format → C12/C13/C28) —
  present and defended (I4, AC2; §7 "What the capability-bar dropped" rejects a bespoke bootstrap
  engine). ✓
- **Mandatory human-design-review gate, non-bypassable, no auto-deploy path** — the keystone, present
  as I2 / AC4 / contract 6 with an enforced negative test (deploy-with-review-unset is blocked).
  Grounded verbatim in README:498. ✓
- **Resume = C20 `factory_build_in_progress` + `gc converge resume`** — present (I5, AC7; §7 drops a
  custom resume mechanism). Grounded verbatim in AI-CONTEXT §16 (694–699). ✓
- **No second build engine, no second eval stack, no custom resume** — all three explicitly dropped in
  §7 and re-asserted in plan T1/risk #5. ✓

**Routing check (C52 must NOT absorb these):** predicate→**C51** ✓, validation rubric→**C53** ✓,
autonomy level→**C56** ✓, sequencing→**C54** ✓ — all correctly listed under "Explicitly NOT" (§1) and
in the §2 dependency table; none is absorbed. The `C52-gate` inventory-dependency is correctly read as
the C52-internal gate (not a phantom component) — OQ2. **G14** (consumes C51's
`transfusion-insufficient` per-component; class-level hedge routed to C54 — OQ5) and **G23** (bar→C53,
intent→C11; explicit AMBIGUITY block + OQ1) are both addressed-or-deferred faithfully.

Citation spot-checks all passed verbatim: README:480–491 (5-box diagram), :429–436 (Phase-2 milestone +
the `[[provider]]`/daily-reporter fixtures), :498 (the gate), :519 (iterate-then-need-substrate), :527
(L4 "for as long as needed"); AI-CONTEXT §16 694–699 (resume procedure); F-MODE F54/L93, F43/L75,
F25/L102; C51 §3.5 (`transfusion-insufficient` is real, emitted on fail/inconclusive).

## Findings

### RC52-01 — major — Spec over-commits to a `factory_build_in_progress → factory_build` *bead transition* mechanism that C20 has explicitly left open (C20:OQ-3)
**Claim.** §1 ("the `factory_build_in_progress` bead transitions to a completed `factory_build` record"),
§3 contract 7 ("the `factory_build_in_progress` bead transitions to a completed `factory_build` record
(C20 lifecycle, D-3)"), §4 ("advances to a completed `factory_build` on deploy"), §5 step 7, and AC6 all
assert a specific lifecycle mechanism: **one bead whose type/record mutates from `factory_build_in_progress`
to `factory_build`.** **Evidence.** The canonical C20 spec keeps `factory_build` and
`factory_build_in_progress` as **two distinct literal `type` strings** (C20 §4.2), and adds an envelope
`status` field whose relationship to the type-encoded lifecycle is **unresolved and explicitly flagged**:
C20:OQ-3 — *"v4 encodes lifecycle in the type string for builds (`factory_build` vs
`factory_build_in_progress`) but C20's faithful elaboration also adds an envelope `status`. … Resolving
this affects whether `factory_build_in_progress` is a distinct type or `factory_build` +
`status=in_progress`."* Under C20's chosen literal-two-types reading, a bead's `type` is an identity
field (the thing `gc bd find --type` matches on) and is not obviously mutable, so "the in-progress bead
*transitions to* a `factory_build` record" asserts a mechanism C20 has neither settled nor endorsed. This
is C52 (the *consumer* of a C20-owned schema, per its own I5/AC8 deference invariant) silently picking the
outcome of an open C20 question — the precise over-reach AC8 forbids ("a needed new field is a change
request to C20 … never a local extension"). **Fix (applied).** Re-tagged the transition language as
lifecycle-*advance* that is recorded through the C20-owned shape **whose concrete form (type-flip vs
`status` transition on one record) is C20:OQ-3**, so C52 commits to *that the build reaches a completed
`factory_build` state* (faithful to AI-CONTEXT §16's two type names) without asserting the unsettled
mechanism. Added the C20:OQ-3 dependency to OQ3 (gate-decision-record home already routes to C20/C53
sweep-2; this is the adjacent open seam).

### RC52-02 — minor — C52 is a named co-owner of review-log XC-2 but the spec carries no XC-2 cross-reference (only the plan mentions it in passing)
**Claim.** §3 contract 2/8, §5 sub-flow A, §6, AC7 all reproduce the cold-start query verbatim
(`gc bd find --type factory_build_in_progress`) as the resume entry point, but the spec never notes that
this exact query is the subject of review-log **XC-2**. **Evidence.** XC-2 names its owners as
*"C20 (B) + **C52 self-bootstrap resume**"* — C52 is one of the two explicitly-named owners of the
reconciliation. XC-2 records that the optimized C20-B (DELTA-02) folds `factory_build_in_progress` into
`factory_build` + `state=in_progress` and therefore needs a compat shim for the literal §16 query; the
canonical C20 keeps the literal type, so C52's verbatim query *does* resolve today — but a reader of C52
alone cannot see that its resume contract sits on a known cross-track seam (and is the same seam as
RC52-01). The plan §5 risk #3 mentions XC-2 once; the spec is silent. Faithful-completeness gap, not a
contradiction (the canonical reading is internally consistent). **Fix (applied).** Added a one-line XC-2
cross-reference at the resume contract (§3 contract 2) noting C52 is a co-owner of the cold-start-query
reconciliation and that the verbatim query resolves under canonical C20's literal-type choice (the
divergence is RC52-01 / C20:OQ-3).

### RC52-03 — minor — Source header lists D-15 as a "relevant binding" but D-15 is tangential to C52
**Claim.** The `> Source:` header cites *"**D-15** (satisfaction holistic against C08 free-form DoD)"*
among C52's binding decisions. **Evidence.** D-15 governs how **C33/C32** compute the satisfaction
distribution (holistic vs enumerated per-criterion DoD). C52 never invokes satisfaction directly — it
consumes **C51's** `{pass|fail|inconclusive}` verdict (and C51, in turn, is graded against C08's DoD).
The dispatch brief names the relevant bindings for C52 as **D-6 and D-3** (and D-3 is indeed load-bearing
here). D-15 is one hop removed (it constrains C51's predicate internals, which C52 treats as a black box),
so listing it as a C52 binding is a minor mis-emphasis that slightly overstates C52's coupling to the
satisfaction-computation decision. Not a fidelity error in any body claim — purely a header citation.
**Fix (applied).** Re-tagged the D-15 mention as the *transitive* binding it is (it shapes C51's predicate,
which C52 consumes), so the header doesn't imply C52 itself is bound by the satisfaction-holism decision.

## Verdict

**accept-with-fixes.** Faithful, well-traced, and correctly scoped to the bar: the three KEEP capabilities
(self-targeted spec-authoring+dispatch, the mandatory non-bypassable design-review gate, resume over the
C20 lifecycle) are present and load-bearing, every absorbable concern (predicate/rubric/autonomy/sequencing)
is correctly routed out, and G14/G23 are addressed-or-deferred with explicit OQs. The one substantive
finding (RC52-01) is a fidelity over-commitment to an unsettled C20 lifecycle mechanism, now qualified to
match C20:OQ-3; the two minor findings add an XC-2 cross-reference and correct a tangential D-15 citation.
All three fixes applied in place; nothing architecturally significant deferred.
