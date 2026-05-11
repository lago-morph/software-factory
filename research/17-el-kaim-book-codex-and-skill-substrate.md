# El Kaim — The Enterprise Architecture Codex and the Claude-Skill Substrate

**Source chapters (local, do not delete):**
- `research/manual/multi/Chapter 6 The Enterprise Architectu.txt` (William El Kaim, "The Enterprise Architecture Codex", Apr 2026 — load-bearing, §§1–13)
- `research/manual/multi/Chapter 4 Why AI and Automation Cha.txt` §3 (MCP, architecture-as-code, named skills, coding agents in the delivery flow)

**Cross-references in this repo:**
- `research/04-every-skill-libraries.md` (Every.to skill-library taxonomy, frontmatter conventions, marketplace pattern)
- `.claude/skills/` (current local skill set: `adr`, `always-commit-skill-to-repo`, `fetch-blocked-urls`, `in-flight-workflow-tracking`, `parallel-subagent-fanout`, `research-pipeline`, `self-retrospective`, `subagent-prompting`)
- `architectures/00-comparison.md` §4.2 (shared role primitives across the four factory architectures)

---

## 1. Why this report exists

Round-3 treated "skills" as a delivery primitive — small named trigger-routed Markdown bundles loaded on demand. El Kaim argues the same physical substrate can carry a different category of object: **typed normative artefacts** (principles, standards, reference architectures, blueprints) governed as code. Chapter 6 names this stack the *Enterprise Architecture Codex* — the layered, semantically grounded, executable knowledge base Report 04 and the §11.11 compound-knowledge thread reached toward but did not spell out. This report extracts the load-bearing pieces and ends with a concrete proposal: extend our local skill library to carry typed objects, not only how-to skills.

---

## 2. The four TOGAF building blocks as typed objects (Ch. 6 §2, §5, §7)

El Kaim grounds the Codex in the TOGAF Architecture Content Framework. Mature EA practice has always produced four kinds of artefact (§2.1–2.4); the Codex contribution is not a new vocabulary but a re-carriage of each one as a typed schema with executable validation logic (§5).

| Object | What it asserts | Key schema fields (Ch. 6 §7) |
|---|---|---|
| **Architecture Principle** | A normative rule for how the enterprise expects technology decisions to be made (e.g. AI-005 *Human-in-the-Loop Escalation*) | `id`, `name`, `category`, `status`, `statement`, `rationale`, `appliesTo.factSheetTypes` + `filter`, `validation.check`/`field`/`expected`/`severity`, `relatedPrinciples` |
| **Technology Standard** | Approved / restricted / deprecated instances in a category, with a radar position (e.g. STD-AI-004 *Policy-as-Code Engine*) | `technology.{name,minimumVersion}`, `applicability`, `constraints`, `exceptionProcess.{owner,slaBusinessDays}`, `validation.{check,against,rule}`, `obsolescenceSignals[]`, `linkedPrinciples[]` |
| **Reference Architecture** | A reusable structural pattern (REF-AIAGENT-001's four-layer Governance / Orchestration / Agent / Data model) | `layers[].{id,position,role,requiredComponents}`, `relationships[].{from,to,via,type,policyBinding}`, `invariants[].{id,rule,severity}`, `renderedBy.skill`, `derivedFromPrinciples` |
| **Blueprint / Transformation Roadmap** | A typed sequence of transitions from current to target state (ROADMAP-AIAGENT-PV-001) | `currentState`, `targetState`, `transitions[].{preconditions,deliverables,kpis,exitGate}`, `feedbackSignals[].{source,trigger,action}`, `linkedSpecifications`, `linkedPrinciples` |

Three properties make the four objects governable rather than rhetorical (§5.1–5.5):

1. **Schema.** Every artefact has fields, written and reviewed against a schema; two authors of the same kind produce structurally comparable outputs.
2. **Relations.** Each object names the others it depends on (`linkedPrinciples`, `derivedFromPrinciples`, `linkedSpecifications`). Changes traverse the graph: edit AI-005 and the engine surfaces every standard, reference, and blueprint that cites it.
3. **Executable validation.** `validation.check` is a runnable predicate against the enterprise's EA-tool data (LeanIX fact sheets, in the worked example); `invariants[]` are checked against actual configuration; `obsolescenceSignals[]` re-open standards before the next review cadence. The artefact and its automation are facets of one object (§7.5).

§4: documents preserve *content* but not *the logic between content*. A principle without an applicability rule, validation criterion, or metamodel mapping is "a statement of preference, not a control"; a static-diagram reference architecture "decays the worst" because its snapshot conditions silently change underneath it.

---

## 3. The business-domain substrate beneath the four blocks (§3) — the layer Report 04 did not name

The four TOGAF blocks float unless they bind to a layer of **enterprise cognitive infrastructure** (§3.5) made of four typed object kinds:

- **Business capability map (§3.1).** Units of business function (CAP-PV-001 *Adverse Event Intake*) with `domain`, `owner`, `criticality`, `parent`/`children`, `regulatoryAnchors[]` (binds to *EMA GVP Module VI*, *21 CFR 314.80*), `supportedBy[]` (links to portfolio apps), `linkedIntent`, `linkedPrinciples`, `owningCouncilMember`. The anchor point principles and standards filter against — without it, a principle either misses the application or over-applies.
- **Enterprise intent (§3.2).** Strategic intent (INTENT-PV-001) lives alongside capabilities, not above them; one intent touches multiple capabilities, and the Codex tracks the links so intent-evolution ripples through downstream decisions.
- **Semantic glossary / ontology (§3.3).** Typed term definitions, synonym mappings, scope boundaries. Stops an AI assistant producing "fluent but semantically wrong" content when "customer" or "adverse event" means different things across units.
- **Organizational model (§3.4).** The EA Council, its L1–L4 delegation classes, escalation paths, approval thresholds — resolves required reviewers from merge requests (replacing static CODEOWNERS that ages out) and names accountable owners on compliance reports.

The graph closes: principle AI-005 → reference REF-AIAGENT-001 (`policyBinding`) → capability CAP-PV-001 (`appliesTo`) → intent INTENT-PV-001 (`linkedIntent`) → Council domain lead (`owningCouncilMember`).

---

## 4. The Git repository layout (§6) — and the diff against our `.claude/skills/`

Chapter 6 §6.1 sketches the ACME Pharma Codex repo:

```
acme-codex/
├── .claude/
│   ├── marketplace.json          # manifest exposing the repo as a marketplace endpoint
│   └── settings.json             # routing / activation rules
├── skills/
│   ├── ea-principles/            # SKILL.md + general/, ai/ YAML object files
│   ├── ea-standards/             # SKILL.md + catalog/ YAML
│   ├── ea-reference-architectures/
│   ├── ea-blueprints/
│   ├── business-capabilities/
│   ├── enterprise-intent/
│   ├── enterprise-ontology/
│   ├── ea-council/
│   ├── bmad/                     # Brief / Map / Act / Double-check
│   ├── compliance/
│   └── diagram-generation/
├── references/
└── tests/scenarios/
```

Each skill folder carries a `SKILL.md` with YAML frontmatter (§6.2):

```yaml
name: ea-principles
description: |
  ACME Pharma enterprise architecture principles. Activates when reviewing
  an application design, assessing an AI agent, authoring a new design
  decision, or evaluating compliance. ...
version: 2.3.1
triggers:
  keywords: [principle, AI principle, compliance check, EU AI Act, design review]
  contexts: [design-review, agent-assessment, decision-authoring, merge-request-review]
dependencies: [enterprise-ontology, ea-council, business-capabilities]
```

`.claude/marketplace.json` (§6.3) names `publishedSkills[]`, a `source.{type,url,branch,skillsPath}` block, a `refresh` policy, and an `accessControl.requiredGroups[]` list. Claude Desktop / Claude Code subscribe to the manifest; on session start they pull, and on prompt match they load skills on demand. Three layers compose at load time (§6.4): internal, shared, public — enterprise-local skills take precedence on trigger overlap.

### How this compares to `.claude/skills/` in this repo

The local skill set is purely *process-oriented* (`adr`, `always-commit-skill-to-repo`, `fetch-blocked-urls`, `in-flight-workflow-tracking`, `parallel-subagent-fanout`, `research-pipeline`, `self-retrospective`, `subagent-prompting`). Frontmatter is `name` + `description` only — no `version`, no explicit `triggers.keywords/contexts`, no `dependencies`. There is no `.claude/marketplace.json` (the manifest El Kaim treats as the distribution surface) and no typed-object folders under any skill.

Report 04's `everyskill` is closer (frontmatter has `version` and `allowed-tools`; a `submit-to-everyskill` meta-skill approximates the marketplace-submit endpoint). But `everyskill` is still a *horizontal* how-to library — none of its entries carry **typed enterprise objects** with `validation.check` predicates against external data. That is the structural gap §3 fills: keep the SKILL.md envelope, put typed YAML domain objects under it, let the skill body explain how to use the objects while the objects themselves carry the executable claims.

---

## 5. The five-layer Codex model (§12)

§12 stacks the Codex in five layers, each one or more skills in the Git repo:

1. **Enterprise Semantic layer.** Business-capability map, enterprise-intent catalog, semantic glossary / ontology, organizational model (Council + L1–L4 delegation). "The substrate; everything above derives from it."
2. **Architectural Artifacts layer.** Principles, standards, reference architectures, active blueprint portfolio — the four TOGAF blocks of §2.
3. **Operating Model layer.** BMAD (Brief / Map / Act / Double-check), the compliance scoring skill, the decision registry (each entry linked to its intent / capability / principles), the EA Council skill (resolves reviewers on merge requests). "This is how the Codex content becomes a decision system rather than a reference."
4. **Deliverables layer.** Catalog / matrix / diagram generation rules. Nothing here is manually authored; every artefact is a projection over the three layers below (§8).
5. **Integration layer.** Connectors out: EA-tool MCP server (LeanIX, Ardoq), Open Policy Agent for Rego evaluation, Git provider for the merge-request workflow, delivery pipelines and audit stores that consume Codex outputs.

Wrapping all five is the **Distribution Surface**: the Git repo, the marketplace manifest, the Claude Desktop / Claude Code clients that subscribe.

Two invariants close §12: every object is *linked to* objects in other layers; every object is *executable* against enterprise data — "the Codex is not documentation about the enterprise, but the enterprise expressed in a form that both humans and systems can act on" (§12 final notes).

---

## 6. The validation chain — JSON Schema, Rego, MCP, and the failure modes (§5, §9.2, §11)

The chapter does not name a single validator; it describes a *chain* whose links each catch a different class of error.

- **JSON Schema (implicit in §5.1, §7).** The `apiVersion: ea.codex/v1` + `kind: <ObjectType>` envelope sets the shape: a principle has `statement`, `rationale`, `appliesTo`, `validation`; a standard has `applicability`, `constraints`, `obsolescenceSignals`; a reference has `layers`, `relationships`, `invariants`. Shape-validity is what stops a merge request from introducing a malformed artefact.
- **Rego / Open Policy Agent (§9.2).** Cross-field and runtime constraints that schemas cannot express: the AI-Gateway Rego policy is *generated from* AI-005 and AI-006's validation fields plus the agent's `prohibitedActions` list, and it `deny`s any agent action whose `humanReviewRoute` is unset or whose `action` is on the prohibited list. The Rego layer is what enforces principles at *execution* time, not only at design-time review.
- **MCP for retrieval grounding (Chapter 4 §3.1; Chapter 6 §13.3).** The Codex skills read LeanIX or Ardoq fact-sheets through MCP servers; SAP LeanIX's MCP server exposes its GraphQL API as MCP tools and Ardoq's AI Gateway provides metamodel-aware access. Grounding is what makes `validation.check` runnable — without MCP, the principle has nothing concrete to evaluate against; with it, the integration cost drops from "weeks of custom connector work to a configuration entry" (Ch. 4 §3.1).

§11 then names the failure modes that this chain does *not* catch:

- **Codex-as-prompts risk (§11, ¶2).** When Codex content is loaded as an AI assistant's instruction context, interpretation depends on the model's prompt-following behaviour — *across model versions, the same content can be interpreted differently*. Mitigation: an evaluation harness running representative scenarios on each model change, surfacing interpretation drift before production.
- **Skill marketplace risk.** As skill count grows, overlapping triggers compete; provenance accumulates without owners. Editorial discipline or sub-agent packaging are the mitigations.
- **Git discipline dependency.** Sloppy MR review collapses the Codex back to Word-document decay.
- **Coverage gap.** What is not in the Codex is not governed; the coverage map must be deliberately maintained.
- **Schema-evolution discipline.** Adding a field affects every artefact of that kind; migration plans, backward compat, version pinning required.

---

## 7. EA-tool vendor landscape (§13) — one paragraph

§13 sketches three vendor trajectories: (a) **incumbent absorbs** (Ardoq, SAP LeanIX host typed principles natively — most shipped capability today, but principles remain "text fields on a governance object" and ontology/policy-engine are architectural mismatches not feature gaps); (b) **Codex absorbs EA tool** via AI-native platforms (Peaqview), data-platform + graph overlays (Databricks/Snowflake + Neo4j/GraphDB), or open-source toolkits (ArcKit's 68 commands) — flexible but multi-vendor assembly burden; (c) **the two compose** through MCP — the dominant near-term configuration and El Kaim's 2026 recommendation regardless of long-term direction. Procurement detail, out of scope for our factory blueprint.

---

## 8. Concrete extension proposal: typed-object skills in our library

Today our `.claude/skills/` carries eight procedural skills. None of them carry typed normative objects. The proposal is to add a second skill *kind* — a **typed-artefact skill** — that uses the existing SKILL.md envelope but adds enforced structure underneath.

**Concrete shape:**

```
.claude/skills/
├── <procedural skills as today>
├── factory-principles/                    # new
│   ├── SKILL.md                           # frontmatter + how-to body
│   ├── schema/principle.schema.json       # JSON Schema for the kind
│   └── catalog/
│       ├── F-PRIN-001-spec-before-code.yaml
│       ├── F-PRIN-002-judge-is-model-family-independent.yaml
│       └── F-PRIN-003-trajectory-is-recorded.yaml
├── factory-standards/                     # new
│   ├── SKILL.md
│   ├── schema/standard.schema.json
│   └── catalog/
│       └── F-STD-001-conventional-commits.yaml
├── factory-reference-architectures/       # new
│   ├── SKILL.md
│   ├── schema/reference.schema.json
│   └── REF-FACTORY-001-four-layer-spec.yaml
└── factory-roles/                         # the §3 substrate, light version
    ├── SKILL.md
    └── roles/{strategist,judge,manager,operator}.yaml
```

**SKILL.md frontmatter changes** (adopt the El Kaim form, additive to Every's): add `version`, `triggers.keywords[]`, `triggers.contexts[]`, `dependencies[]`. The local skills can keep their current frontmatter; the new typed-artefact skills require the full form because the marketplace-style routing depends on it.

**Validation chain (small footprint):**
- **JSON Schema** under each typed-artefact skill, enforced by a pre-commit / CI check that validates every YAML in `catalog/` against `schema/*.schema.json`. This catches malformed objects at MR time.
- **Cross-field checks** as a thin script (Python or Rego) that walks the catalog and verifies references resolve — every `linkedPrinciples` entry exists, no dangling `derivedFromPrinciples`, every `appliesTo.factSheetTypes` is in the role catalog. This is §5.2's "relations form a graph that can be traversed automatically".
- **Evaluation harness against model drift** (the §11 mitigation): a `tests/scenarios/` directory where each typed object has at least one scenario the harness runs at each model upgrade, asserting the model's interpretation of the principle still produces the expected `deny` / `allow` / `flag` outcome. This is the *only* defence against the Codex-as-prompts failure mode and should be added alongside the typed-artefact skills, not after them.

**What this unlocks for the factory:**
- The four architectures compared in `architectures/00-comparison.md` §4.2 share role primitives (Strategist, Spec Author, Judge, Reviewer, Knowledge Curator, Manager, Operator). Today those primitives live in narrative comparison tables. As typed `roles/*.yaml` objects with `delegationLevel`, `requiresHumanApproval`, `outputs`, `dependencies` fields, they become loadable into any subagent prompt and validatable against a chosen architecture's required role-set.
- The compound-knowledge thread (§11.11 in PLAN.md) can be made concrete: each architecture decision in `docs/adr/` references the principle objects it depends on, and a change to a principle surfaces every ADR that cites it — the §5.2 "relations form a graph" invariant applied to our own decision history.
- Report 04's *symphony-thumbtack* five-skill git-flow set (`commit`, `pull`, `push`, `land`, `tasks`) stays procedural and unchanged. The new typed-artefact skills sit alongside it; the two kinds compose, with the procedural skill calling the typed-artefact skill for normative context ("when running `land`, load `factory-principles` to verify the merge does not violate F-PRIN-002").

**What this defers:** the full §12 five-layer Codex (ontology layer, business-capability map, intent catalog, Council organizational model, BMAD operating skill, MCP integration into LeanIX/Ardoq) is out of scope for a software factory whose primary domain is its own delivery practice. We borrow the typed-artefact + schema + cross-field-check + marketplace-frontmatter pattern; we do not borrow the enterprise-pharma scaffolding around it. The §11 evaluation harness, however, is *not* deferrable — without it, model drift can silently invert the meaning of our own factory principles.

---

## 9. Follow-ups for later rounds

- A worked draft of `factory-principles/catalog/` extracting concrete principle objects from `architectures/00-comparison.md` and the four-architecture analyses (e.g. *spec-before-code*, *judge-is-model-family-independent*, *trajectory-is-recorded*, *human-approves-at-named-gate*).
- A worked draft of `factory-roles/roles/*.yaml` carrying the §4.2 shared-role rows as typed objects with required-tool and required-context fields.
- A choice between Rego (matches El Kaim's chain exactly) and a simpler Python-driven cross-field validator (fewer moving parts; adequate for our scale).
- Specification of the model-drift evaluation harness against the §11 failure mode — likely a `tests/scenarios/` directory plus a CI job triggered on Anthropic model-version bumps.
