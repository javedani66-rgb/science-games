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
