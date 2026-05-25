# Spec: `plain-language-decision-brief`

- **ID**: SKILL-SPEC-c2c5015f81
- **Source retrospective**: ../2026-05-25-180.md

## Intent

When a morning-review item or decision brief returns a "I don't understand your jargon" reply from the user, the resolution is a standalone plain-language explainer document — inline glossary for every term, per-item description in concrete language, per-option cost+reversibility analysis, lead-agent recommendation with reasoning — opened as its own independent PR rather than appended to the original brief or buried in chat. In the 2026-05-25 run, PR #169's morning-review item #3 used "fold", "primitive", "candidate", "common ADR" without inline definitions; the user replied "I have no idea what you mean by 'fold'". PR #172 delivered exactly the explainer this skill specifies, and the subsequent chat conversation converged on Option A through a substrate/methodology/discipline frame that wasn't in the original brief.

## Trigger

Activate when a user response to a morning-review item, decision brief, or PR description is:
- "I don't understand"
- "I have no idea what this means"
- "what is X" (where X is a project term)
- "use straightforward language"
- "use plain English"
- Any semantic equivalent expressing project-jargon overwhelm

Negative trigger: a user asking for technical depth on a specific decision (that's an adversarial-review or technical-deep-dive request, not a plain-language brief).

## Inputs

- The original confusing artifact (the morning-review item, decision brief, PR description).
- The set of terms in that artifact that lack inline definitions.
- The underlying analysis docs (e.g., overlap.md, primitive sketches, candidate-registry) — for reference, NOT to include verbatim.

## Outputs

A standalone markdown document at a topic-appropriate path (e.g., `architectures/v3/decisions/<topic>-plain-language-brief.md`), opened as its own independent PR with base `main` (not stacked on the original brief). Contents:

1. **Audience preamble.** One paragraph: who this is for (project owner who knows WHAT we're doing but not HOW we're describing it), no-jargon promise.
2. **Inline glossary.** Table or bulleted list defining every project term used in the brief. Plain-language definitions; no recursive jargon.
3. **Per-item description.** For each item the brief is asking about, a self-contained paragraph in concrete language describing what it does, who uses it, and what the relevant trade-off is.
4. **Per-option analysis.** Each option named with: what changes, concrete cost, reversibility, lead-agent recommendation reasoning.
5. **"What changes if you pick differently"** with concrete revert paths.
6. **"Where the underlying analysis lives"** pointers at the END (so the reader can dig in if they want, but isn't forced to).

## Workflow

1. Read the user's confused reply carefully. Identify the specific terms / framings they flagged as unclear.
2. Branch off `main` (NOT off the original brief's chain) with a name like `claude/<date>-plain-language-<topic>-brief`.
3. Author the document per the section structure above. Write each section as if the reader has never seen any of the project's internal terminology.
4. Self-check: re-read the document and flag any sentence that uses a term you didn't define inline. Either define it or remove it.
5. Open as an independent PR with base `main`.
6. Post a chat reply pointing the user at the document with a raw URL (per AGENTS-MD-fd63756222).
7. Be prepared for a conversation in chat — the brief often surfaces a deeper framing question that wasn't in the original artifact. Use the `conversational-adjudication-for-stuck-decisions` skill if so.
8. When the user converges on an option, post a resolution comment on the brief PR capturing the conversation's substantive points (not just "Option A").

## Concrete examples

### Example 1: 2026-05-25 PR #172 fold brief

Original: morning-summary morning-review item #3 ("2-candidate primitive fold-in re-check") used "fold", "primitive", "candidate", "common ADR" without definitions. User replied "I have no idea what you mean by 'fold'". The plain-language brief at `architectures/v3/decisions/2-candidate-primitive-fold-plain-language-brief.md` carried: inline glossary (8 terms), per-primitive descriptions (P-25 input-validation perimeter; P-27 legacy-code archaeology; P-24 attribution store; P-30 workflow-engine substrate), three options (A keep all folds / B unfold P-30 / C unfold all four), lead-agent recommendation A with reasoning. The subsequent chat conversation surfaced the substrate/methodology/discipline ADR-layering frame, refined the P-30 risk statement, confirmed Option A. Resolution comment posted on PR #172.

### Example 2: Hypothetical Phase-6 mandate-fit matrix brief

User asks "what's a mandate-fit matrix and why do we need one"? Plain-language brief: glossary for mandate / greenfield / brownfield / unified; per-row description of what each candidate is and what mandate it claims; concrete description of what the matrix lets the reader DO (compare candidates side-by-side on work-unit-class fit); the design question is whether the matrix is one-per-candidate or one-shared. Three options + cost/reversibility per option + recommendation.

## Anti-patterns

- **Editing the original brief instead of writing a new document.** The original brief is the artifact the user was confused by; editing it loses the audit trail of "what wasn't clear the first time". A new document at `<topic>-plain-language-brief.md` carries the explainer as a peer artifact.
- **Cross-referencing the underlying analysis docs without inline summaries.** "See overlap.md for the verdict" is what the user was already trying to do and failing. The plain-language brief INLINES the relevant content (often with a verbatim quote).
- **Glossing terms recursively in terms of other project jargon.** A glossary line like "primitive = a substrate building block" is useless if "substrate" isn't defined. Define top-down: domain → mechanism → vocabulary.
- **Burying the recommendation under analysis.** Lead-agent recommendation goes in a named section near the top OR clearly highlighted near the options; reader shouldn't have to scan for it.

## Acceptance criteria

- [ ] Every project term used in the brief is defined inline (in the glossary or in the term's first use).
- [ ] Per-option analysis includes concrete cost + reversibility.
- [ ] Lead-agent recommendation is named in a dedicated section with reasoning.
- [ ] The brief is opened as an independent PR with base `main`, not stacked on the original brief's chain.
- [ ] A resolution comment is posted on the brief PR after the conversation converges.

## Files this skill creates / modifies

- `<analysis-dir>/<topic>-plain-language-brief.md` — new file.
- The brief PR — opened on its own branch, base `main`.
- A resolution comment on the brief PR after the conversation closes.
