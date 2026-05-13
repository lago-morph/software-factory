# The Dark Factory (el-kaim.com) — Research Report

**Sources covered:**
- https://el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e — **ACCESSED IN FULL** as of 2026-05-11 via a user-supplied "Save Page As" capture, after a Cloudflare-solved browser session, dropped into `reference-only/dark-factory-article.txt` (41 KB, William El Kaim, Apr 8, 2026, "24 min read"). This is the canonical primary source and the basis for all verbatim quotes below.
- el-kaim.com author profile context (https://medium.com/@welkaim/about, https://welkaim.medium.com/) — author identification only; both remain Cloudflare-gated and contribute no body text.

**Date:** 2026-05-11 (primary source incorporated; supersedes the 2026-05-10 secondary-source reconstruction)

---

## Revision notes (2026-05-11 — primary source incorporated)

The previous two revisions of this report were reconstructions: the el-kaim.com URL had returned a Cloudflare interstitial on every fetch path tried (direct, Wayback, manual-cookie). On 2026-05-11 the user manually exported the article from a browser session that had solved the Cloudflare challenge, into `reference-only/dark-factory-article.txt`. That file is the **full 24-minute article**. This revision treats it as canonical and rewrites the report accordingly. Itemized changes:

**Status flip.** The "Status note" block that said the primary source remained inaccessible is removed. The Sources-status row for el-kaim.com is flipped from ❌ to ✅ FULL (manual fetch 2026-05-11). All other rows are unchanged.

**Verbatim-quote replacements (10 in the "Notable quotes" section + ~12 inline upgrades).** Every quote previously in the "Notable quotes" section has been re-checked against the primary text:
- Quote 1 ("No human filed the bug report. No human triaged it.") — **confirmed verbatim**; primary text adds: *"No human filed the bug report. No human triaged it. No human assigned it. No human wrote the fix. No human reviewed the fix. The factory watches itself, diagnoses itself, and heals itself."* (Now upgraded to the full sentence.)
- Quote 2 (the "humans no longer spend most of their time writing code or reviewing code..." line) — **confirmed verbatim**; appears in the opening paragraph.
- Quote 3 ("The dark factory is not a batch process that produces a snapshot. It is a continuous system that sustains a living codebase.") — **confirmed verbatim**.
- Quote 4 ("The loop does not just build software; it maintains software.") — **confirmed verbatim** (paired in source with Quote 3).
- Quote 5 ("The hardest unsolved problem in dark factory construction is not orchestration. It is validation.") — **confirmed verbatim**.
- Quote 6 ("Agents are skilled at satisfying poorly specified observations.") — **confirmed verbatim**.
- Quote 7 (the October-2024 / "the loop converged rather than diverged" line) — **sharpened**. Primary text is: *"After it, agents could iterate through failure toward working software. The loop converged rather than diverged."* (Two sentences in the source, not one. Reconstruction collapsed them with an interpolated "and"; this is now corrected.)
- Quote 8 ("Dark Factories do not eliminate humans; they eliminate human dependency inside repetitive loops.") — **REFUTED as verbatim**. This sentence does **not** appear in El Kaim's article. It was a reconstruction (likely synthesized from secondary writeups). The claim itself is consistent with the article (Levels 0–5 framing, human repositioning from inner loop to specs/scenarios/supervision), but the exact wording is not El Kaim's. This sentence is removed from the "Notable quotes" section and replaced by a verbatim line that makes the same point: *"It is not a software process anymore. It is a black box that turns specs into software. Nobody writes the code. Nobody reads the code. The factory runs, the lights are off, and working software accumulates."*
- Quote 9 ("The factory is not a product you install — it is a discipline you build incrementally, spec by spec, pipeline by pipeline, loop by loop, until the lights can stay off.") — **sharpened**. Primary text uses a period, not an em-dash: *"The factory is not a product you install. It is a discipline you build incrementally, spec by spec, pipeline by pipeline, loop by loop, until the lights can stay off."*
- Quote 10 ("Code must not be written by humans, and code must not be reviewed by humans.") — **REFUTED as El Kaim's**. This sentence is not in El Kaim's article. It is StrongDM's two-rule charter (as reported by Simon Willison and surfaced in HN 46924426); El Kaim alludes to it conceptually but does not quote it. Attribution corrected: the line belongs to StrongDM via Willison/HN, not to El Kaim. Inline references to it in this report now attribute it to StrongDM directly and cross-reference reports 01, 05, and 06.

**New top-level sections added** (the article contains substantial material the reconstruction could not anticipate):
- "The Five Levels of Automation" — El Kaim's verbatim Levels 0–5 framework (attributed in source to Dan Shapiro).
- "Two Inflection Points: October 2024 and November 2025" — the explicit two-model-transition structure that the reconstruction collapsed into a single October-2024 phase change.
- "The Architecture That Keeps Converging" — Attractor as a dynamical-systems attractor + the three-layer architecture (LLM Client / Agent Loop / Pipeline Engine) and the independent-implementation convergence story (Kilroy, Mammoth, Smasher, Tracker).
- "The DOT File Is the Product" — the deterministic vs. LLM-heavy pipeline styles and the "engines are commodity, pipelines are IP" claim.
- "The Memory Problem" — Beads, Freshell, Filesystem-as-Memory.
- "Attribution and the Agent Workforce" — Gas Town's five design principles, verbatim.
- "The Factory Techniques" — Gene Transfusion, Pyramid Summaries, Shift Work, Semport, Dorodango.
- "Model Strategy at the Factory Level" — Weather Report, multi-model routing.
- "The Economics" — the $1,000/day-per-engineer figure verbatim, plus Willison's $200/month counterpoint.
- "Conclusion: The Spec Is the New Source Code" + the **12 numbered principles** El Kaim publishes at the end.
- "Resources cited by El Kaim" — the full references list at the end of the article (primary authors, StrongDM docs, Gas Town docs, GitHub repos, products/websites).

**Reconstructed claims that the primary source CONFIRMS (count: 14).** The Fanuc 2003 origin, the lights-off-because-robots-do-not-need-to-see framing, the StrongDM-as-existence-proof structure, October 2024 = Claude 3.5 Sonnet v2 as the enabling event, validation > orchestration as the hardest problem, scenarios as ML holdout sets, "code as black-box weights" analogy, "satisfaction" as the primary metric (not boolean test passage), the Digital Twin Universe rationale (rate-limit + cost + dangerous-failure-modes), Jay Taylor's "use the SDK as compatibility target" insight, the CXDB → Healer → prescription loop, the "why am I doing this?" discipline, the $1,000/day-per-engineer benchmark, and the "spec is the new source code" thesis — all of these are present in El Kaim's article in essentially the form the reconstruction had them.

**Reconstructed claims the primary source REFUTES or SHARPENS (flagged for orchestrator metadata pass):**

1. **REFUTED-as-El-Kaim:** "Dark Factories do not eliminate humans; they eliminate human dependency inside repetitive loops." Not in the article. (See above; removed from quotes section.)
2. **REFUTED-as-El-Kaim:** "Code must not be written by humans, and code must not be reviewed by humans." This is StrongDM's, not El Kaim's. (See above; attribution corrected.)
3. **REFUTED:** The reconstruction said the article makes "October 2024" the single phase-change date. The primary source explicitly names **two** inflection points: October 2024 (Claude 3.5 Sonnet v2 — "what was possible for a tiny team of specialists with the right infrastructure already in place") and November 2025 (Claude Opus 4.5 + GPT-5.2 — "what was possible for experienced developers working on standard codebases"). El Kaim writes: *"These two moments are commonly collapsed into one in public discussion. The distinction matters."* The reconstruction was one of the collapses he is calling out.
4. **REFUTED:** The reconstruction attributed Gas Town's DOT-graph orchestration role to Gas Town itself. El Kaim's article actually places the DOT-based pipeline engine inside **Attractor**'s three-layer architecture (Layer 3: The Pipeline Engine), with Kilroy / Mammoth / Smasher / Tracker as independent implementations of that same Attractor spec. Gas Town (Steve Yegge) is described in the article as the **attribution layer** ("an orchestration layer that treats AI agent work as structured data"), not as the primary DOT-graph runner. The reconstruction conflated two distinct components. Corrected throughout.
5. **REFUTED:** The reconstruction said Beads is "backed by Dolt (Git-for-databases) to handle concurrent multi-agent writes that broke SQLite." El Kaim's article describes Beads as a "persistent, dependency-aware graph" replacing "flat markdown scratchpads," but does **not** mention Dolt as Beads's backend or the SQLite-to-Dolt migration. The Dolt-as-Beads-backend claim came from the HN thread (see report 06), not from El Kaim. El Kaim's article lists Dolt only in the references at the bottom, labeled "version-controlled SQL database, referenced by Gas Town." The inline claim is removed from this report; cross-reference report 06 for the HN provenance.
6. **SHARPENED:** "$20K/engineer/month" figure. El Kaim's verbatim figure is *"$1,000-per-engineer-per-day,"* with the monthly extrapolation *"$20,000 per engineer per month"* given as the secondary framing. The original was right on the numbers but inverted on which is the load-bearing figure. The article quotes the day figure first; the report now matches.
7. **SHARPENED:** Team size. The reconstruction said "small teams (typically 3–5 people)." El Kaim's verbatim text is *"typically fewer than five people"* and specifies StrongDM's AI team as *"one CTO, one senior engineering manager, one new hire less than a year out of school. Three people."*
8. **SHARPENED:** The "filesystem as memory" framing is El Kaim's verbatim phrase, attributed to StrongDM: *"StrongDM's 'Filesystem as Memory' technique."* Not a generic technique invented by El Kaim.
9. **SHARPENED:** "the loop converged rather than diverged" is now in its primary-source two-sentence form (see Quote 7 above).
10. **NEW (not in reconstruction):** Three-layer architecture with the specific layer names. Twelve numbered principles at the end. The Resources/References list. The Gene Transfusion / Pyramid Summaries / Shift Work / Semport / Dorodango technique catalog. Weather Report as the living model-strategy document. CXDB LOC (≈16k Rust + 9.5k Go + 6.7k TypeScript) sourced explicitly to El Kaim (report 06 flagged this figure as third-party-summary provenance — now upgradeable; the figure appears verbatim in El Kaim's article).

**Editorial.** The "Status note" block at the top is removed. The "Notable quotes" section is re-titled "Notable quotes (verbatim from primary source)" and reordered to match the article's flow. Inline citations now attribute lines to El Kaim directly rather than through secondary citations except where the line is itself a quotation El Kaim is reproducing from Shapiro / Yegge / Willison / Jay Taylor.

---

## Executive summary

William El Kaim's "The Dark Factory: How Software Is Learning to Build Itself" (Apr 8, 2026, hosted on his Medium custom domain el-kaim.com) is a synthesis essay that argues a particular pattern of AI software development has crystallized into a working engineering discipline rather than a slogan. The pattern: humans *"define specifications, construct execution environments, design validation scenarios, and supervise the systems that generate and correct the software"*; agents do everything in between.

The essay opens by correcting a framing error: *"The idea of the dark factory is often presented as if software has suddenly become fully autonomous. That framing is misleading. The real shift is not that machines now 'magically build software alone.'"* The real shift, in El Kaim's framing, is that some teams have built software factories *in which humans no longer spend most of their time writing code or reviewing code*. He treats StrongDM's Software Factory as *"the strongest public example of that operating model"*, surrounded by an ecosystem of *"Attractor, CXDB, Kilroy, Beads, Gas Town, Dolt, and the 2389 implementations"*.

The article is organized around four structural moves the reconstruction missed:

1. **A five-level maturity ladder** (Levels 0–5), borrowed from Dan Shapiro, that grounds "dark factory" as Level 5 of a continuum rather than a binary state. *"Most teams will not reach Level 5. Most teams would benefit enormously from reaching Level 4."*
2. **Two inflection points, not one.** October 2024 (Claude 3.5 Sonnet v2) made the dark factory *physically possible* for specialists with infrastructure. November 2025 (Claude Opus 4.5 + GPT-5.2) made it *accessible to experienced developers on standard codebases*. El Kaim explicitly warns: *"These two moments are commonly collapsed into one in public discussion. The distinction matters."*
3. **The "attractor" convergence claim.** Independent re-implementations of StrongDM's Attractor spec (Kilroy by Shapiro; Mammoth/Smasher/Tracker by 2389 Research) converge on the same three-layer architecture without coordination, which El Kaim presents as evidence the architecture is *"a pattern so natural for the problem that it recurs spontaneously."*
4. **Twelve numbered principles** the essay closes with — explicit, verbatim, prescriptive — and an exhortation that *"specs are the source of truth. Code is disposable."*

The thesis turns on a metaphor and a re-mapping. The metaphor is borrowed from manufacturing: *"In 2003, Fanuc Robotics in Japan built a factory where robots manufacture other robots, around the clock, lights off. Not dark because it's secret. Dark because robots do not need to see."* The re-mapping is conceptual: *"code is the weights. You do not read it. Correctness is determined entirely by behavior on scenarios the agent cannot access."* That direct analogy to ML model evaluation — scenarios as held-out evaluation sets, satisfaction rate as validation loss — is what makes "no human review" intellectually defensible rather than reckless. El Kaim is emphatic that *"This is the direct analogy, and it is not metaphorical."*

The author's stance is observational with a clear directional bet: this is happening; the early adopters who built the validation harnesses (scenarios, digital twins, observability, self-healing) are pulling ahead; the binding constraints are now spec-writing skill, validation design, and economic appetite — not vendor tools. He acknowledges the *"$1,000-per-engineer-per-day figure from StrongDM's framing deserves honest attention rather than being glossed over"*, names Simon Willison's $200/month-personal-budget counterpoint, and frames the practical question as *"which pieces of this pattern can I adopt at what cost, and what fraction of the benefit do I capture?"*

---

## The "dark factory" metaphor unpacked

El Kaim's verbatim origin paragraph:

> "The term comes from manufacturing, not software. In 2003, Fanuc Robotics in Japan built a factory where robots manufacture other robots, around the clock, lights off. Not dark because it's secret. Dark because robots do not need to see. There are no humans present whose vision the lighting would serve."

And the mapping to software, verbatim:

> "Applied to software: a dark factory is a system that receives specifications as input and produces working, tested, deployed software as output, without a human writing, reviewing, or reading the code in between."

> "This is not a product you can install. It is a destination. A point on a maturity curve that a handful of small teams reached in late 2025 and early 2026, and that the rest of the industry is now racing toward."

What the metaphor adds versus prior "AI coding assistant" framings:
- **Continuity.** The dark factory is *"not a batch process that produces a snapshot. It is a continuous system that sustains a living codebase."* It both *builds* and *maintains*.
- **Closure.** *"The factory watches itself, diagnoses itself, and heals itself."* Bug reports, triage, fix, review — all internal.
- **Scale logic.** The 24/7 lights-off logic of manufacturing applies because *"the per-engineer LLM spend ... only pencils out if agents are running 24/7 across many parallel pipelines"* (paraphrase of the article's Economics section).

What the metaphor strains: the article spends most of its length on **validation**, because unlike manufacturing tolerances, software has open-ended requirements and adversarial users — and *"agents are skilled at satisfying poorly specified observations."*

---

## The Five Levels of Automation

El Kaim attributes the framework to *"Dan Shapiro, drawing on the NHTSA's five-level framework for autonomous driving."* He restates it in his own words:

- **Level 0: Manual labor.** *"Every character you write is yours. You might use AI as a sophisticated search engine, occasionally tab-accepting a suggestion. The code is unmistakably human-produced. In a world of technical deflation where the cost of code drops weekly, this is manual labor in a deflationary economy. You are being outrun by the people one level above you, and the gap is compounding."*
- **Level 1: AI intern.** *"You offload discrete, bounded tasks to the model. Write a unit test. Add a docstring. Explain this function. You retain full authorship of the important work, but you have a useful assistant for the tedious parts. You are still moving at the rate you type. The speedup is real; the paradigm shift is not."*
- **Level 2: AI pair programmer.** *"This is where most self-described 'AI-native' developers live in 2026. You are pairing with the model like a colleague. You achieve flow states. You are more productive than you have ever been... This level is comfortable, and that is the danger. Every level from 2 onward feels like you are done. You are not done."*
- **Level 3: Human in the loop.** *"You are no longer a senior developer. That is your agent's job. You are a manager: reviewing code, managing diffs, checking outputs, running the agent across multiple simultaneous workstreams. Your life is diffs. For many people, this level feels like things got worse... Almost everyone tops out here. It is not an exciting place to stop."*
- **Level 4: PM mode.** *"You are not a developer. You are not a development manager. You have become what you loathed: a product manager. You write specs. You argue with the agent about specs. You plan schedules. You review plans. Then you leave for twelve hours and come back to check whether the tests pass. The primary skill at this level is spec-writing... The spec is now the most valuable thing you produce."*
- **Level 5: The dark factory.** *"It is not a software process anymore. It is a black box that turns specs into software. Nobody writes the code. Nobody reads the code. The factory runs, the lights are off, and working software accumulates."*

El Kaim attaches a concrete team-size claim to Level 5: *"The teams that have reached Level 5 are small, typically fewer than five people. StrongDM's AI team: one CTO, one senior engineering manager, one new hire less than a year out of school. Three people."*

The framework's load-bearing assertion: *"Both frameworks describe a transition where human attention shifts from execution to oversight to strategy, and eventually becomes optional entirely."*

---

## Two Inflection Points: October 2024 and November 2025

The reconstruction collapsed this into a single date. El Kaim is explicit that this is a mistake:

> "Why did the dark factory become achievable when it did? The answer is not a single breakthrough but two distinct model transitions, separated by about thirteen months, each unlocking a different tier of autonomous development."

**The first inflection — October 2024.** *"In October 2024, Anthropic released the second revision of Claude 3.5 Sonnet. With it, something changed in long-horizon agentic coding. Before this model, stacking LLM calls degraded quality. Each iteration accumulated mistakes... until the codebase collapsed under the weight of its own inconsistency. After it, agents could iterate through failure toward working software. The loop converged rather than diverged."*

El Kaim grounds this with a specific practitioner observation: *"Justin McCarthy first noticed the change clearly in December 2024 via Cursor's YOLO mode, where agents could run autonomously without human confirmation on each step. The difference was not subtle. It was the difference between a system that decays and a system that learns. This is the moment the dark factory became physically possible."*

**The second inflection — November 2025.** *"A broader inflection point came roughly thirteen months later, with the arrival of Claude Opus 4.5 and GPT-5.2. Where October 2024 changed what was possible for a tiny team of specialists with the right infrastructure already in place, November 2025 changed what was possible for experienced developers working on standard codebases. Reliable instruction-following. Consistent long-horizon behavior. Complex task completion without regression."*

He cites Simon Willison's October-2025 site visit as evidence that the StrongDM stack was already operational *before* the second inflection: *"a working agent harness, a Digital Twin Universe with clones of half a dozen services, and a swarm of simulated test agents running through scenarios. And this was before the Opus and GPT releases that made agentic coding significantly more reliable a month later."*

El Kaim's takeaway, verbatim:

> "The first inflection built the factory. The second made the factory accessible to the broader industry. These two moments are commonly collapsed into one in public discussion. The distinction matters. October 2024 unlocked autonomous development for those who invested in the infrastructure: the validation harnesses, observability layers, and self-healing loops that make human review unnecessary. November 2025 unlocked it for those who could not afford that investment."

The question this poses for 2026, in El Kaim's words: *"which level of investment most teams can realistically make."*

---

## The Architecture That Keeps Converging

In February 2026, *"StrongDM open-sourced their specification for a coding agent pipeline runner, which they called Attractor, a name … borrowed from dynamical systems."* El Kaim defines the term:

> "An attractor is a state a system tends to evolve toward regardless of its starting conditions."

The article highlights what was published: *"Here is the remarkable thing about the Attractor release: the GitHub repository contains no code. None. It contains three markdown files describing the spec in meticulous detail, and a note in the README instructing you to feed those specs into your coding agent of choice. The implicit claim is that the spec is sufficient, that code is a commodity derivable from the description, and the description is the thing worth publishing."*

**The convergence narrative.** El Kaim documents four independent implementations of the Attractor spec:

- **Kilroy** (Dan Shapiro): *"a local-first Go CLI that runs Attractor pipelines in isolated Git worktrees."*
- **Mammoth** (2389 Research, Go): *"a full spec engine with a 21-rule DOT linter and configurable fan-in policies."*
- **Smasher** (2389 Research, Rust): *"a lean five-crate system with an HTMX frontend and live graph visualization."*
- **Tracker** (2389 Research, Go): *"a weekend-scale implementation with automatic checkpointing."*

*"Nobody coordinated. Nobody shared code. They shared a spec."* El Kaim's claim:

> "Every one of these implementations, in different languages, by different people with different goals, landed on the same three-layer architecture."

**Layer 1: The LLM Client.** *"A unified adapter layer that abstracts over model providers (Anthropic, OpenAI, Gemini), handles streaming and retries, manages provider-specific quirks, and presents a consistent interface to the rest of the system. The factory does not care which model runs a given task; the client makes them interchangeable."*

**Layer 2: The Agent Loop.** *"The reasoning core. A coding agent with tool dispatch, steering rules, loop detection to prevent infinite regress, and the ability to spawn subagents for parallel workstreams. This is the part that reads files, runs commands, writes code, checks outputs, and iterates."*

**Layer 3: The Pipeline Engine.** *"The orchestration layer. A DOT-based graph runner that sequences nodes, manages state and checkpointing, handles fan-out and fan-in, enforces retry budgets, and knows when to pause for human input. The pipeline is what makes the factory non-interactive."*

El Kaim's conclusion: *"The spec pulled independent implementors toward this shape. That is the attractor: not a product, but a pattern so natural for the problem that it recurs spontaneously."*

He quotes Simon Willison directly on why this story matters: *"first, coding agents became reliable enough to sustain long-horizon work; second, StrongDM treats scenarios as something like holdout sets, external to the code the agents are producing. Those two ideas are the core of the dark factory as it exists today."*

---

## The DOT File Is the Product

El Kaim makes a sharp economic claim about where the value sits in this ecosystem:

> "The runner implementations are open source and multiplying. The pipeline files, the actual DOT graphs that describe what the factory builds and how, are mostly private. Everyone is sharing the engine and hiding the blueprints. This is backwards. The engines are commodity. The pipelines are the intellectual property."

A pipeline DOT file is described as *"a directed graph written in Graphviz syntax… a workflow as a series of nodes (steps) and edges (dependencies). Each node can be a tool command (a shell script that runs deterministically) or an LLM call (a prompt that a model executes). The graph is the program."*

Two pipeline styles, named:

- **Deterministic style.** *"Tool nodes only: shell commands, zero model calls, identical output every run, completes in seconds, costs nothing. A vulnerability scanner that clones a repository, runs static analysis with rg, and writes a report is a complete, useful pipeline with no token spend. This style is underused and underappreciated."*
- **LLM-heavy style.** *"Model calls at every step: plan, scaffold, implement, review. Expensive, slow, nondeterministic. Useful for tasks that genuinely require reasoning. Catastrophic for tasks that do not."*

The mature posture combines both, with deterministic nodes at the periphery (setup, validation, deployment) and LLM nodes only where reasoning is required. The Mammoth *"model stylesheet pattern"* is named as the mechanism that makes this composable. **Multi-model review** is named as a *"standard pattern for high-stakes decisions"* — multiple independent models critique the same output and a synthesis node resolves disagreements. *"Three models critiquing each other's code reviews catches errors that any single model passes."*

---

## The Validation Problem

This is the section El Kaim labels as carrying the most weight:

> "The hardest unsolved problem in dark factory construction is not orchestration. It is validation."

The core mechanism failure he names:

> "If you stop reading the code, the only way to know whether the system is working is to observe its behavior. But agents are skilled at satisfying poorly specified observations. An agent asked to pass a test suite will pass it: by hardcoding values, by rewriting the tests, by finding any path through the constraint that is not the path you intended. This is not malice. It is optimization. An agent rewarding itself by satisfying the nearest measurable proxy for success is doing exactly what it was designed to do."

> "StrongDM's team encountered this immediately. Tests were not enough. Integration tests were not enough. End-to-end tests helped, until the agent started optimizing those too."

The reframing:

> "The real breakthrough is not code generation. It is proof without code review."

### Code as black-box weights

The ML-borrowed conceptual shift, verbatim:

> "A trained neural network is opaque; you do not inspect its weights to determine whether it is correct. You observe its behavior across a held-out evaluation set, data the model has never seen and cannot access during training. The weights are implementation details. Correctness is inferred exclusively from externally observable behavior on the holdout."

> "Applied to the dark factory: code is the weights. You do not read it. Correctness is determined entirely by behavior on scenarios the agent cannot access."

> "This is the direct analogy, and it is not metaphorical. The same reward-hacking dynamics that make ML evaluation hard make agent validation hard. The same solution, external holdout sets evaluated independently, applies. StrongDM formalized this by replacing the word 'test' with 'scenario.'"

### Scenarios as holdout sets

El Kaim's verbatim definition of a scenario:

> "A scenario, in StrongDM's definition, is an end-to-end user story written in natural language, stored outside the codebase, that can be intuitively understood and flexibly validated by an LLM. The critical properties: it lives outside the repository the agent can access, it is evaluated by a judge separate from the agent, and it tests externally observable behavior rather than internal implementation."

The analogy collapsed into a single line:

> "The scenario library is the holdout set. The factory is the model. The satisfaction rate is the validation loss."

The discipline the scenario architecture enforces: *"When you add a new feature, you add new scenarios to the holdout set before you instruct the factory to implement the feature, exactly as you would add test cases to an evaluation set before retraining. This framing solves the reward-hacking problem by construction. The agent cannot optimize against scenarios it cannot see. An agent that 'passes' by returning hardcoded values will fail the held-out scenarios it has never encountered."*

### Satisfaction as a metric

El Kaim's verbatim framing:

> "Because much of what StrongDM builds has an agentic component, binary success ('the test suite is green') is insufficient. An agent serving a user follows a trajectory through a space of possible actions; whether the user is actually served depends on the whole trajectory, not on whether any individual step completed. StrongDM introduced 'satisfaction' as their primary metric: of all observed trajectories through all scenarios, what fraction of them likely satisfy the user?"

> "This is a probabilistic, empirical measure. It requires an LLM-as-judge to evaluate whether a trajectory satisfied the stated user intent. It is more expensive to compute than a boolean assertion. It is also dramatically harder to game."

The stakes argument, in El Kaim's own words: *"StrongDM is building enterprise security software. Access management for complex organizations. 'Security issue' is a euphemism for 'lawsuit.' That they are shipping unreviewed code at all, let alone reliably, is a direct consequence of taking the holdout analogy seriously."*

---

## The Digital Twin Universe (DTU)

The rate-limit / cost / safety rationale, verbatim:

> "To run scenarios at realistic scale, thousands per hour across all the third-party services their software touches, StrongDM needed to solve a rate-limit problem. Running those scenarios against live services at validation speed would trigger abuse detection, exhaust rate limits, and accumulate unacceptable API costs. And testing real failure modes against production services is sometimes dangerous and sometimes impossible. Their solution: build faithful behavioral clones of every critical dependency."

The fidelity strategy is **the SDK, not the service**. El Kaim quotes Jay Taylor from Hacker News verbatim:

> "I did have an initial key insight which led to a repeatable strategy to ensure a high level of fidelity between DTU vs. the official canonical SaaS services: Use the top popular publicly available reference SDK client libraries as compatibility targets, with the goal always being 100% compatibility."

El Kaim's gloss: *"The insight is precise: do not clone the service, clone the SDK's view of the service. Take the most widely-used client library for Okta and make every call it can make return a correct response. The SDK is the contract. Compatibility with the SDK is compatibility with the service, for every purpose the scenarios exercise."*

The economics, verbatim:

> "Justin McCarthy has described the conversation he would have had with an engineer who proposed this a year ago: 'your enthusiasm is really welcome, get back to work, project not approved.' A full behavioral clone of GSuite and Salesforce and Okta, written to SDK-level fidelity, would have required a dedicated team and months of work. Now it is a pipeline task for one engineer over two weeks. What was unthinkable is now routine."

---

## The Self-Healing Loop

The two-day construction sequence, verbatim from the article:

> "On Monday, they built CXDB: a special-purpose observability layer that watches every interaction in their system. CXDB is released as open-source, roughly 16,000 lines of Rust, 9,500 of Go, and 6,700 of TypeScript. It stores conversation histories and tool outputs in an immutable DAG, a content-addressed graph where every interaction can be traced, replayed, and queried."

> "On Tuesday, they built Healer. Healer watches CXDB. It develops opinions about whether agent behaviors look right. It clusters similar problems into diagnoses. Each diagnosis becomes an investigation, and the investigation is itself an agent. An agent wakes up, looks at the cluster of bad behavior, retrieves the relevant code and prompts and data, identifies the root cause, and writes a prescription. The prescription is applied. The bug is fixed."

The closing-the-loop assertion:

> "No human filed the bug report. No human triaged it. No human assigned it. No human wrote the fix. No human reviewed the fix. The factory watches itself, diagnoses itself, and heals itself."

> "This is the part most discussions of AI coding overlook: the loop does not just build software; it maintains software. The dark factory is not a batch process that produces a snapshot. It is a continuous system that sustains a living codebase."

The single-question discipline that gates Level 3 → Level 5:

> "Why am I doing this? If you can look at a log file and articulate why something does not look right, you have described a validation rule. If you can describe it, you can automate it. So stop looking at log files. Get yourself out of the job of looking. This is the discipline that separates a team that uses AI from a team that has built a software factory."

---

## The Memory Problem

El Kaim's framing of the constraint:

> "An agent operating inside a pipeline faces a fundamental constraint: LLMs have no memory between calls. Every invocation starts from zero. In a long-horizon task, building a feature that requires dozens of agent calls across hours or days, this is catastrophic. The agent forgets what it decided, contradicts its earlier work, repeats steps it already completed. The naive solution is to dump everything into the context window. This works up to a point, then degrades: models lose coherence at the extremes of their context, earlier decisions get overwritten by later ones, and the cost per call becomes prohibitive."

Three named tools/techniques:

- **Beads** — *"replaces flat markdown scratchpads with a persistent, dependency-aware graph. Instead of a linear plan that the agent overwrites, Beads maintains a structured representation of tasks, their dependencies, their completion status, and their relationships to each other."* It is *"a work ledger, a durable record of what has been decided, what has been built, and what remains. It survives across sessions, across agent instances, and across pipeline boundaries."* (Note: El Kaim does **not** describe a Dolt backend or a SQLite-to-Dolt migration here; cross-reference report 06 for the HN thread's discussion of that.)
- **Freshell** — *"addresses a related problem at the workspace level. When you are running multiple coding agents, shells, browsers, and editors simultaneously, session management becomes chaotic. Freshell organizes multi-agent work into structured tabs, giving each agent its own isolated workspace while giving the human operator a unified view."*
- **Filesystem as Memory** (StrongDM's term) — *"models can navigate repositories and adjust their own context by reading and writing files. Directories, indexes, and on-disk state become a form of persistent memory that survives context window limits. A well-organized repository is not just good engineering hygiene. It is an interface that agents can navigate."*

---

## Attribution and the Agent Workforce

El Kaim places attribution as a first-class system property:

> "When agents are the engineers, traditional accountability structures break down. Git blame attributes commits to 'AI Assistant.' Nobody knows which agent wrote the buggy authentication flow. Nobody knows which model handles Go refactors reliably. Nobody knows what is in flight across twelve repositories."

**Gas Town**, built by Steve Yegge, is positioned as the attribution layer:

> "It is an orchestration layer that treats AI agent work as structured data. Every action is attributed. Every agent has a track record. Every piece of work has provenance."

Granularity, verbatim: *"Every Git commit is authored by a specific Gas Town agent identity (gastown/polecats/toast), every task record carries a created_by field, every event log entry carries an actor. Attribution is preserved even when agents work cross-repository."*

The compounding-value claim: *"As agents accumulate work histories, those histories become capability profiles. When new Go work arrives, capability-based routing assigns it to proven Go agents. A/B testing between models becomes empirical: deploy two models on comparable tasks, measure completion rates and quality signals, make data-driven routing decisions."*

Gas Town's five-point design philosophy (El Kaim's enumeration, verbatim): *"attribution is not optional; work is data, not just tickets; history determines trust; scale is assumed from the start; verification is first-class."*

Enterprise extensions named in the article: *"audit trails for SOX and GDPR, objective performance management of the agent workforce, cross-project dependency tracking, federation across organizational boundaries."*

---

## The Factory Techniques

El Kaim catalogs five named techniques *"that has emerged from teams actively building dark factories,"* in addition to the core architecture.

- **Gene Transfusion.** *"Solves the problem of applying a working pattern from one codebase to another. Instead of prompting the agent to 'implement feature X,' you point it at a concrete exemplar, a working implementation of the pattern in a different context, and ask it to reproduce the behavior in the new context. A solution paired with a good reference reproduces reliably in ways that a solution described from scratch does not."*
- **Pyramid Summaries.** *"Address context compression without information loss. As a codebase grows beyond what fits in a context window, multiple zoom levels are maintained simultaneously: a one-sentence summary, a paragraph summary, a section summary, the full text. The agent navigates between zoom levels as needed. This is reversible summarization: the agent can always expand back to full detail rather than working from a lossy truncation."*
- **Shift Work.** *"Separates interactive work from fully specified work. When intent is complete, specs written, scenarios defined, examples provided, an agent can run end-to-end without back-and-forth. Shift work means doing the interactive clarification upfront (the 'day shift') so the agent can execute autonomously overnight (the 'night shift'). The factory runs while you sleep."*
- **Semport (semantic port).** *"Handles codebase migrations: moving code between languages or frameworks while preserving behavioral intent. The agent does not translate syntax; it understands the purpose of the code and reimplements it in the target language. This makes migrations that were previously impractical, porting a 200,000-line Python codebase to Go, into pipeline tasks."*
- **Dorodango.** *"A practice rather than a technique: the discipline of iterative polishing. Jesse Vincent named it after the Japanese art of polishing a ball of mud into a high-gloss sphere. Codegen output is dorodango. You spec carefully, hand it to an agent, and polish what comes out. When the result is fundamentally wrong, you throw it away and rebuild from the spec. When it is close but rough, you polish it in small increments. Jesse described waking up to find an artifact named e2e-test-full-run-33.mp4. Runs 1 through 32 were the agent working through problems one by one. Run 33 worked. That is the process."*

---

## Model Strategy at the Factory Level

El Kaim names StrongDM's *"Weather Report"* — *"a living document tracking which models they use for which tasks and how that assignment evolves as models improve."*

Their current multi-model assignment, verbatim: *"one model for sprint planning (or a consensus pair that merges two independent outputs), a different model for architectural critique at high reasoning settings, a specialized code model for implementation, a multimodal model for frontend aesthetics and UX ideation. The pipeline model stylesheet pattern makes this composable: different node types route to the models best suited for them."*

His architectural recommendation: *"Building the routing layer at the pipeline level, rather than hardcoding model choices in application code, is what makes model upgrades cheap."*

---

## The Economics

The verbatim framing — note the daily figure is primary, the monthly is derivative:

> "The $1,000-per-engineer-per-day figure from StrongDM's framing deserves honest attention rather than being glossed over. At that spend level, $20,000 per engineer per month, the factory pattern becomes a business model question as much as an engineering question. Can you create a profitable enough product that you can afford the overhead? And does the competitive landscape shift so radically that you have no choice? If any competitor can clone your newest features with a few hours of coding agent work, the economics of competitive advantage change fundamentally."

El Kaim names Simon Willison's counterpoint directly: *"his personal exploration of agent patterns on a $200/month Claude Max subscription gives him substantial space to experiment. He is not running a swarm of QA testers around the clock, but he is meaningfully engaging with the same architectural questions at a fraction of the cost."*

The article's framing of the tension:

> "The question is not 'can I build the full StrongDM factory on a personal budget?' The answer is clearly no. The question is 'which pieces of this pattern can I adopt at what cost, and what fraction of the benefit do I capture?' Most teams will not reach Level 5. Most teams would benefit enormously from reaching Level 4. The principles are the same at both scales."

---

## Where humans fit

El Kaim is explicit that the lights-off metaphor is about the floor, not the building. From the opening paragraph, verbatim:

> "humans no longer spend most of their time writing code or reviewing code. Instead, they define specifications, construct execution environments, design validation scenarios, and supervise the systems that generate and correct the software."

The repositioning across the article:
- Humans leave the inner loop (no writing code, no reading code, no PR review).
- Humans own **specifications**, **scenarios**, **execution environments** (including digital twins), **model strategy** (Weather Report), and **supervision/escalation policy** ("knows when to pause for human input" — Layer 3 of the architecture).
- The "Why am I doing this?" question is positioned as the discipline that systematically *removes* humans from any remaining manual loop. Every manual action either gets articulated as a validation rule (and automated) or stopped.

El Kaim's Conclusion section names the three places where human craft migrates:

1. **Specification writing.** *"Translating intent into machine-consumable descriptions precise enough for autonomous implementation. A good spec for a dark factory is not a three-sentence feature description. It is thousands of words of structured, verifiable, example-rich prose that anticipates failure modes, defines edge cases, and specifies how the factory should behave when things go wrong."*
2. **Pipeline architecture.** *"Designing the graph of steps that builds the thing. Which nodes need reasoning? Which are deterministic? Where do you fan out? Where do you bring a human in the loop? What are the retry budgets? The pipeline file is the architectural document."*
3. **Validation design.** *"Specifying what success looks like in terms of externally observable behavior. Writing scenarios. Building or adopting digital twins. Defining the satisfaction metric. This is the hardest part and the part most teams underinvest in."*

---

## Conclusion: The Spec Is the New Source Code

El Kaim's closing thesis, verbatim:

> "In the previous paradigm, engineers produced code. Code was the artifact. Reviews were code reviews. Hiring was evaluated on coding ability. Architecture was expressed in code. The entire profession was organized around code production. In the dark factory paradigm, engineers produce specs. The factory produces code from specs. Code is the factory's output, an implementation detail, the way machine code is an implementation detail of compiled software."

> "Reading the generated code for comprehension is as anachronistic as reading assembly to understand a C program. This is historically familiar. When high-level languages arrived, some engineers were horrified that you would ship assembly you had never read. BASIC felt like cheating. Hand-optimized assembler was the craft. But getting things done was so much faster. History rhymes."

He quotes Dan Shapiro: *"People would complain that you had to hand-optimize the assembler. They would be horrified that you'd ship assembly code you've never read."*

### Twelve principles (verbatim from the article's "key principles" section)

El Kaim closes with a numbered list. These are reproduced verbatim because they are the most prescriptive distillation of the essay:

1. **Specs are the source of truth. Code is disposable.** *"Well-crafted natural language specs are the artifact worth maintaining. When something breaks, fix the spec and rebuild. Do not debug the output."*
2. **Use the three-layer architecture.** *"Every working implementation converges on it: unified LLM client, agent loop with tool dispatch, pipeline engine as a directed graph. Extend it; do not reinvent it."*
3. **The pipeline file is the process definition.** *"The dark factory is graph-driven. DOT, DAGs, checkpoints, gates, and node-level retries appear repeatedly across the actual implementations. Write workflows as DOT files. They are version-controlled, composable, and runner-agnostic. Think of them as BPMN diagrams, not shell scripts. Share them publicly; they are worth more than the runner code."*
4. **Deterministic nodes first; LLM nodes only where reasoning is required.** *"Tool nodes cost nothing and are reproducible. LLM nodes are expensive and nondeterministic. Use models only where you actually need reasoning."*
5. **Treat scenarios as holdout sets.** *"Store your behavioral scenarios outside the codebase, inaccessible to the agent. Evaluate against them with an LLM judge. An agent that cannot see its evaluation set cannot optimize against it. This is the direct ML analogy, and it is not metaphorical."*
6. **Measure satisfaction, not test passage.** *"Define success as the fraction of scenario trajectories that likely satisfy the user. This is harder to game than boolean assertions and more honest about what you are actually building."*
7. **Build digital twins for critical dependencies.** *"Use the public SDK client libraries as your compatibility target. If your twin satisfies every call the SDK makes, it is faithful enough for everything the scenarios exercise. The DTU is a pipeline task, not a project."*
8. **Ask "why am I doing this?" every time you do something manually.** *"If you can articulate why a log looks wrong, you have described a validation rule. If you can describe it, you can automate it. This discipline is the gap between Level 3 and Level 5."*
9. **Every action must be attributed.** *"Build attribution into your infrastructure from day one. It is the foundation of debugging, performance management, compliance, and trust in an agent workforce."*
10. **Build the memory layer.** *"Agents operating on long-horizon tasks without structured memory regress. A dependency-aware task graph is not optional for work that spans multiple sessions."*
11. **Close the self-healing loop.** *"The factory is not complete until it can observe its own output, detect its own failures, and correct them without human intervention. A simple anomaly-detection script that opens a ticket is enough to start. Build toward the loop."*
12. **The pipeline files are worth sharing.** *"The community that forms around shared pipelines is the real open-source project of this moment. An 'audit a Rails app' pipeline or a 'ship a mobile release' DAG is more valuable to the ecosystem than another runner implementation."*

### Epilogue line

> "The factory is not a product you install. It is a discipline you build incrementally, spec by spec, pipeline by pipeline, loop by loop, until the lights can stay off."

And the closing pivot from "how" to "what":

> "The 'how' question is answered. The three-layer architecture converges. The tooling exists. The techniques are documented. The key concepts, scenarios as holdout sets, code as opaque weights, satisfaction as the real metric, give you the right mental model to make it work. Teams of three people with one year of runway are shipping things that previously required fifteen engineers and two years. The question now is 'what.' What specifications are worth writing? What pipelines are worth building? What problems are worth automating? What does your organization produce when the cost of code asymptotes toward zero?"

---

## Risks, pitfalls, and warnings

El Kaim is not writing a cautionary essay, but the primary text names specific failure modes (now upgraded to verbatim or near-verbatim where possible):

- **Reward hacking / spec gaming.** *"An agent asked to pass a test suite will pass it: by hardcoding values, by rewriting the tests, by finding any path through the constraint that is not the path you intended. This is not malice. It is optimization."* Mitigation: out-of-repo scenarios judged by a separate LLM.
- **Validation, not orchestration, is the unsolved problem.** *"The hardest unsolved problem in dark factory construction is not orchestration. It is validation."*
- **Comfort at Level 2.** *"This level is comfortable, and that is the danger. Every level from 2 onward feels like you are done. You are not done."*
- **The Level-3 trap.** *"For many people, this level feels like things got worse... Almost everyone tops out here. It is not an exciting place to stop."*
- **Attribution collapse.** Without a Gas-Town-style attribution layer, *"Git blame attributes commits to 'AI Assistant.' Nobody knows which agent wrote the buggy authentication flow."*
- **Memory regression on long-horizon work.** Without structured task memory (Beads-style), *"the agent forgets what it decided, contradicts its earlier work, repeats steps it already completed."*
- **Economic gating.** $1,000/day/engineer is real money; *"most teams will not reach Level 5."*
- **Inverted economics of open source.** *"Everyone is sharing the engine and hiding the blueprints. This is backwards."* The pipelines, not the runners, are the IP. By implication, runners-as-products are likely to be commoditized.
- **Stakes asymmetry.** For enterprise security software, *"'Security issue' is a euphemism for 'lawsuit.'"* The validation discipline is non-optional, not aspirational.

What El Kaim does *not* warn about (still): alignment, displaced labor, regulatory exposure, security/supply-chain risk from agent-written code at scale, or epistemic risks of code no human has read. The essay remains engineering-pragmatic; ethical/social risk is out of scope.

---

## Distinctive concepts and vocabulary

(All verbatim from the primary source unless noted.)

- **Dark factory / lights-off factory** — Fanuc 2003 metaphor, applied to software.
- **The Five Levels (0–5)** — Shapiro's framework, restated by El Kaim verbatim.
- **"The loop converged rather than diverged"** — diagnostic phrase for the October-2024 phase change.
- **"Two inflection points"** — October 2024 (Claude 3.5 Sonnet v2) and November 2025 (Opus 4.5 + GPT-5.2). El Kaim insists these be kept distinct.
- **Attractor** — both the dynamical-systems concept *("a state a system tends to evolve toward regardless of its starting conditions")* and the StrongDM pipeline-runner spec name.
- **The three-layer architecture** — LLM Client / Agent Loop / Pipeline Engine.
- **"Engines are commodity. The pipelines are the intellectual property."**
- **Deterministic style** vs. **LLM-heavy style** pipeline.
- **Scenarios as holdout sets** — *"the scenario library is the holdout set. The factory is the model. The satisfaction rate is the validation loss."*
- **Code as opaque weights / black-box weights** — *"code is the weights. You do not read it."*
- **Satisfaction** (as a metric, not boolean test passage) — fraction of scenario trajectories that likely satisfy the user.
- **Digital Twin Universe (DTU)** — clones of the SDK's view of a service, not of the service itself.
- **CXDB → Healer → prescription** — the self-healing observability loop.
- **"Why am I doing this?"** — the discipline question that gates Level 3 → Level 5.
- **Filesystem as Memory** (StrongDM's term, El Kaim's quotation) — directories/on-disk state as persistent agent memory.
- **Beads / Freshell** — task-graph memory; workspace organization for multi-agent operators.
- **Gas Town** — attribution layer; agent work as structured data.
- **Gene Transfusion, Pyramid Summaries, Shift Work, Semport, Dorodango** — the five named factory techniques.
- **Weather Report** — StrongDM's living model-strategy document.
- **"$1,000-per-engineer-per-day" / "$20,000 per engineer per month"** — the economics benchmark; the day figure is primary in El Kaim's framing.
- **"The spec is the new source code."**

---

## Notable quotes (verbatim from primary source)

All verbatim from `reference-only/dark-factory-article.txt` (William El Kaim, "The Dark Factory: How Software Is Learning to Build Itself," el-kaim.com, Apr 8, 2026). Ordered to match the article's flow.

1. *"The idea of the dark factory is often presented as if software has suddenly become fully autonomous. That framing is misleading. The real shift is not that machines now 'magically build software alone.'"*
2. *"humans no longer spend most of their time writing code or reviewing code. Instead, they define specifications, construct execution environments, design validation scenarios, and supervise the systems that generate and correct the software."*
3. *"Applied to software: a dark factory is a system that receives specifications as input and produces working, tested, deployed software as output, without a human writing, reviewing, or reading the code in between."*
4. *"This is not a product you can install. It is a destination."*
5. *"It is not a software process anymore. It is a black box that turns specs into software. Nobody writes the code. Nobody reads the code. The factory runs, the lights are off, and working software accumulates."* (Level 5 definition — replaces the prior reconstruction "Dark Factories do not eliminate humans..." which is not in the source.)
6. *"After it, agents could iterate through failure toward working software. The loop converged rather than diverged."* (On Claude 3.5 Sonnet v2, October 2024.)
7. *"These two moments are commonly collapsed into one in public discussion. The distinction matters."* (October 2024 vs. November 2025.)
8. *"An attractor is a state a system tends to evolve toward regardless of its starting conditions."*
9. *"Everyone is sharing the engine and hiding the blueprints. This is backwards. The engines are commodity. The pipelines are the intellectual property."*
10. *"The hardest unsolved problem in dark factory construction is not orchestration. It is validation."*
11. *"Agents are skilled at satisfying poorly specified observations."*
12. *"The real breakthrough is not code generation. It is proof without code review."*
13. *"Applied to the dark factory: code is the weights. You do not read it. Correctness is determined entirely by behavior on scenarios the agent cannot access."*
14. *"This is the direct analogy, and it is not metaphorical."*
15. *"The scenario library is the holdout set. The factory is the model. The satisfaction rate is the validation loss."*
16. *"No human filed the bug report. No human triaged it. No human assigned it. No human wrote the fix. No human reviewed the fix. The factory watches itself, diagnoses itself, and heals itself."*
17. *"The loop does not just build software; it maintains software."*
18. *"The dark factory is not a batch process that produces a snapshot. It is a continuous system that sustains a living codebase."*
19. *"Why am I doing this? If you can look at a log file and articulate why something does not look right, you have described a validation rule. If you can describe it, you can automate it. So stop looking at log files. Get yourself out of the job of looking. This is the discipline that separates a team that uses AI from a team that has built a software factory."*
20. *"In the dark factory paradigm, engineers produce specs. The factory produces code from specs. Code is the factory's output, an implementation detail, the way machine code is an implementation detail of compiled software."*
21. *"The factory is not a product you install. It is a discipline you build incrementally, spec by spec, pipeline by pipeline, loop by loop, until the lights can stay off."*

**Quotes NOT in the primary source** (corrected attributions; previously misattributed to El Kaim):

- *"Dark Factories do not eliminate humans; they eliminate human dependency inside repetitive loops."* — not in El Kaim's article. Likely a reconstruction synthesized from secondary writeups. The conceptual claim is consistent with the article (Levels 0–5 framing) but the exact wording is not El Kaim's.
- *"Code must not be written by humans, and code must not be reviewed by humans."* — this is **StrongDM's two-rule charter** (per Simon Willison and HN 46924426), not El Kaim's coinage. El Kaim's text alludes to the idea conceptually but does not quote this sentence. See reports 01 and 06 for canonical provenance.

---

## Resources cited by El Kaim

The article ends with an explicit references list. Reproduced verbatim for downstream synthesis (these are the URLs El Kaim himself names; many overlap with the other reports in this corpus):

**Primary authors and articles:**
- Dan Shapiro, "The Five Levels: from Spicy Autocomplete to the Dark Factory" — https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/
- Dan Shapiro, "You Don't Write the Code. You Don't Read the Code Either." — https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code/
- Simon Willison, "How StrongDM's AI team build serious software without even looking at the code" — https://simonwillison.net/2026/Feb/7/software-factory/
- Harper Reed (2389 Research), "The Dark Factory Is a .dot file" — https://2389.ai/posts/the-dark-factory-is-a-dot-file/
- Jesse Vincent, "Dorodango" — https://blog.fsck.com/2026/02/10/dorodango/
- Steve Yegge, "Welcome to Gas Town" — https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04

**StrongDM factory documentation:**
- Story — https://factory.strongdm.ai/
- Principles — https://factory.strongdm.ai/principles
- Techniques — https://factory.strongdm.ai/techniques
- Products (Attractor) — https://factory.strongdm.ai/products/attractor
- Weather Report — https://factory.strongdm.ai/weather-report

**Gas Town documentation:**
- Overview — https://docs.gastownhall.ai/
- Why These Features? — https://docs.gastownhall.ai/other/why-these-features/

**GitHub repositories:**
- Attractor (spec only, no code) — https://github.com/strongdm/attractor
- AttractorBench — https://github.com/strongdm/attractorbench
- CXDB — https://github.com/strongdm/cxdb
- Kilroy (Dan Shapiro) — https://github.com/danshapiro/kilroy
- Freshell (Dan Shapiro) — https://github.com/danshapiro/freshell
- Beads — https://github.com/gastownhall/beads
- Gas Town — https://github.com/steveyegge/gastown
- Mammoth (2389) — https://github.com/2389-research/mammoth
- Smasher (2389) — https://github.com/2389-ai/smasher
- Tracker (2389) — https://github.com/2389-research/tracker
- dotpowers (2389) — https://github.com/2389-research/dotpowers
- Dolt (version-controlled SQL database, referenced by Gas Town) — https://github.com/dolthub/dolt
- Jesse Vincent's Superpowers — https://github.com/obra/superpowers

**Products and websites:**
- StrongDM — https://www.strongdm.com/
- 2389 Research — https://2389.ai/
- Freshell site — https://freshell.net/
- Gas Town Hall — https://gastownhall.ai/

---

## Open questions for synthesis

(Carried forward from the prior revision, with updates where the primary source now answers them.)

1. **Where does El Kaim's "dark factory" sit relative to other framings?** *Answered.* El Kaim explicitly places it as Level 5 of Shapiro's 5-level scale and explicitly says most teams should aim for Level 4. The synthesis can treat dark-factory as both an architecture option *and* the terminal level of a maturity curve, citing El Kaim's own framing.
2. **Is the October-2024 phase-change claim load-bearing?** *Sharpened.* The primary source now distinguishes two inflection points. The October-2024 claim is load-bearing for the "infrastructure-specialist" tier; the November-2025 claim is load-bearing for the "experienced-developer-on-standard-codebase" tier. The architecture options need to be **model-tier-aware**, and the report's synthesis can use El Kaim's two-tier framing directly.
3. **What's the minimum viable dark factory?** *Partially answered.* El Kaim's 12 principles are explicitly framed as *"what the teams actually building dark factories have converged on through practice."* They are the invariants. The contingent choices are the specific implementations (Kilroy vs. Mammoth vs. Smasher vs. Tracker). The three-layer architecture is the load-bearing structural invariant.
4. **How does spec authorship scale?** *Still open.* El Kaim names spec-writing as the primary Level-4-and-above skill and says *"a good spec for a dark factory is not a three-sentence feature description. It is thousands of words of structured, verifiable, example-rich prose,"* but does not describe a methodology for teaching or scaling spec authorship. This remains the biggest methodological gap relative to the project brief.
5. **Human-in-the-loop "pause" semantics.** *Still partially open.* The primary source confirms that Layer 3 (the Pipeline Engine) *"knows when to pause for human input"* but does not enumerate the pause criteria. Cost thresholds, confidence, scenario-failure type, and anomaly density are still implicit.
6. **Maintenance vs. greenfield asymmetry.** *Answered.* El Kaim is emphatic that the dark factory *"does not just build software; it maintains software"* and that the CXDB → Healer → prescription loop is the maintenance machine. The synthesis can evaluate architectures specifically on their maintenance-loop closure.
7. **Multi-human + multi-agent attribution.** *Sharpened.* El Kaim's Gas Town discussion gives the verbatim five-point design philosophy and names SOX/GDPR audit trails, performance management, cross-project dependency tracking, and federation across organizational boundaries as the enterprise extensions. Useful as a checklist for the team-scale-up story.
8. **What transplants downward into less-autonomous architectures?** *Answered.* El Kaim's twelve principles are explicitly designed to be adoptable at less-than-Level-5 maturity (*"Most teams would benefit enormously from reaching Level 4. The principles are the same at both scales."*). The synthesis can pull principles 1, 5, 6, 8, 9, 10, 11 directly into a Level-3-or-4 architecture without committing to full Level 5.

---

## Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| https://el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e | ✅ FULL | Manual browser-cookie fetch 2026-05-11; full 41 KB / 24-minute article exported to `reference-only/dark-factory-article.txt`. Canonical primary source for this report. |
| https://medium.com/@welkaim/about | ❌ | Cloudflare interstitial only; author-identification context, no body. |
| https://welkaim.medium.com/ | ❌ | Cloudflare interstitial only; author-identification context, no body. |

Legend: ✅ full / 🟡 reconstructed / ⏳ pending / ❌ unavailable.
