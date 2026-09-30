# Next work — stage 2 of version 2 (written 2026-09-30)

Read `CLAUDE.md`, `docs/HANDOFF.md` (section "Version 2, stage 1") and `design/README.md` first.
The teacher checks the live site herself; talk to her in plain Persian. Mockups before code when she asks for mockups.

## A. Must fix first (reported by the teacher)
1. **Level 1 (grades 2–3) trial-and-error stations still cost a chance on a failed try.** Level 1 shows no numbers, so in ramp («بکش!»), pulley, wheel-and-axle and wedge/screw the child can only find the answer by trying. Apply the same rule already used in scale «balance/fewest» and lever «balance»: use `A.trial(ok, msgs)` (app.js `board()`) instead of `A.judge` for the physical try when `KID()`. A failed try shows guidance, resets the scene, costs nothing; success gives 2 points within 3 tries, else 1. Places: `st_ramp.js` (fit/pull, ~line 72–74), `st_pulley.js` (`onBlocked` in choose/lift, ~75–76), `st_wheel.js` (`onBlocked`, ~63–64), `st_wedge.js` (`onBlocked`, ~77–78). Also make the kid prompts say «هر چند بار خواستی امتحان کن». Keep levels b/c/d as they are (numbers are given there, so a wrong try is a real mistake). Run `t2.py all all a` afterwards and test one failed try by hand.
2. **Map: the player's avatar and «تو اینجایی» go off the right edge** when the current stop is on the right side of the path (`jmap()` in journey.js: `tx=q.x>200?q.x+74:q.x-74` — place it toward the centre instead, e.g. `q.x>200?q.x-80:q.x+80`, and keep the label clear of the stop name and the side-quest diamond). Check every stop 1–12 at 390 px and 1280 px.

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
`python3 src/simple-machines/build.py`, then in `src/simple-machines/tests/`: `t2.py all all a|b|c|d` (parallel per station), `t5.py a|b|c|d`, `ov.py <track> <stations>` (must print nothing), `jt.py <grade 0..7> 12` (plays the whole journey incl. quizzes and level-up), `shot1.py <station> <level> <track> [w h]` for quick screenshots. Then `python3 tools/publish_game.py simple-machines physics/simple-machines "کارگاه ماشین‌های ساده"`, commit, push.
