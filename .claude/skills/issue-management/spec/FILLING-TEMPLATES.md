# Filling the issue-management comment templates

This document explains how to fill each placeholder in each template
without breaking the visual consistency described in
[`../SKILL.md`](../SKILL.md).

## Shared placeholders

These placeholders appear in more than one template and have the same
meaning everywhere.

| Placeholder | What to put | Example |
|---|---|---|
| `{{TIMESTAMP_UTC}}` | ISO-8601 UTC timestamp with `Z` suffix, second precision. Do not localize. | `2026-05-21T14:30:00Z` |
| `{{BRANCH_NAME}}` | The git branch the agent is working on. Wrap it in backticks where the template already shows backticks; otherwise leave it bare. | `claude/issue-management-skill-M9IUN` |
| `{{SESSION_SHORT_ID}}` | A short identifier the user can use to disambiguate sessions. Use the last 8 chars of the session ID if available, or the wall-clock minute (`HHMM`) if not. Never put the full session URL — that's noise. | `M9IUN` or `1430` |
| `{{ISSUE_NUMBER}}` | The issue number without `#`. The template adds the `#`. | `111` |

## STARTED — `comment-started.md`

| Placeholder | What to put |
|---|---|
| `{{ONE_OR_TWO_SENTENCE_PARAPHRASE_OF_ISSUE}}` | The agent's restatement of the goal in its own words. This is the artifact that lets the user catch misunderstandings *before* code lands. Do not quote the issue body verbatim — the value here is the *interpretation*. |
| `{{NUMBERED_LIST_OF_FIRST_STEPS_OR_THE_WORD_INVESTIGATING}}` | A short numbered list (1-4 items) of concrete first steps. If the agent has not investigated yet, the single word `Investigating.` is acceptable. |

**Tone**: declarative, present-tense, brief. The STARTED comment is a
"hello, I'm here, I'm working on it" signal — not a design doc.

## QUESTIONS — `comment-questions.md`

| Placeholder | What to put |
|---|---|
| `{{N}}` | The integer number of questions, used in the summary line. |
| `{{WHAT_IS_BLOCKED_OR_NONE}}` | Short phrase naming what the agent can't do without answers. If the agent can keep working on adjacent parts, write `none` and the user knows there's no urgency. |
| `{{QUESTION_K}}` | One question per numbered slot. **Keep each to one sentence.** If a question needs context, put the context in the "Why I'm asking" section, not in the question itself. Phrase each so a one-word or one-line reply is sufficient. |
| `{{ONE_OR_TWO_SENTENCE_CONTEXT_FOR_WHY_THESE_MATTER_NOW}}` | Why the answers matter at this moment. Often "I'm at a decision point between A and B." |
| `{{THE_DEFAULT_OR_THE_WORDS_WILL_PAUSE_AND_WAIT}}` | What the agent will do if the user can't answer in time. Either name a default (and commit to it), or write `Will pause and wait.` Never both. |

**Number of questions per comment**: 1–5. If you have more than 5, you're
fishing rather than blocked; pick the top 3 that actually gate the work.

## ANSWERS — `comment-answers.md`

| Placeholder | What to put |
|---|---|
| `{{N}}` | Number of questions being answered. Should match the prior QUESTIONS comment's count. |
| `{{LINK_OR_NUMBER_OF_PRIOR_QUESTIONS_COMMENT}}` | A GitHub permalink to the prior `[QUESTIONS]` comment, or a short reference like "the QUESTIONS comment above" if the prior comment is the immediately preceding one. |
| `{{ISSUE_THREAD_OR_CHAT}}` | Either `the issue thread` or `chat`. This is how a reader knows whether the answers are visible above this comment or whether the ANSWERS summary is their only record. |
| `{{QUESTION_K_ONE_LINE}}` | Restate each prior question in one line — do not repaste the full original phrasing. This pairing in one comment makes the comment self-contained. |
| `{{SUMMARIZED_ANSWER_K}}` | The agent's understanding of the user's answer, in the agent's words. If the user gave a non-answer ("not sure"), say so explicitly. |
| `{{ONE_OR_TWO_SENTENCES_ON_WHAT_CHANGES_NOW}}` | The actionable effect: which option got chosen, which design got dropped, which file gets touched next. The whole point of the ANSWERS comment is the line *after* the Q/A pairs. |

**Re-ordering**: The Q/A pairs MUST appear in the same order as the
original QUESTIONS comment. Same numbers. Same sequence. This is what
lets a reader skim "Q1 → A1, Q2 → A2" without thinking.

## PR-OPENED — `comment-pr-opened.md`

| Placeholder | What to put |
|---|---|
| `{{PR_NUMBER}}` | The PR number without `#`. |
| `{{PR_TITLE}}` | The PR title exactly as it appears in the PR. |
| `{{PR_URL}}` | The PR's `https://github.com/...` URL. |
| `{{BASE_BRANCH}}` | The PR's base branch (usually `main`, sometimes a parent feature branch per `stacked-pr-on-feature-branch`). |
| `{{DRAFT_OR_READY_FOR_REVIEW}}` | Either `ready for review` (default per `AGENTS.md`) or `draft`. Match the actual PR state. |
| `{{ONE_OR_TWO_SENTENCE_PR_SUMMARY}}` | A short description of what the PR does. This should be a *shorter* version of the PR body's summary, not a copy of the PR title. |
| `{{BULLETED_OR_NONE_LIST_E_G_CI_GREEN_USER_REVIEW_DOCS_PATCH}}` | A short bulleted list of what needs to happen before merge, or the word `none` if the PR is ready to merge as-is. Common items: "CI green", "user review", "address review comments". |

**Verify `Closes #N` before posting.** The template asserts the PR body
contains it; if you haven't actually put it in the PR body, either
update the PR (preferred — `mcp__github__update_pull_request`) or remove
that paragraph from the comment before posting (a lie on the issue
thread is worse than a missing convenience).

## General authoring rules

- **No emojis.** Project style.
- **No nested blockquotes inside the body.** They visually merge with
  the header bar and ruin the silhouette.
- **No trailing whitespace and no stray empty lines.** GitHub renders
  these as visible gaps and breaks the uniform feel.
- **Always include the machine marker HTML comment** at the end. It's
  how future automation grep's for skill-emitted comments.
- **When in doubt, less is more.** These comments are signals, not
  documents.
