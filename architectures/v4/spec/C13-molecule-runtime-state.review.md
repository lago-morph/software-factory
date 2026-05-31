# Adversarial review — C13 Molecule / runtime-state (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Workflow Engine (runtime-state layer)
Target: `spec/C13-molecule-runtime-state.md` + `plan-faithful/C13-molecule-runtime-state.md`
Charter: single canonical track. Track-A posture — attack **fidelity + completeness** (not the design),
**plus** the capability-for-principle bar (HANDOFF §2): flag any addition that *hardens* an existing Gas
City capability rather than adding NEW capability tied to a 12-principle. Gaps assigned: **none** (C13's
"Key gaps" inventory column is empty); focus = fidelity / completeness / the bar / cross-dependency
consistency. Binding decisions D-1..D-5 are settled (flag only violations — none found).

## Summary

C13 is an unusually faithful sweep-1 spec. Every v4 citation I spot-checked resolves **exactly**:
AI-CONTEXT §3.2 concepts 7/8/9 (Formula/Molecule, Dispatch routes bead/wisp, Per-tick reconciler bounded
convergence with gates), §3.3 vocab (molecule / wisp / convoy / order / wait), §16 cold-start steps with
`gc converge resume <bead_id>` **verbatim** (AI-CONTEXT:699), README:235 ("Survives across agent sessions /
Replaces flat scratchpads"), README:259 (self-heal chain), one-shot-specs:62–65 / :81 (the `$epic_id`/`$rfc_path`
parameterized exemplars + the loop / human-gate pipelines), F-MODE F26 ("chain length is a formula property,
visible and lintable"). Cross-dependency claims against C12, C19, C20, C05 are consistent: C19's "no control
loop" stance (C19 §5), C20's envelope `status` (C20 §4.1), C12's "C13 owns the running instance" (C12 §1) and
the §3.3 outbound contract, and the convoy/order-owned-elsewhere split (C40; C12 §3.3 G06 Reading A). All
fills are tagged `[FAITHFUL-FILL]`; G11 / C18 / C39 deferrals are correctly placed; **no D-1..D-5 violation**.

The attack surface is therefore narrow and is concentrated in a handful of **elaborations that edge toward
hardening native `gc` molecule mechanics** (the bar) plus minor citation / consistency nits. No blockers.

## Findings

### RC13-01 — major — Plan T6 / interface-milestone frames a "molecule lifecycle **state machine**" as a net-new C13 deliverable (BAR: "named FSM" hardening)
**Claim.** The plan (`plan-faithful` T6, §2 critical path, §4 milestone 5) names a deliverable **"Define the
molecule lifecycle state machine — instantiated → converging → paused/resumable → converged / failed-escalated"**
and calls it "the most contract-entangled piece." The spec (§4) carries the same four-state lifecycle.
**Evidence / reasoning.** The HANDOFF §2 bar and the ADVERSARY-BRIEF call out *"named FSM"* over native Gas
City molecule lifecycle as exactly the kind of hardening to flag — molecule instantiate/converge/resume
lifecycle is Gas City's, asserted "Native" but unverified (G11). The **spec** is careful: its §4
`[FAITHFUL-FILL]` states "v4 names ... no explicit molecule state machine. The four-state lifecycle above is
exactly what those three operations [instantiate / per-tick convergence / resume] imply ... No state is added
beyond what a cited v4 operation needs." That framing is defensible (it derives the states from cited ops, not
from taste). The **plan**, however, is more assertive than the spec it implements: presenting "author a state
machine" as a C13 work item reads as C13 *introducing* an FSM rather than *describing the minimal lifecycle the
cited `gc` operations already imply*, jointly with C18. The two artifacts are out of register — the spec
hedges, the plan hardens. **Fix (applied).** Reworded plan T6, the §2 critical-path line, the §4 milestone,
and §5 risk-2 to "minimal lifecycle the cited operations (instantiate / converge / resume) imply — **co-owned
with C18**, not a new FSM C13 introduces," matching the spec's §4 fill and keeping the work at "name the states
the operations require" altitude.

### RC13-02 — major — "binding-resolution failure surfaces at instantiation, **not as a half-built tree**" asserts a transactional/atomic instantiation property v4 never states (BAR: "transactional bind→seal" hardening; G11)
**Claim.** §6 (Malformed instantiation) + §4 (consistency) state C13 "will not silently create a node-bead
with an unresolved binding; binding-resolution failure surfaces at instantiation, **not as a half-built tree**."
**Evidence / reasoning.** The `[FAITHFUL-FILL]` tag covers the *validator floor* ("C12 guarantees resolvability;
C13 fails instantiation loudly if a binding/parameter is missing") — that floor is faithful and well-grounded
in C12 §3.3. But "**not as a half-built tree**" additionally asserts that instantiation is **atomic /
all-or-nothing** (no partially-materialized bead-tree on failure). v4 states no such atomicity, and whether
`gc`'s instantiate is transactional is precisely a Gas City internal under G11 (the same class as C19's open
crash/atomicity question, C19 OQ-C19-3, which C13 elsewhere correctly inherits). Asserting all-or-nothing
materialization is the "transactional bind→seal" hardening the bar warns against — and it is the *one* place
the spec's elaboration outruns its own fill tag. **Fix (applied).** Qualified the §6 row and the §4 consistency
bullet so the faithful floor is only "fail **loudly** on an unresolved binding (do not silently dispatch a
node-bead with no binding)"; the **atomicity** of instantiation (whether a failed instantiate leaves a
partial tree or rolls back) is tagged a `gc` internal under G11, deferred to sweep 2 — not asserted as a C13
guarantee.

### RC13-03 — minor — over-strong guarantee verbs for runtime behavior C13-the-state cannot unilaterally enforce
**Claim.** §6 (G18/F52): "C13 **guarantees** the loop cannot exceed the formula-declared bound silently."
§3.3 / §8: the molecule "guarantees" convergence detection and frontier correctness.
**Evidence / reasoning.** The spec's own thesis is that C13 is *state*, not a *loop* (§5: "C13 has no control
loop of its own — the loop that advances it is C18"). The *advance*, gate evaluation, and bound enforcement are
C18's; the bound *value* is C12's; the escalation *policy* is C39's. C13 holds the **counter / slots / topology**
that make the bound *enforceable* and convergence *computable*, but it cannot by itself *guarantee* a runtime
outcome — that conflates the subject with the controller and slightly overclaims (parallels the C20 §4.3
"slots here, policy in C39" discipline, which C13 cites approvingly but then exceeds in verb choice). **Fix
(applied).** Softened the load-bearing verbs: C13 "holds the iteration counter against C12's declared bound so
the bound is **enforceable** (C18/C39 enforce)" and "exposes a **deterministically computable** convergence/
frontier" rather than "guarantees" the runtime result. No scope removed — only the actor of the guarantee
corrected.

### RC13-04 — minor — Batch-placement tension: §2 claims Batch 2 "once C18 exists to drive it," but the inventory places C18 in Batch 3
**Claim.** §2: C13 "lands in **Batch 2** (core build flow, alongside C12/C05/C28) ... once **C18** (reconciler)
exists to drive it."
**Evidence / reasoning.** The canonical inventory (HANDOFF §1 / component-inventory batch table) places **C18
in Batch 3**, not Batch 2. So C13's stated precondition ("C18 exists to drive it") is not satisfiable within
C13's own batch — the live *driver* arrives a batch later. The spec is honest about C18's absence elsewhere
(OQ-C13-2; "C18 has no spec yet at sweep-1") and the plan §2 lists it as an external blocker, but the §2
narrative asserts the Batch-2 placement smoothly without noting the driver lag. This is a real cross-inventory
inconsistency a reader could trip on. **Fix (applied).** Added a clause to §2 noting C18 lands in **Batch 3**,
so sweep-1 can freeze the C13↔C18 contract but the live reconciler that *drives* the molecule follows in a
later batch (consistent with OQ-C13-2 and plan §2 external-blocker (a)).

### RC13-05 — minor — citation precision: §3.1 attributes "referenced by name at instantiation" to C12 §3.1; the verbatim phrasing is C12 §1
**Claim.** §3.1 table, Source-formula-reference row: cites *'C12 §3.1 "referenced by name at instantiation"'*.
**Evidence / reasoning.** The verbatim phrase "referenced **by name** at dispatch and at instantiation" lives in
C12 **§1** (line 32). C12 **§3.1** (row 92) supports the *substance* ("the name a formula is referenced by ...
at molecule instantiation") but not that exact wording. So the cite is a light paraphrase mis-attributed by one
section — substantively faithful, not a fabrication. **Fix (applied).** Re-pointed the cite to "C12 §3.1 row
(formula identity) / §1" so it lands on the supporting text.

### RC13-06 — minor — forward-references C18's (not-yet-authored) contract as if it states settled invariants
**Claim.** §6 (Concurrent advance): "single-writer-per-tick is the reconciler's invariant (C18)"; §3.3 / §4
attribute "tick cadence, frontier-advance, gate evaluation, tick serialization" to C18.
**Evidence / reasoning.** C18 has **no spec at sweep-1**; these are properties C13 *assumes* the reconciler will
provide, not invariants C18 has stated. The spec does hedge (OQ-C13-2 asks to "confirm C18's reconciler
contract") and §6 flags the concurrency item as OQ-C13-2, so this is honestly-scoped — but the in-line phrasing
reads as if C18 already guarantees single-writer-per-tick. Worth a light tag so it is not later mistaken for a
frozen C18 commitment. **Fix (applied).** Tagged the §6 concurrency row and the §3.3 reconciler bullet as
"**assumed pending the C18 contract** (OQ-C13-2)," so the forward-reference is explicit rather than asserted.

## Notes (no fix needed — correct as written)
- The **"frontier / ready set"** elaboration (§3.1 fill) is handled correctly: explicitly *derived* (deps all
  `done`), *no new stored field*, "the standard topological-readiness computation over the DAG the formula
  already defines." This is description, not a new mechanism — passes the bar.
- The **wisp = dispatch-view-of-a-runnable-node-bead** fill (§3.3) is *compatible* with C05 (which is
  deliberately agnostic — "routes bead/wisp," takes no contrary position) and is correctly routed to a joint
  OQ with C05 (OQ-C13-4). No contradiction.
- **"State on beads, no shadow store"** (§3.1 fill / §4 / AC-2) is the right minimal reading of "Molecule =
  instantiated **bead-tree**" + "memory layer survives across sessions" and avoids duplicating C19 — this is
  *de-scoping*, the opposite of hardening. Good.
- The **molecule⇄first-class-`gc`-object** question (OQ-C13-1/3) and the whole structure-is-`gc`'s posture are
  already correctly deferred to G11 / sweep-2; nothing to apply.

## Verdict
**accept-with-fixes.** Fidelity is excellent and sourcing is meticulous; the component itself is faithful
(inventory concept 7, P1/P3/P4/P12) and does not invent capability. All six findings are *qualify-an-elaboration*
fixes that move claims **toward** the faithful floor (soften an FSM framing, defer instantiation-atomicity to
G11, correct guarantee-actors, note the C18 batch lag, fix one citation, tag a C18 forward-reference) — none
remove genuine content or change the design. All six are **applied in place**. Nothing architecturally
significant is left deferred: the two bar-adjacent items (RC13-01 FSM framing, RC13-02 instantiation atomicity)
were resolved by *softening to the spec's own fill posture and to G11*, which is squarely within Track-A
authority; the residual structural unknowns (real `gc` molecule model, C18 contract, one-field `status`
reconciliation) were already the spec's open questions and remain correctly G11/sweep-2-gated.
