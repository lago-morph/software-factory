# agent instruction

**Cross-product integration pass after per-cluster seam reviews.** "When a corpus is authored by parallel subagents grouped into clusters/products and each cluster gets its own seam review, run ONE final cross-product integration adversary over the whole corpus before declaring it done — tracing the end-to-end critical path and diffing every cross-cluster contract at the field level. Per-cluster reviewers each trust the *other* side of a seam crossing two clusters, so contradictions there survive every per-cluster review."

*Grounded in: the Sweep-2 spine run's opus-panel integration adversary caught four build-breakers that all six per-cluster seam reviews missed.*

# justification

Six per-cluster seam adversaries ran and each returned accept-with-fixes; the corpus looked done. A single cross-product adversary then found a deadlock (C52↔C53, where each side's reviewer verified its own half of the hand-off and trusted the other), an enum collision that would make a finished-build query silently return nothing (`factory_build` `completed` vs the bead envelope's `closed`), a sequence-ordering contradiction (C09↔C05), and an enum-membership gap (C41 missing the `tool:` actor kind). Every one lived exactly at a seam crossing two cluster-reviews. The marginal cost is one extra reviewer pass at corpus close; the cost of skipping it is shipping four latent build-breakers that read as "fully reviewed."
