# agent instruction

**Per-batch build-review-integrate, not build-all-then-review.** In a long unattended authoring run that may be cut off at any token-window boundary, close each batch fully (build -> adversary-review -> integrator) before opening the next, rather than building everything and reviewing later. This keeps completed batches fully closed and minimizes the unreviewed surface at any cutoff instant.

*Grounded in: the v4 Sweep-1 run's per-batch cadence.*

# justification

The run was explicitly framed as "the user will cut it off when the token window closes." Under that constraint, build-all-then-review is a trap: if cut off after building 34 components but before reviewing any, the result is 34 unreviewed specs — precisely the worst state. Per-batch closure means at every cutoff instant the completed batches are fully built+reviewed+integrated and only the single in-flight batch is partial. The cost is more, smaller waves (more orchestration turns); the benefit is that the run degrades gracefully under truncation instead of catastrophically. This run closed Batches 2, 3, 4 fully and only ever had one batch in flight, so a cutoff at any point would have left a clean, reviewed corpus.
