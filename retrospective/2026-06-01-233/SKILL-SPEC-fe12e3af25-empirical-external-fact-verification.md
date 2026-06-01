# Spec: `empirical-external-fact-verification`

- **ID**: SKILL-SPEC-fe12e3af25
- **Source retrospective**: ../2026-06-01-233.md

## Intent

Verify a load-bearing external fact (does a tool/repo/binary exist, does an API behave a certain way) with your own tool calls and at least two independent signals plus a control, rather than trusting a subagent's web-search narrative; distinguish transport/proxy artifacts (e.g. a blanket 403) from real results before concluding. This earns its place because in this run the single highest-leverage unknown (does Gas City / `gc` actually exist — gap G11) was nearly answered wrong by a subagent that confidently reported a fabricated version number and install command; three direct probes with a control repo settled it in seconds.

## Trigger

- **Direct:** "is X real / does X exist", "verify this before we build on it", "confirm the tool/repo/API".
- **Proactive:** a subagent or web search returns a confident claim about the existence or behavior of an external dependency that the rest of the work will be built on; OR a tool returns an error that *could* be a transport/proxy artifact (403/timeout/empty) and you're about to treat it as a substantive result.
- **Negative:** facts internal to the repo (read the file); facts already verified this session; low-stakes claims nothing is built on.

## Inputs

- The claimed fact + its source (subagent receipt, web-search result, prior assertion).
- Available verification tools: `curl`/`Bash`, the GitHub API (direct or via jentic), `WebFetch`/`WebSearch`, `git ls-remote`/`clone`, repo `grep`.
- A control case: a known-true and (ideally) a known-false instance of the same query class.

## Outputs

- A definite verdict (CONFIRMED / REFUTED / INDETERMINATE-because-transport) with the independent signals that support it, recorded in the run's notes/PR description.
- Discard of any confabulated specifics from the original narrative.

## Workflow

1. **Name the exact proposition** to verify (e.g. "the repo `owner/name` exists", not "Gas City is real").
2. **Pick ≥2 independent signal sources** that don't share a failure mode (e.g. HTML host + search API + package index — not three calls to the same endpoint).
3. **Add a control**: run the same query against a known-good instance (and a known-bad one if cheap). If the control fails the same way as the target, your signal is a transport/proxy artifact — it tells you nothing; pick a different signal.
4. **Run the probes**; compare target vs control. A 404 where the control is 200 is real absence; a 403/timeout where the control also fails is an artifact.
5. **For behavior claims** (not just existence): prefer running the real thing in a minimal harness; if you cannot (cost/sandbox), write the deterministic test protocol and mark the behavior OPEN rather than inferring it.
6. **Discard confabulated detail.** If the narrative carried specifics you did not independently confirm (a version number, a command), drop them; keep only what the probes established.
7. **Record the verdict + signals** so a reviewer can audit how you concluded.

## Concrete examples

**Example 1 — repo existence (this run).** Claim: "Gas City is real, `gastownhall/gascity`, v1.2.0, `brew install`." Probes: `curl api.github.com/repos/gastownhall/gascity` → 403; control `curl api.github.com/repos/torvalds/linux` → **also 403** ⇒ `/repos/` is proxy-blocked, the 403 is an artifact. Switched signals: `curl -sL github.com/gastownhall/gascity` → 200 (control `torvalds/linux` → 200), and `api.github.com/search/repositories?q=gascity+in:name` → top hit `gastownhall/gascity`. Verdict: repo CONFIRMED real; the "v1.2.0 / brew install" specifics were discarded as unverified (later shown wrong — the build is from source via Go).

**Example 2 — API behavior, can't run it.** Claim: "`gc` prevents an out-of-partition read at tool-call time." No Docker daemon in-sandbox to run a real `gc`. Resolution: do NOT infer; write the runnable prevent-vs-detect test protocol (exact commands + observation→verdict table) and mark the behavior OPEN until executed in a Docker-capable environment.

## Anti-patterns

- **Treating a subagent's web-search narrative as established fact** because it was confident and detailed (confidence and fabricated detail co-occur).
- **Concluding "doesn't exist" from a 403/timeout** without a control (it's usually a transport artifact, not a 404).
- **Inferring behavior you couldn't run** — write the test, mark it OPEN.
- **Keeping the confabulated specifics** ("v1.2.0") after only the general claim was verified.

## Acceptance criteria

1. The exact proposition is stated separately from the source's framing.
2. ≥2 independent signals were used, with at least one control.
3. Transport/proxy artifacts are explicitly distinguished from substantive results.
4. Unverified specifics from the original narrative are dropped, not carried forward.
5. Behavior that could not be executed is marked OPEN with a runnable test, not inferred.

## Files this skill creates / modifies

- None required; it writes its verdict into the run's existing notes / PR description / decision brief. (It is a verification discipline, not an artifact generator.)
