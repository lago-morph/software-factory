# agent instruction

**Read the current label set before any GitHub MCP label-replace write.** The MCP `issue_write update labels=…` REPLACES the entire label set on the issue. Before any label-modifying write, call `issue_read get_labels` to retrieve the current set, compute the new full set (union with additions, minus removals), and write back the merged list. Passing only the new labels wipes the existing ones.

*Grounded in: PR #114 — the issue-management skill's QUESTIONS / ANSWERS / DUPLICATE / INVALID / WONTFIX behaviors all needed this discipline, and it was elevated to a top-level "anti-patterns" entry in the SKILL.md.*

# justification

The GitHub MCP `issue_write update` operation has replace-not-merge semantics for labels. A naive "add the `question` label" call passing only `labels=["question"]` silently wipes every other label on the issue. The issue-management skill encountered this on five separate behaviors (QUESTIONS, ANSWERS, DUPLICATE, INVALID, WONTFIX), and the documented workflow for every one of them now starts with `issue_read get_labels`. This is not a one-skill concern — any future automation that touches GitHub labels via the MCP will hit it.

The marginal cost is one extra MCP read call per label-modifying write. The cost of skipping it is silent destruction of issue metadata, which is invisible until someone notices the missing labels weeks later. Labels are the only at-a-glance signal in GitHub's issue list view; wiping them silently degrades every downstream filter, automation, and reviewer-scan workflow that depends on them.
