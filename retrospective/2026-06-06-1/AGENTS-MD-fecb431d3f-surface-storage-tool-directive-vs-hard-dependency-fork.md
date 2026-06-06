# agent instruction

**Surface a storage/tool directive vs hard-dependency fork before building.** When a user's storage or tooling directive conflicts with a hard dependency of a component you're adopting, surface the fork with AskUserQuestion (naming the trade-off and the rework risk) before building, rather than silently picking one side.

*Grounded in: "use file for the bead store" conflicted with the gastown pack's 368 `gc bd` calls.*

# justification

The user's initial directive was "use file for the bead store" — the gc-native JSON `file` provider. But `gc bd` is gated to bd-contract providers, and the bundled gastown pack makes roughly 368 `gc bd` calls, so the file provider literally cannot run the proven gastown fleet. Silently honoring the directive would have produced a package that boots but cannot run the very workload it exists to host; silently overriding it would have ignored a clear user instruction. Either silent choice risks a full rebuild once the conflict surfaces. The right move — taken this session — is to surface the fork explicitly via AskUserQuestion, naming the trade-off (file provider disables `gc bd`, which gastown depends on) and the rework risk, and let the user decide. This investigation drove the entire bead-store design and ultimately the user chose the managed-Dolt-plus-socat option through a follow-up AskUserQuestion. The marginal cost is one question before building; the cost of skipping it is building the wrong architecture on a misunderstood constraint and discovering it only after the work is done.
