# agent instruction

**Verify relative-link depth from deep sibling directories before commit.** Before committing a markdown file authored several directories deep (e.g. under `_meta/.../panel/`), verify every relative link's `../` depth by running the repo's internal-reference checker (or counting levels to the repo root) -- off-by-one `../` depth is the dominant link bug for deep artifacts, and a subagent writing into a deep directory will reliably get it wrong.

*Grounded in: VERDICT.md and the methodology fact-check both shipped with off-by-one ../ depth from the panel/ dir.*

# justification

Twice in one session a markdown file written four levels deep (`architectures/v4/_meta/next-steps/panel/`) shipped with relative links one `../` too shallow — `../../spec/Cxx` where `../../../spec/Cxx` was correct — and once linked the root report with `../../../../` instead of `../../../../../`. Both were caught only by running `scripts/check-internal-refs.py` after the fact and required a follow-up fix commit each. The pattern is mechanical and predictable: humans and subagents both anchor depth-counting from the wrong directory. The marginal cost of prevention is one checker run (or a five-second level count) before committing a deep file; the cost of skipping it is broken navigation links that erode the artifact and a separate cleanup commit. Running the checker on the changed file is strictly cheaper than the round-trip to discover and fix the break.
