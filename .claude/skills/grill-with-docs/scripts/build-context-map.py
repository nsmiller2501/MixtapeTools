#!/usr/bin/env python3
"""Rebuild agent_memory/CONTEXT-MAP.md from the filesystem.

Scope detection: any directory under agent_memory/ that contains CONTEXT.md
or NOTES.md (or both).

Cross-cutting detection: top-level *.md files in agent_memory/ excluding
CONTEXT.md, NOTES.md, and CONTEXT-MAP.md.

User-written descriptions (the text after "—" on each bullet) are preserved
across rebuilds. Structure (the path portion) is regenerated from the
filesystem and is never read back as authoritative.

Single-purpose mode: if no scope subdirectories exist (only top-level files),
the script removes any existing CONTEXT-MAP.md and exits without writing.

Invocation:

    python3 build-context-map.py <path-to-agent_memory>

The script is idempotent: running twice with no filesystem change produces
identical output.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SCOPE_MARKERS = ("CONTEXT.md", "NOTES.md")
EXCLUDED_TOPLEVEL = {"CONTEXT.md", "NOTES.md", "CONTEXT-MAP.md"}
SEPARATOR = "—"
COLUMN = 38  # pad path to this width before the "—" separator


# ----------------------------------------------------------------------
# Filesystem discovery
# ----------------------------------------------------------------------


def find_scopes(agent_memory: Path) -> list[str]:
    """Return scope paths relative to agent_memory, with trailing slash.

    Root scope ("/") is included if agent_memory itself contains a scope
    marker. Other scopes are returned as "stage/" or "stage/module/" etc.
    """
    scopes: list[str] = []

    # Root scope
    if any((agent_memory / m).is_file() for m in SCOPE_MARKERS):
        scopes.append("/")

    # Nested scopes — walk the tree, skip docs/ subtree (ADRs live there)
    for child in agent_memory.rglob("*"):
        if not child.is_dir():
            continue
        rel = child.relative_to(agent_memory)
        if rel.parts and rel.parts[0] == "docs":
            continue  # docs/adr/ etc. are not scopes
        if any((child / m).is_file() for m in SCOPE_MARKERS):
            scopes.append(f"{rel}/")

    scopes.sort(key=_scope_sort_key)
    return scopes


def find_cross_cutting(agent_memory: Path) -> list[str]:
    """Return top-level .md filenames that count as cross-cutting."""
    files = [
        p.name
        for p in agent_memory.iterdir()
        if p.is_file() and p.suffix == ".md" and p.name not in EXCLUDED_TOPLEVEL
    ]
    files.sort()
    return files


def _scope_sort_key(path: str) -> tuple:
    """Sort scopes alphabetically per level, with numeric prefixes sorted numerically."""
    if path == "/":
        return ((0,),)
    parts = path.rstrip("/").split("/")
    key = []
    for part in parts:
        m = re.match(r"^(\d+)(.*)$", part)
        if m:
            key.append((1, int(m.group(1)), m.group(2)))
        else:
            key.append((2, 0, part))
    return tuple(key)


# ----------------------------------------------------------------------
# Description preservation
# ----------------------------------------------------------------------


# Match a bullet line. The path is in backticks. The description is the text
# (possibly empty) after the "—" separator.
BULLET_RE = re.compile(
    r"^\s*-\s*`([^`]+)`\s*(?:" + re.escape(SEPARATOR) + r"\s*(.*))?$"
)


def parse_existing_descriptions(map_path: Path) -> dict[str, str]:
    """Parse the existing CONTEXT-MAP.md and return path -> description."""
    if not map_path.is_file():
        return {}

    descriptions: dict[str, str] = {}
    for line in map_path.read_text(encoding="utf-8").splitlines():
        m = BULLET_RE.match(line)
        if not m:
            continue
        path = m.group(1)
        desc = (m.group(2) or "").rstrip()
        if desc:
            descriptions[path] = desc
    return descriptions


# ----------------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------------


def render_bullet(path: str, description: str, indent: int) -> str:
    """Render a single bullet with aligned separator column."""
    prefix = "  " * indent + f"- `{path}`"
    padding = max(1, COLUMN - len(prefix))
    if description:
        return f"{prefix}{' ' * padding}{SEPARATOR} {description}"
    return f"{prefix}{' ' * padding}{SEPARATOR}"


def compute_indent(scope: str, all_scopes: set[str]) -> int:
    """Indent equals the number of ancestor scopes actually present in the tree.

    A scope only indents under a parent that exists as a scope. If
    `analyze/structural/` is a scope but `analyze/` is not, the deeper path
    renders at depth 0 — the hierarchy lives in the path string, not in
    visual indent under a phantom parent.
    """
    if scope == "/":
        return 0
    parts = scope.rstrip("/").split("/")
    indent = 0
    for i in range(1, len(parts)):
        ancestor = "/".join(parts[:i]) + "/"
        if ancestor in all_scopes:
            indent += 1
    return indent


def render_scope_bullet(scope: str, descriptions: dict[str, str], all_scopes: set[str]) -> str:
    indent = compute_indent(scope, all_scopes)
    desc = descriptions.get(scope, "")
    return render_bullet(scope, desc, indent)


def render_cross_cutting_bullet(name: str, descriptions: dict[str, str]) -> str:
    return render_bullet(name, descriptions.get(name, ""), indent=0)


def render_map(
    scopes: list[str],
    cross_cutting: list[str],
    descriptions: dict[str, str],
) -> str:
    lines = ["# Context Map", ""]

    lines.append("## Scopes")
    lines.append("")
    if scopes:
        scope_set = set(scopes)
        for scope in scopes:
            lines.append(render_scope_bullet(scope, descriptions, scope_set))
    else:
        lines.append("_No scopes yet._")
    lines.append("")

    lines.append("## Cross-cutting files")
    lines.append("")
    if cross_cutting:
        for name in cross_cutting:
            lines.append(render_cross_cutting_bullet(name, descriptions))
    else:
        lines.append("_None._")
    lines.append("")

    return "\n".join(lines)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------


def build_context_map(agent_memory: Path) -> int:
    if not agent_memory.is_dir():
        print(f"error: {agent_memory} is not a directory", file=sys.stderr)
        return 2

    scopes = find_scopes(agent_memory)
    cross_cutting = find_cross_cutting(agent_memory)
    map_path = agent_memory / "CONTEXT-MAP.md"

    # Single-purpose mode: only root-level files, no nested scopes worth mapping.
    has_nested_scopes = any(s != "/" for s in scopes)
    if not has_nested_scopes and not cross_cutting:
        if map_path.is_file():
            map_path.unlink()
            print(f"removed {map_path} (single-purpose mode, no scopes/cross-cutting)")
        else:
            print("single-purpose mode, no map needed")
        return 0

    descriptions = parse_existing_descriptions(map_path)
    rendered = render_map(scopes, cross_cutting, descriptions)
    map_path.write_text(rendered, encoding="utf-8")
    print(f"wrote {map_path} ({len(scopes)} scopes, {len(cross_cutting)} cross-cutting files)")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Rebuild agent_memory/CONTEXT-MAP.md.")
    parser.add_argument(
        "agent_memory",
        type=Path,
        help="Path to the project's agent_memory/ directory.",
    )
    args = parser.parse_args(argv)
    return build_context_map(args.agent_memory.resolve())


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
