# YouTube transcripts

A `youtube-transcript` is a plain-text transcript of a YouTube video that was found embedded in (or linked from) a document we've already ingested. We treat transcripts the same way we treat images: they are **`files[]` entries on the embedding source's record**, not separate source records.

Why this shape? The embedding document is what cites the video; if two different documents reference the same video and we judge both as useful, we ingest two transcript copies — once per embedding record. Cheap and consistent with the image precedent.

## Lifecycle

```
agent reads file → spots useful YouTube link → adds wanted entry
                                                       │
                                                       ▼
                                  user fetches transcript externally
                                                       │
                                                       ▼
                              user drops .txt (first line = video URL)
                                                       │
                                                       ▼
                              drain / reconcile promotes want → have
```

## File entry shape

```json
{
  "format": "youtube-transcript",
  "filename": null,
  "ingestion_status": "want",
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

`youtube_url` is **required when** `format=youtube-transcript` and **forbidden otherwise** — enforced by the JSON schema. The URL must be in canonical `https://www.youtube.com/watch?v=<ID>` form. Use `python scripts/youtube_urls.py <file>` or the canonicalizer directly:

```bash
python -c "from youtube_urls import canonicalize_youtube_url; print(canonicalize_youtube_url('https://youtu.be/dQw4w9WgXcQ?t=42'))"
# → https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

When the user delivers the transcript, drain/reconcile fills in `filename`, `sha256`, `ingestion_status: have`, and `completeness: unknown`. `youtube_url` stays put.

## Adding a wanted entry (agent, stage 5)

After `drain.py` finishes, the run summary lists **YouTube embed candidates** — every YouTube URL found in a newly-ingested document that isn't already covered by an existing `youtube-transcript` entry on that record. Each candidate has a short snippet of surrounding text.

Your judgement call: does the surrounding text suggest the video is a useful source? If yes, add a wanted entry. If no, ignore it — `casual_url_patterns` in the config already excludes YouTube from `check-source-refs.py`, so the URL won't get flagged as un-cataloged when reports cite it casually.

To add a wanted entry on record `<ID>` for video `<VIDEO_URL>`:

```bash
F=reference-only/sources.json
ID="0a7f3b8e00"
VIDEO_URL=$(python -c "from youtube_urls import canonicalize_youtube_url; print(canonicalize_youtube_url('<URL>'))")

jq --arg id "$ID" --arg url "$VIDEO_URL" '
  .[$id].files |= ((. // []) + [{
    "format": "youtube-transcript",
    "filename": null,
    "ingestion_status": "want",
    "youtube_url": $url
  }])
' "$F" > /tmp/new.json && \
mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
```

## Delivering the transcript (user)

1. Open the YouTube video, copy the transcript text.
2. Create a `.txt` file. Put the **canonical** video URL on the first line. The rest is the transcript body.
3. Drop it in either:
   - `reference-only/<ID>/<name>.txt` — the embedding record's directory. Then run `python scripts/reconcile-source-dir.py <ID>`.
   - `research/manual/<name>.txt` — drain will find a matching wanted entry on any record by `youtube_url` and promote it. If no match exists, drain flags the file in the run summary.

Example transcript file:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ

[0:00] We're no strangers to love...
[0:10] You know the rules, and so do I...
...
```

## How drain handles delivery

When drain sees a `.txt` in an ingestion drop dir whose first non-blank line is a YouTube URL, it:

1. Canonicalizes the URL.
2. Scans every record for a `youtube-transcript` file entry with `ingestion_status=want` and matching `youtube_url`.
3. If found: moves the file to `reference-only/<rid>/<basename>`, sets `filename` / `sha256` / `ingestion_status=have`. Reported under **YouTube transcripts delivered** in the run summary.
4. If not found: leaves the file in place and reports it under **Flagged files** so the agent can decide whether to add the wanted entry first, or move the file manually to the right `<id>/` dir.

`reconcile-source-dir.py` does the same when called on a record whose `<id>/` directory already contains the transcript .txt.

## Audit checks that apply

`audit-records.py` adds three transcript-specific checks (in addition to the existing file-on-disk / sha256 / format-ext checks):

- `youtube-url-required-when-transcript` — every `youtube-transcript` entry has a canonical YouTube URL set.
- `youtube-url-only-on-transcript` — `youtube_url` doesn't appear on any other file format.
- `youtube-transcript-content-matches` — for `have` transcripts, the file's first line is the same URL recorded in `youtube_url`.

A transcript record that's still `want` only triggers check 13 (URL set) and 14 (URL field used correctly).

## When the surrounding text isn't enough

Sometimes the snippet drain emits doesn't carry enough context to judge usefulness. Open the file and read the section around the link. If you're still on the fence, lean toward **not** adding a wanted entry — the user can come back to it.

## Edge cases

| Situation | Handling |
|---|---|
| Same video referenced from two docs we ingest | Two `youtube-transcript` wanted entries — one per embedding record. User delivers the .txt twice (or copies the same file into both `<id>/` dirs). Acceptable; matches the image model. |
| Video URL has tracking params or `?t=42` timestamp | `youtube_urls.canonicalize_youtube_url` strips them. Always use the canonical form when setting `youtube_url`. |
| User delivers a .txt without the URL on the first line | Drain treats it as a plain `txt` source (not a transcript). The audit's first-line check then fails. Fix: prepend the URL to the file and rerun reconcile. |
| Embedding record doesn't exist yet | Drain ingests the embedding doc first (creating its record), then surfaces the YouTube embed. Wanted entries are always added after the parent record exists. |
| Video is a Shorts / live / embed URL | `canonicalize_youtube_url` rewrites all of `youtu.be/<ID>`, `/shorts/<ID>`, `/embed/<ID>`, `/v/<ID>`, `/live/<ID>` to `https://www.youtube.com/watch?v=<ID>`. |
