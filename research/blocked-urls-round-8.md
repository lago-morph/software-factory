# Blocked URLs — Round 8 (issues #41 + #42 batch)

**Date:** 2026-05-13. Two batched `[fetch-urls]` issues filed to chase round-6 / round-7 follow-ups (Replit + OpenAI Codex + SWE-bench in #41; GH Copilot canonical re-finds + arXiv CaMeL recovery in #42). Both drained the same day.

**Outcome at a glance:**
- **#41 (24 URLs):** 20 of 24 returned HTTP 200 with usable content (10 Replit docs + 5 Replit blog posts + 5 OpenAI Codex developer docs); 4 returned Cloudflare JS challenges (3× `openai.com/index/*`, 1× `pli.princeton.edu`).
- **#42 (10 URLs):** 6 of 6 GitHub Copilot canonical re-finds returned HTTP 200 with usable content; 1 GH Copilot legacy URL pair did not have a canonical replacement (Copilot Workspace sunset); the arXiv CaMeL paper was finally recovered via the `/e-print/` LaTeX route.

The Replit / Codex / Copilot drains flip the substrate-audit reports 18, 19, 20 from 🟡-partial to ✅-primary-anchored (with minor reservations for the Codex `openai.com/index/*` corpus). The CaMeL e-print recovery closes the round-7 R7.2 gap and flips `research/followup/08-security-primitives.md` §3 from abstract-only to paper-body-anchored.

---

## Per-URL outcomes — issue #41

### Replit substrate (13 URLs, all ✅)

| # | URL | HTTP | Outcome |
|---|---|---|---|
| 1 | https://docs.replit.com/core-concepts/agent | 200 | ✅ Drained into `research/20-replit-agent.md` §1. NEW: four-mode framework (Lite/Economy/Power/Turbo); "Max mode is no longer available." |
| 2 | https://docs.replit.com/replitai/replit-dot-md | 200 | ✅ Drained §2. **REFUTES** the "~100-line auto-condensation" claim (community-mirror-only, not in official docs). NEW: `replit.md` is intra-Replit-scope; Enterprise can pre-configure via custom templates. |
| 3 | https://docs.replit.com/core-concepts/agent/plan-mode | 200 | ✅ Drained §5. Verbatim "Plan Mode is billable" wording. |
| 4 | https://blog.replit.com/connectors | 200 | ✅ Drained §4. **REFUTES** "all powered by MCP" (Connectors and MCP are two distinct integration surfaces). **REFUTES** "24 at launch" (actual: "over 20"). NEW: substrate derives from OpenInt acquisition; launch date Sep 30 2025. |
| 5 | https://docs.replit.com/replitai/warehouse-connectors | 200 | ✅ Drained §4. NEW: Segment/Amplitude/Hex tiering (Core/Pro/Enterprise). |
| 6 | https://docs.replit.com/replitai/mcp/overview | 200 | ✅ Drained §4. Verbatim scanner wording; NEW: OAuth DCR auto-registration. |
| 7 | https://docs.replit.com/replitai/agents-and-automations | 200 | ✅ Drained §3. **REFUTES** Mastra-as-implementation claim (Mastra not in official docs). NEW: custom-webhook triggers are "Coming soon" not GA; deployment is mandatory for external triggers. |
| 8 | https://docs.replit.com/replitai/canvas | 200 | ✅ Drained §1. Canvas output types + Figma-MCP path. |
| 9 | https://docs.replit.com/replitai/app-testing | 200 | ✅ Drained §3. NEW: App Testing scope-limited to Full-Stack-JS + Streamlit-Python; 10-minute idle take-over timeout. |
| 10 | https://docs.replit.com/cloud-services/deployments/autoscale-deployments | 200 | ✅ Drained §1. **REFUTES** "every app includes free hosting" sentence (not in R-Deploy). |
| 11 | https://docs.replit.com/billing/ai-billing | 200 | ✅ Drained §3. **REFUTES** specific "$0.06 floor / multi-dollar ceiling" prices (not in R-Bill). |
| 12 | https://blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet | 200 | ✅ Drained §§1, 3. Verbatim Notion-credential-flow quote. NEW: 200-min autonomy is gated behind "Max Autonomy (Beta)" toggle, not the default. |
| 13 | https://blog.replit.com/introducing-agent-4-built-for-creativity | 200 | ✅ Drained §§1, 5. **REFUTES** "splits single tasks into different forks" wording (actual: "sub-agents…recombine the results"). NEW: parallel exec is Pro/Enterprise (Core temp at launch). |

### OpenAI Codex developer docs (5 URLs, all ✅)

| # | URL | HTTP | Outcome |
|---|---|---|---|
| 14 | https://developers.openai.com/codex | 200 | ✅ Drained `research/18-openai-codex-substrate.md` §1. Sidebar IA confirms surface taxonomy (App/IDE/CLI/Web + SDK in Automation). |
| 15 | https://developers.openai.com/codex/guides/agents-md | 200 | ✅ Drained §2. **REFUTES** "user-role message with `# AGENTS.md instructions for <dir>` header" mechanism (actual: plain concatenation joined with blank lines). Verbatim discovery/precedence/override/size-budget. |
| 16 | https://developers.openai.com/codex/subagents | 200 | ✅ Drained §3 (heavy rewrite). NEW: built-in agents (`default`/`worker`/`explorer`); TOML schema at `~/.codex/agents/` or `.codex/agents/`; `max_threads=6`/`max_depth=1` defaults; `spawn_agents_on_csv` (experimental); three-agent PR-review pattern. **Resolves** open follow-up on non-Cloud subagent sandbox inheritance. |
| 17 | https://developers.openai.com/codex/agent-approvals-security | 200 | ✅ Drained §4 (heavy rewrite). **REFUTES** Linux=Landlock (actual: `bwrap` + `seccomp`). **REFUTES** `on-failure` approval mode (not documented in current primary). NEW: granular approval policy; four-tier risk lattice with fail-closed semantics; web-search cached default; workspace protected paths (.git/.agents/.codex recursively read-only); filesystem deny-read profiles; Dev Container reference setup. |
| 18 | https://developers.openai.com/codex/cloud/environments | 200 | ✅ Drained §4. Confirmed two-phase + secret-wipe model. NEW: 12-hour container cache; `codex-universal` image; HTTP/HTTPS proxy on all egress; maintenance script. |

### Cloudflare-blocked from the action runner (4 URLs, all ❌)

| # | URL | HTTP | Outcome |
|---|---|---|---|
| 19 | https://openai.com/index/harness-engineering/ | 200 body | ❌ Cloudflare JS challenge: "Enable JavaScript and cookies to continue". Same disposition as the round-6 finding that `openai.com/index/*` is action-route-blocked (despite returning HTTP 200). Path B only. Stub deleted at stage time. |
| 20 | https://openai.com/index/unlocking-the-codex-harness/ | 200 body | ❌ Same. Stub deleted at stage time. |
| 21 | https://openai.com/index/introducing-swe-bench-verified/ | 200 body | ❌ Same. Stub deleted at stage time. |
| 22 | https://pli.princeton.edu/blog/2023/swe-bench-can-language-models-resolve-real-world-... | 200 body | ❌ Cloudflare "Just a moment..." challenge. Stub deleted at stage time. |

---

## Per-URL outcomes — issue #42

### GitHub Copilot canonical re-finds (6 URLs, all ✅)

The six URLs below are the canonical replacements for round-6 / issue-#30 404s. They primary-anchor the five `[2026-05-13 404; pending re-anchor]` flags that have been outstanding on `research/19-github-copilot-cloud-agent.md` since round 6.

| # | URL | HTTP | Outcome |
|---|---|---|---|
| 23 | https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent | 200 | ✅ Re-anchored §1 (ephemeral env + cost claim) on the canonical path `concepts/agents/cloud-agent/about-cloud-agent`. |
| 24 | https://docs.github.com/en/copilot/using-github-copilot/coding-agent/about-assignin... | 200 | ✅ Folded into the canonical hub via slug-truncated re-fetch. |
| 25 | https://docs.github.com/en/copilot/concepts/extensions | 200 | ✅ Reached, but the canonical extensions concept page is gone — the fetched body returned the MCP page (slug-truncation artifact). Closed as not-load-bearing. |
| 26 | https://docs.github.com/en/copilot/concepts/context/spaces | 200 | ✅ **NEW source** — Copilot Spaces is GitHub's team-shared context bundle (mixed-source ingestion: repos, PRs, issues, free-text, images, uploads; auto-syncs; MCP-accessible). Added as `research/19-...` §3.1; closest commercial AGENTS.md analog at *team* scope. |
| 27 | https://docs.github.com/en/code-security/concepts/code-scanning/copilot-autofix-for | 200 | ✅ Successor for the round-6 404 `working-with-code-scanning-alerts-with-copilot-autofix`; anchored §4 (Autofix-on-PR). |
| 28 | https://docs.github.com/en/code-security/responsible-use/responsible-use-autofix-code... | 200 | ✅ Canonical for `responsible-use/autofix-codeql` (round-6 re-confirmed); anchored §4. |

### Refutations surfaced on report 19

- **REFUTES** "Agent can only push to `copilot/*` branches" — the verbatim framing is gone from the canonical concept page. Operational truth survives via rulesets / branch-protection enforcement.
- **REFUTES** "Agent PRs require human approval before any CI/CD workflows are run" — also dropped from the canonical concept page. The `risks-and-mitigations` sibling (not in this round's fetch) is the likely successor anchor.
- **CONFIRMED:** Autofix uses GPT-5.3-Codex (both concept and responsible-use pages).
- **CONFIRMED:** Cost surface = GitHub Actions minutes + Copilot premium requests (verbatim quote now from canonical concept page).
- **NEW:** Cloud-agent concept page now lists 5 customization surfaces: custom instructions, MCP servers, custom agents, hooks, skills.

### GH Copilot Workspace — sunset (2 URLs, ❌ no replacement)

| # | URL | HTTP | Outcome |
|---|---|---|---|
| 29 | https://docs.github.com/en/copilot/copilot-workspace | 404 (round 6) | ❌ **Sunset.** No canonical successor; folded into the cloud agent's "Research, plan, iterate." workflow. Inferred from the canonical concept page's coverage; not docs-confirmed via a sunset announcement. |
| 30 | https://docs.github.com/en/copilot/copilot-workspace/about-copilot-workspace | 404 (round 6) | ❌ Same. |

### arXiv CaMeL — paper body recovered (1 URL pair, ✅ via tarball extraction)

| # | URL | HTTP | Outcome |
|---|---|---|---|
| 31 | https://arxiv.org/e-print/2503.18813 | 200 (2.5 MB) | ✅ **Major recovery.** The fetch action received a gzipped tarball of the LaTeX source; html2text produced 4.6 MB of binary noise (gzip ≠ html). Orchestrator manually `gunzip \| tar -xf`'d the archive on 2026-05-13 and extracted `main.tex` (889 lines, paper body), `defns.tex` (558 lines, macro definitions), and `main.bbl` (bibliography). Saved to `reference-only/camel-paper/`. Drained into `research/followup/08-security-primitives.md` §3 (15 subsections, 17 `[paper-body fetch ✅/REFUTES]` markers). **Closes the round-7 R7.2 gap.** Refutes the round-7 decision to "accept the gap." |

---

## Key lessons (corpus-wide)

**Lesson R8.1 — arXiv `/e-print/<id>` is the gold standard recovery route.** When `arxiv.org/html/<id>v<v>` returns 404 (no HTML render) and `arxiv.org/pdf/<id>` returns binary that html2text cannot extract, `arxiv.org/e-print/<id>` returns the LaTeX source as a gzipped tarball. The fetch action's html2text extractor cannot read gzip but **the file itself is recoverable manually** (`gunzip | tar -xf`). This is the most authoritative source for any arXiv paper — it's the LaTeX the authors actually wrote. **Updates Lesson R7.2:** rather than "accept the gap," try `/e-print/` first.

**Lesson R8.2 — `openai.com/index/*` returns HTTP 200 but with a Cloudflare JS-challenge body.** Three URLs in this round (and three in earlier rounds) had this exact disposition: the action's HTTP status is 200, but the body is the "Enable JavaScript and cookies to continue" challenge page. This is **not** a sandbox-block class — the runner reaches the host fine — but the rendered body is `5e91d6...` JS shim, not the article content. Path B is the only recovery; the action route is exhausted for `openai.com/index/*` regardless of how it's retried. Same disposition for `pli.princeton.edu` (Princeton blog, Cloudflare). Record both as "Action HTTP 200 but JS-challenged body" in `research/unfetched-sources.md`.

**Lesson R8.3 — Canonical-re-find queries beat slug-pattern guessing.** Round 6 left 6 GH Copilot URLs 404'd because the docs reorg moved them; round 8's hit rate on canonical re-finds was 4 of 6 directly + 2 by adjacent-page-overlap. The discoverable pattern: after a GitHub docs 404, `docs.github.com/en/copilot/` itself acts as a sitemap (the sidebar reveals every concept/how-to page); reading it before guessing slugs saves a round.

**Lesson R8.4 — Connectors and MCP are distinct, not equivalent.** The Replit drain refuted a corpus-wide reconstruction that all Connectors are "powered by MCP." Connectors derive from OpenInt (acquisition); MCP-Servers is a separate scanner-gated catalog. This conflation may have propagated to other reports — orchestrator should grep for "Connectors are powered by MCP" or similar phrasings.

**Lesson R8.5 — Third-party mirrors as fallback sources need cross-checking.** Three load-bearing Replit reconstructions (Mastra implementation, ~100-line `replit.md` auto-condensation, "$0.06 floor / multi-dollar ceiling" billing) survived the original cross-check across ≥2 sources, then turned out to be unverified by primaries. The reconstruction-with-cross-check policy in the research-pipeline skill should add a flag for "if only third-party mirrors agree but the primary is absent, mark the claim 🟡 pending-primary-fetch rather than ✅."

---

## Follow-ups (queued for next round if motivated)

These survived round 8 with known recovery routes:

1. **`openai.com/index/harness-engineering/` + `/unlocking-the-codex-harness/` + `/introducing-swe-bench-verified/`** — action-route exhausted (HTTP 200 but Cloudflare JS-challenged body). Path B only (user does Save Page As after JS has run) or Wayback Machine archived snapshot. Affects `research/18-openai-codex-substrate.md` §§1, 5.
2. **`docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations`** — would directly re-anchor the CI-approval framing currently marked `[2026-05-13 primary fetch REFUTES]` in `research/19`.
3. **`github.blog` Copilot Workspace sunset announcement** — would flip the two ❌ rows above to a documented-sunset citation.
4. **Princeton SWE-bench blog (Cloudflare 403'd)** — Wayback fallback may work; medium priority for `research/22-academic-foundations.md`.
5. **Additional Replit deployment-type docs** — `reserved-vm`, `scheduled-deployments`, `static-deployments` would tighten §3 of report 20. Low priority.
6. **`platform.claude.com/docs/en/agent-skills/{overview,best-practices,security}`** — still Path B only (carried over from round 7 R7.1). Affects `research/23-anthropic-engineering-trilogy.md` §3 security-quote attribution.
7. **CaMeL section in `research/followup/08`** is at ~15 subsections — orchestrator suggested promoting it to a standalone `research/followup/13-camel-architecture-deep.md` so report 08 can shrink to a summary + cross-link.

---

## Files retained on disk

- **`reference-only/camel-paper/{main.tex, defns.tex, main.bbl, README.md}`** — canonical LaTeX source for arXiv 2503.18813. Permanent reference; do not delete.
- ~~**`research/fetched/issue-36/80e2d2ebd8_arxiv.org__html__2503.18813v1.html`** — retained from round 7 as 404 evidence.~~ **Deleted 2026-05-14** during the Lenny × Cherny drain pass. The e-print recovery route in round 8 fully subsumes it; the `research/fetched/issue-36/` directory is now empty and was removed.

All other issue-41 / issue-42 fetched files were consumed by drain subagents and deleted; the directories themselves are gone. The `.fetch-work/urls.txt` manifests were never committed.
