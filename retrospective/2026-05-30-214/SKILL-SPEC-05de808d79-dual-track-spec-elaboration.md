# Spec: `dual-track-spec-elaboration`

- **ID**: SKILL-SPEC-05de808d79
- **Source retrospective**: ../2026-05-30-214.md

## Intent

When a user wants a source architecture turned into a detailed spec/plan but is unsure whether to trust the source as-is or improve it, produce **both** in parallel: a **faithful** track that treats the source as a fixed proof and elaborates it exactly, and an **optimized** track that ruthlessly improves it with every change recorded as an explicit, justified delta. Both tracks decompose against one canonical component inventory and reuse the same component IDs, so a reader can diff the two component-by-component and see precisely where — and why — the optimized design departs from the original. This session ran both tracks for 23 components and the structure made the "what did we change and why" question answerable at a glance.

## Trigger

- User says "treat this as a fixed proof AND also ruthlessly optimize it", "do it both ways", "faithful vs improved".
- User is ambivalent about whether the source architecture is correct but wants maximum detail either way.
- Proactively: when asked to elaborate a source that the agent can see has real flaws, but the user may want fidelity to the original preserved as a baseline.
- Negative trigger: when the user clearly wants only one (just implement it / just critique it) — don't double the work.

## Inputs

- A source architecture / design corpus.
- A canonical component inventory (build it first if absent).
- A gap/ambiguity analysis of the source (an adversarial read), so the optimized track has concrete forces to optimize against.

## Outputs

- Parallel directory trees: `spec-faithful/` + `plan-faithful/` and `spec-optimized/` + `plan-optimized/`, one doc per component per track.
- A track-charter file defining the rules each track's authors must obey.
- A future-enhancements bucket for improvements deliberately deferred out of the optimized baseline.

## Workflow

1. **Write track charters.** Faithful: no architectural changes; mark inferred fills `[FAITHFUL-FILL]` and source ambiguities `[AMBIGUITY: Gxx]`, picking the reading most consistent with the rest of the source and saying why. Optimized: improve freely, but every deviation is `[DELTA-NN]` with what the source said, the change, the rationale tied to a concrete force (scale/failure/cost/security/simplicity/parallelizability), and the tradeoff accepted; keep the same component ID for diffability.
2. **Decompose once.** Both tracks key off the same canonical inventory IDs.
3. **Author both tracks in the same fan-out waves** (one builder per component×track), so they progress together.
4. **Review per track with track-appropriate adversaries.** Faithful reviewers attack *fidelity and completeness only*; optimized reviewers attack *the design* (cost, simplicity, failure handling).
5. **Record deferred improvements** in a future-enhancements bucket so the optimized baseline stays honest about scope.
6. **Diff for the user.** Because IDs and decomposition match, a final comparison memo can walk component-by-component.

## Concrete examples

**Example A — judge provider (this session).** Source required a judge model from a different family than the coder, but the platform issues no second-provider credential. Faithful track recorded this as an `[AMBIGUITY]` resolved to "same-provider baseline, cross-provider deferred"; optimized track's C29 independently produced a graded `judge_independence_policy` defaulting to L1 (same-family, satisfiable) with the cross-provider "judge seat" as a deferred enhancement. The user's decision ("same provider now, cross-provider later") slotted straight into both tracks plus the future-enhancements bucket (FE-1).

**Example B — bead schema.** Source named bead types but defined no schema (a blocker gap). Faithful C20 registered every named type with a minimal envelope and flagged the fills; optimized C20 resolved the gap with a concrete schema delta. Same ID, diffable, with the faithful version showing the floor and the optimized version showing the improvement.

## Anti-patterns

- Letting the faithful track quietly "fix" the source — that collapses the very baseline the dual-track exists to preserve; fixes belong only in the optimized track as deltas.
- Optimized deltas justified by taste rather than a named force.
- Diverging the decomposition between tracks — breaks diffability; both must use the same inventory IDs (note any split/merge mapping explicitly).
- Unbounded scope creep in the optimized track — park deferred improvements in a future-enhancements bucket instead of inflating the baseline.

## Acceptance criteria

1. Every faithful claim traces to a source citation; every inferred fill is marked.
2. Every optimized deviation is a marked delta with a force-grounded rationale and an accepted tradeoff.
3. The two tracks share component IDs and decomposition, so any component diffs cleanly.
4. Deferred improvements live in a named bucket, not silently in the baseline.

## Files this skill creates / modifies

- `_meta/TRACK-CHARTERS.md` — the rules for each track.
- `spec-faithful/<ID>-*.md`, `plan-faithful/<ID>-*.md` — the faithful track.
- `spec-optimized/<ID>-*.md`, `plan-optimized/<ID>-*.md` — the optimized track.
- `_meta/FUTURE-ENHANCEMENTS.md` — deliberately deferred improvements.
