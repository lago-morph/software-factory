# El Kaim — Intent-Driven Architecture and Spec Authorship

**Round-4 Cluster A.** Source: William El Kaim, *AI-Augmented Enterprise Architecture* series, Chapters 1, 3, 6, 7, 8.
**Scope:** vocabulary; the nine-field structured-intent model; the three authoring paths and the OPA/Rego meta-validation gate; cautionary cases for unstabilized direction; concrete proposals for our spec template; **the architectural translation from intent and PRD into a governed design space — design decisions, architecture specifications, derived executable constraints, and eval suites bound to the spec** (Chapter 8).

Per round conventions, El Kaim's "ACME Pharma" running example is generalized to enterprise-level language when quoted; SAP / clean-core material from Chapter 5 is out of scope (separate cluster). Chapter 9's SPL / variability material is being drained in parallel into a separate report.

---

## Drain note (Chapter 8) — 2026-05-13

Chapter 8 ("From Intent to Specification") was drained into this report on 2026-05-13 from the manual fetch in `research/manual/`. What changed:

- **New sections added:** §10 (the missing architectural act between intent and execution); §11 (intent and PRD as *demand* artifacts vs. specification as *acceptability*); §12 (design decisions close the design space); §13 (the architecture specification object); §14 (derived executable constraints — the bridge from spec to OPA/Rego); §15 (evals as the second executable control); §16 (delivery implication: PRD + spec as paired inputs); §17 (risks and named anti-patterns Ch8 surfaces, including the *false specification* failure mode).
- **Refinements (not refutations) to existing sections.** Chapter 8 does *not* refute the nine-field intent model in §3; it operates one level *downstream* of it. Where §3 lists `invariants` with optional `bindingHint`, Chapter 8 makes the binding concrete: an invariant projects into one or more `rules` inside an `ArchitectureSpecification` object, each `derivedFrom` a `DecisionRecord`, each with named `evidenceSources`. §3 is left intact; a forward reference to §13–§14 has been added.
- **Refinement to §5 (OPA/Rego dual role).** Ch6/Ch7 named the dual role abstractly. Ch8 makes Role 2 (downstream enforcement) concrete with a worked Rego package (`pv_intake.agent_permissions`) and matched compliant / non-compliant request payloads, and adds a *third* executable control alongside policy: the eval suite (§15).
- **New typed object surfaced.** `kind: ArchitectureSpecification` (apiVersion `ea.codex/v1`) — a Codex object that binds demand (intent + PRD) → concerns → decisions → model (systems, agents, data objects) → rules → variation envelope → governance → feedback in a single artifact, addressable by stable ID.
- **No claims refuted.** Chapter 8 deepens the Round-4 picture; nothing earlier in the report needed retraction.

---

## 1. Why El Kaim matters for us

Our corpus is strong on the *implementation-probe* side of spec-driven work (`spec-driven-ai-dev.md` layers; Compound Atelier's brainstorm-plan-implement; Phase-Gated Foundry's SRS/SAD). It is thin on the *upstream* typed object that fixes business direction before any layer-1 prose. Where we say "spec," El Kaim distinguishes intent, policy, design decision, specification, constraint, control, and feedback as separate typed objects with separate lifecycles. The vocabulary predicts failure modes our spec templates currently absorb silently.

---

## 2. The vocabulary sharpener (Chapter 1 §1)

El Kaim defines a typed chain, not synonyms:

- **Intent is directional** — "names the enterprise outcome being pursued."
- **Policy is constraining** — "states what must not be violated."
- **Design decision is selective** — "chooses a path in a particular context and makes trade-offs explicit."
- **Specification formalizes what has been decided in a form that can guide implementation.**
- **Constraint makes part of that specification testable.**
- **Implementation realizes the specification; execution is the running system; feedback closes the loop.** (all Ch1 §1)

The canonical failure he names: "Traditional enterprise architecture often blurred these distinctions" — "Principles drifted into vague aspirations. Standards documents mixed policy, recommendation, and historical preference. Roadmaps presented intended motion without making the governing design choices explicit." (Ch1 §1) Chapter 3 §1 restates the chain compactly: "Intent defines direction. Capabilities define stable business scope. Policies define constraints. Design decisions define execution choices. Specifications formalize those choices. Controls verify conformance. Feedback updates future decisions."

**Our usage is loose by comparison.** `spec-driven-ai-dev.md` uses "specification" for everything from directional Layer 1 prose down to Given/When/Then ACs. `architectures/00-comparison.md` uses "spec" as one category dimension. We collapse intent, policy, decision, and spec into one artifact and let layering carry the whole distinction. That layering solves *implementation-probe* attribution but leaves no place for "this outcome is non-negotiable" or "this rule must remain intact regardless of what the implementation discovers."

We should adopt **intent → decision → spec → control → feedback**, with the layered spec as the third element. Policy lives orthogonally as a catalog; invariants are the bridge that compiles down into executable controls.

---

## 3. The structured-intent model (Chapter 3 §4.1)

Chapter 3 §4.1 enumerates the nine spec-block fields (with `metadata` as a sibling block):

1. **Identity and metadata.** Stable ID, owner, status, planning horizon. "Identity is what lets decisions, specifications, and controls later reference the intent without ambiguity." (Ch3 §4.1)
2. **Statement.** Prose direction — "the one field where narrative still belongs, because executive language, strategic framing, and business rationale cannot be reduced to structured fields without loss." (Ch3 §4.1)
3. **Business outcomes.** Metric + baseline + target. "An intent without outcomes is an aspiration; an intent with outcomes is a commitment." (Ch3 §4.1)
4. **Capability scope.** Primary and adjacent capabilities, anchored to "stable business capability definitions rather than project names or application labels." (Ch3 §4.1)
5. **Policy references.** Mandatory and advisory, by ID into a policy catalog. The catalog owns the text; the intent owns the reference. (Ch3 §4.1)
6. **Invariants.** "Non-negotiable conditions that any valid realization of the intent must preserve." Differ from policies in scope — policies apply enterprise-wide; invariants are specific to this intent. "They are also the fields that later get compiled into executable policy rules." (Ch3 §4.1)
7. **Non-goals.** "Silence is often misread as permission. A non-goal explicitly names what the enterprise is not trying to do... In most workshops they are the last field to be filled in, because they expose tensions that other parts of the conversation have politely avoided." (Ch3 §4.1)
8. **Decision seeds.** Open architectural questions named explicitly "so that the architecture function can schedule their resolution rather than let them be decided implicitly by whoever writes the first Terraform module or the first integration contract." (Ch3 §4.1)
9. **Guardrails.** Metrics that must not break in pursuit of the outcome. "Outcomes describe what success looks like; guardrails describe what must not break in pursuit of success." (Ch3 §4.1)
10. **Feedback sources.** Named system + signal. "An intent that cannot observe its own progress cannot govern anything." (Ch3 §4.1)

The model is deliberately Kubernetes-shaped (`apiVersion`, `kind: EnterpriseIntent`, `metadata`, `spec`) to make it "consumable by the same class of tooling that already handles declarative YAML objects." (Ch3 §4.1) The invariant `rule` field is typed as a string, not a formal expression language, so that "the intent declares the constraint; the specification declares how it is enforced." (Ch3 Appendix A.3)

The load-bearing fields we currently lack are **invariants**, **non-goals**, and **decision seeds**.

*Forward reference.* Chapter 8 makes the downstream binding of these fields concrete: each invariant projects into one or more `rules` inside an `ArchitectureSpecification` object whose `derivedFrom` points back to a `DecisionRecord`, and each rule names explicit `evidenceSources`. See §13 and §14.

---

## 4. The three authoring paths (Chapter 3 §5)

Chapter 3 §5 names three complementary paths.

**Path 1 — Structured workshop (Ch3 §5.1).** A facilitator walks the artifact field-by-field with sponsor, domain experts, regulatory rep, and accountable stakeholders. "The statement is debated until it stops sounding like a slogan... The non-goals are surfaced last, because they are the field most likely to expose the tension that other parts of the conversation have politely buried." Strength: reasoning happens in the room. Weakness: expensive, inconsistent, does not refresh.

**Path 2 — LLM-assisted with retrieval-grounded validation (Ch3 §5.2).** The tool has three structural elements; skipping any one is how this path fails. The **schema** is the contract — required fields, valid enums, cross-field constraints. The **retrieval layer** is the grounding — "when the LLM proposes a policy reference, that reference must come from the policy catalog and not from the model's training data." The **validation layer** is the gate — "an artifact that lists a non-existent policy or omits a non-goal field is rejected before it leaves the tool, and the model is asked to revise." (Ch3 §5.2)

The named risk is confabulation: "It will invent plausible-sounding policy identifiers, will reference capability nodes at the wrong level of abstraction and will smooth over genuine tensions that a workshop would have surfaced. False precision is the central risk, and it is worse here than in the workshop case because the polish of LLM output disguises its origin." (Ch3 §5.2) Mitigation is structural: hard-fail on unresolved references, require explicit human sign-off on outcomes and invariants, record which fields the model drafted vs. edited.

**Path 3 — EA-tool-resident authoring (Ch3 §5.3).** Artifact lives inside the EA repository alongside the objects it references; "an intent authored in that environment inherits their governance by construction." Requires a first-class `Intent` entity distinct from `Initiative`/`Program`/`Project`, typed relations to Capability/Policy/Metric/Decision, and lifecycle states with a `supersedes` relation.

The mature pattern (Ch3 §5.6) uses all three in sequence: LLM drafts from a sponsor interview, workshop sharpens with accountable owners, EA tool publishes as a governed object.

---

## 5. The OPA-Rego meta-validation gate (Chapter 3 §5.4)

The key insight our current architectures miss: OPA/Rego has *two distinct roles*.

**Role 1 — Meta-validation of the intent artifact itself.** Rego policies run in the authoring pipeline checking cross-field constraints JSON Schema cannot express: "every invariant must reference at least one policy," "every decision seed must have a target resolution date," "every policy reference must resolve to a governed policy ID in the catalog," "every guardrail metric must map to an active feedback source." (Ch3 §5.4) This is the validation layer that prevents LLM confabulation — independent of the LLM, checking that every reference resolves in the catalog.

**Role 2 — Downstream enforcement of declared invariants.** Each invariant is paired with one or more executable Rego rules. "The Rego rule does not replace the invariant; it is the executable expression of it. Both artifacts continue to exist, and the link between them... is stored in the EA tool as a ControlSpec artifact that references both the Intent and the Git path." (Ch3 §5.4)

Chapter 7 §1 sharpens the stake: "If the enterprise supplies poor architecture semantics, vague policies, or weak decision structures, AI systems will reproduce that ambiguity at speed... The same mechanism that makes specification more powerful also makes poor specification more dangerous." (also Ch1 §7.8)

---

## 6. Healthcare.gov and UK Universal Credit (Chapter 3 §2)

These are the chapter's evidence that under-stabilized direction is an **architectural** failure, not a project-management one.

For Healthcare.gov, intent was clear politically — a federal insurance marketplace — but "that strategic direction was never stabilized into an architectural object that fifty-five contractors, multiple federal agencies, and several technology integration partners could consume as a shared reference." Each contractor made defensible local decisions; the system collapsed at launch because "nobody had governed the integration assumptions, performance invariants, or data-flow constraints that would have needed explicit upstream agreement." The rescue "began by doing exactly what the original program had not done: stabilizing scope, constraints, integration boundaries, and operational invariants before allowing any further feature work." (Ch3 §2)

For UK Universal Credit, "scope oscillated between full digital transformation and incremental migration. Platform choices were made and reversed. Invariants around data residency, identity assurance, and local authority integration were discovered rather than declared." (Ch3 §2)

El Kaim is careful: "Neither Healthcare.gov nor Universal Credit failed solely because intent was implicit... But in both cases, the absence of a structured upstream artifact (one that bound direction, scope, invariants, non-goals, and open design choices into a form consumable by downstream teams) amplified every other failure mode. The teams were not failing because they lacked talent. They were failing because the enterprise had not stabilized what it meant before distributing the work." (Ch3 §2)

The translation to our context: a fanout that dispatches subagents from a brief not yet stabilized into invariants, non-goals, and decision seeds is structurally Healthcare.gov in miniature. Each subagent picks a defensible local answer; the answers do not compose.

---

## 7. The Codex framing (Chapter 6 §1–3, §5)

Chapter 6 reframes the four TOGAF building blocks (principles, standards, reference architectures, blueprints) plus the "cognitive infrastructure" beneath them (business capabilities, enterprise intent, semantic ontology, organizational model) as **typed, linked, executable knowledge** rather than documents. (Ch6 §2, §3, §5)

The load-bearing claim: "Documents preserve content but not the logic between content" (Ch6 §4). "A principle is stored without its validation, a standard without its conformance check, a reference without the projection rules that would let it regenerate, and a blueprint without the dependency graph that would let it be sequenced." Our markdown spec files have the same shape — intent, layers, and acceptance criteria, but the *relations* between them are unstated.

The five Codex disciplines (Ch6 §5.1–5.5) are typed objects, explicit relations, lifecycle states, executable validation logic, and metamodel mappings. We do not need El Kaim's full EA tool; we need his *discipline*: typed YAML objects with stable IDs, schema-validated, referenced by stable ID from downstream artifacts.

---

## 8. Compare against our current artifacts

**`spec-driven-ai-dev.md`** has layers, Given/When/Then ACs, and a Pending Observations buffer. Invariants are buried in Layer 1 prose and per-use-case post-conditions. It lacks an explicit **non-goals** field, **decision-seeds** field, and **structured invariant list with downstream binding hints**. Outcomes and guardrails are not separated.

**`architectures/00-comparison.md`** treats "the spec" as the seed of the agent loop in all four architectures. None has an upstream intent object. The Phase-Gated Foundry's Phase 1 (Requirements) is the nearest analog, but SRS-shaped (functional + NFR) rather than intent-shaped (outcomes + invariants + non-goals + decision seeds). The Tournament's "deliberately under-specified seed" is the *opposite* discipline: under-specification as a diversity-driver. The Atelier's `STRATEGY.md` gestures at intent without a schema.

**`research/03-every-compound-engineering.md`** is process-shaped (plan → work → review → compound), not artifact-shaped. It assumes intent lives in the issue description and the operator's head — the "intent left implicit" pattern of Chapter 1.

---

## 9. Concrete proposals for our spec template

**1. Add an explicit `Intent` section above Layer 1.** Required fields: `id`, `statement`, `businessOutcomes` (metric + baseline + target), `nonGoals` (what this spec will *not* do; surfaces buried tensions, Ch3 §4.3), `decisionSeeds` (open questions with `id`, `topic`, `question`, `targetResolutionDate`; each resolves into an ADR), `invariants` (each with `id`, `rule`, optional `bindingHint` naming the downstream control surface — Rego policy path, CEL admission rule, acceptance-test ID, runtime check, per Ch3 Appendix A.3), `guardrails` (metrics that must not regress), `feedbackSources`.

**2. Separate `Policy` from `Invariant`.** Policies are enterprise-wide catalog entries referenced by ID; invariants are this-spec-specific and compile into executable controls. Our current Layer 4 (Quality and Constraints) mixes both. Split: policy references go in the Intent block; per-spec invariants live in Layer 4 with explicit `bindingHint`.

**3. Add an OPA-Rego-style meta-validation gate.** Even without OPA, a pre-flight linter checks: every decision seed has a target date; every invariant has either a binding hint or an explicit `enforcement: manual-review` tag; every policy reference resolves; every guardrail has a feedback source. This is the structural prevention of confabulation when an LLM drafts a spec. (Ch3 §5.2, §5.4)

**4. Three authoring paths, explicitly named.** Workshop / LLM-assisted-with-retrieval / repo-resident as complementary modes, not alternatives. For us: solo-operator drafting (workshop equivalent), agent-drafted from sponsor brief with retrieval over existing specs and ADRs (LLM-assisted), spec promoted into the repo with stable IDs and CODEOWNERS-style review (EA-tool path).

**5. Treat `decisionSeed` resolution as an ADR.** When a seed resolves, an ADR records the resolution and links back to the seed ID. Intent stays stable; decisions evolve — directly the `supersedes` relation of Ch3 §5.3.

**6. Treat unresolved decision seeds as a hard gate before agent dispatch.** Healthcare.gov in miniature: a subagent fanout dispatched before seeds are resolved will produce defensible local answers that do not compose.

**What not to import.** The full Codex-as-skills marketplace packaging (Ch6 §6) is heavier than we need; adopt the typed-object discipline, defer the marketplace endpoint. The EA-tool path (Ch3 §5.3) assumes a LeanIX-class metamodel we do not have; Git-resident schema validation is the practical substitute.

---

## 10. The missing architectural act between intent and execution (Chapter 8 §1)

Chapter 8 names a gap our existing sections gestured at but did not give a name. Between intent (Chapter 3) and execution (Chapter 7) sits an act of architectural translation that, when skipped, lets product demand harden into systems before architecture is asked. By the time architecture is asked to review, "the choices have already started to harden into systems, workflows, integrations, and code. Architecture may still influence the outcome at that point, but it is no longer shaping the design space. It is correcting interpretation after interpretation has already become implementation." (Ch8 §1)

The chapter's reframe: that missing act is the transformation of intent plus product demand into a **governed design space**:

- "Some choices in that space are allowed because they remain consistent with enterprise intent.
- Others are prohibited because they would undermine the architecture.
- Some are delegated to local teams that can decide safely inside a defined envelope.
- Some require escalation because they cross a structural boundary.
- And some can be checked automatically because they have been expressed as executable constraints." (Ch8 §1)

This is what the word *specification* means in El Kaim's vocabulary. He is explicit about what it is not: "A specification is not a longer requirements document, is not a diagram with more metadata, and not a policy copied into a repository. It is the structured form through which architectural judgment becomes usable by delivery teams, governance bodies, platforms, pipelines, and AI agents." (Ch8 §1)

For our fanout / subagent dispatch context, the governed-design-space framing is load-bearing: it is the artifact a subagent reads to know which choices are pre-decided (and citable), which are inside its envelope, and which it must surface for escalation rather than answer locally.

---

## 11. Intent and PRD are *demand* artifacts; the specification defines *acceptability* (Chapter 8 §2–§3)

Chapter 8 sharpens the typed chain from §2 by separating *demand* from *acceptability*.

> "Intent and PRDs express what the enterprise wants. Architecture specification defines the conditions under which that demand may be realized without breaking the enterprise structures that the intent depends on. The PRD tells delivery what the product must achieve; the specification tells delivery what must remain true while achieving it." (Ch8 §2)

A PRD can be fully satisfied while a serious architecture problem is created. In the running enterprise-pharmacovigilance example: an AI layer might retain regulated patient data outside approved stores; regional workflow tools might evolve into shadow case-management systems; the line between AI recommendation and regulated decision might blur in practice; intake evidence might end up trapped where no one can trace it back to the authoritative case. (Ch8 §2)

§3 names the translation problem: "Hidden inside the product language of users, journeys, and features sits a set of unspoken architectural commitments: who owns what data, which system holds authoritative state, where decisions may be made, what evidence must survive the process. None of these are visible in the PRD itself. All of them will be answered by somebody. If architecture does not answer them deliberately, the first delivery team to encounter them will." (Ch8 §3)

This restates §2's Healthcare.gov/Universal Credit reading at the artifact level: under-stabilized translation makes local rationality compound into structural failure. "None of these teams is acting unreasonably, but their local rationality compounds into a system that violates the very intent it was built to serve." (Ch8 §3)

---

## 12. Design decisions close the design space (Chapter 8 §4)

Chapter 8 introduces the `DecisionRecord` (kind: `DecisionRecord`, apiVersion `ea.codex/v1`) as a distinct typed object that sits between intent and specification. Each record names: an `intentReference`, a `prdReference`, the architectural `concern`, the `problem` statement, the `decision.statement`, `rationale`, `rejectedAlternatives` (each with its `reason`), `consequences`, and `reviewTriggers`.

The principle: "The role of architecture is not to centralize every choice; it is to close the choices that would otherwise undermine enterprise intent, and to define the envelope within which other choices can safely be made." (Ch8 §4)

The most architecturally significant move in the worked example is the explicit recording of *rejected alternatives*. El Kaim's claim: "Many architecture failures are not caused by teams explicitly ignoring a known decision; they are caused by teams re-opening a question that was never properly closed. When the alternatives are explicit, delivery teams understand not only what was chosen but why other plausible options were rejected." (Ch8 §4) Until a documented `reviewTrigger` fires, "the boundary holds."

This is the typed object our existing §9.5 ("Treat `decisionSeed` resolution as an ADR") was reaching toward. The `DecisionRecord` shape matches our ADR convention's section order (Context → Decision → Alternatives considered → Consequences) and adds two fields ADRs typically lack: `intentReference` / `prdReference` (explicit back-links to the demand) and `reviewTriggers` (named conditions that can reopen the decision).

---

## 13. The architecture specification as a typed Codex object (Chapter 8 §5)

The `ArchitectureSpecification` (kind: `ArchitectureSpecification`, apiVersion `ea.codex/v1`) is the integrating object. Its blocks:

- `demand` — `intent` (id + statement) and `prd` (id + product + `selectedRequirements`).
- `architecturalConcerns` — short tags like `data-authority`, `system-of-record`, `ai-action-boundary`, `human-approval`, `regional-variation`, `audit-evidence`, `patient-data-retention`.
- `model.systems` — each with `id`, `name`, `role`, `validationStatus` (e.g. `validated`, `not-validated-for-case-management`, `controlled-pilot`).
- `agents` — each with `id`, `name`, `permittedActions`, `prohibitedActions`. This is where the AI-action boundary lives.
- `dataObjects` — each with `id`, `name`, `authority` (system id), `classification` (e.g. `regulated`, `decision-support-evidence`).
- `decisions` — list of DecisionRecord ids.
- `rules` — each with `id`, `name`, `statement`, `derivedFrom` (DecisionRecord id), `evidenceSources` (named logs / registers).
- `variation.allowed` — each entry has `type`, `authority`, `condition`; and `variation.prohibited` — list of named forbidden shapes.
- `governance.primaryAuthority` and `governance.escalationTriggers`.
- `feedback.monitoredSignals` and `feedback.reviewCadence`.

The chapter's framing of what this changes: "A specification of this kind also changes the role of architecture review. The question is no longer whether an architect 'likes' the proposed solution. The question is whether the proposed solution remains inside the design space that has already been defined. If it does, delivery should proceed without unnecessary review. If it does not, the issue should escalate through the authority model already described in the specification." (Ch8 §5)

The structural shape — demand + concerns + model + decisions + rules + variation + governance + feedback in one addressable object — is the practical fulfillment of the Codex disciplines from §7. Compared with our `spec-driven-ai-dev.md` Layer 1–4 prose, the `ArchitectureSpecification` makes *the relations* explicit: every rule has a `derivedFrom` pointer, every data object has an `authority` pointer, every variation has an `authority` and a `condition`.

---

## 14. Derived executable constraints — the bridge to OPA/Rego made concrete (Chapter 8 §6)

Chapter 6/7 established the OPA/Rego dual role abstractly. Chapter 8 supplies the worked example. Each `rule` in the specification can project into a Rego policy whose `package` name (e.g. `pv_intake.agent_permissions`) is bound by ID to the specification (`required_specification := "SPEC-PV-001"`) and decision (`required_decision := "DEC-PV-001"`).

El Kaim is explicit about what executable constraints do *not* replace:

> "Not every rule can be automated, and not every architectural judgment should be reduced to code: A regional regulatory deviation may require interpretation. A recurring exception may signal that the global design is incomplete, not that a team is non-compliant. A pattern of human overrides may show that an AI triage model is not yet reliable enough for the workflow it sits in. Architecture remains a human discipline, because enterprises are full of trade-offs that resist binary evaluation." (Ch8 §6)

And what they *do* do:

> "Executable constraints therefore do not replace architecture. They extend architecture into delivery. They allow architectural decisions to appear inside pipelines, workflow systems, AI runtimes, access-control checks, test suites, deployment gates, and operational monitors, where they can affect execution before non-conformance becomes expensive." (Ch8 §6)

A critical operational detail: the policy must explain its rejection, not merely block. "A gate that simply blocks work creates frustration; a traceable constraint tells the team what boundary was crossed and what must change." (Ch8 §6) The Rego `deny_reasons` set in the worked example produces messages that name the violated action, the specification ID, and the decision ID — a traceable rejection rather than an opaque one. This is directly applicable to our preflight linter design from §9.3: every blocked check should cite the rule, the decision, and the intent it derives from.

For our security-primitives line of inquiry, this is also where Chapter 8 reinforces `research/followup/08-security-primitives.md`: OPA/Rego is not merely an authorization layer; in the specification-driven workflow it is the runtime expression of an architectural decision, with stable ID linkage back through `DecisionRecord` to `EnterpriseIntent`.

---

## 15. Evals as the second executable control (Chapter 8 §7)

Chapter 8's most important contribution to our existing evals work is its claim that **evals belong inside the specification, not alongside it**. They are the second executable control bound to the spec, parallel to the Rego policy.

The argument: Rego catches what can be reduced to a deterministic rule; a large part of what a specification claims about AI behavior cannot. "The specification asserts that the AI Triage Service extracts adverse-event facts reliably, that its triage suggestions correspond to what an experienced pharmacovigilance reviewer would have prioritized, that extraction prompts continue to produce usable evidence when the underlying model is updated, and that regional variations in intake language do not degrade extraction quality below a tolerable threshold. None of these claims can be evaluated by inspecting the agent's permission set." (Ch8 §7)

> "A specification claims that the AI Triage Service may operate inside a decision-support boundary. An eval proves that the service is actually competent enough to sit inside that boundary." (Ch8 §7)

The typed object is `kind: EvaluationSuite` (apiVersion `ea.codex/v1`) with:

- `specificationReference` and `decisionReference` (stable IDs back to the spec and the governing decision).
- `datasets` — each with curator and case count, typically partitioned by region or other variation axis.
- `metrics` — each with `id`, `type` (e.g. `field-level-accuracy`, `ordinal-agreement-with-reviewer`, `binary-recall`, `latency`), `threshold`, and crucially `protects: RULE-PV-NNN` — a direct link to a specification rule.
- `blockingGates` — metrics whose failure stops deployment.
- `regressionPolicy.maxAllowedDegradation` — caps on drift relative to the prior baseline.
- `reviewTriggers` — named conditions (model update, prompt change, new regional dataset, reviewer override rate exceeds baseline).

The discipline is symmetric with Rego: an eval run is a gate, not a report. "A new agent configuration, a new prompt version, a new model, or a new regional extraction pipeline passes through the eval suite before it reaches production. If the suite fails on a blocking gate, the deployment stops and the failure is traced back to the metric, the dataset, and the specification rule it protects." (Ch8 §7)

The two-source feedback model: production behavior produces signals like override rate and blocked-action count; the eval suite produces complementary signals under controlled inputs. "Production tells architecture what is happening under real load; evals tell architecture what the system is capable of under known inputs. The combination is what distinguishes a specification whose claims are asserted from a specification whose claims are verified." (Ch8 §7)

This is the part of Chapter 8 most directly relevant to `research/followup/07-evals-deepdive.md`. The `protects: RULE-ID` link from metric back to specification rule is the structural piece that follow-up should foreground. Our prior evals work treated eval suites as quality gates; Chapter 8's contribution is to bind each metric to a specific architectural commitment, so a metric failure is traceable to a violated specification rule rather than to a vague "quality regression."

The chapter's punchline on the relationship between the two executable controls:

> "The Rego policy enforces what the agent is allowed to do. The eval suite proves that what the agent does, when it is allowed to act, is worth allowing in the first place. Both are executable controls. Both derive from the specification. Together they make specification-driven architecture trustworthy rather than merely well-organized." (Ch8 §7)

---

## 16. Delivery implication: PRD + specification as paired inputs (Chapter 8 §8)

The chapter's operational claim: "Delivery does not receive only a PRD, it receives a PRD plus architecture specification." (Ch8 §8) The two artifacts evolve together; product demand and architectural acceptability influence each other through the early life of an initiative.

For our fanout / subagent dispatch design, this is the directly applicable shape. A subagent brief should not be a PRD analog (story, outcome, success criteria) alone; it should be PRD + specification, where the specification block carries the design space: which decisions are pre-resolved (with their IDs), which agents/tools are inside the permitted-action set, which actions are prohibited, what evidence must be produced, what may vary by execution-time context, and which executable controls (Rego policies, eval gates) will run against the output.

Chapter 8 frames this as a role shift: "Architecture is no longer a downstream reviewer of product intent. It becomes the function that translates product intent into a design space delivery can safely inhabit." (Ch8 §8) The analog in our setting is the operator role at fanout time: not a late reviewer of subagent output, but the function that stabilizes the design space before dispatch.

---

## 17. Risks, limits, and the *false specification* failure mode (Chapter 8 §9)

Chapter 8 names six failure modes for specification-driven architecture:

1. **Cost of discipline.** "Writing a specification takes more discipline than writing a principles document or a target-state slide... The investment only pays back when the specifications are reused across multiple delivery cycles and when the conformance checks they enable replace late-stage rework." (Ch8 §9)
2. **Specification rigidity.** "A specification that is too narrowly drawn may block useful evolution... The defense against rigidity is the variation envelope: explicit ranges of allowed local adaptation that the specification names rather than forbidding by omission." (Ch8 §9)
3. **Implicit knowledge resists formalization.** "The specification should name the boundary at which formal structure ends and human judgment begins, rather than papering over the boundary with thin formalization." (Ch8 §9)
4. **Ownership politics.** "A specification that lives in architecture's repository but governs product delivery is a contract between two functions... The healthy pattern is shared authorship under architectural authority: the architecture function holds the pen on what must remain true, while product and delivery contribute the operational reality that shapes how decisions are framed." (Ch8 §9)
5. **Tooling immaturity.** "Editors do not natively understand schemas like ea.codex/v1. Validation harnesses require setup. The integration between specifications and policy engines, agent runtimes, and delivery pipelines is bespoke in many enterprises... Trying to operate without that investment produces specifications that are formally correct and operationally inert." (Ch8 §9)
6. **The false specification.** "A document that uses the structured form, names the right fields, and references the right decisions, but whose constraints cannot actually be checked and whose evidence cannot actually be produced. This is worse than no specification at all, because it gives governance forums the appearance of control without the substance. The discipline that prevents false specifications is end-to-end execution: every conformance rule must trace to a check that runs, every evidence obligation must trace to a record that exists, and every escalation trigger must trace to a path that activates. A specification that fails this trace is not a specification yet. It is a specification proposal awaiting the work that would make it real." (Ch8 §9)

The *false specification* is the named anti-pattern we should track explicitly. It generalizes our preflight-linter design from §9.3: not just "does the field resolve?" but "does the executable control bound to this rule actually exist, and does it run?" The trace test (rule → check that runs; obligation → record that exists; trigger → path that activates) is a concrete acceptance criterion we can adopt verbatim.

This is also the failure mode that connects Chapter 8 back to Chapter 7's warning that AI amplifies semantic weakness: a false specification handed to an AI coding assistant produces structurally plausible output that no executable control will catch.

---

## Sources

- *Chapter 1, The Limits of Traditional Enterprise Architecture* — §1 (vocabulary), §3 (decision system), §4.1–4.3 (typed decision), §5 (encoded decision example), §7 (risks).
- *Chapter 3, Intent-Driven Architecture* — §2 (Healthcare.gov, Universal Credit), §3 (Working Backwards / Hoshin Kanri / Backstage / Crossplane), §4.1 (nine-field anatomy), §4.2 (worked example), §5.1–5.3 (three authoring paths), §5.4 (OPA dual role), §5.5–5.6 (six-stage pipeline), Appendix A (grammar, JSON Schema, semantic notes).
- *Chapter 6, The Enterprise Architecture Codex* — §1 (vibes-to-codex), §2 (four building blocks), §3 (cognitive infrastructure), §4 (why documents fail), §5 (typed objects, relations, lifecycle, validation, metamodel).
- *Chapter 7, Automating Enterprise Architecture Execution* — §1 (motion punchline: AI amplifies semantic weakness).
- *Chapter 8, From Intent to Specification* — §1 (the missing architectural act; governed-design-space framing), §2 (intent and PRD as demand artifacts), §3 (the architecture translation problem), §4 (`DecisionRecord` typed object and rejected-alternatives discipline), §5 (`ArchitectureSpecification` typed object), §6 (derived executable constraints — worked Rego policy `pv_intake.agent_permissions` with compliant / non-compliant request examples and traceable `deny_reasons`), §7 (`EvaluationSuite` typed object — evals as the second executable control bound by `protects: RULE-ID` to specification rules), §8 (delivery implication — PRD + specification as paired inputs), §9 (six failure modes, including the *false specification*), Appendix A (end-to-end walkthrough). **Read end-to-end from manual fetch 2026-05-13.**

**Sources reviewed status:**

| Chapter | Status |
| --- | --- |
| Chapter 1 | Covered (Round-4 initial pass) |
| Chapter 3 | Covered (Round-4 initial pass) |
| Chapter 6 | Covered (Round-4 initial pass) |
| Chapter 7 | Covered, §1 only (Round-4 initial pass) |
| Chapter 8 | Read end-to-end from manual fetch 2026-05-13 |

**Blocked URLs encountered:** none. Per round conventions, the chapter resource sections were not fetched.

**Open follow-ups:**

- Cluster B / Chapter 2: *continuous architecture* framing alongside the intent artifact for our Healer / production-trace loop.
- Cluster C / Chapter 4: "agent harness" vs "intent thinking" split (Ch7 §2); the architecture-package object (Ch7 §2.2) as candidate replacement for per-issue `STRATEGY.md`.
- Author the actual JSON Schema for our spec template's Intent block, mirroring Ch3 Appendix A.2; extend with a sibling `ArchitectureSpecification` schema mirroring Ch8 §5.
- Update `research/followup/07-evals-deepdive.md` with the `protects: RULE-ID` linkage pattern from Ch8 §7: each eval metric should point back to a specific specification rule, so a metric failure is traceable to a violated architectural commitment.
- Update `research/followup/08-security-primitives.md` with the Ch8 §6 framing of OPA/Rego as the *runtime expression of an architectural decision* (Rego package bound by ID to `DecisionRecord` and `ArchitectureSpecification`), and the traceable-`deny_reasons` pattern.
- Cross-reference with the parallel Chapter 9 drain in `research/24-el-kaim-book-product-line-variability.md` once that report is in place; Ch8's `variation.allowed` / `variation.prohibited` envelope is the surface Ch9's SPL framing builds on.
