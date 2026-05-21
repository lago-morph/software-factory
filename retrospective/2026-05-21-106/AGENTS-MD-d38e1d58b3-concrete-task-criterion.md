# agent instruction

**Concrete-task criterion.** Every entry in a plan doc must be a concrete, executable instruction — exact file paths, exact actions, exact commands or thresholds. "Maybe revisit X someday," "consider Y," or "may want to Z" are not tasks. If an item cannot be reduced to exactly-what-to-do, either move it to a status tracker (sources.json wanted record for source items) or delete it.

*Grounded in: user feedback on cleanup-plan v2 — "there is only work if you can tell me exactly what to do. Otherwise it isn't a task. Use this criteria for all steps."*

# justification

PLAN.md's `## Future research` section had four entries: El Kaim Medium corpus (needed URL harvesting first — not concrete), Noah Radford essay (one URL, one WebFetch — concrete), platform.claude.com Agent Skills (already done — should be deleted), residuals including LukePM / Schillace / jaymin YouTube (mix of done, no-tooling-available, and one genuinely-actionable case). Applying the concrete-task criterion partitioned the four into "delete because done," "delete because not actionable," "move to sources.json as a wanted record," and "keep as one short task because the action is concrete (search the user's laptop)."

Without the criterion, plan docs accrete wishlist items indefinitely. Every reader has to re-evaluate "is this still a task?" on every read. With the criterion, the partition rule is applied at write time once, and the remaining list is uniformly actionable. Marginal cost: 30 seconds per item to ask "can I tell exactly what to do?" Cost of not applying: indefinite wishlist accretion and a doc nobody trusts as a work queue.
