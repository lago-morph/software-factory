# Report 28 — Schillace's Sunday Letters: Attention, Harnesses, and the Agent-Shaped World

**Themes:** human-attention-as-scarce-resource · harness engineering (non-OpenAI canonical voice) · compounding teams · agent-shaped surfaces · last-mile problem · meta-cognitive code
**Date:** 2026-05-16
**Author:** Subagent I (manual-drain dispatch, Cluster I)
**Status:** ✅ FULL — all 11 primary sources drained from manual `research/manual/` capture on 2026-05-16; two MHTML originals kept for embedded diagrams (Schillace's four-panel "What is a harness?" architecture and the hand-drawn "Recipe for Building in the Semantic Era").
**Source count:** 11 (9 substack TXT + 2 substack MHTML w/ corpus-canonical diagrams)
**Primary themes touched:** 1 (attention as scarce resource), 4 (harness / substrate), 6 (engineering practice in the new paradigm), 7 (agents as team members)

---

## 1. Why a super-report

Sam Schillace is one of two practitioner voices in the corpus who has shipped a working harness at scale (Microsoft Amplifier; OpenSource on GitHub) **and** writes weekly about the practice. The other is Simon Willison (report 05). His Sunday Letters Substack has accumulated, across late 2025 through May 2026, a tight set of eleven pieces that move from observation ("I have seen the compounding teams") through definition ("What is a harness and why do I care?") into framework critique ("Artisans and Factory Lines"). The orchestrator decision (`research/manual/new-index.md` row 2) was to land these eleven pieces as a single super-report rather than three smaller theme-anchored reports, on the grounds that the same author, the same Microsoft-internal first-person viewpoint, and the same recurring metric (output per unit of human attention) runs through all of them; fragmenting across three reports would have triple-counted the same voice and obscured the cross-letter conceptual arc.

Schillace's role and biography matter for source weighting. He is currently Microsoft CTO of the Application Innovation organization (previously Deputy CTO of the office of the CTO at Microsoft); before that he was the co-founder of Writely (which became Google Docs) and the founder of Box's Skype-era product organization. He named Semantic Kernel "on a whim, as a code name" (his words, footnote 1 in *What is a harness*) and the name survived. His team at Microsoft is the team of authors behind **Amplifier**, the open-source Microsoft agentic harness. The eleven letters draw on his direct daily experience operating that harness — eight or nine concurrent agent runs at a time, a 12-person team with over 500 projects, and "compounding teams" he personally tracks across the valley.

**The eleven letters in chronological order** (publication dates per the substack header):

| # | Date | Title | Anchor concept |
|---|---|---|---|
| 1 | 2025-09-28 | *I have seen the compounding teams* | Field sighting of 2–3 valley teams that have stopped writing code and instead build a custom Amplifier-shaped framework around a model; recursive build-a-tool-for-making-a-tool; **code review as "a firing offense"**; 5–10 parallel processes; hundreds of dollars/day API spend |
| 2 | 2026-01-04 | *How it will happen* | Code crossed a 2025 tipping point; advanced teams that don't read code at all; the same curve about to repeat across knowledge work via "meta-orchestration" tools |
| 3 | 2026-01-11 | *Attention and collaboration in the AI world* | 3-person teams that feel like 30-person teams; each human saturated managing 5–10 concurrent agents; Jevon's paradox on attention-management tools; norms for centering/de-centering the tool |
| 4 | 2026-01-18 | *The hard part isn't doing the work now; it's choosing the work* | Bottleneck shifted from doing to choosing; "Why Not / What If" innovation framing; "Internet Stages" maturation analogy; taste-and-judgment as the durable skill |
| 5 | 2026-02-08 | *The one scarce resource AI can't replace* (URL slug: `laundry-lists-and-building-blocks`) | Mass-audience software (books) vs transient AI-generated software (shopping lists); agent-OS building-block list (github / markdown / html / yaml / python / rust / go); **"Attention Firewall"** as a concrete tool |
| 6 | 2026-02-15 | *Attention is all ya got* | The "output per unit of human attention" metric; Warren-Buffet / working-stiff / lottery-winner user typology; Harvard study showing agentic coding can *increase* workload; "always smart/productive" expectation analogous to "always on" |
| 7 | 2026-02-22 | *The agent-shaped world* | Shipping-container thesis; surfaces-to-grab-onto enumeration (iterable data, decomposed observable steps, machine-navigable docs, machine-drivable interfaces, recursive self-process audits); Borders / newspapers analogy |
| 8 | 2026-04-05 | *AI and the marshmallow test* | New tech-debt species — code functionally correct but poorly thought-out because the human kicked off an agent without disciplining intent; use the model itself to pressure-test the plan before any code runs |
| 9 | 2026-04-26 | *Machine with Concrete* | Amplifier internals — architecture experts, "session analyzers", **Dev Foundry**, **Crusty Old Engineer** critic; 100+ GitHub repos but little ships → **last-mile problem**; 12-person team / >500 projects |
| 10 | 2026-05-03 | *What is a harness and why do I care?* (KEPT MHTML) | First-person definition of a harness — Semantic Kernel lineage; Context Query; subagents; containers; **recipes (yaml workflows)**; external memory management; self-improving experts (session analyst, foundation expert, Crusty Old Engineer); names the pattern **"gene transfer"** |
| 11 | 2026-05-10 | *Artisans and Factory Lines* (KEPT MHTML) | Senior engineers reflexively wrap LLMs in deterministic code — the "tempting wrong hybrid"; code should retreat from cognitive to **meta-cognitive** scaffolding; five ingredients + four-step method |

The arc is recognisable. (1) sighting → (2)–(7) thesis-building around attention and shape → (8)–(9) failure modes as the practice matures → (10) the canonical harness definition once the term "harness engineering" has settled into industry use → (11) the framework-critique closing piece arguing the new paradigm needs new engineering, not deterministic-era patches. Several letters reference earlier ones explicitly ("I wrote last week about the emerging pattern of intense, agentic coding"; "I wrote about this last week and I can say — it's only getting worse!"). This super-report preserves the cross-letter linkage by clustering by thesis rather than by letter.

---

## 2. The attention thesis

The load-bearing claim across letters (5), (6), (3), and (4) is that **human attention is the binding constraint** on AI-augmented work, and the load-bearing *metric* is **output per unit of human attention** (Schillace's exact phrase, from *Attention is all ya got*). Three reinforcing arguments build the thesis.

**Argument 1 — Impedance mismatch (letter 6).** Two humans cannot exhaust each other because both have a roughly comparable daily quota of cognitive output (humans-with-staff aside). AI does not have that quota. *"AI attention scales, though — all you have to do is ask for more, and you get it. So it's very easy for the AI to overwhelm the human — now there's an impedance mismatch."* The human becomes the rate-limiting reagent in a system where the cheap reagent (model attention) is now effectively unbounded.

**Argument 2 — Three user-classes (letter 6).** Schillace draws a financial-compounding analogy that is the most quotable framing in the eleven letters:

- **Warren-Buffet users** invest their attention in tools that build more tools — they get leverage on the leverage, and the system compounds.
- **Working-stiff users** spend attention task-by-task — net-flat, no compounding.
- **Lottery-winner users** use AI to make more work for themselves and burn out — *"using AI to exhaust yourself without building leverage along the way."* Schillace's exact phrase for the failure case is "attentional bankruptcy."

The Harvard study he cites (uncited by name in the letter, but characterised as "out right now about how it can actually increase workload") is the empirical anchor for the lottery-winner failure case. Whether or not the citation resolves cleanly, the typology lands.

**Argument 3 — The "always smart" expectation (letter 6).** The internet's "always on" expectation eroded work/life boundaries because servers were always reachable. Schillace's symmetric prediction: *"AI is now setting the expectation of 'always smart/productive'. If you can always be reached, why aren't you reachable? If you can always be smart and do 100x the work with AI, why aren't you doing 100x the work, at high speed?"* This is the anti-human-pattern axis of the attention thesis — even users who *would* be Warren-Buffet-style compounders are pulled into lottery-winner behaviour by peer-set expectations and self-imposed ambition.

**Argument 4 — Jevon's paradox on attention-management tools (letter 3).** The natural response — build tools to manage the attentional load — runs into the Jevon paradox. *"We probably will continue to try to build tools to manage the attentional load, but I suspect we'll run into Jevon's paradox here: we are likely to keep ourselves saturated no matter how good the tools get."* Better attention-management tools just raise the attention budget, which raises the agent-count ceiling, which re-saturates. Schillace does not claim this is an iron law, only that the empirical pattern across the teams he sees is consistent with it.

**Argument 5 — Choosing-the-work as the residual scarce skill (letter 4).** *"It's not hard to do work now, it's hard to pick what work to do. I suspect this is a deep truth of the AI age — as agents get more powerful and cheaper, the actual mechanics of the work will matter less. What will matter is the taste and judgment of deciding what to do."* The analogy is calories: as food got cheap, the scarce skill became deciding what and how much to eat. As thinking gets cheap, the scarce skill becomes deciding what to think about.

**Cross-corpus impact.** The attention thesis is the corpus' Theme-1 ("human attention is the substrate constraint") stated in its sharpest practitioner-voice formulation. Up to this report, Theme-1 has been anchored on Willison's "3-tier summary discipline" (report 05) and Cherny's "five-agents-steady-state" (followup/03). Both of those are tactical — discipline-and-cadence prescriptions. Schillace's contribution is the **economic statement of the underlying constraint**: attention is the scarce resource, all the tactical prescriptions exist to optimise for it, and the system-wide compounding outcome depends on how the scarcity is managed. Recommended absorption into the synthesis is in §10 below.

---

## 3. Three-person teams that feel like thirty

Letters (3), (1), and (9) carry the team-shape argument. The core observation is from (3) — Schillace works with valley teams using Claude Code and Amplifier, and the productive ones stay at *no more than three humans*, with each human running 5–10 concurrent agents.

> *"It's almost as if a 3-person team is really a 30-person team, because of all of the agents involved. In fact, that's how it feels."*

The first-order explanation is throughput — agents add productive capacity, so smaller human teams produce more. Schillace explicitly rejects that as insufficient and offers a second-order explanation in letter (3): **collaboration overhead saturates first.** Each human has near-fully-allocated attention managing their own agents. Two such humans trying to collaborate need *spare* attention to generate and consume the interaction, and neither has any. Each additional human multiplies the attention deficit. *"It feels exactly like managing a large group of people, except in this case, it's very easy to add agents to the mix, so you wind up with a lot of them."* (3)

The empirical sightings are in letter (1) — the *I have seen the compounding teams* essay:

- The teams compounding aren't writing code at all. They've built a framework (Amplifier-shaped) around a model with **callback hooks, tool calling, and flow control**, plus an additional layer of "strategies, tools, opinions and behaviors" that lets the system run more independently.
- All of them use **low-level programming tools to give the system access to itself**: filesystem-based; git; markdown; kubernetes; xml. Schillace's prediction: "the next wave of software at scale will be built on these programmer tools, even for non-programmers, the same way models will sometimes privately write code now to solve a hard problem asked by a non-coder."
- The compounding comes from a *recursive* mindset: **"build a tool for making a tool"**. The agents are told "you'll need a tool for that, go ahead and build and use it" and they do — checking the tool into git and making it a permanent improvement.
- **5–10 parallel processes** is the steady-state count.
- API spend is "routinely hundreds of dollars a day (one team has a goal of getting to a thousand)."
- **"Code review is a firing offense"** — in the sense that if a human is reading the code, they're now the bottleneck. *"I know teams with shipping products that have not directly touched or looked at code in multiple months (one jokingly considers a code review a 'firing offense' because it means you're in the way of the tool)."*

Schillace also flags two operational consequences worth quoting verbatim because they directly contradict default human-team practice:

- *"It's much better to have two or three engineers who can design at this high level, working on well-defined but isolated pieces of functionality, than it is to have a large, mixed team."*
- *"It's hard to have some team members coding like this and others coding by hand, and it's impossible to mix that in one repo."* — i.e. the operating-mode transition is per-repository, not per-engineer; mixed practice doesn't just slow the agentic engineers, it makes the repo itself untenable.

Letter (9) — *Machine with Concrete* — provides the scale anchor that closes the team-shape argument: **Schillace's own 12-person team has built over 500 projects.** This is far past any conventional ratio (one engineer can sustain ~3–5 active projects in their head). The 500-projects number is not a productivity boast; the letter is framed as a problem ("it's hard even to understand with the help of AI") — Schillace is using it to motivate the *coordination* problem that comes after the throughput problem is solved.

**Cross-corpus impact.** Schillace's "3 humans = 30 people" anchors the corpus' Theme-7 ("agents as team members") with a Microsoft-internal data point alongside Anthropic (report 23) and Every (reports 03/04). It also corroborates Cherny's "five-agents-steady-state" claim (followup/03) — Cherny's five is per-Cherny; Schillace's eight or nine (letter 3 footnote: "as I write this, I have 9 open Amplifier agents working") is per-Schillace; the order of magnitude matches and the "human attention saturates around N=5–10 concurrent agents" generalisation now has two independent practitioner data points.

---

## 4. The harness definition — with the canonical diagram

The corpus has, until this report, anchored "harness" on OpenAI's *Harness engineering* essay (report 18 §5; Ryan Lopopolo, Feb 2026) and on Jaymin West's Ch 6 / Raschka-component decomposition (report 09 §1). Schillace's *What is a harness and why do I care?* (letter 10, May 2026) is the third corpus-canonical anchor, and importantly the *non-OpenAI, non-academic* one — written for a general technical audience in first person from inside Microsoft Amplifier.

The four-panel diagram embedded in the post is the canonical visual:

![What is an AI Harness? — Schillace's four-panel architecture diagram](figures/28-schillace-sunday-letters/what-is-a-harness-four-panel.png)

*Schillace's "What Is an AI Harness?" diagram (Sunday Letters, 2026-05-03). Top row, left to right: (1) **Start with a model** — the harness begins by calling the model directly through an API; (2) **The harness orchestrates** — instead of just asking once, the harness can plan, loop, dedupe, and use tools (yaml "recipes" + Context Query labelled inset); (3) **It manages memory and context** — models don't form new memories, so harnesses keep external memory and context organised; (4) **It compounds** — as models improve, the harness keeps adding tools (Programs, Books, Complex systems icons); a "Crusty Old Engineer" agent icon appears in this panel. Bottom strip — "The full picture": Models → Tools → Data connectors → Memory systems → Harnesses, with the caption "AI is not one single thing: harnesses orchestrate the rest into a more effective system."*

The post's prose definition unpacks each panel.

**Panel 1 — Start with a model.** The harness wraps the API surface (not the chat surface), giving programmatic control over temperature, streaming, and tool invocation. Schillace lineages this to his own team's first project, the *orchestrator* — *"ours was (and still is) called Semantic Kernel."* The connection to Microsoft Semantic Kernel as the proto-harness is corpus-novel; we have until now treated Semantic Kernel as a separate orchestration framework rather than as an early instance of the harness category.

**Panel 2 — The harness orchestrates.** Beyond single-call orchestration, the harness can:

- **Context Query** — the first request is a set of questions returned in XML with each labelled (`fact` / `unknown` / `needs-web-lookup` / etc.); the second pass either answers directly if known, or invokes a tool. *"It cut down on hallucinations."* This is one of Amplifier's two named tactical patterns surfaced in the eleven letters.
- **Subagents and containers** — a model can create a subagent and hand off work, or spawn a whole container that isolates work into a new virtual environment.
- **Recipes** — yaml-based workflow definitions that orchestrate "long, complex tasks." Schillace mentions building a recipe he calls a *foundry* "that is capable of writing books in my voice" using custom-model judges, linguistic-analysis tools, and "custom editing workflows that interact with me."

**Panel 3 — It manages memory and context.** *"Even though an AI model seems like a person sometimes, it doesn't really have the same kind of mind as a person does — in particular, it can't form new memories."* The harness's job is to keep the externally-managed memory store in good shape so that context-passing across turns approximates what continuous memory would have done. Multiple approaches; Schillace doesn't enumerate them but flags context-quality as "a hard problem."

**Panel 4 — It compounds.** *"The harness builds tools, [so] it gets better at building the next ones. And the models get smarter, so they get better at writing code and using the tools, and the harness can take advantage of that."* This is the Amplifier-specific compounding claim — over time, *"we've gone from very simple tools like Context Query, to the current ones that are building programs, books, and more complex systems and artifacts over days or even weeks, with little or no supervision."*

**The "gene transfer" coinage.** The mechanism by which the harness self-improves is named in letter 10. Amplifier has two self-improving experts (or "tools, depending on how you look at them"):

- **Session analyst** — "a tool [Amplifier] can use to look at other harness sessions and understand how they work." Schillace flags that this is hard because a large session's token count can exceed the model's own context window: "it's a little like reading out of the corner of your eye — has to be done carefully."
- **Foundation expert** — "understands how the system itself is put together."

Together, *"these can often look at a new capability, another codebase, or even a research paper, and work together to add new capabilities to the harness itself. Others have called this 'gene transfer' and it works surprisingly well."* This is Schillace coining (or popularising) the term for the corpus' Theme-2 mechanism of cross-system capability propagation. The fact that he attributes it to "others" rather than himself is unusual — and the corpus has previously seen the phrase only in a single mention in report 01-strongdm-factory. Schillace's adoption of the term in letter 10 is the first instance in the corpus where "gene transfer" appears at the *primary-source* level as a named harness pattern.

**The "Crusty Old Engineer" critic subagent.** Letter 10's first footnote-grade aside is that Amplifier has a third self-improvement-class subagent: *"a 'Crusty Old Engineer' is my absolute favorite — a cynical engineer agent that gives really good design advice."* The Crusty Old Engineer recurs across letter (9), letter (10), and the diagram itself (visible in Panel 4). It is the *adversarial-critic* role in Schillace's harness — the equivalent of OpenAI's `Auto-review` subagent (report 18 §4.4) or the "predator agent" in Arch 4 of the architecture comparison (report 09 §5.5). The role taxonomy in the corpus now has a third name for the same pattern; the synthesis should consolidate.

**The book-foundry caveat.** The post's second footnote is unusually candid: *"Don't worry — this turns out to be an incredibly hard problem. I can get close to good writing, but it feels a bit like Xeno's paradox — it's hard to see how we can ever get all the way there. Real, authentic writing is HARD."* Useful epistemic anchor for the corpus — the head of Amplifier's product organization is openly stating that the prose-writing-foundry use case is not solved and may not be soluble with current methods. Compare to Willison's "97% is a failing grade" doctrine in report 05.

---

## 5. Amplifier internals

Letters (1), (9), (10) and (11) collectively surface a richer picture of Amplifier than the corpus has previously held. Until this drain, Amplifier was named once in followup/06 as a "sibling framework to Superpowers" (Jesse Vincent's mention) and once in report 01 as a secondary StrongDM cross-reference. The internals listed below are now anchored.

**Architecture experts** (letter 9) — domain-specialist subagents that the harness can invoke for design and code decisions. Schillace doesn't enumerate; "architecture experts" is the role name and the role is plural.

**Session analyzers / "session analyst"** (letter 10) — reflective subagent that reads past session transcripts to extract patterns for harness self-improvement. The "reading out of the corner of your eye" simile in letter 10 makes explicit that this is *not* whole-transcript ingestion; it's a context-window-disciplined skimming protocol. Cross-references the corpus' "decision log + trajectory capture" primitives in architectures/00-comparison.md §4.1.

**Dev Foundry** (letter 9) — *"a 'dev foundry' that I built that stamps out bespoke 'dev machines' that can work on tasks for days or weeks on their own."* This is the corpus' first sighting of a *bespoke-environment-stamping* pattern in a shipping harness. The closest analogs are Devin's "Managed Devins" (followup/06 §1), Factory's "Droid Computers" (followup/06 §3), and OpenAI's harness-fleet model from `running-codex-safely` (report 18 §4.4); Dev Foundry sits semantically in the same category but is named for its *factory-side* role (stamping out) rather than its *agent-side* role (Droid / Devin / Codex agent).

**Crusty Old Engineer** (letters 9, 10) — adversarial-critic subagent. See §4 above.

**Foundation expert** (letter 10) — meta-cognitive subagent that understands the system itself; paired with session analyst to do gene-transfer self-improvement.

**Recipes (yaml workflows)** (letter 10) — the named workflow primitive. yaml-based; orchestrates multi-step model calls with tool selection. A "recipe" can grow into a "foundry" (Schillace's book-writing-foundry is a "large recipe"). This is one of two patterns Schillace explicitly names for Amplifier; the other is Context Query.

**Context Query** (letter 10) — XML-categorised question-answering pattern: question → labelled XML categories → conditional second-pass answer-or-tool-invoke. Schillace explicitly credits this with hallucination reduction.

**Callback hooks + tool calling + flow control** (letter 1) — the underlying control primitives, attributed not to Amplifier specifically but to the framework category. Amplifier's specific implementation is implied to be conventional.

**Filesystem / git / markdown / kubernetes / xml as substrate** (letter 1) — explicit. Schillace describes this as the "infrastructure for model-based action" because the models are "so successful using" these tools. Direct support for the corpus' substrate-stack recommendation (report 13 §3) and Jaymin's BMAD agent-as-code framing (report 09 §3).

**Self-improving "gene transfer" loop** (letter 10) — session analyst + foundation expert can ingest *"another codebase or paper"* and graft capabilities into Amplifier itself. The fact that *research papers* are listed as ingest targets is notable — the harness can absorb academic methodology directly, not just code.

**Token budget — internal Microsoft** (letter 9) — *"Microsoft gives us a generous token budget — this is expensive!"* No dollar figure; just acknowledgement that the operating model is not subscription-priced and the team is running on a corporate budget. Compare to Schillace's separate cite in letter (1) of "hundreds of dollars a day" for the valley teams he tracks; Microsoft's internal budget is implied to be larger.

**Open-source status** (letter 10) — Amplifier is "open source on GitHub." This corroborates the followup/06 mention (`github.com/microsoft/amplifier`).

---

## 6. Artisans and factory lines — with the diagram

Letter 11 (*Artisans and Factory Lines*, May 2026) is the framework-critique closing piece. It argues a *failure mode* common to senior engineers and offers a counter-framework. The hand-drawn diagram is the corpus' most teaching-friendly visual on the syntactic↔semantic boundary.

![Recipe for Building in the Semantic Era — Schillace's syntactic-vs-semantic diagram](figures/28-schillace-sunday-letters/artisans-recipe-for-semantic-era.png)

*Schillace's "Recipe for Building in the Semantic Era" diagram (Sunday Letters, 2026-05-10). Three panels across the top: **The Old World — Deterministic Factory** (rigid, precise, predictable; "If it's not specified, it doesn't exist"); **The Tempting Wrong Hybrid** (a man with too-many-patches wrapping an LLM in rule engines, validators, guard rails, schema enforcers, policy filters — caption: "TRAP: trying to escape randomness by wrapping the model in code"); **The New World — Semantic Foundry** (an LLM as a cauldron handling messy, real-world input — nuance, intent, context, exceptions, meaning first). **Five INGREDIENTS** down the left edge: 1. Syntactic code (gears, checklists, tables; APIs, protocols, schemas), 2. Determinism (exact, repeatable, identical parts; same result every time), 3. Semantic reasoning (LLM handles messy real-world meaning), 4. Stochastic behaviour (flexibility, creativity, less perfect predictability), 5. **Meta-cognitive code** (the foreman's clipboard — observes, plans, routes work, remembers, evaluates; separate from the LLM brain). **METHOD: FOUR SIMPLE STEPS** centred on the page: (1) Decide clearly what belongs inside the model and what belongs in code? (2) Stay in the semantic world when the task depends on meaning, nuance or exceptions; (3) Use code for meta-cognitive scaffolding — control, memory, orchestration, evaluation; (4) Invent native engineering patterns instead of recreating expert systems by hand. Chef's notes at the bottom: the old world was brittle but predictable; the new world is powerful and probabilistic; real progress comes from understanding the new paradigm on its own terms.*

**The failure mode named.** *"There is a failure mode that is very common the more senior the engineer: a desire to 'go back to' the syntactic and deterministic world. This can manifest in a lot of ways, but often it shows up as someone trying to wrap a lot of code around an LLM in a subconscious attempt to get away from that uncomfortable randomness, and back to the world of nice, deterministic programs."* Schillace's explanation is psychological: *"Senior engineers have spent decades learning that reliable systems come from explicit control. So when an LLM feels slippery, the reflex is to add another layer of control around it."*

**The diagnostic.** *"If you find yourself thinking 'just one more patch' to your controller or harness, you have probably fallen into this trap."* The diagram's middle panel labels this the "Tempting Wrong Hybrid."

**The artisan-in-the-factory analogy.** *"Imagine trying to build an early factory line — it's all working, using standard parts, going well, except there's this one spot that is fiddly. Let's bring in a craftsman to sit at that spot and hand make the troublesome part! That, of course, wouldn't work at all — the better approach is to understand what the failure is, deeply, and do the novel engineering to get past it — new materials, machines, or techniques."* The point is *factory-line is all or nothing*: you can't add an artisan at a fiddly spot without breaking the whole pipeline's standardisation assumption.

**The meta-cognitive code prescription.** *"In the mass-produced world, there are still artisans — for example, the patternmakers who make the molds and dies for the production line. Similarly, in the LLM world, code has a place, but it is mostly used for 'meta cognitive' things like control, that are hard or awkward for a model to do inside the inference API directly. Code should increasingly move from doing the cognitive work to shaping the conditions under which the cognitive work happens — that's what 'meta-cognitive' means."*

The diagram operationalises this into five "ingredients" and four "method steps." The four method steps (in plainer paraphrase):

1. **Decide clearly** what belongs inside the model and what belongs in code.
2. **Stay in the semantic world** when the task depends on meaning, nuance, or exceptions.
3. **Use code for meta-cognitive scaffolding** — control, memory, orchestration, evaluation. (These are exactly Jaymin's six Raschka components in report 09 §1, minus *prompt shape* and *tool access*.)
4. **Invent native engineering patterns** instead of recreating expert systems by hand.

**The closing thesis.** *"That boundary is where the next generation of software engineering is being invented."* — i.e. the discipline isn't "how do we make LLMs behave like old programs?" but "learning where syntax still belongs, where semantics should be allowed to operate, and how to build the scaffolding that lets both do their proper work."

---

## 7. The agent-shaped world

Letter 7 (*The agent-shaped world*, Feb 2026) is the "shipping-container" essay and one of the conceptually strongest pieces in the eleven. It explains *which* humans compound with AI and which don't — and crucially, why the difference is invisible to those left behind.

**The surfaces-to-grab-onto enumeration** (verbatim list from the post):

- *"They often have things they can iterate and experiment on."* (iterable data)
- *"They have data that the model can get to easily."* (machine-accessible data substrate)
- *"Their workflows decompose into discrete observable steps."* (decomposability)
- *"Their documentation is structured well enough that a machine can navigate it."* (machine-navigable docs — the AGENTS.md / CLAUDE.md / markdown-substrate finding)
- *"Their interfaces are clean enough that something other than a human can drive them."* (machine-drivable interfaces — APIs over GUIs)

And then a recursion clause:

- *"They often stop and look at their own process and ask what is or isn't working, and feed that back into the model."* (recursive self-process audits — the meta-cognitive loop)

**The shipping-container analogy.** McLean's 1950s standardised metal box "looked like a logistics story. A box is a box." But what it actually did was *standardise the interface between production and transport so completely that it restructured global trade*. The revolution *"wasn't the ship — it was what the ship could now assume about the cargo. That assumption, that everything was in standard boxes, meant that the work could be automated — instead of humans manually carrying cargo on and off ships, we could build automated shipyards, and cranes, and trucks and train cars that all handled that standard container."*

The corollary: *"Once the assumption was baked in everywhere, everything compounded. The leverage came from the assumption, not the container."*

Schillace then maps this back to AI:

> *"Any time content is 'plumbed in' so that the agent can see it, they can be effective. Having a system 'shaped' for agents the way containers are 'shaped' for shipping makes all of it more effective — models do well with small, composable, well-defined pieces, and they don't mind doing 'toil' to have them work. A model is perfectly happy with html and ftp to do a presentation, but a human wouldn't be."*

That last line is load-bearing for the agent-OS argument in §9 below — *what feels like toil to a human is fine for a model*, so the right substrate is *the substrate that minimises agent friction even when it would be ergonomic regress for humans*.

**The Borders / newspapers warning.** *"Here's the part that makes me genuinely uneasy about this moment though: the people who don't see this, don't know they're being left behind. […] Their metrics look fine. They're shipping their projects, hitting their numbers, doing their jobs. The gap is invisible because the scoreboard hasn't changed yet. […] Borders was succeeding by bookstore metrics right until it wasn't. Newspapers were profitable deep into the era when they were structurally finished."*

The structural argument: in disruptive transitions, the lagging indicators don't surface the gap until it's too late to close. The closing question is in the same letter and is its operational takeaway:

> *"I think it's a structural question about interfaces: what does it take so that your work is 'on agent' the way we used to say 'online'? That answer is different for every person and role. But it's the urgent question now, and most of us are not yet asking it."*

**Cross-corpus impact.** The agent-shaped-world essay is a strong conceptual sibling of:
- Report 07 (*Dark Factory*) — *Schillace's "agent-shaped surfaces" is the substrate-side mirror of El Kaim's "dark factory" operational stance.*
- Reports 01/02 (*StrongDM Attractor*) — *the Attractor thesis (specs as natural attractors that independent agent runners converge on) is a per-system instance of the shipping-container assumption.*
- Report 27 (*Dotfile pipelines as product*) — *the `.dot` pipeline file is itself a "shipping container" for methodology; what the runners can now assume about the cargo (eight node shapes, CSS-like stylesheet, prompt.md/response.md/status.json contract) is exactly what makes the four-independent-implementations convergence work.*

Worth cross-linking from report 13 (round-2 synthesis) as the practitioner-voice articulation of the substrate-stack recommendation.

---

## 8. The marshmallow test and the last mile

Two failure modes mature into named patterns in letters (8) and (9).

**The modern marshmallow test (letter 8).** Schillace's framing: *"It's very easy to kick off a large, long-running project with an Agentic harness, even if it has a poorly defined goal. The AI will happily pursue that goal, and you're stuck with something that's not complete, workable, or well thought out."* He coins the failure category as a new species of tech debt:

> *"There's a lot of talk about the 'deflationary era of tech debt', and it's certainly true that these tools let you retire issues in a cost-effective way that wouldn't have been possible even a few months ago. But failing this 'modern marshmallow test' is giving rise to a new and different kind of tech debt: large, complex projects that are functionally and syntactically correct, even well organized (as opposed to what we usually think of as tech debt), but poorly thought out and designed, and as a result, very hard to work with and integrate."*

The prescription is uncharacteristically tactical: *"if I take the time up front to think through the problem, I get much better results. And more than that, I have to think through, and express, my intent. If the model understands that clearly, and if I refrain from being overly prescriptive on the how, and mostly focus on the what, I get much better results."* Use the model itself to pressure-test the plan before any code runs. This is the practitioner-voice version of what Yang et al. and Larbi et al. measure quantitatively in report 26 (prompt-underspecification academic anchors).

**Proposed failure mode: F41 — Under-Defined-Intent Debt.** Code functionally / syntactically correct, even well organised, but poorly thought-out because the human kicked off an agent without disciplining intent; downstream debugging finds no clear spec to debug against. Distinct from F36 (instruction-following ceiling, report 26) — F36 is the model's failure to follow a well-specified instruction; F41 is the model's *success* at following an underspecified instruction, producing tech debt that *looks correct*. Mitigation: pre-execution clarifying-question pass; spec-as-source-code with explicit intent capture before agent dispatch.

**The last-mile problem (letter 9).** *"Shipping, going all the way to robustly done, still involves some things that aren't very well 'agent shaped' — little bits of fit and finish, context understanding, making sure the final product is really what I think it is, etc. Some of this can be mitigated — and I think all of it eventually will be — but right now, the 'last mile' of releasing something is still too manual."*

The empirical anchor: *"A few months ago I had a GitHub user with no repos at all. Now I have over a hundred. The machine is spinning! But...not much of that is fully shipped software."* Schillace's read: starting is now easy; finishing is not. The bottleneck has shifted *into the last-mile fit-and-finish work* which is precisely the work that is least agent-shaped.

> *"This is the first [of two priorities]: that finishing something should be as easy as starting it. I think that's possible, and I think largely we have all been so enamored of how easy it is to start things, that we just haven't focused on it yet."*

**Proposed failure mode: F40 — Last-Mile Drift.** Starting projects is trivial; finishing them is bottlenecked on non-agent-shaped fit-and-finish work; aggregate "shipping rate" collapses even as project-start rate skyrockets. Symptom: GitHub repo count grows faster than published / released artifact count. Mitigation: explicitly invest in agent-shaping the last mile (release automation, integration-testing scaffolds, version-bump automation, deploy gates) so the bottleneck is not the regression-to-manual that Schillace observes.

**Why these are F40 and F41, not F36/F37/F38.** Reports 25 and 26 both proposed F36/F37 with number collisions noted at INDEX.md line 66. The synthesis lead will reconcile; I am numbering the Schillace proposals at F40/F41 to avoid additional collision and to flag that these are *operational* failure modes (per-cycle, per-project), distinct from the *spec-quality* failure modes in 25/26 and the *spec→code* failure modes proposed elsewhere. The "last mile" failure mode in particular is a *systems-engineering* failure (the system has the wrong shape for the work that remains) rather than a *prompt* failure.

---

## 9. The agent-OS building blocks

Letter 5 (*The one scarce resource AI can't replace*, URL slug `laundry-lists-and-building-blocks`) is the explicit agent-OS-substrate essay. Two arguments build the case.

**Argument 1 — Mass-audience vs transient software.** *"AI can create a lot of software now. If you think of this as an all or nothing 'it's shipped and done, or its junk', you're missing the point. Complaining that a team is building a lot of software they don't ship, is a bit like complaining they write a shopping list for themselves each week but never publish it as a book."* The point of a shopping list is not to be a book. The point of much AI-generated software is not to be mass-distributed.

Schillace's underlying claim is economic: software's classic "low marginal cost → invest in mass-distribution" game is broken by two new pressures. (a) AI removes creation friction so it's now cheap to build for *one* intention, in the moment, and discard. (b) Inference cost makes distribution non-zero-marginal-cost. So narrow-intent, transient software now dominates, and the bundling-mass-distribution model is for a shrinking minority of cases (akin to books, which still exist).

**Argument 2 — The scarce resource.** With software-creation no longer scarce and software-distribution newly cost-bearing, the *only* durable scarcity is human attention.

> *"That means there's a high premium on low-maintenance building blocks. If you build something for a broad audience, it's not very helpful if it increases their attentional load. It has to be something that has a clear job to do, does it well, doesn't need care and feeding, and gets along well with others."*

The "agent OS" enumeration follows directly:

> *"I think you can see a bit of this emerging in what the beginnings of an operating system for agents might be. Humans need features and hand-holding — we build complex software for them. Agents don't care — they need clarity and efficiency. So simple, well-defined building blocks like **github, markdown, html, yaml, python, rust, go**, etc seem to be getting used more successfully."*

The list is the corpus' first practitioner-voice enumeration of the **agent-OS substrate primitives**. It overlaps cleanly with:

- *I have seen the compounding teams* (letter 1) — "filesystem-based; git; markdown; kubernetes; xml"
- Jaymin's Ch 6 substrate inventory (report 09)
- The architectures/00-comparison.md §4.1 nine-primitive list

The intersection — **git, markdown, yaml** — appears in all three. The Schillace-specific additions are **html** (as the agent-friendly presentation substrate; he built a presentation site for agents out of just HTML and git — *"not as full featured as a presentation application but much easier for it to use"*) and **rust / go** as language choices, alongside python. The pattern across all three lists: agent-friendly primitives are text-based, version-controllable, schema-light, and have low ceremony.

**The "Attention Firewall" pattern.** Schillace's letter 5 also names a concrete tool built by his team:

> *"I have a tool on my desktop that someone on my team built, called 'Attention Firewall'. It just watches background notifications and does filtering — much easier for it than integration with the dozen apps feeding into those notifications — but that would never work for human software."*

The point is twofold. (a) The Attention Firewall is a concrete instance of Theme-3 ("automated policy so humans aren't in every loop") — the policy is *filtering*, the loop the human is removed from is the *every-notification-must-be-seen* loop. (b) The mechanism — *watch background notifications and filter them*, instead of *integrate with twelve different app APIs* — is exactly the *agent-shaped* substrate choice from letter 7. The agent doesn't need the twelve API integrations; it just needs to see the notification stream and decide. Substrate choice = scarcity-aware design.

**Cross-corpus impact.** The agent-OS-building-blocks list anchors the corpus' substrate-stack recommendation (report 13 §3) with a Microsoft-internal practitioner voice. The "Attention Firewall" specifically is a concrete-tool exemplar that the corpus has been missing — Theme-3 has had policy frameworks (followup/10 governance) and high-level principles (Anthropic engineering trilogy, report 23) but few *small named tools* operationalising "humans not in every loop." Attention Firewall is a clean such example.

---

## 10. Cross-corpus impact

This section folds Schillace's contributions into the existing corpus structure. Five impact axes.

### 10.1 Failure mode proposals

Two proposed failure modes for the F40+ range (avoiding the F36/F37 number collision flagged at INDEX.md line 66):

- **F40 — Last-Mile Drift.** (Anchored on letter 9.) Starting projects is trivial; finishing them is bottlenecked on non-agent-shaped fit-and-finish work; aggregate shipping rate collapses even as project-start rate explodes. *Mitigation:* explicit investment in agent-shaping the last mile (release automation, integration-testing scaffolds, deploy gates).
- **F41 — Under-Defined-Intent Debt.** (Anchored on letter 8.) Code functionally / syntactically correct, even well organised, but poorly thought-out because the human kicked off an agent without disciplining intent; downstream debugging finds no clear spec to debug against. Distinct from F36 (instruction-following ceiling) — the model succeeds at following an underspecified instruction. *Mitigation:* pre-execution clarifying-question pass; spec-as-source-code with explicit intent capture before agent dispatch.

A *third* candidate flagged-not-promoted: **non-agent-shaped-workflow** (anchored on letter 7). The reason for non-promotion is that this is more naturally read as a *cause* of F40 (the work isn't agent-shaped, therefore the last mile is bottlenecked) and as a *substrate* requirement rather than a per-cycle failure mode. It surfaces as a *design constraint* (the shipping-container assumption) rather than a *failure-during-operation* mode.

### 10.2 Cross-references into existing reports

- **Report 01 (StrongDM Factory).** Letter 1's "code review as firing offense" is the practitioner-voice articulation of StrongDM's *no-human-reads-the-generated-code* doctrine. Cross-link from this report.
- **Report 02 (StrongDM Attractor) and report 27 (Dotfile pipelines as product).** Letter 7's shipping-container thesis is the conceptual frame for the Attractor convergence and for the runner-vs-blueprint split.
- **Report 07 (Dark Factory).** Letter 7's "agent-shaped world" is the substrate-side framing of El Kaim's dark factory operational stance.
- **Report 09 (Jaymin's harnesses).** Letters 10 and 11 — the two MHTML keepers — are the non-OpenAI canonical harness anchors. Report 09 has been updated this drain to embed both diagrams; see §11 below for the update.
- **Report 13 (Round-2 synthesis).** Schillace's attention thesis and his agent-OS-building-blocks list are anchors for the substrate-stack recommendation in §3 of that report.
- **Report 23 (Anthropic engineering trilogy).** Letter 1's "filesystem-based; git; markdown; kubernetes; xml" substrate enumeration corroborates Anthropic's agent skills / claude-code-sandbox substrate decisions.
- **Followup/06 (Competitor landscape).** Amplifier internals (Dev Foundry, Crusty Old Engineer, session analyst, foundation expert, yaml recipes, gene transfer) are now anchored in this report. Followup/06 is updated this drain to cross-reference rather than re-drain; see §11 below.

### 10.3 Theme alignment

| Theme | Schillace anchor |
|---|---|
| Theme 1 (human-attention scarcity) | Letters 3, 4, 5, 6 — esp. "output per unit of human attention" (6) and the three user classes (6) |
| Theme 2 (gene transfer / capability propagation) | Letter 10 — coins the term at primary-source level |
| Theme 3 (automated policy / humans not in every loop) | Letter 5 — Attention Firewall as concrete instance |
| Theme 4 (substrate / harness as design site) | Letters 1, 5, 10 — agent-OS building blocks, harness definition |
| Theme 6 (engineering practice in the new paradigm) | Letters 8, 11 — meta-cognitive code, marshmallow test |
| Theme 7 (agents as team members) | Letters 1, 3, 9 — compounding teams, 3-feels-like-30, last-mile / 12-team-500-projects |

### 10.4 Cross-quotes between letters

Several explicit cross-references between Schillace's own letters that strengthen the arc:

- Letter 3 ("Attention and collaboration") opens *"I wrote last week about the emerging pattern of intense, agentic coding"* — referencing letter 2 ("How it will happen").
- Letter 4 ("Hard part is choosing the work") *"I wrote about this last week and I can say — it's only getting worse!"* — referencing letter 3.
- Letter 6 ("Attention is all ya got") is the synthesis-of-attention-pieces letter — explicit follow-on to letters 3 and 5.
- Letter 10 ("What is a harness") opens *"I mentioned last week that I have been working on what has variously been called 'agentic coding', 'AI coding' and now 'harness engineering'"* — referencing letter 9.
- Letter 11 ("Artisans and Factory Lines") closes a thread that letter 1 opened: from "I have seen the compounding teams" through to "the next generation of software engineering is being invented" at the syntactic/semantic boundary.

### 10.5 Surprises and contradictions

- **The Semantic Kernel lineage is corpus-new.** Schillace's footnote claim that he named Semantic Kernel "on a whim, as a code name" and that the Microsoft naming machinery never overrode it is biographically novel and biographically delightful, but the substantive surprise is the *lineage claim*: Semantic Kernel is positioned in letter 10 as the proto-Amplifier orchestrator (and therefore the proto-harness) from late 2022. The corpus had been treating Semantic Kernel as a separate orchestration framework. This needs to be reflected in the harness lineage chart in report 09 / report 18.
- **"Gene transfer" attribution.** Schillace says *"Others have called this 'gene transfer'"* in letter 10. The corpus has seen the phrase exactly once before, in report 01 referencing StrongDM. There is an open question about *who in fact originated the term*. Plausibly StrongDM; plausibly Schillace's "others" is StrongDM via cross-pollination at Microsoft. Worth a single follow-up clarification if anyone has a primary-source attribution.
- **Code review as "firing offense."** This is the strongest claim in the eleven letters and the most likely to be misread. Schillace marks it explicitly as "jokingly" — *"one jokingly considers a code review a 'firing offense' because it means you're in the way of the tool."* It is *not* a serious HR policy; it is an in-joke marking the discipline of "if you're reading the code, the system isn't working." The corpus should treat this as a load-bearing *cultural anecdote* rather than a literal anti-pattern proposal.
- **No defect-rate counterfactual.** Across letter 1's "5–10 parallel processes, hundreds of dollars/day" claim, letter 9's "100+ repos but not much shipped" claim, letter 9's "12-person team / 500+ projects" claim — *Schillace does not anywhere publish a defect-rate counterfactual.* The number of issues encountered per shipped artifact, the percentage of agent-generated code that survives a quarter, the fraction of "compounding team" output that is later abandoned — these are all unknowns. Similar caveat to report 18 §5's `harness-engineering` numbers; Schillace's letters and OpenAI's piece are equally silent on this axis.
- **The book-foundry humility.** Letter 10 footnote 2 — that authentic prose writing is *"HARD"* and may be unsolvable — is the closest the eleven letters come to a public limitation of Amplifier. Worth surfacing in followup/06 as a calibration anchor: *the head of Amplifier's product organization has publicly acknowledged that authentic prose generation is not solved.*

---

## 11. Updates to other reports (executed this drain)

This subagent's drain also executed the following updates per the orchestrator decision (`research/manual/new-index.md` row 3, line 107):

- **Report 09 (`09-jaymin-book-harnesses-practices-mental-models.md`)** — added a new subsection embedding both Schillace diagrams (the four-panel harness diagram + the Recipe for Building in the Semantic Era diagram), each with a short caption and a cross-reference back to this report. Both PNGs are referenced from `figures/28-schillace-sunday-letters/` (no duplication).
- **INDEX.md** — added a new row for report 28; refreshed the "Last updated" line; noted the report 09 incorporation in the report-09 row.
- **followup/06-competitor-landscape.md** — added a one-paragraph note that Amplifier internals (Dev Foundry / session analyst / Crusty Old Engineer / yaml recipes / gene-transfer pattern) are now anchored in this report; cross-references rather than re-drains.

---

## 12. Sources

All eleven letters are ✅ FULL — drained from manual `research/manual/` capture on 2026-05-16. Two are MHTML originals kept for their embedded diagrams; the other nine were converted to TXT in the manual indexing pass (the original MHTML files were deleted because no useful images survived).

| # | URL | Manual file | Status |
|---|---|---|---|
| 1 | https://sundaylettersfromsam.substack.com/p/i-have-seen-the-compounding-teams | `manual/I have seen the compounding teams - by Sam Schillace.txt` | ✅ FULL |
| 2 | https://sundaylettersfromsam.substack.com/p/how-it-will-happen | `manual/How it will happen - by Sam Schillace - Sunday Letters.txt` | ✅ FULL |
| 3 | https://sundaylettersfromsam.substack.com/p/attention-and-collaboration-in-the | `manual/Attention and collaboration in the AI world.txt` | ✅ FULL |
| 4 | https://sundaylettersfromsam.substack.com/p/the-hard-part-isnt-doing-the-work | `manual/The hard part isn't doing the work now; it's choosing the work..txt` | ✅ FULL |
| 5 | https://sundaylettersfromsam.substack.com/p/laundry-lists-and-building-blocks | `manual/The one scarce resource AI can't replace - by Sam Schillace.txt` | ✅ FULL |
| 6 | https://sundaylettersfromsam.substack.com/p/attention-is-all-ya-got | `manual/Attention is all ya got - by Sam Schillace - Sunday Letters.txt` | ✅ FULL |
| 7 | https://sundaylettersfromsam.substack.com/p/the-agent-shaped-world | `manual/The agent-shaped world - by Sam Schillace - Sunday Letters.txt` | ✅ FULL |
| 8 | https://sundaylettersfromsam.substack.com/p/ai-and-the-marshmallow-test | `manual/AI and the marshmallow test - by Sam Schillace.txt` | ✅ FULL |
| 9 | https://sundaylettersfromsam.substack.com/p/machine-with-concrete | `manual/Machine with Concrete - by Sam Schillace - Sunday Letters.txt` | ✅ FULL |
| 10 | https://sundaylettersfromsam.substack.com/p/what-is-a-harness-and-why-do-i-care | `manual/What is a harness and why do I care_ - by Sam Schillace.mhtml` (KEPT) | ✅ FULL — 4-panel diagram embedded |
| 11 | https://sundaylettersfromsam.substack.com/p/artisans-and-factory-lines | `manual/Artisans and Factory Lines - by Sam Schillace.mhtml` (KEPT) | ✅ FULL — Recipe diagram embedded |

**Embedded figures:**

- `research/figures/28-schillace-sunday-letters/what-is-a-harness-four-panel.png` — extracted from letter 10 MHTML; 1456×1030; verified content matches the four-panel "What Is an AI Harness?" architecture diagram.
- `research/figures/28-schillace-sunday-letters/artisans-recipe-for-semantic-era.png` — extracted from letter 11 MHTML; 1448×1086; verified content matches the hand-drawn "Recipe for Building in the Semantic Era" diagram.

Both figures are also referenced (not copied) from report 09 §9a per the orchestrator-decision-row-3 directive.

---

*End of report 28 — [`28-schillace-sunday-letters`](28-schillace-sunday-letters.md) v1.0, 2026-05-16.*
