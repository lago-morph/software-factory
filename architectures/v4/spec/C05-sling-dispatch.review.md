# Adversarial review — C05 Sling / dispatch (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Runtime Substrate
Target: spec/C05-sling-dispatch.md + plan-faithful/C05-sling-dispatch.md
Charter: single canonical track. Track-A posture → attack FIDELITY + COMPLETENESS (not the design),
PLUS the capability-for-principle bar ([`HANDOFF.md`](../_meta/HANDOFF.md) §2 / [`SURVIVOR-PASS.md`](../_meta/SURVIVOR-PASS.md)):
flag any addition that HARDENS Gas City's native sling/dispatch instead of adding new capability tied to a
12-principle. Gas City sling is NATIVE — routing, back-pressure, pools, fairness, convoys are Gas City's
(SURVIVOR-PASS C05: all 6 optimized deltas DROP).

## Findings

### RC05-01 — major — "reconciler invokes/triggers dispatch" is the spec's load-bearing inbound interface but is an INFERENCE, cited as if it were a v4 fact (AI-CONTEXT:93)
**Claim.** §2 ("C18 reconciler … decides desired-vs-actual state and triggers (re)dispatch; C05 is the
dispatch action it invokes"), §3.1 Dispatch-request interface, §5 Trigger note, §6 F22, AC-6, and plan
T1/T7 all rest on "the per-tick reconciler (AI-CONTEXT:93) … invokes dispatch." **Evidence.** AI-CONTEXT:93
states only: "Health Patrol (Controller + Convergence) | Per-tick reconciler; bounded convergence with
gates | P4, P11 (partial), P8 (weak)". README:159 says the reconciler does "Desired-state convergence."
**Neither v4 source says the reconciler invokes, triggers, or drives sling/dispatch** — grepping the two
source docs, the reconciler and sling never co-occur in a causal statement. v4 names *what triggers sling*
nowhere. The reconciler-drives-dispatch coupling is a reasonable structural inference (a convergence loop
that finds desired≠actual plausibly issues dispatch), but it is a `[FAITHFUL-FILL]`, not the sourced fact
the inline "(AI-CONTEXT:93)" citation implies. This is the same class of issue the C23 review flagged
(asserting an inferred property as a v4 fact). It is load-bearing: it is C05's *entire* inbound trigger and
the F22 recovery story. **Fix (applied).** Added a `[FAITHFUL-FILL]` note at §2 / §3.1 marking the
reconciler→dispatch trigger relationship as an inference (v4 states the reconciler does desired-state
convergence but never names what triggers sling), and softened the inline citations so "AI-CONTEXT:93" is
read as backing "a per-tick reconciler exists," not "the reconciler invokes dispatch." The structural choice
itself is sound and kept (it is the only convergence mechanism v4 names).

### RC05-02 — major — the dispatch-record contract HARDENS native attribution/event-bus capability — flagged DROP for the identical optimized delta (SURVIVOR-PASS C05 DELTA-06)
**Claim.** §3.2 "Dispatch-record contract (C05 → work-graph / attribution)", the §4 "Dispatch record" row,
INV-4's second sentence ("the only state C05 contributes is the dispatch record"), §7 Observability ("C05
emits a dispatch event per routing decision"), plan T6, and AC-7 elevate "C05 records/emits a dispatch
record" to a named contract + invariant + acceptance criterion + build task. **Evidence.** SURVIVOR-PASS C05
DELTA-06 ("Dispatch record schema") → **DROP**, reason: "Audit log; defensive." Under the bar, *who acted*
is C41's native `created_by` and *the action event* is C23's native append-only log (AI-CONTEXT:87 event
bus "records every action") — both fire on the dispatch regardless of whether C05 declares a contribution.
C05 needing to *contribute* a record is hardening on capability the stack already provides; it adds no new
capability for a 12-principle (P9 attribution is already met by `created_by`; P12 observability by the event
bus). The faithful framing is softer than the optimized delta (it says the fact "rides existing C19/C41/C23,
no new store"), which is why this is major not blocker — but a *contract/INV/AC/build-task* still over-states
C05's role. **Fix (applied).** Demoted the dispatch-record from an outbound *contract* + INV-4 clause + AC +
T6 to a passive cross-cutting note: the dispatch is *already* logged by the native event bus (C23) with
native actor attribution (C41); C05 introduces no record of its own. Reworded §3.2, INV-4, §7, AC-7, and
plan T6 accordingly.

### RC05-03 — major — plan T4 "Pool selection … Implement … select one available member" frames building selection logic Gas City's sling provides natively (SURVIVOR-PASS C05 DELTA-03 DROP)
**Claim.** Plan T4 ("Pool selection — When the target resolves to a pool of N interchangeable role-agents,
select exactly one available member and hand off") is an M-sized *build* task; §1 lists "Select within a
pool" as a C05 responsibility. **Evidence.** AI-CONTEXT:92 says sling "Routes bead/wisp to agent **or
pool**" — routing to a pool (and picking a member) is the *native sling behavior*. SURVIVOR-PASS C05
DELTA-03 ("Pool routing + fairness + anti-starvation") → **DROP**, reason: "Gas City's." Implementing
member-selection is building what Gas City already does. The spec's *description* side is restrained and
correct (§5 / OQ-2: "policy unspecified beyond 'pick exactly one available member,' deferred to sweep 2" —
this is faithful description of native behavior, KEEP). The *plan* side over-reaches by making it an
"Implement" task with a C03 pool-config prerequisite, implying custom selection code. **Fix (applied).**
Reframed plan T4 from "Implement … select" to "Wire/verify Gas City's native pool routing for the
'route-to-pool' target case; no custom selection engine — Gas City picks the member; C05 passes the pool
target through." Selection-policy detail stays deferred (OQ-2). Spec §1/§5 wording on "select within a
pool" softened to "pass a pool target to sling, which selects a member."

### RC05-04 — minor — back-pressure attributed to the C18 reconciler loop where the bar attributes it to Gas City dispatch (SURVIVOR-PASS C05 DELTA-02 DROP)
**Claim.** §6 (pool-exhaustion), §7 (Cost/scale), OQ-3, and plan risk #3 put back-pressure on "the
reconciler's desired-vs-actual retry loop (C18), with C05 holding no internal queue." **Evidence.** This is
the *right* faithful instinct (no custom C05 queue — aligns with the bar; optimized DELTA-02
"Admission-controlled back-pressure" → DROP "Gas City dispatch handles this"). The minor fidelity gap: the
bar's reason is that **Gas City *dispatch* handles back-pressure**, whereas the spec routes it through the
C18 reconciler tick. Re-deriving back-pressure as a C18-orchestration property risks re-inventing, at the
loop level, a property Gas City's sling may already provide natively. **Fix (applied).** Added one clause to
§7 and OQ-3 acknowledging Gas City's native dispatch may itself impose back-pressure; C05 adds none, and
whether back-pressure is observed at the sling layer (Gas City) or re-converged at the reconciler tick (C18)
is a sweep-2 question against the pinned `gc` binary (ties to G11). Keeps "no C05 queue."

### RC05-05 — minor — two mis-cited source line numbers (`rig` and `[[agent]]`)
**Claim.** §1 cites "AI-CONTEXT:102 `rig → agent worker role`" (repeated in §1 twice) and "a
`claude`-provider `[[agent]]`, README:120". **Evidence.** In AI-CONTEXT.md the vocab rows are: line **100**
`rig | agent worker role`; line **102** is `molecule | instantiated workflow / bead-tree`. So `rig` is
AI-CONTEXT:**100**, not :102. In README.md, line **120** is "Agent loop | … | Claude Code CLI | … | Gas City
`claude` provider preset" — it does **not** contain `[[agent]]`; the `[[agent]]` block is declared at
README:**361** (Phase-0). README:120 is correctly cited for "agent loop = C28 / `claude` provider" but is the
wrong line for the `[[agent]]` config-block claim. **Fix (applied).** Corrected `rig` citations to
AI-CONTEXT:100 and re-pointed the `[[agent]]`-block citation to README:361 (kept README:120 only where it
backs the `claude` provider / agent-loop claim). (Other cites spot-checked OK: AI-CONTEXT:92 dispatch row,
:104 convoy, :105 sling, :108 wisp; README:109 binding half-sentence, :128 methodology-in-file, :361/:364
Phase-0 one-`[[agent]]`/no-pool — all verbatim-accurate.)

### RC05-06 — minor — F40 row over-claims a stated coupling to C05; faithful but worth qualifying
**Claim.** §6 F40 row ("Last-mile drift … Healer monitors shipping vs. start rate (F-MODE F40, Partial)").
**Evidence.** F40 is a real F-MODE entry, but it is a *system-level* healer/anomaly concern (C36–C39); its
connection to C05 ("C05's role is faithful re-dispatch under the reconciler") is the same inference as
RC05-01 (reconciler re-invokes C05). It is fine to list F40 as *not C05-native*, but the row should not
imply C05 has a defined role in F40 beyond "is re-invokable." **Fix (applied).** Trimmed the F40 row to state
it is healer/loop-level (C36–C39 + C18), not C05-native, and C05's only contribution is INV-3 (fail-loud so
the loop can re-converge) — removing the implied active re-dispatch role.

### RC05-07 — minor (no change) — INV-1..INV-3 and the no-target/key-mismatch error taxonomy are sound faithful fills; INV-3 vs. Gas City "or pool" boundary noted
**Claim.** INV-1 (single-handoff), INV-2 (key-faithful), INV-3 (resolvable-target/fail-loud), and the §6
interface-local error taxonomy. **Evidence.** These are correctly `[FAITHFUL-FILL]`-tagged, are minimal
well-definedness constraints for "routes a bead/wisp to an agent or pool by template/role," and do not add
scope v4 withholds — they make the one-line responsibility implementable. INV-1's parenthetical correctly
distinguishes single-sling-call from convoy fan-out (AI-CONTEXT:104). No fidelity defect. One latent note:
INV-1 "exactly one selected pool member" presumes C05 does the selecting; with RC05-03 applied (Gas City
selects), INV-1 should read "exactly one recipient (Gas City's pool selection yields one member)." **Fix
(applied).** Adjusted INV-1 wording to not assert C05-side selection, consistent with RC05-03. Taxonomy
otherwise kept as-is.

## Verdict

**accept-with-fixes.** The spec is genuinely faithful in shape — it correctly frames C05 as a *thin seam over
Gas City's native dispatch*, correctly resists an internal queue (OQ-3), correctly defers pool-selection
policy (OQ-2), correctly routes the C09/C05 routing-key authority question to a shared OQ (OQ-1), and its
core invariants are minimal and well-tagged. The defects are the recurring Track-A failure mode plus the bar:
(a) one inferred structural coupling (reconciler→dispatch, RC05-01) presented as sourced fact, and (b) three
places (dispatch-record RC05-02, plan pool-selection RC05-03, back-pressure RC05-04) that drift toward
*hardening Gas City's native sling* — exactly the deltas SURVIVOR-PASS already ruled DROP for the optimized
track. All six findings were fixable in place by re-tagging inferences as fills and demoting native-capability
hardening to passive "the stack already does this" notes; **nothing was deferred**. No architectural change to
the faithful design; the route-and-handoff scope is the correct minimal reading.
