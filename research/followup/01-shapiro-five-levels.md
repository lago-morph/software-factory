# Shapiro's Five Levels — Round-3 Follow-up Report

**Thread:** R3 Thread 1 — Shapiro's canonical 0→5 maturity model
**Date:** 2026-05-11
**Run:** fanout 20260511-054258 sub-05

---

## Source status

- **Canonical Five Levels post URL (correct slug):** https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/ — **not yet fetched.** The original WebFetch from the sandbox returned HTTP 403 (Cloudflare). A subsequent `[fetch-urls]` Action attempt (issue #29) used a guessed slug `/the-five-levels-of-agentic-coding/` which returned HTTP 404 from danshapiro.com. The correct slug above appears verbatim in the "Completely random and unrelated posts" sidebar of the companion post we *did* fetch (see next bullet); it has never been re-attempted from the Action runner. **This URL is recoverable** and should be the next fetch target.
- **Companion Shapiro post fetched (issue #29, 2026-05-13):** https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code/ — **OK**. Dan Shapiro, *"You Don't Write the Code. You Don't Read the Code Either."* (Feb 13 2026). Saved at `research/fetched/issue-29/a1966893ae_danshapiro.com__blog__2026__02__you-dont-write-the-code__.md` and now drained into this report (see "Drain note" below and the "Shapiro's companion post" section near the end). This post does **not** restate the five-level ladder, but it is a primary Shapiro source for the framework's load-bearing claims (StrongDM exemplar, three-person team, "stop reading the code", Kilroy as recommended implementation).
- **Effective primary source for the five-level ladder verbatim:** El Kaim, *The Dark Factory* (Apr 8 2026), incorporated in full into the corpus as `reference-only/dark-factory-article.txt` and digested in `research/07-dark-factory.md`. El Kaim **explicitly restates Shapiro's five-level framework verbatim** and attributes the framework to *"Dan Shapiro, drawing on the NHTSA's five-level framework for autonomous driving."* The verbatim block reproduced below is El Kaim's restatement of Shapiro and remains the closest available primary-grade material in our corpus for the ladder text itself.
- **Gap acknowledged (as of 2026-05-13, partially closed by the companion post — see "Drain note" below).** Three Shapiro-specific things our corpus did *not* contain because the original blog is blocked:
  1. Shapiro's own *named exemplars* per level (we have El Kaim's restatement, which strips exemplars). **Partially closed:** the companion post names StrongDM / Justin McCarthy's team as the canonical Level-5 exemplar in Shapiro's own voice.
  2. Any "you are at Level N if…" diagnostic heuristics Shapiro may include beyond the level descriptions. **Still open.**
  3. Whether Shapiro positions Kilroy explicitly within the level taxonomy. **Closed:** the companion post directly recommends `github.com/danshapiro/kilroy` as *"a real implementation of their software factory"* — confirming Shapiro positions Kilroy as a Level-5 (dark factory) implementation.

## Drain note (issue #29) — 2026-05-13

- The canonical Five Levels URL is **not blocked** — the Action runner reached danshapiro.com successfully for the companion post (`/blog/2026/02/you-dont-write-the-code/`). The 403 originally observed from the sandbox WebFetch is a sandbox-only restriction; an Action-runner re-fetch of the **correct** slug should succeed.
- The 404 recorded in `research/fetched/issue-29/1dde8f41c8_danshapiro.com__blog__2026__01__the-five-levels-of-agentic-coding__.html` (78 KB; `<title>Page not found – Dan Shapiro's Blog</title>`) reflects a guessed slug `the-five-levels-of-agentic-coding`, not the real slug `the-five-levels-from-spicy-autocomplete-to-the-software-factory`. The real slug was recoverable from the companion post's sidebar all along.
- **Action item for the next fetch round:** re-issue `[fetch-urls]` with `https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/` as a single-URL request. High confidence of success.
- **Remaining gaps after this drain:** Shapiro's own verbatim level text (still El Kaim-intermediated); any "you are at Level N if…" self-diagnostic heuristics; named exemplars for Levels 0–3 (the companion post only anchors Level 5).

---

## The Five Levels — verbatim (via El Kaim's restatement of Shapiro)

El Kaim attributes the framework to *"Dan Shapiro, drawing on the NHTSA's five-level framework for autonomous driving"* and reproduces it as follows:

- **Level 0 — Manual labor.** *"Every character you write is yours. You might use AI as a sophisticated search engine, occasionally tab-accepting a suggestion. The code is unmistakably human-produced. In a world of technical deflation where the cost of code drops weekly, this is manual labor in a deflationary economy. You are being outrun by the people one level above you, and the gap is compounding."*

- **Level 1 — AI intern.** *"You offload discrete, bounded tasks to the model. Write a unit test. Add a docstring. Explain this function. You retain full authorship of the important work, but you have a useful assistant for the tedious parts. You are still moving at the rate you type. The speedup is real; the paradigm shift is not."*

- **Level 2 — AI pair programmer.** *"This is where most self-described 'AI-native' developers live in 2026. You are pairing with the model like a colleague. You achieve flow states. You are more productive than you have ever been... This level is comfortable, and that is the danger. Every level from 2 onward feels like you are done. You are not done."*

- **Level 3 — Human in the loop.** *"You are no longer a senior developer. That is your agent's job. You are a manager: reviewing code, managing diffs, checking outputs, running the agent across multiple simultaneous workstreams. Your life is diffs. For many people, this level feels like things got worse... Almost everyone tops out here. It is not an exciting place to stop."*

- **Level 4 — PM mode.** *"You are not a developer. You are not a development manager. You have become what you loathed: a product manager. You write specs. You argue with the agent about specs. You plan schedules. You review plans. Then you leave for twelve hours and come back to check whether the tests pass. The primary skill at this level is spec-writing... The spec is now the most valuable thing you produce."*

- **Level 5 — The dark factory.** *"It is not a software process anymore. It is a black box that turns specs into software. Nobody writes the code. Nobody reads the code. The factory runs, the lights are off, and working software accumulates."*

**Confirmation of count.** Six bands, 0–5 inclusive — *not* five bands. The "Five Levels" title refers to the five *transitions* above Level 0 (matching NHTSA's autonomous-driving framework, which also numbers 0–5 with "five levels" of automation above the manual baseline). El Kaim attaches a concrete Level-5 team-size datum: *"The teams that have reached Level 5 are small, typically fewer than five people. StrongDM's AI team: one CTO, one senior engineering manager, one new hire less than a year out of school. Three people."*

**Load-bearing framing line** (El Kaim, summarising both Shapiro and NHTSA): *"Both frameworks describe a transition where human attention shifts from execution to oversight to strategy, and eventually becomes optional entirely."*

## Capabilities, constraints, and the "topping out" heuristic

The framework has an embedded maturity-test heuristic of the form **"if X is your daily experience, you are at Level N":**

| Level | Daily experience | Constraint | Capability ceiling |
|---|---|---|---|
| 0 | Typing your own characters; AI as search engine | Throughput equals typing speed | Linear, deflating |
| 1 | Delegating tedious tasks; retaining authorship | Throughput still ~typing speed | Marginal speedup |
| 2 | Pairing with the model; flow state | Comfort is the trap | "Feels done"; not done |
| 3 | "Your life is diffs"; managing multiple workstreams | Reviewer fatigue | "Almost everyone tops out here" |
| 4 | Writing specs; 12-hour async cycles | Spec-writing skill is the binding constraint | Throughput now bound by spec quality, not typing |
| 5 | Specs in, software out; nobody reads code | Validation must replace review | "Lights off" — observable behaviour only |

Two prescriptive claims El Kaim attaches to the ladder are worth surfacing for our architecture work:

1. *"Most teams will not reach Level 5. Most teams would benefit enormously from reaching Level 4."* The target for general-purpose factory design is **Level 4 with optional escalation to Level 5**, not Level 5 as default.
2. *"Spec-writing is the primary skill at Level 4 and above."* Any architecture aspiring beyond Level 3 must center on the spec as artefact, not on review tooling.

## Where Shapiro positions his own work

The blog post itself being blocked, we triangulate via two corpus signals:

- **Kilroy** (`github.com/danshapiro/kilroy`) — Shapiro's Go reimplementation of StrongDM's Attractor spec, published as a community port and endorsed by Jay Taylor on HN (46930913: *"if you'd like to save some tokens, you can clone my go version"*). El Kaim describes Kilroy as *"a local-first Go CLI that runs Attractor pipelines in isolated Git worktrees."* Kilroy is one of four convergent Attractor implementations (Kilroy / Mammoth / Smasher / Tracker) cited by El Kaim as evidence of an attractor-as-pattern (Layer 1 LLM Client / Layer 2 Agent Loop / Layer 3 DOT-graph Pipeline Engine).
- **DOT-graph orchestration.** Although the canonical Attractor spec is "graph-structured" generically, the *DOT-graph* convention is community-specific. Kilroy uses DOT pipelines and the community has converged on *"the engines are commodity; the pipelines are intellectual property"* (El Kaim) — i.e., the DOT file *is* the spec at Level 5.

The inference: Shapiro positions himself as a **Level 4–5 practitioner-tooler** — building the local-first runtime (Kilroy) and the meta-infrastructure (Freshell, `github.com/danshapiro/freshell`) for teams operating without code review. This is consistent with him being the framework's author rather than its critic. **We do not have a verbatim self-positioning quote** from the original post.

---

## Architecture mapping — the four architectures on the Shapiro scale

| Architecture | Default Shapiro level | Maximum reachable | Justification |
|---|---|---|---|
| **1 — Specification Refinery** | **Level 4** (PM mode) | Level 5 once spec maturity stabilises | Centres the *layered spec* as the durable artefact; Operator's review is of *diagnostic proposals* not code. Probe-and-classify discipline matches Shapiro's "you argue with the agent about specs" Level-4 description. Once a spec layer is mature and the revelation-cycle surprise rate drops, the architecture degenerates into a Level-5 dark factory for that layer. |
| **2 — Compound Atelier** | **Level 3 → 4 hybrid** | Level 4 with optional Level-5 sub-loops | The Operator *"reads synthesized findings"* and disposes residual at gates — this is Shapiro's Level-3 "life is diffs" softened by the synthesizer pre-digesting findings. Atelier's *reviewer panel* and *Human Review gate* are explicitly review-bearing, which is the Level-3 signature. It cannot ascend to default Level 5 without abandoning the panel, but specific issues can be run lights-off when the persona panel + judge consensus is unanimous. **This is the architecture closest to El Kaim's "most teams would benefit enormously from reaching Level 4" target.** |
| **3 — Phase-Gated Foundry** | **Level 3 (structurally)** | Level 4 in restricted regulated form | The Foundry's *gate chair* role is Shapiro's Level-3 manager promoted to ceremony. Phase-of-origin attribution, SRS/SAD/DD artefact rigour, and the requirement that the human *chairs every gate* keep human review in the loop by design. The Foundry can reach Level 4 by automating gate decisions with judge agents, but its regulatory pitch (FDA / FAA / ISO 26262 / SOC 2) generally precludes Level 5 — regulatory regimes *require* human accountability that Level 5 explicitly removes. |
| **4 — Evolutionary Tournament** | **Level 5 (selection-driven)** | Level 5 native; degrades to Level 4 if scenario corpus is weak | Tournament *replaces review with selection*. The human is a *Geneticist* tuning scoring weights, not a reviewer of code; the human "reads generation summaries + finalist gallery," not diffs. Predator-driven scenario generation + holdout scenarios + fitness-as-judge are the load-bearing Level-5 validation primitives ("code is the weights; scenarios are the holdout set"). The architecture's "F18 weakness" (replacing spec rigour with empiricism) is the *price of Level 5* in Shapiro's terms. |

**Cross-architecture observation.** Three of the four architectures (1, 2, 3) optimise the human's relationship to the *artefact* (spec, workpad, phase document). Only Architecture 4 optimises the human's relationship to the *selection mechanism*. This maps cleanly onto Shapiro's Level-4-vs-Level-5 distinction: Level 4 keeps the human in a high-level authoring role; Level 5 demotes them to a scoring-system tuner. Our recommended path (`00-comparison.md` §7) of **Atelier baseline + selective borrows** is therefore a recommendation to start at the Level-3↔4 boundary and add Level-5 mechanisms (Tournament-style sub-loops) only where the scenario corpus can carry the validation load.

**Caveat for the architecture-comparison doc.** The current `00-comparison.md` describes architectures by their **failure-mode coverage** and **cost shape**, both of which are level-agnostic axes. Adding a row "Default Shapiro level / Max reachable" to §2.1 would make the maturity-ladder positioning explicit and would convert the "Pick X when…" guide in §3 into a two-axis grid (failure-mode emphasis × target level). This is the most concrete actionable change from this thread.

---

## Shapiro's companion post — "You Don't Write the Code. You Don't Read the Code Either." (2026-02-13)

Source: https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code/ (drained from `research/fetched/issue-29/a1966893ae_*.md`, 2026-05-13).

This post is **not** a restatement of the five-level ladder. It is a companion essay that distils the framework into a four-step "index card" and anchors it to a named Level-5 exemplar (StrongDM). It is the primary Shapiro source we have for the framework's *exemplars and prescriptive discipline*, complementing El Kaim's restatement of the ladder text.

**The "index card" distillation — Shapiro's own four-step compression of the ladder** (verbatim):

> **First**, you recognize that, if you want to move quickly, you're not the person best qualified to be writing code anymore. The AI writes the code.
>
> **Second,** you recognize that if you're not writing the code, and you're still reviewing every pull request, *you* are the bottleneck. So you have to stop reading the code, too.
>
> **Third**, you realize this creates an enormous pile of terrifying problems. If nobody's writing code, who understands it? If nobody's reading the code, how do you know it works? How do you know it's getting better instead of worse?
>
> **Finally** — and this is the part that takes a minute to land — you realize that solving those problems is your actual job now.

Shapiro frames this as the *whole thing*: *"That's it. That's the whole thing. That's how you build a software factory. Everything else is commentary."* In ladder terms this is a compression of Levels 3 → 4 → 5: stop writing (exit L2), stop reading (exit L3), confront the validation problem (the L4 → L5 transition), make solving it the job (the L5 stance itself).

**Canonical Level-5 exemplar — StrongDM, in Shapiro's own voice.** The team-size datum that El Kaim attributes to StrongDM is **independently confirmed and named** in Shapiro's voice:

> Justin's team is three people. A CTO, a senior software engineering manager, and a new hire less than a year out of school. That team built it all — the factory, the features, the digital twin universe.

Shapiro names the CTO (Justin McCarthy), attends the on-stage reveal (*"This week he got on stage and showed it to the world. I was in the room. He was not exaggerating."*), and traces his own conversion arc back to an earlier dinner conversation about "[slot machine development](https://www.danshapiro.com/blog/2025/10/slot-machine-development/)".

**New primitives the companion post introduces** (not in El Kaim's restatement; relevant to architecture mapping):

1. **CXDB + Healer — the self-repair loop.** *"On Tuesday, they built Healer. Healer watches CXDB, develops opinions about whether agent behaviors look right, and clusters similar problems into diagnoses. Those diagnoses become investigations — and the investigations are themselves agents. An agent wakes up, looks at the cluster of bad behavior, finds the relevant code and prompts and data, and writes a prescription. The prescription gets applied. The bug gets fixed. No human filed the bug report. No human triaged it. No human wrote the fix."* This is a concrete Level-5 *validation-replaces-review* mechanism — observability layer (CXDB) + diagnostic clustering agent (Healer) + investigation agents + prescription agents — that maps directly onto our Architecture 4 (Evolutionary Tournament) selection mechanism but is described as a *closed-loop diagnostic system* rather than a generational selector.
2. **The Digital Twin Universe — testing infrastructure as a Level-5 prerequisite.** Jay (a StrongDM engineer) reproduced GSuite, Slack, Jira, Okta locally — *"faithful enough that the Python client libraries couldn't tell the difference"* — in *"a couple of weeks."* Shapiro's framing: *"Once you've realized you don't write the code, and you don't read the code, the biggest problem is quality. And the best solution to quality is testing — in the most realistic environment you can."* The digital-twin universe is Shapiro's answer to the L4→L5 validation gap. This is a substantive *prerequisite claim* not in El Kaim: **Level 5 requires a high-fidelity simulated environment of the entire SaaS surface the agents interact with.**
3. **The "Why am I doing this?" mantra — the operational discipline of Level 4/5.** *"Whenever anyone finds themselves doing something manually — reviewing logs, checking output, validating behavior — they stop and ask one question: Why am I doing this?  If you're looking at a log file and something doesn't look right, and you can articulate why it doesn't look right, you've just described a validation rule. And if you can describe it, you can automate it. So stop looking at log files. Get yourself out of the job of looking."* This is the post's most portable claim: **every manual act of inspection is an unwritten validation rule**; the L4→L5 transition is the act of systematically converting inspection into automated validation. This is the discipline that *operationally distinguishes a Level-5 team from a Level-3 team using the same tools*.
4. **"Sharpening the axe" — tools-before-product as a Level-5 budget claim.** *"Last year, 'let's spend our time on the tools before we start the product' was foolish. This year, it's more like the quote attributed to Abraham Lincoln: 'Give me six hours to chop down a tree, and I will spend the first four sharpening my axe.'"* The CXDB/Healer build (Monday/Tuesday before the release) is offered as evidence: a Level-5 team budgets a disproportionate fraction of effort to building the factory's *tooling* (observability, self-repair, digital twins) rather than the product surface.
5. **Kilroy explicitly named as a recommended implementation.** *"If you'd like to build something with a dark factory yourself, you should. There are a few options… You can try out a real implementation of their software factory at https://github.com/danshapiro/kilroy."* This closes the third gap from the original report: Shapiro positions Kilroy as a public reference implementation of the dark-factory pattern (Level 5), alongside <https://factory.strongdm.ai/> and Steve Yegge's Gas Town.

**Historical-analogy framing.** Shapiro defends the "ship code you don't read" stance via a high-level-languages analogy attributed to his father (a CS professor): *"People would complain that you had to hand-optimize the assembler. They would be horrified that you'd ship assembly code you've never read. History rhymes."* This positions "nobody reads the code" as a recurrence of the assembly→HLL abstraction shift, not a novel discontinuity.

**Implication for the architecture-mapping section above.** The companion post strengthens two claims in the existing mapping:
- Architecture 4 (Evolutionary Tournament)'s "validation replaces review" stance now has a named Shapiro-endorsed exemplar mechanism (CXDB + Healer), though the mechanism is a *diagnostic feedback loop* rather than a generational tournament. The two are compatible — Healer can be read as continuous-selection variant — but the companion post does *not* describe a population-of-candidates selection model. Tournament's specific tournament discipline remains a Tournament-specific contribution, not something Shapiro endorses verbatim.
- Architecture 1 (Specification Refinery)'s claim that "validation must replace review" at Level 5 is supported directly: Shapiro's mantra *"if you can describe it, you can automate it. So stop looking at log files."* is a near-verbatim statement of the refinery's probe-and-classify-into-spec discipline. The "Why am I doing this?" question is effectively the refinery's revelation-trigger.

## Open follow-ups

- **Verbatim Shapiro original (still open).** File a fresh `[fetch-urls]` issue for the *correct* slug: `https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/`. The companion post we drained on 2026-05-13 succeeded via the Action runner, so danshapiro.com is reachable from there — the original 404 was a slug-guess error, not a block. High confidence of success on retry.
- **Shapiro's named exemplars for Levels 0–3 (still open).** The companion post anchors Level 5 (StrongDM, three-person team, Justin McCarthy / Jay / Navan) in Shapiro's own voice but does not name exemplars for Levels 0, 1, 2, 3, or 4. These almost certainly appear in the canonical Five Levels post.
- **"You are at Level N if…" diagnostic heuristics (still open).** Neither El Kaim's restatement nor the companion post contains a compact self-diagnostic. Likely present in the canonical post.
- **Shapiro on Kilroy (closed 2026-05-13).** The companion post directly recommends `github.com/danshapiro/kilroy` as *"a real implementation of their software factory"* — confirming Kilroy is Shapiro's own Level-5 reference implementation. The inference in the "Where Shapiro positions his own work" section above is now backed by a primary-source quote.
- **CXDB / Healer / Digital Twin Universe (new, opened 2026-05-13).** The companion post introduces three concrete L4/L5 mechanisms that warrant their own follow-up: are CXDB and Healer documented publicly (e.g., at <https://factory.strongdm.ai/>)? What does the digital-twin universe imply for our architectures' validation budgets?

(Approx. 1,150 words original; ~2,300 after 2026-05-13 drain.)
