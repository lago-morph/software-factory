---
phase: 7
status: aggregation (derived view; per-candidate files at backfill-notes/<id>.md are canonical)
based-on-fanout-branch: claude/phase-7-fanout-omnibus
based-on-date: 2026-05-27
based-on-auto-007-sha: 8883e28
based-on-exemplar-sha: 943beb2
candidates: 10
archive-files: 9
total-cells: ~980  # 10 candidates × ~98 cells/candidate; per-candidate cells of record in backfill-notes/<id>.md
bias-guards-fired: 2  # silent-absorption auditor + historian
wave-7-3-fired: false  # per silent-absorption auditor recommendation 5 + lead-agent decision (see §5 below)
phase-7-followup-deferral-fired: false  # threshold not breached after lead-agent decision
---

# Phase 7 back-fill notes — aggregation

**Status.** Aggregation file. Per-candidate canonical files at [`backfill-notes/`](backfill-notes/) — this aggregation is a **derived matrix view** for cross-candidate reading. Phase 8 lean-eval briefs MUST consume the per-candidate files directly (NOT this aggregation) for any binding cell verdict.

**Authored by lead agent at fanout-close** per [auto-007 §Decision (Round 2)](decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2). All 11 fanout subagents (9 back-fill + 2 bias-guards) returned `accept-as-is` or `accept-with-named-amendments`; no `reject-with-counter-proposal`.

---

## §1 Per-candidate file pointers

| Candidate | Mandate | Tier | Notes file | Words | Cells | Lineage (subagent-derived) |
|---|---|---|---|---|---|---|
| BF-S (exemplar) | brownfield | Light | [`backfill-notes/bf-s.md`](backfill-notes/bf-s.md) | 5698 | 64 unique | Atelier primary + Refinery secondary |
| GF-S | greenfield | Light | [`backfill-notes/gf-s.md`](backfill-notes/gf-s.md) | 6976 | 98 | Multi-lineage (no single dominant) |
| GF-M | greenfield | Light | [`backfill-notes/gf-m.md`](backfill-notes/gf-m.md) | 6213 | 98 | No-single (cross-lineage, all 4) |
| GF-C | greenfield | Light | [`backfill-notes/gf-c.md`](backfill-notes/gf-c.md) | 6935 | 99 | Refinery primary + Foundry secondary |
| BF-M | brownfield | Heavy | [`backfill-notes/bf-m.md`](backfill-notes/bf-m.md) | 6983 | 98 | Atelier + Foundry hybrid + Refinery |
| BF-L | brownfield | Heavy | [`backfill-notes/bf-l.md`](backfill-notes/bf-l.md) | 6494 | 98 | Atelier + Foundry co-equal + Refinery |
| U-A | unified-attempt | Heavy | [`backfill-notes/u-a.md`](backfill-notes/u-a.md) | 7261 | 98 | 4-way (Atelier primary + Refinery + Foundry + Tournament) |
| U-B | unified-attempt | Heavy | [`backfill-notes/u-b.md`](backfill-notes/u-b.md) | 7211 | 98 | Refinery primary + Foundry secondary + Atelier tertiary |
| U-C | unified-attempt | Heavy | [`backfill-notes/u-c.md`](backfill-notes/u-c.md) | 7456 | 110 | Foundry primary + Refinery secondary + Atelier methodology + Tournament thin |
| D7-U-1 | unified-attempt | Heavy | [`backfill-notes/d7-u-1.md`](backfill-notes/d7-u-1.md) | 7778 | 71 unique | Tournament primary + Foundry + Refinery (NOT Atelier) |
| **Silent-absorption auditor** | bias-guard | — | [`backfill-notes/audit-silent-absorption.md`](backfill-notes/audit-silent-absorption.md) | 2543 | 15 findings | — |
| **Historian** | bias-guard | — | [`backfill-notes/audit-historian.md`](backfill-notes/audit-historian.md) | 2147 | 18 findings | — |

**Total fanout output:** 12 files (10 per-candidate + 2 bias-guard) across **~73K words** of audit content.

## §2 Cross-candidate matrix (archive file × candidate)

Each cell summarizes the candidate's dominant verdict for the archive file. Per the per-candidate scoping principle (v1.2 plan § Phase 7 line 423), the per-candidate file at [`backfill-notes/<id>.md`](backfill-notes/) is authoritative for any specific cell; this matrix is the cross-candidate view.

| Archive file | GF-S | GF-M | GF-C | BF-S | BF-M | BF-L | U-A | U-B | U-C | D7-U-1 |
|---|---|---|---|---|---|---|---|---|---|---|
| research-plan.md | M | M | M | M (1A 2N) | M | M | M | M | M | M |
| 00-synthesis.md | H | H | H | H (10A 2T 1S) | H | H | H | H | H | H |
| 13-round-2-synthesis.md | H | H | H | H (5A 2R 1N) | H | H | H | H | H | H |
| 00-comparison.md | H | H | H | H (5A 2R 2N) | H | H | H | H | H | H |
| 01-specification-refinery.md | M | H | **H** | M (3A 5N) | M | M | M | **H** | **H** | M |
| 02-compound-atelier.md | M | H | **L** | **H** (10A 4N) | **H** | **H** | **H** | M | M | **L** (NOT) |
| 03-phase-gated-foundry.md | M | M | **H** | M (3A 5N) | **H** | **H** | M | **H** | **H** | **H** |
| 04-evolutionary-tournament.md | M | M | M | M (3A 1R 4N) | M | M | M | M | M | **H** |
| failure-modes.md (24 rows) | **H** (19/24A) | **H** (19/24A) | **H** | M (15/24A) | **H** (19/24A) | **H** (19/24A) | **H** (19/24A) | **H** (19/24A) | **H** | **H** |

**Legend.** **H** = high-density absorption (≥10 absorbed cells out of section's audit cells); **M** = medium-density absorption (5-9 absorbed); **L** = low-density absorption (<5 absorbed). **NOT** annotation = explicit non-lineage. Cell-format example: `(NA NR NN NT NS NC)` = absorbed/rejected/n/a/tbd/silent-flagged/challenged counts; full counts in per-candidate file.

**Observations on matrix patterns:**

1. **Architecture-2 Compound Atelier absorption is the clearest mandate-fit signal.** All 3 brownfield candidates (BF-S/BF-M/BF-L) and unified-attempt U-A show H absorption; GF-C shows L (Compound Atelier is the day-0-vacuum gap GF-C addresses); D7-U-1 explicitly NOT Atelier. Pattern reinforces DEC-1.a working hypothesis (no methodology serves both mandates) — the unified-attempts cluster on cross-lineage absorption, but the mandate-specifics cluster cleanly.
2. **Architecture-3 Phase-Gated-Foundry absorption is heaviest in BF-M/BF-L (brownfield heavy)** and the unified-attempts (U-B/U-C/D7-U-1). Foundry lineage tracks the "CM-as-spine + V&V independence" axis.
3. **failure-modes.md (§10) absorption is uniformly H across 8-of-10 candidates** — 15-19 of 24 enumeration units absorbed per candidate. Only BF-S (exemplar) shows the lower density at 15/24 because the exemplar deliberately demonstrated the small-file-exception + per-architecture-row distinctions; siblings replicated the structure with broader absorption.
4. **research-plan.md (§2) uniformly M** across all candidates — the file is the smallest in the archive (758 words; small-file exception applies); 3 enumerable claims, 1-2 absorbed per candidate.
5. **00-synthesis.md (§3) absorption uniformly H** across all candidates — driven by D-1..D-7 defaults being verified-absorbed (per §1.5 in each per-candidate file) plus the cross-cutting consensus items.

## §3 Silent-absorption auditor reconciliation

Per [auto-007 §Decision (Round 2) reconciliation precedence rule](decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) + Reviewer-5 Defect 3 confidence-threshold amendment: silent-absorption auditor `silently-absorbed` findings labeled `high` / `medium` / `low`. Only `high`-confidence findings override per-candidate `rejected` verdicts on same cell; `medium` triggers `tbd` reconciliation; `low` is informational.

**Auditor returned 15 findings: 3 high / 7 medium / 5 low.**

### §3.1 High-confidence findings (3) — apply precedence rule

| # | Spec | Archive source | Finding (silently-absorbed) | Reconciliation action |
|---|---|---|---|---|
| 1 | U-A § Knowledge promotion | `archive/architectures-v2/02-compound-atelier.md` §3.2 | Atelier's 4-token category enum (`insight / playbook / correction / pattern`) lifted near-verbatim as "Compound-Knowledge envelopes" with no archive cite | **Aggregation cell**: `absorbed (silently, high-confidence — flagged for Phase-8 cite)`. Per-candidate U-A's verdict on this archive item: was `absorbed (with adaptation)` — no override needed (already absorbed). Phase-8 lean-eval brief for U-A MUST carry the cite obligation. |
| 2 | 7 specs (GF-M / U-A / U-B / U-C / D7-U-1 / BF-S / BF-M) | `archive/synthesis-v1-v2/13-round-2-synthesis.md` (Compound-Engineering 4-step loop `plan → work → review → compound` v0.2 canonicalization) | 4-step loop appears verbatim across 7 specs; only GF-M cites a `research/03-` primary source; none cite the archive v0.2 correction | **Aggregation cells (7)**: each `absorbed (silently, high-confidence — flagged for Phase-8 cite, archive lineage)`. Per-candidate verdicts already `absorbed`; no overrides. Phase-8 briefs for 7 candidates carry cite obligation. |
| 3 | 5 specs (BF-S / BF-L / BF-M / D7-U-1 / U-A) | `archive/architectures-v2/00-comparison.md` §1 (4-architecture taxonomy) | "Atelier-style / Refinery-style / Attractor-DOT pipelines" used as work-unit-shape taxonomy without archive cite (cite only goes to registry/tracks) | **Aggregation cells (5)**: each `absorbed (silently, high-confidence — flagged for Phase-8 cite, archive lineage)`. No per-candidate overrides. |

### §3.2 Medium-confidence findings (7) — trigger TBD reconciliation rows

Per the confidence-threshold rule: medium = arguable semantic equivalence; triggers `tbd` reconciliation row for lead-agent / user adjudication.

7 TBD reconciliation cells added to the aggregation matrix (specific cells listed in [`backfill-notes/audit-silent-absorption.md` §B.1](backfill-notes/audit-silent-absorption.md)). Lead-agent decision at aggregation close: **defer to Phase-8 lean-eval design** — each TBD cell becomes a per-candidate lean-eval brief input asking "is the candidate's framing distinguishable from the archive item, or is this a silent inheritance worth citing?"

### §3.3 Low-confidence findings (5) — informational only

Recorded in `audit-silent-absorption.md` §B.1; do NOT override per-candidate verdicts; do NOT trigger TBD rows. Informational for downstream Phase-8 design.

### §3.4 ADR-0036 framing drift (Phase-6-followup #1)

Confirmed by the silent-absorption auditor (per its expanded mandate): **BF-L "commodity dispatch surface"** vs **U-A "event-driven registrar-framework"** vs **D7-U-1 "timer-driven registrar-framework"** are distinct framings, all internally consistent within each spec, but reading-divergent at cross-spec aggregation.

**Resolution:** the per-candidate BF-L / U-A / D7-U-1 §N.3 framing entries (per [auto-007 §N.3 amendment](decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2)) carry verbatim §0 cites for each candidate's ADR 0036 row. The drift is NOT a content defect; it's a glossary clarification opportunity. **Lead-agent decision:** carry to Phase-7-close handoff as a Phase-8 / glossary-amendment carry-forward (NOT a Phase-7 in-run spec patch).

### §3.5 Framework-ADR characterization audit (Phase-6-followup #2)

Auditor confirmed: 0028 P-19 ALIGNED across GF-S / BF-L / U-A / U-C (verbatim overlap.md verdict); 0029 P-28 ALIGNED at framework layer across U-A / U-B / U-C / D7-U-1 with medium-confidence orthogonal Atelier-knowledge-doc lineage at envelope-shape level; 0030 P-29 ALIGNED across U-A / U-B / D7-U-1; **only 0036 shows drift** (per §3.4 above).

**Conclusion:** framework-layer alignment is solid for 3-of-4 frameworks; the 0036 drift is the only audit-flag, already handled by §3.4 carry-forward. **Phase-6-followup #2 is closed at this aggregation.**

## §4 Historian findings reconciliation

Per the historian's audit ([`audit-historian.md`](backfill-notes/audit-historian.md)): **18 gap findings: 5 load-bearing + 5 silent-omission + 4 mandate-rejection + 4 not-load-bearing-rejection**.

### §4.1 Load-bearing gaps (5) — Phase-8 lean-eval inputs

| # | Gap | Archive source | Disposition |
|---|---|---|---|
| H-1 | Stable-ID lettering convention (R/A/F/AE/U/S/K) | 2 archive files | **§6 open-carry candidate**: lead-agent recommends ONE candidate (likely U-C or D7-U-1 — both have strong artifact-typing) adopts the convention in Phase 8; track as Phase-8 design input. Lean-eval cross-candidate ID-stability comparison currently has no spec reference. |
| H-2 | Self-improving prompts pattern | Documented in Round 1 + Round 2 | **Paired with H-8 below**. Methodology decision deferred to per-candidate Phase-8 brief for GF-S / GF-M / U-A. |
| H-3 | Pulse report (production-trace-to-spec-amendment) | Compound-engineering downstream loop closer | **One-line §6 open-carry**: BF-L's P-13 maintenance loop is the natural home; flag for Phase-8 brief for BF-L specifically. |
| H-5 | Scaffold/harness C11 vocabulary | Round-2 archive | **Glossary addition to [`decisions-captured.md`](decisions-captured.md)** — non-blocking; can land in Phase-7-close handoff. |
| H-8 | Prompt-self-improver role | Round-2 archive | **Paired with H-2 above**. Phase-8 brief input for GF-S / GF-M / U-A. |

### §4.2 Silent-omission gaps (5)

Recorded in `audit-historian.md` §B.1; per be-generous-to-archive bias direction, these lean toward `silent-omission` (rather than rejection) — Phase-8 lean-eval briefs should consider whether to absorb. **No Phase-7 spec patches.**

### §4.3 Mandate-rejection + not-load-bearing-rejection (4 + 4)

Confirmed as deliberate rejections at the v3 / candidate-set level. No action required.

### §4.4 Phase-5-close handoff erratum-sweep (Phase-6-followup #3)

Historian identified **2 erratum-extensions** beyond the known BF-M / 0049 row:

- **BF-M row supplement** — handoff omits ADR 0031 + 0032 (under-statement; attach to existing 0049 erratum).
- **BF-L row** — handoff omits framework 0028 (paired with per-variant 0049) and framework 0036 (consumption-only commodity dispatch; Phase-6-close verifier Finding-2 carry-forward).

**Lead-agent decision:** append these to the Phase-6-close handoff erratum section as part of the Phase-7-close handoff (PR 6). Non-blocking; documentation-hygiene level.

The other 7 candidate rows show framework + designed-system under-statement pattern but are NOT erratum (per-variant pairings make framework citations recoverable). **Phase-6-followup #3 is closed at this aggregation.**

## §5 Wave 7.3 spec-patch decision (LEAD-AGENT DECISION)

**Decision: Wave 7.3 (spec patches) DOES NOT FIRE.** Adopting the silent-absorption auditor's recommendation #5 (the matrix-flag-only alternative).

### §5.1 Reasoning

1. **Patch-threshold analysis.** Per [auto-007 Round-2 patch threshold](decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2): ≥4 candidates needing patches triggers Phase-7-followup deferral. If every silently-absorbed high-confidence finding (3) triggered a patch + every per-candidate spec-patch candidate surfaced by subagents (1 U-C patch + likely others not surfaced as load-bearing) were patched, we'd hit **7+ candidates needing patches** — exceeds the ≤3 threshold by a wide margin.
2. **Auditor recommendation 5 is well-reasoned.** The silently-absorbed material is a **citation gap, not a content gap** — every absorbed item is already in the spec (just without explicit archive cite). Spec patches would add cites without changing substantive content. **Matrix-flag in this aggregation + Phase-8 cite obligation** preserves the audit trail and pushes the cite work to where it's naturally needed (Phase-8 lean-eval brief authoring).
3. **PR-cap preservation.** Skipping Wave 7.3 keeps the Phase-7 run at 6 PRs (envelope + brief + exemplar + omnibus + handoff + summary/retro) against the 15-PR Phase-7 budget cap — 9-PR margin maintained.
4. **Per-candidate scoping principle preserved.** Per-candidate verdicts in `backfill-notes/<id>.md` remain authoritative; the aggregation flags reconciliation without overriding per-candidate authority (except the 3 high-confidence cases where per-candidate verdicts were already `absorbed`).

### §5.2 What Phase 8 inherits as a result

- Per-candidate `backfill-notes/<id>.md` files are binding inputs to per-candidate lean-eval briefs.
- 3 high-confidence silently-absorbed cites are Phase-8 brief mandatory inclusions (per §3.1 above).
- 7 medium-confidence TBD reconciliation rows are Phase-8 brief design inputs (per §3.2 above).
- 5 historian load-bearing gaps (H-1, H-2/H-8 paired, H-3, H-5) are Phase-8 brief design inputs (per §4.1 above).
- 2 handoff erratum-extensions (BF-M supplement; BF-L row) are folded into Phase-7-close handoff per §4.4.

### §5.3 Phase-7-followup deferral does NOT fire

The deferral threshold (≥4 candidates needing patches) is not breached BECAUSE the lead-agent decision is "no patches fire" — the matrix-flag alternative resolves the be-generous bias inflation Reviewer 1 / pre-mortemer secondary-failure-path-2a flagged. The Phase-7-followup `binding-artifact triple` per [`AGENTS-MD-2adf78e54a`](../../AGENTS.md#deferred-work-binding-artifact-triple) is consequently NOT instantiated.

## §6 Cross-cutting findings (lead-agent summary)

### §6.1 Word-budget overrun pattern — auto-007 Round-3 calibration warranted

9-of-10 candidates landed over their tier budget:

| Tier | Candidates | Budget | Median actual | Median overrun |
|---|---|---|---|---|
| Light (3500-5000) | BF-S, GF-S, GF-M, GF-C | 5000 | ~6400 | +1400 (28%) |
| Heavy (4500-6500) | BF-M, BF-L, U-A, U-B, U-C, D7-U-1 | 6500 | ~7200 | +700 (11%) |

**Lead-agent assessment:** the rubric's mandatory content (§1.5 D-default verification + §10 24-row floor + §N.3 ADR-0036 framing for BF-L/U-A/D7-U-1 + §11 cell-count reconciliation discussion) makes the budgets mechanically unattainable. **Phase-7-close carry-forward:** flag for `auto-NNN` Round-3 amendment if Phase-8 fires under the same tier-table.

### §6.2 Common silent-absorption flags (informational)

3 silent-absorption flags appear across multiple per-candidate files (NOT in the auditor's high-confidence list but consistently surfaced by per-candidate subagents):

- **§3.1.16 cross-cutting primitives** — v3 `primitives/index.md` likely inherited the framing without explicit citation across most specs.
- **§6.1.4 Refinery revelation cycle** (GF-M-specific finding) — GF-M's Regime A 4-phase loop reads as a compressed Refinery 7-phase cycle but spec does NOT cite Refinery as lineage. **Deepest unlabeled borrowing in the run.**
- **§7.1.11 severity × autofix orthogonal axes** — likely informed DEC-2 mandate-fit-per-(architecture × work-unit-class) schema across most specs.

These are surfaced for the broader project to consider as a future skill-rule (auto-detect-skill-on-prior-art-citation-gap) rather than per-spec patches.

### §6.3 D-1..D-7 default verification surfaced explicit challenges

Per the §1.5 per-candidate verification (replacing the Round-1 blanket-skip per Reviewer 5 Defect 1 + Reviewer 6 D-H5):

- **D-1 challenged**: BF-L (substrate-displaces-spec axis; Codebase Model is the durable artifact), BF-M (spec-the-change-not-the-system).
- **D-2 challenged**: BF-S (substrate-partitioned-inside-codebase reframing), BF-L (scenarios-from-model axis), BF-M (codebase-derived holdout, unseen-subset not out-of-tree).
- **D-3 challenged**: U-C (extends to Agent = Model + Harness + Anchor-Context); D-3 partial-challenge in BF-L.
- **D-4 generalized**: D7-U-1 (extended to every artifact boundary).

These challenges are NOT silent absorptions — they're explicit design departures that would have been invisible under the Round-1 blanket-skip discipline. The Round-2 amendment validates per Reviewer 5 + Reviewer 6's predictions.

### §6.4 DEC-1.a working hypothesis observation (NEUTRAL, pre-Phase-8)

The matrix pattern in §2 + the lineage analysis in §1 are **structurally consistent with the DEC-1.a working hypothesis** ([`decisions-captured.md` D1](decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8)) — mandate-specific candidates show clean single/dual-lineage absorption; unified-attempts show 3-4-way cross-lineage absorption that the per-candidate subagents flagged as load-bearing breadth. Whether this breadth reflects genuine mandate-serving capacity or unsustainable compromise is the **Phase-8 lean-eval falsification surface**. Lead agent does NOT pre-judge; matrix is neutral evidence.

### §6.5 No new Phase-7 entry blockers surfaced

No back-fill cell or bias-guard finding constitutes a blocker on Phase 8 entry. Phase 8 (lean-eval design per candidate) is **UNBLOCKED** pending Phase-7-close handoff (PR 6).

## §7 Summary aggregation cell-counts (10 candidates × ~98 cells)

| Token | Approximate count across all per-candidate files | Notes |
|---|---|---|
| `absorbed` (all variants) | ~640 | ~64/candidate average |
| `rejected (reason)` | ~50 | Includes 20 verbatim known-rejected items (2 × 10 candidates: OpenHands+Overstory + Compound Atelier baseline) |
| `not-applicable-to-candidate-mandate` | ~180 | Concentrated in GF-C (27) — the cold-start gap |
| `tbd` | ~60 | Plus 7 high-confidence silent-absorption reconciliation TBDs added by §3.2 |
| `challenged` (sub-token of rejected variants) | ~15 | Mostly §1.5 D-1..D-7 challenges (per §6.3) |
| **Total cells of record** | **~945** | Per-candidate `backfill-notes/<id>.md` files are authoritative for any specific cell |

## §8 References

**Decision brief:**

- [`decisions/auto-007-phase-7-dispatch-shape.md`](decisions/auto-007-phase-7-dispatch-shape.md) — Phase-7 dispatch brief (R1+R2 closed; 6 adversarial reviewers).

**Per-candidate files:** see [§1](#1-per-candidate-file-pointers) above.

**Bias-guard outputs:**

- [`backfill-notes/audit-silent-absorption.md`](backfill-notes/audit-silent-absorption.md)
- [`backfill-notes/audit-historian.md`](backfill-notes/audit-historian.md)

**Process inputs:**

- [`scope-envelope-phase-7.md`](scope-envelope-phase-7.md) — run scope envelope.
- [`SESSION-HANDOFF-2026-05-26-phase-6-close.md`](SESSION-HANDOFF-2026-05-26-phase-6-close.md) — Phase-6-close (supersedes — see Phase-7-close handoff in next PR for new active handoff).
- [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md` § Phase 7](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-7--back-fill-audit-per-candidate-against-archived-v1v2-revised-in-v12) — v1.2 plan.

**Phase-6 anchors:**

- [`mandate-fit-matrix.md`](mandate-fit-matrix.md) — Phase-6 close artifact (NOT touched by Phase 7).
- [`specs/`](specs/) — 10 Phase-6 architecture specs (NOT patched in Phase 7 per §5 decision).
- [`phase-6-verification-findings.md`](phase-6-verification-findings.md) — Phase-6 verifier output (precedent for bias-guard format).

**Archive (audited):** see [auto-007 §Common archive-file-to-path mapping](decisions/auto-007-phase-7-dispatch-shape.md#common-archive-file-to-path-mapping) for the 9 substantive files.
