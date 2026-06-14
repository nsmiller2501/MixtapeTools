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

# A numeric figure caption anchored at the start of a line (after any markdown
# markup), capturing the figure number. Used to build the document-order map of
# captioned figures for ordinal matching. The terminator mirrors caption_regex.
NUMERIC_CAPTION_RE = re.compile(
    r"^[\s*#>_]*Fig(?:ure|\.)?\s+(\d+)(?::|\.(?=[\s*]|$)|(?=[\s*])|$)",
    re.IGNORECASE,
)


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


def image_positions(lines: list[str]) -> list[tuple[int, str]]:
    """Every image reference in document order as ``(line_index, source_ref)``."""
    return [
        (line_number, source_ref)
        for line_number, line in enumerate(lines)
        for source_ref in IMAGE_RE.findall(line)
    ]


def captioned_figure_images(lines: list[str], images: list[tuple[int, str]]) -> dict[int, int]:
    """Map each captioned numeric figure to the line of its adjacent image.

    Only captions (label at line start) are used, so the map is reliable. The
    image nearest each caption line is taken as that figure's image; on a tie the
    earlier image wins (marker emits a caption's image close to it either side).
    """
    image_lines = [line_number for line_number, _ in images]
    captioned: dict[int, int] = {}
    for line_number, line in enumerate(lines):
        match = NUMERIC_CAPTION_RE.match(line)
        if not match:
            continue
        number = int(match.group(1))
        if number in captioned or not image_lines:
            continue
        nearest = min(image_lines, key=lambda ln: (abs(ln - line_number), ln))
        captioned[number] = nearest
    return captioned


def ordinal_source_ref(lines: list[str], images: list[tuple[int, str]], figure_label: str) -> str | None:
    """Locate a caption-less figure's image by its ordinal position.

    Figures are numbered in document order and marker emits images in document
    order, so figure N's image must lie between the images of the nearest
    captioned figures that bracket it numerically. This does not depend on
    whether the image sits before or after any in-text mention. Returns ``None``
    when the label is non-numeric or the bracketing is ambiguous (e.g. a gap of
    several missing captions, or extra/multi-panel images between brackets), in
    which case the caller falls back to mention proximity.
    """
    if not figure_label.isdigit() or not images:
        return None
    target = int(figure_label)
    captioned = captioned_figure_images(lines, images)
    if target in captioned or not captioned:
        return None

    lower = [number for number in captioned if number < target]
    higher = [number for number in captioned if number > target]
    lo = max(lower) if lower else None
    hi = min(higher) if higher else None
    lo_img = captioned[lo] if lo is not None else None
    hi_img = captioned[hi] if hi is not None else None

    # Images strictly between the bracketing figures' own images, in order.
    between = [
        source_ref
        for line_number, source_ref in images
        if (lo_img is None or line_number > lo_img)
        and (hi_img is None or line_number < hi_img)
    ]
    if not between:
        return None

    if lo is not None and hi is not None:
        # Confident only when the count of images matches the count of missing
        # figures between the brackets (one image per figure, no extras).
        if len(between) != hi - lo - 1:
            return None
        index = target - lo - 1
    elif lo is not None:  # target sits above every captioned figure
        index = target - lo - 1
    else:                 # target sits below every captioned figure
        index = target - 1
    return between[index] if 0 <= index < len(between) else None


def find_source_ref(
    markdown: str,
    figure_label: str,
    lookback_lines: int,
    lookahead_lines: int,
) -> str:
    lines = markdown.splitlines()
    caption_re = caption_regex(figure_label)
    images = image_positions(lines)

    # Caption lines (label at line start, after markdown markup) are reliable
    # anchors; inline prose mentions ("appear in Figure 3") are not. Collect the
    # nearest image to each kind separately.
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
                    # A figure's image usually follows its first in-text mention;
                    # prefer the forward image on a tie. This is the last-resort
                    # heuristic, used only when ordinal matching cannot resolve.
                    direction_priority = 0 if line_number >= i else 1
                    ref_priority = ref_number if line_number >= i else -ref_number
                    mention_candidates.append((distance, direction_priority, ref_priority, source_ref))

    # 1. This figure has its own caption -> its adjacent image is the match.
    if caption_candidates:
        return min(caption_candidates)[3]

    # 2. No caption for this figure -> place it ordinally between the images of
    #    its captioned neighbours (robust to image-before/after-mention).
    ordinal = ordinal_source_ref(lines, images, figure_label)
    if ordinal is not None:
        return ordinal

    # 3. Last resort: nearest image to an inline mention.
    if mention_candidates:
        return min(mention_candidates)[3]

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
