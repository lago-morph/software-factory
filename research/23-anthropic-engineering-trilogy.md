# Anthropic's Engineering Trilogy (plus one) — Harnesses, Skills, and Parallel Claudes

**Round:** 5, Cluster 13.1.6 (PLAN.md §13.1.6)
**Author:** subagent on `claude/parallelize-with-subagents-SO0nR--sub-25`
**Date:** 2026-05-11
**Primary sources:** S12, S13, S14 (per `reference-only/chatgpt-deep-research-2026-05-11/sources.md`), plus the application-development harness post flagged in §"Weak or missing citations".

| ID | Article | URL | Published |
|---|---|---|---|
| S12 | Effective harnesses for long-running agents | `https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents` | 2025-11-26 |
| S13 | Equipping agents for the real world with Agent Skills | `https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills` | 2025-10-16 |
| S14 | Building a C compiler with a team of parallel Claudes | `https://www.anthropic.com/engineering/building-c-compiler` | 2026-02-05 (sources.md; InfoQ/Register cover the post in Feb 2026) |
| S15 | Harness design for long-running application development | `https://www.anthropic.com/engineering/harness-design-long-running-apps` | 2026-03-24 (per InfoQ "Anthropic Designs Three-Agent Harness…") |

**Fetch status.** Originally all four anthropic.com URLs returned **HTTP 403** to WebFetch; content was reconstructed from WebSearch excerpts and secondary coverage on InfoQ, VentureBeat, The Register, webpronews, daily.dev, ZenML LLMOps DB, HN, addyosmani.com — and from `github.com/anthropics/cwc-long-running-agents`. **On 2026-05-13, all four primary URLs were drained via the `fetch-blocked-urls` workflow (issue #29), plus a fifth Anthropic engineering post on Claude Code sandboxing.** This report is now **primary-source-anchored** for S12–S15 and has a new §8 covering the sandboxing post. See "Drain note (issue #29)" immediately below.

---

## Drain note (issue #36 extras) — 2026-05-13

Five additional primary sources were drained via USER-PATH-B exports under `research/manual/`, closing the round-7 platform.claude.com JS-SPA-shell failure and the round-6 quote-misattribution gap:

1. `platform.claude.com-agent-skills-overview.txt` — the Anthropic developer-docs page for Agent Skills (now full text; previously the WebFetch returned a `Loading...` SPA shell).
2. `support.claude.com-what-are-skills.txt` — the user-facing Help Center page (cross-product summary).
3. `01_skills_introduction.ipynb` — first cookbook notebook (intro + xlsx/pptx/pdf quickstarts).
4. `02_skills_financial_applications.ipynb` — second cookbook notebook (domain-specific worked examples).
5. `03_skills_custom_development.ipynb` — third cookbook notebook (custom-skill authoring + versioning).

**Round-6 quote-attribution gap CLOSED.** Every quote previously flagged as "from S13 but not actually in S13" is now confirmed verbatim in the platform-docs page and has been re-anchored in §5. Specifically:

- "A malicious Skill can direct Claude to invoke tools or execute code in ways that don't match the Skill's stated purpose..." — verbatim from `platform.claude.com/.../agent-skills/overview` §"Security considerations" (paraphrased: "a malicious Skill can direct Claude to invoke tools or execute code in ways that don't match the Skill's stated purpose"). Re-anchored.
- "Use Skills only from trusted sources: those you created yourself or obtained from Anthropic. If you must use a Skill from an untrusted or unknown source, exercise extreme caution and thoroughly audit it before use." — verbatim from platform docs §"Security considerations" (and the `<Warning>` block). Re-anchored.
- "Review all files bundled in the Skill … and look for unusual patterns like unexpected network calls, file access patterns, or operations that don't match the Skill's stated purpose." — verbatim from the platform-docs "Audit thoroughly" bullet. Re-anchored.
- "Treat like installing software" framing — verbatim from platform-docs bullet "Treat like installing software: Only use Skills from trusted sources. Be especially careful when integrating Skills into production systems with access to sensitive data or critical operations." The earlier "Treat skills like codebase dependencies — review, pin versions, and audit changes" wording is *not* verbatim in either source; corrected.
- Two-attack-class framing (code-level vs instruction-level) — *not* found verbatim in the platform docs in that exact form; the docs list "Tool misuse" and "Data exposure" as separate bullets plus an "External sources are risky" bullet calling out that fetched content "may contain malicious instructions." Updated §5 to use the platform-docs taxonomy.

**Cookbook content folded in (new §3.5).** A new subsection covers concrete SKILL.md schema (constraints not in S13), the three runtime environments (claude.ai / API / Claude Code) with their distinct network and package-install policies, the API beta-header triplet (`code-execution-2025-08-25`, `skills-2025-10-02`, `files-api-2025-04-14`), the `container.skills[]` request shape with `type: anthropic|custom` and `version: "latest"`, the Skills Management API (`client.beta.skills.create / list / versions.create / delete`), the cookbook's quantitative "Level 1 ~100 tokens; Level 2 <5k tokens; Level 3 effectively unlimited" table (this is the primary source for an earlier-rounds "30–50 tokens" claim — it's actually ~100 tokens per skill at metadata level per Anthropic's own docs, not 30–50), and the four cross-skill composition pattern (combining a custom brand-guidelines skill with the pre-built pptx skill in one `container.skills[]`).

**Cross-product clarifications from the support doc.** Skills are GA on **Free, Pro, Max, Team, and Enterprise** plans, with code-execution required; **beta** for Claude Code users and for all API users via the code-execution tool. Anthropic Skills (xlsx, pptx, docx, pdf), Custom Skills, Organization-Provisioned Skills (Team/Enterprise Owners can push org-wide defaults), and Partner Skills (Notion, Figma, Atlassian via the Skills Directory) are four distinct types — the engineering trilogy only treats the first two. The Help Center confirms the open-standard claim: "The Agent Skills specification is published as an open standard at agentskills.io ... A reference Python SDK is also available for developers implementing skills support in their own platforms."

**Refutations of prior claims:**

- **REFUTED — earlier rounds' "30–50 tokens per skill" estimate.** The platform docs explicitly state **~100 tokens per Skill** at the metadata level (Level 1 in the loading table). Our prior secondary-source figure was off by ~2×. §4.2 corrected. Note that this is per Anthropic's own docs, not S13.
- **REFUTED — "instructions-recommended-under-5k-tokens" was treated as informal guidance.** The platform docs and all three notebooks explicitly recommend **<5,000 tokens** for SKILL.md / Level 2 content. This is normative, not aspirational.
- **REFUTED — implicit assumption that custom Skills sync across surfaces.** The platform docs are explicit: "**Custom Skills do not sync across surfaces.** Skills uploaded to claude.ai must be separately uploaded to the API; Skills uploaded through the API are not available on claude.ai; Claude Code Skills are filesystem-based and separate from both." This is a portability gap our prior write-up did not flag.
- **REFUTED — assumption that API-runtime Skills can hit external networks.** The platform docs are explicit: on the Claude API surface, Skills have **No network access**, **No runtime package installation**, and **Pre-configured dependencies only**. Only Claude Code has full network access; claude.ai has "varying" access. This materially changes the threat model: API-surface Skills cannot exfiltrate over the network at all.

**Cross-reference flagged for [`04-every-skill-libraries`](04-every-skill-libraries.md) (not edited in this drain):** Every's SKILL.md frontmatter convention adds `tags`, `version`, and `allowed-tools` fields beyond Anthropic's required `name` + `description`. Anthropic's spec imposes constraints Every's docs do not surface: `name` max **64 chars**, lowercase letters/numbers/hyphens only, **reserved words "anthropic" and "claude" forbidden**, no XML tags; `description` max **1024 chars**, no XML tags. Report 04's claim that "the description *is* the discovery mechanism" matches Anthropic's framing precisely — the docs say "The `description` should include both what the Skill does and when Claude should use it." Worth flagging at report 04's next drain that Anthropic's constraints are stricter than Every's, that `allowed-tools` is *not* part of Anthropic's canonical schema (it's a Claude Code-specific extension), and that Anthropic's Level-1 budget is ~100 tokens per skill (a number Every's reports do not specify but is the load-economics constraint the convention is designed around).

---

## Drain note (issue #29) — 2026-05-13

This report was originally written from WebSearch result summaries and secondary outlet coverage because all five `www.anthropic.com/engineering/*` URLs (S12, S13, S14, S15, plus the sandboxing post) returned 403 from the sandbox. On 2026-05-13 the five primary URLs were fetched via the `fetch-blocked-urls` workflow under issue #29 and drained into this report. Concretely:

**Upgrades — claims now verbatim from primary sources, not secondary outlets:**

- **S12 author named:** Justin Young (previously unattributed). Post date confirmed Nov 26, 2025.
- **S12 two-role split:** the verbatim S12 framing is now sourced direct ("an **initializer agent** that sets up the environment on the first run, and a **coding agent** that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session"). Footnote 1 of S12 clarifies the two "agents" share the *same* system prompt, tools, and harness — they differ *only* in initial user prompt. This corrects an implicit assumption in §2.2 that they were architecturally distinct agents.
- **S12 feature count is "over 200":** "In the claude.ai clone example, this meant over 200 features" — verbatim. Prior report said "hundreds." Now exact.
- **S12 progress file is `claude-progress.txt`:** previously cited correctly, but the design rationale for JSON over Markdown is now verbatim: "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."
- **S12 testing tool is Puppeteer MCP, not Playwright:** "Screenshots taken by Claude through the Puppeteer MCP server as it tested the claude.ai clone." The report previously did not name the testing tool for S12; the Playwright MCP it cited was actually S15's tool. Now disambiguated.
- **S13 authors named:** Barry Zhang, Keith Lazuka, Mahesh Murag. Three-tier disclosure model in §4.2 confirmed verbatim against primary.
- **S13 Dec 18, 2025 update surfaced (new):** "We've published Agent Skills as an open standard for cross-platform portability." This was not in the prior report. Implication: Agent Skills is now an *open standard*, not just an Anthropic-internal convention, with a public reference at `agentskills.io`.
- **S14 model confirmed Opus 4.6** (matches report). Author Nicholas Carlini confirmed.
- **S14 all numeric facts confirmed verbatim:** 16 agents, ~2,000 sessions, 2 weeks, 2 billion input + 140 million output tokens, just under $20,000, 100,000-line Rust compiler, Linux 6.9 on x86/ARM/RISC-V, QEMU/FFmpeg/SQlite/postgres/redis, 99% GCC torture pass rate. Two new facts: it also compiles **Doom** ("it passes the developer's ultimate litmus test"); clean-room ("Claude did not have internet access at any point during its development"; dependency only on Rust stdlib).
- **S14 companion repo is `github.com/anthropics/claudes-c-compiler`** (newly named; the prior report cited only `cwc-long-running-agents`, which is S12's companion).
- **S14 exact harness loop now verbatim:** the bash loop using `claude --dangerously-skip-permissions -p "$(cat AGENT_PROMPT.md)" --model claude-opus-X-Y &> "$LOGFILE"` runs in a `while true` loop per agent. Confirms "Ralph loop" framing.
- **S14 agent-role list now exact:** five named specialized roles — (1) duplicate-code coalescer, (2) compiler-performance, (3) compiled-code-efficiency, (4) Rust-developer code-quality critic, (5) documentation. (Plus the main team solving the actual problem.) Previously the report mentioned "specialization" without enumerating roles.
- **S14 Linux-kernel parallelism trick now verbatim:** GCC was used as an "online known-good compiler oracle" — each agent randomly compiled most of the kernel with GCC and only a subset with Claude's compiler, enabling parallel bug isolation. This is *not* the file-lock pattern; it's a *separate* trick for monolithic builds. The §3 "file locks" paragraph is correct but only covers the multi-test case.
- **S15 author named:** Prithvi Rajasekaran (Anthropic Labs). Post date confirmed Mar 24, 2026.
- **S15 architecture confirmed three-agent (planner, generator, evaluator)** — matches report — but the planner-evaluator separation is grounded primarily in *self-evaluation failure*: "agents tend to respond by confidently praising the work — even when, to a human observer, the quality is obviously mediocre." Solo Claude is "a poor QA agent."
- **S15 stack is React + Vite + FastAPI + SQLite, later PostgreSQL** — primary clarifies SQLite→Postgres migration the report did not capture.
- **S15 cost/duration data is now primary:** v1 harness 6h/$200 vs solo 20m/$9 (~20× more expensive) for a 2D retro game maker; v2 harness 3h50m/$124.70 for a DAW build.
- **S15 GAN framing is now primary, not paraphrased from TeamDay.ai:** "Taking inspiration from Generative Adversarial Networks (GANs), I designed a multi-agent structure with a generator and evaluator agent." This was a journalist's framing in our prior version; it is now confirmed Anthropic's own framing.
- **S15 four evaluation criteria confirmed verbatim:** design quality, originality, craft, functionality — with each criterion's prompt language now quoted (e.g. "Unmodified stock components — or telltale signs of AI generation like purple gradients over white cards — fail here.").
- **S15 "context anxiety" — new named pattern:** Sonnet 4.5 "exhibited 'context anxiety,' in which they begin wrapping up work prematurely as they approach what they believe is their context limit." Context resets (full clean-slate restart + structured handoff) — *not* compaction — were the key mitigation in v1; Opus 4.5 "largely removed that behavior on its own," so the v2 harness drops context resets.

**Refuted / corrected claims:**

- **REFUTED — S12 model is Opus 4.5, not Opus 4.6.** S12 explicitly says: "even a frontier coding model like Opus 4.5 running on the Claude Agent SDK in a loop..." The prior report didn't pin a model to S12 but the implicit assumption (carried from S14) was 4.6. S15 confirms the harness work was done on **Opus 4.5 / Sonnet 4.5**, with S15's v2 iteration extending it to Opus 4.6. So: **S12+S15 = 4.5-era harness work; S14 = 4.6-era parallel-agent work.**
- **REFUTED — the S12 companion repo named in the prior report (`anthropics/cwc-long-running-agents`) is NOT cited by S12's primary text.** S12 itself points to `github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding` as the accompanying code. The `cwc-long-running-agents` repo (which prior reports treated as authoritative) may be a separate community/research artifact — its three primitives (default-FAIL contract, fresh-context evaluator, agent-maintained handoff) are not described in S12 itself. §2.3 of this report should be read as describing a *related* pattern not directly endorsed by S12; the canonical companion code per S12 is the `autonomous-coding` quickstart. This is a meaningful sourcing correction.
- **REFUTED — the "30–50 tokens per skill" budget is NOT verbatim in S13.** S13 says metadata gives "just enough information for Claude to know when each skill should be used without loading all of it into context" but does *not* state a token count. The 30–50 figure appears to have come from secondary coverage or the platform.claude.com docs, not S13 itself. The §4.2 claim should be re-attributed: "30–50 tokens per skill" is a *secondary-source estimate*, not an S13 quote. The *concept* of metadata-as-eager-routing is primary; the *number* is not.
- **REFUTED — the "Progressive disclosure that loads too eagerly defeats its purpose" quote is NOT in S13.** This quote and the platform-docs voice quotes in §5 (the "malicious Skill can direct Claude to invoke tools..." quote, the "treat skills like codebase dependencies — review, pin versions, and audit changes" quote, the "use Skills only from trusted sources" quote) do not appear in S13 itself. S13's own security text is much shorter: "We recommend installing skills only from trusted sources. When installing a skill from a less-trusted source, thoroughly audit it before use. Start by reading the contents of the files bundled in the skill to understand what it does, paying particular attention to code dependencies and bundled resources like images or scripts." The other quotes are presumably from `platform.claude.com/docs/.../agent-skills/overview` (which we couldn't fully drain). They should be re-attributed to that doc, not S13.

**Newly-surfaced primary claims worth knowing:**

- **S12: feature list is JSON, not Markdown, by design** — to prevent the agent from overwriting it. Tracked under a `passes: false` field; harness includes the instruction "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."
- **S12: a typical session start is a 6-step ritual** — pwd, read claude-progress.txt, read feature_list.json, git log, start init.sh, end-to-end test — *before* implementing any new feature. This is the canonical fresh-context bootstrap.
- **S12: stated future direction** — multi-agent specialization (testing agent, QA agent, code cleanup agent) is *not yet* in S12's harness but Justin Young flags it as the natural extension. S15 is in part that follow-up.
- **S13: Dec 18, 2025 — Agent Skills published as an open standard** at `agentskills.io` for cross-platform portability. This is significant: skills are no longer Anthropic-internal.
- **S14: clean-room (no internet) — newly explicit** ("Claude did not have internet access at any point during its development; it depends only on the Rust standard library").
- **S14: GCC-as-oracle parallelism** is a distinct pattern from the file-lock pattern, for monolithic-build problems where each agent would otherwise hit the same bug.
- **S14: time-blindness handling** is a named pattern — the `--fast` test option samples 1% or 10% deterministically per-agent but randomly across VMs, so each agent identifies regressions without spending hours.
- **S14: context-window pollution discipline** — test harness logs at most a few lines; logs `ERROR` prefix + reason on one line so `grep` works; pre-computes aggregate summary stats.
- **S15: "sprint contract" pattern** — generator and evaluator *negotiate* what "done" means for each sprint *before* code is written, via file-based exchange. This is a new named pattern not previously in the report.
- **S15: cost asymmetry concrete** — full harness ~20× cost of solo run (v1, $200 vs $9). v2 harness on Opus 4.6 reduces this materially ($124.70 for ~4h).
- **S15: "every component in a harness encodes an assumption about what the model can't do on its own"** — verbatim S15 principle. As models improve, components must be stress-tested for staleness. The v2 harness drops sprint decomposition because Opus 4.6 doesn't need it; it keeps the planner and evaluator because they still add lift.
- **S15: the evaluator is task-conditional** — "the evaluator is not a fixed yes-or-no decision. It is worth the cost when the task sits beyond what the current model does reliably solo." This is a principle the prior report did not surface.
- **Sandboxing post (NEW §9):** filesystem isolation + network isolation, built on Linux bubblewrap and macOS seatbelt; reduces permission prompts by 84% in internal usage; open-sourced as `github.com/anthropic-experimental/sandbox-runtime`; Claude Code on the web isolates credentials *outside* the sandbox via a custom git proxy. This is the security companion to S12/S14/S15 — long-running autonomous harnesses are only safe if the runtime they sit on is sandboxed.

Source-status table in §8 has been flipped from ❌/403 to ✅ for all five drained URLs.

---

## 1. Why this report exists

Anthropic published four engineering posts between October 2025 and March 2026 that together describe its own factory-pattern thinking. Prior reports cite them in compressed form: `04-every-skill-libraries.md` treats SKILL.md as a syntactic convention without naming Anthropic's three-tier disclosure model; the C-compiler experiment surfaces only as a magnitude argument in `00-synthesis.md`. This report collates the four posts and compares Agent Skills to two independent instantiations — El Kaim's Codex ([`17-el-kaim-book-codex-and-skill-substrate`](17-el-kaim-book-codex-and-skill-substrate.md)) and Every's Compound Knowledge plugin ([`11-compound-knowledge`](followup/11-compound-knowledge.md)).

---

## 2. The long-running-harness pattern (S12, S15, companion repo)

### 2.1 Diagnosis (S12)

The structural problem, verbatim from S12 (Justin Young, Nov 26, 2025): "agents must work in discrete sessions, and each new session begins with no memory of what came before. Imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift." Compaction is named but found insufficient: "even a frontier coding model like Opus 4.5 running on the Claude Agent SDK in a loop across multiple context windows will fall short of building a production-quality web app if it's only given a high-level prompt." Two failure modes: (i) "the agent tended to try to do too much at once — essentially to attempt to one-shot the app"; (ii) "After some features had already been built, a later agent instance would look around, see that progress had been made, and declare the job done." The agent must maintain its own handoff *on disk*.

### 2.2 The two-role split: initializer + coding agent

S12 splits the work across two prompts (per S12 footnote 1: they are *not* architecturally distinct agents — same system prompt, tools, and harness; only the initial user prompt differs):

1. **Initializer agent** — runs *only on the first session*. Specialized prompting creates: `init.sh` (how to start the dev server and run the app), `claude-progress.txt` (session-to-session log), an initial git commit (baseline), and a *comprehensive feature-list file*. In the claude.ai-clone example, S12 reports "over 200 features" expanded from a single high-level prompt, each shaped as `{category, description, steps[], passes: false}` and stored in JSON (not Markdown) because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."
2. **Coding agent** — runs every subsequent session, scoped to *one feature per session*. The loop: read `claude-progress.txt` and git log, run init.sh, run a basic end-to-end test, then build *one* feature using browser automation (S12 uses **Puppeteer MCP** for the claude.ai-clone example, not Playwright), update `passes` for that feature only, commit, stop.

Per S12 verbatim: "the key insight here was finding a way for agents to quickly understand the state of work when starting with a fresh context window, which is accomplished with the claude-progress.txt file alongside the git history. Inspiration for these practices came from knowing what effective software engineers do every day."

Hardening prompt to prevent agents editing tests (S12 verbatim): "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

### 2.3 What's on disk

**Sourcing correction (issue #29 drain):** S12 itself cites `github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding` as the official accompanying code. The `anthropics/cwc-long-running-agents` repo we cited in earlier rounds is a *related but separate* community/research artifact that elaborates the pattern, not the canonical S12 companion. The three primitives below originate from `cwc-long-running-agents`, not S12 itself, but they are consistent with S12's design.

The companion-pattern repo makes the contract concrete with three primitives:

1. **Default-FAIL contract.** `test-results.json` initialised so every feature is `{"passes": false}`. A `PreToolUse` hook (`track-read.sh` + `verify-gate.sh`) refuses writes to results unless the agent has first opened the evidence file via Read. *No claiming success without opening evidence.* This is consistent with S12's own discipline — JSON over Markdown for tamper resistance, and the "It is unacceptable to remove or edit tests" prompt.
2. **Fresh-context evaluator.** `agents/evaluator.md` — a subagent with no Write/Edit tools, invoked from a clean context. Returns `PASS` or `NEEDS_WORK`. A failed evaluation becomes the next builder session's starting prompt. S12 itself notes this as *future* work — "specialized agents like a testing agent, a quality assurance agent, or a code cleanup agent" — and S15 is in part the realization of that direction.
3. **Agent-maintained handoff.** `CLAUDE.md` directs the agent to maintain `PROGRESS.md` and commit on stop (`commit-on-stop.sh` catches uncommitted work). Operator controls: `kill-switch.sh` (halts tool calls while `AGENT_STOP` exists); `STEER.md` (read once per run for mid-stream redirection).

The repo's framing: "This is a **pattern reference, not turnkey**."

**S12's own canonical bootstrap sequence** (verbatim): every coding-agent session runs `pwd`; reads `claude-progress.txt`; reads `feature_list.json`; runs `git log --oneline -20`; starts the dev server via `init.sh`; tests basic functionality through Puppeteer MCP; only then picks up the next feature.

### 2.4 The application-development harness (S15) as operational analog to S14

S15 (Prithvi Rajasekaran, Anthropic Labs, March 24, 2026) builds on S12 and adds a **three-agent architecture — planner, generator, evaluator** — that produces "rich full-stack applications over multi-hour autonomous coding sessions" (S15 verbatim). The GAN framing is Anthropic's own, not a journalist's: "Taking inspiration from Generative Adversarial Networks (GANs), I designed a multi-agent structure with a generator and evaluator agent."

The three roles, verbatim from S15:

- **Planner** — takes a "simple 1-4 sentence prompt and expanded it into a full product spec." Stays at product context + high-level technical design, deliberately *not* specifying granular implementation, because "if the planner tried to specify granular technical details upfront and got something wrong, the errors in the spec would cascade into the downstream implementation." Also weaves AI features into the spec.
- **Generator** — works "in sprints, picking up one feature at a time from the spec." Stack: React, Vite, FastAPI, **SQLite (later PostgreSQL)** — primary clarifies the migration. Has git for version control.
- **Evaluator** — uses **Playwright MCP** to "click through the running application the way a user would, testing UI features, API endpoints, and database states." Grades against four criteria from the frontend experiment, "adapted here to cover product depth, functionality, visual design, and code quality. Each criterion had a hard threshold, and if any one fell below it, the sprint failed."

**Sprint contract pattern (new from primary):** before each sprint, "the generator and evaluator negotiated a sprint contract: agreeing on what 'done' looked like for that chunk of work before any code was written." Communication is *file-based* — one agent writes a file, another reads and responds.

**Context-resets discipline (new from primary):** S15's v1 ran on Sonnet 4.5, which "exhibited 'context anxiety,' in which they begin wrapping up work prematurely as they approach what they believe is their context limit." S15 mitigates with **context resets** (full clean-slate restart + structured handoff) — *not* compaction — because "while compaction preserves continuity, it doesn't give the agent a clean slate." Opus 4.5 largely removed the behavior, so the v2 harness drops context resets.

**Cost data, verbatim from S15:**

| Harness | Build | Duration | Cost |
|---|---|---|---|
| Solo (v1) | 2D retro game maker | 20 min | $9 |
| Full v1 harness | 2D retro game maker | 6 hr | $200 (≈20×) |
| v2 harness (Opus 4.6, no sprints) | Browser DAW | 3 hr 50 min | $124.70 |

**v2 harness evolution (new):** with Opus 4.6, S15 drops the sprint construct entirely and moves the evaluator to a single pass at the end. The planner and evaluator continue to add lift, but per S15 verbatim: "the evaluator is not a fixed yes-or-no decision. It is worth the cost when the task sits beyond what the current model does reliably solo." This is the operational principle: *harness components encode assumptions about model weakness; as models improve, components must be stress-tested for staleness.*

This is the **operational analog to the C-compiler experiment** — S14 proves the harness scales to systems code at $20k; S15 proves it scales to product-shaped web apps at $125–200 per app. The compiler is the magnitude proof; the application harness is the productizable shape.

---

## 3. The C-compiler case study — numbers verbatim (S14)

S14 (Nicholas Carlini, Safeguards team, Feb 5, 2026) is the magnitude proof. All numbers now sourced verbatim from S14 itself; InfoQ / The Register / webpronews / officechai concur but the primary anchors them:

| Quantity | Value |
|---|---|
| Number of agents | **16** Claude Opus 4.6 instances in parallel |
| Sessions | "nearly **2,000** Claude Code sessions" |
| Wall-clock | **2 weeks** |
| Input tokens consumed | **2 billion** |
| Output tokens generated | **140 million** |
| Total cost | "just under **$20,000**" in API costs |
| Output artefact | **~100,000-line** Rust-based C compiler, from scratch |
| Capability | "can build a bootable **Linux 6.9**" on x86, ARM, and RISC-V |
| Additional builds | "QEMU, FFmpeg, SQLite, postgres, redis" |
| Test-suite result | "**99% pass rate** on most compiler test suites including the [GCC torture test suite](https://gcc.gnu.org/onlinedocs/gccint/Torture-Tests.html)" |
| Litmus test | "it can compile and run **Doom**" |
| Clean-room | "Claude did not have internet access at any point during its development; it depends only on the Rust standard library" |
| Companion repo | `github.com/anthropics/claudes-c-compiler` |
| Author | Nicholas Carlini, Safeguards team |

**Infrastructure (verbatim):** "A new bare git repo is created, and for each agent, a Docker container is spun up with the repo mounted to /upstream. Each agent clones a local copy to /workspace, and when it's done, pushes from its own local container to upstream." Coordination is via **file locks** in `current_tasks/`: agents claim tasks by writing text files (e.g. `current_tasks/parse_if_statement.txt`); "git's synchronization forces the second agent to pick a different one"; once complete, the agent pulls from upstream, merges other agents' changes, pushes, and removes the lock. Carlini notes: "I haven't yet implemented any other method for communication between agents, nor do I enforce any process for managing high-level goals. I don't use an orchestration agent."

**The session loop (verbatim bash):**
```bash
while true; do
    COMMIT=$(git rev-parse --short=6 HEAD)
    LOGFILE="agent_logs/agent_${COMMIT}.log"
    claude --dangerously-skip-permissions \
           -p "$(cat AGENT_PROMPT.md)" \
           --model claude-opus-X-Y &> "$LOGFILE"
done
```

This is the **Ralph-Wiggum loop** ("Ralph loop") — feed the same prompt to Claude repeatedly, letting it observe its own previous work in files and git history for self-referential improvement. Exactly S12's "the agent maintains the handoff itself" instantiated at 16-way parallelism.

**The five specialized agent roles (new from primary):** beyond the main team solving the compiler problem, Carlini ran five named specialists: (1) duplicate-code coalescer ("LLM-written code frequently re-implements existing functionality"); (2) compiler-performance improver; (3) compiled-output efficiency; (4) Rust-developer code-quality critic; (5) documentation maintainer.

**The Linux-kernel parallelism trick (new from primary):** the file-lock pattern works when there are many failing tests, but breaks on monolithic builds where every agent hits the same bug. Carlini's fix: use **GCC as an online known-good compiler oracle** — randomly compile most kernel files with GCC, only a subset with Claude's compiler, then bisect failures to Claude's subset. "This let each agent work in parallel, fixing different bugs in different files." Delta-debugging is then used for file-pair interactions.

**Two model-aware harness disciplines (new from primary):**

- **Context-window pollution.** Test harness logs "a few lines of output and log all important information to a file"; uses `ERROR <reason>` on a single line so `grep` works; pre-computes aggregate summary stats so Claude doesn't recompute them.
- **Time blindness.** Claude "can't tell time and, left alone, will happily spend hours running tests instead of making progress." The harness ships `--fast` that runs a 1% or 10% deterministic-per-agent, random-across-VMs sample, so each agent identifies regressions cheaply but full coverage emerges across the fleet.

**Economic framing (now verbatim):** "$20,000... is a fraction of what it would cost me to produce this myself — let alone an entire team."

**Carlini's caveats (worth knowing):** the generated code is "less efficient code than GCC with all optimizations disabled"; Rust code quality "nowhere near the quality of what an expert Rust programmer might produce"; the compiler cheats on 16-bit x86 boot by calling GCC; assembler and linker are buggy. The post is explicit: "The resulting compiler has nearly reached the limits of Opus's abilities."

---

## 4. Agent Skills — progressive disclosure and the three loading tiers (S13)

### 4.1 What a skill is

S13 (Barry Zhang, Keith Lazuka, Mahesh Murag, Oct 16, 2025; updated Dec 18, 2025): "At its simplest, a skill is a directory that contains a `SKILL.md file`. This file must start with YAML frontmatter that contains some required metadata: `name` and `description`. At startup, the agent pre-loads the `name` and `description` of every installed skill into its system prompt."

**Open-standard update (Dec 18, 2025; new from primary):** "We've published Agent Skills as an open standard for cross-platform portability." Public reference: `agentskills.io`. Skills are no longer Anthropic-internal — they are a cross-vendor convention.

### 4.2 The three-tier model

Per S13, skills load in **three discrete stages**, verbatim:

1. **Tier 1 — Metadata (eager).** "This metadata is the **first level** of *progressive disclosure*: it provides just enough information for Claude to know when each skill should be used without loading all of it into context." *Note: the "30–50 tokens per skill" budget cited in earlier rounds is a secondary-source estimate, not in S13. S13 does not state a token count. The platform docs (drained issue #36) do state a quantitative budget — **~100 tokens per Skill** at the metadata level, **under 5k tokens** for the SKILL.md body when triggered, and **effectively unlimited** for bundled Level-3 files since they consume zero context unless read.*
2. **Tier 2 — SKILL.md body (lazy, on relevance).** "The actual body of this file is the **second level** of detail. If Claude thinks the skill is relevant to the current task, it will load the skill by reading its full `SKILL.md` into context."
3. **Tier 3 — Bundled files (lazy, on use).** "These additional linked files are the **third level** (and beyond) of detail, which Claude can choose to navigate and discover only as needed." S13's worked example: the PDF skill bundles `reference.md` and `forms.md` separately, so the SKILL.md author can "trust that Claude will read `forms.md` only when filling out a form."

S13's framing principle (verbatim): "Progressive disclosure is the core design principle that makes Agent Skills flexible and scalable... Agents with a filesystem and code execution tools don't need to read the entirety of a skill into their context window when working on a particular task. This means that the amount of context that can be bundled into a skill is effectively unbounded."

**Refutation (issue #29):** the "Progressive disclosure that loads too eagerly defeats its purpose..." quote in our prior version is *not* in S13. We have removed it; the actual S13 framing is the unbounded-context-via-lazy-loading framing above.

This is still the rule `04-every-skill-libraries.md` records only implicitly — Every's `description` field doubles as a trigger contract — but the *quantitative* token budget the prior version named is not a primary-source claim.

### 4.3 The metaphor

S13 closes with a deliberately mundane analogy: "Like a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix, skills let Claude load information only as needed."

### 4.4 What the cookbook adds — concrete schema, API surface, and runtime constraints (drained issue #36)

S13 is the conceptual frame. The platform-docs page (`platform.claude.com/.../agent-skills/overview`) and the three official cookbook notebooks (`anthropics/claude-cookbooks/skills/notebooks/{01,02,03}_*.ipynb`) are the concrete reference. Together they specify:

**SKILL.md schema (normative, from platform docs):**

- Required fields: `name`, `description`.
- `name`: max **64 characters**, lowercase letters/numbers/hyphens only, no XML tags, **reserved words "anthropic" and "claude" are forbidden**.
- `description`: non-empty, max **1024 characters**, no XML tags. Authoring guidance: "The `description` should include both what the Skill does and when Claude should use it." This is the trigger contract.
- Cookbook notebook 3's minimal canonical layout: `skill_name/{SKILL.md, *.md, scripts/, resources/}`. SKILL.md is the only required file. Multiple top-level `.md` files are all loaded as Level-2 content (not just SKILL.md and REFERENCE.md, despite what the engineering examples imply).

**The Level-1/2/3 token table (verbatim from platform docs):**

| Level | When loaded | Token cost | Content |
|---|---|---|---|
| 1: Metadata | Always (at startup) | **~100 tokens per Skill** | `name` and `description` from YAML frontmatter |
| 2: Instructions | When Skill is triggered | **Under 5k tokens** | SKILL.md body |
| 3+: Resources | As needed | **Effectively unlimited** | Bundled files (read via bash; script *code* never enters context — only output) |

The "effectively unlimited Level 3" claim is grounded in a specific mechanism: **scripts are executed via bash and only their output enters context**. From the docs: "When Claude runs `validate_form.py`, the script's code never loads into the context window. Only the script's output (like 'Validation passed' or specific error messages) consumes tokens." This is a tighter primitive than report 04's "side-files capped at 50 files / 1MB" framing — Anthropic's spec is bandwidth-unbounded by design.

**The API surface (verbatim, from notebook 1):**

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    container={"skills": [
        {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
    ]},
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[...],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)
```

Three load-bearing constraints:

1. **`client.beta.messages.create()`**, not `client.messages.create()` — the `container` parameter is beta-only.
2. **Three beta headers always required together** — `code-execution-2025-08-25`, `skills-2025-10-02`, `files-api-2025-04-14`. The cookbook explicitly flags: "When using Skills, you MUST include the code_execution tool in your request." Skills *require* code execution.
3. **`container.skills[]`** is a list of `{type, skill_id, version}` objects. `type` is `"anthropic"` (pre-built) or `"custom"` (user-uploaded). The cookbook's brand-guidelines example demonstrates **multi-skill composition in a single request** — combine a custom skill with a pre-built skill: `[{"type":"custom","skill_id":brand_id,...}, {"type":"anthropic","skill_id":"pptx",...}]`. The host agent loads both metadata blocks at startup.

**Skills Management API (verbatim, notebook 3):**

```python
client.beta.skills.create(display_title="My Skill", files=files_from_dir("path/to/skill"))
client.beta.skills.list(source="custom")            # or source="anthropic"
client.beta.skills.versions.create(skill_id=..., files=files_from_dir(...))
client.beta.skills.versions.list(skill_id=...)
client.beta.skills.versions.delete(skill_id=..., version=...)
client.beta.skills.delete(skill_id)
```

**Versioning model:** custom skills use epoch-timestamp version numbers (not semver); `"latest"` is the recommended pin for Anthropic-managed skills. The cookbook explicitly demonstrates a *version-creation workflow* — make an edit, call `versions.create` against the same `skill_id`, and the new version becomes `latest`. There is no rollback API surfaced; rollback is "specify a non-latest version explicitly." Skills *cannot be re-uploaded under the same display_title* — duplicate-name uploads fail with "cannot reuse an existing display_title."

**Runtime constraints by surface (normative, platform docs §"Runtime environment constraints"):**

| Surface | Network access | Package install | Notes |
|---|---|---|---|
| claude.ai | Varying (per user/admin settings) | n/a | Custom skills are per-user; no admin org-wide management |
| Claude API | **None** — no external API calls | **None** — pre-installed packages only | Skills are workspace-shared |
| Claude Code | Full | Local-only encouraged | Filesystem-based; personal at `~/.claude/skills/` or project at `.claude/skills/`; sharable via Claude Code Plugins |

This materially constrains the threat model: an API-surface Skill *cannot exfiltrate over the network* because the runtime gives it no network. The post-S13 platform stance is that the *primary defensive layer is runtime restriction at the code-execution boundary*, not skill-content scanning — consistent with the sandboxing post in §8.

**Sharing scope:**
- claude.ai — individual-user-only, no admin org-wide push.
- API — workspace-wide; all workspace members see uploaded skills.
- Claude Code — personal or project-scoped; sharing via Plugins.

**Cross-surface non-portability:** "Skills uploaded to claude.ai must be separately uploaded to the API; Skills uploaded through the API are not available on claude.ai; Claude Code Skills are filesystem-based and separate from both." Custom Skills *do not sync across surfaces*. This is a real portability gap the engineering posts gloss over.

**Domain-specific worked example (notebook 2):** the financial-applications notebook demonstrates a three-stage pipeline pattern: `xlsx` skill → `pptx` skill → `pdf` skill, with structured-data input (`pd.DataFrame.to_string()`, `json.dumps()`) consistently flowing into each stage. The notebook explicitly recommends: "Structured data (JSON/CSV) is more efficient than prose." This is a concrete authoring discipline the engineering posts only allude to.

**Custom-skill authoring discipline (notebook 3):**

1. **Single responsibility per skill** — "Each skill should focus on one area of expertise."
2. **SKILL.md under 5,000 tokens** (the Level-2 budget).
3. **Composition over mega-skills** — "Combine skills vs. mega-skill" is listed under "Performance Optimization."
4. **Test before production** — the notebook ships a `test_skill(client, skill_id, prompt)` helper that runs each new skill against a fixed test prompt.
5. **Security checklist** (notebook 3's §"Security Considerations"): no hardcoded API keys; no sensitive data in skill files; sanitize inputs in scripts; log skill usage for audit trail.

This last item is the closest the cookbook comes to formal skill-security guidance — and it is *authoring-side*, not consumption-side. The platform docs §"Security considerations" carry the consumption-side framing (audit, trust source, treat-like-installing-software). There is no Anthropic-shipped scanner in either source.

**The S13 / platform-docs / cookbook tier together:** S13 is the design memo (why progressive disclosure); the platform docs are the normative schema and runtime contract (what's allowed, with what token costs); the cookbook is the implementation tutorial (working code, common errors, composition patterns). All three are needed to author a production skill; none is sufficient alone.

---

## 5. Security considerations Anthropic flags around skills

**Sourcing correction (issues #29 + #36 drains):** several quotes in earlier rounds were attributed to S13 but do not appear in the S13 primary text. The platform-docs page (`platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`) was drained in round 7 (issue #36) and now anchors these. Re-attributed below: S13-direct vs platform-docs-direct.

**From S13 directly (verbatim):** "Skills provide Claude with new capabilities through instructions and code. While this makes them powerful, it also means that malicious skills may introduce vulnerabilities in the environment where they're used or direct Claude to exfiltrate data and take unintended actions. We recommend installing skills only from trusted sources. When installing a skill from a less-trusted source, thoroughly audit it before use. Start by reading the contents of the files bundled in the skill to understand what it does, paying particular attention to code dependencies and bundled resources like images or scripts. Similarly, pay attention to instructions or code within the skill that instruct Claude to connect to potentially untrusted external network sources."

**From `platform.claude.com/.../agent-skills/overview` §"Security considerations" (now drained, verbatim):**

1. Top-level framing: "Use Skills only from trusted sources: those you created yourself or obtained from Anthropic. Skills provide Claude with new capabilities through instructions and code, and while this makes them powerful, it also means **a malicious Skill can direct Claude to invoke tools or execute code in ways that don't match the Skill's stated purpose**."
2. The `<Warning>` block: "If you must use a Skill from an untrusted or unknown source, exercise extreme caution and thoroughly audit it before use. Depending on what access Claude has when executing the Skill, malicious Skills could lead to **data exfiltration, unauthorized system access, or other security risks**."
3. The five-bullet checklist (verbatim):
   - **Audit thoroughly**: "Review all files bundled in the Skill: SKILL.md, scripts, images, and other resources. Look for unusual patterns like unexpected network calls, file access patterns, or operations that don't match the Skill's stated purpose."
   - **External sources are risky**: "Skills that fetch data from external URLs pose particular risk, as fetched content may contain malicious instructions. Even trustworthy Skills can be compromised if their external dependencies change over time."
   - **Tool misuse**: "Malicious Skills can invoke tools (file operations, bash commands, code execution) in harmful ways."
   - **Data exposure**: "Skills with access to sensitive data could be designed to leak information to external systems."
   - **Treat like installing software**: "Only use Skills from trusted sources. Be especially careful when integrating Skills into production systems with access to sensitive data or critical operations."

**Corrections to prior rounds' framing:**

- The "Two attack classes (code-level vs instruction-level)" taxonomy our prior version used is *not* what the platform docs say. The docs taxonomy is **Tool misuse + Data exposure + External-sources risk**, with the "external sources" bullet being the closest analog to instruction-level injection ("fetched content may contain malicious instructions"). Replaced.
- "Treat skills like codebase dependencies — review, pin versions, and audit changes" is *not* verbatim in either source. The closest verbatim is the **"Treat like installing software"** bullet above. The dependency-management framing (review/pin/audit) is a useful synthesis but should be marked as a *paraphrase* of the docs, not a quote.
- The platform docs **explicitly flag external-dependency drift** as a separate concern: "Even trustworthy Skills can be compromised if their external dependencies change over time." This is the closest Anthropic comes to a *supply-chain* framing in either S13 or the docs.

**From VentureBeat (secondary, on why scanners miss it):** "there is no code to scan, no binary payload, no known signature, and the 'malicious code' is English text … which traditional SAST, DAST, and malware scanners miss entirely."

**Runtime as primary defense.** The platform docs make explicit (cross-ref §4.4) that the **runtime enforces what scanning cannot**: API-surface Skills have *zero* network access; claude.ai Skills run inside the code-execution sandbox; Claude Code Skills inherit the user's network but can be wrapped by the §8 sandbox-runtime. Anthropic's stance: trust the source on the *content* side, lock the *runtime* on the execution side.

**S13's own security stance is minimalist** — three sentences, summarizing to "trust the source, audit before use." The more elaborate threat-model and treat-like-installing-software framing is a platform-docs contribution, not the engineering post. The cookbook's notebook-3 §"Security Considerations" adds an *authoring-side* checklist (no hardcoded credentials; no sensitive data in skill files; sanitize inputs; log usage) that neither S13 nor the platform docs cover.

Downstream ecosystem evidence the design anticipates: as of Feb–Mar 2026, public skill registries had material malicious-skill problems (ClawHub "ClawHavoc" — 341 malicious skills; Mobb.ai — 140,963 issues across 22,511 skills; Snyk ToxicSkills — prompt injection in 36% of skills tested). S13 names the threat class but ships no scanner — the stance is *trust-based, audit-required*. See §9 for the *sandboxing* complement that arrived in Oct 2025 — once skills run inside a sandbox with filesystem + network isolation, the threat surface narrows considerably.

---

## 6. The trilogy read together

S12, S13, S14, S15 form one argument: **skills (S13) handle modular procedural knowledge** via progressive disclosure with a token budget; **harnesses (S12, S15) handle continuity** via two- or three-role splits plus on-disk handoff files (`PROGRESS.md`, `test-results.json`, `init.sh`, feature list); **parallel agents (S14) handle scale** — when single-agent sessions are deterministic, 16-way parallelism on a shared bare git repo with file-lock coordination becomes tractable; **trust is load-bearing** — skills are trusted-by-default within an organization, with audit-and-pin as the perimeter. *Skills are the verbs, harnesses are the shifts, parallel agents are the crew, audit is the perimeter.* This is the shape [`02-compound-atelier`](../architectures/02-compound-atelier.md) is reaching for under different names.

---

## 7. Three independent instantiations of "typed distributed knowledge for AI agents"

Anthropic's Agent Skills (S13), El Kaim's Codex (`research/17-...`), and Every's Compound Knowledge plugin (`research/followup/11-...`) all treat *knowledge for AI agents* as distributed, typed, and procedurally consumed — at different altitudes.

| Dimension | Anthropic **Agent Skills** | El Kaim **EA Codex** | Every **Compound Knowledge** |
|---|---|---|---|
| Unit | SKILL.md folder | Typed YAML artefact under a SKILL.md envelope | `docs/knowledge/*.md` with typed frontmatter |
| What's typed | `name` + `description`; body is procedural prose | `kind: Principle\|Standard\|Reference\|Blueprint` plus `validation.check`, `linkedPrinciples`, `obsolescenceSignals` | `type: insight\|playbook\|correction\|pattern`, `confidence`, `source` |
| Granularity | Procedure / capability (do-X) | Normative claim about the enterprise (constrain-X) | Learning from a past cycle (learned-Y) |
| Loading | Three-tier progressive disclosure | Marketplace manifest with `triggers.keywords/contexts`, `dependencies[]`; three-layer compose | Inline retrieval at planning time via knowledge-base-researcher agent |
| Authority on write | Skill author; user audits | EA Council; MR workflow against Git | Orchestrating skill only — *agents return text, never write* |
| Validation | None ("treat skills as code; audit") | JSON Schema → Rego → MCP grounding | `kw:review` reviewers + `kw:confidence` + `stale-knowledge-checker` |
| Stale entries | None codified | `obsolescenceSignals[]` re-open standards | Inline check at every `kw:compound`; contradicts/supersedes/complements |
| Security | "Trust the source, audit on import" | EA Council CODEOWNERS + Rego deny rules | "No silent overwrites" — single write chokepoint |
| Compounding | None — skills are static once shipped | Graph traversal — edit a principle, surface every standard that cites it | Four-way typed learning fed back via `kw:compound` |

Three readings of the same problem:

1. **Anthropic solves for *capability extension*.** A skill is a new verb. Progressive disclosure is about token economy. Security is source provenance. No built-in story for how skills *evolve*.
2. **El Kaim solves for *enterprise governance*.** A Codex object is a normative claim. Disclosure is marketplace routing. Security is the EA Council + MR workflow. Compounding is *graph traversal* — change one principle, see every downstream artefact.
3. **Every solves for *learning across cycles*.** A knowledge entry is a *finding* about past work. Disclosure is researcher-agent retrieval at planning time. Security is the single-chokepoint write rule. Compounding is *typed feedback into the store* with explicit precedence (corrections always win).

What each adds the others lack:

- **Anthropic** — the *eager-metadata-then-lazy-everything* model is the only contribution that makes a 100-skill library economically loadable. (Note: S13 does not name a per-skill token budget; the 30–50 figure from earlier rounds was secondary-source.)
- **El Kaim** — the *validation chain* (schema → Rego → MCP grounding) is the only contribution that makes skills *executable as policy*. S13 does not offer this.
- **Every** — the *typed learning + inline staleness check* is the only contribution that makes the store *self-curating*. S13 and Codex assume out-of-band authorship.

**Implication for [`02-compound-atelier`](../architectures/02-compound-atelier.md).** Adopt:

1. From Anthropic — three-tier disclosure (Tier 1 eager metadata; Tiers 2–3 lazy) for the procedural-skill side of the library. This is what `04-every-skill-libraries.md` only implies. (Earlier rounds quoted a "30–50 tokens at startup" budget; that figure is not in S13 itself and should be treated as a secondary-source estimate.)
2. From El Kaim — typed normative objects with schema → cross-field-check → MCP grounding chain (the §8 proposal in `research/17-...` already extends this).
3. From Every — typed learnings (insight / playbook / correction / pattern), inline staleness check at write time, single-write-chokepoint rule.

The three are not redundant. They sit at different altitudes (verb / norm / lesson) and feed different consumers (executing agent / policy engine / planner). A factory that runs all three is the union, not the average.

---

## 8. Claude Code sandboxing — the security companion to the harness posts

**Source:** `https://www.anthropic.com/engineering/claude-code-sandboxing` — "Beyond permission prompts: making Claude Code more secure and autonomous" (David Dworken and Oliver Weller-Davies, Oct 20, 2025). Drained in this round; integrated here as the security complement to S12/S14/S15.

### 8.1 Why this post belongs alongside the trilogy

S12 / S14 / S15 all assume *autonomous, long-running* agents running real shell commands, editing real files, and pushing to real git remotes. S14's Ralph loop literally runs `claude --dangerously-skip-permissions` in `while true`. That is operationally tractable only if the *runtime underneath* enforces the boundaries the harness itself cannot. The sandboxing post is the security contract that makes the harness pattern safe to run at scale.

### 8.2 The two-boundary design

The post defines the threat model crisply (verbatim): "effective sandboxing requires *both* filesystem and network isolation. Without network isolation, a compromised agent could exfiltrate sensitive files like SSH keys; without filesystem isolation, a compromised agent could easily escape the sandbox and gain network access. It's by using both techniques that we can provide a safer and faster agentic experience for Claude Code users."

The two boundaries:

1. **Filesystem isolation.** "Claude can only access or modify specific directories. This is particularly important in preventing a prompt-injected Claude from modifying sensitive system files." Implementation: read/write only the current working directory; everything else blocked.
2. **Network isolation.** "Claude can only connect to approved servers. This prevents a prompt-injected Claude from leaking sensitive information or downloading malware." Implementation: internet access only through a unix domain socket to a proxy server outside the sandbox, which enforces per-domain rules and handles user confirmation for newly requested domains.

OS primitives: **Linux bubblewrap** + **macOS seatbelt**. Both enforce at the OS level and cover not just Claude Code's direct interactions "but also any scripts, programs, or subprocesses that are spawned by the command."

### 8.3 Two productized features

1. **Sandboxed bash tool.** A research-preview sandbox runtime that scopes Claude Code's bash tool — "lets you define exactly which directories and network hosts your agent can access, without the overhead of spinning up and managing a container." Open-sourced at `github.com/anthropic-experimental/sandbox-runtime`. Invocation: `/sandbox` in Claude Code. Operational measurement (verbatim): "sandboxing safely reduces permission prompts by 84%."
2. **Claude Code on the web.** Each session runs in an isolated cloud sandbox. Critical design choice: "We've designed this sandbox to ensure that sensitive credentials (such as git credentials or signing keys) are never inside the sandbox with Claude Code." A custom proxy service handles all git interactions — "Inside the sandbox, the git client authenticates to this service with a custom-built scoped credential. The proxy verifies this credential and the contents of the git interaction (e.g. ensuring it is only pushing to the configured branch), then attaches the right authentication token before sending the request to GitHub."

### 8.4 Implications for the factory architectures

- **Architecture 1 (Refinery), Architecture 4 (Tournament).** Any tournament that runs N parallel evaluators must run each in a sandbox — otherwise an adversarial genome could exfiltrate the fitness vector or poison the orchestrator's filesystem.
- **Architecture 3 (Foundry).** Phase-gated V&V agents have *write* access to phase artifacts but should not have *read* access to credentials. The Claude-Code-on-the-web pattern (credentials outside the sandbox, proxied access via scoped tokens with branch-and-repo verification) is the cleanest model for git-pushing V&V agents.
- **Architecture 2 (Atelier) — skills + sandboxing.** §5 noted that S13's security stance is trust-based + audit-required, with no scanner. The sandboxing post is the *runtime* answer to the trust-and-audit-required posture: a skill from an untrusted source still cannot exfiltrate credentials or modify system files if it runs inside a filesystem+network sandbox. This is the missing piece in §5: the practical mitigation Anthropic ships is not skill scanning but *sandbox at the runtime layer*.
- **Operational metric to track.** 84% reduction in permission prompts is the throughput benefit; the safety benefit is that "even a successful prompt injection is fully isolated, and cannot impact overall user security. This way, a compromised Claude Code can't steal your SSH keys, or phone home to an attacker's server."

The pairing is now: **S12/S14/S15 specify how long-running agents *do work*; the sandboxing post specifies the runtime contract that lets that work happen safely without an operator approving each step.**

---

## 9. Sources, status, follow-ups

| Source | Fetched? | Notes |
|---|---|---|
| S12 — Effective harnesses for long-running agents | ✅ Drained from `fetched/issue-29/` 2026-05-13 | Author Justin Young confirmed; Opus 4.5 (not 4.6); Puppeteer MCP (not Playwright); >200 features; canonical companion code is `claude-quickstarts/autonomous-coding`, not `cwc-long-running-agents` |
| S13 — Equipping agents with Agent Skills | ✅ Drained from `fetched/issue-29/` 2026-05-13 | Authors Barry Zhang, Keith Lazuka, Mahesh Murag; three-tier disclosure verbatim; "30–50 tokens" budget is NOT in S13; security stance is minimalist; Dec 18 2025 update — open standard at agentskills.io |
| S14 — Building a C compiler with parallel Claudes | ✅ Drained from `fetched/issue-29/` 2026-05-13 | Nicholas Carlini, Safeguards team, Feb 5 2026; all numbers verbatim; companion repo `anthropics/claudes-c-compiler`; GCC-as-oracle parallelism trick; clean-room + Doom litmus test newly surfaced |
| S15 — Harness design for long-running app development | ✅ Drained from `fetched/issue-29/` 2026-05-13 | Prithvi Rajasekaran, Anthropic Labs, Mar 24 2026; sprint contract pattern; context anxiety / context-resets discipline; v1→v2 (Opus 4.5→4.6) harness evolution with v2 dropping sprints; cost data primary |
| Claude Code sandboxing post (new §8) | ✅ Drained from `fetched/issue-29/` 2026-05-13 | David Dworken & Oliver Weller-Davies, Oct 20 2025; 84% permission-prompt reduction; bubblewrap + seatbelt; open-sourced as `anthropic-experimental/sandbox-runtime` |
| `anthropics/cwc-long-running-agents` | FULL | Related to S12 pattern but not the canonical S12 companion (correction this round) |
| `platform.claude.com/.../agent-skills/overview` | ✅ Drained via USER-PATH-B export 2026-05-13 (issue #36 extras) | Closes round-7 SPA-shell failure. Source of: SKILL.md schema constraints (64-char name, 1024-char description, reserved words "anthropic"/"claude" forbidden); the Level-1/2/3 token table (~100 / <5k / unlimited); API beta-header triplet; runtime-per-surface constraint matrix (claude.ai vs API vs Claude Code); cross-surface non-portability; and the §5 security-quotes re-anchoring (round-6 misattribution gap closed) |
| `support.claude.com/.../what-are-skills` (Help Center) | ✅ Drained via USER-PATH-B export 2026-05-13 (issue #36 extras) | Cross-product summary; plan availability (Free/Pro/Max/Team/Enterprise + Claude Code beta + API beta); four skill types (Anthropic / Custom / Org-Provisioned / Partner); confirms open-standard claim ("published as an open standard at agentskills.io ... reference Python SDK"); Projects-vs-Skills and MCP-vs-Skills disambiguation |
| Cookbook notebook 1 — `anthropics/claude-cookbooks/skills/notebooks/01_skills_introduction.ipynb` | ✅ Drained via USER-PATH-B export 2026-05-13 (issue #36 extras) | API surface (`client.beta.messages.create`, `container={"skills":[...]}`); beta-header triplet; xlsx/pptx/pdf pre-built skills; token-savings framing ("~98% on initial context"); the "MUST include code_execution tool" requirement |
| Cookbook notebook 2 — `02_skills_financial_applications.ipynb` | ✅ Drained via USER-PATH-B export 2026-05-13 (issue #36 extras) | Domain-specific worked example: xlsx → pptx → pdf pipeline pattern with structured-data flow; "Structured data (JSON/CSV) is more efficient than prose" authoring discipline; multi-document automated-reporting pipeline shape |
| Cookbook notebook 3 — `03_skills_custom_development.ipynb` | ✅ Drained via USER-PATH-B export 2026-05-13 (issue #36 extras) | Skills Management API (`beta.skills.create/list/versions.create/delete`); custom-skill directory layout; versioning model (epoch-timestamped, no rollback API); multi-skill composition in one `container` (custom brand + pre-built pptx); duplicate display_title constraint; authoring-side security checklist (no hardcoded creds, sanitize inputs, log usage); single-responsibility / under-5k-tokens authoring principles |

**Blocked URLs encountered:** previously four anthropic.com engineering URLs (S12, S13, S14, S15) returned 403. All now drained via issue #29 plus the sandboxing post.

**Fetch issue filed:** issue #29 (closed via this drain).

**Open follow-ups:**

1. ~~Fetch `platform.claude.com/docs/.../agent-skills/overview`~~ — **CLOSED 2026-05-13** by USER-PATH-B export (issue #36 extras). §5 security quotes are now anchored verbatim against the platform docs.
2. Lift §7 into [`02-compound-atelier`](../architectures/02-compound-atelier.md) — likely §3.4 (split Curator into inline check + periodic consolidation per CK) and §7 (three-tier disclosure per Anthropic).
3. The S15 sprint-contract pattern (file-based negotiation of "done" before code is written) deserves cross-reference into the architectures' phase-gate / AC-grounding design.
4. The S14 GCC-as-oracle pattern is a new architectural primitive worth capturing: "known-good oracle + bisect" as a way to enable parallelism on monolithic builds.
5. Track Agent Skills as open standard (agentskills.io) — verify the cross-vendor adoption status in a follow-up round. (Both the support doc and the platform docs now confirm open-standard status with a reference Python SDK; the adoption-side surface — *who* outside Anthropic has implemented the spec — remains unverified.)
6. **NEW (issue #36 extras drain):** Propagate to [`04-every-skill-libraries`](04-every-skill-libraries.md) next drain: (a) Anthropic's strict name constraints (64-char, lowercase-alphanumeric-hyphen, "anthropic"/"claude" forbidden); (b) the ~100/Skill metadata budget; (c) the cross-surface non-portability gap; (d) note that `allowed-tools` is a Claude Code extension, not part of the Anthropic canonical schema.
7. **NEW:** Cross-surface portability gap. Custom Skills don't sync across claude.ai / API / Claude Code. For any factory architecture proposing skills as the universal-knowledge primitive, this is a real friction — the same skill must be uploaded three times, and Claude-Code-Plugins is the only sharing mechanism that doesn't require manual re-upload.
8. **NEW:** API-surface no-network constraint is a structural defense. Worth folding into [`00-synthesis`](synthesis/00-synthesis.md) and the architectures' threat-model sections — for API-deployed agents, network exfiltration is *runtime-impossible*, which materially changes the trust calculus for partner/registry skills.

**Status:** SUCCESS — all five Anthropic engineering URLs drained via issue #29; major corrections applied to model versions, companion-repo attribution, testing tools, and quote sourcing. The three-way comparison with El Kaim's Codex and Every's Compound Knowledge plugin remains intact and is now anchored on primary S13 text. The sandboxing post is integrated as the security companion the trilogy was missing.
