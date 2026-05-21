# 34 — Lenny × How I AI × CJ Hess: Personal Harnesses as the Primary Optimization Surface

**Status:** ✅ FULL
**Date:** 2026-05-16 (Cluster N manual drain)
**Primary sources (2):**
- Claire Vo (Lenny's Newsletter / *How I AI*), *"CJ Hess on Building Custom Dev Tools and Model-vs-Model Code Reviews"* (Feb 9 2026) — `research/manual/How I AI CJ Hess on Building Custom.txt`. CJ Hess identified as a **software engineer at Tenex**.
- Claire Vo (Lenny's Newsletter / *How I AI*), *"Build your own AI developer tools with Claude Code"* — `https://www.lennysnewsletter.com/p/this-week-on-how-i-ai-how-to-build` (drained from `research/manual/lenny-build-your-own-ai-developer-tools-with-claude-code.txt`). CJ Hess introduced **"CJ Hess at 10X"**.
- **Affiliation note.** The two captures name two different employers (Tenex in the *How I AI* show-notes blog; "10X" in the Lenny intro narration). The transcripts are otherwise consistent — same engineer, same Flowy, same `kevin`/`carl` aliases, same Ralph-loop language, same X handle `@cy_hess`. Most likely explanation: one of the two pieces lags the other on employer state (likely Tenex is the more recent affiliation, as the Feb 9 *How I AI* show notes are the later capture by date, and "10X" may be a prior-job reference in the Lenny intro). **Treat as one engineer with two captures, flag affiliation for follow-up.**

**Cross-refs:**
- [`23-anthropic-engineering-trilogy`](23-anthropic-engineering-trilogy.md) (Anthropic's internal Claude-reviews-100%-of-PRs practice from Cherny — same-model self-review case to contrast with CJ's cross-model review).
- [`12-adjacent-ecosystem`](12-adjacent-ecosystem.md) (personal-harness / DIY-tooling ecosystem context).
- [`28-schillace-sunday-letters`](28-schillace-sunday-letters.md) §3.4 (Schillace's Amplifier internals — *Crusty Old Engineer* critic subagent is the closest sibling pattern to `carl`).
- [`27-dotfile-pipelines-as-product`](27-dotfile-pipelines-as-product.md) §4 (dotpowers' four-model cross-critique pattern; loop-cap discipline).
- [`03-cherny-interview`](followup/03-cherny-interview.md) (Cherny's "build for the model six months from now" + Anthropic agent-review practice — Claude-reviewing-Claude is the same-model contrast).
- [`05-simon-willison`](05-simon-willison.md), [`06-hn-and-lenny`](06-hn-and-lenny.md) (Willison agent definition; OpenClaw demand context).
- [`04-every-skill-libraries`](04-every-skill-libraries.md) (Skills convention — SKILL.md as the durable harness primitive).

---

## 1. The thesis — personal harnesses dominate model choice

The single most load-bearing claim CJ Hess makes in the two captures is one most LLM-tier benchmark watchers will reject on first hearing:

> *"I'd honestly argue GPT 5.2 is a smarter model, but … working with Claude is just such a delight. In Claude Code, it just feels so steerable. And I think the one thing it really has is intent understanding."*

The "GPT 5.2 is a smarter model" concession is the load-bearing word. CJ is not a Claude partisan defending a tribe — he uses *both* models daily and runs `carl` (Codex / GPT-5.2) as a critic against `kevin` (Claude Code) on every diff. His reason for preferring Claude Code as the *primary* driver is not model intelligence at all; it is **harness fit**. The Claude Code harness allows him to wrap it in a *personal* ecosystem — bypass-permission aliases, custom skills, a hand-built visualization tool (Flowy), and a Ralph loop — and the harness wrap multiplies the value of the underlying model beyond what raw capability would predict.

This is the corpus' most explicit single-source articulation of **harness-quality-dominates-model-quality** for an individual engineer's daily workflow. It is the empirical practitioner statement of Theme-6 ("same model, different harness, different result") at the **single-engineer / single-machine** scope — peer to but distinct from:

- Schulhoff §6 (report 29): DSPy with small modifications (F1 0.548) beats 20-hour hand-crafted AutoDiCoT (F1 0.53) — same model, different harness, *at the prompt-engineering layer*.
- MacGregor / Valim (report 33): programming-language choice as a harness lever — same model, different language, dramatically different completion rate.
- Schillace's Amplifier (report 28): the agent-OS harness wraps even modest models into compounding-team agents.
- Dotpowers (report 27): same task, different `.dot` pipeline, different outcome — at the *pipeline* layer.

CJ adds the **personal harness** layer below all of those: per-engineer skills + aliases + bespoke dev tools + loops. The other harness layers are typically organizational artifacts. CJ's are individual.

The strong reading: *the unit of harness engineering is one engineer, one machine, one .claude folder.* Organizational harnesses (the team's Skills repo, the org's `AGENTS.md`, the CI gate) are downstream aggregations of what individual engineers prove out in their personal harnesses.

This reframes the corpus' "harness" thread (reports 09 §10, 18 §1, 27, 28, 33, followup/08) by adding the **per-engineer customization surface** as a first-class layer. Most of the corpus has been tracking harness at the organization level (Codex App Server, OpenAI's `running-codex-safely`, Anthropic's Skills + sandbox + subagent system, Notion's Boxy [report 35]). CJ shows that *under* those organizational harnesses, the working engineer is building yet more customization — and that customization is where they think the leverage actually lives.

---

## 2. Flowy — the JSON→flowchart bespoke dev tool

### 2.1 The friction point

CJ's planning workflow before Flowy was the now-common "iterate on a markdown plan, then build from it" pattern (variants of this appear in reports 03, 14, 23, 28, 29, 32). The piece he hated:

> *"there's always this misalignment of that edge character. I don't know why we haven't figured that out yet. But for things like UI mockups, things like, you know, flowcharts of how navigation's going to work, how a certain system is going to work, I really like this visual way to think about things, but I really hate staring at these ASCII like diagrams. Even things kind of like mermaid and everything just didn't feel exactly what I was going for."*

Mermaid was *almost* the answer — LLMs know mermaid syntax, can read and write it, can reason about it. But mermaid's constraint set is fixed and is not CJ's mental model. So he built Flowy: a tool that takes a JSON node/edge definition and renders it as a clean, interactive diagram, with an editor that round-trips edits back into the JSON file. The JSON is the canonical, version-controllable form; the diagram is the human-facing affordance; Claude reads the JSON natively.

### 2.2 What Flowy *is*, structurally

Flowy is a two-thing system:

1. **A small web app** that consumes JSON files (nodes, edges, styles, optional metadata) and renders them as either flowcharts/system diagrams or UI mockups. The editor side of the app writes changes back to the source JSON. CJ runs it locally; the JSON files live alongside his code in the repo's `.flowy/` folder.
2. **Two Claude Code Skills** that teach Claude *how to write Flowy JSON correctly*:
   - `~/.claude/skills/flowy-flowchart/SKILL.md` (flowcharts, system diagrams, animation-timing sequences).
   - `~/.claude/skills/flowy-ui-mockup/SKILL.md` (low-fidelity UI wireframe-style mockups).
   - A third "overview" skill provides a high-level Flowy reference for either.

The skills are conventional Anthropic Skills artifacts (report 04 / report 23 §6): markdown files describing the JSON schema (nodes, edges, shapes, styles, semantic colours, icons, properties), with a quick-start, examples, and — increasingly — pre-flight rules CJ injects when the skill misbehaves.

CJ's own description of the skill-evolution process is illuminating and worth quoting:

> *"I go in there, I change something quick, I say update the skill, and really the process of refinement is me using it and seeing what failed. So here, I don't super care how this file is set up as long as when I make an update afterward, it's performing better. Like I almost feel good letting the model manage what this looks like."*

This is the **skill-as-living-document** pattern — the SKILL.md is owned by the agent that uses it, *not by the human author*. The human is a curator-of-failures: when Flowy renders white-on-pastel and CJ can't read it, he goes to the skill, describes what failed, and lets Claude update the skill so that failure mode doesn't recur. The skill *learns from operational failure*.

Compare to: report 03's compound-engineering retrospectives, report 23 §6 on Skills schema constraints, report 28 §3.4 (Amplifier's *foundation expert* + *session analyst* feeding back into recipes). Same pattern, single-engineer scope.

### 2.3 The 100%-prompted dev tool

The most under-discussed claim in the Lenny capture:

> *"This was my first experiment with a Ralph loop. I'm still not certain how confident I am in them because I had to do a little bit of cleanup, but overall I will say this is kind of a dev tool that was almost 100% prompted."*

Flowy — the underlying web app, not just the skills — was built almost entirely by Claude Code in a Ralph loop (§4 below). It is, on CJ's account, an honest example of an AI-built tool that was used productively *by* the human plus AI pair that built it. This bears a Theme-3 governance dimension (an AI-built tool that the AI then writes into via the skill loop is at risk of compounding its own blind spots) and a Theme-4 substrate dimension (the build-your-own-dev-tool moment is real and not gated on traditional engineering capital cost).

### 2.4 The Flowy invocation pattern

CJ runs Flowy entirely through Claude Code, invoking it via the skills:

> *"On the tips and tricks section, I want to create a spinning wheel where a user presses a button, the wheel spins, and then that is one of the tips. After that, the tip should pop up in a card just below the spinner. Then use the flowy flowchart skill to create an animation timing sequence diagram and a user flow diagram for the tips and tricks page."*

Claude responds by writing two JSON files (animation timing + user flow) using the flowy-flowchart skill. CJ opens them in Flowy, edits them visually if needed (the edits flow back to the JSON), then prompts Claude:

> *"Based on those diagrams, please create UI mockups using the flowy UI mockups skill. Reference other UI mockup flowy JSON files in this repo."*

Claude writes a third JSON file showing UI mockup states. Then CJ commands:

> *"Based on the flowcharts and the mockups, build this feature."*

Claude one-shots the implementation. **The Flowy artifacts have replaced the markdown plan.** This is a corpus-first: the bridge from "design as text" → "design as visual diagram + JSON" → "design as direct input to implementation" without an intermediate markdown spec. The diagrams *are* the plan.

This pierces report 25's AFIS three-strategy gradient. CJ has moved from strategy-1 (NL + decorative diagrams) past strategy-2 (models for NL maturation) into a peculiar strategy-3 variant: **diagrams as the executable specification**, with the JSON underneath as the model-readable form. Strategy-3 in report 25's AFIS framing is typically associated with industrial systems-engineering tools (Cameo, IBM Rhapsody); CJ has reduced it to two SKILL.md files and a 100%-prompted web app.

---

## 3. The `kevin` / `carl` model-vs-model QC loop

### 3.1 Aliases as architecture

CJ has terminal aliases for his two model harnesses:

- `kevin` — Claude Code, invoked with **`--dangerously-skip-permissions`** (bypass-permissions mode; Claude can edit/write/run without per-action approval). CJ: *"I'm a fully bypass permissions guy. So Kevin in my terminal actually routes to Claude with bypass permissions."*
- `carl` — Codex (GPT-5.2 Codex), default config, no special permission setup. CJ: *"my Codex setup is under Carl."*

The aliases are not just shell convenience; they are **role assignment as architecture**. `kevin` is the productive coder. `carl` is the curmudgeonly staff engineer. Naming the binaries gives CJ a vocabulary for the workflow that maps to his mental model of who-does-what. This is a small but interesting Theme-7 ergonomic move: instead of inventing a UI for multi-model orchestration, *use shell aliases as your orchestration UI*.

Compare with report 06's reference to Cherny's "five Claudes steady-state" — Cherny's case is parallel instances of the *same* model class doing different sub-tasks. CJ's case is *different model classes* doing complementary roles in serial pipeline order.

### 3.2 The Carl review prompt

After `kevin` (Claude) finishes implementing a feature, CJ invokes `carl` (Codex) with a deliberately under-specified prompt — he wants Codex to find what Claude couldn't see, *which means he can't pre-shape the search*:

> *"Take a look at our current git diff and give me a report on the following:*
> *1. Does the code accurately reflect the plan/diagram artifacts?*
> *2. Are there any general code smells?*
> *3. If we were to do this again and take a different approach to refactor code around it to overall improve this code base, what approach would be best?"*

Three buckets — correctness against plan, code quality, strategic refactor. CJ explicitly does *not* attach any skills or custom prompts to `carl`. The argument: codex's review value is at the *meta* level (does this fit, is there a cleaner way, is this jamming), and skill-loading would over-constrain the search.

> *"I'm more concerned on the I guess like things that aren't clear rather than something that's like a logical bug. At this point, I feel like I'm mostly a QA person. And if there's something that's logically wrong, I've definitely found that I'll find it. But codex always finds those types of things, but I almost want to look for like the code smells like is there just a cleaner way."*

### 3.3 What Codex actually catches

In the *How I AI* demo, Codex caught three categories of issues Claude had shipped:

1. **Plan-fidelity discrepancy.** The spinner's pointer was *designed* (in the Flowy mockup) to land *on* a dot at rest; in implementation it landed *between* dots. A small, visual, non-test-covered detail Claude had subtly slid past.
2. **Classic React code smells.** Missing dependencies in a useEffect hook.
3. **Refactor opportunity.** "Pull this logic into separate components, define these constants, improve maintainability."

CJ's framing of why this works:

> *"Claude is very eager sometimes and maybe jams things in there without thinking about the bigger picture. And codex I don't think is much better when it's writing code, but when it reviews it almost always is like 'you've implemented this pattern, but it fits nicely if you just rebuild this system a little bit.' And that just keeps your codebase like away from all the vibe coding sins of having, you know, 10 format date functions all over your code."*

Codex isn't a better coder. Codex is a better critic *of Claude*. The asymmetry is operationally productive.

### 3.4 Closing the loop — Codex implements its own fixes

After Codex reports, CJ commits to the cheapest possible move:

> *"great, please make those improvements"*

Codex applies its own suggestions: fixes the pointer-on-dot bug, adds the missing useEffect dependency, factors out the constants. The closed loop is therefore:

```
kevin (Claude) implements
  → carl (Codex) reviews against plan/diagram + code smells + refactor opportunities
    → carl (Codex) implements its own suggested fixes
      → human (CJ) reads diff + accepts/iterates
```

The human is a QA-mode supervisor at the end. The two-model sandwich is automatable; the model-vs-model loop is the architectural primitive.

### 3.5 Cross-model review vs. same-model review

This is where the pattern is corpus-distinctive. The Anthropic engineering trilogy (report 23) and Cherny's interview (followup/03) both document the practice of **Claude reviewing every Claude-generated PR before a human looks at it** — Anthropic's internal Auto-Review subagent (also surfaced in OpenAI's `running-codex-safely`, report 18 §4.4) is the same-model variant. CJ's `kevin/carl` loop differs in one specific way that matters: **the reviewer is a different model class** (Codex / GPT-5.2 vs Claude). The hypothesis driving CJ's choice (made explicit by him) is that **a model's blind spots are correlated with its training data and its post-training reward-model shape**. A reviewer drawn from the same model class will share the blind spots and will fail to catch the failure modes that lie in those blind spots.

This is the empirical-practitioner motivation for what I'll propose below as **F46 — Single-Model Review Blindspot**.

Strong corpus reading: the Anthropic same-model-Auto-Review pattern (report 18 §4.4 / 23) and CJ's cross-model `kevin/carl` pattern are not redundant. They cover different threat surfaces:

- Same-model self-review catches *individual-output* errors — typos, missed edge cases, simple-to-spot mistakes the model could in principle have caught itself but didn't, which a second pass at the same model surfaces. This is essentially a self-consistency primitive (report 29 §1 ensembling).
- Cross-model review catches **systematic blind spots** that the model class shares — patterns the reviewer-model would have *also* shipped if asked to write the feature, but recognizes as wrong when asked to *review* — or, more interestingly, patterns *of-which the original model is unaware* but a different model's training corpus has internalised as problematic.

Operationally: do **both**. Auto-Review subagent (same-model) for cheap pass-1; cross-model critic for the architectural-blind-spot pass. CJ's loop is the cross-model pass.

The corpus comparable that is most thematically isomorphic is **Schillace's Crusty Old Engineer critic subagent in Amplifier** (report 28 §3.4). Crusty Old Engineer is a subagent persona; CJ's `carl` is a different *model*. Both share the design intuition that critique is most effective when delivered by *something other than what produced the artifact*. Schillace gets the otherness via persona prompting on the same model; CJ gets the otherness via model swap. The dotpowers four-model cross-critique pipeline (report 27 §4, Opus / GPT-5.4 / GPT-5.2 / Gemini-3.5-Flash via CSS-stylesheet assignment) is the third variant at pipeline scope: different models assigned to different *phases*, not roles.

---

## 4. The Ralph loop — self-prompted dev cycle

The Lenny capture has the first corpus-level surfacing of the term **"Ralph loop."** From CJ's introduction of Flowy:

> *"This was my first experiment with a Ralph loop. I'm still not certain how confident I am in them because I had to do a little bit of cleanup, but overall I will say this is kind of a dev tool that was almost 100% prompted."*

CJ doesn't define Ralph loop in either capture — he uses it as if the audience knows. The term is current in the X / Twitter AI-engineering subculture and refers (per public usage of the term in late 2025 / early 2026) to a **self-prompted continuous dev cycle**: Claude Code runs in a loop where it (a) reads its own retrospective / next-task file, (b) implements the next slice, (c) writes a new retrospective, (d) repeats — with the human re-engaging only at checkpoints. The name is a riff on a longstanding rubber-ducking idiom ("ralph it out"). Cf. report 27's dotpowers loop primitives, which independently arrived at the same shape with hard caps.

**Loop-cap discipline cross-reference.** Dotpowers (report 27 §4.3) imposes hard loop caps of 5/5/2 (research/build/critique) precisely because unconstrained self-prompted loops can run away — context-window collapse, repeated identical errors, drift from the original intent. CJ's "I'm still not certain how confident I am in them because I had to do a little bit of cleanup" is the empirical-practitioner version of why dotpowers caps. CJ's Ralph loop produced a working Flowy, but not without cleanup; dotpowers caps the loop *before* it requires cleanup. Same primitive, opposite governance posture.

**Substrate dimension.** Ralph loops are only viable when bypass-permissions is on (the `kevin` alias). The agent has to be able to run shell commands, edit files, write tests, and execute them — for hours, unattended — without a human approving each action. This is exactly the configuration the corpus' Theme-3 (governance) thread has been most uneasy about. Shapiro's R3 *"do not give it production scissors"* (report 32) and R4 (isolated env) suggest the only safe way to run a Ralph loop is in a fully sandboxed environment with no network, no production credentials, no irreversible actions reachable. CJ's caveat — *"I find that a lot of like projects where I'm solely working on it or working within the team I'm on, we have all the like rules set up in Git that if I do something horrible, it it's okay"* — suggests Git's revert/branch surface is his de-facto isolation layer.

---

## 5. Git-diff-driven retrospectives

The Lenny capture's most novel substrate hint is brief and easy to miss. From the *How I AI* show-notes blog and corroborated in the Lenny transcript: CJ has a workflow where **Claude reads a Git diff to write its own retrospective** at the end of a session or feature. The retrospective becomes input to the next Ralph loop iteration: what went well, what went badly, what to do differently next time.

This is the **diff-as-self-evaluation** primitive. The corpus has multiple adjacent patterns:

- **Spec-version-history-as-changelog** (Nystrom / Notion, report 35) — the spec evolves over commits, and the version-history *is* the changelog.
- **Compound-engineering retrospectives** (Every, report 03) — every project produces a retrospective that feeds into the next project's plan.
- **Anthropic's Skills update workflow** (report 23 §6) — when a skill misbehaves, the model proposes the skill update.
- **CJ's Flowy skill-update workflow** (§2.2) — the skill is updated by the agent when it fails.

The unifying primitive is **agent-curated postmortem from operational evidence**. In each case the agent ingests an operational signal (the diff, the failed render, the test result), produces a structured artifact (retro, skill update, plan), and *that artifact* is what carries forward. The human's role is curator-of-the-curation, not curator-of-the-evidence.

There is a strong project-relevance hook here: the project has a `retrospective/` folder convention (per `PLAN.md` and `00-synthesis.md`) and the corpus has been treating retrospectives as a human authoring task. CJ's pattern suggests the diff-driven retrospective should be **agent-authored from Git evidence**, then human-reviewed. The project should consider adding a Claude Code skill (or equivalent) `/research/skill/diff-to-retro` that reads the last N commits and proposes a retrospective for human review.

---

## 6. Cross-corpus implications

### 6.1 Where this report most affects existing corpus claims

| Existing claim | This report adds / refines |
|---|---|
| Report 23 / followup/03: Anthropic uses Claude to review every Claude-generated PR before human review. | Adds the contrast case: **cross-model** review (Codex reviewing Claude). Argues both layers are necessary; they catch different threat surfaces (individual error vs. class blind spot). |
| Report 28 §3.4: Amplifier's Crusty Old Engineer is a critic subagent. | Adds the model-class-swap variant. Argues critic-as-different-model is a stronger version of critic-as-different-persona. |
| Report 27: dotpowers' four-model pipeline assigns different models to different phases via CSS. | CJ's `kevin/carl` is the same pattern at single-engineer / single-machine scale — and at *role* (implementer vs. reviewer) rather than *phase* (research vs. build vs. critique). |
| Report 04 / 23 §6: Skills are durable, organization-shared harness artifacts. | Adds the **personal-skill** layer: `~/.claude/skills/` lives in the engineer's home, not the repo. Personal skills (`flowy-flowchart`, `flowy-ui-mockup`) are *not* shared and are continuously edited by the agent that uses them. This is a sub-organizational harness surface the corpus had not explicitly named. |
| Report 32 §8.2: F44 — Lethal-Trifecta Production-Scissors Default. | CJ's bypass-permissions `kevin` alias is the exact configuration F44 warns about. CJ's mitigation (Git revert/branch as de-facto isolation) is partial; he is one accidental network call away from a violation. |
| Report 33: programming-language choice is a harness lever. | CJ adds the per-engineer harness lever *below* language: skills, aliases, bespoke tools. Both are harness; they are stacked, not alternative. |
| Report 25 §6.3: AFIS three modelling strategies. | CJ's Flowy-diagram-as-spec is an unusual strategy-3 instance at single-engineer scale — diagrams are the spec, JSON is the model-readable form. |

### 6.2 Proposed candidate failure mode

**F46 — Single-Model Review Blindspot.** Same-model self-review (Claude reviewing Claude; Codex reviewing Codex) systematically fails to catch the failure modes the model's own training data + post-training reward shape have biased it toward. Cross-model review catches these. Operational signature: a code-review subagent on the same model class reports clean; a human or different-model reviewer finds a class-systematic issue (e.g. a particular React anti-pattern the original model is over-trained to ship). Mitigation: at least one critic in the review chain should be from a *different model class* than the implementer. F46 is a peer/refinement of F44 (Production-Scissors) — F44 is the substrate hardening; F46 is the review-architecture hardening.

Number rationale: F45 (Language-as-Harness Mismatch, report 33) and F44 (Lethal-Trifecta Production-Scissors Default, report 32) are the immediate predecessors in the sequence. F46 continues. Note unresolved F36/F37 collision flagged in INDEX.md §"Looking for a failure mode" — F46 is high enough to avoid further collision but lead-agent reconciliation of F36/F37 is still pending.

### 6.3 What this report does *not* answer

- Where Flowy actually lives (CJ promised to release a public version "this weekend" — Feb 2026 — but neither capture confirms the release).
- How CJ's bypass-permissions blast radius is actually contained beyond Git. (R4 / R5 from Shapiro report 32 §8 suggest network disconnect + isolated env; CJ does not describe either.)
- Whether the Ralph loop is the same shape as the dotpowers Build-loop and the Anthropic agent-review loop. Strong reading: all three are instances of the same primitive (autonomous self-prompted iteration with periodic human gating), but the published loop-cap discipline differs sharply.
- Whether `carl`-as-implementer (after `carl`-as-reviewer) is good enough at the actual implementation that Claude is no longer needed. CJ's framing — *"Codex I don't think is much better when it's writing code, but when it reviews it almost always is"* — suggests no, but is anecdotal.

---

## 7. Sources reviewed

| Source | Status | Notes |
|---|---|---|
| `research/manual/How I AI CJ Hess on Building Custom.txt` | ✅ FULL | Claire Vo / *How I AI* show-notes blog, Feb 9 2026. CJ Hess identified as Tenex SWE. |
| `https://www.lennysnewsletter.com/p/this-week-on-how-i-ai-how-to-build` (via `research/manual/lenny-build-your-own-ai-developer-tools-with-claude-code.txt`) | ✅ FULL | Lenny's Newsletter transcript. CJ Hess introduced as "at 10X." Affiliation discrepancy flagged §header. |
| CJ Hess on X / Twitter (handle `@cy_hess`) | ❌ not drained | Show-notes URL only; would surface Flowy public release if available. Followup candidate. |
| Flowy public release | ❌ not surfaced | CJ promised to release a public version "this weekend" — not confirmed in either capture. Followup candidate. |
