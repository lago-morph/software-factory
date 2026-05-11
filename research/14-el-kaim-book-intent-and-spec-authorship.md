# El Kaim — Intent-Driven Architecture and Spec Authorship

**Round-4 Cluster A.** Source: William El Kaim, *AI-Augmented Enterprise Architecture* series, Chapters 1, 3, 6, 7.
**Scope:** vocabulary; the nine-field structured-intent model; the three authoring paths and the OPA/Rego meta-validation gate; cautionary cases for unstabilized direction; concrete proposals for our spec template.

Per round conventions, El Kaim's "ACME Pharma" running example is generalized when quoted; SAP / clean-core material from Chapter 5 is out of scope (separate cluster).

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

## Sources

- *Chapter 1, The Limits of Traditional Enterprise Architecture* — §1 (vocabulary), §3 (decision system), §4.1–4.3 (typed decision), §5 (encoded decision example), §7 (risks).
- *Chapter 3, Intent-Driven Architecture* — §2 (Healthcare.gov, Universal Credit), §3 (Working Backwards / Hoshin Kanri / Backstage / Crossplane), §4.1 (nine-field anatomy), §4.2 (worked example), §5.1–5.3 (three authoring paths), §5.4 (OPA dual role), §5.5–5.6 (six-stage pipeline), Appendix A (grammar, JSON Schema, semantic notes).
- *Chapter 6, The Enterprise Architecture Codex* — §1 (vibes-to-codex), §2 (four building blocks), §3 (cognitive infrastructure), §4 (why documents fail), §5 (typed objects, relations, lifecycle, validation, metamodel).
- *Chapter 7, Automating Enterprise Architecture Execution* — §1 (motion punchline: AI amplifies semantic weakness).

**Blocked URLs encountered:** none. Per round conventions, the chapter resource sections were not fetched.

**Open follow-ups:**

- Cluster B / Chapter 2: *continuous architecture* framing alongside the intent artifact for our Healer / production-trace loop.
- Cluster C / Chapter 4: "agent harness" vs "intent thinking" split (Ch7 §2); the architecture-package object (Ch7 §2.2) as candidate replacement for per-issue `STRATEGY.md`.
- Author the actual JSON Schema for our spec template's Intent block, mirroring Ch3 Appendix A.2.
