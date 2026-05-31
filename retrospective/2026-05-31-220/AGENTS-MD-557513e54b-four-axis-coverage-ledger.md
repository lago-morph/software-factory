# agent instruction

**Four-axis coverage ledger for multi-component authoring runs.** When a run authors or reviews many components/artifacts that each owe multiple passes, maintain a coverage ledger with one row per component and columns {Built, Reviewed, Incorporated, iNtegrated}, and treat the run as done only when every row is checked on every axis. Mark an axis done only when its evidence exists on disk (a `.review.md` for Reviewed; every finding applied-or-deferred-with-reason for Incorporated).

*Grounded in: the v4 Sweep-1 run, where the ledger surfaced 11 built-but-never-reviewed components and guaranteed all 57 closed on all four axes.*

# justification

The operator's explicit worry entering this run was "do not miss any that weren't reviewed, and make sure all checks are incorporated." A flat to-do list cannot answer "is anything half-done?" because a component can be built-but-unreviewed, reviewed-but-findings-not-incorporated, or incorporated-but-never-integrated — three distinct failure states that look identical from a "is it built?" view. The four-axis ledger made each state visible: it immediately exposed 11 components built in an earlier phase that had never been adversary-reviewed (silent debt that would otherwise have shipped), and it gave a single mechanical stopping condition — every row ✓ on every axis. The marginal cost is one small Markdown table updated once per wave; the cost of its absence is exactly the silent review-debt the operator feared.
