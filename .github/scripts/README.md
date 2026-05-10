# `.github/scripts/`

Helpers for the `fetch-blocked-urls.yml` workflow.

| File | Purpose |
|---|---|
| `extract_urls.py` | Parse the issue body (from env var `BODY`) and emit one URL per line. Handles markdown links, bare URLs, dedup, and trailing-punctuation stripping. |
| `fetch_urls.sh` | Iterate `.fetch-work/urls.txt`, curl each URL (30s timeout, browser-ish UA, redirect-following), save raw HTML + html2text markdown into `research/fetched/issue-<N>/`, and write a per-URL summary to `.fetch-work/summary.md`. |

See `.github/workflows/fetch-blocked-urls.yml` for the wiring, and `research/PLAN.md` §5–6 for the trigger / security model.

## Local test

```bash
BODY=$'foo\nhttps://example.com\n[link](https://example.org)' \
  python3 .github/scripts/extract_urls.py
```

```bash
mkdir -p .fetch-work
echo "https://example.com" > .fetch-work/urls.txt
ISSUE_NUMBER=0 bash .github/scripts/fetch_urls.sh
ls research/fetched/issue-0/
```
