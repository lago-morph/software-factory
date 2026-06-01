# Sweep-2 dispatch addendum (2026-06-01 spine run)

> Read this **with** [`BUILDER-BRIEF.md`](./BUILDER-BRIEF.md) (persona) or [`ADVERSARY-BRIEF.md`](./ADVERSARY-BRIEF.md) (critic). This addendum sets the **Sweep-2 depth contract** for the 25-component safe-self-build spine. The format exemplar is the [`C20-bead-schema.md`](../spec/C20-bead-schema.md) spec — match its shape.

## The depth bar (Sweep-2 = implementation-ready)

Per [`HANDOFF.md` §0.4](./HANDOFF.md). Every deepened spec MUST add, where the component has the surface for it:

1. **Concrete signatures** — function/method/tool-node signatures with typed params + returns (not prose descriptions of interfaces).
2. **Data schemas** — per-type field tables in the C20 shape: **Field | Type | Req | Semantics | R/W-by** (the R/W-by column names the owning/reading component — the ownership annotation).
3. **API / message / config contracts** — for Gas City + Claude Max, the concrete `city.toml`/`pack.toml`/`.gc/site.toml`/env-var/CLI surface. Config keys quoted exactly.
4. **Sequence / state diagrams** — valid Mermaid. Use `sequenceDiagram` for protocols, `stateDiagram-v2` for lifecycles. Keep them syntactically clean (the orchestrator validates a sample per product with a Mermaid validator before integrate). ≤ ~10 nodes each.
   - **Mermaid syntax — avoid the validated build-breaker:** in `stateDiagram-v2`, a **`;` inside a transition label terminates the statement** and breaks the parse. Do NOT put `;` `/` `--` `:` `()` `=` `#` inside transition labels — reword (use a comma or " then ") or move the detail to adjacent prose. Keep state IDs ASCII-simple; multi-line `note` blocks use `<br/>`. If the Mermaid validator tool is available to you, self-validate each diagram before returning.
5. **Error taxonomy** — an **E-code** table: `E-<ID>-NN | condition | surfaced-as | caller recovery`. IDs are component-scoped (e.g. `E-C30-01`).
6. **Acceptance tests** — an **AC-code** table: `AC-<ID>-NN | given/when/then | verifies`. Each AC that exercises a failure path **cross-references the E-code** it asserts (the E↔AC cross-ref — see C20).

Depth is for surface the component actually has. Don't invent surface to fill a table; a component with no error paths says so.

## Deepen IN PLACE — do not rewrite from scratch

- The component's `spec/<ID>-*.md` **already exists** (Sweep-1, plus any `[D-23 substrate-verified …]` / `[D-30 ADOPTED …]` annotations and inline OQs). **Preserve all of it.** Add Sweep-2 depth into/after the relevant sections; do not delete Sweep-1 prose, annotations, or OQs.
- Resolve the component's **inline OQs** where Sweep-2 depth settles them (mark `RESOLVED (Sweep-2): …` in place, keep the OQ text). Leave genuinely-open OQs open; if Sweep-2 surfaces a *new* cross-component conflict, record it in your receipt for the orchestrator's ledger (do **not** edit `review-log.md` yourself).
- Update `plan-faithful/<ID>-*.md` to match (build sequence, parallelism, interface-first ordering for the new depth).

## Cite binding decisions VERBATIM

When your spec relies on a binding decision (D-1 … D-30, or a D-31+ passed to you in the dispatch), quote the **verbatim** decision text from [`review-log.md`](./review-log.md) (or the dispatch) as a blockquote, not a paraphrase (AGENTS-MD-bf4431be57). Drift across parallel builders on the same decision is silent and only surfaces at aggregation.

## Boundaries (binding — do not relitigate)

- **D-30 prevent-gate is adopted.** Unattended (P2) / self-modification (P3b) require the substrate to **BLOCK**, not merely detect. If your component touches the fence/holdout/rig surface, reflect that prevent is *required* and the enforcement watcher is the sanctioned discharge **whose design is deferred until the empirical D-23 spike** — do **NOT** design the watcher.
- The empirical D-23 spike is **owed** (needs Docker); it does not block your spec. Use the [D-23 substrate harvest](./D-23-substrate-harvest.md) (facts F1–F12, `gascity-prototype@b14c278`) as the substrate ground truth; mark anything still needing a pinned-`gc` run as `[needs G11 verification]`.
- Apply the capability-for-principle bar (HANDOFF §2): new capability tied to a 12-principle → KEEP; hardening the existing stack does the same thing "better" → DROP. When in doubt, DROP.

## Receipt format (≤15 lines, return ONLY this — no doc dump)

```
PATHS: <spec path> ; <plan path>
PURPOSE: <1 line>
DEPTH ADDED: signatures=<n> schema-tables=<n> diagrams=<n type> E-codes=<n> AC-codes=<n> (E↔AC refs=<n>)
D-CITED: <D-NN list cited verbatim>
OQs: resolved=<ids> still-open=<ids>
NEW SEAM/CONFLICT (→ orchestrator ledger): <none | one line per conflict: which other component, what contract drifts>
TOP OPEN QUESTION: <one line>
SELF-CHECK (tool-verified): <paste the one-line outputs from the rubric below>
```

## Self-check rubric — RUN THE TOOL, don't self-attest (AGENTS-MD-e74e4811a2)

Before returning, run and paste the outputs:
- `grep -c "E-<YOURID>-" spec/<ID>-*.md` (≥1 if the component has error paths)
- `grep -c "AC-<YOURID>-" spec/<ID>-*.md` (≥1)
- `grep -cE "stateDiagram-v2|sequenceDiagram" spec/<ID>-*.md` (≥1 if it has protocol/lifecycle surface)
- `grep -c "R/W-by\|R-W-by" spec/<ID>-*.md` (≥1 if it owns/reads data — the ownership column)
- confirm the file still contains its Sweep-1 OQ block and any `[D-30 ADOPTED` / `[D-23 substrate-verified` annotations (deepen-in-place check): `grep -c "OQ-\|D-30 ADOPTED\|D-23 substrate-verified" spec/<ID>-*.md`

Never run git. Never touch another component's files. Write your two files; return the receipt.
