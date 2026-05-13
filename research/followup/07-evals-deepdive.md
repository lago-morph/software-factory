# Round-3 Thread 7 — Evals Deep-Dive: Anthropic's Multi-Agent Research System and Husain/Shankar's Evals FAQ

**Date:** 2026-05-11
**Branch:** `claude/parallelize-with-subagents-SO0nR--sub-10`
**Plan reference:** `research/PLAN.md` §11.7
**One-line:** Simon Willison endorses both Anthropic's "How we built our multi-agent research system" and Hamel Husain & Shreya Shankar's "Frequently Asked Questions (And Answers) About AI Evals" as gold-standard primers; the eval discipline in all four of our architectures would be sharpened by reading them.

---

## 1. Why this thread exists

Every architecture in `architectures/` depends on evaluation whose quality is taken for granted: Architecture 1 (Refinery) uses an LLM judge against ACs; Architecture 3 (Foundry) uses independent V&V agents at phase gates; Architecture 4 (Tournament) uses a fitness vector to drive selection; Architecture 2 (Atelier) uses a multi-persona review panel where reviewers act as judges. All four assume the judge / fitness / V&V is good enough to discriminate. Two recent primary sources push back on that assumption and supply concrete guidance. This report extracts both and maps them onto our four architectures.

---

## 2. Anthropic — "How we built our multi-agent research system"

Published June 2025 on `anthropic.com/engineering`. The essay describes the production architecture behind Claude's Research feature: an **orchestrator-worker** pattern where a lead agent (Claude Opus 4) coordinates parallel subagents (Claude Sonnet 4) that each search and reason in isolated contexts, then hand summarized findings back.

### 2.1 Subagents as context-window primitives

The post's most important architectural claim is that **subagents are not just a parallelization trick — they are a context-preservation device**. Each subagent burns its own context window down to a short summary the lead aggregates, so the orchestrator never has to read raw results. The LeadResearcher writes its plan to a Memory store before the 200k-token limit truncates it, so even the orchestrator survives long sessions. Rule: when a task's intermediate state exceeds one context window, fan out to subagents whose only deliverable is a distilled artifact.

### 2.2 Eval methodology

Anthropic's eval setup, as described in the post and in companion writing (notably their "Demystifying evals for AI agents" engineering note):

- **LLM-as-judge with a structured rubric.** The judge evaluates each research output against: *factual accuracy* (claims match sources), *citation accuracy* (cited sources match claims), *completeness* (all requested aspects covered), *source quality* (primary > secondary), and *tool efficiency* (right tools, reasonable number of calls).
- **Single judge call beat multi-judge.** They tried using multiple LLM judges per dimension; a **single LLM call emitting a 0.0–1.0 score and pass/fail** was the most consistent and best-aligned with human judgement.
- **Humans alongside the judge, not below it.** Human evaluators catch what automation misses — hallucinations on unusual queries, subtle source-selection biases, edge-case system failures. The LLM judge scales review across thousands of runs; humans keep the judge honest.
- **Three factors explained 95% of performance variance** on the BrowseComp eval: token usage (80% alone), number of tool calls, and model choice. This is the kind of finding only error analysis on real traces produces.

### 2.3 Lessons learned

- Multi-agent (Opus lead + Sonnet workers) **outperformed single-agent Opus by 90.2%** on internal research eval — but burned ~4× the tokens. Pareto-relevant only where the task warrants it.
- Prompt iteration on the orchestrator's delegation prompt mattered enormously: the lead had to specify *what* a subagent should look for, in what *depth*, and *when to stop*. Under-specified subagent prompts caused redundant searches and conflicting summaries.
- Parallel subagents step on each other unless the lead has a clear delegation grammar enforcing non-overlapping mandates.

---

## 3. Husain & Shankar — "Frequently Asked Questions About AI Evals"

Published mid-2025 on `hamel.dev`, distilled from 700+ engineers and PMs Hamel and Shreya taught on Maven. Simon Willison's July 3, 2025 post on simonwillison.net flags it as **"the best resource I've seen for getting started with evals"**.

### 3.1 The "start small, evolve" methodology

- **Start with error analysis, not infrastructure.** Read 20–50 real LLM outputs by hand, label failure modes, cluster them, *then* design evals against the clusters. A Langfuse/Phoenix dashboard before this is premature optimization.
- **20 traces is the unit of work.** Heuristic: if 20 fresh traces surface no new failure category, you've reached *theoretical saturation* for that pass. Review at least 100 to start.
- **Synthetic data via hand-written dimension tuples.** E.g. a recipe bot's `(dietary_restriction, cuisine, complexity)` — write 20 tuples like `(Vegan, Italian, Multi-step)` to seed inputs. Forces explicit coverage.
- **The eval set evolves.** Every error-analysis pass produces new failure modes; each becomes a code check (cheap) or an LLM-judge prompt (flexible). The set grows like regression tests in mature engineering shops.

### 3.2 LLM-as-judge — when it works, when it doesn't

- **Binary classification works best.** "Did this output have failure mode X — yes/no?" is the shape an LLM judge can be reliably aligned on; multi-class or numeric scoring drifts.
- **Align iteratively.** Hamel reports **>90% agreement with a domain expert in three iterations**: judge labels a batch, expert labels the same batch, disagreements get root-caused, judge prompt is rewritten.
- **Measure TPR and TNR separately, not raw agreement.** With class imbalance, raw agreement is misleading; you need precision/recall (TPR/TNR) on a held-out set.
- **Use a different model for the judge than for the task** when possible; otherwise keep the prompts strictly separate so the judge doesn't share the task's blind spots.
- **Common failure modes:** (a) judge over-scoped, (b) alignment skipped (team trusts judge from day one), (c) no domain expert anchors the labels.

### 3.3 Error analysis as 60–80% of dev time

Husain's most-cited claim — and the one Simon highlighted: **on the projects Hamel has shipped, 60–80% of development time goes to error analysis and evaluation, not to model/prompt/code authoring.** This is the inverse of how most teams allocate effort. The implication: a software factory whose phase budgets assume coding dominates is mis-scoping its own bottleneck.

### 3.4 The "passing 100% of your evals" heuristic

> *"If you're passing 100% of your evals, your evals are too easy."*

The action it implies: **deliberately add harder cases until the pass rate drops into the 60–80% band**. A 70% pass rate signals the eval is doing real discrimination; a 100% pass rate signals the eval set has been outgrown and is now noise. Treat each pass-rate jump as a signal to harden the set, not to celebrate.

### 3.5 Concrete checklist (distilled)

1. Collect 100+ real traces (or synthesize from hand-written dimension tuples).
2. Open-code failure modes; cluster into a taxonomy.
3. For each cluster, decide: code check or LLM judge.
4. For LLM-judge clusters: binary, one failure mode per prompt, iteratively align with a domain expert until TPR & TNR are acceptable on a held-out set.
5. Re-run error analysis after every significant change; harvest new modes; harden the set when pass rate exceeds ~85%.
6. Keep an "open-bench" of edge cases that humans review but the judge does not — to detect drift.

---

## 4. Implications for the four architectures

### 4.1 Architecture 1 — Specification Refinery (LLM judge)

The Refinery's judge scores probe artifacts against ACs. Husain's discipline says:

- **Reframe judge prompts as binary checks per AC**, not holistic "does the probe satisfy the spec?" scoring. Each Given/When/Then becomes its own yes/no judge call.
- **Budget explicit error-analysis time inside each revelation cycle.** Reserve (e.g.) 30 minutes of Operator review per layer to spot-check 20 judge calls and refresh prompts when alignment drifts.
- **Hold pass-rate in the 60–80% band by raising AC difficulty as the spec matures.** A layer whose probes pass all judges is either finished or vacuous; the curator must distinguish.
- **Borrow Anthropic's single-judge-with-rubric pattern** for the few cases where a holistic score is needed (e.g. ranking competing probes).

### 4.2 Architecture 2 — Compound Atelier (multi-persona review panel)

- **Each persona's review is an LLM judge.** Align each persona prompt against a domain expert's labels on at least 50 historical reviews. Without alignment, the panel may look diverse but be uniformly biased.
- **Compound the eval set itself.** Every panel disagreement is a data point — write divergent traces into the knowledge store with the resolution. The panel learns from its own past splits, applying compound-engineering to evals.
- **Beware of the "100% panel approval" signal.** Raise the bar: add an adversarial reviewer, or raise the complexity threshold for the auto-merge path.

### 4.3 Architecture 3 — Phase-Gated Foundry (independent V&V)

The Foundry's V&V agent is the most judge-like structure of the four:

- **Independent provider for V&V is correct** and matches "use a different model for the judge." Reinforce that V&V's provider must differ from the implementation phase's provider.
- **Phase gates should publish a TPR/TNR estimate**, not just pass/fail. Each gate's V&V agent needs a held-out alignment set of past phase artifacts that domain experts labelled. A gate whose V&V hasn't been re-aligned in N cycles is suspect.
- **Apply the "60–80% error-analysis budget" to phase budgets.** Carve out an explicit error-analysis sub-phase that runs every K cycles and updates V&V prompts/rubrics from accumulated failure modes.
- **Bound multi-judge experiments.** Anthropic's finding (single judge beat multi-judge) suggests starting with one well-aligned judge per phase and escalating only if alignment fails.

### 4.4 Architecture 4 — Evolutionary Tournament (fitness components)

The Tournament's fitness function is the highest-stakes judge of the four and the most exposed to **reward hacking** (F2):

- **Each fitness component is a binary check or a calibrated 0.0–1.0 score.** Multi-dimensional vectors are fine, but each dimension must be independently aligned.
- **Hold pass-rate in the 60–80% band by raising scenario difficulty.** If the population uniformly clears the bar, Predator should generate harder scenarios (the architecture already calls for this; the evals lens reinforces *why*).
- **Lineage logs are error-analysis logs.** Tag and cluster every losing genome's failure mode; new fitness components emerge from clusters, not from designer intuition.
- **Subagent-as-context-window pattern fits naturally.** Each fitness evaluator is a subagent: consumes the genome, runs its check, returns a number plus a one-sentence justification. The orchestrator never reads raw traces.
- **Adopt Anthropic's single-judge-with-rubric for satisfaction.** The satisfaction-as-judge channel should be a single LLM call against a stable rubric, calibrated against held-out human satisfaction ratings.

### 4.5 Cross-cutting recommendation

All four architectures should:

1. **Explicitly budget 60–80% of phase/cycle time to error analysis** until proven otherwise. Today's specs implicitly budget the inverse.
2. **Maintain an alignment set per judge / fitness component / persona** — a small held-out corpus of human-labelled examples. A judge whose alignment hasn't been re-measured in N cycles is degraded by default.
3. **Track per-judge pass rate and re-harden when it crosses ~85%.** Apply the "passing 100%" heuristic at every level: spec ACs, phase gates, fitness components, panel approval.
4. **Adopt Anthropic's subagent-as-context-preservation pattern** wherever an evaluation reads more than one context window's worth of intermediate state — most obviously in Tournament fitness eval and Foundry V&V on large artifacts.

---

## 5. Sources and access status

| Source | URL | Status |
|---|---|---|
| Anthropic — multi-agent research system | https://www.anthropic.com/engineering/multi-agent-research-system | 403; recovered via WebSearch summaries |
| Hamel Husain — Evals FAQ | https://hamel.dev/blog/posts/evals-faq/ | 403; recovered via WebSearch summaries |
| Simon Willison — endorsement of FAQ | https://simonwillison.net/2025/Jul/3/faqs-about-ai-evals/ | 403; cited from search excerpts |
| Simon Willison — endorsement of Anthropic post | https://simonwillison.net/2025/Jun/14/multi-agent-research-system/ | 403; cited from search excerpts |
| Anthropic — Demystifying evals for AI agents | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Referenced via search excerpts |
| Hamel Husain — LLM-as-judge guide | https://hamel.dev/blog/posts/llm-judge/ | 403; referenced via search excerpts |

Sandbox blocks `anthropic.com`, `hamel.dev`, `simonwillison.net`, and `web.archive.org`. The substance of every claim above (60–80% error analysis, "passing 100%" heuristic, rubric components, single-judge finding, 90.2% multi-agent gain, 20-trace saturation) is independently cited by multiple search-result summaries; exact phrasing of direct quotes should be confirmed when URLs become reachable. A `[fetch-urls]` issue is recorded as a follow-up rather than filed unilaterally, since prior fetch issues already cover these hosts.

---

## 6. Open follow-ups

- Verbatim retrieval of the four primary URLs via the fetch-blocked-urls workflow, to confirm direct quotes (especially the exact "passing 100%" phrasing and the 60–80% number's surrounding context).
- Cross-reference with `research/09-jaymin-book-harnesses-practices-mental-models.md` for how Overstory frames its own evaluation — Jaymin's framework may already encode some of Husain's discipline implicitly.
- Map specific judge prompts in `architectures/01-specification-refinery.md` §judge into the binary-per-AC pattern as a concrete worked example.
- Author a small ADR proposing the "60–80% pass-rate band" as the project-wide eval-health KPI for any judge or fitness component shipped under the factory.
