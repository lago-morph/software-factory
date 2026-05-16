# Report 25 — Requirements Engineering & Systems Engineering Foundations

**Date:** 2026-05-16
**Author:** Subagent A (manual-drain dispatch)
**Status:** ✅ complete

**Update note (2026-05-16, Cluster N drain).** Report 35 (Ryan Nystrom / Notion) adds the corpus' first industrial primary-source anchor for **AFIS strategy-3 at non-aerospace scale**. The Notion pattern — Markdown spec files checked into the repo's `agent specs` subfolder, Codex implementing/verifying/shipping against them, *the spec's git version history as the changelog* — is an alternative path to AFIS §6.3 strategy-3 that bypasses the tool-locked-model machinery (Cameo, Rhapsody, El Kaim Chapter 8 typed objects). Both paths achieve "model is source of truth"; they differ on substrate. The Notion path is *across*, not *up*: plain Markdown + Git + agent-as-reader/writer. The framing pinned in §6.3 ("Strategy 3 is the El Kaim Chapter 8 endpoint") should be refined: strategy-3 can be reached *up* (El Kaim typed objects) **or** *across* (Notion Markdown + agent). See report 35 §2 for the full Notion anchor.

## Lead question

What does the requirements engineering and systems engineering tradition contribute to spec authorship discipline in AI-augmented software development — specifically, which primary-source mechanics (EARS syntax, INCOSE SE definitions, INCOSE Guide-to-Writing-Requirements rules, systems-engineering complexity framings, the requirements-vs-architecture distinction in modelling) should be reflected in the methodology layer of the software factory?

---

## 1. Why this report exists

Report 14 (`14-el-kaim-book-intent-and-spec-authorship.md`) drained Vincent El Kaim's 9-field structured-intent model and made one large bet: that the *form* of a well-formed enterprise spec — typed fields, explicit non-goals, declared invariants, decision seeds — is what holds AI-augmented delivery together. El Kaim's discipline is the descendant artifact. This report drains the ancestor tradition that artifact stands on: the requirements engineering (RE) and systems engineering (SE) primary sources whose 30–50 years of practice converged on the *same* form for the *same* reasons, long before LLMs entered the picture. Where followup/09 (`followup/09-methodology-ancestors.md`) anchored methodology to Kaner, Rumelt, and Deming — quality, strategy, learning — this report anchors the *specification artifact itself* to its INCOSE and EARS origins.

The motivating observation: every load-bearing distinction in El Kaim Chapter 8 (intent vs. policy vs. design decision vs. specification vs. constraint) and every characteristic he asks of a well-formed spec (unambiguous, singular, verifiable, traceable, feasible) is a direct restatement of INCOSE's Guide to Writing Requirements v4 (GtWR) characteristics C1–C15 and the AFIS *Requirements and Architecture within Modelling Context* white paper's three RE goals. The vocabulary El Kaim uses is the systems engineering vocabulary, with the underlying tradition unmarked. This report marks it.

Four primary sources are drained: (i) Alistair Mavin's canonical EARS guide; (ii) INCOSE TP-2020-002-06 *Systems Engineering and System Definitions*; (iii) the INCOSE Requirements Working Group's GtWR v4 summary sheet; (iv) INCOSE TP-2021-007-01 *A Complexity Primer for Systems Engineers*; (v) the AFIS/INCOSE-FR 2016 white paper *Requirements and Architecture within Modelling Context*.

---

## 2. EARS — the smallest viable requirement grammar

### 2.1 The grammar in Mavin's own words

EARS (Easy Approach to Requirements Syntax) is, in the author's framing, "a mechanism to gently constrain textual requirements. The EARS patterns provide structured guidance that enable authors to write high quality textual requirements." It was developed by Alistair Mavin and colleagues at Rolls-Royce while extracting requirements from airworthiness regulations for a jet-engine control system, "first published in 2009 and has been adopted by many organisations across the world" — Airbus, Bosch, Dyson, Honeywell, Intel, NASA, Rolls-Royce, Siemens.

The generic syntax is verbatim:

> *While \<optional pre-condition\>, when \<optional trigger\>, the \<system name\> shall \<system response\>*

The EARS ruleset states that a requirement must have: **zero or many preconditions; zero or one trigger; one system name; one or many system responses**. Five patterns fall out of which clauses are present.

### 2.2 The five patterns, verbatim

1. **Ubiquitous** (always active, no keyword): *The \<system name\> shall \<system response\>.*
    Example: "The mobile phone shall have a mass of less than XX grams."
2. **State driven** (keyword **While**): *While \<precondition(s)\>, the \<system name\> shall \<system response\>.*
    Example: "While there is no card in the ATM, the ATM shall display 'insert card to begin'."
3. **Event driven** (keyword **When**): *When \<trigger\>, the \<system name\> shall \<system response\>.*
    Example: "When 'mute' is selected, the laptop shall suppress all audio output."
4. **Optional feature** (keyword **Where**): *Where \<feature is included\>, the \<system name\> shall \<system response\>.*
    Example: "Where the car has a sunroof, the car shall have a sunroof control panel on the driver door."
5. **Unwanted behaviour** (keywords **If/Then**): *If \<trigger\>, then the \<system name\> shall \<system response\>.*
    Example: "If an invalid credit card number is entered, then the website shall display 'please re-enter credit card details'."

Complex requirements combine the patterns: *"While the aircraft is on ground, when reverse thrust is commanded, the engine control system shall enable reverse thrust."*

### 2.3 What EARS actually buys

Three things, in Mavin's framing. First, **temporal ordering** — "the clauses always appeared in the same order" — which means parsers (human or machine) decode the requirement deterministically. Second, **scoped responsibility** — every pattern names *the system* explicitly as subject, making the responsible entity unambiguous. Third, **lightweight adoption** — "no specialist tool is necessary, and the resultant requirements are easy to read" — which is the cheap-substrate property that lets the discipline propagate without organisational change.

The non-trivial absence: EARS does not cover *non-functional* requirements (performance, security, durability) cleanly. The Ubiquitous pattern absorbs them, but the grammar's leverage on triggers and pre-conditions is mostly a behavioural-spec leverage. This matters for the software factory because most LLM-generated code is behavioural, but a substantial fraction of failure modes (F12 lethal trifecta, F33 adversarial-prompt defeat, F4 silent quality regression) are non-functional.

### 2.4 Implication for the software factory

The software factory has no canonical grammar for acceptance criteria. `spec-driven-ai-dev.md` Layer 3 prose can be anything from Gherkin to free English. Report 12 §3 already flagged EARS as "directly relevant to our `spec-driven-ai-dev.md` baseline" but did not pull the patterns through. The five patterns are the smallest known grammar that lets an LLM emit deterministic acceptance criteria and lets a downstream judge evaluate them deterministically. The candidate methodology move is: **mandate EARS for the acceptance-criteria field of any spec Layer 3 block; allow free prose only in the rationale and statement fields** (which map to El Kaim's `statement` field, where "executive language… cannot be reduced to structured fields without loss"). This is a Layer-3 substrate decision, not a methodology-wide one.

---

## 3. INCOSE Guide to Writing Requirements v4 — the rule set behind El Kaim

INCOSE-TP-2010-006-04 (June 2023, Summary Sheet) is the canonical primary source for *how* to write a well-formed requirement statement. The full document is a 270-page guide; the summary sheet (7 pages) compresses the 15 characteristics, 42 rules, and 49 attributes into one reference. Three pieces of it are load-bearing for our corpus.

### 3.1 The 15 characteristics of well-formed needs/requirements

GtWR distinguishes characteristics of an *individual* statement (C1–C9) from characteristics of a *set* (C10–C15). Verbatim definitions for the load-bearing nine:

- **C1 Necessary** — "defines capability, characteristic, constraint, or quality factor needed or required to satisfy a lifecycle concept, need, source, or higher-level requirement."
- **C2 Appropriate** — "specific intent and amount of detail of the need or requirement statement is appropriate to the level (the level of abstraction, organization, or system architecture)."
- **C3 Unambiguous** — "must be stated such that their intent is clear and can be interpreted in only one way by all intended audiences."
- **C4 Complete** — "sufficiently describes the necessary capability, characteristic, constraint, conditions, or quality factor."
- **C5 Singular** — "should state a single capability, characteristic, constraint, or quality factor."
- **C6 Feasible** — "can be realized within entity constraints (for example: cost, schedule, technical, legal, ethical, safety) with acceptable risk."
- **C7 Verifiable** — "structured and worded such that its realization can be verified to the approving authority's satisfaction."
- **C8 Correct** — "must be an accurate representation of the need, source, or higher-level requirement from which it was transformed."
- **C9 Conforming** — "should conform to an approved standard pattern and style guide."

For sets: **C10 Complete**, **C11 Consistent** ("does not conflict with or overlap with others in the set; makes use of homogeneous units… are developed using a consistent language (that is, the same words are used throughout the set to mean the same thing)"), **C12 Feasible**, **C13 Comprehensible**, **C14 Able to be validated**, **C15 Correct**.

The mapping to El Kaim Ch3 §4.1 is one-to-one for the load-bearing fields:

| El Kaim field | GtWR characteristic the field protects |
|---|---|
| Identity / metadata | C9 Conforming, plus enables traceability |
| Statement (one prose field) | C3 Unambiguous, C8 Correct |
| Business outcomes (metric + baseline + target) | **C7 Verifiable** — this is the entire reason outcomes need numbers |
| Capability scope | C2 Appropriate |
| Policy references (catalog IDs) | C11 Consistent (same name same thing) |
| Invariants | C1 Necessary, C7 Verifiable (compile to executable Rego) |
| Non-goals | C3 Unambiguous (close the gap "silence is permission") |
| Decision seeds | C4 Complete (forces the unknown to be named, not buried) |
| Guardrails (must-not-break metrics) | C7 Verifiable for the negative case |
| Feedback sources | C14 Able to be validated post-deployment |

El Kaim re-derives, from enterprise architecture frustration, the same nine characteristics INCOSE derived from systems engineering frustration. The artifact converges because the failure modes converge.

### 3.2 The 42 rules — the ones with direct LLM-era purchase

GtWR enumerates 42 rules clustered into 13 quality-focus categories (Accuracy, Concision, Non-ambiguity, Singularity, Completeness, Realism, Conditions, Uniqueness, Abstraction, Quantifiers, Tolerance, Quantification, Uniformity of Language, Modularity). The rules most directly load-bearing for AI-augmented authoring:

- **R1 Structured Statements** — "Need and requirement statements must conform to one of the agreed patterns." This is the rule that mandates EARS (or equivalent). Without R1, every other rule is negotiable.
- **R2 Active Voice** — "Use the active voice in the need or requirement statement with the responsible entity clearly identified as the subject of the sentence."
- **R4 Defined Terms** — "Define all terms used… within an associated glossary and/or data dictionary." The rule LLM authoring most reliably violates: the model invents a term, uses it consistently, and the team adopts it without realising no one defined it.
- **R7 Vague Terms** — forbids "some, any, allowable, several, many, a lot of, a few, almost always, very nearly, nearly, about, close to, almost, approximate" and "ancillary, relevant, routine, common, generic, significant, flexible, expandable, typical, sufficient, adequate, appropriate, efficient, effective, proficient, reasonable, customary." The longest blacklist in the guide and the one LLM output most needs linted.
- **R8 Escape Clauses** — forbids "so far as is possible, as little as possible, where possible, as much as possible, if it should prove necessary, if necessary, to the extent necessary, as appropriate, as required, to the extent practical, if practicable."
- **R9 Open-Ended Clauses** — forbids "including but not limited to, etc., and so on."
- **R16 Use of 'Not'** — negative statements are harder to verify; phrase positively.
- **R18/R19 Single Thought / Combinators** — forbids "and, or, then, unless, but, as well as, but also, however, whether, meanwhile, whereas, on the other hand, otherwise" because each combinator hides a compound requirement.
- **R20 Purpose Phrases** — rationale belongs in the rationale attribute, not in the statement.
- **R26 Absolutes** — "Avoid using unachievable absolutes such as 100% reliability, 100% availability, all, every, always, never."
- **R30 Unique Expression** — "Express each need and requirement once and only once."
- **R31 Solution Free** — "Avoid stating implementation in a need statement or requirement statement." The requirements-vs-architecture line of §5.
- **R35 Temporal Dependencies** — forbids "eventually, until, before, after, as, once, earliest, latest, instantaneous, simultaneous, at last."

R7, R8, R9, R26, R35 collectively define a *static lint pass* that can run against any AI-authored requirement at zero marginal cost. Compare El Kaim's OPA/Rego "Role 1 — Meta-validation of the intent artifact itself" (report 14 §5): GtWR R7–R35 is the *vocabulary-level* meta-validation that complements the *cross-reference-level* meta-validation El Kaim describes.

### 3.3 The 49 attributes — what travels with a requirement

GtWR also enumerates 49 attributes that should accompany a requirement statement. The minimum set (asterisked in the guide) is: **A1 Rationale, A2 Trace to Parent, A3 Trace to Source, A5 Allocation/Budgeting, A6 Verification Success Criteria, A7 V&V Strategy, A8 V&V Method, A9 V&V Responsible Organization, A15 Unique Identifier, A17 Originator/Author, A19 Owner, A28 Verification Status, A29 Validation Status, A34 Priority, A35 Criticality, A36 Risk.**

Three attribute clusters not currently in our spec template:
- **Verification (A6–A14)** — success criteria, strategy, method, responsible org, level, phase, condition of use, results, status. We have acceptance criteria; we do not separately record *who runs them, when, against what condition, with what result history*. (Reports 09 §3 and 23 §5 implicitly invoke this when discussing test harnesses.)
- **Product-line attributes (A47–A49)** — Product Line, Product Line Common Needs and Requirements, Product Line Variant Needs and Requirements. Report 24 (El Kaim Ch9) anchored the product-line discussion; GtWR shows the field-level vocabulary is already standardised.
- **Stability (A26)** — Stability/Volatility. The methodology corpus implicitly tracks this through layer drift; GtWR makes it a first-class attribute.

---

## 4. INCOSE Systems Engineering definitions — the framing layer

INCOSE-TP-2020-002-06 (8 January 2019) is the Fellows Initiative output that fixed INCOSE's *current* definitions of "system" and "systems engineering." The relevant primary text:

### 4.1 The two canonical definitions

> **Systems Engineering** is a transdisciplinary and integrative approach to enable the successful realization, use, and retirement of engineered systems, using systems principles and concepts, and scientific, technological, and management methods.

> An **engineered system** is a system designed or adapted to interact with an anticipated operational environment to achieve one or more intended purposes while complying with applicable constraints.

> A **system** is an arrangement of parts or elements that together exhibit behavior or meaning that the individual constituents do not.

The general definition deliberately covers conceptual systems too: "Systems can be either physical or conceptual, or a combination of both… Conceptual systems are abstract systems of pure information, and do not directly exhibit behavior, but exhibit 'meaning'." Software, the document notes explicitly, is "an important kind of conceptual system, where the evolution of the code tends to be accompanied by an increase in entropy until the code becomes unmaintainable."

### 4.2 The ten focus areas — and the missing diagnostic step

The document enumerates ten SE activities. The one with direct methodology implication: **SE focus #6 — "establishing appropriate process and life cycle models that consider complexity, uncertainty, change and variety"** — is *prior* to the work, not derived from it. Our corpus mostly inverts this: we pick architecture (Atelier, Foundry, Mill, Lighthouse) and *then* discover the complexity it implies. INCOSE's stance is complexity diagnosis first, methodology second. The other nine focus areas (stakeholder success criteria; solution-space investigation; architecting; modelling at each phase; interface management; verification/validation; SE knowledge supply; transition; periodic re-evaluation) all assume the diagnosis has happened. This is the bridge into the Complexity Primer (§5).

### 4.3 The risk-reduction framing

Two sentences worth quoting verbatim:

> The goal of all Systems Engineering activities is to manage risk, including the risk of not delivering what the customer wants and needs, the risk of late delivery, the risk of excess cost, and the risk of negative unintended consequences. One measure of utility of Systems Engineering activities is the degree to which such risk is reduced. Conversely, a measure of acceptability of absence of a System Engineering activity is the level of excess risk incurred as a result.

This is the lens our F-mode catalog (F1–F35) was already operating in, but the catalog never named the framing. Every failure mode is an "excess risk incurred as a result" of an absent SE activity. The reframe: F1–F35 is a *partial* SE risk register specific to AI-augmented delivery, sitting underneath the broader SE risk taxonomy. This is consistent with the followup/09 methodology-ancestors line; SE is a fourth ancestor sitting alongside Kaner/Rumelt/Deming, distinguished by being explicitly about the *technical artefact* rather than the *practice surrounding it*.

### 4.4 The complicated/complex distinction

Verbatim:

> Complicated systems can be viewed as knowable and deterministic, and once developed their configuration can be "frozen"; whereas complex systems are not fully knowable or deterministic, may be dynamically reconfigurable, and continue to co-evolve with their environment throughout their life cycle.

And later: "Most 20th century engineered systems were complicated; most 21st century engineered systems will be complex." This places AI-augmented systems squarely on the complex side — they co-evolve (the LLM is updated; the policy is rewritten; the substrate moves) and they are not fully knowable (next-token-prediction is irreducibly probabilistic). The methodological consequence is the subject of §5.

---

## 5. INCOSE Complexity Primer — the framing our methodology is missing

INCOSE-TP-2021-007-01 (Revision 1 2021) is the Complex Systems Working Group's white paper. It is the most directly transferable of the four primary sources, because the *kind* of system the software factory builds is exactly the kind the primer describes.

### 5.1 The three-level definition

Verbatim:

> A **simple system** has elements, the relationship between the states of which, once observed, are readily comprehended.
> A **complicated system** has elements, the relationship between the states of which can be unfolded and comprehended, leading to sufficient certainty between cause and effect.
> A **complex system** has elements, the relationship between the states of which are weaved together so that they are not fully comprehended, leading to insufficient certainty between cause and effect.

And: "traditional systems engineering approaches, which assume some form of order and deterministic behavior so the relationship between cause and effect is understood, do not handle complex systems engineering well."

### 5.2 Sillitto's objective vs subjective complexity

> Sillitto (2009) described the inability of a human mind to grasp the whole of a complex problem and predict the outcome as **subjective complexity**…
> Sillitto's **Objective Complexity** describes technical or system characteristics that lead to the subjective complexity or difficulty.

The distinction matters: F1–F35 partition cleanly along this line. Subjective failures (F1 hallucination loop, F22 zombie agents, F23 stalled-vs-thinking ambiguity) are *observer-bounded* — they depend on what the human can perceive. Objective failures (F12 lethal trifecta, F33 adversarial-prompt defeat, F27 same-model build/validate circularity) are *system-bounded* — they exist regardless of observer. The primer's framing suggests these classes should be addressed by different toolkits (subjective: better observation, dashboards, status protocols; objective: substrate-level invariants, OPA gates).

### 5.3 The 14 characteristics of complexity

Table 1 of the primer enumerates them: **Diversity, Connectivity, Interactivity, Adaptability, Multiscale, Multi-Perspective, Behavior, Dynamics, Representation, Evolution, System Emergence (General), Unexpected Emergence (Complex), Disproportionate Effects, Indeterminate Boundaries, Contextual Influences**. Each comes with a definition. The most directly load-bearing for our work:

- **Indeterminate Boundaries** — "Complex system boundaries are intricately woven with their environment… can be non-deterministic. The boundary cannot be distinguished based solely on processes inside the system." This is the explanation for F12 lethal trifecta in primary-source terms — the agent's boundary is not where its container is, it is wherever its tool surface reaches.
- **Disproportionate Effects** — "Details seen at the fine scales can influence large scale behavior… Weak ties can have disproportionate effects." This is the explanation for why a single misplaced word in a spec can derail a multi-week implementation.
- **Unexpected Emergence** — "Emergent properties of the holistic system that are unexpected… Behavior not describable as a response system."

### 5.4 The 15 guiding principles

Section IIIA enumerates 15 "complexity thinking" principles. The ones with direct purchase on our methodology, paraphrased with the load-bearing verbatim core:

- **#1 Gardener-not-watchmaker** — treat the solution "as a living entity within a changing environment as opposed to an intricate, static machine."
- **#3 Adaptive stance** — "think 'influence' and 'intervention' rather than 'control' and 'design.'"
- **#9 Achieve balance, not optimization** — "Optimization is often counterproductive within a complex system… complex systems engineers should seek balance among competing tensions."
- **#12 Region-of-outcome spec** — "Focus on desired regions of outcome space rather than specifying detailed outcomes… Instead of zeroing in on an exact solution, focus on what range of solutions will have the desired effects, and design to avoid forbidden ranges."
- **#14 Adaptive feedback loops** — "feedback loops can either hit the limit of their control space, or may be removed in the interest of maintaining stability. To maintain robustness, periodically revisit feedback and ensure adaptation can still occur."

Principle 12 in particular re-frames our specification methodology: a complex-system spec is *region of acceptable outcome*, not *point of required behaviour*. `spec-driven-ai-dev.md` Layer 3 mostly reads as point requirements; the F-catalogue and reviewer panels exist because of the slippage between point spec and acceptable region. INCOSE's framing: this is not a slippage, it is the *correct* shape of a complex-system spec.

### 5.5 Ashby's Law of Requisite Variety

> Ross Ashby's Law of Requisite Variety shows that a system controller must have at least as many degrees of control as the degrees of freedom in the environment to be controlled. If a system operates within an environment of human processes, as in today's air traffic control, then the system solution must have sufficient complexity to do so. In such a system, it is difficult and even dangerous to ignore the complexity.

For the software factory: the methodology layer must have at least as many degrees of control as the degrees of freedom in agent behaviour. F33 (LLM-based security analysers are probabilistic) is Ashby's Law in a specific form — a probabilistic controller has insufficient variety to constrain a probabilistic agent. Deterministic substrate guards do; probabilistic ones don't.

### 5.6 The complexity diagnosis table

Table 2 of the primer maps system type to SE focus:

| Type | SE focus (verbatim) |
|---|---|
| Simple | "Concentrate on choices of elements to build the system and use traditional systems engineering approaches…" |
| Complicated | "Seek information to more fully understand the relationship between system elements and emergent properties… use traditional systems engineering approaches…" |
| Complex | "Identify the sources of complexity and use different approaches as described in Table 3 below for that class of complexity rather than traditional systems engineering…" |
| Complex Adaptive | "Concentrate on understanding possible emergent characteristics… These almost certainly will involve development of established complex systems approaches and a move towards continual evolution as evidenced to Agile systems engineering." |

The diagnostic step is missing from our methodology. We do not say "this delivery is complicated; use waterfall-with-V&V" vs. "this delivery is complex; use Atelier-style co-evolution." The architecture choice (Atelier/Foundry/Mill/Lighthouse) implicitly encodes a complexity bet, but the bet is not made explicit.

Table 3 of the primer gives concrete approach pairings — e.g., for "Complexity in the Problem/Mission" the requirements-elicitation move is "Capture scenarios and mission threads in preference to large numbers of requirements" and the development-process move is "Use Agile, evolutionary systems engineering processes instead of Waterfall systems engineering processes." This is methodology guidance that arrives ready-made for adaptation.

---

## 6. Requirements vs. architecture — the modelling-context distinction

AFIS/INCOSE-FR's 2016 white paper *Requirements and Architecture within Modelling Context* is the primary source for the distinction El Kaim Chapter 8 makes between specification and architecture, but with industrial feedback rather than narrative anchor.

### 6.1 The three RE goals

Section 2.1 of the paper states the goals in the framing every subsequent section refers back to:

> Goal 1: Obtain well-formed requirements: SMART (Specific, Measurable, Achievable, Realistic, Traceable)
> Goal 2: Ensure completeness and consistency of stakeholders Needs
> Goal 3: Ensure completeness and consistency of the System design against the stakeholders Needs

These three goals collapse the GtWR characteristics into a triple. Goal 1 ≈ C1–C9; Goal 2 ≈ C10–C15 applied to needs; Goal 3 ≈ C10–C15 applied to design requirements. The SMART acronym is a shorthand; GtWR is the long form.

### 6.2 The architecture viewpoint stack (ISO 42010-anchored)

The paper lays out three top-level viewpoints (with logical further decomposed):

- **Operational** — "describes the system organization in terms of black box functions or use cases and associated operational scenarios… in response to desired capabilities from stakeholders in operational environment/context."
- **Logical** — "a set of related technical concepts and principles… includes a functional architecture viewpoint, a behavioral architecture viewpoint, a temporal architecture viewpoint and a partition of functions into system components (building blocks) **excluding implementation or technological issues**."
- **Physical** — "the arrangement of physical elements… which provides the design solution… implementable through technologies."

Load-bearing rule: "These viewpoints are intended to organize and structure the system specification, **not to describe implementation discipline solutions**." This is GtWR R31 (Solution Free) at the architecture level — architecture says *what* and *how organised*; implementation says *which technology*.

### 6.3 The three modelling strategies and their cost gradient

The paper enumerates three approaches and their industrial-feedback returns:

1. **Requirements in natural language, illustrated with diagrams.** Diagrams are decorative; "this approach requires efforts to produce diagrams that cannot give credit for specification. Benefits remain limited to high-level communication." This is roughly where our `spec-driven-ai-dev.md` Layer 3 sits today.
2. **Models to mature and verify requirements that remain in natural language.** Models provide "first level of consistency by construction (model is a kind of 'database' with all elements connected) and allows completing consistency through usage of model queries." Faster requirement maturation; impact analysis is possible with traceability links. This is where El Kaim Chapter 8's typed Codex objects sit (`ArchitectureSpecification` references `Intent` and `DecisionRecord`; report 14 §13).
3. **Models as the specification themselves.** "The goal is to support system architecture definition from system requirements down to system element requirements with full traceability done through models." Benefits: "Fast maturation of requirements; Impact analysis on requirement change eased thanks to use of models and navigation between diagrams (instead of navigating in large documents); Specification document can be generated (now that all data are in the model)." Challenges: identifying which model elements are requirements vs. context vs. glue is a "blocking point for some projects."

The gradient is the cost/leverage tradeoff every spec-authorship discussion in our corpus is implicitly running. Our methodology is mostly strategy 1, occasionally strategy 2 (when typed-object proposals from report 14/24 land). Strategy 3 is the El Kaim Chapter 8 endpoint.

### 6.4 The "centralized definition" benefit

Verbatim (p. 17):

> Model brings a centralized definition for requirements. For instance, if there exist different documents that define power supply characteristics, using a model will help building a unique definition in one place by aggregating all characteristics coming from the various documents. There can be several diagrams representing each displaying a subset of the properties, but the model itself contains the whole definition.

This is the GtWR R30 (Unique Expression) and C11 (Consistent) characteristics enforced *by construction* rather than *by inspection*. The architectural lift to our methodology is non-trivial: most of our specs are document-shaped, not graph-shaped. Reports 14 §13 (typed Codex objects), 22 §4 (foundational programming-language theory for specs), and 24 §3 (product-line typed variability) all push in this direction without naming it as the AFIS strategy-2-to-strategy-3 transition.

### 6.5 The strategy-choice warning

Section 3.1 ("Efficient modeling requires goal and strategy") gives a warning we should adopt:

> If a company uses model without clear objectives about the engineering activities it will support, there is great chance that modeling activities end with frustration: frustration on returns that will remain low if modeling activities did not replace or reduce some engineering activities; frustration also on modeling use with low recognition from management or rest of the team if there was a lot of efforts done with modeling and no clear benefits to align on this investment.

Substitute "structured spec format" for "modeling" and this is a precise prediction for any organisation that adopts El Kaim's 9-field intent block without first articulating which engineering activities the structured intent is supposed to *replace* (not *augment*).

---

## 7. Implications for the software factory

This section ties the four primary sources back to the existing corpus. Concrete claims first, then references and proposed (not asserted) failure modes.

### 7.1 Direct cross-references to existing reports

- **Report 14 (El Kaim intent and spec authorship)** is best read as a domain-specific instantiation of GtWR characteristics C1–C15 with EARS-shaped acceptance criteria implicit at Layer 3. The §3.1 mapping table in this report (El Kaim field → GtWR characteristic) is the explicit bridge. Report 14 §13 (`ArchitectureSpecification` as typed Codex object) is a strategy-2/strategy-3 hybrid in AFIS's three-strategy gradient.
- **Followup 09 (methodology ancestors: Kaner, Rumelt, Deming)** — INCOSE/EARS is a fourth ancestor, distinguished from the three Followup-09 names by being explicitly about the *technical artefact* rather than the *practice surrounding it*. A future followup could add §4 to followup/09 covering this ancestor without duplicating this report.
- **Report 22 (academic foundations)** §1 on SWE-bench treats issue text as ground truth. The INCOSE characteristics C7 (Verifiable) and C14 (Able to be validated) explicitly require ground-truth status to be *earned* (by V&V), not *assumed*. The SWE-bench failure mode is an unmarked SE failure.
- **Report 12 (adjacent ecosystem)** §3 already named EARS as relevant; this report pulls the five patterns through.
- **Report 24 (El Kaim product-line variability)** ↔ GtWR attributes A47–A49. The product-line vocabulary is already standardised in SE.
- **Reports 00, 13 (synthesis + Round-2 synthesis)** — the F1–F35 catalogue is partial coverage of the SE risk-reduction goal stated in INCOSE-TP-2020-002-06 §"Systems Engineering." The complete coverage would re-classify the F-modes by Sillitto's subjective/objective axis (§5.2 here) and by the 14 complexity characteristics (§5.3).

### 7.2 What should change in `spec-driven-ai-dev.md`

These are concrete proposals for the methodology document; they are *proposals*, not assertions, for lead-agent review.

1. **Mandate EARS for acceptance-criteria field.** Layer 3 acceptance criteria should be expressed in one of the five EARS patterns. Prose statement, rationale, and risk fields remain free.
2. **Add a GtWR R7–R35 lint pass** as a pre-commit hook on any AI-authored spec block. The vague-terms blacklist (R7) and escape-clauses blacklist (R8) are both copy-pasteable from the GtWR summary sheet.
3. **Add a complexity diagnosis field at the spec head.** Three values: complicated, complex, complex-adaptive (using the Complexity Primer's vocabulary). The methodology pathway then branches: complicated → waterfall-style V&V is acceptable; complex → mandatory feedback-loop instrumentation, region-of-outcome spec instead of point spec; complex-adaptive → continual-evolution mode.
4. **Add a Sillitto-style subjective/objective complexity classifier to F-mode taxonomy** in `00-synthesis.md`. Each F-mode tagged subjective or objective; mitigation pathway differs.
5. **Adopt the GtWR minimum-attribute set** (A1, A2, A3, A6, A7, A8, A9, A15, A17, A19, A28, A29, A34, A35, A36) as the canonical attribute schema. The corpus already implicitly uses most of these; making them explicit closes the gap.
6. **Adopt the AFIS architecture-viewpoint vocabulary** (operational / logical / physical, with functional, behavioural, temporal sub-views of logical) for any architecture-shaped spec section. The El Kaim Ch8 `ArchitectureSpecification` should be tagged with viewpoint.

### 7.3 Proposed failure modes (F36+) for lead-agent review

The corpus catalog currently runs F1–F35 (with F34, F35 introduced in reports 12 and 24 respectively). The primary sources surface candidates that look like genuine additions, but **lead agent should validate each before promoting**:

- **(Proposed) F36 — Vocabulary lint debt.** AI-authored specs accumulate GtWR R7/R8/R9 violations (vague terms, escape clauses, open-ended clauses) at rates well above human-authored specs because LLMs default to hedging language. Symptoms: requirements that read clearly but cannot be verified; downstream evaluators silently substitute their own interpretation. *Mitigation:* GtWR R7–R35 deterministic linter at the authoring boundary. *Status:* candidate.
- **(Proposed) F37 — Point-spec / region-mismatch.** Spec written as a point requirement (`the system shall do X`) for a complex-system context where the appropriate spec shape is a region of acceptable outcome (Complexity Primer principle 12). Symptoms: every implementation satisfies the spec literally but none satisfy stakeholder intent; reviewer panels keep finding "this is technically correct but…" *Mitigation:* complexity-diagnosis field forces shape-choice up front. *Status:* candidate; may be a generalisation of F4 (silent quality regression).
- **(Proposed) F38 — Architecture/specification confusion in typed objects.** When the spec graph and the architecture graph live in the same tool (AFIS strategy-3 endpoint), distinguishing requirement elements from context/glue elements becomes a "blocking point" (AFIS §2.4.2). Symptoms: spec exports balloon with implementation detail; spec deltas appear with architecture changes that should not have touched the spec. *Mitigation:* viewpoint tagging mandatory on every typed object. *Status:* candidate; distinct from F19 (capability/implementation confusion) by being a tooling artefact rather than an authoring one.
- **(Proposed) F39 — Ashby-deficient probabilistic guard.** A probabilistic guard (LLM-as-judge, LLM-as-security-analyzer) is deployed against a probabilistic agent in a high-variety environment. By Ashby's Law the guard has insufficient requisite variety to constrain the agent. Symptoms: rare-event failures slip through; the guard reports green; deterministic post-hoc audit finds violations. Already partially named as F33 (adversarial-prompt defeat); F39 is the broader Ashby framing. *Status:* may be a reframing of F33 rather than a new mode; lead-agent call.

### 7.4 What the SE tradition does *not* offer

Three things the primary sources are silent on; the corpus must continue to source elsewhere:

- **Agent orchestration and council patterns** — SE assumes human delegates with bounded competence. Carried by reports 03, 16, 23.
- **Substrate-level security primitives** — concrete patterns (sandbox capability dropping, secret registries, lethal-trifecta closure) are out of scope. Carried by reports 10, 11, 18–21.
- **The economic case for AI agents** — INCOSE's focus is risk reduction, not productivity leverage. Carried by reports 01, 02, 06, 07.

SE contributes *the artifact* — what well-formed needs and requirements look like, what characteristics they hold, what rules govern their authoring, what complexity-class diagnoses guide methodology choice around them. It does not contribute the *operations* around the artifact. This report fills in the under-articulated half.

---

## Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| https://alistairmavin.com/ears/ | ✅ | EARS canonical guide page. Five patterns verbatim in §2.2; informed §2 and §7.2(1). |
| https://www.incose.org/docs/default-source/default-document-library/final_incose-se-definition_2020-002-06.pdf | ✅ | INCOSE TP-2020-002-06 *Systems Engineering and System Definitions* (8 Jan 2019). Canonical SE/system definitions in §4.1; ten focus areas in §4.2; risk-reduction framing §4.3; complicated/complex distinction §4.4. |
| https://www.incose.org/docs/default-source/working-groups/requirements-wg/gtwr/incose_rwg_gtwr_v4_summary_sheet.pdf | ✅ | INCOSE-TP-2010-006-04 GtWR v4 Summary Sheet (June 2023). 15 characteristics §3.1; 42 rules §3.2; 49 attributes §3.3. The richest primary source for §7.2 lint proposals. |
| https://www.incose.org/docs/default-source/ProductsPublications/a-complexity-primer-for-systems-engineers.pdf | ✅ | INCOSE-TP-2021-007-01 *A Complexity Primer for Systems Engineers* Rev 1 2021. Three-level definition §5.1; Sillitto subjective/objective §5.2; 14 characteristics §5.3; 15 principles §5.4; Ashby's Law §5.5; complexity diagnosis table §5.6. The most directly transferable of the four PDFs. |
| http://www.afis.fr/ (AFIS MBSE Technical Committee, ISBN 978-2-900969-00-7) | ✅ | AFIS / INCOSE-FR *Requirements and Architecture within Modelling Context* (Dec 2016). Three RE goals §6.1; ISO 42010 viewpoint stack §6.2; three modelling strategies §6.3; centralized-definition benefit §6.4; strategy-choice warning §6.5. Primary source for the requirements-vs-architecture distinction. |
