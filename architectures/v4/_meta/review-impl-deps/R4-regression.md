# R4 — Regression & internal-consistency re-check of `implementation-dependencies.md`

**Reviewer role:** adversarial regression reviewer. **Scope:** confirm the two round-1 fixes (fence/eval ordering; "six products" count) are complete and consistent across ALL sections; catch any NEW contradiction the edits introduced; fresh sweep of partition/build-order/edges/anchors.

**Method.** Rebuilt the C01–C57 → product partition from the catalog tables; recomputed every count (rings 19/22/25, Gas-City 15/11, critical path depth, depend-only-on-C01) from the inventory `Depends on` column with C01 as the cycle-break root; cross-checked every per-component "Needs" cell against [`component-inventory.md`](../component-inventory.md); topo-sorted the product-level DAG; walked all 9 fence-mention locations; resolved every internal anchor and cross-reference target.

---

## Findings

[MINOR] line 58 — `[decision D-20](../../decisions-to-make.md)` — The link target `decisions-to-make.md` exists but contains only decisions D-1…D-18 (highest is D-18); it has no "D-20" string. The relevant ruling is that file's **Decision #1** ("Put the safety fence up before the factory runs unattended"), not a "D-20". The link therefore points a reader at a document that never mentions the ID it cites, and lines 247 and 278 reference "decision D-20" as bare text with no link at all. R1 previously flagged D-20 as un-glossed (MINOR); this is the sharper underlying defect. Not introduced by the FIX edits. — Fix: either relabel to the actual decision number/anchor in `decisions-to-make.md` (e.g. `[Decision 1: fence-before-unattended](../../decisions-to-make.md#1-put-the-safety-fence-up-before-the-factory-runs-unattended-or-after)`), or, if "D-20" is a separate `_meta/` ledger ID, link to that ledger instead of `decisions-to-make.md`.

[MINOR] line 224 / build-order Mermaid (lines 218–235) — `SB["Self-build<br/>Bootstrap C51 C52 C53 · Governance docs"]` fed only by `EX --> SB` and `EV --> SB` — Governance docs (C57) are folded into the SB node, and C57 depends on C43 (the fence), but the build-order graph has no `FENCE --> SB` edge. The prose at line 102 correctly states "Governance documents … Depends on … the fence (C43)", so the graph under-represents a dependency the text asserts. Pre-existing (R3 did not flag it); not introduced by the edits; acceptable as a ≤7-node abstraction but technically incomplete. — Fix: optionally add `FENCE --> SB`, or add a half-clause to the caption noting governance docs also draw on the fence (C43).

No FACTUAL, CONTRADICTION, or MAJOR findings.

## Verification results (all PASS)

- **Partition (item 3):** all C01–C57 owned exactly once; the only double-owned component is **C46**, which is the sanctioned MLflow-storage + custom-definitions split. No unowned, no other double-owned. CLEAN.
- **Build order (item 4):** product-level dependency graph is **acyclic** (topo-sortable); no product A precedes product B while a B-component is a dependency of an A-component. CLEAN.
- **Edges (item 5):** all ~50 per-component "Needs" cells match the inventory. The single intentional divergence is **C43** (`C42 (boundary-typing half) — C44 deferred`) vs inventory `C42, C44` — this is the documented fence-split, not a defect. CLEAN.
- **Anchors (item 6):** `#two-cycles-broken-by-an-interface-freeze`, `#the-remaining-custom-products`, `#gas-city--gc-binary-mit`, `#build-order-across-products` all resolve to real headings; the three sibling-doc links (`build-order-plain-english.md`, `architecture-guide-for-engineers.md`, `decisions-to-make.md`) all exist at the relative paths. Only the D-20 *label* (above) is stale, not the path.
- **Counts (FIX-2):** rings 19/22/25 reproduce exactly from the closure of {C53,C43}+C31−C44 → +{C05,C09,C18} → +{C34,C41,C23}; Gas-City total 15, Gas-City-in-backbone 11, depend-only-on-C01 = {C02,C03,C04,C07,C18,C19,C21,C23}=8 (list matches doc verbatim), critical path depth = 10 (doc's stated chain has all-valid edges; multiple length-10 chains exist, doc's is one), widest = 13. **Six products** consistent: backbone Mermaid = 6 nodes, backbone product table = 6 data rows, prose "six products" = 6, components sum to 25 (11+2+3+4+2+3).
- **Fence/eval (FIX-1):** all 9 locations agree. Backbone Mermaid has `E --> F` (holdout below eval) **and** `G --> F` (boundary-typing early); caption line 40 says fence sits "**below** the evaluation tier, not beside it"; product-order line 51 "→ Evaluation tier → the fence … (parallel, both gated on the eval tier)"; rings put C34 in the post-eval safety collar (ring 3); master products table line 95 fence "Depends on … Inspect AI (C30/C32)"; per-component table lines 200–201 (C34 needs C30,C32; C43 needs C42+deferred C44); build-order Mermaid `EV --> FENCE` + caption line 235; scheduling note line 247 "holdout-integrity half (C34) is not early". No residual place implies the whole fence is early or parallel-to-eval. No NEW contradiction introduced by the "two parallel preconditions" framing (fence and bootstrap are both gated on the eval tier and parallel to *each other*, which the diagram's `E-->F` / `E-->B` edges support).

---

## Verdict

**accept-with-named-amendments.**

Rationale: Both round-1 fixes are fully and consistently applied; every quantitative claim reproduces from the inventory; the partition, the product-level DAG, and all per-component edges are clean. The two remaining items are MINOR and pre-existing (a stale decision-ID label on an otherwise-valid link, and one omitted edge in an intentionally-simplified ≤7-node Mermaid graph). Neither blocks acceptance; both are worth a one-line cleanup. No factual error, contradiction, or major defect was found, and the edits introduced no new inconsistency.

Named amendments: (1) fix the `decision D-20` label/link at lines 58/247/278 to point at the decision that actually exists; (2) optionally represent the governance→fence dependency in the build-order graph or its caption.

FIX-1 fence/eval: COMPLETE
FIX-2 product-count: COMPLETE
