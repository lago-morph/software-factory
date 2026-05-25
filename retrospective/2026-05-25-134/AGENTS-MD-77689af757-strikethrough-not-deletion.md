# agent instruction

**Withdraw sections with strikethrough plus pointer, not deletion.** When a section of a doc is being withdrawn (the content is no longer correct), prefer striking the heading through and replacing the body with a short explanation + a link to the resolution doc, over deleting the section outright. Strikethrough preserves the audit trail (a reader scanning prior versions can see what was withdrawn and why); deletion erases the corrective record.

*Grounded in: the GF→BF continuity section in `candidate-registry.md` after the DEC-1.b N/A resolution in PR #134.*

# justification

When DEC-1.b resolved N/A in PR #134, the candidate registry's "Greenfield → brownfield continuity" section was no longer correct content. Two options: delete the section (clean, but removes evidence of the correction), or strike the heading through and replace the body with a short explanation pointing at the resolved-decisions doc. The chosen pattern was strikethrough + pointer:

```markdown
## ~~Greenfield → brownfield continuity~~ — WITHDRAWN

This section originally proposed [...]. The user's actual framing is [...] (see [...]).
```

A reader landing on the registry mid-skim sees both the withdrawal and a one-link path to the corrective context. A reader scanning git history sees the section was struck rather than excised. The cost is a few lines of explanation in place of the deleted content; the benefit is that the corrective signal is durable — it survives future reads, future grep'ing, and future agent passes. Deletion silently erases the lesson; strikethrough makes the lesson part of the record.

Use plain deletion only when the section was wrong from the start (typo, accidental commit), not when it was deliberately authored and later overturned.