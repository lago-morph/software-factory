# agent instruction

**Sibling-seam cross-check when reviewing parallel-built components.** When two components were built in parallel against a shared seam (each unaware of the other's final spec), brief each one's adversary reviewer to read the sibling's spec and verify the seam is described consistently from both sides. A single-component review cannot catch a seam mismatch; the cross-read can.

*Grounded in: the v4 run, where the C14<->C15 DOT-surface seam and the C26<->C27 signal-set seam were mismatched and only the cross-read caught them.*

# justification

Parallel fan-out builds siblings simultaneously, so each builder writes its side of a shared interface blind to the other's final wording. A reviewer reading only its own component sees a self-consistent spec and passes it — the mismatch lives *between* the two docs, invisible from inside either. Two concrete cases this run: C14 declared it would "fail-loud on loops" while C15 needed a loop/back-edge marker in C14's DOT output to lint bounded loops (taken literally, C14 permanently broke C15); and C26 piped metrics+logs+traces to LangFuse while C27 ingests traces only. Both were caught solely because each adversary was told to read the sibling. The marginal cost is one extra file-read per reviewer; the cost of skipping it is a latent interface contradiction that surfaces only at implementation time, far more expensively.
