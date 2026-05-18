<!--
TEMPLATE: main retrospective report
Path target: retrospective/<UTC_DATE>-<PR>.md (forward mode) or retrospective/<UTC_DATE>-<SEQ>.md (no-PR fallback)
Hard cap: ~3500 words. Detail goes into sibling-directory artifacts, not into this report.
Substitute every <ANGLE_BRACKETED_TOKEN> before writing.
-->

# Retrospective — <one-line description of the session's work>

- **UTC date**: <UTC_DATE> (verified via `<tool used — date -u | python3 datetime | node Date.toISOString>`)
- **Last PR**: #<PR> (highest PR number covered by this retro; or `Sequence: <NN>` if no PR exists yet — see Step 1 fallback)
- **Branch at write time**: <branch>
- **Sibling artifacts**: [./<UTC_DATE>-<PR>/](./<UTC_DATE>-<PR>/)
- **Scope**: <SCOPE_LABEL — "full session (from branch divergence)" OR "since <commit-prefix> (previous retrospective in this session)">

## Commit hashes by PR

### PR #<N> — <branch-name> (<open | merged YYYY-MM-DD>)

- `<short-hash>` <subject>
- `<short-hash>` <subject>

<!-- Repeat the `### PR #N` block per PR covered by the retro. -->

## Part 1 — what happened

<!-- Phase-by-phase narrative. Each distinct phase gets a named heading
(`### Phase N — <name>`) and 1–3 paragraphs covering: goal, planned
approach, what actually happened (especially deviations), what was
unplanned but mattered. -->

### Phase 1 — <name>

<paragraph>

### Phase 2 — <name>

<paragraph>

### Metrics

| Metric | Value |
|--------|-------|
| Subagents dispatched | <N> (by category if useful) |
| PRs opened / merged | <M> / <K> |
| Real-world bugs discovered + fixed | <B> |
| Tests added (before / after) | <X> / <Y> |
| Spec amendments | <S> |
| Scenarios driven / skipped | <D> / <Sk> |
| Files touched at major refactors | <F> |

## Part 2 — skills summary

| Skill | ID | Priority | Approx scope | Spec |
|-------|----|----------|--------------|------|
| `<skill-id>` | SKILL-SPEC-<hash> | <high/med/low> | <1–3 words> | [./<UTC_DATE>-<PR>/SKILL-SPEC-<hash>-<skill-id>.md](./<UTC_DATE>-<PR>/SKILL-SPEC-<hash>-<skill-id>.md) |

<!-- One row per skill candidate. Detailed specs are in the sibling
directory at SKILL-SPEC-<hash>-<skill-id>.md (TYPE-HASH-NAME order).
The ID is the durable hash-based identifier. -->

## Part 3 — agents-file suggestions

Proposed additions to the project's agents file (`AGENTS.md`). Each rule
has its own per-rule file in the sibling directory at
`./<UTC_DATE>-<PR>/AGENTS-MD-<hash>-<kebab-name>.md` — the per-rule file
contains exactly two sections: `# agent instruction` (the verbatim rule
text the CI/CD assembler concatenates into `AGENTS.md`) and
`# justification` (the persuasion text the assembler strips out).

This Part 3 mirrors that content inline so the retrospective reviewer
has every proposed rule + its justification in one place at
review-decision time.

### Suggestion 1: <Rule name> — `AGENTS-MD-<hash>`

- **Per-rule file**: [./<UTC_DATE>-<PR>/AGENTS-MD-<hash>-<kebab-name>.md](./<UTC_DATE>-<PR>/AGENTS-MD-<hash>-<kebab-name>.md)

**Proposed agent instruction** (verbatim from the per-rule file's `# agent instruction` section):

> **<Rule name>.** "<The rule, phrased as a do/don't statement, ready
> to paste verbatim into AGENTS.md.>"
>
> *Grounded in: <one-phrase session-event reference>.*

**Justification** (verbatim from the per-rule file's `# justification` section):

<A persuasive paragraph or two. Name the specific session event.
Quantify the cost of not having the rule. State the marginal cost of
adopting it. Make the asymmetry vivid.>

### Suggestion 2: ...

<!-- Repeat per rule. Aim for 5–15 rules. More than 15 is noise — pick
the 15 with the highest signal. -->

## Part 4 — proposed ADRs

Architectural decisions made in this session that the user may want to
record as ADRs. Each candidate has a **full draft** in the sibling
directory, carrying a frozen `ADR-<hash>` ID. The user can adopt any
draft by invoking the `adr` skill, which moves it to
`docs/adr/NNNN-kebab-title.md` while preserving the ID.

| ID | Title | Draft |
|----|-------|-------|
| ADR-<hash> | <Proposed ADR title> | [./<UTC_DATE>-<PR>/ADR-<hash>-<kebab-title>.md](./<UTC_DATE>-<PR>/ADR-<hash>-<kebab-title>.md) |

One-line rationale per draft appears in each draft's `## Context`
opening sentence; no need to duplicate it here.
