# agent instruction

**Keep the committed Dockerfile sandbox-clean; verify via a throwaway patched copy.** Never add sandbox-specific hacks (e.g. trusting a TLS-inspection CA) to a committed Dockerfile meant for laptops; to verify inside such a sandbox, build a throwaway copy patched only for the sandbox and leave the committed file clean.

*Grounded in: the sandbox TLS-proxy blocked in-build HTTPS.*

# justification

The sandbox runs a TLS-inspection proxy that breaks HTTPS inside build containers — `curl` exits 60 and `git` fails certificate verification — so the Dockerfile could not be built as-written without trusting the sandbox CA. The tempting shortcut is to add a `COPY sandbox-ca.crt` / `update-ca-certificates` step to the real Dockerfile so the build "just works" here. That shortcut would have shipped a sandbox-only trust anchor to every laptop user, a security smell and a confusing artifact in a file whose whole purpose is laptop portability. Instead this session built a throwaway copy of the Dockerfile patched only to trust the sandbox CA, used it solely for in-sandbox verification, and left the committed Dockerfile untouched. The marginal cost is one extra file and a `cp`-then-patch step at verify time; the cost of violating the rule is permanent contamination of a shipped artifact with environment-specific hacks that future readers must reverse-engineer and strip. Keeping the committed file clean also means the in-sandbox verification actually tests the file users will run, modulo the single isolated CA delta.
