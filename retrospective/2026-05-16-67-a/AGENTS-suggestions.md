# AGENTS.md suggestions — 2026-05-16-67-a (supplemental)

These are **additional** proposed AGENTS.md rules surfaced by the deeper retrospective pass on PR #67, on top of the 8 in [`../2026-05-16-67/AGENTS-suggestions.md`](../2026-05-16-67/AGENTS-suggestions.md).

Decide each on its own merits. Skip ones that don't apply; copy-paste the ones that do.

---

## Suggestion A: When one subagent run covers multiple pre-allocated checklist rows, flip ALL covered rows immediately

### Proposed addition

> **A subagent run that satisfies multiple pre-allocated checklist rows must flip every covered row in the same commit.** Do not leave any ⬜ behind on the assumption that "the combined drain note covers it". Audit at commit time: `grep -nE "⬜|🔄" <plan-or-checklist-file>` should return only the legend line (if any) after every checklist-bearing commit.
>
> *Grounded in: PR #67 — Cluster A and Cluster B were combined into a single A+B subagent run, but the individual ⬜ rows for A and B were left unflipped. The user caught the lapse post-merge.*

### Why this earns its place in your agents file

The lapse was caught by the user. The audit-trail value of the checklist is exactly what makes the lapse noticeable; tolerating ⬜ rows under a "see combined note below" gloss erodes the value. Cost: one `grep` per commit. Benefit: zero false-pending rows.

---

## Suggestion B: Verify "already present" subagent claims with `ls` + `file` before commit

### Proposed addition

> **When a subagent claims a file or figure is "already present from a prior pass", verify with `ls -la <path>` and `file <path>` before committing.** Don't trust prose claims about file existence or file type; the diff and the filesystem are authoritative.
>
> *Grounded in: PR #67 — Clusters I and K both claimed their image PNGs were "already present from prior orchestrator pass". Both were true (the indexing branch had extracted them) but the claims were unverifiable from the change report alone. A 10-second `ls` + `file` would have hardened the audit trail.*

### Why this earns its place in your agents file

`ls` + `file` is two tool calls. The alternative — discovering at PR-review time that a figure file is missing, or that a `.png` extension lies about its bytes (AVIF inside PNG, hit in Cluster H) — is far more expensive.

---

## Suggestion C: Cross-cluster verification — each new cluster's drain audits the prior cluster's table edits

### Proposed addition

> **When a drain pass touches a report's body, grep that report for stale status markers (`🟡`, `❌`, `still ❌`, `mirror-anchored`, `mirror-era`) that might have been left behind by a prior pass that updated only the sources table.** Cross-section drift between a sources-table flip and the body prose is the dominant editorial failure mode for long-lived primary-source-tracking reports. Catching it within one cluster-cycle of when it landed is far cheaper than catching it in a final synthesis pass.
>
> *Grounded in: PR #67 Cluster F — Cluster E's pass forward-edited report 18's sources table to show ✅ FULL for the Cluster-F URLs, but §1 prose / §5 author attribution / §7 follow-up list / §8 verdict were all still in 🟡 mirror-era voice. Cluster F's primary-text drain caught the drift only because Cluster F also re-read the body.*

### Why this earns its place in your agents file

The catch in Cluster F was lucky, not structural. One grep per cluster (`grep -nE "🟡|❌|mirror-anchored|mirror-era" <target-report>`) makes it structural.

---

## Suggestion D: Plan for Read-tool token-limit on index files

### Proposed addition

> **Long index / status documents may exceed the Read tool's per-call token limit.** Before reading any file whose `wc -l` shows >500 lines or whose `wc -c` shows >50 KB, plan the read in chunks via `offset` and `limit`. Don't issue a Read that you suspect will fail — the round-trip wastes a turn.
>
> *Grounded in: PR #67 Phase 0 — the very first read of `research/manual/new-index.md` (864 lines, 39,606 tokens) errored against the 25k-token Read limit. Recovery: three offset+limit chunks. Anticipating the chunking would have saved a turn.*

### Why this earns its place in your agents file

Token-limit-aware reads are a free discipline. The grep / `wc` check costs one Bash call. The alternative is one wasted turn per oversized file. Index files of this scale are recurring (the corpus has had multiple in PLAN.md / INDEX.md alone).

---

## Suggestion E: At session-end PR steps, expect to ToolSearch for `mcp__github__*` tools

### Proposed addition

> **The GitHub MCP tools are deferred — load them via `ToolSearch` before calling.** When opening, finalizing, or subscribing to a PR at session-end, the canonical pattern is: `ToolSearch query=select:mcp__github__pull_request_read,mcp__github__update_pull_request,mcp__github__subscribe_pr_activity` (or whichever subset the moment requires). Don't try to call them directly — InputValidationError.
>
> *Grounded in: PR #67 finalization — the `mcp__github__pull_request_read` tool had to be ToolSearch-loaded before reading PR review comments. The deferred-tool surface is documented in the session preface but easy to forget at session-end.*

### Why this earns its place in your agents file

Reminds the orchestrator of the harness's token-economy design. The cost of the rule is zero (the ToolSearch call is required anyway). The benefit is removing one source of "I tried to call X and got InputValidationError" friction.

---

## Suggestion F: Retrospective collision suffix — use `-a/-b/-c/...` per the self-retrospective skill

### Proposed addition

> **When a retrospective for the same PR-anchor already exists, use the lowercase letter-suffix `-a/-b/-c/...` per the `self-retrospective` skill's anti-collision rule.** Contemporaneous-plus-deeper retros for the same PR are explicitly allowed (the first runs at session-wrap, the second runs when the user asks for deeper coverage). Never overwrite the original; never renumber.
>
> *Grounded in: PR #67 — the contemporaneous retrospective landed as `retrospective/2026-05-16-67.md`; the user then requested a deeper version. The deeper version landed as `retrospective/2026-05-16-67-a.md` per the skill's documented collision policy.*

### Why this earns its place in your agents file

This is an inherited rule from the `self-retrospective` skill, but worth promoting to the AGENTS file because the collision pattern (contemporaneous + deeper) recurs and is non-obvious to readers who haven't read the skill's SKILL.md preface.
