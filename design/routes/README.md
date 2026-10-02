# Route asset audit and design candidates

This directory stores design candidates for later route work. Nothing here is approved or wired into the game. `assets.json` records paths, purpose, availability and known provenance; paths are relative to that file.

## Available material

The existing game has one 12-stop map with three land sections. The three active grade tracks (`a`, `b`, `c`) select different missions on that shared map; they are not independent environment routes. `src/simple-machines/journey.js` supplies the land colors, procedural SVG map path, labels, stars and markers. These are code, not standalone exported map assets.

The 12 color stop badges and their 12 locked variants already exist under `src/simple-machines/img/`. `design/README.md` identifies `design/nanobanana/badges_color.png` as their source. Reuse these files by reference; do not recut or duplicate them solely for this audit. The source carpentry, construction and factory sheets and `boxes.json` also exist. They provide illustration parts, not ready-made route backgrounds.

The existing source documentation attributes the art sheets to Gemini (Nano Banana Pro). It does not establish a formal third-party license. This manifest reports that limited provenance without inventing a license or ownership assurance.

## New candidates

| File | Intended role |
| --- | --- |
| `icons/workshop.svg` | Workshop map identity |
| `icons/factory.svg` | Factory map identity |
| `icons/fishing-dock.svg` | Fishing dock map identity |
| `icons/pirate-dock.svg` | Pirate dock map identity |
| `icons/difficulty-marker.svg` | Separate three-step difficulty motif |

The five SVGs are original code-native geometry with transparent backgrounds, a 64 × 64 viewBox, warm-brown `#3B2417` outlines, rounded joints and accessible titles. They do not incorporate Nintendo artwork or other extracted third-party art. They are environment/navigation illustrations, not scientific diagrams, apparatus, or new physics models. The difficulty symbol has no assigned level or route mapping; use a visible text label if it is later adopted. When a redundant visible label is present, implementation should treat the icon as decorative instead of announcing it twice.

## Remaining gaps

At least three independent routes need content identities and route definitions before artwork can be placed. These candidates cover small map identities only. Route-specific scenery/backgrounds, route-selector layout, selected/locked states, mobile placement, difficulty wording/mapping and final visual approval remain open. No speculative physics assets were added.

Keep future entries keyed by stable asset IDs and referenced paths in `assets.json`. Keep route identities separate from difficulty and stop badges so additional routes do not require another badge family or imply that an environment defines scientific difficulty. This is a design convention, not a runtime schema change.

## Visual review

`icons-contact-sheet.png` shows each candidate at 64 px and 32 px on a pale background for legibility review. The SVGs retain transparency. Review confirmed distinct silhouettes, readable small-scale shapes and unclipped geometry; integration and contrast against final route backgrounds remain pending.
