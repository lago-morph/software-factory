# `/reference-only/` Category Survey

**Purpose.** Reference-only intuition document for Step 1 of `/reference-only/reorg-plan.md`. Used to anticipate the eventual restored-corpus shape *before* deciding interim category names. Do not modify after Step 1.

**Method.** Surveyed source / reference tables across all 38 numbered reports in `/research/*.md` and all 12 followups in `/research/followup/*.md` (50 reports total). A "source" = one distinct primary artifact: one book counts as one (not per chapter); one vendor docs site counts as one; one paper, podcast episode, or blog post each counts as one. Cross-citations were deduplicated conservatively.

---

## 1. Rough total source count

**Estimate: ~180–220 unique primary sources** across the full citing corpus.

Counting method:
- Each report cites 5–40 sources depending on scope (single-book deep-dives ~5–10; broad academic round-ups like report 22 ~15+).
- Same source frequently appears in 2–5 reports; deduplicated to a single count.
- Range reflects uncertainty around the duplicate-removal threshold (i.e. how aggressive to be when two URLs / titles refer to "the same" source).

Sanity check: this is much larger than the ~5 source units currently on disk in `/reference-only/`, confirming the plan's framing that the present state is heavily depleted and a restoration step will land later.

---

## 2. Broad thematic clusters

Approximate distribution across the eventual restored corpus. Counts are rough.

| Cluster | ~Count | Description |
|---|---|---|
| Vendor substrate docs & product sites | 20–25 | Anthropic (platform, sandbox, skills, engineering posts), OpenAI (Codex docs), GitHub (Copilot cloud-agent docs), Google (Gemini CLI), Replit, Notion, Every.to, StrongDM. |
| Academic papers (benchmarks & methodology) | 40–50 | SWE-bench, SWE-agent, AlphaCode, CodeGen, MTPB, Anthropic multi-agent research, evals primers, prompt-engineering survey, underspecification studies. |
| Books (software engineering & systems thinking) | 8–12 | El Kaim *AI-Augmented Enterprise Architecture* (multi-chapter), Willison guide, Rumelt *Good Strategy Bad Strategy*, Deming PDCA, INCOSE Complexity Primer, Kaner *Scenario Testing*. |
| Author-driven blogs & essays | 25–35 | Willison (~23 pages), Shapiro Five Levels + companions, Schillace Sunday Letters, El Kaim Medium, Yegge, Harper Reed, Jesse Vincent, Steinberger, CJ Hess, Brier, Klaassen. |
| GitHub repositories (frameworks & implementations) | 18–25 | Attractor (spec + reference), CXDB, Kilroy, Forge, Fabro, Overstory, OpenHands, dotpowers, Beads, Mammoth, Tracker, Smasher, Coven, Claude Code, Codex CLI. |
| Podcast transcripts & interviews | 8–12 | Lenny × Willison, Lenny × Cherny, Lenny × CJ Hess (*How I AI*), Heavybit High Leverage. |
| Governance / infrastructure reference | 6–10 | NHTSA levels, Azure Landing Zones, Linux Kconfig, AUTOSAR feature models, ISO 42010, SOX/GDPR audit, MCP protocol. |
| Technical standards & open specs | 4–8 | agentskills.io, GraphQL/REST specs, DOT (Graphviz), JSON/YAML schemas, git docs. |

Dominant four clusters (vendor docs, academic papers, practitioner blogs, GitHub repos) account for ~105–135 sources or 50–65% of the total. Long-tail clusters (books, transcripts, governance, standards) round out the rest.

---

## 3. Obviously cross-cutting / hard-to-place sources

These straddle multiple clusters; the eventual categorization will need to pick one home and note the alternatives.

1. **StrongDM factory.strongdm.ai** — vendor product site, dark-factory exemplar, *and* operational methodology reference. Cited in 8+ reports.
2. **Simon Willison's collected writings** — practitioner blog, tutorial/howto, *and* implicit architecture spec. Treated as the practitioner-grade counterpart to academic foundations.
3. **Shapiro Five Levels ↔ El Kaim *Dark Factory*** — citation loop: El Kaim paraphrases Shapiro while extending him; primary/secondary relationship flips mid-corpus.
4. **Anthropic engineering posts (S12–S15)** — vendor marketing, engineering accountability narrative, *and* methodology paper. Started as blocked-vendor-doc reconstructions before becoming primary-anchored.
5. **El Kaim *AI-Augmented Enterprise Architecture* book** — academic systems thinking (Sillitto, Ashby, Deming), enterprise architecture (TOGAF, Kconfig, Azure), *and* practitioner dark-factory framing. 6+ reports across disciplinary lenses.

---

## 4. Implication for categorization

The distribution suggests interim categories should split primarily along **medium / artifact-kind** (book vs paper vs blog vs vendor doc vs repo vs transcript), since those map cleanly to how the sources arrive on disk (a book is a multi-file directory; a blog post is a single `.txt`; a paper is usually a PDF + notes). The user's eventual restoration step will refill each medium-bucket from git history, and a later step will refine to functional-purpose buckets once the full corpus is back.

That said, the dominant clusters are large enough that a single "blogs / essays" category would balloon past the ~5–15 sizing target. Expect to split practitioner blogs by author or by topic.
