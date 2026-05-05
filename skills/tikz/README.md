# `/tikz` — Quick visual-collision check

> A narrow check for the visual errors that compile cleanly. Three checks, one pass, exits.

`/tikz` catches the class of figure error that produces no warning, no compile error, and no exit code — only a wrong-looking figure that the producing agent cannot see. Labels sitting on curved arrows. Text touching node boundaries. Y-axis titles clipped by the figure margin. `pdflatex` does not warn about any of these. `ggsave` does not refuse to write them. The agent that produced them does not know they are wrong.

This skill replaced an earlier six-pass version that re-audited the entire file after every fix. That version timed out on real decks because the work was quadratic in the number of figures. This version does **three checks, one pass, exits**.

## What it does

Three checks, applied to either TikZ source or rendered figure:

1. **Bezier curve label collisions.** A label inside the arc of a curved arrow. Math mode computes `(chord_length / 2) × tan(bend_angle / 2)` and adds a 0.5cm safety margin; visual mode reads the rendered image and looks.
2. **Label-to-object whitespace.** A label that touches or overlaps a node, axis, marker, bar, or other plot element. 0.4cm minimum clearance.
3. **Edge clipping.** A label running off the figure edge or sitting too close to the boundary. 0.5cm minimum clearance.

That's it. No cross-slide consistency. No autosized-node detection. No scale-factor compensation. If you want those, the previous behavior is in git history.

## Two modes

| Input file | Mode | How it works |
|---|---|---|
| `.tex` | **Math mode** | Greps the source for `bend`, `\node`, `\draw`. Computes coordinates and gaps. Reports collisions with proposed fixes. |
| `.png`, `.jpg`, `.jpeg` | **Visual mode** | Reads the image. Inspects the rendered figure directly using Claude's multimodal vision. |
| `.pdf` (single-figure) | **Visual mode** | Same. |
| `.pdf` (multi-page deck) | **Refused** | Out of scope. Point `/tikz` at the source `.tex` instead. |

Honest limitation on visual mode: large overlaps and edge clipping are caught reliably; subtle whitespace violations under a few pixels may be missed. For high-stakes figures, run `/tikz` on both the source code and the rendered output.

## Why narrow

The whole point is the class of error that compile-clean processes cannot detect. The agent runs `pdflatex`, sees zero errors, declares done — and the figure has a label sitting on a curve. Three checks, focused on those three errors, finishing in a few minutes per figure. That is the entire value proposition. Anything broader, and the skill spends its runtime on diagnostics that don't catch this specific failure.

## Usage

```
/tikz path/to/deck.tex
/tikz figures/regression_plot.png
/tikz figures/standalone_diagram.pdf
```

If you invoke without a file, the skill asks. It does not guess.

## Output

```
[file] — quick check complete

Bezier collisions:    N
Whitespace collisions: M
Edge clipping:        K

Findings:
  - <location>: <description>. Fix: <proposed change>.
  - ...
```

Then it stops. The user reviews and edits. If they want a deeper look at one element, they invoke `/tikz` again on that scope.

## What this skill does NOT do

- It does not iterate. One pass, one report, exit.
- It does not re-audit the whole file after a fix. That's the quadratic blowup that killed the previous version.
- It does not run `pdflatex` in a loop.
- It does not eyeball multi-page PDFs.
- It does not perform cross-slide consistency, autosized-node detection, or the four other passes the previous version did.

## Typical fixes by toolchain

**ggplot2 (R)**: move legend with `theme(legend.position=...)`; crowded labels with `ggrepel::geom_text_repel()`; clipping with `theme(plot.margin = margin(t,r,b,l))`.

**matplotlib (Python)**: `plt.tight_layout()` for auto-padding; save with `bbox_inches='tight'`; legend outside plot with `bbox_to_anchor`.

**TikZ (LaTeX)**: declare canvas with `\useasboundingbox`; control label placement with `node[anchor=...]`; place curve labels as standalone `\node at (midpoint)` outside the arc, not as inline edge labels.
