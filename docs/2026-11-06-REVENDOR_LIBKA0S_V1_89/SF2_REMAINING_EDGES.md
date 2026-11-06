# SF2: the three remaining one-UI-unit lines (2026-11-06)

The SF1-L1 review left three Widgets lines on the old one-UI-unit size: the shared menu's divider
rule (`Widgets.lua:329-331`), the ReorderList row boxes (`WidgetsReorder.lua:367`,
`ROW_BOX.EDGE_SIZE = 1`) and the DragHandle strips (`WidgetsDragHandle.lua:694`,
`dhDrawEdge(handle, 1, ...)`). The owner reported SM-01..SM-11 passed in game, then asked for these
three fixed as well, before the finalize.

- **SF2-L1** (LibKa0s): all three are drawn one physical pixel wide through Core minor 16's
  `__PixelSize` / `__WatchPixels`, the same mechanism SF1-L1 uses, and each moved file's minor is
  bumped. The v1.90.0 release notes and API documents are corrected to match.
- **SF2-L2** (LibKa0s): v1.90.0 has never been pushed, so it is **refreshed**. The local tag moves to
  the new tip, following the skill's *A tag that moved before it was pushed* case. It is still not
  pushed until the finalize.
- **SF2-RV-<X>** (all 17 addons): each re-copies v1.90.0, re-prunes and re-gates, and adds
  `docs/revendor/2026-11-06-v1.90.0/06_REFRESH_1.md` (the old and new tag commits, the per-file minor
  delta and the gate figures). Line 1 of `01_DELTA.md` is left alone.
- Smoke **SM-12**: menu dividers, ReorderList rows and drag-handle strips are crisp at 1 px.
