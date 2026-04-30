#!/usr/bin/env python3
"""
read-pdf installer — sets up the local PDF→markdown converter.

Idempotent. First run creates a per-backend venv at
~/.cache/claude-pdf-converter/venv-<backend>/, installs the backend, and
warms up model downloads. Subsequent runs short-circuit if the backend imports
cleanly under the venv.

Per-backend venvs mean PDF_BACKEND=marker and PDF_BACKEND=docling can coexist
on the same machine — the bake-off can run both without reinstalling.

The venvs live outside any git repo so that backend models (~hundreds of MB)
do not pollute the skills checkout.
"""

import os
import subprocess
import sys
from pathlib import Path

# Backend selection. Final pin chosen post-bake-off; see read-pdf/README.md.
# Override via PDF_BACKEND env var to test the other backend without editing.
BACKEND = os.environ.get("PDF_BACKEND", "docling")  # "docling" | "marker"

# Version pins are placeholders — confirm + update after bake-off.
PINS = {
    "docling": ["docling==2.14.0"],
    "marker": ["marker-pdf==0.3.10"],
}

CACHE_ROOT = Path.home() / ".cache" / "claude-pdf-converter"
VENV_DIR = CACHE_ROOT / f"venv-{BACKEND}"


def venv_python() -> Path:
    return VENV_DIR / "bin" / "python"


def venv_exists() -> bool:
    return venv_python().exists()


def backend_imports() -> bool:
    if not venv_exists():
        return False
    module = "docling" if BACKEND == "docling" else "marker"
    result = subprocess.run(
        [str(venv_python()), "-c", f"import {module}"],
        capture_output=True,
    )
    return result.returncode == 0


def create_venv() -> None:
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    print(
        f"First run: creating venv at {VENV_DIR} and installing "
        f"{BACKEND} (~500MB, 1–3 min, one-time).",
        flush=True,
    )
    subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    subprocess.run(
        [str(venv_python()), "-m", "pip", "install", "--upgrade", "pip"],
        check=True,
    )
    pkgs = PINS.get(BACKEND)
    if not pkgs:
        print(f"error: unknown backend {BACKEND!r}", file=sys.stderr)
        sys.exit(2)
    subprocess.run(
        [str(venv_python()), "-m", "pip", "install", *pkgs],
        check=True,
    )


def warmup_models() -> None:
    """Trigger first-run model download so the first conversion is fast."""
    print("Downloading layout/OCR models (one-time)...", flush=True)
    if BACKEND == "docling":
        warmup = (
            "from docling.document_converter import DocumentConverter; "
            "DocumentConverter()"
        )
    elif BACKEND == "marker":
        warmup = (
            "from marker.models import create_model_dict; create_model_dict()"
        )
    else:
        return
    subprocess.run([str(venv_python()), "-c", warmup], check=True)


def main() -> int:
    if backend_imports():
        return 0
    if not venv_exists():
        create_venv()
    warmup_models()
    print(f"read-pdf setup complete. Backend: {BACKEND}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
