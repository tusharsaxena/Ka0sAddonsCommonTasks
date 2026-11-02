# Addendum: skin fonts and table rows (owner, 2026-11-02, mid-run)

The run was paused at 22:05 during M1, before the re-cut. LibKa0s held R3-DR-1L, R3-L2 and an uncommitted IconBorder test, and nothing had been re-cut or re-vendored. The owner's word: these land in the library work, nothing is re-vendored until they are done, and it is fine to stop and wait.

## What the owner reported

- **Obsidian (img 95; Ka0s Default for comparison, img 96):** the body font is a tad too wide, and Loot History's Date column truncates ("02-Nov-20…"). Make it a tad smaller. The alternating row background in tables is hardly visible: make it slightly more obvious.
- **WoW Default (img 98):** the same truncation, but Friz Quadrata cannot shrink even 0.5 pt without becoming unreadable.

## Rulings

- **No dynamic column widths.** The lead offered "columns fit the font". The owner declined it, because it would mean changing every addon.
- **Ka0s Ubuntu.** Vendor Ubuntu Regular as "Ka0s Ubuntu" and make it WoW Default's font for body, title and HUD. Image 99 shows it in game as the Font override. The client's "Ubuntu" is EllesmereUI's media/fonts/Ubuntu.ttf (Ubuntu Regular, static). Vendor the official static Ubuntu-Regular.ttf, for example from github.com/google/fonts ufl/ubuntu, with UFL.txt (Ubuntu Font Licence 1.0, which allows redistribution). Never vendor the copy out of EllesmereUI.
- **Delete Ka0s Friz Quadrata TT** from the library: the file, Media.lua, FONTS.md, `__FACE_SIZES`, the FRIZ constant and every skin token that names it. Blizzard's own Friz, which LSM calls "Friz Quadrata TT", is not ours and is untouched.

## The lead's calls

- Obsidian's body drops one step, Expressway 12.5 to 12 (or the step that makes "02-Nov-2026" fit Loot History's Date column the way Ka0s Default does). Titles and HUD keep their sizes unless they share the token.
- The alternating row tint in Obsidian rises to a visible step. Check it against the other dark skins, so Obsidian is not the only faint one.
- Ka0s Ubuntu's sizes go into `__FACE_SIZES` by the library's width-parity method. If the parity size still truncates the Date column, take one step smaller: the face is tall, so it stays readable.
- Any other skin on Friz moves to Ka0s Ubuntu too, and the report names it.
- A stored pick of "Ka0s Friz Quadrata TT" anywhere (a skin Font override, or an addon's own font setting) moves to "Ka0s Ubuntu" in a one-time migration. The library already falls back on an override that no longer resolves; the migration keeps the look intended.
- A new font file needs a **full client restart**, and the smoke list says so first.

## Items

These are added to `items.tsv`. R3-L4 to R3-L7 run before R3-REL. R3-FRIZ runs with R3-RV.
