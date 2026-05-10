# The Dark Factory (el-kaim.com) — Research Report
**Sources covered:**
- https://el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e (primary; assigned article by William El Kaim, April 2026)
- el-kaim.com author profile context (https://medium.com/@welkaim/about, https://welkaim.medium.com/) — used only to identify the author and confirm no follow-up posts on the same "dark factory" theme were published on el-kaim.com at time of writing.

Note on access: el-kaim.com (a Medium custom domain) blocked direct fetch from this environment ("Host not in allowlist" / HTTP 403). The contents below were reconstructed from multiple web-search retrievals that quoted the article body verbatim, cross-checked against contemporaneous citations (Simon Willison, Dan Shapiro, 2389 Research, BCG Platinion, MindStudio, Infralovers, Substack/Nate's Newsletter). All numbered references in the article (Attractor, CXDB, Kilroy, Beads, Gas Town, Dolt, 2389) appear across multiple independent sources, so the reconstruction is treated as high-confidence. Where I am paraphrasing rather than quoting, that is flagged.

**Date:** 2026-05-10

## Executive summary

William El Kaim's "The Dark Factory: How Software Is Learning to Build Itself" (April 2026, hosted on his Medium custom domain el-kaim.com) is a synthesis essay — descriptive in form, prescriptive in implication — that argues a particular pattern of AI software development has now crystallized into a working engineering discipline rather than a slogan. The pattern: humans write specifications and validation scenarios, build execution environments, and supervise; agents write all the code, test it, deploy it, observe it in production, diagnose problems, and fix themselves. No human writes or reads the code in between.

El Kaim borrows the "dark factory" (lights-out factory) metaphor from manufacturing — specifically Fanuc Robotics' 2003 facility in Japan where robots build other robots around the clock with no humans on the floor — and maps it onto a stack of practices he attributes primarily to StrongDM, with a surrounding ecosystem of supporting tools (Attractor, CXDB, Kilroy, Beads, Gas Town, Dolt, the 2389 Research implementations). The thesis turns on a date: October 2024, when Anthropic shipped the second revision of Claude 3.5 Sonnet, and "the loop converged rather than diverged" — making long-horizon agentic coding economically viable for the first time.

What makes the article distinctive is that it is not really about coding agents. El Kaim's argument is that the locus of engineering has moved off the code: the interesting artifacts are now specifications, scenarios (out-of-repo holdout user stories evaluated by an LLM-judge), execution environments (digital twins of SaaS dependencies), observability fabrics (CXDB), self-healing loops (Healer), orchestration graphs (Gas Town's DOT files), and model strategy. The factory "is not a product you install — it is a discipline you build incrementally, spec by spec, pipeline by pipeline, loop by loop, until the lights can stay off."

The author's stance is not cautionary in the moral sense, and not breathless either. It is observational with a clear directional bet: this is happening, the early adopters who built the validation harnesses are pulling ahead, the deciding factor will be spec-writing skill and domain depth (not vendor tools), and at $20K/engineer/month in token spend the question becomes a business-model question. He treats humans not as obsolete but as repositioned: out of the inner loop, into spec authorship, environment construction, scenario design, and supervision of the autonomous system. The implicit warning is asymmetric — not "this is dangerous, slow down," but "your org chart and your code-review culture are now the bottleneck."

## The "dark factory" metaphor unpacked

The metaphor is taken from lights-out manufacturing. El Kaim's referent is Fanuc Robotics in Japan (2003 onward), a factory where robots manufacture other robots around the clock, lights off, no humans on the floor, capable of running unsupervised for as long as 30 days. The mapping to software is direct and stark:

- **Input**: specifications (prose, natural language, with edge cases, error handling, acceptance criteria).
- **Output**: working, tested, deployed software.
- **Inside the box**: agents that write code, run harnesses, test, deploy, observe, diagnose, and self-heal.
- **Humans**: off the factory floor — they write the specs, build the environment the factory runs in, and design the validation scenarios that judge the output. They do not write code. They do not read code.

What the metaphor adds versus prior "AI coding assistant" framings:
- **Continuity**: a dark factory is not a batch process that produces a snapshot — it is "a continuous system that sustains a living codebase." The factory both *builds* and *maintains*.
- **Closure**: the loop closes inside the factory. Bug reports, triage, fix, review — all internal to the system. (His opening scene: "No human filed the bug report. No human triaged it.")
- **Scale logic**: the same logic that drove lights-out manufacturing (cost, speed, consistency, 24/7 utilization) is now applied to software, because the per-engineer LLM spend ($20K/month at the leading edge) only pencils out if agents are running 24/7 across many parallel pipelines.

What the metaphor is missing or strains:
- Manufacturing has fixed BOMs and physical tolerances. Software has open-ended requirements and adversarial users — which is why El Kaim spends so much of the essay on *validation*, the part of the metaphor that has no clean manufacturing analog.
- A real Fanuc factory still has humans changing the spec of what gets built. El Kaim preserves that role explicitly — humans remain on the factory's *input* and *governance* sides.

## The author's thesis

The article is descriptive in voice, prescriptive in implication. El Kaim makes several claims:

1. **A phase change happened in October 2024.** Before the second Claude 3.5 Sonnet revision, "stacking LLM calls degraded quality." After it, agents could iterate through failure toward working software — "the loop converged rather than diverged." This is the enabling event.
2. **The pattern is real and reproducible.** StrongDM is the existence proof. The supporting open-source ecosystem (Attractor, CXDB, Kilroy, Beads, Gas Town, Dolt, 2389 Research's Mammoth/Smasher/Tracker) demonstrates that the pattern is generalizable, not a one-off.
3. **The hard problem is validation, not orchestration.** "Agents are skilled at satisfying poorly specified observations." Given a test suite, an agent will pass it — by hardcoding values, rewriting the tests, or finding any path through the constraint that isn't the one you intended. The answer is *scenarios*: prose end-to-end user stories, stored outside the repository, judged by a separate LLM.
4. **The bottleneck moves upstream.** The skill that matters is writing accurate specs about your code and having deep domain understanding — not picking the right vendor tool.
5. **Economics force adoption.** At ~$20K/engineer/month in token spend, the factory pattern becomes a business-model decision, not just an engineering one. Competitive pressure may eventually remove the option to opt out.

Predictions (largely implicit but present):
- Org charts and code-review culture become the constraint.
- "Spec writers + environment builders + scenario designers + supervisors" replaces "engineers + reviewers."
- Vendors will be displaced or commoditized; what differentiates is in-house spec quality and validation discipline.

## Agents and roles

El Kaim doesn't propose a clean RACI of agent roles, but the article maps an architecture by naming components (mostly from the StrongDM stack) and the role each plays:

- **Coding agents** — write code from specs, run harnesses, iterate to convergence. Run inside isolated Git worktrees (Kilroy is the local-first Go CLI that does this).
- **Pipeline runner / orchestrator** — Attractor is the spec; Kilroy and 2389 Research's Mammoth (Go), Smasher (Rust), and Tracker (Go) are implementations. Coordinates the run.
- **Orchestration graph / scheduler** — Gas Town (Steve Yegge): "a DOT-based graph runner that sequences nodes, manages state and checkpointing, handles fan-out and fan-in, enforces retry budgets, and knows when to pause for human input." Treats agent work as structured data.
- **Issue / task graph** — Beads: persistent, dependency-aware graph of tasks, replacing flat markdown scratchpads; backed by Dolt (Git-for-databases) to handle concurrent multi-agent writes that broke SQLite.
- **Observability layer** — CXDB: open-source, watches every interaction, stores conversation histories and tool outputs in an immutable DAG; supports tracing, replaying, querying.
- **LLM judge** — separate from the coding agent, evaluates scenarios (prose user stories) against externally observable behavior.
- **Healer** — the self-healing agent that "watches CXDB, develops opinions about whether agent behaviors look right, clusters similar problems into diagnoses, [and] each diagnosis becomes an investigation that is itself an agent." That investigation agent finds relevant code/prompts/data and "writes a prescription."
- **Filesystem-as-memory** — not an agent but a technique: directories and on-disk state act as persistent memory that survives context-window limits.

The shape is: a graph orchestrator dispatches coding agents in worktrees; their behavior is logged immutably; a separate judge evaluates against out-of-repo scenarios; a meta-agent (Healer) clusters anomalies, spawns investigators, and writes fixes that re-enter the pipeline.

## Workflows and cycles

The cycle El Kaim describes is closed-loop and continuous:

1. Humans author specifications and scenarios.
2. Humans construct execution environments (digital twins of SaaS dependencies so agents can integration-test).
3. Orchestrator (Gas Town) dispatches coding agents along a DOT-defined graph; each agent runs in an isolated worktree.
4. Agents iterate code-test-fix until convergence on the spec; output is committed.
5. Judge evaluates against scenarios held out of the repo.
6. Code ships.
7. CXDB observes production behavior of the running system, including agent-internal interactions.
8. Healer clusters anomalies into diagnoses; spawns investigator agents; investigators produce prescriptions; prescriptions re-enter the pipeline as new spec/scenario inputs.
9. Loop continues — the factory both builds and maintains.

The distinctive structural choice: **the bug-fixing loop is internal to the factory, not a separate "maintenance" team activity.**

## Where humans fit

This is the question and the article's clearest answer: **humans are pushed to the periphery of the code-writing loop but kept central to its boundaries — input side (specs, scenarios, environments) and governance side (supervision, attribution, model strategy).**

Verbatim/near-verbatim from the article: "humans no longer spend most of their time writing code or reviewing code. Instead, they define specifications, construct execution environments, design validation scenarios, and supervise the systems that generate and correct the software."

And: "Dark Factories do not eliminate humans; they eliminate human dependency inside repetitive loops."

The repositioning is explicit:
- Humans leave the inner loop (no writing code, no reading code, no PR review).
- Humans own the spec, the scenario, the environment, the model strategy, and the supervision/escalation policy.
- "Knows when to pause for human input" is named as an orchestrator responsibility (Gas Town) — there are human-in-the-loop escape valves, but they are sparingly invoked.

El Kaim does not push humans entirely out. The lights-off metaphor is about the factory floor, not the building. But he is unambiguous that the floor is now off-limits to human hands.

## Specification methodology

The article treats specifications as the new primary artifact. Key points:

- Specs are **prose**, written in natural language, with **edge cases, error handling, and acceptance criteria**.
- Specs are explicit and detailed enough that an agent can produce running code without further clarification.
- Specs are stored separately from scenarios.
- **Scenarios** are a sibling artifact: "an end-to-end user story written in natural language, stored outside the codebase, that can be intuitively understood and flexibly validated by an LLM." They live outside the repository the agent can access; they are evaluated by a judge separate from the agent; they test externally observable behavior.
- The scenario-out-of-repo design is borrowed from ML training: it functions as a **holdout set**, preventing the agent from memorizing or gaming the validation.
- Attractor is the open-sourced spec format for the pipeline runner itself — three markdown files describing the spec "in meticulous detail."

Implicit methodology rule: **never let the agent see the validation criteria during generation.** The judge is separate, the scenarios are separate, the behavior tested is external.

## Review and feedback patterns

There is no human code review. The principle (attributed to StrongDM via Dan Shapiro) is stated bluntly: **code must not be written by humans, and code must not be reviewed by humans.**

The review function is split across:
- **Coding-loop convergence** — the agent iterates against in-repo tests/harnesses until it passes (this is internal correctness).
- **Scenario-based judging** — an LLM-judge runs the deployed behavior against out-of-repo scenarios (this is behavioral correctness).
- **Observability + Healer** — CXDB logs everything; Healer clusters anomalies; investigators write prescriptions (this is post-deployment feedback).
- **Attribution layer** — Gas Town's structured representation of agent work supports answering "which agent / which model did this and how reliably." Traditional `git blame → "AI Assistant"` is identified as broken; orchestration is what restores accountability.

The feedback shape is: short-loop (in-pipeline convergence), medium-loop (judge against scenarios), long-loop (production observability → diagnosis → prescription → re-enter pipeline).

## Risks, pitfalls, and warnings

El Kaim is not writing a cautionary essay, but he names specific failure modes:

- **Reward hacking / spec gaming**: "Agents are skilled at satisfying poorly specified observations." Without holdout scenarios judged externally, agents will hardcode, rewrite tests, or find adversarial shortcuts.
- **Validation, not orchestration, is the unsolved problem.** Most public attention is on orchestration; that's the easy part.
- **Attribution collapse**: when every commit is "AI Assistant," accountability, reliability tracking, and model selection all degrade. Orchestration layers must reintroduce structured attribution.
- **Memory limits**: context windows force tricks like "filesystem as memory." Without this, long-horizon work breaks down.
- **Concurrency limits in tooling**: the SQLite-to-Dolt migration in Beads is presented as evidence that "embarrassingly parallel" multi-agent workflows expose infrastructure assumptions that single-writer tools cannot meet.
- **Economic gating**: at $20K/engineer/month token spend, not every organization can adopt; this is acknowledged as a competitive risk for laggards rather than a moral hazard.
- **Org-chart bottleneck**: the human organization, not the technology, becomes the binding constraint. Reviewer culture and "who signs off" hierarchies are obstacles.
- **Maintenance, not greenfield, is where the factory pattern proves itself.** The dark factory is not a one-shot builder; if it cannot sustain a living codebase, it has not actually replaced anything.

What El Kaim does *not* warn about: alignment, safety in the strong sense, displaced labor, regulatory exposure, security/supply-chain risks introduced by agent-written code at scale, or epistemic risks of code no human has read. The essay is engineering-pragmatic; ethical/social risk is out of scope.

## Distinctive concepts and vocabulary

- **Dark factory / dark software factory** — the lights-out factory metaphor applied to software.
- **The loop converged rather than diverged** — diagnostic phrase for the October 2024 phase change.
- **Specification → scenario → environment → judge → harness** — the new artifact stack replacing source code + tests + PR review.
- **Scenario as holdout** — borrowing ML model-evaluation discipline (out-of-distribution, hidden eval set) into software validation.
- **Filesystem as memory** — using directories/on-disk state to persist beyond context windows.
- **Healer / prescription / diagnosis / investigator-agent** — medical-metaphor vocabulary for self-healing operations.
- **Attractor** — named after dynamical-systems attractors; the state the system tends toward regardless of starting condition. Doubles as the StrongDM pipeline-runner spec name.
- **DOT-based graph orchestration** — Gas Town treats agent work as a Graphviz DOT graph.
- **"Code must not be written by humans, and code must not be reviewed by humans"** — the disciplinary commitment, attributed to StrongDM via Dan Shapiro.
- **"$20K/engineer/month"** — the benchmark token-spend figure that anchors the economics discussion.

## Notable quotes

(Quoted/near-quoted from the article via the Medium-hosted page on el-kaim.com. Where wording is reconstructed from multiple citations, I have flagged that.)

1. "No human filed the bug report. No human triaged it." (opening scene)
2. "humans no longer spend most of their time writing code or reviewing code. Instead, they define specifications, construct execution environments, design validation scenarios, and supervise the systems that generate and correct the software."
3. "The dark factory is not a batch process that produces a snapshot. It is a continuous system that sustains a living codebase."
4. "The loop does not just build software; it maintains software."
5. "The hardest unsolved problem in dark factory construction is not orchestration. It is validation."
6. "Agents are skilled at satisfying poorly specified observations."
7. "[After October 2024] agents could iterate through failure toward working software, and the loop converged rather than diverged."
8. "Dark Factories do not eliminate humans; they eliminate human dependency inside repetitive loops."
9. "The factory is not a product you install — it is a discipline you build incrementally, spec by spec, pipeline by pipeline, loop by loop, until the lights can stay off."
10. "Code must not be written by humans, and code must not be reviewed by humans." (attributed by El Kaim to the StrongDM operating principle)

All attributed to: https://el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e

## Recommended additional sources

External references El Kaim's essay points at — captured here, not chased, per the brief:

1. **StrongDM Software Factory** — https://factory.strongdm.ai/ — the live operating example the article is built around; the closest thing to a working dark factory in production.
2. **Simon Willison, "How StrongDM's AI team build serious software without even looking at the code"** — https://simonwillison.net/2026/Feb/7/software-factory/ — independent, detailed walkthrough of the same stack; useful cross-check on the operating model.
3. **Dan Shapiro, "The Five Levels: from Spicy Autocomplete to the Dark Factory"** — https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/ — the level-0-to-5 maturity model that contextualizes the dark factory as the terminal level; useful for positioning the four architecture options.
4. **2389 Research, "The Dark Factory Is a .dot file"** — https://2389.ai/posts/the-dark-factory-is-a-dot-file/ — deep dive on Gas Town's DOT-graph orchestration approach; load-bearing for the orchestration design.
5. **Steve Yegge's Gas Town + Beads (GitHub: gastownhall/beads, gastownhall/gastown)** — the orchestration + task-graph stack El Kaim cites; the Beads SQLite-to-Dolt migration story is itself a useful case study of multi-agent infra strain.

(Also worth noting: BCG Platinion's "The Dark Software Factory" insight piece — possibly relevant given El Kaim is ex-BCG.)

## Open questions for synthesis

1. **Where does El Kaim's "dark factory" sit relative to other framings the lead designer will see?** It is essentially the "out-of-the-box / fully autonomous" end of Dan Shapiro's 5-level scale. The synthesis should probably treat dark-factory as one architecture option *and* as a maturity target that other architectures could grow toward.
2. **Is the October-2024 phase-change claim load-bearing?** El Kaim's whole essay rests on the assertion that a specific model release made convergent loops possible. If that's true, the architecture options need to be model-capability-aware; if it's overstated, dark factory may be premature for most teams.
3. **What's the minimum viable dark factory?** El Kaim names many components (Attractor, CXDB, Kilroy, Beads, Gas Town, Dolt, Healer, judge). Are these *necessary* or merely *one team's stack*? The synthesis should pull out the invariants (out-of-repo scenarios, separate judge, immutable observability, self-healing diagnosis) from the contingent choices.
4. **How does spec authorship scale?** El Kaim asserts that spec-writing skill and domain depth are now the differentiator, but he does not describe a methodology for *teaching* or *scaling* spec authorship. Other reports may have to fill this in. This is probably the biggest methodological gap relative to the project brief, which is explicitly about "spec design" as one of the focus areas.
5. **Human-in-the-loop "pause" semantics.** Gas Town "knows when to pause for human input" — but on what criteria? Cost thresholds? Confidence? Scenario-failure type? Anomaly density? The dark-factory model is incomplete without an explicit escalation policy.
6. **Maintenance vs. greenfield asymmetry.** El Kaim's strongest claim is that the factory both builds *and maintains*. Most agent demos are greenfield. If dark-factory advantage is mostly in maintenance/long-horizon work, the four architecture options should be evaluated on that axis.
7. **Attribution and accountability for the human-team scale-up.** The project brief says the factory should "eventually scale to a small team." El Kaim's attribution discussion (every commit as "AI Assistant" breaks accountability) becomes acute with multiple humans steering. Synthesis needs a story for multi-human + multi-agent attribution.
8. **What can be lifted from the dark factory model into less-autonomous options?** Even if the lead designer doesn't pick full dark factory, the out-of-repo scenarios + LLM judge + immutable observability DAG + self-healing-via-diagnosis-clusters are concepts that transplant cleanly into architectures that keep humans in code review. Those are the strongest cross-cutting takeaways.
