---
based-on-commit: d430aeb
based-on-date: 2026-05-23
---

# Contradictions register (Phase 1A)

**Status:** Canonical pairwise-contradictions list in the post-Round-12 corpus. **No resolution attempted at register time** — that is Phase-2/3/4 work. This file's job is to make every contradiction visible.

**How to read.** Each entry: a short claim-pair, the two sources cited at primary-source level, the design question the contradiction sits on, and the load-bearing impact (which architectural choice does it affect?). Tagged for greenfield-relevance, brownfield-relevance, or both.

**Provenance discipline.** Quotes are verbatim or near-verbatim with section references. Where a quote is paraphrased, it is flagged as such. The register draws on the ~16 tensions surfaced in the two archived syntheses (`archive/synthesis-v1-v2/00-synthesis.md` §3, `archive/synthesis-v1-v2/13-round-2-synthesis.md` §2), then extends with material from Round-3–12 reports and followups.

---

## A. Operating-mode contradictions (lights-out / regime)

### CTR-A1 — L5-as-target vs. L5-as-anti-pattern
- **Claim 1 (Shapiro, Five Levels, report [`32`](../../research/32-shapiro-completion-chat-agent-claw.md); followup [`01`](../../research/followup/01-shapiro-five-levels.md)):** L5 is the *terminus* of the ladder — *"It's a black box that turns specs into software… humans are neither needed nor welcome."* Shapiro describes it as *"nearly unbelievable - and it will likely be our future."*
- **Claim 2 (Jaymin West, *Agentic Engineering* Ch 9 §7, report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §2c):** L5 is an **empirical anti-pattern** in 2026. Cites CodeRabbit (1.4× critical-issue rate), Veracode (45% OWASP-vulnerable code), METR (developers 19% slower than self-estimated). Recommends L3–L4 as the "sweet spot."
- **The contradiction:** One source positions L5 as the aspirational terminus; the other names it as currently dangerous and counter-recommended.
- **Design question this sits on:** OQ-B1 (lights-out / L5 / regime), §2.1 of brief.
- **Mandate relevance:** both
- **Load-bearing impact (high):** Decides whether v3's lights-out mandate (UC1) requires defending against an empirical anti-pattern claim or inherits an aspirational frame.
- **Phase-1 bias-guard sharpening (WEAK-1):** Sharper framing: Jaymin's Ch 9 §7 is itself a **two-sided text** — it names L5 as anti-pattern *and* frames 2026 as *"the third historical attempt"* at the factory concept with *"LLMs dissolving the flexibility problem that killed both prior attempts"* (report 09 §7 paraphrase). Jaymin is simultaneously the source of the strongest anti-L5 claim *and* a source of the strongest "this time it works" framing. The contradiction is not merely between Shapiro-and-Jaymin; it is internal to Jaymin Ch 9 §7 and parallel to CTR-C6's Jaymin-vs-Jaymin scaffold contradiction. Why the sharpening matters: CTR-A1 is currently the headline lights-out contradiction. The register treats it as Shapiro-vs-Jaymin. The internal Jaymin-vs-Jaymin reading suggests Jaymin's threshold framework is itself unstable; OQ-B6 cannot just default to "Jaymin's bars" as one credible option without engaging this instability.

### CTR-A2 — Shapiro's self-position vs. corpus-propagated "Shapiro as L5"
- **Claim 1 (Shapiro, Five Levels post, followup [`01`](../../research/followup/01-shapiro-five-levels.md), §"Where Shapiro positions his own work"):** Shapiro positions himself **at L4**, verbatim: *"I'm here."* L5 is described as *other* people: *"I know a handful of people who are doing this. They're small teams, less than five people."*
- **Claim 2 (El Kaim, *Dark Factory*, report [`07`](../../research/07-dark-factory.md); pre-Round-7 corpus propagation):** El Kaim's restatement reads L5 as the terminus all should reach; multiple corpus reports framed Shapiro as a L5 practitioner. Per `research/PLAN.md` §6.1, propagation flag #4: *"Anywhere in the corpus Shapiro is described as 'a Level 5 practitioner' or 'Level 4–5 practitioner-tooler': refute with Shapiro's verbatim L4 self-position."*
- **The contradiction:** Shapiro's stated self-position (L4) is incompatible with the El-Kaim-propagated corpus framing that treats him as L5.
- **Design question this sits on:** OQ-B1; vocabulary mapping for "lights-out" vs. Shapiro's ladder.
- **Mandate relevance:** both
- **Load-bearing impact (high):** Three of the four v2 architectures borrow exemplar weight from "Shapiro at L5"; the refutation reshapes the empirical ceiling claim.

### CTR-A3 — StrongDM "humans-cannot-review" vs. Willison "review-is-morally-required"
- **Claim 1 (StrongDM `/principles`, report [`01`](../../research/01-strongdm-factory.md); archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §3.1):** Verbatim cardinal rule: *"Code must not be written by humans. Code must not be reviewed by humans."*
- **Claim 2 (Simon Willison, May 6 2026 post + Lenny transcript, reports [`05`](../../research/05-simon-willison.md), [`06`](../../research/06-hn-and-lenny.md); archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §3.1):** Names *"inflicting unreviewed code on collaborators"* as the single named anti-pattern. Admits drift under load: *"vibe coding and agentic engineering are getting closer than I'd like"* and names the drift as a candidate *normalization of deviance*.
- **The contradiction:** StrongDM prohibits human review by principle; Willison treats it as morally required even while admitting practice is slipping.
- **Design question this sits on:** OQ-B3 (human re-entry mechanism); regime classification per architecture.
- **Mandate relevance:** both
- **Load-bearing impact (high):** Decides whether the factory's human-in-loop bar is a *threshold* (Jaymin) or a *principle* (StrongDM) or a *practical drift* (Willison).

### CTR-A4 — "Lights-out" (user) vs. "L5" (Jaymin) — vocabulary mapping unresolved
- **Claim 1 (UC1, [`constraints-extracted`](../constraints-extracted.md)):** *"a running lights-out software factory for greenfield applications."*
- **Claim 2 (Jaymin Ch 9 §7, report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §2c):** L5 = *"Level 5 as the target"* and is called out as an anti-pattern.
- **The contradiction:** Per the brief §2.1 itself — *"'Lights-out' (UC1's term) is not necessarily 'L5' (Jaymin's term). The tension is real only if these vocabularies map onto each other."* The mapping is **untested in the corpus**; the corpus alternately treats them as identical (El Kaim conflation) and as distinct (per glossary §0). The contradiction lives in the *meta* — corpus voices are not consistent about whether they refer to the same regime.
- **Design question this sits on:** OQ-B1 — the mandatory mapping test.
- **Mandate relevance:** both
- **Load-bearing impact (high):** Every Phase-2 track inherits this ambiguity; if "lights-out ≠ L5," CTR-A1 is mostly dissolved; if "lights-out = L5," CTR-A1 is decisive.

### CTR-A5 — Jaymin's brownfield ceiling vs. mandate-agnostic v2 stance
- **Claim 1 (Jaymin, report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §2c):** *"Jaymin asserts the L5 dark-factory ceiling for brownfield is around L3."* (Report-09 author quote summarising Jaymin's claim.)
- **Claim 2 (archived [`00-comparison`](../../archive/architectures-v2/00-comparison.md)):** Makes **no greenfield-vs-brownfield distinction**; treats architectures as mandate-agnostic.
- **The contradiction:** Jaymin claims a *brownfield-specific* empirical ceiling at L3; the v2 comparison treats the regime ceiling as mandate-neutral.
- **Design question this sits on:** OQ-B6 thresholds; UC4 working hypothesis (whether brownfield is differently bounded).
- **Mandate relevance:** brownfield
- **Load-bearing impact (high):** Directly informs whether brownfield architectures must declare a different empirical bar than greenfield.

### CTR-A6 — Cherny's 5+ parallel-agents-as-routine vs. Willison's 4-agents-exhaust-by-11am
- **Claim 1 (Cherny, Lenny × Cherny transcript, followup [`03`](../../research/followup/03-cherny-interview.md); archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §3.6):** *"five-agents-steady-state, 1/3-terminal + 1/3-desktop + 1/3-iOS surface split, 10–30 PRs/day, 100% Claude-written since November 2025; +200% productivity per engineer; $100K+/month per-engineer token spend."* Cherny's role is *scheduling*.
- **Claim 2 (Willison, Lenny × Willison transcript, report [`05`](../../research/05-simon-willison.md); archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §3.6):** *"I can fire up like four agents in parallel and have him work on four different problems, and by like, 11am I am wiped out for the day."*
- **The contradiction:** Two practitioners at the same parallelism scale (4–5 agents) report opposite cognitive outcomes — one sustains daily; the other exhausts in ~3 hours.
- **Design question this sits on:** Human-role design (supervisor vs. scheduler); F5 (cognitive ceiling) parameter.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Decides whether the factory enforces low parallelism by default or assumes scheduler-shape humans.

---

## B. Spec / artifact contradictions

### CTR-B1 — Spec format: prose vs. structured-IDs vs. DOT-graph vs. EARS-notation
- **Claim 1 (StrongDM NLSpec, report [`01`](../../research/01-strongdm-factory.md); archived synthesis §3.3):** Specs are **prose markdown**.
- **Claim 2 (Every.to compound engineering, report [`03`](../../research/03-every-compound-engineering.md); archived synthesis §3.3):** **Prose + structured stable IDs** (R/A/F/AE → U).
- **Claim 3 (Attractor, report [`02`](../../research/02-strongdm-attractor.md); archived synthesis §3.3):** Pipeline is **graph-structured** (DOT in practice); spec-of-the-pipeline is the DOT file.
- **Claim 4 (Kiro, report [`12`](../../research/12-adjacent-ecosystem.md) §2.5):** **EARS-notation** for requirements.
- **The contradiction:** Four incompatible structural commitments for the most load-bearing artifact (the spec).
- **Design question this sits on:** D-1 (spec is durable artifact) — but says nothing about format.
- **Mandate relevance:** both
- **Load-bearing impact (high):** Spec format determines reviewability, tooling, and whether agents can mechanically extract requirements.

### CTR-B2 — Spec-malleability: greenfield-fluid vs. fixed-once-mature
- **Claim 1 (UC4, [`constraints-extracted`](../constraints-extracted.md)):** Greenfield is *"spec-malleable"* — *"a malleable architecture during refinement of the spec."*
- **Claim 2 (Nystrom / Notion, report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)):** Spec is *checked into the repo*; **the spec's git version history is the changelog**. The spec is stable enough to anchor implementation/verification/shipping cycles.
- **The contradiction:** UC4 frames the greenfield spec as in-flight and reversible; Nystrom treats the spec as a stable durable artifact whose change history is itself the project changelog. Both can be true at different lifecycle stages, but neither source acknowledges the distinction — they make competing universal claims.
- **Design question this sits on:** UC4 working hypothesis; per-work-unit-class mandate-fit.
- **Mandate relevance:** greenfield
- **Load-bearing impact (medium):** Determines whether the greenfield architecture treats the spec as an in-flight artifact or a versioned source.
- **Phase-1 bias-guard sharpening (MISSED-6):** Brier puts specs in pace-layer 3 above code (followup [`12`](../../research/followup/12-brier-pace-layers.md), pace-layer 1: *"in a world of AI, code is free to produce and reproduce."*); Nystrom puts the **spec's version-control history** at the heart of the methodology (report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)). Both agree spec > code, but disagree on whether the spec itself moves slowly (Brier: stable mid-layer) or *needs an entire revision-tracked change discipline because it moves fast enough that the deltas are the project narrative* (Nystrom). CTR-B2 (greenfield-fluid vs. fixed-once-mature) misses this sharper **spec-velocity** disagreement: Brier predicts spec stability; Nystrom predicts spec churn rich enough to function as changelog. See also CTR-B7 (new entry).

### CTR-B3 — "Spec is the most valuable thing you produce" (El Kaim) vs. spec-third under pace layers (Brier)
- **Claim 1 (El Kaim restatement of Shapiro L4, followup [`01`](../../research/followup/01-shapiro-five-levels.md)):** *"The primary skill at this level is spec-writing… The spec is now the most valuable thing you produce."* (Per followup/01: this is El Kaim's editorialisation; Shapiro himself does not say this.)
- **Claim 2 (Brier, followup [`12`](../../research/followup/12-brier-pace-layers.md)):** Specs are layer **3 of 5** in Brier's pace-layer stack; below them sit *architecture* and *standards* (slower-moving, more durable). Brier's framework demotes specs from "primary artifact" to "middle layer."
- **The contradiction:** El Kaim makes specs the primary artifact at L4+; Brier demotes them under architecture and standards.
- **Design question this sits on:** Artifact-stack ordering; spec-driven vs. layered-culture architectures.
- **Mandate relevance:** both
- **Load-bearing impact (high):** Architecture 1 (Refinery)'s entire pitch — *"the specification is the product"* — is contradicted by Brier's spec-third framing (followup/12 §6: *"Arch 1 (spec-primary contradicted by spec-third)"*).
- **Phase-1 bias-guard sharpening (MISSED-6):** Brier's pace-layer-3 framing predicts spec stability while Nystrom's spec-git-history-as-changelog framing predicts spec churn rich enough to function as changelog. The two corpus-popular voices on spec primacy disagree at the spec-velocity level, not merely the spec-stack-position level. See also CTR-B7 (new entry) for the standalone spec-velocity contradiction.

### CTR-B4 — "Specs as source code" (Grove/Jaymin) vs. "checked-in compiled binaries are also valuable" (implicit Willison)
- **Claim 1 (Sean Grove, per Jaymin, report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §3; promoted to Round-2 C12):** *"throwing away prompts after generating code is like checking in compiled binaries while discarding source."*
- **Claim 2 (Willison's hoarding posture, report [`05`](../../research/05-simon-willison.md); plus low-background-steel framing, report [`05`](../../research/05-simon-willison.md)):** Code itself remains a first-class artifact; the *"low-background steel"* framing values pre-2022 source as itself a durable, irreplaceable resource. Specs are not posited as the *sole* source-of-truth.
- **The contradiction:** Grove's analogy implies code is mere build-output to be regenerated from spec; Willison treats code itself as a durable artifact worth preserving and reviewing.
- **Design question this sits on:** Whether the substrate's durable layer is spec-only or spec-and-code.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Brownfield mandate is especially affected — if code is *output*, the brownfield codebase is not a primary input; if code is durable, it is.

### CTR-B5 — Scenarios live outside the codebase (Round-1 D-2) vs. brownfield scenarios live inside (fragile-default flag)
- **Claim 1 (Round-1 consensus, archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §2.2):** *"The single most-cited innovation across the corpus is StrongDM's repurposing of Cem Kaner's 2003 'scenario testing' — end-to-end user stories, in prose, stored **outside** the codebase the agent can read."*
- **Claim 2 (Brief §4.1 D-2 fragile-default flag):** *"Scenarios live outside the codebase as a holdout set"* — **flagged fragile for brownfield**. Brownfield architectures may genuinely inherit scenarios *from* the codebase (production traces, existing test suites, runtime telemetry).
- **The contradiction:** Round-1 promotes out-of-tree scenarios as universal; the brief flags that brownfield mandates may have to invert the rule (scenarios from the codebase itself).
- **Design question this sits on:** D-2 default; brownfield substrate divergence.
- **Mandate relevance:** brownfield
- **Load-bearing impact (high):** Substrate-level decision (where scenarios live; who can read them). Substrate-vs-methodology layer placement (Phase 4).
- **Phase-1 bias-guard sharpening (WEAK-3):** Sharper framing: StrongDM's own primary pages contain both *"end-to-end 'user story', often stored outside the codebase"* (scenarios out-of-tree) AND *"Tokens are the fuel"* page enumerating *"traces, screen capture, transcripts, **incident replays**, adversarial use, **agentic simulation**"* (report [`01`](../../research/01-strongdm-factory.md) §1) — many of which are **necessarily inside or generated from the running codebase/runtime**. StrongDM's own discipline already permits scenario-equivalents to live inside the running system; the D-2 default ("outside the codebase") is a simplification of StrongDM's actual practice. Why the sharpening matters: The register's framing makes brownfield look like the awkward case requiring D-2 inversion. The sharper framing shows the **D-2 default itself oversimplifies its primary source**; brownfield is not inverting anything novel — it is closer to StrongDM's actual practice than D-2's stated default is.

### CTR-B6 — El Kaim 9-field intent block vs. UC4 spec-malleable hypothesis (MISSED-3)
- **Claim 1 (El Kaim Ch 3 §4.1, report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md)):** Intent block is a Kubernetes-shaped typed object with `invariants` defined as *"Non-negotiable conditions that any valid realization of the intent must preserve"* — explicitly designed as the **stable upstream** anchor that protects against confabulation when an LLM drafts a spec.
- **Claim 2 (UC4 / glossary §0 [`constraints-extracted`](constraints-extracted.md)):** Greenfield is **spec-malleable** — *"the system's architecture is still moving during spec refinement; commitments are reversible."*
- **The contradiction:** El Kaim's intent → decision → spec → control → feedback chain *requires* non-negotiable invariants at the top; UC4's spec-malleable framing makes everything reversible. The register has CTR-B2 (greenfield-fluid vs. fixed-once-mature) but does **not** surface that El Kaim's deepest spec-authorship primary anchor structurally rejects the spec-malleable framing as an *upstream* practice.
- **Design question this sits on:** UC4 working hypothesis falsifiability (D1 motivation).
- **Mandate relevance:** greenfield
- **Load-bearing impact (high):** UC4 hypothesis falsifiability — the strongest spec-authorship primary anchor in the corpus prescribes upstream stability, not malleability.

### CTR-B7 — Brier "code is fashion / free to reproduce" vs. Nystrom "spec git-history IS the changelog" (MISSED-6)
- **Claim 1 (Brier, followup [`12`](../../research/followup/12-brier-pace-layers.md), pace-layer 1):** *"in a world of AI, code is free to produce and reproduce."*
- **Claim 2 (Nystrom / Notion, report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)):** **The spec git-history is the project changelog**; Markdown specs in `agent specs/` subfolder are the **AFIS strategy-3 industrial anchor** — load-bearing durable artifact.
- **The contradiction:** Brier puts specs in pace-layer 3 above code; Nystrom puts the **spec's version-control history** at the heart of the methodology. Both agree spec > code, but disagree on whether the spec itself moves slowly (Brier: stable mid-layer) or *needs an entire revision-tracked change discipline because it moves fast enough that the deltas are the project narrative* (Nystrom). Sharper than CTR-B3 (El Kaim spec-primary vs. Brier spec-third): a **spec-velocity** disagreement between two corpus-popular voices.
- **Design question this sits on:** Spec-velocity (D-1 default).
- **Mandate relevance:** both
- **Load-bearing impact (medium-high):** Affects whether spec change discipline is itself a load-bearing methodology layer (Nystrom) or implicit pace-layer slow (Brier).

---

## C. Substrate vs. methodology contradictions

### CTR-C1 — Agent = Model + Harness (Round-2 C10) vs. graph-node / population architectures don't decompose
- **Claim 1 (Round-2 C10, [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §1.1):** *"Agent = Model + Harness is the canonical 2026 vocabulary."* Five independent practitioners (Fowler, Mollick, Raschka, Schmid, Hashimoto) converged on the formula.
- **Claim 2 (Brief §4.1 D-3 fragile-default flag):** *"Agent = Model + Harness — flagged fragile for graph-node and population architectures."* Architectures that treat agents as graph nodes (Attractor-style) or populations (Tournament-style) **do not decompose cleanly** into "model + harness."
- **The contradiction:** Round-2 promotes the formula as canonical; the brief flags it as decomposing badly for two of the four v2 architectures.
- **Design question this sits on:** D-3 default; whether the vocabulary holds across all architecture shapes.
- **Mandate relevance:** both
- **Load-bearing impact (high):** Affects whether substrate primitives can be defined in terms of "harness" (Round-2 framing) or need a richer vocabulary that also accommodates graph and population shapes.

### CTR-C2 — Substrate-heavy + thin-methodology (Round-2 framing) vs. methodology-dominates (UC4 hypothesis)
- **Claim 1 (Round-2, [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §8):** *"Round 2 turned the software-factory project from 'design a methodology' into 'configure a methodology on top of an existing substrate.'"* — substrate as the load-bearing investment.
- **Claim 2 (UC4 working hypothesis, [`constraints-extracted`](../constraints-extracted.md)):** *"My suspicion is that we won't find one that works best with both [mandates]"* — implies methodology differences are deep enough that substrate-sharing is not enough.
- **The contradiction:** Round-2 implies substrate-heavy + thin-methodology can carry both mandates; UC4 implies the methodology layer is so different per mandate that no substrate-sharing trick rescues a single architecture.
- **Design question this sits on:** UC4 hypothesis falsifiability; OQ-B2 (where the boundary falls).
- **Mandate relevance:** both
- **Load-bearing impact (high):** Decides whether the 3 both-mandates tracks in Phase 2 (D1) are searching for a real architecture or chasing a structurally-impossible one.

### CTR-C3 — Methodology evolution as substrate primitive vs. per-architecture concern
- **Claim 1 (Klaassen's self-improving prompts, report [`03`](../../research/03-every-compound-engineering.md); archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §3.4):** Self-improving prompts are described as a *methodology pattern* of compound engineering — Klaassen's frustration-detector "rewrites the original prompt."
- **Claim 2 (Schillace, *"gene transfer"*, report [`28`](../../research/28-schillace-sunday-letters.md); Shapiro Claw memory + dreaming, report [`32`](../../research/32-shapiro-completion-chat-agent-claw.md)):** Self-improvement is framed as a *substrate-class capability* — what makes a Claw a Claw, what makes Amplifier a gene-transfer system.
- **The contradiction:** Self-improvement is alternately a methodology pattern (Compound Engineering) or a substrate primitive (Claw/Amplifier).
- **Design question this sits on:** OQ-B9 (methodology evolution as per-architecture concern vs. shared-substrate primitive).
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Phase-4 substrate boundary; Phase-5 ADR set composition.

### CTR-C4 — RouterLLM as substrate primitive vs. provider-aligned profiles (do not unify)
- **Claim 1 (OpenHands V1, report [`11`](../../research/11-openhands-substrate-audit.md) §6; Round-2 §4):** **`RouterLLM`** — per-call model-routing layer. Cited as the substrate-level mitigation for F1/F27 (hallucination loop, circularity). Treats provider as routable abstraction.
- **Claim 2 (Attractor, report [`02`](../../research/02-strongdm-attractor.md) line 18; archived synthesis §3.7):** *"Each model family works best with its native agent's tools and system prompts"* — *"codex-rs for OpenAI, Claude Code for Anthropic, gemini-cli for Gemini."* Provider-aligned, *do not unify*. Validated by 3 independent Attractor implementations (followup [`02`](../../research/followup/02-attractor-implementations.md) §4).
- **The contradiction:** OpenHands abstracts the provider behind a router; Attractor explicitly rejects unification and demands per-provider profiles.
- **Design question this sits on:** OQ-B8 (provider-property requirements; right level of abstraction).
- **Mandate relevance:** both
- **Load-bearing impact (high):** Decides shape of substrate's provider layer; affects whether judge-model-family independence (F1/F27 mitigation) is achievable inside a unified abstraction.

### CTR-C5 — OpenHands+Overstory substrate (Round-2 recommendation) vs. Gas City substrate (Round-12 recommendation)
- **Claim 1 (Round-2, [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §8):** *"the substrate is **OpenHands SDK + CLI (per-cycle runtime) + Overstory-design-in-Python (orchestration)**."*
- **Claim 2 (Round-12 gas-systems substrate, report [`38`](../../research/38-gas-systems-substrate.md) §3):** Gas City's "Nine Concepts" architecture *"is the strongest substrate match in the corpus for both methodologies, because every Dark Factory and Compound Engineering primitive maps either to a Gas City primitive or to a pack-level convention on top of one."*
- **The contradiction:** Two corpus-derived synthesis recommendations point at incompatible substrate stacks (OpenHands+Overstory in Python vs. Gas City in Go) for the same problem.
- **Design question this sits on:** Substrate selection; substrate-primitives ADR set (Phase 5).
- **Mandate relevance:** both
- **Load-bearing impact (high):** Direct substrate choice; affects every downstream substrate-primitive ADR.

### CTR-C6 — Scaffold-as-load-bearing (Jaymin book) vs. scaffold-as-anti-pattern (Jaymin Manifesto)
- **Claim 1 (Jaymin book Ch 6, report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §1, promoted to C11):** *"Scaffold and harness are different layers and must be named separately."* Scaffold (CLAUDE.md, AGENTS.md, project conventions) is **load-bearing**; the harness depends on scaffold quality.
- **Claim 2 (Jaymin Manifesto, report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §12.1 / §"Tension flag"):** The manifesto position is that *"grep-equipped CLI agents should read the code itself, and that documentation is a liability because it drifts."* Report 09 explicitly flags: *"This is not a minor disagreement: the book treats scaffold quality as something the harness depends on; the manifesto treats it as anti-pattern."*
- **The contradiction:** Same author, but two stated positions at ~9 months apart that contradict each other on whether scaffold is a substrate primitive.
- **Design question this sits on:** Scaffold ADR; AGENTS.md / CLAUDE.md discoverability primitive (Round-2 substrate primitive #9).
- **Mandate relevance:** both
- **Load-bearing impact (high):** Per report 09 itself: *"the scaffold-vs-harness distinction is not a settled doctrine even within Jaymin's own writing."*
- **Phase-1 bias-guard sharpening (WEAK-2):** Sharper framing: The manifesto frames documentation/scaffold as *"the bitter lesson in action"* — i.e., grounded in the same principle Gas City's "Bitter Lesson" design mantra (report [`38`](../../research/38-gas-systems-substrate.md) §3) anchors its substrate exclusion list on. This puts Jaymin's manifesto on the **same intellectual side as the Gas City substrate** and against the Anthropic Skills / SKILL.md convention, the AGENTS.md discoverability primitive (Round-2 substrate primitive #9), and the Compound Engineering knowledge-store. The contradiction is not isolated to Jaymin: it is a **bitter-lesson vs. scaffold-substrate** cross-corpus cleavage. Why the sharpening matters: Re-frames CTR-C6 as a corpus-wide split (bitter-lesson camp: Jaymin manifesto + Gas City; scaffold-substrate camp: Anthropic Skills + Every SKILL.md + El Kaim Codex + Round-2 C11). The Phase-5 ADR on scaffold cannot be drafted without naming the bitter-lesson side as a coherent corpus position rather than a single-author quirk.

### CTR-C7 — Coordination medium: mail bus (Overstory) vs. GitHub-issues-as-coordination (CI-friendly translation)
- **Claim 1 (Overstory, report [`10`](../../research/10-overstory-substrate-audit.md) §5):** Mail bus is the coordination primitive (`src/mail/`).
- **Claim 2 (Round-2 §5.1, [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md)):** *"Mail-based / convoy / point-to-point coordination doesn't translate to CI runners that share only `git` + GitHub issues/comments. The 'GitHub-issues-as-coordination' pattern (Jaymin Ch 8 §5) is the version that maps cleanly."*
- **The contradiction:** Round-2 declares the Overstory mail-bus substrate primitive incompatible with the CI/CD operating model the same synthesis adopts.
- **Design question this sits on:** Substrate-vs-methodology coordination layer.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Affects which substrate primitives the v3 set inherits without translation.

### CTR-C9 — Anthropic Skills "no network access" vs. "dreaming" overnight research Claws (MISSED-5)
- **Claim 1 (report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5, anchored on platform.claude.com docs):** Anthropic API-surface Skills have **zero network access by runtime fiat** — *"No network access, No runtime package installation, Pre-configured dependencies only."* This is the substrate-level closure rule.
- **Claim 2 (Shapiro Claw post / report [`32`](../../research/32-shapiro-completion-chat-agent-claw.md), Jesse Vincent's assistant exemplar):** Corpus-canonical "dreaming" primitive — *"every night research things that might help it do its job"* — explicitly requires network access (web search, external research) overnight.
- **The contradiction:** Anthropic's substrate closes the network at the Skill-layer for safety; Shapiro's Claw-as-substrate-template requires nighttime network research to deliver the *dreaming* primitive (Round-2 referenced as a Claw-class capability).
- **Design question this sits on:** Substrate-primitive ADR — which closure rule wins.
- **Mandate relevance:** both
- **Load-bearing impact (medium-high):** Forces resolution of which closure rule wins for the substrate-primitive ADR.

### CTR-C10 — Report 37 Portuguese-vs-English language effect on policy vs. RouterLLM provider-agnosticism (MISSED-8)
- **Claim 1 (report [`37`](../../research/37-academic-llm-agent-collusion.md) §5 verbatim):** *"The Portuguese-prompted agents are uniformly more collusive and more stably so across both persona conditions"* — natural-language-of-prompt produces a measurable behavioural-drift signal at the **policy/decision layer**, not just the code-generation layer.
- **Claim 2 (OpenHands V1 RouterLLM, report [`11`](../../research/11-openhands-substrate-audit.md); D-3 / Round-2 C10 "Agent = Model + Harness"):** The substrate-level routing abstraction treats the model+harness as a swappable unit. The substrate has no first-class abstraction for "prompt natural language" as a behaviour-influencing harness parameter.
- **The contradiction:** Report 37 supplies the **first empirical anchor** that a *harness parameter the substrate doesn't model* (natural language of the prompt) materially shifts agent behaviour at the policy layer. If true, "Agent = Model + Harness" is incomplete: it's "Agent = Model + Harness + Natural-Language-Register."
- **Design question this sits on:** Substrate vocabulary completeness (D-3).
- **Mandate relevance:** both
- **Load-bearing impact (medium-high):** Forces re-opening of D-3 (Agent = Model + Harness) on grounds the brief flags as already-fragile, but adds an unfamiliar axis to the fragility argument.

### CTR-C11 — Anthropic Skills "open standard / agentskills.io" vs. Skills "do not sync across surfaces" (MISSED-11)
- **Claim 1 (report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5, Dec 18 2025 update):** *"We've published Agent Skills as an open standard for cross-platform portability"* at agentskills.io.
- **Claim 2 (report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5, REFUTED-line):** *"Custom Skills do not sync across surfaces"* — claude.ai / API / Claude Code each maintain separate Skill stores; explicit portability gap.
- **The contradiction:** Skills are simultaneously promoted as a portable open standard and shipped with a per-surface portability barrier. Affects the scaffold-as-substrate-primitive ADR (CTR-C6 scaffold-vs-anti-pattern adjacent) — corpus is endorsing a substrate primitive whose own primary docs flag is not actually portable today.
- **Design question this sits on:** Scaffold/substrate ADR (Phase 5).
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Anthropic Skills is the closest the corpus has to a cross-vendor scaffold standard; the portability gap is awkward.

---

## D. Failure-mode contradictions

### CTR-D1 — F36/F37 dual-proposal collision (reports 25 vs. 26)
- **Claim 1 (Report [`25`](../../research/25-requirements-engineering-foundations.md) §7.3):** **F36** = *"Vocabulary lint debt — LLM-authored specs systematically violate INCOSE GtWR R7/R8/R9 (vague modifiers; ambiguous pronouns; superlatives)."* **F37** = *"Point-spec / region-mismatch — INCOSE Complexity Primer principle 12: when the *intended* outcome is a region in solution-space, expressing it as a point spec guarantees off-target instances."*
- **Claim 2 (Report [`26`](../../research/26-prompt-underspecification-academic.md) §5):** **F36** = *"Instruction-following ceiling — gpt-4o Pass@1 drops 98.7% → 85.0% as requirements specified grow 1 → 19."* **F37** = *"Silent contradictory-prompt collapse — GPT-4 Pass@1 73.8% → 6.7% on contradictory HumanEval, RIR climbs to 89%."*
- **The contradiction:** Two reports independently propose four *different* phenomena under the same two numbers (F36, F37). All four are real and warrant catalog inclusion.
- **Design question this sits on:** Failure-mode catalog numbering (Phase 1B).
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Documentation-only conflict per PLAN.md §3.6, but blocks failure-mode catalog finalization.

### CTR-D2 — F26 (telephone / sustained chain) vs. F15 (single-prompt collapse) — splitter/lumper
- **Claim 1 (Report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §6 + Manifesto Rule 5; [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §3.1):** **F26** = telephone / sustained inter-agent chain accelerates vision drift; promoted *as separate* from F15.
- **Claim 2 (Round-1 F15, [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §4):** **F15** = *"Single ideation prompts collapse into the model's most-trained directions."*
- **The contradiction:** F26 was promoted as *separate* on the grounds that single-agent and multi-agent failure surfaces differ; the corpus is split on whether the multi-agent variant is truly distinct or a parameterization of F15.
- **Design question this sits on:** Failure-mode catalog granularity.
- **Mandate relevance:** both
- **Load-bearing impact (low):** Per F1B catalog work; downstream mitigations differ slightly.

### CTR-D3 — F27 (circularity / same-model build+validate) — Tournament mitigates vs. exemplifies
- **Claim 1 (Round-2 §7.5, [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md)):** *"F27 (circularity) is most severely failed by Arch 4 (Tournament) and Arch 2 (Atelier) at high parallelism; `RouterLLM` model-family diversity is the substrate-level mitigation."*
- **Claim 2 (archived [`04-evolutionary-tournament`](../../archive/architectures-v2/04-evolutionary-tournament.md), per archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §7 / Appendix):** *"Many parallel candidate implementations from a shared seed; selection pressure via scenario satisfaction; lineage tracking; **explicit model-family diversity to defeat the Hallucination Loop**."* — Tournament is positioned as the *mitigation* for the population-level hallucination problem.
- **The contradiction:** Round-2 names Tournament as *most* vulnerable to F27; the Tournament spec names model-family diversity as its core defense against F1/F27.
- **Design question this sits on:** Whether population-shaped architectures are F27-amplifiers or F27-mitigators.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Decides whether Tournament-style architectures survive a regime declaration test (Round-2 §7.6 sets L4 Automation for Tournament).

### CTR-D4 — F1 (Hallucination Loop) — substrate-mitigable vs. architecture-mitigable
- **Claim 1 (Round-2 §7.5):** F1 sharpened by F27 and *"report 11 §6 (RouterLLM as substrate-level mitigation)"* — substrate-mitigation.
- **Claim 2 (CJ Hess `kevin`/`carl`, report [`34`](../../research/34-lenny-howiai-personal-harnesses.md) §6.2 + F46):** *"Single-Model Review Blindspot"* — same-model self-review fails; cross-model critic catches them. The mitigation is *architectural* (different agent personae running different models), not substrate-level routing.
- **The contradiction:** One framing puts the F1 fix in the routing layer; the other puts it in the agent topology.
- **Design question this sits on:** Substrate-vs-methodology boundary (Phase 4).
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Affects whether judge-independence is enforced at the router or at the orchestration layer.
- **Phase-1 bias-guard sharpening (WEAK-5):** Sharper framing: Anthropic's Auto-Review subagent (report 23 §3.5, five named specialist critics) is a **third position**: F1 is mitigated by same-model-different-role specialization, neither substrate routing nor cross-model topology. This is the position the largest model vendor ships in its own published doctrine. The register treats F1 mitigation as a two-position split; it is a three-position split, and the third position is the one the corpus' deepest substrate-vendor (Anthropic) actually deploys. Why the sharpening matters: Phase-4 substrate-vs-methodology boundary cannot be drawn cleanly between just two F1-mitigation positions. The same-model-different-role position belongs in the register.

### CTR-D5 — F48/F49 (tacit-collusion / discussion-as-amplification) — multi-agent CaMeL closure unknown
- **Claim 1 (Followup [`08`](../../research/followup/08-security-primitives.md) §3):** CaMeL closes the Lethal Trifecta (F12) via typed-interpreter boundary in a **single-agent setting**.
- **Claim 2 (Report [`37`](../../research/37-academic-llm-agent-collusion.md) §8.1; followup [`08`](../../research/followup/08-security-primitives.md) Cluster-O note):** *"the substrate-level guarantee CaMeL provides at the single-agent boundary may not transfer to multi-agent fleets."* F48/F49 sit on the multi-agent generalisation surface.
- **The contradiction:** CaMeL is corpus-canonical as the substrate-level Trifecta closure; report 37's empirical findings imply the closure rule may not extend to the multi-agent fleets every architecture in the corpus assumes.
- **Design question this sits on:** Substrate-level security guarantees for fleets vs. singletons.
- **Mandate relevance:** both
- **Load-bearing impact (high):** Affects whether substrate's security guarantee holds for the parallelism models (Atelier, Tournament) the architectures rely on.

### CTR-D6 — Sycophancy as security primitive vs. Schulhoff's false-presupposition trap
- **Claim 1 (Several defensive patterns, followup [`08`](../../research/followup/08-security-primitives.md) §4.3):** Wrap user input in a security check prompt — *"Detect all instances where the user's input is harmful: {INPUT}"* — as a defensive pattern.
- **Claim 2 (Schulhoff et al., report [`29`](../../research/29-prompt-engineering-survey.md) §5; followup [`08`](../../research/followup/08-security-primitives.md) §4.3):** Verbatim: *"this subtly makes the false presupposition that the user's input is actually harmful. Thus, due to sycophancy, the LLM may be inclined to classify the user's output as harmful."* Followup/08 flags this as *"a direct contradiction to the 'wrap the prompt in a security check' pattern several defensive layers in this report rely on."*
- **The contradiction:** Defensive prompt-wrapping is corpus-recommended *and* corpus-refuted as inducing sycophantic false positives.
- **Design question this sits on:** Substrate-level guard prompts; F12 mitigation pattern.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Affects every architecture's security wrapper design.

### CTR-D7 — Anthropic single-judge finding vs. CTR-D4 cross-model-critic framing (MISSED-1)
- **Claim 1 (Anthropic multi-agent research-system post, via followup [`07`](../../research/followup/07-evals-deepdive.md) §2.3 and §3.6 verbatim):** *"a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements"* — and explicitly: *"For LLM-as-Judge selection, using the same model is usually fine because the judge is doing a different task than your main LLM pipeline."*
- **Claim 2 (CJ Hess `kevin`/`carl`, report [`34`](../../research/34-lenny-howiai-personal-harnesses.md); F46 single-model-review-blindspot; OpenHands RouterLLM mitigation per report [`11`](../../research/11-openhands-substrate-audit.md)):** Same-model self-review is the failure pattern; cross-model critic (carl = Codex/GPT-5.2 reviewing Claude Code) catches what same-model review misses.
- **The contradiction:** Anthropic (the corpus' deepest evals primary) says **same-model judging is fine when the task is different**; CJ Hess/Round-2 say same-model judging is structurally blind. CTR-D4 only captures the substrate-vs-architecture cut of this; it does not register that the corpus is split on whether *judge-model-family independence is even a necessary condition* for the F1/F27 fix.
- **Design question this sits on:** Whether judge-diversity is a substrate primitive (D-7-adjacent) or a methodology preference.
- **Mandate relevance:** both
- **Load-bearing impact (high):** Directly contests whether judge-diversity is a substrate primitive or a methodology preference.

### CTR-D8 — Same-model judge legitimacy vs. F46 / Tournament model-family-diversity (MISSED-2)
- **Claim 1 (followup [`07`](../../research/followup/07-evals-deepdive.md) §3.6 quoting the Husain/Shankar FAQ verbatim):** *"using the same model is usually fine because the judge is doing a different task than your main LLM pipeline. While research has shown that models can exhibit bias when evaluating their own outputs, what ultimately matters is how well your judge aligns with human judgments."*
- **Claim 2 (Tournament spec via archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) Appendix; CTR-D3):** *"explicit model-family diversity to defeat the Hallucination Loop"* — model-family diversity is named as a *necessary* defense.
- **The contradiction:** Husain/Shankar empirically and operationally argue same-model judging is fine if alignment-with-human is measured; Tournament treats model-family diversity as load-bearing. The register flags Tournament-vs-Round-2 (CTR-D3) but not Tournament-vs-Husain/Shankar.
- **Design question this sits on:** F1/F27 mitigation primitive; whether model-family diversity is necessary or contingent.
- **Mandate relevance:** both
- **Load-bearing impact (high):** Sibling to CTR-D4; cleaves the Tournament-design assumption.

---

## E. Empirical / quantitative contradictions (numbers in dispute)

### CTR-E1 — Token spend per engineer — Cherny $100K+/month vs. independent $500–$5000/day
- **Claim 1 (Cherny via Lenny transcript, archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §2.9):** *"$100K+/month per-engineer token spend."*
- **Claim 2 (noosphr HN 46925882, archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §2.9):** *"$500 to $5000 per day per seat"* — at the high end ($5000 × ~22 working days = ~$110K) consistent with Cherny; at the low end ($500 × 22 = $11K) an order of magnitude smaller.
- **The contradiction:** The two corpus-canonical cost anchors disagree by up to 10×; the corpus does not explain whether the variance is workload, model-mix, organization, or methodology.
- **Design question this sits on:** D-5 cost ceilings; substrate's cost-enforcement primitive.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Sets the default cost ceiling the substrate enforces.

### CTR-E2 — Stripe "1,300 agent PRs/week" vs. corpus parallelism ceilings
- **Claim 1 (Nystrom citing Stripe, report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md); third independent corpus confirmation):** Stripe runs *1,300 agent PRs/week* (industrial scale).
- **Claim 2 (Willison cognitive ceiling, archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §2.6; Symphony hard-cap 4 concurrent, archived §3.6):** Practitioner ceilings observed at 4 concurrent agents (Willison) or hard-capped at 4 (Symphony).
- **The contradiction:** Industrial deployment is two-to-three orders of magnitude beyond the named per-practitioner ceilings; the corpus does not reconcile the role-shape (scheduler vs. supervisor) at which the 1,300/week number is achievable.
- **Design question this sits on:** Parallelism ceiling; human role shape; OQ-B7 (organizing axes).
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Sets the substrate's parallelism design center.

### CTR-E3 — CodeRabbit / Veracode / METR numbers — refute lights-out vs. apply differently
- **Claim 1 (Jaymin Ch 9 §7, report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §2c):** CodeRabbit 1.4× critical-issue rate; Veracode 45% OWASP-vulnerable AI code; METR 19% slower than self-estimated. Cited as empirical refutation of L5.
- **Claim 2 (Brief §2.1 footnotes):** Each citation flagged with applicability caveat: CodeRabbit (verify scope, populations, review-protocol equivalence); Veracode (scanning study at code level — applicability to factory-output code with post-cycle V&V is open); METR (applies to *developer-using-agent*, not necessarily *factory-running-agents-on-its-own*).
- **The contradiction:** The numbers are read as *decisive* by Jaymin and as *not-yet-applicable* by the brief's footnote discipline. The same data points support opposite operational conclusions depending on whether their study populations map onto the factory context.
- **Design question this sits on:** OQ-B6 empirical bars; whether Jaymin's thresholds are the right bar set.
- **Mandate relevance:** both
- **Load-bearing impact (high):** If the numbers refute lights-out, the mandate (UC1) must be revised; if they don't, Jaymin's anti-pattern claim weakens.

### CTR-E4 — OpenHands V1 sub-ms persist as substrate-cheap vs. CXDB-or-nothing legacy framing
- **Claim 1 (Round-2 C16, [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §1.1):** *"trajectory capture is a substrate primitive and is now empirically cheap"* — OpenHands V1 sub-ms persist, 7.4ms crash recovery over 433 SWE-Bench Verified replays.
- **Claim 2 (archived [`00-comparison`](../../archive/architectures-v2/00-comparison.md) §7.4 per Round-2 §1.1 reference):** *"CXDB would be the gold standard; cheaper alternatives exist"* — pre-Round-2 framing treats CXDB as the reference and trajectory capture as a nice-to-have.
- **The contradiction:** Round-2's promotion of trajectory capture to substrate primitive contradicts the pre-Round-2 framing that treated it as an optional/aspirational. Both framings still circulate in the corpus.
- **Design question this sits on:** D-7 default (trajectory capture as substrate primitive).
- **Mandate relevance:** both
- **Load-bearing impact (low):** Largely resolved; included for register completeness.

### CTR-E5 — Language-as-harness — Elixir 97.5% vs. ecosystem-churn outweighs (MacGregor paywall tail)
- **Claim 1 (Valim/Tencent via MacGregor, report [`33`](../../research/33-language-choice-as-harness.md)):** *"Elixir 97.5% completion rate across 20 languages; Claude Opus 4 80.3% Elixir vs 74.9% C# vs 72.5% Kotlin."* Implies typed/functional choice is a load-bearing harness lever.
- **Claim 2 (MacGregor paywall-tail telegraph, report [`33`](../../research/33-language-choice-as-harness.md) §"Cliffhanger"):** MacGregor's cliffhanger ("The Training Data Problem" + Yogi Berra epigraph) telegraphs *"ecosystem-churn + training-data abundance dominate in practice"* — counter-claim that language structure may be outweighed by training data volume.
- **The contradiction:** Within MacGregor's own framing, language-as-harness is asserted then qualified; the corpus has the assertion fully drained and the counter-claim only telegraphed (paywall).
- **Design question this sits on:** F45 (language-as-harness mismatch) catalog placement.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Affects whether language choice rises to an ADR-level decision.

### CTR-E6 — CaMeL "~7-point utility tax" empirics vs. lights-out cost / output framing (MISSED-9)
- **Claim 1 (followup [`08`](../../research/followup/08-security-primitives.md) §3, paper-body anchored):** *"77% of tasks with provable security vs. 84% with an undefended system"* — CaMeL imposes a measurable utility tax for substrate-level Trifecta closure.
- **Claim 2 (UC1 lights-out factory + Round-2 §1.1 C13 holdout-discipline-as-substrate; throughput-multiplier framing in report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)):** The substrate-investment thesis is that primitive-level safety is **net-positive** (throughput multiplier). No corpus discussion of the empirical CaMeL utility tax against throughput targets.
- **The contradiction:** The corpus assumes substrate-safety primitives are free or near-free; CaMeL's primary numbers show a 7-point single-pass utility tax (with high per-suite variance per the v2 paper-body fetch). Round-2 elevates substrate-as-cheap; CaMeL is the one substrate-anchored measurement that says **safety has a measurable cost**. (Note: this entry was specified as `CTR-E5` in the bias-guard report; assigned CTR-E6 here because CTR-E5 is already occupied by the language-as-harness entry.)
- **Design question this sits on:** Substrate-cheap thesis (Round-2); D-5 cost ceilings.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Empirical anchor contesting Round-2's "substrate is cheap" thesis.

---

## F. Vocabulary / framing contradictions

### CTR-F1 — "Software factory" (Ford / variance-elimination) vs. "Software company" (Warhol / vision-alignment)
- **Claim 1 (StrongDM / Shapiro / El Kaim corpus, archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) Appendix):** *Software factory* is the canonical frame; *Dark Factory* is the L5 target.
- **Claim 2 (Brier, followup [`12`](../../research/followup/12-brier-pace-layers.md) ¶2 verbatim):** *"I've been incorporating many of StrongDM's concepts about agentic software development into our work at Alephic—but I have one fundamental disagreement: I think factory is the wrong metaphor."* Brier replaces Ford with Warhol; closes: *"It's a software company, not a software factory."*
- **The contradiction:** Brier is *"the only voice in our corpus who has used the StrongDM framework in production and publicly disagrees with its central metaphor"* (followup/12).
- **Design question this sits on:** Whether the v3 artifact name itself is correct; what UC1's *"lights-out software factory"* claim commits to metaphorically.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Reframes Brier's pace-layer alternative; per followup/12 §6 *"Arch 1 (spec-primary contradicted by spec-third) and Arch 4 (selection-without-vision-anchor contradicted by vision-aligned-variance)."*
- **Phase-1 bias-guard sharpening (MISSED-10 — Notion ratification angle):** Nystrom transcript via report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md) §3 has Notion engineers calling Boxy *"both software factory… but I like its internal project name is uh Boxy."* — the most-cited industrial AFIS strategy-3 deployment **adopts the "software factory" framing internally** even while Boxy is the day-to-day name. CTR-F1 omits that the corpus' single strongest industrial primary anchor (Notion/Nystrom) ratifies the factory framing in its own internal vocabulary. This strengthens the factory side of CTR-F1 in a way the register elided.

### CTR-F2 — "Orchestration is the easy part" vs. Round-2 falsification
- **Claim 1 (archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §2.3):** *"orchestration is the easy part; validation is the hard part."*
- **Claim 2 (Round-2 §1.3, [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md)):** *"'orchestration is the easy part' (the synthesis phrasing) is wrong in light of Overstory's 36-subcommand CLI, 4-tier merge resolver, and three-tier watchdog. Orchestration is also hard."*
- **The contradiction:** Round-1 framed validation as the singular hard problem; Round-2 explicitly falsifies that framing.
- **Design question this sits on:** Substrate investment priority.
- **Mandate relevance:** both
- **Load-bearing impact (low):** Largely already-resolved; registered for traceability.

### CTR-F3 — "Persona vs. graph-node" framing (Round-1) vs. Round-2 retired-the-disagreement
- **Claim 1 (archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §3.2):** Pitches persona-based and graph-node-based agent design as competing choices.
- **Claim 2 (Round-2 §2.2, [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md)):** *"retire the disagreement as stated. Replace with a primitive-level claim: 'the substrate must support persona-shaped and graph-node-shaped agent definitions; the architecture chooses which mix to use; the choice is a methodology decision, not a substrate decision.'"*
- **The contradiction:** Round-1 framing treats this as a substrate-level dispute; Round-2 reframes it as a methodology choice on top of a both-shapes substrate.
- **Design question this sits on:** Substrate-vs-methodology boundary.
- **Mandate relevance:** both
- **Load-bearing impact (low):** Reflects framing shift; registered for back-fill audit.

### CTR-F4 — "Spec-malleable / code-archaeological" (lead-agent labels) — Historian-flagged contamination
- **Claim 1 (UC4 prose, [`constraints-extracted`](../constraints-extracted.md)):** The user's prose names the *phenomena*: greenfield is malleable during spec refinement; brownfield is "analyzing what is there and growing it."
- **Claim 2 (Brief §3 footnote ^contamination):** *"The labels 'spec-malleable' and 'code-archaeological' are lead-agent shorthand for UC4's longer prose… they are now anchor terms that downstream tracks could inherit."* Historian flagged contamination risk.
- **The contradiction:** The labels compress the user's claim accurately but anchor downstream framing in ways that could mismatch the underlying claim.
- **Design question this sits on:** UC4 hypothesis testing; ensuring tracks challenge the claim, not the labels.
- **Mandate relevance:** both
- **Load-bearing impact (low):** Process discipline; not architecturally load-bearing on its own.

---

## G. Brownfield-specific contradictions

### CTR-G1 — Maintenance vs. greenfield asymmetry (F20) — corpus admits but does not resolve
- **Claim 1 (El Kaim per F20, archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §4):** *"Most agent demos are greenfield; the dark factory only proves itself if it can sustain a living codebase."*
- **Claim 2 (Corpus default architectures, archived [`00-comparison`](../../archive/architectures-v2/00-comparison.md)):** All four v2 architectures are mandate-agnostic in their spec but greenfield-leaning in their exemplars (StrongDM new product; Compound Atelier issue-queue; Foundry phase-gate greenfield; Tournament population from seed).
- **The contradiction:** The corpus *acknowledges* the brownfield asymmetry as a failure mode and then proceeds to design as if it doesn't exist.
- **Design question this sits on:** UC2 brownfield as co-equal mandate; the entire v3 reframe.
- **Mandate relevance:** brownfield
- **Load-bearing impact (high):** Justifies the entire mandate-fit matrix discipline (D2).

### CTR-G2 — Scenario authorship: out-of-tree (StrongDM) vs. inherited-from-codebase (brownfield default)
- (See CTR-B5; cross-listed here because the contradiction's *brownfield-load-bearing* angle is distinct from its substrate-default angle.)
- **Mandate relevance:** brownfield
- **Load-bearing impact (high):** Brownfield substrate may need to invert D-2.

### CTR-G3 — Cold-start (greenfield) vs. legacy-ingestion (brownfield) — symmetric or asymmetric?
- **Claim 1 (Brief §5, promoted from OQ-B5):** Cold-start is *the load-bearing risk of the greenfield mandate.* Required dedicated synthesis section.
- **Claim 2 (Implicit in UC4 / D1 brownfield tracks):** Legacy-ingestion is the *symmetric* problem for brownfield (the equivalent of cold-start: how does the factory start when day-0 priors look different).
- **The contradiction:** The brief promotes cold-start as a load-bearing concern but leaves legacy-ingestion at OQ-B4 framing only. The two problems may or may not be symmetric; the corpus does not establish this.
- **Design question this sits on:** Whether legacy-ingestion deserves equal-weight mandatory treatment in brownfield tracks.
- **Mandate relevance:** brownfield
- **Load-bearing impact (medium):** Affects Phase-2 brownfield-track briefs.

### CTR-G4 — Code-as-opaque-weights (StrongDM) vs. brownfield-code-as-readable-archaeology (UC4)
- **Claim 1 (StrongDM `/principles`, report [`01`](../../research/01-strongdm-factory.md); archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §0 revision notes):** *"correctness is inferred exclusively from externally observable behavior"* — code as opaque ML weights.
- **Claim 2 (UC4, [`constraints-extracted`](../constraints-extracted.md)):** Brownfield is *"code-archaeological + existing-architecture-as-given"* — the factory must read, analyze, and grow the existing code as a primary input.
- **The contradiction:** StrongDM's discipline treats code as opaque output; UC4's brownfield mandate requires treating code as primary, readable, archaeological input.
- **Design question this sits on:** Whether the same substrate can serve both reading-disciplines.
- **Mandate relevance:** brownfield
- **Load-bearing impact (high):** Decides whether brownfield needs substrate primitives StrongDM-derived architectures lack (code-reading agents, codebase-traversal tools, dependency mapping).

---

## H. Other / uncategorized

### CTR-H1 — Tournament's selection-driven validation vs. Healer's diagnostic-clustering
- **Claim 1 (Tournament architecture, archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) Appendix):** Validation = selection pressure over a population of candidates.
- **Claim 2 (Shapiro companion post, Healer mechanism, followup [`01`](../../research/followup/01-shapiro-five-levels.md) §"Companion post"):** Validation = diagnostic clustering by Healer agent + investigation agents + prescription agents.
- **The contradiction:** Two corpus-supported mechanisms for "validation replaces review" rely on different topologies (population-of-candidates vs. observation-and-prescription). Both claim Shapiro endorsement, but only Healer is described in Shapiro's voice.
- **Design question this sits on:** Validation primitives; F1/F27 mitigation pattern.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Affects which validation primitives the substrate must support.

### CTR-H2 — Knowledge eagerly captured (Compound) vs. lazily logged (CXDB)
- **Claim 1 (Compound Engineering, archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §3.4):** Knowledge captured *eagerly* — `/ce-compound` auto-invoked on phrases like *"that worked"*.
- **Claim 2 (CXDB, StrongDM, archived §3.4):** Knowledge captured *lazily* — everything logged, queried on demand.
- **The contradiction:** Two corpus-endorsed approaches to the knowledge-accumulation primitive.
- **Design question this sits on:** Knowledge-store substrate primitive; D-7 (trajectory capture) interaction.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Affects substrate design for knowledge accumulation between cycles.

### CTR-H3 — Compound Knowledge's inline-staleness vs. Compound Engineering's batch-refresh
- **Claim 1 (Compound Engineering ce-compound-refresh, followup [`11`](../../research/followup/11-compound-knowledge.md) §"Important divergence"):** Weekly batch refresh cadence; five outcomes (Keep / Update / Consolidate / Replace / Delete).
- **Claim 2 (Compound Knowledge plugin, followup [`11`](../../research/followup/11-compound-knowledge.md)):** Folds staleness check *into every kw:compound invocation* via stale-knowledge-checker agent; three outcomes.
- **The contradiction:** Two same-family plugins (Every.to lineage) take opposite stances on whether contradiction-detection is per-write or batch.
- **Design question this sits on:** Knowledge-curator substrate primitive design.
- **Mandate relevance:** both
- **Load-bearing impact (low):** Methodology-layer divergence; both are workable.

### CTR-H4 — Per-employee Claw fleets (Glowforge) vs. cognitive-ceiling caps
- **Claim 1 (Shapiro Claw post, report [`32`](../../research/32-shapiro-completion-chat-agent-claw.md) §6):** *"claw-printer / one-Claw-per-employee"* — Glowforge "printing claws by the dozen: one for every coworker, one for every department, one for every special project."
- **Claim 2 (F5 cognitive ceiling, archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §4):** *"One human supervising parallel agents loses signal by mid-morning."*
- **The contradiction:** "Per-employee Claw fleet" suggests each human supervises N Claws; cognitive ceiling caps the N that any single human can supervise. The two corpus claims are not formally contradictory but pull in different directions — the corpus does not reconcile how the fleet-per-employee model survives F5.
- **Design question this sits on:** Org-design primitive vs. F5 mitigation.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Affects substrate's per-human parallelism caps.
- **Phase-1 bias-guard sharpening (MISSED-7):** Report [`36`](../../research/36-sendbird-quests-token-tiers.md) §3 has already crossed the threshold from "fleet of N per human" to "human is graded on aggregate fleet output (tokens) with smoothness as the autonomy proxy" — six-tier daily-token leaderboard *"Beginner (<1M tokens/day) → AI God (>100M/day)"*; goal is curve-smoothness (smooth = AI works 24/7); the *executives should be top token consumers*. Sendbird operationalizes **token-spend-per-person as a positive-direction org metric** while CTR-E1 frames Cherny's number as a cost ceiling and F5 frames per-human attention as a hard scarce resource. This inverts F5's framing. See CTR-H12 (new entry).

### CTR-H5 — BCG ("structurally easier to audit") vs. Kahana ("tracing difficult by design")
- **Claim 1 (BCG, followup [`10`](../../research/followup/10-governance.md) §6):** Agentic-coded artifact production is *structurally easier to audit* (versioned audit trail, scenarios outside tree, per-action logs).
- **Claim 2 (Kahana, followup [`10`](../../research/followup/10-governance.md) §6 + Cognitive Escrow report [`30`](../../research/30-cognitive-escrow.md)):** *"tracing difficult by design"* — no industry standard, no audit methodology, no procurement checklist.
- **The contradiction:** Followup/10 §6 explicitly notes: *"BCG's 'structurally easier' claim and Kahana's 'tracing difficult by design' claim are not directly contradictory — they describe different layers."* The corpus flags this as a tension to register: artifact production vs. artifact recognition by regulators.
- **Design question this sits on:** Audit-trail substrate primitive; what it must produce for regulator recognition.
- **Mandate relevance:** brownfield (regulator-facing) more than greenfield, but both
- **Load-bearing impact (medium):** Affects Foundry-style regulated-domain pitch.

### CTR-H6 — Mandates "should produce different architectures" (UC2) vs. "same primitives expressing both" (D1 unified tracks)
- **Claim 1 (UC2, [`constraints-extracted`](../constraints-extracted.md)):** *"Greenfield and brownfield can be totally different solutions."*
- **Claim 2 (D1 unified tracks, [`decisions-captured`](../decisions-captured.md)):** *"3 both-mandates tracks (no-axis-prescribed) — each tasked to produce ONE architecture that addresses both mandates."*
- **The contradiction:** UC2 permits divergence; D1 explicitly searches for convergence. Both are present in the user-given constraint set; the brief acknowledges both, but they pull in different directions for the v3 search.
- **Design question this sits on:** Hypothesis falsifiability (UC4 + D1); architecture-count outcome.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Process discipline; affects how Phase-3 merge reconciles the 9 tracks.

### CTR-H7 — Schillace's "code review as firing offense" vs. corpus reviewing-discipline consensus
- **Claim 1 (Schillace, report [`28`](../../research/28-schillace-sunday-letters.md) §"Surprises and contradictions"):** *"code review as firing offense"* anecdote — Schillace explicitly contradicts default human-team practice.
- **Claim 2 (Compound Engineering / Refinery / Foundry / Willison):** All assume code review is a primary engineering discipline. Foundry makes it gate-driven.
- **The contradiction:** Schillace's stance (review-as-firing-offense) is at the far end of a corpus spectrum that has Willison naming unreviewed code as the anti-pattern.
- **Design question this sits on:** Where review sits in regime classification (L3 vs. L4 vs. L5).
- **Mandate relevance:** both
- **Load-bearing impact (high)** (raised from medium per Phase-1 bias-guard MISSED-4)**:** Augments CTR-A3 with a third stance (Schillace).
- **Phase-1 bias-guard sharpening (MISSED-4):** CTR-H7 omits **the most-load-bearing counter-claim**: the two largest substrate vendors have made automated code-review-by-a-distinct-agent a *first-class substrate primitive*. Anthropic S15 (report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5) ships five specialized critics (duplicate-code coalescer / compiler-performance / efficiency / Rust code-quality critic / documentation); OpenAI ships a substrate-resident Auto-Review subagent (report [`18`](../../research/18-openai-codex-substrate.md)). Schillace's framing is not just at odds with practice — it is at odds with substrate. See CTR-H13 (new entry) for the substrate-vendor angle as a distinct contradiction.

### CTR-H8 — Brief §4.1 D-2 ("scenarios outside codebase") fragility — universal vs. brownfield-inverted
- (See CTR-B5; cross-listed.)

### CTR-H9 — Compound Atelier as baseline (Round-2 §7.2) vs. UC6 ❌ "Compound Atelier as baseline"
- **Claim 1 (Round-2 §7.2, [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md)):** *"Methodology baseline: Architecture 2 (Compound Atelier), with the harness/scaffold split made explicit."*
- **Claim 2 ([`constraints-extracted`](../constraints-extracted.md) "What is explicitly NOT a constraint"):** *"❌ 'Compound Atelier as baseline' (00-comparison §7.1)"* — explicitly named as a lead-agent recommendation, not a user constraint.
- **The contradiction:** Round-2 synthesis converged on a baseline that the v3 framing explicitly demotes from constraint-level.
- **Design question this sits on:** Phase-7 back-fill; whether the Round-2 baseline survives v3-from-scratch.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Process — but materially affects Phase-7 absorption decisions.

### CTR-H10 — "L3 Augmentation as 2026 ceiling" (Round-2 §2.1) vs. UC1 lights-out mandate
- **Claim 1 (Round-2 §2.1 / §6.2 / §7.6):** *"nothing in the 2026 evidence supports L5 anywhere except as a research aspiration"*; declares L3 Augmentation as the regime for 3 of 4 architectures.
- **Claim 2 (UC1, [`constraints-extracted`](../constraints-extracted.md)):** *"a running lights-out software factory"* — explicitly L4+ by glossary §0 mapping (or undecided per CTR-A4).
- **The contradiction:** Round-2's empirical-ceiling claim and UC1's lights-out mandate cannot both hold unless the vocabulary-mapping (CTR-A4) dissolves the L5/lights-out identity. Brief explicitly flags this: *"❌ 'L3 Augmentation as the empirical 2026 ceiling' — this is a corpus claim worth testing against the lights-out mandate, not a user constraint."*
- **Design question this sits on:** Direct restatement of OQ-B1.
- **Mandate relevance:** both
- **Load-bearing impact (high):** The mandate itself is at stake.
- **Phase-1 bias-guard sharpening (WEAK-4):** Sharper framing: Round-2 §7.6 actually classifies architectures across L3 and L4 (not "all at L3"); the contradiction is more precisely *"nothing in 2026 evidence supports L5 anywhere except as a research aspiration"* — which means Round-2's ceiling claim is **L5-anti**, not **L3-only**. If UC1 lights-out maps to L4 (per glossary §0), the Round-2 ceiling is **compatible** with UC1 lights-out. CTR-H10 conflates "ceiling is L3" with "ceiling excludes L5," and these have different downstream implications. Why the sharpening matters: The contradiction may dissolve at the L4-vs-L5 mapping rather than at the L3-vs-L4 mapping. CTR-A4 (vocabulary mapping) is the actual decisive contradiction; CTR-H10 should be subordinate to CTR-A4, not parallel to it.

### CTR-H12 — Sendbird per-employee token-tier visibility vs. F47 Goodhart + Cherny per-engineer $100K (MISSED-7)
- **Claim 1 (report [`36`](../../research/36-sendbird-quests-token-tiers.md) §3 verbatim):** Six-tier daily-token leaderboard *"Beginner (<1M tokens/day) → AI God (>100M/day)"*; **goal is curve-smoothness (smooth = AI works 24/7)**; the *executives should be top token consumers*.
- **Claim 2 (CTR-E1 Cherny $100K+/month token spend; F5 cognitive ceiling — archived synthesis §4):** Cherny's industrial-grade token spend per engineer (~$100K+/month); Willison's exhaustion-by-11am cognitive ceiling at 4 agents.
- **The contradiction:** Sendbird operationalizes **token-spend-per-person as a positive-direction org metric** (smoother curve = better) while CTR-E1 frames Cherny's number as a cost ceiling and F5 frames per-human attention as a hard scarce resource. The contradictions register notes CTR-H4 ("Per-employee Claw fleets vs. cognitive-ceiling caps") but **fails to register that report 36 has already crossed the threshold from "fleet of N per human" to "human is graded on aggregate fleet output (tokens) with smoothness as the autonomy proxy."** This inverts F5's framing.
- **Design question this sits on:** Org-design first-principle (CTR-H4 + CTR-E1 cluster); F5 (cognitive ceiling) reframing.
- **Mandate relevance:** both
- **Load-bearing impact (medium-high):** Surfaces that the corpus' Theme-5 measurement primitive (curve-smoothness) directly competes with F5 (cognitive ceiling) as the org-design first-principle.

### CTR-H13 — Schillace's "code review as firing offense" vs. Anthropic Auto-Review + Codex Auto-Review substrate primitive (MISSED-4)
- **Claim 1 (Schillace, report [`28`](../../research/28-schillace-sunday-letters.md) §"Surprises and contradictions"; restated as CTR-H7):** *"code review as firing offense"* — code review treated as anti-pattern at the team-shape layer.
- **Claim 2 (Anthropic S15 / report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5; Codex Auto-Review subagent, report [`18`](../../research/18-openai-codex-substrate.md)):** Both Anthropic and OpenAI ship **named substrate-level Auto-Review agents** — Anthropic's five specialized critics (duplicate-code coalescer / compiler-performance / efficiency / Rust code-quality critic / documentation), OpenAI's substrate-resident Auto-Review subagent.
- **The contradiction:** The two largest substrate vendors have made automated code-review-by-a-distinct-agent a *first-class substrate primitive*. Schillace's framing is not just at odds with practice — it is at odds with substrate. (Note: this entry was specified as `CTR-H11` in the bias-guard report; assigned CTR-H13 here because CTR-H11 is already occupied by "Code is fashion now" vs "low-background steel" entry.)
- **Design question this sits on:** Substrate-vs-methodology boundary on the review primitive.
- **Mandate relevance:** both
- **Load-bearing impact (high):** Forces the v3 set to choose between two corpus-popular positions (Schillace's team-shape doctrine vs. substrate-resident auto-review).

### CTR-H11 — "Code is fashion now" (Brier) vs. "low-background steel" (Willison)
- **Claim 1 (Brier pace layer 1, followup [`12`](../../research/followup/12-brier-pace-layers.md)):** *"in a world of AI, code is free to produce and reproduce."* Fastest layer; high churn expected.
- **Claim 2 (Willison "low-background steel" framing, report [`05`](../../research/05-simon-willison.md)):** Pre-2022 code is uniquely valuable for being un-contaminated by AI-generation; treating code as durable, scarce, irreplaceable.
- **The contradiction:** Two near-contemporary practitioners frame code's *nature* incompatibly — fashionable/regenerable vs. durable/irreplaceable.
- **Design question this sits on:** Whether code is a build-output or a corpus-input for the factory.
- **Mandate relevance:** both
- **Load-bearing impact (medium):** Affects brownfield treatment of legacy code as input.

---

## Soft candidates (not registered as primary contradictions; flagged for later assessment)

- **CXDB-or-equivalent observability tier vs. NDJSON event-tailer.** Both are corpus-endorsed; the framing differs on whether content-addressed storage and BLAKE3 CAS are load-bearing or convenience.
- **Workpad-per-issue (Symphony / Atelier) vs. bead-per-unit (Gas systems).** Different durable-state primitives for the same role; neither author flags them as competing.
- **Per-cycle ceremony tiers (Lightweight / Standard / Deep) vs. regime-classified architectures (Round-2 §7.6 table).** Two scaling dimensions; corpus has not pitched them as alternatives.
- **`AGENTS.md` vs. `CLAUDE.md` vs. `agents.md` discoverability.** Naming-only divergence (Round-2 C11 treats them as scaffold class); no semantic contradiction surfaced.

---

## Coverage notes

- **Total contradictions registered:** 49 (CTR-A1–A6, CTR-B1–B7, CTR-C1–C7 + C9–C11, CTR-D1–D8, CTR-E1–E6, CTR-F1–F4, CTR-G1–G4, CTR-H1–H13; plus 4 soft candidates). Phase-1 bias-guard integration 2026-05-23 added 11 MISSED contradictions (mostly Section C/D/H), sharpened 5 WEAK entries, and surfaced two diagnostic patterns: post-Round-9 reports were systematically under-mined in the original register; contradictions weakening Round-2's substrate-cheap thesis were absent. Both patterns are now addressed by the new entries. Two MISSED entries (MISSED-4, MISSED-9) were assigned different CTR-IDs than the bias-guard report's recommendation because the recommended IDs (CTR-H11, CTR-E5) were already occupied; reassigned to CTR-H13 and CTR-E6.
- **Coverage gaps (areas where more contradictions likely exist but were not exhaustively chased):**
  - **El Kaim book corpus (reports 14–17, 24).** Read only at INDEX-anchor depth. The corpus has flagged 8 El Kaim-vs-Shapiro divergences via PLAN.md §6.1; only 2–3 are explicitly registered here (CTR-A2, CTR-B3). The other 5+ specific paraphrase divergences (L0 outrun-by-people, L1 speedup line, L2 90%-vs-most, NHTSA framing gloss, StrongDM team-size attribution) are listed verbatim in followup/01 §"El Kaim vs. Shapiro discrepancies" but not all individually registered here as they are largely textual fidelity issues rather than architectural contradictions.
  - **Cisco/LangChain pilot data (report 12 §2.2)** — numbers cited by Round-2 as validation; not stress-tested for contradiction against other pilots.
  - **Anthropic engineering trilogy (report 23)** — Skill-budget claims, sandboxing primary docs; not exhaustively cross-checked against OpenHands SecurityAnalyzer / Codex `.rules` DSL.
  - **Brier vs. compound-engineering** — Brier's pace-layer model is contradicted partially by compound-engineering's auto-curation discipline; only CTR-F1 surfaced this in headline form.
  - **Gas systems (reports 38, followups 13/14)** — substrate-level audit went deep; methodology-layer contradictions with Dark Factory's 12 principles are flagged in report 38 §6 but mostly mapped, not contradiction-named.
  - **Followup/14 BCG-vs-Kahana further regulatory contradictions.** CTR-H5 surfaces the main tension; finer SB-53 / SEC-IAC mismatches in report 31 not individually registered.
  - **El Kaim's "Continuous Enterprise Architecture" 12 principles** vs. Round-2 substrate primitives — only spot-checked.
  - **Schulhoff §5 prompt-engineering issues (report 29)** — taxonomy of failure modes (sensitivity, sycophancy, bias, ambiguity, prompt-hacking) was scanned; only CTR-D6 registered the sycophancy-vs-defensive-wrap contradiction explicitly.

- **Distribution by mandate-relevance:** `both` = 30; `brownfield` = 4; `greenfield` = 1 (CTR-B2); register-level mandate-tagging skews `both` because most architectural-level contradictions affect both mandates differently rather than one exclusively.

- **Distribution by load-bearing impact:** `high` = 16; `medium` = 17; `low` = 5.

- **Top 3 by load-bearing impact (for the orchestrator's onward report):**
  1. **CTR-A1 / CTR-A4 / CTR-H10** (the L5-vs-lights-out cluster) — directly contests the v3 mandate.
  2. **CTR-C2** (substrate-heavy + thin-methodology vs. UC4 "different solutions") — decides whether the 3 D1 unified tracks have a target architecture to find.
  3. **CTR-B3 / CTR-F1** (spec-primary vs. spec-third-under-pace-layers; factory vs. company metaphor) — Brier vs. corpus consensus contests both the metaphor and the artifact stack ordering of the entire v3 design.

*End of contradictions.md.*
