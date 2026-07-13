---
name: read-pdf
description: Reads academic PDFs into reusable, project-neutral `_text.md` extracts. Use for paper reading; default to layout-aware conversion and use `--split` for triage or converter failure.
allowed-tools: Bash(python3:*), Bash(curl:*), Bash(wget:*), Bash(mkdir:*), Bash(mv:*), Bash(rm:*), Read, Write, WebSearch, WebFetch, Agent
argument-hint: [--split] [pdf-path-or-search-query]
---

# Read-PDF: Download, Convert, and Deep-Read Academic Papers

Takes a PDF (local or searched) and produces a structured `_text.md` extraction with a bibliographic metadata block, a plain-English synthesis, and 12-dimension research notes.

Default mode converts the PDF to markdown locally using python:marker, prepares bounded source chunks, then reads them through bounded extraction. This preserves equation fidelity, table structure, and figure references without image-based context bloat or whole-file `Read` failures.

`--split` mode splits into 4-page chunks, reads exactly 3 chunks at a time, updates running notes, then writes the same `_text.md` contract.

## When This Skill Is Invoked

The user wants to read, review, or summarize an academic paper. The input is either:
- A file path to a local PDF (e.g., `~/Documents/papers/smith_2024.pdf`)
- A search query or paper title (e.g., `"Gentzkow Shapiro Sinkinson 2014 competition newspapers"`)

**Important:** You cannot search for a paper you don't know exists. Provide either a file path or a specific query. If the user invokes this skill without specifying a paper, ask them.

## Mode selection

- **Default marker mode:** use unless the user explicitly asks for `--split`, triage-only reading, or no local converter setup.
- **`--split` mode:** use when the user invokes `/read-pdf --split`, invokes `/split-pdf`, needs first-split triage, or marker conversion fails and the user wants the vision-batch fallback.

## Prerequisites

- **Python ≥ 3.10** must be available. `install.py` refuses to proceed on Python 3.9 or older. If needed: `brew install python@3.12`, `apt install python3.11`, or python.org installer.
- **Optional GPU acceleration** is auto-detected: NVIDIA CUDA → CPU. (MPS on Apple Silicon is excluded — surya's layout model crashes on MPS at runtime.)

These prerequisites apply only to default marker mode. `--split` mode requires pypdf for `scripts/split.py`; if missing, install it with `python3 -m pip install pypdf`.

## Step 1: Acquire the PDF

**If a local file path is provided:**
- Verify the file exists
- Use the PDF in place. The working directory is the folder containing the PDF.
- Proceed to Step 2

**If a search query or paper title is provided:**
1. Use WebSearch to find the paper
2. Use WebFetch or Bash (curl/wget) to download the PDF
3. Save it to the current working directory
4. Proceed to Step 2

**CRITICAL: Always preserve the original PDF.** Never delete, move, or overwrite it at any point in this workflow.

## Default marker mode

### Step 2: Ensure the converter is installed

```bash
python3 ~/.claude/skills/read-pdf/install.py
```

Idempotent. First run creates a venv at `~/.cache/claude-pdf-converter/venv-marker/` and downloads marker models (~500 MB, 1–3 min). Later runs reuse that venv if `marker` imports cleanly; they do **not** auto-upgrade marker.

Once every 30 days, `install.py` performs a lazy PyPI check for marker major-version updates. If it prints a `read-pdf notice: marker-pdf has a major update available` advisory, pause and surface it to the user. Ask whether they want to upgrade now with:

```bash
python3 ~/.claude/skills/read-pdf/install.py --upgrade-marker
```

Do not purge caches automatically. Explain that existing cached conversions remain valid but were produced by the older marker version. If the user wants fresh conversions after upgrading, delete selected cache entries under `~/.cache/claude-pdf-converter/cache/marker/`, or delete that whole directory; rebuilding a large cache can be very time-consuming.

Surface the "First run" message to the user verbatim if it appears — they should know why this invocation is slow.

### Step 3: Convert

Run the cache-aware converter once:

```bash
python3 ~/.claude/skills/read-pdf/convert.py "<pdf-path>"
```

It reports a SHA-256 cache hit or miss on stderr, prints the absolute `markdown.md` path on stdout, and exits 0 on success. For born-digital PDFs with a usable embedded text layer, it disables marker's full-document OCR path while preserving marker's layout/table processing. **Do not fall back to pdftotext or any other tool on failure** — surface the error and stop. The whole point of this skill is the layout-aware conversion; a degraded fallback produces silently-wrong output.

### Step 4: Check for existing `_text.md`

Look for `<basename>_text.md` in the same folder as the PDF.

If found, ask:
> "An extract already exists (`<basename>_text.md`). Overwrite it, or save the new extraction as `<basename>_text2.md`?"

Proceed using whichever filename the user chooses.

If no local extract exists, check for a cache-level neutral extract at `<markdown_path parent>/text.md`.

Run:

```bash
python3 ~/.claude/skills/read-pdf/scripts/cache_text.py check "<markdown_path>"
```

- If it prints a cache path, run:
  ```bash
  python3 ~/.claude/skills/read-pdf/scripts/cache_text.py pull "<markdown_path>" "<local_text_path>"
  ```
  Then skip Steps 5–6 and notify the user: *"Using cached neutral extract from converter cache; copied to `<basename>_text.md`."*
- If it prints `NOT_CACHED`, continue to Step 5.

### Step 5: Prepare extraction substrate

Run the deterministic substrate builder:

```bash
python3 ~/.claude/skills/read-pdf/scripts/prepare_substrate.py "<markdown_path>"
```

It writes bounded chunk files and `manifest.json` beside the marker cache. The script performs no scholarly interpretation; it only creates a structural manifest over the converted markdown.

### Step 6: Structured Extraction

Use `fanout_worker.md` and `fanout_synthesis.md` with the generated manifest. The manifest selects the execution mode from projected working context:

- **`single_reader` (default):** one reader processes `worker_bundles` sequentially and writes one durable note file after each bundle.
- **`fanout`:** one bounded worker reads each bundle and writes its note file. Use this only when `projected_working_tokens` exceeds the manifest's 100,000-token threshold.

After every expected note file exists, synthesis reads the manifest and worker notes, performs gap-directed rereads of specific chunk files only when needed, and writes the final extraction to `<local_text_path>.tmp`. Validate that the temp file is non-empty and contains `## Bibliographic metadata`, `## Plain-English synthesis`, and all 12 numbered research dimensions; then rename it to `<local_text_path>`. A failed validation leaves no final extract.

The final extraction follows `extraction_schema.md`: a `## Bibliographic metadata` block from the title section, then the research dimensions. Read `extraction_schema.md` before synthesis so the output contract is explicit. After installing the validated `<basename>_text.md` (or `_text2.md` chosen in Step 4), cache the same neutral extract:

```bash
python3 ~/.claude/skills/read-pdf/scripts/cache_text.py push "<markdown_path>" "<local_text_path>"
```

Then notify the user: *"Extract saved to `<basename>_text.md` alongside the source PDF and cached as `text.md` in the converter cache."*

## `--split` mode

Use this branch only when selected by the Mode selection rules above.

**Critical rule:** Never read a full PDF in split mode. Only read the 4-page split files, and only 3 splits at a time (~12 pages).

### Step S2: Reuse or split

1. Look for `<basename>_text.md` next to the PDF. If found, ask: *"An extract already exists (`<basename>_text.md`). Use it, or re-read from scratch?"* On **Use**, read `_text.md` as the source notes and skip the rest of split mode. On **Re-read**, continue.
2. Look for `<foldername>_build/split_<pdf-basename>/*.pdf`. If found, ask: *"Splits already exist (N chunks). Reuse, or re-split?"* On **Reuse**, proceed with existing files. On **Re-split**, delete the split folder and continue.

Create splits by running:

```bash
python3 ~/.claude/skills/read-pdf/scripts/split.py path/to/paper.pdf
```

Directory convention:

```text
articles/
├── smith_2024.pdf
├── smith_2024_text.md
└── articles_build/
    └── split_smith_2024/
        ├── smith_2024_pp1-4.pdf
        ├── smith_2024_pp5-8.pdf
        ├── smith_2024_pp9-12.pdf
        └── notes.md
```

### Step S3: Read in batches of 3 splits

Read exactly 3 split files at a time. After each batch:

1. Read the 3 split PDFs using the Read tool.
2. Update `notes.md` in the split directory.
3. Continue with the next batch until all splits are read.

If the user explicitly requests paced triage, report progress and wait for confirmation after each batch. Do not read ahead while paced triage is active.

### Step S4: Structured extraction

As you read, collect notes into `notes.md` following `extraction_schema.md`. After all batches are complete, synthesize `<basename>_text.md.tmp`, validate the same required blocks and 12 dimensions as default mode, then rename it to `<basename>_text.md`. Keep both `notes.md` and `_text.md`.

## Agent Isolation

When `/read-pdf` is invoked by another skill or batch workflow, use one reader context per paper. Bundle-level subagents are reserved for manifests whose `execution_mode` is `fanout`. See `agent_isolation.md` for the mode router and `isolation_read.md` / `isolation_split.md` for branch-specific launch patterns.

## Files in this skill

- `SKILL.md` — this file (acquire → default marker mode or `--split` mode → extract workflow)
- `extraction_schema.md` — bibliographic metadata block + 12 research dimensions
- `fanout_worker.md` — bounded worker-note prompt for marker chunks
- `fanout_synthesis.md` — synthesis prompt for worker notes and final `_text.md`
- `agent_isolation.md` — isolation mode router
- `isolation_common.md` — shared parent/subagent rule
- `isolation_read.md` — marker-mode isolation pattern
- `isolation_split.md` — split-mode isolation pattern
- `install.py` — idempotent marker venv installer with monthly advisory check
- `convert.py` — PDF → markdown converter (writes to SHA-256-keyed cache)
- `scripts/prepare_substrate.py` — marker markdown → bounded chunks + manifest
- `scripts/cache_text.py` — check/pull/push project-neutral `text.md` extracts in the converter cache
- `scripts/split.py` — pypdf 4-page splitter used by `--split` mode and downstream fallbacks
- `tests/test_prepare_substrate.py` — execution-mode threshold tests
- `README.md` — backend details, cache management, GPU notes
