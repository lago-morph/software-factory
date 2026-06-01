# R7 — Convergence verifier (final consistency pass)

Adversarial convergence pass on `architectures/v4/implementation-dependencies.md` (committed version), confirming Fix A (bead-type schema C20 as its own seventh product) and Fix B (fence detect-vs-prevent caveat) landed cleanly with no residue and no new defect.

## Findings

No findings. The document is internally consistent and both fixes are complete. Detail of every check below.

### Fix A — seven products / C20 as its own product

- No residual "six products": grep for `six product` / `6 product` returns nothing.
- No `C08, C09, C20` bundling and no place showing C20 depending on C08/Spec intake: grep returns nothing.
- Backbone heading (L22) says "seven products"; intro (L24) says "seven products"; the "Two kinds of work" recap (L66) lists the bead-type schema as one of the four from-scratch products.
- Backbone Mermaid (L26–41): 7 nodes (G, CC, S, BS, E, F, B); `BS["Bead-type schema (custom)<br/>C20"]` is its own node with `G --> BS --> B` — depends on Gas City (bead store), feeds Bootstrap. Distinct components across nodes = 25.
- Backbone product table (L44–52): 7 rows; the **Bead-type schema** row (L49) carries C20 alone, "its own dependency (C19), not Spec intake."
- Product-order prose (L54): "(in parallel) `Claude Code`, `Spec intake`, and the `Bead-type schema`" — three parallel siblings off Gas City, all four custom products named in L66.
- Three-rings component lists sum to 25: 11 Gas City + 2 Claude Code/model-floor + 2 Spec intake + 1 Bead schema + 4 eval + 2 fence + 3 bootstrap = 25 (verified arithmetically). Possible ring (L60) = 19 and includes C20; safe ring = 25.
- Catalog agreement: internal-products table (L93) and per-component table (L198) both show C20 as the "Bead-type schema" product depending on C19 only. Bootstrap row (L104) lists "Bead-type schema (C20)" as a separate upstream product. Backbone and catalog AGREE on C20's product and dependency.

### Fix B — fence detect-vs-prevent caveat

- Safety-collar ring (L64): "before digital twins (C44) land, C34 *detects* holdout violations after the fact rather than preventing them at tool-call time — tool-call-time *prevention* is C43's blast-radius bound and stays aspirational until twins ship (per C34 §4.3 / XC-8). The first safe self-build is therefore guarded by detection plus a human gate, not yet by full prevention."
- Build-order fence note (L250): "until twins exist it *detects and audits* violations rather than preventing them at tool-call time. The **twin-isolation half** waits on the digital-twins product (C44), which is what turns the blast-radius bound from aspirational prevention into enforced prevention."
- Both appear, attribute prevention to C43's blast-radius bound, mark it aspirational until twins (C44), and do not over/under-claim. No contradiction.

### Fresh consistency sweep

1. **Partition C01–C57:** rebuilt from the catalog. Zero orphans, zero double-owns except C46 (MLflow tracking-store half + custom definitions half) — the single sanctioned two-product split. PASS.
2. **Counts:** 25 backbone (verified set), 7 products, 19/22/25 rings (19 possible + C05/C09/C18 → 22 runnable + C34/C41/C23 → 25 safe — all re-derived), 15 Gas City total / 11 in backbone, 10-deep critical path (C01→C04→C28→C29→C32→C33→C46→C47→C48→C50, every edge present in inventory), 13-wide (L12 and L240 agree), 8-depend-only-on-C01 (C02,C03,C04,C07,C18,C19,C21,C23 — all confirmed `Depends on: C01` only). PASS.
3. **Per-component Needs vs inventory:** all 57 present; every edge matches `_meta/component-inventory.md` exactly. The only divergence is C43 (doc: C42 + C44-deferred), which is annotated as the intentional fence split. PASS.
4. **Anchors/cross-refs:** D-20 target `decisions-to-make.md#1-put-the-safety-fence-up-before-the-factory-runs-unattended-or-after` resolves to the H2 on L25. `#the-remaining-custom-products` → L189. `#gas-city--gc-binary-mit` → L110 (em-dash + space renders to `--`). All resolve. PASS.
5. **Change-narration / conversation-anchoring:** none. The only "fixed" hit is "the contract … is fixed before either is built" (legitimate prose). PASS.

FIX-A seven-products: COMPLETE
FIX-B fence-caveat: COMPLETE

Verdict: accept-as-is
