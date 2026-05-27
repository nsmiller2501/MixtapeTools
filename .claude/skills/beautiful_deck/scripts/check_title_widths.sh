#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF >&2
Usage: check_title_widths.sh <deck.tex|deck.pdf> [--ignore-pages N,M,...]

Verifies every frametitle fits on one line. Uses 'pdftohtml -xml' to extract
text-line elements with coordinates. For each page, finds the topmost text
line and defines the title region as that line's bbox plus 1.6x its own
height downward; >=2 distinct line baselines in that region = wrap.

This adapts to actual title position (no hardcoded band), so it works across
themes regardless of where the frametitle sits or what font size it uses.

Run AFTER compile_loop.sh exits clean. Exits nonzero on any flagged page.

False positive (decorative top text, custom title slide, section divider)?
Re-run with --ignore-pages listing the offending page numbers.

The script is style-agnostic: it does NOT know the deck's font, frametitle
template, or rule position. It only asks "does the top band hold >1 line of
text?" -- which is the property we care about.
EOF
  exit 2
}

[ "$#" -ge 1 ] || usage

input="$1"; shift
ignore=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --ignore-pages) ignore="$2"; shift 2;;
    -h|--help) usage;;
    *) usage;;
  esac
done

case "$input" in
  *.tex) pdf="${input%.tex}.pdf";;
  *.pdf) pdf="$input";;
  *) echo "Input must be .tex or .pdf" >&2; exit 2;;
esac

[ -f "$pdf" ] || { echo "PDF not found: $pdf (compile first)" >&2; exit 1; }

/usr/local/bin/python3 - "$pdf" "$ignore" <<'PY'
import sys, subprocess, re

pdf, ignore_arg = sys.argv[1], sys.argv[2]
ignore_set = {int(x) for x in ignore_arg.split(',') if x.strip()}

# Title region (per-page, adaptive): topmost text element's bbox extended
# downward by TITLE_HEIGHT_MULT * that element's height. A second wrapped
# line in the SAME font would land inside this region.
# Height filter: within that region, only count lines whose font height is
# within HEIGHT_TOL_FRAC of the first line. Wrapped title lines share font
# height with line 1; smaller body text below the title does not.
# Right-edge filter: text whose left > RIGHT_FRAC * page_width is treated
# as header decoration (page numbers, crests). Filtered out.
# Line tolerance: two text elements with |top_a - top_b| <= TOL_PX are the
# same visual line (some themes split title into multiple <text> spans).
TITLE_HEIGHT_MULT = 1.6
HEIGHT_TOL_FRAC = 0.20
RIGHT_FRAC = 0.85
TOL_PX = 3.0
TOP_FRAC_HARD_CAP = 0.30  # absolute ceiling; anything below this is body

xml = subprocess.check_output(
    ['/opt/homebrew/bin/pdftohtml', '-xml', '-stdout', '-i', '-q', pdf],
    text=True, stderr=subprocess.DEVNULL)

# Per-page parsing. <page number="N" height="H" width="W">...<text top="T" left="L" ...>...</text>...
page_re = re.compile(
    r'<page\s+number="(\d+)"[^>]*?\bheight="([\d.]+)"\s+width="([\d.]+)"[^>]*>(.*?)</page>',
    re.DOTALL)
text_re = re.compile(
    r'<text\s+top="([\d.]+)"\s+left="([\d.]+)"\s+width="([\d.]+)"\s+height="([\d.]+)"[^>]*>(.*?)</text>',
    re.DOTALL)
tag_strip = re.compile(r'<[^>]+>')

problems = []
total_pages = 0
for m in page_re.finditer(xml):
    pnum = int(m.group(1))
    ph = float(m.group(2))
    pw = float(m.group(3))
    body = m.group(4)
    total_pages = max(total_pages, pnum)
    if pnum in ignore_set:
        continue
    right_max_x = pw * RIGHT_FRAC
    hard_cap_y = ph * TOP_FRAC_HARD_CAP

    candidates = []
    for t in text_re.finditer(body):
        top = float(t.group(1))
        left = float(t.group(2))
        height = float(t.group(4))
        if left > right_max_x:
            continue
        raw = tag_strip.sub('', t.group(5)).strip()
        if not raw:
            continue
        candidates.append((top, height, raw))

    if not candidates:
        continue

    candidates.sort(key=lambda r: r[0])
    first_top, first_h, _ = candidates[0]
    title_band_max = min(first_top + first_h * TITLE_HEIGHT_MULT, hard_cap_y)
    height_tol = max(first_h * HEIGHT_TOL_FRAC, 1.0)
    # Title-band texts: in the region AND with font height similar to first.
    # Body text below the title has smaller font height and is filtered out.
    in_band = [
        (top, txt) for (top, h, txt) in candidates
        if top <= title_band_max and abs(h - first_h) <= height_tol
    ]
    if len(in_band) < 2:
        continue

    in_band.sort(key=lambda r: r[0])
    distinct_tops = [in_band[0][0]]
    for top, _ in in_band[1:]:
        if abs(top - distinct_tops[-1]) > TOL_PX:
            distinct_tops.append(top)

    if len(distinct_tops) >= 2:
        joined = ' / '.join(txt for _, txt in in_band)
        problems.append((pnum, joined))

if problems:
    print("Title-wrap check FAILED. Pages with multi-line title band:")
    for p, t in problems:
        print(f"  page {p}: {t}")
    print()
    print("Fix order (SKILL.md Step 2 'Title length and line breaks'):")
    print("  1. Keep assertion, drop setup words.")
    print("  2. Replace clause with sharper verb.")
    print("  3. Move qualifiers to caption / next slide.")
    print("  4. Split the slide.")
    print()
    print("False positive (decorative text, title slide, section divider)?")
    print("  Re-run with --ignore-pages N,M")
    sys.exit(1)
else:
    print(f"Title-wrap check passed ({total_pages} pages checked).")
PY
