# Adversarial review — C44 Digital Twin (per service) (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Digital Twins (P7 / Layer 5)
Target: spec/C44-digital-twin.md + plan-faithful/C44-digital-twin.md
Charter: canonical track → attack FIDELITY and COMPLETENESS only, not the design; PLUS the
capability-for-principle bar (HANDOFF §2): flag any addition that hardens existing stack capability
rather than delivering new capability tied to a 12-principle.

## Summary of attack surface checked

- **THE BAR (off-the-shelf vs custom).** LocalStack / record-replay (VCR/go-vcr/HoverFly) /
  stateful-mock (WireMock/Mountebank/Mockoon) / OpenAPI-mock (Prism/Stoplight) are off-the-shelf. The
  declared keep — *the twin's assembly + the declared cloned-contract surface, exposed as a C17 tool
  node* — is the genuine principle-tied capability the stack does not provide. **C44 honors the bar
  correctly**: §1, INV-4, AC-8, and plan T3/T4/T5 + the critical-path note all repeatedly state the
  three modes are *wired, not written*, and explicitly DROP a custom/general twin-mock-replay framework
  (no C44-specific SURVIVOR-PASS drop is violated; the dropped `boundary_class` tag is C41-07 and C44
  does not invoke it). No bar violation found.
- **SEAMS (G22 → C45, G31 → C43).** Verified against the **now-on-disk** sibling specs: C45 owns the
  fidelity bar (predicate + verdict) and C43 owns the lethal-trifecta blast-radius bound + twin
  isolation (D-13). C44 carries **no fidelity verdict** and **no enforcement teeth** — INV-1 guarantees
  on-contract+served-from-twin (explicitly *not* "indistinguishable from real"); INV-2 only guarantees
  the twin itself does not reach production while serving, and routes the *agent-cannot-bypass*
  enforcement to C43. The gaps do **not** silently fall back into C44. Confirmed clean.
- **D-6 nomenclature.** Spec/plan say "canonical track"; no live "Track A/Track B" framing. Clean.
- **Citations.** Spot-checked ~20 line/section refs against README, AI-CONTEXT, F-MODE-COVERAGE: all
  accurate, including the §7 Layer-5 table (C44 cites §7 correctly — note C45's own spec mis-cites the
  same table as §6.2, but that is out of this review's edit scope). D-13 is quoted faithfully.

## Findings

### RC44-01 — major — "Sibling specs NOT on disk yet / not yet written" is stale and now factually wrong; it misframes OQ-1 and the §6 deferrals
**Claim.** The Source header, both §6 ambiguity blocks (L244, L264), OQ-1 (L351/L354), and plan §5/§"open
questions" (L86, L111) repeatedly assert **C45 and C43 are "the same batch but not on disk yet" / "not yet
written."**
**Evidence.** `ls spec/` and `ls plan-faithful/` show **C43-isolation-boundary.md** and
**C45-twin-fidelity.md both exist** (sweep-1, canonical track). Worse for the original framing: those
specs *confirm* every seam C44 binds — C45 §1/§3 "owns the fidelity predicate (the bar) … does not build
the twin (C44)"; C43 §1 "C43 OWNS the distinct lethal-trifecta blast-radius bound … routes `twin`-typed
surfaces to C44 twins." So the deferrals are not merely "binding the seam from C44's side" against an
absent counterpart — they can be (and now are) **cross-checked against the written counterpart**. The
stale claim understates the strength of the seam and tells the integrator (OQ-1) to "confirm at their
build" what is in fact already confirmable today.
**Fix (applied).** Updated all six locations to state C43/C45 are **on disk (sweep-1, canonical track)
and confirm C44's seam attribution** (C45 owns the fidelity bar/verdict; C43 owns blast-radius +
isolation), with OQ-1 retargeted from "not yet written; confirm at build" to "cross-check the I2/I8 shape
vs C45 §3 and the I1/I2 substitution surface vs C43 §3 at the joint sweep-2 freeze." The deferral
*decisions* (G22→C45, G31→C43, D-13) are unchanged — only the false "absent sibling" premise is corrected.

### RC44-02 — minor — "Service selection (twin vs real) is the caller's/scenario's choice, not C44's" omits C43's twin-by-default routing and reads as a soft contradiction with C43 §3.2
**Claim.** §1 (I1, L45–46) and §2 (C30/C31 row, L90) state twin-vs-real selection is **"the caller's /
scenario's choice, not C44's"** and "C44 is the addressable target, not the selector."
**Evidence.** Correct that C44 is *not* the selector — that disclaimer is sound and must stay. But the
flat phrasing collapses **two distinct selection contexts** and silently omits C43, which §6/OQ-1 elsewhere
leans on: C43 §1/§3.2/INV "twin-by-default" makes **C43** the owner of the deterministic *default-twin
routing* (external dependency → C44 twin unless a per-pack production-scissors declaration opts into
`production`, F44). The scenario/runner choosing a *run target* (C31:OQ-5, an eval-context choice) is a
different axis from C43's default-deny-to-production posture for the broad-tool agent. Naming only "the
caller's/scenario's choice" reads as if no deterministic routing policy exists, which understates C43 and
is in mild tension with C43's "a config that defaults a surface to `production` is invalid" invariant.
**Fix (applied).** Reworded I1 and the C30/C31 row to distinguish the two axes: (a) C44 is the addressable
target, never the selector; (b) **C43** owns the deterministic twin-by-default *routing* policy for the
broad-tool agent (F44), and (c) the scenario/runner selects the *run target* in an eval context
(C31:OQ-5). The "not C44's" disclaimer is preserved; the omission of C43 is closed.

### RC44-03 — minor — The fidelity *reference* seam (C45's OQ-C45-2) is under-connected: C44's record/replay fixtures (I3) are a named candidate source but C44 routes C45 only to the I8 hook
**Claim.** §3 (I8), §4 (Fidelity-observation trail), and §6/AC-9 route C45 to C44's **request/response +
real-vs-twin diff seam (I8)** as the thing C45 consumes, but do not connect C44's **record/replay
fixtures (I3 / "Record/replay fixtures" state)** to C45's fidelity *reference*.
**Evidence.** C45 §6 (OQ-C45-2, binding) decides its behavioural ground truth is a **recorded/golden
reference captured out-of-band via record/replay (README:199)** — "the same capture C44's record/replay
produces" — and explicitly asks "where the reference is stored (**C44's record/replay capture?** a C30
corpus? CXDB?)". So C44's I3 capture-mode fixtures are a first-class candidate for C45's reference corpus,
yet C44 only advertises the I8 *live-trail* hook to C45. This is a completeness gap at a real seam, not a
contradiction (the *home* of the reference is legitimately C45's open question).
**Fix (applied).** Added a one-line note at I3/I8 (and the §6 G22 block) that C44's record/replay capture
(I3) is a candidate source for **C45's recorded fidelity reference** (C45:OQ-C45-2), distinct from the I8
live observation trail — leaving the choice of reference home to C45's OQ, but making the seam visible from
C44's side. No fidelity bar is asserted by C44.

### RC44-04 — minor — Headline citation range "AI-CONTEXT §7 lines 341–345 / 341–346" over-reaches the three twin modes (which are 341–343)
**Claim.** §1 (L13, L23) cites "AI-CONTEXT §7 lines 341–345" and "341–346" to support
"records-and-replays / holds-state / answers-per-contract" and the three composed modes.
**Evidence.** The Layer-5 table rows are: 341 HTTP record/replay, 342 Stateful HTTP mocking, 343
OpenAPI-driven mock (the three modes); **344 is Contract verification (which C44 correctly assigns to
C45), 345 is the LocalStack exemplar, 346 is Twin scaffolding**. So the 341–345/346 range sweeps in rows
that are *not* the three modes (one of which, contract-verification, C44 elsewhere explicitly hands to
C45). The precise per-mode citation is already given correctly in §1's responsibilities list (L34:
"341–343") and §3, so this is cosmetic imprecision, not a mislabel.
**Fix (applied).** Tightened the two headline ranges to **341–343** for the three modes; where LocalStack
(345) is the referent the citation stays on 345. No substantive claim changes.

## Verdict

**accept-with-fixes.** C44 is a faithful, bar-compliant spec: the twin is the genuine principle-tied KEEP
(assembly + declared cloned-contract surface as a C17 tool node), the three modes are correctly framed as
off-the-shelf wiring with a custom-framework explicitly DROPPED, and — verified against the now-on-disk
C43/C45 specs — the fidelity verdict (G22→C45) and the isolation/enforcement teeth (G31→C43, D-13) do
**not** fall back into C44. The one material defect was a **stale "siblings not on disk yet" premise**
(RC44-01, major) that mis-stated reality and softened OQ-1; it is fixed in place. The three minor findings
(C43 routing-ownership omission, the I3→C45 reference seam, a loose citation range) are all fixed.
**No blockers; nothing architecturally significant deferred** — the seam *decisions* (G22→C45, G31→C43)
were already correct and are only strengthened by confirming them against the written siblings.
