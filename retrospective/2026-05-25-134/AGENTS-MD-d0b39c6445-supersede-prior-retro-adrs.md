# agent instruction

**Explicitly supersede prior-retro ADR drafts when the user overturns the underlying decision.** If a prior session's retrospective produced an ADR draft (`retrospective/<date>/ADR-<hash>-*.md`) whose decision the user later overturns, write a new ADR draft in the current retrospective that explicitly supersedes the prior one (name it, link to it, state what's being overturned and why). Do not leave the prior draft in place without a forward-pointer; do not silently delete it.

*Grounded in: PR #134 overturning the continuity-matrix decision recorded in ADR-ff2a376c34 from the PR #132 retrospective.*

# justification

PR #132's retro produced `ADR-ff2a376c34-greenfield-to-brownfield-continuity.md`, a full ADR draft formalizing the temporal-continuity reading of the user's greenfield→brownfield claim. In PR #134 the user corrected the framing (entry-mode, not temporal), withdrew the continuity-matrix Phase-4 deliverable, and resolved DEC-1.b as N/A. Without an explicit superseding ADR in PR #134's retro, the prior draft remains in the retrospective corpus as if it were still a live proposal — a future agent (or the `adr` skill running over the retro tree) could adopt it into `docs/adr/` and reintroduce the overturned decision.

Marginal cost of the superseding ADR: ~10 minutes — one ADR draft following the standard template, with a `## Supersedes` section linking the prior ID. Cost of skipping it: a stale ADR proposal lives indefinitely in the retro corpus; reprocess passes and the `adr` skill have no way to know it's overturned; the corrective signal that took a full session round-trip to surface gets lost. Retros are append-only by design — the supersede-with-forward-pointer pattern is how corrections propagate without rewriting history.