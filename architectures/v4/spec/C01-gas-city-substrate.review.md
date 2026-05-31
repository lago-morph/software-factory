# Adversarial review — C01 Gas City Runtime Substrate (Tracks A + B, sweep 1)

Reviewer persona: Subsystem Adversary (Runtime Substrate)
Targets: spec/C01-gas-city-substrate.md, plan-faithful/C01-gas-city-substrate.md,
spec-optimized/C01-gas-city-substrate.md, plan-optimized/C01-gas-city-substrate.md

## Findings — Track A (faithful: attack fidelity/completeness)

### RC01-01 — minor — Dependency-direction claim is stated as fact but is contested (XC-1 class)
Claim: spec-A §2 lists C03 and C04 as **upstream (C01 depends on)**, calling them "load-order"
dependencies and asserting "C01 cannot be configured without C03's model."
Evidence: The inventory does list `C01 Depends on: C03, C04`, so the citation is faithful. BUT C03's own
inventory row lists `Depends on: C01`, and C07/C02 likewise depend on C01. This is a genuine
cycle in the canonical inventory (C01↔C03), exactly the XC-1 pattern flagged for C19↔C20. Track-A
fidelity requires *recording* the contradiction, not silently presenting one direction as settled.
Fix (APPLIED): added an `> [AMBIGUITY]` note in §2 flagging the C01↔C03 circular dependency and that
both rows are cited verbatim; resolution deferred to integrator. Keeps the faithful citation while not
asserting a non-existent canonical direction.

### RC01-02 — minor — "layer 3" claim under-cites and risks the G01 overload
Claim: spec-A §1 "Per AI-CONTEXT §2 it occupies **layer 3** of the convergent 'three-layer + persistence'
shape (the pipeline engine)."
Evidence: README Part 3 / v3 vocabulary number the three-layer architecture as (1) LLM client, (2) agent
loop, (3) pipeline engine — so "layer 3 = pipeline engine" is consistent with C07's pinned reading. But
the bare word "layer" is the G01 overload; using "layer 3" without disambiguation re-introduces exactly
the bug C07 exists to kill.
Fix (APPLIED): qualified to "the **three-layer-architecture** pipeline-engine tier (C07 'layer' sense 1,
G01)" so it pins the C07 canonical sense rather than the numbered principle-tier sense.

### RC01-03 — minor — INV-4 enumerates `[rigs]` but the canonical section name is `[[rig]]`
Claim: INV-4 and §4 list "`[rigs]`" among Phase-0 off sections.
Evidence: AI-CONTEXT §3.4's explicit-off list does say "rigs"; but §13.3 and C03's catalog use `[[rig]]`
(array-of-tables). Faithful enumeration should match the schema form the skeletons actually use.
Fix (DEFERRED): the source §3.4 literally writes "rigs"; whether it means the `[[rig]]` array form is a
G11-class "what does real `gc` use" question. Left as-is with the existing OQ; flagged here so C03 and C01
converge on one spelling at sweep 2.

## Findings — Track B (optimized: attack the design)

### RC01-04 — major — DELTA-01 (`RuntimeSubstrate` portability interface) is the central bet and is under-justified against its own OQ1
Claim: DELTA-01 reframes C01 as "a thin `RuntimeSubstrate` interface Gas City *implements*, so a
re-platform is a swap behind one contract," and AC-6 demands a stub implementation pass the same suite.
Evidence/reasoning: The spec's own OQ1 concedes the load-bearing risk — Gas City's extraction surface is
"~20 Go files for the runtime alone," and "a faithful-but-thin portability contract may be infeasible."
A portability interface that must wrap an idiosyncratic 20-file Go surface is not "thin"; building a stub
that passes a conformance suite rich enough to be meaningful (provider lifecycle, dispatch, reconciler
tick, event ordering, attribution) is itself a substantial reimplementation. The DELTA claims to "retire
the G11 single-point-of-failure bet" but in the realistic case it only *documents* the lock-in — which is
the fallback OQ1 already names. The delta as written over-promises: it presents an *exit* where the honest
artifact is *a measured lock-in cost*.
Fix (APPLIED): softened DELTA-01's header claim from "retires the G11 single-point-of-failure bet" to
"**bounds** the G11 bet (portability contract where feasible; otherwise a measured, documented lock-in —
see OQ1)"; this keeps the design intent while making the claim falsifiable rather than aspirational.

### RC01-05 — major — DELTA-05 (substrate-level bounded reconciliation) may double-own F52 with C18/C39
Claim: DELTA-05 lifts "bounded-iteration + escalation" into the *substrate* `Tick` contract; failure table
credits C01 with the F52 mitigation; OQ2 admits it's unknown whether Gas City already bounds iteration.
Evidence/reasoning: F52 / loop-closure numeric policy is assigned to C39 (and possibly C18) per inventory
and review-log XC-3 ("C20 provides boundable slots; numeric policy deferred to C39/C18"). C01 asserting it
owns the *guarantee that the loop terminates* while C18 owns "convergence gates" and C39 owns
"termination/escalation contract" creates three owners for one invariant. The split C01 draws ("C01 owns
termination, C18/C39 own the escalation *policy*") is defensible but is exactly the kind of hidden-coupling
the brief flags: if `max_iterations` lives in the substrate but the escalation routing lives in C39, a
change to the policy now touches two layers.
Fix (APPLIED): added an explicit seam note to DELTA-05 / §6 row F52: "**C01 owns only the mechanical
per-node iteration cap + `stuck` emission; the numeric policy (N, oscillation detection, L5 ship-auth) is
C39's (XC-3). C18 owns the convergence-gate semantics.**" This pins the boundary so the three-owner risk
is documented. Whether the cap *belongs* at the substrate at all is DEFERRED (OQ2 / C18 co-spec).

### RC01-06 — minor — DELTA-06 degraded-mode "replay from event bus reconstructs live molecules" assumes more than C23/C19 promise
Claim: §5/§6 DELTA-06: "supervised restart replays from the event bus + bead store to reconstruct live
molecules"; event-bus append is "the linearization point / durability boundary."
Evidence/reasoning: C23 is specced as append-only JSONL recording *actions*; reconstructing in-flight
*molecule* state (a bead-tree mid-execution) from an action log requires either event-sourcing
completeness (every state transition is in the log AND is replayable deterministically) or that the bead
store itself is the authority. The spec asserts the event bus is the linearization point but §4 also says
"bead/CXDB writes are downstream of that" — so a crash between event-append and bead-write leaves the bead
store behind the log, and replay must re-derive bead state. Whether Gas City's event log is replayable to
full molecule state is unverified (G11) and is a strong claim to make at the substrate contract level.
Fix (APPLIED): qualified to "replays committed events and **reconciles** against the bead store to
reconstruct the live molecule set, **to the completeness the event log guarantees** (verified by AC-7;
event-sourcing completeness is a G11 conformance question)." Removes the implicit guarantee that the log
alone is sufficient.

### RC01-07 — minor — Six deltas on a Track-B foundational substrate, all justified, but DELTA-04 duplicates C02's ownership statement
Claim: DELTA-04 "the substrate↔pack tool-node seam is a typed ABI owned by C02."
Evidence: This is correct and consistent with C02 (both tracks) and C17. It is not actually a *delta to v4*
— it is an ownership assignment that C02 already makes. Listing it as a C01 DELTA slightly inflates the
delta count and risks the two specs both claiming to "own the seam exists."
Fix (APPLIED): no wording change needed (C01 already says "C01 only guarantees the subprocess contract
exists; C02 owns the wire format" — which is the correct non-overlapping split). Noted for the integrator
that C01-DELTA-04 and C02-DELTA-01 are complementary, not conflicting.

## Cross-component notes
- **C01↔C03 circular dependency** (RC01-01): real cycle in the inventory; both specs present a direction.
  Integrator must rule. C01-B's "load-order not build-order" framing is the most useful reconciliation.
- **F52 three-owner risk** (RC01-05): C01-B / C18 / C39 must agree the iteration-cap vs escalation-policy
  split. Mirror to review-log XC-3.
- **Tool-node seam ownership** is clean across C01/C02/C17 (all three cede the wire format to C02). Good.

## Verdict
- **Track A: accept-with-fixes** — faithful and well-cited; the dependency-direction and "layer"/`[rigs]`
  fidelity nits are applied or flagged.
- **Track B: accept-with-fixes** — deltas are individually defensible and concretely forced, but DELTA-01
  and DELTA-06 over-claimed guarantees (now softened) and DELTA-05's F52 ownership needed an explicit seam.
  Core design (portability contract + conformance gate + bounded tick + degraded mode) is sound.
