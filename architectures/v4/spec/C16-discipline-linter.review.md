# Adversarial review — C16 Discipline linter (LLM-where-tool) (canonical track, sweep 1)

Reviewer persona: Adversary / critic-fixer — Workflow Engine (C16)
Target: spec/C16-discipline-linter.md + plan-faithful/C16-discipline-linter.md
Charter: single canonical track → attack FIDELITY + COMPLETENESS (not design), PLUS the
capability-for-principle bar (flag any addition that hardens existing stack capability rather than
delivering new capability tied to a 12-principle). Grounding: ADVERSARY-BRIEF, D-6/D-7/D-9, XC-3, G18.

## Findings

### RC16-01 — minor — Self-healing-loop quote ("without human intervention") was uncited; needed an anchor and the inventory-implied line is README:248, not the P11 header at :246
**Claim.** §6 "G18 routing" paragraph paraphrases the self-healing loop "Observability → anomaly →
diagnosis → fix → ship, without human intervention" to justify why the *runtime* loop bound is C39's, but
gave no source line — and the natural anchor a reader would reach for (the P11 header) is README:246, which
is the *heading* "### Principle 11 — Self-healing loop", not the quoted sentence. **Evidence.** README:246 =
`### Principle 11 — Self-healing loop`; README:248 = `Observability → anomaly → diagnosis → fix → ship,
without human intervention.` (verified). The quote is the load-bearing reason the loop-closure half is a
*runtime* concern (C39), so it should be traceable. **Fix (applied).** Added the explicit `README:248`
anchor in the §6 routing sentence. Off-by-two, cosmetic; the routing logic was already correct.

### RC16-02 — minor — G18 routing to C39 is sound and matches XC-3 verbatim, but C39 has no spec yet, so OQ-G18 is the right (and only) safe posture — confirming, not a defect
**Claim.** §1 / §6 / OQ-G18 route the G18 numeric termination/oscillation/L5-ship policy entirely to C39
and keep only the static LLM-vs-tool linter in C16. **Evidence.** XC-3 (review-log) states verbatim: "the
numeric policy (N attempts → escalate, F52 oscillation detection, L5 ship authorization) is deferred to C39
(and possibly C18). Confirm C39 owns it." The inventory also tags G18 against C39's neighbours (C18, C20);
the C39 spec does **not yet exist** on disk (`spec/C39-*.md` absent), so the routing cannot be cross-checked
against C39's own text this sweep. C16 handles this exactly right: it asserts the routing, cites XC-3, and
parks the confirmation in **OQ-G18** with the correct fail-safe ("If C39/C18 disclaim it, G18 needs a new
home; it does **not** revert to C16"). **Fix.** None — this is the correct faithful posture. Recorded so the
sweep-2 integrator knows the C39-side confirmation is still outstanding (no C39 doc to verify against yet).

### RC16-03 — minor — A/B inventory IDs (A36b/B31/B75) cited as provenance; consistent with D-6 (history preserved in _meta), no body-level "Track A/B" framing — clean
**Claim.** The spec header maps `A36b, B31, B75` and cites `component-inventory-A` / `component-inventory-B`.
Under D-6 (single canonical track) one might suspect a Track-A/B framing violation. **Evidence.** D-6 forbids
a component **framing itself** as "Track A/faithful vs a live Track B"; it explicitly **PRESERVES** the A/B
provenance in `_meta/` docs. C16 cites the A/B inventory rows only as *source provenance* (where the
requirement originated) and labels itself `Track: canonical`; a body grep finds **no** "Track A/Track
B/faithful track/optimized track" self-framing. A36b ("Each guard must cite a falsifying scenario"), B31,
and B75 ("every guard points at a falsifying scenario, reviewed monthly") all verify. **Fix.** None — D-6
compliant.

### RC16-04 — minor — Derived/soft upstreams (C17/C02/C03/C46) are correctly fenced as "consistent-elaboration", not asserted as inventory edges — fidelity handled, not a defect
**Claim.** §2's dependency table lists C17/C02/C03/C46 as upstreams though the inventory states only
`C16 Depends on → C12`. **Evidence.** This is the classic faithful-fill risk (inventing dependency edges),
but C16 pre-empts it: the "Dependency-footprint note (fidelity)" explicitly states C12 is the **single
formal** dependency and the rest are "derived/soft … traced through the *other* component's doc, not asserted
as an inventory edge," mirroring C10's identical shape. Each is genuinely traceable (C17/C02 = the tool-node
ABI it is built *as*; C03 = the enable/severity config; C46 = the catch-count sink for the monthly review).
**Fix.** None — the fence is exactly the faithful move; flagged only to confirm I checked the over-claim.

## Bar / over-build checks (all PASS — no findings)
- **Minimal like C10.** No model call (INV-1, AC-4), advisory-by-default (INV-3), read-only (INV-4),
  stateless (§4) — same minimal shape as C10. No hardening beyond the P4-tied capability. PASS.
- **F52 falsifying-scenario obligation present + load-bearing.** INV-2 + AC-2 + the T2 schema requirement
  ("a finding without a falsifying scenario unrepresentable") make it structural, not a slogan — directly
  realises F-MODE:100/:170. Not discipline-without-purpose. PASS.
- **No runtime heal-loop bounding (that's C39).** Explicitly disclaimed in "What C16 is NOT" + §6 + AC-8.
  PASS (see RC16-01/02).
- **No model-based "prove no reasoning needed" reviewer.** Explicitly disclaimed ("NOT a model-based /
  semantic reviewer … cannot *prove* a node needs no reasoning"). PASS.
- **No node-kind redefinition (D-7).** INV-5 + §2 taxonomy row + AC-8: C16 *consumes* C12's
  `{agent,tool,gate,sub_formula}`, never redefines it. Matches C12 §3.1 ("the policy is C16's"; "key on this
  distinction"). PASS.
- **No F38 claim (D-9).** Body grep: zero occurrences of F38. C16 lints *formulas*, F38 is C10's *spec* duty.
  PASS.
- **Source fidelity.** README:154/:160/:162 and F-MODE:100/:170 all verified **verbatim**. No fill mislabeled
  as fact; FAITHFUL-FILL tags are conservative and correctly placed (report shape, heuristic set,
  justification annotation, rule-config home). No contradiction with C12 (cross-checked C12 §3.1, §6, §9).

## Verdict
**accept-with-fixes.** Faithful, minimal, and well-traced; the load-bearing F52 falsifying-scenario
obligation is correctly made structural (INV-2/AC-2/T2), the G18 numeric policy is cleanly routed to C39 per
XC-3 with the correct non-reverting fail-safe (OQ-G18), and the bar is met on every over-build axis (no
runtime loop bound, no semantic reviewer, no taxonomy redefinition, no F38). Only fix needed was a one-line
source anchor (README:248) for the previously-uncited self-healing-loop quote — applied. The single
architecturally-significant open item (C39-side confirmation of G18 ownership) is **DEFERRED** to sweep-2
integration only because **the C39 spec does not exist on disk yet** — there is nothing to cross-verify
against this sweep; it is already parked correctly as OQ-G18 and must not revert to C16. No fidelity blockers.
