# C14 — Formula↔DOT Translator + Visualizer  (Build Plan, canonical track)

> Source / Spec ref: [`spec/C14-formula-dot-translator.md`](../spec/C14-formula-dot-translator.md)

C14 is an **interface/translator** component (no runtime engine of its own — execution is C01 over C12).
"Building" C14 means **fixing the formula↔DOT mapping + DOT profile**, then **proving round-trip fidelity
(G24)** as a CI-enforced property, on top of **off-the-shelf DOT writer/parser + graphviz** (no reinvented
DOT grammar, no second exporter where `gc` is native). The plan is therefore mapping-first and
fidelity-gate-first — small in code (README:135 "~few hundred LOC"), heavy in conformance.

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** Probe `gc` export | Determine whether `gc formula export <name> --format dot` is native (README:385) and capture its observable DOT output. Decides wrap-vs-emit for the export direction (OQ-1). | S | C12 spec; `gc` runnable (G11) |
| **T2** Freeze formula↔DOT mapping table | Concrete encoding of C12 nodes/edges/kinds/bindings/params → DOT (and back). Node kinds are **C12's** `{agent,tool,gate,sub_formula}` (D-7) — reference, never redefine. | M | T1, C12 schema |
| **T3** Define the C14 DOT profile | The restricted DOT subset `import` accepts; pin it against Attractor/Mammoth-shaped DOT (README:301; one-shot `*.dot` exemplars). | M | T2 |
| **T4** Define canonical form | The normalization (node/edge ordering, attribute canonicalization, presentation-noise stripping) that makes `import(export(f)) = f` decidable. | M | T2 |
| **T5** Build `export` | formula → DOT, wrapping native `gc --format dot` where present (T1) else emitting via an off-the-shelf DOT writer. Style nodes by kind for graphviz. | S | T2, T4 |
| **T6** Build `import` | DOT(profile) → C12 formula via off-the-shelf DOT parser; reject out-of-profile constructs by name. | M | T3, T4 |
| **T7** Build the exclusion catalog | Enumerate every DOT construct with no formula equivalent → *lowered-by-rule* or *rejected*. Includes the **loop primitive** entry (OQ-2). | M | T3, T6 |
| **T8** **Round-trip fidelity gate (G24)** | Property-based generator of valid C12 formulas + corpus formulas; CI check `import(export(f)) ≟ f` under canonical form; mismatch fails build with a diff. **The load-bearing deliverable.** | L | T4, T5, T6 |
| **T9** Ship as a C02 pack | Wrap export/import as `[[tool]]` subprocess tool nodes; manifest + reference invocation; lock to a C12 `schema_version`. | S | T5, T6, C02 ABI |
| **T10** C15 hand-off contract | Confirm the emitted DOT parses in the Mammoth-derived linter (C15) and its findings map to real formula properties. **Freeze the C14→C15 DOT-surface contract**: node ids, edges, node-kind tag, **and the loop/back-edge marker** (so C15 §3.3 rule 1 can tell a sanctioned bounded loop from a raw cycle — C15 §9 OQ-2). The loop-marker's concrete encoding is gated on C12:OQ-2; T10 freezes the *contract shape*, not the encoding. | S | T5, C15 spec |

## 2. Dependency graph

```
C12 (formula schema) ─┬─► T1 (gc probe) ─► T2 (mapping) ─┬─► T4 (canonical form) ─┐
        (G11 gc run) ─┘                                  ├─► T3 (DOT profile) ─► T6 (import) ─┐
                                                         └─► T5 (export) ───────────────────┤
                                                                                            ├─► T8 (G24 gate) ★
                                              T7 (exclusion catalog) ◄── T3,T6 ──────────────┘
                          T9 (C02 pack) ◄── T5,T6 ;  T10 (C15 contract) ◄── T5 + C15 spec
```

- **Critical path:** `C12 + gc(G11) → T2 mapping → T4 canonical form → {T5 export, T6 import} → T8 fidelity
  gate`. **T8 is the longest pole and the reason C14 exists** (G24); everything else is plumbing around it.
- **Upstream gates:** C14 cannot freeze its mapping until **C12's formula schema is fixed**, and cannot
  settle the export direction until **`gc` is runnable (G11)** to answer OQ-1. The **loop primitive
  (C12:OQ-2)** is a soft gate on T7/T8 completeness — until C12 freezes iteration, loops are a *rejected*
  catalog entry rather than a round-tripped one.
- **Downstream gated by C14:** **C15** (workflow linter) — its lint value depends on C14's DOT fidelity; and
  human review / graphviz visualization.

## 3. Parallelization

Independent workstreams once T2 (mapping) lands:
- **Stream A (export/visualization):** T1 → T5 → T10. Owns the formula→DOT side + the C15/graphviz feed. Can
  start earliest (T1 is the first probe).
- **Stream B (import/profile):** T3 → T6 → T7. Owns the DOT→formula side + the exclusion catalog — the
  genuinely-custom surface; give it the careful author.
- **Stream C (fidelity):** T4 then **T8**. T4 can be designed in parallel with A/B; T8 converges them and is
  the gate everything funnels into.
- **Stream D (packaging):** T9, independent once T5/T6 exist (pure C02 wrapping).
Streams A and B converge at **T8 (fidelity gate)**; T8 is the single integration point.

## 4. Interfaces-first / contract milestones

Freeze in this order so dependents can build against stubs:
1. **Formula↔DOT mapping table (T2)** — unblocks both directions and tells C15 what DOT shape to expect.
2. **The C14 DOT profile (T3)** — the contract C15 and any DOT-ecosystem producer target; freeze before
   `import` (T6) so the accepted-subset is stable.
3. **Canonical form (T4)** — the equality definition the whole G24 proof rests on; must be frozen before T8.
4. **The exclusion catalog (T7)** — published so consumers know exactly what does *not* round-trip (loops
   until C12:OQ-2; arbitrary edge attrs; ports; clusters; cycles).
The **export direction** is publishable first (it may be near-native via `gc`, README:385); **import +
fidelity** is the trailing, load-bearing work.

## 5. Risks & de-risking order

| Order | Risk | Spike to retire it |
|---|---|---|
| 1 | **G24 — lossless bidirectionality across unequal formats may not hold.** The reason C14 is spec'd. | Stand up T4 (canonical form) + T8 (property-based round-trip gate) **first**, against the corpus formulas, before polishing either direction. If `import(export(f)) ≠ f` somewhere, that's a real finding to fold into the exclusion catalog — *prove it where it holds, bound it where it doesn't* (spec §3.3). |
| 2 | **OQ-1 — is `--format dot` native `gc` or v4-supplied?** Wrong guess → reinventing a native exporter (violates the bar) or binding to a non-existent command (G11). | T1: run `gc formula export --format dot` on the §383 3-step formula; wrap if it works, emit otherwise. Bind to *observable output*, never `gc` internals. |
| 3 | **C12:OQ-2 — loop primitive has no settled DAG/DOT form** ("drives C15/C14"). Breaks the round trip on every iterative formula, and is the **C14→C15 seam contract** (C15 needs a loop marker to lint loops — C15 §9 OQ-2). | **Interim** (C12:OQ-2 unfrozen): loops are a **rejected** catalog entry (fail loud — refuse rather than emit a raw back-edge C15 would mis-flag). **End-state** (C12 lands): loops become a **marked back-edge** (*lowered-by-rule*), re-open T7/T8, freeze the DOT encoding + inverse together so C15's loop-lint is restored. Fail-loud is the temporary blocker, not C14's end-state. T10 freezes the marker's *contract slot* now. |
| 4 | **Expressive-power overflow on import** (arbitrary DOT). | Restrict `import` to the T3 profile from day one; out-of-profile constructs reject by name — never silently coerce (spec §6). |
| 5 | **C12 schema drift** (AI-CONTEXT §3.5, breaking formula-format changes). | T9 locks the mapping to a `schema_version`; an unknown version is rejected, not mistranslated. |

## 6. Definition of done

**Per-component DoD** (ties to spec §8 acceptance criteria):
- **Round-trip identity holds (AC-1/G24):** `import(export(f)) = f` under canonical form for every corpus
  formula and a property-based generator, **CI-enforced**; any mismatch fails the build with a diff. *(The
  load-bearing exit criterion — without it C14 has not done its one job.)*
- Profile DOT round-trips in reverse (AC-2); out-of-profile DOT is **rejected by name**, never coerced
  (AC-3).
- The exclusion catalog classifies every reachable DOT construct *lowered* or *rejected*, with the loop
  primitive listed (AC-4; OQ-2).
- Export is semantically equal to native `gc formula export --format dot` where it exists (AC-5; OQ-1), with
  a contract test guarding `gc`-output drift.
- Emitted DOT parses in the C15 Mammoth-derived linter and findings map to real formula properties (AC-6).
- Node kinds `{agent,tool,gate,sub_formula}` survive the round trip and C14 introduces no kind outside C12's
  set (AC-7; D-7 conformance).

**Per-task DoD:** each task closes when its artifact (probe result / mapping table / profile grammar /
canonical-form def / exporter / importer / exclusion catalog / fidelity gate / pack / C15 contract) is
written, cross-referenced to the spec section it realizes, and — for T2/T3/T4/T5/T6/T7 — exercised by the
passing T8 fidelity gate. The spec's five open questions (§9) are either resolved by the G11/`gc` spike
(OQ-1) and the C12 loop decision (OQ-2) or carried to sweep-2 in `_meta/review-log.md`.
