# Klaassen's Chain-of-Thought Sibling Trilogy — Research Report

**Round-3 Thread 5** per [`PLAN`](../PLAN.md) §11.5. Extends [`03-every-compound-engineering`](../03-every-compound-engineering.md) with three sibling Every.to pieces that add (a) "spec authorship as meta-skill" framing, (b) fidelity-tiered research strategies for "senior-engineer thinking," and (c) the Opus 4.5 "world-changing shift" architectural argument.

**Date:** 2026-05-11 (originally drafted under fanout run 20260511-054258, sub-08; upgraded to primary-source-anchored 2026-05-11 under fanout run 20260511 sub-31 via `research/fetched/issue-23/`).

---

## Drain note (issue #23) — 2026-05-11 upgrade from snippets to primary sources

This report was originally **PARTIAL / snippet-anchored** because every.to had been Cloudflare-blocked (HTTP 403) from every fetch path the sandbox could reach. On 2026-05-11 the GitHub-Action-based fetcher (issue #23) successfully retrieved all three target articles despite the documented Cloudflare posture in `research/blocked-urls.md`. The report has been re-rebuilt against the primary text.

What changed at the claim level:

1. **Article 3 authorship corrected.** "How Every Is Harnessing the World-changing Shift of Opus 4.5" is bylined by **Katie Parrott** (staff writer; the camp write-up), not by Kieran Klaassen. Klaassen and Dan Shipper are the camp presenters; Parrott reports their demos and Q&A. The prior report mis-attributed it to Klaassen.
2. **Three fidelity tiers are defined in Article 1, not Article 2.** Article 2 reuses them as the index for its eight strategies; Article 1 ("Stop Coding") owns the canonical definitions and gives a worked example per tier. The prior report wired them to Article 2.
3. **The "eight planning strategies" claim survives but is only 2 strategies deep in primary source.** Article 2 paywalls after Strategy 2 ("Ground in best practices"); Strategy 3 ("Ground in your codebase") is named but body-locked. The paywall preview confirms strategies 3 and 4 (codebase grounding; turning git history into institutional memory), plus "the 4 other programming planning strategies." The "six unseen strategies" the brief asked us to hunt for are **still unseen** — they sit behind the Every paywall. Verifiable claim set narrows.
4. **The four-clause plan-prompt template is verbatim and intact.** Survey internal, survey local tooling, survey external best-practices, demand N approaches with tradeoffs. Locked down.
5. **The Figma → Puppeteer-diff chain is verbatim and intact**, with a small correction: the iteration target is "until they match," not "until pixel-perfect"; the pixel-perfect claim is the *result*, not the loop condition.
6. **The "vibe planning" / Fidelity-Three framework is now primary-sourced**, including the three-prototypes-with-ascending-difficulty worked example (real-time / simple cache / queue) — material the prior report had as "framework not visible; mark provisional."
7. **The /modify-plugin command is described but not formally specified.** Primary source explains *what it does* (work in two repos simultaneously while pattern-extending the plugin) but does not publish a spec, parameter list, or prompt body. The brief's request for "the /modify-plugin command spec" is partially fulfilled — usage is now firm, no spec sheet exists in the article.
8. **The "44 AI agents", "11 projects in six hours", and `/lfg` claims are NOT in the Opus 4.5 article and have been removed from §3.** Those came from Klaassen X posts the prior report cited indirectly; the article instead gives the figure of "10 projects at once" and references a `/work` command (not `/lfg`). Cross-article material is now tagged so.
9. **"The folder is the agent" framing is not in the Opus 4.5 article either** — it is attributed elsewhere ("The Folder Is the Agent" is a *separate* Every piece). Re-tagged accordingly.

**Corpus-level lesson — every.to is action-fetchable.** `research/unfetched-sources.md` flagged every.to with **"Defer to user — Path B only"** because direct WebFetch and Wayback both 403. The GitHub Action *succeeded* on three every.to article URLs, returning clean markdown renders (the in-body subscriber paywall on Article 2 is a CMS-level gate, not a Cloudflare block — the Action retrieved the same HTML a logged-out browser sees). **Action item:** demote every.to from "Defer to user" in `unfetched-sources.md`; re-test other every.to URLs through the Action path before manual cookie-fetch. The blocked-from-sandbox finding in `blocked-urls.md` still holds for the *sandbox*, but no longer for the *Action runner*.

---

## Sources covered

| URL | Author / date | Fetch status (2026-05-11) | Coverage |
|-----|---------------|---------------------------|----------|
| https://every.to/chain-of-thought/stop-coding-and-start-planning | Kieran Klaassen, Nov 6 2025 (updated Apr 7 2026) | ✅ Action-fetched, full text | Full article free; no paywall |
| https://every.to/chain-of-thought/teach-your-ai-to-think-like-a-senior-engineer | Kieran Klaassen, Nov 7 2025 (updated Mar 14 2026) | ⚠️ Action-fetched, **paywalled after Strategy 2** | Strategies 1–2 full; 3 named only; 4 named in paywall preview; 5–8 inaccessible without subscriber cookies |
| https://every.to/chain-of-thought/how-every-is-harnessing-the-world-changing-shift-of-opus-4-5 | **Katie Parrott** (camp write-up; Klaassen + Shipper as presenters), Dec 9 2025 | ✅ Action-fetched, full text | Full article free |

**Status: PRIMARY-SOURCE-ANCHORED (Articles 1 & 3); PARTIAL (Article 2, paywalled mid-list).**

---

## 1. "Stop Coding and Start Planning" — Klaassen, Nov 6 2025

### Thesis

> *"AI made us sloppy because it made us forget how to plan. Planning used to be a non-negotiable part of the work: sketching screens, prototyping flows, and writing problem statements."* — Klaassen, opening section

The reframing of planning from cost to leverage is explicit:

> *"One approach ships a feature. The other ships a feature and teaches the system how you think for next time. Get this right, and the system learns from every plan."* — §"How people actually use AI" (intro, paragraph 6)

### Spec authorship as meta-skill — the four-clause plan-prompt template

The vibe-vs-plan comparison Klaassen uses as the load-bearing primitive (intro, paragraph 5):

> *"When you vibe code, you prompt, 'Add email validation to the signup form,' and hope the AI takes the right route. When you plan with AI, you write: 'Research how we handle validation elsewhere in the codebase, check if our email library has built-in validation, look up best practices for user-friendly error messages, then create a plan showing three approaches with tradeoffs.'"*

Four clauses, verbatim from the article:

1. *"Research how we handle validation elsewhere in the codebase"* — survey internal patterns.
2. *"Check if our email library has built-in validation"* — survey local tooling.
3. *"Look up best practices for user-friendly error messages"* — survey external best-practices.
4. *"Then create a plan showing three approaches with tradeoffs"* — produce N alternatives with tradeoffs.

This is the most portable spec-authorship primitive in any Every article: it forces the AI to externalize judgment so the human can rule.

### The Figma → five-screens → Puppeteer-review worked example (§"Plans teach the system")

The launch context is **Cora's email bankruptcy feature** — *"a free service that clears users' inbox for them without deleting anything important."* Five Figma screens, designed by Lucas Crespo and Daniel Rodrigues. Klaassen's account of the chain (verbatim from the article):

> *"I created an AI agent with one job: Take a Figma design screenshot, analyze how to implement it, and output a detailed plan grounded in our patterns, components, and way of building."*

> *"Once the plan was complete, I added a second agent to review the work: Compare the Figma screenshot to what got built using Puppeteer, note every difference, and keep iterating until they match. Because the plan was clear and detailed, the review agent could focus entirely on execution, instead of trying to figure out what we were even building."*

Result, verbatim: *"I got five screens, pixel-perfect, including mobile layouts that were never even designed for."*

**Refutation note:** prior report stated the loop condition was "until pixel-perfect." Primary source is *"keep iterating until they match"* — i.e., until the Puppeteer screenshot matches the Figma screenshot. "Pixel-perfect" is the article's claim about the *outcome*, not the loop predicate. The loop terminates on diff-equality between two screenshots; pixel-perfection on unscoped surfaces (mobile) is reported as an emergent bonus.

The new primitive: **plan → build → visual-diff review → iterate** as a single chained unit. Three agents, one chain.

### Fidelity tiers — defined in this article (§"How to plan effectively: Remember the three fidelities")

The three tiers, verbatim names, with primary-source bullets:

**Fidelity One — "The quick fix":**
> *"This is the one-line change, the copy update, the obvious bug fix. A button that's the wrong color or a typo in an error message. Maybe a small bug where the fix is self-evident once you reproduce it."*

Notable F1 expansion claim: *"As models improve, 'quick fix' expands. With Claude Sonnet 4.5, Fidelity One work now includes: changing pricing across the entire codebase, normalizing emails automatically, reorganizing code to remove unused features, fixing tests that accidentally broke, updating libraries and migrating dependencies … Six months ago this was multi-hour work. Today, it's 10 minutes with a well-constructed plan."* — i.e., **fidelity is model-floor-relative**, the same task migrates downward in tier as models improve.

**Fidelity Two — "The sweet spot":**
> *"Features that span multiple files, require some refactoring, and have clear scope but non-obvious implementation. Things like: moving something performed inline … to a background job, adding a new tool call … or capability to the assistant (like archiving emails by query), or researching and reproducing bugs where you're not yet clear what the actual problem is."*

> *"For Fidelity Two work, planning yields massive return on investment. The problem is complex enough that AI might go off the rails without guidance, but simple enough that once you have a good plan, AI can execute it reliably. This is where I spend most of my planning energy, and where the system learns fastest."*

Klaassen's worked F2 example is the **archive-emails-by-query tool call** for Cora. Verbatim prompt he used: *"How do our existing tool calls work? What's our pattern for handling bulk operations? Are there any performance considerations with archiving many emails at once?"* The research surfaced that an existing search-interpretation tool could be reused, plus the Gmail-API quota constraint that would have caused production failures. Twenty minutes of research saved hours of production debugging — explicit return-on-investment framing.

**Fidelity Three — "The big uncertain":**
> *"Major features where you don't even know what you're building yet. Adding multi-account support. Rebuilding the high-level structure of how your code is organized. Integrating a complex third-party system. The requirements are epic, the scope is fuzzy, and no amount of planning will give you certainty because you're still figuring out what 'done' looks like."*

The plan-vs-prototype decision framework the brief asked us to hunt for is now visible — and named:

> *"For Fidelity Three, planning alone isn't enough. You need a hybrid approach: rapid prototyping to clarify what you want, and rigorous planning to build it properly. I call this **vibe planning** — vibe coding, but for disposable software that helps you think. Spin up quick prototypes in a separate environment, click through them, learn what breaks, throw them away, and plan the real implementation based on what you learned. The prototype is disposable; the knowledge isn't."*

The bulk-operations worked example (an F2 that escalated to F3) is the canonical primary-source demonstration:

> *"I stopped trying to plan the perfect solution and instead built three prototypes with ascending levels of difficulty: one with real-time API calls, one with a simple cache layer, one with a full queue system."*

Result: *"The real-time version choked on 1,000 emails. The simple cache had race conditions. The queue system was the only thing that worked. The prototypes convinced me that the complexity wasn't optional — the simple solutions would break."*

The decision framework:

> *"The goal with Fidelity Three is to break the project into multiple Fidelity Two pieces. You can't plan your way through genuine uncertainty. But at least you can prototype your way to clarity, then plan your way to quality from there."*

Encoded in factory terms: **F3 → prototype-grid in disposable environment → re-classify into N parallel F2 plans → execute F2 pipeline.**

### Compounding effect — how the system learns

Verbatim mechanism (§"How planning creates lasting knowledge"):

> *"Coding teaches, 'Here's how to solve this problem.' Planning teaches, 'Here's how to think about problems like this.'"*

> *"When Claude Code writes code based on your feedback, it learns the specific solution to one specific problem. The system creates plans, you react — 'This is too complex' or 'We need to sequence this differently' — and that feedback becomes permanent knowledge."*

Concrete codification example: *"When I first had the Figma agent implement designs, it used plain HTML, which I didn't want for a reusable design system. I corrected it: 'Use View Components instead — that's our component framework.' I codified that preference into the agent's instructions. Now every design implementation starts with View Components by default."*

Calibration claim (§"How planning creates lasting knowledge"): *"In week one of working this way, plans would come back with approaches I'd never take — over-engineered solutions, missing obvious existing patterns, forgetting security checks. **Three months in, plans come back largely reflecting how I'd approach the problem myself** not because I'm prompting better, but because **the system has learned from more than 50 plan reviews** how I think."*

Two model-floor primitives (§ closing): *"Better AI models make the system better. GPT-5 or Claude Sonnet 4.5 or whatever comes next will make better plans automatically. But your specific system gets better because you're accumulating institutional knowledge. Your agents know your preferences. Your research strategies know your domain. Your review process catches your common blind spots."*

Closing line: *"Planning is the highest-leverage activity in AI-assisted development. One hour spent improving your planning system makes every future hour more productive."*

The article ends with a pointer to Article 2: *"In the next piece, published tomorrow, I'll share eight strategies that you can use for more effective planning, plus an experiment that you can use to become a better planner."*

---

## 2. "Teach Your AI to Think Like a Senior Engineer" — Klaassen, Nov 7 2025

### Article-status caveat

The Every CMS paywalls after Strategy 2. Subscriber preview at the cutoff line confirms the eight-strategy structure but only names the next two ("stop reinventing solutions your codebase already has," "turning git history into institutional memory that prevents repeated mistakes") plus "the 4 other programming planning strategies." **Strategies 5–8 remain unfetched** — they sit behind a Every-account subscriber gate, not a Cloudflare block. The 2026-03-14 update date suggests Klaassen has revised the list at least once.

### Setup and thesis (intro, free)

The bulk-archive 53,000 emails example is shared with Article 1, retold to motivate planning:

> *"I asked the research agent to analyze our own bulk operation patterns, check API limits for mass actions, and propose three implementation approaches with tradeoffs. Twenty minutes later, it came back with a reality check: Gmail rate limits would kill us at 2,000 emails, our system would timeout on long operations, and the user would have to wait too long for the result. I thought it would be a quick feature, but it turned into a three-day architectural challenge."*

Operating model (§"The eight planning strategies"):

> *"When you're planning with AI, you're running parallel research operations — each one a specialized agent gathering different kinds of knowledge. Then you work together: The agents bring findings, you make decisions, and together you combine and distill everything into one coherent plan."*

> *"It's much faster for five agents to research in parallel than for a human to plan step by step. Your contribution to the process is taste, judgment, and context about what matters for your product and users."*

Fidelity reuse: *"I use eight research strategies, depending on the fidelity level, which refers to the degree of difficulty. Fidelity One is quick fixes … Fidelity Two covers features spanning multiple files … Fidelity Three covers major features where you don't even know what you're building yet."* — confirms the three tiers from Article 1 are the index for the strategy library.

### Strategy 1 — Reproduce and document (verbatim spec)

> **What it does:** Attempts to reproduce bugs or issues before planning fixes
> **When to use it:** Fidelity One and Two, especially bug fixes
> **The agent's job:** Create a step-by-step reproduction guide
> **Prompt:** *"Reproduce this bug, don't fix it, just gather all the logs and info you need."*

Worked example: the 19 stuck users after the Cora email-bankruptcy launch. Klaassen prompted Claude Code: *"Loop through the AppSignal logs and diagnose this."* Five minutes later: *"Rate limit errors were being swallowed in production. The job hit Gmail's limit, failed silently, and never resumed."* The reproduction showed the system needed **batch processing and job resumption, not just retries**.

Compounding move — Klaassen updated `@kieran-rails-reviewer` (a named code-review agent in his plugin) with the rule: *"For any background job that calls external APIs — does it handle rate limits? Does it retry? Does it leave users in partial states?"* — *"We forgot to retry once. The system won't let us forget again."*

### Strategy 2 — Ground in best practices (verbatim spec)

> **What it does:** Searches the web for how others solved similar problems
> **When to use it:** All fidelities, especially unfamiliar patterns
> **The agent's job:** Find and summarize relevant blog posts, documentation, and solutions
> **Agent:** `@agent-best-practices-researcher` (published in [every-marketplace](https://github.com/EveryInc/every-marketplace/blob/main/plugins/compounding-engineering/agents/best-practices-researcher.md))

Range of use cases the article lists verbatim: *"technical architecture, copywriting patterns, pricing research, or upgrade paths."* Non-technical uses include *"SaaS pricing tiers best practices … Email drip campaign conversion copy … Background job retry strategies."*

Worked example: a gem-upgrade two versions behind. Agent searched *"upgrade path from version X to Y," "breaking changes between versions," "common migration issues"* — found the official upgrade guide and three engineer blog posts. *"That research took three minutes and prevented hours of trial-and-error debugging."*

Compounding move: agent saves key findings to per-domain `docs/*.md` files in the repo (the article names `docs/pay-gem-upgrades.md` and `docs/pricing-research.md`). Next research run checks these first, then the web — local-cache-of-research as compound-engineering substrate.

### Strategies 3–8 — paywalled

Strategy 3's heading is visible: **"Ground in your codebase."** The preview lockup names Strategy 4 indirectly as *"turning git history into institutional memory that prevents repeated mistakes."* The remaining four are listed as *"the 4 other programming planning strategies that teach your AI how you think"* — no names, no specs.

**Hypothesis carryover from the prior snippet-anchored version** (still hypothetical pending direct fetch of the subscriber tier): given Klaassen's plugin agent roster in [`03-every-compound-engineering`](../03-every-compound-engineering.md), the remaining four likely include some of: framework-docs-researcher, repo-research-analyst, spec-flow-analyzer, learnings-researcher, issue-intelligence-analyst, session-historian, slack-researcher, web-researcher. None of those names appear in the article's free portion. Mark provisional.

### Persona shape that produces senior-engineer thinking (free portion)

Primary-source primitives from the free body, reusable as compound-atelier design rules:

1. **Parallel specialization, not one big-brain model.** *"Running multiple specialized research agents in parallel … helps prevent building the wrong solution entirely."* The article explicitly recommends *"five agents to research in parallel"* as the unit of work.
2. **GitHub-publication of agent definitions.** *"Look out for Github links throughout the article — I've added them so you can copy and adapt the exact agents and commands I use, rather than building everything from scratch."* Agent definitions live in `EveryInc/every-marketplace/plugins/compounding-engineering/agents/*.md`. The article *is* the README; the marketplace is the index.
3. **Reproduction-first as canonical F1/F2 entry point.** Strategy 1 isn't a debugger habit — it's the gating step before *any* fix planning begins.
4. **Compounding-the-checklist.** Every encountered class of bug updates a reviewer-agent's checklist; the reviewer's checklist becomes the system's institutional memory.

### Primitives this article adds beyond the canonical guide

- **Fidelity-tier-indexed strategy library.** Each strategy declares which fidelity tier(s) it applies to; planning becomes "tier first, then pick strategies."
- **Named domain knowledge files (`docs/*.md`) as research caches.** Local-first; web fallback.
- **Reviewer-agent self-extension.** When a class of bug recurs, the reviewer is updated, not the implementation. The plugin's *review surface area* compounds.

---

## 3. "How Every Is Harnessing the World-changing Shift of Opus 4.5" — Parrott (camp write-up), Dec 9 2025

### Attribution and authorship correction

The byline is **Katie Parrott** (Every staff writer; AI editorial lead). Klaassen and Dan Shipper are the *demoers* in the underlying Opus 4.5 Claude Code Camp the article reports on; Parrott summarizes their patterns, demos, and Q&A. **The prior version of this report attributed the article to Klaassen — fixed.** Cite this piece as Parrott reporting Klaassen/Shipper.

### The five key takeaways (verbatim, §"Key takeaways")

> 1. *"It finishes what it starts. Previous models spiral into errors three to four steps in. Opus keeps going — from idea to working app."*
> 2. *"It can fix problems in code you didn't write. Opus can modify the pre-written code your app uses … and trace bugs through all the code, frameworks, and dependencies that make your app work."*
> 3. *"It can test your app like a human would. Opus can test features end-to-end, find bugs, and generate before/after screenshots on its own."*
> 4. *"You can build apps by simply describing what you want. Your app calls an AI and tells it what to do — no traditional feature code required."*
> 5. *"Your brain is the bottleneck. The question is no longer 'Can the AI do this?' but 'Which of these 10 things should I build?'"*

### Two-axis shift (§"What makes Opus 4.5 an infinite coding machine?")

Parrott summarizes Shipper's framing: *"The shift has implications on two fronts: how you think about software (coding philosophy) and how you structure that software (code architecture)."*

**Coding philosophy** — *"depth and delegation."* Previous models hit an "error wall" three steps in; Opus *"kept going."* The bug-fixing-across-dependency-layers claim is concrete: *"Opus 4.5 can trace a bug through all three layers and fix it"* (your code → React → browser API). Delegation is enabled by *"multiple things in parallel, by delegating multiple tasks to the model at once."*

**Code architecture — agent-native apps.** Verbatim definition:

> *"Instead of coding recipes, you build a general-purpose agent (an AI that can use tools and follow instructions, similar to a chef that can follow recipes and cook) with access to tools, then give it prompts describing outcomes. The agent figures out the steps."*

Shipper's worked example — the reading-profile feature in his reading app — replaces a multi-step photo-pipeline-and-summarization algorithm with a single prompted agent call. The cost/speed tradeoffs are stated explicitly: *"Agent-native apps are more expensive — every feature costs more money to run because they consume costly compute resources, instead of just executing pre-written code — and slower, because the agent has to think. But model costs are dropping, and you don't have to go all in. Use agent-native architecture for exploration, then write common workflows into traditional code as patterns emerge."* — a hardening-when-stable migration pattern.

### Klaassen's three demoed patterns (§"What a senior engineer can do with it")

**Computer use for testing.** Klaassen uses **Playwright** (not Puppeteer — different article, different tool) for end-to-end testing. Verbatim demo prompt: *"Use Playwright to test this feature. Click through everything and make sure nothing is broken."* The behavior: *"The model booted up Chrome, navigated the interface, found a bug, went back to the code, fixed it, and continued testing. All on its own."*

The before/after-screenshot-on-PR pattern — verbatim: *"Every time he uses the `/work` command (which tells the AI to start building), Playwright captures screenshots of the user interface before and after the change, then adds them to the pull request. Code reviewers can see exactly what changed visually without running the code themselves."*

**The `/work` command is named here — not `/lfg`.** The prior version of this report claimed `/lfg` ("With Opus 4.5, end-to-end flows from idea to PR are actually working, with the /lfg command…"); that quote is **not in this article**. `/work` is what Parrott documents from the camp demo. The `/lfg` claim, if it exists, is from an X post or another article — flagged as unverified-in-this-source.

**Parallel delegation.** *"Within days of getting Opus 4.5 access, Kieran was building 10 things at the same time."* Verbatim contrast with prior models: *"Previous models would bleed context between tasks — they would take some information or instructions you used in one project and apply it in another, or lose track of details. Opus holds the thread on all of them, so the amount of work you are capable of is as much as you can hold in your head at one time."*

The **churn detection in 30 minutes** anecdote is exact and primary: a previously-stalled Cora feature *"to detect warning signs that a user is about to stop using the product."* Verbatim Klaassen-via-Parrott: *"Opus 4.5 finished it in 30 minutes. When it hit a small decision, it made a reasonable choice and kept building instead of stopping to ask."* — the "decision-making without prompting back" primitive.

**Meta-level work — `/modify-plugin`.** Verbatim primary-source description (full paragraph):

> *"Kieran was working on Every Board, a feedback tool the team is building internally, when he realized the compound engineering plugin needed a fourth research agent for design work. Usually, that would require him to stop what he was doing, open up the new tool's code in a different place, make changes, and go back to his original project — by which time he would have forgotten where he was in coding. Instead, he created a command called `/modify-plugin` that let the AI work on both things at once: the Every Board project and making changes to the compound engineering framework — the set of instructions that Kieran has built to define the four steps that make up his AI-powered coding workflow."*

> *"The model maintained what it knew about the design problems Kieran was hitting with the Every Board project, then switched to the codebase for the compound engineering workflow, which contains all of the rules and behaviors that make compound engineering work. It analyzed how the research agents were defined there and added a new agent that fit the pattern."*

Klaassen's quoted reaction: *"This is 4.5. This kind of work would have never been possible before without it becoming a complete mess."*

**What we actually know about `/modify-plugin` from primary source:**
- It is a Claude Code slash-command Klaassen created on his own machine.
- It lets a single Opus 4.5 session simultaneously modify the user's current project *and* the compound-engineering plugin that the session is using.
- It was triggered by Klaassen realizing he needed a fourth research agent (for design work) while building Every Board.
- The agent inspected the plugin's existing research-agent pattern, then extended it.

**What is NOT in primary source:** a published spec, parameter list, or prompt body. The brief asked for the `/modify-plugin` command spec; what exists is a description of usage. The "spec" the brief refers to may be in the [`EveryInc/compound-engineering-plugin`](https://github.com/EveryInc/compound-engineering-plugin) repo — out of scope for this report unless a future round drains that repo.

### Q&A primitives (§"The Q&A")

Worth lifting verbatim because the canonical guide doesn't carry these as quotes:

- **"Is planning still necessary with Opus?"** Klaassen: *"For exploratory work or personal projects, Opus is good enough that you can just start building. But if you're working on a team or building something complex, planning is more valuable than ever because Opus can execute much deeper, more sophisticated plans."* — i.e., model-floor improvement raises the *ceiling* of plan complexity, not just the floor of automation.
- **"How many projects at once?"** Klaassen: *"However many your brain can handle. That's the actual bottleneck now."* Shipper: *"Three to five substantial things feels manageable for me. Beyond that, I start losing track."* — empirically-supported human-bottleneck claim; not "44 agents."
- **"Fatigue?"** Klaassen: *"The fatigue isn't from the volume of work — the AI handles that. It's from switching between different ways of thinking about what you're asking the AI to do."* — context-switch as the binding constraint, not throughput.
- **"Skills?"** Klaassen: *"Skills are bundles of knowledge you can load to perform dedicated tasks. Instead of cramming everything into your Claude.md file, you create skills for specific technologies that trigger only when you need them."* — connects to Skill libraries thread ([`04-every-skill-libraries`](../04-every-skill-libraries.md)).

### What about "44 agents," "11 projects in six hours," `/lfg`, "folder is the agent"?

**Not in this article.** The prior version of this report attributed those four claims to "the Opus 4.5 article." Primary-source check:

- **"44 AI agents":** absent. Article gives "10 projects at once" and Shipper's "three to five substantial things."
- **"11 projects in six hours":** absent. Article gives "10 projects at once" without a duration bound.
- **`/lfg`:** absent. Article names `/work` and `/modify-plugin`.
- **"The folder is the agent":** absent from this article. There is a separately-titled Every piece *The Folder Is the Agent* (referenced in the prior version's Sources section); the claim belongs *there*, not in Parrott's Opus 4.5 piece.

All four claims removed from §3 below. They remain plausible (Klaassen's X posts and the *Folder Is the Agent* article are likely sources), but they should be attributed to those primary sources, not to this article.

### Model-floor argument (synthesized from the article's framing)

Parrott's framing supports the prior report's *"model-floor architecture"* synthesis, but doesn't use that phrase. What the article *does* claim (verbatim or paraphrased):

- *"Previous models were great for demos but would peter out when you tried to build something real — three steps in, they'd start hallucinating fixes and making the same errors over and over again. Opus doesn't hit that wall."* — the wall-vs-no-wall framing.
- *"Opus 4.5 has been out for three weeks. Already engineers are shipping prompt-native apps and parallel work is becoming the default. In another three weeks, we'll probably discover workflows that make today's look primitive."* — the floor-moves-the-architecture-moves framing.

The synthesis stands: **every compound-engineering architecture should declare a model floor.** Klaassen's compound-engineering plugin v2 is dated to Opus 4.5 by Parrott's account (*"This wouldn't have worked a week ago. Previous models would derail after the second parallel"* — paraphrased Klaassen quote referenced in §"Parallel delegation" framing; exact quote not present in this article either, may be from X). The two implications:

1. **Architecture variants pinned to model-class.** Don't ship one architecture — ship "this above this floor; this fallback below it."
2. **Re-validate when the floor moves.** Every new model release is a deliberate re-test of unattended-autonomy depth, parallel-lane count, agent-self-modification scope.

---

## Cross-article synthesis: three additions to compound engineering

1. **Spec authorship is the meta-skill** (Article 1). The spec teaches the system. Plan-prompts are higher-leverage than implementation prompts. The four-clause template — survey internal, survey local tooling, survey external best-practices, demand N approaches with tradeoffs — is the portable primitive. The three fidelity tiers (F1 quick-fix / F2 sweet-spot / F3 big-uncertain) and the **vibe-planning F3 escalation** (prototype-grid in disposable env → re-classify into N parallel F2s) are now primary-sourced.
2. **Fidelity-tier-indexed strategy library** (Article 2). Plan-entry triage by fidelity; strategy library indexed by tier. **Reproduction-first** is canonical for F1/F2 bugs (Strategy 1). **Web grounding with local cache** (`docs/*.md`) is all-fidelity (Strategy 2). Strategies 3–8 are paywalled; Strategy 3 is "ground in your codebase," Strategy 4 mentions git history. Mark the remainder unfetched.
3. **Model-floor architecture** (Article 3, partial primary-source support). Architectures should declare a model floor; above-floor capabilities include parallel-delegation (Klaassen, 10 projects), agent-native app architecture (Shipper), computer-use-for-testing (`/work` + Playwright), and agent-modifies-plugin during a feature build (`/modify-plugin`). Below-floor: degrade explicitly to the canonical three-lane setup.

Most actionable for [`02-compound-atelier`](../../architectures/02-compound-atelier.md): adopt **fidelity-tiering as plan-entry triage**, declare a **model-floor preamble**, and name **Strategy 1 (Reproduce and document)** + **Strategy 2 (Ground in best practices with local cache)** as table-stakes strategies in the planning rubric.

---

## Three concrete actions for Architecture 2

1. **Adopt fidelity-tier triage as the first step of `/plan`.** Before any research agents fan out, the orchestrator classifies the task as F1/F2/F3 against the article-1 definitions. F1 → lightweight reproduce-and-confirm; F2 → full 4-clause plan prompt and N-approaches-with-tradeoffs; F3 → enter vibe-planning mode, build three ascending-complexity prototypes in a disposable workspace, then re-classify into multiple F2 plans.
2. **Ship Strategy 1 and Strategy 2 as Day-1 agents.** Reproduction-first (write the failing reproduction before the plan) and best-practices grounding (with `docs/*.md` local cache that the next run consults first) are the two agents Klaassen has published openly. They are the floor of the strategy library; everything else can be drafted later. Cite [`every-marketplace`](https://github.com/EveryInc/every-marketplace) as the seed corpus.
3. **Declare a model-floor preamble in [`00-comparison`](../../architectures/00-comparison.md).** Each architecture states which model class it assumes (Opus 4.5+, Sonnet 4.5, etc.), and what degrades below the floor. The Compound Atelier should pin itself to Opus 4.5+ for the swarm modes and explicitly downgrade to ≤2 parallel lanes below that.

---

## Unfetched / open items (post-drain)

- **Article 2 Strategies 3–8.** Subscriber paywall; requires Every account cookies (or the cookie-fetch workflow used for prior Every drains). Strategy 3 = "Ground in your codebase"; Strategy 4 = git-history-as-institutional-memory; Strategies 5–8 unnamed.
- **Formal spec of `/modify-plugin`.** Article 3 describes usage, not spec. Likely in [`EveryInc/compound-engineering-plugin`](https://github.com/EveryInc/compound-engineering-plugin) repo source. Out of scope for issue #23.
- **"44 agents," "11 projects in six hours," `/lfg`, "folder is the agent."** Need to be sourced to the correct articles/posts (likely *The Folder Is the Agent*, *Opus 4.5 Collapsed Six Months of Development Work Into One Week*, and Klaassen's X feed). Three of the four were misattributed in the prior version of this report; corrections are above.
- **Klaassen X posts on Opus 4.5** (`status/1993054059520217395`, `status/2019482153541915097`) — still snippet-anchored.

---

## Suggested next actions

1. **Demote every.to from "Defer to user — Path B only" in `unfetched-sources.md`.** The GitHub Action successfully retrieves every.to article URLs. Re-test the other every.to URLs queued under that status before invoking the manual cookie-fetch workflow.
2. **Re-test every.to subscriber-only content.** The Action retrieves the same HTML a logged-out browser sees, so paywalled content stays paywalled. The cookie-fetch workflow is still the right path for paywalled Every content (Article 2 Strategies 3–8; the four already-drained Every articles); the Action is the right path for free Every content.
3. **Fold fidelity-tier triage and Strategies 1+2 into [`02-compound-atelier`](../../architectures/02-compound-atelier.md) §Workflows.**
4. **Add a model-floor preamble row to [`00-comparison`](../../architectures/00-comparison.md)** for all four candidate architectures.
5. **Open a follow-up issue to fetch the four still-paywalled Article 2 strategies** via the cookie-fetch path; track expected primitives (codebase grounding, git-history institutional memory, +4 unknowns).

---

## Sources

- [Stop Coding and Start Planning — Every](https://every.to/chain-of-thought/stop-coding-and-start-planning) — Kieran Klaassen, Nov 6 2025 (updated Apr 7 2026). **✅ Primary-source, full text.** Fetched 2026-05-11 via issue-23 Action.
- [Teach Your AI to Think Like a Senior Engineer — Every](https://every.to/chain-of-thought/teach-your-ai-to-think-like-a-senior-engineer) — Kieran Klaassen, Nov 7 2025 (updated Mar 14 2026). **⚠️ Primary-source, paywalled after Strategy 2.** Fetched 2026-05-11 via issue-23 Action.
- [How Every Is Harnessing the World-changing Shift of Opus 4.5 — Every](https://every.to/chain-of-thought/how-every-is-harnessing-the-world-changing-shift-of-opus-4-5) — **Katie Parrott** (camp write-up; Klaassen + Dan Shipper as presenters), Dec 9 2025. **✅ Primary-source, full text.** Fetched 2026-05-11 via issue-23 Action.
- [`EveryInc/every-marketplace` — best-practices-researcher](https://github.com/EveryInc/every-marketplace/blob/main/plugins/compounding-engineering/agents/best-practices-researcher.md) — referenced as the published agent for Article 2 Strategy 2.
- [`EveryInc/every-marketplace` — framework-docs-researcher](https://github.com/EveryInc/every-marketplace/blob/main/plugins/compounding-engineering/agents/framework-docs-researcher.md) — referenced in Strategy 2 worked example (gem-upgrade).
- [`EveryInc/compound-engineering-plugin`](https://github.com/EveryInc/compound-engineering-plugin) — Klaassen's plugin repo; likely source for `/modify-plugin` spec.
- Related Every pieces (not drained in this issue): [Compound Engineering: How Every Codes With Agents](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents), [Compound Engineering Guide](https://every.to/guides/compound-engineering), [Opus 4.5 Collapsed Six Months of Development Work Into One Week](https://every.to/chain-of-thought/opus-4-5-collapsed-six-months-of-development-work-into-one-week), [The Folder Is the Agent](https://every.to/source-code/the-folder-is-the-agent) — the last is the *likely* primary source for the "folder is the agent" / "44 agents" claims that were previously mis-attributed.
