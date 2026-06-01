# agent instruction

**Run adversarial review to an explicit zero-findings termination bar.** When looping adversarial review over an artifact, fix findings and re-review until a full round returns zero factual, zero contradiction, and zero major findings; minor and polish findings do not block. State the bar up front and stop when it is met, rather than looping indefinitely or stopping after a single round.

*Grounded in: the three-round review loop terminating when round 3 returned zero factual / contradiction / major findings.*

# justification

The user asked to "review again in a loop until there are no factual or contradiction findings, and no other major findings." Naming that exact bar — factual = 0, contradiction = 0, major = 0, minors allowed — gave every round an unambiguous stop condition. Round 1 found a contradiction; round 2 found a contradiction plus a major; round 3 returned 0/0/0 across two reviewers and the loop stopped. Without a stated bar, two failure modes appear: stopping after round 1 (the most common, and round 1 here still had a live contradiction), or polishing forever on cosmetic minors (round 3's reviewers each still raised 3–4 minors that a perfectionist would chase indefinitely). The marginal cost is one sentence in each reviewer brief instructing them to classify findings by severity and one decision rule for the orchestrator. The payoff is a loop that demonstrably converges and a defensible claim that it did. Tie the bar to severity, not to round count.
