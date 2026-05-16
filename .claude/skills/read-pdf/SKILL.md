---
name: read-pdf
description: Downloads or uses a local academic PDF, converts to clean markdown via a local layout-aware converter, then extracts structured reading notes into `_text.md`. Same output contract as `/split-pdf` but preserves equation fidelity, table structure, and figure references machine-readably. Use when the paper contains tables, equations, or figures that need to be captured (not just described); when batch-processing multiple papers and avoiding repeated vision-read token cost; or when the PDF is already saved locally. Prefer this over `/split-pdf` whenever layout fidelity matters.
allowed-tools: Bash(python3:*), Bash(curl:*), Bash(wget:*), Bash(mkdir:*), Read, Write, WebSearch, WebFetch, Agent
argument-hint: [pdf-path-or-search-query]
---

# Read-PDF: Download, Convert, and Deep-Read Academic Papers

Same I/O contract as /split-pdf: takes a PDF (local or searched), produces a structured `_text.md` extraction with a bibliographic metadata block and 8-dimension research notes. The difference is the reading mechanism: instead of Claude vision-reading PDF page images in chunks, read-pdf converts the PDF to markdown locally using python:marker, then reads the text. This preserves equation fidelity, table structure, and figure references without image-based context bloat.

## When This Skill Is Invoked

The user wants to read, review, or summarize an academic paper and either: (a) wants layout-aware equation/table extraction, or (b) already has a local PDF. The input is either:
- A file path to a local PDF (e.g., `~/Documents/papers/smith_2024.pdf`)
- A search query or paper title (e.g., `"Gentzkow Shapiro Sinkinson 2014 competition newspapers"`)

**Important:** You cannot search for a paper you don't know exists. Provide either a file path or a specific query. If the user invokes this skill without specifying a paper, ask them.

## Prerequisites

- **Python ≥ 3.10** must be available. `install.py` refuses to proceed on Python 3.9 or older. If needed: `brew install python@3.12`, `apt install python3.11`, or python.org installer.
- **Optional GPU acceleration** is auto-detected: NVIDIA CUDA → CPU. (MPS on Apple Silicon is excluded — surya's layout model crashes on MPS at runtime.)

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

## Step 2: Ensure the converter is installed

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

## Step 3: Convert

**Before converting, check for a cached conversion.** Compute the SHA-256 hash of the PDF and check whether `markdown.md` already exists in the cache:

```python
import hashlib, os, sys

pdf_path = "<absolute-pdf-path>"

with open(pdf_path, 'rb') as f:
    pdf_hash = hashlib.sha256(f.read()).hexdigest()

markdown_path = os.path.expanduser(
    f'~/.cache/claude-pdf-converter/cache/marker/{pdf_hash}/markdown.md'
)
print(markdown_path if os.path.exists(markdown_path) else "NOT_CACHED")
```

- **If cached:** tell the user "Using cached markdown conversion (SHA-256 match), skipping re-conversion." Use the printed path as `markdown_path`.
- **If not cached:** run:
  ```bash
  python3 ~/.claude/skills/read-pdf/convert.py "<pdf-path>"
  ```
  It prints the absolute path to `markdown.md` on success and exits 0. For born-digital PDFs with a usable embedded text layer, `convert.py` uses that text layer and disables marker's full-document OCR path while preserving marker's layout/table processing. **Do not fall back to pdftotext or any other tool on failure** — surface the error and stop. The whole point of this skill is the layout-aware conversion; a degraded fallback produces silently-wrong output.

## Step 4: Check for existing `_text.md`

Look for `<basename>_text.md` in the same folder as the PDF.

If found, ask:
> "An extract already exists (`<basename>_text.md`). Overwrite it, or save the new extraction as `<basename>_text2.md`?"

Proceed using whichever filename the user chooses.

## Step 5: Structured Extraction

Read `markdown.md` and collect notes following the contract in `extraction_schema.md` — a `## Bibliographic metadata` block from the title section, then 8 research dimensions (research question, audience, method, data, statistical methods, findings, contributions, replication feasibility). Read `extraction_schema.md` before starting so you know what to look for.

Write the final structured extraction to `<basename>_text.md` (or `_text2.md` if chosen in Step 4) in the same folder as the source PDF, with the `## Bibliographic metadata` block first. Then notify the user: *"Extract saved to `<basename>_text.md` alongside the source PDF. Future requests on this paper can reuse it without re-reading."*

## Agent Isolation

When `/read-pdf` is invoked by another skill or workflow, the markdown read + extraction step must run in a subagent to prevent `markdown.md` token bloat in the parent conversation. See `agent_isolation.md` for the launch pattern and rationale.

## Files in this skill

- `SKILL.md` — this file (acquire → install → cache-check → convert → extract workflow)
- `extraction_schema.md` — bibliographic metadata block + 8 research dimensions (shared output contract with `/split-pdf`)
- `agent_isolation.md` — subagent launch pattern for when this skill is invoked by another workflow
- `install.py` — idempotent marker venv installer with monthly advisory check
- `convert.py` — PDF → markdown converter (writes to SHA-256-keyed cache)
- `README.md` — backend details, cache management, GPU notes
