---
name: newproject-git
description: Initializes git versioning for a new research project. Handles `git init`, Dropbox sync exclusion, `.gitignore` creation, and the initial legacy-import commit. Use when starting version control on a freshly scaffolded project or on an existing project that has no `.git` directory yet.
allowed-tools: Bash(git*), Bash(xattr*), Bash(ls*), Read, Write, Edit
argument-hint: ''
---

# Skill: newproject-git

Initialize git versioning for a new research project. Handles git init, Dropbox exclusion, .gitignore creation, and the initial legacy-import commit.

## When to use

Run at the start of any project that doesn't yet have a `.git` directory. Typically follows `/newproject`. Safe to run on an already-initialized repo — each step checks before acting.

## Steps

### 1. Git init (if needed)

Check whether `.git` exists in the current working directory:

```bash
ls -d .git 2>/dev/null
```

If not present, initialize:

```bash
git init
```

### 2. Dropbox exclusion

Exclude the `.git` folder from Dropbox sync (harmless if the project isn't in Dropbox):

```bash
xattr -w com.dropbox.ignored 1 .git
```

### 3. Create .gitignore

Write the following `.gitignore` to the project root. **If `.gitignore` already exists, review it rather than overwriting — ask the user before making changes.**

```
# macOS
.DS_Store

# Claude Code project settings
.claude/

# Obsidian vault settings
.obsidian/

# Personal scratch notes
notes/

# Correspondence: ignore internal read-only artifact folders only.
# Add project-specific subdirs here (e.g. correspondence/referee2/).
# Submission/journal correspondence should be tracked.
# Also ignore internal replication check code etc.
correspondence/referee2/
correspondence/blindspot/
code/replication/

# Data (raw, intermediate, clean — not versioned; reproduce from pipeline)
/data/

# Decks: track only .tex source files
decks/**
!decks/**/
!decks/**/*.tex

# Documents: track only .tex source files
documents/**
!documents/**/
!documents/**/*.tex

# Meeting notes
meetings/

# All pipeline/analysis output (logs, tables, figures)
output/

# Progress logs
progress_logs/

# Reference PDFs (track .bib, not raw PDFs); 
# articles catches this directory in case it's accidentally created by split-pdf/read-pdf
references/raw/
references/wiki/
references/CLAUDE.md
articles/

# Scratch (holds any files temporarily while I decide where they go)
scratch/

# Log files (Stata, Python, R)
*.log

# LaTeX build artifacts
*.aux
*.bbl
*.bcf
*.blg
*.fdb_latexmk
*.fls
*.run.xml
*.synctex.gz
*.toc
*.out
*.lof
*.lot
```

After writing, show the user what will be tracked (`git status`) and flag anything that looks unexpected (large binaries, sensitive files, etc.). Ask before proceeding.

### 4. Initial legacy-import commit

Stage everything not excluded by `.gitignore`:

```bash
git add .
```

Then commit:

```bash
git commit -m "Import legacy codebase

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Report the commit hash and file count to the user.

## Notes

- Never commit `data/raw/` or credential files. If they appear in `git status` output, stop and ask the user to confirm the `.gitignore` is correct.
- The `decks/**` / `!decks/**/` / `!decks/**/*.tex` pattern requires git 1.8.2+. It tracks `.tex` source files but ignores compiled PDFs and images.
- If the project already has commits, skip step 4 and report the existing log to the user.
