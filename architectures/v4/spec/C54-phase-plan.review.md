# Adversarial review — C54 Phase delivery plan (canonical track, sweep 1)

Reviewer persona: Bootstrap-subsystem Adversary — phase sequencing & security-honesty
Target: [`spec/C54-phase-plan.md`](./C54-phase-plan.md) + [`plan-faithful/C54-phase-plan.md`](../plan-faithful/C54-phase-plan.md)
Charter: canonical track → attack FIDELITY and COMPLETENESS only (not the design), PLUS THE BAR
(verify C54 stays a sequencing *plan*, not a PM/scheduling/phase-execution engine).

## Summary posture

C54 is an unusually well-cited, faithful spec. Every README Part 6/7/8 line citation I spot-checked
(342, 350, 355, 367–372, 374, 378, 399, 417, 419, 429–436, 442, 446, 454, 457, 466, 468, 470, 496,
498, 499, 511, 512, 519, 542) verifies **exactly**; AI-CONTEXT (122, 135, 244, 294, 463) verifies;
the F-MODE-COVERAGE "Addressed" markings the spec attacks (F12/F44/F56 via twins, line 54/56/57; the
Phase-3 "overlap" row, line 135) verify; the C52 and C53 specs are mutually consistent with C54 on
gate/ordering ownership; the Phase↔Layer↔Batch cross-walk is faithful to the inventory's Batch scheme
(L107–115). The "stale C52 not on disk" hazard does **not** apply — `spec/C52-self-bootstrap.md` and
`plan-faithful/C52-self-bootstrap.md` are both on disk and C54's reference is live. All four assigned
gaps (G01/G02/G03/G31) are genuinely dispositioned. THE BAR holds: the artifact is a plan + a static
consistency linter (T7), with no scheduler/PM-engine/cost-model/phase-runner. Findings are precision
and completeness, not architecture.

## Findings

### RC54-01 — minor — §4.4 overstates that Part 6 contains no competing "layer" vocabulary
**Claim.** §4.4 Reading A asserts *"Part 6 only ever pairs 'Layer 2' with '(scenarios + judge)'"* and the
faithful-pick paragraph asserts *"the only 'Layer' token that appears in Part 6 is 'Layer 2 (scenarios +
judge)' in the P2 heading (README:417)."* **Evidence.** README Part 6 line **368** reads
"**P2** (three-layer architecture): Claude Code as agent + LLM client, Gas City as pipeline engine, beads
as persistence" — i.e. the *competing* "three-layer" vocabulary (the very vocabulary G01 is about) **does
appear inside Part 6**, as principle P2's name; Part 6 also uses the word "layer" incidentally at 372/393
("memory layer") and 470 ("highest-risk layer"). The narrower, true statement is that every **numbered
`Layer N`** token in Part 6 (lines 348 and 417) is paired with "(scenarios + judge)". The current absolute
phrasing slightly understates how far the G01 ambiguity reaches into C54's own source section. The
substantive pick (within C54, the numbered "Layer 2" = scenarios+judge) is correct and survives.
**Fix (applied).** Qualified both sentences to "the only **numbered** `Layer N` token", noted that Part 6
also carries "three-layer architecture" at README:368 (the competing vocabulary, as principle P2's name)
plus incidental "memory layer"/"highest-risk layer", and that this is *why* the cross-walk + scheme-guard
are needed even within C54.

### RC54-02 — major — C54 is silent on the class-level transfusion-failure (G14) hedge that two sibling specs explicitly route to it
**Claim.** C52 and C51 both assign C54 a sequencing decision C54 never acknowledges. **Evidence.**
[`spec/C52-self-bootstrap.md`](./C52-self-bootstrap.md) **OQ5** states verbatim: *"the strategic fallback
for 'a whole high-value class (Healer/twins/self-opt) cannot be reliably transfused' — re-sequence phases?
hand-build? — is a **C54 phase-plan decision** (C51:OQ-C51-2)… Confirm C54 owns the class-level hedge so
G14 is fully homed across C51/C52/C54."* G14 (ambiguities-and-gaps) is exactly this: *"~half the principles
(P7, P8, P11, P12) have no delivery path… The plan has no fallback for 'factory cannot reliably transfuse.'"*
Those principles are precisely C54's P3a/P3b/P3c/P3d payload, so the "what if a whole P3 sub-phase's
transfusion bet fails" hedge is structurally a **phase-plan** question. C54's spec mentions transfusion
(C51) only as a per-piece discipline and never addresses the class-level failure of a P3 sub-phase. This
is a genuine completeness gap created by sibling components pointing at C54. **Note on scope:** G14 is
**not** one of C54's four assigned gaps (G01/G02/G03/G31), so silently importing it as new C54 scope would
itself be a Track-A violation. **Fix:** DEFERRED — added **OQ-5** to the spec recording the inbound
C52:OQ5 / C51:OQ-C51-2 obligation and flagging the ownership question (does C54 own a class-level
transfusion-failure hedge, e.g. "a failed P3-subphase bet defers/re-sequences that sub-phase rather than
hand-building," or does that hedge live with C51/C52?). The orchestrator should home G14 explicitly across
C51/C52/C54; I did not invent a hedge mechanism inside C54.

### RC54-03 — minor — §6.1 over-attributes C43's "boundary typing" framing to README Part 6
**Claim.** §6.1 says deterministic boundary typing / the lethal-trifecta boundary (C43) "is *named as a P4
capability* ('deterministic-first')." **Evidence.** README:370 names P4 as *"deterministic-first:
reconciler + tool-node primitives available"* — it does **not** use the terms "boundary typing,"
"lethal-trifecta," "CaMeL," or name C43 anywhere in Part 6 prose (grep of README for those terms returns no
Part-6 hit). The *lethal-trifecta boundary-typing* framing is **F-MODE-COVERAGE's** (line 54: "boundary
typing (CaMeL pattern)"), not README Part 6's. The spec's load-bearing honest point — *"no phase is ever
stated for C43's actual build"* — is correct and is the right call; only the "named as a P4 capability"
attribution is loose. **Fix (applied).** Re-attributed precisely: README:370's P4 is "deterministic-first
= reconciler + tool-node primitives"; the *lethal-trifecta boundary-typing* reading of C43 comes from
F-MODE-COVERAGE (CaMeL pattern) and v4 still states **no phase for C43's build** — which is exactly the G31
hole C54 surfaces. Aligned the wording with binding decision **D-13** (C43 owns the Bash/net/fs blast-radius
bound + twin isolation; C42 provides the partition; C34 enforces holdout) so the C43 scope statement
matches the ledger.

### RC54-04 — minor (verification, no change) — cross-walk Batch column is faithful; the P3a↔Batch-3 surprise is intended, not an error
**Claim/Evidence.** The §4.4 cross-walk maps P3a→Batch 3, i.e. a *Phase-3* (post-bootstrap-gate)
deliverable is authored in the *same* Batch as the pre-gate P2 work. I checked this against inventory
L111/L113/L115: C35 (P8/P3a) is indeed Batch 3; C36–C39 (P11/P3b) and C43/C44/C45 (P3b/P3c) are Batch 4;
C46–C50 (P12/P3d) are Batch 5. The mapping is correct, and the apparent oddity (a P3 deliverable authored
in Batch 3) is *precisely the orthogonality the spec is asserting* — Batch is an authoring fan-out order,
Phase is a delivery/gating order. **No fix.** This is a positive confirmation, not a defect; the spec's
"three different '2's" note (L115) already covers the headline non-alignment. (Optional polish, not
applied: the spec could add one clause noting Batch authoring may *precede* a deliverable's Phase gate, so
a reader doesn't misread Batch 3 ⊇ {P2, P3a} as a gate violation — left for the author, the orthogonality
is already stated.)

### RC54-05 — OQ-3 / G31 — the C43 pull-forward question (the orchestrator's morning-review item)
**Claim.** The spec keeps C43 at P3c (Reading A) + a mandatory Caution, and flags pulling it forward as
OQ-3. I am asked to render a view; this is architecturally significant and must NOT be silently
re-sequenced. **Evidence + my view (see "Reviewer view on OQ-3" below).** The spec's faithful disposition
is correct as *faithful* output. My engineering recommendation refines (does not overturn) it: **C43 is two
mechanisms, and they should not share one phase.** Per inventory, C43 `Depends on: C42, C44`; its
*twin-isolation* half is structurally blocked on C44 (twins, genuinely P3c) and legitimately stays at P3c.
But its *deterministic-boundary-typing / blast-radius* half (the Bash/net/fs capability bound — D-13's
"Bash/net/fs typing") depends only on C42 (role partition, Batch 2) + the P4 reconciler/tool-node
primitives (available P0), **not** on twins. The XC-8 exposure window the spec correctly surfaces
(P0–P3b: the factory runs Claude Code with Bash/net/fs and *self-modifies at P3b* with no enforced
boundary) argues that the **boundary-typing half is a precondition for safe unattended P2 operation and for
P3b self-modification**, not a P3c nicety. **Fix:** DEFERRED — left the faithful manifest (C43 at P3c +
Caution) intact per the canonical-track rule against silently re-sequencing a security control, and
sharpened OQ-3 to record the *split* recommendation (boundary-typing → pull forward to a P2 entry
precondition; twin-isolation → stays P3c, blocked on C44) rather than a wholesale pull-forward. This is the
orchestrator's call and aligns with XC-8 ("sequence C43 earlier **or** accept detection-only Phase 0") and
D-13.

## Reviewer view on OQ-3 (C43 pull-forward) — for the morning review

**Pull the *blast-radius-bounding* half of C43 forward to P2; keep the *twin-isolation* half at P3c.**
Rationale: (1) C43 bundles two separable mechanisms — deterministic boundary typing (Bash/net/fs
capability bound) and twin isolation. (2) Only the twin half depends on C44 (twins), which is genuinely
P3c; the boundary-typing half depends only on C42 (Batch 2) + P4 primitives (P0), so it is **not**
structurally blocked from landing at P1/P2. (3) The factory scales unattended at P2 and *self-modifies* at
P3b — both **before** P3c — so running those windows with zero enforced blast-radius bound (only
detection, per XC-8) is the real XC-8/F12/F44/F56 hazard, and a blast-radius bound is a *precondition* for
safe unattended scale, not a late hardening. (4) D-13 already scopes "Bash/net/fs typing" to C43 distinctly
from twin isolation, so the split is consistent with the ledger. Net: the faithful manifest is right to keep
C43-twins at P3c, but the boundary-typing bound should become a **P2 entry precondition** (or v4 must
explicitly "accept detection-only Phase 0" per XC-8). This is the single most consequential sequencing
decision in the plan and remains the integrator's call — flagged, not applied.

## Verdict

**accept-with-fixes.** Faithful, exhaustively and accurately cited, and correctly self-disciplined to stay
a plan (THE BAR holds — no scheduler/PM-engine/cost-model/phase-runner). All four assigned gaps
(G01/G02/G03/G31) are genuinely dispositioned; G03's "6 of 12" double-count correction (→ 5 native +
P3-basic) is well-grounded in README:369 vs AI-CONTEXT:135/463. Applied fixes are precision qualifications
(RC54-01 "only numbered Layer token"; RC54-03 P4/boundary-typing attribution + D-13 alignment) plus a
sharpened OQ-3 recording the C43 *split* recommendation. Two items deferred to the orchestrator, both
architecturally significant: the **C43 pull-forward** (RC54-05/OQ-3, my view: split — boundary-typing → P2,
twins → P3c) and the **class-level transfusion-failure (G14) hedge ownership** (RC54-02/OQ-5, routed to
C54 by C52:OQ5 + C51:OQ-C51-2 but G14 is outside C54's assigned-gap set, so not silently imported). No
fidelity blockers.
