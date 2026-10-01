# Codex continuation — stage 2

Updated: 2026-10-01. Repository: javedani66-rgb/science-games.

## Resume procedure

1. Fetch the CURRENT main HEAD. Read CLAUDE.md, docs/NEXT.md, docs/HANDOFF.md, docs/AUDIT_2026-10-01.md, design/README.md and this file. Follow applicable repository instructions.
2. Check newer commits and source before choosing work. Some unchecked items in older notes were already completed. Do not repeat fixes just because an old checklist says "todo".
3. Continue stage 2, starting with the scale station, then lever, then the remaining stations in docs/NEXT.md. Work one coherent step at a time. Use the approved balance and lever mockups.
4. Preserve the working live site. Edit src/simple-machines/, build generated output through the repository scripts, and publish only after required checks and review pass.
5. After each coherent step, commit and push source plus updated continuation notes. Record the commit, completed checks and their results, remaining checks, exact next action, and whether publication happened. Never report an unfinished or interrupted check as passing.
6. If interrupted, resume from these committed notes. Do not rely on scratch files or background processes surviving a session. In unattended work run tests in foreground chunks under ten minutes, as docs/NEXT.md requires.
7. If another contributor changed the same station, inspect and reconcile the latest changes before editing. Do not overwrite them or continue from the older baseline.

Communicate with the owner in plain Persian. Make routine technical choices autonomously within the agreed scope.

## Baseline inspected

Main HEAD before this documentation commit:
`6df993e5ad0d6d8811f0341a79a3b6f5fa803acb`
(2026-10-01 09:11:21 UTC).
Latest commit: visible question subjects, scale objects before prediction, wheel/wedge/screw comparison scenes, RTL order for alternatives.

Repository documentation and latest commit were inspected through GitHub. No game source has been changed by this continuation setup. No local browser/runtime regression suite was run during setup; runtime and visual behavior remain to be verified when implementation starts.

Earlier repository work already includes stable level IDs, challenge catalogue infrastructure, progress code v3 with older-code reading, force/friction separation, reordered stops 7/8, Predict–Observe–Explain fixes, visible calculation rules, hint/show-me flow, explore-first offer, and side-quest gating. Verify actual source and behavior; do not reimplement these features blindly.

## Additional action list from the comparison and review

Integrate this checklist into the existing station-by-station work, rather than treating it as a separate rewrite. Mark items done only with evidence; partial implementations need their remaining scope recorded.

- [ ] 1. Establish a source/build baseline and check saved-progress compatibility and restore.
- [ ] 2. Audit scientific models, terminology and accepted answers: mass/weight, instruments, friction, torque, work and mechanical advantage; make simplifications explicit and visible when needed.
- [ ] 3. Verify the order of stops 2–3 and early quizzes against prerequisites for every current track.
- [ ] 4. Rebuild teaching sequences as see → try → apply: evidence before terminology and scored assessment; unseen predictions are free.
- [ ] 5. Introduce terms immediately before first use, with short visible explanations and appropriate reading level.
- [ ] 6. Make machine comparisons controlled: wedge, screw, ramp, wheel/axle and pulley; hold irrelevant variables constant and show the quantities needed to reason.
- [ ] 7. Distinguish completing a task from optimizing it; explain the goal and success criteria before judging.
- [ ] 8. Give feedback from the actual scene state; verify the hint ladder and show-me option prevent dead ends.
- [ ] 9. Audit scoring across exploratory and assessed tasks; failed exploration should give guidance and follow the agreed free-try policy.
- [ ] 10. Differentiate teaching and task wording for current a/b/c tracks. Dedicated grade 7–9 content remains DEFERRED under the latest docs/NEXT.md decision; do not implement that extension now.
- [ ] 11. Align engineering/exhibition tasks with actual machine parts and classifications; show the specific part being classified and use supported builds.
- [ ] 12. Connect home tasks and story goals to the scientific action; adapt wording where grade levels require it.
- [ ] 13. Audit persistent quiz outcomes and teacher reporting; distinguish completion from evidence of understanding without inventing an unapproved server or new progress-code format.
- [ ] 14. Review natural Persian, written/spoken register, RTL ordering, and readable Latin formulas/units.
- [ ] 15. Audit accessibility: names/labels, keyboard and focus, motion settings, and alternatives to essential drag-only interaction.
- [ ] 16. Reduce conflicting definitions/formulas by sharing concept data where practical; trace each question and feedback message to what was taught.
- [ ] 17. Verify relevant phone/desktop layouts, save/restore, offline behavior, and interaction after the final changes.

Repository scope constraints still apply: new everyday-object assets, full recorded voices and dedicated grades 7–9 are later-version work unless already approved/supported. Do not add a backend, external account requirement or new service as part of this list.

## Verification and publication

Read the actual test scripts and their command-line arguments first. Preserve test hooks.
Build: `python3 src/simple-machines/build.py`.
Tests live in `src/simple-machines/tests/`.
Use targeted scientific/interaction checks while implementing, then the required full suite at the release boundary: t2 across stations/tracks a–d, t5, ov, jt journeys, failtry, savechk, resetchk, mapchk and leakchk, plus firstscreen for the visible-question requirement. Include relevant desktop/mobile screenshots and save/restore checks.
Use independent review when repository instructions require it.
Publish through `python3 tools/publish_game.py simple-machines physics/simple-machines "کارگاه ماشین‌های ساده"` after all release checks pass, then commit/push and verify the live version. If checks cannot run, record the concrete blocker and keep the current live game intact.

## Checkpoint: scale rebuild (2026-10-01)

Base: `62d629f57d25aab54a37e37a96682718b5f5d4fb`; main was fetched again before saving and had not changed.
The code commit containing this checkpoint is titled `Rebuild scale learning packs and approved balance interaction`.

Completed in source:
- Six balance levels now use stable catalogue challenge ids and see/try/apply packs. Existing level ids, journey mission counts, storage key and code v3 are unchanged. Old in-flight challenge types still mount.
- Approved bal2 artwork exported reproducibly by `tools/build_balance_art.py`; beam/needle rotate about one pivot, pans stay vertical, equal-arm model remains independent of art, assets are embedded for standalone use.
- Predictions visibly say they are unscored. Pan interpretation is visible before the first scored answer even with formulas off. Unknown-mass totals remain hidden until the sum is answered.
- Balance is acknowledged before requesting fewer weights. Exploratory balancing always earns full success credit; using show-me earns one point. The previously agreed free-sum policy is retained: 2 failed sums then success = 2 points, 3 = 1 point. Physical attempts do not count as failed sums.
- Help prevents dead ends; the physical help button is removed when the sum phase starts. Consumed object selections cannot clone an object across pans.
- Balance placing/removal and spring/water handle have keyboard alternatives; focus survives repaint. Lab objects are paged rather than overlapping.
- Spring observation comes before calculation/Moon tasks. Numeric spring comparison uses kg/g masses; Moon decimals are enterable. First-quiz Moon/weight/spring questions are delayed until the relevant stop. Weight word cards moved to stop 3; unsupported bathroom-scale questions remain in legacy mounting code but are not selected by the new main missions.

Verification actually completed:
- Build and `node --check`; `git diff --check`.
- `t2.py scale all a/b/c/d`: all challenges p2, ERR []. These station runs were on intermediate builds; subsequent focused fixes were checked below and need the final release-wide t2 run.
- Final `scalechk.py`: evidence and keyboard placement on all four tracks, no consumed-object duplication, four unsuccessful balancing experiments followed by p2, balanced-before-optimization, no answer-total leak, clean help handoff and disabled sum inputs, water with keyboard, 400 first-quiz prerequisite samples. ALL OK.
- `failtry.py`: ALL OK (all existing physical-try cases and revised b/c mystery order); `savechk.py`: silent/pass.
- `ov.py a/b/c scale`: silent/pass; c was rerun on the final build. `leakchk.py c scale`: no suspected leaks.
- `jt.py 0 3` and `jt.py 3 3`: LOG [], ERR [], saved resume and progress-code round-trip True.
- `firstscreen.py c scale`, `gal.py a scale`, desktop 1280×800 and phone 390×844 screenshots examined. No new object/text obstruction seen.
- Fresh independent reviewer reproduced the two interaction bugs, then independently confirmed their fixes plus visible reading rule and keyboard water slider. No remaining blocker in this scale change scope.

NOT published. `physics/simple-machines/index.html` and `sw.js` were not changed. The release-wide suite and owner's per-station scientific/visual signoff required in docs/NEXT.md have not happened. Do not mistake targeted checks for release approval.

Remaining scale scope: spring-scale/planet art, broader water/port placement decision, persistent quiz outcomes/reporting, full accessibility and offline/device coverage. The 17-item global checklist remains partially open; this checkpoint completes only its scale portions.

## Checkpoint: lever rebuild (2026-10-01)

Base: scale source checkpoint `431c7e1e956b8b4dda06442efd19011fafdd613c`. Main was fetched again before this checkpoint; no new upstream source changes were present. This source commit is titled `Rebuild lever learning packs and approved lift geometry`.

Completed in source:
- Stable level ids now select catalogue packs in see/try/apply order. Level a uses visual dots instead of numeric arm labels. Old in-flight types still mount; journey topology, storage and progress-code version remain unchanged.
- Approved lever3 props are embedded by `tools/build_lever_art.py`. The plank bottom pivots on the wedge apex; the stone begins on the ground, rises on the short end and stays upright. Dragging the wedge, tapping the press target and keyboard manipulation work; decorative layers do not intercept dragging.
- An observed motion challenge compares the actual circular trajectories of the two contact points before assessment. Fulcrum/arm names and ideal assumptions are introduced in the visible prompt. Predictions explicitly cost no points.
- Exploration in lever balance/lift earns p2 on success regardless of failed experiments; show-me after three failed attempts displays the actual solved scene and earns p1. The balance demonstration cancels stale tilt animations. `A.trial` now honors an explicit `pts` override; other station defaults are unchanged.
- Keyboard placement/removal and fulcrum movement preserve focus. Consumed selections cannot clone pieces. The drop hit-test transforms through the inverse beam rotation, so a visible tilted slot accepts an actual drop.
- Known weight arrows stay vertical and share one proportional scale; they avoid house-number labels. Both derived totals and quantitative arrows are hidden during unknown-mass questions; input brick masses remain visible.

Verification actually completed:
- Build, `node --check` and `git diff --check`.
- `t2.py lever all a/b/c/d`: all p2, ERR []. a and c rerun after the final interaction fixes; b/d passed before the inverse-drop/arc/arrow fixes and need the final release suite.
- Final `leverchk.py`: all four tracks observe before assessment, keyboard balancing/free trials, drop onto a visibly tilted plank, hidden mass totals/arrows, real show-me and cancellation of stale tween, all nine fulcrum positions, correct formula/grounded stone, keyboard press, lift help and observed trajectories. ALL OK.
- `ov.py c lever`: final run silent/pass after moving weight arrows above the bricks. Initial arrow/text collisions were corrected.
- `savechk.py`: silent/pass. `leakchk.py c lever`: no derived-total leak; one incidental match of the unknown answer with a visible input brick mass was inspected (both totals were hidden).
- `firstscreen.py c lever`: six challenge kinds, desktop contact sheet examined. Independent reviewer also inspected phone 390×844 and desktop 1280×800 geometry and interaction.
- Independent review found vertical-displacement labels masquerading as paths, tilted-plank drop rejection and misleading hidden-mass arrow scales; all were corrected and targeted regression checks added. Fresh reviewer independently rechecked all fixes on the final build at 390/1280 px: no remaining blocker in this scope and no JavaScript errors.

NOT published. Required release-wide tests and owner's per-station scientific/visual signoff are pending. `physics/simple-machines/index.html` and `sw.js` are unchanged. The seesaw uses the existing procedural room/brick/gauge art; full land palettes, the remaining global checklist and broader art/accessibility coverage are still open. Grades 7–9 dedicated content remains deferred.

## Next concrete action

Continue with ramp, then wedge/screw, wheel/axle and pulley, per docs/NEXT.md. Ramp still lacks evidence-first catalogue packs, controlled displayed comparisons, a keyboard handle, and a real show-me solution. It currently treats a successful nonminimum ramp as a failed attempt; acknowledge lifting before requesting optimization. Inspect current main before editing. Keep source-only checkpoints and postpone publishing until the full release suite and owner review.

## Checkpoint: machine bundle and reporting (2026-10-01)

Combined worktree: `codex/machines-bundle`; includes scale `431c7e1`, lever `781c241`, machines `cd878a3`, merge `2dd2b3e`. Remote main was fetched and remained `431c7e1` before this checkpoint. No publication.

Completed source:
- Ramp, wheel/axle, wedge/screw and pulley now share ideal models and controlled observed comparisons. Numeric assumptions are visible. Stable level/mission ids and progress code v3 remain unchanged.
- Physical exploration earns full credit for any successful allowed configuration; minimum/optimization is only judged when explicitly asked. Three failed trials provide working guide/show-me exits.
- Keyboard controls preserve focus, scene generations reject stale animation callbacks, and pulley observation moves the free end with rope travel.
- Classification identifies the specific part of each tool, supports keyboard bins and wraps long titles. Existing categories/item identifiers remain intact.
- Home tasks/end statements match actual practiced work. Quiz evidence preserves first answers separately from shown-answer corrections; parent/local teacher summary and copied message distinguish these. Detailed evidence stays on this device and is excluded from compact code.
- Lever follow-up assumptions/readable labels reconciled from the original worktree. Purple circular paths retain accurate path wording. Original worktree pending edits were preserved untouched.

Verified before checkpoint: 9010 deterministic physics checks; quiz evidence unit/restore/replay checks; 15 machine browser checks (keyboard, guided exits, nonminimum credit, stale callbacks); actual mobile quiz/report/replay/code31-char roundtrip with zero JS errors. Prior targeted t2 all levels of four machines on a/b/c passed. Sort keyboard checks passed; two title bounds issues were fixed in source, awaiting rebuild.

In progress, not yet passing: full release suite on generated build before the final sort font adjustment (t2 a-d, journeys grades0/2/3/6 x12, t5 a-d, ov a-d, failtry/save/reset/map/lever, leak a-d, firstscreen a/c). Logs in workspace `release_*.log`. The initial suite's no-argument leakchk/firstscreen jobs are invalid invocations; correct explicitly parameterized jobs run separately in release_extra.py. Do not count those invalid jobs as game defects or passing checks.

Next exact action: inspect every release log for exceptions, non-p2/stuck outcomes and JS errors; inspect leak flags and visual sheets. Wait until jobs finish before rebuilding. Then rebuild the small sort title fix and rerun `review_interaction_sort.py` (workspace), relevant sort/ov checks. Fresh `release_review` agent checks science/interaction source independently. Record actual results, commit/push continuation notes. Produce a standalone owner-review preview; publication still requires per-station owner scientific/visual signoff.

Remaining broader enhancements: new everyday art, full land palette/art pass, sound/mute, optional difficulty badges/code changes and dedicated7-9 content were not implemented in this bundle. Do not claim the entire historical wishlist is complete. Real child testing is still pending. Half-hour automatic scheduling is unsupported by the available scheduler (minimum hourly); no substitute recurring cadence was created.
