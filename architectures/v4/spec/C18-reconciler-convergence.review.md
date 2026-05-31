# Adversarial review — C18 Reconciler / Health Patrol loop (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Workflow Engine
Target: spec/C18-reconciler-convergence.md (+ plan-faithful/C18-reconciler-convergence.md)
Charter: canonical-track (post-convergence) → attack FIDELITY and COMPLETENESS only, not the design;
plus the capability-for-principle bar (no hardening dressed up as new capability).

## Summary of attack vectors (all four largely clean)

- **THE BAR — native reconciler, no custom machinery.** PASS. Both docs explicitly drop any custom
  control-loop / scheduler / tick-engine / queue / convergence-checkpoint (spec §1 "What C18 is NOT"
  bullet 1, §7; plan §1, §5 risk 2, §6 DoD). T4 is framed as a *thin wrapper over native Health Patrol*
  ("spec the contract, not the engine"). G11 "invent no `gc` reconciler internals" is honored repeatedly
  (spec §3.1/§4/§9 fills; plan §1/§5). The "modified reconciler" fork-trigger citations (README:334/518,
  AI-CONTEXT:439/476) check out verbatim. Only the P4 deterministic-first gate ordering + bounded
  iteration are kept. No capability-for-principle hardening detected — every kept property maps to a
  12-principle (P4 primarily, P8/P11 partial) and no new authority surface is introduced (§7).
- **D-8 / RC05-01 — C18→C05 (re)dispatch trigger marked `[FAITHFUL-FILL]`.** PASS. Flagged in spec §2
  ("What C18 is NOT" bullet, §2 table row, §2 fill), §3.2, the §5 Mermaid edge, §6 F22, OQ-2; mirrored in
  plan T6 / §4 / §5 risk 3 / §6 DoD. The "never co-occur in a causal sentence" basis is *verified*:
  README:109 ties dispatch to *formulas* ("formulas reference templates by name; sling routes work to
  agents"), not to the reconciler; AI-CONTEXT:92 (sling) and AI-CONTEXT:93 (reconciler) are separate
  concept rows with no causal link. The fill is correctly justified and never asserted as fact.
- **G18 — numeric termination policy routed to C39 (XC-3), not built here.** PASS. C18 owns only the loop
  + per-pass bound enforcement + the bound-reached signal; N→escalate, oscillation/F52 detection, and L5
  ship authorization are routed to C39 throughout (spec §1 NOT-bullet 2, §2 table, §3.1/§3.2, INV-2, §6,
  §7, AC-5, OQ-1; plan T3/T5, §5 risk 1, §6). The INV-2 split ("enforce an injected bound + emit signal"
  vs "own N / detect oscillation / authorize ship") is explicit and matches XC-3's routing. C39 has **no
  spec yet** (Batch-4, not authored) — C18 cannot and does not cite a C39 spec; it correctly grounds the
  seam in the review-log (XC-3) and carries OQ-1 as the load-bearing confirmation item. Faithful posture.

## Findings

### RC18-01 — minor — C40 Orders cited as "AI-CONTEXT:90/§"; line 90 is the *Messaging* concept row, not Orders
**Claim.** §2 dependency table ("Distinct mechanism (not owned) | C40 durable Orders") cites
"AI-CONTEXT:90/§ — D-8: 'Order' owned by C40". **Evidence.** AI-CONTEXT:90 is concept-table row 6,
"Messaging (Mail + Nudge) — Mail = durable; Nudge = ephemeral". "Order" is **not** a numbered concept-row
in AI-CONTEXT §3.2 at all; it surfaces only at AI-CONTEXT:76 (P11 row, "Orders subscribing to
crashes/gates") and AI-CONTEXT:486 (Temporal decision row). The authoritative basis for "Order → C40" is
**D-8** (review-log), which *is* cited and is correct. So the claim's substance holds; only the line
number is wrong and could mislead a reader checking the cite. **Fix (applied).** Dropped the spurious
"AI-CONTEXT:90/§" line anchor and grounded the C40 distinction in **D-8** (the binding decision) plus the
AI-CONTEXT P11 "Orders" mention (line 76), so the citation resolves to text that actually says "Orders".

### RC18-02 — minor — `attempt_no`/`max_attempts`/`escalated`/`closes` presented as C20's *frozen* field names; C20 has not frozen them
**Claim.** The spec repeatedly attributes specific field identifiers to C20 — e.g. §2 table ("consuming
C20's `attempt_no`/`max_attempts`/`escalated`/`closes` schema slots"), §3.1, §3.2, §4, the §3.1/§4 fills.
**Evidence.** C20's own spec (spec/C20-bead-schema.md §4.3 + AMBIGUITY block) names these descriptively —
an **attempt-count** field, a **terminal-state enum** (`resolved` | `escalated` | `abandoned`), and an
**escalation-marker** — and *explicitly defers concrete field schemas to sweep 2*. C20 line ~172 even
flags that the optimized track chose a *different, incompatible* taxonomy (`caused_by`/`closes`). The four
exact tokens `attempt_no`/`max_attempts`/`escalated`/`closes` originate in **XC-3's wording in the
review-log**, not in C20's frozen schema. Stating them as "C20's slots" mildly over-claims that C20 has
registered those identifiers — a sweep-1 fidelity slip (asserting a downstream component froze names it
has not). Note `closes` in particular is a *chain-edge* field in C20's taxonomy, not an attempt-counter
slot, so listing it beside `attempt_no`/`max_attempts` as a bound-counter is slightly mis-grouped.
**Fix (applied).** Re-attributed these to **XC-3's boundable-slot set** ("the `attempt_no`/`max_attempts`/
`escalated`/`closes` slots named in XC-3, backed by C20's attempt-count / terminal-state / escalation
schema fields — concrete field names are C20-sweep-2") at the first/load-bearing occurrences (§2 table,
§3.1 fill), so C18 no longer implies C20 has frozen those exact identifiers. Left the shorthand in
lower-traffic spots intact (it is now disambiguated by the corrected anchors) to avoid churn.

### RC18-03 — minor — README:109 ("formulas … sling routes") is mild positive evidence for the *alternative* trigger and is worth surfacing, not just the absence-of-co-occurrence
**Claim.** The §2 / §3.2 fills justify the C18→C05 edge purely negatively ("the two never co-occur in a
causal sentence"), and name the C12-formula-step alternative only as a bare possibility. **Evidence.** The
*only* place v4 states a sling trigger at all — README:109 — actively ties dispatch to **formulas**
("Gas City formulas reference templates by name; sling routes work to agents with specific templates").
That is not merely "no co-occurrence with the reconciler"; it is a (weak) affirmative pointer toward the
*formula-driven* alternative the fill lists. Surfacing this strengthens the honesty of the fill (the
alternative is faintly v4-supported, the reconciler edge is not) without changing the modelled disposition.
This is a completeness nicety, not an error. **Fix (applied).** Added one clause to the §2 fill noting that
README:109 — v4's only dispatch-trigger sentence — points at *formulas*, so the C12-step alternative is the
faintly-sourced one and the reconciler edge remains the structural inference. Disposition unchanged
(reconciler-driven, flagged).

### RC18-04 — minor (no fix) — "C18 (Batch 3) precedes C39 (Batch 4)" forward-reference is correct but C39 spec absence should be stated as a fact, not just a batch note
**Claim.** Spec §9 OQ-1 / plan §2 say the C39 seam must be frozen "before C39 exists". **Evidence.**
Confirmed: `spec/C39-fix-task-loop-closure.md` does not exist yet. The docs handle this correctly (route
to XC-3, carry OQ-1). The only nicety: a reader may not realize C39 is *literally unwritten* (C13's spec,
by contrast, says outright "C18 has no spec yet at sweep-1"). **Fix.** None applied — this is a stylistic
parallelism preference, not a fidelity defect; the XC-3 grounding is already the correct authority and the
batch-inversion is well-explained. Flagged for awareness only.

## Verdict

**accept-with-fixes.** Faithful, well-traced, and disciplined against the bar. All four assigned attack
vectors (native-reconciler / no custom machinery; RC05-01 trigger flagging; G18→C39 routing; fidelity) pass.
Every load-bearing citation spot-checked against the source docs resolves correctly (README:154/159/160/370/
334/518; AI-CONTEXT:34/69/73/87/92/93/187/439/476; F-MODE-COVERAGE:44/47/76/94/100/170) **except** the C40
line-number (RC18-01, fixed). Cross-component consistency with C05 (mirrored RC05-01 fill, `Depends on: C18`),
C13 (`Depends on: C18`, molecule-as-converged-subject), and C20 (boundable slots routed to C39) holds. The
only substantive fidelity slip was over-claiming that C20 has *frozen* the `attempt_no`/…/`closes` field
names (RC18-02, fixed by re-attributing to XC-3's slot set). No blockers, no majors; nothing architecturally
significant deferred — OQ-1 (C39 ownership) and OQ-2 (C05 trigger) are already the correct
human/orchestrator-confirmation items and are left as the docs' own standing OQs, not new deferrals.
