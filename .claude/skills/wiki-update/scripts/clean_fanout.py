#!/usr/bin/env python3
"""Remove a paper's regenerable raw_build scratch after a successful ingest.

``references/raw/raw_build/`` holds only intermediates: the Protocol M fanout
directory (worker notes and the citation-overlap scan) and Protocol S split
PDFs. All are regenerable from the immutable PDF plus the converter cache, so
they are deleted once the paper's wiki page, ``_text.md``, and bib entry exist.
Protocol S's ``notes.md`` is the deliberate exception (a permanent audit trail)
and is preserved.

The cleanup is deterministic and bounded: it only ever touches paths inside a
directory literally named ``raw_build``.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean a paper's raw_build scratch.")
    parser.add_argument("raw_build_dir", type=Path, help="Project references/raw/raw_build dir")
    parser.add_argument("--basename", required=True, help="Canonical paper basename")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw_build = args.raw_build_dir.expanduser().resolve()

    # Safety guard: only ever operate inside a directory literally named raw_build.
    if raw_build.name != "raw_build":
        raise SystemExit(f"refusing to clean: not a raw_build directory: {raw_build}")

    removed: list[str] = []

    # Protocol M: the whole per-paper fanout scratch dir (worker notes + overlap).
    fanout = raw_build / f"{args.basename}_fanout"
    if fanout.is_dir():
        shutil.rmtree(fanout)
        removed.append(str(fanout))

    # Legacy flat citation-overlap location, written by pre-consolidation runs.
    legacy_overlap = raw_build / f"{args.basename}_citation_overlap.json"
    if legacy_overlap.is_file():
        legacy_overlap.unlink()
        removed.append(str(legacy_overlap))

    # Protocol S: drop the regenerable split PDFs but keep the permanent notes.md.
    split_dir = raw_build / f"split_{args.basename}"
    if split_dir.is_dir():
        for pdf in sorted(split_dir.glob("*.pdf")):
            pdf.unlink()
            removed.append(str(pdf))

    if removed:
        for path in removed:
            print(f"removed {path}")
    else:
        print(f"nothing to clean for {args.basename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
