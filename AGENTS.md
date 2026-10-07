# Project-wide development rules

Project orientation: read [START_HERE_FA.md](START_HERE_FA.md) and [the shared project overview](docs/PROJECT_OVERVIEW_FA.md) before making product or architecture assumptions. The overview records intent and a dated snapshot; it does not replace the latest task-specific handoff, component contract, or newer owner instruction. The October 6 harbor bundles have not been integrated into repository source merely by adding this documentation.

Owner decision, 2026-10-02: modularity applies to **every part of this project**, not just route cards. Read [the modularity policy](docs/MODULARITY.md) before changing a component. Keep content/configuration, presentation/assets and behavior separable; preserve stable progress IDs and use versioned migrations for incompatible save changes. Do not perform an unsolicited whole-project rewrite.

For each bounded task, start from `docs/NEXT.md` and the latest checkpoint in `docs/RELEASE_HANDOFF_2026-10-02.md`, then read only the relevant module and contract. `CLAUDE.md` is the working guide; historical handoffs do not override newer owner decisions. Record the change point, smallest example and required checks so another contributor or AI can continue without rereading the full project.

Latest card decision: all visible card text, difficulty emoji/icon and action labels are centered; Persian text remains RTL. The existing preview and game renderer have not yet received this latest all-centered change. Apply it in the next card implementation pass. See `design/cards/copy-contract.json`.

<!-- principles-digest:start -->
## Owner-approved principles digest (full ledger: `docs/PRINCIPLES.md`; read it before any design proposal)

- Readability and an easy UI come first in every conflict (B13).
- Grade bands 1–2, 3–4, 5–6 (B1); a stage's grade band is not fixed (B14).
- Structure: map → land (topic + own theme) → environment → 3 challenges (green/orange/red, each with its own story, card art and scene) → missions as steps inside a challenge (B26, B2, D11). Land theme is a skin only; button/icon positions stay fixed; difficulty colour is a separate fixed badge (D11, D3).
- **Everything layered and modular, graphics included** (T17).
- Every stage teaches or reviews via a lesson card; the card's problem is a schematic of the game situation; card box + spaced practice from grade 1; cards link to stages (B15, B17, B24).
- No stars or accumulating rewards; entering and leaving only by the child's choice (B4, B5). A failed physical try costs nothing; no artificial failure (A8, A9). Every scored question is answerable from what is on screen (A2).
- Child understanding or UX is claimed only from real observation (B9).
- Every external source behind a principle or decision (paper, similar game, other countries' curricula) is logged with full reference, verification level and limits in `docs/DESIGN_EVIDENCE_REFERENCES_FA.md` (R-codes); the final justification report is built from it (E5).
- Items marked «پیشنهاد» in the ledger are proposals, **not decisions**.
- **Process:** when the owner states a rule or decision in chat, record it in the same turn in `docs/PRINCIPLES.md`, `docs/DECISIONS.md` and `docs/STATE.md`, commit and push. Run `python3 tools/check_project_health.py` at session start and end.
<!-- principles-digest:end -->
