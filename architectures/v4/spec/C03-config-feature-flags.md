# C03 — Layered config / feature-flag model  (Spec, canonical track)

> Source: AI-CONTEXT §3.2 ("nine concepts" #4 — "Config: Layered TOML; section presence = feature flag"); AI-CONTEXT §3.4 (smallest viable install / "Explicitly off" list); AI-CONTEXT §3.1 (coverage map — "Strong when `[formulas]` enabled"); AI-CONTEXT §13.1/§13.2/§13.3 (concrete `pack.toml`/`city.toml` skeletons per phase); AI-CONTEXT §11.1 ("6 of 12 principles natively"); README Part 6 Phase 0/Phase 1 ("Turn on `[formulas]`", "What you do NOT install"); component-inventory C03 row (`A26`, `B70`; depends on C01; gaps G03, G37).
> Inventory ID: C03   Kind: data-store   Status: sweep-2
> Track: A (faithful)
> Binding decisions obeyed: **D-14** (G37 secrets ≠ FE-3 signing), **D-25** (secrets deferred — keep config/env now, adopt minimal off-the-shelf env-injection or SOPS at first real credential; the G37 posture), **D-31** (rig config section is an ARRAY of N rig blocks — multiple rigs per city), **D-32** (rig spelling file-split: `.gc/site.toml` = `[[rig]]` with `path`; `city.toml` spelling needs-pinned-gc-run G11; `[[rigs]] path =` is a PackV2 error), **D-33** (XC-7 RESOLVED — C03 owns the CapabilityDescriptor registry + descriptor schema; C02 carries only `capability_id` reference).

> [D-23 substrate-verified — gascity-prototype@b14c278, 2026-05-25] The following harvest facts directly underwrite C03's layer-merge and config-key claims: **(F1)** canonical `[[rig]]` spelling + `path` belongs only in `.gc/site.toml`; **(F3)** `[defaults.rig.imports.*]` must be in `city.toml` not `pack.toml`; pack transitive imports are de-duplicated (duplicate direct import causes startup refusal); **(F4)** `gc init` is interactive — production workflow authors `pack.toml` / `city.toml` directly; **(F12)** `IS_SANDBOX=1` required for root + three pre-ack dialogs in `~/.claude.json`; **(F2)** `convergence.max_iterations` is NOT a real field (do not emit). Anchor: [gascity-config-anchor.md](_meta/gascity-config-anchor.md).

## 1. Purpose & responsibility

C03 is the **layered TOML configuration model** in which **the presence of a section enables a
capability** and its absence leaves the capability off. It is the single mechanism through which every
other component is feature-gated: `[formulas]` present ⇒ formula DAG composition on; `[mail]` present ⇒
messaging on; `[[rig]]` blocks present ⇒ rig partitioning on; and so on. The config files (`pack.toml`,
`city.toml`, and per-agent template references) are the version-controlled source of truth for *which
parts of the substrate are live in a given install* and for *the parameters those parts run with*.

**Responsibilities**
- Define the **layered config files** v4 uses — `pack.toml` (imports) and `city.toml` (workspace, agents,
  beads, services, rigs, tools, formulas, mail, daemon …) — and the rule that **section presence = the
  feature flag** (AI-CONTEXT §3.2 #4).
- Own the **enablement semantics**: a capability is *off* unless its section is present; turning a
  capability on is "add the section" (README Phase 1: "Turn on `[formulas]`").
- Own the **layering/merge order** by which `pack.toml` imports compose with the local `city.toml`
  (the "layered" in "layered TOML") and per-agent `env = { … }` overrides apply.
- Be the gate that drives the **per-phase install surface**: Phase 0 minimum (the "Explicitly off" set),
  Phase 1 additions, Phase 2 additions (AI-CONTEXT §13.1–§13.3).

**Explicitly NOT**
- NOT the substrate runtime itself (C01) — C03 is the *config data model* C01 reads; C01 is what acts on it.
- NOT the formula/pipeline-file format (C12). `[formulas]` *presence* is C03's flag; the *content* of a
  formula DAG is C12. C03 owns the on/off switch, not the workflow grammar.
- NOT the pack ABI / tool-node protocol (C02). C03 describes `[imports.*]` and `[[tool]]` *declarations*;
  the subprocess tool-node wire protocol is C02.
- NOT a secrets manager. C03 records that credentials appear in `env = { … }` / `[[service]]` blocks
  (AI-CONTEXT §13.2) but defines no secret storage, rotation, or encryption (see G37, §6/§9).
- NOT the phase-delivery plan (C54). C03 supplies the flags each phase toggles; C54 owns the phase ordering.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C01** Gas City substrate | C03 is Gas City concept #4 ("Config"); the substrate parses and acts on these TOML files. C03 has no meaning without C01. The C01↔C03 load-time cycle is a **load-time contract**: C01 reads C03's files; C03's presence flags tell C01 what to activate. This cycle is broken by an interface freeze at M1 (catalog + precedence). |
| Downstream (gated by) | **C12** Formula format | `[formulas]` section presence enables C12 (AI-CONTEXT §3.1, README Phase 1). |
| Downstream (gated by) | **C08** Spec artifact | inventory: C08 `depends on C03`; spec/template wiring is config-declared (`agents/<name>/prompt.template.md`). |
| Downstream (gated by) | **C06** Messaging, **C42** Rig partitioning, **C04** Session/provider, **C40** Orders, **C44**/services | `[mail]`, `[[rig]]`, `[[agent]] provider`, `[daemon]`/orders, `[[service]]` sections each gate their component. |
| Downstream (consumes) | **C02** Pack ABI | `[imports.core]` / pack imports are the layering inputs C03 composes. |

C03 is **foundational** (inventory: yes), in **Batch 1**, authored in parallel with C01/C02/C07 — it is a
load-bearing schema everything references for "is feature X on, and with what parameters."

## 3. Interfaces / contracts

1. **Config-file set** — the ordered layers C03 defines:
   - `pack.toml` — declares imports (`[imports.core]`, future `[imports.<name>]`); the *outer* layer.
   - `city.toml` — the workspace install: `[workspace]`, `[[agent]]`, `[beads]`, and the optional
     capability sections (`[formulas]`, `[mail]`, `[daemon]`, `[[rig]]`, `[[service]]`, `[[tool]]`).
   - `.gc/site.toml` — machine-local; entrypoint-written; carries `[[rig]]` `name`+`path` bindings only
     (F1). Never committed; `.gitignore`d.
   - per-agent `env = { … }` inline tables — the *innermost* override layer (e.g. Claude Code OTEL vars,
     AI-CONTEXT §13.2).
2. **Feature-flag predicate** — "is capability C enabled?" answered by **section presence**: `present ⇒ on`,
   `absent ⇒ off`. This is the contract every gated component queries (directly or via C01).
3. **Layer-merge interface** — "compose imported pack config + local `city.toml` + per-agent env into one
   effective config." Defines precedence (§4.2; concrete merge algebra per anchor §3 and F3).
4. **Capability-parameter accessor** — for an enabled section, read its keys (e.g. `[[service]]
   endpoint = …`, `[beads] provider = "file"`). Presence enables; keys parameterize.

**XC-7 — CapabilityDescriptor ownership — RESOLVED by D-33.**

> **[D-33 ADOPTED — lead, converged C02+C03 builders; 2026-06-01]**
> "The C02 and C03 Sweep-2 builders independently converged: **C03 owns the CapabilityDescriptor registry** (the authored capability catalog — a `city.toml` / config-layer concern); **C02 carries only a `capability_id` reference** in the pack manifest, not the descriptor definition. Resolves **XC-7** (the C02↔C03 ownership straddle flagged in both Sweep-1 specs)."
> — review-log D-33 (Sweep-2 spine-run decisions, 2026-06-01)

**C03 OWNS the CapabilityDescriptor registry + descriptor schema.** The `CapabilityDescriptor` concept (a machine-readable declaration of which config section gates which capability, with `requires` / `conflicts_with` relations) is a config-layer concern: the registry of authored capability descriptors lives in C03 as the feature-flag/config-model owner. C02 carries only a `capability_id` reference in the pack manifest (declaring which capability the pack provides) — C02 does NOT define the descriptor schema. C03 validates `capability_id` references against its registry.

This is the same authorship/registration split as C20→C22 (bead schemas → CXDB registry, per D-3): a pack *produces* a `capability_id` reference, C03 *owns* the registry and descriptor schema. **XC-7 is RESOLVED.** Remove any language in C02 or C03 that asserts the descriptor schema is deferred or belongs to the other component.

**CapabilityDescriptor schema stub (Sweep-2 — owned by C03, D-33):**

> [FAITHFUL-FILL] The exact CapabilityDescriptor schema is not given by v4 or the prototype (G11). The
> following stub is the minimal faithful shape implied by D-33 ("which config section gates which
> capability, with `requires` / `conflicts_with` relations") and the C20→C22 split analogy (D-3).
> Concrete field names need Sweep-3 freeze against the C03 conformance suite and C02 consumer contract.

```
CapabilityDescriptor {
  capability_id:    string          // stable reverse-DNS id, e.g. "softwarefactory.v4.capabilities.override-loop"
                                    // matches the [[pack]] capability_id reference C02 carries
  section:          string          // the city.toml / pack.toml section whose presence enables this capability
                                    // e.g. "[formulas]", "[[rig]]", "[[service]]"
  label:            string          // human-readable label (for tooling / audit)
  requires:         []capability_id // capabilities that must ALSO be enabled (prerequisite sections)
  conflicts_with:   []capability_id // capabilities that MUST NOT be simultaneously enabled
  verification:     string          // "harvest-verified" | "needs-pinned-gc-run (G11)" | "[inferred — needs G11]"
}
```

The registry of `CapabilityDescriptor` entries lives in C03 (not in pack.toml or city.toml).
C02's `capability_id` field in a pack manifest is a *reference into* this registry.
C03 validates the reference at pack import time; an unknown `capability_id` → E-C03-02 (missing required key variant) or a new E-code to be assigned at Sweep-3.

> [needs G11 verification] Whether Gas City has a native CapabilityDescriptor registry concept or whether
> this is a purely v4-side registry is **[needs G11 verification]**. Until confirmed, C03 owns the v4-side
> registry as a config-layer artifact; the enforcement hook (whether `gc` validates `capability_id`
> references natively or a C02/C03 conformance pack does) is a Sweep-3 concern.

**Invariants**
- **Presence-is-the-flag**: no separate `enabled = true` boolean exists for the substrate-native
  capabilities; the *only* on/off signal is whether the section is written. (Faithful to AI-CONTEXT §3.2
  #4 and README "Turn on `[formulas]`" / "Explicitly off".)
- **Absent ⇒ inert**: a capability whose section is absent contributes nothing at runtime (Phase 0's
  "What you do NOT install" is achieved purely by *omitting* sections, not by disabling them).
- **Version-controlled**: `pack.toml` and `city.toml` live in git alongside packs (README:107
  "packs are git-versioned"); the effective feature set of an install is fully reconstructable from
  committed TOML. `.gc/site.toml` is machine-local and `.gitignore`d.
- **No `[autonomy]` block**: there is no Gas City config section named `[autonomy]`. Autonomy policy is
  the C56 autonomy-ladder (a policy construct), not a `gc` config section. Do not emit `[autonomy]` TOML.
- **No `convergence.max_iterations`**: this field does not exist in Gas City (F2). Do not emit it.

## 4. Data model / state

C03 owns the **config files as a layered, version-controlled artifact**. No mutable runtime state of its
own; the substrate (C01) is what loads it each run.

### 4.1 Config-file field table (Sweep-2)

The primary config-key registry for C03's owned surfaces. Uses columns: **Key / Block | File | Type | Req
| Semantics | R/W-by**.

Verification-status vocabulary from [gascity-config-anchor.md](_meta/gascity-config-anchor.md): `harvest-verified`
= proven against the running prototype; `needs-pinned-gc-run (G11)` = named in deep-dive but not exercised;
`[inferred — needs G11]` = not grounded in any primary source.

#### `pack.toml` keys

| Key / Block | File | Type | Req | Semantics | R/W-by |
|---|---|---|---|---|---|
| `[pack] name` | pack.toml | string | R | Pack identity (root pack name) | Pack author writes; C01 reads at load (harvest-verified) |
| `[pack] schema = 2` | pack.toml | int | R | PackV2 schema version; C01 REFUSES startup on wrong value | Pack author writes; C01 enforces (harvest-verified) |
| `[imports.<name>] source` | pack.toml | string | O | Import a bundled pack; source is `"github.com/…//path"` (embedded FS, no network). Transitive imports auto-de-duplicated — do NOT re-import a pack that is already transitively imported (F3 startup-refusal hazard). | Pack author writes; C01 resolves (harvest-verified, F3) |
| `[[tool]] name` | pack.toml | string | O | Deterministic tool-node the pack ships | Pack author writes; C02 executes (needs-pinned-gc-run G11) |
| `[[tool]] cmd` | pack.toml | string | O | Command or script the tool-node runs. **SPELLING NOTE:** C02 §4.1 uses `command`; this table uses `cmd` — **needs-pinned-gc-run (G11)** to settle canonical field name. | Pack author writes; C02 executes (needs-pinned-gc-run G11) |
| `[[tool]] args` | pack.toml | array\<string\> | O | Args with `{placeholder}` substituted from bead/molecule context | Pack author writes; C02 expands (needs-pinned-gc-run G11) |

**Must NOT appear in `pack.toml`:**
- `[defaults.rig.imports.*]` — MUST be in `city.toml` only (F3; PackV2 rejects this in a pack manifest).

#### `city.toml` keys

| Key / Block | File | Type | Req | Semantics | R/W-by |
|---|---|---|---|---|---|
| `[workspace] name` | city.toml | string | R | City identity (workspace name) | Operator writes; C01 reads (harvest-verified) |
| `[workspace] provider` | city.toml | `"claude"` | O | City-default session provider preset (overridden per-agent) | Operator writes; C04 reads (harvest-verified) |
| `[workspace] global_fragments` | city.toml | array\<string\> | O | Prompt fragments injected city-wide | Operator writes; C01/agents read (harvest-verified) |
| `[defaults.rig.imports.<name>] source` | city.toml | string | O | Per-rig pack import scoped to a rig. MUST be here, NOT in pack.toml (F3). | Operator writes; C01 resolves (harvest-verified, F3) |
| `[agent_defaults]` | city.toml | table | O | City-level defaults for `provider`, `wake_mode`, `default_sling_formula` | Operator writes; C01/C04/C05 reads (needs-pinned-gc-run G11 — some fields parsed-but-not-applied) |
| `[[agent]] provider` | city.toml | string | R | Declares a worker agent with a provider (e.g. `"claude"`). Section presence = agent declared. | Operator writes; C01/C04 reads (harvest-verified) |
| `[[agent]] env` | city.toml | inline-table | O | Per-agent env overrides (OTEL/telemetry keys etc.); innermost override layer | Operator writes; C01 applies; C04 inherits (needs-pinned-gc-run G11 for exact keys) |
| `[beads] provider` | city.toml | string | R | Bead store provider: `"file"` (Phase-0), `"bd"` (Dolt, prototype), `"exec:<script>"`. **Section presence = bead store on.** | Operator writes; C01/C19 reads (harvest-verified: `"bd"` in prototype, `"file"` also valid) |
| `[daemon] patrol_interval` | city.toml | duration | O | Health-patrol loop cadence | Operator writes; C18 reads (harvest-verified — field present in prototype) |
| `[daemon] max_restarts` | city.toml | int | O | Max agent restarts in `restart_window` | Operator writes; C18 reads (harvest-verified — field present) |
| `[daemon] restart_window` | city.toml | duration | O | Window for `max_restarts` count | Operator writes; C18 reads (harvest-verified) |
| `[daemon] shutdown_timeout` | city.toml | duration | O | Graceful-stop timeout | Operator writes; C01 reads (harvest-verified) |
| `[daemon] wisp_gc_interval` | city.toml | duration | O | Wisp garbage-collection cadence | Operator writes; C01 reads (harvest-verified) |
| `[daemon] wisp_ttl` | city.toml | duration | O | TTL for ephemeral molecules (wisps) | Operator writes; C13 reads (harvest-verified) |
| `[daemon] formula_v2` | city.toml | bool | O | Opt-in to formula V2 engine | Operator writes; C12 reads (harvest-verified — field present) |
| `[orders] max_timeout` | city.toml | duration | O | Global order timeout | Operator writes; C40 reads (harvest-verified — set in prototype) |
| `[orders] skip` | city.toml | array\<string\> | O | Order-skip filter list | Operator writes; C40 reads (harvest-verified) |
| `[mail] provider` | city.toml | string | O | Messaging provider: `"beadmail"` (default) or `"exec:<script>"`. **Section presence = mail on.** | Operator writes; C06 reads (needs-pinned-gc-run G11 — not enabled in prototype) |
| `[events] provider` | city.toml | string | O | Event stream provider: file JSONL (default → `.gc/events.jsonl`), `"fake"`, `"fail"`, `"exec:<script>"`. **Section presence = event stream on.** | Operator writes; C23 reads (needs-pinned-gc-run G11) |
| `[formulas]` (section) | city.toml | table | O | Formula DAG composition on. **Section presence = C12 enabled.** Content (dir etc.) is C12's domain. | Operator writes; C12 reads (needs-pinned-gc-run G11 — not enabled in prototype) |
| `[session] provider` | city.toml | string | O | Session provider kind: `""` / tmux (default Phase-0), `"fake"`, `"subprocess"`, `"exec:<script>"`, `"k8s"` | Operator writes; C04 reads (harvest-verified: Phase-0 kind = tmux, F7; other kinds needs-pinned-gc-run G11) |
| `[[rig]] name` | city.toml | string | R (if rig block present) | Rig identifier; SPELLING NOTE: see §3 / anchor spelling note — `[[rig]]` is the F1 canonical form; prototype `city.toml.example` uses `[[rigs]]` — **needs-pinned-gc-run G11** to settle spelling in city.toml | Operator writes; C42 reads |
| `[[rig]] prefix` | city.toml | string | R (if rig block present) | Per-rig bead-ID prefix (e.g. `"r1"`); explicit value REQUIRED — ambiguous auto-derived values collide (F10). **Presence = rig partitioning on.** | Operator writes; C19/C42 reads (harvest-verified: prefix mechanism, F10) |
| `[[rig]] read_partition` | city.toml | string | O | Role-based partition label (C42) | Operator writes; C42/C34 reads (needs-pinned-gc-run G11) |
| `[[rig]] write_partition` | city.toml | string | O | Role-based partition label (C42) | Operator writes; C42/C34 reads (needs-pinned-gc-run G11) |
| `[[service]] name` | city.toml | string | R (if service block present) | HTTP service name mounted at `/svc/{name}` on controller edge. **Section presence = service on.** | Operator writes; C44 reads (needs-pinned-gc-run G11) |
| `[convergence]` | city.toml | table | O | Convergence-loop limits. The section MAY exist; `convergence.max_iterations` DOES NOT (F2). Do not emit `max_iterations`. | needs-pinned-gc-run G11 for valid keys |

**Must NOT appear in `city.toml`:**
- A rig `path =` field — path bindings are machine-local; they live in `.gc/site.toml` only (F1).
- `convergence.max_iterations` — not a real field (F2, harvest-verified non-existent).
- `[autonomy]` — no such config block exists (anchor §3 / C56 owns autonomy as a policy construct).

#### `.gc/site.toml` keys (machine-local, entrypoint-written)

| Key / Block | File | Type | Req | Semantics | R/W-by |
|---|---|---|---|---|---|
| `workspace_name` | .gc/site.toml | string | R | Links site config to a workspace | Entrypoint writes; C01 reads (harvest-verified, F1) |
| `[[rig]] name` | .gc/site.toml | string | R | Rig identifier matching city.toml `[[rig]]` name | Entrypoint writes at container-start; C01/C42 reads (harvest-verified, F1) |
| `[[rig]] path` | .gc/site.toml | string | R | **Filesystem binding** `/workspace/rigs/<name>/`; machine-local (only the entrypoint knows runtime paths). NEVER in city.toml. | Entrypoint writes; C42/C43 reads (harvest-verified, F1, entrypoint.sh:70-76) |

#### Environment variables (C03-owned)

| Key | File | Type | Req | Semantics | R/W-by |
|---|---|---|---|---|---|
| `IS_SANDBOX=1` | .env / env | bool | R (root) | Required for `claude --dangerously-skip-permissions` as root (F12) | Operator/entrypoint writes; C01/C04 reads (harvest-verified, F12) |
| `DOLT_REF=refs/heads/dolt-data` | .env / env | string | O | Dolt push/clone ref; default `refs/dolt/data` is rejected by proxies (F9) | Operator/entrypoint writes; C19 reads (harvest-verified, F9) |

### 4.2 Layer-merge precedence (Sweep-2 — resolved from anchor)

**RESOLVED (Sweep-2):** The layer-merge order and override semantics are grounded in F3 + the anchor §2.
The OQ-C03-2 inline question ("layer-merge precedence") is partially resolved below; residual merge-algebra
questions (deep-merge vs replace for same-key scalars in array sections) remain `needs-pinned-gc-run (G11)`.

**Layering order (outer → inner; inner overrides outer):**

```
pack.toml [imports.*]  →  city.toml sections  →  .gc/site.toml  →  [[agent]] env = {…}
    (outer defaults)        (workspace install)   (machine-local)    (innermost per-agent)
```

**Concrete rules (harvest-verified or inferred):**

1. **`pack.toml` imports are the outermost layer.** Pack-provided defaults / sections are the base config
   that `city.toml` overrides. Resolved at startup from embedded FS (no network, F3).
2. **`city.toml` overrides pack defaults.** Any key/section present in `city.toml` supersedes the
   corresponding key from the imported pack. This is the primary authoring surface.
3. **`.gc/site.toml` provides machine-local `[[rig]]` path bindings.** It does NOT participate in
   section-presence logic; it only supplies the `path` field that `city.toml` intentionally omits (F1).
   Written by the entrypoint at container-start time; never committed.
4. **Per-`[[agent]]` `env = { … }` is the innermost override.** Agent-specific env keys win over
   workspace-level env. (AI-CONTEXT §13.2; needs-pinned-gc-run G11 for exact scope of "innermost".)

**Merge semantics (residual — needs-pinned-gc-run G11):**
- Whether same-key scalar values in `pack.toml` and `city.toml` are *replaced* or *deep-merged* is
  unverified. The safe authoring rule: treat each import as providing defaults; author all instance-specific
  values in `city.toml`.
- Array sections (`[[agent]]`, `[[rig]]`, `[[service]]`, `[[tool]]`): whether packs and `city.toml`
  *append* their entries or `city.toml` *replaces* all pack entries is **needs-pinned-gc-run (G11)**.
  The F3 de-duplication rule (duplicate imported pack = startup refusal) implies Gas City does NOT silently
  drop array duplicates — it errors, which is the correct fail-closed behavior.

> **OQ-C03-2 RESOLVED (Sweep-2, partial):** Precedence order is now concrete (pack imports → city.toml →
> site.toml → per-agent env). Deep-merge vs replace algebra for same-key scalars and array-section append
> vs replace semantics remain `needs-pinned-gc-run (G11)`. Mark residual `needs-G11`.

**Secrets precedence (D-25 posture):**

> [D-25 ADOPTED — verbatim from review-log.md:]
> "Secrets: adopt Option A — keep config/env now, adopt a **minimal off-the-shelf secrets approach (env-injection or SOPS-encrypted files) at first real credential**; no premature secrets build. This is the **G37** posture (G37 ≠ FE-3 signing, per D-14)."

> [D-14 ADOPTED — verbatim from review-log.md:]
> "G37 = open secrets/credential-storage gap (owned by C03; plaintext `city.toml`/env today). FE-3 = graduated-mandatory signing, BLOCKED ON G37 but a distinct deferred enhancement. Specs deferring secrets cite **G37**, not FE-3."

C03's secrets posture (canonical track, faithful): credentials appear in `env = { … }` or `[[service]]`
endpoint fields as plaintext or as env-variable references (e.g. `${ENV:LANGFUSE_SECRET_KEY}`). The D-25
decision means the canonical track does NOT build a secrets manager, SecretResolver, or SOPS encryption
layer; those belong at the first real credential (a future step). C03 surfaces G37 as residual risk and
performs detection-only (AC-C03-07 lint).

**OQ-C03-1 RESOLVED (Sweep-2):** The D-25 decision settles the secrets scope: posture is env-injection
now; SOPS/Vault at first real credential. No elaboration within this spec. Marking resolved.

### 4.3 Feature-flag / capability-section catalog (Sweep-2)

Canonical capability sections from v4 + anchor §3, with on/off semantics and verification status.
"Section presence = capability on" for all rows below.

| Section | File | Capability gated | On at phase | C-ID gated | Verification |
|---|---|---|---|---|---|
| `[workspace]` | city.toml | Workspace identity; baseline runtime | Phase 0 (always) | C01 | harvest-verified |
| `[[agent]] provider = "claude"` | city.toml | Agent worker declared | Phase 0 (always) | C04 | harvest-verified |
| `[beads] provider` | city.toml | Bead store (C19 persistence) | Phase 0 (always) | C19 | harvest-verified |
| `[imports.<name>]` | pack.toml | Pack import layer | Phase 0 (always) | C02 | harvest-verified (F3) |
| `[defaults.rig.imports.<name>]` | city.toml | Per-rig pack import | Phase 0 (always) | C02 | harvest-verified (F3) |
| `[session] provider` | city.toml | Session provider kind (tmux = Phase-0 kind) | Phase 0 (always) | C04 | harvest-verified (F7) |
| `[daemon]` | city.toml | Health-patrol / controller loop | Phase 0 (always, minimal) | C18 | harvest-verified (field names present in prototype) |
| `[orders]` | city.toml | Order scheduling on | Phase 0 off → Phase 1 | C40 | harvest-verified (`max_timeout` present in prototype, but orders themselves off at Phase 0 per §3.4) |
| `[formulas]` | city.toml | Formula DAG composition (C12) **ON** | **Phase 1** | C12 | needs-pinned-gc-run (G11) — not enabled in prototype |
| `[[service]]` (langfuse/cxdb/otel) | city.toml | External service wiring | Phase 1 | C44 | needs-pinned-gc-run (G11) |
| `[[agent]] env = { … }` | city.toml | Per-agent OTEL/telemetry env | Phase 1 | C04/C26 | needs-pinned-gc-run (G11 for exact keys) |
| `[mail]` | city.toml | Messaging/nudge (C06) **ON** | Phase 1/2 | C06 | needs-pinned-gc-run (G11) — not enabled in prototype |
| `[events]` | city.toml | Event stream (C23) **ON** | Phase 1/2 | C23 | needs-pinned-gc-run (G11) |
| `[[rig]]` blocks (city.toml) | city.toml | Rig partitioning (C42) **ON** | **Phase 2** | C42 | harvest-verified (prefix mechanism, F10); spelling needs-pinned-gc-run (G11). **D-31 NOTE:** city hosts N rigs — MUST NOT assume one-rig-per-city (D-31 ADOPTED 2026-06-01). |
| `[[rig]] read_partition / write_partition` | city.toml | Role-based partition labels | Phase 2 | C42/C34 | needs-pinned-gc-run (G11) |
| `[[tool]] type = "subprocess"` | pack.toml | Tool-node declaration | Phase 2 | C02 | needs-pinned-gc-run (G11) |

**Phase-0 "off-by-omission" set** (AI-CONTEXT §3.4): `[daemon]` (above minimal), `[mail]`, `[formulas]`,
`[[rig]]` blocks†, Dolt server (use `[beads] provider = "file"` at Phase 0), `[[service]]` blocks, orders.
All off purely by omitting their sections.

> † **Spelling note (OQ-C03-2 / RC03-01 — OPEN).** The AI-CONTEXT §3.4 explicit-off list writes "rigs"
> (prose form). The canonical array form is `[[rig]]` (AI-CONTEXT §13.3; F1; C42). The city.toml spelling
> for the partition/role block is `[[rig]]` per F1 (canonical ruling) but the prototype `city.toml.example`
> uses `[[rigs]]` — **needs-pinned-gc-run (G11)**. The anti-drift invariant that holds in both: **rig
> `path` belongs ONLY in `.gc/site.toml`**. See anchor §3 spelling note.

**G03 phase-relative count (faithful resolution):**

> [AMBIGUITY: G03] **What is the native principle count at the smallest install — 5 or 6?**
> Reading A (literal headline): AI-CONTEXT §11.1/§3.6 assert "6 of 12 native" and count P1,P2,P3,P4,P9,P10.
> Reading B (gated): §3.1 rates P3 "Strong **when `[formulas]` enabled**" and §3.4 + README Phase 0 turn
> `[formulas]` **off** at the smallest install. Under Reading B the smallest install delivers **5**.
> **Pick: Reading B** — the §3.1 coverage map, §3.4 explicit-off list, and README Phase-0 all agree P3 is
> `[formulas]`-gated. The "6 of 12" headline is faithful only as a Phase-1 (formulas-on) statement.
> **Ownership split (consistent with C01-A §6):** C03 *derives* the count from which sections are present;
> C01 *verifies* each native capability against the pinned `gc` (conformance manifest); C57 *reconciles*
> the corpus-wide headline. Complementary, not conflicting.

## 5. Behavior

C03 has no control loop; its behavior is **load-time** and **authoring-time**:

- **Authoring**: enabling a capability = adding its section (and its parameter keys) to `city.toml`
  (or importing a pack that provides it). Disabling = removing the section.
- **Load-time composition**: at substrate startup, C01 reads `pack.toml` imports, merges them under the
  local `city.toml`, overlays `.gc/site.toml` machine-local bindings, applies per-agent `env`, and yields
  the **effective config**; section presence in the effective config is the enablement signal each component
  checks.
- **Phase progression**: moving Phase 0 → 1 → 2 is, at the config layer, exactly the act of adding the
  Phase-1 and Phase-2 sections from §13.2/§13.3 to the Phase-0 skeleton.

### 5.1 Config-load lifecycle — state diagram (Sweep-2)

```mermaid
stateDiagram-v2
    [*] --> Reading : gc start invoked
    Reading --> Merging : pack.toml + city.toml read
    Merging --> SiteOverlay : city.toml keys merged over pack imports
    SiteOverlay --> EnvApply : .gc/site.toml rig paths overlaid
    EnvApply --> Validation : per-agent env = {…} applied (innermost)
    Validation --> Effective : all keys valid; no unknown/missing-required
    Validation --> Error_MissingRequired : required key absent → E-C03-02
    Validation --> Error_UnknownKey : unexpected key for section → E-C03-04
    Validation --> Error_MergeConflict : duplicate pack import → E-C03-01 (F3)
    Effective --> Running : capability flags live; gated components activated
    Running --> [*]
    Error_MissingRequired --> [*]
    Error_UnknownKey --> [*]
    Error_MergeConflict --> [*]
```

### 5.2 Concrete phase skeletons (Sweep-2)

Reference TOML skeletons per phase. These are the committed artifacts T4 in the build plan produces.

**Phase-0 skeleton (`city.toml`):**

```toml
[workspace]
name = "software-factory"
provider = "claude"

[[agent]]
provider = "claude"

[beads]
provider = "bd"      # or "file" for simpler Phase-0; "bd" matches prototype

[daemon]
patrol_interval = "30s"
max_restarts = 5
restart_window = "5m"
shutdown_timeout = "10s"

# NOT present at Phase 0:
# [formulas]
# [mail]
# [events]
# [[rig]]
# [[service]]
```

**Phase-0 skeleton (`pack.toml`):**

```toml
[pack]
name = "software-factory"
schema = 2

[imports.gastown]
source = "github.com/lago-morph/gascity-prototype//pack"
```

**Phase-0 `.gc/site.toml`** (entrypoint-written, never committed):

```toml
workspace_name = "software-factory"

[[rig]]
name   = "main"
path   = "/workspace/rigs/main"
```

**Phase-1 additions to `city.toml`** (add to Phase-0 skeleton):

```toml
[formulas]
# content (dir, etc.) is C12's domain; section presence = C12 on

[[service]]
name = "langfuse"
# endpoint and auth keys go here (G37 residual risk — see §6)

[[service]]
name = "cxdb"
# endpoint keys here

[[agent]]
provider = "claude"
env = { OTEL_EXPORTER_OTLP_ENDPOINT = "http://collector:4318" }
```

**Phase-2 additions to `city.toml`** (add to Phase-1):

```toml
[[rig]]          # spelling: [[rig]] per F1; [[rigs]] per prototype example — needs-pinned-gc-run (G11)
                 # D-31: city hosts N rigs — MUST NOT assume one-rig-per-city (D-31 ADOPTED 2026-06-01)
name   = "worker"
prefix = "r1"    # explicit, required (F10 — auto-derive collides)
# read_partition / write_partition go here (needs-pinned-gc-run G11)

[[rig]]          # needs-pinned-gc-run (G11) — spelling same caveat as above
name   = "judge"
prefix = "gp"
```

## 6. Failure modes & handling

| F-mode / gap | Relevance | Handling in C03 (faithful) |
|---|---|---|
| **G03** — "6 of 12 native" is unsupported because P3 is "Strong **when `[formulas]` enabled**" but Phase 0 turns `[formulas]` **off** | C03 *owns the very flag* (`[formulas]`) the miscount turns on. | RESOLVED (Sweep-2): native count is **phase-relative** — 5 at Phase 0 (formulas off), 6 once `[formulas]` is added in Phase 1. C03's catalog (§4.3) makes the count explicitly derivable from present sections. G03 closed at the config-model layer. |
| **G37** — secrets/credentials appear in `city.toml`/`env` as plaintext with no secrets story | OAuth/CXDB/LangFuse/OTel mTLS creds live in `[[service]]` endpoints and `env = { … }` (AI-CONTEXT §13.2), i.e. *inside C03's files*. | D-25 posture: keep config/env now; adopt env-injection or SOPS at first real credential. Detection-only lint (AC-C03-07). G37 ≠ FE-3 (D-14). |
| Misconfiguration — typo'd / missing section | A capability silently stays off if its section is absent or misnamed. | Absence is *intentional* off (Phase 0 relies on it). Detection of *unintended* omission is E-C03-03 (lint-time expected-sections check). |
| Layer-merge conflict | Duplicate pack import causes startup refusal (F3) | E-C03-01: detected at load time; Gas City refuses startup on duplicate agent definitions. |
| `path =` in `city.toml` rig block | PackV2 validation error (F1) | E-C03-04: unknown key for the city.toml rig section. Authoring rule: path ONLY in `.gc/site.toml`. |
| `convergence.max_iterations` emitted | Not a real field (F2) | E-C03-04: unknown key at config validation. Do not emit this field. |

> [AMBIGUITY: G03] — see §4.3 above.

## 6.1 Error taxonomy (Sweep-2)

| E-code | Condition | Surfaced-as | Caller recovery |
|---|---|---|---|
| **E-C03-01** | **Merge conflict / duplicate import**: a pack is imported directly in `city.toml` AND already transitively imported by another pack (F3 startup-refusal) | `gc start` refuses startup with a duplicate-agent error | Remove the duplicate direct `[imports.<name>]` from `city.toml`; rely on the transitive import only |
| **E-C03-02** | **Missing required key**: a section is present but a required key is absent (e.g. `[workspace]` without `name`, `[[rig]]` without `prefix`) | `gc start` refuses startup with a missing-key error | Add the missing key to the appropriate file |
| **E-C03-03** | **Unintended omission / expected-section missing**: a capability expected to be on (per phase manifest) is absent from the effective config | Lint-time / startup warning (detection-only; off-by-omission is also intentional — OQ-C03-3 open) | Operator reviews phase manifest vs committed `city.toml`; adds section or confirms intentional absence |
| **E-C03-04** | **Unknown or misplaced key**: a key appears in the wrong file (e.g. `path =` in `city.toml` rig block, F1) or a non-existent field name (e.g. `convergence.max_iterations`, F2) | PackV2 validation error at `gc start`; startup refused | Move key to the correct file (e.g. `path` → `.gc/site.toml`); remove the non-existent field |
| **E-C03-05** | **Secrets literal in version-controlled TOML**: a credential-bearing value appears as a plaintext literal in a committed `city.toml` or `pack.toml` (G37 residual risk) | Lint warning (detection-only per D-25 posture; AC-C03-07) | Replace with env-variable reference (e.g. `"${ENV:LANGFUSE_SECRET_KEY}"`); adopt SOPS at first real credential |
| **E-C03-06** | **`[autonomy]` block emitted**: a non-existent Gas City config section was authored | PackV2 rejects unknown top-level section (or silently ignored — needs-pinned-gc-run G11) | Remove the `[autonomy]` block; autonomy is a C56 policy construct, not a config section |
| **E-C03-07** | **`convergence.max_iterations` emitted**: non-existent field (F2) | Gas City config validation error or silent ignore (harvest-verified non-existent, F2) | Remove the field; no max_iterations setting exists in Gas City config |

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security**: C03 is the locus of G37 — `[[service]]` endpoints and per-agent `env = { … }` carry
  endpoints and (implicitly) credentials in plaintext version-controlled TOML. D-25 posture: env-injection
  now; SOPS/Vault at first real credential. G37 ≠ FE-3 (D-14). Detection-only lint surfaces residual risk.
- **Cost**: negligible direct cost; config is small (~30 lines at Phase 0, AI-CONTEXT §13.1). Cost leverage
  is indirect — it gates which (costly) services are wired in.
- **Scale**: config is human-authored and small; no scale concern of its own. It bounds runtime scale by
  which sections (services, rigs, tools) are present.
- **Observability**: the effective config *is* the observability surface for "what is on in this install";
  it is fully reconstructable from committed files.
- **Ops**: changes flow through normal git review (README:107). AI-CONTEXT §3.5 warns of 1–2 breaking
  pack-schema / formula-format changes per quarter — schema-version drift is an ops concern C03 tracks via
  `[pack] schema = 2` and the anchor's verification-status vocabulary.

## 8. Acceptance criteria & test strategy

### 8.1 Sweep-1 criteria

1. **Presence-is-flag**: enabling a capability requires *only* adding its section; with the section absent,
   the capability is provably inert (Phase-0 "Explicitly off" set verified to contribute nothing).
2. **Phase skeletons compose**: the §5.2 Phase-0 skeleton + Phase-1 additions + Phase-2 additions merge
   into a valid effective config with deterministic precedence (no key collisions silently dropped).
3. **Phase-relative native count**: a check derives the native-principle count from present sections and
   yields 5 at the Phase-0 skeleton (formulas off) and 6 once `[formulas]` is added — making G03 explicit.
4. **Round-trip**: the effective feature set of an install is reconstructable from committed `pack.toml` +
   `city.toml` alone (version-control invariant).
5. **Secrets surfaced**: a lint/audit flags any credential-bearing key in `env`/`[[service]]` as a G37
   residual-risk item (detection only; v4 prescribes no mitigation per D-25).

### 8.2 Concrete acceptance tests (Sweep-2)

**AC-codes: AC-C03-NN**

| AC-code | Given / When / Then | Verifies |
|---|---|---|
| **AC-C03-01** | GIVEN the Phase-0 `city.toml` skeleton (§5.2) with `[formulas]` absent; WHEN C03's section-presence predicate is evaluated; THEN the formula capability is OFF and `[formulas]` is not returned as present | Presence-is-flag; Phase-0 "Explicitly off" set (G03); E-C03-03 |
| **AC-C03-02** | GIVEN the Phase-0 skeleton; WHEN `[formulas]` is added (Phase-1 transition); THEN the formula capability is ON | Presence-is-flag; phase-relative count yields 6 (G03) |
| **AC-C03-03** | GIVEN the Phase-0 skeleton; WHEN the section-presence predicate is evaluated across all capability sections; THEN the native-principle count is exactly 5 (P1,P2,P4,P9,P10; P3 not yet on) | G03 phase-relative count |
| **AC-C03-04** | GIVEN a `city.toml` with a `[[rig]]` block that includes `path = "/workspace/rigs/r1"`; WHEN submitted to the config validator; THEN the validator rejects it with E-C03-04 (path belongs in `.gc/site.toml`) | F1; E-C03-04 |
| **AC-C03-05** | GIVEN a `city.toml` with `convergence.max_iterations = 10`; WHEN submitted to the config validator; THEN the validator rejects or warns with E-C03-07 (non-existent field) | F2; E-C03-07 |
| **AC-C03-06** | GIVEN a `pack.toml` importing pack A, and a `city.toml` also declaring `[imports.A]` where pack A is already transitively imported; WHEN `gc start` is invoked; THEN startup is refused with E-C03-01 (duplicate agent error) | F3; E-C03-01 |
| **AC-C03-07** | GIVEN a `city.toml` with `[[service]]` containing a plaintext credential literal (e.g. `secret = "sk-abc123"`); WHEN the secrets-surface lint runs; THEN a G37 residual-risk warning is emitted (detection only; not startup-refused per D-25) | G37; E-C03-05; D-25 posture |
| **AC-C03-08** | GIVEN the Phase-0, Phase-1, and Phase-2 skeletons merged in order; WHEN the effective config is derived; THEN later-layer values for the same key win (inner overrides outer) and no key is silently dropped | Layer-merge precedence (§4.2) |
| **AC-C03-09** | GIVEN a `city.toml` with `[workspace]` but no `name` key; WHEN `gc start` is invoked; THEN startup is refused with E-C03-02 (missing required key) | E-C03-02 |
| **AC-C03-10** | GIVEN a `city.toml` with `[[rig]]` blocks carrying explicit `prefix` values (`"r1"`, `"gp"`); WHEN rig bead-ID namespacing is computed; THEN each rig's beads are prefixed with its explicit value (no auto-derived collision) | F10; harvest-verified rig-prefix mechanism |

**E↔AC cross-references:**
- E-C03-01 → AC-C03-06
- E-C03-02 → AC-C03-09
- E-C03-03 → AC-C03-01 (via expected-section absence)
- E-C03-04 → AC-C03-04, AC-C03-05
- E-C03-05 → AC-C03-07
- E-C03-07 → AC-C03-05

## 9. Open questions

- **OQ-C03-1 RESOLVED (Sweep-2 — D-25 ADOPTED, 2026-05-31):** G37 secrets scope settled — keep
  config/env now; adopt env-injection or SOPS-encrypted files at first real credential. No premature
  secrets build. G37 ≠ FE-3 (D-14). Detection-only lint (AC-C03-07). OQ text preserved:
  _v4 puts OAuth/CXDB/LangFuse/OTel-mTLS credentials in version-controlled `city.toml`/`env` with no
  secrets manager. Faithful spec records the risk and defers._

- **OQ-C03-2 RESOLVED (Sweep-2, partial):** Layer-merge precedence is now concrete (§4.2): pack imports
  → city.toml → site.toml → per-agent env. Residual: deep-merge vs replace for same-key scalars and
  array-section append vs replace semantics remain `needs-pinned-gc-run (G11)`. Original OQ text:
  _Layer-merge precedence is inferred (§4 FAITHFUL-FILL). v4 never states whether imported-pack config
  deep-merges or is replaced by local `city.toml`, nor array-section merge semantics._

- **OQ-C03-3** (→ review-log, STILL OPEN): **Off-by-omission vs unintended-omission.** Because absence
  *is* the off signal, a misnamed/forgotten section is indistinguishable from a deliberate disable. v4
  specifies no guard; is a faithful "expected-sections manifest" warranted, or does that contradict the
  presence-is-the-only-signal invariant? Surfaces as E-C03-03 (detection-only warning).

---

**[D-23 substrate-verified — gascity-prototype@b14c278, 2026-05-25]**

**F1 — `[[rig]]` canonical spelling (NEW-INFO, supports XC-9 resolution):**
Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
the canonical spelling is `[[rig]]` (singular). `[[rigs]] path =` is a PackV2 validation error;
path bindings for a rig's working directory live in `.gc/site.toml` as `[[rig]]` entries, written
at container-start time by the entrypoint (which knows the runtime filesystem paths). `city.toml`
carries `[[rig]]` blocks for partition/role semantics only, without a `path` field. This makes the
`[[rig]]` spelling in C03 canonical (consistent with AI-CONTEXT §13.3).

**F3 — Pack import strictness and `[defaults.rig.imports.*]` placement (NEW-INFO operational constraint):**
Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
(a) `[defaults.rig.imports.*]` entries must live in `city.toml`, not `pack.toml` — PackV2 rejects
them in a pack manifest. (b) Transitive imports are de-duplicated at startup: if pack A imports
pack B transitively, the city must NOT also declare `[imports.B]` directly — doing so produces a
duplicate agent definition and refuses startup. Pack authors should document transitive imports
explicitly so city authors know not to re-import them. C03's layering/merge-order section should
reflect these two constraints.

**F4 — `gc init` is interactive; production workflow authors config files directly (NEW-INFO operational caveat):**
Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
`gc init` is an **interactive command** that prompts for a provider choice and runs
provider-readiness checks; it cannot be run unattended without `--provider <name>
--skip-provider-readiness`. The prototype's production setup path bypasses `gc init` entirely —
`pack.toml` and `city.toml` are authored directly. This is NEW-INFO operational context: no v4
spec references `gc init`; this fact is surfaced here so that any ops procedure or deployment guide
knows not to include `gc init` without these flags in an automated context.

**F12 — Deployment constraints: `IS_SANDBOX=1` for root + three onboarding dialogs must be pre-acked (NEW-INFO deployment constraint):**
Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
**Deployment constraint — root + permissions flag:** `claude --dangerously-skip-permissions`
refuses to run as root unless `IS_SANDBOX=1` is set in the environment. Container images running
as root must set this variable. **Deployment constraint — onboarding dialogs:** Interactive
`claude` presents three pre-run dialogs (theme picker, folder-trust, bypass-permissions warning)
that hang an agent session indefinitely if not pre-acknowledged. Pre-acknowledgement requires:
(a) `hasCompletedOnboarding: true`, `hasSeenWelcome: true`, `theme: "dark"` in
`~/.claude.json` (not `~/.claude/settings.json`); (b) `projects[path].hasTrustDialogAccepted:
true` and `bypassPermissionsModeAccepted: true` for every working directory an agent uses
(written by the entrypoint because paths are known only at runtime). These are production
requirements for any containerised Gas City deployment, not just sandbox quirks.
