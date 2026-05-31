# optimized-differences.md — Decision-Readiness Review

**Persona.** Decision-readiness adversary for jonathan@manton.com (35+ years engineering, reads original sources, visual thinker, corpus-vocabulary discipline).
**Target.** `/home/user/software-factory/architectures/v4/optimized-differences.md` (254 lines, 7 sections + appendix).
**Verdict tier.** accept-with-named-amendments — the report is close to decision-ready but three load-bearing claims need fact-correction and one trade-off column needs to be honest about effort, not "rewind cost."

---

## Section 1 — Findings table

| id | severity | location | finding | suggested fix |
|---|---|---|---|---|
| R-1 | blocker | §2 line 38 ("One-sentence summary") | The headline quote *"Track B has not abandoned v4; it has operationalized it"* is attributed as **"verbatim from the DELTA-enumeration research"** but does NOT appear in `optimized-deltas-enumeration.md`, `optimized-deltas-independence.md`, or `optimized-deltas-force-skeptic.md`. The phrase appears nowhere in the cited source files. This is a fabricated cite presented as a quote. | Either find the real source passage (closest is independence file §4 paragraph about Track A's "fixed proof" stance) and quote it correctly, OR drop the quote marks and the "verbatim" attribution and present the sentence as the report author's synthesis. |
| R-2 | blocker | §2 line 55–61 (three-DELTA table) | Claim: *"three deltas BOTH the independence analyst and the skeptic flagged as the highest-value cherry-pick candidates."* In fact the skeptic's promote-picks (§4 of report, line 166–170, also confirmed in skeptic source file) are **C42-DELTA-02, C20-DELTA-04, C29-DELTA-02**. The independence file's top-5 (§4 of source) are **C19-DELTA-04, C23-DELTA-02/03, C02-DELTA-05/06, C09-DELTA-04, C42-DELTA-03/04**. The §2 table picks C42-DELTA-02 (skeptic only), C20-DELTA-04 (skeptic only), C09-DELTA-04 (independence only). There is **zero overlap** of the specific three between the two sources. §4 line 164 doubles down: *"These overlap perfectly with the independence analyst's top cherry-pick targets — convergent verdict across two different lenses"* — this is false on the specific deltas; only the *general theme* (security/failure operability) overlaps. | Rewrite §2's framing: these three are *the report's curated illustrative set drawn from both source lists*, not "what both lenses converged on." Rewrite §4's "overlap perfectly" sentence to honestly say "overlap on C42-family; the other two skeptic picks (C20-DELTA-04, C29-DELTA-02) do not appear in the independence top-5, and the independence top-5 includes four deltas the skeptic does not promote." |
| R-3 | major | §6 line 222 (decision table, "Rewind cost") | The "Rewind cost if wrong" column is the load-bearing decision lever (per skill: "rewind path if the choice is wrong"). Two of three options say "Low"; the third says "Medium." But "Low" for Option A glosses over the real risk: if you cherry-pick 6–15 deltas and later decide a *systemic* cluster (signing, judge policy, supply chain) was actually right, the 23 existing Track B specs go stale fast — every subsequent Sweep-1 receipt referencing the cherry-picks will need re-grounding against either A or B. The report does not name this. | Replace the "Low / Low / Medium" cells with a one-line description of *what specifically you'd have to redo*. E.g., Option A rewind = "rerun integration-pass against ~15 additional cherry-picked deltas; revive the 4 systemic Track B clusters from their existing specs." Drop the absolute rating in favor of the descriptive shape (matches skill's "descriptive effort scoping"). |
| R-4 | major | §6 line 227–229 (speculative recommendation) | Recommendation is labeled as opinion (good) but does not cite the data that supports it. The phrase *"the marginal value beyond the cherry-picks is ~120 deltas, mostly micro-improvements"* is asserted with no link to the skeptic verdict table (which actually shows 85.4% WJ, including across non-cherry-picked deltas — so "mostly micro-improvements" may understate value). The 2× wave concurrency claim is plausible but not supported in-text. | Add one sentence pointing to §4's verdict table (85.4% WJ across the full 144) and one sentence acknowledging that the 120 "non-cherry-picked" deltas include real value the skeptic deemed well-justified — the recommendation is "Option A despite the value left on the table" rather than "Option A because the rest is micro-improvement." Honest disclosure of cost. |
| R-5 | major | §3 cherry-pick table line 79–85, §5 cherry-pick table line 209–215 | The §5 table presents C42-DELTA-02 as a low-cost cherry-pick ("Only mechanism converting G21/G10 from discipline to enforcement") but per the independence source (verified) C42-DELTA-02 is classified **CLUSTER-2** linked to C04-DELTA-05, not ISOLATED. The report does not disclose that adopting C42-DELTA-02 alone is incoherent; you need C04-DELTA-05 to come along. Same for C23-DELTA-02/03 (which the report shows as a pair — good) and C09-DELTA-04 (ISOLATED, OK). | Add a "cluster-dependency" column to the §5 cherry-pick table, naming reciprocal deltas where adoption is incoherent without them. C42-DELTA-02 needs C04-DELTA-05; C19-DELTA-04 is genuinely isolated; etc. Without this, the reader will choose what looks like a one-file change and discover it's a two-file change at port time. |
| R-6 | major | §2 line 40 vs §4 line 134 — count discrepancy | §2 says *"148 named DELTAs across the 23 built components."* §4 says *"144 deltas judged"* in the skeptic verdict table. The report does not explain the gap (the difference is the 5 deltas already adopted via D-1..D-5 from INTEGRATION-PASS-1, which the independence analysis excludes — but the enumeration counts all 148 raw, while the skeptic worked from 144 unique cases). A reader making decisions from these numbers will trip on the inconsistency. | Add one inline parenthetical: *"148 raw DELTAs total; 4 were resolved via INTEGRATION-PASS-1 (D-1..D-5), leaving 144 for the skeptic verdict and 129 for the independence analysis after a second adjustment."* (Numbers exact per the source files.) |
| R-7 | minor | §3 line 91–104 (secrets-manager mermaid diagram) | Diagram has 6 nodes (good, under 7), but uses node labels that read as captions ("review-log XC-6: 'signing is a mechanism, not a control, until SecretResolver lands'") — this is a hash-ID-style reference in a diagram node. Skill says hash IDs go in footnotes, not body text. | Either move the XC-6 cite to a caption under the diagram, or replace XC-6 node with `BLOCK["signing is a mechanism, not a control, until secrets storage lands"]` and put the XC-6 reference in the appendix audit-trail. |
| R-8 | minor | §3 line 110 — "10 open questions across the corpus. The headline four" | Lists 4 of 10 but does not say where the other 6 are. The secrets-manager source file §4 has all 10 enumerated with verbatim cites — the report could just point there. | Replace "10 open questions across the corpus. The headline four:" with "10 open questions in the secrets-manager source file (§4); the four most decision-blocking:" |
| R-9 | minor | §5 line 196–200 (systemic-clusters mermaid) | Diagram is 7 nodes plus 3 "external-blocker" leaves = 8 visible nodes total (P/S/J/SC + FREE/BLOCK1/BLOCK2/BLOCK3). The skill says ≤7 elements; this is over. Auto-layout still renders but the diagram becomes a horizontal strip that's hard to read. | Split into two diagrams: (1) the 4 systemic clusters, named; (2) for each, the external blocker it sits behind. Or fold the three BLOCK* nodes into edge labels on the dotted arrows from the cluster nodes. |
| R-10 | minor | §6 line 222 (Option C "Medium" rewind) | Option C rewind says *"sunk subagent cost on track-B-only work that can't ship until external decisions land"* — but sunk subagent cost is not the same as "rewind cost." Sunk cost is a separate axis from rewind difficulty. The column is mixing two concepts. | Either rename the column "cost of being wrong" (broader), or split into two columns (rewind difficulty + sunk cost). The reader needs both axes to choose. |
| R-11 | minor | §7 "What I did not verify" | Acknowledges not verifying every DELTA. Good. But does not acknowledge R-2's specific risk: that the report's §2 table and §4 "overlap perfectly" claim were *synthesized* from the two source lists without checking whether the specific deltas actually overlap. This is exactly the kind of thing the reader needs flagged. | Add a bullet: *"I asserted the §2 three-delta set and the §4 'convergent verdict' framing without comparing the skeptic's promote-3 list and the independence top-5 list delta-by-delta. The C42 family overlaps; the specific picks do not. See review for correction."* |

---

## Section 2 — Per-attack-vector summary

1. **Decision-readiness (§6).** The three options are named with trade-offs, but the "rewind cost" column collapses what should be a multi-axis assessment ("rebuild cost" + "sunk subagent cost" + "decision reversibility") into one rating, and the speculative recommendation does not cite the data that should ground it. The reader can pick Option A on the framing as written, but if they pressure-test the "Low rewind" claim they'll find it understates the cost of reviving the 4 systemic clusters later. R-3, R-4, R-10.

2. **Format compliance.** Mostly clean. Mermaid diagram counts are at the edge: §3 secrets diagram is 6 nodes (OK), §5 systemic-clusters diagram is 7+3 (over). One hash-ID-style reference inside a Mermaid node (XC-6) bleeds AI-readable citation form into body presentation. Tables fit on screen. No "per AGENTS-MD-..." style citations. R-7, R-9.

3. **Coverage gaps (the four original questions).**
   - (a) What's optimized about Track B: **answered well**, §2.
   - (b) What's special: **answered partially**, the systemic-clusters framing in §5 lands but the cluster diagram is over-stuffed.
   - (c) Parallel track vs cherry-pick: **answered, but the trade-off column needs honesty work** (R-3).
   - (d) Where the secrets manager is used and the dependencies: **answered comprehensively**, §3 is the strongest section.

4. **Honest acknowledgments (§7).** The disclosure is good in spirit — names what was synthesized, what was read directly, what was trusted from subagent receipts, marks recommendation as opinion. Misses one important thing: the §2 fabricated-quote and §4 "overlap perfectly" claim are exactly the kinds of synthesis errors §7 should flag. The "What I did not verify" bullet should include "did not check the §2 quote against the source file" and "did not delta-by-delta compare skeptic promote list vs independence top-5." R-1, R-2, R-11.

5. **Vocabulary drift.** Disciplined. Uses corpus vocabulary throughout (DELTA, C-IDs, G-IDs, F-IDs, Track A / Track B). No invented parallel terminology. C-IDs are used; hash IDs are minimal (XC-6, D-1..D-5 reference INTEGRATION-PASS-1 rulings — these are corpus terms, not hash IDs in the skill's sense). One minor exception: §3 uses "review-log XC-6" as a body reference; the skill says hash IDs go in footnotes (R-7).

---

## Section 3 — Verdict

**accept-with-named-amendments**

Five amendments (priority order):

1. **Fix R-1 (fabricated quote in §2).** Either find the real cite or drop the quote marks and attribute the sentence to the report author.
2. **Fix R-2 (false convergence claim in §2 and §4).** The three deltas in §2 and the "overlap perfectly" claim in §4 do not survive comparison against the source lists. Rewrite both as the report author's curated illustrative set, not as cross-validated convergent picks.
3. **Fix R-3 + R-10 (rewind-cost column in §6).** Replace the absolute Low/Low/Medium ratings with descriptive scoping that distinguishes rebuild cost, sunk subagent cost, and what specifically would have to be redone. The decision lever is load-bearing.
4. **Fix R-5 (cluster-dependency disclosure in §5).** Add a column to the cherry-pick table naming reciprocal deltas. C42-DELTA-02 needs C04-DELTA-05 — without disclosure the reader will mis-scope the port cost.
5. **Fix R-6 (count discrepancy 148 vs 144).** One sentence reconciling the two numbers.

R-4, R-7, R-8, R-9, R-11 are improvements but not blockers. The amendments above are sufficient to make the report actionable.

---

## Receipt

- **File:** `/home/user/software-factory/architectures/v4/optimized-differences.review-decision.md`
- **Finding count:** 11 total (2 blocker, 4 major, 5 minor)
- **Top 3 findings:**
  1. R-1 blocker — §2 attributes a "verbatim" quote to the DELTA-enumeration file that doesn't appear in any source file.
  2. R-2 blocker — §2 and §4 claim convergent picks between skeptic and independence analyst; the specific deltas do not overlap.
  3. R-3 major — §6 "rewind cost" column collapses the decision lever; needs descriptive scoping per the human-deliverables skill.
- **Verdict:** accept-with-named-amendments (5 amendments)
- **Would I decide from this report?** Yes for Option A on §6's framing, but only because I would have read §3 (secrets-manager) directly and trusted it. The decision lever in §6 needs the rewind-cost honesty fix before I'd commit a subagent budget on that recommendation alone.
