> کارت‌ها و مسیرها: [راهنمای مشارکت گرافیست و توسعه‌دهنده](cards/README.md)، [شواهد بازی‌های ایندی و فروم‌ها](cards/evidence.json) و [قرارداد پیشنهادی متن](cards/copy-contract.json). بازبینی متن و برجستگی مأموریت بندر هنوز باز است.

# design/ — art sources and approved mockups (not shipped to the site)

## nanobanana/ — Gemini (Nano Banana Pro) source sheets
- `sheet1.jpg` carpentry props (approved style: dark wood, flat side view). `sheet2.jpg` construction (partly 3D — prefer `sheet_fix.jpg` for cart, ramps, logs, A-frame, barrel, wheelbarrow, wedge-fulcrum). `sheet3.jpg` factory (partly 3D — prefer `sheet3_fix.jpg`: meshing gears, switches, conveyor, workbench, podium). `badges_color.png` = map badges (already cut into `src/simple-machines/img/badge*.webp`).
- `boxes.json` = bounding box of every object per sheet; `idx_*.png` show the index numbers on each sheet.
  - sheet1: 0/1/7 crates, 2/3/10 spring scales, 4/5/6/8/9 weights, 11+14+15 two-pan balance (11 = stand+beam+pointer, 14/15 = pans), 12–18 friction strips, 19 cart, 20 sawhorse, 21 saw, 22 sled, 26 hammer.
  - sheet_fix: 0/2/6/7 logs, 1 cart, 3/4/5 ramps, 8 A-frame, 9 barrel, 10 wheelbarrow, 11 wedge fulcrum.
  - sheet2: 0 long plank, 3/4/9 rocks, 19/21 pulleys, 22/24/25 rope, 26 hook, 29 container.
  - sheet3_fix: 0 gears, 1 switch on, 2 conveyor, 3 switch off, 4 workbench, 5 podium.
- `harm.py`: `cut(sheet, idxs, holes=True)` removes the white background (flood fill from the border; `holes=False` + largest component for light objects such as the stone) and `gentle(c, alpha, land_rgb)` harmonises an object with the game: unify dark outlines to warm ink `#3B2417`, grade 7% toward the land colour. This "gentle" harmonisation was chosen on purpose — the detailed Nano-Banana objects must sit calmly in a minimal game (strong quantisation looked blotchy and was rejected).
- `recolor.py`: LAB-mask recolour (used to prove shirt recolouring).
- `chosen-style-D.png`: the character style the teacher chose (clean cartoon, thin warm-brown outline).

## mockups/ — approved screen mockups (Python + Playwright → PNG)
- `lever3.py` → physically correct lever scene (stone on the ground with the plank tip under it; after pressing, the stone rests on the short end; pivot dot exactly on the wedge apex; arms measured from the fulcrum, drawn on the floor).
- `bal2.py` → two-pan balance built from sheet1 parts: beam+needle rotate about the pivot, pans hang vertically from rings on the hooks, chains end on eyelets on the pan rims, static light scale with a green zero mark, dark needle (value contrast), base blotch removed.
- `steps_v2.py`, `bsteps_v2.py` → the latest approved page layout (`ui_steps_v2.png`, `ui_balance_v2.png`, header detail `hdr_num.png`): white header buttons without outline, «نقشه» pill, stop-number chip, fixed text panel, one primary button that appears only after success, direct manipulation hints (dashed box + arrows around the fulcrum, dashed pink ring where to press).
- Paths inside these scripts point to the old scratchpad (`.../scratchpad/gem/...`); change them to `design/nanobanana/` before running. Fonts come from `assets/fonts`.

## reports/
- `science_audit_2026-09-30.md`: the scientific/Persian audit of all game texts (already applied in stage 1).

## Runtime balance layers (2026-10-01)
`tools/build_balance_art.py` exports the approved bal2 masks/recolouring from sheet1 to embedded `src/simple-machines/balance_art.js`. Re-run with Pillow, NumPy, OpenCV, SciPy and scikit-learn available; the game build only needs Python and the checked-in generated asset. The live model supplies rotation, equal arms, vertical chains/pans and the readable zero gauge.

## Runtime lever layers (2026-10-01)
`tools/build_lever_art.py` exports the existing lever3 plank/stone/wedge through `harm.py` into embedded `src/simple-machines/lever_art.js`. The wedge stores its alpha-mask apex so the rigid plank pivots on the visible contact point. Stone grounding, motion and contact-point traces are supplied by `makeLift`; no network asset is needed by the game. Use the same Python image dependencies as the balance exporter.
