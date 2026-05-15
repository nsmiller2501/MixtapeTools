# TikZ Collision Audit (`/tikz`)

`/tikz` is a repair skill for residual visual collisions in TikZ figures. It catches problems LaTeX will happily compile: labels sitting on arrows, text touching box edges, curves crossing labels, arrows pointing ambiguously, or repeated diagrams drifting across slides.

The executable protocol lives in [`SKILL.md`](SKILL.md). The mathematical rule book shared with `/beautiful_deck` lives in [`tikz_rules.md`](tikz_rules.md).

## When To Use It

Use `/tikz` after editing a `.tex` file with TikZ diagrams, before shipping a deck, or when a diagram compiles but still looks visually wrong. It is also the downstream cleanup pass after `/beautiful_deck`.

This is not the primary defense against bad diagram generation. `/beautiful_deck` should write safe TikZ from the start using explicit node dimensions, coordinate maps, directional edge labels, and no `scale` on complex diagrams. `/tikz` then audits what remains.

## What It Does

- Finds every `tikzpicture` in the target `.tex` file.
- Reads the shared rule book before auditing.
- Runs ordered geometry checks for cross-slide consistency, Bezier curve clearance, edge-label gaps, directional label keywords, boundary clearance, margins, and debug bounding boxes.
- Applies focused source edits to fix collisions.
- Recompiles and re-audits until the file clears the visual checks and LaTeX warnings.

## Files In This Skill

- [`SKILL.md`](SKILL.md) — the operational checklist Claude or Codex follows.
- [`tikz_rules.md`](tikz_rules.md) — formulas, clearance rules, and worked examples used by both `/tikz` and `/beautiful_deck`.

## Related Skills

- `/beautiful_deck` — writes prevention-oriented TikZ and invokes `/tikz` as a residual audit.
- `/referee2` deck mode — uses the same visual-quality rules when auditing presentations.

This README is only the human overview. If behavior changes, update `SKILL.md` and `tikz_rules.md` first, then keep this summary in sync.

---

*This skill originated in [Scott Cunningham](https://github.com/scunning1975/MixtapeTools)'s MixtapeTools repository.*
