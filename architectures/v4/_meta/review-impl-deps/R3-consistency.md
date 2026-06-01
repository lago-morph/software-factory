# R3 — Internal-consistency review of `implementation-dependencies.md`

**Reviewer persona:** build-lead implementer who must run the build from this doc and is allergic to self-contradiction.
**Document under review:** `architectures/v4/implementation-dependencies.md` (committed version, 280 lines).
**Method:** reconstructed the full C01–C57 → product partition from the catalog master tables and per-product subsections, then cross-checked every count, every product-order edge, and every per-component "Needs" edge against the inventory (`./_meta/component-inventory.md`) as the dependency source of truth. The reconstructed partition is in the appendix.

---

## Findings

### CONTRADICTION — Build-order §"Build order across products" lines 217–235 (graph) + §backbone lines 34–50 vs the fence's own component edges (lines 94, 199)

> (build-order graph, line 222) `SAFE["Safety<br/>The fence · Bead schema · Attribution (in Gas City)"]` … (line 228) `GC --> SAFE`
> (backbone graph, line 37) `G --> F --> B`; (caption line 39) "Inspect AI **and the fence sit at the same depth**"; (line 50) "`Evaluation tier` and `the fence` (parallel)"

…but the fence product **contains C34**, whose edge is:

> (line 199) "Holdout integrity (C34) | C30, C32"
> (master row, line 94) "**The fence** … Depends on (products): … **Inspect AI (C30/C32)**"

**Why they conflict.** Both top-level graphs place the fence as a child of Gas City *only* and at the *same depth as* (parallel to) the Inspect AI evaluation tier. But C34 — a fence component — depends on C30 and C32, which live *inside* the evaluation tier. A component cannot be parallel to the product it depends on. The fence's own master-table "Depends on (products)" row (line 94) even names "Inspect AI (C30/C32)" as a dependency, directly contradicting the graph edge `GC --> SAFE` (which has no `EV --> SAFE` edge) and the backbone's "same depth" caption. If you sequenced the build literally from the backbone graph or the build-order graph, you would try to start C34 before the eval tier exists and stall.
**Fix.** Distinguish the fence's two components by depth. C43's boundary-typing half is genuinely Gas-City-only (C42) and parallel to the eval tier — keep that. But C34 (holdout integrity) is downstream of the eval tier (C30/C32). Either (a) add an `EV --> SAFE` edge to the build-order graph and drop the "same depth" / "parallel" language for the C34 portion, or (b) split the fence so only the C43-C42 half is shown parallel to the eval tier and C34 is shown hanging off C30/C32. The backbone-graph caption "Inspect AI and the fence sit at the same depth" should be narrowed to "the *boundary-typing half* of the fence."

### MAJOR — §backbone ring-3 (line 60) vs §backbone product order (line 50) and graph (line 32) — C34 is in the backbone but the backbone never sequences it after the eval tier

> (line 60) "**+ Safety collar → 25 components.** … **C34 holdout integrity** (without it the satisfaction score the C53 gate trusts can be gamed…)"
> (line 50) "**Product order.** `Gas City` … → `Spec intake` → `Evaluation tier` and `the fence` (parallel) → `Bootstrap`."

**Why they conflict.** C34 is admitted into the 25-component backbone as part of "the fence" product, and the stated backbone product order builds "the fence" in parallel with the evaluation tier. But C34's edge (C30, C32) means C34 cannot begin until the evaluation tier is well underway (C32 is the second-to-last eval component). So the backbone product order is internally inconsistent for the half of the fence it actually carries: it promises fence-in-parallel-with-eval, but the fence component it keeps in the backbone (C34) is strictly after most of the eval tier. (The deferred half, C43+C44, is correctly out — see the clean item below.)
**Fix.** State the backbone fence order as two-staged: C43-boundary-typing parallel with the eval tier, C34-holdout immediately after C32. Adjust line 50 to "`Evaluation tier` (and the boundary-typing half of the fence in parallel); holdout integrity C34 follows C32."

### MINOR — §intro line 3 + line 5 "57 components" / "build order across products" anchor vs catalog completeness

> (line 3) "A build order for the **57 v4 components**"

**Why noted.** The partition I reconstructed (appendix) does account for all 57 with each assigned to exactly one *primary* product, so the "57" headline is correct. The only soft spots are two components deliberately *split* across a custom/adopted pair (C46) and one named in two rows (C24) — see the two items below. No component is missing and none is doubly *owned*; flagging only so the next pass knows the count itself checks out.

### MINOR — C24 named in two product rows (lines 76 and 92)

> (line 76, CXDB external row) "**CXDB** … adopt + integrate (**you write the bridge, C24**)"
> (line 92, internal row) "**CXDB bridge** | **C24** telemetry → CXDB bridge | build from scratch …"

**Why they conflict (weakly).** C24 is *named* in the CXDB external row's "Kind of work" cell and *owned* by the separate "CXDB bridge" internal row. The external row's "Components delivered" column lists only C21, C22, so C24 is not formally double-*assigned* — but a reader skimming the kind-of-work cell could think CXDB-the-adoption delivers C24. The doc itself elsewhere is careful that the bridge is custom (line 152).
**Fix.** In line 76 change "(you write the bridge, C24)" to "(you write the bridge — C24, its own internal product below)" to remove the ambiguity.

### MINOR — C46 is split across two products by design but the partition headline "exactly one product" is strained

> (line 80) "**MLflow/Aim/W&B** … the tracking-store half of C46 meta-metrics (the *definitions* are custom)"
> (line 97) "**Meta-metric stream** | C46 (definitions; storage is the MLflow product)"

**Why noted (NOT a contradiction).** C46 is intentionally one component delivered by two cooperating products: adopted storage (MLflow) + custom definitions (Meta-metric stream). This is stated consistently in all three places it appears (lines 80, 97, 179) and the C47/C48-adopted vs C46/C49/C50-custom split is consistent at lines 81, 97–99, 169, 180–183. The build is actionable. I flag it only because a strict "every component belongs to exactly one product" partition test would trip on C46; the doc handles it honestly but the next reviewer should treat C46 as the one sanctioned exception and not "fix" it into a single owner.

### MINOR — §scheduling line 268 self-heal "chain" arrow C36 → C37 not backed by an edge

> (line 268) "self-heal capability (CXDB bridge C24 → **anomaly C36 → clustering C37** → diagnosis C38 → fix-task closure C39)"

**Why it conflicts (weakly).** The prose draws a linear arrow C36 → C37, but the per-component edges are C36 needs {C24, C21} and C37 needs {C21} — C37 does **not** depend on C36; they are siblings off C21. The dependent chain is really C21 → {C36, C37}; C37 → C38 → C39. The "→" between C36 and C37 over-states the ordering.
**Fix.** Render as "anomaly C36 / clustering C37 (parallel) → diagnosis C38 → fix-task closure C39," consistent with how the doc treats other sibling pairs.

---

## What I checked and found CLEAN (no contradiction)

- **Backbone count integrity.** 25 = 19 (ring-1 closure, line 56, recounted = 19) + 3 (ring-2: C05, C09, C18) + 3 (ring-3: C34, C41, C23). The 25-component set matches *exactly* across the seven-product mermaid (lines 28–33), the backbone table (lines 43–48), and the three rings. No drift.
- **Gas City counts.** "15 components" (line 74 master row = 15; subsection lines 111–126 = 15 rows; build-order GC node line 219 "15") and "**eleven** of those fifteen in the backbone" (line 24, line 108) — the 11 backbone Gas City components (C01,02,03,04,05,17,18,19,23,41,42) are an exact subset of the 15. Consistent everywhere.
- **"Eight depend only on Gas City"** (line 235: C02,C03,C04,C07,C18,C19,C21,C23) — verified each one's "Needs" is C01 only. Correct.
- **Critical path "ten deep"** (line 241: C01→C04→C28→C29→C32→C33→C46→C47→C48→C50) — every edge verified against per-component "Needs." Exactly 10 nodes. Correct.
- **D-20 / fence split** — which half needs C42-only vs C44 is consistent across line 47, line 58, line 94, line 200, line 245: boundary-typing = C42 only (in backbone); twin-isolation = C44 (deferred, out of backbone). The deferred-half-depends-on-Digital-twins is correctly qualified "twin-isolation half only" everywhere, so it does *not* contradict its own deferral. Clean.
- **C46 / self-optimization story** — custom definitions + adopted MLflow storage; C47/C48 adopted, C46/C49/C50 custom — consistent at every mention (see MINOR above; flagged only as the partition exception).
- **Dependency-vs-order at the product level** — Bootstrap correctly placed after Spec intake (C51/C52 need C08) and after the eval tier (C53 needs C33); eval tier correctly after Claude Code (C32 needs C29). No product placed before a product it depends on, **except the fence/eval inversion** flagged above.
- **C31-in-backbone justification** — doc is explicit (line 57) that C31 is NOT in C53's strict closure and is added on functional "a build must be run" grounds; the C53 §AC-9 quote backs it. Internally honest.

---

## Verdict: **accept-with-named-amendments**

The document is overwhelmingly self-consistent: every count cross-checks (25/19/22/15/11/10/8), the backbone diagram/table/rings agree component-for-component, the critical path verifies edge-by-edge, and the D-20 fence split and C46 self-opt split are stated coherently in all their locations. It is actionable: an implementer could sequence the build from it. The one real defect is the **fence-vs-evaluation-tier ordering** (the CONTRADICTION + MAJOR findings, which are two faces of one bug): the fence is shown parallel to the eval tier in *both* top-level graphs and in the product-order prose, yet the fence component kept in the backbone (C34) strictly depends on eval-tier components C30/C32. This would mislead a build-lead into starting holdout integrity before the judge exists. Fixing it requires only splitting the fence by depth (boundary-typing parallel to eval; holdout after C32) in three places (lines 39, 50, and the build-order graph). The remaining items are MINOR wording cleanups. Required amendments:

1. Split the fence by depth in the backbone caption (line 39), product order (line 50), and build-order graph (add `EV --> SAFE` or split the SAFE node) so C34 is sequenced after the eval tier.
2. Disambiguate C24's mention in the CXDB external row (line 76).
3. Soften the C36 → C37 arrow to sibling-parallel (line 268).
4. Optionally annotate C46 as the one sanctioned two-product component so the partition test doesn't re-flag it.

---

## Appendix — Reconstructed component → product partition (C01–C57)

Primary owning product per component, built from the catalog master tables (lines 74–102) and per-product subsections (lines 106–209). "★" = in the 25-component backbone.

| Comp | Owning product | Kind | Backbone | Per-component "Needs" (from doc) |
|---|---|---|---|---|
| C01 ★ | Gas City | adopt | ★ | C03, C04 (load-time, cycle-broken; C01=root) |
| C02 ★ | Gas City | adopt | ★ | C01 |
| C03 ★ | Gas City | adopt | ★ | C01 |
| C04 ★ | Gas City | adopt | ★ | C01 |
| C05 ★ | Gas City | adopt | ★ | C01, C18 |
| C06 | Gas City | adopt | | C04 |
| C07 | Vocabulary & glossary | custom | | C01 |
| C08 ★ | Spec intake | custom | ★ | C03 |
| C09 ★ | Spec intake | custom | ★ | C08, C05 |
| C10 | Spec intake | custom | | C08 |
| C11 | Spec intake | custom | | C08 |
| C12 | Gas City | adopt | | C01, C03 |
| C13 | Gas City | adopt | | C12, C18 |
| C14 | Methodology tooling | custom | | C12 |
| C15 | Methodology tooling | custom | | C14 |
| C16 | Methodology tooling | custom | | C12 |
| C17 ★ | Gas City | adopt | ★ | C02 |
| C18 ★ | Gas City | adopt | ★ | C01 |
| C19 ★ | Gas City | adopt | ★ | C01 |
| C20 ★ | Bead-type schema | custom | ★ | C19 |
| C21 | CXDB | adopt | | C01 |
| C22 | CXDB | adopt | | C21 |
| C23 ★ | Gas City | adopt | ★ | C01 |
| C24 | CXDB bridge | custom | | C21, C28 |
| C25 | Claude Code | adopt | | C28 |
| C26 | OTel+LangFuse | adopt | | C25 |
| C27 | OTel+LangFuse | adopt | | C26 |
| C28 ★ | Claude Code | adopt | ★ | C04 |
| C29 ★ | Model-floor policy | custom | ★ | C28 |
| C30 ★ | Inspect AI | adopt+author | ★ | C17, C42 |
| C31 ★ | Inspect AI | adopt+author | ★ | C30, C17 |
| C32 ★ | Inspect AI | adopt+author | ★ | C30, C29 |
| C33 ★ | Inspect AI | adopt+author | ★ | C32, C19 |
| C34 ★ | The fence | custom | ★ | C30, C32 |
| C35 | Override → rule loop | custom | | C28, C20, C30 |
| C36 | PyOD/HDBSCAN | adopt | | C24, C21 |
| C37 | PyOD/HDBSCAN | adopt | | C21 |
| C38 | Self-heal diagnosis & fix | custom | | C37, C21 |
| C39 | Self-heal diagnosis & fix | custom | | C38, C20, C08 |
| C40 | Gas City | adopt | | C23 |
| C41 ★ | Gas City | adopt | ★ | C01, C19, C23 |
| C42 ★ | Gas City | adopt | ★ | C04 |
| C43 ★ | The fence | custom | ★ (C42 half) | C42 (+C44 deferred half) |
| C44 | Digital twins & fidelity | custom | | C17 |
| C45 | Digital twins & fidelity | custom | | C44, C30 |
| C46 | Meta-metric stream (defs) **+ MLflow (storage)** | custom+adopt | | C33, C21, C25 |
| C47 | DSPy/Optuna (variant) | adopt | | C46 |
| C48 | DSPy/scipy (A/B) | adopt | | C47, C46 |
| C49 | Counterfactual replay | custom | | C21 |
| C50 | Promotion gate | custom | | C48, C12 |
| C51 ★ | Bootstrap | custom | ★ | C08, C20 |
| C52 ★ | Bootstrap | custom | ★ | C51, C08 (+human design-review gate) |
| C53 ★ | Bootstrap | custom | ★ | C52, C33 |
| C54 | Governance documents | custom | | C52 |
| C55 | Methodology experiment | custom | | C12, C30, C33 |
| C56 | Governance documents | custom | | C52 |
| C57 | Governance documents | custom | | C51, C43 |

**Partition integrity result:** all 57 present; exactly one owning product each, with **C46 the single sanctioned two-product split** (definitions=Meta-metric stream, storage=MLflow) and **C24 named-but-not-owned** in the CXDB external row (owned by CXDB bridge). No component is orphaned; no component is doubly owned. Backbone set = the 25 marked ★, matching the rings, the table, and the diagram exactly.
