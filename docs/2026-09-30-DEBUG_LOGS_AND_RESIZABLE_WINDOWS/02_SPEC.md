# Spec

Branch in every touched repo: `feat/2026-09-30-debug-logs-and-resize`. Every repo's own `CLAUDE.md`
governs work inside it (green gate, standards compliance, line endings, never bump an addon's version).

## S1 — WowAddonStandards v2.70.0 (DL-STD-01)

The standard is changed first so every addon lands against the same words. Follow the repo's own
change ripple (section, index blurb in `standards/STANDARDS.md`, anti-pattern range, changelog, version
bump, `NEW_ADDON_CONTEXT.md` context pack, playbooks that cite the changed text).

1. **debug-logging-§8, a diagnosis checklist (MUST).** After the existing bullets, add "**Diagnosis** —
   what a support read of the log needs, beyond the flows above", covering, where the addon has them:
   - **State edges** the addon reacts to: combat in/out, addon-restriction / secret-value state
     (`ADDON_RESTRICTION_STATE_CHANGED`), loading screens / zone and instance changes, group roster
     changes, spec changes, and the addon's own enable/stand-down transitions. One line per edge, with
     the state the addon took from it.
   - **Deferred work**: when work is held (why: combat, secret, lockdown, not loaded) and when it is
     flushed (how much). A held-then-never-flushed state must be visible.
   - **Refusals and no-ops with the reason**: a command refused, a write rejected, an event ignored
     because a guard said no — the line names the guard.
   - **Dependencies**: optional libraries or companion addons found or missing, once at enable.
   - **Errors caught** by a `pcall` the addon owns: the site and the message, once per distinct error.
   Coverage stays judged by "could I reconstruct what happened", and still one gated line per event.
2. **debug-logging-§9, quiet steady state (MUST NOT).** A repeating path — a timer, an OnUpdate, a
   ticker, an event that fires many times a second in combat — **MUST NOT** log when nothing it reports
   has changed. It logs on change of its own summary (compare the built summary with the last one
   logged, behind the gate), or at most once per stated interval with a count. The console's repeat
   folding (`(xN)`) does not satisfy this: a folded pair every few seconds for a whole dungeon still
   evicts the lines that matter from the 3000-line buffer. A per-pass line whose content changes each
   pass (a real recompute) stays compliant under the existing §9.
3. **debug-logging-§1, "What the library guarantees".** "700 × 344" becomes "700 × 344 by default,
   resizable from a bottom-right grip down to a minimum that keeps the title bar's controls clear, the
   size kept on the window for the session only (never saved; a /reload restores the default)". Add the
   same guarantee for the console's copy window and every `Widgets.CopyWindow` (both axes), and to
   performance-§4's step panel (width only: its row count is fixed). An addon **MUST NOT** save these
   sizes (they are the library's session state, not named non-setting state the addon owns).
4. **anti-patterns**: one entry for "a steady-state repeating path that logs every pass" with the
   MultiMeters shape as the measured case (a folded Aggregator/Render pair every ~10 s through a key).
5. **Version** v2.70.0, changelog entry, `NEW_ADDON_CONTEXT.md` refreshed. Grep `../wow-addon` for
   citations of the changed text (e.g. "700 × 344"); report any (do not edit that repo).

## S2 — LibKa0s v1.64.0 (DL-LIB-01)

1. **One shared helper** for all three windows, additive and guarded: a Core function (suggested
   `Core.MakeResizable(frame, opts)`) with no Core floor raise — each caller checks it exists and
   degrades to today's fixed window if not (docs/releasing.md: a floor raise is a vendoring break).
   - A bottom-right grip in the collection's skin (the stock chat size-grabber art is fine), always
     shown, above the window's content.
   - `SetResizable(true)` and `SetResizeBounds(minW, minH, maxW, maxH)` through a Compat-style guard.
     Max defaults to the UIParent size. `opts.widthOnly` pins min/max height to the current height.
   - Mouse down on the grip → `StartSizing("BOTTOMRIGHT")`; mouse up → `StopMovingOrSizing()`, then
     `opts.onResize(w, h)`. Relayout also runs from `OnSizeChanged`.
   - **Session only.** The size lives on the frame (the frames are built once and kept), so it survives
     hide/show and a /reload rebuilds at the default. Nothing opens or reapplies the default size on a
     later show. The client's layout cache must not carry the size across a /reload: after
     `StopMovingOrSizing`, handle `SetUserPlaced` so the size is not restored, **without changing how the
     window's position behaves today** (check what today's drag does and keep it).
2. **Debug console** (`DebugLog.lua`): both axes, default 700 × 344, minimum width computed from the
   title-bar arithmetic (every control plus the title fits), minimum height enough for the title bar,
   status bar and a few lines. On resize: the message frame reflows (it is anchored), the scrollbar
   thumb and line counter resync, the title-bar controls stay placed. Buffer and scroll position kept.
3. **Copy windows** (`Widgets.CopyWindow`, used by the console's Copy and hosts' exports): both axes;
   the descriptor's `width`/`height` stay the defaults; the edit box width tracks the scroll frame on
   resize; each named copy window has its own size.
4. **Perf panel** (`PerfPanel.lua`): width only; the step rows anchor to both edges and stretch; the
   minimum is today's width.
5. **Test kit** (revision 33): mock frames gain `SetResizable`, `IsResizable`, `SetResizeBounds`,
   `GetResizeBounds`, `StartSizing`, `SetUserPlaced`/`IsUserPlaced` as recorders, and `SetSize`/
   `SetWidth`/`SetHeight` fire `OnSizeChanged` when a script is set — only if the kit does not already.
   Fidelity rules of the kit apply (model the client, raise where the client raises).
6. **Tests**: default size unchanged for each window; the grip exists; bounds set (width-only for the
   panel); a resize reflows (console scrollbar/counter, copy edit box width, panel rows); the size
   survives hide/show; two hosts' consoles resize independently; the helper absent → today's window.
7. **Docs**: `docs/api/` for each touched major, CHANGELOG v1.64.0, bump the touched minors, local
   **annotated tag v1.64.0** on the release commit. The tag is **not pushed**.

## S3 — Re-vendor in each addon (DL-<XX>-01)

1. Copy `LibKa0s/` and `testkit/` from the local tag `v1.64.0` into `libs/LibKa0s/` and `tests/_kit/`
   (`git -C ../LibKa0s archive v1.64.0 ...`; whole folders, never a subset). Roll the `CLAUDE.md`
   provenance line to v1.64.0 in the same commit.
2. Refresh the standards reference to v2.70.0 in the three places (TOC `X-Standard`, README badge,
   `CLAUDE.md` "Standards compliance"), as `/wow-addon:revendor-standards` does.
3. Fix any fallout the new kit revision exposes (tests only; no behavior change here). Adopt nothing
   else from the delta.
4. `docs/smoke-tests.md`: add to its debug-console theme the resize checks (console, copy window, perf
   panel if the addon ships one): grip resizes, minimum holds, size kept on close/reopen, default back
   after /reload, another addon's console unaffected. Keep the doc's evergreen shape.
5. Gate green, commit `DL-<XX>-01: ...`.

## S4 — 060 debug coverage in each addon (DL-<XX>-02)

1. **Inventory** (read-only first): every event the addon registers, every state edge it reacts to,
   every deferral/queue and its flush, every refusal/guard, every data mutation, the settings seam, every
   slash verb, every repeating path (timers, OnUpdate, tickers, high-frequency events), and every
   existing `NS.Debug` call with its tag.
2. **Gap list** against debug-logging §8 (flows + the new diagnosis checklist) and §9 (coalescing + the
   new quiet steady state). Judge by "could a support read of the log reconstruct what happened".
3. **Fill and fix**: add the missing lines (one gated line per event, existing tag vocabulary, the
   string-building behind the gate); silence or change-gate every steady-state repeating path. Do not
   remove a line that carries information a diagnosis needs; do not add per-item lines.
4. **Tests**: pin the new lines that matter (a red-under comment naming what breaks without them) and
   one quiet-steady-state test per repeating path fixed (N passes with no change → no new lines).
5. **Docs**: `docs/debug.md` gains (or updates) a "Coverage" section listing each tag, what emits it and
   when; the file-level coverage map of the audit goes to this bundle's `coverage-maps/<Addon>.md`
   (the addon agent writes it and does **not** commit it; the orchestrator commits the maps at M3).
6. Gate green, commit `DL-<XX>-02: ...`.

## Judgment calls (D6)

| # | Call | Why |
|---|---|---|
| J1 | Perf panel resizes width only | Fixed row count; extra height is empty space. |
| J2 | No "reset size" control | A /reload resets it (D3); one more button is YAGNI. |
| J3 | The helper lives in Core, guarded, no floor raise | All three windows reach Core; a floor raise breaks stale vendors. |
| J4 | The standard forbids saving these sizes | Owner asked for session-only; saying so stops an addon persisting them later. |
| J5 | Quiet steady state is change-gated, not time-throttled, by default | A change-gated line carries every real change and nothing else; a throttle may drop one. Time-throttle stays allowed with a count. |
| J6 | Re-vendor and 060 are separate items per addon | The mechanical vendor lands and is reviewed before the judgment-heavy audit. |
