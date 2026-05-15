#!/usr/bin/env bash
# sync-skills.sh — pull skill directories from remotes per skills.manifest.
#
# Format reminder (skills.manifest rows): <id> <mode> <remote> <ref> <source_path>
#   - <source_path> is BOTH the path in the remote and the destination path in our tree (we mirror).
#   - <id> is just a label (used for logs and manifest edits); two rows can refer to the same skill
#     under different directories (e.g. .claude/skills/foo and skills/foo).
#
# Behavior:
#   - For each row with mode=track, copy <remote>/<ref>:<source_path>/ into ./<source_path>/.
#   - If HEAD has local commits touching ./<source_path>/ ahead of <remote>/<ref>, auto-flip that
#     row's mode to `local` and skip (your edits are preserved).
#   - Refuses to run on a dirty working tree (except --dry-run).
#   - mode=local / mode=ignore rows are never touched.
#
# Usage: scripts/sync-skills.sh [--dry-run]

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
MANIFEST="$ROOT/skills.manifest"
DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

if [[ ! -f "$MANIFEST" ]]; then
  echo "error: $MANIFEST not found" >&2
  exit 1
fi

if [[ $DRY_RUN -eq 0 && -n "$(git status --porcelain)" ]]; then
  echo "error: working tree is dirty. Commit or stash first." >&2
  exit 1
fi

# Fetch each referenced remote once.
FETCHED=""
while IFS= read -r line; do
  line="${line%%#*}"
  [[ -z "${line// }" ]] && continue
  read -r id mode remote ref path <<<"$line"
  [[ "$mode" != "track" ]] && continue
  case " $FETCHED " in
    *" $remote "*) ;;
    *)
      if ! git remote get-url "$remote" >/dev/null 2>&1; then
        echo "error: remote '$remote' not configured (referenced by id '$id')" >&2
        echo "  add it with: git remote add $remote <url>" >&2
        exit 1
      fi
      echo "fetching $remote..."
      git fetch --quiet "$remote"
      FETCHED="$FETCHED $remote"
      ;;
  esac
done < "$MANIFEST"

UPDATED=()
FLIPPED=()
UNCHANGED=()
ADDED=()

while IFS= read -r line; do
  stripped="${line%%#*}"
  [[ -z "${stripped// }" ]] && continue
  read -r id mode remote ref path <<<"$stripped"
  [[ "$mode" != "track" ]] && continue

  src="$remote/$ref"
  dst="$path"

  if ! git cat-file -e "$src:$path" 2>/dev/null; then
    echo "warn: $src:$path does not exist; skipping $id" >&2
    continue
  fi

  if [[ -d "$dst" ]]; then
    local_commits=$(git log "$src..HEAD" --oneline -- "$dst" 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$local_commits" -gt 0 ]]; then
      echo "  $id: $local_commits local commit(s) at $dst — flipping to mode=local"
      FLIPPED+=("$id")
      if [[ $DRY_RUN -eq 0 ]]; then
        python3 - "$MANIFEST" "$id" <<'PY'
import sys, re, pathlib
path, target_id = sys.argv[1], sys.argv[2]
p = pathlib.Path(path)
out = []
for ln in p.read_text().splitlines():
    stripped = ln.split("#", 1)[0]
    parts = stripped.split()
    if len(parts) >= 2 and parts[0] == target_id and parts[1] == "track":
        ln = re.sub(r'(\s)track(\s)', r'\1local\2', ln, count=1)
    out.append(ln)
p.write_text("\n".join(out) + "\n")
PY
      fi
      continue
    fi
  fi

  remote_hash=$(git rev-parse "$src:$path")
  local_hash=""
  if [[ -d "$dst" ]]; then
    # Walk HEAD's tree down to $dst to compare tree hashes (handles nested paths).
    local_hash=$(git rev-parse "HEAD:$dst" 2>/dev/null || true)
  fi

  if [[ -n "$local_hash" && "$local_hash" == "$remote_hash" ]]; then
    UNCHANGED+=("$id")
    continue
  fi

  if [[ $DRY_RUN -eq 1 ]]; then
    if [[ -z "$local_hash" ]]; then
      echo "  [dry-run] would add $id at $dst from $src"
      ADDED+=("$id")
    else
      echo "  [dry-run] would update $id at $dst from $src"
      UPDATED+=("$id")
    fi
    continue
  fi

  if [[ -d "$dst" ]]; then
    git rm -rq "$dst"
    UPDATED+=("$id")
  else
    ADDED+=("$id")
  fi
  tmp=$(mktemp -d)
  git archive "$src" "$path" | tar -x -C "$tmp"
  mkdir -p "$(dirname "$dst")"
  mv "$tmp/$path" "$dst"
  rm -rf "$tmp"
  git add "$dst"
done < "$MANIFEST"

echo
echo "=== sync summary ==="
echo "added:     ${#ADDED[@]} ${ADDED[*]:-}"
echo "updated:   ${#UPDATED[@]} ${UPDATED[*]:-}"
echo "unchanged: ${#UNCHANGED[@]} ${UNCHANGED[*]:-}"
echo "flipped to local: ${#FLIPPED[@]} ${FLIPPED[*]:-}"

# Discovery: list directories in <remote>/<ref>:.claude/skills/ or :skills/ with no manifest row.
echo
echo "=== discovery (unclassified upstream skills) ==="
# Known paths = set of source_path values present in the manifest (any mode).
KNOWN_PATHS=$(awk '!/^[[:space:]]*#/ && NF>=5 {print $5}' "$MANIFEST" | sort -u | tr '\n' ' ')
PAIRS=$(awk '!/^[[:space:]]*#/ && NF>=5 && $2!="ignore" {print $3" "$4}' "$MANIFEST" | sort -u)
found_unknown=0
SCAN_PARENTS=(".claude/skills" "skills")
while read -r remote ref; do
  [[ -z "$remote" ]] && continue
  for parent in "${SCAN_PARENTS[@]}"; do
    while read -r entry; do
      [[ -z "$entry" ]] && continue
      candidate="$parent/$entry"
      case " $KNOWN_PATHS " in
        *" $candidate "*) ;;
        *)
          echo "  $remote/$ref:$candidate  (add a row to skills.manifest as track/local/ignore)"
          found_unknown=1
          ;;
      esac
    done < <(git ls-tree -d --name-only "$remote/$ref":"$parent" 2>/dev/null || true)
  done
done <<< "$PAIRS"
[[ $found_unknown -eq 0 ]] && echo "  (none)"

if [[ $DRY_RUN -eq 0 && $(( ${#ADDED[@]} + ${#UPDATED[@]} + ${#FLIPPED[@]} )) -gt 0 ]]; then
  echo
  echo "review with: git status && git diff --cached"
  echo "commit with: git commit -m 'Sync skills from upstream'"
fi
