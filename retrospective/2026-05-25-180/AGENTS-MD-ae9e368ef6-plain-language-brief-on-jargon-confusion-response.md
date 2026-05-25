# agent instruction

**Plain-language brief on jargon-confusion response.** When a user response to a morning-review item, decision brief, or PR description is "I don't understand", "I have no idea what this means", "what is X", or any semantic equivalent, the immediate next artifact is a standalone plain-language explainer authored as its own independent PR. The explainer carries an inline glossary for every term used, per-item description in concrete language a reader without project-jargon background can grasp, and per-option analysis with concrete cost + reversibility. Do NOT respond with a longer chat reply, an edit to the original brief, or a cross-reference to the underlying analysis docs.

*Grounded in: PR #169 line-87 ("I have no idea what you mean by 'fold'... Use straightforward language for someone who knows WHAT we are working on, but is constantly confused by the language you are using when trying to explain HOW we are doing it") — produced PR #172 as the plain-language brief; the subsequent chat conversation converged on Option A through substrate/methodology/discipline layering that wasn't in the original brief.*

# justification

The 2026-05-25 morning summary's morning-review item #3 ("2-candidate primitive fold-in re-check") used "fold", "primitive", "candidate", "common ADR" without inline definitions. The user wasn't asking for more cross-references to docs that defined these — they were asking for a self-contained explainer. PR #172 delivered exactly that (~120 lines with inline glossary + per-primitive plain-language descriptions). The brief became the conversation starter that surfaced the substrate/methodology/discipline ADR-layering frame the agent had been implicitly assuming.

Cost of the rule: a focused ~30-minute authoring task per jargon-confusion event. Substantially more than a chat reply, but the chat reply would have been longer-and-more-jargon-laden — the user explicitly asked for "ALL the information I need to understand the issue and make an informed decision", not for more talking.

Asymmetric cost without: the user either stays confused and rubber-stamps the recommendation (losing decision quality) or has to round-trip multiple times for clarification (losing trust in the decision being made). The PR #172 conversation specifically converged on Option A through frames that hadn't been in the original analysis — the explainer-driven discussion was higher-quality decision-making than the original morning-summary recommendation would have been.

The rule applies on explicit jargon-flag signals: "I don't understand" / "what does X mean" / "use plain language" / "I have no idea what this means". A user asking for technical depth on a specific decision is a different request and gets a different response.
