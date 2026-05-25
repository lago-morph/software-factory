# agent instruction

**Rewrite session-handoff docs end-to-end at phase close.** When a synthesis phase or major work-unit closes, rewrite any `SESSION-HANDOFF-*.md` doc end-to-end rather than patching it in place. The next agent reads the handoff to orient; a half-current handoff (some sections describing closed state, others describing open state) is worse than no handoff because it produces actionable confusion.

*Grounded in: PR #134 closing Phase 3.4, where the previous handoff still described DEC-1 as pending after it was resolved.*

# justification

When PR #134 closed Phase 3.4, the existing `SESSION-HANDOFF-2026-05-25.md` (written mid-phase at PR #132) had DEC-1 marked PENDING, listed open questions about the original A/B/C/D options, and contained the lead-agent's quick assessment of per-candidate defense status under a frame the user later overrode. A surgical patch ("change DEC-1 status to RESOLVED") would have left ~70% of the doc describing a state of the world that no longer existed. The next agent picking up that handoff would have read the stale framing alongside the resolution and tried to reconcile them.

End-to-end rewrite at phase close took ~10 minutes and produced a single internally-consistent handoff: what's closed, what's open, what the next agent's first move is. The marginal cost over a surgical patch is small; the cost-of-confusion savings for the next agent are large. The deeper principle: a handoff doc is a *current-state snapshot*, not a *changelog*. Snapshots get rewritten; changelogs get appended.