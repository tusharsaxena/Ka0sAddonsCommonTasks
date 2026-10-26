# Addendum: the owner's notes on the showroom (2026-10-26)

Added during execution, after SF-01..SF-05 were committed and before the re-vendor. The owner took the
Skin Tester's showroom in all nine skins (on the pre-fix v1.78.0) and asked, beyond the five notes in
`00_PLAN.md`:

> 1. Make all the font sizes relatively similar, so it doesn't break the layouts of any of the addons
>    (ok if not exactly the same, but similar). Use Ka0s default as the reference.
> 2. Make the "A row, hover" a bit more visually distinct; in almost all cases it's hard to distinguish.
> 3. Any other inconsistencies you can find from examining the screenshots.

then, mid-run: WoW Default's checkboxes draw a checkbox inside a checkbox; Ka0s Default's checkboxes should be
more square, like WoW Forever's but in the Ka0s Default style; and **every skin sets a size, Ka0s Default
included**.

## Items

| Id | Repo | Finding | Fix |
|---|---|---|---|
| SF-10 | LibKa0s | The owner's font object was one per role, set to one absolute size, so under any skin with a size every string of a role took it: captions grew to body size (High Contrast's ran into each other) and the Cinzel title lines ran into the next column. | SkinPaint minor 4: sizes are relative. Every skin sets `font.bodySize` and `font.titleSize`; Ka0s Default's (12, 14) are the reference, and a string takes its stock size times the skin's over the reference. One font object per role and size. Each skin is tuned to its face, within 1.5pt of the reference. |
| SF-11 | LibKa0s | The hover wash was the accent at .10 and the selection the accent at .14-.24: one hue, nearly one alpha. | `list.hover` is the skin's body text at .10. Ka0s Default keeps its gold hover. |
| SF-12 | LibKa0s | "Button (disabled)" looked exactly like "Button" in every skin. | SkinPaintControls minor 2: a disabled button's label reads `text.disabled`, follows OnEnable / OnDisable, and takes no hover color. |
| SF-13 | LibKa0s | WoW Default drew a 2px bevel box round `UI-CheckBox-Up`, itself a box. Ka0s Default left the client's round check button. | WoW Default's check edge is none. Checkbox paints under Ka0s Default too: a square box in the control fill under a 1px control line, with the gold mark. |
| SF-14 | LibKa0s | WoW Forever's primary button differed from a normal one only by its edge. | Filled with the tan accent, dark text. |
| SF-15 | LibKa0sSkinTester | The Slider sample was invisible under Ka0s Default: blank textures, which a skin with no slider token leaves as drawn. | Drawn the way a host draws a slider: white textures in a host's tints. |

Checked and left alone: WhiteButtonLabel reads gold in Azeroth, WoW Default and WoW Midnight. That is its
contract (`btn.text`), not a fault.
