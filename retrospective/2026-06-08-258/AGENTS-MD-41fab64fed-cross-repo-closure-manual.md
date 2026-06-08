# agent instruction

**Cross-repo issue and PR closure is manual.** GitHub keyword-closing (`Closes #N`) only works when the PR and the issue live in the same repository. When a PR addresses an issue in a different repo, do not claim the merge will auto-close it; close the issue explicitly against a stated criterion and link the PRs in a comment.

*Grounded in: idea-pipeline issue #21 addressed by PRs in software-factory and software-factory-prototype, which cannot keyword-close it across repos.*

# justification

This session's work spanned three repositories: the tracking issue lived in `idea-pipeline`, while every PR that addressed it landed in `software-factory` and `software-factory-prototype`. A naive `Closes #21` in those PR bodies would have been a lie — GitHub does not resolve closing keywords across repositories — and the PR-OPENED comment's "merging will close this issue" claim would have silently failed, leaving a done issue open forever. Recognizing this up front cost nothing and let the agent set an explicit close criterion ("institutionalized in software-factory main + chunk-1 proven") and close the issue deliberately with linked PRs. The rule prevents a whole class of stale-state bugs in any multi-repo workflow, and the marginal cost is just remembering to close manually rather than relying on automation that does not apply.
