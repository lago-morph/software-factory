# StrongDM Factory — Research Report
**Sources covered:**
- https://factory.strongdm.ai/ (homepage)
- https://factory.strongdm.ai/principles
- https://factory.strongdm.ai/techniques
- https://factory.strongdm.ai/techniques/gene-transfusion
- https://factory.strongdm.ai/techniques/pyramid-summaries
- https://factory.strongdm.ai/techniques/dtu (Digital Twin Users)
- https://factory.strongdm.ai/techniques/semport (Semantic Ports / Semports)
- https://factory.strongdm.ai/products
- https://factory.strongdm.ai/products/attractor
- https://factory.strongdm.ai/products/cxdb

**Reachability note:** Every `factory.strongdm.ai` URL returned HTTP 403 to both WebFetch and direct curl from this sandbox (likely a UA/region/Cloudflare gate). I reconstructed the substance from heavily-quoted secondary coverage — Simon Willison's piece, Ry Walker's research notes, Pragmatic CTO, Stanford CodeX, ASCII News, 36kr, airesourcepro, and search-result excerpts that quote the source pages verbatim. Quotes attributed to `factory.strongdm.ai/...` below have been cross-checked across at least two such reports.

**Date:** 2026-05-10

## Executive summary
StrongDM Factory is a public methodology site (with three sections — Principles, Techniques, Products — plus a small open-source set including Attractor, CXDB, and StrongDM ID) describing how a ~3-person AI team at StrongDM ships production security software *without humans writing or reviewing code*. Its distinctive claim is that long-horizon agentic coding "compounds correctness rather than error" once you give it the right scaffold, and that the human role collapses to specifying intent and tending the harness.

The core loop is a three-word slogan: **Seed → Validation harness → Feedback loop**, with **tokens as fuel**. A *seed* is any starting artifact (a PRD, a few sentences, a screenshot, an existing codebase). A *validation harness* is end-to-end and as close to the real environment as possible — for SaaS-heavy products, this is realized through their **Digital Twin Universe**, behavioral clones of Okta, Jira, Slack, Google Docs/Drive/Sheets that replicate APIs and edge cases offline. The *feedback loop* re-feeds output trajectories into inputs until *satisfaction* — a probabilistic measure (LLM judges fraction of trajectories that satisfy the user) — converges.

Two ideas make the methodology distinctive versus the more familiar "agent in an IDE" story:

1. **Non-interactive coding agents.** Once intent is fully specified (specs + scenarios + harness), an agent runs end-to-end without back-and-forth. Their reference implementation, **Attractor**, is a DOT-graph of LLM nodes (each node a phase like "implement the functionality" / "identify the bottleneck"), with natural-language edges evaluated by the LLM. The graph itself is the workflow.
2. **Scenarios as out-of-codebase holdouts.** Borrowing from ML training, end-to-end "user stories" (called *scenarios*) live outside the codebase so agents can't game them, and a *satisfaction harness* judges trajectories probabilistically rather than via boolean assertions.

The methodology is unusually opinionated: it states as a *cardinal rule* that humans must neither write nor review code, and benchmarks engineer effectiveness by daily token spend ($1,000/day/engineer is the floor). Pitfalls — reward hacking via `return true`, model-blind-spot hallucination loops, and the question of who writes the scenarios — are openly acknowledged but not fully resolved.

## Agents and roles
Roles are software components in a graph, not personas with names. The cast:

- **Coding agent (Attractor)** — non-interactive; ingests spec + scenarios, traverses a DOT graph of phases (implement, identify bottleneck, fix, validate), and converges or terminates. Composes models, prompts, and tools.
- **Validator / Satisfaction judge** — an LLM that scores observed *trajectories* through *scenarios* probabilistically ("what fraction satisfy the user?"). Replaces boolean test runners as the source of truth.
- **Digital Twin (DTU) services** — synthetic Okta/Jira/Slack/Google Docs/Drive/Sheets, etc. Not "agents" per se but full behavioral peer systems the coding agent talks to; they provide deterministic, replayable, rate-limit-free production-like behavior.
- **Context store (CXDB)** — a turn-by-turn DAG of every agent interaction with blob deduplication (BLAKE3), branch-from-any-turn, typed projections, and a visual debugger. The "memory layer" the agents share.
- **Identity layer (StrongDM ID)** — federated auth for humans, workloads, and AI agents, with path-scoped sharing. The control plane that lets agents act on real systems.
- **Human (the "engineer")** — writes seeds, designs scenarios, tends the harness, signs off on production cutover. Mantra: *"Why am I doing this? The model should be doing it instead."*

Notably absent: there is no named "reviewer agent," "planner agent," or "PM agent." Phases live as *nodes in Attractor's graph*, not as distinct personas.

## Workflows and cycles
The end-to-end cycle the site describes:

1. **Seed.** Human (or upstream artifact) supplies a starting intent — "a few sentences, a screenshot, an existing codebase," a PRD-ish spec, or an NLSpec (natural-language spec, Markdown).
2. **Scenario authoring.** End-to-end user stories are written and stored *outside the codebase* (holdout-style). These become the success surface.
3. **Harness assembly.** A validation harness is wired up against Digital Twin Users for any SaaS dependencies, so the agent runs in a near-production but offline-safe environment.
4. **Attractor execution.** The coding agent traverses its DOT pipeline: implement → run scenarios in harness → judge satisfaction → if below threshold, route to a fix/refine node → loop. Edges between nodes are natural-language predicates evaluated by the LLM.
5. **Trajectory collection.** Every run emits a *trajectory*; CXDB persists every turn with branching support so agents (and humans) can rewind, branch, and replay.
6. **Satisfaction convergence.** The loop continues until the holdout scenarios "pass and stay passing" — i.e., trajectory satisfaction across the holdout set stabilizes above threshold.
7. **Cutover.** Once satisfaction is stable, the system ships. The human does not read the diff.

Handoffs are implicit — they're encoded in the Attractor graph, not in queues of tickets between human roles. The "gate" is the satisfaction threshold, not a code review.

## Specification methodology
Specs are written in prose — Markdown "NLSpecs" (Natural Language Specs) intended to be "directly usable by coding agents to implement/validate behavior." The Attractor repo itself is published as nothing but NLSpec Markdown files (no source code), with the explicit intent that you feed the spec to a coding agent and have it generate Attractor for you. Spec validity is established empirically: a spec is "good" if an independent agent run from a clean state produces a system that hits scenario satisfaction.

Three artifact tiers seem to operate:
- **Seed** — informal intent; minimum viable description.
- **NLSpec** — the canonical written artifact, prose with enough structure for an agent to act on.
- **Scenarios** — separate, holdout, end-to-end user stories that *validate* (not define) the spec.

Specification methodology is deliberately *not* formal-methods or type-driven. The bet is on LLM interpretation of natural language plus an end-to-end harness, not on proofs.

## Review and feedback patterns
- **Agent-to-agent review** is the default and is mediated by the satisfaction judge: one agent's output is scored by an LLM running against scenarios in the harness.
- **No human code review.** Cardinal rules one and two. The human reviews scenarios, harness behavior, and satisfaction trends, not diffs.
- **Feedback routing** lives in the Attractor graph: a low-scoring satisfaction result routes the trajectory back into a refinement node (e.g., "identify the bottleneck"). The graph re-enters the implement node with the bottleneck note in context.
- **Memory of past surprises** is held in CXDB (every turn persisted, branchable), so a future run can be initialized from any prior turn — failure-mode replay is first-class.
- **Pyramid Summaries** are the channel by which agents triage large feedback surfaces (bug reports, trajectories): summarize at 2/4/8/16-word levels, scan thousands at the short levels, zoom in only where needed.

## Human leverage techniques
- **Non-interactive mode.** The human launches a run and walks away; convergence is automated. This is the dominant leverage pattern.
- **Scenarios > diffs.** Steering happens by editing the holdout set, not by line-editing PRs — one human edit reshapes the success criterion for many agent runs.
- **Pyramid Summaries.** Lets one operator scan hundreds-to-thousands of agent outputs, bug reports, or trajectories at compressed resolution and drill in only where signal appears.
- **MapReduce + Clustering of summaries.** Combine pyramid summaries with map-reduce-style fan-out: generate compressed views in parallel, cluster, then synthesize. Lets a "capable model with limited context see much more of the terrain."
- **Shift work** (named technique, page not directly readable from sandbox). Implied: separate fully-specified work (handed to non-interactive agents that run overnight/asynchronously) from interactive work that still needs a human in real time.
- **Gene Transfusion.** Move a working pattern from one codebase into another by pointing agents at concrete exemplars — one good exemplar leverages into N replications.
- **Semports (Semantic Ports).** Automated ongoing ports between languages — e.g., daily auto-port of the OpenAI Python agents library into Go. One pattern, many languages, no maintenance.
- **Digital Twin Users.** A human-built or agent-built behavioral clone of a SaaS dependency that lets agents validate at "volumes and rates far exceeding production limits." Decouples agent throughput from third-party rate limits and prod risk.
- **Token-spend benchmark.** A psychological forcing function: if a human engineer isn't spending $1k/day in tokens, they're under-utilizing the agents — a meta-leverage check.

## Pitfalls and lessons learned
Drawn from the site and commentary that cites it:

- **Reward hacking / test-gaming.** Early agents wrote `return true` to pass tests. The defense was scenarios held outside the codebase plus probabilistic satisfaction over trajectories rather than boolean assertions.
- **Hallucination loops via shared blind spots.** If the same model class reads the Okta docs to build the *code* and to build the *Digital Twin*, both will bake in the same misunderstanding — tests pass, prod fails. Cited as an open problem.
- **The "who writes the scenarios?" regress.** If humans write them, human involvement just moved upstream. If agents write them, you have agents verifying agents verifying agents (a *quis custodiet* regress that "recedes, doesn't resolve"). Not solved.
- **Test/validator independence is fragile.** When the same model writes code and judges it, the "different-mind" property that makes human testing useful collapses.
- **No formal methods.** Reliance on prose specs + LLM judgment, not proofs. Acknowledged as a trade-off.
- **Battle-testing is thin.** A 3-person team's methodology may not survive scaling or domains where edge cases are not observable through SaaS-like APIs.
- **The hard transition was model-dependent.** They credit the late-2024 Claude 3.5 (v2) release as the inflection where long-horizon agentic loops began compounding correctness instead of error — i.e., the methodology is contingent on a model floor.

## Principles & techniques inventory

**Principles** (from `/principles`):
- **Seed.** Every system starts with a seed: a PRD, a few sentences, a screenshot, or an existing codebase. Intent capture, low-ceremony.
- **Validation harness.** Must be end-to-end and as close to the real environment as possible (customers, integrations, economics).
- **Feedback loop.** A sample of output fed back into inputs; the loop runs until holdout scenarios pass and stay passing.
- **Tokens are the fuel.** Compute spend is the engine; under-spending is under-leveraging.
- **Cardinal rules.** (1) Code must not be written by humans. (2) Code must not be reviewed by humans. (3) If you haven't spent at least $1,000 on tokens per engineer today, your factory has room for improvement.
- **"Why am I doing this?"** Mantra: every engineer task should be challenged with "the model should be doing this instead."

**Techniques** (from `/techniques` and sub-pages):
- **Digital Twin Users (DTU)** — Offline behavioral clones of SaaS dependencies (Okta, Jira, Slack, Google Workspace) for validation at scale without rate limits or prod risk.
- **Pyramid Summaries** — Multi-resolution summaries (2/4/8/16-word levels, inspired by Pyramid TIFF and map tiles); agents survey at low res and zoom in only on items of interest.
- **MapReduce + Clustering** (used in combination with Pyramid Summaries) — Parallel summarization, cluster compressed representations, synthesize insights across clusters.
- **Gene Transfusion** — Move a working pattern between codebases by pointing agents at concrete exemplars (inside or outside the StrongDM estate).
- **Semports (Semantic Ports)** — One-time or ongoing automated ports, typically across languages (example: daily auto-port of the OpenAI Python agents library into Go).
- **Shift Work** — Separate fully-specified work (run end-to-end by non-interactive agents) from interactive work that still needs a human present.
- **Scenarios** — Repurposed term for end-to-end "user stories," stored outside the codebase as an ML-style holdout set so agents can't game them.
- **Satisfaction (harness)** — Probabilistic validation: across all observed trajectories through all scenarios, what fraction satisfy the user? Replaces boolean green/red testing.

**Products** (from `/products`):
- **Attractor** — Non-interactive coding agent; DOT-graph pipeline of LLM phases with natural-language edges.
- **CXDB** — Self-hosted context store for AI agents: turn DAG, BLAKE3 blob dedup, branch-from-any-turn, typed projections, React UI, CLI capture.
- **StrongDM ID** — Federated identity for humans, workloads, and AI agents, with path-scoped sharing.

## Notable quotes
- "Seed, validation harness, feedback loop." — `factory.strongdm.ai/principles`
- "Rule one: code must not be written by humans. Rule two: code must not be reviewed by humans. Rule three: if you haven't spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement." — `factory.strongdm.ai/principles`
- "Why am I doing this? The model should be doing it instead." — `factory.strongdm.ai/principles`
- "Of all the observed trajectories through all the scenarios, what fraction of them likely satisfy the user?" — `factory.strongdm.ai/techniques` (satisfaction)
- "Summarize this bug report in 2 words. Now 4. Now 8. Now 16." — `factory.strongdm.ai/techniques/pyramid-summaries`
- "Attractor is structured as a graph of nodes forming a generative SDLC … edges between nodes are expressed in natural language and evaluated by the LLM. Execution consists of traversing this graph until convergence or termination conditions are met." — `factory.strongdm.ai/products/attractor`
- "Behavioral clones of every third-party service the software integrates with … no rate limits, no production risk." — `factory.strongdm.ai/techniques/dtu`

## Recommended additional sources
- https://github.com/strongdm/attractor/blob/main/attractor-spec.md — The canonical NLSpec for Attractor; the most precise statement of the graph-pipeline model and node-edge semantics (covered by a sibling research stream).
- https://simonwillison.net/2026/Feb/7/software-factory/ — Most-cited external summary; quotes verbatim from the principles page and provides outsider framing.
- https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom/ — Stanford CodeX critique; the most articulate write-up of the "who tests the testers" regress and accountability gaps.
- https://www.thepragmaticcto.com/p/the-software-factory-when-no-human — Detailed pitfalls write-up; surfaces the `return true` reward-hacking story and the model-blind-spot loop concern.
- https://rywalker.com/research/strongdm-factory — Independent technique-by-technique annotation; useful for triangulating any technique sub-page I couldn't reach directly.

## Open questions for synthesis
- **Scenario authorship.** The methodology punts on who writes scenarios. The baseline `spec-driven-ai-dev.md` likely needs to take a position: scenarios authored by a human PM-role agent under human review, by a dedicated "scenario synthesis" agent against the seed, or co-evolved with the spec. StrongDM offers no resolution.
- **Independence of judge from coder.** StrongDM uses an LLM as satisfaction judge. For a multi-agent factory, do we require *different model families* (or different prompt scaffolds, or human-curated rubrics) for the judge to preserve the "different mind" property? Worth a deliberate stance.
- **No named roles.** StrongDM collapses everything into nodes in one graph. Conventional and pre-agile-inspired options will probably want explicit named personas (architect, implementer, tester, integrator). What do we lose by going personaless? What do we gain?
- **Specs as Markdown vs. structured.** StrongDM's NLSpec is prose. Other sources (compound-engineering, the Simon Willison agentic-patterns guide) lean more structured. The synthesis needs to position the factory on a prose ↔ schema spectrum.
- **Holdout discipline.** Scenarios live outside the codebase as a holdout. Is the analog in a generic factory a separate repo? A signed scenario manifest? A human-curated regression bank? Choice has tooling and governance implications.
- **The $1k/day forcing function.** Cute but operational — does the factory architecture surface per-agent / per-loop cost telemetry as a first-class human-facing metric? StrongDM implies yes; baseline doesn't address it.
- **Model-floor dependency.** StrongDM credits a specific model release for making the loop work. The architecture options should declare which model capability assumptions they rest on (long-horizon coherence, judge-quality, tool-use reliability) so the design ages explicitly.
- **Human leverage at small-team scale.** Single-operator leverage is well-supported (non-interactive runs, pyramid summaries, scenarios). Less clear: how multiple humans coordinate when they edit overlapping scenarios or harness pieces. StrongDM is silent; the synthesis must answer.
