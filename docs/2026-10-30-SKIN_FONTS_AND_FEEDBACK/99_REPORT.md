# Report: skin fonts and feedback (LibKa0s v1.82.0, standard v2.93.0)

This is the execution record. The plan (`00_PLAN.md`), `DECISIONS.md`, `items.tsv` and the addenda stay as written;
everything decided after them is recorded here.

## Where it stands (2026-10-30, end of M3)

- All 60 items have landed (`resume-state.sh -v`: 60/60): the 59 of M0 to M3, and CT-02, this report. Each is a
  commit or an `exceptions.tsv` row with a proof command (the seven IS-* items).
- Every run branch is pushed with its `refs/notes/ka0s-review` note: LibKa0s, WowAddonStandards, LibKa0sSkinTester,
  the 15 addons and this repo. Local and origin heads match in all 18 code repos, and so do the notes refs. This
  repo's branch is pushed at 3498749 (the M2+M3 checkpoint); the CT-02 commits after it are local. Every tree is
  clean and on `feat/2026-10-30-skin-fonts-feedback`.
- **Nothing is merged.** The LibKa0s tag `v1.82.0` is **local only**: tag object 5eca031 on commit 277081f.
  `git ls-remote --tags origin v1.82.0` is empty.
- The run is stopped for the owner's in-game smoke pass (`06_SMOKE_TESTS.md`) and the go-ahead for M5.

## What shipped, per owner item

| # | Owner item | Delivered by | What the player sees |
|---|---|---|---|
| 1 | Overrides reset on a skin change | LK-07 | Picking another skin clears the Font and Texture overrides: from the Skin tab, the picker (a preview clears them, closing restores them, Apply saves) and Apply to all. Re-picking the same skin keeps them; `/xx set` stays a raw write |
| 2 | Obsidian draws Expressway | LK-01, LK-A1, LK-02, WS-01 | Obsidian's body, titles and HUD are Expressway. It ships on the owner's "Ship it anyways" ruling (Addendum 01) |
| 3 | Ka0s Default draws Prototype | LK-01, LK-02 | Ka0s Default's body, titles and HUD are Prototype, shipped with `Prototype.txt` |
| 4 | WoW Forever draws Fira Sans Medium | LK-01, LK-02 | WoW Forever's body is Fira Sans Medium; its titles and HUD stay Fira Sans SemiBold (D-02) |
| 5 | Equal widths, Ka0s Default the baseline; HUD too | LK-05, LK-06, every XX-01 | Every skin's text is about as wide as Ka0s Default's (body 12, title 14, HUD 12). HUD text that uses the skin's face scales by the skin's HUD size (Obsidian 13, Glass 11, and so on); the stored size never changes. `/st widths` prints the ratios in the client |
| 5b | Characters some faces cannot draw | LK-12, BL-02, LH-02, WS-01 | LootHistory and BankLedger read "Database ~1.6 MB" and "Database size: ~"; the Quality tooltip reads "Poor to Legendary"; LootHistory's Transfer glyph is ↔ in the mono face; BankLedger's Direction tooltip drops ▼▲. A test-kit guard fails any display string outside the safe set |
| 6 | Reset buttons; Scope alignment | LK-08 | The Skin tab has Reset font and Reset texture (each greyed while that half is the skin's own), half-width Scope boxes lined up with the dropdowns, and a separate "Other Ka0s addons" heading for Copy |
| 7 | Remove unused fonts | LK-01, LK-A1, LK-02 | Ka0s Inter, Ka0s Inter SemiBold, Ka0s Oxanium SemiBold, Ka0s Oxanium Bold and Ka0s Fira Sans (Regular) are gone from the payload and from the font dropdowns |
| 8 | PGFE expand/collapse | PG-02 | The button is a tinted chevron, 12 px on a 20 px box, centered on the title band in every skin; no "up"/"down" words |
| 9 | AuraMaster TEST marker; glow | AM-02, AM-03, KC-03 | No "TEST" placeholder beside containers in test mode (the unlocked strip's TEST tag stays). Elements that stored the owner's own face (the Ka0s Kait picks) get "Use the skin's font" turned off once, so the face and the old glow come back. KickCD does the same |
| 10 | DropWatcher dropdown, Proc default, hidden sections; two issues | DW-02, DW-03, DW-04, LK-10, IS-01, IS-02 | The Loot rule column fits; both upgrade glows default to Proc, main #19FF19, off-spec #3FC7EB; a glow style's section shows only while a style dropdown picks it (both when two are picked) |
| 11 | Anchor titles cut off; sim placeholder anchor; issue | LK-09, AM-03, KC-02, IS-03, WS-01 | Drag-strip titles re-measure in the strip's own font on every skin repaint, with 2 px slack. KickCD's floating simulation strip is gone; its step panel stays up as the sign |
| 12 | `/xx skin` | LK-11, every XX-01, WS-01 | `/<slash> skin` in every addon opens the picker a new profile shows, whatever was seen before. Refused while disabled; a grey line in combat on every call |
| 13 | Outline by default, as a setting | LK-03, LK-04, every XX-01, WS-01 | A Font outline dropdown on the Skin tab: All text (default), HUD text only, Off. Ignore fonts greys it out and wins. Every font block's flags gain From skin, its default |
| 14 | MultiMeters issues | IS-04, IS-05 | Filed |
| 15 | QuickComms animation issue; test glyphs | IS-06, QC-02 | A comment on #13. `/qc test`'s four groups show numbered glyphs, tinted; a group or callout with no icon draws a folder or a speech bubble, the "?" only without the library |
| 16 | DpsRace Arm Race looks disabled (mid-run) | LK-14, DR-02 | The label reads as enabled in every skin. The cause was the library (below) |
| A02 | DpsRace spell tooltips | DR-03 | Hovering a spell icon or bar in the breakdown, and a cast icon on the damage chart, shows the game's full spell tooltip to the right of the window, mid race and post race, with "Cast at m:ss" on cast icons |
| A03 | DpsRace new-best toast | DR-04 | 25% larger throughout (height 90), trophy as tall as the three rows, equal 6 px row gaps, even padding, class and spec icons beside the "Arms Warrior" text |
| A03 | DropWatcher toast to match | DW-05 | The upgrade toast is 90 px tall, every element scaled by 90/74 |
| A04 | DpsRace breakdown tooltips | DR-05 | Every Spell breakdown tooltip (heading, compare toggle, Clear Pick, the note, the score table) opens beside the window, never at the cursor |
| A04 | DpsRace Difference column | DR-06 | Two right-aligned columns, amount and percent, under one Difference header, 4 px apart; the percent column fits "+100.0%" |

## Milestones

| Milestone | Evidence |
|---|---|
| M0 | Inventory reports A to K and the critic Z in `inputs/inventory/`; `DECISIONS.md` D-01..D-25; `plan-data/baselines.tsv` |
| M1 | LibKa0s at 277081f: 3412 passed, 0 failed, 2 skipped; luacheck 0/0 in 246 files. Release battery `docs/automated-tests/20261030-194244/` (measured 9d83cd4) green: lint, tests, complexity (0 functions over CCN 15, 14 files in the 1000-1500 band, none over the cap); perf not measured (no `tests/perf.lua`). The earlier record `20261030-190625` is kept and superseded. WowAddonStandards 71e47f1, `check-standard.sh` green. Skin Tester bf9f16f: 601/0/1, luacheck 0/0 in 79 files. Checkpoint pushed 2026-10-30 20:25 |
| M2 | 15 addons re-vendored from the local tag. Every vendored copy equals `git archive v1.82.0` apart from the declared icon prune (each reviewer re-diffed it). The lead re-ran every gate after the fix rounds (table below). Checkpoint pushed 2026-10-30 23:29 |
| M3 | Six issues and one comment, one write at a time (below) |
| M4 | This report and `06_SMOKE_TESTS.md` |

## The library and the standard

**LibKa0s v1.82.0** (27 commits, 667fb51..277081f, LK-01's 8bb8b0f the first). Eleven files moved one LibStub minor each: Media 10, Skin 9,
SkinDefs 17, SkinPaint 13, SkinPaintExtras 7, SkinPaintControls 11, WidgetsDragHandle 8, OptionsWidgets 37,
OptionsCompose 14, OptionsAppearance 4, OptionsSkinPicker 3. OptionsSwitch.lua is new (minor 1). The kit is
revision 45.

- Fonts (LK-01, LK-A1, LK-02): Prototype, Fira Sans Medium (google/fonts 4.203, the build of the shipped SemiBold)
  and Expressway ship; Inter, Oxanium and Fira Sans Regular leave. Fifteen faces register with LSM, twelve on ruRU.
- Outline (LK-03, LK-04): `skin.outline` per owner, applied once in `__Tokens`. `S.FontFlags(value, where)` resolves
  From skin; `O.FontGroup{ fromSkin = true, flagsFromSkin = true }` is the minimum font block. The mono role is never
  outlined.
- Sizes (LK-05, LK-06): body/title/HUD sizes per skin measured on the shipped bytes with outline on
  (`plan-data/font_metrics_shipped.txt`), pinned by `tests/test_skin_width_parity.lua`; `S.HudFontSize(size,
  fromSkin)`. High Contrast's description drops "larger type".
- Skin tab (LK-07, LK-08): `lib.__chooseSkin` resets overrides when the drawn look changes; the new layout.
- Strips (LK-09): re-fit on every repaint, `spec.onRefit` for hosts that size their own strips; `SetWidth` clears the
  fit.
- Sections (LK-10): `shownWhen = { any = {...} }`. OptionsWidgets was split first: the switched sections moved
  unchanged to the new OptionsSwitch.lua (OptionsWidgets 1447 to 1370 lines), because the change would have passed
  its 1450-line re-check trigger.
- Skin verb (LK-11): `O.SkinVerb(spec)`, answering frame, or nil with "combat", "queued", "unavailable".
- Glyph guard (LK-12): `Kit.assertDisplayGlyphs` and friends in `testkit/glyphs.lua`; the safe set is ASCII plus the
  118 code points all 15 faces share, generated by `tools/glyph_safe_set.py`.
- Button labels (LK-14): `P.color` in SkinPaint; see the lead decisions.
- Kit (LK-A2): `vendor_sync.lua`'s `BINARY_EXT` covers all 20 binary pins in `.gitattributes`, with a test that keeps
  them in step, and a CRLF text fixture.
- Docs (LK-13, LK-90): five new `docs/api` documents, CHANGELOG with "What a consumer owes", README credits,
  CONSUMERS.md paragraph. Two CCN splits before the tag: P.font (16, LK-03) and dhLendFont (17, LK-90).

**Standard v2.93.0** (WS-01, three commits). library-stack-§8 (faces and terms: OFL by default, other terms only on
a recorded owner ruling that names the face, the terms file beside it; a face no skin names leaves the payload;
locale masks from the cmap), skinning-§3/§4/§6 (faces per skin, width parity with outline on, HUD scale, override
reset, Reset buttons, the Font outline setting, the skin verb, an enabled button reads enabled), options-ui-§16 (the
whole font block, flags From skin), options-ui-§22 (new: hidden sections through `shownWhen`), slash-commands-§2
(`skin` reserved after `config`), preview-mode (a HUD MAY go unmarked in test mode; no simulation marker floats over
a HUD), localization-§7 (new: display strings keep to the safe set). WS-01's review had first written "Expressway
never ships"; 71e47f1 replaced that with the ruling.

**Skin Tester** (ST-01): re-vendor, `skin.outline`, `/st skin` (the showroom's picker button takes the same route), a
"Faces and widths" showroom section, and the `/st widths` probe.

## What landed per addon

Every addon's XX-01 re-vendors v1.82.0 in one commit that carries the stubs and facades the tag needs (degraded
`FontFlags` and `HudFontSize`, the Options stub's `SkinVerb`, `OptionsSwitch.lua` in any hand-written load list), so
no commit is red (D-23). Each then stores the Font outline, adds `/<slash> skin` after `config`, updates README
credits and adds smoke checks. The rest:

| Addon | Items | Beyond the common part |
|---|---|---|
| AbsorbTracker | AT-01 | Value text: From skin flags and the HUD size scale |
| AuraMaster | AM-01..03 | Four font groups with From skin; HUD scale, including the Text style's row pitch and Size to fit (review fix); TEST marker removed; v15 glow restore; strips re-fit through `Anchors.Refit` |
| BankLedger | BL-01, BL-02 | Outline at `settings.appearance.outline` (its existing namespace); no font settings, no HUD; characters replaced; glyph guard adopted |
| ConsumableMaster | CM-01 | Label flags From skin; label and stack count scale; glyph guard adopted |
| DpsRace | DR-01..06 | Five font blocks From skin; Results window text resolves as window text; clocks never outlined from From skin; DR-02 guard test only; DR-03..06 as above |
| DropWatcher | DW-01..05 | The tables' font is a whole font block (lead ruling); DW-02..05 as above; glyph guard adopted with `glyph: mono` markers |
| KickCD | KC-01..03 | Three font groups From skin; countdown, cast bar texts, label and charges badge scale; SimStrip removed; picked faces come off the skin once |
| LootHistory | LH-01, LH-02 | Outline at `settings.appearance.outline`; no font settings, no HUD; Insights KPI cards follow a live outline or skin change (review fix); characters replaced; glyph guard adopted |
| MultiMeters | MM-01 | Its existing flags (kept in its own "NONE" vocabulary) gain From skin; cells, title, column labels, tooltip, empty-state notice and the capped name width scale |
| PanelMaster | PM-01 | No font settings; draws no text of its own |
| PartyFrameEnhanced | PF-01 | Castbar, target and pet fonts From skin and scaled, restyled live; glyph guard adopted |
| PremadeGroupsFilterExtension | PG-01, PG-02 | No font settings, no HUD; the chevron button; its header click band stops at the body (review fix) |
| PrettyChat | PC-01 | No font settings (chat lines use the chat frame's font) |
| QuickComms | QC-01, QC-02 | Five font blocks From skin; HUD scale also sizes the pad cells; numbered test glyphs and default icons |
| WhatGroup | WG-01 | No font settings, no HUD |

## Migrations (lead decision 9 below)

Each addon that stores flags moves a stored previous default to From skin once (Addendum 01). The shapes differ:

| Addon | Step | Shape | What moves |
|---|---|---|---|
| AbsorbTracker | schema v7 | Account-wide stamp, walks every stored profile | `OUTLINE` to `@skin` |
| AuraMaster | schema v14, v15 | Schema steps over every profile | v14: `OUTLINE` to `@skin`. v15: "Use the skin's font" off where another face was stored (decision 6) |
| ConsumableMaster | profile step v5 | Per profile | label `OUTLINE` to `@skin` (after v3 turns `labelOutline=true` into `OUTLINE`) |
| DpsRace | schema v7 | Per profile, once, through the account-wide stamp | `""` (its old default, None) to `@skin` |
| KickCD | v6 to v7, v7 to v8 | Per profile, recorded in `skin.flagsReset` and `skin.fontPicksKept`, run at Init and every profile change | v7: `OUTLINE` to `@skin`. v8: picked faces off the skin |
| MultiMeters | v21 to v22 | Once per account, every window of every profile | header, text, tooltip, meta `NONE` and columnHeader `OUTLINE` to `@skin` |
| PartyFrameEnhanced | schema v3 | Every stored profile, global stamp | castbar, target, pet `OUTLINE` to `@skin` |
| QuickComms | step 11 | Per profile (`Library.MigrateFontFlags`) | `OUTLINE` on the five font blocks to `@skin` |
| DropWatcher | none | New keys only; DW-03 is AceDB defaults | nothing |
| BankLedger, LootHistory, PanelMaster, PGFE, PrettyChat, WhatGroup | none | No stored font settings | nothing |

AceDB strips a value equal to its default at logout, so most profiles reach From skin through the new default, not
the step. A player who picked the old default explicitly before the update cannot be told apart from one who never
chose, and moves to From skin; under All text it looks the same.

## Gates (lead re-runs, against `plan-data/baselines.tsv`)

| Repo | Baseline (master) | Branch head | Tests passed/failed/skipped | luacheck files (0/0) |
|---|---|---|---|---|
| LibKa0s | 667fb51: 3297/0/2, 237 | 277081f | 3412/0/2 (+115) | 246 |
| WowAddonStandards | 9c4837e: green | 71e47f1 | `check-standard.sh` green | n/a |
| LibKa0sSkinTester | 7274e37: 571/0/1, 75 | bf9f16f | 601/0/1 (+30) | 79 |
| AbsorbTracker | fe96c06: 954/0/1, 77 | 779d2e4 | 971/0/1 (+17) | 77 |
| AuraMaster | a9c2831: 2216/0/1, 188 | 89c1a48 | 2246/0/1 (+30) | 192 |
| BankLedger | 01f18b8: 1510/0/1, 111 | 2cbaa60 | 1530/0/1 (+20) | 114 |
| ConsumableMaster | b9f0f64: 1293/0/1, 138 | 9557b0d | 1315/0/1 (+22) | 140 |
| DpsRace | b6e4576: 1146/0/1, 148 | 1b3544f | 1185/0/1 (+39) | 152 |
| DropWatcher | 0d9d843: 1792/0/1, 202 | 858218c | 1826/0/1 (+34) | 205 |
| KickCD | 3852628: 1557/0/1, 153 | f2020aa | 1575/0/1 (+18) | 153 |
| LootHistory | 5b28b54: 1834/0/1, 151 | 69afe0b | 1857/0/1 (+23) | 154 |
| MultiMeters | a3284b3: 2418/0/1, 171 | 7b7d275 | 2447/0/1 (+29) | 174 |
| PanelMaster | f7adca7: 1140/0/1, 80 | e4e2fa1 | 1156/0/1 (+16) | 82 |
| PartyFrameEnhanced | 97b4904: 538/0/1, 87 | 73c78c0 | 565/0/1 (+27) | 90 |
| PremadeGroupsFilterExtension | 6583515: 429/0/1, 64 | c80e35a | 447/0/1 (+18) | 66 |
| PrettyChat | 4fa8452: 631/0/1, 62 | 2369bd6 | 647/0/1 (+16) | 64 |
| QuickComms | be7cbb4: 1260/0/1, 143 | 27e20ff | 1295/0/1 (+35) | 147 |
| WhatGroup | 8360cb3: 1025/0/1, 69 | 08bb84b | 1041/0/1 (+16) | 71 |

The skip counts are the declared skips and did not move. No authored file is over 1500 lines (PrettyChat's generated `GlobalStrings/GlobalStrings.lua`
was over before the run and is untouched); MultiMeters'
`modules/Window.lua` is exactly 1500. KickCD lost the 13 cases of `test_sim_strip.lua` with the strip.

## Exceptions (no commit, with proof)

Only the seven IS-* items, each with a `gh` proof in `exceptions.tsv`. LK-14 needed none: the cause was the library's,
so LK-14 is a commit and DR-02 is DpsRace's guard test.

## Issues filed (M3)

Filed one at a time, 24 to 37 s apart (about 25 s for all but one gap), after a duplicate search in each repo. All open, `state:untriaged`.

| Item | Issue | Title |
|---|---|---|
| IS-01 | https://github.com/tusharsaxena/LibKa0s/issues/67 | Hide the settings sections a selector does not pick, in every Ka0s addon (umbrella sweep for options-ui §22) |
| IS-02 | https://github.com/tusharsaxena/DropWatcher/issues/14 | Toast: stack the toasts when several drops qualify, instead of showing them one after another |
| IS-03 | https://github.com/tusharsaxena/LibKa0s/issues/68 | Check every addon's anchor (mover) title width in every skin, now the skin fonts are frozen |
| IS-04 | https://github.com/tusharsaxena/MultiMeters/issues/61 | Insights view: post-fight analysis of a segment, out of combat |
| IS-05 | https://github.com/tusharsaxena/MultiMeters/issues/62 | Bar animations beyond the fill slide: rank changes, rows entering and leaving, value changes |
| IS-06 | https://github.com/tusharsaxena/QuickComms/issues/13#issuecomment-6528907808 | Comment on #13 (Animate the Comms Pad and the dial on open and close): pad and dial, open and close, four independent switches |
| IS-07 | https://github.com/tusharsaxena/LibKa0s/issues/69 | Skins: measure real Friz Quadrata and set WoW Default's sizes for width parity |

`gh issue view 13 --comments` fails on this gh with a Projects-classic error, so IS-06's proof uses `gh api`.

## Lead decisions taken during the run (after DECISIONS.md)

1. **Expressway ships (LK-A1, Addendum 01).** LK-01 first withheld it: the dafont archive's Typodermic Desktop EULA
   puts embedding in software outside the free license, and the pack copy says "Do not distribute". The owner ruled
   "Ship it anyways." What ships is the owner's pack TTF as `Expressway-Bold.ttf` (Expressway Rg Bold 2.100, the face
   in image-18), not D-01's Regular, with the archive's `Expressway-EULA.pdf` and `Expressway-EULA-Guide.html` as the
   terms record; the ruling is quoted in `fonts.py` and `Media.lua`. Its langmask is **WEST_RU**: the cmap holds all
   66 Russian letters. That corrects D-04's "Latin only". Inter left the payload with it (D-03).
2. **The Arm Race label was the library's (LK-14).** A label painted at 0.4 alpha while disabled kept that alpha
   after it was enabled, because `P.rgb` passed three numbers to `SetTextColor` and the client keeps the old alpha.
   The screenshot pixels match exactly (Obsidian #FFFFFF at 0.4 over #1E80D0 gives 121,179,227). `P.color` adds the
   alpha 1 for `SetTextColor` only when the target is not opaque; Button labels and the CloseButton glyph use it. A
   contrast guard covers every skin (lowest: Obsidian primary 3.87:1). DR-02 landed as DpsRace's guard test with no
   code change. No exception was needed.
3. **LK-10 split OptionsWidgets** into the new OptionsSwitch.lua rather than letting it reach about 1465 lines past
   its re-check trigger.
4. **The kit's binary gap and the re-cut tag (LK-A2, Addendum 05).** ST-01's trial re-vendor of the first tag
   (11a9c9a) failed: `vendor_sync.lua` compared `Expressway-EULA.pdf` as text and stripped its CRs, so every consumer
   would have gone red. LK-A2 fixed it, a second release battery ran (`20261030-194244`), and the local tag moved from
   11a9c9a to 277081f. The re-cut was committed under the LK-A2 id ("LK-A2: Re-run v1.82.0's release battery"), not
   LK-90; LK-90's own commits are c6a9fb7 and 11a9c9a.
5. **The width probe is `/st widths`.** items.tsv says `/skt widths`; the Skin Tester's slash is `/st` (alias
   `/skintester`).
6. **AuraMaster's v15 keeps Friz Quadrata and the five deleted faces on the skin.** D-15 says to turn "Use the skin's
   font" off wherever the stored font is not the skin's own HUD face. Read literally, that would also take every
   untouched starter block off the skin, because the template stores "Friz Quadrata TT", and undo v13's reset across
   the account. A block on a face D-03 deleted would draw the client's fallback font. So v15 turns the box off only
   for a face that is neither the profile's skin HUD face, nor Friz, nor a deleted face (`DELETED_FACES`). On the
   owner's profile it turns off the 3 Ka0s Kait picks and keeps the 137 Prototype picks. KickCD's KC-03 uses the
   same exemptions (`PRE_V182_FACES`). This departs from D-15's wording; **the owner may overrule it.** One side
   effect: a profile on Obsidian would take a Prototype pick off the skin, since Expressway is that skin's face.
7. **DropWatcher's tables get the whole font block.** DW-01 first read D-07 as a check only (DropWatcher had just a
   Tables Font size slider). The lead ruled D-07 applies: bc3c5dc (with 858218c, a comment) gives Window > Layout >
   Tables a full `FontGroup` (face with Use the skin's font, size, color with class color, flags From skin, shadow).
   The defaults keep today's look; only the flags change. **Font color applies to the tables' plain text only**:
   verdicts, item qualities and looter class colors keep their meaning, and a swatch left at its default draws the
   skin's plain color. **The Offset subgroup stays visible** under Button/Button (D-17 names only the four style
   sections).
8. **DpsRace's outline.** The two mono clocks never take an outline from From skin, in any mode; a flag picked on a
   clock still wins. With Ignore fonts on, the HUD's live figures and spell text on From skin still draw OUTLINE:
   that is the library's documented answer, and DpsRace declined to special-case it. Results window text (the Runs
   bars and the detail's spell rows) now resolves as window text, so HUD text only drops its outline. DR-04 read the
   owner's "class and spec tooltip" as icons beside the text (Addendum 03).
9. **Migration shapes differ per addon** (table above). Each meets Addendum 01: every stored profile is migrated
   once and a flag the player picked survives.
10. **Sizes under a font override (LK-05/06 review, open).** A font override keeps the skin's measured sizes and HUD
    factor (pinned by a test). The alternative is Ka0s Default's 12 / 14 / 12. No decision covers it; the owner can
    rule.
11. **The outline under Ignore fonts.** `S.FontFlags(FROM_SKIN, "window")` answers "" and the HUD answers "OUTLINE"
    (LK-03/04 review). Addons whose old default was None (DpsRace, MultiMeters) therefore draw outlined HUD text under
    Ignore fonts where they did not before.
12. **MultiMeters' window title and session line count as HUD text** under HUD text only. The owner confirms this at
    its SKIN-25.
13. **The picker's Apply to all does not carry the outline** (LK-03/04 review); Copy to every Ka0s addon does.

## Things the run noticed

- An early ST-01 attempt's staged work was wiped by a `reset` at 19:16:52 +0530 before it was committed; ST-01 was
  re-implemented from the re-cut tag and reviewed again. The lost blobs were not recovered.
- The first release run's tag predated the kit fix; nothing had re-vendored from it, so moving the local tag was safe.
- Several implementers wrote LF into CRLF files or doubled CRs; the kit's eol test caught each before commit.
- DR-03 passes a secret spell ID to `GameTooltip:SetSpellByID` mid race under `pcall`. Whether the live client accepts
  it cannot be tested headlessly; if not, rows show only the spell name (SM-DR-SF8). DR-03 also moved the chart's
  "+n" crowd marks to the same anchor, which was not asked.
- DW-05 matched DpsRace's height and scale only; DR-04's even row gaps were not carried over (Addendum 03 asked for
  height and scale).
- On the owner's client `Fonts/FRIZQT__.TTF` is Prototype (same md5), so WoW Default looks like Ka0s Default there.
  Real Friz is unmeasured (IS-07).

## Open findings and follow-ups (not filed)

- **Fira Sans Medium key collision.** The owner's SharedMedia_MyMedia registers "Ka0s Fira Sans Medium" as build
  4.301; LibKa0s ships build 4.203 under the same key. LibKa0s registers a key only if LSM does not already hold it,
  and skins resolve faces by key, so whichever registers first is drawn. LK-05 measured 4.203. Ka0s Prototype and
  Ka0s Expressway are byte-identical to the pack copies, so they are unaffected. Before a WoW Forever width result
  counts, check which file the key fetches (`06_SMOKE_TESTS.md`).
- **Strip re-fit after a fresh login (LK-09 review F2).** The OnShow plus `C_Timer.After(0)` re-fit was left out
  (D-12 did not ask for it). If a strip title is cut off after a fresh `/reload` (KickCD's Focus and Target strips
  first), add the one-shot re-fit in WidgetsDragHandle.
- **SimPanel `close = false` gap (KC-02).** SimPanel does not pass a host's `panel.close` to the step panel and always
  adds it to `UISpecialFrames`. KickCD works around it with `Host.PinPanel` / `UnpinPanel`, which touch the panel's
  internal `closeButton` and its global name. A LibKa0s fix would let KickCD delete both.
- **PGFE library gaps (PG-02).** SkinEUI forwards `S.PageButton(btn, "up"/"down")` to EllesmereUI verbatim (the
  words); PageButton has no `opts.icon` / `opts.size`; `icon.arrow` is not in SkinEUI's `ACCENT_TOKENS`, so the
  chevron is Ka0s gold under EllesmereUI. Declined in PGFE: a border-aware inset for the nine-slice skins (Glass, WoW
  Default); SKIN-38 decides.
- **Glyph guard not adopted everywhere.** Five addons call it (BankLedger, ConsumableMaster, DropWatcher,
  LootHistory, PartyFrameEnhanced); the other ten do not. Known hits in four of those: AbsorbTracker (3 hits: `debugNames = {"adoptProfile"}` and `core/Units.lua:125`'s
  `player→` scope string), KickCD (`core/Units.lua:161`, the same kind), PGFE (200 hits, all lookup keys in
  `defaults/Realms.lua`, needs a skip), PrettyChat (Blizzard's € in GlobalStrings). The guard was optional in M2.
- **The flaky LibKa0s test** "tool windows skin: without a registered owner each window is the previous minors'
  paint" failed once in four full runs (call-sequence mismatch) during LK-A2, before and after the fix. It passed at
  every gate that counts.
- **Pre-existing functions above CCN 15** (each untouched by this run; the branch's hunks miss them). They block each
  addon's next `/dev-copilot:bump-version`: DpsRace nine (Database's v6 step `run`, Hud_Appearance `color`,
  DummyList.Read and .Resolve, Hud_States `body.Update`, Usage.KnownItems, Results_Runs `View.ApplyView`, Slash
  `captureLine`, test_skin_literals `scan`); KickCD `setLocked` (18) and `MigrateHudSkin` (16); BankLedger
  `modules/Sim.lua` `itemName` (16); MultiMeters `Runtime.sim` (17); PanelMaster `renderTab` in
  `tests/test_settings_layout.lua` (16); AuraMaster an anonymous function in `tests/test_pages_text.lua:76` (19).
  MultiMeters' `modules/Window.lua` is at exactly 1500 lines; the next change there must peel first.
- **Stale comments in LibKa0s.** Nine shipped files still say Ka0s Default draws Oxanium (DebugLogWindow, PerfPanel,
  SimPanel, Widgets, WidgetsAutocomplete, WidgetsDragHandle, WidgetsLineChart; the Media and SkinDefs lines are
  history). Comment-only; fix when each file's minor next moves. WidgetsDragHandle's minor moved in this run (LK-09,
  7 to 8) and its comment was not fixed.
- **The standard's glyph rule.** localization-§7 makes the guard's generated set the authority, but does not name
  the `glyph: mono` / `glyph: data` markers or the skip-reason rule (LK-12 review info, handed to WS-01; not done).
- `docs/api/CONSUMERS.md` keeps its v1.75.0 stamp and does not measure the new surfaces.
- `plan-data/font_metrics_shipped.txt` still says in its header that `font_metrics.py` generated it; the script is
  `font_metrics_shipped.py`. The bundle file is left as committed.
- Smaller notes: DropWatcher's `plainColor` treats the literal default grey as From skin; QuickComms' QC-02 owes a
  "Refreshed" preview-mode note at its next version bump; older passed smoke rows that name Oxanium or Inter were
  left as recorded in DpsRace (SK4, SK12, SK15, SK25) and PGFE (SKIN-11, 26, 28), superseded by the new checks.

## M5 (on the owner's go-ahead)

Per `RESUME.md` §6:

1. Finalize in order: WowAddonStandards, then LibKa0s (and push tag `v1.82.0` at 277081f), then LibKa0sSkinTester,
   then the 15 addons, then this repo. Merge each with `--no-ff`, push it with its notes, delete the remote branch
   before `git branch -d`. No version bumps.
2. Check that each vendored copy differs from LibKa0s only by the declared icon prune.
3. Run `git stash list` and `git worktree list` in every repo and remove anything this run created. None exist at
   M4: every repo lists no stash and only its main worktree.
