# Owner feedback round 4: plan and spec

The inputs are in `inputs/`: `OWNER_FEEDBACK.md` (verbatim, with every answer the owner gave) and `RECON.md` (the read-only
recon, `wf_4b563bc8-f13`, with file:line evidence). This file is the spec: what each item builds and the calls the lead
made without asking. `plan-data/items.tsv` is the manifest, and `RESUME.md` says how to pick up.

## Scope and branches

One branch name in every repo: `feat/2026-11-26-owner-feedback-round4`. It lives in LibKa0s, DropWatcher, CombatTrail,
RangeMaster and this repo. Builders work in clones under `~/ka0s-scratch/r4/<Repo>`, never in the live repos, which the
game loads. Merge waits for the owner's go-ahead.

Order: R4-LK-01 releases LibKa0s v1.118.0 (local tag) before R4-DW-00 re-vendors it. CombatTrail and RangeMaster run in
parallel with that chain. Each repo's items run in sequence in its one clone.

## Gate (every item)

- `ka0s-bounded lua tests/run.lua`, on the default client and with `KA0S_KIT_CLIENT=forever`;
- `ka0s-bounded luacheck .` at 0 warnings and 0 errors;
- `python3 -m pytest -q -p no:cacheprovider tools/seeds` where present;
- `tests/perf.lua` on both clients where present, with no ceiling raised;
- every file under 1500 lines and every function at CCN 15 or less;
- CRLF where `.gitattributes` says.

A commit whose subject starts `<ID>: ` marks an item done. Smoke rows are written unrun; only the owner runs them.

## LibKa0s

**R4-LK-01: a `dash` icon.** A thick horizontal bar with rounded ends, drawn in the style of the fat skill-up arrow:
- as wide as the arrow's stem and about 48–56/256 tall, so it stays solid at any sub-pixel offset at 14 px;
- a TGA in the media icon set with its own credit (hand-drawn, MIT like the library);
- the icon list, docs, tests and CHANGELOG updated;
- release v1.118.0, with the tag kept local until the merge.

## Drop Watcher

- **R4-DW-00:** re-vendor v1.118.0 and add `dash` to the `LibKa0s icons:` declaration; prune.
- **R4-DW-01, type colors.** The Drops from Type cell gets a fixed tone per type:
  - Creature: white;
  - Elite: game gold;
  - Rare: teal;
  - Rare Elite: pale blue;
  - Boss: rose;
  - Object: tan;
  - Container: lavender.

  The World drop "–" stays muted. Source cells are plain everywhere, including the tooltip's Drops from creature names, the
  Skinned from tab's Creature cell and the tooltip's Skinned from rows (lead's call: "do not color source" applies everywhere).
  The final palette must not repeat a profession tone from R4-DW-04, and both are checked against the tooltip background.
- **R4-DW-02, the dash.** The flat glyph is the `dash` icon in the known-gray tone, in both the tooltip and the window
  (`IST.CraftMark`). Its height is a whole number of pixels at the tooltip scale.
- **R4-DW-03, gathering professions.** The name map gets Herbalism 182, Mining 186, Fishing 356 and Skinning 393.
  `tools/seeds/recipes.py` adds the gathering lines that have recipes in the pinned build, taken through the seed loop as a new
  bundle. Incense Candle then reads Herbalism with its breakpoints. A recipe still known only from the profession window shows
  its Skill as "?", with a tooltip saying its skill levels are unknown. These lines count as professions you have.
- **R4-DW-04, profession colors.** One fixed tone per skill line, used in the tooltip's crafting and gathering rows and in the
  window's Crafting and Gathered from Profession columns. No tone uses a skill-up hue (orange, yellow, green, gray) or red.
  The recon palette is the starting point.
- **R4-DW-05, skill cue (owner: "Orange start + highlight").** The Skill parts always show the orange start, so a recipe
  whose minimum is 1 reads `1 55 75 95`. When your rank is known, the band you are in is highlighted, in both the window
  cell and the tooltip:
  - the highlight is a bracket around the number plus full brightness, and the other numbers are dimmed;
  - below the minimum, the start is shown in red.

  Not-known rows get the cue too. The tooltip memo key includes the band. No rank number is shown.
- **R4-DW-06, the flicker.** The tooltip's separator line is anchored, not measured: two invisible edge textures hang from
  the spacer line, and the line hangs from them. A tooltip clear or hide marks the line stale for its item instead of hiding
  it; a refill of the same item claims it again, and an unclaimed line comes off on the next frame. The mid-fill
  `tip:Show()` stays only where the client is not filling the tooltip. A red-first offline test reproduces the
  one-frame gap and the wrong-height ghost.
- **R4-DW-07, the badge.** A filled two-part badge right after the "Drop Watcher" label, drawn as textures on the tooltip,
  built and kept the same way as the line in R4-DW-06:
  - the left part is the verdict's bright tone, holding the lock and the word;
  - the right part is a darker shade of the same hue, holding the score;
  - Keep is green, Hold yellow, Sell amber and Toss red.

  The tooltip reserves the badge's width so it fits. The confidence tier is never shown, but it is still used inside so that
  Low never says Toss. The fix hint stays, without the tier word. The reasons always include the largest negative part when
  there is one, so the visible reasons add up (lead's call, since the owner asked what 65 means).
- **R4-DW-08, vendors.** A new profile setting, `itemSearch.hideOtherFaction`, is on by default, with a row on the Item Search
  settings page:
  - the tooltip drops the other faction's vendors and adds one dim "+N other-faction vendors" line;
  - when every vendor is from the other faction, the section shows its heading and that line;
  - the window's "Only my faction" chip defaults to the setting, and Reset returns to it;
  - vendors with no known faction stay.

  The owner skipped the vendor cost, so prices are unchanged: a price shows only when one is known.
- **R4-DW-09, quests.** The tooltip row reads `[mark] Title (Level)` on the left, with the level in the title's difficulty
  tone, and `Giver - Zone` on the right. The giver is the first giver whose name isn't a test name, resolved once per item;
  the zone is memoised per giver and map. The window's Giver column uses the same helper and the ` - ` separator. No LibKa0s
  change is needed.
- **R4-DW-10:** docs (settings page, schema, known limitations, module map, test inventory, README) and smoke rows.

## Combat Trail

- **R4-CT-01, sample data.**
  - `MockFights.Record` gets a `log` built by a pure, seeded `SequenceOf(plan)` from the plan's casts, plus made-up buff and
    debuff lines from new optional rotation fields, for each client.
  - A sample seam in `CombatLog` (`UseSample`, `SampleAppend`, `EndSample`) feeds the HUD drawer and the detached window in
    test mode and in the sim. No sample line ever reaches the real ring or a capture.
  - The Results section reads the sample record's log.
- **R4-CT-02, alignment.** `LogTable.JUSTIFY = 'LEFT'` for headers and cells. The icon sits at the Spell column's left
  edge, and the name follows after a one-character gap scaled with the font. This covers the HUD drawer, the detached window
  and the Results section.
- **R4-CT-03, headers.** `NS.Skin.SortHeaderBar` on the table header at 20 px, with sort triangles built like the
  Results list's, tinted by the skin and rebuilt on a skin change. All three homes.
- **R4-CT-04, chips.**
  - `sequence.drawer.chips` defaults to false, and an absent value means hidden.
  - The detached window gets `sequence.window.chips`, also false, plus an eye mark in its header (lead's call: hidden
    everywhere except the Results section).
  - The Results section's chips stay, because they are its filter and carry counts.
- **R4-CT-05, icons.** The detach mark becomes `chevron-right` and the detached window's dock mark `chevron-left`.
  `export` and `arrow-left` leave the declaration and are pruned.
- **R4-CT-06, width.** The default `hud.width` is the minimum width (260). A schema step writes 390 into every stored
  profile that has no width, so only new profiles start narrow. The hard-coded 366 fallbacks follow the new default.
- **R4-CT-07, sizing.**
  - `sequence.drawer.rows` defaults to 5 (was 10), and the minimum is 3 spell rows plus 3 sequence rows.
  - The grip splits the height between the two:
    - shrinking takes a row from the larger side (sequence first on a tie), as in 5/5 → 5/4 → 4/4 → 4/3 → 3/3;
    - growing adds a row to the smaller side (spells first on a tie), up to 15 spell rows, then the sequence grows up to 20;
    - on release both counts are written;
    - the split is a pure, testable `Hud.SplitFor`.
  - With the sequence closed or detached the grip moves only the spell rows, with a minimum of 3. With spells off it moves
    only the sequence.
  - Existing profiles that never changed their row count follow the new default of 5 (lead's call: the owner asked for 5
    each).
- **R4-CT-08, the owner's rulings.**
  - **LG22:** "Open when a fight starts" becomes a HUD setting: at the pull, a closed or hidden HUD opens. The Combat
    Sequence section no longer reopens itself. A schema step carries `sequence.drawer.autoOpen` over to the new HUD key, with
    the old default carried as on.
  - **LG27:** the Your, Hostile target and Friendly target colors are removed, with their switches, `ReadColors` and the two
    skin tokens. A schema step drops the stored `sequence.colors` keys. The Colors tab keeps Row washes.
  - Both smoke rows record the ruling.
- **R4-CT-09:** docs and smoke rows. The old smoke rows that this round changes get superseded notes.

## RangeMaster

- **R4-RM-01, assignment per character.**
  - `db.char.bandSetAssigned[profile] = setId` is written once, at a character's first load on a profile. It takes the class
    or spec preset's set, and creates it from the preset if it is missing.
  - A Devourer whose spec can't be read yet is deferred to the first event that can read it.
  - The assignment never moves by itself, not on a respec, a profile swap or a login.
  - A container's hostile set resolves as its own pick, then the assignment, then the old chain.
  - The Band sets page opens on the assignment, and "(default)" plus the Containers row's "Default band set (X)" name it.
  - A "Use for this character" action on the Band sets page changes it (owner: one per character).
  - Deleting an assigned set moves the assignment to the delete dialog's target and never re-creates the preset. The
    "Used by" line counts assignments. Copying a profile copies them, and resetting it forgets them.
  - The Ka0s container preset reads the assignment instead of matching by name.
  - Schema v6.
- **R4-RM-02, seeding.** A new profile seeds only its creator's class or spec set. Other sets join "Your band sets" only when
  something assigns or picks them: a character's first load, "Use for this character", a container preset, or New,
  Duplicate or "Use this preset". Existing profiles are left as they are (owner: "New profiles only").
- **R4-RM-03:** docs and smoke rows BANDS-31 onward, covering:
  - a new profile on the paladin, which gets one set;
  - the hunter swapping in, which gets the Hunter set assigned and shown;
  - swapping back and forth and a `/reload`, which change nothing;
  - a manual pick, which persists;
  - deleting an assigned set, which reassigns it.

## Review

After the build, one independent read-only reviewer per repo re-runs the gates and checks the work against this spec and
the owner's words, then a fix pass lands its findings as `R4-REV: ...` commits. The lead re-gates and pushes the branches
(milestone M3) and records the result in `EXECUTION_RECORD.md` and `plan-data/checkpoints.tsv`.

## Calls made without asking (beyond the owner's answers)

- "Do not color source" covers the tooltip's creature names and Skinned from too.
- The dash is a LibKa0s icon (a library tag), not a Drop Watcher-only bar.
- The reasons always include the largest negative part.
- When every vendor is from the other faction, Sold by keeps its heading and a "+N other-faction vendors" line.
- Quests use ` - ` in both homes, with the level in the title's tone.
- The sample sequence includes made-up buffs and debuffs, so every chip has rows.
- Existing profiles keep 390 wide, but follow the new default of 5 rows.
- The chips are hidden in the detached window too, with a new eye mark.
- The LG22 HUD auto-open is on by default, carried over from the old key.
