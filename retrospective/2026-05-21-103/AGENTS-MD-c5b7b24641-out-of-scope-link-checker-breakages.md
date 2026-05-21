# agent instruction

**Out-of-scope link-checker breakages stay out of scope.** When the ADR link checker (or any repo link checker) reports broken links in files OTHER than the one being authored or modified, do NOT fix them in the same PR unless the user explicitly asks for cleanup. Note the pre-existing breakages in the PR body so a reviewer sees them and can decide whether a follow-up is warranted.

*Grounded in: ADR-0002 PR #103 — link checker flagged 5 pre-existing breakages in ADR-0001 (stale PLAN.md anchors + two deleted `research/blocked-urls*.md` files); these were left untouched and called out in the PR body rather than fixed inline.*

# justification

In the ADR-0002 PR, `python3 .claude/skills/adr/scripts/check_adr_links.py docs/adr/` returned exit 1 with 5 broken links — all of them in ADR-0001 (three stale `research/PLAN.md` anchors from a renumbering pass, plus two `research/blocked-urls*.md` files that have since been deleted from the repo). It would have been tempting to fix them in the same commit "while I'm here", but the ADR convention says Accepted ADRs are immutable except for typo / link fixes — and the broken anchors are a symptom of a separate restructure that may warrant a superseding ADR rather than silent patching. Touching ADR-0001 would also have ballooned the PR diff and forced the reviewer to re-evaluate the unrelated changes.

The cost of *not* having this rule is real: an agent that habitually fixes adjacent breakages produces PRs that mix concerns, makes review noisier, and risks substantively editing an immutable artifact under the cover of "just a link fix". The marginal cost of adopting the rule is one sentence in the PR body ("pre-existing breakages, out of scope"). That asymmetry — one sentence vs. unreviewable scope creep across the codebase's most explicitly immutable artifacts — is why this earns its place.
