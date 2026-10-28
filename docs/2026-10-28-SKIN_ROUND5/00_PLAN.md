# Skin round 5 (2026-10-28)

The owner's fifth round of notes on the nine skins (`inputs/OWNER_NOTES.md`), after the 2026-10-26 skin
feedback run (SF-01..SF-47) was merged. Branch `feat/2026-10-28-skin-round5` in LibKa0s, LootHistory,
LibKa0sSkinTester and this repo. An item is done when a commit whose subject starts `<ID>: ` exists in
the repo that owns it. LibKa0s v1.78.0 is still unpublished (the tag is local), so this round lands in
it: token, face and minor changes are free of any player-facing migration.

## What the notes found, and why

- **Scroll bars.** A skin with `scroll.track` clear (Obsidian, Glass, WoW Forever) or black on a black
  window (High Contrast) draws no corridor. And the knob is two things at once: the client's knob art,
  tinted `scroll.thumb`, and since SF-44 a flat `scroll.thumbFill` laid over its middle in five skins.
  High Contrast tints the art white and fills it yellow, so both show.
- **Corners.** The window's flat edge is the window's own backdrop edge. The title bar and footer are
  child frames, a level above, and reach to within 1px of the window's outside, so where the edge is
  wider than 1px (Azeroth 3, High Contrast 2, WoW Midnight 2) their fills cover it at all four corners.
- **Faces.** Three skins title in Cinzel, an all-capitals face that no body text can share, over a
  different body face; four skins draw in Barlow or Atkinson, which two others also use. Each skin gets
  one family of its own, for body and title alike.
- **The showroom, skin by skin.** Read from the nine screenshots: the paging arrows, the dropdown arrow
  and the sort arrow are yellow in every skin (the client's art is yellow, and a vertex color only
  multiplies it); WoW Forever's check mark is Ka0s gold under a tan accent; High Contrast's larger type
  wraps two of the showroom's skin cards onto a second line; Glass's "On" label reads dim.

## Items

| Id | Repo | What |
|---|---|---|
| R5-01 | LibKa0s | Every skin draws a scroll corridor and one knob. The bar's own knob art is faded and a flat knob in `scroll.thumb` laid in its place, inset to the corridor, moving and showing with the thumb; `scroll.track` is a corridor every skin sets, visibly apart from its window. `scroll.thumbFill` and `scroll.thumbTexture` are retired (unreleased). Contrast cases: corridor against the window, knob against the corridor, in every skin. |
| R5-02 | LibKa0s | The window's edge (and its inner rule) is drawn on a holder above the window's children, so no child band can cover it. Ka0s Default's 1px edge draws where it did. |
| R5-03 | LibKa0s | One face family per skin, body and title alike: Obsidian Inter, Azeroth Alegreya, Glass Nunito, High Contrast Atkinson Hyperlegible, Ember Bitter, WoW Midnight Philosopher, WoW Forever Fira Sans; Ka0s Default and WoW Default keep the client's Friz Quadrata (the one shared face, argued in the report). Barlow and Cinzel leave the payload. `tools/artwork/fonts.py` pins and builds the new faces; the variable ones are instanced as Cinzel was. Sizes retuned per face. |
| R5-04 | LibKa0s | The showroom audit: the in-client arrow art desaturated before it is tinted (PageButton, Dropdown, SortHeaderBar), so it takes the skin's color; WoW Forever's check mark in its tan; a contrast pass over every skin's state, accent and control text, with the fixes it demands. |
| R5-05 | LibKa0sSkinTester | Re-vendor; the skin cards keep their label on one line under any skin's type size. |
| R5-06 | LootHistory | Re-vendor, and the cases the retired tokens or the new faces move. |
| R5-07 | LibKa0s | The release battery and the local v1.78.0 tag re-cut, unpushed. |
| R5-08 | Ka0sAddonsCommonTasks | `99_REPORT.md`: what landed, the owner's smoke checks R5-S1.., the calls made. |

Order: R5-01..04 in LibKa0s, then R5-05 and R5-06 (independent), then R5-07, then R5-08. Feature branches
are pushed at the end of the round; nothing merges, and no tag is pushed, without the owner's go-ahead.
