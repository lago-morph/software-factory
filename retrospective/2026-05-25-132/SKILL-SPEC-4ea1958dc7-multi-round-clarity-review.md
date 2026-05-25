# Spec: `multi-round-clarity-review`

- **ID**: SKILL-SPEC-4ea1958dc7
- **Source retrospective**: ../2026-05-25-132.md

## Intent

When a load-bearing document needs to be defensible by readers outside the authoring context, single-pass authoring produces undetected clarity drift. The skill dispatches fresh-context reviewers in successive rounds, each with a stable persona and a constrained glossary, applying findings between rounds, until no MEDIUM-severity findings remain. The loop terminates naturally: each round's reviewer finds smaller and smaller issues until the document is genuinely defensible. Grounded in the v3-synthesis primer iteration: 6 rounds, each finding 2-7 MEDIUMs the prior round missed, until round 6 reported "no HIGH and no MEDIUM findings; the document ships."

## Trigger

**Direct triggers** (activate immediately):
- "Review this document for clarity until no major findings remain"
- "Iterate the doc"
- "Loop review on `<file>`"
- "Multi-round review"

**Proactive triggers** (offer the skill):
- A document was just authored that downstream readers must use without consulting the authoring conversation (handoff docs, primers, decision briefs, architecture specs).
- A document has been described by the user as "load-bearing" or "stand-alone."
- A single-round review surfaced HIGH or MEDIUM findings (offer to iterate).

**Negative triggers** (do NOT use):
- The document is throwaway scratch.
- The user explicitly says "single-pass review only."
- The audience is the authoring context (e.g., scratch notes between sub-tasks of the same session).

## Inputs

- **Document path** (required): absolute path to the markdown file under review.
- **Reviewer persona description** (required): 2-4 sentences specifying who the reviewer is, what knowledge they have, what knowledge they do *not* have. Stability matters — the same persona is reused across rounds.
- **Constrained glossary** (optional but strongly recommended): a list of source-level vocabulary the reviewer is allowed to know without the document defining it. Prevents the reviewer from filling in gaps with outside knowledge that real downstream readers won't have.
- **Exit criterion** (optional, default: "0 HIGH and 0 MEDIUM findings"): how to know the loop is done.
- **Maximum rounds** (optional, default: 10): hard ceiling to prevent runaway loops.

## Outputs

- Updated document (in place) with findings applied between rounds.
- Per-round commit on the current branch with message `<doc>: apply round-N clarity review fixes`.
- A short termination message stating which round met the exit criterion and the final residual LOW findings (if any).

## Workflow

1. Confirm the document path and read the current state. Verify it's a markdown file under git.
2. For round N (start at 1):
   a. Dispatch a fresh-context subagent (subagent_type `general-purpose`) with the brief: persona description + constrained glossary + document path + exit criterion + output format. Brief specifies "this is round N; prior-round findings have been incorporated."
   b. Wait for the subagent's structured response (findings sorted by severity, with location + quote + fix recommendation per finding).
   c. If the subagent reports "0 HIGH and 0 MEDIUM findings" — exit loop, proceed to step 4.
   d. Apply all HIGH and MEDIUM findings to the document via Edit calls. LOW findings are optional; apply if cheap, defer if not.
   e. Commit with message `<doc>: apply round-N clarity review fixes` listing what was fixed and why.
   f. If N == max-rounds — exit loop with warning that the exit criterion was not met.
   g. Increment N, go to (a).
3. (Implicit in 2c, 2f.)
4. Print termination summary: round count, total findings applied, residual LOW findings (if any), exit reason.

## Concrete examples

### Example 1: primer iteration (the source-session example)

Input:
- Document: `research-plan-v3-primer.md` (a ~3000-word process primer)
- Persona: experienced software developer (10+ years) familiar with software-factory vocabulary but no knowledge of the specific synthesis methodology or any intermediate artifacts
- Glossary: 18 corpus-level terms (software factory, lights-out, greenfield/brownfield mandates, substrate, methodology, harness, L0-L5, K=5 consistency, etc.)
- Exit criterion: 0 HIGH and 0 MEDIUM
- Max rounds: 10

Round 1 returned 0 HIGH, 7 MEDIUM, 5 LOW. Fixes applied: blind-axis test defined fully on first use; methodology shape concretized with examples; bare identifiers (DEC-N, ADR-N) scrubbed or glossed inline. Commit: "primer: apply round-1 clarity review fixes."

Rounds 2-5 followed the same pattern; finding counts decreased (4 MEDIUMs round 2, 1 MEDIUM round 3, 3 MEDIUMs round 4, 2 MEDIUMs round 5). Each round surfaced previously-invisible issues that fixing prior rounds opened up.

Round 6 returned "No HIGH and no MEDIUM findings; the document ships." Termination. Total: 6 rounds, ~22 issues applied, ~30-50 minutes of subagent time.

### Example 2: hypothetical architecture-spec iteration

Input:
- Document: `architectures/v3/greenfield-spec.md` (a draft architecture specification)
- Persona: senior engineer about to implement the spec; familiar with cloud infrastructure and CI/CD but no prior knowledge of the v3 synthesis or its tracks
- Glossary: 12 implementation-vocabulary terms (substrate primitives, methodology layer, ADRs, etc.)
- Exit criterion: 0 HIGH and 0 MEDIUM

Expected pattern: round 1 finds implementer-blocking issues (missing API contracts, undefined dependencies); round 2 finds operational-blocking issues (no deployment recipe, no failure-mode runbook); rounds 3-4 polish. Termination by round 4-5.

## Anti-patterns

- **Single-pass review.** A single round will not catch the deepest clarity issues, because the document's author shares context with the reviewer (even if dispatched to a fresh subagent — the brief itself carries authoring frame). The compound effect of multiple rounds is what produces the genuine clarity gain.
- **Reusing the same persona across substantively different documents.** The persona must match the audience. A primer's reviewer is not an architecture-spec implementer.
- **Letting reviewers fill in gaps from outside knowledge.** Without a constrained glossary, reviewers default to "I know this from training data so it doesn't need to be in the doc." Real downstream readers may not have that training. The glossary is the constraint that produces useful findings.
- **Continuing past the exit criterion.** Once 0 HIGH and 0 MEDIUM is reached, stop. Additional rounds chase LOW findings that are usually copy-edit issues, not clarity issues. Save the budget for the next document.
- **Skipping the commit between rounds.** Each round's findings + fix should be a separate commit, so the audit trail shows which round produced which improvement. Bulk-committing at the end loses the round-by-round attribution.

## Acceptance criteria

- [ ] Document is updated in place between rounds.
- [ ] Each round produces a commit with the round number in the message.
- [ ] Loop terminates either at "0 HIGH and 0 MEDIUM" or at max-rounds (with explicit warning).
- [ ] Termination summary names round count + final residual findings + exit reason.
- [ ] No round dispatches without the persona + glossary inputs being included in the brief.

## Files this skill creates / modifies

- `<document-path>` — modified in place per round
- (git commits on current branch; no new files)
