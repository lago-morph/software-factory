# agent instruction

**No counts of growing collections in plan docs.** Don't write "N numbered reports + M followups" or "K retrospectives" or "P installed skills" into PLAN.md or other long-lived plan documents. Counts go stale the moment they're written; the directory listing IS the count.

*Grounded in: cleanup-plan v1 items 11+12 — user flagged that hardcoded counts in §2 "will instantly become stale."*

# justification

The session opened with PLAN.md's §1 status line declaring "37 numbered reports + 12 follow-up reports." The actual count at session start was 38 + 14 — the Round-12 gas-systems work had landed two days earlier and PLAN.md was already wrong. The repository-layout section §2 had similar counts ("22 retrospectives", "15 installed skills") that would all rot within days of the next round of work.

Counts are a class of "fact that becomes stale fastest of all" — they invite drift on every commit that touches the underlying directory, but agents almost never proactively update them. The marginal cost of dropping them is one less sentence per section ("the `/research/` directory holds numbered reports and followups" is informationally equivalent to the version with counts but doesn't rot). The cost of keeping them is permanent low-grade lying in the doc, and confused new readers who assume the status line is current.
