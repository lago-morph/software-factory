# agent instruction

**based-on-commit header on syntheses and architecture decisions.** Every synthesis document and every architecture decision document carries a YAML frontmatter at the top recording the commit and date the document is grounded in:

```yaml
---
based-on-commit: <short-hash>
based-on-date: YYYY-MM-DD
---
```

The hash + date are historical (when the document was last substantively edited, not when the header was added), so a future reader can tell what corpus state the document's claims sit on.

*Grounded in: user request during cleanup-plan v2 — "Metadata at the top indicating commit on which we based our syntheses. Put that same information in all files in architecture directory."*

# justification

Syntheses (and architectures-as-decisions) age in a particular way: they remain valid only as long as the corpus they synthesize doesn't shift underneath them. `research/00-synthesis.md` was authored against a 7-report corpus; by session time the corpus held 38 reports + 14 followups. Without a `based-on-commit` header, a reader six months from now has no way to tell whether the synthesis's claims have been overtaken by subsequent research or remain current — they have to manually reconstruct the historical corpus state.

The header costs nothing to write (three lines), nothing to update (only when the document is substantively edited — the header records the edit's commit), and gives a reader an O(1) answer to "what corpus state does this document grok?" Same logic applies to `architectures/*.md`: each architecture spec is a decision made against a snapshot of the research corpus; recording the snapshot's commit lets a future reader cite the spec accurately, reproduce its reasoning, or argue it's stale.

Cost of not having the header: every reader has to do git-log archaeology per document to find its commit grounding, or — more likely — never bothers and treats the document as timelessly current, which it never is.
