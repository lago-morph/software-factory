# Gas City Config Anchor — Single Source of Truth for Sweep-2 Component Builders

**Purpose.** ONE shared "config anchor" that the 8 parallel Sweep-2 component builders cite so they
do NOT drift on Gas City config keys, file layout, or which "native" claims are verified vs unverified.
This is drift-prevention. If a builder needs a config key or a native-capability claim, it MUST come
from this doc with its grounded source; anything not grounded here is `[inferred — needs G11]`.

**Ground truth.** Every fact below is grounded against one of:
- The **harvest** — [`D-23-substrate-harvest.md`](./D-23-substrate-harvest.md), 12 facts (F1–F12) from the working prototype.
- The **prototype primary sources** — cloned `lago-morph/gascity-prototype@b14c278` (PLAN.md dated 2026-05-25), specifically:
  [`city.toml.example`](https://github.com/lago-morph/gascity-prototype/blob/b14c278/city.toml.example),
  [`pack/pack.toml`](https://github.com/lago-morph/gascity-prototype/blob/b14c278/pack/pack.toml),
  [`entrypoint.sh`](https://github.com/lago-morph/gascity-prototype/blob/b14c278/entrypoint.sh),
  [`docs/PLAN.md`](https://github.com/lago-morph/gascity-prototype/blob/b14c278/docs/PLAN.md),
  [`README.md`](https://github.com/lago-morph/gascity-prototype/blob/b14c278/README.md), and the
  post-v1.0.0 upstream-`gascity` walk [`docs/13-gas-city-deep-dive.md`](https://github.com/lago-morph/gascity-prototype/blob/b14c278/docs/13-gas-city-deep-dive.md) (read-only clone of `gastownhall/gascity@183897e`, the authoritative full config-key universe).
- The **Sweep-1 specs** — cited by component id (e.g. [C03](../spec/C03-config-feature-flags.md)).

**Verification-status vocabulary** (used in every table):
- `harvest-verified` — proven against the running prototype (cite F#) or read directly from a prototype primary-source file.
- `needs-pinned-gc-run (G11)` — named in v4/deep-dive but not exercised by the prototype's verified stand-up; the field shape must be confirmed against a pinned `gc` install before any spec writes config to it.
- `prevent-vs-detect-OPEN` — the enforcement-strength boundary the [D-23 spike](./D-23-gas-city-spike-protocol.md) owns; NOT resolved by any harvest.
- `[inferred — needs G11]` — not grounded in any primary source; flagged explicitly, never presented as fact.

---

## 1. Build & runtime facts

| Fact | Value | Source |
|---|---|---|
| Language / toolchain | **Go 1.26.3** (authoritative = `go.mod` of `gastownhall/gascity` at build time; prototype README's "Go 1.25" is stale, go.mod wins) | harvest known-fact; [spike protocol §1](./D-23-gas-city-spike-protocol.md) "verify `head -5 go.mod`"; PLAN.md §file-layout shows the 1.25 README artifact |
| Binary name | **`gc`** (built via `make install` → `/usr/local/bin/gc`) | PLAN.md §file-by-file ("`make install` → /usr/local/bin/gc") |
| Companion binary | **`bd`** (beads CLI; the bead store is driven through it) | prototype `pack/pack.toml` header; PLAN.md item 1 |
| Pin / commit | prototype `lago-morph/gascity-prototype@b14c278` (PLAN dated 2026-05-25); upstream SDK `gastownhall/gascity@183897e` (post-v1.0.0, PackV2) | harvest provenance; deep-dive §provenance |
| Verified-working branch | `claude/great-pascal-RUfkN` (merged at `b14c278`) | PLAN.md §status; [spike protocol §1](./D-23-gas-city-spike-protocol.md) |
| What "install" means | Author `pack.toml` + `city.toml` **directly** and run `gc start --foreground`. The prototype does **NOT** run `gc init` in production flow (it is interactive — F4). Binaries (`gc`, `bd`, `dolt`, node/claude) are pre-staged on the host and `COPY`'d into the image because the sandbox TLS-inspection proxy blocks in-container downloads (F-context, PLAN item 1). | F4; PLAN.md items 1–2 |
| Controller process | **`gc start --foreground`** — the supervisor (PID 7 in-container, tini as PID 1 for zombie reaping). Reconciles desired-vs-running agents, reaps dead sessions, fires due orders. | F6; PLAN.md item 6 |
| Root + permissions | `claude --dangerously-skip-permissions` refuses root unless `IS_SANDBOX=1`; 3 onboarding dialogs must be pre-acked in `~/.claude.json` (NOT `~/.claude/settings.json`). | F12; PLAN.md items 7–8 |

---

## 2. Config file layout

Three files participate. **Getting the right key into the right file is the #1 drift hazard** (PackV2
is strict and *refuses startup* on misplaced keys — F1, F3).

| File | What lives here | What must NOT live here |
|---|---|---|
| **`pack.toml`** (root pack manifest) | `[pack] name`, `[pack] schema = 2`; `[imports.<name>]` with `source = "github.com/…//path"`; pack-shipped `[[tool]]`, prompt templates, formulas. | `[defaults.rig.imports.*]` (→ `city.toml` per F3). A **direct** `[imports.maintenance]` when `gastown` already imports it transitively (duplicate `gastown.dog` agent ⇒ startup refusal — F3). |
| **`city.toml`** (workspace install) | `[workspace]` (name, provider, global_fragments); `[defaults.rig.imports.<name>]`; capability sections `[daemon]`, `[beads]`, `[orders]`, `[mail]`, `[formulas]`, `[[service]]`; `[[agent]]` worker decls; **`[[rig]]`/`[[rigs]]` partition/role blocks carrying `name` + `prefix` but NO `path`** (see §3 spelling note) — **D-31: one city hosts MULTIPLE rigs; this is an ARRAY of N rig entries, not a singleton; specs MUST NOT assume one-rig-per-city** (see §3 D-31 note). | A rig **`path`** field — path bindings are machine-local and live in `.gc/site.toml` (F1). `convergence.max_iterations` (not a real field — F2). |
| **`.gc/site.toml`** (machine-local, entrypoint-written) | `workspace_name`; **`[[rig]]` (singular) blocks carrying `name` + `path`** — the actual `/workspace/rigs/<name>/` filesystem bindings. Written by the entrypoint at container-start because only it knows runtime paths. | Partition/role semantics, prefixes (those are city.toml's job). This file is `.gitignore`d (machine-local). |

**`.gc/` directory** (deep-dive §6) also holds: `events.jsonl` (the event stream), controller socket/pidfile/lock, bead-store working files, molecule artifact dirs, materialized pack imports (`.gc/imports/`), deferred-nudge queue (`.gc/nudges/`).

---

## 3. Canonical config-key table

> **[D-31 ADOPTED 2026-06-01 — Multiple rigs per city.]**
> "A *city* (one Gas City install / the `gc` substrate, C01) hosts **multiple rigs** (C42) — not one.
> The `[[rig]]`/`[[rigs]]` array-of-tables declares N rig partitions inside a single city;
> **rig partitioning (C42) is the isolation of these N co-resident rigs from one another** (e.g. a
> worker rig and a separate judge rig living in the same city — the D-17 holdout read-surface depends
> on worker-rig ≠ judge-rig). Specs MUST model multiple-rigs-per-city explicitly and MUST NOT assume
> one-rig-per-city."
> — review-log D-31 (Sweep-2 spine-run decisions, 2026-06-01)
>
> The `[[rig]]`/`[[rigs]]` section in `city.toml` is therefore an **ARRAY** (N entries); builders must
> author one block per rig role (worker, judge, scenario-author). The D-17 holdout design (worker-rig ≠
> judge-rig) requires at least two rig blocks in a Phase-2 city.toml. Do NOT collapse to a single rig block.

> **DRIFT-CRITICAL SPELLING NOTE (read before using `[[rig]]`).** The harvest's F1 states "canonical
> spelling is `[[rig]]` (singular)". The prototype **primary sources show the spelling is
> file-dependent**, and builders MUST honour the split:
> - **`.gc/site.toml`** uses **`[[rig]]`** (singular) with `name` + `path` — verbatim in
>   [`entrypoint.sh`](https://github.com/lago-morph/gascity-prototype/blob/b14c278/entrypoint.sh) lines 70–76.
> - **`city.toml`** in the prototype uses **`[[rigs]]`** (plural) with `name` + `prefix` (no path) —
>   verbatim in [`city.toml.example`](https://github.com/lago-morph/gascity-prototype/blob/b14c278/city.toml.example) lines 49–56.
>
> F1's normative ruling and the v4 specs (C01/C03/C42) adopt **`[[rig]]`** as the *canonical* city.toml
> spelling; the running prototype's `city.toml.example` uses `[[rigs]]`. The invariant that **holds in
> both** and is the real anti-drift rule: **a rig `path` belongs ONLY in `.gc/site.toml`; `city.toml`
> rig blocks carry `prefix`/partition/role and never `path`.** Whether the city.toml block is spelled
> `[[rig]]` or `[[rigs]]` is **`needs-pinned-gc-run (G11)`** — the prototype example and F1 disagree;
> do NOT silently pick one. (→ orchestrator ledger; see §"Contradiction" in the receipt.) The
> `[[rigs]] path =` form is unambiguously a PackV2 ERROR (F1).

| Key / Block | File | Meaning | Source (F# / spec / prototype path) | Verification status |
|---|---|---|---|---|
| `[workspace] name` | city.toml | City identity | `city.toml.example:9` | harvest-verified |
| `[workspace] provider = "claude"` | city.toml | City-default session provider preset | `city.toml.example:10`; [C03](../spec/C03-config-feature-flags.md):99 | harvest-verified |
| `[workspace] global_fragments = [...]` | city.toml | Prompt fragments injected city-wide | `city.toml.example:11` | harvest-verified |
| `[[agent]] provider = "claude"` | city.toml | Declares a Claude worker (the LLM-backed agent) | known-fact; `city.toml.example` (workspace.provider); deep-dive Level 0-1; [C03](../spec/C03-config-feature-flags.md):99, [C05](../spec/C05-sling-dispatch.md):11 | harvest-verified |
| `[[agent]] env = { … }` | city.toml | Per-agent env (OTEL/telemetry); innermost override | [C03](../spec/C03-config-feature-flags.md):85,104; deep-dive | needs-pinned-gc-run (G11) for exact keys |
| `[agent_defaults]` | city.toml | City-level defaults for `provider`, `wake_mode`, `default_sling_formula` (some fields parsed-but-not-applied tombstones) | deep-dive §config table:325 | needs-pinned-gc-run (G11) |
| `[beads] provider = "file"` | city.toml | File-backed bead store (Phase-0) | known-fact; [C03](../spec/C03-config-feature-flags.md):100; [C01](../spec/C01-gas-city-substrate.md):137 | harvest-verified |
| `[beads] provider = "bd"` | city.toml | Dolt-backed bead store via `bd` binary (prototype's actual setting) | `city.toml.example:32-36`; deep-dive:310 | harvest-verified (F9 Dolt path) |
| `[beads] provider` other values | city.toml | `"exec:<script>"` also accepted | deep-dive:310 | needs-pinned-gc-run (G11) |
| bead **prefix** (`prefix = "r1"`) | city.toml (rig block) | Per-rig bead-ID prefix; the scoping MECHANISM. Explicit value REQUIRED — `rig1`/`rig2` both auto-derive `"ri"` and collide | F10; `city.toml.example:50-56`; README:156 | harvest-verified (mechanism); **prevent-vs-detect-OPEN** (enforcement strength) |
| `[session] provider` | city.toml | Provider-kind: `""`/tmux (default), `"fake"`, `"subprocess"`, `"exec:<script>"`, `"k8s"` | deep-dive:311; F7 (tmux is Phase-0 kind) | harvest-verified that **Phase-0 kind = tmux** (F7); other kinds needs-pinned-gc-run (G11) |
| Provider-kind = **tmux** | (runtime) | Each agent = one interactive `claude` process in its own tmux pane under one tmux server, managed by `gc start` | F7; README §physical view | harvest-verified |
| `[daemon]` | city.toml | Health-patrol/controller loop: `patrol_interval`, `max_restarts`, `restart_window`, `shutdown_timeout`, `wisp_gc_interval`, `wisp_ttl`, `formula_v2` | `city.toml.example:18-30`; deep-dive:316 | harvest-verified (field names present in prototype) |
| `[orders] max_timeout` / `skip` | city.toml | Order scheduling: global timeout + skip-list filters | `city.toml.example:38-40`; deep-dive:317 | harvest-verified (`max_timeout` set in prototype) |
| `[mail] provider = "beadmail"` | city.toml | Messaging on; `"beadmail"` default (mail = beads with `type="message"`) or `"exec:<script>"` | deep-dive:312,774-776; [C03](../spec/C03-config-feature-flags.md):44 | needs-pinned-gc-run (G11) — present in deep-dive, NOT enabled in prototype city.toml |
| `[events] provider` | city.toml | Event stream: file JSONL (default, `.gc/events.jsonl`), `"fake"`, `"fail"`, `"exec:<script>"` | deep-dive:313,281 | needs-pinned-gc-run (G11) |
| `[formulas]` (+ `dir`) | city.toml | Formula DAG composition on; presence is the flag, content is C12 | deep-dive:314,337; [C03](../spec/C03-config-feature-flags.md):102 | needs-pinned-gc-run (G11) — not enabled in prototype |
| `formula` / `molecule` | (work model) | A **molecule** is a formula instantiated at runtime: root bead `type="molecule"` + one child bead per step. A **wisp** is an ephemeral molecule with a TTL. | deep-dive:590-605,1232-1233 | harvest-verified (from deep-dive primary source) |
| `[defaults.rig.imports.<name>]` (`source =`) | city.toml | Per-rig pack import (e.g. gastown rig-scoped agents). MUST be in city.toml, not pack.toml | F3; `city.toml.example:15-16` | harvest-verified |
| `[pack] name` / `[pack] schema = 2` | pack.toml | Root pack identity + PackV2 schema version | `pack/pack.toml:`; deep-dive (PackV2) | harvest-verified |
| `[imports.<name>] source = "github.com/…//path"` | pack.toml | Import a bundled pack (resolved from embedded FS, no network) | `pack/pack.toml`; F3 | harvest-verified |
| `[[rig]]` (`name`, `path`) | **.gc/site.toml** | Machine-local rig filesystem binding (entrypoint-written) | F1; `entrypoint.sh:70-76` | harvest-verified |
| `[[rigs]]` / `[[rig]]` (`name`, `prefix`) | **city.toml** | Rig partition/role + prefix declaration (NO path) | F1 (canonical `[[rig]]`); `city.toml.example:49-56` (prototype `[[rigs]]`) | **city.toml spelling needs-pinned-gc-run (G11)** — F1 vs prototype disagree (see spelling note) |
| `[[rig]] read_partition` / `write_partition` | city.toml | Rig/agent-role partition labels (C42) | [C03](../spec/C03-config-feature-flags.md):105; [C42](../spec/C42-rig-partitioning.md):133,253; AI-CONTEXT §13.3 | needs-pinned-gc-run (G11) — named by v4, not in prototype example; concrete TOML grammar is [C42:OQ](../spec/C42-rig-partitioning.md):376 |
| `[[service]]` (twin) | city.toml / pack.toml | Workspace HTTP service mounted on controller edge under `/svc/{name}`; the C44 twin packaging target | deep-dive:131,323; [C03](../spec/C03-config-feature-flags.md):103; [C02](../spec/C02-pack-extension-abi.md):158 | needs-pinned-gc-run (G11) — **D-23 spike Test B target** ([protocol §4](./D-23-gas-city-spike-protocol.md)); schema unverified |
| `[[tool]]` (`name`, `cmd`, `args` w/ `{placeholder}`) | pack.toml | Deterministic tool-node the pack ships; args substituted from bead/molecule context | [C02](../spec/C02-pack-extension-abi.md):117-120; AI-CONTEXT §13.3 | needs-pinned-gc-run (G11) |
| Orders durability | (runtime) | Bead state survives controller crash because work lives in the bead store; container-death durability rests on dolt push cadence | F6 (fires due orders); F8/README ("source of truth"); deep-dive | needs-pinned-gc-run (G11) — **D-23 spike Test C target** ([protocol §5](./D-23-gas-city-spike-protocol.md)); crash-resume granularity unverified |
| `[autonomy]` block | — | **No such Gas City config block exists.** Autonomy in v4 is the [C56 autonomy-ladder](../spec/C56-autonomy-ladder.md) (a policy construct), not a `gc` config section. Zero hits in prototype or deep-dive. | grep of prototype + deep-dive (none); [C56](../spec/C56-autonomy-ladder.md) | `[inferred — needs G11]` — do NOT emit an `[autonomy]` TOML block |
| `[convergence]` (e.g. `max_iterations`) | city.toml | Convergence-loop limits section EXISTS (deep-dive), but `convergence.max_iterations` is **NOT a real field** (F2) | deep-dive:318; F2 (the specific field is rejected) | section: needs-pinned-gc-run (G11); `max_iterations` field: **harvest-verified NON-existent** (do not use) |
| `[dolt]`, `[api]`, `[chat_sessions]`, `[session_sleep]`, `[doctor]`, `[[pricing]]` | city.toml | Additional upstream sections (dolt overrides, HTTP API, chat auto-suspend, idle-sleep, gc-doctor, per-model pricing) | deep-dive §config table:316-326 | needs-pinned-gc-run (G11) — not exercised by prototype stand-up |
| `DOLT_REF=refs/heads/dolt-data` | .env / env | Dolt push/clone ref; default `refs/dolt/data` is rejected by proxies | F9; `.env.example`; `entrypoint.sh:108-111` | harvest-verified |
| `IS_SANDBOX=1` | env | Required for `claude --dangerously-skip-permissions` as root | F12 | harvest-verified |

---

## 4. Native-claim → verification-status table

One row per "Gas City does X natively" claim. **A builder may rely on a `harvest-verified` claim as a
substrate primitive; a `needs-pinned-gc-run (G11)` claim must be treated as design-against-unverified;
a `prevent-vs-detect-OPEN` claim must NOT be assumed to enforce.**

| Native claim | Component(s) | Status | Conformance test that discharges it |
|---|---|---|---|
| **Beads store** (durable typed work-graph) | C19, C20 | harvest-verified (F8, F9): Dolt SQL server in-container, `bd` CLI, agents read/write through it | `bd create` / `bd ls` / `bd get` round-trip on a rig ([spike §2 smoke-signal](./D-23-gas-city-spike-protocol.md)) |
| **Event bus / stream** | C23 | needs-pinned-gc-run (G11): deep-dive shows `[events] provider` → `.gc/events.jsonl`; prototype README cites "logs lifecycle into the event stream" but the stream was not exercised end-to-end | `gc events --follow` shows agent-lifecycle + bead events ([spike §2](./D-23-gas-city-spike-protocol.md)) |
| **Attribution (`created_by` / provenance)** | C41, C04 | needs-pinned-gc-run (G11): deep-dive shows `gc config explain --provenance` (config-field provenance) and bead fields `From`/`Assignee`; a literal `created_by` field is **`[inferred — needs G11]`** (not found verbatim). `session.id` is the attribution key per [C04](../spec/C04-session-provider.md):53 | inspect a bead's author/provenance fields against pinned `gc`; confirm whether `created_by` is the real field name |
| **Rig partitioning** | C42, C34, C43 | harvest-verified that **prefix is the scoping mechanism** (F10) + rigs register (F11); `read_partition`/`write_partition` TOML grammar is needs-pinned-gc-run (G11) | `[[rig]]` partition validation at config-load; cross-rig bead visibility probe ([spike Test A1](./D-23-gas-city-spike-protocol.md)) |
| **Durable Orders** | C40 | needs-pinned-gc-run (G11): controller "fires due orders" verified (F6); crash-resume granularity / retry bound / container-death durability NOT verified | kill controller + kill container mid-order; observe bead-state survival + resume granularity ([spike Test C](./D-23-gas-city-spike-protocol.md)) |
| **Reconciler / health-patrol** | C18, C56(deacon) | harvest-verified (F6): `gc start` reconciles desired-vs-running, reaps dead sessions; `[daemon]` patrol cadence present (F11 deacon ran) | restart a dead pane; observe controller reconcile it back ([spike §2](./D-23-gas-city-spike-protocol.md)) |
| **Sling / dispatch** | C05 | harvest-verified (F5, F8): `gc sling` dispatches a bead; worker pool `min=0` scales 0→1 on dispatch (new tmux pane) | `gc sling <bead>` spawns a worker pane; pool returns to 0 idle ([spike §2](./D-23-gas-city-spike-protocol.md)) |
| **Sessions / provider runtime** | C04 | harvest-verified (F7): Phase-0 provider-kind = tmux; each agent = one interactive `claude` pane; `gc session list` exists | `gc session list` shows named agent panes; restart-on-death observed |
| **Formula + molecule** | C12, C13 | harvest-verified definitionally (deep-dive: molecule = formula-as-beads, wisp = TTL molecule); `[formulas]` execution NOT enabled in prototype | enable `[formulas]`; `gc sling --formula <name>` cooks a molecule (root + step beads) |
| **Messaging (Mail / Nudge)** | C06 | needs-pinned-gc-run (G11): deep-dive shows Mail = beads `type="message"` (`[mail] provider="beadmail"`), Nudge = `runtime.Provider.Nudge` typing into a session (deferrable to `.gc/nudges/`); NOT enabled in prototype city.toml. F8 confirms agents coordinate THROUGH beads (write/poll), not directly | enable `[mail]`; `gc mail send`/`inbox` round-trip; `gc session nudge` delivers to a pane |
| **Partition ENFORCEMENT (prevent vs detect)** | C34, C43 | **prevent-vs-detect-OPEN** (F10): prefix is the mechanism; whether `gc`/`bd`/OS PREVENTS out-of-prefix access or merely scopes-by-convention is UNVERIFIED | [spike Test A1/A2](./D-23-gas-city-spike-protocol.md): `bd get r2-…` from rig1 cwd; `cat ../rig2/…` — capture exit code, data-returned, in-audit-trail |

---

## 5. Prevent-vs-detect status

State plainly, so no builder treats partition scoping as enforcement:

- **Prefix is the MECHANISM** (F10): a worker dispatched to rig1 sees/creates only `r1-` beads;
  `gp-`/`r1-`/`r2-` partition city/rig1/rig2. This is *confirmed*.
- **Enforcement STRENGTH is UNTESTED.** The prototype never ran the end-to-end smoke test that would
  probe whether `gc`/`bd` (or the OS sandbox) *refuses* an out-of-prefix access, or merely *permits and
  logs* it. F10 marks this boundary explicitly OPEN; the harvest does NOT close it.
- **D-30 (operator-adopted, 2026-06-01) REQUIRES prevent for unattended.** It is the binding gate:
  prevention (native or via a sanctioned-but-deferred enforcement watcher) MUST exist before unattended
  operation. Until then, unattended is human-in-the-loop. (See [review-log D-30](./review-log.md) and the
  [auto-001 decision brief](./decisions/auto-001-detect-only-binding-gate.md).)
- **The empirical D-23 spike is the resolver and is OWED.** It needs Docker (the prototype is not
  runnable without it) and has not been executed — operator deferred live-agent token burn this session.
  Test A1 (bead-layer) and Test A2 (OS/Bash-layer) jointly decide PREVENT / DETECT-ONLY / SILENT and
  route the `auto-001` binding gate. See the [D-23 spike protocol](./D-23-gas-city-spike-protocol.md).

The adopted D-30 requirement, verbatim:

> unattended operation (P2) and self-modification (P3b) require the substrate to BLOCK (prevent at the tool-call/process boundary) — not merely detect — out-of-boundary access on the relevant blast-radius face.

— [review-log D-30](./review-log.md) / [auto-001 brief](./decisions/auto-001-detect-only-binding-gate.md); replicated in
[C34](../spec/C34-holdout-integrity.md):443, [C43](../spec/C43-isolation-boundary.md):457,
[C42](../spec/C42-rig-partitioning.md):412, [C56](../spec/C56-autonomy-ladder.md):385,
[C57](../spec/C57-failure-mode-coverage.md):422.

**Builder rule:** do NOT write any spec text that assumes the bead prefix *enforces* (refuses) cross-partition
access. Cite this section and the [D-23 spike](./D-23-gas-city-spike-protocol.md) as the open resolver; if a
component needs enforcement before P2, it depends on the prevent gate, not on prefix scoping.
