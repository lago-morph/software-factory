# agent instruction

**Don't trust a wrapper 'completed' signal for &-backgrounded long commands.** When a long command is backgrounded with `&` inside a tool wrapper, the wrapper may report completion immediately; confirm true completion by checking the process and its output artifact, not the wrapper's exit signal.

*Grounded in: a premature "completed exit 0" while `docker build &` was still running.*

# justification

During in-sandbox verification this session backgrounded a `docker build ... &` inside the bash tool wrapper. The wrapper returned a "completed exit 0" notification while the build was in fact still running — the `&` detaches the process, so the wrapper observed the shell returning, not the build finishing. Acting on that false signal would mean inspecting a half-built image, drawing wrong conclusions about whether a fix landed, and potentially shipping based on a build that had not actually completed (or had failed after the wrapper already reported success). The defense is cheap: after backgrounding, poll the process (is the `docker build` PID still alive?) and check the concrete output artifact (does the tagged image exist with a fresh timestamp; does the build log end with a success line?) before treating the work as done. The marginal cost is one or two extra status checks; the cost of trusting the premature signal is silent verification on the wrong artifact — the worst kind of false confidence because it looks like a green result.
