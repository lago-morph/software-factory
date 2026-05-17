# File layout

How files are organized under `reference-only/` and how the catalog tracks them.

## The convention

```
reference-only/
├── sources.json            # the catalog (authoritative)
├── sources.schema.json     # JSON schema constraining the catalog
├── sources.md              # auto-generated browse view
├── .regen-trigger          # ephemeral; tickle file for manual workflow trigger
├── 0a7f3b8e00/             # per-source directory (10-char hex id)
│   ├── main.mhtml
│   ├── extract.txt
│   └── figure-1.png
├── 1b2c3d4e00/
│   └── paper.pdf
├── ...
└── <legacy-topic-dirs>/    # pre-id-convention; tolerated
    ├── anthropic-agent-skills/
    ├── lenny-podcast-transcripts/
    ├── el-kaim-book/
    └── camel-paper/
```

## The rule

**Files for record `<id>` live at `reference-only/<id>/<filename>`** unless the file entry has a `location` override.

The directory name is the 10-char hex record id. The file basename is whatever the file is called. No nested subdirectories within `<id>/` (one level only).

## The `location` override

For files that don't fit the convention — typically legacy `reference-only/<topic>/` files or shared assets in `research/figures/` — the file entry's `location` field can override:

```json
{
  "format": "txt",
  "filename": "willison-ai-state-of-the-union-full.txt",
  "location": "reference-only/lenny-podcast-transcripts/willison-ai-state-of-the-union-full.txt",
  "ingestion_status": "have"
}
```

When `location` is set, it takes precedence over the default `reference-only/<id>/<filename>` path. The linter trusts the override and silences the orphan-file warning for files referenced this way.

## Legacy directories

These predate the per-id convention and stay where they are:

| Legacy dir | What it holds |
|---|---|
| `anthropic-agent-skills/` | Multiple files about Anthropic's skills feature |
| `lenny-podcast-transcripts/` | Podcast transcripts from various episodes |
| `el-kaim-book/` | Chapters from William El Kaim's book |
| `camel-paper/` | Source files for the CaMeL paper |
| `chatgpt-deep-research-2026-05-11/` | Research report from ChatGPT (internal artifact) |

Records that reference these files use `location` overrides. New sources go into per-id directories. Don't migrate the legacy ones unless there's a specific reason (broken link, content needs updating, etc.).

## Naming conventions inside a per-id directory

No enforced naming, but good practice:
- `main.<ext>` — the primary content file (the canonical capture)
- `extract.txt` — text extract from a binary/markup source
- `figure-N.<ext>` — diagrams or screenshots
- `paper.pdf` — the canonical PDF
- `transcript.txt` — for audio/video sources
- `<descriptive-name>.<ext>` — anything else

Filenames must be basenames only (no `/`). If you have something that would need a path, restructure or use a `location` override pointing outside `reference-only/<id>/`.

## File status semantics

| `ingestion_status` | Where file lives | `completeness` |
|---|---|---|
| `have` | Present on disk at `reference-only/<id>/<filename>` (or `location`) | `complete` / `partial` / `error` / `unknown` |
| `want` | Not on disk; `filename` may be null | n/a (not yet acquired) |
| `skip-not-necessary` | Decision made not to fetch | n/a |
| `skip-unknown` | Default for new wishlist entries | n/a |

## Format inference

The `reconcile-source-dir.py` script infers format from extension:

| Extension | Format |
|---|---|
| `.html`, `.htm` | `html` |
| `.mhtml` | `mhtml` |
| `.md` | `md` |
| `.txt` | `txt` |
| `.pdf` | `pdf` |
| `.ipynb` | `ipynb` |
| `.png` | `image/png` |
| `.jpg`, `.jpeg` | `image/jpeg` |
| `.svg` | `image/svg+xml` |
| `.gif` | `image/gif` |
| `.webp` | `image/webp` |
| `.json` | `json` |
| `.yaml`, `.yml` | `yaml` |
| `.csv` | `csv` |
| `.zip` | `zip` |
| anything else | `other` |

## Cardinal rules

1. **Filename = basename** in `files[].filename`. Never a path.
2. **`location` is the escape hatch** for files outside `reference-only/<id>/`.
3. **One file = one entry** in `files[]`. Don't share entries across records.
4. **No subdirectories** inside `reference-only/<id>/` (one level only).
5. **Legacy topical dirs are tolerated**; don't migrate them just for tidiness.
