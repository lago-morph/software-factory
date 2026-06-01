# agent instruction

**State what a living document is, not how it changed.** In a document meant to be read fresh — a spec, build order, design doc, or README — do not narrate edit history or the prior version ('this replaces the old X', 'unchanged below', 'now leads with', 'two corrections', 'you asked'). Change-narration and conversation-anchoring bewilder a first-time reader and drift stale; state the current truth directly and let git history record how it changed.

*Grounded in: removing pervasive change-narration from implementation-dependencies.md as the second of the two requested fixes.*

# justification

Half of this task was deleting sentences that told the reader how the document had evolved rather than what it now says: "This replaces the old single-line long pole," "the original view, unchanged below," "Two corrections worth calling out," "the old phase-5 line is corrected by this split," "You asked a sharp question." Every one of these made sense to the editor who wrote them and was noise to a first-time reader, who has no "old version" in mind and no memory of the conversation. The user's words: "We don't care how it changed, we care what it is. The references to changes are bewildering to a first time reader." The cost of leaving them in is a document that reads like a changelog wearing a spec's clothes, and that goes stale the moment the thing it contrasts against is forgotten. The marginal cost of the rule is near zero — it is easier to write the current truth plainly than to write the comparison. This is the document-content analogue of the existing "address user confusion directly, not via meta-honesty sections" rule: keep the meta-narration out of the artifact.
