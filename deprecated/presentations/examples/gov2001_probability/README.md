# Example: Gov 2001 Probability Foundations

> A lecture deck from Harvard's Gov 2001 (Quantitative Research Methodology), demonstrating the rhetoric of decks principles in practice.

---

## What This Is

This is a real lecture deck on probability foundations, created using Claude Code with the deck generation prompt. It demonstrates:

- **Custom Beamer theme** (defined inline, no separate .sty file)
- **One idea per slide**
- **Titles as assertions** (where applicable for teaching)
- **Visual hierarchy** through color, spacing, and typography
- **MB/MC equivalence** — smooth cognitive load throughout

---

## The Theme

The theme is embedded in the preamble (lines 1-132 of the .tex file). Key design choices:

### Typography
```latex
\usepackage{libertine}           % Main text: Linux Libertine
\usepackage[libertine]{newtxmath} % Math: matching style
\usepackage{inconsolata}         % Monospace
```

### Color Palette
```latex
\definecolor{harvardcrimson}{HTML}{A51C30}  % Used sparingly
\definecolor{slate}{HTML}{4A5568}           % Primary text
\definecolor{charcoal}{HTML}{2D3748}        % Headings
\definecolor{forest}{HTML}{276749}          % Accent (key terms)
\definecolor{ocean}{HTML}{2B6CB0}           % Links
\definecolor{warmgray}{HTML}{718096}        % De-emphasized
```

### Design Philosophy
- **Crimson sparingly** — Harvard identity without overwhelming
- **Forest for emphasis** — theorems, key terms, structure
- **Warmgray for de-emphasis** — footnotes, subtitles, context
- **White background** — clean, professional, readable

---

## Rhetoric Principles Applied

### Opening (Slide 2)
```latex
\frametitle{Why Start Here?}
```
Establishes stakes immediately. Not "Agenda" or "Overview" — why should students care?

### Section Breaks
Large, centered section titles with de-emphasized subtitles. Gives the audience a breath between dense material.

### Custom Commands for Hierarchy
```latex
\newcommand{\highlight}[1]{\textcolor{forest}{\bfseries #1}}
\newcommand{\deemph}[1]{\textcolor{warmgray}{#1}}
\newcommand{\red}[1]{\textcolor{harvardcrimson}{#1}}
```
Consistent visual language: green = important, gray = context, red = alert.

---

## Files

| File | Description |
|------|-------------|
| `01b_probability.tex` | Full source with inline theme |
| `01b_probability.pdf` | Compiled output |

---

## To Use This Theme

Copy lines 1-132 from the .tex file into your own deck's preamble. Customize:
- Colors (if not Harvard)
- Course name in footline
- Author/institution

Or extract into a separate `.sty` file for reuse across multiple decks.

---

## Context

This deck was generated using the prompt from `../deck_generation_prompt.md` with the following customization:

```
...professional for a PhD-level course on quantitative methods.
The students are first-year PhD students in Government,
strong in theory but varying exposure to mathematical statistics.
Emphasize intuition alongside formal definitions.
```

The iterative workflow caught:
- Two overfull hbox warnings (fixed by adjusting equation spacing)
- One Tikz label misalignment (coordinate check revealed off-by-0.2cm error)
- Three slides that were too dense (redistributed content)
