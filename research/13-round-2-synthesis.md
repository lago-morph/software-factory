# 13 — Round-2 Synthesis

**Round:** 2 — fanout `20260511-054258`, sub-26 (synthesis position 13)
**Date:** 2026-05-11
**Inputs:** `research/08-jaymin-book-foundations-patterns.md`, `research/09-jaymin-book-harnesses-practices-mental-models.md`, `research/09-jaymin-harnesses-partial.md`, `research/10-overstory-substrate-audit.md`, `research/11-openhands-substrate-audit.md`, `research/12-adjacent-ecosystem.md`.
**Diff targets:** `research/00-synthesis.md` §2 and §3; `architectures/00-comparison.md` §2.4 (F1–F20), §4.1 (shared infrastructure), §7 (recommended path).
**Output protocol:** proposal only. This document does **not** edit `architectures/00-comparison.md`; the orchestrator + future user pass is responsible for the §7 replacement.

---

## 1. What changed in the consensus

Section-by-section diff against `research/00-synthesis.md` §2 ("Where the sources agree"). Round-2 evidence either **strengthens** an existing consensus item, **introduces** a new one, or **falsifies** part of an old one.

### 1.1 New consensus items promoted in Round 2

**C10 — `Agent = Model + Harness` is the canonical 2026 vocabulary.** Five independent practitioners (Fowler, Mollick, Raschka, Schmid, Hashimoto) converged on the formula within a 90-day window in spring 2026 (report 08 §6, report 09 §1, partial 09 §2). LangChain, Google Cloud, Addy Osmani, and IBM use the term in their own definitions (report 12 §2.1–§2.4). OpenHands V1's four design principles (report 11 §4a) and Overstory's `AgentRuntime` interface (report 10 §3) are concrete implementations of the harness concept. This consensus did not exist in `research/00-synthesis.md` v2 — that document's §2 lists nine consensus items but none of them name the harness vocabulary. Round 2 makes the vocabulary load-bearing.

**C11 — Scaffold and harness are different layers and must be named separately.** Scaffold = pre-runtime artifacts (CLAUDE.md, AGENTS.md, system prompts, project conventions). Harness = runtime control system (dispatch, context management, safety enforcement, loop control). Report 08 §1, partial 09 §4, report 09 §1, report 11 §5 (Skills = scaffold; SecurityAnalyzer + ConfirmationPolicy + workspace = harness), and report 10 §5 (mail bus + watchdog tiers + merge resolver = harness; `agents/*.md` + per-task overlay = scaffold) all use the distinction. The original synthesis §4 row "AGENTS.md / discoverability" conflated the two layers; Round 2 demands separation.

**C12 — Specs-as-source-code is the doctrinal frame Jaymin attributes to Sean Grove.** Report 09 §3 quotes the load-bearing analogy: "throwing away prompts after generating code is like checking in compiled binaries while discarding source." Kiro's EARS-notation requirements (report 12 §2.5), Cisco/LangChain's spec-driven Worker+Leader architecture (report 12 §2.2), and the BMAD-METHOD's Living Artifacts (report 09 §3) all instantiate the same doctrine. Round-1 already had this implicit in `spec-driven-ai-dev.md`; Round 2 promotes it to a citable industry-canonical position with attribution.

**C13 — Holdout discipline (acceptance criteria withheld from builders) is named industry-wide.** Report 09 §2a labels StrongDM's scenarios-as-holdout pattern with a single industry-canonical name ("holdout") that previously appeared under three different names across our four architectures (Refinery's "out-of-tree scenarios"; Foundry's "acceptance V&V"; Tournament's "predator agent"). OpenHands' headless `always-approve` mode (report 11 §3) forces the same discipline — trust must be enforced *before* invocation, validated *after*; it cannot be enforced *during*. The Round-1 synthesis §2.2 had this consensus but did not name it.

**C14 — Tiered watchdog supervision (Daemon → Triage → Patrol) is a substrate primitive, not a methodology choice.** Report 08 §3.11 + §7.11, report 09 §4, report 10 §6 (`src/watchdog/{daemon,triage,health}.ts`) all describe the same three-layer pattern: Tier 0/1 mechanical (process alive? heartbeat? resource limits?) at seconds cadence; Tier 1/2 AI triage (is the agent stalled or thinking? reclassify or restart) at seconds-to-minutes cadence; Tier 2/3 strategic (drift across hours, escalate to human) at minutes-to-hours cadence. Both Gas Town (Go) and Overstory (TypeScript) implement this independently. Round-1's "manager loop" primitive collapsed all three tiers into one. Round 2 falsifies that collapse.

**C15 — Cost ceilings are not optional in CI.** Overstory's STEELMAN risk 12 explicitly names the gap: "swarms require active monitoring and circuit breakers" which Overstory does not provide (report 10 §9). The 20-agents × 15-tasks × 6-hour example burns ≈$60; same work sequential ≈$9; the "2-hour speedup cost $51 in coordination" (report 10 §9). OpenHands V1 does not provide cost ceilings either (report 11). Report 09 §5.3 makes this explicit: per-agent + per-task + daily-swarm hard budgets are mandatory in CI because subscription-cost approaches (Claude Code Pro) don't apply to API-backed pipelines (report 09 §7 A3). Round-1's §2.9 had cost as a first-class concern but framed it as observability ("surfacing per-loop cost telemetry"); Round 2 promotes it to an enforcement primitive.

**C16 — Trajectory capture is a substrate primitive and is now empirically cheap.** OpenHands V1's event-sourced state model measures **sub-millisecond per-event persist latency and 7.4ms median crash recovery** over 433 SWE-Bench Verified replays (report 11 §4d). Overstory's NDJSON event tailer is operationally similar (report 10 §8, "trajectory capture: provides"). This was a Round-1 nice-to-have ("CXDB would be the gold standard; cheaper alternatives exist," `architectures/00-comparison.md` §7.4); Round 2 confirms the cheap alternative exists and is production-tested.

### 1.2 Strengthened consensus items (already in §2 of `research/00-synthesis.md`)

- **§2.1 (specs become primary artifact)** — strengthened by Jaymin Ch 9 §3 (Sean Grove, report 09 §3), BMAD's Living Artifacts (report 09 §3), Kiro's EARS notation (report 12 §2.5), and Cisco/LangChain's Leader+Worker spec-driven control plane (report 12 §2.2).
- **§2.4 (LLM running tools in a loop)** — Jaymin's Ch 6 explicitly endorses the framing (partial 09 §1, the `Agent = Model + Harness` formula is exactly this) but reframes "tools in a loop" as the *harness's* job, not the agent's. The agent is the *outcome*, not the architecture.
- **§2.5 (knowledge accumulates between cycles)** — Jaymin's PRESERVE/APPEND/DATE/REMOVE protocol (report 09 §5.4) is a load-bearing operationalization that Round 1 lacked. The "learning-separation" pattern (read-only during execution; single-writer in a post-cycle improve phase) eliminates a class of race conditions Round 1's flat-files-with-curation did not address.
- **§2.6 (cognitive ceiling is real)** — Jaymin's "design starvation" failure mode (F25 below) gives the ceiling a name from the operator side: a swarm of N agents idle because the human can't decompose work fast enough.
- **§2.8 (tiered ceremony beats one-size-fits-all)** — BMAD's "Scale-Adaptive Artifact Depth" (Quick Flow 3 steps vs. Full Planning Path 6 phases, report 09 §3) is direct support; Cisco/LangChain's pilot found "PR review process itself became the bottleneck introduced by human-in-the-loop" (report 12 §2.2), which is the failure mode tiered ceremony exists to avoid.

### 1.3 Falsified or rewritten consensus items

- **§2.3 (validation harnesses are the real engineering)** — the Round-1 wording ("Digital Twin Universe is the most-praised innovation in the corpus") survives but should be reframed. Reports 09 §4 (Operating Agent Swarms), 10 §2 (Overstory's coordinator+mail+merge stack), and 11 (OpenHands' workspace abstraction) demonstrate that *substrate* engineering — the harness layer below the validation harness — is itself a load-bearing investment. The DTU is the *highest* level of validation harness; the substrate that runs it is also engineering, and Round 1 understated this. **Falsified element:** "orchestration is the easy part" (the synthesis phrasing) is wrong in light of Overstory's 36-subcommand CLI, 4-tier merge resolver, and three-tier watchdog. Orchestration is also hard. Validation harnesses are *one of two* hard problems, not the singular one.
- **§2.7 (human leverage moves upstream and downstream)** — Cisco/LangChain's pilot data (93% reduction in time-to-root-cause; 65% reduction in execution time; PR review as the new bottleneck — report 12 §2.2) is the first empirical measurement of the repositioning. The Round-1 wording is consistent; Round 2 makes it citable rather than aspirational.

---

## 2. What changed in the disagreements

Section-by-section diff against `research/00-synthesis.md` §3. The three tensions the brief flags — humans-review-or-not, persona-vs-graph, prose-vs-structured-spec — each got new evidence.

### 2.1 §3.1 — Human review (required / eliminated / tiered)

Round 2 makes the disagreement *sharper*, not softer.

- **OpenHands' headless mode is `always-approve` and cannot be changed in CI** (report 11 §3, verbatim doc quote). Trust must be enforced before invocation (capability scoping, sandbox) and observed afterward (trajectory + diagnostic agent), **not interactively**. This is the strongest implementation-level statement of the StrongDM stance in our corpus. It does not say "code must not be reviewed by humans" — it says "humans cannot interject mid-loop." Those are different claims; OpenHands is consistent with the StrongDM letter and the Simon Willison spirit simultaneously.
- **Jaymin Ch 9 §7 (Software Factories) explicitly names "Level 5 as the target" as an anti-pattern** (report 09 §2c), recommending L3–L4 as the sweet spot. The empirical basis: CodeRabbit's 1.4× critical-issue rate, Veracode's 45% OWASP-vulnerable AI code, METR's 19%-slower-than-self-estimated.
- **Jaymin's Augmentation-vs-Automation threshold matrix** (report 09 §5.5) replaces "humans review?" with a typed binary: Augmentation Mode (≥70% same-outcome on K=5; ≥3-of-5 prompt paraphrase robustness; zero high-severity safety) vs. Automation Mode (≥90% / 5-of-5 / zero medium-or-high). The matrix forces every architecture to declare its target regime.
- **Cisco/LangChain's pilot finding "PR review process itself became the bottleneck introduced by human-in-the-loop"** (report 12 §2.2) is empirical falsification of the strong-review stance for high-throughput contexts. The Cisco team measured the bottleneck — they didn't theorize it.

**Net effect on the disagreement.** Round 1 framed this as a *position* dispute (StrongDM vs. Willison vs. compound engineering). Round 2 reframes it as a *regime classification*: each architecture should declare which Jaymin level it targets (L0–L5) and which mode (Augmentation vs. Automation) it operates in. Then the disagreement is settled per-context: regulated domains stay at L3 Augmentation; high-throughput internal tooling can move to L4 Automation; nothing in the 2026 evidence supports L5 anywhere except as a research aspiration.

**Recommendation for `00-synthesis.md` §3.1 rewrite:** replace the four-bullet position list with a regime classification per architecture (Arch 1 = L3 Augmentation; Arch 2 = L3 drifting toward L4; Arch 3 = L3 by gate-chair design; Arch 4 = L4 by construction). Cite Jaymin's empirical thresholds as the falsification criteria each architecture must meet to claim its declared regime.

### 2.2 §3.2 — Persona-based vs. graph-node agent design

Round 2 collapses this tension. Both ends turn out to be *expressible in the same substrate*.

- **OpenHands' Skill model** (report 11 §5) "can be persona-shaped *or* tool-shaped — not exclusively either." A Skill is markdown + optional MCP tools + a trigger predicate. Persona-flavored Skills are system-prompt augments; tool-flavored Skills bundle MCP tools. The same primitive expresses both. Per the SDK paper's Table 6, OpenHands and Claude Agent SDK are the only two surveyed SDKs with first-class Agent Skills.
- **Overstory's two-layer agent definitions** (report 10 §2 + §3): base definitions (`agents/{role}.md`, 9 files, role-shaped) + per-task overlays (`src/agents/overlay.ts`, task-shaped). Roles are personas; overlays are task-specific. The substrate doesn't choose; the operator does.
- **Jaymin's Multi-Agent Landscape chapter** (report 08 §3.10) maps the 2026 protocol stack — MCP (agent-to-tool), A2A (agent-to-agent), ACP (REST), ANP (decentralized). None of these protocols privilege persona over graph; they are wire formats neutral to the agent-modeling style.
- **Cisco/LangChain's two-tier control plane** (report 12 §2.2) uses *both* — Worker Agents are role-shaped (one per engineer counterpart); the Leader Agent is graph-coordination-shaped (shared prompts, observability, memory, orchestration). The Cisco pilot didn't have to choose.

**Net effect on the disagreement.** Round 2 reframes this from "pick a side" to "the substrate supports both; the methodology chooses." Compound engineering's 50+ personas and Attractor's node-graph are not competing answers; they are two valid configurations of the same harness. The harness (OpenHands Skills + Overstory's overlay system) is the unifying mechanism.

**Recommendation for `00-synthesis.md` §3.2 rewrite:** retire the disagreement as stated. Replace with a primitive-level claim: "the substrate must support persona-shaped *and* graph-node-shaped agent definitions; the architecture chooses which mix to use; the choice is a methodology decision, not a substrate decision."

### 2.3 §3.3 — Spec format (prose / structured / DOT)

Round 2 hardens the answer rather than changing it.

- **Specs are prose with structured metadata** (report 09 §3 makes this Jaymin-canonical; Kiro's EARS notation in report 12 §2.5 is an instance; BMAD's Analysis/Planning/Solutioning/Implementation phases in report 09 §3 are instances).
- **The pipeline is graph-structured** (Overstory's mail-driven coordinator + merge queue is implicitly a graph; Attractor is explicitly DOT; OpenHands' EventLog is a temporal graph). Report 10 §5 + §6 confirm the graph stance for Overstory.
- **The traceability metadata is structured IDs** (Round-1 stable-ID discipline survives unchanged; OpenHands' conversation IDs + event IDs are the substrate-level analog, report 11 §9).

**Net effect on the disagreement.** Round 1's three-part synthesis ("spec is prose; pipeline may be structured; traceability metadata is structured") stands. Round 2 adds **C12 (specs-as-source-code)** as the doctrinal frame for why specs are prose — they must be human-curated, version-controlled, reviewable. The disagreement is largely resolved, with one residual: EARS-notation (Kiro) vs. Given/When/Then (existing baseline) vs. plain prose (StrongDM NLSpec). Round 2 has no decisive evidence among these three; defer to Round 3 thread 8 (Kiro deep-dive).

---

## 3. What changed in the failure-mode list

Diff against `architectures/00-comparison.md` §2.4 (F1–F20). Report 09 explicitly proposes F21–F30; this synthesis incorporates them, vets each against Round-1 evidence, and adds two more derived from reports 10 and 11.

### 3.1 New failure modes promoted (with provenance)

**F21 — Context-window exhaustion / silent degradation.** Source: report 09 §6 (Jaymin Ch 8 §7). Symptoms: ignores earlier instructions, output quality drops, tool calls become less targeted. The partial 09 §12.1 calls this "capability percentage" with a 50%-context-fill soft ceiling. Independently corroborated by Jaymin's §3.4 "Smart Zone" (report 08 §6 vocabulary). *Mitigation:* handoff protocol at 80% utilization; per-session token caps. **Not in F1–F20.**

**F22 — Zombie agents.** Source: report 09 §6. Distinct from F1 (Hallucination Loop, a content failure) — F22 is a *state* failure: process appears functional to mechanical monitoring while producing semantically empty output. Overstory STEELMAN risk 12 (report 10 §9) corroborates with "swarms require active monitoring and circuit breakers." *Mitigation:* Tier-2 AI triage in three-tier watchdog. **Not in F1–F20.**

**F23 — Stalled-vs-thinking ambiguity.** Source: report 09 §6. The operator's *inability to read* the agent's state — mechanical observation cannot distinguish deep reasoning from a stuck loop. Overstory's `detectReady()` runtime method (report 10 §3, table row) is the substrate-level attempt to resolve this for tmux runtimes. *Mitigation:* progress-against-stated-goal checks at Tier 2 escalation. **Not in F1–F20.**

**F24 — Trust creep.** Source: report 09 §6. Adjacent to F7 (normalization of deviance) but specific to *gate relaxation* as the deviance mechanism. Quality gates that catch few issues feel like overhead; they get loosened; subtle degradation accumulates. *Mitigation:* statistical sampling (20–30% random) to calibrate gate accuracy; "quality gates exist for the failure mode, not the success mode." **Adjacent to F7 but distinguishable; promote as separate.**

**F25 — Design starvation.** Source: report 09 §6. A swarm of N agents idle because the human can't decompose work fast enough. Pushing poorly specified issues to "keep agents busy" produces low-quality work requiring expensive rework. *Mitigation:* right-size swarm to design throughput; "10 well-fed agents outperform 30 starving agents." **Not in F1–F20.**

**F26 — Telephone / sustained inter-agent chain.** Source: partial 09 §12.1 (Manifesto Rule 5) + report 09 §6. Sustained chained communication between agent instances accelerates vision-drift. Permitted as a context-reset handoff; forbidden as sustained dialogue. Adjacent to F15 (single-prompt collapse) but adds the *multi-agent* dimension. *Mitigation:* mail-based async coordination (Overstory pattern); never point-to-point sustained. **Promote with clarification that F15 is the single-agent variant.**

**F27 — Circularity / same-model builds and validates.** Source: report 09 §2c (Stanford Law CodeX framing) + report 11 §8 (OpenHands paper §7 limitation: "LLM-based security analysis is subject to adversarial prompts and inconsistent classification"). Adjacent to F1 (hallucination loop) but at the *systems* level — F1 is one agent hallucinating; F27 is a *population* of agents agreeing on a hallucination because they share priors. *Mitigation:* model-family diversity in judge selection (OpenHands `RouterLLM`, report 11 §6); human review for high-severity classes; out-of-tree holdout scenarios written before agent involvement. **Promote as separate from F1 — the population-level mechanism is distinct.**

**F28 — Holdout leakage / acceptance criteria seen by builders.** Source: report 09 §2a (StrongDM scenarios-as-holdout). When acceptance criteria leak into the builder agent's context, the agent teaches to the test. Our four architectures all imply but do not name this. *Mitigation:* substrate-level enforcement — acceptance criteria stored out-of-tree, withheld from builder agents, accessible only to validation agents. **Not in F1–F20.**

**F29 — Talent pipeline depletion.** Source: report 09 §2c (Jaymin Ch 9 §7). Specification quality depends on architects who came through implementation experience; junior dev hiring declined 67% (US) / 46% (UK) in 2024–25. Multi-year feedback loop. *Mitigation:* organizational, not architectural. **Flag as a constraint; not a per-cycle failure mode.**

**F30 — Liability vacuum.** Source: report 09 §2c. No regulatory framework adapted to software production where no human reviewed the final artifact. Distinct from F14 (attribution collapse, internal) — F30 is external regulatory attribution. *Mitigation:* explicit Augmentation Mode for regulated work; named human reviewer of record in the audit trail. **Promote as separate from F14.**

### 3.2 Additional failure modes from reports 10 and 11

**F31 — Substrate safety floor = weakest runtime adapter.** Source: report 10 §8 + §9 + §10. Overstory's `AgentRuntime` interface admits 11 adapters; only Claude Code is `stable`; Aider/Copilot/Cursor/OpenCode explicitly opt out of guards. The substrate-wide safety guarantee is the minimum across adapters. *Mitigation:* substrate-level guard mediator that every adapter must consult; reject experimental adapters in CI. **Not in F1–F20 — a substrate failure mode, not a methodology one.**

**F32 — Mail-injection / unsigned coordination messages.** Source: report 10 §5 + §9 (STEELMAN risk 10). Overstory's mail bus has no signature on the `from` field; any process that can write the SQLite file can impersonate any agent. *Mitigation:* HMAC or nonce-signed mail rows; reject unsigned at injection time. **Not in F1–F20.**

**F33 — Adversarial-prompt defeat of LLM-based security analysis.** Source: report 11 §8 (OpenHands paper §7 explicit limitation). `LLMSecurityAnalyzer` is a *probabilistic* defence; the lethal trifecta (F12) is *narrowed* by it, not closed. *Mitigation:* keep deterministic perimeter (egress allowlist, container capability dropping, no host network) doing the heavy lifting; treat LLM-based analysis as defence-in-depth. **Sharpens F12 rather than replacing it.**

### 3.3 F1–F20 status check

Round 2 contradicts none of F1–F20. Several are sharpened:

- **F1 (Hallucination Loop)** — sharpened by F27 (population-level variant) and report 11 §6 (RouterLLM as substrate-level mitigation).
- **F7 (Normalization of deviance)** — sharpened by F24 (trust creep, gate-specific variant).
- **F8 (Stale knowledge)** — sharpened by report 09 §5.4 (PRESERVE/APPEND/DATE/REMOVE) — methodology-level operationalization.
- **F12 (Lethal trifecta)** — sharpened by F33 (LLM-based analyzer is not a solution) and report 11 §8 (concrete sandboxing posture).
- **F14 (Attribution collapse)** — sharpened by report 09 §4 ("Agent CVs" — per-agent performance history) and report 10 §5 (structured per-action metadata).
- **F15 (Single-prompt collapse)** — sharpened by F26 (multi-agent telephone variant) and Jaymin's Orchestrator + Expert Swarm patterns (report 08 §3.3, §3.8).
- **F17 (Parallel agents on shared dirs)** — sharpened by Overstory's `validateWorktreeCreation` two-step post-flight (report 10 §4) and `hasContentfulCanonical` data-loss guard (report 10 §6).

**Net failure-mode count: F1–F33 with two reserved positions (F29, F30) for non-per-cycle constraints. Eleven new failure modes promoted, of which nine are operational and per-cycle, two are systemic.**

---

## 4. Shared-infrastructure coverage matrix

The Round-1 §4.1 list of nine substrate primitives, scored against Overstory (report 10), OpenHands V1 (report 11), and the Round-1 corpus (StrongDM/Attractor + Symphony + compound-engineering plugin).

Legend: ✅ provides (present and usable as-is), 🟡 partial (incomplete in a way that matters), ❌ absent.

| §4.1 primitive | Round-1 corpus | Overstory | OpenHands V1 |
|---|---|---|---|
| **Worktree per unit of work** | 🟡 (Symphony's worktree-per-issue, compound engineering's per-cycle branches; described, not packaged) | ✅ (`src/worktree/manager.ts:54-119`; branch `overstory/{agent}/{task}`; pre-flight + post-flight validation; `validateWorktreeCreation` and `rollbackWorktree`) | 🟡 (Docker workspace per conversation is moral equivalent; git worktrees would be additive) |
| **Sandboxed agent execution** | 🟡 (Attractor sandbox primitive named; not implemented in our extractable artifacts) | 🟡 (Claude Code adapter only; 10/11 adapters opt out — see F31; **safety floor = weakest adapter**) | ✅ (Docker workspace + `RemoteWorkspace` + `SecurityAnalyzer` + `ConfirmationPolicy` + `SecretRegistry`; first-class) |
| **Stable ID assignment (R/A/F/AE/U/S/K)** | ✅ (compound engineering's stable-ID discipline) | ❌ (uses agent names + task IDs; no methodology-level IDs) | 🟡 (event-sourced conversation + event IDs at substrate level; methodology IDs are an overlay) |
| **Out-of-construction-tree scenarios** | ✅ (StrongDM NLSpec + scenarios) | ❌ (worktrees side-by-side under `.overstory/worktrees/`; no scenario tree) | ❌ (architecture-specific, would build on top) |
| **LLM-judge with model-family independence** | ✅ (StrongDM's satisfaction-as-judge; provider-aligned profiles) | 🟡 (merge resolver + watchdog triage can route to different runtime; no judge *role*; reviewer is same-runtime) | ✅ (`RouterLLM` + `select_llm()` API; LiteLLM 100+ providers; only surveyed SDK with full multi-LLM routing per Tab. 6) |
| **Trajectory capture** | 🟡 (CXDB described; not extracted as a usable artifact) | ✅ (NDJSON events → `events.db`; `ov replay`, `ov trace`, `ov feed`, `ov inspect`) | ✅ (event-sourced V1 EventLog; sub-ms persist; 7.4ms crash recovery; JSONL on stdout in headless mode) |
| **Manager loop / orchestrator** | 🟡 (Symphony orchestration; compound-engineering plugin's chain; described, not packaged) | ✅ (`ov coordinator start` 1810 lines; exit triggers; mail-driven dispatch; `check-complete`) | 🟡 (single-conversation lifecycle; fleet orchestration via blocking-parallel `delegate` tool only) |
| **Decision log / audit trail** | ✅ (compound engineering's `docs/solutions/` + workpad; CXDB) | 🟡 (machine-readable SQLite history; no human-readable decision log per cycle) | ✅ (event-sourced EventLog; JSONL stream is decision log) |
| **AGENTS.md / discoverability** | ✅ (compound engineering's `AGENTS.md`; Simon Willison's discoverability discipline) | ✅ (per-runtime `instructionPath`; `runtime.deployConfig`; `agents/{role}.md` + per-task overlay) | ✅ (AGENTS.md convention native; Skills load from `.cursorrules` / `agents.md`) |

### 4.1 Two new primitives Round 2 promotes for §4.1

Independent of the existing nine, Round 2 evidence promotes two additional primitives that should be in §4.1:

| New primitive | Round-1 corpus | Overstory | OpenHands V1 |
|---|---|---|---|
| **Tiered watchdog (Daemon/Triage/Patrol)** | ❌ (no analog in extracted artifacts) | ✅ (`src/watchdog/{daemon,triage,health}.ts`; progressive escalation 0:warn → 3:terminate; AI triage with `retry\|terminate\|extend`) | 🟡 (event-sourced state supports it; not packaged as a separate component) |
| **Hard cost ceilings (per-cycle / per-task / daily)** | ❌ (cost as observability, not enforcement) | ❌ (`ov costs` reports after-the-fact; no kill-on-budget; STEELMAN risk 12 names the gap) | ❌ (no `--max-cost-usd` flag in headless mode; would be a wrapper-level concern) |

### 4.2 Reading the matrix

- **Overstory provides the *most* substrate primitives** (7 of 9 fully or partially) but its safety floor is the weakest runtime adapter (F31), and it provides neither stable-ID assignment nor out-of-tree scenarios.
- **OpenHands provides the *highest quality* substrate primitives** (6 of 9 fully) with first-class sandboxing, secrets management, and multi-LLM routing — but lacks fleet orchestration. It is a *runtime*, not an *orchestrator*.
- **The Round-1 corpus provides the *methodology* primitives** (stable IDs, out-of-tree scenarios, decision logs) but has no extractable substrate code.
- **The natural composition** is: OpenHands as per-cycle runtime + Overstory's design (re-implemented or used directly) as orchestrator + Round-1 corpus's methodology overlay. This is exactly what reports 10 §10 and 11 §10 independently recommend.

**The build-vs-buy decision is *available*, not just *possible*.** For every §4.1 primitive there is at least one MIT-licensed reference implementation; we are no longer in "design from first principles" territory.

---

## 5. CI/CD pipeline adaptation thesis

The user's framing is the tie-breaker: *we want to run the software factory as a CI/CD pipeline.* This rules out a number of otherwise-attractive options and decides several tradeoffs that Round 1 left open.

### 5.1 What "CI/CD pipeline" demands of the substrate

Report 09 §7 enumerates ten desktop-shaped assumptions in Jaymin's operating discipline that fail in a CI/CD context. The key requirements that emerge:

1. **Event-driven, not rhythm-driven.** No daily operator-at-dashboard pattern. Escalations become GitHub issues + workflow-failure notifications + structured triage reports.
2. **Ephemeral runners.** GitHub Actions workflows *are* the process; no daemon to heartbeat. Tier 1 watchdog must collapse to workflow-step timeouts + max-time guards + exit-code-driven escalation.
3. **Hard cost ceilings non-optional.** Every token is a billed token; subscription-cost approaches (Claude Code Pro) don't apply. The Gas Town pay-per-use model is the only one available; hard budgets become a substrate requirement.
4. **GitHub as the coordination medium.** Mail-based / convoy / point-to-point coordination doesn't translate to CI runners that share only `git` + GitHub issues/comments. The "GitHub-issues-as-coordination" pattern (Jaymin Ch 8 §5) is the version that maps cleanly.
5. **One-shot driver.** `ov run --task <id> --until-done --max-cost-usd N --timeout-s T` (a command that does not exist in Overstory today, report 10 §7) is the contract CI requires. Either we write the wrapper or we re-implement the orchestrator with this contract at the center.
6. **Substrate-level guard mediator.** The safety floor cannot be "the weakest runtime adapter" (F31). In CI, where no human can interject, the substrate must enforce.
7. **`always-approve` semantics.** OpenHands' headless contract (report 11 §3) is the right shape: trust enforced before invocation; observed afterward; never interactively. Adopt this.

### 5.2 The three-layer substrate stack

The plausible substrate stack, layered from bottom to top:

**Layer 1 — Per-cycle runtime: OpenHands SDK headless.**
- Adopt as the per-cycle agent runtime under every architecture (report 11 §10).
- Invoke as `openhands --headless --json -t "<probe brief>"` in a Docker sandbox (`DockerWorkspace`).
- Captures JSONL event stream as the decision log (satisfies F31 partial + the Round-1 trajectory-capture primitive).
- `RouterLLM` for model-family diversity (satisfies F1/F27 mitigation).
- `SecurityAnalyzer` + `ConfirmationPolicy` + `SecretRegistry` for substrate-level guards (satisfies F12 partial + F33 narrowing).
- `Sub-Agent Delegation` tool for blocking-parallel sub-agents within a single conversation.

**Layer 2 — Orchestration: Overstory design, Python re-implementation.**
- Adopt the *design IP* (report 10 §10): `AgentRuntime` interface, mail schema, 4-tier merge resolver including `hasContentfulCanonical` and `looksLikeProse`, sentinel-file merge lock with pid-liveness takeover, FIFO queue with `resolved_tier`, three-tier watchdog escalation, mulch-backed conflict-history learning with skip-after-2-failures, `check-complete` exit-trigger model.
- Re-implement in Python on top of OpenHands SDK (report 10 §10 reasons 1, 2, 3).
- Translate "mail bus" to GitHub issues + comments as the coordination medium (per §5.1 above and Jaymin Ch 8 §5).
- Substitute Overstory's tmux-first model with OpenHands' headless-only model.
- Substitute Overstory's per-runtime guards with substrate-level guard mediator that every OpenHands invocation consults.
- Add hard cost ceilings (per-cycle / per-task / daily) as a non-optional primitive (resolves F31 + the C15 consensus).
- Add `factory run --task <id> --until-done --max-cost-usd N --timeout-s T` as the one-shot CI driver (closes the report 10 §7 gap).

**Layer 3 — Methodology overlay: one of the four architectures.**
- Run as configuration on top of Layers 1 + 2.
- The architecture is the methodology; the infrastructure is shared (Round-1 §4 stance, now even more strongly supported).
- Different cycles can run different architectures; the substrate doesn't care.

### 5.3 Reconciling sub-02 and sub-11 recommendations

The brief notes that sub-02 (Overstory audit, report 10) recommended "steal Overstory's design, re-implement in Python on top of OpenHands SDK" and sub-11 (OpenHands audit, report 11) recommended "adopt OpenHands SDK + CLI as the per-cycle agent runtime, keep orchestration above OpenHands." These are not in tension. They are complementary statements about *two different layers* of the same stack.

- Sub-11's "orchestration above OpenHands" is the *gap* sub-02 fills with Overstory's design.
- Sub-02's "Python re-implementation on top of OpenHands SDK" is the *substrate* sub-11 names as the per-cycle runtime.
- Both agree on the same conclusion stated as a stack: **OpenHands SDK + CLI underneath; Overstory-design-in-Python on top.**

The reconciliation makes the CI/CD adaptation tractable:
- Closing the "no `ov run`" gap (sub-02's reason 3) is also closing the "fleet orchestration is not provided by OpenHands" gap (sub-11's recommendation 4).
- Substituting OpenHands' headless contract for Overstory's tmux/desktop assumption is the CI/CD translation (report 09 §7).
- Inheriting OpenHands' `RouterLLM` + `SecurityAnalyzer` + `SecretRegistry` resolves the F31 (substrate safety floor) failure inherited from Overstory's 10-experimental-adapter footprint.

### 5.4 What this rules out

- **Forking Overstory as-is** — locks us into Bun + TypeScript and inherits 10 experimental adapters with no guards (report 10 §10, F31).
- **Building substrate from scratch in Python** — discards ~50 specific design choices Jaymin made informed by production pain (report 10 §10 "why not re-implement from scratch").
- **Adopting the third-party OpenHands GitHub Action** — 10 stars, bus factor 1, not co-designed with All-Hands-AI (report 11 §7). Roll our own thin wrapper (~80 lines).
- **Using Claude Code Pro as the runtime** — subscription model doesn't apply to API-backed CI (report 09 §7 A3).
- **Mail-based agent coordination within the substrate** — doesn't compose with ephemeral GitHub Actions runners (report 09 §7 A5).
- **L5 dark-factory ambition** — explicitly anti-pattern per Jaymin Ch 9 §7 (report 09 §2c); empirical 2026 ceiling is L3–L4.

---

## 6. Updated recommended path forward (proposal — does not edit `architectures/00-comparison.md`)

This section proposes a replacement for `architectures/00-comparison.md` §7. The original §7 is preserved verbatim in §6.1 below so the diff is traceable. The proposed replacement is in §6.2. The orchestrator + future user pass owns the actual edit.

### 6.1 §7 (Round 1) — preserved for diff

**§7.1 — Pick Architecture 2 (Compound Atelier) as the working baseline.** Reasons: only fully-realized public reference implementation; broadest 20-failure-mode coverage; scales solo-to-small-team via queue+workpad; knowledge accumulation is most concrete; cleanest hybridization interfaces.

**§7.2 — Then enhance with selective borrows from the others.** From Arch 1: layered spec for high-stakes greenfield. From Arch 3: defect-of-origin attribution. From Arch 4: small N=3–4 tournaments inside uncertain Atelier issues.

**§7.3 — Reserve full-architecture adoption for specific contexts.** Full Refinery for greenfield high-stakes; full Foundry for regulated environments; full Tournament for designated exploration projects.

**§7.4 — Build the shared infrastructure first.** Worktree-per-unit isolation; sandboxed agent execution with capability scoping; stable-ID enforcement + RTM-equivalent; out-of-construction-tree scenario storage; trajectory capture; manager-loop / orchestrator with 5-state queue.

### 6.2 §7 (Round 2 proposal) — replacement

**§7.1 — Substrate stack first; methodology overlay second.**

The Round-1 §7 framing was correct that infrastructure investment unlocks architectural optionality. Round 2 sharpens this: the substrate is no longer a green-field build. Two production-tested reference implementations exist (OpenHands V1 and Overstory) and a complete substrate stack can be assembled from them in known proportions. Specifically:

1. **Per-cycle runtime: OpenHands SDK + CLI (headless mode).** Adopt as the per-cycle agent runtime under every architecture. Invoke as `openhands --headless --json -t "<probe brief>"` in a Docker sandbox.
2. **Orchestration: Overstory design re-implemented in Python.** Steal the design IP — `AgentRuntime` interface (or its OpenHands equivalent), mail schema (translated to GitHub issues + comments for CI), 4-tier merge resolver, three-tier watchdog, sentinel locks, FIFO queue with `resolved_tier`, mulch-backed conflict-history learning, `check-complete` exit triggers. Do not adopt the implementation; it is Bun-locked and its safety floor is the weakest runtime adapter.
3. **CI driver: one-shot `factory run --task <id> --until-done --max-cost-usd N --timeout-s T`.** Close the gap report 10 §7 names. Hard cost ceilings, runaway-spawn detection, structured-failure → CI-exit-code mapping. The wrapper is small (~150 lines per Overstory's own estimate); the contract is large (it is what makes the rest CI-deployable).

**§7.2 — Methodology baseline: Architecture 2 (Compound Atelier), with the harness/scaffold split made explicit.**

The Round-1 reasons for choosing Atelier survive Round 2 unchanged: only fully-realized public reference; broadest failure-mode coverage; scales naturally; knowledge accumulation is concrete; cleanest hybridization interfaces. Round 2 adds: Cisco/LangChain's pilot (report 12 §2.2) is *external empirical validation* of the Worker+Leader two-tier control plane that Atelier's Operator+worker chain implements. 93% reduction in time-to-root-cause and 65% reduction in execution time are the numbers.

The Round-2 refinement: the Atelier's "shared infrastructure" should be re-named **the shared harness** (per C10/C11). The nine substrate primitives (now eleven, with tiered watchdog and cost ceilings added per §4.1) are *harness* components. The AGENTS.md / discoverability + stable-ID + scenarios layer is *scaffold*. The methodology runs on top of both.

**§7.3 — Selective borrows, regime-classified.**

Each architecture declares its target Jaymin level + Augmentation/Automation regime:

- **From Architecture 1 (Refinery, L3 Augmentation):** the layered spec discipline + revelation cycle for high-stakes greenfield work. Failure classification (silence/ambiguity/incorrectness/inconsistency/undiscovered preference) becomes the per-cycle audit pattern.
- **From Architecture 3 (Foundry, L3 Augmentation):** defect-of-origin attribution; phase artifacts (SRS, SAD, DD) for regulated work. The phase model is the right shape when audit trails matter.
- **From Architecture 4 (Tournament, L4 Automation, with explicit threshold validation):** small N=3–4 tournaments inside uncertain Atelier issues; `RouterLLM`-enforced model-family diversity (report 11 §6) closes F1/F27.

**§7.4 — What the harness must enforce (substrate-level, methodology-agnostic).**

The shared harness must provide:

1. Worktree per unit of work (Overstory pattern; `validateWorktreeCreation` + `rollbackWorktree`).
2. Sandboxed agent execution at the substrate level, not per-adapter (closes F31).
3. Stable ID assignment + cross-artifact RTM-equivalent.
4. Out-of-construction-tree scenarios with holdout-leakage enforcement (closes F28).
5. LLM judge with `RouterLLM`-enforced model-family independence (closes F27).
6. Trajectory capture (event-sourced; OpenHands V1's EventLog as reference; sub-ms persist is achievable).
7. Manager loop / orchestrator with the 5-state queue *and* `check-complete` exit-trigger model.
8. Decision log / audit trail (JSONL event stream from headless OpenHands satisfies this for free).
9. AGENTS.md / discoverability (scaffold layer, not harness — but every harness must consult it).
10. **Tiered watchdog (Daemon/Triage/Patrol)** with cadences seconds / seconds-to-minutes / minutes-to-hours (closes F22/F23).
11. **Hard cost ceilings (per-cycle / per-task / daily)** with kill-on-budget enforcement (resolves the C15 consensus).
12. **Substrate-level guard mediator** (capability/path/bash guards every adapter consults; closes F31).
13. **Mail-injection signing** (HMAC or nonce on coordination messages; closes F32).
14. **Cost telemetry + Agent CV aggregation** (per-agent quality-gate pass rate, rework frequency, average tokens per task; closes the F14 sharpening from report 09 §4).

Eleven of these fourteen are in §4.1 already (with #2 and #6 upgraded by Round 2 evidence). Three are new primitives Round 2 promotes (#10, #11, #12 are explicit; #13 and #14 follow from F32 and the report-09 §4 sharpening).

**§7.5 — Failure-mode coverage updated.**

The per-architecture coverage table in §2.4 of the comparison doc should extend to F1–F33 with the eleven new failure modes mapped against the four architectures. The mapping should be guided by:

- F21–F25 are operational and per-cycle; primarily mitigated by the *harness*, not by the architecture choice. Adopting OpenHands V1 (event-sourcing, EventLog persistence, sub-ms latency) + three-tier watchdog (Overstory pattern) closes these for *all four* architectures simultaneously.
- F26 (telephone) is architecture-specific: most severe for Arch 2 (persona panels) and Arch 4 (tournament chains); mitigated by mail-based async coordination at the substrate.
- F27 (circularity) is most severely failed by Arch 4 (Tournament) and Arch 2 (Atelier) at high parallelism; `RouterLLM` model-family diversity is the substrate-level mitigation.
- F28 (holdout leakage) is architecture-agnostic but must be enforced by the substrate (out-of-tree scenarios, no leakage into builder context).
- F31–F33 are substrate failures; addressed by substrate engineering, not by methodology choice.

**§7.6 — Regime classification (replaces "when to pick which" framing).**

Each architecture declares its target operating regime per Jaymin's threshold matrix (report 09 §5.5):

| Architecture | Target level | Mode | Threshold for claiming the regime |
|---|---|---|---|
| Arch 1 (Refinery) | L3 | Augmentation | ≥70% K=5 consistency; ≥3-of-5 prompt-paraphrase robustness; zero high-severity safety |
| Arch 2 (Atelier) | L3 (drifting to L4) | Augmentation | Same as above for the baseline; declare L4 only if Automation thresholds met |
| Arch 3 (Foundry) | L3 | Augmentation | Same as above + per-phase gate-board sign-off; defect-of-origin attribution |
| Arch 4 (Tournament) | L4 | Automation | ≥90% K=5 consistency; 5-of-5 robustness; zero medium-or-high safety |

L5 is explicitly not a target for any architecture. The talent pipeline (F29) and liability vacuum (F30) constraints argue against L5 as a goal even in principle.

### 6.3 What Round 1's §7 got right that Round 2 preserves

- **Architecture 2 (Compound Atelier) as the working baseline.** Survives Round 2 unchanged; further validated by Cisco/LangChain pilot data.
- **Build the shared infrastructure first.** Survives Round 2 unchanged; sharpened by the OpenHands+Overstory substrate stack.
- **Selective borrows from the other three architectures.** Survives Round 2 unchanged; sharpened by regime-classification.

### 6.4 What Round 1's §7 missed that Round 2 corrects

- **No mention of an existing substrate.** Round 1 implicitly framed the shared infrastructure as a green-field build. Round 2 demonstrates two production-tested reference implementations exist; the build-vs-buy decision is *available* (§4.2 above).
- **No mention of CI/CD as the operating model.** Round 1's §4.1 list is desktop-shaped (manager loop assumed long-lived; trajectory capture assumed observable in real time). Round 2 names CI/CD as the explicit operating model and translates the substrate primitives accordingly.
- **No mention of regime classification.** Round 1's "human review required / eliminated / tiered" framing is replaced by Jaymin's level + mode taxonomy with empirical thresholds.
- **No cost-ceiling primitive.** Round 1 had cost as observability; Round 2 promotes it to enforcement.
- **No tiered-watchdog primitive.** Round 1 collapsed mechanical / AI-triage / strategic supervision into one "manager loop"; Round 2 separates the three tiers.

---

## 7. Open questions for Round 3

The Round-3 follow-up threads are already catalogued in `research/PLAN.md` §11. This section cross-references rather than duplicates. Threads sharpened by Round 2 evidence:

- **Thread 4 (Steve Yegge's Gas Town + Beads).** Round 2 strengthens this: Gas Town is now named as one of two production implementations of the three-tier watchdog (the other being Overstory). A direct read of Gas Town's Go implementation would let us pick a substrate-level reference for the watchdog primitive.
- **Thread 5 (Klaassen's three sibling Every articles).** Round 2 strengthens this: Cisco/LangChain's pilot is the first empirical validation of the Worker+Leader pattern Klaassen describes. The sibling articles likely contain the per-stage adoption ladder details Round 1's synthesis already incorporated; Round 3 should harvest the remaining detail.
- **Thread 8 (Security primitives — CaMeL + Safe YOLO + Lethal Trifecta).** Round 2 sharpens this with F33 (LLM-based analyzer is probabilistic only) and report 11 §8 (OpenHands' concrete `SecurityAnalyzer` + `ConfirmationPolicy` + `SecretRegistry`). A red-team pass on `LLMSecurityAnalyzer` with the prompt-injection corpus is the actionable Round-3 task; report 11 §10 already flags it as a new follow-up.
- **Thread 11 (Compound Knowledge plugin deep-dive).** Round 2 strengthens this with PRESERVE/APPEND/DATE/REMOVE (report 09 §5.4) and Agent-as-Code (BMAD pattern). Round 3 should map the Compound Knowledge plugin onto Jaymin's knowledge-evolution protocol.

New Round-3 candidates surfaced specifically by this synthesis:

- **Kiro substrate audit.** Report 12 §2.5 flags Kiro as a near-peer of Arch 1 + Arch 3 as a product. Two open questions: (1) does Kiro's spec → design → tasks → execution loop satisfy the layered-spec discipline of Arch 1, or does it conflate layers? (2) Is Kiro's CLI invocable from CI in a headless-like mode?
- **Sub-Agent Delegation tool deep-dive in OpenHands.** Report 11 §4e + §10 flags this. For Arch 2 (Atelier, N parallel issues) and Arch 4 (Tournament, N parallel candidates), we need max fan-out, fault-tolerance behavior on crash, event-log merge semantics, and non-blocking extensibility.
- **Gas Town read.** Listed under Thread 4 but worth promoting: the Go implementation of the three-tier watchdog is the alternative reference to Overstory's TypeScript version. Comparing the two would let us pick the substrate-level reference with confidence.
- **El Kaim Round 4 clusters (PLAN.md §12).** The Continuous / Intent-Driven Enterprise Architecture book deserves the same harness/scaffold treatment Round 2 gave Jaymin's book. Already catalogued; not duplicated here.

No new follow-ups are blocking the Round-2 conclusions; all are deepening.

---

## 8. Closing claim

Round 2 turned the software-factory project from "design a methodology" into "configure a methodology on top of an existing substrate." The substrate is **OpenHands SDK + CLI (per-cycle runtime) + Overstory-design-in-Python (orchestration)**, with **GitHub issues + comments as the coordination medium** (CI-friendly translation of mail), **hard cost ceilings** (non-optional, not best-practice), **tiered watchdog** (Daemon/Triage/Patrol), and **substrate-level guard mediation** (closes F31). The methodology layer is **Architecture 2 (Compound Atelier)** declaring L3 Augmentation, with selective borrows from Arch 1 (layered spec), Arch 3 (defect-of-origin), and Arch 4 (small N=3–4 tournaments with `RouterLLM` diversity). The four-architecture set survives Round 2 with refined regime-classification but no structural change.

The Round-1 baseline recommendation — Atelier as the working baseline — is preserved. Round 2's contribution is the substrate stack underneath it and the CI/CD operating-model translation that lets the whole thing run as a pipeline.

---

*End of report — research/13-round-2-synthesis.md v1.0*
