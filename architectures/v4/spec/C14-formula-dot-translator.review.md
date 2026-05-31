# Adversarial review — C14 Formula↔DOT Translator + Visualizer (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Workflow Engine (critic-fixer)
Target: `spec/C14-formula-dot-translator.md` + `plan-faithful/C14-formula-dot-translator.md`
Charter: canonical single track → attack FIDELITY and COMPLETENESS (not design), PLUS the
capability-for-principle bar (HANDOFF §2): flag any addition that hardens on existing stack
capability rather than delivering new principle-tied capability.

## The bar checks (dispatch-mandated)

- **WRAPS native `gc formula export --format dot`, does not reinvent DOT export — PASS.** §1, §3.1
  ([FAITHFUL-FILL]), §5, §8 AC-5, plan T1/T5 all frame export as "wrap `gc --format dot` where native,
  else emit via an off-the-shelf DOT writer," binding to *observable* output, never `gc` internals
  (OQ-1). Correctly cites README:385 ("Add `gc formula export … --format dot`") and README:384
  ("transfusion source: **any DOT writer/parser library**"). No second exporter is invented.
- **Off-the-shelf Graphviz/DOT ecosystem, no custom renderer/parser — PASS.** §1 NOT-list and §7 are
  explicit: "NOT graphviz / the renderer" (graphviz is off-the-shelf, README:143), "NOT a DOT
  writer/parser library" (README:384). C14 is the *semantic mapping + fidelity proof* layered on a
  library, not a re-implemented grammar.
- **Does NOT contain the Mammoth 21-rule linter (that is C15) — PASS.** §1 "NOT the DOT-ecosystem
  linter … the rules themselves … live in C15"; §2 names C15 the downstream consumer of the DOT
  surface. No linter logic leaks into C14.
- **The genuine KEEP (import direction + G24 fidelity proof) is correctly identified — PASS.** §1, §3.2,
  §3.3 name import + the round-trip property as C14's "irreducible custom surface" and "whole reason to
  be a spec'd component." This is the right principle-tied capability under the bar.

## Findings

### RC14-01 — major — C14↔C15 DOT-surface seam: the **loop/back-edge marker** C15 declares it needs is absent from C14's export-surface contract, and the two sides' interim handling of loops is contradictory (not merely deferred)
**Claim.** The C14→C15 DOT-surface contract is described **inconsistently on the two sides** for the
loop/iteration construct. C15 says the DOT it consumes must carry loop markers and that C14 must *emit*
loop-bearing DOT so C15 can lint loops; C14 says it will **reject / fail-loud** on loop constructs and
emit no loop-bearing DOT. Both correctly trace the root to C12:OQ-2, but the *seam contract itself* is
contradictory rather than reconciled, and C14's export-surface table omits the marker C15 names.
**Evidence.**
- C15 §9 OQ-2 (line 292): the load-bearing contract "C15 needs C14 to freeze" is whether the DOT export
  "carr[ies] the node-kind tag, **loop-construct markers**, and node ids C15's structural rules need."
- C15 §3.3 rule 1 (lines 131–133): C15 "flags a graph cycle that is *not* a sanctioned bounded-loop
  construct" — i.e. C15 must be able to **distinguish a sanctioned bounded loop from a raw back-edge in
  the DOT surface**, which requires C14 to emit the bounded loop *with a marker*, not omit/reject it.
  C15 AC-5 (line 269) likewise tests "a back-edge cycle (**not a bounded loop**)" as a positive finding —
  presupposing the DOT distinguishes the two.
- C14 §3.1 export mapping table (lines 81–88) enumerates node id / kind / binding / edge / gate /
  parameters — **no loop or back-edge marker row.** The loop appears only in §3.4 / §6 (line 194) /
  §9 OQ-2 (line 251) as a "**rejected** catalog entry," with export that "**fails loud** rather than
  emitting lossy DOT."
- Net contradiction: C15's loop-lint capability *requires* C14 to emit marked loop DOT; C14's stated
  posture is to refuse to emit any loop-bearing DOT. If taken literally and permanently, **C15 can never
  lint loops** — contradicting C15's own framing that loops "drive C15/C14" and the inventory line that
  C15 lints "a back-edge cycle."
**Why this is fidelity, not design.** The shared *root* (C12 hasn't frozen the loop primitive — C12:OQ-2)
is correctly identified by both specs; that part is sound. The defect is that C14 (a) does not name the
loop/back-edge **marker** as a first-class element of the C14→C15 **export surface** even though C15
explicitly enumerates it, and (b) conflates two different states — "C12 hasn't frozen the primitive yet"
(the real, temporary blocker) with "C14 will refuse to emit it" (a permanent capability removal that
breaks C15). Reconciling the seam description is a faithfulness fix, not a design change.
**Fix (applied).** In C14 §3.1, added a **loop / back-edge marker** row to the export mapping table,
named as the C14→C15 seam element (concrete DOT encoding deferred to C12:OQ-2, consistent with the rest
of the table being sweep-1 named-not-typed). In §3.4, reconciled the interim posture: distinguished
"C12 has not frozen the loop primitive (the blocker)" from C14's *target* of emitting a **marked**
back-edge so C15 can lint it — fail-loud is the **interim** behaviour *until* C12 freezes the primitive,
**not** C14's end-state; once frozen, C14 emits the marked construct (it does not stay a permanent
rejection). Cross-referenced C15 §9 OQ-2 explicitly as the consumer of this marker.

### RC14-02 — minor — `gc formula export` is cited as suggesting "export is, or will be, a `gc`-native subcommand," but README:133 marks the visualizer/exporter "**Custom**"; the two README signals are not both surfaced, leaving OQ-1 looking more settled toward "native" than the corpus supports
**Claim.** §3.1's [FAITHFUL-FILL] leans on README:385 ("Add `gc formula export … --format dot`") to argue
export is "**is, or will be**, a `gc`-native subcommand." But README:133 — the row C14's own Source header
quotes — labels the visualizer "**Custom: formula → DOT exporter + graphviz**," and README:384 says
"**Build** the formula↔DOT bidirectional translator." The corpus carries *both* a "native `gc` export"
signal (:385) and a "custom exporter" signal (:133/:384); the spec foregrounds the native reading and
relegates the custom reading, which slightly overstates how settled OQ-1 is.
**Evidence.** README:133 "Custom: formula → DOT exporter"; README:384 "Build the formula↔DOT bidirectional
translator as a small Go tool"; vs README:385 "Add `gc formula export <name> --format dot`." The OQ-1
framing ("native wrapper preferred — don't reinvent") is the right *default under the bar*, but the
evidence is genuinely split, not merely "unverified whether :385 is native."
**Why minor.** The spec's operational conclusion is already correct and conservative (bind to observable
output if present, else emit via off-the-shelf writer — never reinvent a *native* exporter, never bind to
invented internals). Only the *characterization of the evidence* is lopsided. No wrong artifact results.
**Fix (applied).** Added the README:133 "Custom" / README:384 "Build" counter-signal to the §3.1
[FAITHFUL-FILL] and to OQ-1, so the open question reads as genuinely two-sided (corpus says both "Add a
`gc` subcommand" and "Custom/Build a tool"), with the bar's "wrap-not-reinvent" default unchanged.

### RC14-03 — minor — §1 cites README:392 P3-delivered as "full, including visualization" to ground C14's existence, but README:392 also marks the *linter* "(optionally)"; fine for C14, but the visualization-is-full claim should not be read as making the **translator/import** a delivered Phase-1 guarantee
**Claim.** §1 says C14 exists "to render a formula for human review (… P3 delivered 'full, including
visualization', README:392)." README:392 reads "P3 … full, including visualization **and (optionally)**
Mammoth-derived 21-rule linter." The "full … visualization" phrase backs the **export/visualize** half;
it does **not** assert the **bidirectional translator/import** is a Phase-1 *delivered* guarantee (the
translator is the "small side project," README:538, "doesn't have to be perfect"). The spec mostly keeps
this straight but §1's phrasing could be read as elevating import to "delivered-full."
**Evidence.** README:392 ties "full" to visualization; README:538 frames the *bidirectional* capability
as the enabler of linting and explicitly hedges it ("doesn't have to be perfect"). C14's load-bearing
obligation (G24 round-trip) is correctly the *trailing* work in the plan (plan §4 "import + fidelity is
the trailing, load-bearing work"), so the spec's own plan already treats import as not-yet-guaranteed.
**Why minor.** Internally the spec is consistent (import/fidelity is trailing everywhere else); this is a
one-phrase emphasis risk in §1, not a substantive misattribution.
**Fix (applied).** Tightened §1 so "full, including visualization (README:392)" is scoped to the
*export/visualize* half, and the bidirectional/import half is explicitly the "small side project"
(README:538) whose guarantee is the G24 proof — not a Phase-1 completeness claim.

### RC14-04 — minor — D-7 conformance is correct, but §3.1 hard-codes the node-kind **set** inline (`{agent, tool, gate, sub_formula}`) in several places; faithful, yet one spot risks reading as C14 *asserting* the set rather than *referencing* C12's
**Claim.** The spec is D-7-conformant in intent everywhere (§1, §2, §3.1 all say the set is "C12's (D-7),"
"named by C12," "must never redefine it"). But the set literal is repeated inline (§1, §2 table, §3.1
table row, §8 AC-7). Repetition is not a violation — D-7 only forbids *redefining* — and C12 itself lists
the set inline too. The one residual risk: §8 AC-7 phrases it as "C14 never introduces a kind value
outside C12's set," which is the correct test, but the inline literal could drift from C12 if C12's
sweep-2 `gc`-grounding changes the set.
**Evidence.** D-7 (review-log line 34): set is "named by C12 … C02 references … does not redefine."
C12 §3.1 itself flags the set + on-disk field home as a [FAITHFUL-FILL] pending real `gc` grammar
(G11/sweep-2) — so the *literal* is not yet frozen even in C12.
**Why minor / mostly accept.** This is a faithfulness *robustness* note, not a violation; the spec
correctly defers authority to C12 and never claims ownership.
**Fix (applied).** Added a single parenthetical at the §3.1 kind row noting the set literal is
**reproduced from C12 (D-7) and is itself a C12 sweep-2/G11 [FAITHFUL-FILL]** — so any change tracks C12,
and no reader mistakes C14's inline copy for an independent definition.

### RC14-05 — minor — completeness: the spec covers F26/F53 but does not state that C14 **closes no F-mode on its own** (it is an enabler), unlike the C15 sibling which says so explicitly
**Claim.** §6 maps F26 and F53 and correctly says "the rule that flags … is C15's" / "the check is C15."
But it never states the summary fact — C14 *closes* no failure mode by itself; it is an **enabler** of
the F26/F53 mitigations C15 owns. The C15 sibling spec states exactly this ("There is no F-mode C15
*closes* on its own — it is an enforcement mechanism …"), and the symmetry aids the integrator.
**Evidence.** §6 rows already attribute the actual mitigation to C15 in every case; the missing piece is
the one-line "enabler, not owner" summary the C15 doc carries.
**Why minor.** Purely a completeness/clarity parallelism with the sibling; no fidelity error.
**Fix (applied).** Added a one-line closing note to §6: C14 owns **no** F-mode mitigation outright; it is
the fidelity/visibility **enabler** for the F26/F53 controls C15 owns — its sole duty is that the DOT is a
faithful image so C15's findings concern the real workflow.

## Deferred (architecturally significant — needs human/orchestrator decision)

- **DEFERRED-A — the loop/back-edge DOT encoding itself (RC14-01's resolution).** Naming the marker in
  the seam contract is applied; *which* DOT encoding represents a sanctioned bounded loop (a marked
  back-edge attribute? a synthetic loop-controller node?) is **blocked on C12:OQ-2** (C12 has not frozen
  the iteration primitive) and is a joint C12/C14/C15 freeze. C14 cannot and must not invent it. Left as
  C14 OQ-2; flagged here so the integrator sequences the C12 loop-primitive decision before C14/C15
  sweep-2, since it is the single contract gating C15's loop-linting.

## Verdict
**accept-with-fixes.** A strong, faithful, well-traced spec+plan: the bar is cleanly satisfied (wraps
native export, off-the-shelf DOT lib + graphviz, linter correctly in C15), G24 is converted from an
assertion into a CI-enforced property with a canonical form + exclusion catalog (the genuine KEEP), and
D-7 is referenced not redefined. The one substantive issue (RC14-01) is a real C14↔C15 **seam fidelity
mismatch** on the loop/back-edge marker — C14's export-surface contract omitted the marker C15 declares
it needs, and the interim loop handling was contradictory across the two specs; both are reconciled in
C14's three files. The remaining fixes qualify lopsided citations and add sibling-parallel completeness
notes. The only architecturally-significant item — the concrete loop DOT encoding — is correctly blocked
on C12:OQ-2 and deferred. No blockers.
