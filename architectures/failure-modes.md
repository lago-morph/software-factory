# Failure modes — canonical index

**Status:** Canonical project-wide index of failure modes.
**Seed source:** [`architectures/00-comparison.md` §2.4 at commit `8530bee`](https://github.com/lago-morph/software-factory/blob/8530bee96eaf8b7ac892c973c3b9c7a159299765/architectures/00-comparison.md#L79-L113) — extracted verbatim 2026-05-21 per issue [#111](https://github.com/lago-morph/software-factory/issues/111). The permalink pins the pre-extraction state of the comparison doc; the live file (which changes a lot) is at [`00-comparison.md`](00-comparison.md).
**Convention:** Every new failure mode discovered in research reports, retrospectives, or architecture work is registered here. See [`.claude/skills/research-pipeline/resources/_drain/stage-5-content-processing.md`](../.claude/skills/research-pipeline/resources/_drain/stage-5-content-processing.md) for the registration, renumbering, and propagation procedure.

Failure-mode *definitions* (what F1–F20 mean) live in [`research/synthesis/00-synthesis.md`](../research/synthesis/00-synthesis.md) §4; later additions (F21–F49+) are scattered across reports (see [`research/INDEX.md`](../research/INDEX.md) "Looking for a failure mode" entry). The matrix below is per-architecture *coverage* for F1–F20 — extend it as new failure modes are promoted.

---

## Schema and update discipline

The §2.4 coverage table is the **only** structural surface in this file and follows a strict schema:

- **Header row:** `| Failure mode | N: ShortName | ... |` with one `N: ShortName` column per architecture alternative file `architectures/0N-*.md` (00-comparison.md and this file excluded). Column ordering is by integer N ascending; the `ShortName` is the slug used in the comparison doc (Refinery, Atelier, Foundry, Tournament).
- **Body rows:** `| F<K> <Name> | <cell> | <cell> | ... |` with exactly one cell per architecture column. Row identifier `F<K>` must be unique and is the same number used by the proposing research report (registration procedure in [`stage-5-content-processing.md`](../.claude/skills/research-pipeline/resources/_drain/stage-5-content-processing.md)).
- **End marker:** the §2.4 table ends at the `**Coverage column scores ...**` heading. The summary tables that follow are NOT validated cell-by-cell.

**Update rule (enforced by CI):** when you modify `architectures/0N-*.md`, you must also update **column N — and only column N** — of this table. When you add a new alternative `architectures/0M-*.md`, add a new column `M: ShortName`; when you remove one, drop its column. The [`failure-modes-gate.yml`](../.github/workflows/failure-modes-gate.yml) workflow runs [`.github/scripts/lint-failure-modes.py`](../.github/scripts/lint-failure-modes.py) on every PR that touches `architectures/**` and hard-fails on:

1. An `architectures/0N-*.md` change with no matching column-N update.
2. A column-N change with no matching `architectures/0N-*.md` edit (spillover).
3. Structural drift — header count ≠ alternative count, row width mismatch, etc.

The escape hatch is the PR label **`failure-mode-only`** — apply it when you are deliberately refining a cell's wording with no architecture-doc change. The gate then permits column edits without a corresponding arch-file edit. (It still blocks spillover when an arch file *is* edited — the label is for column-only PRs, not column-plus-spillover ones.)

Run the linter locally before pushing:

```bash
python3 .github/scripts/lint-failure-modes.py                       # structure-only
python3 .github/scripts/lint-failure-modes.py --check-diff origin/main  # full
```

---

### 2.4 Failure mode coverage

| Failure mode | 1: Refinery | 2: Atelier | 3: Foundry | 4: Tournament |
|---|---|---|---|---|
| F1 Hallucination Loop | Independent judge | Persona diversity | Independent V&V | **Diversity policy (structural)** |
| F2 Reward hacking | Holdout scenarios + pattern detector | Adversarial reviewer | Acceptance V&V holdout | **Predator agent + holdout** |
| F3 Spec-completeness | Layered spec; pending buffer | Gap lenses + spec-flow | SRS rigor + risk register | Under-specification + exploration |
| F4 Code quality | Optional reviewer panel | **Reviewer panel (strongest)** | Cleanroom discipline | Simplicity component in fitness |
| F5 Cognitive ceiling | Manager loop | 5-state queue | Gate review tempo | Per-generation summaries |
| F6 Cognitive debt | Walkthroughs + decision logs | Workpad + plan readability | SAD/DD readable artifacts | Trajectory walkthrough on gallery |
| F7 Normalization of deviance | Surprise rate per layer | Refresh-curator review | Defect-of-origin trends | Predator continuous pressure |
| F8 Stale knowledge | Curator + discoverability | **Refresh skill (strongest)** | RTM regenerated per cycle | Genome curation cadence |
| F9 Spec overfitting | Classify-before-amend; pending buffer | WHAT-not-HOW; anti-pattern named | Phase order; expensive amendments | Under-specified seed; diversity selection |
| F10 Findings disappear | Pending buffer | **Residual work gate (strongest)** | Defect database | Generation summary log |
| F11 Renumbering | Stable-ID rule | Stable-ID rule | **RTM as spine (strongest)** | Stable IDs across generations |
| F12 Lethal trifecta | Sandbox | Worktree + sandbox | Sandbox + Phase-2 security review | Per-candidate sandbox + security judge |
| F13 Missing-config | Layer 4 + Spec Analyst | Reliability-reviewer + adversarial doc | NFR-N + IR-N requirements | Predator probes config |
| F14 Attribution collapse | Decision log | Stable IDs + commit refs | **Phase-of-origin (strongest)** | Lineage tracker |
| F15 Single-prompt collapse | Probe brief constraints | **Six divergent frames (strongest)** | Multiple stances per phase | **Diversity policy ≥4 scaffolds (strongest)** |
| F16 Resume-fidelity | Trajectory checkpoints | Workpad survives | Phase checkpoints | Per-candidate isolation |
| F17 Parallel agents on shared dirs | Worktree per cycle | **Worktree per issue (strongest)** | Worktree per U-ID | **Worktree per candidate (strongest)** |
| F18 Prose-spec rigor | Given/When/Then ACs | AE-IDs concrete | **Formal templates (strongest)** | **Empirical: scenarios as contract (strongest)** |
| F19 Model-floor dependency | Surfaced explicitly | Per-stack reviewer prompts | Different provider per phase | **Tested across families (strongest)** |
| F20 Maintenance asymmetry | Same loop applies | Pulse reports | Same six phases | Bug-shaped genomes; production scenarios feed predator |

**Coverage column scores (subjective; ★ = stronger):**

| Architecture | Coverage strength |
|---|---|
| 1 — Specification Refinery | ★★★★ — strong on F3, F9, F7; medium on F4, F18 |
| 2 — Compound Atelier | ★★★★★ — strongest on F4, F8, F10, F11, F15, F17 |
| 3 — Phase-Gated Foundry | ★★★★ — strongest on F11, F14, F18; medium on F5 (gate calendar burden) |
| 4 — Evolutionary Tournament | ★★★★ — strongest on F1, F15, F17, F19; weakest on F18 (replaces rigor with empiricism) |

No architecture covers all 20 failure modes equally. The differences are signal — they show what each architecture optimizes for.
