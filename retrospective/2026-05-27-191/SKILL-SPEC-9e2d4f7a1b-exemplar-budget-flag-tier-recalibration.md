# Spec: `exemplar-budget-flag-tier-recalibration`

- **ID**: SKILL-SPEC-9e2d4f7a1b
- **Source retrospective**: ../2026-05-27-191.md

## Intent

When a uniform-schema parallel fanout uses a tiered word-budget rubric (e.g., "Light: 3500-5000 words; Heavy: 4500-6500"), the exemplar's measured word count is the first piece of evidence about whether the tier table is calibrated. The exemplar-budget-flag pattern surfaces that evidence into the exemplar's YAML frontmatter via an `exemplar-budget-flag:` block, instructs sibling subagents to expect the same overrun pattern, and — if ≥50% of sibling subagents subsequently overrun their tier — carries a tier-recalibration recommendation into the close handoff for the next-round dispatch brief. Phase 7 was the canonical demonstration: BF-S exemplar landed at 5698 words (Light tier upper 5000; +14%), and 9-of-10 sibling subagents subsequently overran their tier (Light median +28%; Heavy median +11%) — calibration evidence that would have been lost without the flag.

## Trigger

Direct user phrases:
- "the exemplar is over budget — should I cut it?"
- "the fanout is overrunning the word budget"
- "do we need to recalibrate the tier table?"

Proactive triggers:
- When authoring an exemplar for a uniform-schema fanout AND the exemplar's self-check (a) `wc -w` returns over the tier upper bound.
- When ≥3 sibling subagents in a fanout return digests reporting their notes file is over tier.
- At fanout-close, when counting per-tier overrun fractions for the close handoff.

Negative triggers:
- Single-author work (no fanout; the budget is a per-doc target, not a tier).
- The exemplar lands within budget AND no sibling overruns — no flag needed.

## Inputs

- The exemplar file (post-self-check).
- The tier table from the dispatch brief (Phase-7: Light 3500-5000; Heavy 4500-6500).
- At close: the wc -w values from every sibling subagent's notes file.

## Outputs

- `exemplar-budget-flag:` block in the exemplar's YAML frontmatter, with: measured wc-w, tier name + bound, overrun magnitude (absolute + %), root-cause attribution by section, instruction to sibling subagents on expected landing range, lead-agent decision (ACCEPT / RE-AUTHOR), justification for not re-authoring (if applicable).
- Sibling subagents' dispatch briefs carry a one-line forward instruction: "Light-tier candidates may land at 5000-5700 if their §1.5 + §N.3 sections are full."
- At close, if ≥50% of siblings overran their tier: a carry-forward bullet in the close handoff naming the calibration evidence and recommending the next-round dispatch brief's tier-table revision.

## Workflow

1. **Author the exemplar.** Run self-check item (a) `wc -w` immediately after authoring.
2. **If exemplar is within tier bounds**: no flag needed; proceed to fanout dispatch.
3. **If exemplar is over tier upper bound by ≤25%**: write the `exemplar-budget-flag:` YAML block in the exemplar's frontmatter. Identify the root cause(s) by section (typically: rubric-mandatory subsections that the original budget didn't allocate for). Make the lead-agent decision ACCEPT with flag; do NOT re-author. Instruct sibling subagents in the fanout dispatch brief that their tier may land at upper-bound + the observed overrun fraction. Document the asymmetry: forcing re-author damages exemplar quality; flagging preserves both quality and audit trail.
4. **If exemplar is over tier upper bound by >25%**: consider re-authoring. The flag is no longer "calibration evidence"; it's "rubric is mechanically unattainable." Either re-author with strict pruning OR rewrite the tier table in the dispatch brief BEFORE firing the fanout.
5. **At fanout-close**: count siblings' overrun fractions per tier. If ≥50% of subagents in a tier overran, add a carry-forward bullet to the close handoff: "Tier-recalibration evidence: <fraction>-of-<total> <tier-name>-tier subagents overran by <median>. Recommend revising <next-round-brief>'s tier table to <new-bounds>." If <50% overran, the exemplar was anomalous; no recalibration recommended.

## Concrete examples

### Example 1: BF-S exemplar in Phase-7 (actual session)

- **Tier**: Light (3500-5000 words per auto-007 Round 2 rubric).
- **Measured wc-w**: 5698 (+14% over upper bound).
- **Root-cause attribution**: (a) §1.5 D-1..D-7 verification subsection (~300 words; new in Round 2); (b) §11 cell-count reconciliation discussion (~150 words; new for silent-absorption auditor reconciliation surface); (c) §N.3 notes per archive file (~150 words extra above rubric minimum).
- **Flag YAML block** (copied verbatim from `backfill-notes/bf-s.md` frontmatter):
  ```yaml
  exemplar-budget-flag: |
    Exemplar measured at 5698 words; Light tier upper bound is 5000. ~700-word overrun
    attributed to: (a) the §1.5 D-1..D-7 verification subsection (~300 words) added per
    Reviewer 5 Defect 1 amendment; (b) the §11 summary discussion of cell-count discrepancy
    (~150 words) added to support silent-absorption auditor reconciliation; (c) the §N.3
    notes per archive file (~150 words extra above the rubric minimum). Sibling subagents
    whose candidate is Light-tiered should expect to land at the Light upper bound (5000)
    or slightly over; the auto-007 tier table calibration may need a Round-3 revision
    if multiple sibling specs land over. Lead-agent decision: ACCEPT the exemplar at 5698
    words; do NOT re-author; sibling subagents are instructed in the dispatch brief that
    Light-tier candidates may land at 5000-5700 if their §1.5 + §N.3 sections are full.
  ```
- **Subsequent fanout**: 9-of-10 sibling subagents overran their tier. Light median +28%; Heavy median +11%.
- **Close handoff carry-forward** (verbatim from `SESSION-HANDOFF-2026-05-27-phase-7-close.md` "advisory carry-forwards"): *"Word-budget tier recalibration for auto-NNN dispatch briefs. 9-of-10 candidates landed over their tier budget in Phase 7 (Light median +28%; Heavy median +11%). Future auto-NNN tier-tables should adjust Light to 5000-6500 and Heavy to 5500-7500. Address only if Phase 8 fires under the same tier-table pattern."*

### Example 2: counter-example — anomalous exemplar (hypothetical, calibrated against Phase-7 data)

If the BF-S exemplar had landed at 5698 (over Light 5000) but only 1-of-9 sibling subagents subsequently overran by >5%, the flag would have indicated "exemplar-specific overrun" — perhaps the exemplar author was over-thorough on §11 reconciliation. The close handoff would NOT carry a tier-recalibration recommendation; the lesson is "exemplar trim discipline" not "rubric calibration." The 50%-threshold rule prevents single-outlier flagging from triggering unnecessary recalibrations.

## Anti-patterns

- **Rigid re-authoring of an over-budget exemplar.** Phase-7's exemplar was 14% over Light tier. Forcing re-author would have damaged the exemplar's demonstration of the rubric's mandatory content (§1.5 D-default verification; §N.3 ADR-0036 framing for BF-L/U-A/D7-U-1) — exactly the elements that surfaced 5 explicit-challenges + 3 framing-distinct entries downstream. The flag preserved both quality and audit trail.
- **Blaming siblings for overrun when the exemplar set the precedent.** If the exemplar landed at 114% of budget, sibling subagents reading the exemplar as the shape model will reproduce the pattern. Their overruns are evidence about the tier-table calibration, not subagent defects.
- **Calibrating the next-round tier from a single exemplar.** The 50%-threshold rule is mandatory: only recommend recalibration when ≥50% of sibling subagents overran. A single over-budget exemplar is anomaly evidence; an N-of-M pattern is calibration evidence.

## Acceptance criteria

- [ ] Exemplar's YAML frontmatter contains `exemplar-budget-flag:` block when measured wc-w > tier upper bound.
- [ ] Sibling subagents' dispatch brief carries forward instruction on expected landing range.
- [ ] Close handoff carries tier-recalibration recommendation IFF ≥50% of sibling subagents overran.
- [ ] No silent overruns: every over-budget output is mechanically documented in YAML (not just narrative).

## Files this skill creates / modifies

- `<exemplar-file>` — adds `exemplar-budget-flag:` YAML block in frontmatter.
- `<dispatch-brief>` — adds sibling-subagent forward instruction on landing range.
- `<close-handoff>` — adds tier-recalibration carry-forward bullet when ≥50% threshold met.
