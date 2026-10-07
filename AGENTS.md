# Project-wide development rules

Project orientation: read [START_HERE_FA.md](START_HERE_FA.md) and [the shared project overview](docs/PROJECT_OVERVIEW_FA.md) before making product or architecture assumptions. The overview records intent and a dated snapshot; it does not replace the latest task-specific handoff, component contract, or newer owner instruction. The October 6 harbor bundles have not been integrated into repository source merely by adding this documentation.

Owner decision, 2026-10-02: modularity applies to **every part of this project**, not just route cards. Read [the modularity policy](docs/MODULARITY.md) before changing a component. Keep content/configuration, presentation/assets and behavior separable; preserve stable progress IDs and use versioned migrations for incompatible save changes. Do not perform an unsolicited whole-project rewrite.

For each bounded task, start from `docs/NEXT.md` and the latest checkpoint in `docs/RELEASE_HANDOFF_2026-10-02.md`, then read only the relevant module and contract. `CLAUDE.md` is the working guide; historical handoffs do not override newer owner decisions. Record the change point, smallest example and required checks so another contributor or AI can continue without rereading the full project.

Latest card decision: all visible card text, difficulty emoji/icon and action labels are centered; Persian text remains RTL. The existing preview and game renderer have not yet received this latest all-centered change. Apply it in the next card implementation pass. See `design/cards/copy-contract.json`.
