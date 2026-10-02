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


## Current continuation checkpoint — 2026-10-02, lower-secondary archive and primary-only choices

This checkpoint supersedes the previous missing-source note: the owner corrected the folder, identified the earlier books as upper-secondary experimental-sciences sources, and instructed that lower-secondary choices be removed from this game while their report is kept for future, more complex or 3D games.

- Base main before this stage: `8a3d49f23cb59a586b5af0325f0f74acfd9d13e4`; base tree: `aa951a3dc92967757fcb934dc12d69aa9dad739c`. This commit contains the source changes, reports and targeted tests below; use the commit containing this section as the new stage checkpoint.
- Reviewed the supplied science books for grades 7–9. Grade 7: code 706, 1405 printing; grade 8: code 806, 1399 printing; grade 9: code 906, 1399 printing. The older 8/9 editions require current-edition comparison before future development. Review was selective: contents, introductions and relevant physics chapters, with representative rendered pages; no full biological/geological or teacher-guide audit is claimed.
- Two bounded agents reviewed grade 7/8 and grade 9; a third implemented the primary-only choice flow and compatibility checks. Findings are reconciled in [lower-secondary curriculum guide](CURRICULUM_LEVELS_LOWER_SECONDARY_2026-10-02.md). The [primary guide](CURRICULUM_LEVELS_PRIMARY_2026-10-02.md) now links the new product-scope decision. No textbooks, page images or private Drive links were uploaded.
- Fresh onboarding, adult grade/level selectors and standalone station choices now offer only grades 2–6 / tracks a–c. Completing c no longer offers advancement to d. The physics model and question bank are unchanged.
- Historical grade indices, track d, profiles and progress-code decoding remain compatible. Existing historical profiles can resume, preserving stars, stash and response evidence; an explicit adult change to a primary grade keeps their old data. Track d is no longer newly offered or unlocked. This is a deliberate compatibility boundary, not a dedicated lower-secondary curriculum.
- Checks completed: JavaScript syntax checks for journey.js/app.js; primarycompat.js; quizevidence.js; Python compile for the new UI test; local build; primaryonly.py browser checks of fresh choices, c completion, legacy 7/8/9 profiles/codes/evidence, explicit migration and standalone choices; savechk.py passed with exit 0 and no findings. Playwright headless-shell was installed in the scratch test environment. No tests are claimed from the failed earlier full-Chromium launch attempt.
- The frozen 27-job evidence recorded above applies to the old source checkpoint only. It does not certify this changed candidate. The final full suite remains due once replay/content changes are complete and the revised candidate is frozen.
- No publication command was run. Public HTML, service worker and previous review ZIP are unchanged. No child pilot or new owner station signoff occurred.

Next concrete work: implement replay after demonstration and completion with stable progress and distinct learning evidence, then reduce required primary-grade calculations using the existing audit and curriculum guide. Lower-secondary development stays deferred; the archive guides a future separate design. Upper-secondary math-stream sources have not yet been supplied or reviewed. Review and test the final revised candidate before requesting station signoff for publication.


## Current continuation checkpoint — 2026-10-02, map/path precedents research

The owner requested a study of comparable map/path games before the full current-content difficulty inventory. The owner explicitly authorized agent delegation wherever helpful; use distinct bounded agents and parallel work as needed. Before a new task, announce a visible model/effort recommendation and pause for the owner's choice or continuation instruction. These are project continuation preferences, not a claim that global ChatGPT memory was written.

- Base main: `7967ddeef8f3bd52279b4c11a77362e769e402e8`; base tree: `e6aca37cd52b3a698884eb445f8a27382079c6a3`. The commit containing this section is the durable checkpoint for this documentation stage.
- Three agents reviewed official sources for Wonder/Yoshi, Prodigy/DragonBox, and Slay the Spire/Celeste. The root reopened the sources used in the synthesis and inspected current journey map/mission/side flow. Khan Academy Kids and Game Accessibility Guidelines provide complementary navigation/accessibility examples.
- Added [map/path game research](MAP_PATH_GAME_RESEARCH_2026-10-02.md), in Persian: six game cases, evidence vs design inference, exact source links, limits of transfer, current-code implications, a proposed harbor branch diagram, content/progression data requirements and pilot questions.
- No games were directly played and no child pilot or learning-efficacy study was conducted. Official descriptions support stated mechanics; historical release notes support recorded UI changes. They do not establish outcomes for Persian-speaking primary pupils or two pedagogically equivalent routes.
- Design direction discussed by the owner: thematic routes such as carpentry workshop/factory and fishing/pirate docks; optional harder branches with challenge symbols; alternate routes may progress only when required learning goals are covered. Red alone must not encode difficulty, and current red location-marker use requires review.
- Existing side quests unlock after main stop completion and do not replace the main route. The report explicitly distinguishes a proposed alternate route from this existing system.
- A bounded independent review found no factual/source-limit blocker in the Slay the Spire/Celeste cases and confirmed that alternate-route credit depends on required learning-goal coverage.
- Checks: report source-reference inventory, relative report links, Persian glyphs, balanced diagram fences and whitespace diff. No code/build changes, new gameplay tests, live publication or changes to the old review ZIP occurred.

Next concrete work: the full inventory of existing content (missions, quizzes, endless mode, labs, home tasks), recording prerequisites and separate conceptual/calculation/reading/control difficulty. Then select one harbor prototype and define equivalent learning-goal coverage for its two routes before implementation. Replay and primary-required-calculation revisions remain pending. Publication still requires the final revised-candidate checks and per-station owner signoff.


## Current continuation checkpoint — 2026-10-02, content inventory and extensible route planning

The owner chose medium effort to conserve the remaining usage budget, explicitly requested parallel agents, reusable foundations for three or more routes, design assets where useful, and Git checkpoints. Medium was used for the bounded delegated audits. Before a new task, preserve the earlier announce-model/effort-and-wait preference; this stage was authorized. This is a project preference record, not a global-memory write.

- Base main: `d2f9bafe747c149ded83abc23ae8e530b3379aaa`. This checkpoint adds analysis/design/tooling only. Runtime source is unchanged relative to that base; the earlier primary-only choice changes remain in place.
- Five bounded agents audited force/scale/friction, lever/ramp/pulley, wheel/wedge/sort, quiz/support, and route assets. Root reconciled source/runtime limits, normalized Persian text and source-reference paths, and compiled [content/route foundation](CONTENT_ROUTE_FOUNDATION_2026-10-02.md).
- `design/content/source-inventory.json` extracts 9 stations, 78 registered level IDs, 221 catalog challenge IDs and 205 quiz IDs (185 with active a/b/c labels, 20 d-only historical). It includes stop/support metadata and source hashes. Generator type sampling uses 64 deterministic seeds per band; it does not exhaust numerical variants, mount the UI or certify physics.
- `design/content/content-audit.json` records all 78 level and 205 question assessments, prerequisites, rationale, required changes and source references. All 221 catalog IDs link to family/parent assessments; these are not 221 independent item approvals. Grade arrays are related evidence, not eligibility gates. Topic/definition/video review limits are explicit. Level proposals: 20 core, 38 mixed, 8 challenge, 12 extension. Question proposals: 40 core, 82 mixed, 42 challenge, 41 extension.
- `design/routes/harbor-plan.json` is a draft planning example with three alternative routes and one side route. Stable route/activity/goal IDs and arbitrary arrays avoid a fixed two-route model. Proposed goal coverage and difficulty are unapproved; source IDs are reuse candidates that require splitting/review. The validator accepts drafts only and is not a runtime game engine.
- Five original SVG map candidates (workshop/factory/fishing/pirate/difficulty) and a contact sheet were added. `assets.json` records 35 existing/new asset references with limited known provenance. No Nintendo art was extracted. These are navigation candidates, not shipped art or physics apparatus.
- Checks passed: deterministic re-export compared byte-for-byte; source hashes; complete unique level/question/catalog coverage; all catalog observed types have family links; axis/placement checks; existing source-reference and 35 asset paths; question track-label match; valid draft plan; three/four alternative route tests and rejection of unknown refs, missing goals, side completion credit, forbidden return, progression cycles, non-draft status and invalid axes. Small-icon contact sheet was visually reviewed at 64/32 px.
- No gameplay content edits, replay implementation, branched-map integration, child pilot, live publication or old candidate ZIP update occurred. The old 27-job evidence still does not certify a future revised candidate.

Next concrete work: split and rewrite the mixed harbor activities for grades 5/6, verify the common learning goals of each proposed alternative, then implement a small selectable harbor prototype together with replay and separate assisted/independent learning evidence. Preserve current save/code compatibility and introduce versioned stable route/activity IDs before storing route progress. Reduce mandatory primary calculations according to the item audit. Run targeted checks and the final frozen-candidate suite, then obtain per-station owner signoff before publication. Lower-secondary dedicated development remains deferred.


## Current continuation checkpoint — 2026-10-02, whole-game rollout order

The owner confirmed that detailed rewrite/integration must cover all lands and levels after the harbor pilot, and requested an efficient path avoiding duplicate work and wasted tokens. The announced GPT-6.1 Sol / medium recommendation was accepted. This stage records a roadmap only; it does not implement H1.

- Base main: `23264b13090a7ed87cc71d3aaf8acd960ccff4b7`. Added [whole-game rollout](WHOLE_GAME_ROLLOUT_2026-10-02.md) and `design/routes/rollout-ledger.json`; the ledger assigns all 9 stations, 78 levels, 221 catalog IDs, 205 quiz IDs and 12 stops. Initial audits already exist; rewrite, final item verification, integration and child validation remain pending.
- Execution order: H1 pulley harbor pilot (grades 5/6 plus necessary shared contracts), H2 full harbor (ramp/wheel/pulley; 24 levels), R1 first land (force/scale/friction; 28), R2 construction (lever/wedge; 17), R3 exhibition (sort; 9), R4 reconciliation/final frozen-build checks. H1 content carries into H2 rather than being restarted. Minimal prerequisite fixes can precede the pilot if they actually block it.
- These are content work groups. Current LANDS still merges construction/harbor; any map split is a single shared task. One owner handles shared route/save/replay code and one question ledger prevents duplicate edits. Future grade-specific activity choices must not simply use track groups or audit grade arrays as approval.
- All 61 current a/b/c mission level IDs and the other 17 registered IDs are explicitly retained. Every original ID needs a disposition and migration result where applicable; station completion includes standalone/endless/lab/questions/definitions and stop-specific home/learn/side/map surfaces. Historical d stays compatibility/archive.
- The roadmap defines change-impact review, reuse of source/page evidence and assets, bounded agent inputs, targeted checks while building, the final frozen suite, and checkpoint fields for resumption. NEXT.md now points to this roadmap instead of restarting historical lever/scale-next instructions.
- Read-only delegated dependency review checked station counts, 61+17 coverage, shared prerequisites/text ownership and current land/stop boundaries. Ledger IDs were compared to baseline inventory, relative references checked and whitespace checked. No gameplay/source/live/build changes or new educational/child approval occurred.

Next concrete action: H1, beginning with actual grade-5/6 pulley learning goals and split activities; then implement the minimum shared route/replay/evidence/save contract and a selectable harbor sample. Subsequent groups must reuse the accepted implementation and review only real changed dependencies. Preserve the owner's announce-model/effort-and-wait preference for new tasks. At each completed batch update the ledger and this checkpoint; do not begin a fresh whole-book/game audit without an identified changed source or missing evidence.


## Current continuation checkpoint — 2026-10-02, H1 harbor source prototype

The owner accepted GPT-6.1 Sol / medium and explicitly requested as many parallel agents as useful. One bounded agent built harbor content/renderer; another independently reviewed and added regression checks. Root owned app/journey/save integration. No publication was requested or performed.

- Base main: `a6b1d509877dcae7047634db7bc84e916bbd593e`. See [H1 implementation](HARBOR_IMPLEMENTATION_2026-10-02.md), [content witness](HARBOR_CONTENT_2026-10-02.md) and source files harbor-content.js/harbor-routes.js.
- Two data-driven routes each contain direction, comparison and need-fit activities. Eligible profiles are grade indices 3/4 and track c. Actual observations gate questions; compare uses identical internal W60/S40/h1 and requires fixed blocked plus fixed/movable lifted. No numerical answer, support count or required formula; a qualitative renderer flag applies only to this pilot. A short independent help avoids old shared-formula/definition leakage.
- Same-spec replay after completion/show-me is added to normal playLevel, including header restart. Practice does not overwrite original res, catalog credit or resume state. The review caught and corrected a resume rewind after replay-back. Original results determine final stars.
- Harbor first/latest main run and practice evidence are separate, per-profile, versioned and local. Help and correction are distinguished from first independent answers. Corrupt activity records are normalized. Prior goals gate activities and can be reused when changing route.
- This is a separate practice branch, not equivalent credit for the old mixed/advanced stop-10 missions. STOPS, grade/track slots and code formats are unchanged. Legacy codes omit route evidence. Main-region progression and route-code transfer require H2 design/migration; current version-mismatch handling resets pilot state and must be replaced with an explicit preservation/migration policy before a versioned public rollout.
- Re-extraction proves legacy level/catalog/question/stop definitions unchanged; hashes of changed/new files and six pilot activities are recorded in content-audit. Historical assessments remain proposals, not refreshed full approvals. Rollout ledger records prototype status with no legacy level marked rewritten.
- Targeted checks: JavaScript syntax; build; harbor_routes.js (independent regression/content-gate checks); harbor_browser.py (all six activities, both routes, replay, reload, legacy save/code equality, 390/1280 layouts); primarycompat.js; quizevidence.js; savechk.py (exit 0, no findings); machinephysics.js (9010 deterministic checks); content inventory/hash/coverage checks. Final full suite and child/owner station review remain due. Mobile selector and comparison screenshots are in design/routes/h1-*.png. failtry.py also passed (all scenarios OK, ERR []); a third-route data-extension assertion passed without adding a shipped route.
- Built local pages only. Public HTML, service worker and old review ZIP are unchanged. No child pilot or owner scientific/visual signoff is claimed.

Next: review the H1 sample and define common required stop-10 goals and compatible main progression/code migration, then H2 complete harbor (ramp/wheel/pulley and grade-specific primary content). Reuse this route/replay implementation and its checks. Continue under the whole-game roadmap; do not restart unrelated full audits. New task model/effort announcement and owner choice preference remains in force.


## Current continuation checkpoint — 2026-10-02, route visual/text research

- Base main: `0ae943727e903897b6e11f8073690429fb5b7eb0`. Owner explicitly requested agents, similar-game research, saved lessons and a report covering graphics, justification/alignment and related usability. Two bounded agents worked in parallel: visual precedents and Persian text/accessibility. GPT-6.1 Sol / medium scope continues.
- Added [research and concrete H1 recommendations](ROUTE_VISUAL_TEXT_RESEARCH_2026-10-02.md) and `design/routes/ui-guidelines.json`. Root checked primary pages and viewed Wonder, Khan Kids and Sackboy images; Forza/Grounded examples were also inspected. Sackboy provenance and screenshot/mobile/child-study limits are explicit. No third-party artwork was copied into the repository.
- Recommended semantic whole-card green/orange/red difficulty, separate selection/completion/lock/focus, original scene identity, shared role tracks, right-aligned Persian descriptions, bidi isolation and visible branches. Color sequence is our project proposal; examples do not establish it as a universal game convention. Guidance accepts arbitrary route counts and avoids array-index semantics.
- Current CSS/code confirms centered white cards, differing title heights, small mobile text, completion replacing selected text and an anchor/down-arrow connector. Proposed changes are not implemented. Agent text note's historical next-work paragraph was superseded by existing H1/inventory checkpoints and was not adopted.
- Checks: JSON parse, relative local report links and whitespace checks. Research only: no runtime/build change, no new game regression run or child result. Live HTML, service worker and review ZIP remain unchanged.

Next concrete action: refine and visually check H1 selector under the new rules before H2 progression/code migration and full-harbor content. Preserve all existing progress/evidence contracts; reuse the whole-game rollout rather than repeat baseline audits. Announce model/effort and allow owner adjustment before beginning a new task.


## Current continuation checkpoint — 2026-10-02, H1 selector UI refinement

- Base main: `ff96bd77ed0060220fe2618a4a8ee85deeb8b21d`. Owner accepted announced GPT-6.1 Sol / medium by instructing continuation. Root implemented; one bounded agent reviewed Persian wording/accessibility and the final source/mobile image without edits. See [UI checkpoint](HARBOR_UI_REFINEMENT_2026-10-02.md).
- Semantic tier colors cover whole cards; two original embedded SVG scenes are saved with provenance. Shared grid roles, right-aligned descriptions, separate selected/completed state, keyboard focus, contextual lock reasons and responsive SVG connections support arbitrary route counts. Only two routes ship.
- Reviewer caught completed prerequisites still being named in the lock reason. A shared missing-goal helper now drives both availability and explanation; focused regression verifies it. Content version and stable IDs/save formats are unchanged; short summaries and tier metadata do not reset evidence.
- Checks passed on the final local build: JS syntax/build; harbor_selector.py at 320/390/1280, text200%, role alignment/overflow, focus, distinct simultaneous states, role text contrast >=4.5:1 and four reordered fixture routes; harbor_routes.js; harbor_browser.py (six activities, save/code/replay/reload); primarycompat.js; source re-extraction unchanged except hashes and content audit/path checks. Source/audit hashes refreshed; scientific assessments were not repeated. Mobile/desktop screenshots saved in design/routes/h1-selector-*-refined.png.
- Public HTML, service worker and old review ZIP are unchanged. No owner/child approval or full revised-release suite claimed. Subgrid fallback, grayscale human review and future mixed-script text remain bounded review items.

Next concrete action: H2 full harbor, beginning with shared required stop goals and versioned preservation/migration for main progression and code transfer. Reuse H1 source/UI/activities and the whole-game roadmap. Do not restart the baseline content/book audit. Announce model/effort and allow owner adjustment before the new task.


## Current continuation checkpoint — 2026-10-02, indie card UI research and contributor foundation

- Base main: `a05dcdc202ed713d8cbc4d2e9708041ad723869b`. Owner accepted announced GPT-6.1 Sol / medium and explicitly requested indie games, creator forums and YouTube. Three bounded agents split visual precedents, forum accounts and video discovery. Root verified source pages and selected images; no repeated broad map/content audit.
- Added [card study](INDIE_CARD_UI_RESEARCH_2026-10-02.md), `design/cards/README.md`, `evidence.json` and `copy-contract.json`. Records distinguish route/shop/upgrade/reward/action cards, first-hand reports versus visual observations, unresolved problems and untested project inferences. Four YouTube links verified via creator/publisher pages; playback/transcripts unavailable, no watched-video or timestamp claim.
- Wildfrost shop, Dicey upgrade/trade, Obelisk rewards/event and Dolven image reviewed. Root caught a misidentified Dicey screenshot: VECy3S is two-card trade, not a three-card Buy shop; that claim is rejected and the correction is recorded in evidence. Forum cases include Rampallians and The Cup; designer/creator accounts include Battle Casters, Dragon Bridge and Steamhounds.
- Owner copy/typography review stays open despite prior technical passes. Proposed goalLead uses actual bold font, balanced information roles and last-line/end-of-block review. JSON examples are proposals, not runtime rewrites. Contributor guide specifies editable art, crop/text zones, states, provenance, stable IDs and before/after decision records. No third-party art or new licensing assertion added.
- Checks: JSON parse, unique evidence/video IDs, four video entries explicitly watched=false with empty timestamps, local links and whitespace. Runtime/build/source hashes and live/public output unchanged; no gameplay tests repeated for documentation-only changes.

Next: a bounded second harbor copy/hierarchy pass before H2; use the new contract, inspect actual rendered last lines and selective emphasis, preserve progress and record child/owner findings separately. Keep the announce-model/effort-and-wait preference before starting a new task. After that resume H2 and the existing whole-game rollout; do not restart primary textbook or whole-game audits.


## Current continuation checkpoint — 2026-10-02, owner card preview

- Base main: `19d239794f4c479810c9b7b7e10f9b3428de8f09`. Owner accepted announced GPT-6.1 Sol / medium by asking continuation. One bounded read-only agent rechecked Dicey/Wildfrost title placement; root viewed the same two official images. No broad repeated research, video viewing or child-study claim.
- [Latest owner decisions](HARBOR_CARD_OWNER_REVIEW_2026-10-02.md) supersede historical visible-status/count guidance for route selection cards. Live conversational preview has centered titles, stronger tier fills, accessible emoji, requested CTAs, independent ring/elevation/check selection, no visible selected/open sentences or activity counter. Preview copy is directly editable locally; it does not automatically write runtime or save files.
- Updated copy contract/evidence; saved three preview screenshots and two Twemoji PNG sources with full graphics license and attribution. No commercial game artwork copied. Rewards/costumes/treasure/video/teacher code are recorded as future design only; do not assume implemented or that a shared code proves individual completion.
- Verified 320/390/736 layouts, textarea growth, emoji loading, exclusive aria-pressed state, no script errors; measured palette text contrast. New dark visual/200%/child review remains pending. No runtime/build/public/service-worker/save changes; existing selector/game tests are not rerun or claimed for this preview-only turn.

Next: collect owner feedback on preview, implement the agreed reusable card roles in H1 source, update targeted selector checks without losing progress/replay contracts, then H2 and whole-game rollout. Never restart the completed books/content audit or broad indie research.
