# agent instruction

**Verify the committed tree, not the working tree, after a revert.** When you revert or `git checkout --` a file to undo a change, verify the result with `git show HEAD:<path>` (or grep over the committed blob), not by reading the working tree — and never claim a fix landed on the strength of a working-tree read alone.

*Grounded in: the wrap-up session's spec-annotation reconciliation, where a working-tree revert had to be confirmed against `git show HEAD:` to know which copy of the annotations was actually committed.*

# justification

Twice in this session the working tree and the committed tree diverged in ways that a plain `Read` could not distinguish: once when a background subagent re-applied annotations that a foreground retry had already committed (leaving duplicates only in the working tree), and once when a `git checkout --` revert restored a file whose committed state then had to be confirmed before trusting it. A working-tree read answers "what's on disk right now," which is the wrong question after a revert or a racing concurrent writer; the right question is "what did I actually commit," and only `git show HEAD:<path>` answers that. The cost of getting this wrong is shipping a duplicated or stale artifact while believing the opposite — exactly the failure mode that produced a duplicate-annotation scare mid-session. The marginal cost of the rule is one `git show` or one `grep` over the committed blob, versus the multi-step recovery of un-doing a wrongly-trusted state.
