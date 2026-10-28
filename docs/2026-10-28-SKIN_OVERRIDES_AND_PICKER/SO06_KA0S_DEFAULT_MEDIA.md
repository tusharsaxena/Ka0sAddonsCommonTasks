# Addendum SO-06: Ka0s Default's face and bar texture

Added 2026-10-28 during execution, on the owner's word: "Set the default font for Ka0s Default to be Ka0s
Prototype; and the default Texture to be Ka0s Melli Dark ... Ship both of them as part of the Ka0s
Default skin package in LibKa0s." The source is the owner's `SharedMedia_MyMedia` pack.

This settles Ka0s Default's card in the texture mockup: it was Ka0s Gradient, and it is now Ka0s Melli
Dark. The other eight cards still wait for the owner's approval under SO-04.

## What ships (LibKa0s)

- `LibKa0s/media/fonts/Prototype-Regular.ttf`: a byte-for-byte copy of `font/Ka0s Prototype.ttf`.
  `Prototype-LICENSE.txt` beside it records the font's embedded notice.
- `LibKa0s/media/textures/melli-dark.tga`: a byte-for-byte copy of `statusbar/Ka0s Melli Dark.tga`
  (64x64, grayscale, 32-bit).
- Media minor 9: `FONTS["Ka0s Prototype"]` (western only, since the face has no Cyrillic) and
  `TEXTURES["Ka0s Melli Dark"]`, both under the pack's own LSM names. A player who also runs the pack
  gets one dropdown entry for each, not two.
- SkinDefs minor 14: Ka0s Default sets `font.body`, `font.title` and `hud.font` to Ka0s Prototype and
  `bar.texture` to Ka0s Melli Dark. The other skins inherit Ka0s Default's tokens. A `KEEP` table holds
  what they inherited before (Friz Quadrata and the Blizzard bar), so no other skin's look changes.
  `font.mono` stays JetBrains Mono.

## The license question (for the owner)

Ka0s Prototype's name table reads "Copyright 2001, free for personal use, freely distributed with
Prototype.txt". 1001fonts lists it as not free for commercial use, with commercial licensing through
the author at mickeyavenue.com. Every other face LibKa0s ships is SIL OFL 1.1. Shipping it to every
consumer on CurseForge is a public redistribution, and CurseForge pays authors. The SO-06 commit
therefore stays local, and is not pushed, until the owner rules on it.

Ka0s Melli Dark's original author is not recorded in the pack. The "Melli" bars are widely
redistributed in SharedMedia packs. That is also recorded as an open provenance question.
