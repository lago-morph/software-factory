# D-23 Substrate Harvest — Gas City Prototype Empirical Evidence Map

**Purpose.** Maps each substrate fact the Gas City prototype empirically proved → the affected v4
spec(s)/open-question(s) → a verdict → a precise proposed annotation. Lets the lead agent fold
verified-against-real-`gc` facts into the corpus and close OQs.

**Prototype provenance.** Repo `lago-morph/gascity-prototype`, default-branch tip commit `b14c278`,
PLAN.md dated 2026-05-25. Every fact below cites this source. Internal docs referenced:
[`docs/PLAN.md`](https://github.com/lago-morph/gascity-prototype/blob/b14c278/docs/PLAN.md) (primary evidence) and
[`README.md`](https://github.com/lago-morph/gascity-prototype/blob/b14c278/README.md) (physical/logical/flow views).

---

## Contradictions — LEAD-VERIFIED 2026-06-01: 0 TRUE CONTRADICTIONS

The harvest subagent flagged F2/F4/F9 as `CONTRADICTS-CLAIM` (a v4 spec makes/implies a claim the
prototype disproves). The lead agent verified each against the **actual** v4 spec text and found
**none of them contradicts v4** — all three are reclassified `NEW-INFO` (operational caveats /
candidate-eliminations). The v4 corpus's discipline of deferring unverified substrate field names to
G11 verification held up. (This is a morning-summary headline: a panel-flagged risk class produced
zero spec-correctness bugs.)

| # | Fact summary | Affected spec(s) | Lead verification (grep of actual v4 text) | Reclassified |
|---|---|---|---|---|
| F2 | `convergence.max_iterations` is **not a real `gc` field** | C18, C39 | C18 §3.2 / C39 explicitly **defer** the numeric policy to **C20 schema slots** (`max_attempts`) + pinned-`gc` G11 verification; they never assert a `convergence.*` config field. The finding *confirms* that prudence and eliminates one candidate field name. | `NEW-INFO` |
| F4 | `gc init` is interactive; production authors config directly | C03, C04 | **Zero** references to `gc init` anywhere in v4 specs/AI-CONTEXT/README/plan-faithful. No opposing claim exists. | `NEW-INFO` (ops caveat) |
| F9 | Dolt push needs `--ref refs/heads/*` via proxy | C19, C41 | **Zero** references to dolt refs in v4 specs. No claim that the default works. Caveat is proxy/CI-specific. | `NEW-INFO` (portability caveat) |

> **Per-fact entries below retain the subagent's original `(d) Verdict` for traceability, each
> annotated `[LEAD-RECLASSIFIED → NEW-INFO 2026-06-01]`. There remain no `CONTRADICTS-CLAIM` facts
> after lead verification.**

---

## Per-Fact Entries

---

### F1 — `[[rig]]` path bindings live in `.gc/site.toml`, not in `[[rigs]] path=` in `city.toml`

**(a) Fact.** The `gc` PackV2 schema places rig path bindings in `.gc/site.toml` as `[[rig]]`
entries (singular), and rejects `[[rigs]] path =` in `city.toml`; `city.toml` uses `[[rig]]` blocks
for partition/role declarations without a `path` field.

**(b) Evidence.**

> "`[[rigs]] path =` is rejected — path bindings live in `.gc/site.toml` as `[[rig]]` entries
> (singular). … The entrypoint owns writing site.toml because it knows the actual
> `/workspace/rigs/<name>/` paths."

— `docs/PLAN.md` §"Things this build had to figure out", item 3
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C42 / C42:OQ-4 / XC-9 / C01 / C03

**(d) Verdict.** `RESOLVES-OQ`

**(e) Proposed annotation.** Add to C42 §9 (OQ-C42-4) and the XC-9 entry in review-log:

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> the canonical spelling is `[[rig]]` (singular). `[[rigs]] path =` is a PackV2 validation error;
> path bindings for a rig's working directory live in `.gc/site.toml` as `[[rig]]` entries, written
> at container-start time by the entrypoint (which knows the runtime filesystem paths). `city.toml`
> carries `[[rig]]` blocks for partition/role semantics only, without a `path` field. This resolves
> XC-9 in favour of `[[rig]]` and makes the spelling in C01/C03/C42 canonical.

**(f) Disposition.** `safe-to-apply`

---

### F2 — `convergence.max_iterations` is not a real `gc` field

**(a) Fact.** PackV2 strictness rejects `convergence.max_iterations`; it is not a valid field in any
`gc` config file (city.toml or pack.toml).

**(b) Evidence.**

> "`convergence.max_iterations` isn't a real field."

— `docs/PLAN.md` §"Things this build had to figure out", item 3
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C18 (convergence loop, INV-2 bound), C39 (numeric
termination policy, G18), C03 (config feature flags)

**(d) Verdict.** ~~`CONTRADICTS-CLAIM`~~ **`NEW-INFO`** `[LEAD-RECLASSIFIED → NEW-INFO 2026-06-01]` — C18/C39 never assert a `convergence.*` field; they defer the numeric policy to C20 schema slots + G11. The finding eliminates one candidate field name; it does not contradict v4.

**(e) Proposed annotation.** Add to C18 §9 (OQ) and C39 §9 (OQ1):

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> `convergence.max_iterations` is **not** a real `gc` config field — PackV2 strict-mode rejects it.
> Any v4 text implying this is the config knob for bounded convergence is incorrect. The actual
> mechanism by which `gc` expresses a per-pass bound is **unverified** (G11/G18 remain open); C39's
> numeric termination policy cannot bind to this field name. Sweep-2 must identify the real field
> shape from a pinned `gc` install before C39 writes any config.

**(f) Disposition.** `needs-lead-review`

---

### F3 — Pack loading, import strictness, and `[defaults.rig.imports.*]` placement

**(a) Fact.** Packs load via `gc import install`; `[imports.gastown]` belongs in `pack.toml`;
`[defaults.rig.imports.*]` must be in `city.toml`, not `pack.toml`; importing `maintenance`
directly (when `gastown` already imports it transitively) creates a duplicate `gastown.dog` agent
and causes startup refusal.

**(b) Evidence.**

> "PackV2 strictness: `[defaults.rig.imports.*]` must live in `city.toml`, not `pack.toml`. …
> **Don't import `maintenance` directly** — the bundled `gastown` pack already imports it
> transitively. Adding our own `[imports.maintenance]` creates a duplicate `gastown.dog` agent and
> refuses startup."

— `docs/PLAN.md` §"Things this build had to figure out", items 3 and 5
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C02 (pack extension ABI, pack-on-disk layout), C02:OQ
(C28:OQ-4, pack-level contract), C28:OQ-4, C03 (config layering / merge order)

**(d) Verdict.** `NEW-INFO`

**(e) Proposed annotation.** Add to C02 §9 (OQs) and to C03 §6:

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> (a) `[defaults.rig.imports.*]` entries must live in `city.toml`, not `pack.toml` — PackV2 rejects
> them in a pack manifest. (b) Transitive imports are de-duplicated at startup: if pack A imports
> pack B transitively, the city must NOT also declare `[imports.B]` directly — doing so produces a
> duplicate agent definition and refuses startup. Pack authors should document transitive imports
> explicitly so city authors know not to re-import them. C02's pack-on-disk layout and C03's
> layering/merge-order sections should reflect these two constraints.

**(f) Disposition.** `safe-to-apply`

---

### F4 — `gc init` is interactive; production workflow authors config files directly

**(a) Fact.** `gc init` prompts interactively for a provider and runs provider-readiness checks;
it cannot be used unattended. The production workflow for the prototype is to author `pack.toml` and
`city.toml` directly without ever calling `gc init`.

**(b) Evidence.**

> "**`gc init` is interactive** and asks for a provider; bypass with `gc init --provider claude
> --skip-provider-readiness`. We don't run `gc init` at all in production flow — `pack.toml` +
> `city.toml` are authored directly."

— `docs/PLAN.md` §"Things this build had to figure out", item 2
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C03 (config feature flags / layered config authoring),
C04:OQ-4 (provider-kind selection, inferred config-driven)

**(d) Verdict.** ~~`CONTRADICTS-CLAIM`~~ **`NEW-INFO`** `[LEAD-RECLASSIFIED → NEW-INFO 2026-06-01]` — no v4 spec references `gc init` at all (grep-verified), so there is no claim to contradict; this is a deployment ops caveat.

**(e) Proposed annotation.** Add to C03 §6 and C04 §9:

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> `gc init` is an **interactive command** that prompts for a provider choice and runs
> provider-readiness checks; it cannot be run unattended without `--provider <name>
> --skip-provider-readiness`. The prototype's production setup path bypasses `gc init` entirely —
> `pack.toml` and `city.toml` are authored directly. Any v4 spec or ops procedure that calls
> `gc init` without these flags in an automated context will hang waiting for input.

**(f) Disposition.** `needs-lead-review`

---

### F5 — Worker/dog pool min=0; scales on demand for cost discipline

**(a) Fact.** Worker agent pools (including the `dog` role) run with a minimum pool size of 0 and
scale up on demand; the coordinator calls `gc sling` to dispatch a task which causes the controller
to spawn a worker pane, keeping idle costs at zero.

**(b) Evidence.**

> "worker pool was at 0 (cost discipline); now scales to 1 — new tmux pane, fresh `claude` process,
> cwd = rig1's dir"

— `README.md` §"Flow view — how a piece of work moves through the system", step ③
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

Also, from the gastown pack design:

> "Cap pool sizes sensibly. Watch for runaway agent fan-out."

— `docs/PLAN.md` §"Order of execution", step 8
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C05 (sling dispatch, pool sizing), C05:OQ-2 (pool
member-selection policy), C05:OQ-3 (back-pressure)

**(d) Verdict.** `CONFIRMS-CLAIM`

**(e) Proposed annotation.** Add to C05 §6 or §9:

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> worker pools operate with `min=0` — no worker claude processes run at idle. When the coordinator
> dispatches a task via `gc sling`, the controller spawns a new tmux pane with a fresh `claude`
> process on demand. This is the literal cost-discipline mechanism: pool scales 0→1 on dispatch,
> returns to 0 when idle (health-patrol scales it back). C05:OQ-2 (member-selection policy) remains
> open; the verified fact is only that min=0 and on-demand spawn is the observed behaviour.

**(f) Disposition.** `safe-to-apply`

---

### F6 — Controller = `gc start --foreground`; reconciles desired-vs-running, reaps dead sessions, fires due orders

**(a) Fact.** The Gas City controller process is `gc start --foreground`; it reconciles the desired
set of agents against the running set, reaps dead sessions, and fires due orders — directly
analogous to Erlang/OTP supervisor behaviour.

**(b) Evidence.**

From the README physical view:

> "PID 7: gc start --foreground (the controller)"

From the vocabulary primer:

> "**Controller** | The supervisor process (`gc start`) that watches the desired set of agents and
> brings them up / restarts them / scales the pools."

From the logical view:

> "Controller (gc start) - reconciles desired vs running agents - fires due orders - reaps dead
> sessions"

— `README.md` §"Vocabulary primer" and §"Physical view" and §"Logical view"
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

Also from entrypoint flow:

> "exec gc start --foreground"

— `docs/PLAN.md` §"Entrypoint flow"
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C04 (session provider runtime), C18 (reconciler /
Health Patrol loop), C40 (durable orders)

**(d) Verdict.** `CONFIRMS-CLAIM`

**(e) Proposed annotation.** Add to C04 §6 and C18 §6:

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> the Gas City controller is the process started by `gc start --foreground`; it runs as PID 7
> in the prototype container (with tini as PID 1 for zombie reaping — see F12). Its three
> observed duties are: (1) reconcile desired-vs-running agents (bring up missing, restart dead);
> (2) reap dead sessions; (3) fire due orders. This is the concrete realisation of C18's
> "per-tick desired-state convergence" and C40's "durable orders" mechanisms as a single
> Erlang/OTP-style supervisor process.

**(f) Disposition.** `safe-to-apply`

---

### F7 — Each agent = an interactive `claude` process in its own tmux pane

**(a) Fact.** Every agent role (coordinator, health-patrol, bootstrap, workers, per-rig observers)
runs as a separate interactive `claude` process in its own tmux pane inside the container, managed
by a single tmux server.

**(b) Evidence.**

> "Each agent role gets its own tmux pane running an interactive `claude` process. The controller
> watches the panes and restarts dead ones."

— `README.md` §"Physical view — what runs where", Notes
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

Also the physical diagram shows explicitly:
> "pane: coordinator agent ← claude process / pane: health-patrol agent ← claude / pane: bootstrap
> agent ← claude / pane: worker pool member ← claude (×N)"

— `README.md` §"Physical view"
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C04:OQ-4 (Provider-kind = tmux, selection criterion)

**(d) Verdict.** `RESOLVES-OQ`

**(e) Proposed annotation.** Add to C04 §9 (OQ4):

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> the Phase-0 Provider-kind is **tmux**. Each agent (coordinator, health-patrol, bootstrap,
> per-rig observers, worker pool members) runs as a separate interactive `claude` process in its own
> tmux pane, all within a single tmux server named after the city. The controller manages the panes
> and restarts dead ones. This is the concrete realisation of C04's tmux Provider and resolves
> C04:OQ-4: the Phase-0 selection criterion is tmux, config-driven, as the spec inferred.

**(f) Disposition.** `safe-to-apply`

---

### F8 — Agents coordinate THROUGH beads (write→poll), not directly

**(a) Fact.** Inter-agent coordination is exclusively via bead writes and polls; agents do not
communicate directly with each other. When the coordinator wants the reviewer to act, it writes a
bead; the reviewer's prompt tells it to poll for beads addressed to it.

**(b) Evidence.**

> "**Agents talk through beads, not directly.** When the coordinator wants the reviewer to look at
> something, it writes a bead; the reviewer's prompt tells it to poll for beads addressed to it."

— `README.md` §"Logical view — what's connected to what", Notes
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

Also from the flow view:

> "② Coordinator notices — polls beads via its tmux prompt — sees an open bead in rig1's scope,
> decides to dispatch — calls `gc sling r1-abc` to route it to the worker pool"

— `README.md` §"Flow view"
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C05 (sling dispatch), C06 (agent messaging)

**(d) Verdict.** `CONFIRMS-CLAIM`

**(e) Proposed annotation.** Add to C06 §6:

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> all inter-agent coordination passes through the bead store — agents write beads and recipients
> poll for beads addressed to them. No agent-to-agent direct channel (e.g. tmux send-keys to another
> pane) was observed or needed. This confirms that the bead store is the sole coordination medium
> and that C06's messaging contract must be implemented as bead operations, not as a separate
> transport.

**(f) Disposition.** `safe-to-apply`

---

### F9 — Bead store = local Dolt SQL server; durability via periodic `dolt push`; `refs/heads/*` required

**(a) Fact.** The bead store runs as a local Dolt SQL server inside the container; durability is
achieved by periodic `dolt push` to a GitHub git-remote. The dolt push **requires** the
`--ref refs/heads/*` flag because the default `refs/dolt/data` namespace is rejected by some git
proxies (and by the Anthropic sandbox proxy specifically).

**(b) Evidence.**

> "**Dolt push/clone to beadstore** — verified end-to-end. Caveat: the proxy only allows pushes to
> `refs/heads/*`, so dolt must use `--ref refs/heads/dolt-data` (not its default `refs/dolt/data`)."

— `docs/PLAN.md` §"Risk verification results (2026-05-25)", item 2
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

> "**Dolt git-remote needs an explicit ref** because the sandbox proxy only allows pushes to
> `refs/heads/*`. Use `--ref refs/heads/dolt-data` (set as `DOLT_REF` in env)."

— `docs/PLAN.md` §"Things this build had to figure out", item 10
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

> "The bead store is a real database. Dolt runs a local SQL server inside the container; the agents
> and the controller all read/write through it. Periodically the database is `dolt push`ed up to the
> beadstore repo for durability."

— `README.md` §"Physical view — what runs where", Notes
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C19 (bead work-graph, Dolt backend), C20 (bead schema),
C21 (CXDB trajectory store), C23 (event bus), C41 (identity attribution)

**(d) Verdict.** ~~`CONTRADICTS-CLAIM`~~ **`NEW-INFO`** `[LEAD-RECLASSIFIED → NEW-INFO 2026-06-01]` — no v4 spec references dolt refs (grep-verified); there is no claim that the default works. This is a portability/ops caveat for proxy-mediated git (sandbox/CI), not a v4 correction. The `refs/heads/*` form is the portable configuration.

**(e) Proposed annotation.** Add to C19 §5 (operational notes) and C19 §9 (OQs):

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> the Dolt bead store backend runs as a **local Dolt SQL server** inside the container; durability
> is achieved by periodic `dolt push` to a GitHub git-remote repository. **Critical operational
> constraint:** `dolt push` must use `--ref refs/heads/<branch>` (e.g. `refs/heads/dolt-data`).
> Dolt's default push namespace `refs/dolt/data` is rejected by many git proxies and by the
> Anthropic sandbox proxy; specifying `refs/heads/*` is the portable, proxy-compatible form. Any
> deployment guide or ops runbook that uses the default dolt ref will fail in proxy-mediated
> environments. Set `DOLT_REF=refs/heads/dolt-data` in env and pass `--ref $DOLT_REF` to all dolt
> push/clone operations.

**(f) Disposition.** `needs-lead-review`

---

### F10 — Bead scope enforced by bead PREFIX; explicit `prefix=` required to avoid collision

**(a) Fact.** Bead scope per rig is enforced by bead **prefix** (e.g. `gp-`, `r1-`, `r2-`). The
prefix is the real scoping mechanism. Rig names `rig1` and `rig2` both auto-derive the prefix
`"ri"` and collide; an explicit `prefix = "r1"` / `prefix = "r2"` in `city.toml` is required to
avoid this.

**CRITICAL open boundary:** the prototype proved that the prefix is the scoping **mechanism**.
It did NOT prove whether `gc` **prevents** an out-of-prefix access or merely **scopes by
convention**. The smoke test that would confirm enforcement strength was explicitly deferred. This
boundary is OPEN — it is the D-23 spike target — and must NOT be recorded as resolved here.

**(b) Evidence.**

> "**Pool prefix collisions:** rig names `rig1` and `rig2` both auto-derive bead prefix `"ri"` and
> collide. Set explicit `prefix = "r1"` / `prefix = "r2"` in city.toml."

— `docs/PLAN.md` §"Things this build had to figure out", item 4
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

> "**Scope is enforced by bead prefix.** A worker dispatched to rig1 can only see and create beads
> with the `r1-` prefix."

— `README.md` §"Logical view — what's connected to what", Notes
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

Smoke test status:

> "Smoke test (`bd create` on a rig, mayor reconciles end-to-end) **deferred** to a follow-up
> session to keep token spend in check"

— `docs/PLAN.md` §Status paragraph
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C42 (rig partitioning, bead prefix), C34 (holdout
integrity, enforcement strength), C34:OQ-C34-1, C43:OQ-C43-1, XC-9 (partial, spelling)

**(d) Verdict.** `NEW-INFO` for the prefix-as-mechanism and collision-avoidance facts.
The prevent-vs-detect OQ (`C34:OQ-C34-1` / `C43:OQ-C43-1`) remains **OPEN** — this harvest
explicitly does NOT close it.

**(e) Proposed annotation.** Add to C42 §6 and to C34:OQ-C34-1 / C43:OQ-C43-1:

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> **Bead scope is implemented as bead prefix.** Prefixes `gp-` (city HQ), `r1-` (rig1), `r2-`
> (rig2) are the real scoping mechanism — agents scoped to rig1 see/write only `r1-` prefixed
> beads. **Operational constraint:** rig names `rig1` and `rig2` both auto-derive prefix `"ri"` and
> collide at startup; explicit `prefix = "r1"` and `prefix = "r2"` in `city.toml` are required.
> Naming rigs to avoid short-prefix collisions is a production authoring concern, not a framework
> safeguard.
>
> **OPEN — prevent-vs-detect (C34:OQ-C34-1 / C43:OQ-C43-1 / D-23 spike):** The prototype proved
> that prefix is the MECHANISM for scoping. It did NOT verify whether `gc` PREVENTS an
> out-of-prefix bead access at the tool-call level or merely scopes-by-convention with
> detect-after-the-fact. The end-to-end smoke test (which would test this path) was deferred.
> This boundary remains the D-23 spike target and must NOT be treated as resolved by this harvest.

**(f) Disposition.** `safe-to-apply` for the prefix/collision fact; `needs-lead-review` for any
annotation touching the prevent-vs-detect boundary.

---

### F11 — Gastown pack roles and their v4 coordinator/health-patrol/bootstrap/worker mappings

**(a) Fact.** The bundled `gastown` pack defines the following named agent roles, which map to v4's
generic coordinator / health-patrol / bootstrap / observer / reviewer / worker roles: `mayor`
(coordinator), `deacon` (health-patrol), `boot` (bootstrap), `witness` (observer), `refinery`
(reviewer), `polecat` (worker), `crew` (worker variant), `dog` (pool worker). The prototype ran
all six named gastown agents successfully.

**(b) Evidence.**

> "First city stand-up verified: all 6 named gastown agents (mayor / deacon / boot + 3
> control-dispatchers) running real claude sessions; mayor + boot exchanging inter-agent commands
> within seconds of startup."

— `docs/PLAN.md` §Status paragraph
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

From README logical view (generic names):

> "City-scope agents: coordinator / health-patrol / bootstrap / worker pool (0..N)
>  Per-rig agents: rig1: observer / rig1: reviewer* / rig2: observer / rig2: reviewer*
>  (* spawned on demand)"

— `README.md` §"Logical view"
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

Also from PLAN.md §8 (gastown pack roles listed):

> "Import the bundled `gastown` pack. … Watch for runaway agent fan-out. … mayor + deacon + witness
> + refinery + polecat + crew + dog sessions all start under the controller."

— `docs/PLAN.md` §"Order of execution", step 8
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C04 (session provider, agent roster), C05 (sling dispatch,
pool membership), C07 (vocabulary glossary, Gas City term → generic mapping)

**(d) Verdict.** `CONFIRMS-CLAIM` (v4 described these generic roles; the prototype confirms the
gastown pack is the concrete realisation and names the pack-specific terms)

**(e) Proposed annotation.** Add to C07 §3 (vocabulary table):

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> the bundled `gastown` pack instantiates v4's generic agent-role vocabulary with these concrete
> names: `mayor` = coordinator; `deacon` = health-patrol; `boot` = bootstrap agent; `witness` =
> per-rig observer; `refinery` = per-rig reviewer (spawned on demand); `polecat` / `crew` = worker
> variants; `dog` = pool worker (min=0, spawned on dispatch). All six city-scope named agents were
> verified running as real `claude` processes in distinct tmux panes under the controller (2026-05-25
> stand-up). The `gastown` pack is the Phase-0 reference implementation of v4's role taxonomy.

**(f) Disposition.** `safe-to-apply`

---

### F12 — `claude --dangerously-skip-permissions` refuses root unless `IS_SANDBOX=1`; interactive claude has 3 onboarding dialogs

**(a) Fact.** Running `claude --dangerously-skip-permissions` as root is refused by `claude-code`
unless the environment variable `IS_SANDBOX=1` is set. Additionally, interactive `claude` has three
pre-run onboarding dialogs (theme picker, "trust this folder", "bypass permissions warning") that
must be pre-acknowledged via config files baked into the image/entrypoint, or they will hang an
agent session indefinitely.

**(b) Evidence.**

> "**`claude --dangerously-skip-permissions` refuses to run as root** unless `IS_SANDBOX=1` is set.
> The container runs as root by default; the env var bypass is cleaner than introducing a non-root
> user with mount permission complications."

— `docs/PLAN.md` §"Things this build had to figure out", item 7
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

> "**Interactive claude has three pre-run dialogs** that hang an agent session forever if not
> pre-acked: theme picker → `hasCompletedOnboarding: true`, `hasSeenWelcome: true`, `theme: "dark"`
> in `~/.claude.json` (NOT `~/.claude/settings.json`). "trust this folder" →
> `projects[path].hasTrustDialogAccepted: true` for every cwd the agent uses. "bypass permissions"
> warning → `bypassPermissionsModeAccepted: true` globally + per-path."

— `docs/PLAN.md` §"Things this build had to figure out", item 8
(lago-morph/gascity-prototype@b14c278, 2026-05-25)

**(c) Affected v4 spec(s) + OQ id(s).** C03 (config feature flags, deployment env), C04 (session
provider, agent bootstrap)

**(d) Verdict.** `NEW-INFO`

**(e) Proposed annotation.** Add to C04 §7 (failure modes / ops) or C03 §6 (ops notes):

> Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
> **Deployment constraint — root + permissions flag:** `claude --dangerously-skip-permissions`
> refuses to run as root unless `IS_SANDBOX=1` is set in the environment. Container images running
> as root must set this variable. **Deployment constraint — onboarding dialogs:** Interactive
> `claude` presents three pre-run dialogs (theme picker, folder-trust, bypass-permissions warning)
> that hang an agent session indefinitely if not pre-acknowledged. Pre-acknowledgement requires:
> (a) `hasCompletedOnboarding: true`, `hasSeenWelcome: true`, `theme: "dark"` in
> `~/.claude.json` (not `~/.claude/settings.json`); (b) `projects[path].hasTrustDialogAccepted:
> true` and `bypassPermissionsModeAccepted: true` for every working directory an agent uses
> (written by the entrypoint because paths are known only at runtime). These are production
> requirements for any containerised Gas City deployment, not just sandbox quirks.

**(f) Disposition.** `safe-to-apply`

---

## Summary Table

| # | Fact | Verdict | OQ(s) resolved | Disposition |
|---|---|---|---|---|
| F1 | `[[rig]]` singular / site.toml path bindings | RESOLVES-OQ | C42:OQ-4, XC-9 | safe-to-apply |
| F2 | `convergence.max_iterations` not a real field | NEW-INFO (was CONTRADICTS; lead-reclassified) | — | applied as ops note |
| F3 | Pack import strictness; `[defaults.rig.imports.*]` in city.toml; no duplicate transitive imports | NEW-INFO | C28:OQ-4 (partial) | safe-to-apply |
| F4 | `gc init` is interactive; production uses direct config authoring | NEW-INFO (was CONTRADICTS; lead-reclassified) | — | applied as ops note |
| F5 | Worker pool min=0, scales on demand | CONFIRMS-CLAIM | — | safe-to-apply |
| F6 | Controller = `gc start --foreground`; reconcile/reap/fire | CONFIRMS-CLAIM | — | safe-to-apply |
| F7 | Each agent = interactive `claude` in its own tmux pane | RESOLVES-OQ | C04:OQ-4 | safe-to-apply |
| F8 | Agents coordinate through beads only (write/poll), not directly | CONFIRMS-CLAIM | — | safe-to-apply |
| F9 | Dolt SQL server + periodic push; `refs/heads/*` required | NEW-INFO (was CONTRADICTS; lead-reclassified) | — | applied as ops note |
| F10 | Bead prefix = scoping mechanism; explicit prefix= to avoid collision; prevent-vs-detect OPEN | NEW-INFO | — (D-23 spike stays open) | safe-to-apply (mechanism); needs-lead-review (enforcement boundary) |
| F11 | Gastown pack roles ↔ v4 generic roles verified | CONFIRMS-CLAIM | — | safe-to-apply |
| F12 | IS_SANDBOX=1 for root; 3 onboarding dialogs must be pre-acked | NEW-INFO | — | safe-to-apply |

---

## OQ Resolution Register (this harvest)

| OQ id | Resolution |
|---|---|
| C42:OQ-4 | RESOLVED by F1 — canonical spelling is `[[rig]]`; path bindings in `.gc/site.toml` |
| XC-9 | RESOLVED by F1 — `[[rig]]` is canonical; propagate to C01/C03/C42 |
| C04:OQ-4 | RESOLVED by F7 — Phase-0 Provider-kind = tmux; each agent = one interactive `claude` pane |
| C28:OQ-4 (partial) | PARTIALLY INFORMED by F3 — pack-level contract: `[defaults.rig.imports.*]` in city.toml; transitive-import deduplication; full schema still needs G11 pinned-`gc` verification |

---

## Prevent-vs-Detect Explicitly OPEN

Per D-23 and PF-1, the question of whether `gc` **prevents** an out-of-prefix bead access at the
tool-call level or merely **scopes by convention with detect-after-the-fact** is **NOT resolved by
this harvest**. F10 records the prefix as the confirmed mechanism; F10 explicitly marks the
enforcement-strength boundary OPEN. C34:OQ-C34-1 and C43:OQ-C43-1 remain live with the D-23 spike
as the resolver. No annotation in this harvest should be read as closing the prevent-vs-detect
question.
