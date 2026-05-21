# agent instruction

**Before deleting a named artifact, grep the repo for stale references.** Before deleting a skill directory, a template file, a script, a doc, or any other named artifact, run a recursive grep of the repository for references to the artifact's name (and any close synonyms). Update or remove every match before committing the deletion.

*Grounded in: PR #114, where consolidating the `add-issue-behavior` skill into `issue-management` required a `grep -rn "add-issue-behavior\|sibling"` sweep to confirm no stale cross-references survived the delete.*

# justification

When commit `c4d4f8d` removed the `add-issue-behavior` skill directory, the main `issue-management/SKILL.md` had several cross-references — `../add-issue-behavior/SKILL.md` links, "Invoke the sibling skill" anti-patterns, "See also" entries. A pre-delete grep caught all of them in one pass; without it, the merged PR would have shipped with broken links that fail silently until someone clicks.

The marginal cost is one `grep -rn` invocation against the deleted artifact's name. The cost of skipping it is link rot that nobody notices until they need the link — at which point the original author isn't around to remember what the link was for. Names also drift: synonyms ("sibling skill", "sub-skill", "companion") need to be in the grep pattern alongside the literal name. The discipline applies symmetrically when *renaming* an artifact, not just deleting one.
