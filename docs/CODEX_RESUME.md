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

## Next concrete action

Continue the lever step: inspect its actual current tasks, arrange see/try/apply packs with stable level ids, add the approved lever3 lift scene with the pivot on the wedge apex, preserve direct fulcrum dragging, and fix hint/show-me dead ends. Check current main again, then targeted lever tests and source-only checkpoint push. Do not publish before the release-wide checks and required owner review.
