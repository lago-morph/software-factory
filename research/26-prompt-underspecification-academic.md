# Report 26 — Academic Literature on LLM Prompt Underspecification

**Date:** 2026-05-16
**Author:** Subagent B (manual-drain dispatch)
**Status:** ✅ complete

## Lead question

What does the recent academic literature on LLM-based code generation and requirements engineering reveal about prompt underspecification, ambiguity, contradictory task descriptions, and incomplete requirements — and how should those findings inform the methodology layer of an AI-augmented software factory (in particular: spec-authorship discipline, evals, and the "spec → code" gap that the corpus' Round-4 El Kaim reports already named as central)?

## Why these three papers, why now

The corpus has accumulated a *practitioner*-anchored consensus that the "spec → code" gap is the load-bearing risk in any AI-augmented software factory: El Kaim Chapter 8 (Report 14 §10–17) names the missing architectural act between intent and execution; the failure-mode catalog F1–F35 lists at least eight modes that ultimately reduce to "the agent built what the prompt literally said, not what the user actually needed" (F3 spec-completeness fallacy, F4 code-quality teardown, F9 spec overfitting, F13 missing-config blindspot, F15 single-prompt ideation collapse, F18 prose specs lack rigor, F26 telephone drift, F34 cross-layer drift). Yet none of these are anchored in *academic-empirical* measurements of the underspecification phenomenon itself.

The three papers drained here close that gap:

1. **Norheim et al., "Challenges in applying large language models to requirements engineering tasks"** (*Design Science*, vol. 10, e16, 18 Sept 2024 — DOI 10.1017/dsj.2024.8) — a survey article from an MIT/RWTH/Airbus group that catalogues *why the requirements-engineering field's seventy-year struggle with NL ambiguity transfers wholesale to LLM-augmented practice* and what the field has tried.
2. **Yang, Shi, Ma, Liu, Kästner, Wu, "What Prompts Don't Say: Understanding and Managing Underspecification in LLM Prompts"** (arXiv:2505.13360v3, CMU + Google DeepMind, 2025) — the first empirical characterization paper of *prompt* underspecification (rather than ML model underspecification), with 8,400 measured data points and named optimizer primitives (COPRO-R, Bayesian) that produce both accuracy and token-budget wins.
3. **Larbi, Akli, Papadakis, Bouyousfi, Cordy, Sarro, Le Traon, "When Prompts Go Wrong: Evaluating Code Model Robustness to Ambiguous, Contradictory, and Incomplete Task Descriptions"** (arXiv:2507.20439v1, U. Luxembourg + UCL, 2025) — the first robustness benchmark for code-generation LLMs under *deliberately mutated* HumanEval / MBPP descriptions, with a numerical mapping from defect type (ambiguity / contradiction / incompleteness) to Pass@1 drop magnitude and to Python exception class.

The three together give us: (i) a discipline-level framing from RE, (ii) a quantified empirical surface from prompting practice, and (iii) a quantified empirical surface from code-generation evaluation. The trifecta lets us pin claims in the methodology layer to numbers, named taxonomies, and named techniques — not just to practitioner intuition.

## 1. Norheim et al. (Design Science 2024) — the RE-discipline survey

**Thesis (in one sentence).** "Although NLP techniques long lagged… recent developments in the field have led to a renewed interest and hope in the ability of NLP to tackle the many challenges that previously would have been received with skepticism," yet LLM-applied-to-RE remains "still in its infancy," with three structural challenges (limited requirements-specific data, inconsistent data annotation, inadequately-defined RE use cases) that must be solved before LLMs deliver substantive RE benefits (Paper §1, §4).

### 1.1 The five-category RE task taxonomy (Paper §3)

The paper proposes a five-category classification of RE tasks viewed *as LLM tasks* (Paper §3, Fig. 1, Table 1):

| Category | What it does | Existing LLM examples |
|---|---|---|
| **Generation** (§3.1) | NL text in → proposed requirements out (elicitation, refinement, product-line templating) | RE-BERT (Araújo & Marcacini 2021); Arora et al. 2023 GPT-4 zero-shot |
| **Quality assessment** (§3.2) | Detect ambiguity, conformance-to-template, missing/redundant/conflicting requirements at the document level | Draeger 2023; Malik et al. 2022; Luitel et al. 2023 (masked-LM completion for incompleteness) |
| **Analysis** (§3.3) | NER / classification / traceability that produces information used downstream | NoRBERT (Hey et al. 2020), SpaceBERT, aero-BERT, RDC-BERT (Deshpande et al. 2021) |
| **Translation** (§3.4) | Map informal NL to semi-formal/formal (e.g. NL → LTL) | Hahn et al. 2022 (T5 → RegEx/FOL/LTL); Cosler et al. 2023 (few-shot GPT-3, 31/36 on edge cases) |
| **Design** (§3.5) | Validated requirements → design artifacts. Paper notes: "We did not find any published work that specifically targets the use of LLMs to generate design artifacts based on a set of requirements alone." |

The "Analysis is by far the most commonly addressed [task]… most explore NLP-specific operations such as sequence classification or NER rather than addressing RE tasks directly" (Paper §3.7) is the single most useful claim for our purposes: the field has done a lot of *NLP on requirements text* and almost nothing on *generating designs / code from validated requirements*. The empty cell in Paper §3.5 is the literal vacuum that El Kaim Ch8 (Report 14 §10) calls "the missing architectural act between intent and execution."

### 1.2 The three challenges (Paper §4) — taxonomy

The paper's load-bearing classification (Paper §4):

- **Limited requirements-specific data** (§4.1). Public datasets exist (PURE: 79 documents; PROMISE: 625 requirements from 15 student projects, software-only) but are *small and software-biased*. Hardware requirements are barely represented; system-vs-derived requirement diversity is barely represented. Lim 2022 covered "42 hardware systems, including two communication systems, five telescope systems, and 35 spacecraft systems" — and that is the *best* hardware coverage available. The downstream consequence: "any bias in the data sampling… may distort the model's outcomes" (Paper §4.1).
- **Inconsistent data annotation** (§4.2). Even the existing datasets lack RE-task-specific annotation. "The lack of benchmarks is critical, as it makes it impossible to compare multiple NLP methods that attempt to solve the same task, and that can thereby claim that they are able to solve this task beyond a set of crafted use cases" (Paper §4.2). Soares et al. (2019) reframed the same entity-relation extraction task six different ways and got a 46.6-percentage-point F1 gap — i.e. *task framing dominates model quality*.
- **Inadequately-defined RE use cases** (§4.3). "Technology push rather than need pull" — most published LLM-for-RE studies are "what-if scenarios, where NLP practitioners seek the application of their techniques to RE." The paper's sharpest argument: "F1 score… is a poor indicator of the overall benefit resulting from the application of the model" (Paper §4.3, §5, §6). For requirement extraction, Lim 2022 is cited verbatim: *"the failure to extract all required information may result in the construction of an incomplete system model, affecting its functionality and desired ilities. In this specific context, recall should be prioritized over precision."* The **Perfect Recall Condition** (Lucassen et al. 2016 via Berry et al. 2012) is named: for tools whose role is "do not miss any critical information, or mislead the user with wrong information," nothing short of recall=1 *and* precision=1 is acceptable.

### 1.3 Adoption challenge (Paper §4.4)

Adoption "will require new skill sets that may not currently exist among RE professionals, particularly in ML methods and tools, model training and validation." This is a labor-market claim that maps directly onto F29 (talent pipeline depletion) from Report 13. The paper sharpens it: even if pipeline is solved, "the current performance of the best LLM-based NLP tools is less than perfect in precision and recall… these models will continue to produce false positive and false negative predictions for the foreseeable future. Organizations will have to determine in which RE applications the error level is tolerable and in which cases it is not" (§4.4).

### 1.4 Future-directions checklist (Paper §5.1) — what we should already have

Verbatim:

> "Increased use of hardware requirements datasets that include the increased degree of dependency that can come with hardware compared with software requirements.
>
> Comparing the challenges that requirements of different types and from different stakeholders or different stages of the system lifecycle might pose to NLP and LLM methods…
>
> Develop benchmark requirements datasets to enable the systematic exploration and evaluation of the application of NLP and LLM methods to different RE tasks…
>
> Identify RE tasks and reference use cases in the context of a real Product Development Process to design and deploy NLP and LLM methods and evaluate their strengths and limitations relative to existing methods." (Paper §5.1)

The third and fourth bullets are exactly what `research/followup/07-evals-deepdive.md` and El Kaim's `EvaluationSuite` typed object (Report 14 §15) try to provide on the methodology side. This paper is the academic warrant for that work.

## 2. Yang et al. (arXiv:2505.13360v3) — "What Prompts Don't Say"

**Thesis (one sentence).** "Prompt underspecification is a common challenge when interacting with LLMs… while LLMs can often infer unspecified requirements by default (41.1%), such behavior is fragile: Under-specified prompts are 2x as likely to regress across model or prompt changes, sometimes with accuracy drops exceeding 20%" (Paper Abstract).

### 2.1 Definitional move (Paper §1)

The paper's definition is operative and we should adopt it:

> "We define underspecification as the omission of essential requirements in a prompt, such that multiple valid but inconsistent behaviors remain possible." (Paper §1)

This is more precise than the existing corpus's loose talk of "vague specs" or "spec overfitting." It anchors the failure on *unspecified requirements that are nonetheless essential* — i.e. requirements the developer would, on reflection, want enforced.

### 2.2 The amplification taxonomy (Paper §2 + Table 1)

Paper §2 articulates *why* underspecification is worse for prompts than for traditional software or ML. Table 1 (Paper §2) is reproduced here because it is the cleanest framing in the literature:

| Aspect | LLM Prompt | Traditional ML | Traditional Software |
|---|---|---|---|
| Specification Method | NL prompts (instructions, examples) | Training data + architecture + pipeline | NL + sometimes formal specifications |
| Engineering Practices | Ad-hoc, trial-and-error iteration (Liang 2024; Zamfirescu-Pereira 2023) | More structured experimentation pipelines | Systematic RE and design processes (Van Lamsweerde 2009) |
| Artifact Evolution | Frequent changes with little version control | Periodic, some version control | Evolution intentionally tracked and limited |
| Consequences | Inconsistent and unexpected LLM behaviors | Generalization failures, model biases | Software that does not meet customer needs |

The two amplifiers named (Paper §2): (a) **"Ad-hoc prompt engineering amplifies underspecification"** — the "minimal-specification" pattern of "begin with an initial prompt, observe violations of expected behavior, and iteratively revise through adding more instructions… this trial-and-error process lacks the rigor of traditional requirements engineering"; (b) **"Rapid Prompt-LLM co-evolution amplifies underspecification"** — *both* prompts and models change underneath developers, so "previously validated behaviors may no longer hold, requiring repeated rediscovery of requirements." The dual evolution claim is verifiable empirically (Paper §3.3, below) and is the load-bearing argument against "vibe-check" prompt maintenance.

### 2.3 The empirical study (Paper §3) — setup

- **Tasks**: code-explain (Commitpackft), trip-advisory (UltraChat subset), product-gen (Amazon ESCI), plus health-consulting and lesson-planning in Appendix D.
- **Data**: 200 examples per task, 15/35/50 train/val/test split.
- **Requirements**: 20 per task, elicited via three methods chosen to mirror RE practice (Van Lamsweerde 2009): *existing prompts* (Anthropic, Google, popular GPTs), *brainstorming* (gpt-4o anticipates failure modes), *error analysis* (gpt-4o reviews small-LLM outputs).
- **Validators**: 95.6% human-LLM agreement (Paper §3.1).
- **Prompt construction**: cyclic design where each prompt includes N consecutive requirements (N=10 default) so each requirement appears equally often.
- **Models**: Llama-3.3-70B-Instruct, gpt-4o-2024-08-06, o3-mini (Paper §3.2); plus gpt-4o variants 05-13/08-06/11-20 and Llama-3 variants for the model-update study (Paper §3.3).
- **Scale**: 8,400 measured data points + over 1.5M LLM calls in total (Paper Limitations + Appendix A.9).

### 2.4 Headline quantitative findings (Paper §3.2–3.4)

| Finding | Number | Paper anchor |
|---|---|---|
| Accuracy drop when requirement unspecified vs. specified (mean) | **−22.6%**, up to **−93.1%** | §3.2 |
| Cases where LLM nonetheless guesses an unspecified requirement (≥0.98 accuracy) | **41.1%** | §3.2 |
| Format-related requirements guessed by default | **70.7%** | §3.2 |
| Conditional requirements guessed by default | **22.9%** | §3.2 |
| Requirements from existing developer prompts that LLMs would have guessed anyway | **65.2%** | §3.2 |
| Standard deviation on unspecified requirements vs. specified | **8.9% vs. ~3.5%** (over 2× increase) | §3.2 |
| Std dev controlling for requirement conflicts | **7.9% unspecified vs. 0.8% specified** | §3.2 + Appendix C.3 |
| Stronger reasoning models do better at guessing | o3-mini **44.7%**, +20.2% over Llama-3.3-70B | §3.2 |
| Rate of model-update regressions on unspecified requirements (>20% drop) | **5.9%** | §3.3 |
| Same rate on specified requirements | **~3%** (almost 2× increase) | §3.3 |
| Specific update example: gpt-4o 05-13 → 08-06 on "produce skimmable outputs" | **−48%** | §3.3 |
| Same update on "mention customer support information" | **−14%** | §3.3 |
| Average accuracy on a single specified requirement (upper bound) | **98.7%** | §3.4 |
| Average accuracy with 19 requirements specified together (gpt-4o) | **85.0%** (i.e. **−13.7%**) | §3.4 |
| Same for Llama-3.3-70B-Instruct | **79.7%** (i.e. **−19%**) | §3.4 |
| Worst observed per-requirement drop, "use analogies and examples" on gpt-4o | **−81.3%** | §3.4 |

The §3.2 result is the most load-bearing for our corpus: **specifying a requirement is worth ~22.6 percentage points on average**, but **41.1% of the time the requirement is followed by default anyway**. So a naïve "spec everything" prompt is paying token cost for behavior that would happen anyway, while simultaneously consuming the instruction-following budget — and §3.4 shows that budget is *not* free. "Specifying 19 requirements together yields only an 85.0% average accuracy for gpt-4o. Smaller models like Llama-3.3-70B-Instruct struggle even more, with only 79.7%" (Paper §3.4). This is a quantitative version of F18 (prose specs lack rigor) — but with a twist: the failure is not that prose is too weak, it is that *too much prose actively degrades instruction-following*.

### 2.5 Named techniques the paper proposes (Paper §4)

- **COPRO-R.** Existing DSPy COPRO optimizer (Khattab et al. 2023) augmented with requirement-specific validators. Optimizer feedback becomes per-requirement accuracy (specified *or unspecified*). Result (Paper §4 Table 2): **+5.8% average accuracy** over original prompts.
- **Bayesian / requirement-selection optimizer.** Model each requirement as a binary hyperparameter (specified ∈ {0,1}); the configuration `r ∈ {0,1}^n` is the search variable; objective is `r* = argmax_r f(r)` where `f` is average requirement accuracy. The search uses Tree-structured Parzen Estimator (Bergstra et al. 2011). Result: **+3.8% accuracy** *and* **−41 to −45% token usage**, with a "global, format, and developer-written requirements are more likely to be dropped" pattern (56.5% / 77.0% / 57.9% drop rates respectively vs. 52.8% overall average) that aligns with §3.2's "LLMs are especially good at guessing format-related requirements."
- **Real-world agentic-coding case study (Paper §4 + Appendix E).** A Cursor-community baseline prompt for "website-gen" went from 0.441 accuracy at 431 tokens → 0.535 at 654 tokens (COPRO-R) → **0.474 at 121 tokens (Bayesian)**. The Bayesian optimizer **reduced token usage by 71.9%** in the agentic-coding context.

### 2.6 The "manage underspecification" framework (Paper §5)

Paper §5 lists three practices, framed explicitly as Sommerville-style software-engineering imports:

1. **"Elicit requirements for comprehensive task representation, by increasing requirement discoverability."** Synthetic data generation, top-down brainstorming, bottom-up data-driven analysis, structured safety engineering (Hong et al. 2025).
2. **"Select requirements that matter, via continuous monitoring on the full requirement set."** Background validation of *all* tracked requirements (specified *and* not), drift detection, model-migration re-selection. "Existing practices of manual inspection ('vibe check') of a few examples will not be sustainable" (Paper §3.3).
3. **"Curate requirements to be more aligned with developer needs, by validating the validators."** Close the loop between requirements and their validators; treat low-confidence/inconsistent validator outputs as a *signal of ambiguity in the requirement itself* (Shankar et al. 2024).

### 2.7 Most load-bearing verbatim quotes

> "We define underspecification as the omission of essential requirements in a prompt, such that multiple valid but inconsistent behaviors remain possible." (§1)

> "LLMs are often able to guess unspecified requirements – in 41.1% of cases, they are able to achieve more than 98% accuracy on unspecified requirements. Indeed, for 65% of all requirements, we found at least one LLM+prompt combination that is able to guess it without explicit specification." (§3.2)

> "5.9% requirements regress more than 20% over model updates when they are unspecified – an almost 2x increase compared to specified requirements." (§3.3)

> "Specifying 19 requirements together yields only an 85.0% average accuracy for gpt-4o." (§3.4)

> "Intentional underspecification can be a strategy to focus the model only on select requirements without distracting it with requirements it follows by default." (§3.4)

## 3. Larbi et al. (arXiv:2507.20439v1) — "When Prompts Go Wrong"

**Thesis (one sentence).** "Even minor imperfections in task description phrasing can cause significant performance degradation, with contradictory task descriptions resulting in numerous logical errors. Moreover, while larger models tend to be more resilient than smaller variants, they are not immune to the challenges posed by unclear requirements." (Paper Abstract)

### 3.1 The three-defect taxonomy (Paper §4)

Anchored in IEEE Std 830-1998 and Montgomery et al. 2022, the paper enforces the three most prevalent requirement quality issues:

- **Ambiguity** (§4): "A task description is ambiguous if it has more than one interpretation, for example, because it uses vague wording."
- **Contradiction / inconsistency** (§4): "A task description is contradictory if a subset of its statements are conflicting, for example if it expresses incompatible post-conditions or gives conflicting examples."
- **Incompleteness** (§4): "A task description is incomplete if it does not define the responses to all realizable classes of input data in all realizable classes of situations. For example, it may omit information about key parameters or edge cases."

The paper cites Bertrand Meyer's "seven sins of specifiers" (Meyer 1985) and Van Lamsweerde 2009 as the prior taxonomies; it argues that these three — ambiguity, contradiction, incompleteness — are the most prevalent in practice.

### 3.2 Benchmark introduced (Paper §4)

A mutated extension of **HumanEval (164 hand-crafted tasks) and MBPP (974 crowd-sourced tasks)** in which GPT-4 acts as a *mutation engine* steered by a published mutation-guideline taxonomy (Paper §4.1, Listing 1; Paper Fig. 3). Each original task description gets three mutated variants (incomplete, contradictory, ambiguous). The mutations are validated through a two-stage process:

- Five-reviewer expert validation (2 PhD students, 2 postdocs, 1 MSc) scoring *naturalness* (does this look like a real developer prompt?) and *defect presence* (does it actually exhibit the labeled defect type?). Results: **85% rated natural, 93% rated as containing a valid instance of the intended quality issue** (Paper §4.2).
- Manual refinement of the failing ~7–15%, with re-validation.

Dataset and code are released at `github.com/serval-uni-lu/Robustness-of-LLMs-to-prompt-imperfections` (Paper §5.3).

### 3.3 Headline quantitative findings (Paper §6)

**RQ1 (can LLMs detect unclear prompts?).** No. MCC for binary "clear vs unclear" classification on HumanEval ranges **−0.06 to 0.47**; on MBPP, **−0.1 to 0.45**. For three-way category classification (ambiguous / contradictory / incomplete), GPT-4 tops out at **MCC = 0.55 on HumanEval, 0.45 on MBPP** (Paper §6.1). The class hardest to detect across nearly all models is *Ambiguous*. Per Paper §6.1: "Code generation models cannot reliably detect problems in task descriptions. This shows that, unlike humans, they cannot natively react to low-quality requirements and would nevertheless attempt to produce a solution." This *empirically falsifies* the casual assumption that one can rely on the model to ask for clarification — the model will not even reliably *notice* that clarification is needed.

**RQ2 (performance under unclear prompts).** Pass@1 drops are large, model-family-wide, and **worst for contradictory prompts**:

HumanEval Pass@1 drops vs. original (Paper Table 2):

| Model | Original | Incomplete | Ambiguous | Contradictory |
|---|---|---|---|---|
| GPT-4 | 73.8 | 45.1 (−28.7) | 34.8 (−39) | **6.7 (−67.1)** |
| Qwen2.5-32B | 86.0 | 61.1 (−24.9) | 56.1 (−29.9) | **8.5 (−77.5)** |
| DeepSeek-coder-33B | 71.3 | 48.8 (−22.5) | 44.5 (−26.8) | **9.1 (−61.6)** |
| CodeLlama-34B | 50.0 | 29.3 (−20.7) | 26.8 (−23.2) | 4.9 (−45.1) |
| Qwen2.5-7B | 79.3 | 56.1 (−23.2) | 54.9 (−24.4) | **4.3 (−75.0)** |

Across the seven evaluated models, **contradictory descriptions drop Pass@1 by up to 77.5 percentage points (Qwen2.5-7B on HumanEval) and by 65.6 percentage points on average across the strongest models** (calculation: GPT-4 −67.1, Qwen2.5-32B −77.5, DeepSeek-33B −61.6, CodeLlama-34B −45.1, mean ≈ 62.8). On MBPP the drops are smaller but still severe (Paper Table 3: GPT-4 Pass@1 drops from 38.6 to 8.4 under contradictory, **−30.2**).

The **Runnable but Incorrect Rate (RIR)** — the share of programs that *executed without errors* but failed the test cases — is the most disturbing number in the paper. For GPT-4 on HumanEval:

> "The Runnable but Incorrect Rate (RIR) are also increasing significantly, e.g., the GPT-4 model increases the incorrect behaviors of the produced code from 24% in the original descriptions to 54%, 65% and 89% in the cases of Incomplete, Ambiguous and contradictory descriptions." (Paper §6.2)

For MBPP, GPT-4 RIR climbs from 54.6% (original) to **88.4% (incomplete)**, 80.3% (ambiguous), 64.9% (contradictory) (Paper Table 3). The headline from §8 (Conclusion): *60–90% of the code that compiles is semantically incorrect under unclear prompts.* Successful Execution Rate (SER) stays high (often >90%), so the broken code looks like working code — a *direct empirical confirmation of F2 (reward hacking) and F1 (hallucination loop) at the requirements-quality layer*.

**RQ3 (failure modes).** The paper extracts 3,114 Python exceptions from incorrect generations and bins them by defect category (Paper Table 4):

| Defect | Dominant Python exceptions | Interpretation |
|---|---|---|
| **Incomplete** | NotFoundError **82.4%**, IndentationError 52.1%, SyntaxError 41.3%, TypeError 37.3% | "Structural gaps… models to hallucinate or mishandle variables, arguments, or input types" |
| **Ambiguous** | KeyError 38.9%, AttributeError 31.4%, IndexError 28.2% | "Semantically flawed logic that nonetheless executes" |
| **Contradictory** | NameError 22.9%, ValueError 20.4% (high relative to original) | "Models are confused by internal inconsistencies, leading to conflicting variable usage or return semantics" |
| **Original** | NameError 29.8%, ValueError 30.1% | Baseline noise |

The taxonomy is sharp: **incompleteness produces structural / runtime failures; ambiguity produces semantically-misaligned-but-executable code; contradiction produces logical inconsistency**. This is a directly testable signature for triaging field failures back to the prompt defect that caused them.

### 3.4 Most load-bearing verbatim quotes

> "Code generation models cannot reliably classify clear and unclear task descriptions (-0.1 to 0.55 MCC). This indicates their inability to mimic human reaction to low-quality requirements (asking clarification) and confirms the necessity to evaluate their robustness capacity to generate the expected code in spite of quality issues in the description." (§1)

> "Across both data sets and all models, Pass@1 performance decreases significantly when faced with unclear task descriptions. On average, ambiguous descriptions lead to a 25–30% reduction in Pass@1 accuracy, while incomplete descriptions cause drops of 20 to 25%. Contradictory descriptions have the most severe impact, reducing accuracy by up to 40%." (§6.2)

> "60-90% of the code that compiles is semantically incorrect [under unclear prompts]. Although larger models generally outperform smaller ones in terms of compilation rates, the code they produce is (largely) semantically incorrect code. This means that scale alone does not guarantee robustness especially under contradictory or vague requirements." (§8)

## 4. Cross-paper synthesis — taxonomies and named constructs

### 4.1 Three converging taxonomies of requirement defects

Each paper carves the underspecification space slightly differently. Stacked:

| Construct | Norheim et al. | Yang et al. | Larbi et al. |
|---|---|---|---|
| Top-level concept | Requirement quality (correctness, consistency, completeness) | Underspecification (omission of essential requirements) | Task-description imperfections |
| Sub-types named | Generation / Quality / Analysis / Translation / Design (RE tasks); + correctness / consistency / completeness as quality dimensions | Format / Content / Style; Conditional vs. unconditional; Global vs. local; Developer-written vs. auto-elicited | Ambiguity / Contradiction / Incompleteness |
| Anchored in | IEEE/INCOSE RE tradition; Berry et al., Lucassen et al. (Perfect Recall Condition) | Sommerville 2015; Van Lamsweerde 2009; D'Amour 2022 (ML underspecification) | IEEE Std 830-1998; Meyer 1985 ("seven sins of specifiers"); Van Lamsweerde 2009 |

The clean operational fusion: **adopt Larbi et al.'s ambiguity / contradiction / incompleteness as the *defect taxonomy*** (because it is binary-labelable, has a benchmark, and maps to Python exception classes for triage) and **adopt Yang et al.'s definition of underspecification as omission-of-essential-requirements as the *concept*** (because it is the operative concept across all three papers and is testable via differential prompts). The Norheim et al. RE-task taxonomy (Generation / Quality / Analysis / Translation / Design) is the *governance layer* — it tells you where in the lifecycle each defect is born.

### 4.2 Quantified consensus on three claims

Three claims now have empirical support across two or three of these papers and should be treated as established:

1. **Specifying a requirement gives a substantial accuracy lift.** Yang et al. §3.2 measure **+22.6 pp average, up to +93.1 pp**. Larbi et al. §6.2 measure the inverse: removing/mutating requirements drops Pass@1 by **20–40 pp** depending on defect type, with contradictions costing **up to 77.5 pp** in the worst case.
2. **LLMs cannot reliably detect when a prompt is underspecified.** Larbi et al. §6.1 quantifies: MCC tops out at **0.55 (GPT-4 on HumanEval), 0.45 (GPT-4 on MBPP)**. Yang et al. §3.2 establishes the same for prompts: developers under-specify routinely and the model only sometimes (41.1%) covers the gap. Norheim et al. §4.3 names this as "Perfect Recall Condition" — for high-stakes RE applications, anything less than recall=1 *and* precision=1 is unacceptable.
3. **Compounding requirements creates instruction-following pressure.** Yang et al. §3.4 measures: gpt-4o drops from 98.7% (1 requirement) to 85.0% (19 requirements). The naïve "spec-everything" response to underspecification is itself a failure mode.

A fourth claim with weaker but useful support: **stronger / larger models are more resilient but not immune**. Yang et al. §3.2 shows o3-mini does 20.2% better at guessing unspecified requirements than Llama-3.3-70B; Larbi et al. §6.2 shows the 32–34B family generally beats the 6–7B family but Qwen-7B sometimes beats Qwen-32B on MBPP. Norheim et al. §4.4 explicitly warns that future LLMs will retain non-zero error rates.

### 4.3 Named techniques across the three papers

| Name | Paper | What it does | Mapping to corpus primitives |
|---|---|---|---|
| **COPRO-R** | Yang §4 | DSPy COPRO + per-requirement validators | The "eval suite as gate" pattern from El Kaim Ch8 §7 (Report 14 §15) — each metric protects a specific requirement |
| **Bayesian (TPE) requirement-selection optimizer** | Yang §4 | Searches `{0,1}^n` to pick which requirements to specify | Closest existing corpus primitive: none. *New shape.* |
| **Requirement validators** | Yang §3.1 + Appendix A.6 | Per-requirement Python or LLM-judge with 95.6% human agreement | El Kaim `EvaluationSuite.metrics` (Report 14 §15) — each metric with `protects: RULE-ID` |
| **Continuous validation of unspecified requirements** | Yang §5 | Run background validators on all tracked requirements, not just specified ones | Extends the Healer / production-trace loop (Report 14 §16) |
| **Mutation-based defect benchmark** | Larbi §4 | GPT-4 as mutation engine + 5-reviewer validation | New shape; matches StrongDM's "scenarios as out-of-tree holdouts" (F28 mitigation, Report 13) |
| **NL → LTL translation** | Norheim §3.4 | T5 / GPT-3 fine-tuned for formal-spec translation | Closest corpus primitive: `OPA-Rego` derived executable constraints (El Kaim Ch8 §6, Report 14 §14) |
| **Perfect Recall Condition** | Norheim §4.3 (citing Lucassen et al. 2016) | For high-stakes RE tools, recall=1 AND precision=1 | Concept-level; informs F33 (adversarial-prompt defeat) and the "evals as gate" framing |

The "COPRO-R" / "EvaluationSuite" mapping is the most useful single bridge: **Yang et al.'s requirement-specific validator is the exact same shape as El Kaim's `EvaluationSuite.metrics` with `protects: RULE-ID`**. The academic paper provides what El Kaim's chapter only sketches: empirical evidence that this shape produces +5.8% accuracy with no token-cost penalty.

## 5. Implications for the software factory

### 5.1 Failure-mode catalog — reinforcements and proposals

The three papers strongly **reinforce** the following existing failure modes (Report 00 §4, Report 13 §3, followup/12):

- **F1 (Hallucination Loop)** — Larbi et al. §6.2 shows GPT-4's RIR (runnable-but-incorrect) climbs from 24% → 89% under contradictory prompts; this is the population-scale version of F1 driven by *prompt defect*, not model defect.
- **F2 (Reward hacking)** — Yang et al. §3.4 shows specifying many requirements creates conflicts and instruction-following degradation: a smaller "passes the spec" feels like satisfying all 19 requirements when in fact 5 are silently being neglected.
- **F3 (Spec-completeness fallacy)** — Yang et al. §3.4 + §5 make this empirical: requirements *cannot* all be specified; the methodological move is "select what to specify, monitor what isn't."
- **F4 (Code-quality teardown)** — Larbi et al. §6.3 Table 4 gives the exception-class signature: a repo full of code that runs but throws AttributeError on real inputs is the empirical signature of ambiguous prompts.
- **F9 (Spec overfitting)** — Yang et al. §3.3 quantifies model-update regression on unspecified requirements: 5.9% of unspecified requirements degrade by >20% on any given model update. Spec overfitting is now a *measurable drift*, not just a sociological claim.
- **F15 (Single-prompt ideation collapse)** — Yang et al. §3.2 shows a single-prompt practice misses 65% of plausible requirements (the discoverability gap behind §3.1).
- **F18 (Prose specs lack rigor)** — All three papers reinforce. Norheim §3.4 specifically calls for *NL → formal* translation; Yang §3.4 shows prose alone is bounded by ~85% accuracy at scale.
- **F34 (Cross-layer drift, followup/12)** — Yang §3.3's "behavioral drift" is the prompt-layer analog of Brier's pace-layer drift: the prompt is consistent with the spec, but the *model* has shifted underneath.
- **F35 (Federation-as-Family Drift)** — Yang §5's "continuous monitoring of all tracked requirements" is precisely the discipline F35 demands at the spec/family level.

The three papers also surface **two candidate proposals for the F-mode catalog**. These are flagged as **proposals for lead-agent review** rather than asserted:

> **Proposed F36 — Instruction-following ceiling.** The naïve fix to underspecification ("spec everything") fails for an independently measurable reason: LLMs cannot reliably follow >10–20 specified requirements simultaneously. Empirical anchor: Yang et al. §3.4 — gpt-4o drops from 98.7% (1 requirement) to 85.0% (19 requirements); Llama-3.3-70B drops to 79.7%. Distinct from F18 (prose specs lack rigor) because the failure is not vagueness but *budget exhaustion*; distinct from F3 (spec-completeness fallacy) because it persists *even when the spec is complete*. **Mitigation:** Bayesian / TPE requirement-selection optimization (Yang §4.2); split requirements across sub-modules in agent workflows; use background validators to monitor unspecified requirements rather than embed them in the active prompt. **Proposed, awaiting lead-agent decision.**

> **Proposed F37 — Silent contradictory-prompt collapse.** The model does not flag contradictory prompts and produces dramatically wrong output that *runs*. Empirical anchor: Larbi et al. §6.1 (MCC 0.55 max for detection) + §6.2 (GPT-4 Pass@1 drops from 73.8% to 6.7% on contradictory HumanEval prompts; RIR climbs to 89%). Distinct from F1 because the failure is upstream of the model (in the prompt); distinct from F18 because the prompt may be syntactically rigorous yet contain contradictions only a domain-aware reviewer would catch. **Mitigation:** pre-flight contradictory-prompt detection as a substrate primitive (not relying on the model itself); paired-spec / triangulation; the El Kaim Ch8 §6 OPA-Rego *contradiction* check pattern; the dataset from Larbi et al. as a fixed eval. **Proposed, awaiting lead-agent decision.**

### 5.2 Concrete changes for `spec-driven-ai-dev.md` and friends

> **Status note (2026-05-21, issue [#105](https://github.com/lago-morph/software-factory/issues/105)):** `spec-driven-ai-dev.md` is a cataloged source (record [`3592091691`](../reference-only/3592091691/spec-driven-ai-dev.md)), not a mutable internal artifact. The proposals below are research findings that can inform a v3 methodology document authored separately; they are not pending edits against the source file.

Five concrete proposals, each grounded in a numbered claim above:

1. **Adopt Yang et al.'s definition of underspecification verbatim** in the spec-authorship doc. The current corpus uses "vague," "incomplete," "spec overfitting" inconsistently. Replace with: *"underspecification = omission of essential requirements such that multiple valid but inconsistent behaviors remain possible"* (Yang §1).
2. **Adopt Larbi et al.'s three-defect taxonomy (ambiguity / contradiction / incompleteness) as the QA checklist for spec authorship.** Pair each defect with its Python-exception signature (Larbi Table 4) for field-failure triage: AttributeError/KeyError → review for ambiguity; NotFoundError/SyntaxError/TypeError → review for incompleteness; NameError/ValueError → review for contradictions.
3. **Bind each `EvaluationSuite.metric` to *both* "specified" and "implicitly assumed" requirements.** Currently `protects: RULE-ID` (El Kaim Ch8 §7) only references rules that are explicitly stated. Yang et al. §3.3 shows that *unspecified-but-implicitly-assumed* requirements are 2× more likely to regress on model updates. The eval suite must therefore include metrics that test for *unspecified-but-expected* behaviors. Concrete add: an `assumes: REQ-ID` field alongside `protects: RULE-ID`.
4. **Add a "specification budget" check to the preflight linter (Report 14 §9.3).** Empirical limit from Yang §3.4: prompts with >10–15 requirements are paying for accuracy losses. The preflight linter should warn when a spec block being injected into a prompt exceeds ~10 active requirements; surplus requirements should be moved to background validators per Yang §5.
5. **Add a "contradiction-detection" check to the preflight linter.** Per Larbi §6.1 (MCC ≤0.55), the *model itself* cannot be trusted to detect contradictions. Use a deterministic pre-flight pass (a separate LLM call dedicated to consistency, an OPA-Rego constraint, or a small classifier) before dispatching the prompt to a builder agent. This is the substrate-level enforcement that closes the proposed F37.

### 5.3 Mapping paper-named techniques to corpus primitives

| Paper-named technique | Corpus primitive it maps to | Action |
|---|---|---|
| Yang's COPRO-R (per-requirement validator + optimizer feedback) | El Kaim `EvaluationSuite.metrics[*].protects: RULE-ID` (Report 14 §15) | Treat COPRO-R as the *automatable* version of the El Kaim eval-suite shape; cite both in spec-driven-ai-dev.md |
| Yang's Bayesian requirement-selection | New shape — closest existing primitive is StrongDM's "satisfaction scoring" (Report 01) | Propose a new primitive: "active-spec / background-spec partitioning" |
| Yang's continuous monitoring of all tracked requirements | The Healer / production-trace loop (Report 14 §16; followup/07 evals) | Extend followup/07 to require background validation of *unspecified* assumed behaviors |
| Larbi's mutation-based defect benchmark | F28 mitigation: out-of-tree scenarios (Report 13 §3) | Adopt mutation-engine pattern for generating *acceptance-test* holdouts; cite Larbi §4.1 mutation guidelines |
| Norheim's NL → LTL translation | OPA-Rego derived executable constraints (Report 14 §14) | Position Rego as the corpus equivalent of formal-spec translation; cite Cosler et al. 2023 as proof-of-feasibility (31/36 edge-case translations correct with few-shot GPT-3) |
| Norheim's Perfect Recall Condition | El Kaim Ch8 §9 "false specification" failure mode (Report 14 §17) | Cite Norheim §4.3 + Lucassen 2016 as the discipline-level precedent for the "every rule must trace to a check that runs" trace test |

### 5.4 Cross-references the lead agent should consider weaving in

- `research/14-el-kaim-book-intent-and-spec-authorship.md` §15 (evals as second executable control) — Yang et al. §4.2's COPRO-R *is* the eval-as-gate pattern, with empirical numbers attached (+5.8%, +3.8%, −41–45% tokens).
- `research/22-academic-foundations.md` — extend the §11.7 evals deep-dive (or its replacement) to cite Yang et al. as the prompt-side companion to AlphaCode's verify-by-tests pipeline. The shared insight: *generate many, then verify against a per-requirement criterion*.
- `research/05-simon-willison.md` — Willison's "97% is a failing grade" doctrine now has direct empirical support: Larbi et al. §6.2's GPT-4 RIR climbs from 24% on clean prompts to 89% on contradictory prompts. The 97% claim is not just rhetoric; the field-failure mode is *exactly* "looks like it works (SER stays high) but is semantically broken."
- `research/followup/07-evals-deepdive.md` — adopt Yang et al.'s "validators with 95.6% human-LLM agreement" as a calibration target; adopt Larbi et al.'s exception-class binning as a field-failure triage method.
- `research/followup/08-security-primitives.md` — Larbi §6.1's finding that LLMs cannot detect contradictory prompts is a *direct adjunct* to F12 (lethal trifecta) / F33 (adversarial-prompt defeat of LLM-based security analysis). The prompt itself can be the adversarial input.
- `research/00-synthesis.md` §4 — the F1–F35 table should grow to include proposed F36 (instruction-following ceiling) and F37 (silent contradictory-prompt collapse) pending lead-agent review.
- `research/13-round-2-synthesis.md` §3 — both proposed failure modes are *methodology-layer*, not substrate-layer, in the §3 dichotomy. They sit alongside F1–F30, not F31–F33.

### 5.5 What this report does *not* settle

- Whether prose-spec authorship (El Kaim Ch8 §5) or formal-spec translation (Norheim §3.4, NL → LTL) is the right primary mode for the corpus. The three papers together suggest a *hybrid*: prose for human readability + auto-derived formal constraints + per-requirement validators.
- Whether the Bayesian / TPE optimizer should run *inside* the methodology layer or as a separate offline tool. Yang et al. §4.2 doesn't take a position; the practical answer depends on substrate.
- Whether F36 and F37 should be promoted or merged into existing modes. Recommend **lead-agent review**.
- Whether the Larbi et al. benchmark itself should be adopted as a permanent corpus eval (it's HumanEval/MBPP-based, so subject to data-contamination concerns the authors acknowledge in §7).

---

## Sources reviewed

Status legend: ✅ full primary text read · 🟡 partial · ❌ unobtainable.

| Source URL | Status | Notes |
|---|---|---|
| https://www.cambridge.org/core/journals/design-science/article/challenges-in-applying-large-language-models-to-requirements-engineering-tasks/1FC7666F0A0B4E7091D2D4B2D46321B5 | ✅ | Norheim et al., *Design Science* vol. 10, e16 (DOI 10.1017/dsj.2024.8). Read end-to-end from manual-fetched MHTML (research/manual/, ~153 KB raw). Anchored Sections 1 (RE-discipline survey), 4.1–4.3 (five-task taxonomy + three challenges) and 5.1 (future-directions checklist) of this report. |
| https://arxiv.org/html/2505.13360v3 | ✅ | Yang et al. arXiv:2505.13360v3 (CMU + Google DeepMind). Read end-to-end from manual-fetched HTML (research/manual/, ~137 KB raw). Anchored Sections 2 (paper) and 4 (cross-paper synthesis quantitative claims) of this report. All Table 2 numbers and §3.2/§3.3/§3.4 numbers verified verbatim against paper text. Code/data: https://github.com/malusamayo/underspec-analysis. |
| https://arxiv.org/html/2507.20439v1 | ✅ | Larbi et al. arXiv:2507.20439v1 (U. Luxembourg + UCL). Read end-to-end from manual-fetched HTML (research/manual/, ~86 KB raw). Anchored Sections 3 (paper) and 4 (cross-paper synthesis) of this report. Tables 2, 3, 4 numbers verified verbatim. Code/data: https://github.com/serval-uni-lu/Robustness-of-LLMs-to-prompt-imperfections. |

**Word count target:** ~4,500 words (within the 3,500–5,500 band specified in the brief).

**Open follow-ups (for lead-agent triage):**

- Decide on proposed F36 (instruction-following ceiling) and F37 (silent contradictory-prompt collapse).
- Update `research/INDEX.md` and `research/PLAN.md` to reflect Report 26 and the two proposed F-modes (out of scope for this subagent).
- Consider extending `research/followup/07-evals-deepdive.md` with COPRO-R and the requirement-validator pattern as concrete operationalizations of `EvaluationSuite.metrics`.
- Consider whether the Larbi et al. mutation dataset should be adopted as a corpus-level holdout eval.
