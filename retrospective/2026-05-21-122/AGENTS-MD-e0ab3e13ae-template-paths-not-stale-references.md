# agent instruction

**Wildcard and template placeholder paths are not references.** When auditing, rewriting, or grepping for doc references in `.md` files, treat any backtick-wrapped path containing `*`, `<`, `>`, `{`, or `}` as a template placeholder, not an actual reference to a file. Skip these matches in both check passes and bulk-transform passes. Common examples: `architectures/0N-*.md`, `docs/adr/NNNN-kebab-title.md`, `docs/brainstorms/<topic>-requirements.md`, `templates/comment-<tag>.md`, `retrospective/YYYY-MM-DD-PPP.md`.

*Grounded in: issue #104 bulk audit — initial check-internal-refs.py runs surfaced ~20 high-count false-positive "stale" references that were all wildcard/template patterns in skill documentation.*

# justification

Bulk-transforming paths into links has high blast radius: a script that rewrites `` `architectures/0N-*.md` `` to a markdown link produces a broken link (the target doesn't exist; the `*` was a wildcard) and a confusing UX (the placeholder in the link text suggests "click here for the wildcard", which makes no sense). Worse, in a `check-internal-refs.py`-style audit, every template placeholder becomes a "STALE" finding, which trains the human reviewer to dismiss the tool's output as noisy and skip the real findings buried among the false positives.

The session that produced PR #122 ran the initial audit and got a 40+-finding list with several high-count entries (`docs/adr/NNNN-kebab-title.md` × 6, `retrospective/YYYY-MM-DD-PPP.md` × 9, `research/manual/.subagent-brief.md` × 4, `docs/brainstorms/<topic>-requirements.md`, etc.) that were all documentation patterns rather than broken references. Adding the `if any(c in path_str for c in "*<>{}"): continue` filter eliminated all of those false positives in one line. Cost of the rule: trivial. Cost of skipping: false-positive-driven trust erosion in any reference-maintenance tooling.
