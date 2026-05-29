# Spec: `sample-first-merge-signoff`

- **ID**: SKILL-SPEC-a1383f3d95
- **Source retrospective**: ../2026-05-29-211.md

## Intent

For multi-part deliverables where the parts share a format that needs validation, ship the first sample as its own PR with the format established but only one part complete. Wait for the PR to merge (treating merge as the signoff signal). Then ship the remaining parts in a second PR. Prevents producing N parts in a wrong format that all need rework. Used successfully for the v3 build-guide items 5-6 (GF-M sample in PR #206, then 9 others in PR #207).

## Trigger

**Direct triggers**:
- User asks for "10 X" or "one per Y" or "N parts of Z" where format consistency matters.
- User says "sample-first" explicitly.
- A multi-part deliverable is starting where part-1 and part-N share format.
- Slash-command: `/sample-first <deliverable-name>`.

**Proactive triggers**:
- About to produce ≥3 parts of similar shape (per-candidate documents, per-component specs, per-X reports).
- The format involves diagrams, tables, or other structure that's expensive to redo.
- The user is likely to want format adjustments (they have strong preferences).

**Negative triggers**:
- Only 1-2 parts (sample-first is overhead for n=2).
- Format is trivial (plain prose, single paragraph each).
- User has explicitly approved the format already.

## Inputs

- The set of parts to produce (e.g., "10 candidates", "5 modules").
- The proposed format (shape of each part).
- A representative part to ship first (the sample candidate).
- Optional: the user's explicit signoff criteria.

## Outputs

- **PR #1**: The sample part fully complete, the other parts stubbed/skeletal with explicit "pending sample-first signoff" markers. PR description names the format conventions used and lists what to look at (specific cells in tables, diagram shapes, prose tone).
- **Wait**: PR #1 merges → signoff achieved.
- **PR #2**: The remaining parts, all in the established format. Brief PR description noting the format was signed off in PR #1.

## Workflow

1. **Identify the part set.** Confirm there are ≥3 parts and the format matters.
2. **Pick the representative sample.** Should be:
   - Average complexity (not the easiest, not the hardest).
   - Exercising all the format's load-bearing decisions.
   - User-suggestable if applicable ("which candidate should be the sample?").
3. **Establish the format with the sample.** Write the sample part with every format element present.
4. **Stub the other parts.** Each gets a "stub" or "pending" marker in the same file structure.
5. **Open PR #1.** Description: "Sample-first for X. PR has the format established with <sample part>; the other N parts are stubbed pending signoff. Look at: <specific format aspects>."
6. **Wait for merge.** Treat merge as the explicit signoff. Do NOT proceed to PR #2 before merge.
7. **Open PR #2 with the remaining parts.** Same file(s), other parts now filled in matching the sample's format. Brief PR description noting format was established in PR #1.
8. **Verify format consistency.** Before opening PR #2, spot-check at least 3 parts against the sample to ensure format match.

## Concrete examples

### Example 1: v3 build-guide items 5-6 (the canonical case)

**Input**: 10 v3 candidate methodologies need per-candidate methodology diagrams + discipline binding tables + substrate composition diagrams.

**Sample**: GF-M chosen (cheapest candidate, exercises all format decisions: methodology diagram with multi-step flow, discipline table with multiple ✓ rows, substrate diagram with custom component, prose paragraph about when to reach for it).

**PR #1** (PR #206):
- File created with all 10 sections.
- GF-M section fully complete (3 diagrams, 1 table, prose paragraph).
- Other 9 sections stubbed with "(pending GF-M signoff)" markers.
- PR description: "Sample-first for build-guide items 5-6. GF-M is the representative. Look at: (1) methodology diagram element count and choice of nodes, (2) discipline binding table format with 'why GF-M binds' column, (3) substrate diagram conventions (NEW annotation, dotted edges for connections to custom piece), (4) prose paragraph length and conversational tone."

**Merge → signoff achieved.**

**PR #2** (PR #207):
- Same file.
- 9 remaining candidates filled in matching the GF-M format.
- Brief PR description: "Builds on PR #206 format. 9 candidates × 3 artifacts each = 27 new diagrams, all matching GF-M's conventions. Plus discipline tables and prose paragraphs."

**Result**: Zero format rework. 30 Mermaid diagrams shipped with zero rendering bugs.

### Example 2: hypothetical per-module specs

**Input**: 5 modules each need a one-page spec.

**Sample**: Pick the module with the most cross-cutting concerns. Write its spec fully. Stub the other 4 with their names and "(pending signoff)".

**PR #1**: Sample spec + 4 stubs. "Look at: section structure, level of detail on contracts, format of error case enumeration."

**Merge.**

**PR #2**: 4 remaining specs filled in.

## Anti-patterns

- **Producing all N parts in PR #1.** Defeats the purpose. If format is wrong, all N need rework.
- **Skipping the sample because "the format is obvious".** Format is rarely obvious to the reader; sample-first surfaces disagreements early.
- **Treating "I'll just do it and ask for feedback" as equivalent.** Feedback on N-part documents is hard to give precisely. PR-level signoff is concrete.
- **Picking the easiest part as the sample.** It won't exercise the format's load-bearing decisions. Pick average complexity.
- **Starting PR #2 before PR #1 merges.** Even with verbal approval. Wait for the merge.
- **Ignoring format adjustments between PR #1 and #2.** If feedback comes during PR #1 review, fold it in before PR #2 opens.

## Acceptance criteria

1. PR #1 has exactly one part fully complete and others stubbed.
2. PR #1 description names what to look at (≥3 specific format aspects).
3. PR #2 doesn't open until PR #1 is merged.
4. PR #2's parts visibly match the sample's format (spot-checked).
5. The user's reaction to PR #2 is approval, not "let's redo the format".

## Files this skill creates / modifies

- The deliverable file(s) — same file across both PRs, but different fill-levels.
- Optional: a CONVENTIONS.md or HANDOFF.md noting the format established in PR #1.
