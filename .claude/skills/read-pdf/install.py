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
import shutil
import subprocess
import sys
from pathlib import Path

# Backend selection. Final pin chosen post-bake-off; see read-pdf/README.md.
# Override via PDF_BACKEND env var to test the other backend without editing.
BACKEND = os.environ.get("PDF_BACKEND", "docling")  # "docling" | "marker"

# Version pins. Both backends require Python 3.10+ for current releases.
# Pre-bake-off placeholders — confirm + tighten after bake-off.
PINS = {
    "docling": ["docling"],          # latest; pin post-bake-off
    "marker": ["marker-pdf"],        # latest; pin post-bake-off
}

# Both backends require Python ≥3.10. macOS system python is often 3.9, so
# search common install locations for a suitable interpreter to use as the
# venv base.
PY_MIN = (3, 10)
PY_CANDIDATES = [
    "python3.13", "python3.12", "python3.11", "python3.10",
    "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13",
    "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12",
    "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11",
    "/opt/homebrew/bin/python3.13",
    "/opt/homebrew/bin/python3.12",
    "/opt/homebrew/bin/python3.11",
    "/opt/homebrew/bin/python3",
]


def find_python() -> str:
    """Return path to a Python ≥3.10. Prefers the running interpreter if it qualifies."""
    if sys.version_info >= PY_MIN:
        return sys.executable
    for cand in PY_CANDIDATES:
        path = shutil.which(cand) if "/" not in cand else (cand if Path(cand).exists() else None)
        if not path:
            continue
        try:
            out = subprocess.check_output(
                [path, "-c", "import sys; print('%d.%d' % sys.version_info[:2])"],
                text=True,
            ).strip()
            major, minor = (int(x) for x in out.split("."))
            if (major, minor) >= PY_MIN:
                return path
        except Exception:
            continue
    print(
        f"error: need Python ≥{PY_MIN[0]}.{PY_MIN[1]} but found only "
        f"{sys.version_info.major}.{sys.version_info.minor}. "
        f"Install Python 3.11+ (e.g. via python.org or homebrew).",
        file=sys.stderr,
    )
    sys.exit(2)

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
    base_python = find_python()
    subprocess.run([base_python, "-m", "venv", str(VENV_DIR)], check=True)
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
