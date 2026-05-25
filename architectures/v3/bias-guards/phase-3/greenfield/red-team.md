---
guard: red-team
target: draft-greenfield-synthesis
phase: 3.2
based-on-commit: e02d0ba
based-on-date: 2026-05-25
---

# Phase-3.2 red-team critique — greenfield draft

## §1 Persona stance

I am hunting for moments where the draft's strongest "ROBUST (all three tracks support, with corpus grounding)" claims rest on **single-source** corpus material that has been re-shaped into multi-source consensus by inheritance from the brief's framing, the failure-modes/contradictions registers, or the three Phase-2 tracks' shared cold-start required-reading list. The draft is most attackable in two places: (a) where unanimous Phase-2 convergence is doing the load-bearing work even though the brief itself pre-recommended the answer (§2.1 lead-agent working stance → ROBUST-G1), and (b) where day-0 substrate primitives have been promoted from a phenomenological corpus finding (Kahana cognitive escrow; Caremark exposure) into substrate-typed architectural commitments that the underlying primary sources never warrant at substrate-primitive granularity (ROBUST-G4, ROBUST-G5, ROBUST-G14, ROBUST-G19). The draft's hardest defense is its long citation lists; the attack is to show that the citation lists are doing brand-coverage work but the *individual citations* do not say what the ROBUST claim says.

## §2 Top attack findings

### Attack 1 — ROBUST-G1 (HIGH). "Day 0 = L3-Augmentation with no automation-eligible work units" is a Phase-2 unanimous convergence that the corpus only partially warrants; option (e) survives interrogation.

The draft splits the claim into "the (c)+(b) convergence" + "the underlying claim that day-0 = L3 is independently corpus-grounded" and asserts only the first half is brief-anchored. But the second half does not hold up:

- The cited evidence for "day-0 = L3" is F25 design-starvation greenfield-critical and F1/F27 greenfield-critical without out-of-distribution ground truth. F25 is a *throughput* failure mode about agents idling when the human cannot decompose work fast enough; it does **not** name day-0 regime classification. F1/F27 are *circularity* failure modes mitigated by cross-model judges; they require a holdout, not L3 specifically.
- Brief §2.1 option (e) — "Reject the L5-as-anti-pattern claim with corpus-grounded counter-evidence" — is *defensible from the brief's own footnote discipline*. Each of the three anchors carries an applicability caveat the brief authored: METR studies *developer-using-agent*, not *factory-running-agents*; Veracode is a code-scanner study without post-cycle V&V; CodeRabbit needs scope/population/review-protocol equivalence checked. None of these has been verified by any of the three Phase-2 tracks.
- CTR-H10 WEAK-4 sharpening actually argues *against* the day-0 L3 commitment: Round-2's empirical ceiling is **L5-anti, not L3-only**. If UC1 lights-out maps to L4 (per glossary §0), L4-day-0 with sample-audit is *not contradicted by Jaymin*.

**Severity: HIGH.** This is the load-bearing operating-mode commitment.

**Recommended action.** Demote ROBUST-G1 to DECISIONS-PENDING. Add a DPG asking: "Is day-0 *necessarily* L3, or can a defensible greenfield architecture run day-0 at L4 with sample-audit + cross-family judge from cycle 1, accepting Jaymin's bar but disputing its day-0 applicability?" Surface the D7-G-1 test result as a Phase-3.4 input.

### Attack 2 — ROBUST-G14 / DPG-7 (HIGH). The "EscrowSurface" substrate primitive has *one* primary source (Kahana, report 30) and that source explicitly disclaims primitive-level prescription.

The draft *acknowledges* the F-ANCHOR-2 single-source flag and surfaces it as DPG-7 — but still lists ROBUST-G14 with the five sub-primitives intact, retaining `EscrowSurface` as a candidate substrate primitive in the merged draft. The corpus does not support this at primitive granularity:

- Report 30 §3 anchors the *phenomenon* and Kahana's *governance critique* (STIR is voluntary; fragile). Report 30 §4 names the interval as a *design site*. **The five-primitive catalogue (reflective-question, success-criterion, similar-past, delegation-level, STIR cascade) appears in report 30 §4 with the verbatim caveat that "The catalogue is corpus-novel — Kahana names the *site*; this section enumerates *primitives*."** That paragraph is the report-author's own extraction, explicitly flagged as outside Kahana's primary text.
- The corpus' other voluntary-discipline-fragility anchors (Schillace Attention Firewall report 28 §6; Anthropic Auto-Review sensitive-action gates report 23 §3.5; Notion standup pre-read report 35) all sit at the *methodology/team-discipline* layer, not the substrate-primitive layer. None of them is *promoted to substrate* in its primary source.

**Severity: HIGH.** This is the largest single-source substrate-primitive promotion in the draft.

**Recommended action.** Demote ROBUST-G14 to DECISIONS-PENDING-and-tighten. Rewrite as: "substrate-triggered cognitive-escrow surface is corpus-warranted at the *phenomenology* layer; promotion to substrate primitive is single-source and methodology-layer is the safer default unless D7-G-2 disconfirms." Drop the five-primitive enumeration from ROBUST and move it to a Phase-5 ADR candidate.

### Attack 3 — ROBUST-G5 (HIGH). "≥3 region-shaped scenarios" is not in the corpus; it is the cold-start track's invented threshold.

Report 25 §5 explicates INCOSE Complexity Primer principle 12 ("Focus on desired regions of outcome space rather than specifying detailed outcomes"). The corpus does not anywhere prescribe `≥3` as a numeric bar for region-shaped scenarios at day 0. Cross-referencing followup 09 (Kaner), there is no numeric minimum either. The `≥3` number is the cold-start track's invention: GF-S §5.2 says "Operator authors ≥3 region-shaped scenarios" (invented at the track level); GF-M's bootstrap protocol does not require a count; GF-C says "5–10 scenarios."

ROBUST-G5 is *not* "all three tracks support" — it is one track's invented threshold reified by merge.

**Severity: HIGH.** This is a substrate refusal-to-start gate. Reifying an invented number into substrate enforcement is exactly the bias D5 prohibits.

**Recommended action.** Demote ROBUST-G5 to DECISIONS-PENDING. Replace `≥3` with "architecture-declared minimum scenario count; default deferred to Phase-6." Or remove the numeric bar entirely from ROBUST and keep only the *qualitative* requirement.

### Attack 4 — ROBUST-G19 (MEDIUM-HIGH). "RSI-declaration day-0 before the first cycle" extends Kahana's mid-market RSI test beyond what report 31 warrants.

Report 31 §1 defines the three-part RSI test and §2 walks Caremark prong-1 board exposure. Kahana's load-bearing operational claim is that **directors who fail to require oversight infrastructure for an RSI system face Caremark exposure**. The corpus does not say "the AILCCP three-controls must be scaffolded *before* the first cycle of a factory that *may* meet the RSI test at steady-state" — that is the cold-start-first track's structural commitment, generalised by the synthesis to "all three tracks."

In fact: GF-S §5.1 treats RSI three-part test as *substrate-evaluated property*; GF-M §5.3 ties it to methodology-side promotion; only GF-C makes RSI-declaration a day-0 substrate primitive.

**Severity: MEDIUM-HIGH.** Board-reporting requirement is real; day-0 timing is not.

**Recommended action.** Soften ROBUST-G19 to: "If the factory's intent block declares RSI-three-part conditions will be met at steady-state, the AILCCP three-controls and Caremark board-reporting structure are scaffolded *prior to the first cycle that meets those conditions* — which may be day-0 if RSI begins immediately, or later."

### Attack 5 — ROBUST-G10 (MEDIUM). "Cross-model judge mandatory at high-stakes / cold-start cycles" papers over a genuine three-way corpus split.

The draft acknowledges three judge sub-shapes (same-model-different-role; different-family-on-builder; different-family-on-spec) and Splitter Cluster-1 says they must remain distinct. But ROBUST-G10 *then* claims the (b) sub-shape is the right cold-start default and dismisses Anthropic's single-judge finding (followup 07 §3.6) as "track record precondition unmet."

The corpus does not say this. Followup 07 §3.6 says verbatim: *"using the same model is usually fine because the judge is doing a different task than your main LLM pipeline."* Their criterion is *alignment-with-human-judgment*, not *track record*. The draft has invented a "track record precondition" to make cold-start lean toward cross-model; that precondition is not in the source.

The corpus also has a genuine *third* position: Anthropic's Auto-Review subagent (report 23 §3.5) is *same-model-different-role* — the position the largest substrate vendor actually deploys.

**Severity: MEDIUM.** Cost-and-correctness consequence (cross-model is ~2× cost).

**Recommended action.** Revise ROBUST-G10 to "Typed judge primitive is robust; the choice of sub-shape at cold-start is methodology-layer and DECISIONS-PENDING." Move cross-model-at-cold-start into a DPG explicitly naming CTR-D7 / CTR-D8 / CTR-D4 WEAK-5.

## §3 What survives the attack

- **ROBUST-G4** (intent block in El Kaim's 9-field shape). Report 14 §3/§4.1 is a primary anchor but the 9-field discipline + invariants framing is *re-derived* by INCOSE GtWR (report 25 §3) — the corpus has two independent voices converging.
- **ROBUST-G6 / G7 / G8** (deterministic GtWR/EARS lint, requirement-count budgeter, contradiction detection via paraphrase divergence). All anchored on reports 25 + 26 with independent corpus voices.
- **ROBUST-G9** (production-scissors substrate-default-off). Genuinely multi-source (Shapiro R1-R5 report 32 §8.2; CaMeL followup 08 §3; Anthropic Skills closure rule report 23 §3.5; F44 multi-anchor).
- **ROBUST-G11 / G12 / G13** (watchdog, trajectory capture, cost ceilings). Round-2-grounded with cross-track unanimous acceptance.
- **ROBUST-G15 / G16 / G17** (no self-judge, production off, holdout substrate-enforced). G-CONV-1, G-CONV-2, G-CONV-6 in anchor-detector.

Roughly half the ROBUST set is genuinely robust; the other half (G1, G5, G10, G14, G19) is single-source-anchored or convergence-anchored and should be demoted.

## §4 Recommended edits for Phase-3.4 integration

1. **§1.1 ROBUST-G1 — demote and split.** Restate as DPG-1-new awaiting D7-G-1 result.
2. **§1.2 ROBUST-G5 — drop the numeric bar.** Replace `≥3 region-shaped scenarios` with architecture-declared minimum.
3. **§1.3 ROBUST-G10 — soften and surface the three-way split.** Remove "track record precondition unmet." Move sub-shape choice to DPG-3-new.
4. **§1.3 ROBUST-G14 — collapse into DPG-7.** Drop from §1; surface phenomenon (operator touchpoints are substrate-instrumentable) as ROBUST under different framing.
5. **§1.4 ROBUST-G19 — narrow scope.** Replace "scaffolded *before the first cycle*" with "*prior to any cycle that meets Kahana's three-part RSI test*."
6. **§5 dispatch notes.** Add D7-G-3: blind-axis test prohibiting invented numeric bars (ROBUST-G5).
7. **§4 citations.** Citation-tightening discipline: every ROBUST claim must cite *underlying corpus material at section level*.

Net effect: ~5 ROBUST claims demote to DECISIONS-PENDING (G1, G5, G10, G14, G19); ~14 stay; surviving ROBUST set is smaller but corpus-defensible. DPG list grows from 9 to ~13.
