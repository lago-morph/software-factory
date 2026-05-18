# agent instruction

**Sequence narrowest-first when replace_all on overlapping tokens.** "When using Edit `replace_all` to rename a token whose new value contains the old value as a substring (e.g., `AGENT-` → `AGENTS-MD-`), do the most-specific pattern first (`AGENT-<hash>` → `AGENTS-MD-<hash>`), then handle any remaining standalone matches case-by-case. A naive prefix replace_all double-substitutes (`AGENT-` matches inside `AGENTS-MD-` if applied after the rename has already created `AGENTS-MD-` text in the file)."

*Grounded in: PR #95 AGENT- → AGENTS-MD- migration where staged replacement order avoided the substring-overlap trap.*

# justification

In PR #95 I needed to rename `AGENT-` to `AGENTS-MD-` across SKILL.md (20 hits) and SPEC.md (24 hits). A naive `Edit replace_all old_string="AGENT-" new_string="AGENTS-MD-"` would have substituted the existing `AGENTS-MD-` strings the project already had (introduced in the previous commit) — wait no, more subtly: since `AGENT-` is a substring of `AGENTS-MD-`, a single `replace_all` pass would still be safe because Edit's exact-string match doesn't iterate. But the analogous SED-style global substitution on a fresh file WOULD double-substitute on a second run, and the safer mental model is to assume that for any overlapping rename.

I sequenced it as: first `replace_all` the longest specific pattern (`AGENT-<hash>` → `AGENTS-MD-<hash>`), then grepped for remaining `AGENT-` (not preceded by `AGENTS-`) and handled the survivors with one-off Edits. This avoided having to reason about whether Edit's exact-match semantics would or wouldn't double-substitute. The marginal cost is one grep between the two replace_all calls. The marginal benefit is that the rename is robustly correct under any string-matching engine, not just Edit's exact-match.
