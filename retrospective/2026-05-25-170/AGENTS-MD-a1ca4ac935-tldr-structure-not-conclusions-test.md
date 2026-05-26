# agent instruction

**TL;DR structure-not-conclusions test.** Every line of a top-of-doc `## TL;DR (≤200 words)` section MUST pass the heuristic "would this line need updating if the doc's conclusions changed?" — if yes, rewrite to name a structural element rather than a conclusion. Conclusion-restatement TL;DRs drift silently and fail the regeneration loop the TL;DR-first discipline depends on.

*Grounded in: PR A5 verification subagent flagged the candidate-registry TL;DR's "GF → BF continuity matrix is withdrawn" line as restating a policy conclusion.*

# justification

In the 2026-05-25 Phase-5-entry run, PR A2 authored the candidate-registry TL;DR with a line announcing the GF→BF continuity-matrix withdrawal as a policy verdict. The PR-A5 fresh-context verification subagent correctly applied the test — would this line need updating if the policy flipped? Yes ⇒ the line restates content. Fixed by rephrasing to name the structural element (presence of a strikethrough-marked section in the registry) rather than the verdict outcome.

Without the rule, every future TL;DR author repeats the failure mode. The autonomous-run skill's end-of-run TL;DR-regeneration sub-step (codified in PR A3) cannot mechanically catch this because the regen subagent does not know what was conclusion vs structure — it just rewrites the whole TL;DR from the body, erasing whatever structural framing the original line carried. The marginal cost of the rule is one heuristic check per TL;DR line at authoring time, ~30 seconds. The asymmetric cost without the rule: the TL;DR-first discipline (load-bearing for context-slimming per CONTEXT-SLIMMING-PLAN.md) silently rots run-over-run, and the regeneration loop produces increasingly stale TL;DRs that the morning user trusts as accurate summaries.
