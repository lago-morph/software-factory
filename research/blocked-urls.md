# Blocked URLs — Sandbox Reachability Report (v5)
**Date:** 2026-05-10 (v2); 2026-05-11 (v3 update after issue #8 Wayback fetches landed); 2026-05-11 (v4 update after first manual browser-cookie fetch round); 2026-05-11 (v5 update after second manual round — "Save Page As" + reader-view + user notes)
**Version:** 5 — incorporates two rounds of manual content drops into `research/manual/`, drained per the research-pipeline skill's Phase 0.
**Purpose:** Originally enumerated every URL the research subagents could not fetch. After the user committed local copies of the previously-blocked pages to the repo root, most became accessible (v2). Issue #8 ran a Wayback-Machine retry pass for the rest (v3). v4 recorded a third pass — manual browser-cookie fetches. v5 records a fourth pass — text exports from "Save Page As" on a browser that had solved the Cloudflare challenge, plus reader-view exports of two Lenny pages with user-supplied notes. The el-kaim Dark Factory article is now ✅ FULL; both Lenny URLs are confirmed **video-only** (no text body exists at the URL). Local cached source files have since been deleted from the repo (content is incorporated into the reports).

---

## What is now accessible

The user committed local saved copies of the previously-blocked pages to the repo root. After verification:

| Original URL | Local file | Status |
|---|---|---|
| https://factory.strongdm.ai/ | `factory.strongdm.ai.html` | ✅ ACCESSED (27 KB, real content) |
| https://factory.strongdm.ai/principles | `factory.strongdm.ai__principles.html` | ✅ ACCESSED |
| https://factory.strongdm.ai/techniques | `factory.strongdm.ai__techniques.html` | ✅ ACCESSED |
| https://factory.strongdm.ai/techniques/dtu | `factory.strongdm.ai__techniques__dtu.html` | ✅ ACCESSED |
| https://factory.strongdm.ai/techniques/gene-transfusion | `factory.strongdm.ai__techniques__gene-transfusion.html` | ✅ ACCESSED |
| https://factory.strongdm.ai/techniques/pyramid-summaries | `factory.strongdm.ai__techniques__pyramid-summaries.html` | ✅ ACCESSED |
| https://factory.strongdm.ai/techniques/semport | `factory.strongdm.ai__techniques__semport.html` | ✅ ACCESSED |
| https://factory.strongdm.ai/products | `factory.strongdm.ai__products.html` | ✅ ACCESSED |
| https://factory.strongdm.ai/products/attractor | `factory.strongdm.ai__products__attractor.html` | ✅ ACCESSED |
| https://factory.strongdm.ai/products/cxdb | `factory.strongdm.ai__products__cxdb.html` | ✅ ACCESSED |
| https://every.to/guides/compound-engineering | `every.to__guides__compound-engineering.html` | ✅ ACCESSED |
| https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents | `every.to__chain-of-thought__...html` | ✅ ACCESSED |
| https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it | (manual fetch incorporated; cache file deleted) | ✅ FULLY ACCESSED — manual browser-cookie fetch (2026-05-11) returned the full article past the paywall. Post-paywall content (five Cora use cases, five-step playbook, three metrics, $400/$400k claim) incorporated into report 03 §"The Cora playbook". |
| https://every.to/p/the-agent-that-saved-my-brain | `every.to__p__the-agent-that-saved-my-brain.html` | ✅ ACCESSED |
| https://simonwillison.net/2026/Feb/7/software-factory/ | `simonwillison.net__2026__Feb__7__software-factory.html` | ✅ ACCESSED |
| https://simonwillison.net/guides/agentic-engineering-patterns/ (index + 12 chapters) | 13 separate local files | ✅ ALL ACCESSED |
| https://simonwillison.net/2026/Feb/23/agentic-engineering-patterns/ | `simonwillison.net__2026__Feb__23__...html` | ✅ ACCESSED |
| https://simonwillison.net/2025/Sep/30/designing-agentic-loops/ | local | ✅ ACCESSED |
| https://simonwillison.net/2025/Oct/5/parallel-coding-agents/ | local | ✅ ACCESSED |
| https://simonwillison.net/2025/May/22/tools-in-a-loop/ | local | ✅ ACCESSED |
| https://simonwillison.net/2025/Sep/18/agents/ | local | ✅ ACCESSED |
| https://simonwillison.net/2025/Apr/19/claude-code-best-practices/ | local | ✅ ACCESSED |
| https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/ | local | ✅ ACCESSED |
| https://simonwillison.net/tags/evals/ | local | ✅ ACCESSED (large index) |
| https://simonwillison.net/tags/agentic-engineering/ | local | ✅ ACCESSED (large index) |
| https://news.ycombinator.com/item?id=46924426 | `news.ycombinator.com__item__q__id_eq_46924426.html` | ✅ ACCESSED (712 KB, 459 comments, 304 points) |
| https://www.lennysnewsletter.com/p/an-ai-state-of-the-union | (all retrieval routes consumed; cache files deleted) | 🎬 **VIDEO-ONLY** — round-2 user note (2026-05-11) confirmed *"only content here was a video. However there were references."* The "paywall" is around a "biggest takeaways" editorial summary, not a transcript. Three retrieval routes attempted (direct fetch, Wayback issue #8, manual browser-cookie). To extract Willison's actual answers, a **transcript-extraction service** against the YouTube video (`https://youtu.be/wc8FBhQtdsA`) is needed — paywall bypass would not help. References list already incorporated into report 06. |
| https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens | (all retrieval routes consumed; cache files deleted) | 🎬 **VIDEO-ONLY** — same disposition as the sibling Willison interview. Round-2 user note: *"Confirmed this was just a video. Here are references at end."* YouTube URL: `https://youtu.be/We7BZVKbCVw`. **The "10–30 PRs/day" and "10–15 parallel sessions" Cherny numbers remain un-primary-sourced** — they were carried over from secondary summaries (see report 06 §"Lenny's Boris Cherny interview"). |

GitHub repos remained accessible throughout (the user did not need to commit copies).

---

## What remains BLOCKED

| URL | Status |
|---|---|
| https://el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e | ✅ **FULLY ACCESSED 2026-05-11** via "Save Page As → text export" from a real browser session that had solved the Cloudflare challenge. 41 KB text export incorporated into `research/07-dark-factory.md` — report 07 transitions from reconstructed-from-secondary-sources to primary-source-anchored. Three prior routes failed (direct fetch, Wayback never archived, manual browser-cookie returned a 5.8 KB JS-challenge stub); the fourth route (Path B in `unfetched-sources.md`) is the one that worked. |
| https://medium.com/@welkaim/about | ❌ Cloudflare challenge page only. Manual browser-cookie fetch (2026-05-11) also returned a 5.5 KB stub. Low priority now that the canonical Dark Factory article (above) is unlocked — this is the author profile, not the article. |
| https://welkaim.medium.com/ | ❌ Cloudflare challenge page only. Manual browser-cookie fetch (2026-05-11) also returned a 5.5 KB stub. Low priority — same disposition as the @welkaim/about page. |

**Implication for report 07 (Dark Factory):** the reconstruction-from-secondary-sources stands. No verbatim El Kaim quotes are available in the corpus. Sibling reports (01, 05, 06) attribute the "Dark Factory" framing to Dan Shapiro, not to El Kaim — so cross-attribution from sibling primary sources cannot upgrade the El Kaim report's quote confidence.

**To fully resolve report 07:** the user would need to fetch the el-kaim Medium article from a non-Cloudflare-challenged environment (e.g., manual browser save with cookies). Wayback is no longer a viable route — the article was never archived there.

---

## Recommended future fetches (sources surfaced by primary access)

The primary-source pass surfaced new external references worth fetching. Highest leverage first:

### From StrongDM Factory homepage footnotes

1. **Luke PM, "The Software Factory"** — cited in `/principles` footnote 1
2. **Sam Schillace, "I Have Seen the Compounding Teams"** — cited in `/principles` footnote 1
3. **Dan Shapiro, "Five Levels from Spicy Autocomplete to the Software Factory"** — the maturity-model essay; cited verbatim by Simon Willison and El Kaim
4. **Competitor factories** named in homepage footnote 2: Devin, 8090, Factory, Superconductor, Jesse Vincent's Superpowers

### From every.to articles (Klaassen's sibling pieces)

5. **Kieran Klaassen, "Stop Coding and Start Planning"**
6. **Kieran Klaassen, "Teach Your AI to Think Like a Senior Engineer"**
7. **Kieran Klaassen / collaborators, "How Every Is Harnessing the World-changing Shift of Opus 4.5"**

### From HN thread (community Attractor implementations)

8. **danshapiro/kilroy** (Go reimplementation of Attractor)
9. **smartcomputer-ai/forge** (Luke Buehler)
10. **joyrexus/software-factory** (synthesis repo)
11. **17+ named community Attractor ports** across Rust, Go, Python, Java, F#, PHP, Tcl, TypeScript, Scala, Ruby, C, C# — surfaced in the StrongDM Attractor product page; full list on `factory.strongdm.ai/products/attractor`

### From Lenny references (45 confirmed URLs)

12. **Boris Cherny, "Head of Claude Code: What happens after coding is solved"** (Feb 19, 2026 Lenny interview) — the strongest scaling data point in the corpus; cited but not directly read
13. **Sander Schulhoff, "The coming AI security crisis"** and "AI prompt engineering in 2025"
14. **arXiv: "The Prompt Report"** (2406.06608) and DeepMind CaMeL (2503.18813)
15. **Tesseract / Wispr Flow / NanoClaw / kākāpō** (Lenny references; relevance unclear without fetching)

### From other research reports' open questions

16. **2389 Research, "The Dark Factory Is a .dot file"** — deep dive on Gas Town's DOT-graph orchestration
17. **Stanford CodeX, "Built by agents, tested by agents, trusted by whom?"** — governance/liability angle
18. **The Pragmatic CTO, "The software factory when no human..."** — pitfalls write-up

### Paywalled but accessible with credentials

19. **Lenny Rachitsky, "An AI state of the union"** — **video-only.** 2026-05-11 user note confirmed no text body exists at the URL; the actual content is at `https://youtu.be/wc8FBhQtdsA`. A transcript-extraction service against the YouTube video is the only remaining recovery path.
20. ~~**Kieran Klaassen, "My AI Had Already Fixed..."**~~ — **Resolved 2026-05-11.** Manual browser-cookie fetch returned the full article; post-paywall content (five Cora use cases, five-step playbook, three project metrics, the $400/$400k claim) incorporated into report 03 §"The Cora playbook".
21. **Boris Cherny, "Head of Claude Code: What happens after coding is solved"** — same disposition as #19. **Video-only.** YouTube URL: `https://youtu.be/We7BZVKbCVw`. The "10–30 PRs/day" and "10–15 parallel sessions" claims remain un-primary-sourced.
22. ~~**William El Kaim, "The Dark Factory..."**~~ — **Resolved 2026-05-11.** Full article incorporated into report 07; see "What remains BLOCKED" table above.

---

## Effect on the architectures

Most architecture decisions were *not* materially changed by the primary-source pass. The four architectures remain stable. Specific corrections that propagated:

- **DTU = Digital Twin Universe** (not Users) — corrected in all four architecture specs.
- **"Willison: 4 agents → 11 AM" was fabricated** — softened to "mentally exhausted by 11 AM" in synthesis and Architecture 4 (which had cited the specific number).
- **Simon's review stance is more nuanced** — synthesis §3.1 updated; Architecture 1 reference unchanged (Simon is not the only justification for that architecture).
- **Self-improving prompts** (Klaassen frustration-detector, Tedesco Montaigne) — added to Architecture 2 as a documented pattern.
- **Scenarios partially agent-generated** — added as a primitive in synthesis §5.1 and referenced in Architecture 1's scenario discussion.
- **Attractor is "graph-structured" generically; DOT is community convention** — corrected in synthesis §3.2 and §3.8; Architecture 1 and Architecture 4 references softened.
- **Compound engineering canonical loop is 4-step** (Plan → Work → Review → Compound), not 5 — corrected in Architecture 2.
- **Looking-the-part hazard** — added as part of failure mode F7 (normalization of deviance) in synthesis §4.

The recommended starting path in the comparison doc (Atelier as baseline + selective borrows) is unchanged.
