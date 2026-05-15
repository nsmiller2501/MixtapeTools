# `/read-pdf` — Local PDF → markdown converter

**Skill location:** [`.claude/skills/read-pdf/SKILL.md`](../../.claude/skills/read-pdf/SKILL.md)

---

## What This Skill Does

You give Claude a path to a PDF and the skill returns a clean markdown rendering of its content — equations as LaTeX math mode, tables as pipe-syntax markdown, and figures clipped pixel-accurately into a `figures/` directory and referenced inline. The conversion runs locally via a layout-aware backend (`docling` or `marker`) inside a dedicated Python venv. Output is cached by SHA-256 of the PDF bytes, so subsequent invocations on the same file return immediately.

It is the **local-conversion counterpart to `/split-pdf`**:

| Skill | Where the PDF is parsed | Best for |
|---|---|---|
| `/split-pdf` | Anthropic's servers (via Read on PDF chunks) | First-time users, no local install, narrative reading flow |
| `/read-pdf` | Your machine (docling/marker in a venv) | Repeated processing, table/figure fidelity, batch reference ingest |

Both keep the original PDF untouched. The two skills serve the same general purpose, trading off claude code token usage (/split-pdf) versus local compute requirements (/read-pdf).

---

## Why It Exists

`/split-pdf` does narrative deep-reading well — it splits, reads in batches, and produces an 8-dimension structured extraction. But it has three structural limits:

1. **Tables.** PDF rendering loses table structure. Claude can read the values but cannot reproduce a clean machine-readable table without re-typing it.
2. **Figures.** Claude can describe a figure but cannot extract it as a usable image. 
3. **Equations.** Long equation derivations rendered as PDF images are the most token-expensive content per unit information.

Local layout-aware conversion fixes all three: TableFormer-style models reproduce tables structurally, figure detection clips images pixel-accurately, and equation recognition emits LaTeX directly into the markdown.

---

## How It Works

```
~/.cache/claude-pdf-converter/
├── venv/                                 # one-time install of the chosen backend
└── cache/
    └── <sha256-of-pdf>/
        ├── markdown.md                   # verbatim conversion + inline ![](figures/...)
        ├── figures/
        │   ├── fig_1.png                 # extracted images
        │   └── fig_2.png
        └── meta.json                     # backend, version, page/figure counts, timestamp
```

| Step | Action |
|------|--------|
| **Install** | `python3 ~/.claude/skills/read-pdf/install.py` (idempotent; downloads models on first run only) |
| **Convert** | `python3 ~/.claude/skills/read-pdf/convert.py <pdf>` (cache check → backend → write markdown + figures) |
| **Hand off** | The script prints the absolute path to `markdown.md`; the caller reads it |

### Usage

```
/read-pdf path/to/paper.pdf
```

When called by another skill, the caller invokes `convert.py` directly via bash rather than spawning `/read-pdf` as a slash command — the script is the contract.

### First-run cost

The first invocation on a fresh machine creates a venv at `~/.cache/claude-pdf-converter/venv/` and downloads the backend's layout/OCR models (~500 MB, 1–3 min). The skill prints a one-line warning so the user knows why it's slow. Every subsequent invocation skips this entirely.

The venv lives **outside any git repo** so the model files do not pollute a checkout.

---

## Equations

Equation handling depends on the backend's capability:

- **Native mode** (default for both `docling` and `marker`): equations come through as LaTeX math mode (`$...$` / `$$...$$`) inline in the markdown. No further work.
- **Image-fallback mode** (used only if a backend produces unusable equations on a given paper): equations are clipped as images into `figures/eq_*.png` and a vision sub-agent transcribes them to LaTeX. The skill rewrites the markdown to inline the transcribed math. `meta.json` records `equation_extraction_mode` so the caller knows whether to run the fallback step.

Whether the fallback path is needed will be decided by the bake-off (see below).

---

## Backend Selection (Bake-off)

`convert.py` ships with two backend implementations: `docling` (IBM) and `marker` (VikParuchuri). The default is set at the top of `convert.py`. The decision pending bake-off on real academic PDFs in `_bakeoff_pdf2md/`:

| Dimension | What we're checking |
|---|---|
| **Tables** | Multi-row headers, regression tables with SE/significance, full-width tables |
| **Figures** | Clean PNG extraction, correct inline placement, captions adjacent in markdown |
| **Equations** | Verbatim LaTeX math-mode fidelity — decides native vs. image-fallback path |
| **Two-column layouts** | NBER/AER-style two-column flow, no column bleed |
| **Footnotes** | Proper rendering, not lost or interleaved with body |
| **Table notes / figure notes** | Captured separately from footnotes |
| **References section** | Quality of bibliography rendering (informs whether we need GROBID later) |
| **OCR** | Old scanned papers without a text layer |

To run the bake-off manually with the alternate backend:

```bash
PDF_BACKEND=marker python3 ~/.claude/skills/read-pdf/install.py
PDF_BACKEND=marker python3 ~/.claude/skills/read-pdf/convert.py path/to/test.pdf
```

The `PDF_BACKEND` env var separates venvs per backend (each backend creates its own venv at first install) — running this command does **not** clobber the docling venv.

---

## Failure Mode

Hard fail. If the backend errors on a given PDF (encrypted, malformed, OCR fails), the script exits non-zero and the caller surfaces the error. There is no silent fallback to `pdftotext` or any other tool — silent fallbacks would produce potentially wrong conversions that may look fine on inspection.

---

## Limitations

- **First-run is slow** — venv creation + model download takes 1–3 minutes. After that, conversion of a typical 30-page paper takes ~30s–2min depending on backend and CPU/GPU.
- **No GPU acceleration by default** — both backends run CPU-only out of the box. GPU acceleration is possible but requires extra setup not handled by `install.py`.
- **PDF acquisition is out of scope** — this skill does not download PDFs.
- **Cache is not auto-evicted** — re-converting the same PDF is free, but the cache grows monotonically. Wipe with `rm -rf ~/.cache/claude-pdf-converter/cache/` if needed.

---

## Acknowledgments

The design — layout-aware local conversion, content-hashed caching, an isolated venv, and pixel-accurate figure clipping — is shaped by the realities of academic-paper ingestion at scale. The two candidate backends ([docling](https://github.com/docling-project/docling) and [marker](https://github.com/VikParuchuri/marker)) are open-source projects whose authors did the actual hard work of making layout-aware PDF parsing tractable.

This skill originated in [Scott Cunningham](https://github.com/scunning1975/MixtapeTools)'s MixtapeTools repository.
