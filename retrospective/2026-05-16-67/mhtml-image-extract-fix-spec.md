# Spec: `mhtml-image-extract-fix`

## Intent

The MHTML image-extraction helper at `.claude/skills/research-pipeline/scripts/mhtml_extract.py` has three real defects that surface every time a corpus drain extracts useful images from a captured web page. Subagents waste a turn each on them; this skill fixes the script (or, if non-disruptive, replaces the surface). Grounded in PR #67: Clusters C, H, I, K, L all hit at least one of the three issues.

## Trigger

Direct triggers:
- "Fix mhtml_extract.py"
- "Why is the saved image not the one info reported?"
- "The PNG is actually AVIF"

Proactive triggers:
- A subagent reports "image off-by-one between info and save-image."
- A subagent reports "saved a `.png` but `file` says AVIF."
- A subagent says it "can't find `scripts/mhtml_extract.py`."

## Inputs

- Current source at `.claude/skills/research-pipeline/scripts/mhtml_extract.py`.
- Optionally a calling brief that demonstrates the bug (e.g. "Cluster H saved image 8 (1-based) / 7 (0-based)" — both indices saved the same image with different metadata).

## Outputs

- A patched `mhtml_extract.py` with consistent indexing semantics + transparent AVIF→PNG conversion + a version-stamp comment recording the fix.
- A docstring + `--help` block matching the new behavior.
- If `info` output format changes, callers that parse it must be updated; the `research-pipeline` skill should be re-validated against a known MHTML fixture.

## Workflow

1. **Reproduce the bugs.** Pick any MHTML capture with embedded images. Run `info` and `save-image 0`, `save-image 1`; verify which index produces which file by reading the saved bytes (Pillow `Image.open(path).size` will show distinct sizes for distinct images).
2. **Pick a single index base.** Recommend 0-based (Pythonic; matches `save-image`'s current behavior). Update `info` to emit 0-based indices. Document in `info`'s JSON output: `{"index_base": 0, ...}`.
3. **Detect AVIF transparently.** Inspect the MIME type on save. If `content-type` is `image/avif` or the bytes start with the AVIF box signature (`ftypavif`), decode with Pillow's pillow-avif-plugin (or `pyheif`) and re-encode to PNG before writing. Preserve the originally requested extension; if user said `.png`, deliver true PNG bytes.
4. **Add a `--list` subcommand** (alias of `info` but human-readable) so subagents don't need to pipe `info` through `python3 -m json.tool`.
5. **Path note in the skill's main `SKILL.md`** — make explicit that the script lives at `.claude/skills/research-pipeline/scripts/mhtml_extract.py`. Update any briefs that point at `scripts/mhtml_extract.py`.
6. **Run the link checker** if one exists for the research-pipeline skill; verify no broken paths.
7. **Commit on a feature branch**, push, open a draft PR.

## Concrete examples

### Example 1: Cluster H — the canonical Cluster-H bug

```
$ python3 .claude/skills/research-pipeline/scripts/mhtml_extract.py info "research/manual/Replit — Introducing Replit Agent App Monitoring.mhtml" | python3 -m json.tool | head -30
{
  "images": [
    {"index": 1, "size": 12345, ...},     # <-- 1-based!
    ...
  ]
}

$ python3 .claude/skills/research-pipeline/scripts/mhtml_extract.py save-image "research/manual/Replit — Introducing Replit Agent App Monitoring.mhtml" 7 /tmp/img.png
# saved index 7 (0-based) — different image than info said was index 7 (1-based)
```

After fix:
```
$ python3 .claude/skills/research-pipeline/scripts/mhtml_extract.py info ... | python3 -m json.tool | head -30
{
  "index_base": 0,
  "images": [
    {"index": 0, "size": 12345, ...},
    ...
  ]
}
$ python3 .claude/skills/research-pipeline/scripts/mhtml_extract.py save-image ... 7 /tmp/img.png
# saves the same image info reported as index 7
```

### Example 2: Cluster H AVIF inside PNG

```
$ python3 .claude/skills/research-pipeline/scripts/mhtml_extract.py save-image ... 0 /tmp/img.png
$ file /tmp/img.png
/tmp/img.png: ISO Media, AVIF Image    # <-- bytes are AVIF, extension lies
```

After fix:
```
$ python3 .claude/skills/research-pipeline/scripts/mhtml_extract.py save-image ... 0 /tmp/img.png
$ file /tmp/img.png
/tmp/img.png: PNG image data, 1144 x 682, 8-bit/color RGB, non-interlaced
```

## Anti-patterns

- **Adding a `--legacy-1-based` flag for "compatibility."** No one is using the 1-based behavior on purpose — it's a bug. Just fix it.
- **Writing a wrapper script that calls the original with an index translation.** Two paths to the same thing is worse than one wrong path.
- **Failing silently when AVIF decoding is missing.** If the Python env lacks pillow-avif-plugin / pyheif, raise a clear error with the install command.
- **Touching the MHTML parser body when the bug is in image indexing.** Scope discipline; this fix is two functions max.

## Acceptance criteria

1. `info` and `save-image` agree on indices for ≥3 fixture MHTMLs spanning AVIF, PNG, and JPEG embeds.
2. `file <saved-path>` reports a real PNG (not AVIF, not WEBP) for every image saved with a `.png` target.
3. The `info` JSON output includes an explicit `index_base` field documenting the convention.
4. The `research-pipeline` skill's `SKILL.md` references the correct script path.
5. No regressions on the existing `to-txt` subcommand (used by every drain).

## Files this skill creates / modifies

- `.claude/skills/research-pipeline/scripts/mhtml_extract.py` — primary fix.
- `.claude/skills/research-pipeline/SKILL.md` — path / option docs updated.
- Possibly `requirements.txt` or `pyproject.toml` if `pillow-avif-plugin` needs to be declared.
