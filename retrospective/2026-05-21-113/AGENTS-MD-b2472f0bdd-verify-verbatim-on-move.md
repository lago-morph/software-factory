# agent instruction

**Verify-verbatim when moving content between files.** When you relocate a block of text from one file to another and the goal is byte-identical preservation (a section move, a quote extraction, an artifact split), extract the source range with `sed -n 'A,Bp'` (or equivalent line-bounded tool) and immediately verify with `diff <(sed -n 'A,Bp' source) <newfile-tail>` so any silent corruption is caught before the move is committed. Do not trust Edit / Write tools alone to preserve content verbatim.

*Grounded in: PR #113 §2.4 extraction from `architectures/00-comparison.md` into `architectures/failure-modes.md`.*

# justification

Issue #111 explicitly said "Use tools for this to ensure is verbatim." The discipline cost less than 60 seconds (one extra `diff` command). The marginal benefit is asymmetric: a silent byte-drift (a curly quote sneaking in, a tab→space conversion, a trailing whitespace edit) is invisible at code-review time and propagates into every downstream consumer of the moved content. PR #113's audit-trail commit messages and the §2.4 row-by-row diff hold up to inspection precisely because the extraction was tool-driven and verified. Adopting the rule trades one shell pipeline for forever-eliminating that class of silent corruption on file moves.
