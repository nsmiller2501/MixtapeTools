# `/newproject-git` — Initialize Project Version Control

Initializes git versioning for a newly scaffolded or legacy research project.

## Usage

```
/newproject-git
```

Run it from the project root after `/newproject`, or from an existing research project that does not yet have a `.git` directory.

## What It Does

- Runs `git init` if the project is not already a git repository.
- Marks `.git` as ignored by Dropbox sync when supported by the host system.
- Creates a research-project `.gitignore` from `.claude/skills/newproject-git/templates/.gitignore`.
- Shows `git status` before committing so large binaries, raw data, or credentials can be caught.
- Creates the initial legacy-import commit when the repository has no prior commits.

## Safety Rules

- Never commit `data/raw/` or credential files.
- If `.gitignore` already exists, review it instead of overwriting it.
- If the project already has commits, skip the import commit and report the current log.

The executable protocol lives in [`.claude/skills/newproject-git/SKILL.md`](../../.claude/skills/newproject-git/SKILL.md).

---

*This skill originated in [Scott Cunningham](https://github.com/scunning1975/MixtapeTools)'s MixtapeTools repository.*
