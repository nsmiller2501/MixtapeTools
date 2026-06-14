#!/usr/bin/env python3
"""Copy a marker-extracted paper figure into a project's wiki figure folder.

The caller supplies the paper's figure number, not a cache filename. The script
finds the nearest markdown image around the matching caption -- both the
``Figure N`` style and the Springer/ERE ``Fig. N`` style (including bold
``**Fig. N**``) are recognized -- copies it to ``references/wiki/figures/``,
and prints the wiki-relative link.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

from PIL import Image


IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def caption_regex(figure_label: str) -> re.Pattern[str]:
    """Match common figure captions across the ``Figure N`` and Springer/ERE
    ``Fig. N`` conventions without confusing Figure 1.2 for Figure 1."""
    # Prefix accepts "Figure", "Fig.", or bare "Fig". Terminator requires the
    # label to be followed by a colon, an end-of-token period (incl. one closing
    # a bold caption like ``**Figure 1.**``), whitespace, a bold marker
    # (``**Fig. N**``), or end of line -- so "Figure 1" never matches
    # "Figure 1.2" or "Figure 14".
    return re.compile(
        rf"\bFig(?:ure|\.)?\s+{re.escape(figure_label)}(?::|\.(?=[\s*]|$)|(?=[\s*])|$)",
        re.IGNORECASE,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Copy marker figure to wiki figures.")
    parser.add_argument("markdown", type=Path, help="Path to marker markdown.md")
    parser.add_argument("wiki_figures_dir", type=Path, help="Project references/wiki/figures dir")
    parser.add_argument("--basename", required=True, help="Canonical paper basename")
    parser.add_argument("--figure", required=True, help="Paper figure label, e.g. 4 or A.1")
    parser.add_argument("--lookback-lines", type=int, default=8)
    parser.add_argument("--lookahead-lines", type=int, default=8)
    return parser.parse_args()


def canonical_suffix(path: Path) -> str:
    with Image.open(path) as image:
        if image.format == "JPEG":
            return ".jpg"
        if image.format == "PNG":
            return ".png"
        if image.format:
            return f".{image.format.lower()}"
    return path.suffix.lower()


def find_source_ref(
    markdown: str,
    figure_label: str,
    lookback_lines: int,
    lookahead_lines: int,
) -> str:
    lines = markdown.splitlines()
    caption_re = caption_regex(figure_label)

    # Collect image candidates from caption lines and inline prose mentions
    # separately. A real caption begins with the figure label (after any
    # markdown markup); an inline mention has it mid-sentence. Inline mentions
    # typically precede the figure's image and sit close to a neighbouring
    # figure's image, so they must never outrank a caption.
    caption_candidates: list[tuple[int, int, int, str]] = []
    mention_candidates: list[tuple[int, int, int, str]] = []
    for i, line in enumerate(lines):
        if not caption_re.search(line):
            continue
        is_caption = bool(caption_re.match(line.lstrip(" \t*#>_")))

        start = max(0, i - lookback_lines)
        stop = min(len(lines), i + lookahead_lines + 1)
        for line_number in range(start, stop):
            source_refs = IMAGE_RE.findall(lines[line_number])
            for ref_number, source_ref in enumerate(source_refs):
                distance = abs(line_number - i)
                if is_caption:
                    # Marker may emit a caption's image just before or after it;
                    # keep the nearest, preferring backward on a tie (legacy).
                    direction_priority = 0 if line_number <= i else 1
                    ref_priority = -ref_number if line_number <= i else ref_number
                    caption_candidates.append((distance, direction_priority, ref_priority, source_ref))
                else:
                    # A figure's image follows its first in-text mention; prefer
                    # the forward image on a tie so a mention does not grab the
                    # previous figure's image sitting just above it.
                    direction_priority = 0 if line_number >= i else 1
                    ref_priority = ref_number if line_number >= i else -ref_number
                    mention_candidates.append((distance, direction_priority, ref_priority, source_ref))

    for candidates in (caption_candidates, mention_candidates):
        if candidates:
            return min(candidates)[3]
    raise SystemExit(f"figure {figure_label} image reference not found")


def resolve_source_path(markdown_path: Path, source_ref: str) -> Path:
    source_path = (markdown_path.parent / source_ref).resolve()
    if source_path.is_file():
        return source_path

    ref_parts = Path(source_ref).parts
    if len(ref_parts) >= 2 and ref_parts[0] == ref_parts[1]:
        deduped_ref = Path(*ref_parts[1:])
        deduped_path = (markdown_path.parent / deduped_ref).resolve()
        if deduped_path.is_file():
            return deduped_path

    raise SystemExit(f"figure source not found: {source_path}")


def main() -> int:
    args = parse_args()
    markdown_path = args.markdown.expanduser().resolve()
    wiki_figures_dir = args.wiki_figures_dir.expanduser().resolve()
    markdown = markdown_path.read_text(encoding="utf-8", errors="replace")

    source_ref = find_source_ref(markdown, args.figure, args.lookback_lines, args.lookahead_lines)
    source_path = resolve_source_path(markdown_path, source_ref)

    suffix = canonical_suffix(source_path)
    wiki_figures_dir.mkdir(parents=True, exist_ok=True)
    dest_path = wiki_figures_dir / f"{args.basename}_fig{args.figure}{suffix}"
    shutil.copy2(source_path, dest_path)
    print(f"figures/{dest_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
