# agent instruction

**Handle live credentials without printing them.** When a task requires a real token or credential, load it by reading the source file or FD directly into an env-file or env var, and verify only with non-revealing checks (e.g. `grep -c`); never echo, `cat`, or otherwise emit the secret into logs or transcripts.

*Grounded in: the live-token runs built `.env` from the token file and verified with `grep -c`, never printing the token.*

# justification

This session ran the prototype three times with a real API token (auth check, bead-lifecycle, native-dispatch) and never once printed it. The `.env` was written directly from the token file/FD, and presence was verified with `grep -c` (a count, not the value). The cost of not having this rule is catastrophic and irreversible: a single `echo $TOKEN` or `cat .env` leaks a live credential into a transcript, a log, or a PR that may persist and be readable long after the session — a leak you cannot un-leak. The marginal cost of the rule is essentially zero: read the secret into the env without rendering it, and verify with a non-revealing check. There is no scenario where printing the credential is necessary, so the safe pattern costs nothing and the unsafe pattern risks everything.
