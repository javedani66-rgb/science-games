# Science games — working guide

**Owner policy (2026-10-02):** project-wide modularity and low-cost continuation are mandatory for new/touched components. Read `AGENTS.md` and `docs/MODULARITY.md`; do not infer a whole-project rewrite. Latest card alignment is centered for all text/icons, preserving RTL.

Static site on GitHub Pages: https://javedani66-rgb.github.io/science-games/
Owner: a primary-school science teacher in Iran (grades 2–6). All user-facing text is Persian (RTL).
Talk to the teacher in Persian, in plain words; she/he is not a programmer.

<!-- principles-digest:start -->
## Owner-approved principles digest (full ledger: `docs/PRINCIPLES.md`; read it before any design proposal)

- Readability and an easy UI come first in every conflict (B13).
- Grade bands 1–2, 3–4, 5–6 (B1); a stage's grade band is not fixed (B14).
- Structure: map → land (topic + own theme) → environment → 3 challenges (green/orange/red, each with its own story, card art and scene) → missions as steps inside a challenge (B26, B2, D11). Land theme is a skin only; button/icon positions stay fixed; difficulty colour is a separate fixed badge (D11, D3).
- **Everything layered and modular, graphics included** (T17).
- Every stage teaches or reviews via a lesson card; the card's problem is a schematic of the game situation; card box + spaced practice from grade 1; cards link to stages (B15, B17, B24).
- No stars or accumulating rewards; entering and leaving only by the child's choice (B4, B5). A failed physical try costs nothing; no artificial failure (A8, A9). Every scored question is answerable from what is on screen (A2).
- Child understanding or UX is claimed only from real observation (B9).
- Every external source behind a principle or decision (paper, similar game, other countries' curricula) is logged with full reference, verification level and limits in `docs/research/DESIGN_EVIDENCE_REFERENCES_FA.md` (R-codes); the final justification report is built from it (E5).
- Items marked «پیشنهاد» in the ledger are proposals, **not decisions**.
- **Process:** when the owner states a rule or decision in chat, record it in the same turn in `docs/PRINCIPLES.md`, `docs/DECISIONS.md` and `docs/STATE.md`, commit and push. Run `python3 tools/check_project_health.py` at session start and end.
<!-- principles-digest:end -->

**Start with `START_HERE_FA.md`, then `docs/STATE.md`** (where we are, open items), `docs/README_FA.md` (map of the docs folder), `docs/FUTURE_TASKS_FA.md` (task list) and `design/README.md` (art sources, approved mockups, `design/ASSET_LAYOUT_FA.md`). Old handoffs live in `docs/archive/` — history only, do not start there.

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
- Science/language: «نیرو» not «زور»; mass (جرم, kg, two-pan balance) vs weight (وزن, N, نیروسنج); formulas LTR with standard symbols (`ltrMath`, `.eqi`); units in Persian (نیوتون، کیلوگرم — scientific terms follow the official textbooks first, then common scientific usage, B28/D33; the code still has «نیوتن» until the planned replace).
- Register: questions, instructions, science text and ALL buttons are written Persian; only Ostad's own lines are spoken, taken from `voice.js` (process praise, never «باهوشی») — see `docs/voice.md`.
- **Approved grade bands (owner, D13/B1):** 1–2, 3–4, 5–6. The code's tracks a/b/c are the old grouping (a≈grades 2–3, b≈4, c≈5–6) until migrated; see `docs/GAME_STRUCTURE_FA.md`.
- Reading levels: track a (grades 2–3, `KID()`) = short sentences, no numbers/formulas, bigger font; b (grade 4) numbers; c (5–6) formulas.
- SVG text: `T(x,y,text,{anchor})` — note `direction=rtl`, so `anchor:"start"` = right edge at x, `"end"` = left edge at x. Font size is multiplied by 1.6 when halo is on. Keep labels off arrows (`arrow()` polygons carry class `farr`, which ov.py checks).
- New games: new folder `src/<game>/` + site folder (`physics/…`, `chemistry/…`, `biology/…`), add a card in `index.html`, publish with the tool (it adds the path to sw.js FILES). Reuse fonts from `assets/fonts`.

## How to work with the teacher (her explicit rule, 2026-09-30)

- **Never block the chat on slow tests.** Start long runs (t2 all, jt, t5, ov all, leakchk) in the background with `nohup … > log 2>&1 &`, one chain for everything, logs in a temp folder. Do NOT `sleep`/poll-wait for them. Keep answering the teacher meanwhile; read the logs only when she asks or when you return to the work. Saves tokens and keeps the conversation fast.
- During coding: only quick targeted checks (`node --check`, one station/level). Run the full suite **once, at the end**, on the final build — never rebuild while a background run is using the built pages.
- The live site must stay working while she tests: commit + push `src/` as you go (the live site changes only when `publish_game.py` runs); publish only after the full suite passed.
- The cloud workspace restarts after the chat is idle for a while (background jobs die). When working unattended, run the suite in foreground chunks under 10 minutes each (e.g. `xargs -P 2`) instead of one long background chain.
- Background runs die with the session: note in `docs/STATE.md` that a run is in progress so the next session reruns it.
