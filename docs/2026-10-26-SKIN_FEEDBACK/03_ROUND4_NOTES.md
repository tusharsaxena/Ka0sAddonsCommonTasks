# Addendum: the owner's fourth round (2026-10-26)

Added during execution, after round 3 was pushed and after the owner stopped the merge. The owner, on
Loot History and the showroom:

> 1. Azeroth: the light background is not going to work; I need a much darker background. Rework this.
> 2. "Ka0s Default sets no font" ... It should set a font. This is the second instance where I have seen
>    Ka0s Default fall back to what the game defines. This is not what I want at all. Make sure even Ka0s
>    Default has a setting for everything. Audit all such things in Ka0s Default and all other skins.
> 3. WoW Forever: the font looks a bit blurry, replace it. The background can be a tad browner and less
>    black, not too much.

The round overturns a reading the run had held since round 1: that Ka0s Default sets no face and leaves the
client's look wherever it has no value. The owner rejected it.

## The audit

Ka0s Default left **53 tokens** nil. Faces and sizes (`font.body`, `font.title`, `font.mono`, the outline
and the shadow); the title and footer bands and `title.align`; the input text and placeholder; the slider's
track, fill and thumb; the tab, nav, popup and tooltip edges and fills; the list header band and selection;
the bar and icon edges; the glow; the eight `q.*` quality colors; every gradient stop and art token.

The engine special-cased it in about fifteen places (SkinPaint's `stockDefault` / `isDefault` branches in
Shell, FadeRegions, FadeNineSlice and the TitleBar fill; SkinPaintControls' ScrollBar; SkinAce's pull-out,
restore and early return). The other eight skins set none only where the absence is the design: no
inner rule, no gloss, no gradient stop.

## Items

| Id | Repo | Fix |
|---|---|---|
| SF-30 | LibKa0s | Every Ka0s Default token has a value (SkinDefs minor 8): Friz Quadrata by name for body and title, JetBrains Mono, the client's quality colors written out, the bands, edges and fills the client draws, or `false` (the explicit none) for a decoration it does not draw. No primitive branches on Ka0s Default (SkinPaint minor 6, SkinPaintControls minor 4, SkinAce minor 2): its stock art is faded and its window, scroll thumb and AceGUI rows painted from tokens like every skin. `P.isDefault` stays, answering false, for Options' `__chromeAway`. Skin key 4.7.5.2.3.1.1 -> 4.8.6.2.4.1.2. |
| SF-31 | LibKa0s | Azeroth reworked dark: tooled leather `#2B1D12` under a `#6b4a22` edge, parchment text `#E9DDBC`, gold `#E2B659`, the red wax seal on the primary button and the selected tab. Its light-skin inks are gone; it takes Ka0s Default's semantic, quality, tooltip and chart colors. |
| SF-32 | LibKa0s | WoW Forever: Atkinson Hyperlegible (Barlow read blurry), and the charcoal a step browner (`#2e251c` to `#18120d`). |
| SF-33 | LootHistory | Re-vendor, and the pins that held the old rule: the Insights golden regenerated (41 lines, quality-bar colors only, Common stays white); the switch cases switch to a test-only skin (`tests/skin_support.lua`), because no shipped skin moves every token they compare now; the settings cases expect Ka0s Default to paint. Two test-isolation fixes the new payload exposed: the settings canvases start hidden after boot, as in the client, and the stand-down suite closes the pages an earlier suite left open deterministically (a snapshot, then one re-sync). |
| SF-34 | LibKa0sSkinTester | Re-vendor. |
| SF-06 | LibKa0s | The release battery and the local v1.78.0 tag re-cut, again unpushed. |

## Still open from this round

- **Azeroth's title bar in Loot History** showed the window's fill instead of the bar's. The working theory
  is a frame-level tie: Loot History's bar is a plain Frame, so its fill goes on a holder one level down,
  which is the window's own level. The owner's in-client probe will confirm or rule it out. The showroom's
  bar is a backdrop frame and is painted directly.
