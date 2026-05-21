# Report 24 — El Kaim Chapter 9: Software Product Lines and Variability

**Date:** 2026-05-13
**Author:** Lead agent (drained from manual fetch)
**Status:** complete
**Round:** 6 (post-#29/#30/#31 drain)
**Source:** William El Kaim, *AI-Augmented Enterprise Architecture* series, Chapter 9 ("Software Product Line and Variability").

Per round conventions, El Kaim's running examples (ACME Pharma's digital-study platform, customer-identity-platform) are generalized to enterprise-level language when quoted. A sibling subagent is draining Chapter 8 into `research/14-el-kaim-book-intent-and-spec-authorship.md` in parallel; Chapter 9's product-line / variability material does not fit cleanly into reports 14, 15, 16, or 17 and is therefore drained into this new dedicated report.

---

## Lead question

What does Chapter 9 add to our corpus that the existing twenty-three reports and twelve followups do not already cover? The four candidate architectures (`architectures/01-specification-refinery.md`, `02-compound-atelier.md`, `03-phase-gated-foundry.md`, `04-evolutionary-tournament.md`) all assume a single product target: one repo, one spec, one converging artifact. The four existing El Kaim reports (14–17) cover intent, BMAD/attractor flow, the L1–L4 delegation council, and the Codex skill substrate — all framed at the level of a single architectural decision or a single deliverable. Chapter 9 introduces a unit-of-work above that level: a *family* of related solutions sharing a managed core and a bounded variability envelope. It names the discipline that turns one-shot spec authorship into a generative seed for many derived products, and it forces the enterprise to declare which concerns are stable, which are allowed to vary, and at what moment a variation is bound. Nothing else in our corpus addresses multi-product variability as a first-class architectural concern.

## Why this report exists

Our methodology can author one spec well. It cannot yet answer the question "we are about to build the fourth near-duplicate of this — what should be the same and what is allowed to differ?" Chapter 9 names that as the central question and gives it a typed object (`kind: ProductLineDefinition` / `kind: ProductLineSpec`), a vocabulary (commonality, variation points, binding times, derivation rules, core assets, variation budgets, family decay), and a derivation discipline (a family generates a bound product model rather than being copy-pasted into one). It anchors the discipline in the SEI literature distinguishing planned product lines from opportunistic reuse, and in three working systems (Linux Kconfig, Azure Landing Zones, AUTOSAR feature models) that demonstrate variability at scale.

The gap is concrete. `spec-driven-ai-dev.md` has no field for "this spec is one member of a family"; `architectures/00-comparison.md` has no dimension for "supports family-level reuse with bounded variation"; the F-mode catalog has no failure mode for "the enterprise believes it has a product line while running a loose federation of descendants" (Ch9 §7). This report fills those gaps and proposes — not asserts — the additions our methodology should consider.

---

## 1. Family-based architecture as the unit of work (Ch9 §1)

Chapter 9 reframes the unit of architectural work. Where intent (Ch3) and the architecture specification (Ch8, drained into `research/14-el-kaim-book-intent-and-spec-authorship.md` §13) are scoped to one solution, a *family architecture* is scoped to a managed set of related solutions. The load-bearing definition: "a managed family of software-intensive systems that share core features and core assets while accommodating specific differences for a bounded market or mission" (Ch9 §1). The chapter then immediately deflates the word "product": "What matters in that definition is not the word 'product.' What matters is the idea of a family, the presence of a deliberate core asset base, and the fact that variability is managed rather than tolerated as drift" (Ch9 §1).

This is the move that makes the discipline applicable to enterprise architecture rather than only to boxed software. Ch9 §1 enumerates concrete enterprise-shaped families: a country rollout model for an ERP platform; a family of digital onboarding solutions; a regulated workflow platform for several business units; a set of internal developer platforms for different risk zones; a family of AI-enabled service patterns "with bounded differences in data residency, approval flow, and model usage" (Ch9 §1). The takeaway is that almost any enterprise solution category that recurs is a family candidate, not a one-off architecture engagement.

The SEI anchoring is load-bearing for our methodology grounding: Ch9 §1 explicitly cites SEI literature "distinguish[ing] planned product lines from opportunistic reuse and from single-system development with borrowed assets." Our current methodology defaults to the third category (borrowed assets — copy-paste from prior repos, ad hoc skill imports). The progression Ch9 names is the direction we should move in: opportunistic reuse → planned product line.

## 2. The bounded question set (Ch9 §1, §2)

Chapter 9 §1 names a deliberate, bounded set of questions that the discipline forces an enterprise to answer:

1. Which concerns are *common* to every member of the family?
2. Which are allowed to *vary*?
3. At what moment is a variation *bound*?
4. Which *assets* are shared across the family?
5. Which *decisions* govern valid combinations?
6. Which *derivation path* turns the family definition into a concrete product instance?

These questions, Ch9 §1 argues, "force the enterprise to define what is stable, what is variable, and what must remain governable." This three-way split — stable / variable / governable — is the conceptual core of the chapter. It is sharper than our current "spec / non-goals / decision seeds" triad because it explicitly admits a *third* axis: governability. A choice can be variable yet still required to remain inside an envelope the architecture knows how to verify. That governable-but-variable category is what reference architectures fail to express (Ch9 §2: "they often leave unanswered the question delivery teams actually face: which subset applies here, under which conditions, with which allowed substitutions, and with which non-negotiable constraints?").

The chapter's diagnostic for traditional EA: "Variability is recorded after the fact rather than designed as part of the architecture" (Ch9 §2). The corrective stance: "Architects must stop treating variability as an exception to a reference model and start treating it as a design concern with its own structure" (Ch9 §2).

## 3. The three working-system anchors (Ch9 §3)

Ch9 §3 grounds the discipline in three live systems. The point of each is that variability can be made explicit, machine-readable, and constraint-aware rather than handled in spreadsheets, tribal knowledge, or architecture review meetings.

**Linux Kconfig** (Ch9 §3): "a configuration database organized as a tree of options, supporting defaults, dependencies, and constrained selection logic." The lesson Ch9 extracts is not the syntax but the discipline: "A large family of related products is maintainable when options are named, dependencies are formalized, defaults are controlled, and invalid combinations are prevented before realization proceeds." Variability is useful "only when the dependency model is precise enough to keep the family coherent."

**Azure Landing Zones** (Ch9 §3): a "modular, repeatable platform architecture with a reusable core and bounded tailoring," with "a family scope (enterprise Azure estates), a stable core (identity, management groups, governance, policy, connectivity, platform baselines), variation points (deployment scenarios, topology choices, organizational segmentation, rollout paths), and a derivation mechanism (modular reference implementations and templates)." Ch9 reads this as "product-line thinking in infrastructure clothing."

**AUTOSAR feature model** (Ch9 §3) supplies the most formally precise vocabulary, distinguishing three layers that Ch9 wants the enterprise architect to keep separate:

- **Feature model** — "describes available features and their relations" (problem space).
- **Product line model** — "captures the family with variation points" of all binding times (solution space).
- **Product model** — "created by keeping some variations and discarding others through binding" (a derived realized instance).

Ch9 §3 makes the demand explicit: "Enterprise architecture often blurs those layers... Product-line discipline forces a cleaner separation. The family is not the instance. The feature space is not the bound design. The reference model is not the delivered product."

## 4. The `ProductLineDefinition` / `ProductLineSpec` Codex object (Ch9 §4, §5)

Ch9 §4 introduces a new typed object for the Enterprise Architecture Codex (extending the typed-object discipline drained into `research/17-el-kaim-book-codex-and-skill-substrate.md` §2). The schema (`apiVersion: ea.codex/v1`, `kind: ProductLineDefinition`) binds:

- `intent` — the family-level statement of direction (one level above the per-spec `Intent` block we drained into report 14 §3).
- `scope` — the capabilities and in-scope product types the family serves.
- `common_assets` — the invariant core: domain model, services, controls. Ch9 §4: "defines the invariant core, including domain objects and controls, making the family semantic and governable rather than only technical."
- `variation_points` — each named, typed (`alternative` / `multiple` / `optional`), with allowed values and an explicit `binding_time`.
- `derivation_rules` — when/require/forbid clauses connecting variant selection to policy consequences.
- `decision_links` — references to `DecisionRecord` artifacts (typed in Ch8) that govern variation points as enterprise architectural choices.
- `product_derivation` — typed inputs (selected variant values, applicable policies) and typed outputs (`target_architecture_spec`, `control_profile`, `deployment_template`).

The mental model Ch9 names directly: "A product line definition is not merely a documentation object. It is a seed in the sense introduced in Post 5. The `ProductLineDefinition` serves as the structured contract that drives the attractor loop... The family definition is the seed. The derivation logic is the generation path. The conformance checks are the validation harness" (Ch9 §4). This is the same attractor-loop vocabulary drained into `research/15-el-kaim-book-bmad-attractor-dark-factory.md` §6, *lifted one level* to family scope: the convergence metric is now "the proportion of family instances that satisfy the conformance rules across the scenario pack without drift" (Ch9 §4).

## 5. Binding times as the governance axis (Ch9 §4)

Each variation point in the schema carries an explicit `binding_time`. Ch9 §4 names four binding-time tiers in the worked artifacts and adds a stratification of *who* owns each tier:

- **strategy/decision** binding — the choice requires an explicit architectural decision with governance consequence. Example from Ch9 §4: `deployment_mode: shared|dedicated` is bound at *decision* time because Ch9 §5 decision DD-ACME-041 forbids interventional studies on shared hosting. "Certain choices belong to enterprise policy, some to platform teams, some to solution architects, and some to runtime configuration. Product-line thinking forces those boundaries to be explicit" (Ch9 §4).
- **design** binding — the choice is fixed when the bound product model is authored. Example: `assurance_level: standard|strong|qualified` is bound at design time.
- **build** binding — the choice is resolved at build/assembly time. Example: `channel_adapter: web|mobile|contact-center|partner-api` (multiple).
- **deployment** binding — the choice can be resolved per environment without changing the architecture. Example: `region_pack: EU|US|APAC` is bound at deployment time. Ch9 §4 contrasts these directly: "`deployment_mode` has binding_time 'decision' because it requires an explicit architectural choice with governance consequence, while `region_pack` has binding_time 'deployment' because it can be resolved later without changing the architecture."

This stratification is the load-bearing operational primitive of the chapter. Without it, "every program performs its own binding work" (Ch9 §2). With it, binding responsibility is explicit per variation point, and the same governance forum that owns the family owns the audit trail of which variants were bound when, by whom, and against which decision record.

## 6. Top-down design vs. bottom-up discovery (Ch9 §4)

Ch9 §4 explicitly admits two valid paths to identifying a family — directly answering the practical question "how do we know when something is a family?":

- **Top-down design** — "appropriate when the enterprise knows in advance that it will build multiple related solutions (a multi-country regulatory platform, for example)."
- **Bottom-up discovery** — "appropriate when the enterprise has already built several solutions and recognizes recurring structure. In this case, the product-line discipline works by extracting the common core and naming the variation points after the fact, then governing future instances through the family architecture rather than allowing continued ad hoc divergence" (Ch9 §4).

This is methodologically important for our context because most software-factory work today produces opportunistic-reuse artifacts (a skill is copied from one repo to another, a brainstorm template is forked). Bottom-up family discovery is the migration path *from* our current state *to* product-line discipline, without requiring an upfront commitment to family modeling.

## 7. Cross-family composition (Ch9 §4)

Ch9 §4 also names what happens at family boundaries. A derived product may need to compose assets from two families (a customer-identity-platform and a digital-study-platform). The chapter's answer: "The family architecture should therefore define its integration contracts explicitly (the services in `common_assets` and the interface contracts those services expose) so that products derived from different families can compose through governed interfaces rather than through ad hoc integration." Composition is a property of the family contract, not of the derived product. This anticipates a failure mode that our current methodology would silently absorb (two specs each declaring its own integration contract and discovering incompatibilities only at integration time).

## 8. Variation budgets and family decay (Ch9 §4, §7)

Ch9 §4 names "variation budgets" as a typed concern: "Every allowed variation has a cost in operational support, test burden, audit scope, and integration complexity. A family architecture makes those costs visible and prevents unconstrained expansion." Ch9 §7 enumerates the trade-offs and failure modes the discipline carries:

1. **Modeling cost** — visible early, payoff only at repeated use. "Enterprises that do not commit to repeated use will see only the cost."
2. **Over-generalization** — anticipating every future difference. "Product-line discipline is not the art of maximizing flexibility. It is the art of choosing a bounded and economically meaningful flexibility."
3. **Political friction** — bounded variation removes some local freedom; "Business units accustomed to negotiating bespoke solutions may interpret that as central control."
4. **Testing complexity** — scales with the variation surface; decisions that *forbid* combinations protect operational simplicity.
5. **Family decay** (named by Ch9 §7 as "the most insidious failure mode") — "A family decays when product instances evolve locally faster than the core asset base. Teams add local patches, regional overlays, and urgent workarounds that never flow back into the family model. Over time the enterprise believes it has a product line while running a loose federation of descendants."
6. **Constraint conflicts** — derivation rules can interact non-obviously; "The family architecture should include constraint-checking logic, applying the same rule-evaluation mechanism used for derivation itself, so that incompatibilities are detected before a product is derived rather than after it has entered delivery."
7. **Poor-fit problem spaces** — "When the problem space is highly exploratory, when repetition is weak, or when every solution has deep uniqueness, formalizing a family prematurely will produce bureaucracy without leverage."
8. **Cultural reframing** — Ch9 §7 names this as "the deepest challenge": "Product-line architecture replaces a heroic notion of architecture (solving each project anew) with a more industrial notion (designing families, assets, and derivation paths)."

## 9. Derivation rules as policy-as-code (Ch9 §5)

Ch9 §5 demonstrates that derivation rules are not documentation; they are executable. The worked example (an `acme.studyplatform` Rego package) shows three deny rules expressing family-level constraints: interventional studies must use dedicated hosting; EU deployments require EU data residency controls; constrained-workflow AI requires a human review step. Ch9 §5: "A project cannot merely claim alignment with the [enterprise] platform family. Its chosen variant can be checked automatically against the product-line rules. That is a concrete instance of the series's thesis: architecture becomes executable when decisions and constraints are formal enough to participate in delivery flow."

This is the *third* role for OPA/Rego in El Kaim's framework, on top of the two roles drained into `research/14-el-kaim-book-intent-and-spec-authorship.md` §5 (meta-validation of the intent artifact; downstream enforcement of declared invariants). Role 3 is **family-membership enforcement**: a derived product's variant configuration is checked against the family's derivation rules before realization proceeds.

## 10. What changes for the architect's role (Ch9 §6)

Ch9 §6 names the operational shift bluntly: "architects stop centering every engagement on a single-solution design cycle. A significant portion of their work shifts toward family scoping, variability governance, asset curation, and derivation logic. Architecture review checks whether the requested product belongs in an existing family, whether its variation choices are valid, and whether the family itself needs to evolve."

The boundary between enterprise architecture and platform engineering blurs in a productive direction (Ch9 §6): "Enterprise architects define family scope, policy linkage, and semantic commonality. Platform and solution architects define technical assets, derivation mechanics, and control automation. Product managers or capability owners decide where repeatability is strong enough to justify family investment." This is a typed division of labor — comparable in spirit to the L1–L4 delegation classification drained into `research/16-el-kaim-book-council-and-delegation.md` §1, but oriented along *family ownership* rather than per-deliverable accountability. The two are complementary, not redundant.

Ch9 §6 adds a velocity constraint that maps directly to our concerns about agent throughput: "The discipline only works if the architect can answer those questions quickly enough that the delivery team's velocity is preserved. A family architecture that is correct but slow to consult will be routed around, and the family will decay into irrelevance even when its intrinsic design is sound." This generates a derived requirement for our methodology — see §12 below.

---

## How Chapter 9 connects to our other work

- **`research/14-el-kaim-book-intent-and-spec-authorship.md` §3 (the nine-field intent model).** Chapter 9's `ProductLineDefinition` is what the nine-field intent gets *parameterized over* when the enterprise has a family. The per-spec `Intent` block in report 14 describes one solution's direction; the family-level `intent` block in Ch9 §4 describes the direction shared by every derived member. The relationship is generative: a family intent + a bound variant configuration *produces* a per-spec intent. Conversely, when multiple per-spec intents in our repo share more than they differ, Ch9 §4's bottom-up-discovery path applies — extract the common core and promote it to a family intent.
- **`research/14-el-kaim-book-intent-and-spec-authorship.md` §13 (the `ArchitectureSpecification` object).** Ch9 §4's `target_architecture_spec` output is *exactly* a per-spec `ArchitectureSpecification`. Product derivation is the generation path that turns a family-level Codex object into the per-spec Codex object Chapter 8 defines. The two reports compose: report 14 owns the bound instance; report 24 owns the family that generates it.
- **`research/15-el-kaim-book-bmad-attractor-dark-factory.md` §6 (convergence as satisfaction, not pass/fail).** Ch9 §4 explicitly lifts the attractor loop to family scope: "The convergence metric is the proportion of family instances that satisfy the conformance rules across the scenario pack without drift." This is the same metric shape — satisfaction across a pack — but the pack is now a *scenario × variant* matrix rather than a flat scenario set. Our scenario-pack format (report 15 §4) needs a variant-dimension extension when the spec is a family member.
- **`research/16-el-kaim-book-council-and-delegation.md` §1 (L1–L4 delegation).** Family ownership is orthogonal to L1–L4. A family owner sits above the per-solution delegation tree; the L1–L4 classification applies *within* each derived product. The Council reviews family-level decisions (Ch9 §6: "Architecture review checks whether the requested product belongs in an existing family") in addition to per-product reviews.
- **`research/17-el-kaim-book-codex-and-skill-substrate.md` §2 (typed objects), §4 (Git layout), §8 (typed-object skills).** A `.claude/skills/` directory is a primitive form of shared core asset (Ch9 §1: "the core assets of a family are not only technical. They include policy models, decision records, canonical data contracts, process patterns, compliance controls, deployment blueprints, test packs, integration mappings, and approval logic"). Our skill library currently looks like opportunistic reuse — skills are copied from project to project without a typed declaration of which family they belong to. Promoting the library to a planned product-line core asset base would require: declaring the family scope each skill serves; naming each skill's variation points; and recording binding times for any options the skill exposes.
- **`architectures/00-comparison.md`.** None of the four candidate architectures currently addresses multi-product variability. Specification Refinery, Compound Atelier, Phase-Gated Foundry, and Evolutionary Tournament all assume the unit of work is one converging artifact. Chapter 9 names this as a corpus-level gap. We should *flag*, not assert, that none of the four is currently a family-aware architecture; whether to extend any of them to family scope is a future decision. The cleanest extension candidate is Phase-Gated Foundry (which already has typed SRS/SAD phases) — adding a Phase 0 "family membership" step would mirror Ch9 §6's flow.
- **`research/followup/06-competitor-landscape.md`.** Two real-world examples of variability-binding decisions: Factory.ai's "Droid Computers" primitive (one droid per developer = bind at developer scope) and 8090's two-SKU split (enterprise-tier vs. standard-tier = bind at sales-contract scope). Both are implicit product-line decisions — a binding time has been chosen — but neither vendor publishes a `ProductLineDefinition`-shaped artifact that would let a customer audit which variation envelope they are inside. Ch9 §6's velocity constraint applies: an implicit family that is slow to consult will be routed around.
- **`research/followup/12-brier-pace-layers.md`.** Pace-layered systems are a complementary discipline: the slow layers (governance, semantic core) become a family's `common_assets`, and the fast layers (channel adapters, region packs) become its `variation_points` with build/deployment binding times. Ch9's binding-time stratification operationalizes pace-layer thinking.

---

## What we should adopt

These are *proposals*, not accepted positions.

> **Status note (2026-05-21, issue [#105](https://github.com/lago-morph/software-factory/issues/105)):** `spec-driven-ai-dev.md` is a cataloged source (record [`3592091691`](../reference-only/3592091691/spec-driven-ai-dev.md)), not a mutable internal artifact. Proposal §2 below (and any other change targeting that file) is a research finding that can inform a v3 methodology document authored separately; it is not a pending edit against the source.

**1. Vocabulary additions to our methodology.** Add the following terms to our shared methodology glossary (wherever we record canonical definitions): *family architecture*, *variation point* (with type: alternative / multiple / optional), *binding time* (with the four tiers: decision / design / build / deployment), *core asset*, *derivation rule*, *bound product model*, *variation budget*, *family decay*. Each term should cite Ch9 by section. The progression *opportunistic reuse → planned product line* (Ch9 §1, SEI anchor) is the methodology-level frame.

**2. Structural addition to `spec-driven-ai-dev.md`.** Propose an optional **"Family scope"** block at the top of the spec, sibling to the `Intent` block proposed in `research/14-el-kaim-book-intent-and-spec-authorship.md` §9. Fields: `familyId` (reference to a `ProductLineDefinition`, or `none` for one-off specs); `boundVariants` (the variant values this spec selects, e.g. `region: EU`, `assurance_level: strong`); `familyExtension` (optional — names a genuinely new requirement that the family did not anticipate, flagged for evolving the family rather than absorbed as a one-off, per Ch9 §6). When `familyId` is present, the spec's invariants are inherited from the family's `common_assets.controls` plus the `derivation_rules` activated by the bound variants; only spec-local invariants need explicit declaration.

**3. A new candidate Codex object: `ProductLineDefinition`.** Mirroring Ch9 §4's schema. The object is a sibling to the `ArchitectureSpecification` object drained into report 14 §13, addressable by stable ID and referenced from each member spec's `familyId` field. The validation gate for this object is structural (the meta-validation role from report 14 §5): every variation point must have a binding time; every derivation rule must reference declared variation points; every `decision_links` entry must point to an existing `DecisionRecord`; every `forbid` clause must be satisfiable by at least one legal variant combination (no dead families).

**4. A scenario-pack extension for family-scoped specs.** The scenario pack format from `research/15-el-kaim-book-bmad-attractor-dark-factory.md` §4 currently runs scenarios against one spec. When the spec is a family member, the pack should run scenarios against the *variant matrix* — a sample of legal variant combinations — to measure Ch9 §4's family-level convergence metric. This is an extension, not a replacement: per-spec convergence is still measured; family-level convergence is measured additionally.

**5. Promote the skill library toward planned-product-line discipline.** Currently `.claude/skills/` is opportunistic reuse (Ch9 §1). The migration path is Ch9 §4's bottom-up-discovery route: identify clusters of skills that share more than they differ; extract the common core as a family-level skill spec; declare the variation points each cluster exposes (e.g., "language target" might be a variation point of a code-generation skill family). This is a Round-7+ project, not a Round-6 commitment.

**6. Candidate failure mode F35 — *Federation-as-Family*.** Drawn directly from Ch9 §7's "family decay" passage: *the enterprise believes it has a product line while running a loose federation of descendants*. Proposed failure-mode definition: **F35 — Federation-as-Family Drift.** The artifact (skill library, template set, reference architecture, agent fleet) is treated as a managed family at the governance level — reused, referenced, claimed-aligned-with — while in practice, instances evolve locally faster than the core asset base, local patches and overlays never flow back, and no derivation-rule check is run against new instances. Detection signal: new instances declare alignment with a family but their variant configuration is not validated against any executable rule. Mitigation (Ch9 §7): "Continuous feedback and explicit retirement of unsupported variants are essential to prevent this drift, and the governance forum must hold itself accountable for catching it early." This candidate is a strong fit for our F-mode catalog because the precondition (reuse-as-advice, variability-as-exception) is the *default* state of our current methodology, not an edge case. **Proposed, not asserted accepted.**

**7. A flag against `architectures/00-comparison.md`.** Add a row or note flagging that none of the four candidate architectures currently treats family scope as a first-class concern. This is a gap to make visible; the decision about whether to extend any architecture to be family-aware is deferred.

**What not to import.** Ch9's full AUTOSAR feature-model formalism (Ch9 §3) is heavier than our scale justifies; the three-layer separation (feature model / product line model / bound product model) is useful as a *conceptual* layering inside our Codex but does not require us to adopt AUTOSAR's exchange format. Likewise, Kconfig syntax (Ch9 §3) is not the lesson — the lesson is constraint-aware variability — and our YAML+Rego stack already covers it.

---

## Sources reviewed

| Source | Status | Notes |
|---|---|---|
| El Kaim, "Chapter 9: Software Product Line and Variability" (Medium, 19 min read, posted 2026-05-12; ~37 KB at `research/manual/Chapter 9 Software Product Line and.txt`) | complete | Read end-to-end from manual fetch landed 2026-05-13. Drained into all sections of this report. Source file will be moved to `reference-only/el-kaim-book/` by the orchestrator after the drain commit (not by this subagent). |
| SEI at CMU, *Software Product Lines* (Ch9 §9 reference) | not fetched | Cited by Ch9 §1 as the foundational definition of product lines, core assets, and the planned-vs-opportunistic-reuse distinction. Per round conventions, chapter resource sections were not fetched. Candidate for a future SEI-foundations followup if methodology grounding needs to be deepened. |
| Linux Kernel Documentation, *Kconfig Language* (Ch9 §9 reference) | not fetched | Cited by Ch9 §3 as the canonical large-scale example of explicit variability modeling. Recorded for completeness; the lesson Ch9 extracts is the discipline, not the syntax, so direct fetch is not required for this report. |
| Microsoft Learn, *What is an Azure landing zone?* (Ch9 §9 reference) | not fetched | Cited by Ch9 §3 as the enterprise-scale example of modular, repeatable platform architecture. Recorded for completeness. |
| AUTOSAR, *Feature Model Exchange Format* (Ch9 §9 reference) | not fetched | Cited by Ch9 §3 as the formal three-layer model (feature model / product line model / bound product model). Recorded for completeness; the conceptual layering is captured in §3 above without needing the exchange-format spec. |

**Blocked URLs encountered:** none. Per round conventions, Chapter 9's external reference list was not fetched.

**Open follow-ups:**

- Author a JSON Schema for the proposed `ProductLineDefinition` Codex object, mirroring the schema sketches in Ch3 Appendix A.2 (per `research/14-el-kaim-book-intent-and-spec-authorship.md` §3) and Ch8's `ArchitectureSpecification` object.
- Survey our existing skill library and identify candidate clusters for bottom-up family discovery (Ch9 §4); produce a short report cataloguing which skills could be promoted to family-level core assets.
- Decide whether F35 (Federation-as-Family Drift) is accepted into the F-mode catalog and, if so, define its detection signal and mitigation more rigorously than the sketch in §6 above.
- Decide whether `architectures/00-comparison.md` should add a family-awareness dimension as a categorization axis, or whether family scope should be treated as a separate orthogonal concern.
