---
name: autonomous-run
description: Operate autonomously for an extended unattended session (overnight, while-user-is-away, long-running). Negotiates a scope envelope with the user up-front to align intent; writes decision briefs with two rounds of real-subagent adversarial review when reaching user-input territory; preserves rewindability via stacked PRs (up to 30 per run); produces a required morning-summary artifact with a suggested merge order; auto-invokes the self-retrospective skill when the run stops. Use this skill whenever the user says "unattended run", "overnight", "overnight run", "long-running", "long run", "delegated execution", "while I'm away", "while I'm asleep", "kick off and walk away", "babysit this", "do this on your own", "keep working while I'm not here", or any semantically equivalent phrase. Also fires for webhook-triggered runs and scheduled jobs where the user is structurally absent.
tags: [unattended, overnight, long-running, automation, workflow, autonomous]
allowed-tools: [*]
---

# Skill: autonomous-run

The user has explicitly delegated execution for an extended session. They are
not at the keyboard. Your job is to **get a lot done** during the session,
with reversible decisions and complete morning hand-off, so they can review in
a single sitting when they return.

This skill is the procedural backbone of an unattended run. It chains several
other skills (stacked PRs, in-flight tracking, commit discipline, parallel
fanout, self-retrospective) into a single working mode.

---

## When to load

Trigger phrases (load on the first occurrence in a session):

- "unattended run", "overnight", "overnight run", "long-running", "long run"
- "delegated execution", "while I'm away", "while I'm asleep"
- "kick off and walk away", "babysit this", "do this on your own"
- "keep working while I'm not here"
- webhook-triggered or scheduled-job runs where the user is structurally absent
- semantic equivalents — if the user is communicating that they will not be
  responsive for a substantial period and they want you to make progress, load
  this skill

[`AGENTS.md` carve-out](../../../AGENTS.md): the interactive "don't start
substantive work the user didn't ask for" rule **does not apply** during an
unattended run. The user has delegated execution; their absence is the
authorization to act.

---

## First action: scope-envelope alignment (REQUIRED before any work)

Before any non-Read tool call, write a one-page scope-envelope document and
post it to the user. **Wait briefly for their reply** (a minute or two for
acknowledgement; if no reply, proceed with the envelope as written — the user
is unreachable by definition under this skill, and the envelope is the
fallback contract).

The scope envelope aligns intent. It prevents two failure modes from last
night's overnight run: (a) doing less than the user wanted ("the run last
night finished way too quickly"), or (b) doing more / different than the user
wanted (drifting into unauthorized scope).

**Scope-envelope contents** (template at
[`resources/template-scope-envelope.md`](resources/template-scope-envelope.md)):

1. **What I plan to do.** 3-7 bulleted deliverables, each ≤ one sentence.
2. **What I plan to NOT do.** 2-4 bulleted boundaries — adjacent work I will
   *not* touch unless you explicitly ask.
3. **Scale estimate.** Number of PRs (target a meaningful chunk of the 30-PR
   cap), number of subagents, expected run duration.
4. **First decision points.** 2-4 questions I will hit early. For each: my
   current best answer + the alternative + the rewind point if you disagree.
5. **What I'll surface in the morning summary.** Explicit list of items that
   will land as morning-review items (not auto-decided).
6. **Stop conditions.** What would cause me to stop the run early
   (context-budget exhaustion, blocked on auth, hard-failed subagents, etc.)
   vs continue.

The user reads the envelope and either:
- Confirms (or doesn't reply — taken as implicit confirmation after a short
  wait). Run begins.
- Adjusts ("do more X, less Y"; "skip first decision; I'll handle it"). You
  revise the envelope and proceed.
- Cancels. Run does not start.

The envelope is committed as the first file of the run, on the first stacked
branch, so the morning user can rewind to "before the run began" by reverting
the whole chain or to "after the envelope, before the work" by reverting from
the second PR onward.

---

## Working mode (three rules)

1. **Prefer reversible action over freeze.** The user would rather you get a
   lot done with reversible decisions than do nothing waiting for input.
2. **When in genuine doubt between two strong options, pick one and flag the
   alternative as a morning-review item.** Do not freeze on legitimate
   user-input territory — write the decision brief, run the review rounds,
   pick a side, document the rewind path, and proceed.
3. **Every decision is rewindable.** Brief + commit + branch SHA make any
   choice reversible. Document the rewind point in both the brief and the PR
   description.

---

## Decision-brief protocol (two rounds, ≥3 real reviewers each round)

When you reach a point that would normally trigger an `AskUserQuestion` call,
instead write a decision brief at
`architectures/v3/decisions/auto-NNN-<slug>.md` (or analog path for the
project) per
[`resources/template-decision-brief.md`](resources/template-decision-brief.md).

### Round 1 — initial brief + first adversarial wave

1. **Write Round-1 brief.** Sections: Question, Alternatives (≥3 named
   options), Decision (your best call), Reasoning, Downstream impact,
   Round-1 if-user-overrides rewind point.
2. **Dispatch ≥3 real adversarial reviewer subagents** per
   [`AGENTS.md` `AGENTS-MD-d72e1a4f3c`](../../../AGENTS.md#adversarial-review-must-be-real-subagents).
   Inline-simulated reviewers are forbidden. Choose angles from
   [`resources/adversarial-reviewer-angles.md`](resources/adversarial-reviewer-angles.md).
3. **Commit the Round-1 brief** on its own commit on its own stacked branch.

### Round 2 — revise the brief + second adversarial wave

4. **Incorporate Round-1 findings.** Revise the brief — if reviewers
   converged on a different option, switch. If they raised amendments, fold
   them in. Mark Round-1 as `superseded` (preserve text for traceability).
   Add a Round-2 section: revised decision, reasoning, downstream impact.
5. **Dispatch ≥3 MORE real adversarial reviewer subagents** on the revised
   brief. Use different angles where possible (e.g., if Round 1 was hawk +
   skeptic + purist, Round 2 might be regulator + cell-defender + naive-
   newcomer). Round-2 reviewers must read the revised brief cold; do not
   include Round-1 transcript in their context.
6. **Final decision after Round 2.** If Round-2 reviewers converged on
   another change, switch again (mark Round 2 superseded, write Round 3 —
   though this should be rare). If Round-2 reviewers `accept as-is`, the
   decision is final.
7. **Commit the Round-2 revision** on the same branch. Proceed.

### Why two rounds?

A single round risks Round-1 reviewers identifying the wrong objections
(they're cold to the brief but warm to the prevailing methodology; their
counter-proposals may not survive a second wave's challenge). Two rounds
gives you adversarial pressure on both the original and the revised
artifact. Stop earlier than Round 2 only when Round-1 reviewers
unanimously `accept as-is` AND their reasoning shows they engaged the
hardest objection (not just the surface ones).

---

## Stacked-PR discipline

Cross-reference: [`stacked-pr-on-feature-branch`](../stacked-pr-on-feature-branch/SKILL.md).

- Each logically-grouped chunk (one decision brief + its implementation, or
  one dispatch wave, or one phase-close) is its own branch off the previous
  tip, with PR base set to that previous branch.
- PRs default to ready-for-review, NOT draft, per AGENTS.md.
- **Cap: 30 PRs per unattended run.** Beyond 30 the review burden becomes
  unmanageable. If you hit 30 with substantial work remaining, end the run
  with a handoff doc and stop — do not push past the cap.
- **Floor (target, not hard): aim for the upper end (20-30 PRs per run).**
  The 2026-05-25 overnight run produced only 10 PRs and "finished way too
  quickly" per the user. Don't stop because a sub-phase closed — start the
  next sub-phase. Use the scope envelope to bound the run; otherwise push.
- Each PR must be reviewable independently. The user reads PR descriptions,
  **not the diff** — see [PR description discipline](#pr-description-discipline).

---

## PR description discipline

The user reviews PR descriptions, not code diffs. Each PR's description is
the only artifact the user reads for that chunk of work. Write accordingly.

**Required sections per PR description:**

1. **Summary** — 2-4 sentences. What changed and why.
2. **Key findings or decisions** — bulleted list, specific. Not "improved X"
   but "found that BF-S's B7 partition-leakage is structural; downgraded the
   ROBUST claim to rate-limited side-channel mitigation."
3. **Rewind point** — the specific commit SHA(s) to revert and what each
   reversal undoes.
4. **Test plan / acceptance criteria** — checkboxed list of what the user
   would verify if they were code-reviewing. Even if you don't expect them to
   run it, this captures *what good looks like*.
5. **Targets `<parent-branch>`** notice when stacked — names the parent PR
   and explains the auto-rebase behavior.

If a PR description is one paragraph of bland summary, the user has nothing
to grasp. Write descriptions that surface findings, not work-done.

---

## Volume guidance (the run should not stop often)

The user explicitly said the run should not stop often. Stop conditions are
limited and each requires a deliberate decision:

**Allowed stop conditions:**

1. Context-budget exhaustion approaching (write summary + retrospective
   before you run out of room).
2. Hard-failed dependency (auth dropped, subagent harness errored, GitHub
   unreachable, etc.). Try the
   [`github-connection-resilience`](../github-connection-resilience/SKILL.md)
   recovery first.
3. Scope envelope completion (the explicit deliverables list is done). Even
   here, prefer extending into adjacent scope (with a brief + review rounds)
   over stopping.
4. 30-PR cap hit.
5. User-message-arrived interrupt.

**NOT allowed stop conditions:**

- A sub-phase closed and the next sub-phase would need user input (write a
  decision brief instead).
- A subagent returned ambiguous results (write a follow-up brief and
  dispatch a clarifying subagent).
- The decision feels like user-judgment territory (write the brief; the
  whole point of this skill is that user-judgment territory gets handled
  via brief + review rounds, not by freezing).
- "I think I'm done" (you're probably not — check the scope envelope and
  the carried-forward work).

When you do stop, the [End-of-run protocol](#end-of-run-protocol) is
non-optional.

---

## Subagent fanout cadence

Cross-reference:
[`parallel-subagent-fanout`](../parallel-subagent-fanout/SKILL.md),
[`subagent-prompting`](../subagent-prompting/SKILL.md).

- Practical parallel limit: ~20-25 subagents per wave. Beyond that, harness
  load + your aggregation budget become risks.
- Brief subagents to **write directly to files** (give them the file path
  and require they write rather than return content). Require ≤100-word
  summary returns. This protects lead-agent context.
- Reviews/adversarial subagents are exempt from the file-write requirement —
  their output is the deliverable, not a file artifact. But keep their
  return budget tight (400-700 words each).

---

## Adversarial-review discipline (real subagents only)

Codified in [`AGENTS.md` `AGENTS-MD-d72e1a4f3c`](../../../AGENTS.md#adversarial-review-must-be-real-subagents).

The lead agent inventing what a reviewer would say is forbidden. Inline
simulation produces objections the lead agent has already mentally defused
and counter-proposals the lead agent has already prepared rebuttals for. It
looks like adversarial pressure but exerts none.

The [`resources/adversarial-reviewer-angles.md`](resources/adversarial-reviewer-angles.md)
file lists ready-to-use reviewer angles with one-sentence descriptions, so
you don't reinvent them per brief.

---

## Context-budget self-management

- Commit + push every checkpoint (cross-reference
  [`always-commit-skill-to-repo`](../always-commit-skill-to-repo/SKILL.md)).
  An ephemeral sandbox can vanish; committed work survives.
- Offload detail to disk early. If a subagent returns a 1500-word sketch,
  it should be in a file, not in your conversation transcript.
- Reduce per-subagent return verbosity as you approach context limits.
  A 100-word summary becomes 50; per-primitive sketches become per-cluster.
- When approaching ~70% context budget: write the morning summary +
  retrospective NOW, then continue if possible. Don't wait until 90%.
- Track in-flight subagents per
  [`in-flight-workflow-tracking`](../in-flight-workflow-tracking/SKILL.md).

---

## Morning-summary artifact (REQUIRED — every run, no exceptions)

Write a top-level `overnight-summary.md` (or `run-summary.md` if the run
isn't overnight) at the repo root, in its own final PR at the top of the
stack. Template at
[`resources/template-overnight-summary.md`](resources/template-overnight-summary.md).

**Required sections:**

1. **TL;DR** — 4-6 bullets. What changed, what's resolved, what's queued,
   what's morning-review territory.
2. **Suggested merge order** — explicit, numbered list of which PRs to merge
   in what sequence. Stack-bottom first by default; call out any PRs that
   are safe to merge independently. The user reads this list and merges in
   order without re-deriving the chain shape.
3. **PRs opened (in stack order)** — table with: PR #, branch, title, base,
   status, per-PR rewind point. The PR descriptions are the primary review
   artifact; this table is the index.
4. **Decision briefs written** — table with one-line summary of each brief
   + its Round-1 / Round-2 status.
5. **Chain status** — current state of any cross-PR work (e.g., "Phase 3.5
   closed; Phase 4 queued"). Include carried-forward state.
6. **Morning-review items** — explicit list of decisions or adjudications
   needing user input. For each: the question, the lead-agent recommendation,
   the rewind path if user disagrees. The 2026-05-25 run had 1 such item;
   the next run may have more or fewer. Zero is a valid state if the run
   genuinely closed everything.
7. **What I deliberately did NOT do** — adjacent work I bounded out (per
   the scope envelope) and any in-scope work I chose to defer with reason.
   Honesty here is critical; hiding deferrals is forbidden.
8. **Rewind points** — table mapping commit SHAs to what each reversal
   undoes (full chain summary).
9. **Session metadata** — branch chain at run end, subagent count, run
   start / end timestamps.

The summary is the user's primary review artifact. Treat it as the
deliverable, not an afterthought.

---

## Handoff document discipline

If a phase closes during the run (e.g., a multi-phase pipeline like
research synthesis hits a phase boundary), update the project's
SESSION-HANDOFF document:

- Write a new `SESSION-HANDOFF-YYYY-MM-DD-phase-N-close.md` at the project's
  conventional handoff location, per
  [`resources/template-handoff-doc.md`](resources/template-handoff-doc.md).
- Mark the prior handoff `[SUPERSEDED]` with a banner pointing at the new
  file.
- Fix stale-path references per
  [`AGENTS.md` § Internal document references rule 3](../../../AGENTS.md#internal-document-references).

The handoff is the durable cross-session state; the morning summary is the
single-session review artifact. Both are required when a phase closes
during the run.

---

## End-of-run protocol

When the run stops (any of the allowed stop conditions above):

1. **Drain all in-flight subagents.** If subagents are still running, wait
   for them or write a "drained mid-flight" annotation. Per
   [`in-flight-workflow-tracking`](../in-flight-workflow-tracking/SKILL.md),
   nothing leaves in-flight without a recorded outcome.
2. **Commit + push everything.** Verify `git status` is clean.
3. **Write the morning summary** if not already written. Push as its own PR
   at the top of the stack.
4. **Update the handoff document** if a phase closed during the run.
5. **Auto-invoke [`self-retrospective`](../self-retrospective/SKILL.md).**
   The retro captures durable lessons from the run before they're lost to
   context truncation. Even if you think the run was uneventful, the retro
   surfaces subtle patterns. Run it before the final stop.
6. **Subscribe to all PRs opened** (per
   [`in-flight-workflow-tracking`](../in-flight-workflow-tracking/SKILL.md)).
   Even if the run is ending, the user may merge PRs which trigger webhook
   events that the next session inherits.
7. **End the run with a one-paragraph status message** to the user. Names
   the morning-summary PR, the suggested merge order, and any morning-review
   items.

The end-of-run protocol is non-optional. A run that ends without a
retrospective + summary leaves durable lessons un-captured and morning
review under-served.

---

## Anti-patterns

- **Stopping early because a sub-phase closed.** Start the next sub-phase
  with a decision brief if needed. The run should not stop often.
- **Inline-simulating adversarial reviewers** to save a few subagent
  dispatches. AGENTS.md forbids this. The whole point is that real
  subagents catch the lead agent's blind spots.
- **One round of adversarial review when the brief is load-bearing.**
  Two rounds is the minimum for substantive decisions; one round risks
  missing the second-order objections.
- **Writing thin PR descriptions.** The user reviews PR descriptions, not
  code. A thin description means the user can't grasp what changed.
- **Stacking past 30 PRs.** Review burden becomes unmanageable. Bound the
  run; write the handoff; stop.
- **Skipping the morning summary.** Required, always.
- **Skipping the self-retrospective at end of run.** The retro captures
  durable lessons; skipping it is a slow-burn cost over many runs.
- **Pushing more work to a merged branch.** Each chunk gets a new branch
  off the previous tip.
- **Burying deferrals in the summary.** "What I deliberately did NOT do"
  must be explicit; hiding deferrals creates morning confusion.
- **Hitting context-budget exhaustion without preparation.** Write the
  summary + retro at ~70% budget, not 90%.

---

## Files this skill creates / modifies

This skill is procedural — its SKILL.md and resources documents the
pattern but doesn't install any artifacts into consumer repos. The skill
itself uses:

- `SKILL.md` — this file.
- `resources/template-decision-brief.md`
- `resources/template-overnight-summary.md`
- `resources/template-handoff-doc.md`
- `resources/template-scope-envelope.md`
- `resources/adversarial-reviewer-angles.md`

A run that invokes this skill creates (in the consumer repo):
- One scope envelope (first commit of the run)
- N decision briefs (`decisions/auto-NNN-*.md`)
- N stacked PRs (≤30, target 20-30)
- One morning summary (`overnight-summary.md` or analog) at repo root
- Optional handoff document if a phase closes
- A self-retrospective dir at end of run

---

## See also

- [`stacked-pr-on-feature-branch`](../stacked-pr-on-feature-branch/SKILL.md)
- [`always-commit-skill-to-repo`](../always-commit-skill-to-repo/SKILL.md)
- [`in-flight-workflow-tracking`](../in-flight-workflow-tracking/SKILL.md)
- [`parallel-subagent-fanout`](../parallel-subagent-fanout/SKILL.md)
- [`subagent-prompting`](../subagent-prompting/SKILL.md)
- [`self-retrospective`](../self-retrospective/SKILL.md)
- [`github-connection-resilience`](../github-connection-resilience/SKILL.md)
- [`AGENTS.md` `AGENTS-MD-d72e1a4f3c`](../../../AGENTS.md#adversarial-review-must-be-real-subagents) — the real-subagent adversarial-review rule
