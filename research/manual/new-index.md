# `research/manual/` — new-source index

**Status:** preliminary indexing pass (drafted 2026-05-16). NOT a drain. PLAN.md is intentionally untouched. The next agent will use this index to plan how to chunk the incorporation into existing reports / new reports.

This document indexes ~71 sources newly dropped into `research/manual/`. Each source has been classified along the seven thematic axes below and (where relevant) checked against the existing 27 numbered reports + 12 followups for prior processing. Sources that were already drained have been deleted; sources without any informative images have been converted to `.txt` (the original `.mhtml` deleted); sources whose images carry real informational content (architecture diagrams, dot-graph renders, taxonomy figures, etc.) are kept as `.mhtml`.

---

## The seven themes (the next agent should use these to chunk ingestion)

The user articulated seven thematic motivations for this batch. Every per-source block below is tagged with the theme numbers it speaks to.

### 1. Human attention as a scarce resource

Human attention is the **binding constraint** of the software factory. Human interaction must be **infrequent and batched** — the factory cannot scale if every decision triggers a context-switch.

**Review-summary discipline (verbatim from the brief):**
- 8–10-word headline summary
- 2–3-sentence brief summary
- 1-page guide covering rationale, pros, cons, and follow-on effects

A number of articles in this batch address how humans interact with increasingly agentic systems — collaboration patterns, attention firewalls, cognitive escrow, the "choosing the work" bottleneck — and feed directly into this theme.

### 2. Agent self-improvement, drift, and collusion

Agents can and should self-improve, but the same mechanisms create new failure modes: **drift** (gradual divergence from intent) and **collusion** (independent agents converging on undesirable joint behavior). One or two papers in this batch directly model agent collusion in a market-like setting; others address the recursive-self-improvement → board-fiduciary-exposure pipeline.

### 3. Governance and guardrails

The factory could in principle run **fully sandboxed**, but the value comes from letting it reach web resources, external tools, and the MCP ecosystem — which requires guardrails to retain trust. The tension behind reducing human interaction is therefore: **how do you automate guardrails, and even set policy so that certain decisions no longer require a human review step?** Stanford CodeX's AILCCP / 48-controls / Cognitive-Escrow / Caremark-RSI series is the densest governance cluster.

### 4. StrongDM-attractor infrastructure (dotfile + harness implementations)

There is a cluster of infrastructure built in the spirit of the StrongDM attractor:
- The **dotfile** library/example is a portable methodology — a single DOT graph that any compliant runner can execute. This batch contains the canonical 2389 Research dot-file article + the literal `dotpowers.dot` payload + the four 2389-family runners (Coven, Mammoth, Smasher, Tracker).
- Various **implemented harnesses**: danshapiro/kilroy and strongdm/attractorbench round out the picture.

### 5. Agent evaluation / probing

To know whether agents are building what we want, we have to probe them. This batch includes SWE-bench (original + Verified), Notion's spec-driven CI loop, Replit's app-testing self-validation, model-vs-model code review (CJ Hess's `kevin`/`carl` aliases), and the Tencent language benchmark — i.e. multiple primary anchors for automating evaluation.

### 6. Harness engineering

The shell around the agent matters so much that **rewriting the harness changes benchmark performance with the same LLM**. The architecture implication is that we must engineer + monitor + evaluate + optimize harnesses with explicit feedback loops. OpenAI's three previously-Cloudflare-blocked harness posts (Harness Engineering, Unlocking the Codex Harness, Running Codex Safely) and Schillace's "What is a harness" four-panel diagram are the canonical primary anchors in this batch; the Codex `.rules` Starlark DSL and Codex subagent TOML are the load-bearing primitives.

### 7. Agents as team members

If the factory is going to approach "dark factory" operation, coordination of many agents has to use **traditional management techniques alongside new ones**. Sources in this batch include Cherny's five-agents-steady-state, Schillace's "compounding teams" + Amplifier, Kim's Sendbird quest-marketplace / token-tier leaderboards, Nystrom's Boxy-from-Notion-comment background agent, and Shapiro's claw-printer / one-claw-per-employee proposal.

---

## How to read each per-source block

Each `###` block has:

- **Title** (cleaned of mojibake)
- **URL** (reconstructed from MHTML `Snapshot-Content-Location` / `Content-Location` headers)
- **Type** — `mhtml` | `txt` | `pdf` | `converted-txt`
- **Themes** — one or more of 1–7 from above
- **Summary** — 1–2 sentences in our voice, content-bearing
- **Image inventory** — total image count and whether any are informationally useful (diagrams, architecture, data) versus chrome (avatars, decorative hero art, UI screenshots)
- **Action taken** — `kept mhtml (useful images preserved)` / `converted to TXT, deleted mhtml` / `deleted (already drained into report NN)` / `txt/pdf passthrough`
- **Prior processing** — citation of any existing report/followup that already drained this URL
- **Recommendation** — one of: `incorporate into report NN`, `supplement to followup/NN`, `new report — <slug> — <one-line angle>`, `skip — already covered in report NN`, `low-priority — <reason>`

---

## Per-source entries

<!-- Subagent outputs will be inserted here in batches; see the orchestrator's assembly logic. -->
