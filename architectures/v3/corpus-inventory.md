---
based-on-commit: d1a60c0
based-on-date: 2026-05-23
---

# Corpus inventory (Phase 1C)

**Status:** Per-report anchor (one paragraph) + mandate-relevance tag for every report in the post-Round-12 corpus. Used by all 9 Phase-2 tracks to pick deep-read targets.

**Mandate-relevance scale:**
- `greenfield-primary` — directly informs the greenfield mandate; G-track subagents must read.
- `brownfield-primary` — directly informs the brownfield mandate; B-track subagents must read.
- `both-primary` — informs both mandates; all G/B tracks + all 3 U (unified) tracks must read.
- `both-secondary` — relevant to both but not load-bearing; read on demand.
- `tangential` — corpus-completeness only; read if subagent has spare cycles.

**How to read each entry.** Title + URL/source + one-paragraph anchor (what the report covers; what's load-bearing for v3) + mandate tag + supporting tags (e.g., `cold-start-input` for the Historian M5 list, `substrate-audit`, `governance`, `regime`, `language-as-harness`).

**Inventory scope note.** The Phase-1C brief names 38 numbered reports + 14 followups. Reports 00 (Round-1 synthesis) and 13 (Round-2 synthesis) are archived under [`archive/synthesis-v1-v2/`](../../archive/synthesis-v1-v2/) per UC6 and are explicitly excluded from inventory per the brief. The numbered-report range therefore inventories 36 entries (`01–12, 14–38`); total inventoried = 36 + 14 = 50 anchors.

---

## A. Numbered reports (01-12, 14-38)

### Report 01 — strongdm-factory
- **Subject:** StrongDM's `factory.strongdm.ai` site — principles, DTU / gene-transfusion / pyramid-summary / semport techniques; the canonical "Software Factory" brand source.
- **Anchor:** The corpus' primary anchor for the "software factory" label itself: StrongDM's three-person AI team's public manifesto + supporting techniques (DTU = Definition of Task Understanding; gene-transfusion = cross-agent knowledge propagation; pyramid summaries; semport). Names the **"no human review"** posture that report 02 (Attractor) operationalises and reports 07/12/15/30/31 critique. Footnote-1 attribution closure (2026-05-16): Luke Moynihan's lukepm.com *"The Software Factory"* (Dec 2024) drained as definitional/speculative provenance only — **not a substrate-claim anchor**. Load-bearing for v3 as the source of the brand and the no-human-review pattern both mandate tracks must address.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `substrate-claim`, `governance-target`, `methodology-source`
- **Notes:** Footnote-1 attribution closure (Luke PM) is provenance, not a substrate anchor.

### Report 02 — strongdm-attractor
- **Subject:** StrongDM's Attractor product page + ~17+ community ports (Kilroy, Forge, Fabro, Coven, Mammoth, Smasher, Tracker, dotpowers).
- **Anchor:** The canonical Attractor primitive set — Graphviz `.dot` graph, eight canonical node shapes, `model_stylesheet` cascade, `goal_gate` + `retry_target`, `status.json` per-stage contract, provider-aligned coding-agent profiles. Documents both StrongDM's reference and the ~17 community implementations that reproduce the primitive set with low drift. The Attractor *pipeline-as-orchestrator* shape is one of the two organising patterns in the corpus (the other being Compound Atelier from report 03). Load-bearing for any architecture that treats methodology as a graph/pipeline rather than a queue.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `methodology-shape`, `graph-as-spec`, `substrate-pattern`, `community-implementations`
- **Notes:** Tightly coupled to followup/02 (community ports) and report 27 (dotfile-pipelines).

### Report 03 — every-compound-engineering
- **Subject:** Every's compound-engineering guide + Klaassen's *"My AI had already fixed"* (Cora playbook).
- **Anchor:** Source of the **Compound Engineering** methodology (plan → work → review → compound) and the `docs/solutions/` knowledge-accumulation directory — the other pole to StrongDM Attractor's graph orchestration. The "queue of issues + accumulating skills + agent panel review" shape that anchored v2's Compound Atelier architecture. Load-bearing for any methodology track that treats the unit of work as an issue against an evolving knowledge base; the Compound loop is one of the two canonical methodology shapes in the corpus.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `methodology-shape`, `knowledge-accumulation`, `queue-as-unit-of-work`, `plugin-architecture`
- **Notes:** Companion to followup/11 (Compound Knowledge plugin) and followup/05 (Klaassen siblings).

### Report 04 — every-skill-libraries
- **Subject:** Every's `SKILL.md` convention; Compound Knowledge plugin's skill-library structure.
- **Anchor:** Names the SKILL.md convention as a portable scaffold-layer primitive — pre-runtime artifacts that agents discover and read on demand. The corpus' canonical anchor for **scaffold-as-distinct-from-harness** (Round-2 C11 distinction). Concrete schema constraints applied later in report 23 (Anthropic Skills primary docs: 64-char name limit, ~100 token Level-1 budget, zero network access for API-surface Skills). Load-bearing for substrate tracks defining how reusable knowledge is shipped between cycles.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `scaffold`, `skill-substrate`, `knowledge-portability`

### Report 05 — simon-willison
- **Subject:** Simon Willison's `agentic-engineering-patterns` 12-chapter guide + software-factory post + Lenny × Willison FULL podcast transcript.
- **Anchor:** Willison as the corpus' canonical practitioner-anchor: **lethal trifecta** framing (private-data × untrusted-content × exfiltration), **97%-is-a-failing-grade** doctrine, **OpenClaw / "Claws"** as a load-bearing latent-demand exemplar, Challenger-disaster prediction with the self-falsification clause, end-of-2026 prediction (50% of engineers ≥95% AI-written code), low-background-steel analogy. Defines the Agent in the canonical sense ("LLM + tools + loop"; cited verbatim by Shapiro in report 32). Load-bearing for both substrate-security tracks (trifecta) and methodology tracks (workflow patterns).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `security-primitives`, `agent-definition`, `practitioner-anchor`, `lethal-trifecta`

### Report 06 — hn-and-lenny
- **Subject:** HN thread on dark factories + Lenny Cherny/Willison podcast references; FULL Cherny transcript.
- **Anchor:** Adds the Cherny side of the Lenny pod (FULL after 2026-05-14 drain): **five-Claudes-steady-state** architecture (1/3 terminal + 1/3 desktop + 1/3 iOS surface split), **less-capable-models-cost-more-tokens** ("multi-cladding" Anthropic internal term), Anthropic financial triple ($2B revenue / $15B total / $350B valuation), Sonnet-3.5 → Opus-4.6 unattended-runtime scaling (15s → 30min). Plus HN community sentiment as macro-vibes data. The **iteration-count-is-the-bottleneck** thesis is later refined to **CI-speed-is-the-multiplier-on-iteration-count** in report 35.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `practitioner-anchor`, `runtime-scaling`, `parallel-agents`
- **Notes:** Cherny transcript ≈ followup/03; this report's HN-side coverage is mostly atmospheric.

### Report 07 — dark-factory
- **Subject:** El Kaim's *"The Dark Factory"* Medium article (anchored on `reference-only/dark-factory-article.txt`).
- **Anchor:** The "lights-out manufacturing as software-org metaphor" essay El Kaim built his EA-book methodology spine on (reports 14–17, 24). Names the Japanese robotics-plant analogy that gives the v3 brief its UC1 anchor. The metaphor is contested by report 12 (Brier's pace-layers) and report 28 (Schillace's softer team-shape framing). Load-bearing as the metaphor whose validity each v3 mandate track must position itself against (per UC1 lights-out = factory-mode requirement, but Brier and Schillace propose alternative framings).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `factory-metaphor`, `methodology-source`

### Report 08 — jaymin-book-foundations-patterns
- **Subject:** Jaymin West's *Agentic Engineering* book, Chapters 1–5 (foundations + patterns).
- **Anchor:** Jaymin's foundational patterns — prompt-engineering primitives, agent-loop shapes, the spec-driven default. Anchors Round-2 C10 (Agent = Model + Harness) and the Sean Grove "spec as the durable, version-controlled artifact" attribution (D-1 in §4 of the brief). Slightly less load-bearing than report 09 (Ch 6+) because the threshold-bar framing lives there.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `methodology-source`, `pattern-catalog`, `spec-as-artifact`

### Report 09 — jaymin-book-harnesses-practices-mental-models
- **Subject:** Jaymin West's *Agentic Engineering* Chapter 6 (harnesses) + practices + mental models; Schillace harness diagrams (cross-embed from report 28).
- **Anchor:** **Load-bearing for the §2.1 lights-out / L5 / regime tension.** Defines the Augmentation/Automation threshold matrix (K=5 ≥70%/≥90%; prompt-paraphrase robustness ≥3/5 vs 5/5; safety-incident severity), the **CodeRabbit 1.4×** / **Veracode 45%** / **METR 19%** corpus-citation triple, and names **L5 ("dark factory") as a 2026 empirical anti-pattern**. Every Phase-2 track must address either Jaymin's bars (option a/d in brief §2.1) or substitute a different bar source. Embeds the two corpus-canonical Schillace harness diagrams. Load-bearing for OQ-B6 (which empirical bars).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `regime`, `threshold-bars`, `lights-out-tension`, `harness`, `OQ-B6`
- **Notes:** This is one of the 2–3 most load-bearing reports in the corpus.

### Report 10 — overstory-substrate-audit
- **Subject:** Overstory substrate audit (governance F-modes G12/G13/G14).
- **Anchor:** Substrate-layer audit of the Overstory framework (Python design language for agent compositions). Surfaces governance failure modes G12–G14. Relevant to substrate tracks that want a baseline non-OpenHands comparison; otherwise narrow scope.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `substrate-audit`, `governance`

### Report 11 — openhands-substrate-audit
- **Subject:** OpenHands V1 substrate audit (arXiv paper + docs.all-hands.dev) — sub-ms per-event persist, 7.4ms median crash recovery, RouterLLM per-call routing.
- **Anchor:** The corpus' deepest substrate-primitive measurement source. Anchors D-7 (trajectory capture is cheap and production-tested), the RouterLLM provider-routing-abstraction example referenced in OQ-B8, and the OpenHands "433 SWE-Bench Verified replays" measurement context cited in the glossary. **Not a normative dependency** per brief §0 — cited as measurement evidence only. Load-bearing for any substrate track sizing the cost of event-sourced trajectory capture or evaluating per-call routing as a substrate primitive.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `substrate-audit`, `trajectory-capture`, `provider-routing`, `OQ-B8`

### Report 12 — adjacent-ecosystem
- **Subject:** Adjacent ecosystem audit (Cisco/LangChain, IBM, Cloud, AddyOsmani, Kiro, others); §2.5 Kiro extension.
- **Anchor:** Broad sweep across vendor + adjacent-tooling ecosystem. The §2.5 Kiro extension (added 2026-05-16) is the most actively-loaded section — Kiro's spec-driven development paradigm overlaps with brownfield refactoring concerns. Largely a breadth source; useful for substrate-comparison tracks but no single load-bearing claim.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `vendor-survey`, `ecosystem-breadth`
- **Notes:** §2.5 Kiro extension is the load-bearing slice; rest is breadth.

### Report 14 — el-kaim-book-intent-and-spec-authorship
- **Subject:** El Kaim EA book — intent + spec authorship (Chapters 1, 3, 6, 7, 8); 9-field spec discipline; ArchitectureSpecification typed object with derivedFrom rules; EvaluationSuite with `protects: RULE-ID` linkage.
- **Anchor:** The corpus' deepest treatment of **typed spec objects + intent-block discipline** at the architecture level. Defines the 9-field intent block, the ArchitectureSpecification typed object, the `protects: RULE-ID` linkage from EvaluationSuite to architectural rules. Report 25 demonstrates that El Kaim's framework maps 1:1 onto INCOSE GtWR C1–C15 (the RE/SE foundational catalog) — best read as a *domain instantiation* of GtWR rather than a novel framework. Load-bearing for greenfield cold-start (where typed-spec discipline is the bootstrapping artifact) and brownfield (where typed specs constrain refactoring intent).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `spec-as-artifact`, `intent-block`, `typed-spec`, `cold-start-related`

### Report 15 — el-kaim-book-bmad-attractor-dark-factory
- **Subject:** El Kaim EA book — BMAD + Attractor + Dark Factory linkage.
- **Anchor:** El Kaim's synthesis chapter linking three external methodologies (BMAD, Attractor, Dark Factory) into a unified design language. Useful for cross-referencing report 02 (Attractor) and report 07 (Dark Factory) against El Kaim's typed-object vocabulary. Secondary; load-bearing only if a unified-track architecture wants El Kaim's three-way mapping as a structural template.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `methodology-synthesis`, `pattern-mapping`

### Report 16 — el-kaim-book-council-and-delegation
- **Subject:** El Kaim EA book — Council pattern + delegation primitives.
- **Anchor:** Multi-agent **Council** pattern (panel of agent-reviewers with structured delegation contract). Companion to Compound Engineering's review-panel shape (report 03). Useful for tracks that propose multi-agent review/coordination as a substrate primitive.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `multi-agent`, `review-pattern`, `delegation`

### Report 17 — el-kaim-book-codex-and-skill-substrate
- **Subject:** El Kaim EA book — Codex + skill substrate (knowledge store + skill discovery).
- **Anchor:** El Kaim's "Codex" knowledge-store + skill-substrate primitives. Pairs with reports 04 and 23 on scaffold/Skill conventions. Secondary; informs scaffold-substrate tracks.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `scaffold`, `knowledge-store`, `skill-substrate`

### Report 18 — openai-codex-substrate
- **Subject:** OpenAI Codex substrate audit — `.rules` Starlark DSL, `requirements.toml` admin enforcement, OS-keyring credentials, OpenTelemetry five-event-category export, Auto-review subagent, harness-engineering posture.
- **Anchor:** The corpus' deepest commercial-substrate audit. Anchors the **`.rules` DSL as auditable-V&V-auto-rejection primitive** (one of the corpus' strongest substrate-layer governance examples); the **OTEL five-event-category export** (user prompts / tool approvals / tool results / MCP usage / network-proxy decisions) feeding an AI security-triage agent; the **Auto-review subagent** as cross-model V&V; **harness-engineering** as a discipline (Lopopolo + Chen pieces, primary-anchored 2026-05-16). Cited by reports 30/31/32/33/34 as substrate-level partial implementations of governance / cognitive-escrow / Claw-hardening patterns.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `substrate-audit`, `governance-primitive`, `rules-DSL`, `OTEL`, `auto-review`

### Report 19 — github-copilot-cloud-agent
- **Subject:** GitHub Copilot cloud-agent substrate; Copilot Spaces (team-shared context bundle).
- **Anchor:** Vendor-substrate audit of GitHub's cloud-agent surface. Notable: Copilot Spaces ≈ closest commercial AGENTS.md analog at team scope. Less substrate-novel than report 18 (Codex); useful for vendor-comparison tracks.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `substrate-audit`, `vendor`, `team-scope`

### Report 20 — replit-agent
- **Subject:** Replit Agent substrate; 4-mode framework (Lite/Economy/Power/Turbo); App Monitoring; Connectors-via-OpenInt.
- **Anchor:** Vendor-substrate audit of Replit's full-stack agent surface. Notable: App Monitoring ("built, launched, and looked after") demonstrates substrate-extends-into-observability; in-product screenshot shows tools/connectors exposed as **`skills`** inside the Agent loop (cross-references report 04 SKILL.md convention). Useful for tracks proposing post-deploy observability as a substrate primitive.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `substrate-audit`, `vendor`, `post-deploy-observability`

### Report 21 — tabnine-enterprise
- **Subject:** Tabnine enterprise substrate.
- **Anchor:** Vendor audit; enterprise context isolation, on-prem deploy, model-routing posture. Narrow-scope; useful as one data point in vendor-substrate comparison.
- **Mandate-relevance:** `tangential`
- **Supporting tags:** `substrate-audit`, `vendor`, `enterprise`

### Report 22 — academic-foundations
- **Subject:** Academic foundations across SE research; SWE-bench Verified; nutshell-bench Princeton PLI diagram; OpenAI Verified construction pipeline.
- **Anchor:** SE-research foundations + benchmark provenance. Notable: SWE-bench Verified's 93-developer / 1,699-sample / 4-level-severity / ensemble-3 annotation methodology and the 16% → 33.2% GPT-4o lift the public proxy did not surface; the **canonical "nutshell-bench" diagram** (Issue + Codebase → LM → PR → Tests). Load-bearing for tracks that ground V&V in benchmark methodology or that need a published-evaluation baseline for the architectures.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `academic`, `benchmark-methodology`, `V&V-baseline`
- **Notes:** Nutshell-bench diagram updated 2026-05-16 (Cluster F drain); previously partial.

### Report 23 — anthropic-engineering-trilogy
- **Subject:** Anthropic engineering posts S12–S15 + Claude Code sandboxing post + Agent Skills primary docs + 3 cookbook notebooks.
- **Anchor:** Anthropic's published engineering doctrine. Anchors **Claude Code sandboxing** (§8 added 2026-05-13), the **Agent Skills schema** with concrete constraints (64-char name limit, ~100-token Level-1 budget, API-surface Skills have ZERO network access by runtime fiat), and the **Anthropic Auto-Review subagent** pattern (same-model review — contrasted by report 34 with CJ Hess's `kevin/carl` cross-model review). Load-bearing for substrate tracks (sandboxing + skills schema) and methodology tracks (review patterns).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `substrate-primitive`, `sandboxing`, `skills-schema`, `auto-review`

### Report 24 — el-kaim-book-product-line-variability
- **Subject:** El Kaim EA Chapter 9 — software product lines, variability, family-based architecture (ProductLineDefinition / ProductLineSpec); Linux Kconfig + Azure Landing Zones + AUTOSAR anchors.
- **Anchor:** Family-of-products / variability framing as a meta-architectural concern. Proposes **F35 — Federation-as-Family Drift**. Useful for multi-architecture-family tracks; tangential to single-codebase scope (per brief §7) but informs the v3 multi-architecture question of when one architecture is many.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `architecture-family`, `variability`, `F35`

### Report 25 — requirements-engineering-foundations
- **Subject:** RE/SE primary methodology — EARS canonical guide (5 patterns); INCOSE TP-2020-002-06; INCOSE GtWR v4 (15 chars + 42 rules + 49 attrs); INCOSE Complexity Primer; AFIS/INCOSE-FR strategy-3 (models-as-spec).
- **Anchor:** **Cold-start required reading per brief §5.1 (Historian M5).** The RE/SE counterpart to report 14 (El Kaim). Demonstrates El Kaim ↔ GtWR C1–C15 1:1 mapping (corpus has been treating El Kaim as novel — best read as a domain instantiation of GtWR). Proposes candidate F36–F39 (vocabulary-lint debt; point-spec/region-mismatch; architecture/spec confusion; Ashby-deficient probabilistic guard). The **strategy-3 models-as-spec** framing is the corpus' canonical name for what Notion/Nystrom (report 35) implements industrially.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `cold-start-input`, `RE-foundations`, `EARS`, `GtWR`, `F36-F39`
- **Notes:** F36/F37 number collision with report 26 — lead-agent triage required per brief glossary.

### Report 26 — prompt-underspecification-academic
- **Subject:** Academic LLM+RE empirical — Norheim et al. (Cambridge / *Design Science* 2024, five-task taxonomy); Yang et al. (CMU + Google DeepMind, "What Prompts Don't Say": Pass@1 98.7%→85.0%; 41.1% guess-correctly baseline; 65.2% redundancy); Larbi et al. (U. Luxembourg + UCL, "When Prompts Go Wrong": GPT-4 73.8%→6.7% on contradictory HumanEval, RIR 89%, MCC ≤0.55).
- **Anchor:** **Cold-start required reading per brief §5.1 (Historian M5).** The corpus' academic-empirical anchor for the "spec → code gap" intuition. Yang et al.'s **same-model-different-prompt spread** is the academic instantiation of Theme-6 (followed by Schulhoff DSPy in report 29). Larbi et al.'s **silent contradictory-prompt collapse** (73.8%→6.7%) directly motivates the substrate-level need for prompt-contradiction detection. Proposes candidate F36/F37 — **number collision** with report 25 (lead-agent triage).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `cold-start-input`, `academic`, `prompt-fragility`, `F36-F37-collision`
- **Notes:** F36/F37 number collision flagged in brief §0; lead-agent call.

### Report 27 — dotfile-pipelines-as-product
- **Subject:** Harper Reed's *"The Dark Factory Is a .dot file"* essay; `dotpowers.dot` blob (~1,300 lines, 6-phase pipeline, four-model assignment via CSS); `danshapiro/kilroy` re-capture; `strongdm/attractorbench` (Apache-2.0, 17 stars, four tiers).
- **Anchor:** Reframes Attractor as **`.dot` file = durable artifact; engines = commodity**. The `.dot` → `.dip` → `.dipx` migration refines report 07's framing. AttractorBench (v13 Gemini = 0.508 anchor) is named as the conformance surface. Load-bearing for tracks that propose pipeline definitions (not runners) as the leverage point; pairs with report 02 + followup/02 (community Attractor ports).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `pipeline-as-spec`, `methodology-shape`, `attractor-evolution`, `conformance-bench`

### Report 28 — schillace-sunday-letters
- **Subject:** Super-report across all 11 Sam Schillace Sunday Letters (Sep 2025 – May 2026); Amplifier internals (Dev Foundry / session analyst / foundation expert / Crusty Old Engineer / yaml recipes / Context Query / gene transfer).
- **Anchor:** **One of the corpus' richest super-reports.** Anchors Theme-1 (attention-as-scarce-resource) with **"output per unit of human attention"** and three user-classes (Warren-Buffet / working-stiff / lottery-winner); Theme-7 (team-shape) with the **3-feels-like-30** ratio + **12-person-team / >500 projects** scale anchor + **code-review-as-firing-offense** anecdote; Theme-4 (substrate) with the agent-OS building-block list. Embeds the two canonical Schillace harness diagrams. **Attention Firewall** as the first concrete cognitive-escrow exemplar (per report 30). Proposes F40 (Last-Mile Drift) + F41 (Under-Defined-Intent Debt) — chosen high to avoid F36/F37 collision. Schillace lineages Amplifier back to Microsoft Semantic Kernel (corpus-novel).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `team-shape`, `attention-firewall`, `harness-diagrams`, `F40-F41`, `Amplifier`

### Report 29 — prompt-engineering-survey
- **Subject:** Schulhoff et al. *The Prompt Report: A Systematic Survey of Prompt Engineering Techniques* (arXiv:2406.06608v6, 76pp); 58-text-technique taxonomy across 6 families; DSPy + small modifications F1 0.548 beats 20-hour hand-crafted AutoDiCoT F1 0.53.
- **Anchor:** The corpus' academic taxonomy spine for prompt engineering. The §4.2 LLM-as-Judge catalogue anchors followup/07 (evals); the §5 Prompting Issues (injection / jailbreaking / sensitivity / sycophancy / bias / ambiguity) anchors followup/08 (security). The DSPy-beats-AutoDiCoT case study is the academic instantiation of **same-model-different-harness-different-result** (Theme-6) at the prompt layer. PRISMA pipeline numbers extracted. Cross-corpus impact table (§7) maps each family onto existing corpus reports.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `academic`, `prompt-taxonomy`, `DSPy`, `same-model-different-harness`

### Report 30 — cognitive-escrow
- **Subject:** Kahana, *Cognitive Escrow* (Stanford CodeX, 2026-03-07) — the prompt→response interval as a phenomenological "suspension state"; AILCCP Human-Centered missing-fourth-question; STIR discipline.
- **Anchor:** **Cold-start required reading per brief §5.1 (Historian M5).** Frames the prompt→response interval as a **harness-engineering design surface** (not just governance). Names the AILCCP Human-Centered principle's three current questions as all assuming the human is *present* and missing a fourth question about the *interval*. Schillace's Attention Firewall (report 28) named as the corpus' first concrete interval-as-design-site exemplar; Codex `.rules` + OTEL (report 18) as partial substrate-level implementation. Proposes F42 (Cognitive-Escrow Negligence).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `cold-start-input`, `governance`, `harness-design`, `F42`, `Stanford-CodeX`

### Report 31 — caremark-rsi-board-exposure
- **Subject:** Kahana, *The Ungovernable Machine* (Stanford CodeX, 2026-03-17) — Caremark-line duty-of-oversight + RSI three-part test + SB 53 + SEC IAC; Caremark spine (Caremark 1996 → Stone v. Ritter → Marchand → Clovis → Teamsters v. Chou → Hughes v. Hu → Boeing → McDonald's officer-Caremark extension → SolarWinds).
- **Anchor:** **Cold-start required reading per brief §5.1 (Historian M5).** Delaware-law-grounded board exposure analysis for RSI deployments. RSI three-part test (durable self-modification + compounding ability + limited human gating); corpus-load-bearing scope claim that **RSI is not limited to frontier labs** — mid-market deployments can meet the test. Three RSI failure modes (behavioural drift / self-poisoning / goal subversion) mapped to three AILCCP controls (sandboxing / immutable logging / Human Approval Gate). Proposes F43 (RSI Board-Visibility Gap). Cross-references report 02 (StrongDM "no human review" as paradigm Caremark exposure).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `cold-start-input`, `governance`, `Caremark`, `RSI`, `F43`, `Stanford-CodeX`

### Report 32 — shapiro-completion-chat-agent-claw
- **Subject:** Dan Shapiro, *Completion, Chat, Agent, Claw* (May 13 2026) — Claw = agent + memory + goals + autonomy; five hardening rules (R1–R5); claw-printer / one-Claw-per-employee Glowforge org pattern.
- **Anchor:** Compositional successor sub-taxonomy to the Five Levels (followup/01) on an orthogonal axis (system composition vs operator position). The **five hardening rules** (R1 read-anything-but-only-draft; R2 thumbprint every artifact; R3 *"do not give it production scissors"*; R4 isolated env; R5 disconnect-by-default) are empirical-practitioner restatement of Willison's Lethal Trifecta closure at the integration/API boundary. **Claw-printer / one-Claw-per-employee** is the Glowforge supply-side peer of Notion/Boxy (report 35) + Sendbird/quests (report 36) — three-source corpus convergence on per-employee as org-design primitive. Proposes F44 (Lethal-Trifecta Production-Scissors Default). Jesse Vincent's assistant's *"every night research things that might help it do its job"* is the corpus' first concrete **dreaming** exemplar.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `Claw`, `hardening-rules`, `per-employee-primitive`, `F44`, `dreaming`

### Report 33 — language-choice-as-harness
- **Subject:** Allan MacGregor *"When AI Agents Write Your Code, Does Language Choice Matter?"* (Feb 17 2026, free portion drained; paid tail flagged); Jose Valim Elixir benchmark (Tencent 20 languages, Elixir 97.5%, Opus 4 80.3% Elixir vs 74.9% C#); de Montalembert *"the more flexible and forgiving the target language, the more dangerous the AI partner becomes."*
- **Anchor:** Reframes programming-language choice as a **first-class harness-engineering decision** on the same lever board as `.rules`, sandbox shape, judge prompts, AGENTS.md. Three pillars: compiler-as-AI-code-reviewer; LLM-architecture-fit (stateless / pure-function vs mutable-OOP); de Montalembert hazard. Proposes F45 (Language-as-Harness Mismatch). StrongDM/Attractor ecosystem's empirical posture (Smasher Rust / Tracker+Mammoth Go / Coven Rust+Go / Kilroy Go) suggests implicit endorsement; canonical pages do not theorise it. **Empirically extended to the policy layer by report 37** (Stanford Computational Antitrust).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `language-as-harness`, `F45`, `harness-lever`, `pragmatic-cto`
- **Notes:** Paid-tail still flagged for fetch-blocked-urls; report status 🟡.

### Report 34 — lenny-howiai-personal-harnesses
- **Subject:** CJ Hess (Tenex SWE) — Flowy (JSON→flowchart, ~100% prompted via Ralph loop; `~/.claude/skills/flowy-flowchart/SKILL.md`); `kevin/carl` model-vs-model QC loop; Ralph loop; diff-driven retrospectives.
- **Anchor:** Corpus' canonical anchor for **harness-quality-dominates-model-quality at single-engineer scope** (CJ: *"I'd honestly argue GPT 5.2 is a smarter model"* despite preferring Claude Code daily — model concession is load-bearing). `kevin/carl` cross-model QC (kevin = Claude Code with bypass-permissions; carl = Codex / GPT-5.2 as *"curmudgeonly staff engineer"*) contrasts with Anthropic's same-model Auto-Review (report 23). Proposes F46 (Single-Model Review Blindspot). Adds the **personal-skill** layer below organizational skills.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `personal-harness`, `cross-model-review`, `Ralph-loop`, `F46`, `diff-driven-retro`

### Report 35 — lenny-howiai-spec-driven-and-team-ops
- **Subject:** Ryan Nystrom (Notion engineering manager, post-Campsite) — Project Afterburner (CI to 25%); Boxy VM-based background agent dispatched from Notion comments; **Markdown-spec-in-repo as AFIS strategy-3 industrial anchor**; "yap your spec" Whisper→Codex pipeline; *"you're wrong; defend your argument with evidence"* sycophancy-breaking prompt; line-managers-who-still-code; Stripe 1,300-agent-PRs/week third confirmation.
- **Anchor:** First industrial primary anchor for **AFIS strategy-3 at non-aerospace scale** (Markdown specs in `agent specs/` subfolder; spec-version-history-as-changelog). Boxy is Notion's per-engineer Claw fleet (third independent instance of one-Claw-per-employee, peer to Shapiro/Glowforge in report 32 and Sendbird in report 36). The standup pre-read agent is the corpus' second concrete Attention Firewall exemplar after Schillace. **CI-as-substrate-bottleneck thesis** refines Cherny's "iteration count is the bottleneck" to *CI speed multiplies iteration count*. Manager-as-operator first-person primary anchor.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `AFIS-strategy-3`, `Markdown-spec`, `per-employee-primitive`, `CI-as-bottleneck`, `attention-firewall`, `Boxy`

### Report 36 — sendbird-quests-token-tiers
- **Subject:** John Kim (Sendbird CEO) — Automators quest-marketplace; six-tier per-person token leaderboard (Beginner / Intermediate / Expert / Architect / Catalyst / AI God); InfoSec-vetted secure templates; cross-functional AI task force; hiring rewrite (curiosity / agency / energy).
- **Anchor:** Corpus' first primary source for a **gamified org-wide AI-adoption playbook** built on game-design primitives. Four primitives: (1) Automators marketplace (risk-level / weeks-saved / beneficiary quest tags; XP redeemable for gift cards + Wednesday-standup slot); (2) per-person daily-token tiers (curve-smoothness as measurement primitive — smooth = agents work 24/7); (3) InfoSec-vetted secure templates (substrate-carries-the-guarantee model); (4) AI Engineer for Internal Operations reporting directly to CEO. Proposes F47 (Visible-Metric Drift / Goodhart-on-Tokens). Completes three-source corpus convergence on per-employee primitive. §5.4 stacked-pattern table is strongest Cluster-N synthesis artifact.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `org-design`, `per-employee-primitive`, `token-tiers`, `F47`, `Goodhart`

### Report 37 — academic-llm-agent-collusion
- **Subject:** Neves & Bussmann, *Smart Agent-Based Modelling with LLMs* (Stanford Computational Antitrust Vol. 6, 2026; CADE / Cerebro Project, Brasil) — Bertrand-duopoly LLM agents reach tacit collusion ($7.30–$8.30 median vs $6.00 Bertrand-Nash; up to 100% supra-competitive); Portuguese-prompted agents systematically more collusive than English; *"mimicking concerns about collusion"* sub-effect.
- **Anchor:** **First academic-empirical anchor for Theme-2 alignment-drift / collusion in a market setting at LLM scale.** Tacit collusion without instruction; **language-effect on policy** extends report 33 (language-as-harness) from code-generation layer to decision/policy layer (corpus-novel); discussion-as-amplification (agents discuss collusion, recognise it as failure mode, then implement softer/deniable version) is multi-agent instantiation of Schulhoff §5 sycophancy paradox. Proposes F48 (Tacit-Collusion-via-Shared-Context) + F49 (Discussion-as-Amplification). Second Stanford Law venue in the corpus (Computational Antitrust paired with CodeX). Relevant to multi-agent-substrate tracks and any unified architecture using inter-agent communication.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `academic`, `multi-agent`, `collusion`, `F48-F49`, `Stanford-Computational-Antitrust`, `language-as-harness-extension`

### Report 38 — gas-systems-substrate
- **Subject:** Gas City SDK (`github.com/gastownhall/gascity`, v1.0.0+) + Gas Town workspace OS — mapping onto Dark Factory + Compound Engineering as candidate execution substrate. Nine Concepts (5 primitives + 4 derived); Beads' `discovered-from` edge.
- **Anchor:** Synthesis report (with deep-dive companions in followup/13 and followup/14). **Substrate-vs-application split** between Gas City SDK and Gastown role pack is the central architectural fact. Three design mantras: Zero Framework Cognition / Bitter Lesson / Primitive Test. Three identified gaps vs methodology requirements: no first-class LLM-as-judge primitive; no DOT pipeline parser; no context-fidelity slider. **Beads' `discovered-from` edge** is the corpus' strongest candidate "compounding-of-knowledge" primitive at the engine level — strictly more expressive than Compound Atelier's flat-file `docs/solutions/`. Substrate-maturity warning: post-v1.0.0 but 1–2 breaking schema changes per quarter expected through 2026.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `substrate-candidate`, `beads`, `discovered-from-edge`, `pack-architecture`
- **Notes:** Supersedes followup/04 on internal-package structure.

---

## B. Followups (01-14)

### Followup 01 — shapiro-five-levels
- **Subject:** Shapiro's canonical *"The five levels — from spicy autocomplete to the software factory"* post; L0–L5 maturity model; Shapiro self-positions at L4 ("I'm here").
- **Anchor:** **Load-bearing for §2.1 lights-out / L5 / regime tension.** The canonical primary source for L0–L5 (glossary §0). Shapiro's L4 self-position is the explicit refusal of L5 as personal practice — corpus' counter-anchor to UC1 lights-out (which the brief interprets as not-necessarily-L5 per Skeptic #13). 8 El Kaim-vs-Shapiro discrepancies documented. Successor framing added 2026-05-16 cross-references report 32 (Claw ≈ L4/L5; "Claw = the substrate L5 runs on").
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `regime`, `Five-Levels`, `lights-out-tension`, `OQ-B6`

### Followup 02 — attractor-implementations
- **Subject:** Community Attractor ports (~17 named, Go/Rust/Python/TypeScript); Kilroy, Forge, Fabro (succeeds archived brynary/attractor), 2389 Research family (Coven, Mammoth, Smasher, Tracker, dotpowers).
- **Anchor:** Documents the ~17 community implementations of the StrongDM Attractor primitive set with low drift. Notable: brynary/attractor archived 2026-04-28 → succeeded by Fabro (Rust, Qlty.sh). 2389 Research family adds five named ports + dotpowers `.dot` payload. Companion to report 02 (Attractor canon) and report 27 (dotfile-pipelines).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `community-implementations`, `attractor-ecosystem`, `language-diversity`

### Followup 03 — cherny-interview
- **Subject:** Boris Cherny Lenny interview, FULL primary-source-anchored transcript.
- **Anchor:** Cherny's 4-layer AI-product principles ("build for the model six months from now"), 3-layer safety framework (mech-interp / evals / wild), Cowork 10-day build anecdote, race-to-the-top open-source-sandbox principle. Resolves five-Claudes-parallel architecture (steady-state with 1/3 terminal + 1/3 desktop + 1/3 iOS surface split, *"multi-cladding"* Anthropic-internal term). `/loops`, `/batch`, "thousands of overnight agents" remain unresolved single-secondary-source claims.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `practitioner-anchor`, `parallel-agents`, `safety-framework`, `multi-cladding`

### Followup 04 — gastown-beads
- **Subject:** Gas Town's DOT-graph orchestration (pre-Gas-City-extraction view of Beads).
- **Anchor:** Early architectural read of Gas Town's bead store + DOT orchestration. **Superseded by report 38 + followup/14** on substrate-application split (Gas City extracted from Gas Town); remains consistent on the Attractor-comparison axis. Read followup/14 first; this report serves as historical context.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `beads`, `superseded-by-38`

### Followup 05 — klaassen-siblings
- **Subject:** Klaassen's three every.to *"Stop Coding..."* sibling articles; Article 1 fidelity-three tiers; Article 2 eight planning strategies (Strategies 1-2 visible, 3-8 paywalled); Parrott Opus-4.5 article.
- **Anchor:** Augments report 03 with three sibling pieces. Fidelity-three framework (Fidelity-1/2/3 with three-prototypes-of-ascending-difficulty worked example) primary-sourced. Four-clause plan-prompt template (survey internal / survey local tooling / survey external best-practices / demand N approaches with tradeoffs). `/modify-plugin` command described not specified. Eight planning strategies — six remain paywalled. Manager-as-operator anchor (peer to Nystrom in report 35).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `planning-strategies`, `manager-as-operator`, `Compound-Engineering`

### Followup 06 — competitor-landscape
- **Subject:** Five named competitors — Devin / Factory / 8090 / Superconductor / Superpowers; Factory's Droid Computers primitive; Superconductor's multiplayer "take the wheel" shared-agent-session; 8090's *"Software Factory"* (name-disambiguates from Notion-Boxy *"software factory"* internal framing).
- **Anchor:** Vendor competitive landscape. Devin pricing refuted; Superconductor §4 fully re-anchored to .com. Multiplayer "take the wheel" is Superconductor's unique differentiator. Useful as market-context anchor for substrate-comparison tracks.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `vendor`, `competitive-landscape`, `name-disambiguation`

### Followup 07 — evals-deepdive
- **Subject:** Anthropic multi-agent research system + Husain/Shankar Evals FAQ + Hamel tetralogy + Simon Willison FAQ; verbatim quotes; orchestrator-worker architecture; Critique Shadowing / Capability Funnel / fifteen-five / synthetic data.
- **Anchor:** Corpus' deepest evals-discipline anchor. **60–80% of development time on error analysis** (verbatim Husain/Shankar). Anthropic's single-judge finding (*"a single LLM call with a single prompt outputting 0.0-1.0 + pass-fail was the most consistent"*). 20-trace saturation heuristic. Multi-agent uses ~15× more tokens than chat (corrected — prior draft said 4×). Filesystem-as-shared-artifact pattern to avoid "game of telephone." "Think like your agents" prompt-engineering principle. Binary > Likert (annotators default to middle values). Load-bearing for substrate tracks defining V&V primitives.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `evals`, `LLM-as-judge`, `multi-agent`, `error-analysis`

### Followup 08 — security-primitives
- **Subject:** Lethal trifecta (Willison) + Dual LLM (Willison 2023) + CaMeL (Google DeepMind + ETH Zürich, arXiv 2503.18813) + Claude Code sandboxing / Safe YOLO.
- **Anchor:** Corpus' deepest security-substrate anchor. CaMeL paper-body recovered via arXiv `/e-print/` LaTeX route (2026-05-13); §3 expanded from 7 to ~15 subsections (PI-SEC formal security game, six-component architecture, NORMAL/STRICT interpreter modes, side-channel attacks, AgentDojo **77% provable security vs 84% undefended** — ~7-point utility tax). Cluster-L cross-reference to report 29 §5 (Prompting Issues). Load-bearing for substrate-security tracks; pairs with report 18 (Codex `.rules` DSL as substrate-layer mitigation).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `security-primitives`, `lethal-trifecta`, `CaMeL`, `sandboxing`

### Followup 09 — methodology-ancestors
- **Subject:** Three pre-LLM methodology ancestors — Cem Kaner *Scenario Testing* (2003), Richard Rumelt *Good Strategy/Bad Strategy* (2011), and (third ancestor — Marick / Cynefin / similar; partial-source provenance).
- **Anchor:** Genealogy report grounding scenario-testing, strategy-kernel-as-spec, and complexity-classification framings the corpus' architectures inherit. Kaner's five characteristics (story / motivating / credible / complex / easy to evaluate) + sixth dimension (power) underlie the corpus' "scenarios as holdout set" default (D-2). Rumelt's kernel (diagnosis / guiding policy / coherent action) underlies the spec-as-strategic-direction framings. Partial-source provenance (WebFetch 403s; reconstructed from snippets) — structural shape firm, passage-level fidelity could be sharper.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `methodology-ancestors`, `scenario-testing`, `Rumelt-kernel`, `partial-source`

### Followup 10 — governance
- **Subject:** Stanford CodeX (Kahana) + BCG Platinion + Pragmatic CTO (MacGregor) governance/liability/audit-trail literature; AILCCP framework (37 principles / 48 controls / 43 standards / 10 phases / 18 risks / 500+ cross-references / per-phase metrics); Three Gaps (liability / disclosure / contractual); BCG Five Pillars; Replit prod-DB wipe + Moltbook first Mass AI Breach.
- **Anchor:** **Cold-start required reading per brief §5.1 (Historian M5).** Deepest governance-literature anchor. The AILCCP foundational article (§A), 48-controls catalogue (§B), and structural overview (§C) added 2026-05-16. Concrete failure cases: Replit production-database wipe (July 2025; 1,200 executives' data destroyed during code freeze); Moltbook first Mass AI Breach (Jan 2026; 1.5M API keys exposed in 3 days from missing RLS config). CodeRabbit / Veracode / FormAI numeric quality data. **BCG's "auditability by design"** claim partially refutes prior framing that current architectures need explicit governance retrofits. Load-bearing for any architecture targeting regulated regimes.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `cold-start-input`, `governance`, `liability`, `AILCCP`, `BCG-Five-Pillars`, `regulatory`

### Followup 11 — compound-knowledge
- **Subject:** Every's Compound Knowledge plugin (CK) v1.0.0; four-way classification (insight / playbook / correction / pattern); `kw:confidence` first-class skill; no-silent-overwrites rule.
- **Anchor:** Companion to report 03 (Compound Engineering). CK is the knowledge-work twin of CE — same loop, same Git-tracked Markdown substrate. **Two CK additions to CE: typed four-way classification + first-class confidence-check primitive.** CK folds staleness check inline into every `kw:compound` invocation (vs CE's separate `ce-compound-refresh` cadence). Sharpens v2 Architecture-2's knowledge-document shape (§3.2), Curator role (§3.4), and knowledge architecture (§7).
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `knowledge-accumulation`, `Compound-Knowledge`, `typed-learnings`, `kw-confidence`

### Followup 12 — brier-pace-layers
- **Subject:** Noah Brier (Alephic, ex-Percolate) — *"The Culture of AI Engineering"* (every.to Thesis, 2026-05-08); five-layer pace-layer stack (Code / Plans / Specs / Architecture / Standards); Brand-pace-layers ancestor; *"software company, not software factory"* counter-metaphor; proposes F34 (cross-layer drift).
- **Anchor:** **The corpus' single explicit public counter-metaphor to the software-factory framing.** Brier is the only voice in the corpus who has used the StrongDM framework in production and publicly disagrees with its central metaphor. Five-layer stack with **patterns sift downward** (project doc → Skill → enforced standard) operationalises Brand's pace-layers at AI-engineering scale. Names StrongDM, Shapiro, Factory.ai as targets. ARCHITECTURE.md per repo (Naur "real program is the mental model"). Load-bearing for tracks positioning against UC1 factory-metaphor — at minimum, must be named and engaged.
- **Mandate-relevance:** `both-primary`
- **Supporting tags:** `counter-metaphor`, `pace-layers`, `F34`, `ARCHITECTURE.md`

### Followup 13 — gas-city-deep-dive
- **Subject:** ~10.2k-word architecture reference for Gas City SDK (`github.com/gastownhall/gascity`, v1.0.0+); Nine Concepts (5 primitives + 4 derived); ~55 internal packages; ~45-command `gc` CLI; PackV2 + progressive activation Levels 0–8; runtime.Provider interface; formula/molecule/order/convergence/sling primitives; K8s-style reconciler with Erlang/OTP mapping; HTTP+SSE embedding story (no Go library yet); five bundled packs (core/bd/dolt/maintenance/gastown).
- **Anchor:** Engine-level architectural reference for the Gas City substrate candidate. Authored by a subagent against read-only repo walk; every claim cites a file path. Pairs with report 38 (synthesis) + followup/14 (Gas Town application). Load-bearing for any substrate-track architecture that wants to seriously evaluate Gas City as a built substrate (rather than designing one from scratch). ~20 known limitations + open architectural questions enumerated.
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `substrate-candidate`, `gas-city`, `nine-concepts`, `pack-architecture`
- **Notes:** Read report 38 first for synthesis; this is the engine-level depth source.

### Followup 14 — gas-town-deep-dive
- **Subject:** ~9.3k-word architecture reference for Gas Town workspace OS (`github.com/gastownhall/gastown`); 9-role taxonomy (Mayor / Deacon / Boot / Dogs / Witness / Refinery / Polecat / Crew / Overseer); state model (Town / Rig / Hook / Convoy / Molecule / Wisp); six-stage bead lifecycle; ~250 cobra commands; 10 agent runtimes; Wasteland federation (Phase-1 wild-west mode); 13 plugins; OTEL event/identity model; `gt-proxy-server` mTLS sandboxing (containerized polecat isolation, **NOT LLM routing**).
- **Anchor:** Application-level reference for the canonical Gas-City-built application. Notable corpus-impact: refutes prior comparison report's assumption that `gt-proxy-server` was LLM-routing (it is per-agent mTLS containerized sandbox isolation). *"Transport changes, ledger endures"* design quote. Bors-style Refinery merge queue with bisecting. CHANGELOG architectural milestones (v0.8.0 OTEL+Scheduler+Wasteland; v0.9.0 persistent polecats + Bors; v1.0.0 Windows + PR merge strategies). Supersedes followup/04 on internal-package structure. **~10 open questions explicitly marked as planned/not-yet-implemented.**
- **Mandate-relevance:** `both-secondary`
- **Supporting tags:** `substrate-application`, `gas-town`, `role-taxonomy`, `sandbox-isolation`

---

## C. Cold-start required-reading subset (Historian M5)

Per [`00-brief-v3` §5.1](00-brief-v3.md), these reports must be read by every greenfield cold-start track and every both-mandates track that addresses greenfield:

- Report [`25`](../../research/25-requirements-engineering-foundations.md) — RE/SE foundational catalog (EARS + INCOSE GtWR + Complexity Primer + AFIS strategy-3); the prior-art base camp for any greenfield bootstrap, and the source demonstrating El Kaim ↔ GtWR 1:1 mapping.
- Report [`26`](../../research/26-prompt-underspecification-academic.md) — Academic empirical anchor for the spec→code gap (Norheim / Yang / Larbi); load-bearing for the bootstrap-against-silent-failure question (Pass@1 98.7%→85.0% as specs scale; 73.8%→6.7% on contradictory prompts).
- Report [`30`](../../research/30-cognitive-escrow.md) — Stanford CodeX framing of the prompt→response interval as harness-engineering design surface; names the gap (AILCCP missing fourth question) the cold-start architecture must address structurally.
- Report [`31`](../../research/31-caremark-rsi-board-exposure.md) — Delaware Caremark-line + RSI three-part test; the regulator-facing accountability surface a greenfield cold-start architecture has to be defensible against from day 0.
- Followup [`10`](../../research/followup/10-governance.md) — AILCCP framework (37 principles / 48 controls / 43 standards / 10 phases / 18 risks); BCG Five Pillars + Three Gaps; concrete-failure cases (Replit DB wipe, Moltbook breach); the operational ground-truth for governance-by-design.

---

## D. Disputed tags (lead-agent attention)

Items the 1C-bias miscategorization auditor (per the plan) should pressure-test:

1. **Report 10 (overstory-substrate-audit) → `both-secondary`.** Could be argued `both-primary` if a substrate track wants a baseline non-OpenHands comparison; argued tangential by some readings. Pressure-test: is the substrate-audit content load-bearing for any specific Phase-2 substrate question, or is report 11 (OpenHands) sufficient on its own?
2. **Report 21 (tabnine-enterprise) → `tangential`.** Could be argued `both-secondary` if enterprise-context-isolation or on-prem-deploy posture becomes a load-bearing brownfield concern. Pressure-test: does any brownfield track in Phase 2 need an enterprise-substrate baseline?
3. **Report 24 (el-kaim-product-line-variability) → `both-secondary`.** Could be argued `both-primary` if a both-mandates track decides multi-architecture-family framing is load-bearing (per OQ-B7 alternative axes). The brief excludes multi-codebase coordination from v3 scope (§7), which weakens the case.
4. **Report 37 (academic-llm-agent-collusion) → `both-primary`.** Could be argued `both-secondary` — the empirical setting is market pricing, not software production. Kept at `both-primary` because (a) it empirically extends report 33's language-as-harness to the decision layer (corpus-novel); (b) any unified architecture using inter-agent communication needs the F48/F49 failure modes named; (c) Theme-2 alignment-drift in market settings is the first academic-empirical anchor in the corpus.
5. **Followup 09 (methodology-ancestors) → `both-secondary`.** Could be argued `both-primary` because Kaner's scenario-testing five characteristics + sixth power dimension underlie D-2 (scenarios as holdout set, flagged fragile for brownfield). Demoted because partial-source provenance (WebFetch 403s) means the passage-level fidelity is shaky; the structural framing is sufficient as secondary read.
6. **Followup 12 (brier-pace-layers) → `both-primary`.** Could be argued `both-secondary` since it's a single-author counter-metaphor essay. Kept at `both-primary` because (a) it is the *only* explicit public counter-metaphor to UC1's factory framing in the corpus; (b) every track positioning relative to UC1 must engage Brier at minimum; (c) the pattern-sift-downward operational pattern is corpus-novel.
7. **Reports 04 / 17 / 23 (scaffold-substrate layer).** Three reports touching SKILL.md / scaffold / skill-substrate. All tagged `both-primary` (report 23) or `both-secondary` (reports 04, 17). Some risk of double-counting; pressure-test: does the substrate track need all three deep-read, or is report 23's primary-doc anchoring sufficient and 04/17 confirmable as secondary?

## E. Coverage notes

- **Total reports inventoried: 36 numbered (01–12, 14–38) + 14 followups = 50 anchors.** Brief language ("38 + 14 = 52") includes reports 00 and 13 in the range but excludes them explicitly as archived syntheses; actual count is 50.
- **Reports with brief anchors (short/partial/mostly-attribution):**
  - Report 01 footnote-1 attribution (Luke PM): provenance closure, not substrate claim.
  - Report 21 (tabnine-enterprise): narrow-scope vendor audit.
  - Report 22 status flagged: nutshell-bench updates added 2026-05-16; underlying academic content is broad but the corpus-load-bearing slice is narrow.
  - Followup 04 (gastown-beads): superseded by followup/14 + report 38; retained as historical context.
  - Followup 09 (methodology-ancestors): partial-source provenance; structural shape firm, passages soft.
- **Reports where more reading time would have been valuable:**
  - Report 33 (language-choice-as-harness) status 🟡 — paid tail of MacGregor's post still blocked; F45 framing rests on free-portion drain.
  - Report 24 (el-kaim-product-line-variability) — variability + family framing has real overlap with the multi-codebase question the brief explicitly defers; deserves a deep-read by any track entertaining alternative axes per OQ-B7.
  - Followup 09 — full primary fidelity would sharpen the scenario-as-unit-of-acceptance + Rumelt-kernel-as-strategic-spec foundations the corpus inherits.
- **Structural patterns observed:**
  - Round 9–10 reports (25, 26, 30, 31, followup 10) skew `both-primary` because they introduced the RE/SE foundations + Stanford CodeX governance threads simultaneously — these are the cold-start required-reading subset by user designation (Historian M5).
  - Round-N cluster (34, 35, 36) converges three independent sources on per-employee as org-design primitive within ~90 days (Glowforge / Notion / Sendbird) — a corpus-novel synthesis-layer pattern.
  - Vendor-substrate reports (19, 20, 21) cluster at `both-secondary` or `tangential` — useful for substrate-comparison breadth but rarely load-bearing on a single claim.
  - The El Kaim books (14–17, 24) skew `both-secondary` except for report 14 (spec/intent), which is `both-primary` because of its 1:1 mapping to GtWR.
  - The numbering-collision burden is real: F36/F37 collision between reports 25 and 26 (lead-agent triage per brief glossary); subsequent reports (28, 30, 31, 32, 33, 36, 37) deliberately chose high-end F-numbers to avoid further collision — but no triage of the F36/F37 numbers themselves has been performed in the corpus.

*End of corpus-inventory.md.*
