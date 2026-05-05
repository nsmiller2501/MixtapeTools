# /newbook — Scaffold a Book Project

A skill that scaffolds a book-shaped project in one step: folders, a `memoir`-based LaTeX skeleton, a custom style with voiced-sidebar callouts, a bibliography stub, a `CLAUDE.md`, a `README.md`, and one chapter file per chapter. Parallel to `/newproject` and `/bibcheck`.

This is the skill that produced *AI Agents and the Research Worker*.

---

## Why this exists

Books are different from research projects. They have parts and chapters, named voices, an editorial standard for prose, a `.bib` that has to be auditable, a future online version, and a long-running rhythm where structure matters more than tooling. `/newproject` is right for an empirical paper. `/newbook` is right for a manuscript.

The skill is opinionated:

- **memoir** as the document class. Maximum flexibility; converts cleanly to HTML for the eventual online version.
- **Palatino** body, **Gov 2001 palette** for color, **voiced sidebars** as the design DNA.
- **One chapter per file** under `chapters/`, all `\input`-ed from `book.tex`. Enables parallel collaboration and HTML conversion.
- **`% SUBSTACK MAP:` placeholder block** in every chapter, so the book stays connected to the Substack drafts that fed it.
- **`flushbottom`** + `\emergencystretch=3em` — fewer overfull-hbox warnings on book-length text.

---

## Usage

```
/newbook ai-agents-book --title="AI Agents and the Research Worker"
```

Arguments:

| Argument | Effect |
|---|---|
| `<slug>` (required) | Folder name. Spaces become dashes; lowercase. |
| `--title="..."` (optional) | Working title. Defaults to title-case of slug. |
| `--chapters=N` (optional) | Number of numbered chapters. Default 11. |

If you invoke with no arguments, the skill asks before creating anything.

---

## What gets scaffolded

```
<slug>/
├── CLAUDE.md                   # Voice cast, lineage rules, do-not list
├── README.md                   # What the book is, how to compile
├── book.tex                    # Main file; \input each chapter
├── style/
│   └── <slug>.sty              # Palette, voiced-sidebar macros, chapter heads
├── chapters/
│   ├── 00_frontmatter.tex      # Title, dedication slot, epigraph, preface
│   ├── 01.tex                  # Chapter stubs with TODO bullets and one voice
│   ├── 02.tex
│   └── …                       # through Chapter N (default 11)
├── bibliography/
│   └── <slug>.bib              # Empty; ready for /bibcheck once populated
├── correspondence/             # Letters and email threads
├── decks/
│   └── README.md               # Pointers (NOT copies) to source decks
├── figures/                    # Generated figures
├── code/                       # Reproducibility examples
├── drafts/                     # Working drafts
├── progress_logs/              # Session continuity
└── substacks/                  # Substack post sources that feed chapters
```

---

## Voice cast (default — customize via CLAUDE.md)

Each `\voice{<name>}{<text>}` sidebar gets a fixed color:

| Voice | Color |
|---|---|
| Fisher | slate |
| Ricardo / Thompson | warmgray |
| Skeptic | charcoal |
| Manager | ocean |
| IC | forest |
| Verifier | crimson |
| Goldin / Katz / Autor / Acemoglu | ocean |
| Schumpeter | warmgray |

Add or rename voices in `style/<slug>.sty` and document the cast in `CLAUDE.md`.

---

## What this skill does NOT do

- It does not write prose. It writes stubs.
- It does not invent citations. The `.bib` is empty.
- It does not run `biber` or push to GitHub. Those are user actions.
- It does not migrate existing decks or Substack posts into the book — those are pointer-only references.

---

## Related skills

- `/newproject` — same idea, but for an empirical research project (data, code, output).
- `/bibcheck` — run on the book's `.bib` once you have entries.
- `/referee2` — run on a draft chapter once it exists.
- `/blindspot` — run on every figure or table the book introduces.
