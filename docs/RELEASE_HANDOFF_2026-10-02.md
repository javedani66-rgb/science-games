# Release continuation handoff — 2026-10-02

Repository: `javedani66-rgb/science-games`
Branch: `main`
Verified source checkpoint: `a3115af5df8f5af94d5d194449c8002e602fbb80`
Previous source change: `0468be10f8f76d6bc5ef98a3c32ef1464a145275`
Tree at verification checkpoint: `7fd9e879cdf09693f8dec42cb18937703a11be06`

## Saved work

The source checkpoint contains the rebuilt simple-machines stations, shared ideal-machine physics, evidence-first challenges, quiz outcome reporting, accessibility and layout fixes, and regression tests. The verification commit changes no source files. The live page and service worker were not changed by this release candidate.

A portable owner-review package named `science-games-review.zip` is saved in the user's Library. It contains `preview.html`, `stations.html`, the child-pilot plan, release-check report, and Persian instructions. The preview and station pages were byte-compared with a fresh build of this source checkpoint and matched exactly.

## Verification already completed

The frozen final build passed all 27 release jobs. The recorded outcomes include 132 level runs and 789 full-credit challenges across tracks a–d; complete journeys for grades 0, 2, 3, and 6; endless mode, save/restore, reset, map and lever checks; zero findings in final overlap checks across all four tracks; and reviewed answer-leak flags. Physics model checks: 9,010. Focused machine interaction checks: 15/15. Offline layout checks covered 320×568, 390×844, and 1280×800. Independent review reported no release blocker.

Detailed test results and boundaries are in the Library review package, `RELEASE_CHECKS.md`. Do not rerun the full suite unless source/build inputs change or a specific discrepancy is found.

## Remaining release gates

1. The project owner reviews the science and visuals station by station. The repository's `docs/NEXT.md` explicitly requires this signoff before publishing.
2. After signoff, run `python3 tools/publish_game.py simple-machines physics/simple-machines "کارگاه ماشین‌های ساده"`, commit and push the generated site/service-worker changes, then verify the live version.
3. Run the 10–15 minute child pilot using `CHILD_TEST_PLAN.md`; record observations separately from technical QA. No child pilot or learning-efficacy claim has been completed.

## Resume instructions

Fetch the current `main` before acting and check whether it advanced beyond the checkpoint above. Preserve unrelated or uncommitted local changes. Work only on release-preparation tasks that do not require owner judgment until the owner signoff is available. Do not publish before signoff. If no independent technical task remains, report that the project is ready for owner review and stop at that gate.
