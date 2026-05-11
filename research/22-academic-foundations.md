# Research Report 22 — Academic Foundations: AlphaCode, SWE-bench, SWE-agent, CodeGen

**Date:** 2026-05-11
**Author:** Round-5 Cluster 13.1.5 subagent (fanout run 20260511-054258, sub-24); upgraded to primary-text-anchored on 2026-05-11 by drain sub-29
**Scope:** Read S4 (AlphaCode), S5 (SWE-bench), S6 (SWE-agent paper), S7 (SWE-agent project docs) plus a primary CodeGen reference. Extract the academic foundations underneath the four agentic-coding architectures in `architectures/`. Compare against `research/05-simon-willison.md`, `research/11-openhands-substrate-audit.md`, and (the §11.7 evals deep-dive — not yet merged on this branch; cross-reference deferred).

## Drain note (issue #28) — 2026-05-11 primary-source upgrade

This report was originally written from WebSearch excerpts + GitHub READMEs because all arXiv / SWE-bench / DeepMind / OpenAI / OpenReview URLs returned 403 from the sandbox at first read. The GitHub-Action fetcher (issue #28) successfully retrieved the primary HTML for those URLs and rendered Markdown into `research/fetched/issue-28/`. This drain (sub-29) replaced excerpt-anchored claims with verbatim primary-source quotes and dated project-page numbers. Material claim-level changes:

- **AlphaCode pipeline:** locked down with verbatim §4 quotes from the ar5iv-rendered full paper (arXiv:2203.07814v1) — pre-train → fine-tune → large-scale sample → filter-by-example-tests → cluster — including the "approximately 99% of model samples" filter rate and "millions of samples per problem" upper bound (was loosely paraphrased before).
- **AlphaCode CodeContests result:** added the paper's CodeContests validation-set number ("With up to a million samples per problem, we can solve 34.2% of problems") that the WebSearch excerpts had not surfaced; the 54.3% top-half number is now properly contextualised against the in-paper development metric.
- **AlphaCode test-input generator:** added the previously-missing detail that AlphaCode trained a *separate* model to generate test inputs for the clustering step (§4.6).
- **CodeGen MTPB:** locked the "**115 diverse problem sets**" and "the same intent provided to CODEGEN in multi-turn fashion **significantly improves program synthesis** over that provided as a single turn" wording from the arXiv:2203.13474v5 abstract verbatim; added the ICLR 2023 "notable top 25%" venue acceptance status (from OpenReview).
- **SWE-bench original baseline refuted/replaced:** the prior report said "single digits", "around 4-5% pass@1". The arXiv:2310.06770v3 abstract specifies **"Claude 2, is able to solve a mere 1.96% of the issues"** — the original RAG baseline. The swebench.com homepage corroborates "initial Retrieval Augmented Generation (RAG) baseline scored just 1.96%". The 4-5% figure was incorrect; this is now corrected to 1.96% (Claude 2, RAG baseline).
- **SWE-agent original number:** the swebench.com home page states "SWE-agent, was the first agent-based AI system ever introduced for performing software engineering tasks, achieving a score of **12.47%** on SWE-bench". The paper's abstract reports "**12.5%**" pass@1 (the same number to one less significant figure). Both are now cited verbatim.
- **mini-SWE-agent 65% number:** dated to **July 24, 2025** per swe-agent.com/latest news entry ("Mini-SWE-Agent achieves 65% on SWE-bench verified in 100 lines of python!"); the swebench.com news entry dates the same announcement to **07/2025** ("mini-SWE-agent scores 65% on SWE-bench Verified in 100 lines of python code").
- **SWE-bench Verified scope:** confirmed at **500 instances** "human-filtered subset", created "in collaboration with OpenAI" (swebench.com/verified — retrieval 2026-05-11). Verified leaderboard runs all LMs through mini-SWE-agent for apples-to-apples model comparison.
- **ACI design (SWE-agent):** the swe-agent.com/latest/background/aci/ doc enumerates four verbatim engineered features (linter on edit, special-built file viewer at 100 lines per turn, full-directory search command, "Your command ran successfully and did not produce any output" empty-output message) — replacing the prior Simplicity / Efficiency principle paraphrases that came from second-hand summaries.
- **DeepMind blog:** confirmed pipeline language verbatim ("create a massive amount of C++ and Python programs for each problem... Then we filter, cluster, and rerank those solutions to a small set of 10 candidate programs") from deepmind.google/discover/blog/competitive-programming-with-alphacode (2022-12-08 republication of 2022-02-02 original).
- **Sources status table:** flipped ✅ for AlphaCode (ar5iv full text + DeepMind blog), CodeGen (arXiv abstract + OpenReview), SWE-bench (arXiv abstract + swebench.com project pages), SWE-agent (arXiv abstract + OpenReview + swe-agent.com docs).

OpenAI's "Introducing SWE-bench Verified" blog and Princeton's PLI blog were behind Cloudflare challenges in the fetcher capture (HTML-only, no text body); the swebench.com/verified primary project page is used in their place. The arXiv-HTML renders of v3 SWE-bench, v3 SWE-agent, and v5 CodeGen returned only nav-chrome (no body); the ar5iv mirror provided AlphaCode's full body.

## Sources reviewed

Status legend: ✅ full primary text read · 🟡 abstract / project-page only · ❌ unobtainable.

| Source ID | Citation | URL | Status | Notes |
|---|---|---|---|---|
| S4 | Li et al. *Competition-Level Code Generation with AlphaCode* (arXiv:2203.07814v1, 8 Feb 2022; Science 8 Dec 2022) | https://arxiv.org/abs/2203.07814 | ✅ | Full body via ar5iv mirror (`ar5iv.labs.arxiv.org/html/2203.07814`). 74-page paper. Abstract + §4 pipeline (sampling/filtering/clustering) + §5 results read verbatim. DOI: 10.1126/science.abq1158. |
| — | DeepMind blog *Competitive programming with AlphaCode* (2022-02-02, republished 2022-12-08) | https://deepmind.google/discover/blog/competitive-programming-with-alphacode | ✅ | Full post body fetched. |
| S5 | Jimenez et al. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* (arXiv:2310.06770v3, last revised 11 Nov 2024; ICLR 2024) | https://arxiv.org/abs/2310.06770 | ✅ (abstract) / 🟡 (full body) | Abstract page fetched. arXiv-HTML v3 render returned only nav-chrome (no body). OpenReview record at https://openreview.net/forum?id=VTF8yNQM66. |
| — | SWE-bench project site (`swebench.com`, including `/`, `/verified.html`, `/lite.html`, `/original.html`) | https://www.swebench.com/ | ✅ | All four pages fetched 2026-05-11. Provide canonical dataset scope (2,294 Full · 500 Verified · 300 Lite · 517 Multimodal), current news entries, and citation. |
| S6 | Yang et al. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering* (arXiv:2405.15793v3, last revised 11 Nov 2024; NeurIPS 2024 poster) | https://arxiv.org/abs/2405.15793 | ✅ (abstract + OpenReview) / 🟡 (full body) | Abstract + OpenReview record (forum_id=mXpq6ut8J3) fetched. arXiv-HTML v3 render is nav-chrome only. |
| S7 | SWE-agent docs (`swe-agent.com/latest/`, `/latest/background/aci/`) | https://swe-agent.com/latest/ | ✅ | Both pages fetched 2026-05-11. ACI doc lists four engineered features verbatim. Project banner now reads: "📣 We now recommend mini-swe-agent instead of SWE-agent: Same performance, much more simple & flexible". |
| — (CodeGen) | Nijkamp et al. *CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis* (arXiv:2203.13474v5, last revised 27 Feb 2023; ICLR 2023 notable top 25%) | https://arxiv.org/abs/2203.13474 | ✅ (abstract + OpenReview) | Abstract + OpenReview record (forum_id=iaYcJKpY2B_) fetched. arXiv-HTML v5 render is nav-chrome only. |
| — | OpenAI *Introducing SWE-bench Verified* (Aug 13, 2024 announcement) | https://openai.com/index/introducing-swe-bench-verified/ | ❌ | Fetched HTML is a Cloudflare challenge — no body. Project description from swebench.com/verified used instead. |
| — | Princeton PLI blog *SWE-bench: Can Language Models...* | https://pli.princeton.edu/blog/2023/swe-bench-... | ❌ | Fetched HTML is Cloudflare challenge — no body. swebench.com used instead. |

**Date stamp on all benchmark numbers:** unless otherwise noted, every benchmark number in this report is the snapshot as of 2026-05-11. Benchmark numbers are time-sensitive; the SWE-bench leaderboard moves week-over-week.

---

## 1. Why these four, why now

The Round-5 plan (§13.1.5) flags an asymmetry in our corpus: most of what we have is *practitioner* material — StrongDM, Simon Willison, Every.to, El Kaim, the Anthropic/OpenAI/GitHub product blogs — and the academic substrate that those practitioners build on is referenced indirectly but never collated. The four papers in scope are the substrate, in roughly chronological order:

1. **AlphaCode (Li et al., arXiv:2203.07814v1, 2022; Science, 2022 — S4).** The first end-to-end demonstration that *generate-many-then-verify* could solve nontrivial code tasks at a competitive level. Per the paper's abstract, "three key components were critical: (1) an extensive and clean competitive programming dataset for training and evaluation, (2) large and efficient-to-sample transformer-based architectures, and (3) large-scale model sampling to explore the search space, followed by filtering based on program behavior to a small set of submissions." Top 54.3% on Codeforces (top half of human competitors) was the headline.
2. **CodeGen (Nijkamp et al., arXiv:2203.13474v5, 2022–2023; ICLR 2023 notable top 25%).** The first open-source 16.1B-parameter family for code, and (critically for our purposes) the introduction of the **Multi-Turn Programming Benchmark (MTPB)** — 115 problem sets factorized into multi-turn prompts — with the finding that "the same intent provided to CODEGEN in multi-turn fashion significantly improves program synthesis over that provided as a single turn" (abstract, verbatim). This is the academic version of the modern "spec → plan → implement → test" loop.
3. **SWE-bench (Jimenez et al., arXiv:2310.06770v3, ICLR 2024 — S5).** The first benchmark that grounded "can language models do software engineering" in *real GitHub issues from real Python repos*. **2,294 task instances drawn from 12 popular Python repositories**, each task with a Fail-to-Pass test set as the ground truth. The original RAG baseline was 1.96% (Claude 2).
4. **SWE-agent (Yang et al., arXiv:2405.15793v3, NeurIPS 2024 poster — S6).** The "12.5% pass@1 on SWE-bench" paper, and more importantly the paper that named and operationalized the **agent-computer interface (ACI)**: "specially built interfaces" for LM agents as a "new category of end users with their own needs and abilities" (abstract, verbatim). The trajectory since — 12.5% (May 2024) → 65% mini-SWE-agent (July 2025) → >74% (early 2026, per S7 / mini-SWE-agent README) — is the closest thing the field has to a public "factory yield" learning curve.

These four together describe the academic ancestry of every architecture in `architectures/`:

- The **Atelier** (multi-reviewer panel) ancestry is AlphaCode's sample-and-cluster — sample diverse candidates, score them, select.
- The **Foundry** (phase-gated pipeline) ancestry is SWE-bench's Fail-to-Pass evaluation criterion plus CodeGen's multi-turn factorization — both are "the spec is a list of acceptance gates."
- The **Lighthouse** (one human + small fleet) ancestry is SWE-agent's ACI insight — a single LM driving a careful tool surface can outperform far more complex setups.
- The **Mill** (high-throughput dark factory) ancestry is the AlphaCode pipeline scaled up: generate a fleet of candidates, filter by held-out scenarios, cluster, ship the cluster representative. StrongDM's "satisfaction scoring" is the modern descendant.

## 2. AlphaCode (S4) — orchestration-and-verification, before "agents" were a word

AlphaCode is best read today as the first **orchestrated** code-generation system, not as a language-model paper. The model is a transformer (up to 41.1B parameters in the published numbers — see Table 3 of the paper), but the load-bearing engineering is the pipeline around the model. Per §4 of arXiv:2203.07814v1 (verbatim) the approach is a four-step process:

> "1. Pre-train a transformer-based language model on GitHub code with standard language modelling objectives. This model can reasonably represent the space of human coding, which greatly reduces the problem search space.
>
> 2. Fine-tune the model on our dataset of competitive programming data, using GOLD (Pang and He, 2020) with tempering (Dabre and Fujita, 2020) as the training objective. This further reduces the search space, and compensates for the small amount of competitive programming data by leveraging pre-training.
>
> 3. Generate a very large number of samples from our models for each problem.
>
> 4. Filter the samples to obtain a small set of candidate submissions (at most 10), to be evaluated on the hidden test cases, by using the example tests and clustering to pick samples based on program behaviour."

Per §4 (concluding sentence of the four-step list): "the large-scale sampling followed by filtering is unique to our setup, and we found that this process greatly improves problem solve rate."

**Large-scale sampling (§4.4 verbatim).** "Sampling from transformer models can be easily parallelized, which allowed us to scale to **millions of samples per problem** – a critical driving force for performance improvement." To diversify the sample pool, the model (i) generates half-Python half-C++, (ii) randomises problem tags and difficulty ratings, and (iii) uses a relatively high sampling temperature.

**Filtering by example tests (§4.5 verbatim).** "One powerful tool for selecting these submissions is filtering samples to only those that pass the example tests given in the problem statement. **Filtering removes approximately 99% of model samples**, although the exact amount depends on the problem and model, and filtering can still leave tens of thousands of candidate samples for many problems."

**Clustering by program behaviour (§4.6).** Verbatim: "Filtering using example tests can still leave thousands of candidate programs per problem. Randomly picking from this pool wastes the limited submission budget on programs that are syntactically different but semantically equivalent. Semantically equivalent programs could be detected if we had additional test inputs, by executing all remaining programs on these inputs and grouping programs that produce the same outputs together into clusters." The paper notes a subtle but load-bearing engineering decision: AlphaCode "trained a separate test input generation model, using the same architecture as our main models, and initialised from the same GitHub pre-trained checkpoint" — the test inputs used to cluster are themselves model-generated. After clustering: "selecting one solution from each cluster from largest to smallest performed best, perhaps because there are many ways solutions can be incorrect while correct solutions tend to behave the same and therefore are grouped into larger clusters."

**The headline results (S4, dated 2022-02-08 arXiv v1).**

- *Codeforces simulated evaluation.* Abstract: "AlphaCode achieved on average a ranking of top **54.3%** in competitions with more than 5,000 participants." §1 elaborates: estimated Codeforces rating 1238, "within the top 28% of users who have participated in a contest in the last 6 months."
- *CodeContests validation set (the in-paper development metric, §5).* Verbatim: "With up to a **million samples per problem, we can solve 34.2% of problems** in our validation set; and with one hundred thousand samples, we solve 31.8% of problems in our validation set, and 29.6% of problems in our test set."

The "three key components" claim is verbatim from the abstract: "(1) an extensive and clean competitive programming dataset for training and evaluation, (2) large and efficient-to-sample transformer-based architectures, and (3) large-scale model sampling to explore the search space, followed by filtering based on program behavior to a small set of submissions."

**The DeepMind blog (2022-02-02 / republished 2022-12-08, verbatim).** "We pre-train our model on selected public GitHub code and fine-tune it on our relatively small competitive programming dataset. At evaluation time, we create a massive amount of C++ and Python programs for each problem, orders of magnitude larger than previous work. Then we filter, cluster, and rerank those solutions to a small set of 10 candidate programs that we submit for external assessment. This automated system replaces competitors' trial-and-error process of debugging, compiling, passing tests, and eventually submitting." The blog also dates the milestone: "AlphaCode placed at about the level of the median competitor, marking the first time an AI code generation system has reached a competitive level of performance in programming competitions."

**What this contributes to our architectures.** AlphaCode is the prototype of the **generate-then-verify** loop. Three observations transfer directly:

- *Diversity over fidelity at the sampling stage.* Per §4.4: half-Python, half-C++, randomised tags/ratings, high temperature. The model is trained to produce many plausible candidates, not one polished one. This is the academic predecessor of StrongDM's "code is cheap, fire off the prompt anyway" — and of Simon Willison's "parallel coding agents" pattern (`research/05-simon-willison.md`, Oct 5 2025 post).
- *Example tests as the cheap filter, removing 99% of samples (§4.5 verbatim).* The first sieve is the cheap one. This anticipates Simon's "first run the tests" pattern and the Foundry architecture's static-gate phase.
- *Cluster-by-behavior as the consensus filter (§4.6).* This is the academic version of "let the satisfaction score break ties" — a probabilistic, trajectory-aware quality bar rather than a single boolean. Critically, AlphaCode's clustering needs a *separate model-generated test-input generator* (§4.6): the consensus filter is itself a learned artifact, not a hand-written one. StrongDM's scenario/satisfaction methodology (`research/05-simon-willison.md` §"The software factory post") is the practitioner descendant.

**What AlphaCode does *not* model.** It assumes a stateless single-shot problem (competitive programming), not a multi-turn engineering task. There is no spec refinement, no test authoring (tests are given), no deployment, no review, no organizational context. It is a beautiful demonstration of orchestration-and-verification at the *algorithm* scale, but the unit of work is one self-contained problem, not a real-world change to a 100k-line repo.

## 3. CodeGen (Nijkamp et al., arXiv:2203.13474v5; ICLR 2023 notable top 25%) — multi-turn synthesis as the academic frame

CodeGen was first submitted to arXiv on 25 March 2022 (v1) with v5 finalized 27 February 2023 — the version associated with the ICLR 2023 publication. Per the OpenReview record (forum_id=iaYcJKpY2B_), CodeGen was accepted as **ICLR 2023 notable top 25%**. The CodeGen family (350M, 1B, 3B, 7B, **16.1B** parameters; CodeGen1 and CodeGen2 variants) was trained on a mix of natural language and code, and released alongside the **JAXFORMER** training library.

**The abstract (verbatim, in two load-bearing halves).** Half one — the open release: "we train and release a family of large language models up to **16.1B parameters**, called CODEGEN, on natural language and programming language data, and open source the training library JAXFORMER. We show the utility of the trained model by demonstrating that it is competitive with the previous state-of-the-art on zero-shot Python code generation on HumanEval."

Half two — the multi-turn contribution: "We further investigate the multi-step paradigm for program synthesis, where a single program is factorized into multiple prompts specifying subproblems. To this end, we construct an open benchmark, **Multi-Turn Programming Benchmark (MTPB), consisting of 115 diverse problem sets that are factorized into multi-turn prompts**. Our analysis on MTPB shows that **the same intent provided to CODEGEN in multi-turn fashion significantly improves program synthesis over that provided as a single turn**."

In other words: if you give the model *the same total instruction* in pieces, it produces better code than if you give it all at once. This is the academic precedent for nearly every modern coding-agent practice that decomposes work — plan-mode in Codex, the planner / coder / reviewer split in compound engineering, the spec-then-test-then-implement loop in Simon Willison's red/green TDD chapter, the SWE-agent ACI's separation of *navigate*, *view*, *edit*, *test*. It is also the academic ancestor of the **`AGENTS.md` + tests + scenarios** layered spec that `research/05-simon-willison.md` §"Specification methodology" describes.

The OpenReview TL;DR (verbatim) compresses it: "We open-source a large language models, CodeGen, for program synthesis and propose a multi-turn program synthesis benchmark for evaluation."

**What this contributes to our architectures.** Three transfers:

- *Decomposition is empirically free yield.* The MTPB finding is not "decomposition is sometimes useful"; it is "decomposition **significantly improves** synthesis on the same total intent" (abstract emphasis added). This is the academic license for the Foundry's phase gates and the Atelier's reviewer-panel.
- *The benchmark format itself.* MTPB is a *spec-as-conversation* benchmark — each of 115 problems is a sequence of natural-language sub-specifications. This is the closest published analogue to what StrongDM's Attractor repo *is* — three markdown files that together specify the system (per `research/05-simon-willison.md`).
- *Open-source baseline.* CodeGen also matters as the first credibly-open large code model. Every "open-source agent harness" thread in our corpus (OpenHands, mini-SWE-agent, the StrongDM cxdb release) rests on the existence of credible open code models.

**Status caveat on CodeGen citation.** The Round-5 sources audit (`research/external-syntheses/chatgpt-deep-research-2026-05-11/sources.md` §"Weak or missing citations") flagged CodeGen as one of the named-but-uncited references in the original report. This report adopts arXiv:2203.13474v5 as the canonical primary citation; the OpenReview record at https://openreview.net/forum?id=iaYcJKpY2B_ confirms the ICLR 2023 venue and review status.

## 4. SWE-bench (S5) — realistic-issue benchmarking, and its blind spots

SWE-bench is the benchmark that finally made "can the model do my job" a falsifiable question.

**The dataset (S5, abstract verbatim).** "an evaluation framework consisting of **2,294 software engineering problems** drawn from real GitHub issues and corresponding pull requests across **12 popular Python repositories**." The swebench.com home page elaborates: "Each instance is based on a pull request that (1) is associated with an issue, and (2) modified 1+ testing related files. Per instance, we construct an execution environment (Docker Image) with the repository successfully installed at the commit that the Pull Request is based on. Without the Pull Request's changes, a number of test(s) fail. After the Pull Request is merged, the same set of test(s) pass. These 'Fail-to-Pass' tests are the primary signal for evaluation."

**The evaluation criterion (swebench.com homepage, verbatim).** "SWE-bench evaluation works as follows. Per task instance, an AI system is given the issue text. The AI system should then modify the codebase in order to resolve the described issues. When the AI system is finished, we run the aforementioned Fail-to-Pass tests to check if the issue was successfully resolved."

**The original baseline (October 2023 paper publication).** Per arXiv:2310.06770v3 abstract (verbatim): "Our evaluations show that both state-of-the-art proprietary models and our fine-tuned model SWE-Llama can resolve only the simplest issues. **The best-performing model, Claude 2, is able to solve a mere 1.96% of the issues.**" The swebench.com homepage confirms: "SWE-bench was released in October 2023, where our initial Retrieval Augmented Generation (RAG) baseline scored just 1.96%." (This refutes the prior report's "around 4-5% pass@1" claim — see Drain note.)

**Variants (as of 2026-05-11, from swebench.com).**

- **SWE-bench Full** — the original 2,294-instance benchmark. (Quote: "Each entry reports the **% Resolved** metric, the percentage of instances solved (out of 2294 Full, 500 Verified, 300 Lite & Multilingual, 517 Multimodal).")
- **SWE-bench Lite** — 300 test instances + 23 development instances. Per swebench.com/lite: "selected to preserve the distribution and difficulty spectrum of the original benchmark while focusing on more self-contained, functional bug fixes." Lite covers "11 of the original 12 repositories." Selection rules include "Removed instances that edit more than 1 file" and "Removed instances where the gold patch has more than 3 edit hunks."
- **SWE-bench Verified** — per swebench.com/verified: "**A human-validated subset of 500 SWE-bench instances** for reliable evaluation of coding agents and language models. … Human annotators reviewed each instance to ensure the problem descriptions are clear, the test patches are correct, and the tasks are solvable given the available information." Released in collaboration with OpenAI in August 2024 ("[08/2024] SWE-bench x OpenAI = SWE-bench Verified" per swebench.com home news entry).
- **SWE-bench Multilingual** — 300 tasks across 9 programming languages.
- **SWE-bench Multimodal** — 517 instances with visual elements.

**The "bash-only" comparison rail (swebench.com/verified verbatim).** "While the full leaderboard compares arbitrary systems, we are also interested in evaluating language models directly. To make an apples-to-apples comparison of LMs easier, we evaluate all LMs using mini-SWE-agent in a minimal bash environment. No tools, no special scaffold structure; just a simple ReAct agent loop. These results represent the state-of-the-art LM performance when given just a bash shell and a problem."

**The trajectory (dated benchmark numbers as of 2026-05-11).** The newsfeed on swebench.com (verbatim):

- **[03/2024] Check out SWE-agent (12.47% on SWE-bench)** — the original SWE-agent score on SWE-bench Full.
- **[07/2025] mini-SWE-agent scores 65% on SWE-bench Verified in 100 lines of python code.** (Dated July 24, 2025 per the swe-agent.com/latest news entry.)
- **[11/2025] Introducing CodeClash, our new eval of LMs as goal (not task) oriented developers!**

The mini-SWE-agent project README (fetched directly from GitHub on 2026-05-11) advertises ">74% on SWE-bench Verified" with Gemini 3 Pro on a 100-line bash-only harness. This >74% figure is the current snapshot as of 2026-05-11 (the swebench.com leaderboard moves week-over-week; treat as date-stamped).

**What SWE-bench measures.**

- *Code reading at scale.* The repo is real; the agent has to navigate it. Per the paper abstract: "Resolving issues in SWE-bench frequently requires understanding and coordinating changes across multiple functions, classes, and even files simultaneously, calling for models to interact with execution environments, process extremely long contexts and perform complex reasoning that goes far beyond traditional code generation tasks."
- *Issue interpretation.* The issue text is real and frequently under-specified.
- *Patch generation under test pressure.* The Fail-to-Pass tests are the acceptance criterion.
- *Test setup robustness.* The benchmark's Docker images force the agent to handle a real install + test runner.

**What SWE-bench measures that our architectures need** — and what they don't — see §7 and §8 below for the full mapping.

## 5. SWE-agent (S6, S7) — the ACI insight and the 12.5% → 74%+ trajectory

SWE-agent's contribution is a concept and an existence proof. The concept is the **agent-computer interface (ACI)**: a deliberately designed surface between a language model and the operating environment. The existence proof is the SWE-bench score lift.

**The paper abstract (arXiv:2405.15793v3, verbatim).** "Just as humans benefit from powerful software applications, such as integrated development environments, for complex tasks like software engineering, we posit that LM agents represent a new category of end users with their own needs and abilities, and would benefit from specially-built interfaces to the software they use. We investigate how interface design affects the performance of language model agents. As a result of this exploration, we introduce SWE-agent: a system that facilitates LM agents to autonomously use computers to solve software engineering tasks. SWE-agent's custom agent-computer interface (ACI) significantly enhances an agent's ability to create and edit code files, navigate entire repositories, and execute tests and other programs. We evaluate SWE-agent on SWE-bench and HumanEvalFix, achieving state-of-the-art performance on both with a **pass@1 rate of 12.5% and 87.7%**, respectively, far exceeding the previous state-of-the-art achieved with non-interactive LMs."

**OpenReview TL;DR (forum_id=mXpq6ut8J3, verbatim).** "We introduce the concept of agent-computer interfaces to enhance LM agent performance on software engineering tasks."

**The ACI design (swe-agent.com/latest/background/aci/, verbatim — primary text now available).** The doc identifies four engineered features:

> "1. We add a **linter** that runs when an edit command is issued, and do not let the edit command go through if the code isn't syntactically correct.
>
> 2. We supply the agent with a **special-built file viewer**, instead of having it just `cat` files. We found that this file viewer works best when displaying just **100 lines in each turn**. The **file editor** that we built has commands for scrolling up and down and for performing a search within the file.
>
> 3. We supply the agent with a special-built full-directory string **searching command**. We found that it was important for this tool to succinctly list the matches- we simply list each file that had at least one match. Showing the model more context about each match proved to be too confusing for the model.
>
> 4. When commands have an empty output we return a message saying 'Your command ran successfully and did not produce any output.'"

The doc frames the lesson in one sentence: "Just like how typical language models requires good prompt engineering, **good ACI design leads to much better results when using agents**. As we show in the SWE-agent paper, a baseline agent without a well-tuned ACI does much worse than SWE-agent."

**The trajectory (dated benchmark numbers).**

- **2024-03 / 2024-05** (SWE-agent paper, S6): **12.5% pass@1** on SWE-bench (original) — the abstract figure. The swebench.com news entry dates the first announcement to "[03/2024] Check out SWE-agent (12.47% on SWE-bench)" — the same number to one more significant figure.
- **2025-07** (mini-SWE-agent public release): **65%** on SWE-bench Verified, in approximately 100 lines of Python with bash as the only tool. Per swe-agent.com/latest news (verbatim, dated July 24, 2025): "Mini-SWE-Agent achieves 65% on SWE-bench verified in 100 lines of python!"
- **2026-05-11** (mini-SWE-agent README, fetched 2026-05-11): **>74%** on SWE-bench Verified, with Gemini 3 Pro as the underlying LM.

**The mini-SWE-agent twist on the ACI argument.** The swe-agent.com docs now carry a project-wide banner (fetched 2026-05-11, verbatim): "📣 We now recommend mini-swe-agent instead of SWE-agent: Same performance, much more simple & flexible." Coupled with the ACI page's closing line ("SWE-agent has been superseded by **mini-swe-agent**. mini-swe-agent is simpler & more flexible while still being as performant. … SWE-agent is now in maintenance-only mode."), the project's own position is that interface complexity is not load-bearing once models are strong enough.

From the mini-SWE-agent README (verbatim): "Does not have any tools other than bash"; "Just some 100 lines of python for the agent class"; uses `subprocess.run` for "independent action execution rather than maintaining stateful shell sessions"; "completely linear history."

This is a striking refinement of the ACI thesis. The 2024 paper said *"interface design matters more than tool count."* The 2026 mini-SWE-agent says *"as the model improves, even bash counts as a good interface — what matters is the harness's discipline (linear history, no hidden state, no MCP, no plugins)."* For our architectures, this is the strongest empirical evidence that the **harness, not the tool surface, is the leverage point** — directly aligned with our Round-1 substrate-audit findings on OpenHands and Codex CLI.

**What SWE-agent contributes to our architectures.**

- *The ACI is the unit of design.* Every architecture in `architectures/` has an implicit ACI for each agent role. Naming it explicitly, per SWE-agent, is one of the most leveraged moves an architect can make.
- *Simple beats complex when the model is strong.* mini-SWE-agent argues for a minimum-viable ACI. The Lighthouse architecture (one human + small fleet) is mini-SWE-agent's natural home.
- *Linear history is load-bearing.* mini-SWE-agent's "completely linear history" is the same property that OpenHands' V1 SDK enforces via event-sourcing (`research/11-openhands-substrate-audit.md` §4.2) — and that the Anthropic harness blog endorses for long-running agents.
- *Bash + tests is enough for many tasks.* This is the academic vindication of Simon Willison's "First run the tests" + AGENTS.md + `python -c` substrate (`research/05-simon-willison.md` §"Agentic manual testing"). The factory does not need a bespoke tool surface for everything.
- *Curated micro-features matter when they do.* The 100-line file viewer, the empty-output message, the linted-edit gate (ACI doc verbatim) are the concrete primitives a Foundry phase-actor or Atelier reviewer would need to implement; they are the "shapes the model can use" the architectures must design at each role boundary.

## 6. Where each contributes to the foundations of our four architectures

A compact mapping (referenced against `architectures/00-comparison.md` and the spec-driven baseline):

| Paper | Atelier (panel) | Foundry (phase-gated) | Lighthouse (one + fleet) | Mill (dark factory) |
|---|---|---|---|---|
| AlphaCode (S4) | Cluster-by-behavior as the *reviewer-panel-as-consensus* primitive (§4.6: largest cluster first). | Filter-by-example-tests (§4.5, "removes approximately 99%") as the *cheap-gate-first* phase. | — | Generate-many-then-verify (§4.4, "millions of samples per problem") as the throughput primitive; cluster representatives as the shipped batch. |
| CodeGen (multi-turn) | Multi-turn factorization as the academic license for role separation across reviewers. | Multi-turn factorization as the academic license for phase decomposition; MTPB (115 problems) as the academic spec-as-conversation precedent. | Multi-turn synthesis with one driver and a tool loop. | — |
| SWE-bench (S5) | The evaluation criterion the panel ultimately reports to (Fail-to-Pass). | Fail-to-Pass tests as the canonical phase-gate. | Single pass@1 as the leverage metric. | The benchmark the satisfaction score must beat or replace. |
| SWE-agent (S6, S7) | The ACI for each reviewer role (lint, viewer, search, empty-output message). | The ACI for each phase actor. | The minimum-viable ACI (mini-SWE-agent: bash only, linear history) for the single driver. | The ACI for the many small workers. |

## 7. What the benchmarks measure that our architectures need

These academic foundations give our architectures real, transferable things:

1. **A falsifiable acceptance criterion.** SWE-bench's Fail-to-Pass tests are the canonical "did the change work" signal. Every architecture in `architectures/` needs an equivalent — and SWE-bench shows the criterion can be machine-checked end-to-end against a real repo, not just a toy.
2. **A scale precedent for orchestration.** AlphaCode showed that pipelining model output through cheap filters (example tests, 99% removed), then expensive ones (clustering on model-generated test inputs), beats trying to extract one perfect answer. Every multi-agent architecture in `architectures/` rests on this orchestration substrate.
3. **A spec-decomposition precedent.** CodeGen's MTPB result — multi-turn beats single-turn on the same total intent — gives the architectures empirical license to insist on phase / role / spec decomposition rather than treating the spec as a monolithic prompt.
4. **An ACI design discipline.** SWE-agent named the unit (lint-on-edit, 100-line viewer, succinct search, empty-output message). mini-SWE-agent showed that the principles compose with stronger models into a 100-line agent that beats much fancier predecessors. Every per-role agent surface in `architectures/` should be designed as an explicit ACI.
5. **A learning curve.** The 1.96% (RAG baseline, Oct 2023) → 12.47% (SWE-agent, Mar 2024) → 65% (mini-SWE-agent, Jul 2025) → >74% (mini-SWE-agent + Gemini 3 Pro, May 2026) trajectory in roughly 2.5 years is itself a piece of architectural data: with a fixed benchmark, fixed task definition, and a stable evaluation harness, real progress is observable. The architectures should each report a benchmark number, with a date, that future revisions can compare against.

## 8. What the benchmarks do NOT measure that our architectures cover

This is the more important list. The four architectures all need to handle work that the academic benchmarks above explicitly do not score:

1. **Spec refinement and ambiguity.** SWE-bench treats the issue text as ground truth. Our `spec-driven-ai-dev.md` baseline treats the spec as a work product. The Foundry's phase-zero spec gate, the Atelier's reviewer-panel feedback on spec-vs-implementation drift, the Lighthouse's "send out a scout" exploratory loop, and the Mill's scenario / satisfaction methodology are all spec-refinement mechanisms that have no counterpart in the academic benchmarks. (Cross-reference: `research/05-simon-willison.md` §"Specification methodology"; the StrongDM "scenarios as holdout set" pattern.)
2. **Test authoring under model uncertainty.** SWE-bench provides the tests. In real practice the agent (or the human) must *write* the tests, and Simon Willison's "how can you prove software works when both implementation and tests come from the agent?" is the load-bearing question. The architectures answer it with (a) red/green TDD discipline, (b) scenario-based holdout sets, (c) Showboat-style trajectory artifacts as a second-pass review surface, (d) human review at the spec/scenario layer rather than the code layer. None of this is benchmarked. (Even AlphaCode's clustering relies on a *separate model-generated test-input generator* — a quietly load-bearing artifact that the field treats as part of the substrate, not as a benchmarked deliverable.)
3. **Deployment safety and rollback.** No benchmark in this set models deployment, canary, observability, or rollback. The architectures must bring these in via the substrate layer (CI/CD, feature flags, SLOs). This is where `research/11-openhands-substrate-audit.md`'s headless-mode JSONL contract becomes load-bearing — observable agent trajectories are a deployment-safety prerequisite that the academic literature does not require.
4. **Organizational governance and provenance.** No benchmark requires SBOMs, attestations, code-owners review, or audit trails. The architectures must integrate SPDX (S21), SLSA (S25), and review-policy substrate. The El Kaim Council and BCG Platinion governance threads (Round-3 §11.10) are entirely outside the academic frame.
5. **Multi-PR / multi-service coordination.** Real software changes cross PRs, services, and teams. SWE-bench is single-PR. The architectures must define how multi-PR work is decomposed, coordinated, and rolled back as a unit. (The Anthropic C-compiler case study — `research/external-syntheses` S14 — is the closest practitioner analogue.)
6. **Cost, latency, and human attention budgets.** SWE-bench reports pass@1 but not tokens or dollars. mini-SWE-agent's "100 lines, >74%" is partly a cost argument the benchmark does not score. The StrongDM "$1,000/day per engineer" floor (`research/05-simon-willison.md` §"Wait, $1,000/day per engineer?") is *the* practitioner constraint that academic work elides. Each architecture must answer it.
7. **Long-running maintenance and cognitive debt.** SWE-bench measures one-shot resolution. The architectures must answer Simon Willison's cognitive-debt critique — the system that the team ships must remain *understandable* over time. Linear walkthroughs, interactive explanations, and StrongDM Pyramid Summaries are the practitioner answers; no academic benchmark scores them.
8. **The "looking-the-part" hazard.** Simon Willison's May 6 2026 observation — that an LLM-built repo with comprehensive tests and a beautiful README no longer proves care — has no academic counterpart. The architectures must surface *usage signals*, not just test coverage and PR-description quality, as part of quality measurement.
9. **Trust drift / normalization of deviance.** Each successful unmonitored run raises the threshold for human attention. No benchmark scores this; every architecture must instrument it.

## 9. Cross-references to existing reports

- **`research/05-simon-willison.md`** — Simon Willison treats SWE-bench and the AlphaCode pipeline as implicit substrate but does not cite them; this report makes the substrate explicit. Simon's red/green TDD and "First run the tests" patterns are the practitioner-grade versions of SWE-bench's Fail-to-Pass criterion. His parallel-coding-agents post is the practitioner-grade version of AlphaCode's sample-many-then-cluster pipeline (now anchored to §4.4–4.6 verbatim text in this report).
- **`research/11-openhands-substrate-audit.md`** — OpenHands' V1 SDK design principles (sandboxing opt-in; event-sourced linear history; LLM-centric tool interfaces) are direct lineal descendants of SWE-agent's ACI principles. The OpenHands paper's §4.4 "tool system" is the engineering-grade version of SWE-agent §3 / swe-agent.com/latest/background/aci/.
- **§11.7 evals deep-dive** — `research/followup/07-evals-deepdive.md` is referenced in the brief but not yet merged on this branch as of 2026-05-11 (the followup directory contains no `07-evals-deepdive.md`). When merged, the natural cross-reference is from this report's §8(2) (test authoring under model uncertainty) and §8(7) (long-running maintenance) into the evals thread.
- **`research/external-syntheses/chatgpt-deep-research-2026-05-11/sources.md`** §"Weak or missing citations" — flagged CodeGen, LangGraph, OpenHands, and Simon Willison as named-but-uncited in the original report. This report adopts arXiv:2203.13474v5 as the canonical CodeGen citation (ICLR 2023 notable top 25%).

## 10. Open follow-ups

1. **OpenAI "Introducing SWE-bench Verified" full text.** Cloudflare-blocked from the issue-#28 fetcher; capture via a different route if the OpenAI blog post text becomes critical for citation. The swebench.com/verified page already carries the canonical "500 instances, human-validated, in collaboration with OpenAI" claim that the blog post originated.
2. **Princeton PLI blog full text.** Same as above — Cloudflare-blocked. swebench.com is the substitute source.
3. **arXiv full PDF body for SWE-bench v3 and SWE-agent v3.** The fetched HTML renderings returned only nav-chrome; abstracts are anchored, but §3 (ACI design principles) of the SWE-agent paper would be valuable to lock down beyond what the swe-agent.com docs page already provides verbatim.
4. **Cross-reference with the merged evals deep-dive** when it lands on main.
5. **Track the SWE-bench Verified leaderboard delta.** Today's >74% mini-SWE-agent number is the snapshot as of 2026-05-11; the next Round-N pass should re-date it. The 65% → >74% step (Jul 2025 → May 2026) is one 10-month interval; the cadence is visible.
6. **Open question:** does the AlphaCode cluster-by-behavior primitive translate to repository-scale tasks (where "behavior" is fuzzier than competitive-programming I/O)? AlphaCode itself uses a *separate model-generated test-input generator* (§4.6); StrongDM's "satisfaction" score is one operationalization for the repo-scale case. The academic literature does not yet have a clean answer.
7. **Open question:** is there a benchmark on the horizon that closes the spec-refinement gap (§8.1)? MTPB partially closes it but is small (115 problems) and synthetic. A "real-issue-real-spec-refinement" benchmark would be a major contribution. CodeClash (announced Nov 2025 per swebench.com) is the closest visible candidate.

---

**Word count (approximate):** ~4,500 words.

**Sources status summary (post-drain, 2026-05-11):**
- ✅ direct full read: AlphaCode paper (ar5iv mirror full text), DeepMind AlphaCode blog, swebench.com home + /verified + /lite + /original, swe-agent.com/latest + ACI doc, mini-SWE-agent README, Salesforce CodeGen README.
- ✅ abstract-anchored: SWE-bench (arXiv:2310.06770v3), SWE-agent (arXiv:2405.15793v3), CodeGen (arXiv:2203.13474v5), CodeGen ICLR 2023 OpenReview, SWE-agent NeurIPS 2024 OpenReview.
- ❌ unobtainable (Cloudflare): OpenAI "Introducing SWE-bench Verified" blog, Princeton PLI blog. Both substituted by swebench.com primary pages.
