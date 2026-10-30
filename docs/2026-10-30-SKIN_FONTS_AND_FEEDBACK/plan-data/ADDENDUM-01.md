# Addendum 01 (2026-10-30, during M1)

- **LK-01 withheld Expressway** (LibKa0s 8bb8b0f): the dafont archive's Typodermic Desktop EULA 2026 puts embedding
  in software outside the free license (OS/2 fsType 4), and the owner's pack copy says "Do not distribute". WS-01's
  review then wrote a "never ships, whatever the ruling" clause into library-stack-§8.
- **Owner ruling, 2026-10-30, after seeing that evidence: "Ship it anyways."** LK-A1 ships it: the owner's pack
  TTF (`Ka0s Expressway.ttf`, the face in image-18, which the client already loads), with the archive's EULA files
  beside it as the terms record and the ruling quoted in `fonts.py` and `Media.lua`. Obsidian draws it for body,
  titles and HUD (D-02); Inter leaves the payload (D-03). WS-01 is amended to match: a non-OFL face ships only on a
  recorded owner ruling, and the ruling here names Expressway.
- **Kept from WS-01's review:** a stored font flag equal to the addon's previous default moves to From skin once on
  the v1.82.0 re-vendor (per-profile migration); only a flag the player changed counts as picked. Every M2 item
  that stores flags carries that migration step.

# Addendum 02 (2026-10-30, owner, during M1)

DpsRace (image-58, image-59): hovering a spell's icon or its bar in the Spell breakdown opens the game's full spell
tooltip, anchored to the right of the DpsRace window. The damage chart's cast-marker tooltip (today "Colossus Smash /
Cast at 0:45") also shows the full spell tooltip, keeping the cast time, anchored the same way. Both in the mid-race
and post-race views. Item DR-03 (`addendum-02.tsv`).
