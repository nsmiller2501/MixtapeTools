---
name: split-pdf
description: Downloads, splits, and deeply reads academic PDFs by splitting into 4-page chunks and reading them in small batches — avoiding context-window crashes and shallow comprehension. Use when asked to read, review, or summarize an academic paper without specialized layout needs. Prefer `/read-pdf` instead when the paper contains tables, equations, or figures that need machine-readable capture rather than vision-read description.
allowed-tools: Bash(python*), Bash(pip*), Bash(curl*), Bash(wget*), Bash(mkdir*), Bash(ls*), Read, Write, Edit, WebSearch, WebFetch, Agent
argument-hint: [pdf-path-or-search-query]
---

# Split-PDF: Download, Split, and Deep-Read Academic Papers

**CRITICAL RULE: Never read a full PDF. Never.** Only read the 4-page split files, and only 3 splits at a time (~12 pages). Reading a full PDF will either crash the session with an unrecoverable "prompt too long" error — destroying all context — or produce shallow, hallucinated output. There are no exceptions.

## When This Skill Is Invoked

The user wants you to read, review, or summarize an academic paper. The input is either:
- A file path to a local PDF (e.g., `~/Documents/papers/smith_2024.pdf`)
- A search query or paper title (e.g., `"Gentzkow Shapiro Sinkinson 2014 competition newspapers"`)

**Important:** You cannot search for a paper you don't know exists. The user MUST provide either a file path or a specific search query — an author name, a title, keywords, a year, or some combination that identifies the paper. If the user invokes this skill without specifying what paper to read, ask them. Do not guess.

## Step 1: Acquire the PDF

**If a local file path is provided:**
- Verify the file exists
- Use the PDF in place. The working directory is the folder containing the PDF.
- Proceed to Step 2

**If a search query or paper title is provided:**
1. Use WebSearch to find the paper
2. Use WebFetch or Bash (curl/wget) to download the PDF
3. Save it to the current working directory (create the directory if needed)
4. Proceed to Step 2

**CRITICAL: Always preserve the original PDF.** The source PDF must NEVER be deleted, moved, or overwritten at any point in this workflow. The split files are derivatives; the original is the permanent artifact. Do not clean up, do not remove, do not tidy. The original stays.

## Step 2: Split the PDF

**Reuse checks (in order, before splitting):**

1. **Existing extract.** Look for `<basename>_text.md` next to the PDF. If found, ask: *"An extract already exists (`<basename>_text.md`). Use it, or re-read from scratch?"* On **Use**, read `_text.md` as the source notes and skip the rest of Steps 2 and 3. On **Re-read**, continue.
2. **Existing splits.** Look for `<foldername>_build/split_<pdf-basename>/*.pdf`. If found, ask: *"Splits already exist (N chunks). Reuse, or re-split?"* On **Reuse**, proceed to Step 3 with existing files. On **Re-split**, delete the split folder and continue.

Create splits by running:

```bash
python3 ~/.claude/skills/split-pdf/scripts/split.py path/to/paper.pdf
```

**Directory convention:**
```
articles/                             # any working folder
├── smith_2024.pdf                    # original PDF — NEVER DELETE THIS
├── smith_2024_text.md                # structured extract — created after deep-read
└── articles_build/                   # <foldername>_build/ — shared build folder
    └── split_smith_2024/             # split_<pdf-basename>/
        ├── smith_2024_pp1-4.pdf
        ├── smith_2024_pp5-8.pdf
        ├── smith_2024_pp9-12.pdf
        ├── notes.md                  # working copy — source for _text.md
        └── ...
```

The `<foldername>_build/` convention keeps split artifacts and other working files separate from source and finished outputs. Multiple PDFs in the same folder share one build directory.

If PyPDF2 is not installed: `pip install PyPDF2`.

## Step 3: Read in Batches of 3 Splits

Read **exactly 3 split files at a time** (~12 pages). After each batch:

1. **Read** the 3 split PDFs using the Read tool
2. **Update** the running notes file (`notes.md` in the split subdirectory)
3. **Pause** and tell the user:

> "I have finished reading splits [X-Y] and updated the notes. I have [N] more splits remaining. Would you like me to continue with the next 3?"

4. **Wait** for the user to confirm before reading the next batch

Do NOT read ahead. Do NOT read all splits at once. The pause-and-confirm protocol is mandatory.

## Step 4: Structured Extraction

As you read, collect notes into `notes.md` (in the split subdirectory) following the contract in `extraction_schema.md` — a `## Bibliographic metadata` block from the first split, then 8 research dimensions (research question, audience, method, data, statistical methods, findings, contributions, replication feasibility). Read `extraction_schema.md` before starting Step 3 so you know what to look for in each batch.

Update `notes.md` incrementally after each batch — do not rewrite from scratch; update whichever dimensions have new information.

**After all batches are complete**, write the final notes to `<basename>_text.md` in the same folder as the source PDF (with the `## Bibliographic metadata` block first), then notify the user: *"Extract saved to `<basename>_text.md` alongside the source PDF. Future requests on this paper can reuse it without re-reading."*

`_text.md` is the persistent artifact; `notes.md` is the working copy. Both are kept — never delete either.

## Agent Isolation

When `/split-pdf` is invoked by another skill or workflow, PDF reading must run in a subagent to prevent PDF-image context bloat in the parent conversation. See `agent_isolation.md` for the launch pattern and rationale.

## When NOT to Split

- Papers shorter than ~15 pages: read directly (still use the Read tool, not Bash)
- Policy briefs or non-technical documents: a rough summary is fine
- Triage only: read just the first split (pages 1-4) for abstract and introduction

## Files in this skill

- `SKILL.md` — this file (acquire → split → batch-read → extract workflow)
- `extraction_schema.md` — bibliographic metadata block + 8 research dimensions (shared output contract with `/read-pdf`)
- `agent_isolation.md` — subagent launch pattern for when this skill is invoked by another workflow
- `methodology.md` — why batched reading works
- `scripts/split.py` — PyPDF2 4-page splitter
- `README.md` — human-facing overview and acknowledgments
