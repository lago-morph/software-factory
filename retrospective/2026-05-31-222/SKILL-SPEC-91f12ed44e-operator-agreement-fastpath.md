# Spec: `operator-agreement-fastpath`

- **ID**: SKILL-SPEC-91f12ed44e
- **Source retrospective**: ../2026-05-31-222.md

## Intent

When a user has been handed a written decision document (a decisions-to-make doc, a recommendations memo, a brief with a numbered options table) and replies with a blanket "I agree with your recommendations," the agent should treat that as the binding answer to every item — recording each as a numbered ledger decision and applying it — rather than re-walking the same questions through an interactive question tool. In this session the prompt instructed the agent to use `AskUserQuestion` to walk the operator through six decision items; the operator had already replied "I agree with your recommendations in decisions-to-make.md" before the agent reached that step. Re-asking would have been redundant friction. The skill encodes the recognition that agreement-on-the-document is itself the decision, and the correct next action is to transcribe-and-apply, not to re-elicit.

## Trigger

Activate when **all** of these hold:
- A written artifact with explicit, enumerated recommendations exists (a decisions doc, an options table with a "my recommendation" column, a brief with adopt/defer verdicts).
- The user issues a blanket acceptance: "I agree with your recommendations," "go with your recommendations," "all of them look good," "approved," "do what you suggested."
- The acceptance is not scoped to a subset ("I agree with 1 and 3 but not 2" routes to per-item handling, NOT this fast-path).

Negative triggers: do NOT fast-path when the user's reply introduces a new constraint, picks a non-recommended option, or expresses any reservation — those require per-item engagement. Do NOT fast-path a document that has no explicit recommendation per item (there is nothing to transcribe).

## Inputs

- The decision document (path + contents), with one recommendation per item.
- The user's acceptance message.
- The target decision ledger (e.g. `architectures/v4/_meta/review-log.md`) and its existing decision-id series (e.g. `D-19` → next is `D-20`).
- Any "rewind path" / affected-component notes the decision doc already carries per item.

## Outputs

- One numbered binding decision per item, appended to the ledger, each citing the source doc and the user's agreement with a date.
- Any provisional ruling the items confirm is flipped to adopted (e.g. a `PROVISIONAL` decision → `ADOPTED`).
- The mechanical edits the decisions imply (a one-line wiring fix, a status flip) applied in the same pass.
- A short confirmation to the user mapping each item to its recorded decision id.

## Workflow

1. Read the decision document in full; extract the per-item recommendation and the affected components/rewind path each item names.
2. Find the ledger's current highest decision id; the next decision starts there.
3. For each item, write a numbered ledger entry: the decision verbatim from the recommendation, marked ADOPTED, attributed to the user + date, citing the source doc item number.
4. If an item confirms a previously-PROVISIONAL ledger decision, edit that decision in place: flip PROVISIONAL→ADOPTED and cross-reference the new confirming id.
5. Apply any mechanical edit an item authorizes (a dependency-edge fix, a one-line annotation), and resolve the corresponding open-question/cross-component rows in the ledger.
6. Commit and push the ledger + mechanical edits as one wave.
7. Reply to the user with a compact table mapping each source-doc item to its recorded decision id; do NOT re-ask via an interactive tool.

## Concrete examples

### Example 1: the six-item decisions doc (this session)

Input: `decisions-to-make.md` carries six items, each with a "my recommendation (opinion)" line; the user replies "I agree with your recommendations in decisions-to-make.md." The prompt separately said to use `AskUserQuestion` for items 1 and 2.

Action: recognized the blanket agreement as binding for all six. Recorded D-20..D-25 in `review-log.md` (one per item), flipped the provisional D-18 to ADOPTED (item 1 confirmed it), applied the one mechanical edit (item 5: the C46 dependency edge `C33, C24` → `C33, C21, C25`), and resolved the matching open-question rows (XC-8, C54:OQ-3, C57:OQ-C57-3, C46:OQ-6). Replied with a six-row table mapping item→decision-id. No `AskUserQuestion` call was made.

### Example 2: partial agreement (negative case)

Input: a 4-item brief; user replies "agree with everything except #3, let's defer that one."

Action: fast-path items 1, 2, 4 as adopted ledger entries; route item 3 to per-item handling (record it as deferred with the user's stated reason, or ask the one scoped follow-up the deferral raises). The blanket fast-path does NOT apply because the acceptance was scoped.

## Anti-patterns

- **Re-asking what the user already answered.** When the user has accepted the document, invoking an interactive question tool to re-present the same options is redundant friction — it reads as the agent not having absorbed the reply. Cite the moment: the prompt said "use AskUserQuestion for #1 and #2," but the operator had already agreed in writing.
- **Transcribing without applying.** Recording the decisions in the ledger but skipping the mechanical edits they authorize leaves the corpus inconsistent with its own decision log. Apply the wiring fix / status flip in the same wave.
- **Losing the provisional-flip.** If an accepted item confirms an earlier provisional ruling, forgetting to flip it leaves two conflicting states (PROVISIONAL in one place, ADOPTED in another).

## Acceptance criteria

- [ ] Every item in the source document has exactly one numbered, dated, attributed ledger decision.
- [ ] Any provisional ruling the items confirm is flipped to adopted, with a cross-reference.
- [ ] Every mechanical edit the decisions authorize is applied in the same wave, and the corresponding open-question rows are resolved.
- [ ] No interactive re-asking tool was invoked for an item the user already accepted.
- [ ] The user receives a compact item→decision-id mapping.

## Files this skill creates / modifies

- `<decision-ledger>.md` (e.g. `architectures/v4/_meta/review-log.md`) — appends one binding decision per accepted item; flips confirmed provisionals.
- The component/spec/inventory files any accepted item authorizes a mechanical edit to.
