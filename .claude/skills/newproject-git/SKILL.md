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

Read `~/.claude/skills/newproject-git/templates/.gitignore` and write those exact contents to `.gitignore` in the project root. **If `.gitignore` already exists, review it rather than overwriting — ask the user before making changes.**

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
