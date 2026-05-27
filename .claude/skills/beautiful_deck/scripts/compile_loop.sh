#!/usr/bin/env bash
set -euo pipefail

# Parse flags: --render-pages dumps PNG previews to a temp dir for visual
# inspection (the multimodal Read tool can ingest PNGs but not PDFs).
# Keeps scratch artifacts out of the deck folder.
render_pages=0
args=()
for a in "$@"; do
  case "$a" in
    --render-pages) render_pages=1;;
    *) args+=("$a");;
  esac
done
set -- "${args[@]+"${args[@]}"}"

if [ "$#" -ne 1 ]; then
  echo "Usage: compile_loop.sh <deck.tex> [--render-pages]" >&2
  exit 2
fi

tex_file="$1"

if [ ! -f "$tex_file" ]; then
  echo "File not found: $tex_file" >&2
  exit 1
fi

work_dir="$(cd "$(dirname "$tex_file")" && pwd)"
base_name="$(basename "$tex_file")"
stem="${base_name%.tex}"
log_file="$work_dir/$stem.log"
pdf_file="$work_dir/$stem.pdf"
compile_output="$(mktemp "${TMPDIR:-/tmp}/beautiful_deck_compile.XXXXXX")"
trap 'rm -f "$compile_output"' EXIT

(
  cd "$work_dir"
  pdflatex -interaction=nonstopmode "$base_name" >"$compile_output" 2>&1 || true
)

if [ ! -f "$log_file" ]; then
  echo "Compile did not produce log file: $log_file" >&2
  echo "pdflatex output:" >&2
  cat "$compile_output" >&2
  exit 1
fi

fatal_count="$(grep -c '^!' "$log_file" || true)"
box_count="$(grep -cE 'Overfull|Underfull' "$log_file" || true)"
font_count="$(grep -i 'warning' "$log_file" | grep -ci 'font' || true)"
reference_count="$(grep -i 'warning' "$log_file" | grep -ciE 'reference|label|citation' || true)"

printf 'Compile check: %s\n' "$tex_file"
printf 'PDF: %s\n' "$pdf_file"
printf 'Fatal errors: %s\n' "$fatal_count"
printf 'Overfull/Underfull: %s\n' "$box_count"
printf 'Font warnings: %s\n' "$font_count"
printf 'Reference/label/citation warnings: %s\n' "$reference_count"

if [ "$fatal_count" -gt 0 ]; then
  printf '\n## Fatal errors\n'
  grep -n '^!' "$log_file" || true
fi

if [ "$box_count" -gt 0 ]; then
  printf '\n## Overfull/Underfull warnings\n'
  grep -nE 'Overfull|Underfull' "$log_file" || true
fi

if [ "$font_count" -gt 0 ]; then
  printf '\n## Font warnings\n'
  grep -in 'warning' "$log_file" | grep -i 'font' || true
fi

if [ "$reference_count" -gt 0 ]; then
  printf '\n## Reference/label/citation warnings\n'
  grep -in 'warning' "$log_file" | grep -iE 'reference|label|citation' || true
fi

if [ "$render_pages" = 1 ] && [ -f "$pdf_file" ]; then
  render_dir="$(mktemp -d "${TMPDIR:-/tmp}/beautiful_deck_render.XXXXXX")"
  /opt/homebrew/bin/pdftoppm -png -r 150 "$pdf_file" "$render_dir/page"
  printf '\nRendered pages (PNG, 150dpi): %s/\n' "$render_dir"
fi

if [ "$fatal_count" -gt 0 ] || [ "$box_count" -gt 0 ] || [ "$font_count" -gt 0 ] || [ "$reference_count" -gt 0 ]; then
  exit 1
fi
