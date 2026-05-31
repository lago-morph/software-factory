# agent instruction

**Distrust empty or truncated tool output; re-verify before a destructive action.** When a Bash or Read result comes back empty, truncated, or visibly garbled, treat the underlying state as unknown — re-run a narrowed, deterministic check — before overwriting, deleting, or reverting on the basis of it.

*Grounded in: a stretch of this session where Bash returned empty/garbled output, leading to a good committed file being overwritten with an inferior reconstruction that then had to be restored from git.*

# justification

Mid-session the Bash tool intermittently returned empty or truncated output. Acting on one such corrupted read, I concluded a committed consistency report was missing or thin and overwrote it with a hand-reconstructed version — which was both less thorough than the subagent's original and broke the internal-reference checker. The original had to be restored from git (`git checkout <sha> -- <path>`), costing two extra commits and a credibility hit on the deliverable. The lesson is that a corrupted tool result is not evidence of the file's state; it is evidence of nothing. The marginal cost of the rule is a single re-run of a narrowed check (`git show HEAD:<path> | head`, `wc -l`, a targeted grep) — seconds — against the cost of a destructive action taken on a phantom reading, which here was a full overwrite-then-restore cycle plus a regression in a shipped artifact.
