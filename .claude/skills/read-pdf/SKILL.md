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

If the chosen backend (post-bake-off) reproduces equations as LaTeX math mode (`$...$` / `$$...$$`) inline in `markdown.md`, no further work is needed.

If `meta.json` reports `equation_extraction_mode: "image_fallback"`, equations were clipped as images into `figures/eq_*.png`. In that case, after Step 2 launch a vision sub-agent to transcribe each `eq_*.png` to LaTeX math mode and edit the markdown to replace the image references with the transcribed math. Prompt skeleton:

```
Read the image at <path>. It is a single equation clipped from an academic paper.
Transcribe it as LaTeX, in display math mode ($$ ... $$). Output only the LaTeX —
no commentary, no surrounding text. If the equation is not legible, output the
literal string "[unreadable equation]".
```

Do this in a sub-agent, not the main session — equation images would otherwise pile into the parent's context.

`equation_extraction_mode` values: `"native"` (backend produced LaTeX directly — no fallback needed) or `"image_fallback"` (vision transcription required).

## Cache management

- The cache is keyed by SHA-256 of the PDF bytes. Re-saving the same PDF under a new name produces a cache hit.
- Cache entries are not auto-evicted. To force a re-conversion, delete the entry:

  ```bash
  rm -rf ~/.cache/claude-pdf-converter/cache/<sha256>/
  ```

- To wipe the entire cache (e.g., after a backend upgrade): `rm -rf ~/.cache/claude-pdf-converter/cache/`. The venv at `~/.cache/claude-pdf-converter/venv/` is untouched.

## Backend

The conversion backend is configured in `convert.py` via the `PDF_BACKEND` constant. Currently selectable: `docling` or `marker`. Final selection pending bake-off on `_bakeoff_pdf2md/` test PDFs — see [README.md](README.md) for the bake-off rubric and current pin versions.

## Quick Reference

| Step | Action |
|------|--------|
| **Install** | `python3 ~/.claude/skills/read-pdf/install.py` (idempotent; downloads models on first run) |
| **Convert** | `python3 ~/.claude/skills/read-pdf/convert.py <pdf>` (prints path to `markdown.md`) |
| **Equation fallback** | If `meta.json:equation_extraction_mode == "image_fallback"`, transcribe `figures/eq_*.png` via vision sub-agent |
| **Cache** | Keyed by SHA-256 of PDF bytes; located at `~/.cache/claude-pdf-converter/cache/<hash>/` |
| **Failure mode** | Hard fail. No silent fallback to pdftotext or other tools. |

For background on backend selection and the bake-off, see [README.md](README.md).
