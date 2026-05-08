# `/newproject-git` — Git Initialization for Research Projects

Initializes git versioning for a new research project. Typically run immediately after `/newproject`.

## Usage

```
/newproject-git
```

Run from the project root (the directory that contains `CLAUDE.md`).

## What It Does

1. **`git init`** — initializes the repository if `.git` doesn't already exist.
2. **Dropbox exclusion** — sets `com.dropbox.ignored` on `.git` so Dropbox skips it.
3. **`.gitignore`** — writes a standard research `.gitignore` covering data directories, LaTeX build artifacts, macOS junk, and Claude Code internals. Prompts before overwriting an existing file.
4. **Initial commit** — stages everything not excluded and makes a single "Import legacy codebase" commit.

## What Gets Tracked

Source code, `.tex` files, `.bib`, `CLAUDE.md`, `README.md`, and other text files. Explicitly excluded:

- `data/` (raw, intermediate, clean — reproduce from pipeline)
- `output/` (tables, figures — regenerate from code)
- `references/raw/` and `references/wiki/` (PDFs and generated wiki)
- `decks/**` and `documents/**` except `.tex` source files
- `.claude/`, `.obsidian/`, `meetings/`, `scratch/`, `notes/`, `progress_logs/`
- LaTeX build artifacts (`*.aux`, `*.bbl`, `*.bcf`, etc.)

## Notes

- Safe to run on an already-initialized repo — each step checks before acting.
- If `data/raw/` or any credential file appears in `git status`, the skill stops and asks for confirmation before committing.
- Pairs with `/newproject`, which creates the directory structure this skill then versions.
