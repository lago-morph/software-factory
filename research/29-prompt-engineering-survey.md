# Research Report 29 — The Prompt Report: A Systematic Survey of Prompt Engineering Techniques

**Date:** 2026-05-16
**Status:** ✅ FULL — primary-source-anchored
**Author:** Cluster L drain subagent
**Source count:** 1 primary (Schulhoff et al., arXiv:2406.06608v6, 76 pp, last revised Feb 2025)

**Scope.** Anchor the corpus' prompt-engineering and harness discussion in the largest available primary meta-analysis — Schulhoff et al.'s PRISMA-style review of 1,565 prompt-engineering papers (the result of an initial 4,797-record sweep across arXiv, Semantic Scholar, and ACL). Establish the 58-text-based-technique taxonomy as the academic spine the rest of the corpus (reports 05, 14, 22, 23, 25, 26, 28; followups 07, 08) implicitly draws on. Provide a 1:1 cross-corpus mapping table, a closing case study on DSPy vs hand-crafted prompt engineering, and an open-questions list.

---

## Drain note (Cluster L manual MHTML capture) — 2026-05-16

This report is **new** — the Schulhoff *Prompt Report* (arXiv:2406.06608) was previously cited in `06-hn-and-lenny.md` and `05-simon-willison.md` only via Lenny's-newsletter security podcast (the CaMeL endorsement context) and was not a sources-table anchor anywhere in the corpus. Primary source: manual MHTML capture of the arXiv HTML render at `https://arxiv.org/html/2406.06608v6` (`research/manual/The Prompt Report_ A Systematic Survey of Prompt Engineering Techniques.mhtml`; 310,181 chars of body text; 15 images of which 3 are non-decorative). Drained 2026-05-16.

Three images extracted from the MHTML into `research/figures/29-prompt-engineering-survey/`:

- `prisma-pipeline.png` (from MHTML image index 11, source URL `…/x3.png`, 205 KB) — the PRISMA-style screening pipeline (4,797 records → 4,247 dedup → 3,985 reviewed → 2,352 after non-"prompt" removal → 1,565 in qualitative synthesis). Embedded in §1.
- `eval_strategies.png` (from MHTML image index 1, source URL `…/extracted/6236072/assets/eval_strategies.png`, 482 KB) — the 2×2×2 grid of do/don't exemplar-selection diagrams for Few-Shot prompting. Embedded in §6.
- `dspy-bar-chart.png` (from MHTML image index 2, source URL `…/x12.png`, 207 KB; aliased as `x4.png` in the brief but located at `x12.png` in the v6 render) — bar chart of F1/Recall/Precision across 10-Shot AutoDiCoT / 20-Shot AutoDiCoT / DSPy Default / DSPy + Small Modifications. Embedded in §6.

---

## Sources reviewed

| Source ID | Citation | URL | Status | Notes |
|---|---|---|---|---|
| S-Schulhoff | Schulhoff, S., Ilie, M., Balepur, N., Kahadze, K., Liu, A., Si, C., Li, Y., Gupta, A., Han, H., Schulhoff, S. *et al.* *The Prompt Report: A Systematic Survey of Prompt Engineering Techniques.* arXiv:2406.06608v6 (originally posted June 2024; v6 Feb 2025). 76 pages. | https://arxiv.org/html/2406.06608v6 | ✅ FULL | Primary MHTML capture drained 2026-05-16 from `research/manual/`. Body text extracted (310k chars); three diagrams extracted into `figures/29-prompt-engineering-survey/`. PRISMA-style meta-analysis of 1,565 prompt-engineering papers; the paper itself reports a v1 release in June 2024 with iterations through v6. Co-authored at the University of Maryland (Schulhoff is the founder of *Learn Prompting*). |

---

## 1. What the survey is — PRISMA, 1,565 papers, 58 techniques

Schulhoff et al.'s *Prompt Report* is the largest primary meta-analysis of prompt engineering currently in print. It applies the **PRISMA** (Preferred Reporting Items for Systematic Reviews and Meta-Analyses; Page et al., 2021) literature-review methodology to a population of prompt-engineering papers mined from arXiv, Semantic Scholar, and the ACL Anthology, queried with 44 prompt-related keywords. The pipeline:

![PRISMA-style screening pipeline: 3,677 records from arXiv + 2,087 from Semantic Scholar + 1,058 from ACL = 4,797 → 4,247 after title de-duplication → 3,985 papers human-reviewed → 2,352 after removing papers that don't contain "prompt" → 1,565 records in qualitative synthesis. A parallel LLM-review track validates the human screen with 89% precision / 75% recall (81% F1).](figures/29-prompt-engineering-survey/prisma-pipeline.png)

*Caption: PRISMA pipeline (Schulhoff et al., Figure 2.1). The figure surfaces two non-abstract details: (a) the LLM-screen track was **validated against 100 ground-truth annotations** at 89% precision / 75% recall / 81% F1 before being used to triage the dataset; (b) the final 1,565 papers are the union of the human and the LLM annotations, not the intersection — the survey treats the LLM as a labour-multiplier on the screen, not as a gate.*

Headline numbers (Schulhoff et al., §2.1.1, verbatim where quoted):

- **4,797** initial records (3,677 arXiv + 2,087 Semantic Scholar + 1,058 ACL).
- **4,247** after title de-duplication.
- **3,985** papers human-reviewed; **2,352** after removing papers that don't contain "prompt" (the keyword catches false positives — papers that use "prompt" only in passing).
- **1,565** papers in qualitative synthesis ("The combined human and LLM annotations generate a final set of 1,565 papers").
- **58** text-based prompting techniques, organized into **6 major categories** (§2.2.1 — §2.2.5 plus a top-level Zero-Shot branch).
- **44** keywords used to query the three source databases (listed in Appendix A.4).

The survey is the academic counterpart to the corpus' practitioner discussion: it gives a single citation for nearly every prompt-engineering technique the corpus already names (Few-Shot, Chain-of-Thought, Self-Consistency, Tree-of-Thought, Step-Back, Self-Refine, Plan-and-Solve, …) and one canonical taxonomy of where each technique fits.

**A non-obvious methodological choice.** Schulhoff et al. (§2.1) deliberately limit scope to *discrete, text-based, prefix prompts* (the kind of prompt a practitioner can type into the chat box). Continuous prompts (prompt-tuning / soft prompts), prompts that require fine-tuning, and prompts on non-LM modalities are deferred to §3 (Multilingual) and §4 (Multimodal + Agent) extensions. The corpus' load-bearing concern is the discrete-prefix-prompt slice, so the survey's main taxonomy is the right anchor.

---

## 2. The 58-technique taxonomy — six families

Schulhoff et al. (§2.2, Figure 2.2) organize all 58 text-based techniques into six families. The naming differs slightly between the prose and the figure — the prose lists ICL (Few-Shot + Zero-Shot), Thought Generation, Decomposition, Ensembling, and Self-Criticism; the figure splits Zero-Shot out as its own top-level branch parallel to Few-Shot under ICL. I follow the prose grouping below and note Zero-Shot's status explicitly.

### 2.1 In-Context Learning (ICL) — Zero-Shot + Few-Shot

ICL is the umbrella for any prompting technique that teaches a task via the prompt itself, without weight updates. Schulhoff et al. (§2.2.1, verbatim): *"ICL refers to the ability of GenAIs to learn skills and tasks by providing them with exemplars and or relevant instructions within the prompt, without the need for weight updates/retraining."* The survey emphasizes a subtle point that the corpus has not yet anchored: *"Note that the word 'learn' is misleading. ICL can simply be task specification — the skills are not necessarily new, and can have already been included in the training data."*

Zero-Shot members (Figure 2.2): **Emotion Prompting**, **Role Prompting**, **Style Prompting**, **S2A** (System 2 Attention), **SimToM** (Simulation Theory of Mind), **RaR** (Rephrase and Respond), **RE2** (Re-reading), **Self-Ask**. One-sentence definitions: Emotion / Role / Style add an affective, persona-, or stylistic frame; S2A and SimToM ask the model to first filter or simulate another viewpoint; RaR and RE2 ask the model to either rephrase or re-read the prompt before answering; Self-Ask interpolates self-generated sub-questions before answering.

Few-Shot members + design dimensions (§2.2.1.1): **SG-ICL** (Self-Generated In-Context Learning), **KNN** and **Vote-K** exemplar selection, **Prompt Mining**, plus the six design decisions (Exemplar Quantity, Ordering, Label Distribution, Label Quality, Format, Similarity) that govern how exemplars are chosen and ordered. One verbatim finding from §2.2.1.1: *"On some tasks, exemplar order can cause accuracy to vary from sub-50% to 90%+"* — a quantitative anchor for the corpus' "prompt sensitivity is non-trivial" intuition.

### 2.2 Thought Generation — Chain-of-Thought and its descendants

The Chain-of-Thought (CoT) family asks the model to emit explicit reasoning before its answer. Schulhoff et al. divide it into Zero-Shot CoT (no exemplars; the "let's think step by step" pattern) and Few-Shot CoT (exemplars include reasoning traces).

Zero-Shot CoT members: **Analogical Prompting**, **Step-Back Prompting**, **Thread-of-Thought (ThoT)**, **Tab-CoT**. Few-Shot CoT members: **Active-Prompt**, **Auto-CoT**, **Complexity-Based**, **Contrastive**, **Memory-of-Thought**, **Uncertainty-Routed CoT**, **AutoDiCoT** (Automatic Directed CoT). One-sentence definitions: Step-Back abstracts the question one level before answering; Tab-CoT formats reasoning as a table; Auto-CoT bootstraps its own reasoning exemplars; Contrastive shows the model good *and bad* reasoning; AutoDiCoT (the survey's own case-study technique) automatically generates CoTs but also shows examples of *bad* reasoning to steer the model away from a known failure mode.

### 2.3 Decomposition — make the problem smaller

Schulhoff et al. (§2.2.3, verbatim): *"Significant research has focused on decomposing complex problems into simpler sub-questions … some decomposition techniques are similar to thought-inducing techniques, such as CoT, which often naturally breaks down problems into simpler components. However, explicitly breaking down problems can further improve LLMs' problem solving ability."*

Members: **DECOMP**, **Faithful CoT**, **Least-to-Most**, **Plan-and-Solve**, **Program-of-Thought**, **Recursion-of-Thought**, **Skeleton-of-Thought**, **Tree-of-Thought (ToT)**, **Metacognitive Prompting**. One-sentence definitions: Plan-and-Solve emits a plan first then executes it; Program-of-Thought offloads computation to a code interpreter; Tree-of-Thought explores reasoning as a search tree; Skeleton-of-Thought generates a skeleton, then fills each section in parallel; Least-to-Most builds up from sub-problems. Decomposition is the academic spine of every corpus pattern that uses a *planner → coder → reviewer* split — including Cherny's plan-mode (followup/03 §2), Claude Code's `/plan` slash command (report 05 §6), and the Foundry phase-gate architecture (`architectures/04-foundry.md`).

### 2.4 Ensembling — multiple prompts, majority vote

Schulhoff et al. (§2.2.4, verbatim): *"In GenAI, ensembling is the process of using multiple prompts to solve the same problem, then aggregating these responses into a final output. In many cases, a majority vote — selecting the most frequent response — is used to generate the final output. Ensembling techniques reduce the variance of LLM outputs and often improving accuracy, but come with the cost of increasing the number of model calls needed to reach a final answer."*

Members: **COSP** (Consistency-based Self-adaptive Prompting), **DENSE** (Demonstration Ensembling), **DiVeRSe**, **Max Mutual Information**, **Meta-CoT**, **MoRE** (Mixture of Reasoning Experts), **Self-Consistency**, **Universal Self-Consistency**, **USP** (Universal Self-adaptive Prompting), **Prompt Paraphrasing**. Ensembling is the academic counterpart to AlphaCode's cluster-by-behavior consensus filter (report 22 §2 verbatim: *"selecting one solution from each cluster from largest to smallest performed best"*) and to the Atelier architecture's reviewer panel.

### 2.5 Self-Criticism — let the model judge its own work

Schulhoff et al. (§2.2.5, verbatim): *"When creating GenAI systems, it can be useful to have LLMs criticize their own outputs … This could simply be a judgement (e.g., is this output correct) or the LLM could be prompted to provide feedback, which is then used to improve the answer."*

Members: **Chain-of-Verification**, **Self-Calibration**, **Self-Refine**, **Self-Verification**, **ReverseCoT**, **Cumulative Reasoning**. Self-Criticism is the academic anchor for every "code-review-as-prompt" pattern in the corpus — Cherny's Claude-reviews-100%-of-Anthropic-PRs (followup/03), CJ Hess's `carl` GPT-5.2-Codex curmudgeonly-staff-engineer second-pass (cluster N), and Schillace's "Crusty Old Engineer" critic role in Amplifier (report 28 §3).

### 2.6 The five-vs-six question

The taxonomy is "6 major categories" in the prose abstract (Schulhoff et al., §1, verbatim: *"identify 58 different text-based prompting techniques … broken into 6 major categories"*) but Figure 2.2 enumerates five families plus a top-level Zero-Shot branch. The reconciliation: Zero-Shot is both a member of ICL (under §2.2.1) and its own top-level prompt-engineering pattern (because it's the limit case of ICL with zero exemplars). Practitioners reading the taxonomy should think of it as five technique families plus the "no-exemplars-at-all" zero-th case.

---

## 3. The extensions catalogue — beyond text-only single-shot

Schulhoff et al. extend the 58-technique taxonomy along four axes in §§3–4. Each extension surfaces a sub-taxonomy that anchors a distinct corpus thread:

**§3 Multilingual prompting.** Covers Cross-Lingual In-Context Learning (CLICL), Chain-of-Translation, Cross-Lingual Self-Consistency, and the open question of whether English-only prompting templates degrade non-English-language outputs. Directly anchors the El Kaim 9-field-intent block's explicit `Language` slot (report 14 §6) and the Tencent Elixir-completion-rate benchmark question raised in cluster M (`The Software Factory: When AI Agents Write Your Code, Does Language Choice Matter?`).

**§4 Multimodal prompting.** Image, audio, video, segmentation, and 3D-input prompting techniques. The taxonomy notes that text-prompting techniques transfer asymmetrically — e.g. Chain-of-Thought generalises to image-CoT, but Few-Shot exemplar-selection design decisions (§2.2.1.1) get more constrained because exemplar tokens are large.

**§4 Agent prompting.** Schulhoff et al. taxonomize agent prompting into four sub-families:

- **Tool-Use agents** — prompting patterns for retrieve / search / call-API tools (PAL, ART, MM-ReAct, Toolformer).
- **Code-Generation agents** — patterns for sandboxed code execution; includes Program-of-Thought + Program-Aided Language Models, with explicit framing that the *code is the action*. Direct anchor for SWE-agent (report 22 §5) and Codex (report 18).
- **Observation-based agents** — the ReAct family (Reason + Act) including Reflexion (verbal self-feedback) and Voyager (long-horizon Minecraft agent). Schulhoff highlights GITM (Zhu et al., 2023), which *"starts with an arbitrary goal, breaks it down into subgoals recursively, then iteratively plans and executes actions by producing structured text (e.g. 'equip(sword)') rather than writing code."* This is the academic predecessor of Shapiro's Claw (report 32) — "memory + goals + autonomy" — at the prompt level.
- **Retrieval-Augmented Generation (RAG)** — verifier-RAG, FLARE, IRCoT, GenRead. Anchors the corpus' AGENTS.md + Spec retrieval thread (report 05, followup/11).

**§4.2 LLM-as-Judge evaluation prompting.** The survey gives the corpus' first systematic LLM-as-judge catalogue. See §5 below.

This extensions catalogue is the structural reason this report does *not* fold into report 26 (prompt under-specification): it is broader than the under-specification slice. It directly anchors:

- **Report 22 §4** (SWE-bench evaluation) — the Code-Generation + Tool-Use agent sub-families are the academic taxonomy that SWE-bench, SWE-agent, and Codex instantiate.
- **followup/07-evals-deepdive** (LLM-as-judge) — §4.2 is the academic catalogue (see §5 below).
- **followup/08-security-primitives** (prompt injection / jailbreaking) — see §4 below.
- **Report 26** (prompt under-specification academic) — Schulhoff et al. independently surface the same brittleness phenomenon (§2.2.1.1 exemplar-order swings; §5 prompt sensitivity).

---

## 4. §5 Prompting Issues — the failure-mode taxonomy

Schulhoff et al. close (§5) with a "Prompting Issues" section that is, in effect, a failure-mode taxonomy of the discipline. Five families:

### 4.1 Prompt hacking — prompt injection + jailbreaking

Verbatim (§5.1): *"Prompt hacking refers to a class of attacks which manipulate the prompt in order to attack a GenAI. Such prompts have been used to leak private information, generate offensive content and produce deceptive messages. Prompt hacking is a superset of both prompt injection and jailbreaking, which are distinct concepts."* The survey adopts Schulhoff's own 2023 framing: **prompt injection** is the *cross-trust-boundary* case (developer instructions injected by user content); **jailbreaking** is the *single-trust* case (user attacks the model directly without crossing a developer's prompt template).

The §5.1 catalogue covers: defense-via-prompt-instruction (Schulhoff 2022), input-classifier defenses, output-filter defenses, and the survey's bottom-line conclusion (verbatim): *"prompt hacking (both injection and jailbreaking) remain unsolved problems and likely are impossible to solve entirely."* The survey also surfaces a real-world enforcement precedent (verbatim): *"Garcia (2024) describe how an airline chatbot gave a customer incorrect information about refunds. The customer appealed in court and won."* This is the academic counterpart to the lethal-trifecta primary (followup/08 §1) and the CaMeL paper-body (followup/08 §3).

### 4.2 Prompt sensitivity

The survey acknowledges (§5) that *"these systems are being cajoled, not programmed, and, in addition to being quite sensitive to the specific LLM being used, they can be incredibly sensitive to specific details in prompts without there being any obvious reason those details should matter."* The §2.2.1.1 finding — *"exemplar order can cause accuracy to vary from sub-50% to 90%+"* — is the quantitative anchor.

### 4.3 Sycophancy

Verbatim (§5): *"sycophancy refers to the concept that LLMs will often express agreement with the user, even when that view contradicts the model's own initial output."* Sharma et al. (2023) find that *"questioning the LLM's original answer (e.g. 'Are you sure?'), strongly providing an assessment of correctness (e.g. 'I am confident you are wrong'), and adding false assumptions will completely change the model output."* A non-obvious operational caveat the survey raises (verbatim): *"a practitioner may use the prompt template 'Detect all instances where the user's input is harmful: {INPUT}' in an attempt to prevent adversarial inputs, but this subtly makes the false presupposition that the user's input is actually harmful. Thus, due to sycophancy, the LLM may be inclined to classify the user's output as harmful."* This is a direct contradiction to several "wrap the prompt in a security check" patterns the corpus has discussed.

### 4.4 Bias

The survey catalogues empirical work showing that exemplar selection, label distribution (§2.2.1.1 Exemplar Label Distribution), and demographic framings systematically bias model outputs. The §2.2.1.1 verbatim finding — *"if 10 exemplars from one class and 2 exemplars of another class are included, this may cause the model to be biased toward the first class"* — is the quantitative anchor.

### 4.5 Ambiguity / under-specification

The survey identifies ambiguity in prompts as a load-bearing failure mode but does not catalogue it as comprehensively as Yang et al. (arXiv:2505.13360v3) does in report 26. Schulhoff et al. instead treat it as orthogonal to the discrete-prompt taxonomy and refer readers to follow-up empirical work (e.g. §6 case study, where ambiguity in the *labeling task* manifests as an F1 ceiling — see §6 below).

### 4.6 Cross-references into the corpus

- **followup/08-security-primitives §1 (lethal trifecta) + §3 (CaMeL):** §5.1 is the academic taxonomy that the practitioner-grade lethal-trifecta and CaMeL work fits inside. Schulhoff et al.'s framing that prompt hacking *"likely are impossible to solve entirely"* is the academic counterpart to Willison's "97% is a failing grade" doctrine (report 05).
- **Report 26 (prompt under-specification academic):** §4.5 ambiguity / under-specification is Schulhoff et al.'s minimal pointer; report 26 (Yang et al.; Norheim et al.; Larbi et al.) is the empirical deep dive.

---

## 5. LLM-as-judge — the §4.2 evaluation-prompting catalogue

Schulhoff et al. (§4.2) catalogue LLM-as-judge evaluation prompting under the Agent extension. The catalogue is the first published systematic enumeration of judge patterns and is the academic anchor for followup/07-evals-deepdive's Hamel-Husain-Anthropic Critique-Shadowing thread.

The catalogue covers:

- **Single-output judging** — score a single output on a rubric (the simplest binary or Likert pattern).
- **Pairwise judging** — choose better of two outputs (the pattern most LLM-arena leaderboards use).
- **Reference-based judging** — score relative to a gold-standard reference (the Critique-Shadowing pattern in followup/07 §3.9).
- **Self-judging** — overlap with Self-Criticism §2.2.5 (the model judges its own output; the survey notes the obvious sycophancy risk).
- **Multi-criterion judging** — decompose the rubric into binary-per-acceptance-criterion (the pattern Husain & Shankar endorse in followup/07 §3).

The survey closes with the same caveat the corpus already names — judge prompts are themselves prone to the §5.1 prompt-hacking issues and the §5.2 sensitivity issues, so they must be evaluated against ground truth before deployment. (Schulhoff et al., §2.1.1 verbatim: *"We validate the prompt against 100 ground-truth annotations, achieving 89% precision and 75% recall (for an F₁ of 81%)."* — their *own* LLM-screen judge was calibrated against human labels before use; this is the methodological recommendation they implicitly make for every judge prompt.)

---

## 6. The DSPy case study — same model, different harness, different result

Schulhoff et al.'s §6 is a 47-step / 20-hour prompt-engineering case study on a real-world entrapment-detection task, ending with a head-to-head against the **DSPy** automatic prompt-optimization framework (Khattab et al., 2023). The case study is the survey's central empirical contribution and is the academic vindication of Theme-6 (harness engineering): given the same model, the same task, and the same metric, the *harness* (manual vs DSPy-optimized prompt) is the leverage point.

### 6.1 The Few-Shot design-decision pictogram

![A 2-by-2-by-2 grid of Few-Shot exemplar-selection design choices, with green check-marks for the recommended pattern in each pair and red X for the dis-recommended counterpart. Top row: 'Include as many exemplars as possible' (4 items vs 1 item) and 'Randomly order exemplars' (varied order vs all positives clumped). Middle row: 'Provide a balanced label distribution' (alternating labels vs skewed) and 'Ensure exemplars are labeled correctly' (correct vs swapped). Bottom row: 'Choose a common format' (Im:Label vs equals-separated noise) and 'Select similar exemplars to the test instance' (matched-style exemplars vs mismatched-style).](figures/29-prompt-engineering-survey/eval_strategies.png)

*Caption: Figure 2.3 (Schulhoff et al.). Six Few-Shot design decisions, each rendered as a do/don't pictogram. The asterisk on every header reads (verbatim): "Please note that recommendations here do not generalize to all tasks; in some cases, each of them could hurt performance." This is the survey's quiet acknowledgement that the discipline is empirical, not deductive — even its own canonical recommendations are tuning-set-dependent.*

The pictogram is the visual the §6 case study walks the reader through — each of the 47 prompt-engineering steps in the entrapment-detection task is, in effect, a single experiment along one or more of these axes.

### 6.2 The case-study trajectory

A condensed narrative (Schulhoff et al., §6.2.3, verbatim where quoted):

> "The exercise proceeded through 47 recorded development steps, cumulatively about 20 hours of work. From a cold start with 0% performance (the prompt wouldn't return properly structured responses), performance was boosted to an F1 of 0.53, where that F1 is the harmonic mean of 0.86 precision and 0.38 recall."

The trajectory reveals the *messiness* of manual prompt engineering. Several non-obvious findings the survey records (paraphrased + direct quotes):

- A duplicated email pasted in by accident *improved* performance; *removing the duplicate decreased it.* The author was unable to explain why.
- Anonymizing the email (replacing names with random names) *decreased* performance by 0.08 F1 — a surprising sycophancy-adjacent or training-distribution-adjacent effect.
- Switching from "Q/R/A" abbreviations to "Question/Reasoning/Answer" full words *decreased* F1 by 0.05.
- Adding a 20th-shot exemplar *worsened* test-set performance vs the 10-shot version — confirming the §2.2.1.1 Exemplar Quantity claim that "benefits may diminish beyond 20 exemplars."

The §6 take-aways (Schulhoff et al., verbatim, §6.2.4): *"these systems are being cajoled, not programmed, and, in addition to being quite sensitive to the specific LLM being used, they can be incredibly sensitive to specific details in prompts without there being any obvious reason those details should matter."*

### 6.3 DSPy vs the human prompt engineer

Schulhoff et al. (§6.2.3.3 DSPy, verbatim):

> "We concluded the case study by exploring an alternative to manual prompt engineering, the DSPy framework (Khattab et al., 2023), which automatically optimizes LLM prompts for a given target metric. … Over 16 iterations, DSPy bootstrapped synthetic LLM-generated demonstrations and randomly sampled training exemplars, with the ultimate objective of maximizing F1 on the same development set used above. … The best resulting prompt includes 15 exemplars (without CoT reasoning) and one bootstrapped reasoning demonstration. It achieves 0.548 F1 (and 0.385 / 0.952 precision / recall) on the test set, **without making any use of the professor's email nor the incorrect instruction about the explicitness of entrapment**. It also performs much better than the human prompt engineer's prompts on the test set, which demonstrates the significant promise of automated prompt engineering."

![Bar chart titled "Scores of Different Prompting Techniques on Test Set" showing F1 (dark navy), Recall (teal), Precision (light teal) for four prompting techniques: 10-Shot AutoDiCoT (F1 ~0.35, Recall ~0.70, Precision ~0.22), 20-Shot AutoDiCoT (F1 ~0.25, Recall ~0.80, Precision ~0.15), DSPy Default (F1 ~0.50, Recall ~0.65, Precision ~0.40), DSPy Default + Small Modifications (F1 ~0.55, Recall ~0.95, Precision ~0.38).](figures/29-prompt-engineering-survey/dspy-bar-chart.png)

*Caption: Figure 6.19 (Schulhoff et al.). DSPy + small modifications (rightmost cluster) beats both the 10-shot and 20-shot hand-crafted AutoDiCoT prompts on F1 and on Recall, despite the human prompt engineer having spent 20 hours over 47 steps on the manual versions. Two findings worth surfacing: (a) DSPy chose **15 exemplars without CoT reasoning + 1 bootstrapped reasoning demonstration** — a non-obvious mix that violates the "include CoT reasoning in exemplars" heuristic; (b) DSPy did not use **the professor's email or the incorrect explicitness instruction** that the manual prompts depended on for their best F1 — the automated optimizer simply avoided the brittle scaffolding the human had built.*

### 6.4 Theme-6 interpretation

The DSPy case study is the academic instantiation of Theme-6 (harness engineering): **same model, different harness, different result.** Specifically:

- The model is gpt-4-0125-preview throughout (DSPy default).
- The task and metric are identical (entrapment-detection F1 on a held-out test set).
- The only difference is the *harness*: a 20-hour human-driven prompt-engineering loop vs a 16-iteration DSPy optimization with `BootstrapFewShotWithRandomSearch`.
- DSPy + small modifications scores 0.548 F1 (test set) vs the human's best 0.53 F1 (development set) → a ≥0.02-F1 lift, but the more important finding is that DSPy *generalised better* — the human's prompt was overfit to a duplicated email and an incorrect instruction that the optimizer discarded.

This is the strongest empirical evidence in the corpus that the leverage point is the harness around the model, not the model itself — directly aligned with Schillace's "harness engineering" thesis (report 28), the OpenAI Codex / harness-engineering primary (report 18 §5), and the mini-SWE-agent simplicity argument (report 22 §5).

The survey's own §6.2.4 closing note (verbatim) caveats the result: *"there was significant promise in an automated method for exploring the prompting space, but also that combining that automation with human prompt engineering/revision was the most successful approach."* DSPy is not a replacement for the human; it is the leverage layer that finds the regions the human should explore.

---

## 7. Cross-corpus impact — the 58-technique taxonomy mapped onto existing reports

The Schulhoff taxonomy is the academic spine the corpus has been writing around without naming. The table below maps each major category and a representative technique onto the corpus reports that already discuss the pattern under a different name:

| Schulhoff family | Representative technique | Corpus appearance |
|---|---|---|
| ICL — Zero-Shot | **Role Prompting** (§2.2.1.3) | Anthropic's prompt-engineering posts (report 23 §3, "be the persona") — Anthropic's "role" framing is Schulhoff §2.2.1.3 verbatim. El Kaim's 9-field intent block (report 14 §6, `Persona`) — explicit field. |
| ICL — Few-Shot | **Exemplar Quantity / Ordering** design decisions (§2.2.1.1) | Anthropic engineering trilogy (report 23 §2 on n-shot prompting). Willison's prompt-injection essays (report 05 §4) treat exemplar choice as a side-channel for injection. |
| Thought Generation | **Plan-mode / Step-Back / CoT** (§2.2.2) | Cherny's plan-mode (followup/03 §2) is Step-Back + Decomposition. Anthropic's extended-thinking (followup/03 §2.4, report 23 §4) is Zero-Shot CoT operationalized at the SDK level. Schillace's "pressure-test the plan" (report 28 §8) is Self-Verification on a Plan-and-Solve output. |
| Decomposition | **Plan-and-Solve / Tree-of-Thought / Skeleton-of-Thought** (§2.2.3) | The Foundry phase-gate architecture (architectures/04). The El Kaim 9-field intent block decomposes intent into Persona / Goal / Outcome / Constraints / Inputs / Dependencies / Risks / Acceptance / Owner (report 14 + report 25 §3). |
| Ensembling | **Self-Consistency / Universal Self-Consistency** (§2.2.4) | AlphaCode's cluster-by-behavior (report 22 §2 §4.6). The Atelier reviewer-panel architecture. StrongDM's "satisfaction score" (report 01) as an ensembling-of-rubric-judges pattern. |
| Self-Criticism | **Self-Refine / Chain-of-Verification** (§2.2.5) | Cherny's "Claude reviews 100% of Anthropic PRs" (followup/03 §3). CJ Hess's `carl` (GPT-5.2 Codex curmudgeonly staff engineer; cluster N). Schillace's "Crusty Old Engineer" critic role in Amplifier (report 28 §3). |
| Agent — Tool-Use | **PAL / ART / Toolformer** (§4 Agent) | SWE-agent ACI (report 22 §5). Codex tool-use (report 18 §3). MCP universally (multiple reports). |
| Agent — Code-Gen | **Program-of-Thought / Code-as-Action** (§4 Agent) | SWE-agent + Codex (reports 22, 18). The Foundry phase-gate's "implement" gate. |
| Agent — Observation-based | **ReAct / Reflexion / Voyager** (§4 Agent) | OpenHands' agent loop (report 11). mini-SWE-agent linear-history loop (report 22 §5). |
| Agent — RAG | **FLARE / IRCoT / GenRead** (§4 Agent) | AGENTS.md + Spec retrieval thread (report 05 §3). Compound Knowledge plugin (followup/11). |
| LLM-as-Judge | **Reference-based / Pairwise / Multi-criterion** (§4.2) | Hamel Critique-Shadowing (followup/07 §3.9). Husain & Shankar binary-per-AC pattern (followup/07 §3). El Kaim's `EvaluationSuite` with `protects: RULE-ID` linkage (report 14, report 25). |
| §5.1 Prompt-hacking | Injection / Jailbreaking | Willison's lethal trifecta + Dual LLM (followup/08 §1, §2). CaMeL paper body (followup/08 §3). |
| §5 Sensitivity | Exemplar-order swings 50%→90%+ (§2.2.1.1) | Yang et al.'s Pass@1 98.7%→85.0% under spec growth (report 26 §3). Larbi et al.'s GPT-4 Pass@1 73.8%→6.7% on contradictory prompts (report 26 §4). |
| §5 Sycophancy | "Are you sure?" → flipped output | Willison's "97% is a failing grade" doctrine (report 05). Schillace's "marshmallow test" framing (report 28 §5). |

The table is the structural argument for treating this report as the corpus' academic spine: nearly every prompt-engineering pattern the corpus already discusses sits inside one of Schulhoff et al.'s six families, and naming it explicitly gives every future report a single citation to anchor on.

---

## 8. Open questions

1. **Robustness of prompt-engineering effects.** The §6 case study shows that a 20-hour human-driven prompt engineering exercise produces F1 = 0.53 with a brittle scaffold (duplicated email, incorrect instruction); DSPy + small modifications produces F1 = 0.548 with a clean scaffold and *better generalisation*. Open question: does this result generalise beyond the entrapment-detection task to (a) software-engineering tasks like SWE-bench, (b) agentic tool-use, (c) multi-turn conversations? If yes, the corpus' practitioner-side advocacy of hand-crafted prompts (report 05 §"AGENTS.md craft", report 14 9-field intent block) needs a Theme-6 caveat: hand-crafted prompts may be over-fit; auto-optimised prompts may generalise better.

2. **Coverage of agent vs single-shot.** The 58-technique taxonomy is text-based single-shot; the agent extensions in §4 are catalogued more lightly. Open question: how many of the 58 techniques carry over to multi-turn agent loops, and how many fail (because, e.g., exemplar-ordering interacts badly with conversational state)? This is the natural follow-up survey.

3. **The 1,565 → 58 compression rate.** The PRISMA pipeline compresses 1,565 papers into 58 techniques — a 27:1 compression. Open question: are the 1,507 papers not represented as named techniques *redundant* (multiple papers proposing the same technique) or *novel-but-niche* (proposing techniques the survey deemed too narrow to taxonomize)? The Schulhoff team have released the dataset on HuggingFace (`PromptSystematicReview/Prompt_Systematic_Review_Dataset`) — a future drain could audit the compression.

4. **Calibration drift in the LLM-screen track.** The PRISMA pipeline validates the LLM-screen prompt at 89% precision / 75% recall against 100 ground-truth annotations. Open question: does that calibration hold as the screen scales from 100 to 3,985 papers, or does the precision-recall trade drift on out-of-distribution prompts (e.g. papers using "prompt" in a non-LM sense)? This is the practical instantiation of the corpus' "judge prompts must be evaluated" rule (§5 above).

5. **Failure-mode catalogue alignment.** Schulhoff §5 names five issue families (prompt-hacking, sensitivity, sycophancy, bias, ambiguity); the corpus has F1–F44 + several proposed F-modes from reports 25/26/28/30/31/32. Open question: which Schulhoff issues map onto which F-mode? A first-pass mapping: §5.1 prompt-hacking ↔ F12 (lethal trifecta); §5 sensitivity ↔ F36 (instruction-following ceiling, report 26); §5 sycophancy ↔ F44 (lethal-trifecta production-scissors default, report 32); §5 ambiguity ↔ F37 (silent contradictory-prompt collapse) + F41 (under-defined-intent debt). A clean tabular F-mode-to-Schulhoff-issue alignment is a candidate next-pass synthesis task.

6. **Does the Few-Shot design-decision pictogram (Figure 2.3) generalise to agent loops?** The §6.1 pictogram is the survey's most-reproduced visual but is single-shot-only. Open question: do the same six design decisions (Quantity, Ordering, Label Distribution, Label Quality, Format, Similarity) govern multi-turn exemplar choice in agent loops, or do new decisions (turn-ordering, tool-call exemplars, observation-format) dominate?

---

## 9. Sources

| Source | Citation | URL | Status | Notes |
|---|---|---|---|---|
| S-Schulhoff | Schulhoff et al. *The Prompt Report: A Systematic Survey of Prompt Engineering Techniques.* arXiv:2406.06608v6 (originally June 2024; v6 Feb 2025). 76 pages. | https://arxiv.org/html/2406.06608v6 | ✅ FULL | Primary MHTML capture from `research/manual/The Prompt Report_ A Systematic Survey of Prompt Engineering Techniques.mhtml` drained 2026-05-16. Body text extracted (310k chars). Three diagrams extracted into `figures/29-prompt-engineering-survey/`: `prisma-pipeline.png` (§1), `eval_strategies.png` (§6.1), `dspy-bar-chart.png` (§6.3). Co-authored across the University of Maryland (Schulhoff is founder of Learn Prompting) and a multi-institution team. PRISMA-style meta-analysis of 1,565 prompt-engineering papers (4,797 initial records). |

---

**Word count (approximate):** ~5,200 words.

**Cross-references in this report:**

- Anchors **followup/07-evals-deepdive** at the LLM-as-judge layer (§5 above, mapping into followup/07 §3).
- Anchors **followup/08-security-primitives** at the prompt-injection / jailbreaking taxonomy layer (§4 above, mapping into followup/08 §1 + §3).
- Cross-referenced from **report 22 §4** (SWE-bench evaluation; Code-Generation + Tool-Use agent sub-families).
- Cross-referenced from **report 23** (Anthropic engineering trilogy; Role / Few-Shot / Step-Back).
- Cross-referenced from **report 26** (prompt under-specification academic; §5 ambiguity is Schulhoff's minimal pointer, report 26 is the empirical deep-dive).
- Cross-referenced from **followup/03** (Cherny interview; plan-mode = Step-Back + Decomposition).
- Cross-referenced from **report 28** (Schillace; pressure-test-the-plan = Self-Verification on Plan-and-Solve).
- Cross-referenced from **report 32** (Shapiro Claw; §4 Observation-based GITM is the academic predecessor of the autonomy-with-memory pattern).
