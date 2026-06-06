# agent instruction

**Demote every prior active-handoff marker when rotating the handoff.** When you write a new SESSION-HANDOFF and repoint AGENT-ENTRY §2, grep the current-state list for every existing "active handoff" marker and demote ALL of them to "superseded …" — there must be exactly one active handoff pointer. Do not assume only the immediately-prior handoff is marked active.

*Grounded in: AGENT-ENTRY §2 carried two stale "active handoff" markers (the 2026-06-05 v4 handoff and the v3 Phase-8 handoff) at rotation time.*

# justification

When rotating the handoff this session I found AGENT-ENTRY §2 already claimed TWO active handoffs — the 2026-06-05 v4 one and a leftover v3 Phase-8 one — so "where are we?" had two contradictory answers. Repointing only the obvious one would have left three. The rule costs one `grep "active handoff"` over the file; skipping it leaves a navigation doc that lies about the current pickup point, which is exactly the doc a fresh session trusts first.
