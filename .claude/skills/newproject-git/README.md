# `/newproject-git` — Git Initialization For Research Projects

`/newproject-git` initializes version control for a research project, usually right after `/newproject` scaffolds the directory structure.

The executable protocol lives in [`SKILL.md`](SKILL.md). This README is the human overview.

## Usage

```bash
/newproject-git
```

Run it from the project root, the directory that contains `CLAUDE.md`.

## What It Does

- Initializes git if the project does not already have a `.git` directory.
- Marks `.git` as ignored by Dropbox when applicable.
- Writes the standard research `.gitignore`, asking before replacing an existing one.
- Checks for obvious sensitive or heavyweight files before committing.
- Creates the initial import commit.

## What It Tracks

The intended tracked surface is source code, text, LaTeX source, BibTeX, project documentation, and other reproducible inputs. Generated output, raw data, large PDFs, local notes, scratch files, Claude internals, and LaTeX build artifacts are excluded by default.

For the exact `.gitignore` contents and safety checks, read [`SKILL.md`](SKILL.md).

## Related Skills

- `/newproject` — scaffolds the project this skill versions.
