# Release continuation handoff — 2026-10-02

Repository: `javedani66-rgb/science-games`
Branch: `main`
Verified source checkpoint: `a3115af5df8f5af94d5d194449c8002e602fbb80`
Handoff documentation commit: `f93fd0cade0d6438e29f0ba492f26d1ee626f2b0`
Previous source change: `0468be10f8f76d6bc5ef98a3c32ef1464a145275`
Tree at verification checkpoint: `7fd9e879cdf09693f8dec42cb18937703a11be06`

## Saved work

The source checkpoint contains the rebuilt simple-machines stations, shared ideal-machine physics, evidence-first challenges, quiz outcome reporting, accessibility and layout fixes, and regression tests. The verification commit changes no source files. The live page and service worker were not changed by this release candidate.

A portable owner-review package named `science-games-review.zip` is saved in the user's Library. It contains `preview.html`, `stations.html`, the child-pilot plan, release-check report, and Persian instructions. The preview and station pages were byte-compared with a fresh build of this source checkpoint and matched exactly.

## Verification already completed

The frozen final build passed all 27 release jobs. The recorded outcomes include 132 level runs and 789 full-credit challenges across tracks a–d; complete journeys for grades 0, 2, 3, and 6; endless mode, save/restore, reset, map and lever checks; zero findings in final overlap checks across all four tracks; and reviewed answer-leak flags. Physics model checks: 9,010. Focused machine interaction checks: 15/15. Offline layout checks covered 320×568, 390×844, and 1280×800. Independent review reported no release blocker.

Detailed test results and boundaries are in the Library review package, `RELEASE_CHECKS.md`. Do not rerun the full suite unless source/build inputs change or a specific discrepancy is found. This handoff and verification commit supersede older historical checklist entries in `docs/NEXT.md` and earlier continuation notes wherever they still describe the scale/lever work as next or the final test suite as pending.

## Work that can proceed without owner input

- Fetch current `main`, compare it with the verified checkpoint, inspect changed files, and preserve any unrelated local edits.
- Keep this handoff current and resolve stale or contradictory release notes when the correction is supported by committed evidence.
- Inspect the publication script and verify release prerequisites. Build or run targeted tests only if relevant inputs changed; run the release suite only for changed code/build inputs or a concrete discrepancy.
- Prepare deployment commands and a live-verification checklist. After owner signoff, publish, commit/push generated output, and verify the deployed version.
- Ask agents for bounded, independent reviews when needed. Useful parallel assignments: (1) science/content and evidence-to-question review, advisory only; (2) visual, keyboard and responsive interaction review; (3) source/build/test and publication-integrity review. Give agents the current commit and changed-file scope. Do not rerun completed checks or ask several agents to repeat the same review. Reconcile findings before any edit.

## Owner input still required

1. The project owner reviews the science and visuals station by station. `docs/NEXT.md` explicitly requires this signoff before publishing; agent reviews cannot replace it.
2. A 10–15 minute child pilot requires an actual child participant and a human observer. Use `CHILD_TEST_PLAN.md`; report observations separately from technical QA.
3. Any new scope or product choice arising from the pilot requires owner prioritization. No learning-efficacy claim is supported by the current technical suite.

## Next run plan

At the scheduled continuation, fetch current `main` and read this handoff. First check for newer commits and whether the owner has supplied station signoff. If source/build inputs changed, assign distinct review scopes to agents where useful, inspect their findings, then run only the appropriate tests. If no code changed, do not repeat the completed suite; finish any concrete release-preparation task and report the remaining owner gate. Never publish before per-station signoff. If signoff is already recorded, proceed with the repository publish script, commit/push, and live verification.

## Resume instructions

Preserve unrelated or uncommitted local changes. The live game remains the working version until the release gate is met. If no independent technical task remains, leave the release candidate ready for owner review and stop at that gate.

## Checkpoint rule

At the end of every coherent work stage, update this handoff before pausing or handing the work to another session. Record the current `main` commit, what changed, the exact checks completed and their outcomes, whether the public game changed, open owner decisions or gates, and the next concrete action. Link to durable reports or logs when they exist. Commit and push the updated handoff with the stage checkpoint when repository access permits; if that fails, preserve the update locally and report the failure clearly. Do not leave an unfinished or interrupted check marked as passed.

## Continuation checkpoint — 2026-10-02, release preparation

- Fetched `main` and fast-forwarded a clean local checkout to `4b97c24606a2c18ef4ab5c050a356182170a3b5d` (main before this documentation checkpoint). No local edits were discarded.
- Compared the full tracked tree against `a3115af5df8f5af94d5d194449c8002e602fbb80`: only this handoff changed. Source, build inputs, publication script, live HTML and service worker are unchanged.
- Read the current `CLAUDE.md`, this handoff, `docs/HANDOFF.md`, `docs/NEXT.md`, `design/README.md`, build script and publication script. The newer handoff remains authoritative over historical unchecked tasks.
- Static preflight: all 19 JavaScript inputs listed by the build script exist and are nonempty. The three embedded fonts, web manifest, icon, service worker and existing live HTML are present. This checks file availability only; it is not a new build, browser test or deployment test.
- The existing review ZIP contains `preview.html`, `stations.html`, `CHILD_TEST_PLAN.md`, `RELEASE_CHECKS.md`, `README.txt` and `RESULTS.txt`. SHA-256: `08b333877a86e35d0bd3520e9705e145e4beb10515dcb042ed43124f5ba0d225`. The child plan and detailed reports are archive members, not standalone tracked repository files.
- No regression tests were rerun and no agents were assigned: there are no changed code/build inputs or new discrepancies requiring a review. The previous 27-job results remain the recorded technical evidence.
- No owner scientific/visual signoff is recorded in the supplied conversation or current release handoff. No child pilot was conducted. No publication command was executed; the public game remains unchanged.

Durable verification evidence: [frozen release verification commit](https://github.com/javedani66-rgb/science-games/commit/a3115af5df8f5af94d5d194449c8002e602fbb80), whose commit message records the completed suite; [publication script at the verified checkpoint](https://github.com/javedani66-rgb/science-games/blob/a3115af5df8f5af94d5d194449c8002e602fbb80/tools/publish_game.py). Detailed reports remain in the previously saved owner-review archive.

### Prepared publication and live-verification checklist

Run this sequence only after the owner signoff is recorded for each station in the reviewed release candidate:

1. Fetch `main` again, preserve concurrent edits and compare source/build inputs against the verified checkpoint. If they differ, review the changed scope and run the necessary checks before publishing; signoff must apply to the resulting candidate.
2. From the repository root run `python3 tools/publish_game.py simple-machines physics/simple-machines "کارگاه ماشین‌های ساده"`. The script rebuilds the game, wraps the PWA HTML, writes the live page and changes the service-worker version. It has no dry-run mode; do not execute it during preparation.
3. Review `git diff -- physics/simple-machines/index.html sw.js`. Confirm the intended generated page, Persian RTL wrapper, manifest/icon paths and new service-worker version. Stage only the intended release files and checkpoint notes; commit and push to `main` without force. Do not include unrelated local files.
4. Verify the deployment result and https://javedani66-rgb.github.io/science-games/physics/simple-machines/ . Check the portal link, fresh-load version, an existing-profile resume, representative station interaction, teacher report and offline reload after the service worker installs. Check for console errors and horizontal overflow on phone and desktop. If the live origin is inaccessible, record that limitation and leave live verification pending.
5. Record the release commit, public URL, exact checks/results and any remaining live-verification gap here. Conduct the child pilot only with a real child and human observer, using the archive's plan; never substitute technical checks for pilot observations.

Next concrete action: await and record owner scientific/visual signoff per station. No independent implementation task remains within this release-preparation stage. After signoff, execute the checklist above; any new scope remains a separate owner decision.


## Current continuation checkpoint — 2026-10-02, textbook alignment and replay feedback

This checkpoint supersedes the previous “no independent implementation task remains” statement. The owner has supplied new feedback: completed activities must remain replayable and the game should invite a child to try again after a demonstrated solution; the owner also requested a textbook-grounded grade-level report before further level decisions.

- Source reviewed: `d7aae618ccfda61745c9fbfe1376f8be2290b37f`; game source remains the verified candidate at `a3115af5df8f5af94d5d194449c8002e602fbb80`. Remote main copies of journey.js and st_ramp.js matched the local blobs.
- Read the six supplied primary science textbooks selectively: contents and teaching introductions, relevant measurement/force/motion/machine chapters, and representative inquiry activities. Representative pages were rendered and inspected. This was not a cover-to-cover or teacher-guide review.
- Three bounded agents reviewed books 1–3, books 4–6, and the current game question/replay flows. Findings were reconciled into [primary curriculum guide](CURRICULUM_LEVELS_PRIMARY_2026-10-02.md), committed as `fd3ba10f2925a124072633593fb2db9d8fade0c1`, and [question/replay audit](GAME_LEVEL_REPLAY_AUDIT_2026-10-02.md), committed as `518de8fb86b1e28d0bf32b633cc7217111397a5f`.
- Reports distinguish observed textbook requirements, design recommendations and review limitations. They include printed/PDF page references and actual game question identifiers. No textbook files, page images or private source links were uploaded.
- Findings: grade 4 main missions currently require formal machine-force calculations; grade 5/6 also include work/joules, mechanical advantage and wedge/screw formulas beyond the explicit demands of the reviewed chapters. Hiding formulas does not remove required calculations. Grade 2/3 also need review of vocabulary and concepts such as Moon weight and buoyancy.
- Replay already exists from the journey map, but successful mission results and completed individual challenges lack consistent direct replay. “Show me” locks the challenge and awards one point; it does not offer independent re-execution. The audit specifies same-example practice, fresh-example transfer, preserved progress, no duplicate points, and distinct assisted-learning evidence.
- No game code, published HTML, service worker or candidate ZIP was changed. Previous technical tests were not repeated. No child pilot was performed. The reports are analysis/specifications, not implemented features.
- Latest main before this checkpoint update: `518de8fb86b1e28d0bf32b633cc7217111397a5f`. Scientific/visual signoff is still absent and must apply to any revised candidate. Do not publish the older candidate by treating the owner's feedback as approval.

Next concrete work: use the curriculum guide and replay specification to prepare the next content/replay revision within the owner's authorized scope. Priorities are replay after demonstration and completion, grade-4 required calculation removal/optional routing, then distinct grade prerequisites for 2/3 and 5/6. Any code changes require targeted evidence/progress/replay checks followed by the final frozen-build suite under project rules. Keep grade 7–9 dedicated expansion deferred. At the end of each coherent stage, update this checkpoint and push it.


## Source check checkpoint — 2026-10-02, requested lower-secondary extension

The owner requested textbook alignment for grades 7–9 and confirmed this scope after a file mismatch was found. The newly supplied folder contains five PDFs whose covers and title pages identify upper-secondary books: C110217 (science laboratory 1, grade 10), C111217 (science laboratory 2, grade 11), C110214 (physics 1, grade 10), C111244 (physics 2, grade 11, experimental-sciences track), and C112244 (physics 3, grade 12, experimental-sciences track). All five covers were inspected. These are not evidence for grade 7–9 curriculum.

No lower-secondary grade-level conclusions were made from these files; no new game code, public output or tests were changed. The primary report remains unchanged. Latest main before this note: c39fd2e0a1385bb8558c782649fde2b566f9eaa5. Next action for this source-analysis task: obtain the intended science textbooks for grades 7, 8 and 9, then extend the curriculum guide with exact page references and distinguish grade-specific prerequisite demands. Do not silently substitute grades 10–12 or label existing track d curriculum-aligned. The owner has authorized analysis of lower-secondary sources, not revival of the previously deferred dedicated grade 7–9 implementation.
