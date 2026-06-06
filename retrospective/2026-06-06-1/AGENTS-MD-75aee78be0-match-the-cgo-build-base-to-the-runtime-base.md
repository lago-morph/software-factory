# agent instruction

**Match the CGO build base to the runtime base.** When building a CGO binary in a multi-stage Docker image, build it on the same base image (same distro release) as the runtime stage, or use a binary that links system libraries by SONAME (e.g. ICU); otherwise it will fail to load at runtime with a missing-library error.

*Grounded in: gc built on bookworm (ICU 72) failed to load on noble (ICU 74).*

# justification

This session compiled `gc` in a Debian bookworm builder stage and ran it on an ubuntu noble runtime stage. bookworm ships ICU 72 (`libicui18n.so.72`); noble ships ICU 74. `gc` links ICU by versioned SONAME, so at runtime the loader could not find `libicui18n.so.72` and the binary failed to start with exit 127 — a failure that a build-only check (the binary compiles, the image builds) completely hides, because the break only manifests on first invocation in the runtime stage. Crucially this would have hit the user's laptop identically, not just the sandbox. The fix was free: build on the same `ubuntu:24.04` base as the runtime. The marginal cost of the rule is one line of judgment when choosing the builder base; the cost of omitting it was an entire rebuild cycle plus the misdirection of debugging an exit-127 that looked like a missing argument rather than a missing shared library. The asymmetry — one base-image choice versus a silent, laptop-reproducing runtime failure — strongly favors making this a standing rule for any CGO/multi-stage image.
