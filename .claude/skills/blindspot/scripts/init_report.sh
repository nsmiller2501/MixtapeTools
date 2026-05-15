#!/usr/bin/env sh
set -eu

slug="${*:-blindspot-report}"

slug="$(
  printf '%s' "$slug" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//'
)"

if [ -z "$slug" ]; then
  slug="blindspot-report"
fi

report_dir="correspondence/blindspot"
mkdir -p "$report_dir"

date_prefix="$(date +%F)"
path="$report_dir/${date_prefix}_${slug}.md"
counter=2

while [ -e "$path" ]; do
  path="$report_dir/${date_prefix}_${slug}_${counter}.md"
  counter=$((counter + 1))
done

: > "$path"
printf '%s\n' "$path"
