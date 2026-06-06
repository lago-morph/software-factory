# agent instruction

**Known `check-internal-refs.py` BARE_TEXT false positives.** The repo's `scripts/check-internal-refs.py` BARE_TEXT heuristic flags descriptive link-text phrases (e.g. "the next-steps report", "the binding spec") even when they are already inside a well-formed markdown link. These are false positives consistent with the existing corpus: verify the link has a real, resolving target, then move on. Do NOT rewrite good descriptive link text to silence the heuristic, and do NOT treat a nonzero finding count as failure — the checker exits 0 by design.

*Grounded in: the same BARE_TEXT phrases recurred on BOARD.md, the backbone plan, and the handoff across PRs #249/#250/#251, all inside valid links.*

# justification

Across all three PRs this session, the link checker flagged phrases like "the next-steps report" and "the binding spec" that were already proper `[text](path)` links — the identical pattern the merged charter and methodology docs use. Each time I confirmed the link target resolved and left the text alone. Without this rule a future agent burns a review cycle "fixing" correct, corpus-consistent link text to appease a heuristic that exits 0 anyway; with it, the agent runs one `ls`/grep on the target and proceeds. The checker is advisory — knowing which of its findings are noise is the whole value.
