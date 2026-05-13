# Next batched fetch-urls issue — draft body

Paste the block below into a new GitHub issue with title `[fetch-urls] Round-8 — Replit + OpenAI Codex + SWE-bench` and label `fetch-urls`.

The workflow will pick it up, fetch each URL, commit to `fetched/issue-<N>`, and post a per-URL summary comment. Then run the `research-pipeline` skill (`/drain` or just `drain`) on a fresh session to fold the content into target reports.

**Hosts in this batch — all currently 🟡 reconstructed in the corpus and never tried via the action.** Per round-6 lesson (`research/blocked-urls-round-6.md`), older "Cloudflare-gated" / "known-blocked" tags on `docs.replit.com`, `blog.replit.com`, `developers.openai.com`, `openai.com/index/*` have been wrong before — try first.

**Closes / upgrades:**
- 13 Replit Agent claims in `research/20-replit-agent.md` from 🟡 → ✅
- 7 OpenAI Codex claims in `research/18-openai-codex-substrate.md` from 🟡 → ✅
- 1 SWE-bench announcement quote in `research/22-academic-foundations.md` from ❌ → ✅

**Out of scope (handled separately):**
- 6 GitHub Copilot docs URLs from issue #30 that 404'd — needs a WebSearch pass first to find the new canonical paths (GH docs reorganized); not in this batch.
- 2 of 3 platform.claude.com Agent Skills pages (best-practices, security) — JS-SPA, Path B only.
- Lenny full transcripts — user is transcribing locally.

---

## Issue body (paste below the title)

```
Round-8 follow-up batch. 22 URLs across Replit Agent docs/blog, OpenAI Codex docs, OpenAI SWE-bench announcement, and Princeton PLI SWE-bench post. All currently 🟡 reconstructed in the corpus via WebSearch / mirror sites; never tried via the action. Round-6 lesson: older "blocked" tags on these hosts may be stale. Try the action first; escalate to Path B only on real failures.

### Replit Agent (13 URLs → research/20-replit-agent.md)

https://docs.replit.com/core-concepts/agent
https://docs.replit.com/replitai/replit-dot-md
https://docs.replit.com/core-concepts/agent/plan-mode
https://blog.replit.com/connectors
https://docs.replit.com/replitai/warehouse-connectors
https://docs.replit.com/replitai/mcp/overview
https://docs.replit.com/replitai/agents-and-automations
https://docs.replit.com/replitai/canvas
https://docs.replit.com/replitai/app-testing
https://docs.replit.com/cloud-services/deployments/autoscale-deployments
https://docs.replit.com/billing/ai-billing
https://blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet
https://blog.replit.com/introducing-agent-4-built-for-creativity

### OpenAI Codex (7 URLs → research/18-openai-codex-substrate.md)

https://developers.openai.com/codex
https://developers.openai.com/codex/guides/agents-md
https://developers.openai.com/codex/subagents
https://developers.openai.com/codex/agent-approvals-security
https://developers.openai.com/codex/cloud/environments
https://openai.com/index/harness-engineering/
https://openai.com/index/unlocking-the-codex-harness/

### SWE-bench (2 URLs → research/22-academic-foundations.md)

https://openai.com/index/introducing-swe-bench-verified/
https://pli.princeton.edu/blog/2023/swe-bench-can-language-models-resolve-real-world-github-issues/
```

---

## After the action runs

1. The action will commit `fetched/issue-<N>` branch and post a per-URL HTTP-status comment.
2. Activate the `research-pipeline` skill (`/drain`) in a fresh session.
3. The drain will dispatch ~3 subagents (one per target report) in parallel, anchor verbatim quotes, refute reconstructions where they contradict primary, and flip 🟡 → ✅ rows.
4. Update `research/blocked-urls-round-8.md` with per-URL outcomes (especially: which hosts were action-reachable after all — important for future batches).
5. Open follow-up PR.
