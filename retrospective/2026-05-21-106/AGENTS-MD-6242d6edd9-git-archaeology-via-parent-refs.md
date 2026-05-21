# agent instruction

**Git archaeology via parent commit refs when visible history is shallow.** When `git log --all -- <file>` returns only a single merge commit or otherwise looks suspiciously empty, the repo's visible history may be shorter than the actual history (squashed import, partial clone, etc.). Walk via the merge commit's parent refs by hash: `git cat-file -p <merge-commit>` to read parent SHAs, then `git log <parent-sha> -- <file>` to walk further back. The parent commits remain accessible by hash even when no ref points at them.

*Grounded in: cleanup-plan v3 — needed historical based-on-commit for syntheses and architecture files; `git log --all` returned only one merge commit until I walked via parents.*

# justification

The session needed historical `based-on-commit` hashes for `research/00-synthesis.md`, `research/13-round-2-synthesis.md`, and the five `architectures/*.md` files (to populate the new metadata header convention). The expected `git log --follow --all -- <file>` invocation returned only one commit per file — `42ed807` (the PR #48 merge). That was suspicious because the synthesis files obviously have edit history.

The fix: `git cat-file -p 42ed807` exposed the parent commit SHAs (`ff0426ee` and `38db197b`), neither of which had a ref pointing at it but both of which were still reachable as git objects. `git log ff0426ee -- research/00-synthesis.md` then surfaced the actual edit history: `f480c8b` (most recent, 2026-05-13), `c495dc9` (2026-05-10), `8b12fa4` (2026-05-10). The "true" last-substantive-edit commits were two-to-three steps deeper than the visible history showed.

This pattern arises any time a repo had its history rewritten, squash-imported, or shallow-cloned. The marginal cost of the check is one extra `cat-file` call when `git log --all` looks too sparse to be true; the cost of trusting the apparent history is anchoring documents on the wrong commit hash forever.
