# R6 — Skim review (busy PM persona)

Read at skim depth only: title, every heading, every table header + first column, every Mermaid caption, every **bold lead-in**, first sentence of each paragraph. Not full prose.

## Skim-reconstruction (what the argument looks like from skim signals alone)

1. This is a build order for 57 v4 components, organized by **product** — the thing you build/test/integrate as a whole — not by phases. (Title + "What this is" + "Why products, not build-phases".)
2. There are two kinds of product: **external** (adopt + configure someone else's binary/library) and **internal** (build original engineering from scratch). One Gas City install brings up ~fifteen components at once.
3. Parallelism is a soft rule: components with no edge between them build in parallel; widest is thirteen, deepest chain is ten.
4. The **backbone** is the shortest path to *safe self-building* — apex is the bootstrap-validation milestone (C53) behind the isolation fence (C43). It's 25 components but only **six products**; Gas City alone is eleven of them.
5. The backbone builds in **three rings**: possible (19, dependency closure) → runnable (22, +run-flow) → safe (25, +safety collar).
6. "The products" section is the spine: external products table, then internal products table, then a per-product subsection drill-down (Gas City, Claude Code, CXDB, Inspect AI, etc.). Gas City rests on a conformance check that nobody has run yet — that's the literal first step.
7. **Build order across products**: Gas City is the root → execution/intake fan out wide and shallow → evaluation tier is the hinge → fence + self-build + observability → self-optimization is a sequential tail you can't compress with staffing. Critical path is ten deep.
8. After the backbone, a **top-ten cost/benefit** list (vocabulary, OTLP, spec linter…) starts the next conversation; self-heal and self-optimization chains are deliberately left for last. Closes with scheduling takeaways.

**Did the reconstruction match the doc's actual intent? YES.** The product-first organizing principle lands cleanly at skim depth; the backbone/rings/build-order/top-ten spine is legible from headings + captions + bold lead-ins alone.

## Findings

`[MINOR]` Backbone heading "### The backbone is six products, not twenty-five components" — quote: *"six products, not twenty-five components"* — At skim depth this heading is one of two places (with "six products, not twenty-five") that uses the "X, not Y" negation framing. It works, but a skimmer hitting "**The backbone is six products, not twenty-five components**" right after a paragraph that just said "The backbone is **25 components**" gets a momentary whiplash (25 vs not-25). The reconciliation ("25 components but 6 products") is only in the non-skimmed prose. Fix: tighten heading to "### The backbone: 25 components, but only six products to build" so the both-numbers framing survives the skim.

`[MINOR]` "Three rings: possible, runnable, *safe*" heading + the three bold lead-ins ("**Dependency closure… — 19 components**", "**+ Run-flow → 22 components**", "**+ Safety collar → 25 components**") — At skim depth the three ring counts (19 → 22 → 25) read cleanly and are self-contained. No problem with the headings themselves; noting only that the *names* "possible/runnable/safe" in the heading don't line-map onto the three bold lead-ins (which are named "closure/run-flow/safety collar"). A skimmer can't tell which ring word goes with which lead-in. Fix: align the heading triad words with the lead-in words (e.g., lead-ins become "**Possible — 19**", "**Runnable — 22**", "**Safe — 25**").

`[MINOR]` Backbone Mermaid caption (line 40) — quote: *"The fence sits **below** the evaluation tier, not beside it"* — This caption is long (a full paragraph of qualification: which half of the fence, what it scores against, what can be pulled forward). At skim depth the **bold "below"** is the only thing that lands, and it contradicts the diagram, which shows the fence (F) fed by both G and E — i.e. it reads as *beside* E as much as below it. The "not beside it" nuance requires reading the full caption. A skim-reader who reads only "fence sits below the evaluation tier" + glances at the diagram (G-->F, E-->F) sees a fork, not a clean "below." Borderline CONTRADICTION-at-skim; rated MINOR because the diagram edges do support "below" on the C34 path. Fix: shorten the caption's first sentence to the load-bearing claim and move the half-by-half nuance into prose.

`[MINOR]` "After the backbone: the top ten to build next, by cost/benefit" — table first column is `#` (1–10), so the skim-scan of the first column yields only "1 2 3 … 10". The actually-informative column is the second ("Component (product)"). A first-column-only skimmer learns nothing from this table without drifting to column two. Fix: either lead with the component column or make the rank visible in the component column.

`[INFO/none]` No residual meta/change-narration found at skim level. No "this replaces…", "you asked…", "corrected", "now leads with…", or "see split below" in any heading, caption, or bold lead-in. The doc is clean of conversation-anchoring. Good.

`[INFO/none]` No older "phases/waves" mental model leaks at skim depth. The single visible "phase" token is C54 "phase delivery plan" / C54 "phase plan" — a *component name*, not an organizing principle, and clearly scoped as a governance document. "Why products, not build-phases" actively inoculates against the phase model. Organizing principle survives the skim intact.

`[INFO/none]` Cognitive-load checks: backbone diagram = 6 boxes (OK, ≤7). Product build-order diagram = 7 boxes (GC/EX/EV/FENCE/SB/OBS/OPT — at the limit but OK). Critical-path diagram = 10 boxes in a single LR line — exceeds ~7, but it's a deliberately linear chain (a path, not a graph), so the load is low; acceptable. External-products table has 8 rows × 4 cols and internal table 16 rows × 4 cols — the 16-row internal table is dense but the first column (product name) carries it; survives a skim. No invented jargon in headings without definition ("gene-transfusion", "lethal-trifecta", "holdout integrity" all appear with inline gloss at their definition point; "the hinge" is defined in caption + prose).

## Verdict: accept-with-named-amendments

Rationale: The skim path is fundamentally sound — the product-first organizing principle, the backbone/rings spine, and the wide-then-sequential build-order narrative all reconstruct correctly from skim signals, and there is zero residual change-narration. No FACTUAL or hard CONTRADICTION findings at skim depth. The named amendments are all MINOR polish to the skim layer: (1) make the "25 components but 6 products" both-numbers framing survive in the backbone heading, (2) align the three-rings heading words with their bold lead-ins, (3) shorten the backbone diagram caption so the bold "below" doesn't over-assert against a forked diagram, and (4) make the top-ten table's first column informative. None block acceptance.
