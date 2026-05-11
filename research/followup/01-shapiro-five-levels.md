# Shapiro's Five Levels — Round-3 Follow-up Report

**Thread:** R3 Thread 1 — Shapiro's canonical 0→5 maturity model
**Date:** 2026-05-11
**Run:** fanout 20260511-054258 sub-05

---

## Source status

- **Primary URL:** https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/ — **BLOCKED (HTTP 403)** from the sandbox WebFetch. Wayback (`web.archive.org`) is also unreachable from the sandbox.
- **Effective primary source used:** El Kaim, *The Dark Factory* (Apr 8 2026), incorporated in full into the corpus as `research/manual/The Dark Factory How Software Is Le.txt` and digested in `research/07-dark-factory.md`. El Kaim **explicitly restates Shapiro's five-level framework verbatim** and attributes the framework to *"Dan Shapiro, drawing on the NHTSA's five-level framework for autonomous driving."* The verbatim block reproduced below is El Kaim's restatement of Shapiro and is the closest available primary-grade material in our corpus. The Shapiro original is also a co-source of the Dark Factory framing (`research/05-simon-willison.md` confirms Simon Willison cites this exact URL).
- **Gap acknowledged.** Three Shapiro-specific things our corpus does *not* contain because the original blog is blocked:
  1. Shapiro's own *named exemplars* per level (we have El Kaim's restatement, which strips exemplars).
  2. Any "you are at Level N if…" diagnostic heuristics Shapiro may include beyond the level descriptions.
  3. Whether Shapiro positions Kilroy explicitly within the level taxonomy (we know from HN 46930913 that Shapiro published Kilroy as an Attractor port; we infer but cannot confirm he places himself at Level 4/5).

A follow-up `[fetch-urls]` issue would be required to retrieve the canonical Shapiro post; the existing `research/blocked-urls-round-2.md` already lists `danshapiro.com` as Cloudflare-gated. This report proceeds from the El Kaim restatement, which is sufficient for the architecture-mapping task.

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

## Open follow-ups

- **Verbatim Shapiro original** — file `[fetch-urls]` issue for `danshapiro.com/blog/2026/01/the-five-levels-...` and the companion `danshapiro.com/blog/2026/02/you-dont-write-the-code/` (also cited in `07-dark-factory.md` references and likely contains additional level commentary).
- **Shapiro's named exemplars** — almost certainly present in the original post but absent from El Kaim's restatement; would let us anchor each level to a public team/project beyond Level 5's StrongDM.
- **"You are at Level N if…" diagnostic heuristics** — only partially reconstructible from El Kaim. The original may carry a more compact self-diagnostic.
- **Shapiro on Kilroy** — confirm whether the original post names Kilroy as Shapiro's own Level-N exemplar; this would let us cite a self-positioning quote rather than infer.

(Approx. 1,150 words.)
