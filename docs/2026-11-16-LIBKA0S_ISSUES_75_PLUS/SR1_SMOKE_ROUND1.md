# Addendum: smoke round 1 feedback (2026-11-16)

The owner's first smoke pass after Checkpoint B. Everything not listed here passed. The plan files stay as they
were; this addendum adds items with the ids below, and each is done when a commit whose subject starts `<ID>: `
exists on `feat/2026-11-16-libka0s-75-plus` in its repo.

## Owner feedback, verbatim in substance

1. Skin Tester: Ka0sMedia_Font, Ka0sMedia_Statusbar and AceGUI Dropdown look stock, not like Dropdown and
   WowStyle1DropdownTemplate. "Is this because Ignore settings panel is on?"
2. A tooltip attached below a title-bar mark (the copy window's "Open settings") is illegible: it opens where
   the mouse pointer is. Swap it.
3. The debug console's header buttons have no tooltips. Do a deep pass on all such windows and make sure they
   all have tooltips.
4. All skins: the X's default color does not match the other header buttons; nor does Diagnostics. On hover
   the X goes red, which is fine, but the others only glow, barely perceptibly. Keep the glow and also color
   them with a skin color, for example the color Diagnostics is now. Standardize for ALL windows and all skins.
5. DropWatcher's section headers are too similar to its rows; Skill Master's work well. Standardize across all
   skins.

## Findings and rulings (the lead's, under the owner's standing guidelines)

1. **No change.** The Skin Tester's SavedVariables carry no `skin.ignorePanel`, so the default (on, since
   QFE-ST2) applies, and with it those three samples are deliberately stock (SHOW-28, "(Scope: panel)").
   Clearing General → Skin → Scope → Ignore settings panel skins them. Answered; no item.
2. **SR-L1.** Every attached tooltip (`LibKa0s-Tooltip-1.0` `PlaceAttached`: title-bar marks, HUD drag
   strips, footers, the skin picker's attached sites) opens **above** its control, centered, `TIP_GAP` away,
   and flips **below** only when it does not fit above. The pointer hangs down from its hotspot, so above is the
   side it never covers. Supersedes design §3.6's "chrome below, footer above".
3. **SR-L2 and the addon pass.** Every title-bar control on every window carries a tooltip, including the debug
   console (supersedes R9 C2's "no tooltips on the console"): close ("Close"), settings, Copy, Clear, the
   Debug toggle and the Diagnostics link, the perf, sim, copy and skin-picker windows, the icon browser and a
   HUD strip's marks. Addon-owned windows' title-bar controls get the same pass, addon by addon.
4. **SR-L3 and the addon pass.** Title-bar controls, every window, every skin:
   - **rest:** `icon.tint` for every control, the close X and the Diagnostics link included;
   - **hover:** the existing glow kept, and the control tinted `text.link` (the Diagnostics link's rest
     color today); the close X keeps `close.hot`, red;
   - pinned per skin by tests. State toggles that carry meaning in their color (the console's Debug ON/OFF)
     keep their state colors.
5. **SR-L4 and the DropWatcher/SkillMaster pass.** Cause: Ka0s Default's `list.header.bg` is white at 0.04,
   and LK-84 raised `list.stripe` to 0.08, so a header band is now fainter than a striped row. Skill Master
   paints its own `sm.headerBg` (black 0.35) and reads well. Every skin gets a `list.header.bg` that is told
   apart from the plain row, the stripe and the hover, with contrast floors in `tests/test_skin_defs.lua` as
   LK-82 did; Ka0s Default's value is modelled on Skill Master's band. DropWatcher's group headers (both
   layouts) and Skill Master's block headers paint `list.header.bg`.

## Items

| Id | Repo | What |
|---|---|---|
| SR-L1 | LibKa0s | Attached tooltips above, flip below; every library call site and test |
| SR-L2 | LibKa0s | A tooltip on every library title-bar control, console included; per-window acceptance cases |
| SR-L3 | LibKa0s | Title-bar rest `icon.tint`, hover glow + `text.link`, close hover `close.hot`; every skin pinned |
| SR-L4 | LibKa0s | `list.header.bg` distinct in every skin, contrast floors |
| SR-REL | LibKa0s | v1.105.0 release record amended (unreleased), release battery re-run |
| SR-STD | WowAddonStandards | v2.113.0 (unreleased) wording amended for the four rulings |
| SR-<ABBR> | each addon | Re-copy the re-cut tag; its own title-bar controls (tooltips, colors); DW and SM header bands |
| SR-SMOKE | CommonTasks | The re-smoke sheet, `SR1_SMOKE.md` |
