---
based-on-commit: ed48c26
based-on-date: 2026-05-23
---

# Software Factory — v3 Brief (post-bias-guard revision)

**Status:** Active brief for the v3 architecture synthesis. Revised 2026-05-23 to absorb Phase-0 bias-guard findings (Skeptic + Naive newcomer + Historian) and the user decisions captured in [`decisions-captured.md`](decisions-captured.md). Supersedes the implicit Round-1 brief (which targeted "general execution environment, solo→small team") and the [`research-plan.md`](../../archive/research-plan.md) "lights-out greenfield" framing (now expanded to brownfield as a co-equal mandate).

**Authoritative on:** what the v3 architecture set must address; the operating discipline for the synthesis process; the load-bearing tensions the synthesis must surface.
**Not authoritative on:** how those things get addressed. The 9 Phase-2 tracks, the Phase-3 merge, and the Phase-6 architecture specs decide that.

**Provenance.** Every load-bearing claim cites either a user-authored constraint in [`constraints-extracted.md`](constraints-extracted.md) (tagged `UC1`–`UC8`), a user decision in [`decisions-captured.md`](decisions-captured.md) (tagged `D1`–`D4`), or a corpus source. Lead-agent inferences are flagged as such.

---

## 0. Glossary (defined terms used in this brief)

These terms have specific meanings in this brief. Synthesis subagents must use them per the definitions below; if a subagent has reason to challenge a definition, that is itself a finding to surface.

| Term | Definition |
|---|---|
| **Software factory** | An autonomous (lights-out) system that produces working software with minimal continuous human-in-the-loop intervention. The artifact this project is designing. |
| **Lights-out** | No human in the per-cycle inner loop for work units the factory has classified as automation-eligible. Compatible with humans setting policy, sample-auditing post-hoc, intervening on watchdog escalation, and re-entering on declared trigger conditions. Lights-out is **not** identical to L5 (see §2.1). |
| **Greenfield (mandate)** | The target system has no pre-existing implementation. Priors from adjacent domains, exemplar projects, frameworks, library ecosystems, and operator-curated knowledge from *other* factory runs are permitted and expected. "No pre-existing implementation" — not "no priors." (Per Skeptic finding #6 revision.) |
| **Brownfield (mandate)** | The target system has a pre-existing implementation. The codebase, its tests, dependencies, runtime telemetry, and accumulated history are primary inputs that constrain what the factory can do. |
| **Both-mandates** | An architecture (or analysis track) that addresses greenfield and brownfield in a single design, with the same primitives expressing both. Not assumed possible; tested in Phase 2's 3 no-axis-prescribed tracks per D1. |
| **Mandate-fit** | A classification of how well an architecture serves a given mandate × work-unit-class combination (per D2). Possible values per cell: `greenfield-fit` / `brownfield-fit` / `both` / `n/a`. |
| **Work-unit-class** | The kind of work a single factory cycle does. Initial 5-class list (subject to Phase-2/3/4 revision): `initial-spec` / `refactor` / `mvp` / `post-mvp-evolution` / `regression-fix`. |
| **Substrate** | Lead-agent working definition: shared platform primitives the architectures consume but do not own (sandbox, trajectory capture, judge routing, cost ceilings, watchdog, scenario storage, coordination medium, guard mediator, secret store, AGENTS.md discoverability). The *contents* of this list are a Phase-4 output, not pre-decided. The *existence* of the substrate/methodology boundary is itself open for challenge (Skeptic finding #3, partially addressed). |
| **Methodology** | Lead-agent working definition: the per-cycle process an architecture runs (how work units are framed, what the unit-of-work looks like, what gates apply, how knowledge accumulates, how errors are handled). Sits on top of the substrate. |
| **Harness** | Per Round-2 C10: the runtime control system below the agent (dispatch, context management, safety enforcement, loop control). "Agent = Model + Harness." Distinct from scaffold. |
| **Scaffold** | Per Round-2 C11: pre-runtime artifacts (`CLAUDE.md`, `AGENTS.md`, system prompts, project conventions, skill specs). Read at runtime; not part of the runtime itself. |
| **Spec-malleable** *(Skeptic-flagged lead-agent label, per Historian contamination footnote)* | Greenfield characteristic in UC4: the system's architecture is still moving during spec refinement; commitments are reversible. |
| **Code-archaeological** *(Skeptic-flagged lead-agent label, per Historian contamination footnote)* | Brownfield characteristic in UC4: the system's architecture is fixed by the existing codebase; the factory analyzes what is there and grows it. The label compresses UC4's longer prose; adversarial subagents should challenge the underlying claim, not the label. |
| **OpenHands V1** | An MIT-licensed agent-runtime SDK + CLI; per report [`11`](../../research/11-openhands-substrate-audit.md) (OpenHands substrate audit). Cited in this brief only as a source of measurement data; **not** a normative dependency. |
| **RouterLLM** | Per-call model-routing layer documented in OpenHands V1 (report [`11`](../../research/11-openhands-substrate-audit.md) §6). Cited as one example of provider-routing abstraction; the abstraction itself is open for challenge. |
| **Daemon / Triage / Patrol** | Per Round-2 C14: the three tiers of the watchdog pattern. **Daemon** = mechanical liveness (process alive? heartbeat? resource limits?) at seconds cadence. **Triage** = AI reclassification (is the agent stalled or thinking?) at seconds-to-minutes cadence. **Patrol** = strategic drift detection across hours, escalating to human. |
| **Atelier-style** / **Refinery-style** | Two of the four v2 architectures (now archived). *Atelier-style* unit of work = an issue from a queue. *Refinery-style* unit of work = a change request against a layered spec. Both terms used only as shorthand in OQ-B4; the v2 architectures are not authoritative for v3. |
| **`docs/solutions/`** | The compound-engineering plugin's accumulated knowledge-store directory ([`research/03`](../../research/03-every-compound-engineering.md)). Mentioned in OQ-B5 as one example of a "prior-runs artifact"; the *convention* (a specific directory) is not normative for v3. |
| **Adversarial pass** | A multi-persona subagent review where each subagent attacks a target draft from a defined perspective (red-team, pre-mortem, regulator, CFO, on-call, newcomer, etc.). Output: per-persona critique, integrated into the target as an objections-and-responses appendix. |
| **Persona-diverse review** | Any subagent-review step where the personas are explicitly drawn from the bias-guard catalog ([`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) §3). Distinct from "adversarial pass" only in framing — adversarial pass is the most aggressive form of persona-diverse review. |
| **Back-fill** | Phase 7: lead-agent pass that enumerates every claim, framing, primitive, or recommendation in the archived v1/v2 material and classifies each as `absorbed`, `rejected (reason)`, or `TBD` against the v3 set. |
| **L0–L5** | Shapiro's Five Levels of AI coding autonomy (canonical post, report [`32`](../../research/32-shapiro-completion-chat-agent-claw.md)): **L0** none / **L1** completion (autocomplete) / **L2** chat (conversational coding) / **L3** agent (LLM with tools and a loop, human approves discrete steps) / **L4** agent operating autonomously over multi-step work under standing operator policy ("I'm here," Shapiro's self-position) / **L5** dark factory (no human in the loop, ever). |
| **Augmentation Mode** / **Automation Mode** (Jaymin) | Per report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5. **Augmentation Mode** = human-in-loop per cycle; required thresholds ≥70% K=5 consistency, ≥3-of-5 prompt-paraphrase robustness, zero high-severity safety incidents. **Automation Mode** = no human in inner loop; required thresholds ≥90% K=5 consistency, 5-of-5 prompt-paraphrase robustness, zero medium-or-high safety incidents. *These thresholds are corpus-derived (Skeptic #10), not user-mandated; see OQ-B6.* |
| **K=5 consistency** | Run the same task 5 times across 5 independent agent invocations; measure what fraction reach the same outcome. ≥70% / ≥90% are the Augmentation / Automation bars. |
| **Prompt-paraphrase robustness** | Restate the same task using 5 different prompt formulations; measure what fraction produce equivalent outcomes. ≥3-of-5 / 5-of-5 are the bars. |
| **Safety-incident severity** | Loosely: `low` = recoverable in-cycle; `medium` = requires rollback; `high` = data loss / security exposure / merged-and-shipped defect with user impact. Jaymin's thresholds use this severity-class taxonomy. *Definitions are lead-agent paraphrase of Jaymin's framing; verify against report 09 if the bars become load-bearing.* |
| **F36/F37 collision** | Reports 25 and 26, dispatched in parallel during Round-9, each independently proposed candidate failure modes numbered F36 and F37 with *different* phenomena attached. Resolution is **a lead-agent triage call** per [[`PLAN`](../../research/PLAN.md)](../../research/PLAN.md) §3.6; **subagents must not silently resolve this**. |

---

## 1. What we are building

A **software factory** (per glossary §0) — autonomous over extended time horizons, with the human's role moved upstream (spec authorship, scenario curation, regime tuning, scoring-weight tuning, escalation review) and downstream (review of aggregated outputs, regime drift detection, sample auditing), but **not in the per-cycle inner loop** for work units the factory has classified as automation-eligible.

Two mandates, treated as potentially distinct solutions:

- **Greenfield mandate** (per glossary §0).
- **Brownfield mandate** (per glossary §0).

These may produce **different architectures**. They may also share substrate. *Which* primitives are shared is determined in Phase 4, not pre-listed here (per Skeptic finding #14 revision).

---

## 2. Operating mode: lights-out (with named tension)

The factory operates **lights-out** per the glossary definition: no human in the per-cycle inner loop for automation-eligible work units, compatible with humans setting policy, sample-auditing post-hoc, intervening on watchdog escalation, and re-entering on declared trigger conditions.

### 2.1 The lights-out / L5 / regime tension (load-bearing, must be addressed)

The post-Round-12 corpus contains tensions that the v3 synthesis must address head-on. The crucial first step is to **test the vocabulary mapping** before assuming the tension is real (per Skeptic finding #13):

> *"Lights-out" (UC1's term) is not necessarily "L5" (Jaymin's term). The tension is real only if these vocabularies map onto each other. The synthesis's first task in this area is to test the mapping.*

If the mapping holds, the corpus presents these tensions:

- **Jaymin West, *Agentic Engineering* Ch 9 §7** (report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md), *Jaymin's harnesses & practices*): names **L5 ("dark factory") as an empirical anti-pattern** in 2026. Cites **CodeRabbit** (1.4× critical-issue rate vs. human-reviewed; methodology: comparison study summarized in report 09 — verify scope, populations, and review-protocol equivalence before treating as a refutation of lights-out), **Veracode** (45% OWASP-vulnerable AI-generated code; methodology: scanning study at code level — applicability to factory-output code with post-cycle V&V is open), **METR** (developers 19% slower than self-estimated when using agents unattended; methodology: developer-productivity study — applies to *developer-using-agent*, not necessarily *factory-running-agents-on-its-own*; the analogue may or may not hold).
- **Dan Shapiro, *Five Levels* canonical post** (report [`32`](../../research/32-shapiro-completion-chat-agent-claw.md), *Shapiro's Completion/Chat/Agent/Claw + Five Levels*; followup [`01`](../../research/followup/01-shapiro-five-levels.md), *Shapiro Five Levels canonical drain*): positions himself at **L4 ("I'm here")** — explicit refusal of L5 as personal practice.
- **Jaymin's Augmentation-vs-Automation threshold matrix** (report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5): see glossary §0 for definitions. Automation Mode thresholds are *corpus-derived recommendations from one author* (Skeptic finding #10), **not user-mandated bars**. The user (UC1) said "lights-out"; Jaymin's thresholds are one candidate empirical bar set.

**This tension cannot be hand-waved.** The v3 synthesis must address it in one of several ways (any may be valid; the choice is a per-architecture concern):

- (a) Explain how the lights-out mandate clears Jaymin's (or some other source's) empirical bars at a per-cycle level (which threshold metrics, by what mechanism, measured how).
- (b) Redefine the operating mode (e.g., lights-out *over a defined work-unit-class surface* rather than uniformly).
- (c) Declare a regime-classification scheme that names where the factory operates at L4 vs. L5 and which work units flow to which.
- (d) Adopt a different threshold-bar source (or set of sources) than Jaymin's, with justification.
- (e) Reject the L5-as-anti-pattern claim with corpus-grounded counter-evidence.

The lead agent's working stance: option (c) plus (b) is the most likely shape, but the choice is open and load-bearing. **Mandatory treatment in every Phase-2 track.**

---

## 3. Working hypothesis — to test, not assume

**User-stated hypothesis** (UC4):

> No single architecture works best for both mandates. Greenfield is **spec-malleable** (architecture changes during spec refinement). Brownfield is **code-archaeological + existing-architecture-as-given** (architecture is largely fixed by the existing codebase; the factory analyses what is there and grows it).

> [^contamination]: The labels **"spec-malleable"** and **"code-archaeological"** are lead-agent shorthand for UC4's longer prose. They are accurate compressions, not distortions — but they are now anchor terms that downstream tracks could inherit. Adversarial subagents should challenge the *underlying claim* in UC4, not the *labels*. Historian flagged this as a mild contamination risk; this footnote is the agreed mitigation.

**Discipline.** The v3 synthesis treats this as a **genuinely falsifiable hypothesis** (per D1):

- Phase 2 dispatches **3 both-mandates tracks** (`no-axis-prescribed`) in parallel with the 6 mandate-specific tracks. Each both-mandates subagent is tasked with producing ONE architecture that addresses both mandates from scratch; each picks its own organizing axis (mandate is not required to be primary); each defends the axis choice.
- The corpus may support a substrate-heavy + thin-methodology design that works for both with different overlays. The 3 both-mandates tracks are the explicit search for that design.
- A spec-malleable phase could plausibly be applied to brownfield as a wrapper layer (spec the *change*, not the system). A code-archaeological phase could plausibly precede greenfield work too (analyze the *problem domain* corpus rather than an existing codebase).

If all 3 both-mandates tracks converge on architectures that internally split by mandate, the hypothesis is empirically confirmed. If 1+ produce defensible unified architectures, the hypothesis is falsified for that architecture's domain of applicability.

---

## 4. Round-1/Round-2 defaults carried forward (per D3)

**This section is not a list of invariants.** The original v3 brief framed it that way; Skeptic finding #4 surfaced that the framing made challenge socially costly. Per D3, the items below are **defaults** carried forward from prior synthesis rounds. Every Phase-2 track (all 9) **must** mark each item as either:

- `accepted with justification` — track agrees this default applies in its framing; one-sentence justification.
- `challenged` — track has corpus evidence this default does not apply (or applies only conditionally) in its framing; cite the corpus.

Phase 3's merge step surfaces challenges as DECISIONS-PENDING items for user review (per ADR-0005's concrete-task discipline).

**Particularly fragile defaults** (track authors: pay attention):

- *"Scenarios live outside the codebase as a holdout set"* — brownfield architectures may genuinely inherit scenarios *from* the codebase (production traces, existing test suites, runtime telemetry).
- *"Agent = Model + Harness"* — architectures that treat agents as graph nodes (Attractor-style) or populations (Tournament-style) do not decompose cleanly into "model + harness."

### 4.1 The defaults

D-1. **Specs are the durable, version-controlled, human-curated artifact** ([`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §2.1, *Round-1 synthesis*; report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §3 attributes Sean Grove). True for both mandates, though the *content* and *malleability* of the spec differ.
D-2. **Scenarios live outside the codebase as a holdout set** ([`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §2.2, *Round-1 synthesis*). **Flagged fragile for brownfield.**
D-3. **Agent = Model + Harness** ([`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §1.1 C10, *Round-2 synthesis*). Harness and scaffold are distinct layers (C11). **Flagged fragile for graph-node and population architectures.**
D-4. **Holdout discipline** (acceptance criteria withheld from builder agents) is substrate-enforced, not methodology-optional ([`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §1.1 C13, *Round-2 synthesis*).
D-5. **Hard cost ceilings are non-optional in CI** ([`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §1.1 C15, *Round-2 synthesis*).
D-6. **Tiered watchdog (Daemon / Triage / Patrol) is a substrate primitive** ([`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §1.1 C14, *Round-2 synthesis*). See glossary §0 for cadences.
D-7. **Trajectory capture is cheap and production-tested** ([`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §1.1 C16, *Round-2 synthesis*; OpenHands V1 sub-ms per-event persist, 7.4ms median crash recovery — *measurement context: OpenHands' own benchmark across 433 SWE-Bench Verified replays; generalizes to other substrates only insofar as event-sourced persistence layers are comparable*).

---

## 5. Greenfield cold-start — mandatory dedicated synthesis section (per Historian M4/M5)

**Promoted from open question to mandatory section.** The cold-start problem for greenfield was originally OQ-B5 in the earlier brief draft. Historian M4 surfaced that the user-authored language in [`research-plan.md`](../../archive/research-plan.md) §"One specific risk for the greenfield mandate" ranks cold-start as **the load-bearing risk** of the greenfield mandate, deserving a dedicated synthesis section before v3 architectures land. Per D4, this is promoted.

Every Phase-2 greenfield track (3 tracks) and every Phase-2 both-mandates track that addresses greenfield (at least 1 of the 3, possibly all 3) **must** carry an explicit `## Cold-start` section in its output.

### 5.1 Required inputs to the cold-start treatment (per Historian M5)

The user named the following research threads as specifically relevant:

- **Report [`25`](../../research/25-requirements-engineering-foundations.md)** (Requirements engineering foundations, RE/SE methodology).
- **Report [`26`](../../research/26-prompt-underspecification-academic.md)** (Prompt underspecification, LLM-RE academic).
- **Report [`30`](../../research/30-cognitive-escrow.md)** (Cognitive escrow, Stanford CodeX governance).
- **Report [`31`](../../research/31-caremark-rsi-board-exposure.md)** (Caremark RSI board-exposure, Stanford CodeX governance).
- **Followup [`10`](../../research/followup/10-governance.md)** (Governance, AILCCP).

These threads are *required reading* for cold-start tracks. Other corpus material may be brought in additionally.

### 5.2 What the cold-start section must answer

- How does a *greenfield* factory bootstrap on day 0 — no scenarios, no issue queue, no `docs/solutions/`, no prior runs?
- What priors are available (adjacent domains, exemplar projects, library docs, operator knowledge)?
- How is the bootstrap protected against silent failure (the architecture has no track record yet to evaluate it against)?
- What is the trajectory from day 0 → day N (when does the factory transition from cold-start to steady-state)?

---

## 6. Required outputs from v3 (per D2 schema)

The v3 work produces:

1. **Failure-mode catalog** (canonical, consolidated). F1–F49+ resolved including the F36/F37 collision (collision triage is **a lead-agent call, not a subagent call** — see glossary §0); severity ranked separately for greenfield and brownfield. → `failure-modes-v3.md`.
2. **Contradictions register.** Pairwise contradictions in the corpus, both sources cited, no resolution attempted at register time. → `contradictions.md`.
3. **Corpus inventory.** Per-report 1-paragraph anchor + greenfield/brownfield/both tag. → `corpus-inventory.md`.
4. **Mandate-specific syntheses + unified synthesis** (per D1): greenfield + brownfield + unified, each surviving multi-persona adversarial review. → 3 files in `architectures/v3/`.
5. **Shared-substrate document and divergence document.** The load-bearing boundary (greenfield/brownfield divergence at substrate vs. methodology layer). → 2 files.
6. **ADRs** for every binding decision (~14, split across shared-substrate and mandate-specific). → `docs/adr/NNNN-*.md`. Architecture specs cite synthesis; ADRs do not cite reports (per Historian M3, ADR-0002).
7. **Architecture specs** (count emergent, not predetermined). Each carries a YAML frontmatter header per ADR-0004 (`based-on-commit` + `based-on-date`, per Historian M1) **and** a per-(work-unit-class) mandate-fit block per D2:
   ```yaml
   ---
   based-on-commit: <short-hash>
   based-on-date: YYYY-MM-DD
   mandate-fit:
     initial-spec: greenfield | brownfield | both | n/a
     refactor: greenfield | brownfield | both | n/a
     mvp: greenfield | brownfield | both | n/a
     post-mvp-evolution: greenfield | brownfield | both | n/a
     regression-fix: greenfield | brownfield | both | n/a
   ---
   ```
   The 5-class taxonomy is illustrative; the synthesis may produce a different cut. If so, the YAML schema updates accordingly.
8. **Comparison document with a first-class mandate-fit matrix** (per D2): rows = architectures; columns = work-unit-classes; cells = mandate-fit value. Headline view honors the user's original ask (top-level greenfield/brownfield organization); the matrix body exposes the work-unit-class dimension. **This is the single most user-facing artifact** of v3 — it must be defensible at the matrix-cell level. → `00-comparison-v3.md`.
9. **Back-fill audit** documenting what survived from archived v1/v2 material and why (Phase 7 output). → `backfill-notes.md`.
10. **Lean-evaluation briefs** per architecture (1-day manual run designs; Phase 8). → `lean-evals/<arch>.md` × N.

---

## 7. Out of scope — restated as questions, not exclusions (per Skeptic #11, #12)

The following are *not closed by this brief* but are not actively addressed in v3. Several were previously framed as scope exclusions; per the bias-guard pass, several have been promoted to open questions because they smuggle architectural commitments when framed as exclusions:

- **Specific provider selection** is deferred to operator time, but **architectures may declare provider-property requirements** (diversity, long-context, vision, tool-calling latency). The RouterLLM-equivalent abstraction is itself open for challenge (per Skeptic #11). → OQ-B8.
- **Methodology evolution** as a per-architecture concern vs. a shared-substrate primitive (per Skeptic #12). → OQ-B9.
- **Specific cloud / CI vendor.** GitHub Actions is the current operating environment ([`PLAN`](../../research/PLAN.md) §8); architectures should not assume it.
- **Multi-codebase coordination** (one factory operating across multiple codebases). Single-codebase per factory instance is the v3 scope; multi-codebase is future work.
- **Production observability beyond trajectory-capture + decision-log primitives.**

---

## 8. Open questions surfaced *by this brief* (deliberate)

The brief itself raises questions it does not resolve. These are flagged for explicit Phase-2/3 treatment so they cannot be silently smoothed.

- **OQ-B1.** How is the lights-out / L5 / regime tension (§2.1) resolved at the architecture level? Per glossary §0, this requires first testing the lights-out↔L5 vocabulary mapping. Mandatory treatment in every Phase-2 track.
- **OQ-B2.** Where does the greenfield/brownfield boundary fall — at the methodology layer, the substrate layer, or both? Mandatory treatment in Phase 4.
- **OQ-B3.** **(Reframed per Skeptic #8.)** What is the human re-entry mechanism — what conditions cause a human to enter the inner loop, who decides, and what is the substrate-level protocol for handing back? (The old binary "no human ever vs. no human in inner loop" is preempted by the lights-out definition in glossary §0.)
- **OQ-B4.** For brownfield: is the unit of work an *issue* (Atelier-style; see glossary §0), a *change request against a spec* (Refinery-style; see glossary §0), or a *codebase-evolution proposal* (a shape not in the v2 architecture set)? Mandatory treatment in Phase-2 brownfield tracks.
- **OQ-B5.** *(Promoted to §5 per Historian M4.)*
- **OQ-B6.** **(New per Skeptic #10.)** Which empirical bars should the lights-out architectures be required to clear, and from which source(s)? Jaymin's thresholds are one candidate; others may exist in the corpus or be defensibly proposed.
- **OQ-B7.** **(New per Skeptic #1, partially resolved by D1.)** Beyond mandate, what organizing axes (regime, stakes, synchronicity, work-unit-class, codebase-lifecycle stage) deserve architectural-level treatment? The 3 both-mandates tracks (D1) have explicit authorization to surface alternative axes.
- **OQ-B8.** **(New per Skeptic #11.)** Provider-property requirements: which provider properties (diversity, long-context, vision, tool-calling latency) must architectures declare? Is the RouterLLM-equivalent abstraction the right level?
- **OQ-B9.** **(New per Skeptic #12.)** Is methodology evolution a per-architecture concern or a shared-substrate primitive?
- **OQ-B10.** **(New per Skeptic #15.)** The archive-and-rebuild discipline (UC6) prioritizes anchor-avoidance over insight-preservation. The Phase-7 back-fill audit is the asymmetric mitigation, but is itself subject to recency bias. Lead agent should be especially generous toward archive items in Phase 7. *Not for Phase-2 resolution; a process discipline reminder.*

---

## 9. Operating discipline for the v3 process

- **Accuracy ≫ speed ≫ tokens** (UC5). Default to more bias guards, more personas, more checkpoints.
- **Archive-and-rebuild over edit-in-place** for the existing 4 architectures and 2 syntheses (UC6). Phase 7 is the controlled re-introduction.
- **Persona-diverse subagent review at every phase**, not just adversarial ([`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) §3).
- **Cross-session resumption** is a first-class concern: every artifact committed and pushed; checkpoints documented in the plan.
- **YAML frontmatter on every v3 artifact** per ADR-0004 (`based-on-commit` + `based-on-date`). Subagents must include this header.
- **Concrete-task discipline** per ADR-0005: TBD / DECISIONS-PENDING items must each name an explicit next action (who does what to which file).
- **Three-layer pipeline citation discipline** per ADR-0002: architecture specs cite synthesis (not raw reports); ADRs cite neither.
- **`UC`-prefixed user constraints, `D`-prefixed user decisions, `C`-prefixed Round-2 consensus tags**: namespace collision avoided.

---

## 10. Phase map (for orientation)

The v3 work follows the 8-phase plan in [`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md). One-line summary per phase:

- **Phase 0** — Brief + archival. Build this brief; archive v1/v2 architectures + syntheses.
- **Phase 1** — Pre-synthesis substrate (parallel × 3): contradictions register + failure-mode catalog + corpus inventory.
- **Phase 2** — **9-track synthesis fanout** (parallel × 9 per D1): 3 greenfield + 3 brownfield + 3 both-mandates (`no-axis-prescribed`).
- **Phase 3** — Merge + adversarial. 3 mandate-syntheses produced (greenfield, brownfield, unified); each undergoes a multi-persona adversarial pass.
- **Phase 4** — Shared/divergent extraction. Where do mandates genuinely share substrate; where do they diverge.
- **Phase 5** — ADRs (parallel × ~14). Shared-substrate ADRs in wave 1; mandate-specific ADRs in wave 2.
- **Phase 6** — Architecture specs from first principles. Count emergent. Per-(architecture × work-unit-class) mandate-fit matrix.
- **Phase 7** — Back-fill audit. Compare v3 set to archived v1/v2; mark each archive item `absorbed` / `rejected (reason)` / `TBD`.
- **Phase 8** — Lean-evaluation briefs per architecture (1-day manual run designs).

---

*End of 00-brief-v3.md (post-bias-guard revision).*
