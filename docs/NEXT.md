# Next work — stage 2 of version 2 (written 2026-09-30)

Read `CLAUDE.md`, `docs/HANDOFF.md` (section "Version 2, stage 1") and `design/README.md` first.
The teacher checks the live site herself; talk to her in plain Persian. Mockups before code when she asks for mockups.

## RESUME HERE (teacher decisions 2026-09-30 20:20)
- **Teacher 23:07: ignore her 12-session lesson plan for now — design the game first; the lesson plan will be adjusted to the game later.** So stops/challenges may move freely (still: keep saved progress safe — migrate or bump the progress-code version when mission counts change).
- **Do NOT work on grade 7–9 content (B.4) for now.** First make the current version stable and complete; level d later.
- **The teacher tests the live site while we work — it must never break.** Only publish + push after the full test set in D passes. Work one station at a time; each finished station = one tested commit + push, so the site is always a working version.
- **Teacher 22:26: run the slow tests (t2 all, jt, t5, ov all) only once at the end, not after each station.** Commit+push src changes as you go (live site changes only when publish_game.py runs), so work is resumable.
- **Sessions may hit their limit.** After every step, update the checklist below and push the notes, so a new session can continue from here without the chat.
- Open questions to the teacher (not answered yet): start with scale+lever (approved mockups)? mockups first for other stations? one register (spoken/written) for buttons? Ask again briefly if still unanswered.

- 2026-09-30 20:30 fixed: scale «mystery» (levels 2+) «بررسی» is now a free try (`A.trial`), with guidance by state (no weights / not balanced / balanced but wrong sum). Tested in `failtry.py`.
- Asked the teacher: in levels 2+ (numbers shown) should ramp «fit», pulley/wheel/wedge «choose» also be free tries? Today they keep «یک فرصت دیگر داری».

- **2026-09-30 21:39 teacher approved (for ALL similar places):** no «امتحان کن / برداشتن پایه‌ها» button where the result can be shown live. Scale: no supports; beam tilts live as weights are dropped; balanced = done. The separate «جرم نامعلوم» (scale mystery) becomes «balance + then ask the mass» (same challenge type/count, progress safe). Then the same idea station by station (lever balance supports, lever lab, force tug «برو!», ramp «بکش!», …) — a real calculation/prediction question keeps its «بررسی».
- Live-work checklist: [x] scale balance/fewest/mystery live (published 2026-09-30; mystery hides right-pan total until the mass is answered)  [~] lever balance live + lever lab + scale lab (code done, NOT yet published — run full tests at the end, then publish)  [x] lever published. [~] physical tries free at ALL levels (ramp, pulley, wheel, wedge, lever lift, force tug) + «هر چند بار خواستی امتحان کن» in prompts — code done 22:40, full test run + publish pending. Rule: state results (scale, seesaw) = live; action results (pull, crank, push, tug) = keep the action, failed try free; calculation/prediction questions keep two chances.

### Teacher review 2026-09-30 22:34 — do these INSIDE stage 2, station by station (content + graphics of a station together, so each station is touched once)
1. **Order easy → hard.** Inside every level: recognise → compare/predict → do by hand → calculate; and across levels. Reordering challenges *inside* a level's `gen()` is safe for progress (stars are stored per level, missions reference levels). Check every station, every track (a–d) and the quiz order.
2. **Definitions just in time.** A term (اصطکاک، نیروی خالص، جرم، وزن، تکیه‌گاه، بازوی محرک…) must be introduced (short card or one line) right before the first challenge that needs it — not only in the word cards at the stop start, and never after it is used. Audit per stop and per track.
3. **Friction.** (a) The friction force of each surface is not visible — in a question like «با ۲۰ نیوتن روی کدام سطح تکان نمی‌خورد؟» levels b+ must show friction values (a label per strip), level a must show clearly different arrow sizes + a kid hint. (b) Friction challenges (`fric`) are mixed into the force station levels together with tug-of-war (`predict/balance/net`) and repeat across levels. Separate them: force = pull/push, net force, tug; friction (stop 4) = surfaces and friction size; remove repeats, add new friction tasks (e.g. change the surface so the box moves / stops). Keep level count; keep mission→level indices or migrate.
4. **Wording.** «دو جسم به هم دست بزنند» → «یکدیگر را لمس کنند» (quiz `f-c2`). Do a full pass for similar spoken/inexact words in written texts (together with item C «register»).
5. **«روی ماه / روی زمین» tag** (`placeTag` in st_scale.js) looks bad — replace with a proper sign graphic in the art style; same pass for similar plain boxes: moon astronaut figure, «تراز» gauge box of the seesaw, empty white tray panel when all pieces are used.
6. **Variety + teaching rhythm (teacher 22:38).** Research report with ~30 new challenges by station and difficulty: Claude Doc https://claude.ai/code/artifact/52d248c0-58af-498b-8d98-47344755f155 (priority: force+friction, lever roles on real tools, "which machine for this job"). More kinds of challenges; every 1–3 challenges must teach one idea (learn → try → apply, ending with a one-line takeaway).
7. **Difficulty tags آسان / سخت / خیلی سخت / هیولا — APPROVED by the teacher 22:39 (my proposal):** tag every challenge; main path (what the class does) = آسان→سخت for everyone at grade level; «خیلی سخت» and «هیولا» = optional challenges at each stop the child chooses (special badge, visible on teacher page; progress-code version bump). A child who is stuck gets more hints, not an easier path.
- Note: a screenshot still showed «برداشتن پایه‌ها» on the seesaw = old cached version; the live seesaw was published 22:15.

   - **Teacher 22:59:** optional «خیلی سخت/هیولا» must NEVER block the path — the child chooses to enter or skip; nothing is locked behind them. Main-path free-try challenges must not stall either: after 3 failed tries offer «راهنمایی بیشتر» and then «نشانم بده» (solution shown, 1 point).
   - **Everyday-object challenges (scissors, tweezers, doorknob, screwdriver, flagpole, bicycle, …) → VERSION 3**, because they need assets in our style. Exception: ones we already have assets for (wheelbarrow sheet_fix #10, saw/hammer sheet1 #21/#26, barrel sheet_fix #9, pulleys sheet2) may go into stage 2.
8. **After the background run: rebuild (reset feature added 23:05 in journey.js), run `resetchk.py` + `jt.py 0 3` + `failtry.py`, then publish.** Full test run started 22:50 on commit after «untouched stepper» (results in /tmp/claude-0/fin/*.log if same session; otherwise rerun D + `leakchk.py a|b|c`), then publish.** Teacher 22:39: test all other stations for the same kinds of problems.** Done/doing: untouched stepper «بررسی» no longer costs a chance (core.js `btn`); leak check (answer visible on screen before answering) `tests/leakchk.py`.

9. **Split land «کارگاه ساختمانی و بندر» into two (teacher 23:03, proposal: stops 5–8 کارگاه ساختمانی = lever 1, lever 2, ramp, wedge/screw; stops 9–10 بندر = wheel & axle (winch), pulley (crane)) — waiting for her OK on the split point.** Presentation only (no saved data depends on lands): `LANDS` + `landOf` in journey.js, `mlayout()` banner gap before stop 9, a 4th palette `body[data-land="3"]` in style.css, map banner, land badge art. Port assets already in design/nanobanana: sheet2 #29 container, #19/#21 pulleys, #22/#24/#25 rope, #26 hook. Do it together with the map/graphics work in stage 2.

10. **Where do the moon and water challenges go (teacher 23:05)?** Proposal sent, waiting: moon stays in «جرم و وزن / نیروسنج» (stops 2–3, it is the key evidence mass ≠ weight) but its scene gets a proper «trip to the moon» look; water: one simple challenge stays at stop 3 (feels lighter in water), the rest (why, buoyancy numbers, floating/sinking) moves to the new «بندر» land as optional خیلی سخت/هیولا challenges — mission count unchanged, progress safe. Lesson plan no longer a constraint (23:07) → go with the proposal.

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
