# Beautiful Deck Style Preferences

These are user-specific stylistic defaults, not rhetorical rules. Rhetorical choices still come from `rhetoric_of_decks.md`, audience, and content. Apply these preferences unless they conflict with the deck's audience-specific design or the user explicitly asks for a different style.

## Principle: Form From Function

Prefer visual elements that do a job. Decoration is welcome only when it also improves orientation, hierarchy, pacing, or comprehension.

## Progress Rule Under Frame Titles

Every content slide should have a thin horizontal separator between the assertion title and the slide body. Make it functional by turning it into a quiet progress indicator:

- Draw a low-opacity baseline across the full usable slide width.
- Overlay the same line at full opacity from left to right according to deck progress.
- At the start of the deck, only the low-opacity baseline is visible.
- At slide `NN/2`, roughly the left half is fully opaque.
- Near the end, almost the full line is fully opaque.
- Inherit color from the deck's core accent or frame-title color.
- Keep the treatment subtle; it should orient the speaker and audience without competing with content.

For Beamer, implement this in the frame-title template or a shared slide-header macro so it is automatic and consistent. Prefer a computed width such as `\insertframenumber/\inserttotalframenumber * \paperwidth` over manually edited per-slide values.
