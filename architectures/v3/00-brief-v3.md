# Software Factory — v3 Brief

**Status:** Active brief for the v3 architecture synthesis. Supersedes the implicit Round-1 brief (which targeted "general execution environment, solo→small team") and supersedes the [`research-plan.md`](../../research-plan.md) "lights-out greenfield" framing (which now expands to cover brownfield as a co-equal mandate).

**Authoritative on:** what the v3 architecture set must address.
**Not authoritative on:** how it gets addressed. The synthesis (Phases 2–4) and architecture specs (Phase 6) decide that.

**Provenance.** Every load-bearing claim in this brief traces to a user-authored statement catalogued in [`constraints-extracted.md`](constraints-extracted.md). Lead-agent inferences are flagged as such.

---

## 1. What we are building

A **software factory** — an autonomous (lights-out) system that produces working software with minimal continuous human-in-the-loop intervention.

Two mandates, treated as potentially distinct solutions:

- **Greenfield mandate.** The factory produces a new software system from a problem statement / spec, with no pre-existing codebase, no pre-existing scenarios, no pre-existing issue queue.
- **Brownfield mandate.** The factory produces changes to (or evolutions of) an existing codebase, with the codebase itself as a primary input. The existing architecture, dependencies, tests, scenarios, and history constrain what the factory can do.

These two mandates may produce **different architectures**. They may also share a common **substrate** (sandbox, scenario storage, cost ceilings, watchdog, trajectory capture, etc.). The v3 work determines empirically — against the corpus — where the boundary falls.

---

## 2. Operating mode: lights-out (with named tension)

The factory operates **lights-out** — autonomously over extended time horizons, with the human's role moved upstream (spec authorship, scenario curation, regime tuning) and downstream (review of aggregated outputs, regime drift detection), but **not in the per-cycle inner loop**.

### 2.1 The L5-vs-lights-out tension (load-bearing, must be addressed)

The post-Round-12 corpus contains a direct, unresolved contradiction with this operating mode:

- **Jaymin West, *Agentic Engineering* Ch 9 §7** (report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §2c): names **L5 ("dark factory") as an empirical anti-pattern** in 2026. Cites CodeRabbit (1.4× critical-issue rate vs. human-reviewed), Veracode (45% OWASP-vulnerable AI-generated code), METR (developers 19% slower than self-estimated when using agents unattended).
- **Dan Shapiro, *Five Levels* canonical post** (report [`32`](../../research/32-shapiro-completion-chat-agent-claw.md), followup [`01`](../../research/followup/01-shapiro-five-levels.md)): positions himself at **L4 ("I'm here")** — explicit refusal of L5 as personal practice.
- **Jaymin's Augmentation-vs-Automation threshold matrix** (report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5): Automation Mode requires ≥90% K=5 consistency, 5-of-5 prompt-paraphrase robustness, zero medium-or-high safety incidents. These are empirical bars the lights-out mandate must clear, not aspirations.

**This tension cannot be hand-waved.** The v3 synthesis must either:

(a) explain how the lights-out mandate clears Jaymin's empirical bars at a per-cycle level (which threshold metrics are met, by what mechanism), or
(b) explicitly redefine the operating mode (e.g., lights-out *over a defined surface* rather than lights-out *uniformly*), or
(c) declare a regime-classification scheme that names where the factory operates at L4 vs. L5 and which work units flow to which.

The lead agent's working stance: option (c) is the most likely shape, but the choice is open and load-bearing. Flag this for explicit treatment in every Phase-2 track.

---

## 3. Working hypothesis — to test, not assume

**User-stated hypothesis** ([`constraints-extracted.md`](constraints-extracted.md) C4):

> No single architecture works best for both mandates. Greenfield is **spec-malleable** (architecture changes during spec refinement). Brownfield is **code-archaeological + existing-architecture-as-given** (architecture is largely fixed by the existing codebase; the factory analyses what is there and grows it).

**Discipline.** The v3 synthesis treats this as a **falsifiable hypothesis**. The corpus may surprise us:

- A substrate-heavy + thin-methodology design could plausibly work for both with different overlays (Round-2's "substrate is shared; methodology differs" framing leaves room for this).
- A spec-malleable phase could plausibly be applied to brownfield as a wrapper layer (spec the *change*, not the system).
- A code-archaeological phase could plausibly precede greenfield work too (analyze the *problem domain* corpus rather than an existing codebase).

The plan must be able to *find* a both-mandates architecture if it exists, not rule it out structurally. The hypothesis is tested in Phase 3 by a dedicated cross-mandate adversarial pass.

---

## 4. What's invariant (carried over from prior rounds without re-litigation)

The following are well-supported across the corpus and are *background* for v3 — they do not need to be re-derived, but the v3 architectures must respect them:

- **Specs are the durable, version-controlled, human-curated artifact** ([`00-synthesis`](../../research/synthesis/00-synthesis.md) §2.1; report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §3 attributes Sean Grove). True for both mandates, though the *content* and *malleability* of the spec differ.
- **Scenarios live outside the codebase as a holdout set** ([`00-synthesis`](../../research/synthesis/00-synthesis.md) §2.2). Both mandates; brownfield additionally inherits scenarios *from the existing codebase's test suite + production traces*.
- **Agent = Model + Harness** ([`13-round-2-synthesis`](../../research/synthesis/13-round-2-synthesis.md) §1.1 C10). Harness and scaffold are distinct layers (C11). Both mandates.
- **Holdout discipline** (acceptance criteria withheld from builder agents) is substrate-enforced, not methodology-optional ([`13-round-2-synthesis`](../../research/synthesis/13-round-2-synthesis.md) §1.1 C13). Both mandates.
- **Hard cost ceilings are non-optional in CI** ([`13-round-2-synthesis`](../../research/synthesis/13-round-2-synthesis.md) §1.1 C15). Both mandates.
- **Tiered watchdog (Daemon / Triage / Patrol) is a substrate primitive** ([`13-round-2-synthesis`](../../research/synthesis/13-round-2-synthesis.md) §1.1 C14). Both mandates.
- **Trajectory capture is cheap and production-tested** ([`13-round-2-synthesis`](../../research/synthesis/13-round-2-synthesis.md) §1.1 C16; OpenHands V1 sub-ms per-event persist, 7.4ms median crash recovery). Both mandates.

**Lead-agent note.** These items are derived from the Round-1 and Round-2 syntheses that will be archived in Phase 0.4–0.6. They are reproduced here so the v3 synthesis does not have to re-derive them. If the v3 synthesis finds reason to challenge any of them, it is free to do so — the citation is provided for traceability, not lock-in.

---

## 5. Explicit out-of-scope

Out of scope for v3 (per [`constraints-extracted.md`](constraints-extracted.md) and prior project decisions):

- Choosing a specific LLM provider or model. The architectures must work across providers; the harness's `RouterLLM`-equivalent is the right level for that decision.
- Choosing a specific cloud or CI vendor. GitHub Actions is the current operating environment ([`PLAN`](../../research/PLAN.md) §8) but architectures should not assume it.
- Multi-codebase coordination (one factory operating across multiple codebases). Single-codebase per factory instance is the v3 scope; multi-codebase is future work.
- Production observability beyond what's needed to close the trajectory-capture + decision-log primitives.
- Methodology evolution as a separate sub-architecture. Each v3 architecture must include its own methodology-evolution mechanism, but a meta-architecture for evolving the architecture itself is out of scope.

---

## 6. Required outputs from v3

The v3 work produces:

1. A canonical, consolidated **failure-mode catalog** (F1–F49+ resolved including the F36/F37 collision; severity ranked separately for greenfield and brownfield).
2. A canonical **contradictions register** (pairwise, sourced, unresolved at register time).
3. A canonical **corpus inventory** (per-report anchor + mandate-fit tag).
4. **Mandate-specific syntheses** (greenfield + brownfield), each surviving multi-persona adversarial review.
5. A **shared-substrate document** and a **divergence document** (the load-bearing boundary).
6. **ADRs** for every binding decision (~14, split across shared-substrate and mandate-specific).
7. **Architecture specs** (count emergent, not predetermined), each carrying a `mandate-fit` YAML header.
8. A **comparison document** with a first-class **mandate-fit matrix** (greenfield-fit × brownfield-fit × resolution-of-tension-if-both).
9. A **back-fill audit** documenting what survived from archived v1/v2 material and why.
10. **Lean-evaluation briefs** per architecture (1-day manual run designs).

Item 8's matrix is the single most user-facing artifact. It must be defensible at the matrix-cell level.

---

## 7. Operating discipline for the v3 process

- **Accuracy ≫ speed ≫ tokens** ([`constraints-extracted.md`](constraints-extracted.md) C5). Default to more bias guards, more personas, more checkpoints.
- **Archive-and-rebuild over edit-in-place** for the existing 4 architectures and 2 syntheses ([`constraints-extracted.md`](constraints-extracted.md) C6).
- **Persona-diverse subagent review at every phase**, not just adversarial ([`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) §3).
- **Cross-session resumption** is a first-class concern: every artifact committed and pushed; checkpoints documented in the plan.

---

## 8. Open questions surfaced *by this brief* (deliberate)

The brief itself raises questions it does not resolve. These are flagged for explicit Phase-2/3 treatment so they cannot be silently smoothed:

- **OQ-B1.** How is the L5-vs-lights-out tension (§2.1) resolved at the architecture level? Mandatory treatment in every Phase-2 track.
- **OQ-B2.** Where does the greenfield/brownfield boundary fall — at the methodology layer, the substrate layer, or both? Mandatory treatment in Phase 4.
- **OQ-B3.** Does "lights-out" mean *no human ever*, or *no human in the per-cycle inner loop*? The brief currently uses the latter framing (§2). If a Phase-2 track concludes a stricter or looser definition is necessary, flag it.
- **OQ-B4.** For brownfield: is the unit of work an *issue* (Atelier-style), a *change request against a spec* (Refinery-style), or a *codebase-evolution proposal* (a shape not yet in the four-architecture set)? Mandatory treatment in Phase-2 brownfield tracks.
- **OQ-B5.** For greenfield: how does the cold-start problem (no scenarios, no issue queue, no `docs/solutions/`, no prior runs) bootstrap? Mandatory treatment in Phase-2 greenfield cold-start-first track at minimum.
- **OQ-B6.** Does the corpus support a both-mandates architecture (working-hypothesis test from §3)? Resolved in Phase 3 cross-mandate adversarial pass.

---

*End of 00-brief-v3.md.*
