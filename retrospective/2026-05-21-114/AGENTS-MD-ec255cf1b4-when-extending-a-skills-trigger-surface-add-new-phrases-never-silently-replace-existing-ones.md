# agent instruction

**When extending a skill's trigger surface, add new phrases; never silently replace existing ones.** When the user proposes a new or more-specific trigger phrasing for an existing skill, ADD it to the trigger surface alongside the existing phrasings. Treat existing triggers as user-facing affordances: removing them without explicit instruction breaks discoverability for users who learned the old phrasings.

*Grounded in: PR #114 — the user requested a more specific modify-behavior trigger; I over-narrowed and removed the looser phrasings; the user corrected: "I want the trigger phrases we had for everything else. Maybe add this as a general trigger phrase also. But keep the old ones too."*

# justification

When I consolidated the `add-issue-behavior` skill into `issue-management` and adopted the user's new canonical *"I want to (action) issue behavior (name)"* phrasing, I dropped the original looser triggers ("add a behavior to the issue skill", "change the X behavior", "the STARTED comment should also …", etc.). The user noticed immediately and corrected me. Trigger phrases are user-facing API: every existing phrasing represents a way the user (or future agents) might naturally express the request.

The marginal cost of keeping the old phrasings is a few lines of description text in the frontmatter and a short bullet list in the body. The cost of dropping them is a missed trigger plus a round-trip to re-add. Trigger removal must be explicit ("drop this phrasing because X") — never a side-effect of phrasing-replacement work.
