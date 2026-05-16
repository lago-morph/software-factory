# Language Choice as Harness — Research Report

**Status:** 🟡 partial (primary source paywalled past the cut; supporting cross-references ✅)
**Date:** 2026-05-16 (Cluster-M manual drain)
**Primary source:** Allan MacGregor, *"When AI Agents Write Your Code, Does Language Choice Matter?"* — `https://www.thepragmaticcto.com/p/when-ai-agents-write-your-code-does` — Feb 17, 2026; converted-txt at `research/manual/When AI Agents Write Your Code, Does Language Choice Matter_.txt`. Free portion fully drained; paid tail ("The Training Data Problem" onward) is paywalled and flagged for fetch-blocked-urls follow-up.
**Supporting cross-references:** Jose Valim "Why Elixir is the best language for AI" (Feb 5 2026 — cited via MacGregor, not drained primary); Tencent multi-language LLM benchmark (cited via Valim → MacGregor, not drained primary); Alexandru Nedelcu on Scala 3 macros via LSP (cited via MacGregor); Jonathan de Montalembert quote (cited via MacGregor).

---

## Lead question

If an AI agent writes most of your codebase, does the **target programming language** affect the quality, correctness, or governance posture of what comes out? And if it does, is "language choice" a first-class harness-engineering decision — i.e., a knob on the same dashboard as `.rules`, sandbox shape, judge prompts, and `AGENTS.md`?

MacGregor's free-portion answer: **yes**, on structural grounds — the *compiler* of a typed/functional language is itself a free, tireless, first-pass code reviewer that closes the LLM feedback loop tighter than a dynamically-typed runtime can, and stateless/immutable/pure-function shape matches LLMs' own context-window-bounded operational model. The paywalled tail signals a counter-argument — "*In theory, theory and practice are the same. In practice, they are not.*" (Yogi Berra epigraph) — that ecosystem-churn and training-data abundance will dominate in practice.

This report extracts the free-portion thesis, situates it in the corpus' existing harness/governance lattice, and flags the paywalled counter for future drain.

---

## §1 The thesis — language as harness primitive

MacGregor's framing is that the "best language for AI" debate is the new "best language for web dev" tribal war ("the actors change but the plot stays the same"), but underneath the tribalism there is a real structural question:

> "Claude Code, Cursor, Copilot, Devin — these tools are writing 30-80% of new code at many companies right now. If an AI agent is generating most of your codebase, does the target language affect the quality of what comes out?"

His answer reframes Valim's Elixir-specific arguments as a class of **structural properties** that *any* language exhibiting them confers on its AI-generated code:

1. **A type system the compiler can use to reject invalid generated code before a human sees it.**
2. **Immutability / stateless functions / pure-function semantics** that fit the LLM's tokenized, context-window-bounded operational model.
3. **Ecosystem stability** (low churn → consistent training data → fewer deprecated-API hallucinations).
4. **Executable documentation** verified in test suites, which means the *training examples themselves* are more likely correct.

The corpus has been treating prompt design, sandbox shape, `.rules`, and `AGENTS.md` as the levers of harness engineering (reports 18, 23, 27, 28, 29). MacGregor's claim — and this report's framing — is that **target-language selection is on that same lever board**. It is not an aesthetic / cultural / hiring-pool question; it is a *blast-radius* and *feedback-loop-tightness* question that compounds with every other harness choice.

This is corpus-novel. Before this drain, no report treated programming-language choice as a harness primitive. Report 18 §4.3 (Codex `.rules` DSL) and report 27 (dotfile pipelines as product) come closest — both treat *language-rule-like artifacts* (Starlark `prefix_rule(...)`, DOT-graph pipeline blueprints) as durable substrate — but neither names the underlying programming language itself as the substrate. MacGregor's piece does.

---

## §2 The Tencent benchmark — Valim's empirical anchor

MacGregor opens by citing Valim's Feb 5 2026 *"Why Elixir is the best language for AI"* post, which itself anchors on a Tencent benchmark (the Tencent paper URL is **not** in this drain — flagged for primary-source pull; see §9):

> "On February 5th, Jose Valim published a blog post titled 'Why Elixir is the best language for AI.' His argument wasn't hand-waving. He pointed to a Tencent benchmark where **Elixir achieved a 97.5% completion rate across twenty programming languages**; **Claude Opus 4 scored 80.3% on Elixir versus 74.9% for C# and 72.5% for Kotlin**."

Three concrete numbers:

| Metric | Value | Notes |
|---|---|---|
| Elixir completion rate, all-models composite | **97.5%** | Across 20 languages benchmarked |
| Claude Opus 4 — Elixir | **80.3%** | Top of the languages cited |
| Claude Opus 4 — C# | **74.9%** | -5.4 pp vs Elixir |
| Claude Opus 4 — Kotlin | **72.5%** | -7.8 pp vs Elixir |

**Caveat 1 — secondary citation.** Both the Tencent benchmark and Valim's post are cited via MacGregor; neither is in this drain at primary-source level. The numbers may be paraphrased, the Tencent benchmark may have a per-task pass criterion that differs from naive "completion rate" intuition, and the 20-language slate is not enumerated. The numbers should not be treated as load-bearing without primary verification.

**Caveat 2 — model is Claude Opus 4.** The corpus' current default model floor (per reports 06, 32) is Opus 4.6 / Sonnet 4.6 — Opus 4 is **not** the corpus' default. Whether the Opus 4.6 / Sonnet 4.6 numbers replicate the same per-language ordering is an open question (§8).

**Caveat 3 — benchmark task slate.** "Completion rate" alone tells you nothing about the *bug rate of the completed code*. A language could complete more tasks while shipping more silent bugs; conversely, a stricter language could fail more tasks at compile time while shipping fewer bugs through to runtime. The corpus' own framing (e.g. SWE-Bench Verified in report 22) is that benchmark task slate + scoring rule define the result; a Tencent benchmark whose scoring rule is "syntactically valid output that runs without crashing" tells a different story from one scoring "passes a held-out test suite". This is flagged for the primary-source pull.

Even so: a **7.8 pp spread** between the best and worst language for the *same model* is a substantial harness-level effect — comparable in magnitude to the prompt-engineering effects documented in report 26 (Yang et al.'s 98.7%→85.0% Pass@1 collapse as spec count scales 1→19) and report 29 (DSPy's F1 0.548 beating a 20-hour hand-crafted prompt at F1 0.53).

---

## §3 The compiler as AI code reviewer

The load-bearing structural argument is **not** Elixir-specific. MacGregor (verbatim):

> "In languages like Scala, Haskell, or Rust, the feedback loop is tight: AI generates code, the compiler rejects what's invalid, the AI iterates, and eventually produces something correct. The type system catches errors before runtime — without needing a human in the loop. […] An entire category of bugs gets caught before a pull request ever reaches a human reviewer; your engineers spend time on logic and architecture instead of hunting for type mismatches and null reference errors that a compiler would have caught instantly."

This frames the compiler as a **zero-marginal-cost first-pass code reviewer** that:

- Never gets tired.
- Never rubber-stamps a pull request.
- Catches entire categories of bugs deterministically.
- Returns its rejection inside the LLM's iteration loop, not after a human has spent attention on the PR.

**Mapping into the corpus' substrate lattice.** The compiler-as-AI-reviewer pattern is the *language-level* peer of three already-anchored substrate primitives:

| Corpus primitive | Layer | Function |
|---|---|---|
| Codex `.rules` Starlark DSL (report 18 §4.3) | Tool-policy layer | Auditable allow/prompt/forbid + inline `match`/`not_match` unit tests; `codex execpolicy check` CI harness; admin-enforced precedence via `requirements.toml`. Rejects out-of-policy *invocations* before they reach a human. |
| Anthropic auto-review subagent (followup/03 + report 23) | Agent layer | LLM-based reviewer subagent reads the PR diff and gates merge; same "reviewer that doesn't get tired" framing, different substrate. |
| Type system / compiler (this report) | Language layer | Compiler reads the *artifact itself* and rejects type-invalid code; structurally cannot be bypassed by the generating model. |

The compiler reviewer has one property the other two lack: **it is not itself an LLM**, so it is not susceptible to shared-blind-spot hallucination (a known open question for report 01 / report 02 — what happens when judge and coder share a model family). A Haskell compiler will reject `x :: Int` being passed a `String` regardless of whether the LLM that emitted the code "agrees".

Nedelcu's Scala-3 case (cited by MacGregor) sharpens the point. Despite limited training data, AI agents succeed at Scala 3 macros because the compiler provides real-time LSP feedback — "macros emit structured edit commands the LLM can execute precisely". The LSP loop is short enough that the LLM never *ships* the broken macro; it iterates against the compiler until the artifact compiles, and only then is it visible to a human reviewer.

---

## §4 LLM-architecture fit — stateless / immutable / pure functions

MacGregor's second structural argument is that the *shape of the code* matters as much as the type system. LLMs operate under:

- **Limited context windows.** Measured in tokens, not in object graphs.
- **No memory persistence between generations.** Each generation starts fresh.
- **Best output on small, self-described functions** with clear inputs and outputs.

This matches *functional* code shape directly:

- Stateless functions → no hidden state to track between generations.
- Immutable data → all transformations are explicit; the LLM doesn't need to reason about "what changed somewhere else".
- Pure functions → no side effects; the function's behaviour is fully described by its signature.

The contrast (verbatim):

> "Contrast this with mutable object-oriented code. Object state can change anywhere. An AI agent generating a method on a class needs to understand what every other method might have done to that object's state before this method runs. That's a lot of context to track; context that fits poorly in a window measured in tokens. The AI doesn't just need to understand the function it's writing — it needs to understand the entire object graph that function touches. In a large OOP codebase, that graph sprawls across files, modules, and inheritance hierarchies that no context window can fully capture."

**This is a precise context-engineering claim.** It says: *for a fixed model and fixed context window, the same task is structurally easier to complete correctly in a functional codebase than in a sprawling mutable-OOP one*. The harness primitive isn't the language label; it's the *shape of the object graph the function-under-generation must understand*. Languages that force stateless / immutable / pure shape make every generation cheaper to context-load.

**Cross-corpus resonance.** This converges with three corpus threads from different directions:

- **Report 18 §1 (Codex App Server / Thread / Turn / Item primitives).** The Codex harness treats each turn as a self-contained unit; the Thread/Turn structure is itself a functional decomposition of agent state. The OOP-vs-functional argument here applies one level up: the *agent loop* is shaped functionally even when the *code it writes* is not.
- **Report 28 §4 (Schillace's agent-OS building blocks — github/markdown/html/yaml/python/rust/go).** Schillace's list is conspicuously functional-leaning at the data layer (markdown, yaml) and includes rust + go (both have strong type discipline) — but Python is on the list, and OOP-Python is the worst-case shape under MacGregor's argument. Schillace does not address this.
- **Report 29 §6 (DSPy case study — same model, different harness, different result).** MacGregor's argument is *same model, different language, different result*. Both are Theme-6 ("harness dominates model at the margin") evidence; this report extends Theme-6 to the language layer.

---

## §5 The flexible-language hazard — Theme-3 governance

Jonathan de Montalembert's framing (quoted by MacGregor, verbatim):

> "The more flexible and forgiving the target language, the more dangerous the AI partner becomes."

This is a **governance claim**, not a productivity claim. The argument:

- A flexible language (Python, JavaScript, Ruby, dynamically-typed Lisp) **lets the LLM ship more code without compile-time rejection**.
- Most of the rejected-code-from-stricter-languages is rejected *because it was wrong*.
- A flexible language therefore does not make the LLM *less wrong* — it makes the LLM's wrongness *invisible until runtime*, and runtime in agentic systems means production.
- **Wider blast radius for hallucinated code.**

MacGregor:

> "Deterministic languages with sound type systems constrain AI mistakes at compile time. Flexible languages let those mistakes ship."

**This is a Theme-3 (governance / blast-radius) argument that the corpus has not yet anchored at the language layer.** Existing Theme-3 anchors:

- **Willison's Lethal Trifecta** (followup/08) — at the *capability/data* layer.
- **CaMeL typed-interpreter boundary** (followup/08 §3) — at the *runtime/interpreter* layer.
- **Shapiro's five Claw hardening rules R1–R5** (report 32) — at the *integration/API* layer.
- **Codex `.rules` + sandbox + approval matrix** (report 18 §4) — at the *tool-invocation* layer.
- **Cognitive Escrow / interval-as-design-site** (report 30) — at the *attention* layer.

MacGregor / de Montalembert add: **the target programming language is itself a blast-radius lever**. Choosing Python for a high-autonomy Claw — when the same task could be expressed in a typed/functional language — multiplies the surface area through which an LLM's hallucinated code can ship.

This produces the F-mode proposal at the heart of this report (§7).

---

## §6 Counter-argument preview — "The Training Data Problem"

MacGregor's free portion ends at a section header:

> ## The Training Data Problem
> "*In theory, theory and practice are the same. In practice, they are not.*" — Yogi Berra
> The structural argument is sound in theory. In practice, it runs into a wall.

Followed immediately by the paywall:

> *Continue reading this post for free, courtesy of Allan MacGregor.*

The cliffhanger telegraphs the counter-argument: **even if compiler-tightness and functional-shape are structurally favourable, the training-data problem dominates in practice**. The most likely shape of MacGregor's counter:

1. **Training data abundance dominates.** Python/JavaScript have orders of magnitude more public code than Elixir/Haskell/Scala. The LLM's *prior* on what idiomatic code looks like is shaped by whatever language has the most training corpus. A 5–8pp Tencent-benchmark spread may be swamped by the much-larger gap in LLM fluency with the language's idioms, libraries, and gotchas.
2. **Ecosystem churn matters more than ecosystem stability — when the churn happens in the dominant language.** Even if Elixir has been stable since v1.0, Python's NumPy/pandas/SciPy churn happens in the language LLMs already write fluently. The "training data confusion for models navigating deprecated APIs" argument cuts both ways: stable-niche-language vs. churning-dominant-language.
3. **Hiring / runtime / ecosystem-fit constraints.** The choice is not made on harness grounds alone. The team that has to maintain the code after AI shipped it still needs to read it; the production runtime still needs to deploy it; the ecosystem libraries still need to exist.

The paywalled tail is **flagged for fetch-blocked-urls follow-up.** The shape of the counter is the load-bearing missing piece — until it is drained, this report is partial.

---

## §7 Cross-corpus implications

### 7.1 Proposed candidate failure mode — F45

**F45 — Language-as-Harness Mismatch.** *Choosing a permissive / dynamically-typed / mutable-OOP-heavy language for a high-autonomy AI-agent harness multiplies the blast radius of hallucinated code, because the compiler cannot serve as a first-pass reviewer and because object-graph context exceeds what fits in the LLM's window. Symptoms: high "ships and runs once" rate, low "ships and stays correct" rate; failures concentrated at type-system-equivalent boundaries that other languages would have caught at compile time; high engineer-attention spend on review tasks (type mismatches, null derefs) that a stricter language would have foreclosed.*

**Numbering rationale.** F40 / F41 (report 28) and F42 / F43 (reports 30 / 31) and F44 (report 32) are now in play; F45 is the next slot, chosen high to avoid the F36/F37 collision flagged at INDEX.md line 71 between reports 25 and 26.

**Lead-agent triage required** before F45 is canonicalized — the INDEX.md collision note at line 71 already requests reconciliation of the F36/F37 number-collision; F45 should be reconciled in the same pass.

### 7.2 Cross-references into existing corpus reports

| Report / followup | Section | Linkage |
|---|---|---|
| Report 18 (Codex substrate) | §4.3 `.rules` DSL | Tool-policy substrate as a *rule-layer* peer of the language layer; both are "first-pass auto-rejection" surfaces. |
| Report 23 (Anthropic engineering trilogy) | Auto-review subagent | LLM-as-reviewer at the agent layer; type system is its language-layer peer. |
| Report 26 (prompt underspecification academic) | Yang et al. 98.7%→85.0% | Same-model spread driven by *prompts*; this report's Tencent spread is the *language* analogue. Both are Theme-6 evidence. |
| Report 27 (dotfile pipelines as product) | `.dot` as durable artifact | Methodology-layer analogue: choosing the right *blueprint* language (DOT-as-pipeline-DSL) is the methodology-substrate peer of choosing the right *target* language for generated code. |
| Report 28 (Schillace) | §4 agent-OS building blocks | Schillace's list (markdown/yaml/rust/go/python) implicitly takes language positions but does not theorise them; this report supplies the theory. |
| Report 29 (prompt engineering survey) | §6 DSPy case study | Same model, different prompt-engineering harness, F1 0.548 vs 0.53. This report's Opus-4 80.3% Elixir vs 72.5% Kotlin is the language-layer instantiation of the same pattern. |
| Report 32 (Shapiro Claw) | §8.2 F44 / R3 "production scissors" | Permissive language is itself a form of giving the Claw production scissors. F45 specialises F44 to the language layer. |
| Followup/07 (evals deepdive) | §3 LLM-as-judge | Per-language coding benchmarks are a Theme-5 sub-thread; the Tencent benchmark belongs in followup/07's drain inventory. |
| Followup/08 (security primitives) | Lethal Trifecta + CaMeL | The compiler is a *structural* version of the same closure rule CaMeL achieves via typed-interpreter boundaries; de Montalembert's hazard is the language-layer Lethal Trifecta. |

---

## §8 Open questions

1. **Tencent benchmark replication on Opus 4.6 / Sonnet 4.6.** The cited numbers are for Claude Opus 4. The corpus' default model floor (per reports 06, 32) is Opus 4.6 / Sonnet 4.6. Are the per-language spreads stable across model versions? Has the spread *widened* (frontier models continue to specialise toward the higher-training-data languages) or *narrowed* (frontier models close the gap on Elixir-like niche languages)?
2. **Gradually-typed languages — TypeScript, Python+mypy, Python+pyright.** Does the compiler-tightening effect propagate to languages where types are *optional but available*? MacGregor doesn't address this directly; it's the most operationally-relevant question for teams that can't migrate off Python/JavaScript but can adopt type checking. (Anecdotal: the Codex `.rules` DSL is Starlark-based and the OpenAI codebase is heavily TypeScript — report 18 §4.3 — so OpenAI's own answer appears to be "gradually-typed dominant language + strict tool-policy DSL".)
3. **The StrongDM / Attractor ecosystem's language posture.** Smasher = Rust (report 27 + manual corpus). Tracker / Mammoth = Go (manual corpus). Coven = Rust + Go (manual corpus). Kilroy = Go (followup/02). dotpowers = methodology, no native language (report 27). The StrongDM stack is *almost entirely typed-systems languages* — Rust and Go. This may be implicit endorsement of MacGregor's structural argument, or it may be cultural / operational (Rust/Go are the security-infra default), or both. None of the StrongDM canonical pages (per report 01) explicitly theorise language choice; the empirical pattern is suggestive.
4. **MacGregor's paywalled counter-argument body.** What does "The Training Data Problem" specifically say? Does it abandon the structural argument, qualify it, or argue that the structural argument loses when ecosystem-churn / training-data effects are quantified? Until the paywalled tail is drained, this report is partial.
5. **F45 numbering reconciliation.** F45 here, F44 in report 32, F42 / F43 in reports 30 / 31, F40 / F41 in report 28, plus the unresolved F36 / F37 collision between reports 25 and 26. Lead-agent triage pass needed.
6. **Codex `.rules` × language choice composition.** If a team picks Python (permissive) but enforces strict `.rules` policy and a sandbox + approval matrix, do they recover the compiler-as-reviewer effect? Or are the two surfaces orthogonal? (Speculative answer: orthogonal — `.rules` rejects *tool invocations*, the compiler rejects *artifacts*. A Python file with `eval(user_input)` will compile fine but be `.rules`-rejected; a Rust file with `let x: i32 = "hello"` will be compiler-rejected but `.rules`-passed.)

---

## §9 Sources

| Source | URL | Status | Notes |
|---|---|---|---|
| Allan MacGregor — *When AI Agents Write Your Code, Does Language Choice Matter?* | https://www.thepragmaticcto.com/p/when-ai-agents-write-your-code-does | 🟡 partial | Free portion fully drained from `research/manual/When AI Agents Write Your Code, Does Language Choice Matter_.txt` on 2026-05-16; paid tail ("The Training Data Problem" onward) paywalled. **Flagged for fetch-blocked-urls follow-up.** |
| Jose Valim — *Why Elixir is the best language for AI* (Feb 5 2026) | (not in this drain; cited via MacGregor) | ⏳ blocked-on-fetch | Cited as the source of Valim's Elixir-specific arguments + the Tencent benchmark anchor. Primary URL not in MacGregor's text; needs separate discovery. |
| Tencent multi-language LLM benchmark | (not in this drain; cited via Valim → MacGregor) | ⏳ blocked-on-fetch | Cited as the source of the 97.5% / 80.3% / 74.9% / 72.5% numbers. **High priority** — the load-bearing numbers in §2 are currently secondary-citation only. Needs the Tencent paper URL, 20-language slate, per-task scoring rule, and per-model breakdown. |
| Alexandru Nedelcu — Scala 3 macros via LSP | (not in this drain; cited via MacGregor) | ⏳ blocked-on-fetch | Cited as the canonical "LSP closes the loop" exemplar for typed-language AI codegen. Worth a primary drain for the operational details (which LSP server, which macro classes, what the compiler-rejection-rate-vs-iteration-count curve looks like). |
| Jonathan de Montalembert — "the more flexible and forgiving the target language, the more dangerous the AI partner becomes" | (not in this drain; cited via MacGregor) | ⏳ blocked-on-fetch | Single quote; original venue / context not surfaced in MacGregor's piece. Worth tracking the original venue for de Montalembert's full argument shape. |

**Cross-references to corpus reports** (all ✅ primary-anchored): reports 01, 18, 22, 23, 26, 27, 28, 29, 32; followups 02, 07, 08, 10.

---

## §10 Verdict

Programming-language choice is a first-class harness-engineering decision, on the same lever board as `.rules`, sandbox shape, judge prompts, and `AGENTS.md`. MacGregor's structural argument — compiler-as-AI-reviewer + functional-shape fit with LLM operational model + ecosystem stability — is sound on the evidence in the free portion. The corpus has not previously anchored language choice at this level; this report establishes the anchor.

The Tencent benchmark numbers (Elixir 97.5% / Opus-4 80.3% Elixir vs 74.9% C# vs 72.5% Kotlin) are the empirical claim worth verifying against the primary source before being load-bearing. The paywalled counter-argument ("training-data abundance dominates in practice") is the load-bearing missing piece and is flagged for fetch-blocked-urls drain.

**Operational guidance for the corpus' architectures:**

- **Architecture 1 (Specification Refinery) + Architecture 3 (Phase-Gated Foundry):** prefer typed/functional target languages for the *generated artifacts*; the compiler becomes a free V&V layer at the phase gate.
- **Architecture 4 (Evolutionary Tournament):** add a "compile cleanly" fitness component as a zero-marginal-cost first-pass filter before the more expensive judge / human evaluations run.
- **All architectures:** if the target language is permissive (Python, JavaScript) by necessity, compensate at adjacent harness layers — gradual typing (mypy / pyright / TypeScript-strict), strict `.rules`, tighter sandbox, narrower approval matrix. The compiler-reviewer hole has to be filled somewhere.

**Candidate failure mode F45 — Language-as-Harness Mismatch** proposed and flagged for lead-agent triage alongside the existing F36/F37 collision.
