# Research Report 22 — Academic Foundations: AlphaCode, SWE-bench, SWE-agent, CodeGen

**Date:** 2026-05-11
**Author:** Round-5 Cluster 13.1.5 subagent (fanout run 20260511-054258, sub-24)
**Scope:** Read S4 (AlphaCode), S5 (SWE-bench), S6 (SWE-agent paper), S7 (SWE-agent project docs) plus a primary CodeGen reference. Extract the academic foundations underneath the four agentic-coding architectures in `architectures/`. Compare against `research/05-simon-willison.md`, `research/11-openhands-substrate-audit.md`, and (the §11.7 evals deep-dive — not yet merged on this branch; cross-reference deferred).

## Sources reviewed

Status legend: ✅ full review · 🟡 reconstructed from excerpts / abstracts · ⏳ retrieval pending via fetch issue · ❌ unobtainable.

| Source ID | Citation | URL | Status | Notes |
|---|---|---|---|---|
| S4 | Li et al. *Competition-Level Code Generation with AlphaCode* (2022) | https://arxiv.org/abs/2203.07814 | 🟡 | arxiv direct fetch 403; ar5iv mirror also 403; DeepMind blog 403. Reconstructed from WebSearch excerpts of the paper + DeepMind blog + community summaries. Filed fetch issue #28 for full-text capture. |
| S5 | Jimenez et al. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* (ICLR 2024) | https://arxiv.org/abs/2310.06770 | 🟡 | arxiv 403; swebench.com 403; pli.princeton.edu blog 403. Reconstructed from WebSearch excerpts of the abstract, the OpenReview record, and the Princeton blog. Filed fetch issue #28. |
| S6 | Yang et al. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering* (NeurIPS 2024) | https://arxiv.org/abs/2405.15793 | 🟡 | arxiv 403; swe-agent.com 403. Reconstructed from WebSearch excerpts of the paper's abstract and §3, plus the project's ACI background page (also 403, content inferred from project README). Filed fetch issue #28. |
| S7 | SWE-agent Team. *Getting Started* (n.d.) — and mini-SWE-agent README | https://swe-agent.com/latest/ · https://github.com/SWE-agent/mini-swe-agent | ✅ (mini-SWE-agent README via direct WebFetch) / 🟡 (latest docs page) | mini-SWE-agent GitHub README fetched directly (October 2025 content, page advertises ">74% on SWE-bench Verified" with Gemini 3 Pro as of an undated X/Twitter post). swe-agent.com/latest 403 from sandbox. |
| — (CodeGen) | Nijkamp et al. *CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis* (ICLR 2023) | https://arxiv.org/abs/2203.13474 | 🟡 | arxiv 403; OpenReview 403; Hugging Face papers page 403; Semantic Scholar 403. Reconstructed from WebSearch excerpts of the abstract + Salesforce CodeGen GitHub README (the latter fetched directly). Filed fetch issue #28. |

**Date stamp on all benchmark numbers:** unless otherwise noted, every benchmark number in this report is reported as of 2026-05-10 to 2026-05-11 — the access window for this Round-5 pass. Benchmark numbers are time-sensitive; the SWE-bench leaderboard in particular moves week-over-week.

---

## 1. Why these four, why now

The Round-5 plan (§13.1.5) flags an asymmetry in our corpus: most of what we have is *practitioner* material — StrongDM, Simon Willison, Every.to, El Kaim, the Anthropic/OpenAI/GitHub product blogs — and the academic substrate that those practitioners build on is referenced indirectly but never collated. The four papers in scope are the substrate, in roughly chronological order:

1. **AlphaCode (Li et al., 2022 — S4).** The first end-to-end demonstration that *generate-many-then-verify* could solve nontrivial code tasks at a competitive level. The pipeline — extreme-scale sampling, filter-by-example-tests, cluster-by-behavior, submit the top representatives — is the ur-pattern of orchestration-and-verification. Codeforces 54.3% (top half of human competitors) was the headline number per S4.
2. **CodeGen (Nijkamp et al., 2022).** The first open-source 16B-parameter family for code, and (critically for our purposes) the introduction of the **Multi-Turn Programming Benchmark (MTPB)** — 115 problem sets factorized into multi-turn prompts — with the finding that decomposing a single intent across multiple turns *significantly* improves synthesis quality versus posing the same intent in a single prompt. This is the academic version of the modern "spec → plan → implement → test" loop.
3. **SWE-bench (Jimenez et al., ICLR 2024 — S5).** The first benchmark that grounded "can language models do software engineering" in *real GitHub issues from real Python repos*. 2,294 task instances drawn from 12 repositories, each task with a Fail-to-Pass test set as the ground truth. The original baseline pass rates were in the single digits.
4. **SWE-agent (Yang et al., NeurIPS 2024 — S6).** The "12.5% pass@1 on SWE-bench" paper, and more importantly the paper that named and operationalized the **agent-computer interface (ACI)**: simple, efficient, LM-centric commands and feedback formats. The trajectory since — 12.5% (May 2024) → 65% mini-SWE-agent (Aug 2025) → >74% (early 2026, per S7's mini-SWE-agent README) — is the closest thing the field has to a public "factory yield" learning curve.

These four together describe the academic ancestry of every architecture in `architectures/`:

- The **Atelier** (multi-reviewer panel) ancestry is AlphaCode's sample-and-cluster — sample diverse candidates, score them, select.
- The **Foundry** (phase-gated pipeline) ancestry is SWE-bench's Fail-to-Pass evaluation criterion plus CodeGen's multi-turn factorization — both are "the spec is a list of acceptance gates."
- The **Lighthouse** (one human + small fleet) ancestry is SWE-agent's ACI insight — a single LM driving a careful tool surface can outperform far more complex setups.
- The **Mill** (high-throughput dark factory) ancestry is the AlphaCode pipeline scaled up: generate a fleet of candidates, filter by held-out scenarios, cluster, ship the cluster representative. StrongDM's "satisfaction scoring" is the modern descendant.

## 2. AlphaCode (S4) — orchestration-and-verification, before "agents" were a word

AlphaCode is best read today as the first **orchestrated** code-generation system, not as a language-model paper. The model is a transformer (up to 41B parameters in the published numbers), but the load-bearing engineering is the pipeline around the model. Per S4 and the DeepMind blog summary:

**The pipeline (S4).**

1. **Generate up to one million candidate programs per problem.** This is the "sampling" stage — deliberately oversampled to cover the search space. AlphaCode trains the model with strong sample diversity (random temperature, varied prompts) precisely because the downstream pipeline can afford to throw most of them away.
2. **Filter using the example tests bundled with each problem.** Competitive-programming problems come with a handful of example inputs and outputs. AlphaCode runs each candidate against those tests and discards the ones that fail. Per the DeepMind summary, this filter alone removes roughly 99% of generated candidates.
3. **Cluster the survivors by program behavior.** The remaining candidates are run on additional model-generated test inputs, and grouped by their output equivalence class — programs that produce the same outputs on the same inputs are clustered together. This step finds *behavioral consensus* rather than syntactic similarity.
4. **Submit one representative from each of the 10 largest clusters.** The rationale, per S4: the largest behavioral clusters represent the most common solution strategies, which are statistically more likely to be correct. The submission budget is 10 per problem (matching Codeforces' contest rules).

**The headline result (S4, dated 2022-03-16).** "AlphaCode achieved an average ranking of top **54.3%** in simulated evaluations on recent programming competitions on the Codeforces platform with more than 5,000 participants." Top half of human competitors, in other words. As of 2026-05-11 this number is four years old, but it remains the canonical citation.

**The three components per S4.** The paper explicitly names three ingredients as critical: "(1) an extensive and clean competitive programming dataset for training and evaluation, (2) large and efficient-to-sample transformer-based architectures, and (3) large-scale model sampling to explore the search space, followed by filtering based on program behavior to a small set of submissions."

**What this contributes to our architectures.** AlphaCode is the prototype of the **generate-then-verify** loop. Three observations transfer directly:

- *Diversity over fidelity at the sampling stage.* The model is trained to produce many plausible candidates, not one polished one. This is the academic predecessor of StrongDM's "code is cheap, fire off the prompt anyway" — and of Simon Willison's "parallel coding agents" pattern (`research/05-simon-willison.md`, Oct 5 2025 post).
- *Example tests as the cheap filter.* The first sieve is the cheap one. This anticipates Simon's "first run the tests" pattern and the Foundry architecture's static-gate phase.
- *Cluster-by-behavior as the consensus filter.* This is the academic version of "let the satisfaction score break ties" — a probabilistic, trajectory-aware quality bar rather than a single boolean. The StrongDM scenario/satisfaction methodology (`research/05-simon-willison.md` §"The software factory post") is the practitioner descendant.

**What AlphaCode does *not* model.** It assumes a stateless single-shot problem (competitive programming), not a multi-turn engineering task. There is no spec refinement, no test authoring (tests are given), no deployment, no review, no organizational context. It is a beautiful demonstration of orchestration-and-verification at the *algorithm* scale, but the unit of work is one self-contained problem, not a real-world change to a 100k-line repo.

## 3. CodeGen (Nijkamp et al., 2022) — multi-turn synthesis as the academic frame

CodeGen was released March 25, 2022 as Salesforce Research's open-source answer to Codex. The CodeGen family (350M, 1B, 3B, 7B, 16B parameters; CodeGen1 and CodeGen2 variants) was trained on a mix of natural language and code, on TPU-v4, and released along with the **JAXFORMER** training library. The Salesforce GitHub README claims the models are "competitive with OpenAI Codex" on standard benchmarks.

**The multi-turn contribution.** The paper's distinctive academic move is the **Multi-Turn Programming Benchmark (MTPB)** — a deliberately constructed benchmark of **115 diverse problem sets**, each factorized into a sequence of natural-language prompts that together describe the target program. The headline empirical finding (paraphrased from the abstract): "the same intent provided to CODEGEN in multi-turn fashion significantly improves program synthesis over that provided as a single turn."

In other words: if you give the model *the same total instruction* in pieces, it produces better code than if you give it all at once. This is the academic precedent for nearly every modern coding-agent practice that decomposes work — plan-mode in Codex, the planner / coder / reviewer split in compound engineering, the spec-then-test-then-implement loop in Simon Willison's red/green TDD chapter, the SWE-agent ACI's separation of *navigate*, *view*, *edit*, *test*. It is also the academic ancestor of the **`AGENTS.md` + tests + scenarios** layered spec that `research/05-simon-willison.md` §"Specification methodology" describes.

**What this contributes to our architectures.** Three transfers:

- *Decomposition is empirically free yield.* The MTPB finding is not "decomposition is sometimes useful"; it is "decomposition significantly improves synthesis on the same total intent." This is the academic license for the Foundry's phase gates and the Atelier's reviewer-panel.
- *The benchmark format itself.* MTPB is a *spec-as-conversation* benchmark — each problem is a sequence of natural-language sub-specifications. This is the closest published analogue to what StrongDM's Attractor repo *is* — three markdown files that together specify the system (per `research/05-simon-willison.md`).
- *Open-source baseline.* CodeGen also matters as the first credibly-open large code model. Every "open-source agent harness" thread in our corpus (OpenHands, mini-SWE-agent, the StrongDM cxdb release) rests on the existence of credible open code models.

**Status caveat on CodeGen citation.** The Round-5 sources audit (`research/external-syntheses/chatgpt-deep-research-2026-05-11/sources.md` §"Weak or missing citations") flagged CodeGen as one of the named-but-uncited references in the original report. This report adopts arXiv 2203.13474 as the canonical primary citation. The Salesforce GitHub repository (`github.com/salesforce/CodeGen`) was directly fetchable from the sandbox and confirms the model family, training substrate, and the multi-turn framing — the paper itself was not directly fetchable (filed in fetch issue #28).

## 4. SWE-bench (S5) — realistic-issue benchmarking, and its blind spots

SWE-bench is the benchmark that finally made "can the model do my job" a falsifiable question. Per the abstract and the Princeton blog summary:

**The dataset (S5).** **2,294 task instances** drawn from **12 popular Python repositories** (the Princeton blog lists django, sympy, scikit-learn, matplotlib, sphinx, requests, flask, pylint, astropy, seaborn, xarray, pytest). Each instance is constructed from a real pull request that (a) is associated with a real issue and (b) modifies at least one test-related file. For each instance the benchmark provides a Docker image with the repo installed at the *pre-PR* commit, plus the issue text, plus a designated set of "Fail-to-Pass" tests that fail without the PR's changes and pass after.

**The evaluation criterion.** The model receives the issue text and is asked to modify the codebase. After it claims to be done, the benchmark applies its patch and runs the Fail-to-Pass tests. If they pass, the instance is resolved.

**The original baselines (May 2024 / paper publication).** Per the original paper and S6 (which uses the original SWE-bench as its evaluation target): Claude 2 and GPT-4 scored in single digits without an agent harness. The state-of-the-art *before* SWE-agent was around 4-5% pass@1.

**Variants (as of 2026-05-11).**

- **SWE-bench Full** (the original 2,294-instance benchmark).
- **SWE-bench Lite** (a 300-instance simpler subset for low-cost evaluation).
- **SWE-bench Verified** (a **500-instance** human-verified curation released by OpenAI in August 2024, addressing concerns that some original instances had under-specified issues, brittle tests, or environment problems — see OpenAI's "Introducing SWE-bench Verified" post, filed for fetch in issue #28).
- **SWE-bench Multimodal** and **SWE-bench Multilingual** — later extensions to non-Python and non-text issues.

**The trajectory (dated benchmark numbers as of 2026-05-11).** SWE-bench Verified is the variant most commonly reported in 2026. Per the mini-SWE-agent README (fetched directly from GitHub on 2026-05-11): "scores >74% on SWE-bench Verified" (with Gemini 3 Pro on a 100-line bash-only harness). The S7 SWE-agent project docs preserve an older 65% Verified number on mini-SWE-agent (per `sources.md` §"time-sensitive benchmark numbers"). Both numbers should be treated as date-stamped snapshots — the leaderboard moves.

**What SWE-bench measures.**

- *Code reading at scale.* The repo is real; the agent has to navigate it.
- *Issue interpretation.* The issue text is real and frequently under-specified.
- *Patch generation under test pressure.* The Fail-to-Pass tests are the acceptance criterion.
- *Test setup robustness.* The benchmark's Docker images force the agent to handle a real install + test runner.

**What SWE-bench explicitly does NOT measure** — and this is where the benchmark stops short of the four architectures' actual scope:

1. **Spec refinement.** SWE-bench gives the agent the issue text *as is*. There is no incentive for the agent to push back on a bad spec, to ask clarifying questions, or to refine the spec before coding. In real software development the spec is itself a work product that evolves — the "revelation cycle" in our spec-driven baseline (`spec-driven-ai-dev.md`) is precisely the spec-refinement step that SWE-bench skips by construction.
2. **Test authoring.** The Fail-to-Pass tests are *given* by the benchmark. The agent does not write them. This eliminates the single hardest problem in real-world agentic development (Simon Willison's "how can you prove that software you are producing works if both the implementation and the tests are being written for you by coding agents?", Feb 7 2026) — and elides the StrongDM scenario / DTU / satisfaction-scoring practice entirely.
3. **Deployment safety.** SWE-bench does not deploy anything. There is no canary, no rollback, no feature flag, no migration, no observability. The agent's output is a patch, not a shipped change.
4. **Organizational governance.** No reviewers, no approvers, no compliance check, no SBOM, no provenance, no audit trail. The benchmark is single-agent against tests; the four architectures all assume a governance surface.
5. **Multi-PR coordination.** Real engineering involves coordinated changes across PRs, branches, services, and teams. SWE-bench is per-PR.
6. **Cost.** The benchmark reports pass@1 but does not constrain tokens, time, or dollars. (mini-SWE-agent's value proposition — "scores >74% in 100 lines of Python" — is partly a cost-and-simplicity argument the benchmark itself does not surface.)
7. **Maintenance.** SWE-bench measures whether the patch makes the tests pass *once*, not whether the code is maintainable, whether it introduces subtle bugs, or whether it will break the next PR. There is no Brian Will / Hamel Husain "this is your evals problem" feedback loop.

The Princeton blog and the original SWE-bench paper are honest about (1)-(4); the field has been less honest about (5)-(7). For our architectures, every gap above is a *design surface* the architecture has to fill.

## 5. SWE-agent (S6, S7) — the ACI insight and the 12.5% → 74%+ trajectory

SWE-agent's contribution is a concept and an existence proof. The concept is the **agent-computer interface (ACI)**: a deliberately designed surface between a language model and the operating environment, optimized for the model's strengths and weaknesses. The existence proof is that, holding the underlying LM fixed, redesigning the interface raised SWE-bench pass@1 from ~4-5% to **12.5%** (S6, NeurIPS 2024). Per the abstract: "SWE-agent achieved a pass@1 rate of 12.5% on SWE-bench and 87.7% on HumanEvalFix, far exceeding the previous state-of-the-art achieved with non-interactive LMs."

**The ACI design principles (S6 §3, reconstructed from search excerpts pending full-text capture).**

- **Simplicity.** "Actions should be simple and easy to understand, with simple commands having a few options and concise documentation that are easier for agents to use." The corollary: prefer a small command vocabulary with well-shaped arguments to a large one with many options.
- **Efficiency.** "Actions should be efficient, with important operations (e.g., file navigation, editing) consolidated into as few actions as possible to help agents make meaningful progress towards a goal in a single step." The corollary: each tool call should make non-trivial forward progress; avoid death-by-paper-cut.

**The original SWE-agent commands.** From the project README and the ACI background page (linked from S7; latter 403 from sandbox, content inferred): a small set of commands — `open <path>`, `goto <line>`, `scroll_up`/`scroll_down`, `find_file`, `search_dir`, `edit <range> ... end_of_edit`, `submit` — each with carefully shaped feedback that fits in a small viewport. The ACI is *interface design*, not tool count.

**The trajectory (dated benchmark numbers).**

- **2024-05** (SWE-agent paper, S6): **12.5% pass@1** on SWE-bench (original), with GPT-4 Turbo as the underlying LM.
- **2025-08** (mini-SWE-agent first public release, per the Hacker News thread linked from the README): **65%** on SWE-bench Verified, in approximately 100 lines of Python with bash as the only tool. The S7 SWE-agent docs preserve this number.
- **2026 (early)** (mini-SWE-agent README, fetched 2026-05-11): **>74%** on SWE-bench Verified, with Gemini 3 Pro as the underlying LM. The README also lists adopters including "Meta, NVIDIA, Essential AI, IBM, Nebius, Anyscale, Princeton University, Stanford University, and many more."

**The mini-SWE-agent twist on the ACI argument.** The original SWE-agent paper argued that carefully-designed tools beat raw shell access. The mini-SWE-agent argues — and the benchmark numbers back it — that for modern models the *bash shell itself* is now an adequate ACI, provided the harness gives the model a clean linear conversation history and a single-tool surface. From the mini-SWE-agent README (verbatim): "Does not have any tools other than bash"; "Just some 100 lines of python for the agent class"; uses `subprocess.run` for "independent action execution rather than maintaining stateful shell sessions"; "completely linear history."

This is a striking refinement of the ACI thesis. The 2024 paper said *"interface design matters more than tool count."* The 2026 mini-SWE-agent says *"as the model improves, even bash counts as a good interface — what matters is the harness's discipline (linear history, no hidden state, no MCP, no plugins)."* For our architectures, this is the strongest empirical evidence that the **harness, not the tool surface, is the leverage point** — directly aligned with our Round-1 substrate-audit findings on OpenHands and Codex CLI.

**What SWE-agent contributes to our architectures.**

- *The ACI is the unit of design.* Every architecture in `architectures/` has an implicit ACI for each agent role. Naming it explicitly, per SWE-agent, is one of the most leveraged moves an architect can make.
- *Simple beats complex when the model is strong.* mini-SWE-agent argues for a minimum-viable ACI. The Lighthouse architecture (one human + small fleet) is mini-SWE-agent's natural home.
- *Linear history is load-bearing.* mini-SWE-agent's "completely linear history" is the same property that OpenHands' V1 SDK enforces via event-sourcing (`research/11-openhands-substrate-audit.md` §4.2) — and that the Anthropic harness blog endorses for long-running agents.
- *Bash + tests is enough for many tasks.* This is the academic vindication of Simon Willison's "First run the tests" + AGENTS.md + `python -c` substrate (`research/05-simon-willison.md` §"Agentic manual testing"). The factory does not need a bespoke tool surface for everything.

## 6. Where each contributes to the foundations of our four architectures

A compact mapping (referenced against `architectures/00-comparison.md` and the spec-driven baseline):

| Paper | Atelier (panel) | Foundry (phase-gated) | Lighthouse (one + fleet) | Mill (dark factory) |
|---|---|---|---|---|
| AlphaCode (S4) | Cluster-by-behavior as the *reviewer-panel-as-consensus* primitive. | Filter-by-example-tests as the *cheap-gate-first* phase. | — | Generate-many-then-verify as the throughput primitive; cluster representatives as the shipped batch. |
| CodeGen (multi-turn) | Multi-turn factorization as the academic license for role separation across reviewers. | Multi-turn factorization as the academic license for phase decomposition; MTPB as the academic spec-as-conversation precedent. | Multi-turn synthesis with one driver and a tool loop. | — |
| SWE-bench (S5) | The evaluation criterion the panel ultimately reports to. | Fail-to-Pass tests as the canonical phase-gate. | Single pass@1 as the leverage metric. | The benchmark the satisfaction score must beat or replace. |
| SWE-agent (S6, S7) | The ACI for each reviewer role. | The ACI for each phase actor. | The minimum-viable ACI (mini-SWE-agent) for the single driver. | The ACI for the many small workers. |

## 7. What the benchmarks measure that our architectures need

These academic foundations give our architectures real, transferable things:

1. **A falsifiable acceptance criterion.** SWE-bench's Fail-to-Pass tests are the canonical "did the change work" signal. Every architecture in `architectures/` needs an equivalent — and SWE-bench shows the criterion can be machine-checked end-to-end against a real repo, not just a toy.
2. **A scale precedent for orchestration.** AlphaCode showed that pipelining model output through cheap filters, then expensive ones, then a clustering / consensus step, beats trying to extract one perfect answer. Every multi-agent architecture in `architectures/` rests on this orchestration substrate.
3. **A spec-decomposition precedent.** CodeGen's MTPB result — multi-turn beats single-turn on the same total intent — gives the architectures empirical license to insist on phase / role / spec decomposition rather than treating the spec as a monolithic prompt.
4. **An ACI design discipline.** SWE-agent named the unit and gave principles. mini-SWE-agent showed that the principles compose with stronger models into a 100-line agent that beats much fancier predecessors. Every per-role agent surface in `architectures/` should be designed as an explicit ACI.
5. **A learning curve.** The 12.5% → 65% → 74%+ trajectory in roughly two years is itself a piece of architectural data: with a fixed benchmark, fixed task definition, and a stable evaluation harness, real progress is observable. The architectures should each report a benchmark number, with a date, that future revisions can compare against.

## 8. What the benchmarks do NOT measure that our architectures cover

This is the more important list. The four architectures all need to handle work that the academic benchmarks above explicitly do not score:

1. **Spec refinement and ambiguity.** SWE-bench treats the issue text as ground truth. Our `spec-driven-ai-dev.md` baseline treats the spec as a work product. The Foundry's phase-zero spec gate, the Atelier's reviewer-panel feedback on spec-vs-implementation drift, the Lighthouse's "send out a scout" exploratory loop, and the Mill's scenario / satisfaction methodology are all spec-refinement mechanisms that have no counterpart in the academic benchmarks. (Cross-reference: `research/05-simon-willison.md` §"Specification methodology"; the StrongDM "scenarios as holdout set" pattern.)
2. **Test authoring under model uncertainty.** SWE-bench provides the tests. In real practice the agent (or the human) must *write* the tests, and Simon Willison's "how can you prove software works when both implementation and tests come from the agent?" is the load-bearing question. The architectures answer it with (a) red/green TDD discipline, (b) scenario-based holdout sets, (c) Showboat-style trajectory artifacts as a second-pass review surface, (d) human review at the spec/scenario layer rather than the code layer. None of this is benchmarked.
3. **Deployment safety and rollback.** No benchmark in this set models deployment, canary, observability, or rollback. The architectures must bring these in via the substrate layer (CI/CD, feature flags, SLOs). This is where `research/11-openhands-substrate-audit.md`'s headless-mode JSONL contract becomes load-bearing — observable agent trajectories are a deployment-safety prerequisite that the academic literature does not require.
4. **Organizational governance and provenance.** No benchmark requires SBOMs, attestations, code-owners review, or audit trails. The architectures must integrate SPDX (S21), SLSA (S25), and review-policy substrate. The El Kaim Council and BCG Platinion governance threads (Round-3 §11.10) are entirely outside the academic frame.
5. **Multi-PR / multi-service coordination.** Real software changes cross PRs, services, and teams. SWE-bench is single-PR. The architectures must define how multi-PR work is decomposed, coordinated, and rolled back as a unit. (The Anthropic C-compiler case study — `research/external-syntheses` S14 — is the closest practitioner analogue.)
6. **Cost, latency, and human attention budgets.** SWE-bench reports pass@1 but not tokens or dollars. mini-SWE-agent's "100 lines, >74%" is partly a cost argument the benchmark does not score. The StrongDM "$1,000/day per engineer" floor (`research/05-simon-willison.md` §"Wait, $1,000/day per engineer?") is *the* practitioner constraint that academic work elides. Each architecture must answer it.
7. **Long-running maintenance and cognitive debt.** SWE-bench measures one-shot resolution. The architectures must answer Simon Willison's cognitive-debt critique — the system that the team ships must remain *understandable* over time. Linear walkthroughs, interactive explanations, and StrongDM Pyramid Summaries are the practitioner answers; no academic benchmark scores them.
8. **The "looking-the-part" hazard.** Simon Willison's May 6 2026 observation — that an LLM-built repo with comprehensive tests and a beautiful README no longer proves care — has no academic counterpart. The architectures must surface *usage signals*, not just test coverage and PR-description quality, as part of quality measurement.
9. **Trust drift / normalization of deviance.** Each successful unmonitored run raises the threshold for human attention. No benchmark scores this; every architecture must instrument it.

## 9. Cross-references to existing reports

- **`research/05-simon-willison.md`** — Simon Willison treats SWE-bench and the AlphaCode pipeline as implicit substrate but does not cite them; this report makes the substrate explicit. Simon's red/green TDD and "First run the tests" patterns are the practitioner-grade versions of SWE-bench's Fail-to-Pass criterion. His parallel-coding-agents post is the practitioner-grade version of AlphaCode's sample-many-then-cluster pipeline.
- **`research/11-openhands-substrate-audit.md`** — OpenHands' V1 SDK design principles (sandboxing opt-in; event-sourced linear history; LLM-centric tool interfaces) are direct lineal descendants of SWE-agent's ACI principles. The OpenHands paper's §4.4 "tool system" is the engineering-grade version of SWE-agent §3.
- **§11.7 evals deep-dive** — `research/followup/07-evals-deepdive.md` is referenced in the brief but not yet merged on this branch as of 2026-05-11 (the followup directory contains no `07-evals-deepdive.md`). When merged, the natural cross-reference is from this report's §8(2) (test authoring under model uncertainty) and §8(7) (long-running maintenance) into the evals thread.
- **`research/external-syntheses/chatgpt-deep-research-2026-05-11/sources.md`** §"Weak or missing citations" — flagged CodeGen, LangGraph, OpenHands, and Simon Willison as named-but-uncited in the original report. This report adopts arXiv 2203.13474 as the canonical CodeGen citation.

## 10. Open follow-ups

1. **Full-text capture of the four primary papers.** Filed as fetch issue #28. Once arXiv, swebench.com, swe-agent.com, deepmind.google, openai.com, and pli.princeton.edu content is captured, sections 2-5 of this report can be upgraded from excerpt-anchored to primary-text-anchored.
2. **Cross-reference with the merged evals deep-dive** when it lands on main.
3. **Track the SWE-bench Verified leaderboard delta.** Today's >74% mini-SWE-agent number is the snapshot as of 2026-05-11; the next Round-N pass should re-date it.
4. **Open question:** does the AlphaCode cluster-by-behavior primitive translate to repository-scale tasks (where "behavior" is fuzzier than competitive-programming I/O)? StrongDM's "satisfaction" score is one operationalization; the academic literature does not yet have a clean answer.
5. **Open question:** is there a benchmark on the horizon that closes the spec-refinement gap (§8.1)? MTPB partially closes it but is small (115 problems) and synthetic. A "real-issue-real-spec-refinement" benchmark would be a major contribution.

---

**Word count (approximate):** ~3,000 words.

**Sources status summary:**
- ✅ direct full read: mini-SWE-agent README (`github.com/SWE-agent/mini-swe-agent`), Salesforce CodeGen README.
- 🟡 reconstructed from search-engine excerpts and abstracts: AlphaCode (S4), SWE-bench paper (S5), SWE-agent paper (S6), SWE-agent project docs (S7), CodeGen paper.
- ⏳ filed for fetch (issue #28): the 20+ URLs across arxiv.org, swebench.com, swe-agent.com, deepmind.google, openai.com, pli.princeton.edu, openreview.net, huggingface.co, semanticscholar.org.
