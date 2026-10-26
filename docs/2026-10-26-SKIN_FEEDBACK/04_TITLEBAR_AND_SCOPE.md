# Addendum: the title-bar probe and the Scope (2026-10-27)

Added during execution, after round 4 was pushed.

## The title-bar probe (SF-35 to SF-37)

Round 4 left one open: on Azeroth, Loot History's title bar showed the window's fill instead of
`title.bg`. The owner ran three in-client probe lines:

```
LH win 1 bar 2 kids 2
LH kid 1 1 true BACKGROUND 1 1
LH kid 2 3 true OVERLAY 1 0.96...
LH win tex 4..11 BORDER 130871 1
LH win tex 12 BACKGROUND 130871 1
LH win tex 13 BACKGROUND nil 1
```

The window is at frame level 1 and its plain title bar at 2. The bar's fill holder, one level below
the bar, sits at 1, level with the window and its BACKGROUND backdrop. The client may draw either of
two frames at one level first, so the window's fill covered the bar's.

| Id | Repo | Fix |
|---|---|---|
| SF-35 | LibKa0s | A fill or wash is a region of its own target at the bottom sublevels of BACKGROUND (`P.SUB`, through `P.subTex`), no longer on a frame one level down. This covers the extras' fills and gradients, ListRow's washes, and Strip and Cover. A target always draws after its parent. `P.subTex` sets the alpha back to 1 on every paint, because EllesmereUI fades every direct region of a frame it skins. SkinPaint 7, SkinPaintControls 5, SkinPaintExtras 3. Two new cases (the probe's layout, the alpha reset), each mutation-checked. |
| SF-36 | LootHistory | Re-vendor. |
| SF-37 | LibKa0sSkinTester | Re-vendor. Its bar is a backdrop frame and was never affected. |

## The Scope (SF-38 to SF-40)

The owner, on the Appearance tab:

> I had asked you for a feature earlier: 1. ignore settings panel from skinning behavior, 2. ignore
> fonts from skinning behavior. Both separate toggles in the appearance tab, a separate section below
> the skin selector, together with the copy to every Ka0s addon button:
> [Ignore settings panel] [Ignore fonts]
> [Copy to every Ka0s addon]

The 2026-10-26 plan had deferred this as "the scope and font settings".

| Id | Repo | What |
|---|---|---|
| SF-38 | LibKa0s | Skin minor 5: `GetIgnore` / `SetIgnore(owner, panel, fonts)`, live (repaint and listeners). `SetIgnore` answers `reload` when the panel exception turns on after the panel was painted this session. `WriteChoice` takes a third argument. SkinPaint 8: `P.font` hands a string back its own face while fonts are ignored. SkinAce 3 and OptionsScroll 7: no AceGUI row and no chrome painted while the panel is ignored; the Options listener is installed from the ungated facade. OptionsAppearance 2: the **Scope** section between the skins and the copy button, and the copy carries it. Found on the way: `paintPage` kept a self-answering `CreateTexture` stub as the page's backdrop, so a looks change showed the page. Client textures are real, so players never saw it; the fix is P.tex's own guard. Eight new cases, each gate mutation-checked. |
| SF-39 | LootHistory | `settings.appearance.ignorePanel` / `.ignoreFonts` (default false, two skipRender rows), the write and apply seams, profile events, the degraded stub, the moved pins, and four host cases. |
| SF-40 | LibKa0sSkinTester | `skin.ignorePanel` / `skin.ignoreFonts`, the same seams, one host case. |

My calls, stated so they can be overturned:

- **The section's heading is "Scope"**, and the check boxes say "Ignore settings panel" and "Ignore
  fonts", the owner's words.
- **Ignore settings panel needs a reload to turn on** once the panel was skinned that session: the
  page chrome cannot be handed back in place. Turning it off is live, and Ignore fonts is live both ways.
- **Ignore fonts keeps the skin's colors**, because only the face, size and shadow come from the fonts.
- **Copy to every Ka0s addon copies the Scope** along with the source and skin, and its confirmation
  says so.
