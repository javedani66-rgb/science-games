# Next work — stage 2 of version 2 (written 2026-09-30)

Read `CLAUDE.md`, `docs/HANDOFF.md` (section "Version 2, stage 1") and `design/README.md` first.
The teacher checks the live site herself; talk to her in plain Persian. Mockups before code when she asks for mockups.

## NOW (2026-10-01 morning session) — step 1 of ORDER OF WORK
- [x] friction arrows: one scale (push = friction when static) — commit bf363ba, not yet published.
- [x] step 1a: every level gets a stable `id`; stars stored by id (`S.ls["<track>:<id>"]`), STOPS missions = level ids; old `S.prog[..].lv` migrated on load (test seeds too).
- [x] step 1b (infra only): challenge catalogue `CH` (id, st, diff 0..3 = آسان/سخت/خیلی سخت/هیولا, teach, terms, mk(r)); a level may list `ch:[ids]` instead of `gen`; best points per challenge in `S.cb`. Stations move to CH one by one in steps 2–4.
- [x] step 1c: progress code v3 (31 letters: + 2 bits/stop for optional doors, 2-bit version); v1/v2 still read.
- [x] step 1d: stop order 7 = wedge/screw, 8 = ramp (STOPS, HOME, LEARN, WORDS, QTERMS, stop icons, badges 7↔8; saved home/side/words + v1/v2 codes swapped). Lands 3+3 = presentation, left for the graphics pass.
- [ ] verify: tests/savechk.py (new, prints nothing when fine) + jt.py; then full suite.
- [~] step 2 (force/friction split) code done 08:30: new station `fric` (st_fric.js: makeSlide one-lane scene, surface picker, goals move/stop/flag, «کمترین هل» with stepper; friction meter on every surface: squares for level 1, «اصطکاک تا X نیوتن» for 2+); force station = tug only (lab, levels, endless); stop 1 = force (a: a1,a2 · b: 1,2 · c: 2,3), stop 4 = fric (a: a1,a2 · b: 1,2 · c: 2,3); fric levels use the CH catalogue (defCh in st_fric.js). Hint ladder in A.trial: 2nd fail adds `more`, 3rd fail shows «نشانم بده» (1 point). t2.py has a fric solver; t5 includes fric.
- [x] scale weight arrows: one shared scale for both pans (heavier pan's arrow was clipped by the floor and drawn SHORTER — teacher screenshot 08:02). Source only; rebuild after background tests end.
- [ ] **Teacher 08:02 (angry, rightly): «کدام کفه پایین می‌رود؟» (`heavier`) asks a blind guess from looks, while the game teaches "don't trust looks" (cotton vs iron same mass) and costs points.** Proposed (waiting for OK): predict (free, no points) → child puts both objects on the pans, live tilt → scored question about what was SEEN («کدام جرم بیشتری داشت؟», cotton/iron: «چرا ظاهر گولمان زد؟»). Then audit ALL stations for questions whose answer can't be known from the scene.
- [x] 2026-10-01 ~09:00 audit fixes (docs/AUDIT_2026-10-01.md): POE helper `poe()` in app.js (scale heavier/moon/moonbal, lever predict level 1 + lever.1, first friction item, kid spring-scale `hang`); rules in every calc prompt; ramp builds before comparing; examples in QDEF for quiz items; praise okSay/okDo; spring wording «کش می‌آید»; new kid mission scale.a5 «فنرِ نیروسنج» → stop 2 kid = a1,a2,a3, stop 3 kid = a5,a4; side quests open only after the stop's missions.
- [ ] **NEXT SESSION STARTS HERE (teacher moved to a new chat 08:22):** the full suite was started in the old session (19 jobs passed, rest unknown — background jobs die with the old session). So: (1) add the «اول آزمایشگاه» offer: the first time a child opens mission 1 of a stop, a small sheet offers «آزمایش آزاد» or «شروع مأموریت» (never blocks; remember per stop, e.g. `p.lab[i]`; PhET recommends ~5 min open exploration first — teacher approved 08:19); (2) build once, run the FULL suite in the background (t2 all stations incl. fric × a b c d, t5, ov, jt 0/2/3/6 ×12, failtry, savechk, resetchk, mapchk, leakchk) — note jt/mapchk/resetchk may need small updates for the side-quest lock and the new kid missions at stops 1–3; (3) publish + push only if all pass; (4) tell the teacher in Persian; then continue stage 2 (scale rebuild, then lever …).
- Teacher 08:19: two missions at stop 1 for level 1 is OK (matches Legends of Learning 15–30 min sessions). Talk to her in Persian only.
- Teacher 2026-10-01 07:51: run EVERYTHING that can run in the background in the background (even a 2-min ov.py), never wait in the chat.

## RESUME HERE (teacher decisions 2026-09-30 20:20)
- **Teacher 23:16 decided:** (a) lands split **3 + 3**: کارگاه ساختمانی = stops 5 lever 1, 6 lever 2, 7 wedge/screw; بندر = 8 ramp (loading ships), 9 wheel & axle, 10 pulley — i.e. swap the ramp and wedge/screw stops (lesson plan is no constraint). (b) **Register (APPROVED 23:19; lines in `voice.js`, guide `docs/voice.md`; wired: ok/okTries/okLate/retry/wrong/quiz — still to wire: stopDone, hard, welcome, back):** written for questions, instructions, explanations, definitions, feedback about the science and ALL buttons («شروع آزمون», «چالش بعد» without ezafe mark); spoken allowed only in the character's own voice — short fixed praise/encouragement lines and celebratory titles in its speech bubble (e.g. «وقتِ آزمونه!», «آفرین، دمت گرم!»). Never mix registers inside one sentence or one element. (c) **Sound ON by default**, speaker button in every header.
- **Teacher 23:07: ignore her 12-session lesson plan for now — design the game first; the lesson plan will be adjusted to the game later.** So stops/challenges may move freely. **Teacher 23:10: all current players are her own test profiles — wiping progress is OK.** Still: old saved data/codes must not crash the game (bump the code version, reset unreadable data cleanly).
- Proposal 23:10: the «نیروسنج» stop stays early (it is the tool for measuring force/weight used everywhere after it); only the water challenges move to «بندر», where they use the spring scale again (crane hangs cargo from a spring scale into the sea).
- **Do NOT work on grade 7–9 content (B.4) for now.** First make the current version stable and complete; level d later.
- **The teacher tests the live site while we work — it must never break.** Only publish + push after the full test set in D passes. Work one station at a time; each finished station = one tested commit + push, so the site is always a working version.
- **Teacher 22:26: run the slow tests (t2 all, jt, t5, ov all) only once at the end, not after each station.** Commit+push src changes as you go (live site changes only when publish_game.py runs), so work is resumable.
- **Sessions may hit their limit.** After every step, update the checklist below and push the notes, so a new session can continue from here without the chat.
- Open questions to the teacher (not answered yet): start with scale+lever (approved mockups)? mockups first for other stations? one register (spoken/written) for buttons? Ask again briefly if still unanswered.

- 2026-09-30 20:30 fixed: scale «mystery» (levels 2+) «بررسی» is now a free try (`A.trial`), with guidance by state (no weights / not balanced / balanced but wrong sum). Tested in `failtry.py`.
- Asked the teacher: in levels 2+ (numbers shown) should ramp «fit», pulley/wheel/wedge «choose» also be free tries? Today they keep «یک فرصت دیگر داری».

- **2026-09-30 21:39 teacher approved (for ALL similar places):** no «امتحان کن / برداشتن پایه‌ها» button where the result can be shown live. Scale: no supports; beam tilts live as weights are dropped; balanced = done. The separate «جرم نامعلوم» (scale mystery) becomes «balance + then ask the mass» (same challenge type/count, progress safe). Then the same idea station by station (lever balance supports, lever lab, force tug «برو!», ramp «بکش!», …) — a real calculation/prediction question keeps its «بررسی».
- Live-work checklist: [x] scale balance/fewest/mystery live (published 2026-09-30; mystery hides right-pan total until the mass is answered)  [~] lever balance live + lever lab + scale lab (code done, NOT yet published — run full tests at the end, then publish)  [x] lever published. [~] physical tries free at ALL levels (ramp, pulley, wheel, wedge, lever lift, force tug) + «هر چند بار خواستی امتحان کن» in prompts — code done 22:40, full test run + publish pending. Rule: state results (scale, seesaw) = live; action results (pull, crank, push, tug) = keep the action, failed try free; calculation/prediction questions keep two chances.

## SCIENCE ACCURACY → 10 (teacher 23:26)
- **Real error found:** friction strip — push arrow scale 1.6 px/N, friction 1.9 px/N (st_force.js makeFriction) → when the box does not move, friction (= push) is drawn LONGER than the push. Use one scale for all force arrows in a scene (and cap equally); when static, friction arrow = push arrow exactly.
- One small physics core (per machine: formula + stated assumptions) that every scene and every question reads from; automated physics test: random parameters → scene state/answers equal the formula (ramp F=Wh/L, lever Σm·d, pulley F=W/n & s=n·h, wheel F=W/R, wedge, screw, net force, static vs moving friction, g≈10 / moon 1.6, buoyancy).
- «فرض‌های ما» card per station for grade 4+: friction ignored where it is, ropes/pulleys weightless, g ≈ ۱۰ (really 9.8), ideal machines (no efficiency loss) — so simplifications are stated, not hidden.
- Terminology from the Iranian textbooks (نیروی محرک/مقاوم، بازوی محرک/مقاوم، مزیت مکانیکی، تکیه‌گاه): ask the teacher for the textbook pages/PDF (gama.ir was unreachable from the sandbox) and build a glossary file every text must follow.
- Independent review before each publish: a fresh reviewer agent with the glossary + physics checklist; and the teacher (or a physics colleague) signs off per station.
- Re-check known weak spots: lever mystery at distance 1, scale waterF brick answer = reading, seesaw fixed ±14° tilt (fine, but say "تا جایی که تخته به زمین بخورد").

## ORDER OF WORK (teacher 23:25: content first, graphics second) — follow this
1. Challenge catalogue as data + progress by challenge id + code v3 (enabler; wipe OK).
2. Force and friction split, rebuilt as 3-packs (see, try, apply) easy→hard, just-in-time terms, hint ladder «راهنمایی بیشتر → نشانم بده», misconception challenges from the research doc. Publish.
3. Same for scale, then lever. Publish each.
4. Ramp, wedge/screw, wheel & axle, pulley (in the new 3+3 land order). Publish each.
5. Machine hunt: «which machine for this job?», compound machines; a short mini-test at the start and end of each land (LoL idea); one story mission per station (Tinybop idea); optional خیلی سخت/هیولا doors + badges.
6. Sound + mute (cheap, big gain) — can slot in any time after step 1.
7. THEN graphics pass station by station: Nano-Banana props, full land palettes, 4-land map, moon trip, port, signs.
Target (comparison doc, without Iran criteria): 61 → ~72 (guidance 6→8, order 5→8, sound 1→7, graphics 5→7, variety 7→8, game feel 7→8).

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
8. [x] **Published 2026-10-01 ~03:00 Tehran after the full suite passed** (t2 all 8 stations × 4 levels, failtry, leakchk a/b/c, ov a–d, t5 a–d, jt 0/2/3/6 ×12 stops, mapchk, resetchk). Note: this cloud workspace restarts when the chat is idle and kills background jobs — overnight, run tests in foreground chunks ≤9 min instead.

9. **Split land «کارگاه ساختمانی و بندر» into two (teacher 23:03, proposal: stops 5–8 کارگاه ساختمانی = lever 1, lever 2, ramp, wedge/screw; stops 9–10 بندر = wheel & axle (winch), pulley (crane)) — waiting for her OK on the split point.** Presentation only (no saved data depends on lands): `LANDS` + `landOf` in journey.js, `mlayout()` banner gap before stop 9, a 4th palette `body[data-land="3"]` in style.css, map banner, land badge art. Port assets already in design/nanobanana: sheet2 #29 container, #19/#21 pulleys, #22/#24/#25 rope, #26 hook. Do it together with the map/graphics work in stage 2.

10. **Where do the moon and water challenges go (teacher 23:05)?** Proposal sent, waiting: moon stays in «جرم و وزن / نیروسنج» (stops 2–3, it is the key evidence mass ≠ weight) but its scene gets a proper «trip to the moon» look; water: one simple challenge stays at stop 3 (feels lighter in water), the rest (why, buoyancy numbers, floating/sinking) moves to the new «بندر» land as optional خیلی سخت/هیولا challenges — mission count unchanged, progress safe. Lesson plan no longer a constraint (23:07) → go with the proposal.

11. Comparison with PhET, Tinybop, Edheads, Legends of Learning (Claude Doc https://claude.ai/code/artifact/cfdfe280-36ee-451d-8e8d-0a6b04c2e5da): we lead only thanks to Persian/Iran fit; weakest: sound, graphics, easy→hard order; borrow story missions per station (Tinybop), pre/post mini-test per land (LoL).
11b. **Full audit 23:15** (Claude Doc https://claude.ai/code/artifact/b137e73f-fc9a-4e0f-8b0e-2547607f1895). Priority: (1) publish tonight's work after the full run; (2) refactor challenges into a DATA catalogue (id, station, type, params, difficulty آسان/سخت/خیلی سخت/هیولا, teaches, terms, misconception) + progress keyed by challenge id + progress code v3 (wipe OK); (3) station by station content+graphics; (4) map: 4 lands, water in port, moon trip, optional-challenge doors/badges; (5) **sound + mute button — never ported from the «سفر در کارخانه» prototype (8 Kenney sounds, speaker toggle remembered in localStorage)**; (6) language pass; (7) v3: everyday objects, recorded voice for level-1 texts (speechSynthesis rarely has a Persian voice), grades 7–9. Leak fixes still to do: lever mystery at distance 1 (answer = right torque), scale waterF brick (answer = underwater reading).

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
