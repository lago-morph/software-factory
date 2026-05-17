# Category taxonomy

The catalog uses **15 canonical categories** as the primary subject-matter grouping. Every record SHOULD have at least one category tag from this list. A record can have multiple — and SHOULD if it genuinely spans multiple subjects (e.g., a 2389-research product page is both `dark-factory` and `other-vendor-substrate`).

The renderer in `scripts/render-sources-md.py` groups records by category in the generated markdown view. A record with N category tags appears in N sections — deliberate duplication for browsability.

## The 15 categories

| Tag | Definition |
|---|---|
| `dark-factory` | Shapiro / El Kaim / StrongDM foundational essays on AI-built software as a paradigm. The Dark-Factory canon. |
| `intent-driven-architecture` | Intent-driven / continuous enterprise architecture, RISE-style automation, software product-line variability. El Kaim book chapters live here. |
| `spec-authorship` | Requirements engineering, BMAD, scenario testing, INCOSE primer, spec-as-prompt practice. |
| `willison-canon` | Simon Willison's collected writings + interviews. Treated as its own subject because of dominance and breadth (≥23 essays + the SOTU transcript). |
| `compound-engineering` | Compound-engineering workflows, personal harnesses, lived-experience practitioner accounts (Klaassen, Reed, Nystrom, *How I AI* episodes). |
| `anthropic-substrate` | Claude Code substrate, Anthropic engineering posts on infrastructure, Cherny / Anthropic interviews. |
| `openai-substrate` | Codex substrate, OpenAI cookbook, running-codex-safely docs, agents.md / subagents specs. |
| `other-vendor-substrate` | GitHub Copilot cloud-agent, Replit Agent v3/v4, Devin / Cognition, Factory.ai, Tabnine, Cursor, Kiro, OpenHands, Google Gemini CLI, Notion, Every.to harnesses, StrongDM. |
| `skills-composition` | Skills as a composition primitive — agentskills.io, Anthropic Agent Skills docs + cookbooks, El Kaim codex/skill substrate, MCP protocol. |
| `evals-and-benchmarks` | SWE-bench, SWE-agent, AlphaCode, CodeGen, evals primers (Husain, Shankar, Yan), prompt-engineering survey. |
| `academic-foundations` | Academic methodology papers: underspecification, multi-task program benchmark, CHI/ICSE/ESEC studies. OpenReview pages. |
| `security-primitives` | Threat models, prompt-injection defenses, capability/data-flow security (CaMeL, AgentDojo). |
| `governance-and-legal` | SOX/GDPR audit, Caremark / RSI board exposure, NHTSA levels, AUTOSAR, ISO 42010, Stanford CodeX series. |
| `ai-engineering-culture` | Team-level dynamics, organisational culture, the social/operational side of AI engineering. Schillace Sunday Letters live here. |
| `meta-synthesis` | Derived syntheses over the corpus (counterfactual deep-research outputs, QC re-reads, internal artifacts). |

## How to choose a tag during ingestion

When drain stage 3 creates or updates a record, it should set `tags` based on a quick read of the source. Heuristic order:

### 1. URL-based defaults (catch most cases)

| URL pattern | Default tag(s) |
|---|---|
| `simonwillison.net/*` | `willison-canon` |
| `hamel.dev/*`, `eugeneyan.com/*` | `evals-and-benchmarks` |
| `developers.openai.com/*`, `openai.com/index/*` | `openai-substrate` |
| `blog.replit.com/*`, `docs.replit.com/*` | `other-vendor-substrate` |
| `docs.tabnine.com/*` | `other-vendor-substrate` |
| `factory.ai/*`, `cognition.ai/*`, `cursor.com/*`, `kiro.dev/*` | `other-vendor-substrate` |
| `docs.github.com/*` (Copilot pages), `github.blog/*` | `other-vendor-substrate` |
| `docs.all-hands.dev/*`, `swe-agent.com/*`, `openhands*` | `other-vendor-substrate` |
| `factory.strongdm.ai/*`, `strongdm.com/*` | `other-vendor-substrate`, `dark-factory` |
| `anthropic.com/engineering/*` | `anthropic-substrate` |
| `platform.claude.com/docs/en/agent-skills/*`, `support.claude.com/*` Skills | `skills-composition` (also `anthropic-substrate`) |
| `every.to/*` | `compound-engineering` |
| `lennysnewsletter.com/p/head-of-claude-code-*` | `anthropic-substrate` |
| `lennysnewsletter.com/p/an-ai-state-of-the-union` | `willison-canon` |
| `chatprd.ai/how-i-ai/*` | `compound-engineering` |
| `law.stanford.edu/*` | `governance-and-legal` |
| `arxiv.org/*` (SWE-bench / SWE-agent / AlphaCode / CodeGen / eval / benchmark in title) | `evals-and-benchmarks` |
| `arxiv.org/*` (CaMeL / prompt injection in title) | `security-primitives` |
| `arxiv.org/*` (OpenHands in title) | `other-vendor-substrate` |
| `arxiv.org/*` (everything else academic) | `academic-foundations` |
| `pli.princeton.edu/*` | `evals-and-benchmarks` |
| `openreview.net/*` | `academic-foundations` |
| `swebench.com/*`, `ar5iv.labs.arxiv.org/*` | `evals-and-benchmarks` / `academic-foundations` |
| `2389.ai/*`, `2389-research/*` | `dark-factory`, `other-vendor-substrate` |
| `danshapiro.com/*` | `dark-factory` |
| `el-kaim.com/*`, `welkaim.medium.com` | `dark-factory` |
| `sundaylettersfromsam.substack.com/*` | `ai-engineering-culture` |
| `jayminwest.com/*` | `ai-engineering-culture` |
| `lukepm.com/*`, `bcgplatinion.com/*`, `thepragmaticcto.com/*` | `dark-factory` |
| `addyosmani.com/*` | `ai-engineering-culture` |

### 2. Title-based augmentations (apply on top of URL defaults)

| Title contains | Add tag |
|---|---|
| `skill` (lowercase) | `skills-composition` |
| `eval` or `judge` | `evals-and-benchmarks` |
| `prompt injection`, `CaMeL` | `security-primitives` |
| `harness` | `ai-engineering-culture` |
| `dark factory`, `dot file`, `dotpowers` | `dark-factory` |
| `Anthropic` or `Claude` + `agent` | `anthropic-substrate` |
| `Shapiro` | `dark-factory` |
| `INCOSE`, `Neves-Bussmann` | `academic-foundations` |
| `Tabnine` | `other-vendor-substrate` |

### 3. Manual override

When automation gets it wrong (most often: a hybrid source that legitimately spans 2+ categories the heuristics miss), edit the tags directly via the standard catalog-edit pattern:

```bash
F=reference-only/sources.json
jq --arg id "0a7f3b8e00" --arg tag "compound-engineering" \
   '.[$id].tags = ((.[$id].tags // []) + [$tag] | unique)' "$F" > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

## What if a record genuinely fits none of the 15?

That's a signal to either:
1. **Reconsider** — most sources fit at least one of the 15. Re-read the source.
2. **Promote a new category** — if you find 5+ records that all share a coherent theme not covered by the 15, propose extending the taxonomy. Edit this file + the renderer's `CATEGORY_ORDER` list together.

Don't leave records untagged forever. The renderer's "(no category)" bucket exists for transient cases (drain just ran, manual review pending), not as a permanent home.

## Rendering behavior

`scripts/render-sources-md.py` renders one section per category in the order defined by `CATEGORY_ORDER`. A record with N tags appears in all N sections — full content each time, not a stub. This means a long cross-cutting source (e.g., a Schillace post that's both `compound-engineering` and `ai-engineering-culture`) will appear twice in the rendered file. That's deliberate: navigation by category is the primary access pattern; full re-listing is cheaper than navigation cost.

A "By status" cross-cutting section follows the category view as a compact link list (no duplication of the full record block).
