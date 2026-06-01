# Spec: `iterative-multi-persona-review-loop`

- **ID**: SKILL-SPEC-d979f8eb32
- **Source retrospective**: ../2026-06-01-227.md

## Intent

Run a document or artifact through repeated rounds of real-subagent adversarial review, rotating reviewer personas between rounds and dispatching a dedicated regression-verifier each round that checks the prior round's named fixes for completeness, until a full round returns zero factual, zero contradiction, and zero major findings. It earns its place because in this session a three-round loop over a restructured architecture document surfaced a fence/eval ordering contradiction in round 1, a C20 dual-modeling contradiction and a missing safety caveat in round 2, then converged clean in round 3 — none of which a single review pass would have caught.

## Trigger

- Direct: the user asks to "review in a loop", "have N reviewers with different personas", "loop until there are no factual or contradiction findings", "adversarially review and iterate", "tear this apart until it's clean".
- Proactive: after a non-trivial restructure or authoring of a high-stakes long-lived artifact (architecture doc, spec, plan, ADR set) where a single review would under-cover; especially when the artifact has many internal cross-references that can drift.
- Negative: a one-line change, a throwaway scratch doc, or code already covered by `/code-review`. Do not spin up a multi-round loop for trivial edits.

## Inputs

- The target artifact path(s) (committed, so reviewers read a stable version).
- The change goals stated as testable properties (e.g. "products are first-class", "zero change-narration").
- The termination bar (default: a full round with 0 factual / 0 contradiction / 0 major findings; minors do not block).
- Source-of-truth references reviewers must check claims against (e.g. an inventory, the specs).

## Outputs

- One review record per reviewer per round, written to disk under a `review-*/` directory (e.g. `R1-first-time-reader.md` … `R8-fresh-eyes.md`), each carrying severity-classified findings and a verdict from the three admissible tiers.
- Edits to the target artifact folding each round's findings.
- A commit per round (artifact fixes + that round's review records).
- A short convergence statement once the bar is met.

## Workflow

1. Commit the artifact so every reviewer reads the same SHA. State the change goals and the termination bar explicitly.
2. **Round 1 — broad coverage.** Dispatch ≥3 real subagents (the `Agent` tool, never inline-simulated) with distinct personas: a first-time reader (clarity), a source-of-truth fact-checker (every claim verbatim against the authority), and an internal-consistency reviewer (rebuilds the artifact's invariants — counts, partitions, cross-refs). Each writes a ≤15-line receipt; full findings go to disk. Give each the three verdict tiers: `accept-as-is`, `accept-with-named-amendments`, `reject-with-counter-proposal`.
3. Read the receipts (not transcripts). Fold every factual/contradiction/major finding; adopt cheap minors. Re-validate any diagrams and run repo link/ref checkers. Commit.
4. **Each subsequent round** dispatches: (a) a **regression-verifier** briefed with the prior round's fixes BY NAME, returning a COMPLETE/INCOMPLETE verdict per fix and hunting for defects the fixes introduced; plus (b) one or two **rotated personas** for breadth (e.g. a skeptical domain architect, a skim-only PM, a fresh-eyes onboarding engineer). Rotate when prior feedback converges, to widen coverage.
5. Fold findings; commit per round.
6. **Terminate** when a full round returns 0 factual / 0 contradiction / 0 major across all reviewers. Adopt remaining minors, do a final validation pass, and state convergence.
7. If a round still has factual/contradiction/major findings, loop back to step 4.

## Concrete examples

### Example 1: this session's three-round loop

Target: `architectures/v4/implementation-dependencies.md`, just restructured product-first. Goals: products first-class; zero change-narration. Bar: 0 factual / 0 contradiction / 0 major.
- Round 1 (first-time-reader, fact-checker, consistency): 0 factual; R3 found a contradiction — the fence was drawn parallel to the eval tier its C34 holdout depends on. Plus a product-count slip, a W&B license error, two broken anchors. Folded; committed.
- Round 2 (regression-verifier, skeptical architect, skim PM): regression-verifier confirmed "FIX-1 fence/eval: COMPLETE"; the architect found a contradiction (C20 modeled two ways) + a major (missing detect-vs-prevent caveat). Folded → bead-schema became its own product (seven products); committed.
- Round 3 (convergence-verifier, fresh-eyes onboarding engineer): convergence-verifier returned 0 findings / accept-as-is; fresh-eyes returned 0 factual / 0 contradiction / 0 major, "build from this doc: yes." Bar met → adopted three precision minors, validated, converged.

### Example 2: reviewing a new ADR set before adoption

Target: five freshly drafted ADRs. Goals: each decision is unambiguous; alternatives are real; no two ADRs contradict. Round 1: a fact-checker (claims vs the PRs that motivated them), a consistency reviewer (cross-ADR contradictions), a first-time reader (could a newcomer act on each?). Round 2: a regression-verifier on the round-1 fixes plus a skeptical reviewer challenging whether each "decision" is architectural vs tactical. Terminate when a round is clean of factual/contradiction/major findings.

## Anti-patterns

- **Inline-simulated reviewers.** Prose "a skeptic might say…" written by the lead inherits the lead's anchoring. Use real `Agent` dispatches (this repo mandates it).
- **Stopping after round 1.** Round 1 here still had a live contradiction; one round is not the loop.
- **No regression-verifier.** Without a reviewer re-checking prior fixes by name, a fix spread across nine locations can be half-applied undetected.
- **Chasing minors forever.** Once factual/contradiction/major are zero, adopt sensible minors and stop; do not relitigate cosmetics across endless rounds.
- **Reading subagent transcripts into the orchestrator's context.** Take the ≤15-line receipts; full findings stay on disk.
- **Same three personas every round.** Convergent feedback signals it is time to rotate personas for breadth.

## Acceptance criteria

- [ ] Every reviewer is a real subagent with a written on-disk record and a three-tier verdict.
- [ ] From round 2 on, exactly one reviewer per round is a regression-verifier reporting per-fix COMPLETE/INCOMPLETE.
- [ ] The loop terminates only after a full round with 0 factual / 0 contradiction / 0 major findings.
- [ ] Each round produces a commit (artifact fixes + that round's review records).
- [ ] Personas rotate at least once across the loop when feedback converges.

## Files this skill creates / modifies

- `<artifact-dir>/review-*/R<N>-<persona>.md` — one review record per reviewer per round.
- The target artifact(s) — edited to fold findings.
- (No new permanent skill files; this is an orchestration pattern over the `Agent` tool.)
