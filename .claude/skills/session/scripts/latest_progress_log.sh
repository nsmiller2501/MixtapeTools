#!/usr/bin/env sh
set -eu

log_dir="${1:-progress_logs}"

if [ ! -d "$log_dir" ]; then
  echo "No progress log directory found: $log_dir" >&2
  exit 1
fi

latest="$(
  find "$log_dir" -maxdepth 1 -type f -name '*.md' -print \
    | sort -r \
    | head -n 1
)"

if [ -z "$latest" ]; then
  echo "No progress logs found in: $log_dir" >&2
  exit 1
fi

printf '%s\n' "$latest"
