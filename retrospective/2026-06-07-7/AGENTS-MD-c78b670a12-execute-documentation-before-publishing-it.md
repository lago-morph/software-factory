# agent instruction

**Execute documentation before publishing it.** When you write or edit user-facing documentation that contains runnable commands, execute every command against the real running system and reconcile the docs to observed behavior before declaring them done; do not ship commands you only reasoned about.

*Grounded in: five tutorial commands shipped wrong, all caught only by running them against the live container.*

# justification

In this session the operator insisted "you have to test documentation," and running every command in the README and GETTING-STARTED against the live container surfaced five separate doc bugs that were invisible on the page: a `gc bd` command run from the wrong directory, a sling target (`rig1/polecat`) that did not exist, a tmux session-name translation gap, a `gc events --follow` that silently needs a service that wasn't running, and a run-3 `jq` pipeline that failed silently. Every one of these reads as authoritative prose; every one fails on first real run. The cost of not having this rule is shipping a tutorial that fails for the very first reader who follows it — the highest-trust, lowest-tolerance moment a doc has. The marginal cost of the rule is one pass of pasting each command into the already-running system. The asymmetry is stark: minutes of execution versus a quickstart that doesn't start.
