# agent instruction

**Sample-first for multi-part deliverables.** "For multi-part deliverables where the parts share a format that needs human validation (per-candidate documents, per-component specs, per-something-N artifacts), ship the first sample as its own PR with the format established but only one part complete. Wait for the PR to merge — treat merge as the signoff signal. Then ship the remaining parts in a second PR. Do not produce N parts simultaneously in an unvalidated format."

*Grounded in: build-guide items 5-6 successfully shipped as PR #206 (GF-M sample) then PR #207 (9 others), avoiding the risk of producing 30 diagrams in a wrong format.*

# justification

Build-guide items 5-6 had 30 Mermaid diagrams across 10 candidates. If the format had been wrong (wrong abstraction level, wrong column layout, wrong prose tone), fixing 30 diagrams would have been substantial rework. The sample-first pattern shipped one candidate (GF-M, 3 diagrams), validated by merge, then shipped the other 9 (27 diagrams) confidently. Format held. The marginal cost of the sample-first PR is one extra PR cycle; the cost of producing N parts in a wrong format scales with N. For N=10 with substantial per-part work (diagrams + tables + prose), the asymmetry favors sample-first overwhelmingly.
