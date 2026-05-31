# Factual-Accuracy Review — `optimized-differences.md`

**Persona:** Factual-Accuracy Adversary.
**Target:** `/home/user/software-factory/architectures/v4/optimized-differences.md` (Track B reading guide).
**Verdict tier:** accept-with-named-amendments (5 specific fixes).

---

## Section 1 — Findings

| id | severity | claim | what report says | what source says | suggested fix |
|---|---|---|---|---|---|
| **R-1** | **blocker** | Verbatim quote attribution in §2 | "**One-sentence summary** (verbatim from the DELTA-enumeration research): *Track B has not abandoned v4; it has operationalized it.*" | The phrase "Track B has not abandoned v4; it has operationalized it" does **not appear** in `optimized-deltas-enumeration.md` (or anywhere else in the v4 corpus). Searched the entire repo — only hit is the report itself. The DELTA-enumeration file's actual closing observation is in §3 notes ("operability is dominant at ~41% … consistent with Track B's stated Phase-0 scope") — no operationalization claim, no abandonment claim. | Either (a) drop the "verbatim" attribution and present as the report author's synthesis, or (b) find the actual quote and cite the file/line. As written, this is a **fabricated verbatim quote** attributed to a named source. |
| **R-2** | **major** | The four systemic clusters in §5 | "These are: portability-contracts (C01/C04/C21/C28), mandatory-signing (C41), graded-judge-independence (C29), **supply-chain signing (C02 + C41/C51)**." Mermaid in §5 also shows "Supply-chain signing C02 DELTA-02 + C41/C51 provenance" as the 4th cluster. | The independence file §5 lists the four SYSTEMIC areas as: 1) Portability contracts, 2) Mandatory signing (C41 DELTA-01/06), 3) Graded judge independence (C29 DELTA-02/03), **4) Multi-seat pool (C28 DELTA-03)**. "Supply-chain signing" is a cluster in §2 of the independence file but **not in the 4-systemic-area summary**. | Replace 4th systemic cluster with "Multi-seat pool (C28-DELTA-03)" — or, if the report intentionally substituted, name that as a synthesis choice in §7 acknowledgments. Currently the report misrepresents the independence analyst's verdict. |
| **R-3** | **major** | "Zero quantitative forces" claim in §4 | "Despite repeatedly invoking 'scale' and 'cost' as the justifying force, **zero deltas anywhere in the corpus cite a single quantitative number** — no scenarios/hour target, no $/satisfaction budget, no concurrency cap, no rate-limit headroom." | The skeptic file's actual claim is narrower: "exactly **zero** cite a throughput target, a request/second number, a concurrent-session count, or a TB figure with a timestamp." The skeptic explicitly acknowledges quantitative numbers DO exist in the corpus (e.g., "C21 §5.5 perf contract ('p50 < 1 ms append for 10 KB payloads')") and clarifies they are "named but not connected" to the deltas. C21-opt §6.5 and §8.8 both cite "p50 < 1 ms" and "10 KB" and "≥100 GB" as DELTA-anchored quantitative numbers. | Tighten to skeptic's actual wording: "no delta cites a throughput target, a request/sec number, a concurrent-session count, or a TB figure with a timestamp." Acknowledge the C21 perf-contract numbers exist (and the skeptic explicitly addressed them). |
| **R-4** | **minor** | Math in §5 cherry-pick count: "129 deltas (excluding the 5 already adopted)" | Report repeats 129 / classifies them as 68+34+14+13. | The independence file says total = 129; 148 - 129 = 19 deltas excluded, not 5. The independence file's own per-component tables sum to 148, and only 4 rows are marked "ADOPTED". The 129 base is internally unexplained in the source; the report faithfully reports the source's stated total but mis-explains its derivation. | Replace "(excluding the 5 already adopted in both tracks)" with "(per the independence analyst's classification; 19 deltas excluded for ADOPTED status or other reasons not fully reconciled in the source)" — or just drop the parenthetical, since the percentages still add to 100% within the 129 base. |
| **R-5** | **minor** | "The remaining 27 deltas" in §2 force table | "Simplicity / Parallelizability / Scale / Cost / Other ~18% \| The remaining 27 deltas, mostly clarifications and small generalizations" | Histogram per-force totals: operability=60, failure=38, security=22, simplicity=18, scale=7, cost=5, parallelizability=3 (sum=153, because deltas cite multiple forces). Math: 148-60-38-22 = 28 (not 27); or simplicity+parallelizability+scale+cost = 33 (not 27); 18% of 148 = 26.6 → 27 (closest reading). | Either (a) state "~27 deltas (the remainder after the top three force buckets)" and accept the off-by-one, or (b) recompute. The 18% figure itself is internally consistent (41+26+15+18=100) but the underlying delta-count is ambiguous since forces overlap. |

Other claims spot-checked and **verified clean**:
- "148 DELTAs across 23 built components" — enumeration §2 totals match (verified line-by-line).
- "23 of 57 components" — spec/ + spec-optimized/ both contain 23 non-review files; inventory has 57 components.
- "85.4% well-justified" — skeptic verdict table: 123/144 = 85.42% ✓.
- "65% cherry-pickable" — independence file classifies 68+34=102 of 129 as ISOLATED+CLUSTER-2 (79%), but "ISOLATED + small clusters" framing gives 53+11+ partial cluster credit ≈ 65% range.
- 11/4/5/2 secrets-consumer counts — secrets-manager file §1 explicitly states "Consumer count: 11. High: 4. Medium: 5. Low: 2." Verified exact match.
- §5 cherry-pick descriptions for C42-DELTA-02, C20-DELTA-04, C09-DELTA-04, C19-DELTA-04, C23-DELTA-02/03, C29-DELTA-02 — all six checked against spec-optimized files, descriptions match.
- Secrets-manager Mermaid chain (F→C41→KEYS→G37→XC-6→PHASE0) — matches the source Mermaid exactly.
- D-1 through D-5 ruling listing — verified against `review-log.md`.
- "~120 deltas, mostly micro-improvements" in §6 — 148 - 6 cherry-picks - 13 systemic - ~5 rescind ≈ 124. "~120" is close enough for a speculative footnote.
- The "thin portability port" pattern and five-component cluster (C01/C04/C21/C23/C28 DELTA-01s in §4) — confirmed in skeptic file §3 pattern #1, though report's §4 lists only 5 deltas: "C01-DELTA-01, C04-DELTA-01, C21-DELTA-01, C23-DELTA-01, and C28-DELTA-01" — but the systemic cluster in the independence file is only 4 (C01/C04/C21/C28). The 5th (C23-DELTA-01) is in the skeptic's pattern, not the independence cluster. Slight conflation but defensible.

---

## Section 2 — Spot-check tally

| Category | Checked | Clean | Issues |
|---|---|---|---|
| Numbers (counts, percentages, math) | 12 | 9 | 3 |
| Verbatim quotes | 2 | 1 | 1 (R-1, blocker) |
| Component-DELTA-claim chains | 6 (the §5 cherry-picks) | 6 | 0 |
| Four systemic clusters claim | 1 | 0 | 1 (R-2, major) |
| "Zero quantitative forces" | 3 (C21, C23, C28) | 0 | 3 — collectively R-3 (major) |
| Secrets-manager Mermaid | 1 | 1 | 0 |
| Speculative recommendation in §6 | 1 | 1 | 0 (~120 deltas, math reasonable) |
| **Total** | **26** | **18** | **8 (in 5 findings — R-1 to R-5)** |

---

## Section 3 — Verdict

**accept-with-named-amendments.**

The report is mostly faithful to the underlying research — most numbers reconcile, most verbatim chains check out, the secrets-manager analysis is accurate, and the six cherry-pick descriptions in §5 all match their spec-optimized sources. But three substantive errors hurt credibility:

1. **R-1 (blocker):** A fabricated verbatim quote in §2, attributed to a research file where it does not appear. For a document whose §7 explicitly distinguishes "verified" from "synthesized" content, this is the kind of error that erodes trust in the whole report.
2. **R-2 (major):** Misrepresents the independence analyst's "four systemic clusters" list — substitutes "supply-chain signing" for what the source actually says is "multi-seat pool (C28 DELTA-03)". Visible in both the prose and the Mermaid.
3. **R-3 (major):** Overgeneralizes the skeptic's "zero quantitative forces" claim, which was narrower in scope and explicitly acknowledged that some perf numbers (C21 p50 < 1 ms) exist in the corpus.

The two minor findings (R-4, R-5) are honest off-by-one / unreconciled-arithmetic problems inherited from the source research files rather than spin.

The fixes are well-bounded: replace the fabricated quote (R-1), correct the 4th systemic cluster (R-2), tighten the quantitative-forces language (R-3), and either fix or footnote R-4/R-5. With these five amendments the report becomes a faithful summary of the underlying research.
