# Science games — working guide

Static site on GitHub Pages: https://javedani66-rgb.github.io/science-games/
Owner: a primary-school science teacher in Iran (grades 2–6). All user-facing text is Persian (RTL).
Talk to the teacher in Persian, in plain words; she/he is not a programmer.

**Read `docs/HANDOFF.md` first** — it has the project history, decisions and open items. Then `docs/NEXT.md` (current task list) and `design/README.md` (art sources and approved mockups).

## Layout

```
index.html                     portal (hand-edited; one card per live game + "سرزمینِ علوم بزرگ‌تر می‌شه…" box)
manifest.webmanifest, icons/   PWA install
sw.js                          service worker, network-first + offline cache; V is bumped by the publish tool
assets/fonts/                  Vazirmatn R/B, Lalezar (shared by all games)
physics/simple-machines/       BUILT game (do not edit by hand)
src/simple-machines/           game source → build.py concatenates into one IIFE + inlines fonts
src/simple-machines/tests/     Playwright tests (Chromium is preinstalled in Claude's cloud workspace)
tools/publish_game.py          build + wrap with PWA head + copy into site + bump sw.js
```

## Change → test → publish

1. Edit files in `src/simple-machines/`.
2. `python3 src/simple-machines/build.py` (writes gitignored page/preview/test/jtest html next to it).
3. Test (from `src/simple-machines/tests/`):
   - `python3 t2.py all all a|b|c` — solves every level of every station per track (expect all `p2`, `ERR []`). Slow: run stations in parallel background jobs, ~2 min per station.
   - `python3 t5.py a|b|c` — endless mode.
   - `python3 ov.py <track> <stations>` — **text/arrow overlap + clipping detector**. Must print nothing. The teacher has complained twice about text overlapping arrows/graphics; run this after any scene change and also eyeball `gal.py <track> <stations>` contact sheets (tests/shots/sheet_*.png) for text over non-arrow shapes.
   - `python3 failtry.py` — a failed physical try (ramp «بکش!», pulley/wheel/wedge choose, lever «فشار بده!», tug «برو!») costs nothing at ANY level; scale «جرم نامعلوم» wrong sum is free too. Scale and seesaw are live (no supports). Only calculation/prediction questions keep the two-chance rule.
   - `python3 mapchk.py <gradeIndex>` — map avatar/«تو اینجایی» inside the map and clear of other items for stops 1–12 (prints nothing when fine).
   - `python3 jt.py <gradeIndex 0..4> [stops]` — plays the 12-stop journey as a child, checks resume, side quest, parent hold-button, progress-code round-trip, teacher page.
   - Test pages: `test.html` sets `window.__TEST` (old station grid, legacy storage key); `jtest.html` sets `window.__JT` (journey UI + debug hooks `window.__J`).
4. `python3 tools/publish_game.py simple-machines physics/simple-machines "کارگاه ماشین‌های ساده"`
5. Commit and push to `main`; Pages redeploys in ~1–2 min. The github.io URL is not reachable from Claude's sandbox — ask the teacher to check.

## Rules that matter

- Never break saved progress: localStorage key `sm-journey-v1` ({profiles, cur, week}); star data per track in `profile.S.prog["<track>:<station>"].lv[]`. Journey missions reference levels by index (`STOPS` in journey.js) — if you reorder/insert levels, migrate or keep indices stable. The progress code (`makeCode/readCode`, 23 letters) encodes stars by stop/mission position; changing STOPS mission counts changes the code format — bump/handle versions.
- Science/language: «نیرو» not «زور»; mass (جرم, kg, two-pan balance) vs weight (وزن, N, نیروسنج); formulas LTR with standard symbols (`ltrMath`, `.eqi`); units in Persian (نیوتن، کیلوگرم).
- Reading levels: track a (grades 2–3, `KID()`) = short sentences, no numbers/formulas, bigger font; b (grade 4) numbers; c (5–6) formulas.
- SVG text: `T(x,y,text,{anchor})` — note `direction=rtl`, so `anchor:"start"` = right edge at x, `"end"` = left edge at x. Font size is multiplied by 1.6 when halo is on. Keep labels off arrows (`arrow()` polygons carry class `farr`, which ov.py checks).
- New games: new folder `src/<game>/` + site folder (`physics/…`, `chemistry/…`, `biology/…`), add a card in `index.html`, publish with the tool (it adds the path to sw.js FILES). Reuse fonts from `assets/fonts`.
