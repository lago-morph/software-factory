# Spec: `exemplar-budget-flag-tier-recalibration`

- **ID**: SKILL-SPEC-9e2d4f7a1b
- **Source retrospective**: ../2026-05-27-191.md

## Intent

Encapsulate the `exemplar-budget-flag:` YAML pattern in an exemplar artifact's frontmatter — a structured place to document a word-budget overrun, root-cause attribution, and a sibling-subagent instruction. Pairs with a systematic-overrun detector: when ≥50% of sibling subagents subsequently overrun their tier by similar margins, the flag becomes evidence for a next-round tier-table recalibration. Concrete moment: the Phase-7 BF-S exemplar (auto-007 Light tier 3500-5000) landed at 5698 words (+14%). The lead agent considered re-authoring but instead recorded the overrun in `exemplar-budget-flag:`, attributed it to ~300 words of new §1.5 D-default verification + ~150 words of §11 reconciliation discussion + ~150 words of §N.3 notes, and instructed sibling subagents Light-tier could land at 5000-5700. Subsequently 9-of-10 sibling per-candidate notes files overran (median Light +28%; Heavy +11%) — the exemplar surfaced the pattern first, and the YAML evidence trail let auto-007 Round 3 (had one fired) collect tier-recalibration data systematically rather than ad-hoc-eyeballing 10 subagent digests.

## Trigger

User says "the exemplar's over budget", "recalibrate the tier table", "check fanout overrun pattern", or proactively when an exemplar's self-check item (a) `wc -w` flags overrun against a pre-published tier table. Also triggered at fanout-close when the lead agent reviews subagent digests for systematic-overrun detection. Negative trigger: skip for one-off documents not part of a uniform-schema fanout — overrun on a standalone doc is just an edit-down decision, no tier-recalibration evidence to collect.

## Inputs

- The exemplar artifact's path and current word count (from `wc -w`).
- The pre-published tier table from the decision brief (which tier the exemplar's candidate is in + its word-count bounds).
- After fanout: sibling subagent digests reporting their own `wc -w` against their tier bounds.

## Outputs

- An `exemplar-budget-flag:` YAML block in the exemplar's frontmatter naming: (a) measured words, (b) tier upper bound, (c) overrun magnitude, (d) attributed root causes with word-cost breakdown, (e) sibling-subagent instruction (revised tier-bound or "land at upper bound is OK").
- After fanout: if systematic overrun detected (≥50% of siblings overrun by similar margin), a `tier-recalibration-evidence:` note in the close handoff naming the candidates that overran + suggested next-round tier-bound revision.

## Workflow

1. **Run exemplar self-check item (a)**: `wc -w <exemplar-path>` against the published tier bounds.
2. **If within tier**: skip this skill; proceed to fanout dispatch.
3. **If overrun**: do NOT immediately re-author. Instead:
   - a. Decompose the overrun into root-cause word-cost breakdown (which §s carry words not anticipated in the rubric).
   - b. Decide: is the overrun a *rubric-completeness gap* (rubric forgot a required subsection) or an *author-verbosity gap* (just wordy)? Rubric-completeness → keep words, recalibrate tier. Author-verbosity → edit down.
   - c. If rubric-completeness: write the `exemplar-budget-flag:` YAML block per the format below; accept the exemplar; revise the sibling-subagent dispatch brief's tier guidance with the new upper bound.
4. **After fanout**: collect sibling `wc -w` results from digests. Count siblings within tier vs over.
5. **If ≥50% of siblings overrun by ≥10%**: write `tier-recalibration-evidence:` note in the phase-close handoff naming the overrunning candidates + word counts + suggested next-round tier table (Light upper bound revised up by overrun median; same for Heavy).
6. **If <50% overrun**: exemplar-budget-flag stood as a one-off; no systemic recalibration evidence. Document in handoff as "exemplar overrun was outlier".

## Concrete examples

### Example 1: Phase-7 BF-S exemplar (the originating session)

`architectures/v3/backfill-notes/bf-s.md` frontmatter shipped:

```yaml
exemplar-budget-flag: |
  Exemplar measured at 5698 words; Light tier upper bound is 5000. ~700-word overrun
  attributed to: (a) the §1.5 D-1..D-7 verification subsection (~300 words) added per
  Reviewer 5 Defect 1 amendment; (b) the §11 summary discussion of cell-count discrepancy
  (~150 words) added to support silent-absorption auditor reconciliation; (c) the §N.3
  notes per archive file (~150 words extra above the rubric minimum). Sibling subagents
  whose candidate is Light-tiered should expect to land at the Light upper bound (5000)
  or slightly over; the auto-007 tier table calibration may need a Round-3 revision
  if multiple sibling specs land over.
```

The dispatch brief for Wave 7.1 inherited this: "Light-tier candidates may land at 5000-5700 if §1.5 + §N.3 sections are full." Post-fanout: 9-of-10 candidates overran (Light median +28%, Heavy median +11%) → systematic. Recorded in `SESSION-HANDOFF-2026-05-27-phase-7-close.md` as next-round tier-table recalibration evidence (Light → 4000-5800; Heavy → 5000-7200).

### Example 2: Hypothetical — exemplar within tier, no flag needed

For a future Phase-8 lean-eval fanout, the exemplar lands at 4200 (Light tier 4000-5500). Self-check (a) passes; no `exemplar-budget-flag:` YAML block is needed; dispatch proceeds with the published tier table unchanged.

## Anti-patterns

- **Re-author the exemplar on overrun without root-cause attribution**. Loses the rubric-completeness signal. If the rubric is the cause, sibling subagents will overrun too and the run will produce 9 ad-hoc overrun explanations instead of one systematic record.
- **Silently raise the tier table in the brief without `exemplar-budget-flag:` evidence**. Drifts the tier table from its calibration source. Future authors don't know why bounds are what they are.
- **Treat one-off exemplar overrun as evidence of tier-recalibration**. Without ≥50% sibling overrun the evidence is anecdotal; recalibrating on one data point produces tier-table thrash.

## Acceptance criteria

- [ ] Every exemplar that overruns its tier ships an `exemplar-budget-flag:` YAML block with root-cause word-cost breakdown.
- [ ] Sibling-subagent dispatch brief inherits the revised tier guidance verbatim.
- [ ] At fanout-close, if ≥50% of siblings overrun by ≥10%, a `tier-recalibration-evidence:` note is written to the phase-close handoff.
- [ ] No tier-table revision is published without `exemplar-budget-flag:` or `tier-recalibration-evidence:` as the calibration source.

## Files this skill creates / modifies

- `<exemplar-path>` — frontmatter gains `exemplar-budget-flag:` block when overrun.
- `<dispatch-brief-path>` — tier guidance section revised with sibling subagent instruction.
- `SESSION-HANDOFF-<DATE>-phase-N-close.md` — gains `tier-recalibration-evidence:` note if systematic.
- `architectures/v3/decisions/auto-NNN-*.md` — next round's tier table revised with cite to the recalibration evidence.
