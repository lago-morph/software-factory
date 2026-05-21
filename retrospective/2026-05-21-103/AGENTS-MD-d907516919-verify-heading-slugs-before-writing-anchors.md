# agent instruction

**Verify heading slugs by grep before writing anchor links into long markdown files.** Before composing a `References` block (in an ADR, a retrospective, or any cross-referencing document) that uses GFM anchor links into long target files, run `grep -n '^#' <target-file>` to confirm the heading text. The repo's link checker is post-hoc — a typo wastes a CI round-trip; the grep is one tool call.

*Grounded in: ADR-0002 References — verified anchors in `research-plan.md`, `research/00-synthesis.md`, `research/PLAN.md`, `architectures/00-comparison.md` before writing the bullet list; link checker came back clean for the new ADR on first run.*

# justification

The ADR convention requires relative paths with anchor fragments for direct subsection linking (`[overview.md](../overview.md) [§5](../overview.md#5-foo), [§6.2](../overview.md#62-bar)`). GFM slug rules — lowercase, hyphenate spaces, strip most punctuation, *do not collapse consecutive hyphens* — are easy to get wrong from memory, especially for headings with em-dashes, numeric prefixes, or parenthetical clauses. The link checker (`check_adr_links.py`) catches mistakes reliably, but it runs after the commit; a typo means another fix-up commit and another CI cycle.

In the ADR-0002 session, the candidate references included `research/PLAN.md §3.2`, `research/00-synthesis.md §4`, `architectures/00-comparison.md §7.1` and §7.4, plus four anchors into `research-plan.md` itself. A single `grep -n '^#' <file>` per target file — four tool calls total — confirmed every slug before the file was written. The link checker came back clean for the new ADR on first invocation; only pre-existing breakages in ADR-0001 surfaced.

The marginal cost is N+1 grep calls (one per referenced file). The avoided cost is at least one fix-up commit per typo, plus the friction of re-running the checker, re-pushing, and waiting for CI. For any ADR with more than two anchor references the rule pays for itself immediately.
