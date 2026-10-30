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

# Addendum 03 (2026-10-30, owner, during M1)

DpsRace's new-best toast (image-60):
- 25% larger overall, with every element scaled to match.
- The trophy icon is as tall as the three text rows (headline, the Cleave / 1:00 tags, the DPS line), and the toast
  widens as needed to fit it.
- The three rows get a little more spacing, equal between each pair. The padding above the first row and below the
  last row is evened out.
- Class and spec icons go next to the "Arms Warrior" text. The owner wrote "class and spec tooltip"; the lead reads
  it as icons, the only reading that fits "next to the text". Item DR-04.

Then DropWatcher's toast is resized so its height matches the new DpsRace toast, with its elements scaled to match.
Item DW-05, run after DR-04 lands so the height can be read from DpsRace's code (the two addons run in parallel in
M2, so DW-05 waits on DpsRace's commit). Both rows are in `addendum-03.tsv`.

# Addendum 04 (2026-10-30, owner, during M1)

DpsRace's Spell breakdown:
- **DR-05 (image-61, image-62).** Some hovers in the breakdown, such as the "Compare vs runner-up" Damage and DPS rows
  and the headers and text, show their tooltip at the cursor. Every tooltip in the section anchors to the right of
  the window, as the spell rows' tooltips already do (image-62). The anchor is shared with DR-03, so DR-05 follows
  it.
- **DR-06 (image-63).** The Difference column becomes two columns under one shared "Difference" header: the amount
  (`+512.6K`) and the percent (`+5.0%`), both right-aligned and with a tight gap between them. The percent column is
  wide enough for a signed value with three integer digits and one decimal (`+100.0%`, `-100.0%`) in every skin.

# Addendum 05 (2026-10-30, lead, end of M1)

ST-01's trial re-vendor of the v1.82.0 tag (11a9c9a) went red on a library gap. The test kit's `vendor_sync.lua`
`BINARY_EXT` table says it matches `.gitattributes`' binary pins but has no `pdf` (nor `tar`, `gz`, `7z`, `bin`,
`param`). It strips CR from the shipped `Expressway-EULA.pdf`, so a byte-identical vendored copy fails its own
vendor-sync case. Every consumer would go red. LK-A2 fixes the table, adds a kit test that it covers every `binary`
line in `.gitattributes`, re-runs the release battery and re-cuts the **local** v1.82.0 tag (never pushed, so
moving it is safe). ST-01 then runs on the re-cut tag. RESUME §5's path, taken in M1 instead of M2.

# Addendum 06 (2026-10-31, owner, after M4)

DropWatcher's Situations defaults (image-64). Tracked and auto-open: Mythic+, Dungeon, Follower dungeon, Raid,
Delve, Scenario, Solo. Raid Finder: tracked, no auto-open. PvP and Open world group: neither. Quality "Use global"
everywhere. Loot rule Personal everywhere except PvP (Legacy), so Follower dungeon moves from Legacy to Personal.
Master Auto-open stays on. These are AceDB defaults: a profile that never changed a cell takes them, a stored choice
stays (D-18's rule, no migration). Item DW-06.

# Addendum 07 (2026-10-31, owner, after M4)

The owner asked for the three follow-ups `99_REPORT.md` left open:
- **The display-glyph guard in the ten addons that do not call it** (AT-02, AM-04, DR-07, KC-04, MM-02, PM-02, PG-03,
  PC-02, QC-03, WG-02). Each adds a `tests/test_glyphs.lua` calling `T.assertDisplayGlyphs` (BankLedger's is the
  model). A character a shipped face cannot draw in player-facing text becomes a safe one (D-19's rule). Strings that
  are data, not display text, get a `glyph: data` mark with a reason; ones drawn in the mono role get `glyph: mono`.
  Examples are PGFE's realm lookup keys and PrettyChat's Blizzard GlobalStrings.
- **No function above CCN 15** in the six addons that have pre-existing ones (AM-05, BL-03, DR-08, KC-05, MM-03,
  PM-03). These are behaviour-preserving refactors measured with the vendored complexity suite, so each addon's next
  `/dev-copilot:bump-version` is not blocked.
- **MultiMeters' `modules/Window.lua`** is at the 1500-line cap; MM-04 splits it into cohesive files with headroom,
  with the same public surface.

# Addendum 08 (2026-10-31, owner, after M4)

DropWatcher (image-66): a tradeable drop of your own shows the Offer button even when nobody could take it. Do not
offer when you are the only human player present: solo, in a delve (Brann or other companions are NPCs), in a
follower dungeon (the party's followers are NPCs), or in any group whose other members are all non-player units.
The row shows the existing "No action" state, with a tooltip naming the reason, instead. When a human joins, the
Offer returns. Item DW-07.
