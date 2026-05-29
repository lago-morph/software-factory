# Spec: `principle-component-decomposition`

- **ID**: SKILL-SPEC-52ebe6353b
- **Source retrospective**: ../2026-05-29-211.md

## Intent

When documenting an architecture against a set of principles, break each principle into its discrete components (the specific things that have to exist to implement the principle), then for each component identify the best few OSS sources, note licenses, and describe placement in the chosen substrate. Forces engineering specificity: "we implement principle X" becomes "we implement principle X via these N components, using these specific OSS projects with these licenses". Surfaces gaps where no good OSS exists.

## Trigger

**Direct triggers**:
- "Map our principles to components."
- "What does it take to implement principle X?"
- "What OSS gives us principle Y?"
- Slash-command: `/decompose-principle <principle-id>`.

**Proactive triggers**:
- A principle-based architecture is being documented (e.g., v4 against the 12 principles).
- A "we'll implement these N principles" claim is being made without concrete component-level grounding.
- An architecture review is asking "what specifically gets us each principle?"

**Negative triggers**:
- The architecture isn't principle-based.
- The principles are too abstract to decompose into discrete components (e.g., values statements).

## Inputs

- The principle (one at a time, or a set).
- The chosen substrate (what we're building on, e.g., Gas City + Claude Code + CXDB).
- The target use case if it constrains OSS choices (license posture, deployment shape).

## Outputs

For each principle, a table with columns:

| Component | What it does | OSS choice(s) | License | Placement in substrate |
|---|---|---|---|---|

Plus a short summary paragraph: "Substrate handles A, B, C natively. New work for D, E. Per-component effort is small/medium/major."

## Workflow

1. **State the principle in its operative form.** Not "specs are good" but "specs are the source of truth; when something breaks, fix the spec and rebuild."
2. **Enumerate components.** Ask: what discrete things have to exist for this principle to be operative? Examples for "specs as source of truth": spec format, spec storage, spec versioning, spec rendering, spec validation, spec → execution binding.
3. **For each component, identify OSS sources.** Use 1-3 candidates per slot. Note license per candidate.
4. **For each OSS choice, note placement.** Where in the substrate does this live? "Native via Gas City prompt templates" / "Custom pack" / "Standalone Go tool".
5. **Highlight gaps.** If no good OSS exists for a component, say so explicitly. This is the most valuable signal.
6. **Write the table.** Use the canonical 5-column format.
7. **Summarize.** One paragraph naming what's native, what's custom, total effort scope.

## Concrete examples

### Example 1: Principle 11 (Self-healing loop) decomposed for v4

| Component | What it does | OSS choice(s) | License | Placement in substrate |
|---|---|---|---|---|
| Event substrate | Records every action | Gas City event bus + CXDB | MIT / Apache 2.0 | Native + bridge |
| Anomaly detection (numeric) | Detects unusual patterns | PyOD, Anomalib | BSD / Apache 2.0 | Python tool node in Gas City pack |
| Trajectory embedding | Embeds trajectories for clustering | sentence-transformers | Apache 2.0 | Python tool node |
| Trajectory clustering | Groups similar failures | HDBSCAN, scikit-learn | BSD | Python tool node |
| Diagnosis agent | LLM root-cause analysis | Custom Claude Code agent (transfusion: Tracker `Diagnose`/`Audit`/`Doctor`) | TBD verify | Specialized Gas City agent pack |
| Fix-task generation | Diagnosis → bead | Custom | n/a | Native bead writing |
| Durable workflow | Survives crashes / retries | Gas City Orders + Temporal | MIT / Apache 2.0 | Orders native; Temporal optional |
| Loop closure tracking | Did fix actually fix it? | Custom bead chain | n/a | Native bead schema |

Summary: Gas City + CXDB + PyOD + sentence-transformers handle substrate; diagnosis agent is the focused custom work. Tracker's diagnosis APIs are the strongest LLM-pipeline-runner transfusion source for this layer.

### Example 2: Principle 1 (Specs as source of truth) decomposed

| Component | What it does | OSS choice(s) | License | Placement in substrate |
|---|---|---|---|---|
| Spec format | Defines the artifact that drives execution | Gas City prompt templates (Go text/template + Markdown) | MIT | Native — `agents/<name>/prompt.template.md` |
| Spec storage | Version-controlled, attributable | Git + Gas City pack structure | MIT | Native — packs are git-versioned |
| Spec linter (optional) | EARS-style structural rules | Custom (transfusion target: any EARS-rule implementation) | n/a | Gas City pack with deterministic tool node |
| Spec → execution binding | How system knows which spec drives which work | Gas City formulas reference templates by name; sling routes work | MIT | Native |

Summary: P1 is essentially handled by Gas City's prompt-template machinery. Spec linter is a small custom add when EARS-style discipline is desired.

## Anti-patterns

- **Stopping at "we use Gas City for this."** Decompose further. What specifically about Gas City? Which subsystem?
- **One OSS source per component.** Always identify alternatives. The reader needs to see the trade space, not just the pick.
- **Skipping licenses.** License is part of every choice. Don't omit.
- **Forgetting placement.** "Native" / "custom pack" / "standalone tool" tells the engineer what they're actually building.
- **Hiding gaps in vague language.** "Bespoke" usually means "we don't have a good answer". Say so.
- **Decomposing principles that aren't operative.** "Specs are good" is a value, not a principle. Decompose only operative principles.

## Acceptance criteria

1. Every component has all five columns filled.
2. Every OSS choice has a license note.
3. Gaps (no good OSS) are explicitly marked, not hidden.
4. Substrate placement is concrete ("Gas City pack X" not "somewhere in Gas City").
5. The summary paragraph captures what's native vs custom vs major investment.
6. A reader can use the decomposition to estimate engineering effort.

## Files this skill creates / modifies

- The architecture document — adds per-principle decomposition tables in the appropriate section.
- (Optional) a separate `PRINCIPLES.md` file if the decomposition is large enough to warrant its own file.
