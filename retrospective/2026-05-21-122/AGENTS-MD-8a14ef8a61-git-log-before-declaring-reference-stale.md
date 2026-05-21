# agent instruction

**Grep git log before declaring a doc reference stale.** Before treating a backtick-wrapped path as a broken or stale reference, run `git log --all --follow -- <path>` and also `git log --all -- docs/adr/` for any ADR that documents a directory move. Many "broken" links are actually relocated files that an ADR or recent rename commit ratifies; the correct fix is to update the path to the new location, not to delete the reference. Only after confirming no rename exists should a reference be redirected to a different artifact or removed.

*Grounded in: issue #104 — 20 of the top-30 stale references were a single rename event (`research/00-synthesis.md` → `research/synthesis/00-synthesis.md`) documented by ADR-0004.*

# justification

The issue #104 audit initially classified `research/00-synthesis.md` and `research/13-round-2-synthesis.md` as "broken references". A first instinct is to either delete those references or redirect them to "the synthesis" prose. Both moves would have been wrong: ADR-0004 (`docs/adr/0004-synthesis-subdir-and-based-on-commit-header.md`) records the move from `research/<N>-*.md` to `research/synthesis/<N>-*.md` as a deliberate decision; the file still exists, just at a new path. The right fix is the sed-style rename pre-pass (which the `doc-reference-hygiene` skill includes as a step) that updates the path. One git command — `git log --all --follow -- research/00-synthesis.md` — would have shown the rename history immediately.

Quantified: 20 references plus 5 sibling references for the round-2 file were a single rename event. A "delete the references" approach loses 25 cross-references between documents that should be a single git mv away from working again. Cost of the rule: one `git log --all --follow` invocation per unique stale path. Cost of skipping: cross-document navigation rot that compounds with every future rename. Generalises beyond this repo — every long-lived repo has rename events that mass-stale a class of references, and the ADR log (or `docs/adr/` equivalent) is the curated index of which renames were deliberate.
