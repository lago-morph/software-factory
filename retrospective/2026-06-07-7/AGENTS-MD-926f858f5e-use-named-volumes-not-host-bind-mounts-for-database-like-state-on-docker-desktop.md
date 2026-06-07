# agent instruction

**Use named volumes, not host bind mounts, for database-like state on Docker Desktop.** Put database or DB-like runtime state in a named Docker volume, not a host bind mount, when the target may be Docker Desktop (Windows/macOS); the translated host filesystem is pathologically slow for the many small reads/writes and file locking such state generates.

*Grounded in: Dolt crawled on a `./workspace` host bind mount and ran fast on a named volume.*

# justification

The prototype stored its Dolt bead-store on a `./workspace` host bind mount. On Docker Desktop the host filesystem is reached through a translation layer (drvfs/9p over the WSL2 VM), and Dolt's access pattern — many small reads and writes plus file locking — is the worst case for that layer. The operator experienced an "extremely slow" bead store; switching to a named Docker volume made it fast. The cost of not having this rule is a deliverable that is unusably slow on the most common developer platform (Windows + Docker Desktop), discovered only after an operator reports it, and only debuggable by someone who knows the bind-mount-translation tax. The marginal cost is one line in the compose file: a named volume instead of a bind mount (and telling operators to use `docker compose exec`/`cp` to inspect state and `down -v` to wipe it). For DB-like state on Docker Desktop, the bind mount is a performance trap with no upside the prototype needs.
