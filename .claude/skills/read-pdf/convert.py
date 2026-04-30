#!/usr/bin/env python3
"""
read-pdf converter — PDF → markdown + figures.

Caches by SHA-256 of the PDF bytes. Re-running on the same content is free.

Usage:
    python3 convert.py <pdf-path>

Prints the absolute path to the cached markdown.md on success (exit 0).
On backend failure, exits non-zero with the error on stderr — no fallback.

Cache layout:
    ~/.cache/claude-pdf-converter/cache/<sha256>/
        markdown.md       # verbatim conversion with inline ![](figures/...)
        figures/*.png     # extracted figures (and equations if image-fallback)
        meta.json         # backend, version, page/figure counts, source path
"""

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

BACKEND = os.environ.get("PDF_BACKEND", "docling")  # "docling" | "marker"
CACHE_ROOT = Path.home() / ".cache" / "claude-pdf-converter"
# Cache is namespaced by backend — different backends produce different output
# for the same PDF, so they must not share cache entries.
CACHE_DIR = CACHE_ROOT / "cache" / BACKEND
VENV_PYTHON = CACHE_ROOT / f"venv-{BACKEND}" / "bin" / "python"
SKILL_DIR = Path(__file__).resolve().parent


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def in_venv() -> bool:
    try:
        return Path(sys.executable).resolve() == VENV_PYTHON.resolve()
    except FileNotFoundError:
        return False


def reexec_in_venv(args: list[str]) -> None:
    """Re-run this script under the backend venv's Python."""
    if not VENV_PYTHON.exists():
        installer = SKILL_DIR / "install.py"
        subprocess.run([sys.executable, str(installer)], check=True)
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), str(Path(__file__).resolve()), *args])


# ---------------------------------------------------------------------------
# Backend implementations
# ---------------------------------------------------------------------------
# These are skeletons against the published APIs. Verify and refine after the
# bake-off — in particular: figure-iteration APIs, equation-mode detection,
# and table-rendering options vary between backend versions.

def convert_with_docling(pdf_path: Path, out_dir: Path) -> dict:
    from docling.document_converter import DocumentConverter

    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    doc = result.document

    figures_dir = out_dir / "figures"
    figures_dir.mkdir(exist_ok=True)

    md = doc.export_to_markdown()

    fig_count = 0
    for i, picture in enumerate(getattr(doc, "pictures", []) or []):
        try:
            img = picture.get_image(doc) if hasattr(picture, "get_image") else None
            if img is None:
                continue
            img_path = figures_dir / f"fig_{i + 1}.png"
            img.save(img_path)
            fig_count += 1
        except Exception as exc:  # pragma: no cover — best-effort extraction
            print(f"warn: figure {i + 1} extraction failed: {exc}", file=sys.stderr)

    (out_dir / "markdown.md").write_text(md, encoding="utf-8")

    page_count = None
    pages_attr = getattr(doc, "pages", None)
    if pages_attr is not None:
        try:
            page_count = len(pages_attr)
        except TypeError:
            page_count = None

    return {
        "backend": "docling",
        "page_count": page_count,
        "figure_count": fig_count,
        # TODO post-bake-off: detect when docling emitted equations as LaTeX
        # vs. left them as raster blocks. Set "image_fallback" if the latter,
        # and write equation crops to figures/eq_*.png for vision transcription.
        "equation_extraction_mode": "native",
    }


def convert_with_marker(pdf_path: Path, out_dir: Path) -> dict:
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered

    converter = PdfConverter(artifact_dict=create_model_dict())
    rendered = converter(str(pdf_path))
    text, _, images = text_from_rendered(rendered)

    figures_dir = out_dir / "figures"
    figures_dir.mkdir(exist_ok=True)

    fig_count = 0
    for name, img in (images or {}).items():
        out_name = figures_dir / Path(name).name
        try:
            img.save(out_name)
            fig_count += 1
        except Exception as exc:  # pragma: no cover
            print(f"warn: figure {name} save failed: {exc}", file=sys.stderr)

    (out_dir / "markdown.md").write_text(text, encoding="utf-8")

    return {
        "backend": "marker",
        "page_count": None,
        "figure_count": fig_count,
        "equation_extraction_mode": "native",  # marker emits LaTeX directly
    }


BACKENDS = {
    "docling": convert_with_docling,
    "marker": convert_with_marker,
}


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: convert.py <pdf-path>", file=sys.stderr)
        return 2

    pdf_path = Path(sys.argv[1]).expanduser().resolve()
    if not pdf_path.is_file():
        print(f"error: not a file: {pdf_path}", file=sys.stderr)
        return 2

    if not in_venv():
        reexec_in_venv([str(pdf_path)])

    digest = sha256_of(pdf_path)
    out_dir = CACHE_DIR / digest
    md_path = out_dir / "markdown.md"
    if md_path.is_file():
        print(str(md_path))
        return 0

    backend_fn = BACKENDS.get(BACKEND)
    if backend_fn is None:
        print(f"error: unknown backend {BACKEND!r}", file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    info = backend_fn(pdf_path, out_dir)
    info.update(
        {
            "source_path": str(pdf_path),
            "sha256": digest,
            "elapsed_seconds": round(time.time() - started, 2),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    )
    (out_dir / "meta.json").write_text(
        json.dumps(info, indent=2), encoding="utf-8"
    )
    print(str(md_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
