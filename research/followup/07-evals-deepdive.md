# Round-3 Thread 7 — Evals Deep-Dive: Anthropic's Multi-Agent Research System and Husain/Shankar's Evals FAQ

**Date:** 2026-05-11
**Branch:** `claude/parallelize-with-subagents-SO0nR--sub-10` (original) → upgraded under `claude/parallelize-with-subagents-SO0nR--sub-32`
**Plan reference:** `research/PLAN.md` §11.7
**One-line:** Simon Willison endorses both Anthropic's "How we built our multi-agent research system" and Hamel Husain & Shreya Shankar's "Frequently Asked Questions (And Answers) About AI Evals" as gold-standard primers; the eval discipline in all four of our architectures would be sharpened by reading them.

---

## Drain note (issue #24) — 2026-05-11

This report was originally written from WebSearch result summaries because `anthropic.com`, `hamel.dev`, and `simonwillison.net` were 403 from the sandbox. On 2026-05-11 the four primary URLs were fetched via the `fetch-blocked-urls` workflow under issue #24 and drained into this report. The report is now **primary-source-anchored** rather than summary-anchored. Concretely:

- The "60–80% of development time on error analysis" quote is now verbatim from Husain/Shankar §"How much of my development budget should I allocate to evals?", with surrounding context.
- The "passing 100% of your evals" heuristic is now verbatim, with Husain's exact recommended action ("70% pass rate might indicate a more meaningful evaluation that's actually stress-testing your application").
- The 90.2% multi-agent gain is now verbatim from Anthropic, with the specific test case (board members of IT S&P 500 companies) and the methodology context (internal research eval, breadth-first queries).
- The single-judge finding is now verbatim from Anthropic: "a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements."
- The 20-trace saturation heuristic is now verbatim from Husain: "if ~20 traces don't turn up a new category, you can stop (but review at least 100 to start)."
- The Anthropic eval rubric components (factual accuracy / citation accuracy / completeness / source quality / tool efficiency) are now verbatim with the parenthetical operational definitions.
- The orchestrator-worker architecture is now described with primary-source detail: LeadResearcher → Memory persistence → parallel Subagents with interleaved thinking → CitationAgent. The 200,000-token truncation rationale for Memory is included.
- **Refuted claim removed:** prior report's "**>90% agreement with a domain expert in three iterations**" was not verifiable from the primary FAQ; the FAQ talks about iterative TPR/TNR alignment but does not cite this number. The claim has been replaced with the actually-stated guidance (focus on TPR/TNR on a held-out set; iterate until acceptable).
- **Refuted claim corrected:** prior report said multi-agent "burned ~4× the tokens." The Anthropic post is more specific: agents typically use **~4× more tokens than chat**, and **multi-agent systems use about 15× more tokens than chats**. Token economics corrected.
- New claims surfaced from primary sources: end-state evaluation pattern for stateful agents; filesystem-as-shared-artifact pattern to avoid the "game of telephone"; rainbow deployments for stateful agents; "Think like your agents" prompt-engineering principle; binary > Likert because Likert annotators "default to middle values to avoid making hard decisions."

Source-status table at the foot of this report has been flipped from ❌/⚠️ to ✅ for the four drained URLs.

---

## Drain note (issue #29) — 2026-05-13

Issue #29 fetched six more primary sources that this report had been citing only through search summaries or had cross-referenced as future follow-ups. After draining:

- **Hamel, "Your AI Product Needs Evals" (Mar 2024)** is now anchored as the *philosophical* root of the discipline — the post the FAQ, the llm-judge guide, and the field-guide all build on. New §"0. The philosophical anchor (Husain 2024)" added below to host the load-bearing quotes ("a failure to create robust evaluation systems," "Iterating Quickly == Success," the three-level Level 1/2/3 hierarchy, "Eval Systems Unlock Superpowers For Free").
- **Hamel, "Creating an LLM-as-a-Judge" / "Critique Shadowing" (Oct 2024)** is now anchored as the operational manual for any judge in our architectures. A new §"3.9 Critique Shadowing (the llm-judge guide)" walks through the 7-step process (Principal Domain Expert → diverse dataset → pass/fail with critiques → fix errors → iterate prompt to alignment → error analysis → specialized judges).
- **Reinstated and re-attributed claim:** the previous report removed ">90% expert agreement in three iterations" because the FAQ didn't carry it. The llm-judge post DOES carry it verbatim, in the Honeycomb Query Assistant case study with Phillip Carter: "It took us only three iterations to achieve > 90% agreement between the LLM and Phillip." The field-guide post re-states the same fact ("It took three iterations to achieve >90% agreement"). The claim is restored, sourced correctly to hamel.dev/blog/posts/llm-judge/ §"Keep Iterating on the Prompt Until Convergence With Domain Expert" and to the field-guide §5.3.
- **Hamel, "A Field Guide to Rapidly Improving AI Products" (Mar 2025)** adds three substantial new claims none of the prior sources carried: (a) a NurtureBoss case study where bottom-up error analysis took date-handling success from 33% → 95%, with three issue clusters accounting for over 60% of all failures; (b) the explicit "**experiments, not features**" roadmap reframing via Bryan Bischof's "capability funnel" and Eugene Yan's "fifteen-five" failure-sharing ritual; (c) the operational claim that few-shot critique examples in judge prompts "often yields 15-20% higher agreement rates between human and LLM evaluations." New §"4.6 Roadmap reframing — count experiments, not features" added.
- **Simon Willison, "FAQs about AI evals" (Jul 3, 2025)** is short — essentially two pull quotes (the 60–80% and the 70% pass-rate ones) plus an endorsement. It is a second-order endorsement of the FAQ, not a source of new claims; its citation in the existing report ("Simon Willison's July 3, 2025 endorsement…") is now anchored on the verbatim post text.
- **Simon Willison, "How we built our multi-agent research system" (Jun 14, 2025)** adds two things Anthropic's own post did not foreground: (i) the **"tools in a loop" definition of agent** Simon pulled into focus ("A multi-agent system consists of multiple agents (LLMs autonomously using tools in a loop) working together"); (ii) the existence of the open-sourced **research-lead-agent and research-subagent prompts** at `anthropics/anthropic-cookbook/patterns/agents/prompts`, including the OODA-loop instruction block for subagents. New §"2.6 The open-sourced prompts (via Simon Willison)" added.
- **No refutations this round.** The drain reinforces and extends; one prior removal (the >90%/three-iterations claim) is now restored with corrected attribution.

Six URLs in the sources table flipped to ✅; the residual ⏳/⚠️ marks on the llm-judge URL and on the "demystifying evals" Anthropic post are now resolved (llm-judge ✅; demystifying-evals still ⏳ but de-prioritized since the llm-judge post is the canonical operational manual).

---

## Drain note (Cluster L cross-reference) — 2026-05-16

The new **report 29 — Prompt Engineering Survey** (`research/29-prompt-engineering-survey.md`, drained 2026-05-16 from Schulhoff et al.'s *The Prompt Report*, arXiv:2406.06608v6) is the **academic taxonomy anchor for this thread's LLM-as-judge discussion**. Report 29 §5 (*LLM-as-judge — the §4.2 evaluation-prompting catalogue*) summarizes Schulhoff et al.'s five-pattern catalogue: **single-output judging**, **pairwise judging**, **reference-based judging**, **self-judging**, and **multi-criterion judging**. Each maps onto a pattern already discussed here:

- *Single-output / multi-criterion* ↔ this report's §3 (Husain & Shankar's binary-per-AC pattern) and the Anthropic single-judge finding (verbatim from §2: *"a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements"*).
- *Reference-based* ↔ this report's §3.9 (Hamel's Critique-Shadowing process).
- *Self-judging* ↔ Schulhoff's Self-Criticism family (§2.5 of report 29) and the corpus' "Crusty Old Engineer" critic role in Amplifier (report 28).
- *Pairwise* ↔ the LLM-arena pattern (referenced in §3 but not the canonical pattern this thread endorses).

A non-obvious detail report 29 surfaces that is directly applicable to this thread: Schulhoff et al.'s own PRISMA *LLM-screen prompt* was validated against 100 ground-truth annotations at **89% precision / 75% recall / 81% F1** before being used to triage 3,985 papers (report 29 §1). This is the methodological recommendation they implicitly make for every judge prompt — calibrate against a small held-out human-labelled set before deploying. It corroborates the Hamel field-guide claim (this report §4.6) that few-shot critique examples in judge prompts *"often yields 15-20% higher agreement rates between human and LLM evaluations"* — both arrive at the same operational rule from independent directions. Report 29 §5 is therefore the canonical citation to use whenever the corpus needs to anchor the LLM-as-judge discipline in academic literature; this thread is the practitioner-grade companion.

---

## 1. Why this thread exists

Every architecture in `architectures/` depends on evaluation whose quality is taken for granted: Architecture 1 (Refinery) uses an LLM judge against ACs; Architecture 3 (Foundry) uses independent V&V agents at phase gates; Architecture 4 (Tournament) uses a fitness vector to drive selection; Architecture 2 (Atelier) uses a multi-persona review panel where reviewers act as judges. All four assume the judge / fitness / V&V is good enough to discriminate. Several primary sources push back on that assumption and supply concrete guidance. This report extracts the load-bearing ones and maps them onto our four architectures.

---

## 0. The philosophical anchor — Husain, "Your AI Product Needs Evals" (March 2024)

The earliest of Hamel Husain's evals posts (hamel.dev/blog/posts/evals/, March 29, 2024) is the philosophical anchor under everything that follows. The opening sentence states the discipline's thesis directly (verbatim):

> "I've seen many successful and unsuccessful approaches to building LLM products. I've found that unsuccessful products almost always share a common root cause: **a failure to create robust evaluation systems.**"

The post frames evals not as a QA activity but as **the limiting reagent of iteration speed**. From §"Iterating Quickly == Success" (verbatim):

> "Like software engineering, success with AI hinges on how fast you can iterate. You must have processes and tools for: 1. Evaluating quality (ex: tests). 2. Debugging issues (ex: logging & inspecting data). 3. Changing the behavior or the system (prompt eng, fine-tuning, writing code). **Many people focus exclusively on #3 above, which prevents them from improving their LLM products beyond a demo.** […] If you streamline your evaluation process, all other activities become easy."

This is the explicit ideological commitment that the FAQ later operationalizes ("60-80% of development time on error analysis"). The 2024 post supplies the *why*; the 2026 FAQ supplies the *how-much*. Quote the 2024 post when justifying the discipline; quote the FAQ when justifying the budget.

### 0.1 The three-level evaluation hierarchy

Husain's 2024 taxonomy (still the canonical one in the 2025 field-guide and 2024 llm-judge post):

- **Level 1: Unit tests.** Cheap pytest-style assertions, run on every code change. "Rechat has hundreds of these unit tests. We continuously update them based on new failures we observe in the data."
- **Level 2: Human & Model eval.** Trace logging + a custom data viewer + alignment with a domain expert. Run on a cadence, not on every change.
- **Level 3: A/B testing.** Only after the product is mature enough to deserve real-user exposure.

Verbatim cost ordering (§"The Types Of Evaluation"):

> "The cost of Level 3 > Level 2 > Level 1. This dictates the cadence and manner you execute them. […] It's also helpful to conquer a good portion of your Level 1 tests before you move into model-based tests."

Verbatim methodology on pass rate at Level 1 (matching the 2026 FAQ's "70% band" claim, four years earlier):

> "Unlike traditional unit tests, you don't necessarily need a 100% pass rate. Your pass rate is a product decision, depending on the failures you are willing to tolerate."

### 0.2 "Eval Systems Unlock Superpowers For Free"

The 2024 post's most quoted section name argues that the same infrastructure built for evals serves three other workflows — **debugging**, **fine-tuning data curation**, and **synthetic data generation** — for free. Verbatim (§"Eval Systems Unlock Superpowers For Free", with footnote attributing the framing to Bryan Bischof at Hex):

> "There is an incredibly large overlap between the infrastructure needed for evaluation and that for debugging."

And earlier (§"Data Synthesis & Curation"):

> "99% of the labor involved with fine-tuning is assembling high-quality data that covers your AI product's surface area. However, if you have a solid evaluation system like Rechat's, you already have a robust data generation and curation engine!"

**Implication for all four architectures:** every dollar invested in an eval system is double-counted as a debugging tool and a synthetic-data engine. Whatever budget the architecture spends on V&V, judges, or fitness functions can be amortized against future fine-tuning rounds and against incident response. The Foundry's V&V infrastructure, for instance, doubles as the post-mortem toolkit when a phase fails.

### 0.3 Husain's closing list (verbatim, from §"Conclusion")

A useful checklist to cross-reference against any architecture's eval design:

> "- Remove ALL friction from looking at data.
> - Keep it simple. Don't buy fancy LLM tools. Use what you have first.
> - You are doing it wrong if you aren't looking at lots of data.
> - Don't rely on generic evaluation frameworks to measure the quality of your AI. Instead, create an evaluation system specific to your problem.
> - Write lots of tests and frequently update them.
> - LLMs can be used to unblock the creation of an eval system. Examples include using a LLM to: Generate test cases and write assertions; Generate synthetic data; Critique and label data etc.
> - Re-use your eval infrastructure for debugging and fine-tuning."

---

## 2. Anthropic — "How we built our multi-agent research system"

Published June 13, 2025 on `anthropic.com/engineering`. Authors: Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford. The essay describes the production architecture behind Claude's Research feature: an **orchestrator-worker** pattern where a lead agent (Claude Opus 4) coordinates parallel subagents (Claude Sonnet 4) that each search and reason in isolated contexts, then hand summarized findings back.

### 2.1 Subagents as context-window primitives

Anthropic frames subagents not as a parallelization trick but as a **compression primitive**. Verbatim (anthropic.com/engineering/multi-agent-research-system, §"Benefits of a multi-agent system", ¶3):

> "The essence of search is compression: distilling insights from a vast corpus. Subagents facilitate compression by operating in parallel with their own context windows, exploring different aspects of the question simultaneously before condensing the most important tokens for the lead research agent. Each subagent also provides separation of concerns—distinct tools, prompts, and exploration trajectories—which reduces path dependency and enables thorough, independent investigations."

The orchestrator survives long sessions by persisting state outside the context window. From §"Architecture overview for Research" (caption to the process diagram):

> "The LeadResearcher begins by thinking through the approach and saving its plan to Memory to persist the context, since if the context window exceeds 200,000 tokens it will be truncated and it is important to retain the plan."

Rule (paraphrased from §"Long-horizon conversation management" in the Appendix): when a task's intermediate state exceeds one context window, fan out to subagents whose only deliverable is a distilled artifact, and have the orchestrator stash its plan to durable memory before the 200k-token limit kicks in:

> "When context limits approach, agents can spawn fresh subagents with clean contexts while maintaining continuity through careful handoffs. Further, they can retrieve stored context like the research plan from their memory rather than losing previous work when reaching the context limit."

A related Appendix pattern — **filesystem as shared artifact bus** — explicitly avoids the "game of telephone" that pure prompt-passing creates:

> "Direct subagent outputs can bypass the main coordinator for certain types of results, improving both fidelity and performance. Rather than requiring subagents to communicate everything through the lead agent, implement artifact systems where specialized agents can create outputs that persist independently. Subagents call tools to store their work in external systems, then pass lightweight references back to the coordinator."

### 2.2 The 90.2% gain (verbatim) and the cost

From §"Benefits of a multi-agent system", ¶5:

> "Our internal evaluations show that multi-agent research systems excel especially for breadth-first queries that involve pursuing multiple independent directions simultaneously. We found that a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval. For example, when asked to identify all the board members of the companies in the Information Technology S&P 500, the multi-agent system found the correct answers by decomposing this into tasks for subagents, while the single agent system failed to find the answer with slow, sequential searches."

The performance-variance decomposition (same section, next paragraph):

> "Three factors explained 95% of the performance variance in the BrowseComp evaluation (which tests the ability of browsing agents to locate hard-to-find information). We found that token usage by itself explains 80% of the variance, with the number of tool calls and the model choice as the two other explanatory factors."

The cost, also verbatim (§"Benefits…", ¶7):

> "In our data, agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats. For economic viability, multi-agent systems require tasks where the value of the task is high enough to pay for the increased performance."

Implication for our architectures: 15× is the multi-agent tax; the value-of-task threshold must clear that bar.

### 2.3 Eval methodology — the single-judge finding

From §"Effective evaluation of agents", under "LLM-as-judge evaluation scales when done well":

> "Research outputs are difficult to evaluate programmatically, since they are free-form text and rarely have a single correct answer. LLMs are a natural fit for grading outputs. We used an LLM judge that evaluated each output against criteria in a rubric: factual accuracy (do claims match sources?), citation accuracy (do the cited sources match the claims?), completeness (are all requested aspects covered?), source quality (did it use primary sources over lower-quality secondary sources?), and tool efficiency (did it use the right tools a reasonable number of times?). We experimented with multiple judges to evaluate each component, but found that a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements."

On the small-sample start (verbatim, same section, "Start evaluating immediately with small samples"):

> "We started with a set of about 20 queries representing real usage patterns. Testing these queries often allowed us to clearly see the impact of changes. We often hear that AI developer teams delay creating evals because they believe that only large evals with hundreds of test cases are useful. However, it's best to start with small-scale testing right away with a few examples, rather than delaying until you can build more thorough evals."

Humans alongside, not below, the judge (verbatim, "Human evaluation catches what automation misses"):

> "People testing agents find edge cases that evals miss. These include hallucinated answers on unusual queries, system failures, or subtle source selection biases. In our case, human testers noticed that our early agents consistently chose SEO-optimized content farms over authoritative but less highly-ranked sources like academic PDFs or personal blogs. Adding source quality heuristics to our prompts helped resolve this issue."

### 2.4 End-state evaluation for stateful agents

A pattern from the Appendix that maps directly onto our Foundry / Tournament architectures:

> "Evaluating agents that modify persistent state across multi-turn conversations presents unique challenges. Unlike read-only research tasks, each action can change the environment for subsequent steps, creating dependencies that traditional evaluation methods struggle to handle. We found success focusing on end-state evaluation rather than turn-by-turn analysis. Instead of judging whether the agent followed a specific process, evaluate whether it achieved the correct final state. […] For complex workflows, break evaluation into discrete checkpoints where specific state changes should have occurred, rather than attempting to validate every intermediate step."

### 2.5 Prompt-engineering lessons (verbatim list, abbreviated)

Anthropic's eight numbered principles (§"Prompt engineering and evaluations…"):

1. **Think like your agents.** Build a Console simulation with the exact prompts and tools; watch agents work step-by-step.
2. **Teach the orchestrator how to delegate.** "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries." Without that, subagents duplicate work or leave gaps; cite: "one subagent explored the 2021 automotive chip crisis while 2 others duplicated work investigating current 2025 supply chains."
3. **Scale effort to query complexity.** Explicit rules: "Simple fact-finding requires just 1 agent with 3-10 tool calls, direct comparisons might need 2-4 subagents with 10-15 calls each, and complex research might use more than 10 subagents with clearly divided responsibilities."
4. **Tool design and selection are critical.** Bad tool descriptions send agents down wrong paths; a tool-testing agent that rewrote MCP descriptions "resulted in a 40% decrease in task completion time."
5. **Let agents improve themselves.** Claude 4 can diagnose its own prompt failures and suggest improvements.
6. **Start wide, then narrow down.** "Agents often default to overly long, specific queries that return few results."
7. **Guide the thinking process.** Extended thinking as a "controllable scratchpad."
8. **Parallel tool calling transforms speed and performance.** Lead agent spawns 3–5 subagents in parallel; subagents use 3+ tools in parallel; "cut research time by up to 90% for complex queries."

Production reliability lessons (§"Production reliability and engineering challenges"): agents are stateful; errors compound; restarts are expensive, so resume-from-checkpoint is essential; deployment uses **rainbow deployments** to avoid disrupting in-flight agents; current bottleneck is synchronous subagent execution.

### 2.6 Simon Willison's commentary — what he highlighted that Anthropic understated

Simon Willison's June 14, 2025 link-blog post (simonwillison.net/2025/Jun/14/multi-agent-research-system/) is largely confirmatory of Anthropic's post but surfaces two things worth citing:

**(i) The "tools in a loop" agent definition.** Simon pulls forward what Anthropic frames in passing — but he treats it as the operational definition the rest of the engineering essay depends on:

> "A multi-agent system consists of multiple agents (LLMs autonomously using tools in a loop) working together. Our Research feature involves an agent that plans a research process based on user queries, and then uses tools to create parallel agents that search for information simultaneously."

This phrasing is the cleanest available citation when our own architecture docs need to distinguish "agent" from "pipeline." All four of our architectures should use "tools in a loop" as the test for whether a component is an agent in the multi-agent sense.

**(ii) Open-sourced prompts.** Anthropic released the actual research-lead-agent and research-subagent prompts in their cookbook (`anthropics/anthropic-cookbook/patterns/agents/prompts`). Simon quotes two load-bearing fragments. The first is the parallel-tool-call directive in the lead agent's prompt:

> "`<use_parallel_tool_calls> For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially. Call tools in parallel to run subagents at the same time. You MUST use parallel tool calls for creating multiple subagents (typically running 3 subagents at the same time) at the start of the research, unless it is a straightforward query. […] </use_parallel_tool_calls>`"

The second is the **OODA research loop** block prescribed for each subagent (loaded directly into the subagent system prompt):

> "`Research loop: Execute an excellent OODA (observe, orient, decide, act) loop by (a) observing what information has been gathered so far, what still needs to be gathered to accomplish the task, and what tools are available currently; (b) orienting toward what tools and queries would be best to gather the needed information and updating beliefs based on what has been learned so far; (c) making an informed, well-reasoned decision to use a specific tool in a certain way; (d) acting to use this tool. Repeat this loop in an efficient way to research well and learn based on new results.`"

**Implication for Architecture 3 (Foundry) and Architecture 4 (Tournament):** Anthropic's open-sourced prompts are a working template for the subagent system prompts in both architectures. The OODA fragment in particular is a candidate for adoption verbatim in any V&V subagent (Foundry) or fitness-evaluator subagent (Tournament) that needs to drive a multi-step research loop. Cite the cookbook URL directly in the relevant architecture docs.

---

## 3. Husain & Shankar — "Frequently Asked Questions About AI Evals"

Published January 15, 2026 on `hamel.dev` (NB: the WebSearch summaries said "mid-2025" — the FAQ itself dates to early 2026, distilling questions from the cohort course running since 2025; Simon Willison's commentary post is July 3, 2025 covering a then-current draft). Distilled from 700+ engineers and PMs the authors taught on Maven.

Simon Willison's July 3, 2025 endorsement (simonwillison.net/2025/Jul/3/faqs-about-ai-evals/, ¶2):

> "There's a ton of actionable advice in here. I continue to believe that a robust approach to evals is the single most important distinguishing factor between well-engineered, reliable AI systems and YOLO cross-fingers and hope it works development."

### 3.1 Error analysis as 60–80% of development time (verbatim)

From hamel.dev/blog/posts/evals-faq/ §"How much of my development budget should I allocate to evals?", ¶4:

> "In the projects we've worked on, **we've spent 60-80% of our development time on error analysis and evaluation**. Expect most of your effort to go toward understanding failures (i.e. looking at data) rather than building automated checks."

Surrounding context (¶1 of the same Q): "It's important to recognize that evaluation is part of the development process rather than a distinct line item, similar to how debugging is part of software development." The 60–80% is therefore framed not as overhead but as the activity that constitutes development.

### 3.2 The "passing 100% of your evals" heuristic (verbatim)

Same section, ¶5:

> "Be wary of optimizing for high eval pass rates. If you're passing 100% of your evals, you're likely not challenging your system enough. **A 70% pass rate might indicate a more meaningful evaluation that's actually stress-testing your application.** Focus on evals that help you catch real issues, not ones that make your metrics look good."

**Meaning:** a 100% pass rate is a signal the eval set has been outgrown; raise difficulty until the rate drops back into a stress-testing band (Husain anchors on 70%). The action it implies: **deliberately add harder cases until the pass rate drops into a discriminating band**. Treat each pass-rate jump as a signal to harden the set, not to celebrate.

### 3.3 Error analysis — the open/axial coding workflow

From §"Why is 'error analysis' so important in LLM evals, and how is it performed?":

1. **Create a dataset:** representative traces or synthetic data.
2. **Open coding:** "Human annotator(s) (ideally a benevolent dictator) review and write open-ended notes about traces, noting any issues. This process is akin to 'journaling' and is adapted from qualitative research methodologies. When beginning, it is recommended to focus on noting the first failure observed in a trace, as upstream errors can cause downstream issues."
3. **Axial coding:** "Categorize the open-ended notes into a 'failure taxonomy.' In other words, group similar failures into distinct categories. This is the most important step. At the end, count the number of failures in each category."
4. **Iterative refinement until theoretical saturation** (verbatim):

> "Keep iterating on more traces until you reach theoretical saturation, meaning new traces do not seem to reveal new failure modes or information to you. As a rule of thumb, you should aim to review at least 100 traces. My rough heuristic is if ~20 traces don't turn up a new category, you can stop (but review at least 100 to start). Remember, the goal is to prioritize the failures that actually happen the most, not catch every possible failure (evals are not free, so we need to be pragmatic)."

### 3.4 Synthetic data via hand-written dimension tuples

From §"What is the best approach for generating synthetic data?":

> "Start by defining dimensions: categories that describe different aspects of user queries. […] For a recipe app, dimensions might include Dietary Restriction (vegan, gluten-free, none), Cuisine Type (Italian, Asian, comfort food), and Query Complexity (simple request, multi-step, edge case). […] **Create tuples manually first**: Write 20 tuples by hand—specific combinations selecting one value from each dimension. Example: (Vegan, Italian, Multi-step). This manual work helps you understand your problem space."

Two-step generation: first scale tuples via LLM, then in a *separate prompt* convert each tuple into a natural-language query. This separation avoids repetitive phrasing.

### 3.5 Binary > Likert (verbatim)

From §"Why do you recommend binary (pass/fail) evaluations instead of 1-5 ratings (Likert scales)?":

> "Binary evaluations force clearer thinking and more consistent labeling. Likert scales introduce significant challenges: the difference between adjacent points (like 3 vs 4) is subjective and inconsistent across annotators, detecting statistical differences requires larger sample sizes, and annotators often default to middle values to avoid making hard decisions. Having binary options forces people to make a decision rather than hiding uncertainty in middle values."

Implication for compound scoring: "instead of rating factual accuracy 1-5, you could track '4 out of 5 expected facts included' as separate binary checks." Decompose a numeric score into orthogonal binary checks rather than asking the judge for a real number.

### 3.6 LLM-as-judge — when it works, when it doesn't

From §"Can I use the same model for both the main task and evaluation?":

> "For LLM-as-Judge selection, using the same model is usually fine because the judge is doing a different task than your main LLM pipeline. While research has shown that models can exhibit bias when evaluating their own outputs, what ultimately matters is how well your judge aligns with human judgments. The judges we recommend building do scoped binary classification tasks. We've found that iterative alignment with human labels is usually achievable on this constrained task. Focus on achieving high True Positive Rate (TPR) and True Negative Rate (TNR) with your judge on a held out labeled test set. If you struggle to achieve good alignment with human scores, then consider trying a different model."

**Correction vs prior report (revised under issue #29):** the *FAQ* does not state "Hamel reports >90% agreement with a domain expert in three iterations" — earlier-prior-report removed the claim on those grounds. But the **llm-judge post does carry it verbatim** in the Honeycomb Query Assistant case study (hamel.dev/blog/posts/llm-judge/ §"Keep Iterating on the Prompt Until Convergence With Domain Expert"):

> "It took us only three iterations to achieve > 90% agreement between the LLM and Phillip. Your mileage may vary depending on the complexity of the task."

The 2025 field-guide post re-states the same finding (§"Measure Alignment Between Automated Evals and Human Judgment"): "It took three iterations to achieve >90% agreement, but this investment paid off in a system the team could trust." The claim is therefore **reinstated and re-anchored** to the llm-judge / field-guide rather than to the FAQ. Both posts also append the warning that raw agreement is misleading on imbalanced datasets — precision/recall (or TPR/TNR per the FAQ) should be the metric of record once the class balance shifts.

Avoid generic metrics (§"Should I use 'ready-to-use' evaluation metrics?"):

> "Generic evaluations waste time and create false confidence… These metrics measure abstract qualities that may not matter for your use case. Good scores on them don't mean your system works."

A quote the FAQ pulls from the course: "*The abuse of generic metrics is endemic. Many eval vendors promote off the shelf metrics, which ensnare engineers into superfluous tasks.*"

### 3.7 Other process-level guidance worth surfacing

- **Benevolent dictator over committee.** A single domain expert is the most effective annotator structure for most teams; "if you feel like you need five subject matter experts to judge a single interaction, it's a sign your product scope might be too broad."
- **Don't outsource error analysis.** "Outsourcing error analysis is usually a big mistake (with some exceptions). The core of evaluation is building the product intuition that only comes from systematically analyzing your system's failures."
- **Re-run error analysis on a 2–4 week cycle** with at least 100 fresh traces per cycle; weekly outlier-review of 10–20 traces between cycles.
- **CI vs. production evals diverge.** CI uses small (100+ examples), curated, deterministic checks where possible. Production sampling uses asynchronous LLM-as-judge with confidence intervals.
- **Eval-driven development is mostly wrong.** "Generally no. Eval-driven development (writing evaluators before implementing features) sounds appealing but creates more problems than it solves. Unlike traditional software where failure modes are predictable, LLMs have infinite surface area for potential failures. You can't anticipate what will break." Exception: hard constraints like "never mention competitors."
- **Agentic workflows are evaluated in two phases:** (1) end-to-end task success ("did we meet the user's goal?"); (2) step-level diagnostics (tool choice, parameter extraction, error handling, context retention, efficiency, goal checkpoints). Use **transition failure matrices** ("last successful state vs. where the first failure occurred") to localize hotspots.
- **Annotate only the first failure in a trace** initially; downstream failures often cascade from the first.
- **Criteria drift is real:** "evaluation criteria tends to shift after reviewing a model's outputs, a phenomenon known as 'criteria drift'" (citing Shankar et al., "Who Validates the Validators?", arXiv:2404.12272). This is why prompt optimization tools that hill-climb a fixed metric miss the point.

### 3.8 Concrete checklist (distilled)

1. Collect 100+ real traces (or synthesize from hand-written dimension tuples).
2. Open-code failure modes; cluster into a taxonomy via axial coding.
3. For each cluster, decide: code check (cheap) or LLM judge (expensive — only for persistent generalization failures).
4. For LLM-judge clusters: binary, one failure mode per prompt, iteratively align with a domain expert until TPR & TNR are acceptable on a held-out set.
5. Re-run error analysis every 2–4 weeks; harvest new modes; harden the set when pass rate climbs out of the discriminating band.
6. Keep an "open-bench" of edge cases that humans review but the judge does not — to detect drift.

### 3.9 Critique Shadowing — the llm-judge operational manual (Husain, Oct 2024)

Husain's "Using LLM-as-a-Judge For Evaluation: A Complete Guide" (hamel.dev/blog/posts/llm-judge/) is the operational manual the FAQ assumes you've read. It names the process **Critique Shadowing** and breaks it into seven steps. Each step has a load-bearing detail not present in the FAQ:

**Step 1 — Find *The* Principal Domain Expert.** Verbatim (§"Step 1"):

> "In most organizations there is usually one (maybe two) key individuals whose judgment is crucial for the success of your AI product. […] Many developers attempt to act as the domain expert themselves, or find a convenient proxy (ex: their superior). This is a recipe for disaster. People will have varying opinions about what is acceptable, and you can't make everyone happy. What's important is that your principal domain expert is satisfied."

The "benevolent dictator" guidance in the FAQ §3.7 derives from this. Husain explicitly lists exception cases: for independent developers the developer *is* the expert; for small companies it may be the CEO; for AI-augmenting-leadership scenarios "you should regularly validate their assumptions against real user feedback."

**Step 2 — Create a Dataset across three dimensions.** Husain's canonical taxonomy is **Features × Scenarios × Personas**, with worked tables for a B2C example (order tracking / contact search / meeting scheduler × multiple-matches / no-matches / ambiguous-request / invalid-data / system-errors / incomplete-information / unsupported-feature × new-user / expert / non-native-speaker / busy-professional / technophobe / elderly). Verbatim caveat:

> "This taxonomy (features, scenarios, personas) is not universal. […] The idea is you should outline dimensions that make sense for your use case and generate data that covers them. You'll likely refine these after the first round of evaluations."

**Step 3 — Pass/fail with critiques.** The non-negotiable: the domain expert outputs a binary plus a *detailed* critique. The critique's purpose is not just explanation:

> "The critique should be detailed enough so that you can use it in a few-shot prompt for a LLM judge. In other words, it should be detailed enough that a new employee could understand it. Being too terse is a common mistake."

Critiques have a hidden second function — they force domain experts to externalize tacit knowledge:

> "In practice, domain experts may not have fully internalized all the judgment criteria. By forcing them to make a pass/fail decision and explain their reasoning, they clarify their expectations and provide valuable guidance for refining the AI."

**Step 4 — Fix obvious errors before building the judge.** "Remember, the whole point of the LLM as a judge is to help you find these errors, so it's totally fine if you find them earlier!" Don't build a judge to detect bugs that human review surfaces immediately.

**Step 5 — Build the judge iteratively, using the critiques as few-shot examples.** The Honeycomb Query Assistant prompt template is given verbatim and is reproducible: NLQ in `<nlq>`, generated query in `<query>`, critique + outcome in `<critique>` tags, three labelled examples wrapped in `<examples>…</examples>`. Three iterations were enough to reach >90% agreement (see §3.6 above for the corrected attribution).

Husain explicitly warns against four common judge-prompt mistakes (§"Mistakes I've noticed in LLM judge prompts"): no critiques in the examples; terse critiques; missing external context (user metadata, system state); insufficiently diverse examples.

**Step 6 — Error analysis on the judge's outputs.** Once the judge is aligned, run it on unseen data and **slice the failure rate by dimension** (feature × scenario × persona). Husain's worked example table shows a "No Matches × New User" cell at 75% failure for Order Tracking, vs ~20% elsewhere — the kind of localized hotspot that bottom-up error analysis surfaces but generic metrics hide. Root-cause every failed trace into a small taxonomy (his example: Missing User Education 40%, Authentication/Access Issues 30%, Poor Context Handling 20%, Inadequate Error Messages 10%). 15 minutes of classification is enough to start.

**Step 7 — Specialized judges only after Steps 1-6.** "The key takeaway is don't jump directly to using specialized LLM judges until you have gone through this critique shadowing process."

**The meta-claim, verbatim (§"It's Not The Judge That Created Value, After all"):**

> "The real value of this process is looking at your data and doing careful analysis. Even though an AI judge can be a helpful tool, going through this process is what drives results. I would go as far as saying that creating a LLM judge is a nice 'hack' I use to trick people into carefully looking at their data!"

**Implication for our architectures:** Critique Shadowing is the procedure that should produce the *initial* judge / V&V / fitness component prompts in every architecture — not designer intuition. Architecture 1's judge prompts, Architecture 3's V&V agent prompts, Architecture 4's fitness component prompts, and Architecture 2's persona reviewer prompts should each be the output of running Steps 1-5 on a real dataset with a real domain expert (the Operator, or a designated SME). The FAQ's continuous discipline (§3.7's 2-4 week error-analysis cycle) is then how the judge stays aligned over time.

### 3.10 Synthetic data with zero users — the Rechat/Lucy pattern

The llm-judge post and field-guide together give a concrete, reproducible recipe for bootstrapping evals when no user data exists. The field-guide formalizes it as **dimensions → grounded prompts → real-data-backed scenario verification**. Verbatim from field-guide §4:

> "The key to useful synthetic data is grounding it in real system constraints. […] 1. Using real listing IDs and addresses from their database. 2. Incorporating actual agent schedules and availability windows. 3. Respecting business rules like showing restrictions and notice periods. 4. Including market-specific details like HOA requirements or local regulations."

And the verification loop (verbatim):

> "Verify scenario coverage: Ensure your generated data actually triggers the scenarios you want to test. A query intended to test 'no matches found' should actually return zero results when run against your system."

This raises the bar above the FAQ's "hand-write 20 dimension tuples" guidance: the tuples must be *backed by real system state*, and the generated query must be *executed against that state* to confirm the scenario fires. For Architecture 4 (Tournament), this means every fitness scenario should be backed by a real artifact in a test fixture, not just a textual description.

Bryan Bischof's blessing (quoted in both posts):

> "LLMs are surprisingly good at generating excellent - and diverse - examples of user prompts. […] If this sounds a bit like the Large Language Snake is eating its tail, I was just as surprised as you! All I can say is: it works, ship it."

---

## 4. Implications for the four architectures

### 4.1 Architecture 1 — Specification Refinery (LLM judge)

The Refinery's judge scores probe artifacts against ACs. Husain's discipline says:

- **Reframe judge prompts as binary checks per AC**, not holistic "does the probe satisfy the spec?" scoring. Each Given/When/Then becomes its own yes/no judge call. This matches the FAQ's "instead of rating factual accuracy 1-5, you could track '4 out of 5 expected facts included' as separate binary checks."
- **Budget explicit error-analysis time inside each revelation cycle.** Reserve (e.g.) 30 minutes of Operator review per layer to spot-check 20 judge calls and refresh prompts when alignment drifts. The FAQ's "review 10-20 traces weekly" cadence maps directly.
- **Hold pass-rate in a stress-testing band by raising AC difficulty as the spec matures.** A layer whose probes pass all judges is either finished or vacuous; the curator must distinguish.
- **Borrow Anthropic's single-judge-with-rubric pattern** for the few cases where a holistic score is needed (e.g. ranking competing probes): one LLM call, structured rubric, 0.0–1.0 + pass/fail.

### 4.2 Architecture 2 — Compound Atelier (multi-persona review panel)

- **Each persona's review is an LLM judge.** Align each persona prompt against a domain expert's labels on a held-out set until TPR/TNR are acceptable. Without alignment, the panel may look diverse but be uniformly biased.
- **Compound the eval set itself.** Every panel disagreement is a data point — write divergent traces into the knowledge store with the resolution. The panel learns from its own past splits, applying compound-engineering to evals.
- **Beware of the "100% panel approval" signal.** Raise the bar: add an adversarial reviewer, or raise the complexity threshold for the auto-merge path. Aim for the discriminating band (Husain's 70% pole).
- **Annotate only the first failure** when reviewing panel disagreements; downstream cascades follow.

### 4.3 Architecture 3 — Phase-Gated Foundry (independent V&V)

The Foundry's V&V agent is the most judge-like structure of the four:

- **Independent provider for V&V is correct** but the FAQ qualifies this: using the same model is fine *if* you can achieve TPR/TNR alignment on a held-out set. Reinforce that V&V's provider must differ from implementation *when alignment fails*, not by default.
- **Phase gates should publish a TPR/TNR estimate**, not just pass/fail. Each gate's V&V agent needs a held-out alignment set of past phase artifacts that domain experts labelled. A gate whose V&V hasn't been re-aligned in N cycles is suspect.
- **Apply the "60–80% error-analysis budget" to phase budgets.** Carve out an explicit error-analysis sub-phase that runs every K cycles and updates V&V prompts/rubrics from accumulated failure modes.
- **Bound multi-judge experiments.** Anthropic's finding (single judge beat multi-judge) suggests starting with one well-aligned judge per phase and escalating only if alignment fails.
- **End-state evaluation** maps onto Foundry V&V: rather than judging every intermediate state, define checkpoints where specific state changes should have occurred (Anthropic Appendix, §"End-state evaluation").

### 4.4 Architecture 4 — Evolutionary Tournament (fitness components)

The Tournament's fitness function is the highest-stakes judge of the four and the most exposed to **reward hacking** (F2):

- **Each fitness component is a binary check or a calibrated 0.0–1.0 score** (Anthropic pattern). Multi-dimensional vectors are fine, but each dimension must be independently aligned via TPR/TNR on a held-out set.
- **Hold pass-rate in a stress-testing band by raising scenario difficulty.** If the population uniformly clears the bar, Predator should generate harder scenarios (the architecture already calls for this; the evals lens reinforces *why*).
- **Lineage logs are error-analysis logs.** Tag and cluster every losing genome's failure mode; new fitness components emerge from clusters, not from designer intuition. This is Husain's open/axial coding applied to a tournament.
- **Subagent-as-context-window pattern fits naturally.** Each fitness evaluator is a subagent: consumes the genome, runs its check, returns a number plus a one-sentence justification. The orchestrator never reads raw traces — and the **filesystem-as-shared-artifact** pattern from Anthropic's Appendix avoids passing raw genome state through the orchestrator's context.
- **Adopt Anthropic's single-judge-with-rubric for satisfaction.** The satisfaction-as-judge channel should be a single LLM call against a stable rubric, calibrated against held-out human satisfaction ratings.
- **Token economics matter.** Anthropic's 15× multi-agent tax means each generation in a tournament with N subagent evaluators per genome multiplies cost; the Tournament value-of-task threshold needs to clear this bar before scaling population size.

### 4.5 Roadmap reframing — count experiments, not features (Husain field-guide §6)

Hamel's field-guide closes with a roadmap-level argument that lands directly on the planning posture in `architectures/`. Verbatim:

> "Traditional roadmaps assume we know what's possible. With conventional software, that's often true — given enough time and resources, you can build most features reliably. With AI, especially at the cutting edge, you're constantly testing the boundaries of what's feasible. […] The key metric for AI roadmaps isn't features shipped — it's experiments run."

Two operational patterns:

**(a) The Capability Funnel (Bryan Bischof, ex-Hex).** Decompose every feature into progressive levels of utility so that *partial* progress is legible. Example for a query assistant: (1) syntactically valid queries → (2) execute without errors → (3) return relevant results → (4) match user intent → (5) optimal queries that solve the user's problem. The funnel makes it possible to report "we're at level 3, climbing to level 4" instead of binary ship/no-ship — a much better fit for the long-tailed failure curves all four architectures generate.

**(b) The Fifteen-Five failure-sharing ritual (Eugene Yan).** A weekly written update — fifteen minutes to write, five minutes to read — that **explicitly documents failures alongside successes**, normalized by leadership going out of their way to share their own. Verbatim:

> "In my fifteen-fives, I document my failures and my successes. Within our team, we also have weekly 'no-prep sharing sessions' where we discuss what we've been working on and what we've learned. When I do this, I go out of my way to share failures."

The point is *cultural infrastructure* for an experiment-driven roadmap: failures become learning artifacts that other team members re-use, not events that get hidden.

**Eugene Yan's project-shape timeline** (also verbatim, useful as a project-planning template):

> "First, I take two weeks to do a data feasibility analysis, i.e 'do I have the right data?' Then I take an additional month to do a technical feasibility analysis, i.e 'can AI solve this?' After that, if it still works I'll spend six weeks building a prototype we can A/B test."

**Concrete numerical claim worth tracking:** Husain reports that including critique examples as few-shot in judge prompts "often yields 15-20% higher agreement rates between human and LLM evaluations compared to prompts without example critiques." (Field-guide §5.) Use this as the operational ROI argument when an architecture's judge prompts don't include critique examples.

**Implication for our docs:** the project plan in `research/PLAN.md` and the per-architecture roadmaps should count **experiments run per week** as a leading indicator, with feature ship dates as lagging indicators contingent on experiment outcomes. The Foundry's phase-gate cadence and the Tournament's generation cadence are already structured this way; the Refinery and Atelier roadmaps should adopt the same framing.

### 4.6 Cross-cutting recommendation

All four architectures should:

1. **Explicitly budget 60–80% of phase/cycle time to error analysis** until proven otherwise. Today's specs implicitly budget the inverse. Husain's verbatim claim: "we've spent 60-80% of our development time on error analysis and evaluation."
2. **Maintain an alignment set per judge / fitness component / persona** — a small held-out corpus of human-labelled examples, scored on TPR and TNR. A judge whose alignment hasn't been re-measured in N cycles is degraded by default.
3. **Track per-judge pass rate and re-harden when it leaves the stress-testing band.** Apply the "passing 100%" heuristic at every level: spec ACs, phase gates, fitness components, panel approval. Husain's anchor: 70% pass rate is healthier than 100%.
4. **Adopt Anthropic's subagent-as-context-preservation pattern** wherever an evaluation reads more than one context window's worth of intermediate state — most obviously in Tournament fitness eval and Foundry V&V on large artifacts. Persist plans to memory before 200k truncation; use the filesystem as an artifact bus.
5. **Adopt transition failure matrices** for any architecture with sequential phases (Foundry especially): rows are last-successful states, columns are first-failure locations.

---

## 5. Sources and access status

| Source | URL | Status |
|---|---|---|
| Anthropic — multi-agent research system | https://www.anthropic.com/engineering/multi-agent-research-system | ✅ Drained from `fetched/issue-24/` 2026-05-11 (orchestrator-worker pattern, 90.2% gain, single-judge finding, eight prompt principles, end-state eval) |
| Hamel Husain — Evals FAQ | https://hamel.dev/blog/posts/evals-faq/ | ✅ Drained from `fetched/issue-24/` 2026-05-11 (60-80% budget, 70% pass-rate band, open/axial coding, binary > Likert, criteria drift) |
| Simon Willison — endorsement of FAQ | https://simonwillison.net/2025/Jul/3/faqs-about-ai-evals/ | ✅ Re-anchored from `fetched/issue-29/` 2026-05-13 (second-order endorsement; verbatim pull quotes of the 60-80% and 70% pass-rate claims) |
| Simon Willison — endorsement of Anthropic post | https://simonwillison.net/2025/Jun/14/multi-agent-research-system/ | ✅ Re-anchored from `fetched/issue-29/` 2026-05-13 (foregrounds "tools in a loop" agent definition; surfaces open-sourced cookbook prompts and OODA loop block — §2.6) |
| Hamel Husain — "Your AI Product Needs Evals" | https://hamel.dev/blog/posts/evals/ | ✅ Drained from `fetched/issue-29/` 2026-05-13 (philosophical anchor; Level 1/2/3 hierarchy; "Eval Systems Unlock Superpowers For Free" — new §0) |
| Hamel Husain — "Creating an LLM-as-a-Judge" / Critique Shadowing | https://hamel.dev/blog/posts/llm-judge/ | ✅ Drained from `fetched/issue-29/` 2026-05-13 (7-step Critique Shadowing operational manual; Honeycomb >90%/3-iterations case; Features×Scenarios×Personas dataset taxonomy — new §3.9) |
| Hamel Husain — "A Field Guide to Rapidly Improving AI Products" | https://hamel.dev/blog/posts/field-guide/ | ✅ Drained from `fetched/issue-29/` 2026-05-13 (NurtureBoss 33%→95% case; Capability Funnel; fifteen-five ritual; "experiments not features" — new §4.5; 15-20% agreement lift from critique few-shots) |
| Anthropic — Demystifying evals for AI agents | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | ⏳ De-prioritized — the llm-judge post is now the canonical operational manual; this URL can be back-filled later only if a specific claim depends on it. |
| **AttractorBench** (`strongdm/attractorbench`) — NLSpec instruction-following benchmark | https://github.com/strongdm/attractorbench | ⏳ **FLAGGED (not drained here) — added 2026-05-16 per Cluster-C dispatch (see `research/27-dotfile-pipelines-as-product.md` §5).** Landing page captured at head `cb5797e` (Feb 26, 2026); Apache-2.0; 17 stars / 8 forks. Four tiers (0 Smoke, 1 Unified LLM SDK, 2 Coding Agent Loop, 3 Attractor Pipeline; ~30 / ~2,150 / ~1,450 / ~2,080 spec lines respectively; 7 / 35 / 20 / 28 conformance tests). Language-agnostic (`make build`/`make test`/`./bin/conformance`); deterministic mock-LLM verifier; **cost-aware weighted composite** (Main: 5% build + 5% self-test + 30% T1 + 30% T2 + 30% T3; Single-tier: 10% + 10% + 80%). **v13 leaderboard slate — Gemini best = 0.508**, flagged provisional pending burn-in. `AGENTS.md` curation runbook, manual `LEADERBOARD.md` + `RUN_LOG.md`. Eval-contamination defence: `specs/` in repo, conformance tests + mock server generated locally from `src/attractorbench/adapter.py`. Worth a full drain because: (a) the **tier structure** is the corpus's only working model for tiered conformance benchmarks of methodology-substrate systems; (b) the **cost-aware composite** is an incentive-structure design choice that pushes toward hybrid deterministic+LLM pipelines (relevant to the Tournament fitness-vector design); (c) **v13 / Gemini = 0.508** is the anchor for future-comparable runs (drain the leaderboard contents and cost-vs-conformance Pareto frontier across v1–v13); (d) the eval-contamination defence is a reproducibility pattern that should be cross-referenced into §3 (Husain/Shankar's "Don't peek at the test set" discipline). Cross-references: report 27 §5 (methodology-layer framing); followup/02 §11.8 (the runner-roster side of the same ecosystem). |

All six URLs targeted by the issue #29 drain are now anchored on verbatim quotes from the fetched markdown renders. Combined with the four URLs anchored under issue #24, the report is end-to-end primary-source-anchored. The "Demystifying evals" Anthropic post is superseded as the operational manual by Husain's llm-judge guide; the **AttractorBench** row is a forward-looking drain flag, not yet primary-source-anchored beyond the landing page metadata, scheduled for a future round per Cluster-C orchestrator decisions on 2026-05-16.

---

## 6. Open follow-ups

- Cross-reference with `research/09-jaymin-book-harnesses-practices-mental-models.md` for how Overstory frames its own evaluation — Jaymin's framework may already encode some of Husain's discipline implicitly.
- Map specific judge prompts in `architectures/01-specification-refinery.md` §judge into the binary-per-AC pattern as a concrete worked example.
- Author a small ADR proposing the "70% pass-rate band" as the project-wide eval-health KPI for any judge or fitness component shipped under the factory.
- ~~Fetch the two remaining tangential URLs (`anthropic.com/engineering/demystifying-evals-for-ai-agents`, `hamel.dev/blog/posts/llm-judge/`) in a follow-up fetch round to back-fill the few remaining secondary citations.~~ **Done (partial):** `hamel.dev/blog/posts/llm-judge/` drained under issue #29 (now the canonical Critique Shadowing manual, §3.9). The Anthropic "Demystifying evals" post is de-prioritized — no current claim depends on it.
- Consider adopting Anthropic's open-sourced research-lead-agent and research-subagent prompts (anthropics/anthropic-cookbook/patterns/agents/prompts) as the starting template for Foundry V&V subagents and Tournament fitness-evaluator subagents; the OODA-loop block in particular looks directly reusable (§2.6).
- Map the Capability Funnel (§4.5) onto each of the four architectures' progress reporting — e.g., Foundry phase gates and Tournament generation milestones probably already encode it implicitly but should make the levels explicit.
