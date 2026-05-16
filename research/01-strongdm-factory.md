# StrongDM Factory — Research Report

**Sources covered — all ACCESSED via local saved copies (previously blocked HTTP 403 from sandbox). Local files in `/home/user/software-factory/` are prefixed `factory.strongdm.ai__*.html`:**
- https://factory.strongdm.ai/ — `factory.strongdm.ai.html`
- https://factory.strongdm.ai/principles — `…__principles.html`
- https://factory.strongdm.ai/techniques — `…__techniques.html`
- https://factory.strongdm.ai/techniques/dtu — `…__techniques__dtu.html`
- https://factory.strongdm.ai/techniques/gene-transfusion — `…__techniques__gene-transfusion.html`
- https://factory.strongdm.ai/techniques/pyramid-summaries — `…__techniques__pyramid-summaries.html`
- https://factory.strongdm.ai/techniques/semport — `…__techniques__semport.html`
- https://factory.strongdm.ai/products — `…__products.html`
- https://factory.strongdm.ai/products/attractor — `…__products__attractor.html`
- https://factory.strongdm.ai/products/cxdb — `…__products__cxdb.html`

**Date:** 2026-05-10

## Revision notes

This revision replaces a reconstruction (built from secondary coverage when the primary site was 403-blocked) with direct extraction from the canonical pages.

**Verified verbatim:** The cardinal rules now match the homepage exactly: "Code must not be written by humans" / "Code must not be reviewed by humans" / "If you haven't spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement". The kōan: "Why am I doing this? (implied: the model should be doing this instead)". Principles slogan: "Seed → Validation harness → Feedback loop. Tokens are the fuel." Satisfaction definition ("of all the observed trajectories through all the scenarios, what fraction of them likely satisfy the user?") is verbatim from the homepage, not the techniques page.

**Added material:**
- StrongDM AI team founding (July 14, 2025; Justin McCarthy, Jay Taylor, Navan Chauhan); "Hands off!" charter line; credit to "the second revision of Claude 3.5 (October 2024)" and Cursor's YOLO mode as catalyst.
- The narrative arc from tests → integration → regression → e2e → behavior → scenarios → satisfaction, and the `return true` reward-hacking story in their own words.
- "Tokens are the fuel" page's enumerated representations: traces, screen capture, transcripts, incident replays, adversarial use, agentic simulation, just-in-time surveys, customer interviews, price elasticity testing.
- **The Filesystem** as a named first-class technique (missing entirely before).
- The "opaque ML weights" framing from `/techniques`: code's correctness is inferred only from externally observable behavior.
- Gene Transfusion's three propagation modes and five-step flow; Caddy's Let's Encrypt as canonical exemplar.
- Pyramid Summaries' "executive parallel" and the explicit Map/Cluster/Reduce decomposition.
- Semport's canonical mechanics (daily auto-port of `openai/openai-agents-python` to Go; Attractor "ledgers the fix, runs the tests, tags the release") and three variants (one-time, ongoing, adaptive).
- DTU's four-property enumeration and boundary-replication recipe ("validate doubles against the live dependency until we stop finding behavioral differences").
- Attractor's four key properties (deterministic, observable, resumable, composable), node prompts, and sample natural-language edges; plus the large community implementation ecosystem (17+ ports).
- CXDB performance claims (p50 < 1ms append, 70%+ storage reduction via Zstd + BLAKE3 CAS, dual binary/HTTP ports 9009/9010, Rust+Go+React stack) and competitive positioning vs. LangSmith / Langfuse / Helicone / OTel / LiteLLM.
- The site's own list of related practitioners and competitor factories.

**Corrections to prior report:**
- "DTU" stands for **Digital Twin *Universe***, not "Digital Twin *Users*" — the URL slug misled the reconstruction.
- The principles page does **not** number the rules ("Rule one…"). They are presented as kōan, then two rules, then a "practical form". The numbered phrasing was a secondary-source rewording.
- The canonical Attractor page describes a "graph of nodes, forming a generative SDLC" / "graph-structured pipeline" — *not* "DOT-graph". DOT is a community-implementation convention.
- "Scenarios" and "Satisfaction" are defined on the **homepage**, not as standalone technique pages — they sit upstream of the techniques inventory entirely.
- "Shift Work" exists as a one-line definition on `/techniques` (no dedicated subpage), confirming the prior report's guess.
- The catalyst model is "the second revision of Claude 3.5" (more specific than "Claude 3.5 v2").
- The prior report named "Hallucination loops via shared blind spots" as a canonical pitfall; the canonical pages do not directly admit this — it came from secondary commentary and is now flagged as an open question rather than a documented lesson.

**Footnote-1 attribution chain — LukePM source recovered (2026-05-16, Cluster-M manual drain).** The StrongDM homepage's footnote 1 has historically pointed at a `lukepm.com/blog/the-software-factory/` post (2024-12-24). The article itself was previously flagged as "not in corpus" (`plan-sync.md`). With this Cluster-M manual drain it is now anchored: a definitional, speculative post by "luke" (Luke Moynihan) sketching specialized AI agents (Business Analyst, DevOps, QA) coordinated by an "AI compiler" that auto-optimizes generated code, arguing speed/agility will displace code quality and correctness as primary engineering concerns. No benchmarks, no architecture detail, no governance discussion. Durable value: **closes the StrongDM footnote-1 attribution chain**; **not a substrate-claim anchor** and should not be cited as a methodology source. The corresponding row in the Sources table below reflects status ✅ FULL drained from the manual capture at `research/manual/The Software Factory _ LukePM.com.txt`, marked low-priority.

**New external references surfaced by the primary sources (for future research):**
- Luke PM, "The Software Factory"; Sam Schillace, "I Have Seen the Compounding Teams"; Dan Shapiro, "Five Levels from Spicy Autocomplete to the Software Factory" (all cited in homepage footnote 1).
- Competitor factories (homepage footnote 2): Devin, 8090, Factory, Superconductor, Jesse Vincent's Superpowers.
- Reference LLM-native SDKs Semport pulls from: Vercel AI SDK, OpenAI Agents SDK.
- Caddy's Let's Encrypt integration (the canonical Gene Transfusion exemplar).
- 17+ named community Attractor ports across Rust, Go, Python, Java, F#, PHP, Tcl, TypeScript, Scala, Ruby, C, C# — Fabro (Bryan Helmkamp), Kilroy (Dan Shapiro), Forge (Luke Buehler), Arc (Point Labs), and Amol Kabe's multi-agent factory variant being the most distinctive.

## Executive summary

StrongDM Factory is the public methodology site of the StrongDM AI team — three engineers (Justin McCarthy, Jay Taylor, Navan Chauhan, founded July 14, 2025) — describing how they ship production security software with no human-written or human-reviewed code. Four sections: **Story** (`/`), **Principles**, **Techniques** (+ per-technique subpages), and **Products** (+ per-product subpages).

The thesis: with "the second revision of Claude 3.5" (October 2024) as a model floor, long-horizon agentic coding "began to compound correctness rather than error" rather than decay through accumulated misunderstandings. Given that floor, the engineering problem stops being *writing code* and becomes *specifying intent, building a validation harness, and feeding tokens into a feedback loop until convergence*.

The core slogan is **"Seed → Validation harness → Feedback loop. Tokens are the fuel."** (`/principles`). A seed is "a PRD, a few sentences, a screenshot, or an existing codebase." The harness must be "end-to-end, as close to the real environment as possible: customers, integrations, economics." The loop "runs until the holdout scenarios pass (and stay passing)".

Two distinctive moves:

1. **Scenarios + Satisfaction replace tests.** A *scenario* is "an end-to-end 'user story', often stored outside the codebase (similar to a 'holdout' set in model training)." *Satisfaction* is probabilistic: "of all the observed trajectories through all the scenarios, what fraction of them likely satisfy the user?" (`/`). The holdout sits outside the codebase the agent can edit, defending against `return true`-style reward-hacking.
2. **The Digital Twin Universe (DTU).** Rather than running scenarios against live SaaS, StrongDM built behavioral clones of Okta, Jira, Slack, Google Docs, Drive, and Sheets. The economic premise: "Creating a high fidelity clone of a significant SaaS application was always possible, but never economically feasible" — agents now make it routine (`/techniques/dtu`).

The site frames this as "deliberate naivete: finding and removing the habits, conventions, and constraints of Software 1.0" (`/`).

## Agents and roles

Roles are software components, not personas:

- **Coding agent (Attractor)** — "a non-interactive coding agent … composes models, prompts, and tools into a graph-structured pipeline … designed to operate end-to-end once the work is fully specified" (`/products/attractor`). Node prompts include "implement the functionality", "identify the bottleneck", "optimize for performance", "verify behavioral correctness"; edges are natural-language predicates evaluated by the LLM.
- **Satisfaction judge** — an LLM scoring trajectory fraction that "likely satisfy the user". Replaces boolean assertions.
- **Digital Twin Universe** — behavioral clones at the API boundary, "built from API contracts and observed edge cases" and "validate[d] against the live dependency until we stop finding behavioral differences" (`/techniques/dtu`).
- **CXDB** — "a self-hosted context store for AI agents [that] persists every turn of every conversation with full type awareness, branching support, and a visual debugger" (`/products/cxdb`). Turn DAG + BLAKE3 blob CAS + dynamic type system = the agents' shared memory.
- **StrongDM ID** — federated identity for humans, workloads, and AI agents with path-scoped sharing.
- **Human engineer** — writes seeds, curates scenarios, tends harnesses, decides cutover. "Hands off!" was the founding charter line.

There is no named "reviewer," "planner," or "PM" agent on the canonical site. (Community Attractor implementations like Amol Kabe's *do* introduce specialized Coding/Validator/Debugger/Planner agents.)

## Workflows and cycles

End-to-end cycle reconstructed from the canonical pages:

1. **Seed.** "A PRD, a few sentences, a screenshot, or an existing codebase" (`/principles`).
2. **Scenario curation.** End-to-end user stories stored outside the codebase. The homepage shows a "synthetic scenario curation and shaping interface" screenshot — suggesting agent-assisted authoring.
3. **Harness assembly.** Wire up against DTUs plus any other input modalities (traces, screen capture, transcripts, incident replays, adversarial use, agentic simulation, customer interviews, price elasticity tests).
4. **Attractor execution.** "Execution consists of traversing this graph until convergence or termination conditions are met" (`/products/attractor`). Edges are natural-language predicates ("Proceed once a bottleneck is identified"; "Take this edge if the copywriting standards have been met").
5. **Trajectory persistence in CXDB.** Every turn lands in a turn DAG; branching is O(1).
6. **Satisfaction convergence.** Loop runs "until the holdout scenarios pass (and stay passing)" (`/principles`).
7. **Cutover.** No human diff review; the gate is satisfaction stability.

Attractor's claimed key properties: deterministic given the same inputs, observable at every node transition, resumable from any checkpoint, composable with other graphs.

## Specification methodology

The site treats *intent* as the human's output and *code* as a derived, opaque artifact. From `/techniques`: "Code was treated analogously to an ML model snapshot: opaque weights whose correctness is inferred exclusively from externally observable behavior. Internal structure is treated as opaque."

Three-artifact tier: **Seed** (informal intent) → **Spec** (prose; called "NLSpec" in the GitHub spec, not on canonical pages) → **Scenarios** (out-of-codebase holdout user stories that validate, not define, behavior). Deliberately non-formal: prose + LLM judgment + harness, not types or proofs.

## Review and feedback patterns

- **Agent-to-agent review** mediated by the satisfaction judge against the scenario holdout.
- **No human code review** — restated as cardinal rule.
- **Feedback routing inside Attractor.** Low satisfaction routes the trajectory to a "fix" or "identify the bottleneck" node; the graph re-enters implementation with that note in context.
- **Branchable memory in CXDB.** "Branch from any point without copying history. Forking is O(1)" — so failure-mode replay (and "what if we'd done X here") is first-class.
- **Pyramid Summaries** for high-volume triage. "Summarize this bug report in 2 words. Now 4. Now 8. Now 16." Agents survey "hundreds of items at their 2-word level, identify the interesting ones, and expand only those" (`/techniques/pyramid-summaries`). Combined with MapReduce + Clustering, "a capable model with limited context can 'see' much more of the terrain."

## Human leverage techniques

- **Non-interactive execution.** Attractor "is designed to operate end-to-end once the work is fully specified" (`/products/attractor`); the human launches and walks away.
- **Scenarios > diffs.** Steering happens by editing the holdout, not by editing code.
- **Shift Work.** "Separate interactive work from fully specified work. When intent is complete (specs, tests, existing apps), an agent can run end-to-end without back-and-forth" (`/techniques`).
- **Pyramid Summaries + MapReduce + Clustering.** Compress, cluster compressed forms, synthesize, drill in only where signal warrants. Executive-style drill-down.
- **Gene Transfusion.** Point agents at concrete exemplars (e.g., Caddy's Let's Encrypt integration); three propagation modes (cross-language, direct inlining, library embodiment).
- **Semports.** Continuous auto-port of trusted upstream libraries into your preferred language — "while our human team members sleep" (`/techniques/semport`).
- **DTU.** Validate "at volumes and rates far exceeding production limits" without prod risk.
- **The Filesystem.** On-disk state as a memory substrate the agent reads and writes itself.
- **Token-spend benchmark.** The $1,000/day/engineer floor as a meta-leverage check.

## Pitfalls and lessons learned

- **Reward hacking via the codebase.** "A test, stored in the codebase, can be lazily rewritten to match the code. The code could be rewritten to trivially pass the test" (`/`). Defense: out-of-codebase scenarios + probabilistic satisfaction.
- **`return true` shortcuts.** "The agent, obsessed with the immediate task, soon began to take shortcuts: `return true` is a great way to pass narrowly written tests, but probably won't generalize to the software you want" (`/`).
- **Rigid tests fail with agentic systems.** "Tests are too rigid - we were coding with agents, but we're also building with LLMs and agent loops as design primitives; evaluating success often required LLM-as-judge" (`/`).
- **Model-floor dependency.** The methodology is explicitly contingent on the late-2024 model floor ("the second revision of Claude 3.5").
- **Battle-testing is thin.** A 3-person team; the canonical pages are advocacy, not retrospective post-mortems.
- *Not directly admitted on canonical pages but flagged by secondary commentary:* shared-blind-spot hallucination loops (when judge and coder share a model class), and the recursive question of who writes the scenarios. See open questions below.

## Principles & techniques inventory

**Principles** (from `/` and `/principles`):
- **Seed**, **Validation harness**, **Feedback loop**, **Tokens as fuel** — see Executive summary.
- **Cardinal rules (homepage, verbatim):** kōan "Why am I doing this? (implied: the model should be doing this instead)"; rules "Code must not be written by humans" / "Code must not be reviewed by humans"; practical "If you haven't spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement".
- **Tokens-are-fuel representations** the engineer can convert problems into: traces, screen capture, conversation transcripts, incident replays, adversarial use, agentic simulation, just-in-time surveys, customer interviews, price elasticity testing.

**Techniques** (canonical list on `/techniques`):
- **Digital Twin Universe (DTU)** — behavioral clones at API boundaries.
- **Gene Transfusion** — exemplar-driven pattern propagation; three modes (cross-language, direct inlining, library embodiment); five-step flow.
- **The Filesystem** — on-disk state as agent memory substrate.
- **Shift Work** — separate interactive from fully-specified work.
- **Semport** — automated translation across languages/frameworks; one-time / ongoing / adaptive variants.
- **Pyramid Summaries** — reversible multi-zoom summarization (2/4/8/16 words), inspired by Pyramid TIFF and Google Maps tiles; combine with MapReduce + Clustering.

Defined upstream on the homepage rather than as techniques: **Scenarios** (out-of-codebase holdout user stories) and **Satisfaction** (probabilistic LLM-judged validation across trajectories).

**Products** (from `/products`):
- **CXDB** — self-hosted context store; turn DAG, BLAKE3 blob CAS, dynamic msgpack→JSON type system, p50 < 1ms appends, ~70% storage reduction, dual binary/HTTP protocols (ports 9009/9010), Rust+Go+React, Apache 2.0.
- **StrongDM ID** — federated identity for humans, workloads, and AI agents with path-scoped sharing.
- **Attractor** — non-interactive coding agent as a graph of phases; deterministic / observable / resumable / composable; open spec with 17+ community ports.

## Notable quotes

- "Seed → Validation harness → Feedback loop. Tokens are the fuel." — `/principles`
- "Code must not be written by humans / Code must not be reviewed by humans / If you haven't spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement." — `/`
- "Why am I doing this? (implied: the model should be doing this instead)" — `/`
- "Of all the observed trajectories through all the scenarios, what fraction of them likely satisfy the user?" — `/`
- "Code was treated analogously to an ML model snapshot: opaque weights whose correctness is inferred exclusively from externally observable behavior." — `/techniques`
- "Attractor is structured as a graph of nodes, forming a generative SDLC. … Edges between nodes are expressed in natural language and evaluated by the LLM. Execution consists of traversing this graph until convergence or termination conditions are met." — `/products/attractor`
- "We can run thousands of scenarios per hour without hitting rate limits, triggering abuse detection, or accumulating API costs." — `/techniques/dtu`
- "Summarize this bug report in 2 words. Now 4. Now 8. Now 16." — `/techniques/pyramid-summaries`
- "Those of us building software factories must practice a deliberate naivete: finding and removing the habits, conventions, and constraints of Software 1.0." — `/`
- "The OpenAI team does great work (in Python), and we receive it (in Go) and it just … works." — `/techniques/semport`

## Recommended additional sources

- The Attractor spec on GitHub (`strongdm/attractor` — referenced as "View on GitHub" from `/products/attractor`). Sibling research stream.
- The CXDB source on GitHub (`strongdm/cxdb` — Apache 2.0). Concrete reference for any factory's context-store layer.
- Luke PM, "The Software Factory" (cited in homepage footnote 1). **Drained ✅ FULL 2026-05-16 (Cluster-M manual drain)** from `research/manual/The Software Factory _ LukePM.com.txt` — short 2024-12-24 blog by Luke Moynihan; definitional / speculative; "AI Business Analyst + AI DevOps + AI QA + AI compiler" sketch; no benchmarks or architecture detail. Closes the homepage footnote-1 attribution chain. **Not a substrate-claim anchor.**
- Sam Schillace, "I Have Seen the Compounding Teams" (cited in homepage footnote 1).
- Dan Shapiro, "Five Levels from Spicy Autocomplete to the Software Factory" (cited in homepage footnote 1; Shapiro also authored the **Kilroy** Attractor port).
- Competitor factories named in homepage footnote 2: Devin, 8090, Factory (factory.ai), Superconductor, Jesse Vincent's Superpowers.
- Reference LLM-native SDKs Semport pulls from: Vercel AI SDK, OpenAI Agents SDK (`openai/openai-agents-python`).
- Notable community Attractor implementations: Fabro (Bryan Helmkamp, Rust), Kilroy (Dan Shapiro, Go), Forge (Luke Buehler, Rust), Arc (Point Labs, TypeScript — explicitly implements "convergence loops … holdout test scenarios"), and Amol Kabe's Python "multi-agent Software Factory" that names Coding/Validator/Debugger/Planner specialists.

## Open questions for synthesis

- **Scenario authorship.** Canonical pages don't say who writes scenarios. The homepage screenshot caption — "Synthetic scenario curation and shaping interface" — suggests agent-generated scenarios with human shaping, but the regress (agent-generates → agent-judges) is unresolved.
- **Judge independence.** Canonical pages don't take a position on cross-family judging or human-curated rubrics. The synthesis should.
- **Personaless design.** StrongDM collapses everything into Attractor nodes + a satisfaction judge + DTUs. What's lost / gained vs. named personas (architect, implementer, tester)?
- **NLSpec vs. structured.** "NLSpec" is a GitHub-spec term, not used on canonical pages. Position on the prose↔schema spectrum is still required.
- **Holdout discipline.** "Outside the codebase" is asserted; mechanics (separate repo? signed manifest? human-curated bank?) are unspecified.
- **$1k/day telemetry.** The floor is asserted but the surface for engineers to see token-spend live is undocumented. Per-loop / per-agent cost telemetry should be a first-class metric.
- **Model-floor coupling.** Methodology depends on "the second revision of Claude 3.5". Synthesis architectures should declare their model-capability assumptions.
- **Multi-human coordination.** Pages are silent on what happens when two humans edit overlapping scenarios or harness pieces.
- **DTU build cost.** Pages assert DTUs are "routine" but don't quantify how long the Okta/Jira/Slack/Google-Workspace twins took. This datum would calibrate any factory's harness-investment plan.
