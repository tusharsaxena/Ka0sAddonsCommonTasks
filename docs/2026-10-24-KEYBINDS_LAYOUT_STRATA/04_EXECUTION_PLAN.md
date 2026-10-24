# Execution plan

Git is the only state: an item is done when a commit whose subject starts `<ID>: ` sits on the run branch in its
repo. Items run through `plan-data/tools/execute_milestone.js`: implement (test first), an independent review that
writes a `refs/notes/ka0s-review` note, and one fix round. Items run serially within a repo and in parallel across
repos. Workflow agents commit locally and never push. The lead pushes at checkpoints.

## M1 — Upstream (23 items)

- **WowAddonStandards v2.88.0** (WS-00…WS-07, WS-90): options-ui-§20 *The Keybindings tab*; the launcher-§6 rewrite
  (per-addon `category="BINDING_HEADER_<FOLDERUPPER>"`, no `header=`, label pattern, `NS.BINDINGS`); the new
  `frame-layering` section with its anti-patterns and pointers (standalone-windows, preview-mode, debug-logging,
  options-ui, events-frames-taint); the strata tooltip rule; the playbook and context-pack ripple; library-stack-§7
  rows; close.
- **LibKa0s v1.77.0** (LK-00…LK-20, LK-90): kit revision 42 (binding mock, frame-layer recorder, Bindings.xml shape
  helper, `Kit.keybindThroughTab`); `OptionsKeybinds.lua` (model, tab, sync); toplevel tool windows that re-raise a
  shown StaticPopup; the DragHandle `level` option; clamped menus; IdList suggestions closing on combat;
  `O.StrataTooltip`; close with the LOCAL annotated tag `v1.77.0`.
- **dev-copilot 2.6.0** (DC-00…DC-02): the WoW review's frame-layering check and Bindings.xml / Keybindings-tab check.

Checkpoint: every item reviewed; each repo's gates green on the run branch; push the three run branches and notes,
but never the tag. Append to `checkpoints.tsv`.

## M2 — Addons, 015 and 030 (37 items)

Per addon: `<PFX>-RV` re-vendors LibKa0s v1.77.0 and the standard v2.88.0 reference; `<PFX>-KB` (7 windowed addons)
covers item 015; `<PFX>-ZS` covers item 030 with the strata changes in `plan-data/accepted.json`.

**Before launch:** export the owner's decisions and run `plan-data/tools/make_accepted.py` (RESUME §3). The ZS items
read `accepted.json`, so a strata change the owner rejected is never made.

Checkpoint: as M1, for the 15 addon repos.

## M3 — Settings layout, item 020 (owner-gated)

Planned after the owner finishes reviewing `preview.html`. It is added as `plan-data/addendum-01.{json,tsv}`: the
upstream layout rules the review keeps (the `U-*` rows on the page), a LibKa0s re-tag if those need library surface
(an `RV2` per addon), and one `<PFX>-LY` item per addon that applies exactly the `layout` ids in `accepted.json`.
**No layout code changes before the owner says the review is done.**

## M4 — Record and finalize

CT-01 is the lead's record. **CT-02 happens only on the owner's explicit merge go-ahead**: finalize every repo in
dependency order, push the v1.77.0 tag, and delete every branch, stash and worktree this run created.
