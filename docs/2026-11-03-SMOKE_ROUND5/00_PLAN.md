# Smoke round 5: plan (2026-11-03)

Inputs: `inputs/OWNER_FEEDBACK.md` (items 1 to 7, images 31 to 56), `inputs/OWNER_ANSWERS.md`, and
`inputs/INVESTIGATION.md` (read-only workflow wf_d3235619-e06, each topic challenged by a skeptic; where a skeptic
corrected the investigator, the skeptic wins). Header shade signed off from `R5_MOCKUP.html`: **C**.

Branch `feat/2026-11-01-full-skinning` in every repo (still unmerged). Outfitter is never touched. LibKa0s v1.85.0 is
re-cut locally and never pushed without the go-ahead.

## Lead's calls

1. **Item 1, header:** Ka0s Default only, option C: `title.bgTop` #262006, `title.bgBottom` #141103, `title.bg` (flat
   blend) #1D1805, picker swatch 2 #1d1805. MultiMeters' `SKIN_FALLBACK["title.bg"]` moves with it. Other skins
   unchanged.
2. **Item 2, window geometry like LootHistory:** the header band sits flush inside the window edge, at Shell's own
   inset (the flat edge's `win.borderSize`, else 1), at `title.height` (30). Content keeps its 6 px inset, as
   LootHistory's table does. No strip of body colour between the edge and the band, in any window of any addon.
   - MultiMeters: the meter's header strip moves to that geometry with the title gradient. A custom header colour uses the
     same geometry, drawn flat. A collapsed meter is exactly the band plus its edges. The meter's row unit icons stay
     HUD (black edge, round 4 ruling).
3. **Item 3, DpsRace header:** the fix goes in the library at the root cause. Shell's top band draws above a backdrop
   window's own fill, in the BACKGROUND layer with a sublevel above the backdrop Center; the bottom bar is unchanged.
   - This gives the band to all four DpsRace windows and to every library window: the debug console, the copy window,
     the perf panel, the sim panels and the skin picker.
   - Toasts opt out with `noTopBar`.
   - Popovers get the full band, with the title and close button centred on it: DropWatcher's offer panel, note
     editor and detail card, and the QuickComms modal.
   - Hosts that paint Shell twice keep exactly one band.
4. **Item 3a:** the DpsRace HUD title is left-aligned in every skin. The Results, Timeline and Gear titles follow the
   skin's `title.align`.
5. **Item 4, QuickComms:** the item is the pad window (images 40 and 41), not the radial dial. Its header gets the
   library title band (gradient), on its own header tokens. The text stays left-aligned, because the pad is compact
   and shares its row with chips and the collapse button. Section rows ("Solo") draw no band in any skin, so the header
   is the only band. The header is a borderless band, as in LootHistory, in every skin including WoW Default. When the
   pad grows upward, the band sits at the bottom with the same gradient direction.
6. **Item 5, vertical centring:** every header child (title, close, header buttons, chevrons, badges) is anchored
   LEFT, CENTER or RIGHT to the band's own frame at y = 0, in every window and every skin. Centring is on the band's
   geometric middle, with no per-font nudges unless smoke shows a face visibly off. Under the EllesmereUI source,
   header children centre on its 25 px bar.
7. **Item 6, dropdowns:**
   - The skin picker's list gets its own outside-press listener. This covers the /st window, the settings-page picker
     and the SkinNotice picker.
   - A press on the picker's own body, title, eye or gear also closes the list, and the button's own click still runs.
   - Two open pickers close independently.
   - Escape is unchanged: it closes the window.
   - Every other custom Ka0s pullout in the library and in all 16 addons that the round 4 R4-L1 watcher misses gets
     the same behaviour.
8. **Item 6b, /dr sim:**
   - A bare `/dr sim` opens the idle panel like MultiMeters': the scenario dropdown, a Start button, and the steps
     previewed, with nothing run yet.
   - `/dr sim <scenario>` starts that scenario at once.
   - The sample race is an imaginary 15 s race played in real time, so the countdown ticks real seconds (owner's
     answer). After the buzzer, everything also plays at real speed, and the result card holds for 4 s before the
     Results window opens.
   - The sim's sample history stays consistent with a 0:15 board, so "Your best" and the toast still demonstrate.
   - MultiMeters' sim is unchanged.
9. **Item 7, icons:** the rule, to be recorded in LibKa0s `docs/api`:
   - Every Blizzard icon art is cropped by at least 0.07 per side.
   - In a window, and on settings pages, it gets a 1 px edge in `icon.outline`.
   - On the HUD and on toasts, including DropWatcher's toast, it gets a 1 px edge in `icon.border`
     (`S.IconBorder{hud=true}`).
   - Icons that stand alone in a window are rebuilt as framed textures. This covers DpsRace's Used column, Usage list
     and spec and class icons, and DropWatcher's cards, which move from `icon.border` to `icon.outline`.
   - Inline `|T` icons in tooltips and chat are cropped only (5:59 of 64).
   - Atlas glyphs, Ka0s catalog marks and round art are exempt.
   - DropWatcher's optional quality border is untouched.

## Milestones

- **M1, LibKa0s:**
  - R5-L1: the header shade.
  - R5-L2: the band above the backdrop fill, the toast opt-out, and library windows getting the band.
  - R5-L3: the band frame and header centring.
  - R5-L4: outside-press close for the picker list and library pullouts.
  - R5-L5: library-drawn icons cropped and edged.
  - An independent review, then R5-REL re-cuts v1.85.0 locally.
- **M2, the 16 addons, each followed by an independent review:**
  - R5-RV: re-vendor.
  - R5-WIN: the item 2 and item 5 sweep, per addon.
  - R5-DD: host pullouts.
  - R5-ICON: icons.
  - Plus R5-MM1 (MultiMeters), R5-DR1 (DpsRace header and 3a), R5-DR2 (DpsRace sim), R5-QC1 (QuickComms) and
    R5-PG1 (PGFE).
- **M3:** R5-GATE writes `06_SMOKE_TESTS.md` and `99_REPORT.md`, adds the checkpoint rows and pushes 18 repos (no
  tag, no Outfitter).

Then the owner runs the smoke tests and gives the go-ahead. After that: `/dev-copilot:finalize`, push the tag, close
LibKa0s #71 and #72 spaced apart, and clean up branches, stashes and worktrees.
