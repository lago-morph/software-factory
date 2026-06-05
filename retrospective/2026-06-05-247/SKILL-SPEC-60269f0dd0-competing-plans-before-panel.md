# Spec: `competing-plans-before-panel`

- **ID**: SKILL-SPEC-60269f0dd0
- **Source retrospective**: ../2026-06-05-247.md

## Intent

When a strategic planning question is open — several defensible directions, no obvious winner — the
default failure mode is for the lead agent to write one plan and then "review" it, inheriting its own
anchoring. This skill prevents that: author a shared grounding brief plus one exemplar, dispatch 2–3
subagents to write *competing* full plans under deliberately distinct strategic lenses, synthesize them
into one unified candidate, and only then run the adversarial panel. The panel critiques a synthesis
that has already absorbed the strongest case for each direction, so its amendments land on real seams
rather than on a single author's blind spots. In PR #247 this produced three plans (velocity / de-risk
/ yield) whose synthesis survived a six-expert panel with all six returning "accept-with-amendments"
and several amendments landing exactly on the lens boundaries.

## Trigger

- **Direct**: "give me a few options for what to do next", "compare and contrast approaches", "I want a
  selection of directions", "have other agents come up with multiple plans".
- **Proactive**: an open strategic/architectural question with ≥2 genuinely defensible directions and a
  decision that will shape multiple future sessions; the user signals they want rigor ("think long and
  hard", "use a panel"), or the lead agent notices it is about to write "the" plan for a contested
  question.
- **Negative**: a well-bounded task with one obvious approach; a pure implementation ticket; a question
  the user has already decided the direction on (don't re-litigate a settled call).

## Inputs

- The open question + any operator constraints/preferences stated so far.
- The corpus needed to ground the plans (specs, prior decisions, external workloads).
- The number and identity of the strategic lenses (default 3; pick lenses that genuinely pull in
  different directions, e.g. fastest-to-value, lowest-risk, highest-throughput).

## Outputs

- A shared grounding brief + exemplar plan (the anchor every author and reviewer reads).
- One file per competing plan (`plan-<lens>.md`), each a full plan, not a sketch.
- A synthesized unified plan.
- (Then hands off to the adversarial-panel step / `subagent-prompting` for the review wave.)
- Commits at each wave boundary; the working corpus lives under a `_meta/.../` directory.

## Workflow

1. Write a **grounding brief** that fixes the facts every author must work from, and author **one
   exemplar plan** (per the repo's "exemplar before parallel fanout" rule) in a deliberately-named lens
   so authors have a format model to improve on or argue against.
2. Choose 2–3 **distinct strategic lenses** that genuinely diverge. Name them so the divergence is
   obvious (velocity / de-risk / yield is one good triple).
3. Dispatch one real subagent per lens, each briefed to: read the grounding brief, write a *full* plan
   in its lens to a named file, and return a ≤15-line receipt (thesis, 3 biggest differences from the
   exemplar, strongest argument, top risk). Run them in parallel.
4. Read the receipts (and drill into the plans as needed); **synthesize** one unified candidate that
   takes the strongest move from each lens and records where they conflict.
5. Hand the synthesis — not the exemplar — to the adversarial panel. Require the three-tier verdict
   (accept / accept-with-amendments / reject-with-counter-proposal).
6. Fold the panel's amendments into the deliverable; keep the competing plans and the synthesis as the
   historical reasoning trail.

## Concrete examples

### Example 1: "What's next for the factory?" (PR #247)

Input: an open question about how to exercise a just-built factory. The lead wrote a grounding brief +
a bootstrap-first exemplar, then dispatched three subagents — `plan-A-velocity` ("drive one nail,
calibrate the judge first"), `plan-B-derisk` ("verify substrate + judge before leaning on self-build"),
`plan-C-yield` ("production line ordered by the real dependency graph"). The synthesis absorbed
calibrate-first (A), the holdout/substrate de-risking (B), and the buildable-slice ordering (C). The
six-expert panel then caught that C's "parallel rigs" buy no speed on one seat and that the
"clusterless slice" wasn't clusterless — amendments that only surfaced because the synthesis carried C's
throughput claims into the panel for adversarial testing.

### Example 2: choosing a persistence layer for a new service

Input: "should we use Postgres, SQLite, or a document store?" Dispatch three plans — one optimizing for
operational simplicity, one for query flexibility, one for migration safety. The simplicity plan argues
SQLite; the flexibility plan argues Postgres+JSONB; the migration plan argues a schema-versioned
Postgres. Synthesis: Postgres with a JSONB escape hatch and the migration plan's versioning discipline.
The panel then stress-tests the synthesis's "JSONB escape hatch" against the migration plan's concerns —
a tension invisible to any single-author plan.

## Anti-patterns

- **Writing one plan and calling the self-review a "panel".** The lead's inline objections inherit the
  lead's anchoring (this repo already bans inline-simulated reviewers). The competing plans must be
  *real* subagent dispatches under genuinely different lenses.
- **Lenses that don't actually diverge.** Three plans that all say roughly the same thing waste the
  fanout. Choose lenses that pull in opposite directions (fast vs safe vs throughput).
- **Skipping the synthesis and panelling all three plans separately.** The panel should critique one
  unified candidate; reviewing three plans in parallel produces three disconnected critique sets and no
  decision.
- **Letting the exemplar become the answer.** The exemplar is a format model and one option; if the
  synthesis is just the exemplar with edits, the competing plans were theater.

## Acceptance criteria

- [ ] A shared grounding brief + exemplar exist and were given to every plan author.
- [ ] ≥2 competing plans exist as full plans (not sketches), each in a distinct named lens.
- [ ] A synthesis exists that visibly takes ≥1 move from each competing plan and names their conflicts.
- [ ] The adversarial panel reviewed the synthesis, not the exemplar, with the three-tier verdict.
- [ ] At least one panel amendment is traceable to a seam between two lenses.

## Files this skill creates / modifies

- `<meta-dir>/00-grounding-and-exemplar.md` — the shared anchor + exemplar plan.
- `<meta-dir>/plan-<lens>.md` — one full competing plan per lens.
- `<meta-dir>/10-unified-plan.md` — the synthesis handed to the panel.
- (Downstream) `<meta-dir>/panel/*.md` — the adversarial-panel critiques + verdict.
