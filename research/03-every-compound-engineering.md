# Every.to Compound Engineering — Research Report (Revised)

**Sources covered:**
- https://every.to/guides/compound-engineering — **ACCESSED** via local copy at `/home/user/software-factory/every.to__guides__compound-engineering.html` (the canonical guide; unsigned author but the same voice as Kieran Klaassen)
- https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents — **ACCESSED** via local copy at `/home/user/software-factory/every.to__chain-of-thought__compound-engineering-how-every-codes-with-agents.html` (Dan Shipper and Kieran Klaassen, December 11, 2025; updated April 6, 2026)
- https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it — **ACCESSED** via local copy at `/home/user/software-factory/every.to__source-code__my-ai-had-already-fixed-the-code-before-i-saw-it.html` (Kieran Klaassen, August 18, 2025; updated April 23, 2026; **paywalled after ~10 minute-investment section**)
- https://every.to/p/the-agent-that-saved-my-brain — **ACCESSED** via local copy at `/home/user/software-factory/every.to__p__the-agent-that-saved-my-brain.html` (Austin Tedesco, March 23, 2026; updated May 4, 2026)
- https://github.com/EveryInc/compound-engineering-plugin — full plugin docs (`README.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/skills/*.md` for all major skills)
- https://github.com/EveryInc/compound-knowledge-plugin — full plugin docs (`README.md`, `AGENTS.md`, `kw-compound` and reviewer/researcher agent docs)

**Date:** 2026-05-10

---

## Revision notes

This is a substantive revision of the original report, which had been reconstructed entirely from the GitHub plugin READMEs because the every.to URLs returned 403. Now that the four primary every.to articles are available locally, the following changes were made:

**Verified verbatim and quote-corrected.** Roughly a dozen paraphrased lines previously attributed to the plugin README have been swapped for verbatim quotes from the canonical articles where the articles confirm them. Quote attributions are now author/article-level, not plugin-file-level.

**New material added:**
- **Origin story.** Kieran Klaassen's "Before I opened my laptop, the code had reviewed itself" moment — Claude Code citing PRs #234, #219, #241 in its self-review comments — is now in the executive summary as the founding anecdote.
- **Self-improving prompts resolved (open question #5).** The "My AI Had Already Fixed" article describes Claude iterating on its *own* frustration-detection prompt until a test passes, then updating the prompt based on chain-of-thought analysis of failed runs. The "Agent That Saved My Brain" article describes Austin Tedesco telling Montaigne "to update its own instructions to rely on this as the source of truth." Both are explicit agent-rewriting-agent-instructions patterns.
- **Team-scale and productivity claims (open question #6).** Five products, "primarily single-person engineering teams," "thousands of people every day," and the explicit claim that "a single developer can do the work of five developers a few years ago."
- **Five-stage adoption ladder** (Stage 0 manual → Stage 5 parallel cloud).
- **Two-tier time-allocation rule.** The 80/20 (planning+review vs work+compound *per feature*) is paired with a separate 50/50 rule (feature work vs system-improvement work *across all engineering time*).
- **Eight named "beliefs to let go"** and seven "beliefs to adopt" / core principles.
- **Three questions to ask any AI output** — a poor-person's substitute for multi-agent review.
- **"First attempt 95% garbage, second attempt 50%"** — Klaassen's concrete iteration claim.
- **Tool-agnosticism** explicitly stated: Claude Code primary; Factory's Droid and OpenAI's Codex CLI also in use.
- **Lineage of the Compound Knowledge plugin** — Tedesco's article confirms it was "inspired by Kieran Klaassen's compound engineering system."

**Corrections:**
- The original report described the loop as five-step (brainstorm → plan → work → review → compound). The canonical every.to articles describe it as **four-step (Plan → Work → Review/Assess → Compound)**, with brainstorming subsumed into Plan. The plugin's five-step loop is an elaboration, not the canonical statement.
- Agent counts in the guide ("26 specialized agents, 23 workflow commands, 13 skills") differ from the plugin README's "50+ agents, 37+ skills." Likely a versioning gap; both numbers are now cited with provenance.
- The "Three review-doc reviewer parallelism" and similar plugin-internal language was tightened to match what the articles actually claim, which is less granular.

**Newly-discovered external references:**
- Three sibling every.to articles named in "Chain of Thought": "Stop Coding and Start Planning," "Teach Your AI to Think Like a Senior Engineer," and "How Every Is Harnessing the World-changing Shift of Opus 4.5" — all by Klaassen or co-bylined.
- W. Edwards Deming's PDCA cycle, surfaced in a reader comment and acknowledged in spirit by the loop's shape.
- Factory's Droid (factory.strongdm.ai) and OpenAI's Codex CLI as alternative harnesses Every's team uses.

**Still open:** the paywalled portion of "My AI Had Already Fixed the Code Before I Saw It" (cuts off at the frustration-detector example) likely contains additional concrete examples; the open question about its full contents persists.

---

## Executive summary

Compound engineering, as practiced by Every Inc., is the thesis that **"each unit of engineering work should make subsequent units easier—not harder"** (Every.to guide). It is an explicit inversion of the conventional curve: where "most codebases get harder to work with over time because each feature you add injects more complexity," compound engineering aims for the opposite — *"features adding complexity and fragility, they teach the system new capabilities. Bug fixes eliminate entire categories of future bugs."*

The founding anecdote is Kieran Klaassen's: *"Before I opened my laptop, the code had reviewed itself."* He found Claude Code had already left strong PR comments citing prior reviews — *"Changed variable naming to match pattern from PR #234, removed excessive test coverage per feedback on PR #219, added error handling similar to approved approach in PR #241."* The mental shift this prompted: *"It felt like cheating, but it wasn't—it was compounding. Every time we fix something, the system learns. Every time we review something, the system learns. Every time we fail in an avoidable way, the system learns."*

The canonical loop, as stated by Klaassen and Dan Shipper in the *Chain of Thought* article, is **four-step**:

> "Plan → Work → Review → Compound → Repeat. The first three steps—plan, work, and review—should be familiar to any developer. It's the fourth step that separates compound engineering from other engineering. This is where the gains accumulate. Skip it, and you've done traditional engineering with AI assistance." (Every.to guide)

Two time-allocation rules sit on top of this loop:

1. **Per cycle:** *"The plan and review steps should comprise 80 percent of an engineer's time, and work and compound the other 20 percent."* (Every.to guide)
2. **Across all engineering work:** *"50 percent of engineering time to building features, and 50 percent to improving the system... An hour spent creating a review agent saves 10 hours of review over the next year."* (Every.to guide)

What scales the methodology: Every runs *"five products—Cora, Monologue, Sparkle, Spiral, and our website Every.to—with primarily single-person engineering teams"* (Every.to guide), used by *"thousands of people every day for important work—they're not just nice demos"* (Shipper/Klaassen). The headline productivity claim: *"a single developer can do the work of five developers a few years ago, based on our experience at Every."*

What actually compounds is a small, deliberately-bounded set of durable artifacts:

- `CLAUDE.md` / `AGENTS.md` — *"the most important file that the agent reads every session. Put your preferences, patterns, and project context here. When something goes wrong, add a note so the agent learns."* (guide)
- `docs/solutions/` — *"builds your institutional knowledge because each solved problem becomes searchable documentation. Future sessions will find past solutions automatically."* (guide)
- `docs/brainstorms/` and `docs/plans/` — pre-execution artifacts that survive into future cycles.
- `STRATEGY.md` and `docs/pulse-reports/` (plugin-internal) — bracket the loop with product reality.

The plugin embodies the methodology, with the guide citing *"26 specialized agents, 23 workflow commands, 13 skills"* (an earlier count) and the current GitHub README citing 50+ agents and 37+ skills — the plugin is a live work-in-progress. It is *"tool-agnostic—some members of our team also use startup Factory's Droid and OpenAI's Codex CLI."*

---

## The compounding mechanism

What compounds: **durable artifacts on disk that future agents are wired to read.** *"These learnings... get written down as prompts that live inside of your codebase or in plugins like ours, every developer on your team gets them for free. Everyone becomes more productive: A new hire who's never been in the codebase before is as well-armed to avoid common mistakes as someone who's been on the team for a long time."* (Shipper/Klaassen)

The mechanism, in Klaassen's framing: *"AI engineering makes you faster today. Compounding engineering makes you faster tomorrow, and each day after."*

Six mechanisms make iteration `n+1` cheaper than iteration `n`:

1. **Reusable upstream anchors.** `CLAUDE.md` and `AGENTS.md` are read every session. `STRATEGY.md` (plugin-internal) is read by every downstream skill — a single edit propagates across all future cycles.

2. **Self-improving prompts.** This is the most striking mechanism, and it's described concretely in two articles. In "My AI Had Already Fixed," Klaassen describes building a frustration-detector: he runs the detection prompt ten times, finds it works only four out of ten, then *"Claude analyzes why it failed the other six times. It studies the chain of thought... and discovers a pattern: It's missing hedged language a user might use, like, 'Hmm, not quite,' which actually signals frustration when paired with repeated requests. Claude then updates the original frustration-detection prompt to specifically look for this polite-but-frustrated language. On the next iteration, it's able to identify a frustrated user nine times out of 10."* The agent rewrites its own prompt based on its own failure analysis. In the Montaigne article, Tedesco describes the same pattern at a higher level: *"I pointed it to where the real numbers live, and then told it to update its own instructions to rely on this as the source of truth. The fix took two minutes, and Montaigne has gotten MRR right ever since."*

3. **Stable IDs across artifacts** (plugin-level). R-IDs, A-IDs, F-IDs, AE-IDs flow from brainstorm into plan; U-IDs flow into commits and test scenarios. Cross-references don't go stale.

4. **Knowledge store auto-consulted at planning time.** *"docs/solutions/ builds your institutional knowledge because each solved problem becomes searchable documentation. Future sessions will find past solutions automatically."* (guide) The plugin's `ce-learnings-researcher` runs in Phase 1 of `/ce-plan`.

5. **Pattern-promotion during review.** Multi-agent review *"combined into a single, prioritized list"* (guide); plugin-level cross-persona agreement raises severity.

6. **Periodic hygiene.** *"Without active maintenance, the knowledge store loses trustworthiness... the compound effect inverts: bad learnings make work harder, not easier."* (plugin's `ce-compound-refresh`)

A subtler compounding mechanism: **automated extraction of human review feedback.** *"After we do a code review, for example, we'll ask the agent to look at the comments, summarize them, and store them for later. The latest models are smart enough to do all of this with very little extra instruction—and they're also smart enough to actually use it the next time."* (Shipper/Klaassen)

---

## Agents and roles

The Every.to guide names a slightly leaner set than the plugin README; the canonical roles described in the article are:

### Review agents (the public count: 14)

The guide enumerates *"14 specialized agents that analyze code in parallel. Each agent focuses on a specific domain and returns prioritized findings"*:

- **Security.** `security-sentinel` — *"Scans for top 10 vulnerabilities as defined by OWASP, injection attacks, authentication flaws, and authorization bypasses."*
- **Performance.** `performance-oracle` — *"Detects N+1 queries, missing indexes, caching opportunities, and algorithmic bottlenecks."*
- **Architecture.** `architecture-strategist`, `pattern-recognition-specialist`.
- **Data.** `data-integrity-guardian`, `data-migration-expert`.
- **Quality.** `code-simplicity-reviewer`.
- **Stack-specific:** `kieran-rails-reviewer`, `kieran-python-reviewer`, `kieran-typescript-reviewer`, `dhh-rails-reviewer`.
- **Deployment.** `deployment-verification-agent` — *"Generates pre-deploy checklists, post-deploy verification steps, and rollback plans."*
- **Frontend.** `julik-frontend-races-reviewer` — *"Detects race conditions in JavaScript and Stimulus controllers."*
- **Agent-native.** `agent-native-reviewer` — *"Ensures features are accessible to agents, not just humans."*

The current plugin (50+ agents) extends this with `ce-adversarial-reviewer`, `ce-reliability-reviewer`, `ce-api-contract-reviewer`, `ce-schema-drift-detector`, `ce-correctness-reviewer`, `ce-testing-reviewer`, `ce-maintainability-reviewer`, `ce-project-standards-reviewer`, doc-side reviewers (`ce-coherence-reviewer`, `ce-feasibility-reviewer`, `ce-adversarial-document-reviewer`, etc.), and stack-extensions like `ce-swift-ios-reviewer`.

### Researchers (plan-time)

- `repo-research-analyst` — codebase patterns.
- `framework-docs-researcher` — documentation.
- `best-practices-researcher` — industry standards.
- `spec-flow-analyzer` — user flows and edge cases.
- (Plugin extensions): `learnings-researcher`, `git-history-analyzer`, `issue-intelligence-analyst`, `session-historian`, `slack-researcher`, `web-researcher`.

### Design

- `design-iterator` — *"Takes a screenshot of the current design, analyzes what's not working, makes improvements, and repeats. Each pass refines the design further."*
- `figma-design-sync` — *"Pulls the design from Figma, compares to what's built, identifies differences, and fixes them automatically."*
- `design-implementation-reviewer` — *"Checks that the implementations match the Figma specifications. It catches visual bugs before they reach users."*

### Compound Knowledge plugin (knowledge-work twin)

Created by Austin Tedesco for non-engineering work; *"inspired by Kieran Klaassen's compound engineering system"* (Tedesco). Six skills (`/kw:brainstorm`, `/kw:plan`, `/kw:confidence`, `/kw:review`, `/kw:work`, `/kw:compound`), three research agents (`knowledge-base-researcher`, `past-work-researcher`, `stale-knowledge-checker`), two review agents (`strategic-alignment-reviewer`, `data-accuracy-reviewer`). The CK agents return text only; only the orchestrating skill writes files.

---

## Workflows and cycles

The canonical four-step loop from the guide:

```
Plan → Work → Review → Compound → Repeat
```

The plugin internally expands this into a longer chain (strategy → ideate → brainstorm → plan → work → review → compound → product-pulse), but the article-level statement is four steps. Klaassen and Shipper:

> "The loop works the same whether you are fixing a bug in five minutes or building a feature over several days. You just spend more or less time on each step." (Every.to guide)

### 1. Plan

> "Planning transforms an idea into a blueprint, and better plans produce better results."

Five sub-actions: *"Understand the requirement... Research the codebase... Research externally... Design the solution... Validate the plan."*

> "Plans are the new code. The plan document is now the most important thing you produce. Instead of coding first and documenting later, as you might have traditionally, start with a plan. This becomes the source of truth your agents use to generate, test, and validate code. Having a plan helps capture decisions before they become bugs. Fixing ideas on paper is cheaper than fixing code later." (guide)

The plugin's `/workflows:plan` spawns *"three parallel research agents: repo-research-analyst (codebase patterns), framework-docs-researcher (documentation), and best-practices-researcher (industry standards). Then the spec-flow-analyzer agent analyzes user flows and edge cases. Results are merged into a structured plan with affected files and implementation steps."* With `ultrathink` enabled, `/deepen-plan` runs after and *"spawns over 40 parallel research agents."*

### 2. Work

> "Execution follows the plan. The agent implements while the developer monitors... If you trust the plan, there's no need to watch every line of code." (guide)

Critical capability: model context protocols. *"One of the most important tricks for this step is using a model context protocol like Playwright or XcodeBuildMCP. These are tools that allow the agent to use your web app or simulate use on a phone as it's being built, as if it were one of your users. So it will write some code, walk through the app and notice issues, and then modify the code and repeat until it's done."* (Shipper/Klaassen)

### 3. Review (Assess)

> "This step catches issues before they ship. More importantly, it captures learnings for the next cycle, which becomes the basis for compound engineering." (guide)

Findings are tiered P1 / P2 / P3 (critical / important / minor). The plugin's automated path is `/resolve_pr_parallel`: *"P1 issues are fixed first, then P2s. Each fix runs in isolation so they don't step on each other, but you still manually review the generated fixes at the end."* The human-filtered alternative is `/triage`, which *"presents each finding one by one for human decision: approve (add to to-do list), skip (delete), or customize."*

The conceptual core, from Shipper/Klaassen: *"Our compound engineering plugin... reviews code in parallel with 12 subagents that each check it from a different perspective. One looks for common security issues, another checks for common performance issues, another looks at it to see if anything was overbuilt, so software isn't bloated or too complex. All of these different perspectives are synthesized and presented so that the developer can decide what needs to be fixed and what can be ignored."*

### 4. Compound (the money step)

> "This is the money step. We take what we learned in any of the previous steps—bugs, potential performance issues, new ways of solving particular problems—and record them so that the agent can use them next time. This is what makes compounding happen in compound engineering." (Shipper/Klaassen)

Four sub-actions: *"Capture the solution... Make it findable [YAML frontmatter]... Update the system [add patterns into CLAUDE.md]... Verify the learning [Would the system catch this automatically next time?]."* (guide)

The plugin's `/workflows:compound` *"spawns six parallel subagents: context analyzer (understands the problem), solution extractor (captures what worked), related docs finder (links to existing knowledge), prevention strategist (documents how to avoid recurrence), category classifier (tags for discovery), and documentation writer (formats the final doc)."* (guide)

### The end-to-end one-shot

`/lfg` (let's f-ing go) chains the whole pipeline: *"plan → deepen-plan → work → review → resolve findings → browser tests → feature video → compound. It pauses for plan approval, then runs autonomously, and spawns more than 50 agents across all stages. With one command, you have a complete feature."* (guide)

---

## Specification / brief methodology

Three observations.

**1. Plans are the new code.** This is the single sharpest claim in the methodology:

> "Plans are the new code. The plan document is now the most important thing you produce... This becomes the source of truth your agents use to generate, test, and validate code." (guide)

**2. Plans are scope-tiered and capture-bound.** The brainstorm command *"helps you brainstorm answers about what to build and plan answers for how to build them. Use this when requirements are fuzzy."* (guide) Outputs include objective, proposed architecture, *"specific ideas for how the code might be written, a list of sources for its research, and success criteria"* (Shipper/Klaassen). At the plugin level the brief carries stable IDs (R/A/F/AE/U) so cross-references don't go stale across edits.

**3. Headless / autonomous variants exist for higher-level orchestration.** The plugin's `mode:headless` lets a skill be composed into a larger orchestrator while still emitting a one-line human-readable summary.

The methodological commitment: *"start with a plan. This becomes the source of truth your agents use to generate, test, and validate code. Having a plan helps capture decisions before they become bugs. Fixing ideas on paper is cheaper than fixing code later."* (guide)

The honest counter-claim: *"As models get better, especially with small projects, you have to plan less and less—the agent just gets what you want, or maybe does something surprising but good. With complex production projects, though, a good plan is an essential part of building high-quality software that works as you expect."* (Shipper/Klaassen)

---

## Review and feedback patterns

Five patterns deserve attention.

**1. Parallel multi-persona review with synthesis.** *"Spawns more than 14 specialized agents in parallel that run simultaneously... Everything gets combined into a single, prioritized list."* (guide) The 12-subagent count in the *Chain of Thought* article is a slightly older snapshot of the same pattern.

**2. P1/P2/P3 severity, with explicit autofix routing.** The guide gives the canonical example block:

```
P1 - CRITICAL (must fix):
[ ] SQL injection vulnerability in search query (security-sentinel)
[ ] Missing transaction around user creation (data-integrity-guardian)
P2 - IMPORTANT (should fix):
[ ] N+1 query in comments loading (performance-oracle)
[ ] Controller doing business logic (kieran-rails-reviewer)
P3 - MINOR (nice to fix):
[ ] Unused variable (code-simplicity-reviewer)
```

The plugin layers a second orthogonal axis (`safe_auto` / `gated_auto` / `manual` / `advisory`) for *who acts next* — see the plugin's `ce-code-review` doc.

**3. Trust the system, not the line.** *"AI assistance doesn't scale if every line requires human review. You need to trust the AI. Trust doesn't mean blind faith. It means setting up guardrails such as tests, automatic review, and monitoring that flag issues so you don't have to watch every step. When you feel as if you can't trust the output, don't compensate by switching to manually reviewing the code. Add a system that makes that step trustworthy, such as creating a review agent that flags issues."* (guide)

**4. Human review focus shifts from implementation to intent.** *"When AI review agents have already analyzed a PR, human reviewers focus on intent, not implementation. Ask yourself: Does this match what we agreed to build? Does the approach make sense? Are there business logic issues? Don't bother checking for syntax errors, security vulnerabilities, performance issues, or style—that's what the review agents already did."* (guide)

**5. Three questions to ask any AI output.** Even without a multi-agent harness, the guide offers a portable substitute:

> "'What was the hardest decision you made here?' This forces the AI to reveal where the tricky parts are and where it had to make judgment calls.
> 'What alternatives did you reject, and why?' This shows you the options it considered and helps catch if it made a bad choice.
> 'What are you least confident about?' This gets the AI to admit where it might be wrong. LLMs know where their weaknesses are, but you have to ask."

The plugin adds round-to-round suppression (fingerprint matching prevents the same finding from re-surfacing), adversarial peer reviewers as named voices, and a Residual Work Gate that forbids silent ship-with-findings.

---

## Knowledge / memory architecture

The architecture has five components.

**1. Flat-file storage.** *"docs/solutions/ builds your institutional knowledge because each solved problem becomes searchable documentation. Future sessions will find past solutions automatically."* (guide) Plain markdown, git-tracked, greppable. The Compound Knowledge plugin's README states: *"The knowledge files are plain markdown, git-tracked, and greppable."*

**2. YAML frontmatter for retrieval.** *"Add YAML frontmatter to make sure it is tagged with the right metadata, tags, and categories for retrieval."* (guide) CE includes `module`, `tags`, `problem_type`, `confidence`, `created`, `source`, `last_updated`.

**3. CLAUDE.md / AGENTS.md as the read-every-session memory.** *"CLAUDE.md is the most important file that the agent reads every session. Put your preferences, patterns, and project context here. When something goes wrong, add a note so the agent learns."* (guide)

**4. Self-modifying memory.** The two clearest descriptions of agents updating instructions are (a) Klaassen's frustration-detector example, where Claude rewrites its own prompt based on chain-of-thought analysis of failed runs, and (b) Tedesco's MRR correction: *"I pointed it to where the real numbers live, and then told it to update its own instructions to rely on this as the source of truth."*

**5. Anti-duplication and discoverability** (plugin-level). The plugin's compound skill checks every run whether `AGENTS.md` / `CLAUDE.md` surfaces `docs/solutions/`, and proposes the minimal addition if not. *"Knowledge only compounds value when it's findable."* (plugin's `ce-compound`)

The Montaigne case study extends this idea outside engineering. Tedesco described layering: *"It has access to everything I use for growth work, including Stripe, PostHog, Slack, Notion, Figma, the full Every product suite, email, and calendar. It also has knowledge layers built on context about the business and a bench of skills for repeat workflows."* Montaigne *"has more than 80 skills that it can apply to the data it can access."*

---

## Human leverage techniques

The guide and articles encode several techniques for a human steering many agents.

**1. The 80/20 rule per cycle, and the 50/50 rule across all engineering time.** From the guide:

> "Previously, I suggested an 80/20 rule for building features: 80 percent of time planning and review, 20 percent on working and compounding. When you look at your broader responsibilities as a developer, you should allocate 50 percent of engineering time to building features, and 50 percent to improving the system—in other words, any work that helps build institutional knowledge rather than shipping something specific... In traditional engineering, teams put 90 percent of their time into features and 10 percent into everything else. Work that isn't a feature feels like a distraction... But that 'everything else' is what makes future features easier."

**2. Agent-native environment parity.** *"If a developer can see or do something, the agent should be allowed to see or do it too. Running tests, checking production logs, debugging with screenshots, creating pull requests. Anything that you don't let the agent handle, you have to do yourself manually. The goal should be full environmental parity between human and AI developers."* (guide)

**3. Parallelization as the new bottleneck.** *"You used to be the bottleneck because human attention only allows one task at a time. The new bottleneck is compute—how many agents you can run at once."* (guide)

**4. Five-stage adoption ladder.** The guide names five stages and explicitly warns against skipping: *"Skipping stages doesn't work because you will feel uncomfortable and distrustful of the tools. Each rung builds the mental models and habits required for the next."*

- **Stage 0:** Manual development (no AI).
- **Stage 1:** Chat-based assistance (ChatGPT / Claude as a smart reference).
- **Stage 2:** Agentic tools with line-by-line review (Claude Code, Cursor Composer). *"Most developers plateau here and don't get to enjoy the upside of handing more over to AI."*
- **Stage 3:** Plan-first, PR-only review. *"This is the stage where everything changes... Compound engineering begins here."*
- **Stage 4:** Idea to PR (single machine).
- **Stage 5:** Parallel cloud execution. *"You kick off three features, three agents work independently, and you review PRs as they finish... No longer an individual contributor are you. You're commanding a fleet."*

**5. Skip permissions deliberately.** *"With skip permissions, you can maintain a flow state because you are not being interrupted by requests for permission... This will unlock five to 10 times faster iteration."* (guide) The `--dangerously-skip-permissions` flag is *"intentionally scary to make you think before using it"*; safety comes from git, tests, worktrees, and final PR review.

**6. Worktree isolation.** *"Use git worktrees for risky work. Experiments happen in an isolated directory."* (guide) Where parallel agents share a tree, the plugin bars subagents from staging or committing.

**7. Extract taste into the system, not into review.** *"Every codebase reflects the taste of the developers who built it... That taste usually isn't documented anywhere. It lives in senior engineers' heads and is transferred through code review. This neither scales nor lets others on the team learn. The solution is to extract and document these choices."* (guide)

**8. Async-by-default team communication.** *"Compound engineering works well asynchronously. Plans can be created, reviewed, and approved without scheduling a meeting. Instead of telling your colleague, 'Let's meet to discuss the approach,' try, 'I've created a plan document—please comment by end of day.'"* (guide)

**9. PR ownership stays with the initiator.** *"The person who initiated the work owns the PR, regardless of who (or what) wrote the code. You're responsible for the quality of the plan, reviewing the work, fixing any issues, and the impact after merge."* (guide)

**10. Auto-invoke triggers** ("that worked", "it's fixed") and **plan-tier ceremony scaling** (Lightweight / Standard / Deep) — both plugin-level. The human chooses where the work warrants the full pipeline.

---

## Pitfalls and lessons learned

**Eight beliefs to let go.** Listed verbatim from the guide:

1. *"'The code must be written by hand.' The actual requirement for you to do your job well as a software engineer is simply to write good code... Who types—a human or an agent—doesn't matter."*
2. *"'Every line must be manually reviewed.'... If you don't trust the results, fix the system, instead of compensating by doing everything yourself."*
3. *"'Solutions must originate from the engineer.'... the engineer's job becomes to add taste—knowing which solution fits this codebase, this team, and this context."*
4. *"'Code is the primary artifact.' A system that produces code is more valuable than any individual piece of code."*
5. *"'Writing code is the core job function.' A developer's job is ship value... Effective compound engineers write less code than before and ship more."*
6. *"'First attempts should be good.' In our experience, first attempts have a 95 percent garbage rate. Second attempts are still 50 percent. This isn't failure—it's the process. So make it your goal to get it right the first time. Focus on iterating fast enough that your third attempt lands in less time than attempt one."*
7. *"'Code is self-expression.'... Letting go of code as self-expression is liberating. No attachment means you take feedback better, refactor without flinching, and skip the arguments about whether the code is good enough."*
8. *"'More typing equals more learning.'... The developer who reviews 10 AI implementations understands more patterns than the one who hand-typed two."*

**Transition challenges** the guide names explicitly:

- *"Less typing feels like less work. It isn't. Directing an agent requires more thinking than implementation because you are spending less time on keystrokes and more time thinking about important decisions."*
- *"Letting go feels risky. Autonomous execution... triggers anxiety in many developers. This fades once they recognize they're not ceding control. Instead, they're encoding it into constraints, conventions, and review processes that scale better than manual oversight."*
- *"Who built this? Features shipping without directly writing the code can feel like cheating. But planning, reviewing, and ensuring quality standards is the work."*

**Building-vs-doing seduction.** Tedesco names a failure mode the engineering articles do not: *"Working on the system is seductive because it feels like progress, but you can end up in a frustrating loop while ignoring the real work at hand... I could make that landing page, or I could perfect the skill inside of Montaigne that generates landing pages for me. Sometimes it genuinely is better to spend the day making the system better rather than using it. But it's easy to look up five hours later and realize I still don't have anything usable shipped, and I've only improved the system by five percent. I think a lot of people are feeling some version of this right now."* This is the 50/50 rule's failure mode — over-rotation toward system work.

**Plugin-level pitfalls** (carried over from the original report, all still confirmed by the plugin docs):
- Pre-written implementation in plans is brittle (WHAT not HOW).
- Renumbering breaks references (stable IDs).
- Two docs on the same problem inevitably drift apart.
- Stale knowledge inverts compounding (require `/ce-compound-refresh`).
- Findings disappearing into chat is a failure mode (Residual Work Gate).
- Discoverability silently kills compounding.

---

## Notable quotes

1. *"Each unit of engineering work should make subsequent units easier—not harder."* — Every.to guide, opening line.
2. *"Most codebases get harder to work with over time because each feature you add injects more complexity. After 10 years, teams spend more time fighting their system than building on it... Compound engineering flips this on its head. Instead of features adding complexity and fragility, they teach the system new capabilities."* — Every.to guide.
3. *"Before I opened my laptop, the code had reviewed itself."* — Klaassen, "My AI Had Already Fixed the Code Before I Saw It."
4. *"It felt like cheating, but it wasn't—it was compounding. Every time we fix something, the system learns. Every time we review something, the system learns. Every time we fail in an avoidable way, the system learns. That's how we build Cora, Every's AI-enabled email assistant, now: Create systems that create systems, then get out of the way."* — Klaassen.
5. *"AI engineering makes you faster today. Compounding engineering makes you faster tomorrow, and each day after."* — Klaassen.
6. *"Plan → Work → Review → Compound → Repeat. The first three steps—plan, work, and review—should be familiar to any developer. It's the fourth step that separates compound engineering from other engineering. This is where the gains accumulate. Skip it, and you've done traditional engineering with AI assistance."* — Every.to guide.
7. *"The plan and review steps should comprise 80 percent of an engineer's time, and work and compound the other 20 percent."* — Every.to guide.
8. *"An hour spent creating a review agent saves 10 hours of review over the next year."* — Every.to guide.
9. *"This is the money step."* — Shipper/Klaassen, on the Compound step.
10. *"Plans are the new code. The plan document is now the most important thing you produce."* — Every.to guide.
11. *"Today, if your AI is used right, a single developer can do the work of five developers a few years ago, based on our experience at Every."* — Shipper/Klaassen.
12. *"First attempts have a 95 percent garbage rate. Second attempts are still 50 percent. This isn't failure—it's the process."* — Every.to guide.
13. *"Claude then updates the original frustration-detection prompt to specifically look for this polite-but-frustrated language."* — Klaassen, the canonical agent-rewrites-prompt moment.
14. *"I... told it to update its own instructions to rely on this as the source of truth. The fix took two minutes, and Montaigne has gotten MRR right ever since."* — Tedesco.
15. *"If a developer can see or do something, the agent should be allowed to see or do it too."* — Every.to guide.
16. *"You used to be the bottleneck because human attention only allows one task at a time. The new bottleneck is compute—how many agents you can run at once."* — Every.to guide.
17. *"Working on the system is seductive because it feels like progress, but you can end up in a frustrating loop while ignoring the real work at hand."* — Tedesco.

---

## Recommended additional sources

1. **"Stop Coding and Start Planning"** (Kieran Klaassen, November 6, 2025) — *"Spend an hour teaching AI how you think, and it gets smarter with every feature you build."* Cited from the source-code article's related-essays.
2. **"Teach Your AI to Think Like a Senior Engineer"** (cited in the *Chain of Thought* article's reading list).
3. **"How Every Is Harnessing the World-changing Shift of Opus 4.5"** (cited in the *Chain of Thought* article's reading list).
4. **"I Stopped Writing Code. My Productivity Exploded."** (Yash Poojary, June 20, 2025) — third-party confirmation of the methodology.
5. **"How to Use Claude Code for Everyday Tasks—No Programming Required"** (Katie Parrott, October 9, 2025) — non-engineer Every team members using Claude Code; companion to Tedesco's Montaigne piece.
6. **Richard Rumelt, *Good Strategy Bad Strategy*** — explicitly named in the plugin's `ce-strategy` skill as the source of the diagnosis / guiding policy / coherent action interview structure.
7. **Andrej Karpathy on autoresearch / experiment loops** — cited in the plugin as the inspiration for `ce-optimize`.
8. **W. Edwards Deming's PDCA cycle** — surfaced by readers in the *Chain of Thought* comments and structurally identical to Plan-Work-Review-Compound; useful prior-art lineage to acknowledge.
9. **Factory's Droid** (https://factory.strongdm.ai) and **OpenAI's Codex CLI** — named as alternative harnesses Every's team uses; *"compound engineering... is tool-agnostic."*
10. **Compound Knowledge plugin** — Tedesco's knowledge-work twin, *"inspired by Kieran Klaassen's compound engineering system."*

---

## Open questions for synthesis

1. **Spec-driven vs compound: where do they intersect?** Spec-driven AI dev emphasizes forward spec authorship; compound engineering puts equally heavy weight on *retroactive* knowledge capture. The guide's "Plans are the new code" claim aligns the two; the open synthesis question is whether the spec lives upstream (one document) or is split into brainstorm + plan + solution (three documents with different lifecycles).

2. **Four-step vs five-step loop.** The Every.to articles canonicalize Plan → Work → Review → Compound. The plugin internally expands to brainstorm → plan → work → review → compound (+ strategy, + product-pulse). Whether the brainstorm/plan split survives outside Every's specific workflow is an open call for any factory adopting the methodology.

3. **Self-improving prompts vs self-improving agents.** Resolved as a *pattern* by the frustration-detector and MRR examples, but the boundary is interesting: Klaassen describes a *prompt* being rewritten by the agent itself; the plugin's `ce-compound` writes docs that other skills read, which is a different shape. A software factory might want both, with clear rules about which kind of self-modification is allowed where.

4. **Single-author velocity vs team scale.** Partially resolved: Every runs five products with single-person engineering teams, claims 5x per-developer productivity, and uses async-by-default team patterns. The CE plugin README's "I do not accept outside contributions" note remains a constraint at the *plugin-asset* level even as the *methodology* explicitly addresses team collaboration. The factory question is whether the plugin pattern (one author per asset) scales by replicating per-team plugins or by codifying a shared base.

5. **Adversarial peer review as named role vs shared attribute.** The plugin's `ce-adversarial-reviewer` is a named voice; the article-level guide doesn't carry this distinction. Whether to name an adversary or to require adversariality of every reviewer is a design call.

6. **Stable-ID discipline costs.** R/A/F/AE/U-IDs are plugin-level only; the article-level methodology doesn't require them. A factory should decide whether the IDs are essential to compounding or are belt-and-braces for the rich plans the methodology already produces.

7. **Knowledge-store curation cost at scale.** `/ce-compound-refresh` is a deliberate burden. Open: what curation cadence keeps compounding net-positive vs net-negative when the store reaches 100s of files?

8. **The seduction failure mode.** Tedesco names it directly: an engineer can spend a day improving the system by 5% and ship nothing. The 50/50 rule sets the target ratio, but the day-to-day signal for "am I in the wrong mode" is not yet codified.

9. **Strategy and pulse-report as the only persistent non-versioned-by-code state.** Plugin-level; the article-level guide doesn't yet name these as canonical. Whether the factory pattern needs more or less PM-style memory is an open question.

10. **Failure recovery vs compounding.** Crash recovery (per-experiment `result.yaml` markers in `/ce-optimize`, resume-on-restart) is a different memory tier than the knowledge store. A robust factory may need three tiers: immediate (recovery), local-cycle (plan + brainstorm), durable-compounding (solutions + strategy).

11. **The paywall.** The full text of "My AI Had Already Fixed the Code Before I Saw It" is paywalled past the frustration-detector example. The intro and the first concrete case are visible; later concrete examples (the article promises "the same affliction" with multiple worked cases) are not. Worth fetching with subscriber access during final synthesis.
