# CONTEXT-MAP.md Format

`CONTEXT-MAP.md` is the project's table of contents for `agent_memory/`. It shows the scope tree and registers top-level cross-cutting files. Future agents read it first to orient.

The map is **rebuilt by `scripts/build-context-map.py`** — never edit the structure by hand. User-written descriptions are preserved across rebuilds.

## Structure

```md
# Context Map

## Scopes

- `/`                                — project-wide glossary and notes
- `acquire/`                         — data acquisition stage
  - `acquire/firm_registry/`        — Chinese firm registry scrape (2010 snapshot)
  - `acquire/customs/`               — customs records pull, 2011-2015
- `analyze/`                         — analysis stage
  - `analyze/descriptive/`           — descriptive statistics, sample profiles
  - `analyze/structural/`            — structural model estimation
- `write/`                           —

## Cross-cutting files

- `sample_restrictions.md`           — sample inclusion/exclusion rules
- `key_decisions.md`                 — project-level methodology decisions
- `codebook.md`                      — variable definitions, units
- `dropped_analyses.md`              — abandoned approaches with reasons
```

### Components

- **Header**: `# Context Map`. Fixed.
- **Scopes section**: tree of scope paths with optional descriptions. Indented to show hierarchy. Order: alphabetical at each level, with numeric prefixes sorted numerically.
- **Cross-cutting section**: flat list of top-level `agent_memory/*.md` files (excluding `CONTEXT.md`, `NOTES.md`, `CONTEXT-MAP.md`).

### Description preservation

Each bullet has the form:

```
- `<path>/`                          — <user description>
```

The script:
- Regenerates the path/`/` portion from the filesystem.
- Preserves anything after the first `—` separator as user-editable description.
- For new entries, emits a blank description: `- acquire/firm_registry/   —`. The user (or the skill during grilling) fills it in.

## Helper script

`scripts/build-context-map.py` does the heavy lifting. The skill invokes it; the LLM never edits the tree structure directly.

### Invocation

```bash
python3 ~/.claude/skills/grill-with-docs/scripts/build-context-map.py <path-to-agent_memory>
```

### When to invoke

1. **Any new scope directory** at any depth (after `mkdir agent_memory/.../<new-scope>/`).
2. **Cross-cutting file discovery** — first time a session runs, or any time the user adds a top-level `.md`.
3. **User trigger** — phrases like "refresh map", "rebuild map", "update context-map".
4. **Session start sanity check** — cheap, fast, idempotent.

### Script contract

- **Input**: path to `agent_memory/` directory.
- **Output**: writes/overwrites `<agent_memory>/CONTEXT-MAP.md`.
- **Scope detection**: a directory is a "scope" if it contains `CONTEXT.md` OR `NOTES.md` (or both).
- **Cross-cutting detection**: top-level `.md` files in `agent_memory/`, excluding `CONTEXT.md`, `NOTES.md`, `CONTEXT-MAP.md`.
- **Description preservation**: parses existing CONTEXT-MAP.md, matches bullets by path, keeps text after `—`. New paths get blank description.
- **Idempotent**: running twice with no filesystem change produces identical output.
- **Stable sort**: alphabetical at each level, numeric prefixes sorted numerically (`02_build` before `10_analyze`).
- **No semantic decisions**: never invents descriptions, never guesses what a scope means.

### Single-purpose mode

If `agent_memory/` contains only top-level files and no scope subdirectories, the script can either:

- Omit `CONTEXT-MAP.md` entirely (no scopes to map, single-purpose).
- Or emit a minimal map showing just the root and any cross-cutting files.

Default behavior: omit. The skill creates `CONTEXT-MAP.md` only when a second scope appears.

## Writing descriptions during grilling

When the skill creates a new scope, it should fill in the bullet's description in the next CONTEXT-MAP rebuild. The flow:

1. User confirms new scope: `acquire/firm_registry/`.
2. Skill `mkdir`s the directory and writes first `CONTEXT.md` or `NOTES.md` content.
3. Skill runs the helper script. The new bullet appears with a blank description.
4. Skill edits the CONTEXT-MAP.md to fill in the description, using the user's stated intent (e.g. "Chinese firm registry scrape (2010 snapshot)"). This is a normal markdown edit — the structure stays untouched, only the description text changes.

Subsequent script runs will preserve that description.
