# Adversarial review — C23 Event Bus (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Persistence & Memory
Target: spec/C23-event-bus.md
Charter: Track A → attack FIDELITY and COMPLETENESS only, not the design.

## Findings

### RC23A-01 — major — G27 resolution silently contradicts the AI-CONTEXT §5.4 impedance ranking; the reading is defensible but the "Lowest = property not directive" reinterpretation is itself a fill
**Claim.** §6 [AMBIGUITY: G27] picks reading (b) — raw-API-bodies is the wired CXDB source, event-bus is
a latent available source — and reinterprets §5.4's "Lowest impedance" ranking as "a property statement,
not a build directive." **Evidence.** AI-CONTEXT §5.4 literally *ranks* the event-bus path **Lowest /
best** and the raw-bodies path #2; v4 then builds the #2 path with no stated reason (G27 in the gap
analysis is exactly this unexplained override). The spec's resolution is well-argued (CXDB's *turn* unit
needs conversation payloads that live in raw bodies, not in action events) and correctly routes the
contradiction to an OQ — this is the right faithful move under Track A rule 3 (record both, pick the one
most consistent with the rest of v4, state why). The one fidelity risk: the spec asserts the event bus
"does not contain" the model request/response bodies as if v4 stated it; v4 says events are "trajectory-
shaped" (§5.4), which *suggests* but does not *state* they lack the full bodies. **Fix (applied).**
Re-tagged the "event bus does not contain the bodies" claim as the faithful inference it is (the basis
for choosing (b)), so it isn't read as a v4 fact. The (b) choice itself is sound and kept.

### RC23A-02 — minor — INV-2 "gap-free enough to checkpoint" is vaguer than v4 and weaker than the Track-B twin
**Claim.** INV-2 says `seq` is "strictly-increasing" and "gap-free enough to checkpoint against."
**Evidence.** v4 says "monotonic seq" (AI-CONTEXT §3.2), which is *monotonic*, not necessarily gap-free.
"Gap-free enough" is an unhelpful hedge — checkpointing works against monotonic-but-gapped seq too (you
resume from last-seen). OQ-4 correctly raises the gap-free-vs-gapped question against the real Gas City
binary. The faithful reading should not assert gap-freeness (which v4 doesn't state) nor hedge it
ambiguously. **Fix (applied).** Reworded INV-2 to "strictly-increasing monotonic `seq` imposing a total
order; whether it is gap-free (single appender) or monotonic-but-gapped under concurrency is OQ-4 against
the pinned binary" — matching what v4 actually states and deferring the rest.

### RC23A-03 — minor — "Records every action" (INV-4) is asserted as a completeness guarantee v4 doesn't fully back
**Claim.** INV-4 / AC-7 assert the bus is *complete* — "no action path bypasses the log." **Evidence.**
v4 says the bus "records every action" (README line 252) as a description of intent, but never proves
there is no bypass path; for an *adopted* Gas City primitive, whether every internal Gas City action
actually emits an event is an unverified upstream property (the same G11-class concern C21/C01 carry).
Asserting it as an invariant C23 *upholds* slightly overstates: C23 (adopted) inherits whatever
completeness Gas City provides. **Fix (applied).** Qualified INV-4 to note it is an *adopted Gas City
property* to be verified by the conformance pack (AC-7), not a guarantee C23-the-spec independently
enforces — consistent with the §1 "NOT factory-authored" framing.

### RC23A-04 — minor — Bundle-id namespace: C23 is correctly silent (events are JSONL, not CXDB-typed), but the cross-store note should appear
**Claim.** C23 carries plain JSONL records with no `{bundle_id,type,version}` triple (it is pre-CXDB);
the XC-4 namespace collision is a C20/C21/C22 concern, not C23's. **Evidence.** Correct — C23-A rightly
does not name a bundle-id. But because C23 is the *lowest-impedance CXDB source* (I5) and the Track-B
twin proposes feeding C23 records into C21, a reader should know the typed-bundle question is resolved
downstream (at the C24 bridge / C22), not at C23. **Fix (applied).** Added a one-line note at I5 that when
C23 records are bridged into CXDB they acquire a `{bundle_id,type,version}` *there* (C22/C24), and the
canonical namespace is the XC-4 integrator ruling — so C23-A is consistent with the subsystem.

## Verdict
**accept-with-fixes.** Strong, faithful, well-traced; the F14/F10/F11 attribution+audit story and the
CXDB-independence (G33 support for C21) are the correct minimal readings. The G27 resolution is sound
and properly routed to an OQ. Fixes are all "qualify an adopted/inferred property as such rather than
asserting it as a v4 fact" (seq gap-freeness, action-completeness, the event-bus-lacks-bodies inference)
plus an XC-4 cross-reference. No fidelity blockers; nothing architectural deferred.
