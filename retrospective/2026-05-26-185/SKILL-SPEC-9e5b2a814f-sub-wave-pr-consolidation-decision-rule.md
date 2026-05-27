# SKILL-SPEC-9e5b2a814f — sub-wave-pr-consolidation-decision-rule

## Name
`sub-wave-pr-consolidation-decision-rule`

## Priority
**Medium.** PR-cap optimization with audit-trail preservation.

## Description (for skill discovery)
When a brief plans N sub-wave PRs (one per cluster) and the N sub-waves write disjoint files, decide at delivery time whether to consolidate to one omnibus PR. Triggers on multi-sub-wave dispatches where the brief commits to N≥2 PRs per cluster. The skill encodes the three-condition decision rule + the deviation-acknowledgement requirement.

## What this skill does

### Decision check (3 conditions, ALL must hold for consolidation to be valid)

1. **Disjoint files invariant.** Each sub-wave's output files do not overlap with sibling sub-waves'. Concretely: `set(files_in_subwave_1) ∩ set(files_in_subwave_2) == ∅` for every pair.
2. **Cluster rationale survives in the omnibus.** The brief's clustering reason (e.g., mandate-specific framing of GF / BF / U specs) is preserved as omnibus PR description sections.
3. **Blocking-isolation is preserved.** A failing spec MUST be isolatable for re-author without affecting siblings. If consolidation bundles blocking + non-blocking work in a way that re-author requires the whole omnibus to re-land, condition (c) fails.

### If all 3 conditions hold

- Consolidate to one omnibus PR.
- The PR description MUST contain a "Sub-wave PR consolidation deviation (honestly acknowledged)" section naming: (i) the brief's planned N sub-wave PRs; (ii) the consolidation rationale; (iii) the PR-cap savings; (iv) confirmation of the three conditions.
- The run's morning summary MUST repeat the deviation acknowledgement.
- The session handoff MUST repeat the deviation acknowledgement.

### If any condition fails

- Honor the brief's N-PR plan.
- Stack the N PRs in dispatch order; each PR targets the prior one's branch per the stacked-PR-on-feature-branch pattern.

## When NOT to use
- When the brief explicitly justifies N-PR split for non-disjoint-files reasons (e.g., per-cluster CI gates, per-cluster reviewer assignment).
- When N is small (≤2). The optimization isn't worth the deviation-acknowledgement overhead.

## Origin event
2026-05-26 Phase-6 autonomous run: auto-006 brief committed to 4 sub-wave PRs. All 9 sibling specs landed on a shared parent branch and wrote disjoint files. Consolidation to 1 omnibus PR saved 3 PRs against the ≤15 cap. The three-condition check was applied post-hoc; this skill makes it explicit and pre-flight.
