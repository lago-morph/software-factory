# Blocked URLs — Round 6 (issues #29 / #30 / #31)

**Date:** 2026-05-13. Three batched `[fetch-urls]` issues filed earlier in the session were drained on the same day after the workflow committed `fetched/issue-29`, `fetched/issue-30`, `fetched/issue-31` to origin.

**Purpose:** Per-URL final outcome from the three batches. Anything still ❌ at the end of this round needs a follow-up fetch attempt (with corrected slug, alternate route, or known-blocked acknowledgement) and is logged into the "Follow-ups" section at the bottom.

**Cross-corpus lesson:** Most of the previously-listed "Cloudflare-only / paywall-only" classifications turned out to be **incorrect** when the action runner was actually tried. The runner reaches `simonwillison.net`, `hamel.dev`, `anthropic.com/engineering`, `arxiv.org/abs`, `danshapiro.com`, `devin.ai`, `factory.ai`, `8090.inc`, and `blog.fsck.com` directly with HTTP 200. The only round-6 hosts that still produced 200s were `docs.github.com` (and only some pages — others 404'd because of GitHub docs reorgs, not blocks). Update `research/unfetched-sources.md` Tier-A claims accordingly.

---

## Issue #29 — Anthropic engineering × 5 + Hamel × 4 + Simon Willison × 5 + arXiv CaMeL + Shapiro × 2

**Outcome:** 16 of 18 URLs returned HTTP 200; 2 returned HTTP 404 (slug guess miss + arXiv html v2 nonexistent). All 200s were drained into target reports. The two 404s are recorded with corrected follow-up paths.

| # | URL | Status | Drain target |
|---|---|---|---|
| 1 | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | ✅ 200 | `research/23-anthropic-engineering-trilogy.md` §2 (S12) |
| 2 | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | ✅ 200 | `research/23` §3 (S13) |
| 3 | https://www.anthropic.com/engineering/building-c-compiler | ✅ 200 | `research/23` §4 (S14) |
| 4 | https://www.anthropic.com/engineering/harness-design-long-running-apps | ✅ 200 | `research/23` §5 (S15) |
| 5 | https://www.anthropic.com/engineering/claude-code-sandboxing | ✅ 200 | `research/23` §8 (NEW section) |
| 6 | https://hamel.dev/blog/posts/evals-faq/ | ✅ 200 | `research/followup/07-evals-deepdive.md` §3 (confirmation of issue-#24 drain) |
| 7 | https://hamel.dev/blog/posts/llm-judge/ | ✅ 200 | `research/followup/07` §3.9 (Critique Shadowing) |
| 8 | https://hamel.dev/blog/posts/field-guide/ | ✅ 200 | `research/followup/07` §4.5 (Capability Funnel + fifteen-five) |
| 9 | https://hamel.dev/blog/posts/evals/ | ✅ 200 | `research/followup/07` §0 (philosophical anchor) |
| 10 | https://simonwillison.net/2025/Jul/3/faqs-about-ai-evals/ | ✅ 200 | `research/followup/07` (confirmation only; ✅ flipped) |
| 11 | https://simonwillison.net/2025/Jun/14/multi-agent-research-system/ | ✅ 200 | `research/followup/07` §2.6 (subagent cookbook prompts) |
| 12 | https://simonwillison.net/2025/Apr/11/camel/ | ✅ 200 | `research/followup/08-security-primitives.md` §3 (CaMeL architectural explainer) |
| 13 | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | ✅ 200 | `research/followup/08` §1 (verbatim trifecta) |
| 14 | https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ | ✅ 200 | `research/followup/08` §2 (Dual LLM verbatim) |
| 15 | https://arxiv.org/abs/2503.18813 | ✅ 200 | `research/followup/08` §3a (CaMeL abstract verbatim with 77%/84% AgentDojo figures) |
| 16 | https://arxiv.org/html/2503.18813v2 | ❌ 404 | Paper body not retrievable. **Follow-up:** try arxiv.org/pdf/2503.18813 or html/2503.18813v1. |
| 17 | https://danshapiro.com/blog/2026/01/the-five-levels-of-agentic-coding/ | ❌ 404 | **Slug guess miss.** Correct slug surfaced in companion post sidebar: `the-five-levels-from-spicy-autocomplete-to-the-software-factory`. **Follow-up:** retry `https://danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/`. |
| 18 | https://danshapiro.com/blog/2026/02/you-dont-write-the-code/ | ✅ 200 | `research/followup/01-shapiro-five-levels.md` §"Shapiro's companion post" (a different post; compressed L3→L5 narrative, not the level ladder) |

**Refutations of prior reconstruction surfaced by this drain:**
- Report 23: Opus model is 4.5 not 4.6 in S12; testing tool is Puppeteer MCP not Playwright; companion repo is `claude-quickstarts/autonomous-coding` not `cwc-long-running-agents`; "30–50 tokens per skill" not in S13; "Progressive disclosure that loads too eagerly defeats its purpose" not in S13; several security quotes attributed to S13 are actually from `platform.claude.com/.../agent-skills/overview` (not yet drained).
- followup/08: 3 "verbatim" trifecta-leg sentences were snippet-confabulated; "Any time a system combines access to private data..." quote not in primary; "first credible prompt injection defense" misquoted (load-bearing "doesn't just throw more AI" qualifier was omitted); attribution corrected to Google DeepMind + ETH Zürich; 77%/84% AgentDojo figures now exact.
- followup/07: prior issue-#24 removal of ">90% expert agreement in three iterations" REVERSED; the claim is real, the source was wrong — it's from the Hamel llm-judge post (Honeycomb / Phillip Carter), not the FAQ.

---

## Issue #30 — GitHub Copilot cloud agent + CodeQL/Autofix docs

**Outcome:** 3 of 9 URLs returned HTTP 200; 6 returned HTTP 404. The 404s are GitHub-docs reorganizations — the URLs are dead, not blocked. Five of the report's prior citations now stand on 404'd URLs and are flagged `[2026-05-13 404; pending re-anchor]`.

| # | URL | Status | Notes |
|---|---|---|---|
| 1 | https://docs.github.com/en/copilot/concepts/agents/about-coding-agent | ❌ 404 | Page moved/removed. Follow-up: locate new canonical URL. |
| 2 | https://docs.github.com/en/copilot/how-tos/agents/coding-agent | ✅ 200 | Drained into `research/19` §1–§3. The umbrella how-to page now anchors execution model, workflow, integrations. |
| 3 | https://docs.github.com/en/copilot/concepts/copilot-extensions/about-extensions-for-copilot | ❌ 404 | Page moved/removed. |
| 4 | https://docs.github.com/en/copilot/how-tos/agents/about-assigning-tasks-to-copilot | ❌ 404 | Page moved/removed. |
| 5 | https://docs.github.com/en/copilot/copilot-workspace | ❌ 404 | Page moved/removed. (Copilot Workspace is being sunset?) |
| 6 | https://docs.github.com/en/copilot/copilot-workspace/about-copilot-workspace | ❌ 404 | Page moved/removed. |
| 7 | https://docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts/about-autofix-for-codeql-code-scanning | ✅ 200 | Drained into `research/19` §4 (CodeQL Autofix verbatim: GPT-5.3-Codex model, 9-language coverage, 2,300-alert harness, 4 documented failure modes). |
| 8 | https://docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts/working-with-code-scanning-alerts-with-copilot-autofix | ❌ 404 | Page moved/removed. Partial overlap with the responsible-use page (§5 in report). |
| 9 | https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql | ✅ 200 | Drained into `research/19` §4 (CodeQL languages, three modes of operation). |

**Recovery path:** all 6 URLs need new canonical paths identified. Suggested: WebSearch for `"about-coding-agent" site:docs.github.com` to find the new home of each topic.

---

## Issue #31 — Cognition Devin / Factory / 8090 / Superconductor / Jesse Vincent Superpowers

**Outcome:** 6 of 9 URLs returned HTTP 200; 3 returned HTTP 404. **Cloudflare blocks did NOT propagate to the action runner** — these vendors are all reachable from GitHub Actions IPs.

| # | URL | Status | Notes |
|---|---|---|---|
| 1 | https://www.cognition.ai/blog/devin | ❌ 404 | Blog post URL changed. Follow-up: search cognition.ai for the current canonical "Devin announcement" URL. |
| 2 | https://devin.ai/ | ✅ 200 | Drained. Surfaces "Managed Devins" (Devin orchestrating Devins) as a new multi-agent primitive. |
| 3 | https://devin.ai/pricing | ✅ 200 | Drained. **Pricing model fully refuted vs prior reconstruction.** Current tiers: Free / Pro $20 / Max $200 / Teams $80 / Enterprise. ACU unit no longer publicly named. |
| 4 | https://www.factory.ai/ | ✅ 200 | Drained. New primitive: "Droid Computers" (persistent remote/self-hosted orchestration machines). Positioning softened to "AI that will work with you, not replace you." Series C $150M @ $1.5B confirmed on-page. |
| 5 | https://www.factory.ai/product | ❌ 404 | Page moved/removed. |
| 6 | https://www.8090.inc/ | ✅ 200 | Drained. Governance repositioning: "AI is writing your software. Who's in control?". EY Big-Four partnership confirmed by on-page quote. |
| 7 | https://www.8090.inc/blog | ❌ 404 | Blog index has moved or doesn't exist. |
| 8 | https://www.superconductor.io/ | ✅ 200 (but wrong site) | Returns the Atom.com domain-for-sale parking page. **The live Superconductor product is at superconductor.com** (`.com` not `.io`). Follow-up: re-fetch `https://www.superconductor.com/`. |
| 9 | https://blog.fsck.com/2025/10/09/superpowers/ | ✅ 200 | Drained. Workflow corrected to three-phase brainstorm/plan/implement; install path = Claude Code plugin marketplace `obra/superpowers-marketplace`; skills pressure-tested via Cialdini adversarial-persuasion scenarios. |

---

## Follow-ups (queued for next fetch round)

These survived round 6 with retrievable paths now known. Suitable for a single batched `[fetch-urls]` issue:

1. **Shapiro five-levels canonical post:** `https://danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/` (correct slug per companion post sidebar).
2. **CaMeL paper body:** `https://arxiv.org/pdf/2503.18813` or `https://arxiv.org/html/2503.18813v1` (v2 html 404'd).
3. **Superconductor live product:** `https://www.superconductor.com/`.
4. **Cognition Devin blog post:** Locate new URL via search (the announcement is still public, just moved).
5. **GitHub Copilot docs (6 URLs):** Locate new canonical paths for each via search. Particularly important: about-coding-agent (anchors several §1 claims in `research/19`), about-assigning-tasks (§2), working-with-autofix (§4–§5).
6. **`platform.claude.com/.../agent-skills/overview` (or wherever Anthropic now hosts the platform-level Agent Skills security guidance):** several quotes attributed to S13 in `research/23` are actually here. Locate and drain.

## 404 evidence files retained on disk

Kept under `research/fetched/issue-29/`, `research/fetched/issue-30/`, `research/fetched/issue-31/` as evidence of the 404 outcomes. May be deleted once the follow-up URLs above are fetched and confirmed; until then, they document what was attempted and why each attempt failed (slug-guess vs. doc-reorg vs. wrong-domain).
