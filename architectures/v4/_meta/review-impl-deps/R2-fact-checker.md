# R2 — Source-of-truth fact-check of `implementation-dependencies.md`

Persona: meticulous source-of-truth fact-checker. Every claim was re-derived from the authoritative sources (component-inventory.md "Depends on" column, README Part 4/5, AI-CONTEXT.md, architecture-guide-for-engineers.md), not trusted from the doc. Edge/closure/count math was re-computed programmatically from the inventory.

Severity legend: FACTUAL (wrong fact), CONTRADICTION (doc contradicts a source), MAJOR, MINOR.

---

## Findings

### License errors

**[MAJOR] doc-line 80 — "MLflow/Aim/W&B (Apache-2.0)" mis-licenses Weights & Biases.** The doc collapses three tracking stores under a single `(Apache-2.0)` label. Source says W&B is NOT Apache-2.0. README Part 4 §Principle-12 tracking row, verbatim: `| Meta-metric tracking | Records meta-metrics over time | MLflow, Aim, Weights & Biases (free tier) | Apache 2.0 / Apache 2.0 / freemium | Gas City pack |`. So MLflow=Apache-2.0, Aim=Apache-2.0, **W&B=freemium**. W&B is also absent from the Part 5 hygiene table entirely (only MLflow line 318 "Apache 2.0", Aim line 319 "Apache 2.0" appear). Fix: relabel as "MLflow/Aim (Apache-2.0) + W&B (freemium)".

**[MINOR] doc-line 78 — "LangFuse (MIT)" is internally inconsistent across the corpus, though faithful to the cited license authority.** README Part 5 (the designated license authority), line 294 verbatim: `| LangFuse | MIT (most) / **MIT** core, observability platform | Core is MIT; some integrations vary; self-host is clean |`. The doc agrees with Part 5, so this is NOT a doc error. BUT AI-CONTEXT.md repeatedly lists LangFuse as Apache 2.0 (lines 313/315/316/326/374), and README Part 4 §Principle-11 also says "LangFuse … Apache 2.0" in its placement narrative. The doc correctly followed the Part-5 hygiene table; the discrepancy is upstream corpus drift. No fix required in this doc; flagged so reviewers don't "correct" the doc toward the wrong value.

### Attribution / product-mapping checks — all clean

Every product→component attribution was confirmed against the inventory "Maps from"/description and README Part 4: Gas City delivers the 15 listed (C01-C06, C12, C13, C17-C19, C23, C40, C41, C42 — inventory subsystem "Runtime Substrate"+native rows); Claude Code = C28 agent loop (inv C28 "Claude Code agent loop") + C25 OTLP (inv C25 "Claude Code native OTLP", depends C28); CXDB = C21/C22 (inv "CXDB trajectory store"/"CXDB type registry"); Inspect AI = C30-C33 (README Part 4 §P5/§P6 all "Inspect AI"); OTel Collector C26 + LangFuse C27 (inv C26/C27); PyOD/Anomalib/sentence-transformers/HDBSCAN = C36/C37 (README §P11 rows verbatim); DSPy/Optuna/Unleash/scipy/Evidently = C47/C48 (README §P12); Pact MIT for C45 (Part 5 line 309). No mis-attribution found.

### Dependency-edge checks — all 57 verbatim-correct

Re-derived every per-component "Needs" entry in the doc's mini-tables (Gas City, Claude Code, CXDB, Inspect AI, observability, custom-products tables) against the inventory "Depends on" column. **Zero mismatches across all 57 components.** Spot example: C46 "Needs C33, C21, C25" === inventory C46 "Depends on … C33, C21, C25". C43 stated as inventory `C42, C44` (doc line 58) === inventory row C43 "Depends on … C42, C44".

### Count / quantified-claim checks — all correct

- "Gas City delivers 15 / eleven in backbone" — list has exactly 15; the 11 bolded backbone IDs match. OK.
- "25-component backbone" — re-derived ring1(19)+runflow(C05/C09/C18→22)+collar(C34/C41/C23→25); product-table union also = 25, sets identical. OK.
- "19 components (ring 1)" — strict closure of {C53,C43-via-C42-only} = **18**; doc lists 19 by *adding C31 on functional grounds* and says so explicitly (line 57: "strict closure of C53 alone does not transit C31"). Internally consistent; see MINOR note below.
- "22" / "25" rings — OK.
- "critical path ten deep" — longest chain = 10 levels; doc's path C01→C04→C28→C29→C32→C33→C46→C47→C48→C50 is edge-valid and length 10. OK.
- "thirteen wide" — widest dependency level = 13 (C05,C06,C08,C12,C17,C20,C22,C28,C37,C40,C41,C42,C49). OK.
- "eight depend only on C01" — exactly {C02,C03,C04,C07,C18,C19,C21,C23}; matches doc line 235 verbatim. OK.

### Cycle claims — correct

Literal 2-cycles in inventory edges = exactly **{C01↔C03, C01↔C04}** (both touch C01) — matches doc line 134. C19/C20 is one-directional (inv: C20 "Depends on C19"; C19 "Depends on C01" — no C19→C20), so the doc's "conceptual, not literal-edge" framing (line 136) is correct.

### OPA — brief premise does not hold; doc is silent, not wrong

The review brief asserts "the doc claims OPA is NOT used (dropped)". The doc makes **no such claim** — it never mentions OPA at all. Sources still list OPA: inventory C34 row verbatim "Read-isolation policy (perms + OPA + rig partition)"; README line 425 "OPA policy for finer control later"; AI-CONTEXT lines 303/335 list OPA (Apache 2.0). The doc's C34 description ("Holdout integrity") omits OPA but does not deny it. **No factual error** — at most an omission, not a contradiction.

### MINOR — ring-1 framing is loose

**[MINOR] doc-lines 56-57 — "Dependency closure of the two apexes — 19 components" then admits C31 is not in the closure.** The header calls 19 "the transitive closure" but the strict closure is 18; C31 is a functional add. Wording conflates "closure (18)" with "closure + 1 functional add (19)". Recommend: "18-component strict closure + C31 (functional) = 19" to avoid a reader re-deriving 18 and thinking the doc erred.

### Unverifiable-but-uncontradicted

"35 of the 57 components in flight" (line 274) is a product-grouping estimate, not a graph invariant; not independently falsifiable from the inventory but not contradicted.

---

## Verdict: **accept-with-named-amendments**

Rationale: The doc is exceptionally faithful to the inventory — all 57 dependency edges, both cycles, the C19/C20 direction, the 25-backbone membership, and every numeric claim (10-deep, 13-wide, 8-only-C01, 15/11 Gas City) re-derive correctly from the source of truth. No FACTUAL or CONTRADICTION-class error against the inventory was found. The only substantive defect is one license mislabel (W&B as Apache-2.0; amend line 80). Secondary: tighten the ring-1 "closure" wording (line 57) and be aware the LangFuse-MIT value, while matching Part 5, conflicts with the rest of the corpus. None of these undermine the build order. Amend the three named items and accept.
