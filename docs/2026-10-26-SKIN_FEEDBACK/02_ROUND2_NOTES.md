# Addendum: the owner's second round (2026-10-26)

Added during execution, after round 1 was pushed. The owner, on the showroom in all nine skins: "Much
better now!", then:

> 1. Azeroth: still too bright, step the bright foreground down a notch again. Text visibility is better but
>    still not great; maybe explore a different font (examples: the search box hint and the sort header).
> 2. WoW Default: I don't like the border around buttons; make it more original WoW like.
> 3. Ember, Obsidian, High Contrast, WoW Forever: the button primary text looks off; experiment with a
>    different color.
> 4. High Contrast: the selected tab's text looks off, like #3.
> 5. Slider: make it consistent across all skins, Ka0s Default the reference, each in its own colors.
> 6. Button (primary): across all skins, a primary differs from a normal button (good: Forever, High
>    Contrast, Glass, Obsidian; bad: Ka0s Default, Azeroth, WoW Default).

## Findings and fixes

| Id | Note | Finding | Fix |
|---|---|---|---|
| SF-16 | 1 | Both examples were strings a primitive only tinted (an EditBox hint, a sort header), so they kept the client's font and its dark shadow, smeared on parchment. | Parchment `#C9B88F`; the body in Atkinson Hyperlegible (designed for legibility); the grays and semantic inks darkened to 3:1, which the contrast cases demanded (`#7A6A50` read 2.7). The face fix is SF-22. |
| SF-17 | 2 | The 2px `bevelOut` gold edge. | The client's thin dark rim (`#1A0805`). |
| SF-18 | 3 | Dark text on a bright fill, under a black drop shadow. | Obsidian `#2A86D1` with white text; Ember white text; Forever `#9C7A58` with white text; High Contrast yellow on black. SF-22 also drops the shadow from any dark label. |
| SF-19 | 4 | The same: black on yellow. | Yellow on black, the yellow underline kept. |
| SF-20 | 5 | The primitive filled the whole slider frame with the track color and boxed it; Ka0s Default's (host-drawn) is a thin bar. | SkinPaintControls 3: a 4px bar centered in the slider, no box in any skin; each skin colors bar, fill and thumb (High Contrast's bar white, WoW Default's fill gold). |
| SF-21 | 6 | Ka0s Default's primary tokens were its normal button's; Azeroth's and WoW Default's primaries were their normal red. | Ka0s Default's primary is gold; Azeroth's normal buttons are leather with cream text, the wax red left to the primary; WoW Default's primary is a brighter red under a thin gold edge with white text. A case holds every skin's primary apart from its normal button. |
| SF-22 | 1, 3, 4 | (as above) | SkinPaint 5: `P.label` gives every string a primitive colors the skin's face; a dark label (luminance under .3) takes a shadowless font object. |
| SF-23 | | | LootHistory re-vendor. |
| SF-24 | | | LibKa0sSkinTester re-vendor. |
