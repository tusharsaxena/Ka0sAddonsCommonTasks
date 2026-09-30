# In-game checks (owner)

What only the client can confirm. The headless kit does not fire `OnSizeChanged` from `SetSize`, so the
relayout on a real drag is proven here, not in the suites. Each addon's own `docs/smoke-tests.md` carries
its detailed rows (the resize rows DL-<XX>-01 added and the debug rows DL-<XX>-02 added).

## 090: resizable windows (do in two addons at once, e.g. AuraMaster and MultiMeters)

1. Open the debug console (`/<prefix> debug`). It opens at the usual size (700 × 344). A grip shows in the
   bottom-right corner.
2. Drag the grip larger, then smaller. The log reflows; the scrollbar and the line counter follow; the
   title-bar buttons never overlap; it will not shrink below a size that keeps them clear.
3. Close the console and reopen it: the new size is kept.
4. Resize the second addon's console: the first addon's console keeps its own size.
5. Press Copy: the copy window opens at its usual size and resizes the same way; the text box follows the
   width. Close and reopen: kept.
6. In an addon with the perf harness (AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, MultiMeters):
   `/<prefix> perf` and resize the step panel. Only the width changes; the rows stretch.
7. `/reload`. Every window is back at its default size. **Also note the position**: a dragged window may
   come back where you left it (the client's layout cache, see the LibKa0s v1.64.0 CHANGELOG). The size
   must not come back. Report either surprise.

## 060: debug logs (with `/<prefix> debug on`)

1. **MultiMeters through a key**: the console stays quiet between pulls and through a long pull while
   nothing changes. No `(x41)` Aggregator/Render pairs every ten seconds.
2. **Combat and restriction edges** in any addon: entering and leaving combat, and a key start
   (restriction on), each leave one line naming the edge and what the addon did.
3. **Held work**: change a setting in combat in AuraMaster (or toggle a Blizzard frame); a "held" line
   appears, and after combat a single "applied after combat" line.
4. **Refusals**: a refused command (for example a verb while the addon is disabled, where the addon can
   see it, or an unknown value) leaves a line naming why.
5. **[Init] with logging turned on** shows the summary, and names missing optional libraries or a
   stood-down state when there is one.
6. Leave logging on through a normal session and check the log is still readable: no per-item lines on
   bag or roster updates.
