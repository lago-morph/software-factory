# agent instruction

**Use `/pull/N/files/<commit-sha>` for commit-scoped GitHub PR review URLs.** When handing off work for user review of a specific commit's content within an open PR, the URL `https://github.com/<owner>/<repo>/pull/<N>/files/<commit-sha>` scopes the GitHub PR review interface to that commit's diff while preserving line-comment affordances. Use this URL pattern when the commit is part of an in-progress PR; use the PR-root `/files` URL when the entire PR is the scope.

*Grounded in: user asked for clickable review link for a specific commit (decision briefs); the /pull/N/files/<sha> pattern is what works.*

# justification

The user explicitly asked for a clickable GitHub review-interface link for a specific commit (the decision-briefs commit). The PR-root `/files` URL shows all changed files in the entire PR, which is too broad for commit-scoped review. The commit-detail URL `/commit/<sha>` doesn't preserve the PR review-comment affordances. The pattern `/pull/<N>/files/<sha>` is the sweet spot: scoped to commit, full review affordances. Memorizing the pattern saves 30-60 seconds per occurrence and avoids the user having to navigate from a less-useful URL.
