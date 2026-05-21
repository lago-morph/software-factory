# agent instruction

**Embed a machine-readable marker in every skill-emitted GitHub comment.** Every comment that a skill posts on a GitHub issue or PR must end with an HTML comment marker of the form `<!-- skill-name:event-tag:vN -->` so future automation can grep, count, and validate skill-emitted comments. The marker survives copy-paste and is invisible in rendered markdown.

*Grounded in: PR #114 — the `issue-management` skill's templates all end with `<!-- issue-management:TAG:v1 -->`, enabling future tooling to audit which agent-emitted comments exist and whether they used the current schema version.*

# justification

GitHub issue threads grow long; distinguishing skill-emitted "agent-was-here" comments from free-form conversation by eye becomes impossible at scale. The marker `<!-- skill-name:event-tag:vN -->` is invisible in rendered markdown (HTML comments are stripped by GitHub's markdown renderer) but trivially greppable in the raw API response. The version suffix lets a future schema migration distinguish v1 comments from v2 comments without false positives — e.g., a future "ANSWERS comment now includes a confidence score" change bumps to `v2`, and v1 comments remain identifiable as the prior schema.

The marginal cost is a single line per comment template. The cost of skipping it is that no future automation can reliably audit, count, or version-migrate skill output — every analysis becomes a regex against unstructured prose, which is fragile to template wording changes.
