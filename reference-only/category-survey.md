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

### Axis choice: subject-matter

Two viable axes emerge from the cluster table:

- **Medium / artifact-kind axis** — book vs paper vs blog vs vendor doc vs repo vs transcript. Maps cleanly to how the sources arrive on disk; trivial to assign.
- **Subject-matter axis** — what topic the source primarily speaks to.

**Step 1.2 chose subject-matter** after a first-pass attempt at medium-based categorisation was rejected by the orchestrator. Rationale: a reader of `/reference-only/` is hunting for primary-source backing for a *claim about a topic*, not for "all essays" or "all transcripts" — the medium is irrelevant to the navigation cue. The subject axis also surfaces cross-cutter tension (e.g. the lenny-podcast-transcripts dir straddles `practitioner-harnesses` and `anthropic-substrate`) that the medium axis hides, and that surfaced tension is useful because it forces explicit "what is this source actually *for*" decisions.

### Sizing: ~15 categories, not 6

The first pass under subject-matter used 6 categories. With ~200 sources projected, 6 categories averages 33 sources/category — 2× the plan's ~5–15 ceiling. The plan's hard rule ("split a category if it would balloon past ~15") must drive category count from the start.

**Math:** `target_category_count = ceil(estimated_total_sources / target_per_category)` → for 180–220 sources at 5–15 each, target is ~13–40 categories. The third-pass taxonomy lands on 15.

### Projected sizing per category (~180–220 total)

| Category | Projected sources at restoration | Rationale |
|---|---|---|
| `dark-factory` | 5–10 | Shapiro Five Levels, El Kaim Dark Factory canon + derivatives, StrongDM factory site, related framing essays. |
| `intent-driven-architecture` | 5–10 | El Kaim book (1 unit), TOGAF / Kconfig / Azure refs, Sillitto complexity, architectural-viewpoint papers. |
| `spec-authorship` | 5–10 | BMAD, INCOSE primer, requirements-engineering survey, Kaner scenario testing, spec-as-prompt practitioner essays. |
| `willison-canon` | 10–15 | ~23 Willison essays (some count as one collected source, some as separate), SOTU transcript, lethal-trifecta canon, Heavybit interview. |
| `compound-engineering` | 10–15 | Klaassen, Reed, Vincent, Hess, Steinberger essays + *How I AI* podcast episodes + blog-tier compound-engineering pieces. |
| `anthropic-substrate` | 8–12 | Claude Code platform docs, Anthropic engineering posts, Cherny interview, sandbox/agent-platform docs. |
| `openai-substrate` | 5–10 | Codex docs, running-codex-safely, OpenAI cookbook, Codex CLI repo. |
| `other-vendor-substrate` | 10–15 | Copilot cloud-agent, Replit Agent, Gemini CLI, Notion, Every.to, StrongDM substrate. **May need split by vendor.** |
| `skills-composition` | 5–10 | agentskills.io, Anthropic Agent Skills (1 unit), MCP protocol, El Kaim codex/skill chapter, composition primitive papers. |
| `evals-and-benchmarks` | 10–15 | SWE-bench, SWE-agent, AlphaCode, CodeGen, MTPB, evals primers. |
| `academic-foundations` | 10–15 | Underspecification studies, multi-agent collusion, prompt-engineering survey, theoretical foundations. |
| `security-primitives` | 5–10 | CaMeL, AgentDojo, threat-model papers, lethal-trifecta-as-defense pieces. |
| `governance-and-legal` | 5–10 | SOX/GDPR, Caremark / RSI board exposure, NHTSA levels, AUTOSAR feature models, ISO 42010. |
| `ai-engineering-culture` | 5–10 | Brier, Schillace Sunday Letters, Lenny *How I AI* on team-ops, organisational research, pace-layer essays. |
| `meta-synthesis` | 1–5 | ChatGPT deep-research one-shots, future counterfactual syntheses. Naturally small. |

**Most likely to need further splitting at restoration**: `other-vendor-substrate` (split by vendor); possibly `willison-canon` if it grows past 15 (split by topic — performance / lethal-trifecta / skills / etc.).

### Empty categories are first-class

6 of the 15 categories have no current on-disk source. These are not created as empty directories; they are listed in the top-level inventory README's "Categories" table with a "(empty, restored later)" marker. They encode the *anticipated* shape, which is the point of sizing for the restored corpus.
