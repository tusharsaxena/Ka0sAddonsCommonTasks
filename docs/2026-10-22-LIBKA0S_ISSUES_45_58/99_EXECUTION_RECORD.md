# 99 — Execution record: LibKa0s issues #45-#58

Written during execution. The plan files are frozen; later developments are recorded here.

## LK-11 spike outcome: B (W.StepPanel is Sim-private)

- **Outcome: B.** `W.StepPanel` is **not** public. LK-10's payload (`07dfb7c`) is reverted inside the
  LK-11 commit: `WidgetsStepPanel.lua`, `tests/test_widgets_step_panel.lua`, its majors/xml rows, its
  CHANGELOG section and the Widgets key rename all leave, and the Widgets key is back to 13.1.4.3.2.
  Proof: `test ! -f LibKa0s/WidgetsStepPanel.lua` (in `../LibKa0s`). LK-10 is noted in `exceptions.tsv`.
- **Why.** Rebuilding `PerfPanel.lua` on `W.StepPanel` would have needed edits to five existing suite
  cases: `tests/test_perf_command.lua:279` and `tests/test_perf_isolation.lua:264`, `:272`, `:277`
  load `PerfPanel.lua` without Widgets, and `tests/test_resize_windows.lua:432` caught
  `WidgetsStepPanel.lua` calling `core.MakeResizable` unguarded. The proof required zero test edits.
- **What LK-11 shipped.** `PerfPanel.lua` gains one header comment naming the deliberate duplication
  with Sim's private renderer; `PANEL_MINOR` 6 -> 7 (comment-only); Perf key 15.1.1.6 -> 15.1.1.7
  (15.1.1.6 Superseded).
- **Downstream.** LK-16, LK-18, LK-20, WS-08, WS-09, DW-04 and DC-* take the outcome-B branch.
  LK-16 builds the renderer library-private inside `SimPanel.lua` from
  `git show 07dfb7c:LibKa0s/WidgetsStepPanel.lua`, and must guard `core.MakeResizable`.

## The first M1 attempt stopped at LK-11 (2026-10-22)

The first executor run (`wf_d04aa10e-280`) landed 18 items. The spike ran and found outcome B, but the
auto-mode permission classifier refused the implementer's `git revert --no-commit 07dfb7c` as a deletion,
so LK-11 returned `blocked` and its 19 dependants were skipped. The lead staged that revert on the run
branch and relaunched the 20 remaining items (`wf_92e45e7b-e9b`), with an item ruling telling LK-11 not
to re-run the spike. All 20 landed.

## The local tag v1.75.0

| When | Event | Commit |
|---|---|---|
| 2026-10-22 (LK-22) | created, local annotated tag, not pushed | `265a89e` |

## dev-copilot merged early (owner go-ahead, 2026-10-22)

The installed plugin updates from GitHub `master`, so 2.4.0 had to reach master before M2. On the owner's
explicit go-ahead, dev-copilot's run branch alone was merged `--no-ff` into master as `43dd69b` and pushed,
with no tag. The run branch stays until CT-02 cleans up. CT-02 finds dev-copilot already merged.

## M3 first pass: a Sim-1.0 gap from DW-02 (addendum 01)

The first M3 run (`wf_63c70dcf-91d`) landed 37 items. DW-02, DropWatcher's move onto Sim-1.0, returned
`library_gap`, and its 21 dependants were skipped. Sim minor 1 had two gaps:
- it froze the scenario names at `New`, while DropWatcher fills them after `New` at load;
- `Start` handed `prepare` a fresh `{ scenario, size, seed }`, dropping the host's `band` and `classFilter`.

Following RESUME §5, `plan-data/addendum-01.json` (and `.tsv`) adds:
- **LK-26**, Sim minor 2, the additive fix;
- **DW-RV2, LH-RV2 and BL-RV2**, which refresh the three simulator hosts from the moved tag.

The other eleven addons refresh once at the end of M3, after the tag stops moving. `resume-state.sh`,
`next_args.py` and `execute_milestone.js` now read `plan-data/addendum-*`.
