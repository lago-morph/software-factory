# Spec: `user-facing-status-line-discipline`

- **ID**: SKILL-SPEC-3819bca95d
- **Source retrospective**: ../2026-05-25-180.md

## Intent

When the user is running multiple agents in parallel, status messages from any single agent MUST minimize cognitive load: name the file/branch/PR-number in one navigable line; do NOT sprawl cross-references; do NOT explain via "here's where to navigate to next"; do NOT enumerate multiple ways to reach the same artifact. The user is context-switching across agents; each cross-reference is a tax. In the 2026-05-25 PR #169 thread, after 4 failed markdown-link-formatting attempts, the user said "I am running a bunch of agents at the same time. I need you to be helping my workflow, not increasing my cognitive load for things like trying to figure out what branch, what document, what directory, I'm supposed to be looking at." This skill is the response.

## Trigger

Activate when:
- The user has declared running multiple agents in parallel ("I'm running a bunch of agents").
- The user has expressed cognitive-load frustration ("I'm confused about what to look at", "I have to figure out which directory").
- Inferred: any session where the agent is replying to GitHub webhook events back-to-back (high implicit chance of multi-agent context).

Negative trigger: a single-agent session where the user is co-driving in real-time — there context-richness is welcome.

## Inputs

- The user's stated context (single-agent vs multi-agent).
- The artifact the agent needs to point at (file, branch, PR number, line).

## Outputs

Status messages that follow the discipline:
- **One-line answers when possible.** "Done — PR #178" beats "Here's a summary of the work, with cross-references to the underlying analysis…".
- **One navigable identifier per artifact.** "PR #178" or "the file at `path/to/file.md`" — pick one; don't list both.
- **No "where to navigate to next" sprawls.** Don't end status with "you can also see this in PR #179, or in the file at X, or in the chat history".

## Workflow

1. Before composing a status message, ask: "is the user running multiple agents?" If yes (or unknown but webhook-triggered), apply discipline strictly.
2. Identify the ONE artifact the user needs to navigate to. The PR number is usually the right answer when the work is on GitHub; the file path is the right answer when the work is local.
3. Compose the message in one or two sentences. Lead with the verb ("Done", "Merged", "Posted"); name the artifact; stop.
4. For multi-PR status updates, use a numbered list with one artifact per line; do NOT add cross-reference notes per line.
5. For PR-comment replies that need a clickable URL, use the raw URL on its own line per AGENTS-MD-fd63756222 (markdown-link mangling rule); do not iterate through markdown-link variants.
6. NEVER include sentences like "If you also want to see X, click Y or navigate to Z."

## Concrete examples

### Example 1: 2026-05-25 webhook PR-merge replies (good shape)

After the user merged PRs in the Phase-5 stack in order, each merge produced one webhook. Agent replies:
- "PR #165 (B1 auto-005 decision brief) merged. Phase 5 stack proceeding."
- "PR #166 (B2 Wave 5.1a + 5.2 — 18 ADRs) merged. 27 Phase-5 ADRs now in main."
- etc.

One line per merge; PR number + title in parentheses; one substantive update; stop. The user can scan the chat for "merged" and see status without re-orienting.

### Example 2: 2026-05-25 PR-comment debug loop (bad shape — what NOT to do)

After PR #169 line-87 thread, the agent attempted 4 markdown-link variants to give the user a clickable URL: backtick-wrapped, plain text, raw URL, plain-label-link. Each attempt was a separate PR comment. Each failed for the same harness-formatter reason. The cumulative effect was 4 round-trips on a question the user thought was a single-message item. The right shape: attempt 1 fails → escalate to bare URL in chat output (per the markdown-link mangling rule); do not iterate.

## Anti-patterns

- **The "here are three ways to find it" reply.** When the user needs to navigate to one artifact, give them one path. Multiple paths are a tax.
- **Cross-referencing the PR description from the PR title from the file in the PR.** Pick one. The user can navigate the others themselves once they're in.
- **Webhook-reply over-elaboration.** "PR #N merged. Now Phase X is in main, which unblocks Y, which means Z." Stop at "PR #N merged."
- **Iterating through markdown-link variants for a URL that won't render.** One attempt; if it didn't work, escalate to raw URL in chat.

## Acceptance criteria

- [ ] Status messages are ≤2 sentences for routine updates.
- [ ] One navigable identifier per status message (PR # OR file path, not both).
- [ ] No "you can also navigate via X" sentences.
- [ ] PR-comment clickable URLs use raw URL on own line (per AGENTS-MD-fd63756222) after the first markdown-link attempt fails.

## Files this skill creates / modifies

- No files. This is a behavioral discipline for status output.
