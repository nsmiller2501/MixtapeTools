#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF >&2
Usage: check_word_breaks.sh <deck.tex|deck.pdf> [--ignore-pages N,M,...]

Verifies no word breaks across lines. Scans each page via 'pdftotext -layout'
for the pattern \\w{2,}-\\n\\w+ -- catches:
  - LaTeX auto-hyphenation at line end (e.g., extrac- / tion)
  - Compound words wrapping at their internal hyphen (e.g., well- / being)

Applies to ALL text on each page: prose, TikZ nodes, table cells, listings,
captions.

Run AFTER compile_loop.sh exits clean. Exits nonzero on any flagged page.

False positive (legitimate compound at a clean phrase boundary)?
Re-run with --ignore-pages, OR fix the source:
  - \\mbox{whole-word}          -> forbid the break
  - widen the column / TikZ node 'text width'
  - rephrase to avoid the long word at line-end
  - reduce local font size only if other fixes fail
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

pages="$(/opt/homebrew/bin/pdfinfo "$pdf" | awk -F: '/^Pages:/ {gsub(/ /,"",$2); print $2}')"

/usr/local/bin/python3 - "$pdf" "$pages" "$ignore" <<'PY'
import sys, subprocess, re

pdf, pages_s, ignore_arg = sys.argv[1], sys.argv[2], sys.argv[3]
total = int(pages_s)
ignore_set = {int(x) for x in ignore_arg.split(',') if x.strip()}

problems = []
for p in range(1, total + 1):
    if p in ignore_set:
        continue
    txt = subprocess.check_output(
        ['/opt/homebrew/bin/pdftotext', '-layout', '-f', str(p), '-l', str(p), pdf, '-'],
        text=True)
    # \w+- at end of one line, \w+ at start of next (allow leading whitespace).
    # Two-char minimum on prefix avoids false matches on '-' lone bullet glyphs.
    for m in re.finditer(r'(\w{2,}-)\n[ \t]*(\w+)', txt):
        problems.append((p, m.group(1), m.group(2)))

if problems:
    print("Word-break check FAILED. Lines split mid-word or at compound hyphen:")
    for p, before, after in problems:
        print(f"  page {p}: ...{before} / {after}...")
    print()
    print("Fix (SKILL.md Step 2 'Title length and line breaks' + 'Table and node word-break check'):")
    print("  - \\mbox{whole-word}            forbid the break")
    print("  - widen column / TikZ node `text width`")
    print("  - rephrase to avoid the long word at line-end")
    print("  - reduce local font size only if other fixes fail")
    print()
    print("False positive (legitimate compound at clean boundary)?")
    print("  Re-run with --ignore-pages N,M")
    sys.exit(1)
else:
    print(f"Word-break check passed ({total} pages checked).")
PY
