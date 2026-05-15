# `/read-pdf` — Local PDF → markdown converter

**Skill location:** [`.claude/skills/read-pdf/SKILL.md`](../../.claude/skills/read-pdf/SKILL.md)

---

## What This Skill Does

You give Claude a path to a PDF and the skill returns a clean markdown rendering of its content — equations as LaTeX math mode, tables as pipe-syntax markdown, and figures clipped pixel-accurately into a `figures/` directory and referenced inline. The conversion runs locally via marker inside a dedicated Python venv. Output is cached by SHA-256 of the PDF bytes, so subsequent invocations on the same file return immediately.

It is the **local-conversion counterpart to `/split-pdf`**:

| Skill | Where the PDF is parsed | Best for |
|---|---|---|
| `/split-pdf` | Anthropic's servers (via Read on PDF chunks) | First-time users, no local install, narrative reading flow |
| `/read-pdf` | Your machine (marker in a venv) | Repeated processing, table/figure fidelity, batch reference ingest |

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
├── venv-marker/                          # one-time marker install
└── cache/
    └── marker/
        └── <sha256-of-pdf>/
            ├── markdown.md               # verbatim conversion + inline ![](figures/...)
            ├── figures/
            │   ├── fig_1.png             # extracted images
            │   └── fig_2.png
            └── meta.json                 # backend, page/figure counts, timestamp
```

| Step | Action |
|------|--------|
| **Install** | `python3 ~/.claude/skills/read-pdf/install.py` (idempotent; downloads models on first run only, then reuses the venv; monthly advisory check for marker major updates) |
| **Convert** | `python3 ~/.claude/skills/read-pdf/convert.py <pdf>` (cache check → backend → write markdown + figures) |
| **Hand off** | The script prints the absolute path to `markdown.md`; the caller reads it |

### Usage

```
/read-pdf path/to/paper.pdf
```

When called by another skill, the caller invokes `convert.py` directly via bash rather than spawning `/read-pdf` as a slash command — the script is the contract.

### First-run cost

The first invocation on a fresh machine creates a venv at `~/.cache/claude-pdf-converter/venv-marker/` and downloads the backend's layout/OCR models (~500 MB, 1–3 min). The skill prints a one-line warning so the user knows why it's slow. Every subsequent invocation reuses that venv if `marker` imports cleanly; it does not auto-upgrade marker.

The venv lives **outside any git repo** so the model files do not pollute a checkout.

---

## Equations

Marker emits equations as LaTeX math mode (`$...$` / `$$...$$`) inline in the markdown. The skill does not run an image-fallback equation transcription path.

---

## Backend Selection

`convert.py` uses marker (`marker-pdf`). Backend selection is fixed in code; there is no runtime backend override. If a future bake-off chooses a different backend, edit the `BACKEND` constant so the cache namespace and venv are regenerated cleanly.

`install.py` installs the current PyPI `marker-pdf` release only when the marker venv is first created. If marker already imports cleanly, setup reuses it and performs at most one lightweight PyPI check every 30 days. It warns only when PyPI has crossed a marker major-version boundary, and it never auto-upgrades.

If you opt into a major upgrade, run:

```bash
python3 ~/.claude/skills/read-pdf/install.py --upgrade-marker
```

Existing cached conversions remain in place. To force fresh conversions after upgrading, delete selected cache entries under `~/.cache/claude-pdf-converter/cache/marker/`, or delete that whole directory. Rebuilding a large cache can be very time-consuming.

---

## Failure Mode

Hard fail. If the backend errors on a given PDF (encrypted, malformed, OCR fails), the script exits non-zero and the caller surfaces the error. There is no silent fallback to `pdftotext` or any other tool — silent fallbacks would produce potentially wrong conversions that may look fine on inspection.

---

## Limitations

- **First-run is slow** — venv creation + model download takes 1–3 minutes. After that, conversion of a typical 30-page paper takes ~30s–2min depending on backend and CPU/GPU.
- **GPU acceleration is conservative** — CUDA is used when available; Apple Silicon MPS is deliberately disabled because surya's layout model crashes on MPS.
- **Cache is not auto-evicted** — re-converting the same PDF is free, but the cache grows monotonically. Wipe with `rm -rf ~/.cache/claude-pdf-converter/cache/` if needed.

---

## Acknowledgments

The design — layout-aware local conversion, content-hashed caching, an isolated venv, and pixel-accurate figure clipping — is shaped by the realities of academic-paper ingestion at scale. Marker is an open-source project whose authors did the actual hard work of making layout-aware PDF parsing tractable.

This skill originated in [Scott Cunningham](https://github.com/scunning1975/MixtapeTools)'s MixtapeTools repository.
