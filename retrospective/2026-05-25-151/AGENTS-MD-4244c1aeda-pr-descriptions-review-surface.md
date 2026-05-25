# agent instruction

**PR descriptions are the user's review surface; write them substantively.** Reviewers (especially when the user is reviewing during morning hand-off of an unattended run) read PR descriptions, not code diffs. Every PR description must include: (a) Summary — 2-4 sentences naming what changed and why; (b) Key findings or decisions — specific bulleted list, not generic platitudes; (c) Rewind point — at least one named commit SHA to revert plus what each reversal undoes; (d) Test plan or acceptance criteria — a checkboxed list of what verification would look like; (e) Stacked-PR base notice when applicable, naming the parent PR and the auto-rebase behavior. Thin one-paragraph PR descriptions are forbidden.

*Grounded in: user statement during 2026-05-25 review of the overnight chain (PRs #136-#145).*

# justification

The user reviewed the 10-PR overnight chain in PRs #136–#145 by reading PR descriptions in sequence and merging in order; they did not open file diffs. Their stated review style: "I do not review code in general. I review the PR descriptions." Under this review style, the PR description is functionally the entire change — anything missing from the description is invisible during review. Every chain merge proceeded based on the description's claims. This is also the failure mode behind unauthorized scope creep on long-running runs: if the description is bland, the reviewer can't detect that the PR did more or less than authorized. The marginal cost of the rule is a few minutes per PR (already paid in this session's chain — PRs #136–#145 all had this structure). The cost of omitting it is silent acceptance of unintended changes. The rule formalizes what worked in this session and prevents regression.
