# agent instruction

**Design files for downstream tooling with strict structural contracts.** "When a markdown file will be consumed by CI/CD automation or other tooling (assembler, linter, generator), define its format with a strict structural contract (e.g., 'exactly two H1 sections in this order, nothing else') rather than a soft convention (e.g., 'please don't use ## here'). A strict contract is robust against drift and parseable with `grep` + `awk`; a soft convention silently rots."

*Grounded in: PR #95 evolution from "the body has no ## headers please" (soft) to the strict `# agent instruction` + `# justification` two-section contract (machine-parseable).*

# justification

The first PR #95 iteration of the per-rule agents file format was: "H1 title at top + ID metadata bullets + rule blockquote body, please don't use ## headings inside." That's a soft convention — three coupled rules, none individually enforceable by a simple parser. The CI/CD assembler would have needed actual markdown parsing to find the rule body and reject malformed files.

The final iteration is: "exactly `# agent instruction` followed by `# justification`, nothing else." A grep for `# agent instruction` finds the rule body's start, the next `# ` line bounds it, everything from `# justification` onward is dropped. Any deviation is visible in a single `grep -c '^# '` (it should return 2) and any future agent authoring the file is guided by a template (`resources/template-agents-md-rule.md`) that encodes the exact layout.

Cost of the rule: ~10 minutes of design time per new tooling-consumed file format, picking explicit structural markers. Benefit: the assembler is trivially correct, drift is detectable, and the format outlives the author who specified it. This is a general principle — strictness is robustness when there's a machine reader downstream.
