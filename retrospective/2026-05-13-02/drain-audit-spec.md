# Spec: `drain-audit`

## Intent

After multiple drain rounds, the corpus accumulates a mix of ✅ / 🟡 / ⏳ / ❌ source-status rows scattered across many reports. The user periodically needs to know: *what is left before the research phase is complete?* Without a systematic audit, this question becomes "skim 24 reports and 13 followups and try to remember." With `drain-audit`, it becomes a single cross-corpus sweep that produces (a) a triaged list of remaining gaps, (b) a batched fetch issue for action-recoverable URLs, (c) a Path-B-only list staged for the user, (d) a recommended order of operations to close out, and (e) a "research phase complete?" checklist.

Grounded in this session's Phase E: the user asked "what else do we need to do?" after a long drain cycle. The first attempt at answering was the inline audit in chat (93 non-✅ rows triaged). The second attempt — at the user's request — was `user-next-steps.md` at repo root. `drain-audit` makes that pattern repeatable, callable by name, with consistent output structure.

## Trigger

**Direct phrases:**
- "Audit the sources tables"
- "What's left before we finish research?"
- "Are we done with research?"
- "Where are the remaining gaps?"
- "Triage the Sources tables"
- `/drain-audit`

**Proactive trigger:** offer at the end of a session that drained ≥2 fetch issues, since the marginal cost of running the audit is small and the value of catching missed gaps before declaring the phase done is high.

**Negative trigger (do NOT activate):**
- Mid-drain (audit while a fetch is in-flight produces a stale snapshot).
- When `research/` has no Sources tables yet (no audit material).

## Inputs

- The set of files under `research/*.md` and `research/followup/*.md` (auto-discovered).
- Optionally: a `--since` ISO date to scope what counts as "recent" in the report.
- Optionally: a `--path B-bias=high|low` flag to bias triage toward "request Path B from user" vs "accept the gap."
- Current open `[fetch-urls]` issues (read via GitHub MCP if available; gracefully degrade if not).

## Outputs

Files produced under repo root + a staged fetch issue body:

1. **`user-next-steps.md`** at repo root — human-facing audit report. Sections: status snapshot, 4-priority triage table, "research phase complete?" checklist, recommended order, in-flight tracking table.
2. **`research/next-fetch-batch.md`** — staged GitHub issue body covering the action-recoverable URLs in Priority 1. The user (or a future MCP-connected session) pastes this into a new `[fetch-urls]` issue.
3. **Inline summary in chat** — ≤ 20 lines: which P1 URLs are in the staged batch, which P2 items need Path B, which P3 items are user-decision, and the "research phase complete?" checklist row count.

Side effects:
- If GitHub MCP is available, file the staged issue directly and update `research/next-fetch-batch.md` to record the issue number.
- If a Sources row's status field is stale (e.g., a `❌` row whose URL has actually been drained since), correct it inline before producing the audit.

## Workflow

1. **Phase 0 — confirm clean state.** Run `find research/ -type f \( -name '*.html' -o -name '*.md' -o -name '*.txt' -o -name '*.pdf' \) ! -path 'research/*.md' ! -path 'research/INDEX.md' ! -path 'research/PLAN.md' ! -path 'research/blocked-urls*.md' ! -path 'research/unfetched-sources.md' ! -path 'research/followup/*' ! -path 'research/fetched/*' ! -name 'README.md'`. If non-empty, recommend a `drain` pass first and exit cleanly.

2. **Inventory non-✅ rows.** Run `grep -nE "^\| .*\| (❌|🟡|⏳)" research/*.md research/followup/*.md`. Stash the matches with file:line.

3. **Filter false positives.** Many reports have ✅/❌ cells in feature-comparison tables, not source-status tables. The source-status table is always at the bottom of each report with a heading like `## Sources reviewed` or similar. Verify each match falls under that heading by inspecting the file's structure (run `grep -n "^## " <file>` and check which H2 the matched line falls within).

4. **Triage into 4 priorities.**
   - **P1 (action-recoverable):** URLs where the host has been action-reachable in any recent round (cross-check `research/blocked-urls.md`, `research/blocked-urls-round-*.md`, and the prior session's drain outcomes). Note: hosts previously tagged "Cloudflare-only" or "Path B only" must be re-tested if they haven't been action-fetched in the last 2 rounds — those tags get stale.
   - **P2 (Path B only):** URLs that are confirmed JS-SPA (returned `Loading...` placeholders or identical-byte shells from prior action fetches) or require authentication. Stage a Path B instructions block for the user.
   - **P3 (user is doing or has agreed to do):** Items already in the user's hands per PLAN.md tracking.
   - **P4 (accept the gap):** Rows where the report's surrounding claims are firm without the missing source, OR where multiple recovery routes have failed.

5. **For each P1 cluster, draft a `research/next-fetch-batch.md` block.** One section per source cluster (Replit / Codex / etc.), listing URLs one per line, with a one-paragraph "why valuable" + "closes which claims" justification.

6. **Identify pending in-corpus cleanups that don't need new content.** Examples this session: Shapiro El Kaim-conflation attribution note (round-7 finding awaiting propagation); Anthropic Skills cookbook cross-refs into report 04 (flagged by drain subagent but not applied). Sweep `research/PLAN.md` "Cross-corpus propagation flags" and "Curated human-review backlog" sections; sweep drain notes in recent reports for `[NEW: ...pending...]` markers.

7. **Write `user-next-steps.md`** at repo root with the structure: status snapshot → 4-priority triage tables (one per priority, with cluster / affected report / URLs / why valuable columns) → pending corrections (with "applied on this branch" / "pending" markers) → bigger work needing user decisions → "research phase complete?" checklist → recommended order → in-flight tracking table.

8. **Write `research/next-fetch-batch.md`** with the issue body. Include the exact text to paste into a new GitHub issue (title + body + label).

9. **If GitHub MCP is available**, file the issue directly and update `next-fetch-batch.md` with the issue number + URL.

10. **Print inline summary** in chat: ≤ 20 lines. Include the P1 issue number (if filed) or instructions to paste the staged body. Reference the report path.

11. **Commit + push** the audit artifacts. If on a feature branch, recommend opening (or updating) a PR.

## Concrete examples

### Example 1 — clean end-of-phase audit

Session has just drained issues #29 / #30 / #31 / #36. User asks "what else needs to be done before we close research?"

- Phase 0 inventory: empty (research/manual/ has only README.md; research/fetched/ has only 11 expected 404-evidence files).
- Non-✅ rows: 93 across 17 files.
- After false-positive filter: 67 rows are real source-status entries (the rest are feature-comparison cells in reports 09 and 13).
- Triage:
  - P1: 29 URLs across reports 18 (OpenAI Codex docs), 20 (Replit Agent docs/blog), 19 (GH Copilot canonical re-finds), 22 (SWE-bench), and arxiv LaTeX source for CaMeL paper.
  - P2: 2 platform.claude.com Agent Skills docs (JS-SPA; user did one, two remain).
  - P3: Lenny Cherny + Willison full 60-min remainders (user transcribing).
  - P4: 17 rows accepted-gap.
- Staged fetch batch: `research/next-fetch-batch.md` with full URL list + paste-ready issue body.
- `user-next-steps.md` written; commit + push.
- Inline summary: "29 P1 URLs staged in `research/next-fetch-batch.md`; if MCP available, filing now as issue. 2 P2 items need Path B from you. Lenny full transcripts pending overnight."

### Example 2 — audit catches a propagation gap that didn't make it into a prior drain

Drain X refuted claim Y. Subagent applied refutation in its target report but the PLAN's "Cross-corpus propagation flags" section recorded that ~4 other reports also reference Y; those were never updated.

- `drain-audit` reads the propagation flags from PLAN.md.
- Greps the corpus for the stale framing across the listed reports.
- For each hit, surfaces it in the `user-next-steps.md` "Pending corrections" section with a `[ ]` checkbox and the exact file:line location.
- The audit does NOT auto-apply the corrections — the user reviews and decides. (Auto-application is the `cross-corpus-propagation` skill's job.)

## Anti-patterns

- **Re-running the audit during a fetch-in-flight.** If `git ls-remote origin 'fetched/*'` shows a branch the corpus hasn't merged yet, the audit will produce a stale snapshot. Run drain first.
- **Treating feature-comparison ❌ cells as source-status entries.** Reports 09 and 13 have comparison tables with ❌/🟡/✅ cells that mean "this architecture lacks feature X," not "we couldn't fetch source X." Filter by checking which H2 each match falls within.
- **Conflating "action 404'd" with "URL is dead."** Round-6 lesson: action runner IPs can return 404 for URLs that previously returned 200, when the page has been reorganized. Check sibling URLs from the same fetch issue and WebSearch for new canonical paths before classifying as P4 accept-the-gap.
- **Auto-applying P1 to a fetch issue without staging.** Always write `next-fetch-batch.md` first; let the user (and a future reader) audit what's about to be queued. Even if MCP is available and the issue is filed automatically, the staged file is the record.
- **Skipping the "research phase complete?" checklist.** The whole point of the audit is to give the user a tractable answer to "are we done?" — without that checklist, the audit is just a triage table.

## Acceptance criteria

1. `user-next-steps.md` exists at repo root, structured per the template above.
2. `research/next-fetch-batch.md` exists with a paste-ready issue body — title, label, URL list, justification.
3. Every non-✅ row in any Sources table appears in exactly one priority tier (P1 / P2 / P3 / P4) in the audit.
4. The inline chat summary is ≤ 20 lines and references file paths rather than re-quoting their content.
5. If GitHub MCP is available, the P1 issue is filed and the issue URL is recorded in `next-fetch-batch.md`.

## Files this skill creates / modifies

- `user-next-steps.md` (root) — created or overwritten.
- `research/next-fetch-batch.md` — created or overwritten.
- Optional: inline source-status row corrections in any report whose row is stale (e.g., flipping ❌ → ✅ for a URL that has actually been drained but the table wasn't updated). Always commit these inline so the audit is consistent with the corpus state.
- May trigger: GitHub issue creation via `mcp__github__issue_write` if MCP is available.
