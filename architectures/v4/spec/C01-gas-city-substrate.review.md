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

---

# Sweep-2 Adversarial Review — C01 + Gas City Conformance Check
Reviewer: Subsystem Adversary (Runtime Substrate), 2026-06-01
Targets: `spec/C01-gas-city-substrate.md`, `plan-faithful/C01-gas-city-substrate.md`,
         `architectures/v4/_meta/gascity-conformance-check.md`

## Findings

### RC01-S2-01 — minor — C01 install/pin contract is concrete and correct; no fidelity gap

**Claim (spec §3.1):** Go 1.26.3, `gc` binary from `lago-morph/gascity-prototype@b14c278`, upstream
SDK `gastownhall/gascity@183897e`, controller invocation `gc start --foreground`, companion binary `bd`.
**Evidence:** All values match the config anchor §1 table verbatim; the "go.mod is authoritative"
caveat is faithfully preserved; the binary name `gc` → `/usr/local/bin/gc` via `make install` is
grounded in PLAN.md. No invented values; no over-assertion of Go 1.26.3 as hard-coded (the hedge is
present). The Phase-0 config (~30 lines TOML) matches AI-CONTEXT §13.1.
**Verdict:** no fix needed — the install/pin contract is as concrete and correct as the source allows.

### RC01-S2-02 — **blocker** — Conformance check Outcome Routing table missing the `A1 DETECT-ONLY` row; no composite A1+A2 decision rule; C01 §8.1 shorthand is unsafe

**Claim (conformance check §Outcome Routing, C01 spec §8.1):** "Test A PREVENT → D-30 watcher not
needed" and the Outcome Routing table provides per-sub-test rows for A1-PREVENT, A2-PREVENT,
A2-SILENT.
**Problem:** Three gaps make the composite verdict ambiguous:
1. **Missing `A1 DETECT-ONLY` row** in the Outcome Routing table. If A1 is DETECT-ONLY (bead layer
   fails) the operator has no explicit routing row — only the inline A1 implication table inside
   Test A1 covers it, and that table is disconnected from the Outcome Routing table that downstream
   spec authors read.
2. **No composite decision rule.** The A1 and A2 sub-tests can produce conflicting signals (A1=PREVENT,
   A2=SILENT is the most dangerous: the bead layer enforces but the OS layer leaks silently). The
   Outcome Routing table has an A2-SILENT row but no rule that says "A1=PREVENT + A2=SILENT = overall
   SILENT, NOT overall PREVENT." Without this rule, an operator reading only C01 §8.1 ("Test A PREVENT
   → watcher not needed") could conclude — falsely — that the watcher is not needed when A1=PREVENT but
   A2=SILENT.
3. **C01 §8.1 shorthand is unsafe:** "Test A PREVENT → D-30 watcher not needed" is true only when
   BOTH A1 AND A2 = PREVENT. The shorthand as written admits the A1=PREVENT + A2=SILENT mis-read.
**Evidence:** Outcome Routing table rows 711–713 (as originally numbered); C01 spec §8.1 routing
bullets. The A1 implication table (lines 218–220) correctly states "D-30 watcher MUST be built" for
DETECT-ONLY and SILENT but this is local to Test A1's section; the routing table that summarizes the
full battery does not carry this row.
**Fix (APPLIED):**
- Conformance check Outcome Routing table: added `A1 DETECT-ONLY` row and `A1=PREVENT + A2=SILENT`
  composite row; added a COMPOSITE VERDICT RULE block above the table making the worst-case-combination
  rule explicit.
- C01 spec §8.1: expanded the routing bullets to (a) clarify "overall PREVENT = A1 AND A2 = PREVENT",
  (b) call out A1=PREVENT + A2=SILENT as overall SILENT explicitly, (c) preserve the existing
  DETECT-ONLY / SILENT bullets with "any layer" clarification.
**Severity: blocker** — without this fix, the conformance check procedure could be followed correctly
and the operator could still draw the wrong watcher-needed conclusion.

### RC01-S2-03 — minor — C01 spec missing the standard `[D-30 ADOPTED …]` inline annotation block

**Claim:** Sweep-2 convention (AGENTS.md / SWEEP2-DISPATCH.md) requires `[D-30 ADOPTED …]` inline
annotations in component specs that touch the prevent-gate surface, matching the format applied to
C34/C43/C42/C56/C57.
**Evidence:** C01's header lists `D-30` in the "Binding decisions obeyed" line but the standard
`**[D-30 ADOPTED — operator, 2026-06-01]**` block with verbatim decision text is absent from the
body (§7 Security section), while C34/C43 carry it. The D-30 verbatim quote in §8.1 is present but
uses blockquote format, not the `[D-30 ADOPTED …]` annotation format the spine uses for propagation
tracking.
**Fix (APPLIED):** Added a `[D-30 ADOPTED …]` inline annotation block in C01 §7 Security section
with verbatim decision text and the P2/P3b human-in-the-loop gate statement.

### RC01-S2-04 — minor — C01 correctly treats itself as the dependency ROOT; cycle resolution is sound

**Claim (spec §2):** C01↔C03 and C01↔C04 cycles are broken by treating C01 as root and freezing
an interface contract that C03/C04 build against.
**Evidence:** The spec explicitly flags both cycles, cites both inventory rows verbatim (not silently
resolving to one direction), and uses the M1 interface-freeze pattern — the same approach applied to
C19↔C20. The plan §2 confirms "C01's T1/T2 install proceeds independently; C03/C04 build against
the C01 seam contract." This is the correct faithful treatment.
**Verdict:** no fix needed — the cycle resolution is correctly stated. The prior Sweep-1 ambiguity
flag (RC01-01) was applied; this confirms it holds at Sweep-2 depth.

### RC01-S2-05 — minor — The 6 G11 flag uncertainties in the conformance check are honestly marked and non-fatal to the procedure

**Claim (conformance check §Protocol Ambiguities, items 1–6):** Six items are flagged as
unrunnable-or-uncertain: `bd create --prefix r2` flag existence, `gc events --since` syntax, `gc
session list --json` flag, dolt SQL direct access for Test E, tmux pane title format for Test G, and
reconciler tick interval for Test G.
**Evidence:** Each item provides a concrete fallback or observation instruction. None of the six
makes a test UNRUNNABLE — they degrade to a different observation method, not to "cannot be answered."
Test A's core probes (A1a `bd get r2-TARGET`, A1b `bd get gp-TARGET`, A2a `cat ../rig2/README.md`)
do not depend on any of the six uncertain items; the keystone test is not blocked by them. The items
are correctly listed in the Orchestrator section, not inline in the test procedure in a way that would
cause misreads.
**Verdict:** no fix needed — the uncertainty flags are honest and appropriately scoped.

### RC01-S2-06 — minor — D-23 and D-30 verbatim citations in C01 spec and conformance check are accurate

**Claim (C01 spec §8.1 blockquotes; conformance check Test A D-30 blockquote).**
**Evidence:** D-23 verbatim from review-log: "do NOT bind holdout-integrity (C34) or the fence (C43)
to either 'prevent' or 'detect' until a focused Gas City reality-check spike verifies what a real
`gc` actually enforces at tool-call/config-load time. This spike is the first move of the next pass
(Sweep-2) and the highest-leverage de-risking action (it underwrites every 'Gas City does X natively'
claim)." — C01 §8.1 matches this verbatim ✓
D-30 verbatim from review-log: "unattended operation (P2) and self-modification (P3b) require the
substrate to BLOCK (prevent at the tool-call/process boundary) — not merely detect — out-of-boundary
access on the relevant blast-radius face." — Conformance check Test A blockquote and C01 §8.1 match ✓
**Verdict:** citations are accurate. No drift from review-log.

### RC01-S2-07 — minor — AC-C01-2 condition ("all tests PASS") should be "all tests have recorded outcomes"

**Claim (AC-C01-2, spec §8.1):** "when the full conformance check battery (Tests A–G) runs; then all
tests PASS and outcomes are recorded."
**Problem:** Several tests (particularly A, B, C, D) can FAIL and still close their OQ and route
their architectural consequence correctly. A FAIL on Test A is the scenario that triggers the watcher
design path — this is a valid, expected, and architecturally important outcome. Requiring "all tests
PASS" for AC-C01-2 to be satisfied makes the conformance check look like it can only succeed if Gas
City is perfect, which is not the intent. The real criterion is: outcomes are recorded and routed.
**Fix (APPLIED — minor reword in AC-C01-2):** Changed AC-C01-2 "then/then" text to "all tests have
been run and their outcomes (PASS or FAIL) are recorded in the Results Record; Test A outcome has
been routed per the D-30 composite verdict rule." The existing cross-ref to E-C01-07 and E-C01-09
is preserved.

### RC01-S2-08 — minor — Plan T3 prereq cites "C04 (tmux provider)" but C04 is not a build prereq for standing up a tmux session

**Claim (plan-faithful §1, T3):** "Prereqs: T2, C04 (tmux provider — F7), C28"
**Evidence:** The tmux provider is a Gas City native built into `gc` itself (F7 says "Phase-0
Provider-kind = tmux"); C04 is the v4 SPEC that documents the session model, not a component that
must be built before `gc start` can use tmux. Listing C04 as a T3 prereq implies a build dependency
that does not exist — it conflates "C04's spec describes this" with "C04 must be implemented first."
**Fix (APPLIED):** Changed T3 prereq from "C04 (tmux provider — F7), C28" to "C28 (the `claude`
binary, pre-staged)" with a note: "C04 is the owning spec for the session model but does not need to
be built before `gc start` uses the native tmux provider (F7)."

## E↔AC integrity check

The E-code → AC-code cross-reference table in the plan (§6) is complete and correct:
- E-C01-06 (misplaced config key) maps to AC-C01-5 and AC-C01-7 ✓ (AC-C01-7 exercises the
  rejection path, cross-refs E-C01-06 ✓)
- E-C01-09 (prevent-vs-detect unknown) maps to AC-C01-8 ✓ (AC-C01-8 asserts the outcome is
  recorded and routed)
- E-C01-10 (DOLT_REF mismatch) maps to AC-C01-2 ✓ (the conformance check's Test C exercises
  container-restart durability where the mismatch would surface)
No orphan E-codes or AC-codes found.

## Self-check (tool output)

```
grep -c "E-C01-" spec/C01-gas-city-substrate.md        → 17  (≥1 ✓)
grep -c "AC-C01-" spec/C01-gas-city-substrate.md       → 14  (≥1 ✓)
grep -cE "stateDiagram-v2|sequenceDiagram" spec/C01-*  → 2   (≥1 ✓)
grep -c "R/W-by" spec/C01-gas-city-substrate.md        → 2   (≥1 ✓)
grep -c "OQ-\|D-30 ADOPTED\|D-23 substrate-verified"   → 6   (OQs + both annotations present ✓)
```

## Sweep-2 Verdict

**accept-with-fixes** — the C01 spec and plan are implementation-ready at Sweep-2 depth; the install/
pin contract is concrete, the cycle resolution is sound, the D-23/D-30 citations are verbatim-accurate,
and the E↔AC cross-references are complete. Three fixes applied in place: (1) RC01-S2-02 conformance
check routing table + C01 §8.1 composite-verdict rule (blocker — prevents a false watcher-not-needed
conclusion when A1=PREVENT + A2=SILENT); (2) RC01-S2-03 [D-30 ADOPTED] inline annotation; (3) RC01-S2-07
AC-C01-2 PASS condition reworded. One plan fix applied: RC01-S2-08 T3 prereq clarified. No items
deferred to orchestrator ledger.
