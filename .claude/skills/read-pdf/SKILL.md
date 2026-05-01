---
name: read-pdf
description: Convert academic PDFs to clean markdown with extracted tables and figures, locally. Layout-aware conversion preserves equation fidelity, table structure, and figure clips. Output is cached by content hash so re-converting the same PDF is free. Use when a workflow needs a markdown representation of a PDF's content (read-pdf is the local-conversion counterpart to split-pdf, which offloads PDF reading to Anthropic's servers).
allowed-tools: Bash(python3:*), Bash(mkdir:*), Bash(cp:*), Read, Write, Agent
argument-hint: [pdf-path]
---

# read-pdf: Local PDF → markdown converter

Converts a PDF into a single markdown file with inline figure references and a sidecar `figures/` directory of extracted images. Designed for academic papers: equations preserved as math-mode LaTeX, tables as pipe-syntax markdown, figures clipped pixel-accurately and referenced inline.

The output is cached by SHA-256 of the source PDF in `~/.cache/claude-pdf-converter/cache/<hash>/`. Subsequent invocations on the same file return the cached path immediately.

## When This Skill Is Invoked

The user (or another skill, e.g. `wiki-update-local`) wants a clean markdown rendering of a PDF. The argument is a path to a local PDF.

If the user gave a search query rather than a path, ask them to download the PDF first — this skill does not handle acquisition.

## Prerequisites

- **Python ≥ 3.10** must be available on the host (any OS — macOS, Linux, Windows). The installer in Step 1 will refuse to proceed if it can only find Python 3.9 or older. If `python3 --version` reports < 3.10, install a newer Python first (`brew install python@3.12`, `apt install python3.11`, `winget install Python.Python.3.12`, or python.org installer) before invoking this skill.
- **Optional GPU acceleration** is auto-detected and used when available, in priority order: NVIDIA CUDA → Apple Silicon MPS → CPU. Acceleration is transparent — no flags needed. On an M-series Mac or a CUDA box, expect a 3–5× speedup over CPU.

## Step 1: Ensure the converter is installed

The converter runs in a dedicated Python venv at `~/.cache/claude-pdf-converter/venv/`. The first invocation on a fresh machine creates this venv and downloads the layout/OCR models (~500 MB, 1–3 min). Subsequent invocations short-circuit.

Run:

```bash
python3 ~/.claude/skills/read-pdf/install.py
```

`install.py` is idempotent. If the venv already exists and the backend imports cleanly, it exits immediately. On first run, it prints:

> First run: creating venv at ~/.cache/claude-pdf-converter/venv and installing <backend> (~500MB, 1–3 min, one-time).

Surface that message to the user verbatim if it appears — they should know why this invocation is slow.

## Step 2: Convert

Run:

```bash
python3 ~/.claude/skills/read-pdf/convert.py "<pdf-path>"
```

`convert.py` prints the absolute path to the resulting `markdown.md` on success and exits 0. On failure it exits non-zero and prints the backend's error to stderr — **do not fall back to pdftotext or any other tool**. Surface the error to the user and stop. The whole point of this skill is the layout-aware conversion; a degraded fallback would hide bugs and produce silently-wrong conversions.

The cache layout for each PDF:

```
~/.cache/claude-pdf-converter/cache/<sha256>/
├── markdown.md       # verbatim conversion with inline ![](figures/fig_N.png)
├── figures/          # extracted images, pixel-accurate clips
│   ├── fig_1.png
│   └── ...
└── meta.json         # backend, version, page count, source path, timestamp
```

Cache hits are silent — `convert.py` just prints the path. Cache misses run the backend and print the same path.

## Step 3: Hand off the markdown

Read the printed `markdown.md` path and either:

- Return it to the calling skill (typical use), or
- For standalone invocation, summarize what's in it: page count, figure count (read `meta.json`), and a one-paragraph topic summary derived from the first ~500 words of the markdown.

When another skill calls `read-pdf` programmatically, it should invoke `convert.py` directly (bash) rather than spawning `/read-pdf` as a slash command — slash invocation re-enters Claude unnecessarily and adds latency. The script is the contract; the skill is the user-facing wrapper.

## Equations

Marker emits equations as LaTeX math mode (`$...$` inline, `$$...$$` display) directly in `markdown.md`. No vision fallback is required. `meta.json` records `equation_extraction_mode: "native"` for traceability.

## Cache management

- The cache is keyed by SHA-256 of the PDF bytes. Re-saving the same PDF under a new name produces a cache hit.
- Cache entries are not auto-evicted. To force a re-conversion, delete the entry:

  ```bash
  rm -rf ~/.cache/claude-pdf-converter/cache/<sha256>/
  ```

- To wipe the entire cache (e.g., after a backend upgrade): `rm -rf ~/.cache/claude-pdf-converter/cache/`. The venv at `~/.cache/claude-pdf-converter/venv/` is untouched.

## Backend

The conversion backend is **marker** (`marker-pdf`). Selected after a head-to-head bake-off against docling on a representative set of empirical-economics PDFs; marker won on equation fidelity, table structure, and figure extraction quality.

Backend selection is fixed in `convert.py`. There is no runtime override — if the bake-off needs to be redone for a future backend candidate, edit the `BACKEND` constant explicitly so the cache namespace and venv are regenerated cleanly.

## Quick Reference

| Step | Action |
|------|--------|
| **Install** | `python3 ~/.claude/skills/read-pdf/install.py` (idempotent; downloads models on first run) |
| **Convert** | `python3 ~/.claude/skills/read-pdf/convert.py <pdf>` (prints path to `markdown.md`) |
| **Cache** | Keyed by SHA-256 of PDF bytes; located at `~/.cache/claude-pdf-converter/cache/marker/<hash>/` |
| **GPU** | Auto-detected (CUDA → MPS → CPU). No flag needed. |
| **Failure mode** | Hard fail. No silent fallback to pdftotext or other tools. |
