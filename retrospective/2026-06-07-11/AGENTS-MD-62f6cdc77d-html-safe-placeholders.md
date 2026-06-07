# agent instruction

**HTML-safe placeholders in PR and issue bodies.** Do not put `<angle-bracket>` placeholders inside inline code in a PR or issue body: GitHub renders the body through an HTML sanitizer that silently strips them, even inside backticks. Use uppercase word placeholders (`ID-OR-ALIAS`, `MESSAGE`) or escape as `&lt;...&gt;`.

*Grounded in: PR #9's body lost its `<id-or-alias> <message...>` text to HTML stripping and had to be re-edited.*

# justification

PR #9's description documented a CLI signature as `` `gc session nudge <id-or-alias> <message...>` ``. When the body rendered, GitHub's HTML sanitizer ate the `<id-or-alias>` and `<message...>` tokens — even inside the backticks — leaving the nonsensical "takes ` `". The whole point of that PR was to teach a command signature, so the stripped body actively misinformed reviewers. The fix was a second `update_pull_request` call rewriting every placeholder to an HTML-safe form. The marginal cost of getting it right the first time is zero (write `ID-OR-ALIAS` instead of `<id-or-alias>`); the cost of getting it wrong is a re-edit plus, if unnoticed, a permanently garbled record of the exact thing the PR was trying to convey.
