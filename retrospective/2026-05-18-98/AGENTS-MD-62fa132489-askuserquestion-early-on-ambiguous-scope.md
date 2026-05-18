# agent instruction

**AskUserQuestion early when audit scope is ambiguous.** When the user asks for an audit/fix task and the scope could plausibly mean "just the surface issue" or "the whole document including discovered drift", use AskUserQuestion with 2–3 named options before committing to one. The cost of a 30-second clarification round trip is far less than the cost of doing the wrong scope and re-doing it.

*Grounded in: PR #98 — after identifying 7 orphan PRs needing PLAN.md back-fill, asked the user via AskUserQuestion with 3 options; user picked one in seconds and the rest of the work was unambiguous.*

# justification

The session had two ambiguity points. For the first — *which* orphan PRs to back-fill (the substantive 7, or only the drains, or all 7 with assigned round numbers) — I used AskUserQuestion with 3 named options and got a clear answer in one round trip; the back-fill work then proceeded without further scope chatter. For the second — how deep to go on the iteration sweep — the user's request ("iterate until no major or factually-wrong minor errors") was self-contained enough not to need clarification. The contrast is instructive: the explicit AskUserQuestion pattern was cheap and decisive; an open-ended "what do you want me to do here?" would have taken 2–3 round trips of clarifying chatter. Cost of adopting the rule: one AskUserQuestion call (≈ 10 seconds of agent time + ≈ 10 seconds of user click time). Cost of not adopting: starting on the wrong scope, then redoing — typically a 10× cost multiplier when the doc is long.
