# agent instruction

**Raw URLs in chat replies when the link target has special characters.** GitHub PR-comment markdown can mangle links that include long branch names, hyphens, dots, and slashes — wrapping the URL in backticks (rendering it as code) or otherwise breaking the click target. When the agent is providing a clickable URL to a deeply-nested file, the safer default is a bare URL on its own line (GitHub auto-linkifies it) OR a link in the chat output (where the harness's formatter is reliable). Do NOT iterate through 3+ markdown-link variants debugging the formatter — escalate to the bare URL within the second attempt.

*Grounded in: PR #169 line-87 — 4 sequential markdown-link attempts all rendered as code-formatted text rather than clickable links; user finally said "Why do I even try. Put the link HERE [in chat], where we know you can do it without it being malformed".*

# justification

In the 2026-05-25 PR #169 line-87 thread, after producing PR #172 (the plain-language brief), the agent attempted to give the user a clickable URL to the brief file via four sequential markdown-link variants:

1. Backtick-wrapped path-in-link: ``[`file.md`](url)`` — rendered as code.
2. Descriptive label: `[Click here to open](url)` — rendered as code.
3. Raw URL inside backticks: ``[label](`url`)`` — rendered as code.
4. Plain-text label markdown link: `[plain label](url)` — rendered as code.

All four failed for the same reason: the harness's outgoing PR-comment formatter wraps URLs with hyphens/dots/slashes in backticks. Each attempt was a separate PR comment, so the cumulative effect was 4 round-trips on a question the user thought was a single-message item. The user's "Why do I even try" rebuke is the kind of trust erosion that compounds across sessions.

The fix is mechanical: bare URL on its own line auto-linkifies in GitHub PR comments and renders as a clickable link regardless of special characters. Chat output formatting is reliable for markdown links. So the safer defaults are:

- **In PR comments**: bare URL on its own line.
- **In chat output**: markdown link or bare URL — both work.

Cost of the rule: one mental check ("does my URL have hyphens/dots/slashes that the formatter might mangle?") before each PR-comment link attempt.

Asymmetric cost without: each iterative markdown-link debug attempt is a user round-trip with no progress. The "escalate within 2 attempts" rule caps the wasted round-trips.
