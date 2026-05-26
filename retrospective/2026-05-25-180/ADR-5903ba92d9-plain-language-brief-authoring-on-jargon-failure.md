# ADR: Plain-language brief authoring on jargon-failure

- **ID**: ADR-5903ba92d9
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-180.md
- **PRs covered**: #169, #172

## Context

In the 2026-05-25 morning summary (PR #169), morning-review item #3 ("2-candidate primitive fold-in re-check") used project-internal jargon — "fold", "primitive", "candidate", "common ADR" — without inline definitions. The user replied on line 87: "I have no idea what you mean by 'fold'. Write me a decision brief with ALL the information I need to understand the issue and make an informed decision. You keep using jargon that I am not familiar with, and referring to many different documents without concretely saying why you are referring to them. Use straightforward language for someone who knows WHAT we are working on, but is constantly confused by the language you are using when trying to explain HOW we are doing it."

The response was PR #172 — a standalone plain-language explainer at `architectures/v3/decisions/2-candidate-primitive-fold-plain-language-brief.md` with inline glossary, per-primitive plain-language descriptions, three options with cost+reversibility, and lead-agent recommendation. The brief became the conversation-starter for a substantive chat dialogue that surfaced the substrate/methodology/discipline ADR-layering frame (which wasn't in the original morning-summary brief). User converged on Option A.

The pattern: when project-internal jargon obscures a decision from the user, the response is a self-contained explainer, not a longer-and-more-jargon-laden chat reply.

## Decision

**When a user response to a morning-review item, decision brief, or PR description is "I don't understand", "I have no idea what this means", "what is X", or any semantic equivalent, the immediate next artifact is a standalone plain-language explainer authored as its own independent PR.** The explainer:
- Carries an inline glossary for every term used.
- Describes each item in concrete language a reader without project-jargon background can grasp.
- Provides per-option analysis with concrete cost + reversibility.
- States the lead-agent recommendation in a named section with reasoning.
- Points at the underlying analysis docs at the END (so the reader can dig in if they want, but isn't forced to).

The explainer is opened as its own PR with base `main` (NOT stacked on the original brief). After conversation converges, a resolution comment is posted on the explainer PR capturing the decision.

## Alternatives considered

- **Reply in chat with a longer explanation.** Rejected because chat is ephemeral; the explanation evaporates when the session ends. A document with its own PR is durably referenceable. The user explicitly asked for "a decision brief with ALL the information", not for a longer chat reply.
- **Edit the original brief to add definitions in place.** Rejected because the original brief is the artifact the user was confused by; editing it loses the audit trail of "what wasn't clear the first time". A new document at `<topic>-plain-language-brief.md` carries the explainer as a peer artifact.
- **Cross-reference the underlying analysis docs.** Rejected because that's exactly what the user was already trying to do and failing. The plain-language brief INLINES the relevant content (often with verbatim quotes); cross-references go at the END for optional further reading.

## Consequences

**Easier:** When project-jargon obscures a decision, the agent has a concrete recipe to fix it. The user can adjudicate cleanly. The brief itself often surfaces missing framings (as the PR #172 conversation surfaced the substrate/methodology/discipline layering) that improve the underlying decision quality.

**Harder:** Authoring a plain-language brief is ~30 minutes of focused work — substantially more than a chat reply. The agent must self-discipline against the temptation to just over-explain in the next chat message.

**Trade-off accepted:** Extra authoring time on jargon-confusion events in exchange for durable, navigable explainers that improve user adjudication quality.

**Explicitly NOT promising:** the rule doesn't apply to every "I have a question" reply from the user. It applies when the user explicitly flags jargon as the obstacle ("I don't understand", "what is X", "use plain language", "what does Y mean"). A user asking for technical depth on a specific decision is a different request and gets a different response.

## References

- [`../2026-05-25-180.md`](../2026-05-25-180.md) — source retrospective.
- [`./AGENTS-MD-ae9e368ef6-plain-language-brief-on-jargon-confusion-response.md`](./AGENTS-MD-ae9e368ef6-plain-language-brief-on-jargon-confusion-response.md) — per-rule agents-file addition.
- [`./SKILL-SPEC-c2c5015f81-plain-language-decision-brief.md`](./SKILL-SPEC-c2c5015f81-plain-language-decision-brief.md) — the operational skill spec.
- [`./SKILL-SPEC-ee35b95172-conversational-adjudication-for-stuck-decisions.md`](./SKILL-SPEC-ee35b95172-conversational-adjudication-for-stuck-decisions.md) — companion skill for the conversation that the brief usually triggers.
- PR #169 line 87 — user-rebuke commit-of-record.
- PR #172 — the plain-language brief produced in response.
