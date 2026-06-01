# C02 — Pack & Tool-Node ABI  (Spec, canonical track)

> Source: README §Part 4 (placement tables, lines ~107–256), §Part 5 ("Specific cautions" line 334; license-strategy table line 288), §Part 6 (Phase 0 lines 359–362; Phase 1 line 389; Phase 2 lines 424–426), §Part 7 (design bets lines 509–518), §Part 8 (line 535). AI-CONTEXT §3.4 (smallest viable install, lines 114–122), §3.5 (migration tail, line 128), §3.6 (extractability), §10.1 / decision tables (lines 439, 465, 476, 502), §13.1 (`pack.toml`/`city.toml` skeletons, lines 524–544), §13.2 (Phase-1 env + service blocks), §13.3 (rig partition + tool-node subprocess sketch, lines 599–608). F-MODE-COVERAGE F44 (per-pack production-scissors), F31 (single-adapter floor), F35/F43 (pack governance/RSI declaration). component-inventory C02 row; gaps G29, G06.
> Inventory ID: C02   Kind: interface   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C02 is the **sole extension surface of the v4 factory**. v4 does not fork Gas City and does not import it
as a Go library; every customization v4 needs is delivered as a **pack** — a distributable bundle of TOML
config + tool-node binaries + prompt templates — and the deterministic steps inside a pack run as
**tool nodes**: subprocess binaries invoked by Gas City over a fixed input/output protocol (AI-CONTEXT
§10.1 decision "Pack-based extension of Gas City; no fork — Yes"; README:334, :509, :518).

C02 owns the two contracts that make that claim true:

1. **The pack bundle contract** — what a distributable pack *is* on disk: its manifest (`pack.toml`), the
   declarations it may carry (`[imports.*]`, `[[tool]]`, hook registrations, prompt templates, formulas),
   and how Gas City imports and composes it into a running `city` (AI-CONTEXT §13.1, README:360).
2. **The subprocess tool-node ABI** — how Gas City hands inputs to a tool-node binary and how the binary
   returns outputs/exit status. This is the seam G29 flags as "the actual seam and is undocumented": a
   pack's tool nodes are Go (or any-language) programs that "must speak Gas City's tool-node protocol,"
   and that protocol is the load-bearing contract C02 must pin (AI-CONTEXT §13.3 sketch; README:389).

**Responsibilities**
- Define the **pack manifest schema** and the rules by which packs are imported and layered (which
  declarations a pack may contribute; how `[imports.core]` and pack-supplied sections compose with
  `city.toml`).
- Define the **tool-node invocation ABI**: the `[[tool]]` declaration shape (`name`, `type = "subprocess"`,
  `command`, `args` with `{placeholder}` substitution, `work_partition`), and the runtime contract for how
  a subprocess receives its inputs (substituted args / env / working dir / stdin) and returns outputs
  (stdout / exit code / written partition files).
- Establish that **no Go import / no fork** is required for any v4 extension, and pin the explicit boundary
  beyond which that stops being true (source-level Gas City modification: new runtime Provider, modified
  reconciler, urgent upstream bug fix — README:334).
- Carry the per-pack **declaration discipline** v4 leans on for failure-mode coverage: production-scissors
  declared per pack (F44), pack derivation-rule / governance hooks (F35), RSI status declared in
  `pack.toml` (F43).

**Explicitly NOT**
- NOT the Gas City substrate itself (C01). C02 is the *interface* onto C01's pack-loader and tool-bead
  machinery; C01 provides the `gc` binary, the reconciler, and the Provider runtime that *invoke* tool
  nodes.
- NOT the tool-node *abstraction* as a workflow concept (C17). C17 is the unified workflow-engine view of
  "a deterministic step / Gas City tool bead"; C02 is the concrete **wire protocol + bundle format** that
  C17's nodes are realized over. C17 depends on C02.
- NOT the config/feature-flag *model* (C03). C03 owns "section presence = capability"; C02 owns the
  bundle/ABI shape. They meet where a pack contributes config sections.
- NOT a Go-library SDK, an FFI, or a plugin-`.so` mechanism. The only sanctioned mechanism is
  **subprocess** tool nodes + TOML + templates (AI-CONTEXT §3.5, README:334).
- NOT the individual packs' contents (the CXDB bridge, Inspect-AI wrapper, anomaly pack, etc.). Those are
  C24/C30/C36… each authored *as* a pack *against* C02's contract.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C01** Gas City substrate | C01 supplies the `gc` pack-loader, tool-bead executor, and Provider runtime that load packs and spawn tool-node subprocesses. C02 is the contract; C01 is the engine. |
| Peer / supplies terms | **C07** vocabulary-glossary | C02 cites C07 for the canonical meaning of `pack`, `tool node`/`tool bead`, `formula`, `city`, `rig` (G06). |
| Downstream (realized over C02) | **C17** tool-node-abstraction | C17's deterministic workflow steps are subprocess tool nodes speaking the C02 ABI. |
| Downstream (every "your work" pack) | **C10, C14, C15, C16, C24, C30, C31, C32, C33, C35, C36–C39, C44, C46–C50** | Each custom component the inventory marks "Gas City pack" / "tool node" is built as a pack against C02. The README placement tables route ~25 components through this surface. |
| Downstream (config seam) | **C03** config-feature-flags | A pack contributes config sections; C03 governs how section presence gates capability. |

C02 is **foundational** (inventory: yes) and lives in **Batch 1**, authored in parallel with the other
load-bearing primitives because almost every later component is "a pack" and must build against this ABI.

## 3. Interfaces / contracts

Sweep 1 — interfaces **named and described**; concrete signatures/schemas deferred to sweep 2.

### 3.1 Pack bundle (inbound: how a pack is authored & imported)

1. **`pack.toml` manifest** — the pack's declaration root. Named contents (described, not yet fully typed):
   - `[imports.<name>]` — pull in another pack (the Phase-0 minimum is exactly `[imports.core]`,
     AI-CONTEXT §13.1). The core import supplies the base agent/bead/runtime vocabulary.
   - `[[tool]]` blocks — tool-node declarations (see 3.2).
   - Hook registrations — Claude Code `PreToolUse`/`PostToolUse` hooks a pack registers (README:212
     "Gas City pack registers hooks").
   - Prompt templates — references to `agents/<name>/prompt.template.md` (Go `text/template` + Markdown,
     AI-CONTEXT §3.2 concept 5).
   - Formulas — TOML DAG templates the pack ships (C12), enabled when `[formulas]` is on.
   - > [FAITHFUL-FILL] **Declaration-discipline fields.** F-MODE-COVERAGE references three per-pack
     declarations that have no schema in the four docs: production-scissors (F44), pack derivation rule
     (F35), and RSI status (F43, "pack-author declares RSI status in pack.toml"). The minimal faithful fill
     is to reserve named manifest keys for them (e.g. `[pack.safety] production_scissors = false`,
     `rsi = "none"`, `[pack.derivation] from = "<exemplar>"`). This is the smallest choice consistent with
     v4 because the F-mode doc already *states* these live in `pack.toml`; C02 only needs to name the keys,
     not design the policy engines (those are C43/C57's concern).

2. **Pack-import / composition contract** — how `gc` merges a pack's declarations with `city.toml`. The
   docs give the layering by example (Phase-0 `[imports.core]` + `city.toml`; Phase-1 adds `[formulas]`,
   `[[service]]` blocks; Phase-2 adds `[[rig]]`, `[[tool]]`). The contract is: **section presence enables
   a capability** (C03), and packs contribute sections additively.
   > [AMBIGUITY: G06/composition] The docs never state precedence when a pack and `city.toml` declare the
   > same section. **Reading A:** `city.toml` (the local workspace) overrides imported packs. **Reading B:**
   > last-import-wins. Pick **Reading A** — it is most consistent with v4's "layered TOML, local config is
   > authoritative" framing (AI-CONTEXT §3.2 concept 4; C03), and with `city.toml` being the per-workspace
   > root in every skeleton. Recorded for sweep-2 confirmation.

### 3.2 Tool-node ABI (the load-bearing seam — G29)

The one concrete shape v4 gives is the `[[tool]]` subprocess sketch (AI-CONTEXT §13.3, lines 601–608):

```toml
[[tool]]
name = "inspect_eval"
type = "subprocess"
command = "inspect"
args = ["eval", "{scenario_path}", "--task", "{task}"]
work_partition = "scenarios"
```

From this, the named ABI elements (faithful elaboration, sweep-1 descriptions):

| Element | Description | Source / fill |
|---|---|---|
| `name` | Logical tool-node identity referenced by formulas/slings. | §13.3 sketch |
| `type = "subprocess"` | The only invocation kind v4 names; the binary is spawned as a child process, **not** linked. | §13.3; README:334 (subprocess, not Go import) |
| `command` | Path/name of the tool-node binary (Go or any language). | §13.3 sketch |
| `args` with `{placeholder}` | Argument vector with `{name}` placeholders substituted from the bead/molecule context (e.g. `{scenario_path}`, `{task}`). | §13.3 sketch |
| `work_partition` | The rig read/write partition the subprocess runs against (ties to C42 isolation). | §13.3 sketch |
| **Input channel** | How the substituted context reaches the binary. | > [FAITHFUL-FILL] |
| **Output channel** | How the binary returns results to Gas City. | > [FAITHFUL-FILL] |
| **Status channel** | Success/failure signal. | > [FAITHFUL-FILL] |

> [AMBIGUITY: G29] **The input/output channel is genuinely undocumented** — G29's exact complaint ("how a
> subprocess tool node receives inputs and returns outputs … is undocumented"). Two faithful readings:
> **Reading A (args + files):** inputs arrive *only* as substituted `args`/env and as files in
> `work_partition`; outputs are files the binary writes back into `work_partition`, status is the process
> **exit code** (0 = success). This is what the §13.3 sketch literally shows (`inspect eval … --task` is a
> pure CLI invocation that reads/writes the partition). **Reading B (stdin/stdout JSON):** a structured
> JSON document on stdin, structured JSON on stdout, exit code as status — the shape the raw-bodies→CXDB
> bridge ("posts to CXDB via HTTP/JSON", README:389) and "small Go tool node reading judge outputs"
> (README:426) imply for richer payloads.
> **Pick Reading A as the canonical floor, with Reading B as the optional structured profile.** Rationale:
> Reading A is the only shape the docs *show*; every cited tool node (Inspect AI CLI, the bridge watching a
> directory, the satisfaction aggregator reading beads) functions under args+partition-files+exit-code, so
> the args/files/exit-code contract is the minimal-consistent ABI. Reading B is then a non-breaking
> superset for tool nodes that need to stream a structured request (deferred to sweep-2 as the "json"
> tool-node profile). This keeps the single mandatory contract small (G29) while not contradicting the
> HTTP/JSON-shaped bridge.
> **Cross-track note:** the optimized track (C02-B DELTA-01/03) makes the structured stdin/stdout-JSON
> envelope the *primary* path and demotes argv/`{placeholder}` to a compat shim — i.e. it promotes this
> doc's optional Reading B to its floor. The divergence is deliberate; a reader diffing the canonical spec
> against the frozen `spec-optimized/` reference should expect opposite primary I/O channels by design.

3. **Tool-node invariants** (sweep-1 statements):
   - A tool node is **deterministic-first**: it is the surface for steps that "don't need a model"
     (README:154); LLM nodes are a different node kind owned by C28, not C02. The formula node-kind set
     `{agent, tool, gate, sub_formula}` is **named by C12** (taxonomy home, **D-7**); C02 references C12's
     `tool` kind here for the tool-node ABI but does **not** redefine the set.
   - A tool node is **language-agnostic** at the ABI: Go, Python ("Python tool node", README:253–255), or
     any binary that honors the subprocess contract. The "no Go import" rule (README:334) is about *Gas
     City as a library*, not about the tool node's own language.
   - A tool node is **side-effecting only within its `work_partition`** (rig isolation, §13.3 + C42).
   - Invocation is **stateless per call** > [FAITHFUL-FILL]: nothing in v4 describes a persistent tool-node
     daemon, and `type="subprocess"` implies spawn-per-step; minimal-consistent assumption is one process
     per node execution. (A long-lived "service" is the separate `[[service]]` block, §13.2, not a tool
     node.) **Caveat:** the tool-node↔`[[service]]` boundary for the C24 directory-watch bridge and the
     C44 twin is undrawn in the corpus (the optimized tracks raise this as C02-B OQ4 / C17 OQ4). The
     faithful reading holds spawn-per-step as the *only* shape v4 shows, but C24/C44-shaped long-lived
     work may belong on the `[[service]]` side, not under this invariant — see OQ5.

### 3.3 Outbound: what C02 guarantees to dependents

- To **C17**: a stable "declare a deterministic step as a `[[tool]]` subprocess" contract so the workflow
  engine can place tool beads without knowing the binary's language.
- To **every pack-built component**: a frozen bundle layout so a pack authored in Phase 1 still loads in
  Phase 3 (subject to AI-CONTEXT §3.5's warning of 1–2 breaking pack-schema changes/quarter — C02 must
  version the manifest; see 7).

## 4. Data model / state

C02 is an **interface/contract**, not a data store; it owns *format definitions*, not live state.

- **Pack-on-disk layout** (named, sweep-1): a pack directory containing `pack.toml` (manifest),
  `agents/<name>/prompt.template.md` (templates), tool-node binaries (referenced by `command`), and
  optionally formula TOML files. > [FAITHFUL-FILL] exact directory tree (`packs/<name>/…`) inferred from
  AI-CONTEXT §16 line 697 "`packs/*/spec.md`" and README:360; minimal-consistent because the docs only
  ever show `pack.toml` + templates + binaries as the contents.
- **Manifest schema version** — C02 must carry a version field so the §3.5 quarterly breaking changes are
  detectable. > [FAITHFUL-FILL]: not named in v4; smallest fill is a single `schema_version` key in
  `pack.toml`, because §3.5 explicitly predicts breaking pack-schema changes and gives no other way to
  guard them.
- C02 holds **no runtime state**: the molecule/bead state a tool node reads/writes belongs to C13/C19;
  the partition files belong to C42's rigs.

## 5. Behavior

Key flow (sweep-1 narrative; sequence diagram deferred to sweep-2):

1. Operator authors a pack: writes `pack.toml`, drops tool-node binaries + prompt templates.
2. `gc` **imports** the pack (`[imports.core]` etc.), merging its declarations into the running `city`
   under the composition rule (3.1.2; local `city.toml` authoritative).
3. A formula/sling reaches a deterministic step bound to a `[[tool]]` node.
4. Gas City **substitutes** `{placeholders}` in `args` from bead/molecule context, then **spawns** the
   `command` as a subprocess in the declared `work_partition`.
5. The subprocess does its work against partition files (and, in the optional JSON profile, stdin), then
   **returns** outputs (partition files / stdout) and a **status** (exit code).
6. Gas City records the step's actor/result (C41 `created_by`, C23 event bus) and the reconciler advances.

The Phase-progression behavior the docs assert: Phase 0 install needs **zero custom code** — only
`[imports.core]` + `city.toml` + one template (README:359–362) — and *every* later capability arrives by
*adding packs*, never by forking. C02 is the invariant that makes "no fork" true across all four phases.

## 6. Failure modes & handling

| F-mode | Relevance to C02 | Handling (faithful) |
|---|---|---|
| **F31** Substrate safety floor = weakest adapter | C02 keeps the extension surface to one mechanism (subprocess packs over one substrate). | The single-adapter / single-mechanism choice *is* the mitigation (F-MODE §73: "Addressed by single-adapter choice"). C02 forbids alternate plugin mechanisms that would reintroduce a weaker floor. |
| **F44** Lethal-trifecta production-scissors | A pack's tool node may touch Bash/network/fs. | Per-pack declaration: "production scissors require explicit declaration per pack" (F-MODE §56). C02 reserves the manifest key (3.1.1 fill); enforcement is C43. |
| **F35** Federation-as-family drift | v4's pack architecture "creates exactly this risk if pack governance is not explicit" (F-MODE §101). | C02 reserves the `[pack.derivation]` rule key; the derivation-rule *check* ships as a Phase-1 governance pack (F-MODE §172) — itself a C02 pack. |
| **F43** RSI board-visibility gap | Self-modifying packs. | `pack.toml` declares RSI status (F-MODE §75); C02 names the key, discipline remains operator-required (partial). |
| **Pack-schema breakage** (AI-CONTEXT §3.5) | 1–2 breaking pack/formula-format changes per quarter expected. | `schema_version` in the manifest (4) lets `gc` reject/upgrade incompatible packs rather than fail silently. |
| **Tool-node nonzero exit / crash** | A subprocess fails. | Exit code ≠ 0 is the failure signal (3.2 Reading A); the reconciler/Health-Patrol (C18) and Orders (C40) own retry/escalation. > [FAITHFUL-FILL]: v4 gives no per-tool retry contract at the ABI; minimal-consistent placement is "ABI surfaces exit code; convergence loop decides," since C18/C40 own retries/crash-survival in the docs. |

> [FAITHFUL-FILL] G29 is a **minor** gap and is *resolved here* by elaborating the ABI (3.2); no other
> C02-assigned failure mode is deferred.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** The ABI is where the lethal-trifecta boundary is enforced *per pack*: subprocess +
  `work_partition` confine a tool node; production scissors must be declared (F44). C02's "subprocess, not
  in-process plugin" choice means a misbehaving tool node cannot corrupt `gc`'s address space — a security
  property of the subprocess boundary itself.
- **Cost / scale.** Spawn-per-step subprocess invocation has process-startup overhead; v4 accepts this
  because tool nodes are "cheap and reproducible" (README:154) and run only "where reasoning is not
  required." No token cost (deterministic). > [FAITHFUL-FILL] no perf budget is stated; not invented here.
- **Observability.** Every tool-node invocation is an actor action: it carries `created_by` (C41) and lands
  on the event bus (C23). C02 must ensure the ABI exposes enough (node `name`, args, exit code) for that
  record — consistent with P9 attribution being "native, every bead and event carries `created_by`"
  (README:371).
- **Ops / licensing.** C02 is the mechanism that makes the **MIT / no-fork** license posture hold: because
  v4 never imports Gas City's `internal/` Go paths, the GitHub `internal/` import block is a non-issue
  (README:288, :334; AI-CONTEXT §10.1 line 502 "Corrected 2026-05-29"). The boundary beyond which a fork
  *would* be needed (new Provider / modified reconciler / urgent bug fix) is named and out of v4 scope.

## 8. Acceptance criteria & test strategy

Sweep-1 high-level criteria (concrete tests at sweep-2):

1. **Phase-0 minimum loads** — a `pack.toml` with only `[imports.core]` plus the §13.1 `city.toml` + one
   prompt template boots a one-agent `city` with **no custom Go code and no fork** (README:359–362).
2. **Subprocess tool node runs end-to-end** — the §13.3 `inspect_eval` `[[tool]]` (or an equivalent stub)
   is invoked with `{placeholder}` args substituted, executes in its `work_partition`, and its exit code
   is read as status (3.2 Reading A).
3. **No-fork invariant holds across phases** — Phases 1–3 add capability *only* by importing packs and
   adding TOML sections; no step requires importing Gas City as a Go library or modifying its source
   (the load-bearing claim of README §Part 7).
4. **Manifest declarations compose** — a pack contributing `[[tool]]`, a hook, a template, and a formula
   layers correctly with `city.toml`, with `city.toml` authoritative on conflict (3.1.2 Reading A).
5. **Declaration-discipline keys are honored** — a pack declaring production-scissors / RSI / derivation is
   readable by the governance checks (F44/F35/F43) — i.e. the keys exist and parse (enforcement tested by
   C43/C57).
6. **Schema-version guard** — a pack with an incompatible `schema_version` is rejected rather than
   mis-loaded (§3.5 breaking-change tolerance).

## 9. Open questions

(Mirrored into `_meta/review-log.md`.)

1. **[G29 — top open question] Exact tool-node I/O channel: args+files+exit-code (Reading A) vs. an
   additional stdin/stdout-JSON profile (Reading B)?** Sweep-1 picks A as the mandatory floor with B as an
   optional structured profile; sweep-2 must freeze the wire bytes (env vars passed? stdin format? stdout
   parse rule?) because every downstream pack (C24 bridge, C31 runner, C33 aggregator) builds against it.
2. **Pack-vs-`city.toml` precedence on duplicate sections** — confirm Reading A (local authoritative)
   against actual `gc` behavior (G11 — Gas City unverified).
3. **Manifest `schema_version` semantics** — does `gc` already version pack schemas, or is this a v4-side
   guard? Depends on verifying Gas City (G11).
4. **Declaration-discipline key names** — the F44/F35/F43 manifest keys are reserved here; their exact
   names/shape must be reconciled with C43 (isolation) and C57 (failure-mode register) so the governance
   packs and the manifest agree.
5. **Long-lived vs spawn-per-step tool nodes (OQ5)** — confirm no persistent tool-node daemon exists (vs the
   `[[service]]` block), so the "stateless per call" invariant is safe. Specifically: do the C24 directory-
   watch bridge and the C44 twin run as tool nodes or as `[[service]]` blocks? The corpus does not draw this
   boundary; the optimized tracks defer it (C02-B OQ4 / C17 OQ4). Reconcile at sweep-2 before C24/C44 build.

---

**[D-23 substrate-verified — gascity-prototype@b14c278, 2026-05-25]**

**F3 — Pack import strictness; `[defaults.rig.imports.*]` placement; transitive-import deduplication (NEW-INFO operational constraint):**
Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
(a) `[defaults.rig.imports.*]` entries must live in `city.toml`, not `pack.toml` — PackV2 rejects
them in a pack manifest. (b) Transitive imports are de-duplicated at startup: if pack A imports
pack B transitively, the city must NOT also declare `[imports.B]` directly — doing so produces a
duplicate agent definition and refuses startup. Pack authors should document transitive imports
explicitly so city authors know not to re-import them. C02's pack-on-disk layout documentation
(§4) should reflect these two constraints. This partially informs C02:OQ4 (declaration-discipline
key names) — specifically, the import placement rule: `[imports.*]` belongs in `pack.toml`,
`[defaults.rig.imports.*]` belongs in `city.toml`.
