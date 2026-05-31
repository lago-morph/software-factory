# C09 — Prompt template & spec→execution binding (`prompt-template-binding`)  (Build Plan, Track B)

> Source / Spec ref: [`spec-optimized/C09-prompt-template-binding.md`](../spec-optimized/C09-prompt-template-binding.md)
> Companion faithful plan: none authored at sweep 1; faithful spec at [`spec/C09-prompt-template-binding.md`](../spec/C09-prompt-template-binding.md).

## 1. Work breakdown

| ID | Task | Size | Prereqs |
|---|---|---|---|
| T1 | **Freeze the C09 inbound/outbound contracts** (M1): `spec_id` resolve interface (with C08), `template_ref` shape (with C12, OQ2), typed render-context schema v1 (DELTA-02: `spec`/`bead`/`run`/`actor` roots), binding-record schema (DELTA-03), `prompt.id` emission (DELTA-05, with C28). | M | C08 `spec_id` contract; C12 `NodeBinding`; C05 dispatch hook; C28 correlation keys |
| T2 | **Template artifact + `template_id`**: define `agents/<name>/prompt.template.md` shell shape; content-address the body (`template_id`, reuse C21/C08 hashing); pack-build registration (C03). | S | T1; C03 pack layout; C21 hashing primitive |
| T3 | **Sandboxed render engine** (DELTA-04/INV-5): restricted Go `text/template` FuncMap (pure helpers only; no fs/exec/net/env); `missingkey=error` strict mode (DELTA-05); pack-build-time rejection of non-allowlisted funcs. | M | T1, T2 |
| T4 | **Spec-resolution + bind** (DELTA-01/INV-2/INV-4): resolve `spec_id`→immutable C08 bundle; resolve `template_ref`→template; enforce one-pair binding; fail-loud on zero/multiple/unresolvable. | M | T1; C08 resolvable bundle (stub OK) |
| T5 | **Embed strategy** (DELTA-06): `link`/`inline`/`summarized` selection from `spec.detail_level` + size budget; the `summarized` projection (Goal/Constraints/DoD inlined, full linked). | M | T3, T4; (policy ties to C29, OQ4) |
| T6 | **Binding record** (DELTA-03): mint `binding_id = hash({spec_id, template_id, formula_node_id, agent_role, context_schema_version})`; attach `created_by` (C41); persist append-only on C23/C19. | M | T1, T4; C19/C23/C41 write seams (stubs OK) |
| T7 | **`prompt.id` correlation** (DELTA-05/INV-6): mint + attach `prompt.id`; verify it lands on the trajectory join via C28→C21 (against stub). | S | T1, T3; C28/C21 stub |
| T8 | **Rebuild-loop wiring**: re-render same template against a new `spec_id`; new `binding_id` records the revision step (Principle 1). | S | T3, T4, T6 |
| T9 | **Acceptance fixtures** (AC-1…AC-10): conformant/negative templates, determinism golden, typed-context pos/neg, sandbox pack-build negative, resolution one/zero/two, binding-record + `prompt.id` assertions, methodology-leak cross-check, rebuild fixture, embed-strategy fixture. | M | T2–T8 |

## 2. Dependency graph

**Upstream that must precede C09 (interface-level, stubbable):**
- **C08** — must publish the `spec_id` resolution contract (a resolvable, immutable bundle). C09 can build against a C08 *stub* once the `spec_id`→bundle shape is frozen (M1). **Hard, but parallelizable via stub.**
- **C12** — must publish the `template_ref`/`NodeBinding` reference shape (OQ2). Shared freeze (M1).
- **C05** — the dispatch hook that invokes C09 (resolve→bind→render→emit). C09 supplies the binding; C05 owns routing.
- **C28** — the `prompt.id`/correlation-key contract (consumer of the rendered instruction).
- **C03/C21** — pack layout (template lives in a pack) + content-addressing primitive (`template_id`).
- **C19/C23/C41** — binding-record persistence + attribution (write seams, stubbable).

**Critical path inside C09:** T1 (contract freeze) → T3 (render engine) + T4 (resolve/bind) → T5 (embed) / T6 (binding record) → T9 (fixtures). T1 is the gate; everything else fans out behind it.

**Downstream gated on C09:** C28 (consumes the instruction), C32/C33/C34/C35/C46 (consume the `binding_id` join), C39 (rebuild loop re-renders via C09). None need C09 *complete* — they need its **contracts** (M1), so freeze T1 early.

## 3. Parallelization

After **T1 (contract freeze)** lands, these run as independent workstreams:
- **WS-A (render):** T2 (template artifact) → T3 (sandbox engine) → T7 (`prompt.id`).
- **WS-B (bind):** T4 (resolve/bind) → T6 (binding record) → T8 (rebuild loop).
- **WS-C (embed):** T5 (embed strategy) — depends on T3+T4 but is otherwise self-contained; can be developed against fixtures.
- **WS-D (fixtures):** T9 — fixtures for each AC can be authored in parallel with the engine they test (write the negative-sandbox fixture while T3 is in flight, etc.).

WS-A and WS-B are the two halves of the seam ("becomes an instruction" vs "which spec drives which work") and are genuinely independent post-freeze — assign to two builders.

## 4. Interfaces-first / contract milestones

Freeze these in **M1** so dependents build against stubs in parallel:
1. **`spec_id` resolve contract (with C08).** `resolve(spec_id) → immutable bundle{goal, constraints, dod_ref, out_of_scope, detail_level}`. **C08 owns identity; C09 consumes** (OQ1). One-line integrator ratification required.
2. **`template_ref` shape (with C12).** Recommend `{agent_role, template_name}`, resolved against the pack, `template_id` recorded in the binding (OQ2).
3. **Typed render-context schema v1 (DELTA-02).** Four roots (`spec`/`bead`/`run`/`actor`) + `context_schema_version`; `.bead`/`.run` carry open pack-param sub-maps (OQ3).
4. **Binding-record schema (DELTA-03).** `{binding_id, spec_id, template_id, formula_node_id, agent_role, context_schema_version, run_id, created_by}`.
5. **`prompt.id` emission (with C28).** Mint point + correlation guarantee onto the trajectory.

Freezing 1–5 lets C28, C32–C35, C46, C39 stub C09 immediately.

## 5. Risks & de-risking order

| Risk | De-risk first |
|---|---|
| **C08↔C09 seam ownership (OQ1) churns both specs** | Spike T1.1: a one-page agreed `spec_id` resolve contract ratified with the C08 author + integrator *before* any render code. Highest-leverage uncertainty; cheap to retire. |
| **`template_ref` shape mismatch with C12 (OQ2)** | Joint freeze with C12 in M1; build a round-trip fixture (formula `agent` node → C09 resolves → one template). |
| **Sandbox FuncMap too restrictive / too permissive (DELTA-04)** | Prototype T3 against the Phase-0 worker template (AI-CONTEXT:542) + 2–3 realistic shells; confirm the allowlist covers real needs without fs/exec. Pack-build negative fixture proves rejection. |
| **`embed_strategy` size budget is model-dependent (OQ4)** | Defer the *concrete budget* to sweep 2 (ties to C29 model-floor); ship T5 with the strategy *mechanism* and a placeholder budget so the binding layer is in place. |
| **Real Gas City prompt-template machinery differs (G11)** | Validate the template path/rendering against actual `gc` once available (shared C01/G11 risk); keep C09's render engine swappable behind the contract. |

## 6. Definition of done

**Per-component DoD (ties to spec §8 ACs):**
- Contracts 1–5 frozen + ratified (M1); C08↔C09 ownership (OQ1) settled by integrator. → AC-1, AC-6, AC-7.
- Render is deterministic (AC-2), typed-context strict-missing-key (AC-3), sandboxed with pack-build rejection of non-allowlisted funcs (AC-4). → INV-1/INV-5.
- Binding is unique-at-dispatch with fail-loud zero/multiple (AC-5) and mints a content-addressed `binding_id` persisted on C19/C23 with `created_by` (AC-6). → INV-2/INV-4/DELTA-03.
- Rendered instruction carries a `prompt.id` joinable to the trajectory (AC-7) and contains spec/instruction, never the formula DAG (AC-8). → INV-3/INV-6.
- Rebuild loop: new `spec_id` (same template) → changed instruction + new `binding_id` (AC-9). → Principle 1.
- `embed_strategy` selects `link`/`summarized` for large specs under budget, `inline` for small (AC-10). → DELTA-06/F36.

**Per-task DoD:** each task ships its fixture(s) from T9 green; sandbox + missing-key + binding-uniqueness negatives all fail loud (no silent empty/partial instruction).

**Exit:** C09 renders a real Phase-0 worker template against a resolved-`spec_id` stub, mints a binding record, emits a correlatable instruction, and re-renders on a spec revision — with OQ1 ratified and the C12/C08/C28 contract freezes recorded for sweep 2.
