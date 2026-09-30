# Next work — stage 2 of version 2 (written 2026-09-30)

Read `CLAUDE.md`, `docs/HANDOFF.md` (section "Version 2, stage 1") and `design/README.md` first.
The teacher checks the live site herself; talk to her in plain Persian. Mockups before code when she asks for mockups.

## RESUME HERE (teacher decisions 2026-09-30 20:20)
- **Do NOT work on grade 7–9 content (B.4) for now.** First make the current version stable and complete; level d later.
- **The teacher tests the live site while we work — it must never break.** Only publish + push after the full test set in D passes. Work one station at a time; each finished station = one tested commit + push, so the site is always a working version.
- **Sessions may hit their limit.** After every step, update the checklist below and push the notes, so a new session can continue from here without the chat.
- Open questions to the teacher (not answered yet): start with scale+lever (approved mockups)? mockups first for other stations? one register (spoken/written) for buttons? Ask again briefly if still unanswered.

- 2026-09-30 20:30 fixed: scale «mystery» (levels 2+) «بررسی» is now a free try (`A.trial`), with guidance by state (no weights / not balanced / balanced but wrong sum). Tested in `failtry.py`.
- Asked the teacher: in levels 2+ (numbers shown) should ramp «fit», pulley/wheel/wedge «choose» also be free tries? Today they keep «یک فرصت دیگر داری».

### Stage-2 checklist (tick as you go)
- [ ] scale: Nano-Banana balance (`design/mockups/bal2.py`) + drag weights to pan
- [ ] lever: `lever3.py` scene + drag the fulcrum (no slider)
- [ ] ramp  - [ ] pulley  - [ ] wheel  - [ ] wedge/screw  - [ ] force  - [ ] sort
- [ ] full land palettes in scenes (B.3)
- [ ] section C small items

## A. Must fix first — DONE (2026-09-30)
1. Level 1 free experiments: ramp «بکش!», pulley/wheel «choose», wedge/screw now use `A.trial` when `KID()` (failed try = guidance + reset, costs nothing; success on try 1–3 → 2 points, later → 1). Kid prompts say «هر چند بار خواستی امتحان کن». Levels b/c/d unchanged. Test: `tests/failtry.py`.
2. Map «تو اینجایی»: `hereSpot()` in journey.js picks the nearest free spot (inside the map; clear of stops, names, numbers, stars, side-quest diamonds, quiz pills, land titles). Test: `tests/mapchk.py <grade>` (all 12 stops at 390 and 1280 px; prints nothing when fine; screenshots `shots/map_*`).

## B. Stage 2 (agreed plan)
1. Replace the procedural scene drawings with Nano-Banana objects, station by station, starting with scale (`design/mockups/bal2.py`) and lever (`lever3.py`). Keep test hooks (`window.__T`, ids `#sc #cl #fb #nv #dots`) and keep `t2.py` solvable; `ov.py` must print nothing.
2. Direct manipulation: drag the fulcrum itself (no slider), drag weights to the pan; no «امتحان کن/بررسی کن» where the result can be shown live.
3. Land-palette scenes: move from the light tints used in stage 1 to the full land palettes of the mockups once objects are the new light/dark-contrast assets.
4. Level 4 (grades 7–9) specific content: torque (گشتاور), efficiency (بازده), gears (چرخ‌دنده; asset in `sheet3_fix` #0). Today level d = level c missions with formulas on. Changing mission counts per stop changes the progress code — keep ≤3 missions per stop or bump the code version.

## C. Smaller items from the independent review (not yet done)
- Quiz/UI register: «وقتِ آزمونه!»/«بزن بریم!» are spoken style, other buttons written; ezafe mark only in «چالشِ بعد/سؤالِ بعد/سطحِ بالاتر» — choose one style (ask the teacher; she herself wrote «وقت آزمونه»).
- Dashed map path runs through some stop labels (e.g. «جرم و وزن»).
- Home tasks (`HOME`) are the same for all grades; consider level-specific wording.
- Level-d backpack notebook is very long; group cards by stop or make them collapsible.
- Skin tone is not recolourable (only shirt colour); the 8 characters cover different skin tones. If the teacher wants skin choice, generate skin variants in Gemini (automatic recolour of skin failed earlier).
- Map on desktop is a narrow centred column (fine, but could be wider).

## D. Tests to run after changes
`python3 src/simple-machines/build.py`, then in `src/simple-machines/tests/`: `t2.py all all a|b|c|d` (parallel per station), `t5.py a|b|c|d`, `ov.py <track> <stations>` (must print nothing), `jt.py <grade 0..7> 12` (plays the whole journey incl. quizzes and level-up), `failtry.py` (level-1 free tries), `mapchk.py <grade>` (map marker), `shot1.py <station> <level> <track> [w h]` for quick screenshots. Then `python3 tools/publish_game.py simple-machines physics/simple-machines "کارگاه ماشین‌های ساده"`, commit, push.
