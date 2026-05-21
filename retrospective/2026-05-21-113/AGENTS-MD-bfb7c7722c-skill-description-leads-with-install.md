# agent instruction

**Lead self-installing skill descriptions with the install command.** For any skill that ships derived artifacts requiring local installation, the frontmatter `description` field must lead with the install command itself — not a summary, not the trigger list. The trigger list goes AFTER. The reasoning: the description is what an agent sees when deciding whether to use the skill, and the install must happen before any other action; placing the install command in the first sentence makes it physically impossible to invoke the skill without seeing the install. The SKILL.md body must mirror this by placing the pre-flight section above the intro paragraph behind a STOP header.

*Grounded in: PR #113 — user direction "the skill must not be a manual step they have to remember" required moving the install command to the top of both the description and SKILL.md.*

# justification

The original `architecture-failure-mode-gate` SKILL.md had its pre-flight at section position 2 (after the intro paragraph), which is where the existing `research-pipeline` and `self-bootstrapping-skill` examples place it too. The user judged that insufficient — burying the pre-flight even one section below the H1 was enough that "agents skip pre-flights when they're buried below the interesting content." The fix is to make the install command the first content the agent sees in BOTH surfaces: the frontmatter description and the SKILL.md body. The marginal cost is reordering two paragraphs. The benefit is removing the entire failure mode of "agent forgets to run the install" — and the user's explicit reason for asking is that they have repeatedly seen this failure mode in this repo.
