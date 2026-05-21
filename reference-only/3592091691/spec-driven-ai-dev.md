# Specification-Driven Agentic Development System
## A Methodology for Iterative Specification Refinement Using AI Agents

**Version:** 0.1 (Initial Specification)
**Status:** Draft — suitable for prototype development
**Purpose:** This document is a self-contained specification of a system and methodology for iteratively refining software specifications using AI agents, automated testing, and structured human feedback. It is intended to be complete enough that a reader — human or AI agent — can understand not just what to build, but why, and can begin prototyping the approach with toy scenarios.

---

## 1. Philosophy and Motivation

### 1.1 The Inversion of Scarcity

Traditional software development treats developer time as the scarce resource. Agile methodologies were designed around this constraint — breaking work into short sprints so that wrong directions are caught early, minimizing the cost of human effort spent on things that don't serve the user's actual needs.

The emergence of capable AI coding agents changes this calculus fundamentally. The cost of implementing a specification is dropping rapidly toward near-zero, at least for well-scoped systems. What remains expensive — and what has become the binding constraint — is producing a specification that is complete, consistent, and accurate enough to drive implementation without constant human intervention.

This system is built on that inversion: **the specification, not the implementation, is the scarce and valuable artifact.** The implementation is cheap. The specification is not. Therefore, the methodology that was designed to protect the expensive resource — iterative, incremental, feedback-driven development — should be applied to the specification itself, not to the resulting software.

### 1.2 The Implementation as Specification Probe

The central insight of this methodology is that an AI-generated implementation serves a dual purpose. Its obvious purpose is to produce working software. Its less obvious but more important purpose — especially in early iterations — is to act as a **probe of the specification's completeness and precision.**

When an AI agent implements a specification and produces something unexpected, that surprise is not primarily a failure of the AI. It is a signal from the specification. The implementation has revealed a gap, an ambiguity, a silence, or an inconsistency that the specification author did not know existed. The implementation made that latent problem visible.

This reframing is important because it changes what "success" means in early iterations. A probe that produces surprises is not a failed implementation — it is a successful experiment. It has done its job. The implementation is disposable. The knowledge it generated about the specification is not.

### 1.3 Why Specifications Fail

Specifications fail for distinct reasons that require distinct remedies. Conflating these failure modes leads to applying the wrong fix and potentially making the specification worse. This system treats failure classification as a first-class activity, not an afterthought.

The five failure modes are:

**Silence:** The specification did not address a decision point that the implementation agent encountered. The agent made a reasonable choice given what it knew. The result may be perfectly valid according to the spec but not what the user wanted. Fix: add coverage.

**Ambiguity:** The specification addressed the decision point, but in language that permitted multiple valid interpretations. The agent chose one interpretation. Fix: add precision.

**Incorrectness:** The specification stated something that the author did not actually mean. The agent faithfully implemented something wrong. Fix: correct the statement.

**Inconsistency:** The specification made two statements that cannot both be satisfied simultaneously. The agent resolved the conflict in a way the user disagrees with. Fix: reconcile the contradiction.

**Undiscovered preference:** The specification was technically complete and the implementation was compliant, but the user did not know what they wanted until they saw what they did not want. This is the hardest failure mode because no amount of specification work can fix it until the user has done the introspective work of articulating the preference they didn't know they had. Fix: structured reflection followed by specification addition.

### 1.4 The Layering Principle

A full-stack implementation probe produces entangled feedback. When something is unexpected, it is not always clear whether the surprise originates in the business logic, the data model, the interaction design, or a technology choice the AI made. Entangled feedback makes it hard to write targeted spec amendments, and targeted amendments are essential to avoiding the risk of **spec overfitting** — ratifying what the AI happened to build rather than specifying what the user actually wants.

The solution is to organize the specification into distinct layers of abstraction, and to probe and refine one layer at a time before moving to the next. Layers are ordered from most stable and abstract to least stable and most concrete. Changes in lower-numbered layers are more expensive later because everything above them depends on them.

This layered approach ensures that feedback is attributable. If only the business rules layer is being probed, any surprise must originate there. Feedback about presentation or technology that surfaces during a business-rules probe is captured but not applied yet.

### 1.5 Two Channels of Feedback

The system recognizes two structurally different kinds of feedback that require different handling:

**Channel 1 — Compliance Failures:** The implementation diverged from what the specification says. These are detectable by automated acceptance tests. Something the spec required did not happen, or something the spec prohibited did happen.

**Channel 2 — Completeness Failures:** The implementation complied with the specification, but the result was not what the user wanted. These are detectable only by human review. No automated test can catch them by definition, because they represent things the specification did not say.

These channels are complementary and non-overlapping. A test passing does not mean the user is satisfied. A test failing does not mean the spec is incomplete. Treating them as the same kind of problem is a systematic error that this methodology is designed to prevent.

---

## 2. System Overview

### 2.1 What the System Is

The system is a structured, multi-agent pipeline that manages the iterative refinement of a layered software specification. It consists of:

- A persistent layered specification document (the primary artifact)
- A Specification Analyst Agent that manages the refinement process
- An Implementation Agent that builds probe artifacts from the spec
- A Diagnostic Agent that analyzes implementation failures
- An automated test executor (e.g., Playwright) that checks compliance
- A human reviewer who provides Channel 2 feedback
- A pending observations buffer that captures out-of-layer feedback without losing it

The system is not a code generation pipeline. Its output is a mature, validated specification. Code generation is a side effect of the probing process.

### 2.2 What the System Is Not

The system is not a replacement for human judgment about what is wanted. It is a structured process for making that judgment more precise and complete. The human remains the authority on whether the spec captures their intent. The agents enforce process discipline, classify failures, check consistency, and manage the spec document. They do not decide what the software should do.

The system is also not a one-shot specification tool. It is explicitly designed around the expectation that specifications are incomplete when first written, and that the process of discovering their incompleteness is valuable and should be structured rather than accidental.

---

## 3. The Specification Document

### 3.1 Structure

The specification document is the central artifact of the system. It is a living document that is amended across cycles. It has a defined layer structure that is maintained throughout the process. All agents interact with the same document. Its history is preserved so that amendments can be traced to the failure observations that motivated them.

The document contains the following layers, in order from most to least abstract:

**Layer 1 — Domain and Business Rules**
The entities that exist in the domain, their relationships, the invariants that must always hold, the transformations that are valid, and the business rules that govern behavior. This layer is technology-agnostic and solution-agnostic. It describes what is true about the domain, not how any system will handle it.

**Layer 2 — Behavioral and Process**
The use cases the system must support, the workflows that govern them, the actors involved (human users, external systems, other agents, timers), the basic flow of each use case, the alternative flows that handle variations, and the exception flows that handle failures. This is where most specification gaps are found in practice. Each use case should identify its preconditions, postconditions, and the invariants it must preserve.

**Layer 3 — Integration and Data**
What information must be persisted, how it is related, what must be retrievable and by what criteria, and what data must be exchanged with external systems. This layer is still technology-agnostic — it specifies what the data requirements are, not which database or API protocol will satisfy them.

**Layer 4 — Quality and Constraints**
Non-functional requirements: performance expectations, security requirements, scalability targets, reliability requirements, behavioral guardrails, and any constraints that cut across functional concerns. This layer is often omitted in practice and is one of the most common sources of late-stage surprises.

**Layer 5 — Presentation and Interaction**
How the system presents itself to users, the interaction patterns it supports, the look and feel requirements, and the accessibility requirements. This layer is specified last because meaningful presentation requirements cannot be written until the behavioral and data layers are stable.

**Pending Observations Buffer**
A section of the document that captures feedback observations that surfaced during a probe of one layer but belong to a different layer. These observations are not applied to the spec yet — they are preserved for when that layer is being actively worked. Each observation in the buffer is tagged with the layer it belongs to and the cycle in which it was captured.

### 3.2 Acceptance Criteria Format

Each behavioral requirement in Layers 2 through 5 must be accompanied by acceptance criteria written in a form that is directly automatable. The Specification Analyst Agent enforces this constraint during spec amendment — any requirement that cannot be expressed as an observable, automatable check must be flagged and either reformulated or explicitly designated as a human-review-only criterion.

The standard format for acceptance criteria is:

**Given** [a specific system state or precondition]
**When** [a specific action or event occurs]
**Then** [a specific, observable, verifiable outcome results]

Acceptance criteria that cannot be written in this form, or that require subjective judgment to evaluate, are designated as Channel 2 criteria and are not automated. They are still recorded in the spec and reviewed by the human during each cycle.

### 3.3 Testability as a Spec Quality Signal

A specification that cannot be tested is a specification that cannot be validated. The proportion of acceptance criteria that are automatable is therefore a quality metric for the specification itself, not just for the implementation. A low automation rate in Layer 2 or Layer 3 is a signal that the spec is still too vague.

---

## 4. The Agents

### 4.1 Specification Analyst Agent

**Role:** The process owner and spec guardian. This agent manages the revelation cycle, conducts structured interviews with the human reviewer, classifies failure observations, proposes spec amendments, checks consistency, and maintains the pending observations buffer. This agent does not write business logic or make decisions about what the software should do.

**Responsibilities:**
- Confirm the current active layer and the scope of each probe
- Generate a probe brief for the Implementation Agent that is scoped to the active layer and explicitly excludes constraints from layers not yet probed
- Conduct structured intake interviews with the human reviewer after each probe
- Classify each observation into one of the five failure modes
- For observations belonging to non-active layers, route them to the pending observations buffer
- Propose spec amendments only for the active layer
- Perform a consistency check across the full spec after each amendment set
- Produce a cycle summary including what changed, what was buffered, and a stability assessment
- Flag any proposed acceptance criterion that is not automatable
- Track surprise rate across cycles to generate a layer stability signal

**Key behavioral constraints:**
The Analyst Agent must not proceed from observation intake to amendment drafting without explicit failure classification. It must push back if the human attempts to amend a layer that is not currently active. It must not ratify an implementation decision as correct simply because the human didn't object to it — silence is not acceptance. It must surface consistency concerns even when the human has approved an amendment.

### 4.2 Implementation Agent

**Role:** Builds probe artifacts from the specification. Receives a probe brief from the Analyst Agent that specifies the active layer and scope. Builds the minimum artifact necessary to exercise the spec at that layer. Produces a structured decision log alongside the artifact.

**Responsibilities:**
- Implement only what the probe brief specifies
- Make no decisions beyond what the spec requires without logging them explicitly
- Produce a structured decision log that records: every decision point encountered, what the spec said (or didn't say) about it, and what choice was made and why
- Flag any spec section that required interpretation rather than direct implementation

**The decision log requirement** is critical. The decision log is what makes the Diagnostic Agent's job possible. Without it, failure analysis is guesswork. The decision log transforms the probe from a black box into a transparent experiment.

### 4.3 Diagnostic Agent

**Role:** Analyzes Channel 1 failures — cases where the implementation diverged from the specification. Receives the spec, the Playwright test failure output, and the Implementation Agent's decision log. Produces a structured failure analysis for each failing test.

**Responsibilities:**
- For each test failure, identify the specific spec section(s) involved
- Classify the failure into one of the five failure modes using the decision log as evidence
- Propose a targeted spec amendment that would prevent this specific failure
- Flag cases where the failure suggests an inconsistency elsewhere in the spec, not just at the failing point
- Note cases where the failure log suggests the implementation agent made a correct interpretation of an ambiguous spec — in these cases the agent's choice was reasonable, and the fix is precision, not correction

**The Diagnostic Agent does not propose general spec improvements.** It is strictly reactive to specific failures. Proactive spec improvement is the Analyst Agent's responsibility.

### 4.4 Automated Test Executor

**Role:** Executes the automatable acceptance criteria against the probe artifact. Produces a structured pass/fail log with sufficient detail for the Diagnostic Agent to perform failure analysis.

**Requirements:**
- Must execute acceptance criteria as written in the spec, not as interpreted
- Must produce failure output that includes: which criterion failed, what was expected, what was observed, and at what point in the interaction sequence the divergence occurred
- Must not attempt to infer intent or work around failures

---

## 5. The Revelation Cycle

A revelation cycle is the fundamental unit of iteration in this methodology. Each cycle produces a more complete and precise specification. The implementation produced during the cycle is a side effect of the probing process, not its goal.

### 5.1 Phase 1 — Probe Commissioning

The Specification Analyst Agent opens the cycle by confirming:
- Which layer is currently active
- What the current spec says about that layer
- What acceptance criteria exist for that layer and which are automatable
- What observations are in the pending buffer that belong to this layer (these are surfaced now for potential incorporation before the probe begins)

The Analyst Agent then generates a probe brief for the Implementation Agent. The probe brief includes:
- The active layer's spec content
- The acceptance criteria to be tested
- An explicit statement of what the probe is not testing (to prevent scope creep)
- The instruction to produce a decision log

### 5.2 Phase 2 — Implementation and Testing

The Implementation Agent builds the probe artifact and decision log. The automated test executor runs the acceptance criteria. Both outputs — the artifact and the test results — are collected before any analysis begins.

The human reviewer observes the artifact. This observation is unguided at this stage — the human simply uses or inspects the probe artifact and notes reactions without structure yet.

### 5.3 Phase 3 — Observation Intake

The Specification Analyst Agent conducts a structured interview with the human reviewer. The goal is to surface and classify all observations before any amendment is proposed. The interview is structured around questions, not open-ended reflection:

For each observation the human raises:
- "Was this a surprise, or expected?"
- "Does the spec address this situation?"
- "If the spec addresses it, did the implementation follow it?"
- "If the implementation followed the spec, is the spec wrong, or did you not know what you wanted?"
- "Which layer does this observation belong to?"

The Analyst Agent also presents the Channel 1 failures from the automated test executor and the Diagnostic Agent's analysis of each, for the human to review and confirm or correct.

All observations are recorded before any are acted upon.

### 5.4 Phase 4 — Failure Classification

Each observation is assigned a failure mode classification. The Analyst Agent proposes a classification for each observation and the human confirms or corrects it. This is not a bureaucratic step — the classification directly determines what kind of spec amendment is appropriate, and getting it wrong leads to amendments that don't actually address the problem.

Observations that belong to non-active layers are routed to the pending buffer with their classification preserved. They will be revisited when that layer becomes active.

### 5.5 Phase 5 — Amendment Drafting

For active-layer observations only, the Analyst Agent proposes specific spec amendments. Each amendment is:
- Targeted to the specific failure it addresses
- Written in the same format and language as the surrounding spec content
- Accompanied by the acceptance criteria it implies (which must be in automatable form where possible)
- Linked to the observation that motivated it (for traceability)

The human reviews and approves, rejects, or modifies each proposed amendment. Amendments are not applied until approved.

### 5.6 Phase 6 — Consistency Check

Before closing the cycle, the Analyst Agent reviews the full spec — not just the active layer — for consistency issues introduced by the approved amendments. This is not a comprehensive formal verification, but a structured review asking:
- Does any amendment contradict something stated elsewhere in the spec?
- Does any amendment resolve an ambiguity in a way that conflicts with a decision recorded elsewhere?
- Does any amendment introduce a new dependency on a layer not yet specified?

Consistency issues found here are flagged and must be resolved before the cycle closes.

### 5.7 Phase 7 — Cycle Close

The Analyst Agent produces a cycle summary:
- What changed in the spec (with amendment rationale)
- What was buffered (with layer tags)
- The stability assessment: how many surprises this cycle produced compared to prior cycles for this layer
- Whether the active layer appears stable enough to either close or continue probing

The layer is considered stable when a probe produces observations that are predominantly undiscovered preferences (which may require one more round of reflection) rather than silence, ambiguity, or inconsistency. Stability is a judgment call made by the human with the Analyst Agent's data as input.

---

## 6. Information Flow Summary

```
Human Intent
     |
     v
[Specification Document] <-------- amended by --------+
     |                                                 |
     | probe brief                                     |
     v                                                 |
[Implementation Agent]                    [Specification Analyst Agent]
     |                                                 ^
     |-- probe artifact --> [Human Review] -- Channel 2 observations -->|
     |-- decision log ----> [Diagnostic Agent] -- classified failures -->|
     |-- artifact --------> [Test Executor] -- pass/fail log ---------->|
```

The Specification Document is the persistent artifact that accumulates knowledge across all cycles. Everything else is transient — produced for a cycle and consumed by the analysis process.

---

## 7. Layer Transition Criteria

Moving from one layer to the next is a deliberate decision, not an automatic progression. The criteria for layer transition are:

- The current layer's probe produces no Channel 1 failures in the most recent cycle
- The human reviewer reports no Channel 2 surprises that have not been classified and either addressed or explicitly deferred
- The Analyst Agent's consistency check finds no unresolved issues
- The pending observations buffer contains no observations tagged to the current layer that have not been reviewed

When transitioning, the Analyst Agent surfaces all pending observations tagged to the next layer. These become the starting context for the new layer's first probe commissioning.

---

## 8. Spec Overfitting Prevention

Spec overfitting occurs when the specification evolves to describe what the AI happened to build rather than what the user actually wants. It is the primary risk of reactive spec iteration and must be actively managed.

The disciplines that prevent it are:

**Classify before amending.** Amendments written before classification are likely to ratify rather than specify.

**Silence is not acceptance.** When the human does not object to an implementation decision, the Analyst Agent must explicitly ask whether the spec should constrain that decision or whether AI discretion is genuinely acceptable there. The answer goes in the spec either way.

**Probe brief scoping.** By limiting each probe to an active layer, the probe brief prevents the implementation from filling in all layers at once. Decisions made in unprobed layers are not available to ratify.

**Consistency checking.** A spec that is internally consistent is harder to overfit to a specific implementation because the implementation must satisfy all constraints simultaneously, not just the ones recently amended.

**Pending buffer discipline.** Out-of-layer observations are captured but not applied. This prevents the temptation to "fix" layer 5 problems by amending layer 2, which would lock in implementation decisions prematurely.

---

## 9. Exit Conditions

### 9.1 Layer Stability

A layer is stable when successive probes produce no new Channel 1 failures and the human's Channel 2 observations are limited to undiscovered preferences that have been articulated and added to the spec.

### 9.2 Specification Maturity

The specification as a whole is mature when all layers are stable and a full-stack probe — exercising all layers simultaneously — produces no surprises. This is the exit condition for the specification development process.

### 9.3 Implementation Readiness

A mature specification is ready for unattended implementation when:
- All acceptance criteria are either automatable or explicitly designated for human review
- All layers have been probed and are stable
- A full-stack probe has been completed without surprises
- The human has reviewed and approved the specification as a whole

---

## 10. Self-Application

This specification is itself a candidate for the process it describes. A prototype of the system could be built using this document as the initial specification, then used to probe and refine the document itself. This is not circular — it is an application of the methodology's core insight. The first implementation built from this spec will reveal gaps, ambiguities, and silences in it. Those revelations should be fed back into this document according to the process it defines.

This self-referential property is not a coincidence. A methodology for producing complete specifications should be able to produce a complete specification of itself. The degree to which it can is a measure of its maturity.

---

## 11. Key Terminology Reference

| Term | Definition |
|------|-----------|
| Revelation cycle | One complete iteration of probe commissioning, implementation, testing, observation intake, classification, amendment, and consistency check |
| Specification probe | An implementation built not to be used but to reveal gaps in the specification |
| Channel 1 failure | An implementation divergence from the spec, detectable by automated testing |
| Channel 2 failure | A user dissatisfaction with a spec-compliant implementation, detectable only by human review |
| Pending observations buffer | A holding area for out-of-layer feedback that is captured but not yet applied |
| Decision log | A structured record produced by the Implementation Agent of every decision point encountered and how it was resolved |
| Spec overfitting | The failure mode where the spec evolves to describe what the AI built rather than what the user wants |
| Layer stability | The condition where a layer's probes produce no new classification failures |
| Spec maturity | The condition where all layers are stable and a full-stack probe produces no surprises |
| Failure mode | The category of cause for a spec failure: silence, ambiguity, incorrectness, inconsistency, or undiscovered preference |

---

*End of Specification v0.1*
