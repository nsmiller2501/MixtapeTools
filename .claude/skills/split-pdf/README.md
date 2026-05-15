# `/split-pdf` — Deep-Read Academic Papers

`/split-pdf` reads academic PDFs carefully without overloading the session. It downloads or uses a local PDF, splits it into small chunks, reads those chunks in batches, and writes a persistent structured extraction next to the original PDF.

The executable protocol lives in [`SKILL.md`](SKILL.md). The rationale for the batching design lives in [`methodology.md`](methodology.md).

## When To Use It

Use `/split-pdf` when you want Claude or Codex to read, review, or summarize an academic paper and ordinary PDF reading would be too large or too shallow.

Prefer `/read-pdf` when the paper has tables, equations, or figures that need machine-readable layout capture rather than image-based reading notes.

## What It Produces

- The original PDF remains in place and is never deleted.
- Split PDFs are written under `<foldername>_build/split_<basename>/`.
- Working notes are accumulated as `notes.md` inside the split directory.
- The final reusable extraction is saved as `<basename>_text.md` next to the PDF.

The extraction records bibliographic metadata plus the research question, audience, method, data, statistical methods, findings, contribution, and replication feasibility.

## How It Works

The skill reads 4-page chunks in small batches, pausing between batches during standalone use so the user can correct course before errors compound. When another skill calls it, PDF reading should run in a subagent so page images do not bloat the parent session.

Those operational details belong in [`SKILL.md`](SKILL.md), not in this README. If you need the exact pause-and-confirm protocol, directory convention, or extraction checklist, read the skill file.

## Related Skills

- `/read-pdf` — preferred for layout-sensitive extraction.
- `/wiki-update` — uses the same batched-reading idea when ingesting references into a project wiki.

---

The in-place PDF handling, persistent `_text.md` extraction, split reuse, build directory convention, and agent isolation protocol were inspired by improvements identified by [Ben Bentzin](https://www.mccombs.utexas.edu), who adapted the original skill for his workflows and shared his findings in April 2026.

This skill originated in [Scott Cunningham](https://github.com/scunning1975/MixtapeTools)'s MixtapeTools repository.
