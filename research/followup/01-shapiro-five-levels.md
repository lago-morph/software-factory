# Shapiro's Five Levels — Round-3 Follow-up Report

**Thread:** R3 Thread 1 — Shapiro's canonical 0→5 maturity model
**Date:** 2026-05-11 (original) · 2026-05-13 (issue-29 drain) · 2026-05-13 (issue-36 drain — canonical primary)
**Run:** fanout 20260511-054258 sub-05

---

## Source status

- **Canonical Five Levels post (PRIMARY, NOW IN HAND):** https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/ — **✅ FULL — fetched via issue #36 with correct slug `the-five-levels-from-spicy-autocomplete-to-the-software-factory`.** Saved at `research/fetched/issue-36/c62a32953d_danshapiro.com__blog__2026__01__the-five-levels-from-spicy-autocomplete-to-the-s.md`. Title as published: **"The Five Levels: from Spicy Autocomplete to the Dark Factory"** (note: title says **Dark Factory** even though URL slug says "software factory"). Dated January 23, 2026. This report has been re-anchored to Shapiro's verbatim text in the 2026-05-13 issue-36 drain (see Drain note below).
- **Companion Shapiro post (issue #29, 2026-05-13):** https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code/ — **OK**. *"You Don't Write the Code. You Don't Read the Code Either."* (Feb 13 2026). This post does **not** restate the five-level ladder; it is a companion essay that distils the framework into a four-step "index card," anchors it to a named Level-5 exemplar (StrongDM), and explicitly recommends Kilroy. Drained into the "Shapiro's companion post" section near the end.
- **Secondary restatement (now demoted):** El Kaim, *The Dark Factory* (Apr 8 2026), `reference-only/dark-factory-article.txt` and `research/07-dark-factory.md`. El Kaim *paraphrases and embellishes* Shapiro's framework rather than reproducing it verbatim. As of the 2026-05-13 issue-36 drain, El Kaim is treated as a **secondary** convergence citation, **not** the primary text. Multiple El Kaim divergences from Shapiro's actual wording are documented in the Drain note below.

## Drain note (issue #29) — 2026-05-13

- The canonical Five Levels URL is **not blocked** — the Action runner reached danshapiro.com successfully for the companion post. The 403 originally observed from the sandbox WebFetch is a sandbox-only restriction.
- The 404 originally recorded for slug `the-five-levels-of-agentic-coding` was a slug-guess miss; the real slug `the-five-levels-from-spicy-autocomplete-to-the-software-factory` was recoverable from the companion post's sidebar all along.
- **Action item:** re-issue `[fetch-urls]` with the real slug. *(Completed in issue #36 — see next drain note.)*

## Drain note (issue #36) — 2026-05-13

The canonical Shapiro post is now in hand and this report has been **re-anchored from El Kaim's restatement to Shapiro's primary text**. Summary of changes:

**Gaps closed (vs. the three acknowledged in the prior round):**

1. **Shapiro's own named exemplars per level — CLOSED.** The exemplars are *cars and driver-assist tiers*, mirroring the NHTSA framework Shapiro draws on. Per-level: L0 = "your parents' Volvo, maybe with an automatic transmission"; L1 = "lanekeeping and cruise control"; L2 = "Autopilot on the highway" (Tesla); L3 = "a Waymo with a safety driver"; L4 = "a robotaxi"; L5 = "it's not really a car any more." There are **no per-level *team* exemplars** (StrongDM, Glowforge, etc.) named in the canonical post — only the cars. The team-naming (StrongDM / Justin McCarthy / three-person team) appears **only in the companion post**, not in the Five Levels post itself.
2. **"You are at Level N if…" diagnostic heuristics — CLOSED (no separate heuristic exists).** Shapiro does **not** ship a separate diagnostic block. The level descriptions themselves are the diagnostics, in second person ("You're writing the important stuff, but you offload specific, discrete tasks…", "Your life is diffs", "You write a spec. You argue with it about the spec."). The "if X is your daily experience, you are at Level N" table in the prior version of this report was a *reconstruction*, not a Shapiro artefact — it has been preserved below but re-labelled as a derived reading rather than a Shapiro original.
3. **Whether Shapiro positions Kilroy within the level taxonomy — CLOSED, NEGATIVE.** Kilroy is **not mentioned anywhere** in the Five Levels post. The only Kilroy positioning in Shapiro's own voice is in the companion post ("a real implementation of their software factory at https://github.com/danshapiro/kilroy"). The Five Levels post itself names **no tools or implementations** at all — except a passing mention of Claude Code at Level 4 ("you craft skills (for Claude Code, because most folks at level 4 seem to find their way to Claude Code)").

**Bonus closure — Shapiro's own self-positioning, in his own voice.** The canonical post contains a verbatim self-position that the prior version had to *infer*: at the end of the Level 4 description, Shapiro writes simply **"I'm here."** This refutes the prior report's inference that Shapiro is "a Level 4–5 practitioner-tooler" — Shapiro positions himself **at Level 4**, not at Level 5. (The Level-5 practitioners he describes as "a handful of people I know… small teams, less than five people" — i.e., other people, not him.)

**Re-anchored sections:**

- "The Five Levels — verbatim" — replaced El Kaim's paraphrase with Shapiro's actual text plus the per-level car exemplar.
- "Where Shapiro positions his own work" — replaced inference-based positioning with the verbatim "I'm here" at Level 4.
- "Capabilities, constraints, and the 'topping out' heuristic" — preserved but re-labelled as a *derived* reading; the prescriptive claims sourced to El Kaim that are *not* in the canonical post are flagged as El Kaim editorialisation.

**El Kaim vs. Shapiro discrepancies surfaced (this is the major refutation harvest):**

- **L0.** Shapiro: *"This is manual labor in a deflationary world."* El Kaim *expanded* this into: *"In a world of technical deflation where the cost of code drops weekly, this is manual labor in a deflationary economy. You are being outrun by the people one level above you, and the gap is compounding."* The "outrun by people one level above you, and the gap is compounding" claim is **El Kaim editorialisation**, not Shapiro.
- **L1.** El Kaim added the line *"The speedup is real; the paradigm shift is not."* This sentence does **not** appear in Shapiro. Shapiro's actual line is *"You're seeing speedups, but your job is unchanged. You're still moving at the rate you type."*
- **L2.** El Kaim: *"This is where most self-described 'AI-native' developers live in 2026."* Shapiro is **more specific**: *"This is where 90% of 'AI-native' developers are living right now."* El Kaim also dropped Shapiro's concrete tooling cue *"You're not using chat, you're getting real mileage out of an AI-native coding tool."* The closing warning *"Every level from 2 onward feels like you are done. You are not done"* is approximately faithful but compressed.
- **L3.** Approximately faithful. Shapiro has *"Your coding agent is always running multiple tabs. You spend your days reviewing code. So much code. Your life is diffs."* El Kaim's *"running the agent across multiple simultaneous workstreams"* is a corporate paraphrase of *"multiple tabs"*. The Waymo-with-safety-driver exemplar is dropped.
- **L4.** **Significant divergence.** El Kaim's *"The primary skill at this level is spec-writing… The spec is now the most valuable thing you produce"* does **not** appear in Shapiro. Shapiro's actual L4 description includes *"You craft skills (for Claude Code, because most folks at level 4 seem to find their way to Claude Code)"* — a concrete tool reference El Kaim dropped. The "spec is the most valuable thing you produce" claim is El Kaim's interpretive amplification, not Shapiro's wording.
- **L5.** **Most significant divergence.** El Kaim: *"Nobody writes the code. Nobody reads the code. The factory runs, the lights are off, and working software accumulates."* Shapiro's actual L5 text is *"It's a black box that turns specs into software."* The famous *"nobody writes / nobody reads"* framing comes from the **companion post**, not the Five Levels post. El Kaim collapsed the two posts. The "lights off, working software accumulates" phrasing is also El Kaim, not Shapiro.
- **StrongDM team-size attribution.** El Kaim: *"StrongDM's AI team: one CTO, one senior engineering manager, one new hire less than a year out of school. Three people."* Shapiro's Five Levels post says only *"small teams, less than five people"* and **does not name StrongDM**. The named StrongDM/Justin/Jay datum is **companion-post only**. El Kaim either cross-referenced the companion post or had separate source for the named team-size claim.
- **NHTSA framing.** El Kaim's framing line *"Both frameworks describe a transition where human attention shifts from execution to oversight to strategy, and eventually becomes optional entirely"* is **El Kaim's analytic gloss**, not Shapiro. Shapiro frames the NHTSA borrowing pragmatically: *"it let everyone have a common language for both where things were, and where things were going."* No "human attention shifts from execution to oversight to strategy" claim in Shapiro.
- **Count footnote.** Shapiro confirms in footnote 1 the prior report's "five transitions above Level 0" reading: *"Actually they made four, which was really five because it was zero-based. Then they realized they had to add a fifth. Which was actually the sixth."* This is direct Shapiro confirmation that the post is six bands (0–5) packaged as "five levels."
- **Title.** Shapiro's published title is **"The Five Levels: from Spicy Autocomplete to the Dark Factory"** (URL slug says "software-factory" but the title says **Dark** Factory). El Kaim's "Dark Factory" essay-title borrows directly from Shapiro's title.

**Implications elsewhere in the corpus** (cross-references, no edits to other reports):

- `research/07-dark-factory.md` — should note El Kaim *paraphrases* Shapiro rather than reproducing him. Particularly the L4 "spec is the most valuable thing you produce" and L5 "nobody writes / nobody reads" framings are El Kaim's compressions, not Shapiro verbatim.
- `research/strongdm/01-*.md` and `research/strongdm/02-*.md` (or wherever StrongDM is treated) — the named team-size datum (CTO + senior eng manager + junior hire) traces to Shapiro's companion post, not to the Five Levels post; the Five Levels post says only "small teams, less than five people."
- Anywhere Kilroy is referenced as "Shapiro's reference Level-5 implementation" — this attribution is supported only by the companion post; Kilroy is **not mentioned in the Five Levels post itself**.
- Anywhere our corpus says "Shapiro positions himself as a Level 5 practitioner" — refute. Shapiro explicitly positions himself at **Level 4** ("I'm here.").
- The drafting-readers list in the Five Levels post (Jesse Vincent, Justin Massa, Ramon Marc, Tenzin Wangdhen, Noah Radford) is a new lead surface — Noah Radford's "[road runner economy](https://nraford7.github.io/road-runner-economy/)" is explicitly endorsed by Shapiro and is probably a future research target.

---

## The Five Levels — verbatim (Shapiro primary, January 23 2026)

Each level is paired with a NHTSA-style **car exemplar** (the structuring metaphor of the post).

- **Level 0 — Manual labor.** Car exemplar: *"your parents' Volvo, maybe with an automatic transmission."* Shapiro: *"Whether it's vi or Visual Studio, not a character hits the disk without your approval. You might use AI as a search engine on steroids or occasionally hit tab to accept a suggestion, but the code is unmistakably yours. This is manual labor in a deflationary world."*

- **Level 1 — AI intern.** Car exemplar: *"lanekeeping and cruise control."* Shapiro: *"You're writing the important stuff, but you offload specific, discrete tasks to your AI intern. 'Write a unit test for this.' 'Add a docstring.' You could be using anything from copy-paste ChatGPT to Copilot. You're seeing speedups, but your job is unchanged. You're still moving at the rate you type."*

- **Level 2 — AI pair programmer.** Car exemplar: *"Autopilot on the highway."* Shapiro: *"As a coder, you feel free. You've got a junior buddy to hand off all your boring stuff to. This is where 90% of 'AI-native' developers are living right now. You are pairing with the AI like a colleague. You get into a flow state; you're more productive than you've ever been. You're not using chat, you're getting real mileage out of an AI-native coding tool. But here is the danger: level 2, and every level after it, feels like you are done. But you are not done."*

- **Level 3 — Human in the loop.** Car exemplar: *"a Waymo with a safety driver."* Shapiro: *"You're not a senior developer anymore; that's your AI's job. You are… a manager. You are the human in the loop. Your coding agent is always running multiple tabs. You spend your days reviewing code. So much code. Your life is diffs. For many people, this feels like things got worse. And almost everyone tops out here."*

- **Level 4 — PM mode.** Car exemplar: *"a robotaxi, and while it's driving, you can do something else."* Shapiro: *"You're not a developer. You're not a development manager either. You've now become that which you loathed: you're a PM. You write a spec. You argue with it about the spec. You craft skills (for Claude Code, because most folks at level 4 seem to find their way to Claude Code). You plan schedules. You review plans. Then you leave for 12 hours, and check to see if the tests pass."* Followed immediately by Shapiro's self-position: *"I'm here."* (Footnote: "PM" = "Program manager? Project manager? Product manager? Yes.")

- **Level 5 — The dark factory.** Car exemplar: *"it's not really a car any more."* Shapiro: *"You're not really running anybody else's software any more. And your software process isn't really a software process any more. It's a black box that turns specs into software."* On the "Dark" name: *"Maybe you've heard of the Fanuc Dark Factory, the robot factory staffed by robots. It's dark, because it's a place where humans are neither needed nor welcome."* On exemplars: *"I know a handful of people who are doing this. They're small teams, less than five people. And what they're doing is nearly unbelievable - and it will likely be our future."* (No team is named in this post.)

**Confirmation of count.** Six bands, 0–5 inclusive — *not* five bands. Shapiro confirms this directly in footnote 1: *"Actually they made four, which was really five because it was zero-based. Then they realized they had to add a fifth. Which was actually the sixth."* The "Five Levels" title refers to NHTSA's labelling convention, not the literal cardinality of the bands.

**NHTSA borrowing.** Shapiro cites the 2013 NHTSA five-levels-of-driving-automation framework directly: *"it let everyone have a common language for both where things were, and where things were going."* No deeper analytic claim about "human attention shifting from execution to oversight to strategy" appears in the post — that framing is El Kaim's gloss.

## Capabilities, constraints, and the "topping out" reading (derived)

Shapiro does **not** ship a separate "you are at Level N if…" diagnostic table. The level descriptions themselves serve as second-person diagnostics. The table below is a **derived reading** for our internal use, not a Shapiro original; it preserves the prior round's mapping but is now flagged as reconstruction.

| Level | Daily experience (Shapiro's own second-person framing) | Constraint | Capability ceiling |
|---|---|---|---|
| 0 | "Not a character hits the disk without your approval" | Throughput equals typing speed | Linear, deflating |
| 1 | "You offload specific, discrete tasks to your AI intern" | Throughput still ~typing speed | "Speedups, but your job is unchanged" |
| 2 | "Pairing with the AI like a colleague"; flow state | Comfort is the trap | "Feels like you are done. But you are not done" |
| 3 | "Your life is diffs"; "multiple tabs" | Reviewer fatigue | "Almost everyone tops out here" |
| 4 | "You craft skills"; 12-hour async cycles; "I'm here" (Shapiro self-positions) | Spec/skill craft | (No explicit ceiling claim in Shapiro) |
| 5 | "Black box that turns specs into software"; "humans are neither needed nor welcome" | Validation must replace review (not stated in this post; comes from companion) | "Nearly unbelievable" |

The two prescriptive claims previously attributed to El Kaim — *"most teams won't reach L5 / most would benefit from L4"* and *"spec-writing is the primary skill at L4 and above"* — are **El Kaim editorialisations** and not present in Shapiro's canonical post. They may still be analytically useful for our architecture work but should not be cited as Shapiro.

## Where Shapiro positions his own work

The canonical post settles this with two words. After describing Level 4 (PM mode, robotaxi), Shapiro writes: **"I'm here."** Shapiro positions himself **at Level 4**, not Level 5. The Level-5 cohort is described as other people: *"I know a handful of people who are doing this. They're small teams, less than five people."*

This **refutes** the prior version of this section, which inferred Shapiro was a "Level 4–5 practitioner-tooler" partly because he ships Kilroy. The Kilroy positioning is real and comes from the companion post (*"a real implementation of their software factory"*), but the Five Levels post itself does not cite Kilroy and does not claim Shapiro is operating at Level 5. The companion-post Kilroy recommendation should be read as Shapiro **endorsing** a Level-5 reference implementation he did not himself build at Level-5 scale, not as Shapiro positioning himself at Level 5.

---

## Architecture mapping — the four architectures on the Shapiro scale

| Architecture | Default Shapiro level | Maximum reachable | Justification |
|---|---|---|---|
| **1 — Specification Refinery** | **Level 4** (PM mode) | Level 5 once spec maturity stabilises | Centres the *layered spec* as the durable artefact; Operator's review is of *diagnostic proposals* not code. Probe-and-classify discipline matches Shapiro's "you write a spec. You argue with it about the spec" L4 description. Once a spec layer is mature and the revelation-cycle surprise rate drops, the architecture degenerates into a Level-5 dark factory for that layer. |
| **2 — Compound Atelier** | **Level 3 → 4 hybrid** | Level 4 with optional Level-5 sub-loops | The Operator *"reads synthesized findings"* and disposes residual at gates — this is Shapiro's Level-3 "life is diffs" softened by the synthesizer pre-digesting findings. Atelier's *reviewer panel* and *Human Review gate* are explicitly review-bearing, which is the Level-3 signature. It cannot ascend to default Level 5 without abandoning the panel. |
| **3 — Phase-Gated Foundry** | **Level 3 (structurally)** | Level 4 in restricted regulated form | The Foundry's *gate chair* role is Shapiro's Level-3 manager promoted to ceremony. Phase-of-origin attribution, SRS/SAD/DD artefact rigour, and the requirement that the human *chairs every gate* keep human review in the loop by design. The Foundry can reach Level 4 by automating gate decisions with judge agents, but its regulatory pitch generally precludes Level 5 — regulatory regimes *require* human accountability that Level 5 explicitly removes. |
| **4 — Evolutionary Tournament** | **Level 5 (selection-driven)** | Level 5 native; degrades to Level 4 if scenario corpus is weak | Tournament *replaces review with selection*. The human is a *Geneticist* tuning scoring weights, not a reviewer of code; the human "reads generation summaries + finalist gallery," not diffs. Predator-driven scenario generation + holdout scenarios + fitness-as-judge are the load-bearing Level-5 validation primitives. |

**Cross-architecture observation.** Three of the four architectures (1, 2, 3) optimise the human's relationship to the *artefact* (spec, workpad, phase document). Only Architecture 4 optimises the human's relationship to the *selection mechanism*. This maps cleanly onto Shapiro's Level-4-vs-Level-5 distinction: Level 4 keeps the human in a high-level authoring role (Shapiro's own seat, "I'm here"); Level 5 demotes them to a scoring-system tuner. Our recommended path (`00-comparison.md` §7) of **Atelier baseline + selective borrows** is therefore a recommendation to start at the Level-3↔4 boundary and add Level-5 mechanisms (Tournament-style sub-loops) only where the scenario corpus can carry the validation load.

**Caveat for the architecture-comparison doc.** The current `00-comparison.md` describes architectures by their **failure-mode coverage** and **cost shape**, both of which are level-agnostic axes. Adding a row "Default Shapiro level / Max reachable" to §2.1 would make the maturity-ladder positioning explicit and would convert the "Pick X when…" guide in §3 into a two-axis grid (failure-mode emphasis × target level).

---

## Shapiro's companion post — "You Don't Write the Code. You Don't Read the Code Either." (2026-02-13)

Source: https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code/ (drained from `research/fetched/issue-29/a1966893ae_*.md`, 2026-05-13).

This post is **not** a restatement of the five-level ladder. It is a companion essay that distils the framework into a four-step "index card" and anchors it to a named Level-5 exemplar (StrongDM). It is the primary Shapiro source we have for the framework's *exemplars and prescriptive discipline*, complementing the canonical Five Levels post which is structured by car/NHTSA exemplars rather than team exemplars.

**The "index card" distillation — Shapiro's own four-step compression of the ladder** (verbatim):

> **First**, you recognize that, if you want to move quickly, you're not the person best qualified to be writing code anymore. The AI writes the code.
>
> **Second,** you recognize that if you're not writing the code, and you're still reviewing every pull request, *you* are the bottleneck. So you have to stop reading the code, too.
>
> **Third**, you realize this creates an enormous pile of terrifying problems. If nobody's writing code, who understands it? If nobody's reading the code, how do you know it works? How do you know it's getting better instead of worse?
>
> **Finally** — and this is the part that takes a minute to land — you realize that solving those problems is your actual job now.

Shapiro frames this as the *whole thing*: *"That's it. That's the whole thing. That's how you build a software factory. Everything else is commentary."* In ladder terms this is a compression of Levels 3 → 4 → 5: stop writing (exit L2), stop reading (exit L3), confront the validation problem (the L4 → L5 transition), make solving it the job (the L5 stance itself). **Important:** the famous *"nobody writes / nobody reads"* framing — which El Kaim retrofitted into the L5 description in his restatement — originates **here**, in the companion post, not in the canonical Five Levels post.

**Canonical Level-5 exemplar — StrongDM, in Shapiro's own voice.** The team-size datum El Kaim attributes to StrongDM is named only in this companion post:

> Justin's team is three people. A CTO, a senior software engineering manager, and a new hire less than a year out of school. That team built it all — the factory, the features, the digital twin universe.

Shapiro names the CTO (Justin McCarthy), attends the on-stage reveal (*"This week he got on stage and showed it to the world. I was in the room. He was not exaggerating."*), and traces his own conversion arc back to an earlier dinner conversation about "[slot machine development](https://www.danshapiro.com/blog/2025/10/slot-machine-development/)".

**New primitives the companion post introduces** (not in the canonical Five Levels post; relevant to architecture mapping):

1. **CXDB + Healer — the self-repair loop.** *"On Tuesday, they built Healer. Healer watches CXDB, develops opinions about whether agent behaviors look right, and clusters similar problems into diagnoses. Those diagnoses become investigations — and the investigations are themselves agents. An agent wakes up, looks at the cluster of bad behavior, finds the relevant code and prompts and data, and writes a prescription. The prescription gets applied. The bug gets fixed. No human filed the bug report. No human triaged it. No human wrote the fix."* Concrete Level-5 *validation-replaces-review* mechanism — observability layer (CXDB) + diagnostic clustering agent (Healer) + investigation agents + prescription agents.
2. **The Digital Twin Universe — testing infrastructure as a Level-5 prerequisite.** Jay (a StrongDM engineer) reproduced GSuite, Slack, Jira, Okta locally — *"faithful enough that the Python client libraries couldn't tell the difference"* — in *"a couple of weeks."* Shapiro's framing: *"Once you've realized you don't write the code, and you don't read the code, the biggest problem is quality. And the best solution to quality is testing — in the most realistic environment you can."* **Level 5 requires a high-fidelity simulated environment of the entire SaaS surface the agents interact with.**
3. **The "Why am I doing this?" mantra — the operational discipline of Level 4/5.** *"Whenever anyone finds themselves doing something manually — reviewing logs, checking output, validating behavior — they stop and ask one question: Why am I doing this?  If you're looking at a log file and something doesn't look right, and you can articulate why it doesn't look right, you've just described a validation rule. And if you can describe it, you can automate it. So stop looking at log files. Get yourself out of the job of looking."* **Every manual act of inspection is an unwritten validation rule**; the L4→L5 transition is the act of systematically converting inspection into automated validation.
4. **"Sharpening the axe" — tools-before-product as a Level-5 budget claim.** *"Last year, 'let's spend our time on the tools before we start the product' was foolish. This year, it's more like the quote attributed to Abraham Lincoln: 'Give me six hours to chop down a tree, and I will spend the first four sharpening my axe.'"* A Level-5 team budgets a disproportionate fraction of effort to building the factory's *tooling* (observability, self-repair, digital twins) rather than the product surface.
5. **Kilroy explicitly named as a recommended implementation.** *"If you'd like to build something with a dark factory yourself, you should. There are a few options… You can try out a real implementation of their software factory at https://github.com/danshapiro/kilroy."* Note: this is the **only** Kilroy positioning in Shapiro's voice across both posts. The canonical Five Levels post does not mention Kilroy.

**Historical-analogy framing.** Shapiro defends the "ship code you don't read" stance via a high-level-languages analogy attributed to his father (a CS professor): *"People would complain that you had to hand-optimize the assembler. They would be horrified that you'd ship assembly code you've never read. History rhymes."* This positions "nobody reads the code" as a recurrence of the assembly→HLL abstraction shift, not a novel discontinuity.

**Implication for the architecture-mapping section above.** The companion post strengthens two claims in the existing mapping:
- Architecture 4 (Evolutionary Tournament)'s "validation replaces review" stance now has a named Shapiro-endorsed exemplar mechanism (CXDB + Healer), though the mechanism is a *diagnostic feedback loop* rather than a generational tournament. The two are compatible — Healer can be read as continuous-selection variant — but the companion post does *not* describe a population-of-candidates selection model. Tournament's specific tournament discipline remains a Tournament-specific contribution, not something Shapiro endorses verbatim.
- Architecture 1 (Specification Refinery)'s claim that "validation must replace review" at Level 5 is supported directly: Shapiro's mantra *"if you can describe it, you can automate it. So stop looking at log files."* is a near-verbatim statement of the refinery's probe-and-classify-into-spec discipline. The "Why am I doing this?" question is effectively the refinery's revelation-trigger.

## Successor framing — Shapiro's "Completion, Chat, Agent, Claw" (May 13 2026)

Shapiro published a **successor taxonomy** on May 13 2026: *"Completion, Chat, Agent, Claw"* (https://www.danshapiro.com/blog/2026/05/completion-chat-agent-claw/), drained as **`research/32-shapiro-completion-chat-agent-claw.md`**. It is *not* a restatement of the Five Levels; it is a parallel, compositional sub-taxonomy on an orthogonal axis. Where the Five Levels are an *operator-position* ladder (where the human sits), the Claw ladder is a *capability-composition* ladder (what the agent is made of): **Chat** = stacked completions; **Agent** = chat + tools + loop ("LLMs using tools in a loop", which Shapiro credits to Simon Willison verbatim); **Claw** = agent + memory + goals + autonomy. The Allie-Miller refactor recorded in the post (*"memory is the tool, not the impact"*) names self-improvement-toward-operator-goals as the load-bearing differentiator between an Agent and a Claw — the same pattern Schillace coins as *"gene transfer"* in his Sunday Letter #10 (per `research/28-schillace-sunday-letters.md` §3.4).

Mapping onto the Five Levels: Completion ≈ L0; Chat ≈ L1; Agent ≈ L2/L3; Claw ≈ L4/L5 — with the strong reading that **the Claw is the substrate that L5 runs on** ("the black box that turns specs into software" *is* a Claw-class system applied to software production). The Claw post is silent on Shapiro's self-position; the operational anecdote (claw printer, "first one deployed today") is consistent with L4 → L5 motion in the personal-operations vertical while remaining L4 for code (StrongDM remains his named L5 exemplar). See report 32 §7 for the full mapping and §6 for the *one-Claw-per-employee / claw-printer* org-design primitive — corpus-novel and the supply-side peer of Sendbird's per-employee quests + token tiers (forthcoming report 36).

## Open follow-ups

- **Verbatim Shapiro original (CLOSED 2026-05-13 via issue #36).** The canonical Five Levels post is now in hand. All three previously-acknowledged gaps are closed (see Drain note above).
- **Shapiro's named *team* exemplars for Levels 0–3 (unresolvable in the canonical post).** The Five Levels post structures its exemplars as cars/NHTSA tiers, not teams. There are no per-level team exemplars to find — the framework was authored without them. The only team exemplar is the unnamed L5 cohort ("a handful of people I know… less than five people"); the named StrongDM team comes from the companion post.
- **Drafting-readers list — new lead surface.** The Five Levels post thanks Jesse Vincent, Justin Massa, Ramon Marc, Tenzin Wangdhen, and Noah Radford for reading drafts. Noah Radford's "[road runner economy](https://nraford7.github.io/road-runner-economy/)" is explicitly endorsed by Shapiro and is a candidate research target for the broader corpus. **Update 2026-05-16:** Jesse Vincent's assistant reappears in the Claw post (§4 of report 32) as the corpus' first concrete "dreaming" exemplar — an assistant given the goal *"Every night, research things that might help it do its job"* that taught itself to read ADHD literature unprompted. Worth treating Jesse Vincent as a named research target now, not just a draft-reader name.
- **CXDB / Healer / Digital Twin Universe (still open from 2026-05-13).** Are CXDB and Healer documented publicly (e.g., at <https://factory.strongdm.ai/>)? What does the digital-twin universe imply for our architectures' validation budgets?
- **Title-vs-slug discrepancy (cosmetic).** Shapiro's published title says "Dark Factory" but his URL slug says "software-factory." Both are valid Shapiro framings; "dark factory" is the term that propagated to El Kaim and beyond.

(Approx. 1,150 words original; ~2,300 after 2026-05-13 issue-29 drain; ~3,700 after 2026-05-13 issue-36 drain; ~4,050 after 2026-05-16 Cluster-K successor-framing addition.)
