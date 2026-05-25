# agent instruction

**Adversarial-review verdict tiers must include `reject-with-counter-proposal`.** Briefs that dispatch real adversarial subagents per the adversarial-review rule MUST present three admissible verdict tiers to each reviewer: `accept-as-is`, `accept-with-named-amendments`, and `reject-with-counter-proposal`. A 2-tier schema (accept / accept-with-amendments) lets reviewers default to amendments even when the underlying shape is wrong.

*Grounded in: auto-003 Round 1 — the methodology-purist reviewer used `reject-with-counter-proposal` to surface the count-gate-vs-smoke-test structural issue; a 2-tier review would have produced an accept-with-amendments that masked the structural problem.*

# justification

Adversarial reviewers given only "accept" and "accept-with-amendments" verdicts will produce amendments by default, because that's the path of least resistance — pointing out details to tweak is easier than proposing to throw out the shape. In auto-003 Round 1, the methodology-purist reviewer returned `reject-with-counter-proposal` with a specific counter-shape (the smoke-test-first pattern that mirrored auto-002 R2). The other reviewer returned `accept-with-named-amendments`. If both had been constrained to the 2-tier schema, the rejection signal would have been smuggled into amendments and the lead agent would have layered amendments onto a structurally-wrong gate. The marginal cost of adding the third tier to a reviewer brief is one sentence; the cost of a structurally-wrong decision propagating through Phase 4 and Phase 5 is days of rework.
