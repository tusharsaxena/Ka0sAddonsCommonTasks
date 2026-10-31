# D_GLYPHS: characters some skin fonts cannot draw (item 5b)

Read-only inventory, 2026-10-30. Owner item 5b, image-19: the LootHistory footer reads "Database [] 1.6 MB" in a
skin whose face has no `≈`.

## Method

- **Scope.** Every `.lua`, `.toc` and `.xml` in `LibKa0s/LibKa0s`, `LibKa0sSkinTester` and the 15 roster addons.
  `libs/` and `tests/_kit/` are excluded. Each addon's own `tests/` was scanned separately, for assertions.
- **Lexing.** A Lua lexer separated comments from string literals and decoded `\ddd` and `\xNN` escapes back to
  UTF-8. The decoding matters, because most of the glyphs that matter are written as escapes
  (`"\226\137\136"` = `≈`), and a plain grep misses them. This found 3,990 string literals with non-ASCII text,
  plus about 300k non-ASCII characters in comments, almost all `─` `—` `§`. The comments are ignored.
- **Font coverage.** fontTools `getBestCmap()` was run against every face a skin ships:
  - Prototype, Expressway and Fira Sans Medium, from `SharedMedia_MyMedia/font/`.
  - Vollkorn and Vollkorn Bold, Nunito and Nunito SemiBold, Atkinson and Atkinson Bold, Bitter and Bitter Bold, and
    Philosopher and Philosopher Bold, from `LibKa0s/LibKa0s/media/fonts/`.
  - JetBrains Mono, which is `font.mono` in every skin (`LibKa0s/LibKa0s/SkinDefs.lua:235`).
  - Friz Quadrata, `_retail_/Fonts/FRIZQT__.TTF`, which is the WoW skin's face and the client default.
  - Inter, Fira Sans and Oxanium were also checked, for information only.

## 1. Which characters are safe

**Every shipped face draws these.** No change is needed for the skin fonts:

`— – … • · × › § ° ± ’ ‘ “ ” £ ¥`, NBSP and `é ê è à â ä ö ü ù É Ä Ö Ü`.

Your display text uses them about 1,400 times. Per repo, they are mostly em dashes in tooltips and in slash help;
the counts are in section 6. They stay as they are unless the lead chooses option B in section 5.

**Some shipped faces lack these.** Each row lists the faces that cannot draw the character:

| Char | U+ | Faces that lack it | ASCII replacement |
|---|---|---|---|
| `≈` | 2248 | Expressway, Philosopher, Philosopher Bold | `~` |
| `≠` | 2260 | Expressway, Philosopher, Philosopher Bold | `!=` |
| `→ ← ↑ ↓` | 2190-2193 | Prototype, Expressway, Nunito (both), Atkinson (both), Philosopher (both), **Friz** | `->` `<-` `^` `v` |
| `↔` | 2194 | (JetBrains Mono has it) | `<->` |
| `⇄` | 21C4 | **every face, JetBrains Mono included** | `<>` / `↔` in mono / a texture |
| `▲ ▼` | 25B2/25BC | Prototype, Expressway, Nunito, Atkinson, Philosopher, **Friz** (JetBrains Mono has them) | `+`/`-`, `^`/`v`, or a texture |
| `▸ ▾` | 25B8/25BE | every face except JetBrains Mono, Fira Sans Medium | `>` / `v` |
| `⊕ ⊘ ⌄ ✓ ✗ ─` | | every face except JetBrains Mono (and Inter for ⊕ ⊘) | `(+)` `(/)` `v` `x` `x` `-` |
| `€` | 20AC | Prototype, Friz | (Blizzard's string, see PrettyChat) |
| Cyrillic | | Prototype, Atkinson (both), Friz | n/a: not our text, see Q4 |
| CJK | | every face | n/a: test data only |
| `Ā ā Ĺ ĺ Σ σ` | | several | n/a: test data only |

## 2. Occurrences in display text that must change

The sink and the face matter more than the character.

- **Debug lines** (`NS.Debug`) go to the console. The console body is `SetFont(ctx.d.font)` = `FONT_MONO` =
  JetBrains Mono (`LibKa0s/LibKa0s/DebugLogWindow.lua:377`). The font override leaves `font.mono` alone
  (`Skin.lua:680`).
- **DropWatcher verdict glyphs** go through `NS.SkinMono` (`DropWatcher/core/SkinSetup.lua:269-283`), which is also
  JetBrains Mono.
- **Everything else** is drawn in the skin's body face or in the tooltip's face.

### LootHistory

| File:line | String | Char | Face it renders in | Faces that lack it | Proposed change |
|---|---|---|---|---|---|
| `modules/Browser.lua:591` | `("Database \226\137\136 %s")`, the window footer (**image-19**) | ≈ | skin body | Expressway, Philosopher(B) | `"Database ~%s"`, or `"Database: %s (est.)"` |
| `settings/Panel.lua:149-150` | `"\nDatabase size: \226\137\136 " .. … .. "  (estimated)"` | ≈ | panel label (skin body) | same | `"Database size: ~%s (estimated)"` |
| `core/Constants.lua:117` | `C.DirGlyph.MOVE = "\226\135\132"`, drawn by `modules/BrowserTable.lua:1162` into a glyph FontString set to `C.FONT_MONO` (`:799`) | ⇄ | JetBrains Mono | **all, mono included**. The owner's SavedVariables hold **160 MOVE rows**, each drawn as a box today | `"\226\134\148"` (↔, which mono draws). An ASCII option is `"<>"`. IN/OUT `▲▼` are fine in mono |
| `modules/BrowserTable.lua:237` | `desc = "Item quality (Poor → Legendary)."`, a column-header tooltip | → | tooltip (Friz or skin body) | Friz, Prototype, Expressway, Nunito, Atkinson, Philosopher | `"Poor to Legendary"` or `"Poor -> Legendary"` |

These are fine, drawn as textures: the sort arrows are `|T` markup via `NS.IconMarkup`
(`modules/BrowserTable.lua:339-340`, `modules/HoldingsTab.lua:317-318`).

### BankLedger

| File:line | String | Char | Face | Faces that lack it | Proposed change |
|---|---|---|---|---|---|
| `modules/Browser.lua:754` | `("Database \226\137\136 %s")`, the footer | ≈ | skin body | Expressway, Philosopher(B) | `"Database ~%s"` |
| `settings/Panel.lua:159` | `"\nDatabase size: \226\137\136 "` | ≈ | panel label | same | `"Database size: ~"` |
| `modules/LedgerTable.lua:70-71` | `"Deposit (\226\150\188) … withdraw (\226\150\178) …"`, a column tooltip | ▼ ▲ | tooltip | Friz, Prototype, Expressway, Nunito, Atkinson, Philosopher | `"Deposit (down arrow) …"`, or drop the glyph references from the prose |

These are fine, in mono: `C.DirectionGlyph` ▲▼ (`core/Constants.lua:82-85`), drawn at `modules/LedgerTable.lua:591`,
in `SessionWindow.lua:369` and in the dropdown `glyphFont = C.FONT_MONO` (`modules/Browser.lua:320`, consumed at
`LibKa0s/LibKa0s/Widgets.lua:318-319`). Sort arrows are textures (`modules/LedgerTable.lua:219-220`).

### MultiMeters

| File:line | String | Char | Change |
|---|---|---|---|
| `MultiMeters.toc:3` | `## Notes: … one column per stat — read from …` | — | Safe, because every face draws it, and the AddOns list uses the client font anyway. Optional `-` |

No other .toc has non-ASCII in `## Title` or `## Notes`. Every other .toc and Bindings.xml hit is a comment.

### DropWatcher: fine today, provided font.mono stays JetBrains Mono

- `modules/WindowCells.lua:43`: `WC.GLYPH = { upgrade="▲", sidegrade="≈", downgrade="▼" }`.
- `modules/CompactCards.lua:63`: `CC.NO_GLYPH = "⊘"`.

Every draw site goes through `NS.SkinMono` or `NS.SkinMonoFont()` (`DetailCard.lua:128`, `CompactGroup.lua:209`,
`Toast.lua:273`, `TipGrid.lua:103`, `WindowHistory.lua:366`, `WindowGroup.lua:545,590`), and JetBrains Mono draws
all four. The comment at `core/SkinSetup.lua:268` says "Every Ka0s skin's font.mono carries the verdict glyphs", and
that holds only while every skin keeps JetBrains Mono. `CC.Plain` and `CC.VerdictText`
(`modules/CompactCards.lua:127,387`) concatenate the glyph into plain text, but nothing outside tests calls
`CC.Plain`.

### PrettyChat

`GlobalStrings/GlobalStrings.lua:2248` and `GlobalStrings_003.lua:488` hold `"€%s"`, a mirror of Blizzard's
`BLIZZARD_STORE_CURRENCY_FORMAT_EURO`. It is chat output in the chat font. **Leave it.**

### No change: debug-console lines

These all render in JetBrains Mono, which draws `→`, `≠` and `↔`. Change them only if the lead picks option B.

| Repo | File:line | Text |
|---|---|---|
| LibKa0sSkinTester | `core/LibKa0sSkinTester.lua:60` | `copied profile '%s' → '%s'` |
| AbsorbTracker | `core/AbsorbTracker.lua:267,269,440,459`; `core/Database.lua:278,283`; `core/Units.lua:125` (Bulk scope `player→unit`, only in a `[Set]` debug line: `LibKa0s/LibKa0s/Schema.lua:677`) | shield / profile / migrate arrows |
| ConsumableMaster | `core/ConsumableMaster.lua:592` | copied profile → |
| DropWatcher | `core/DropWatcher.lua:568` | copied profile → |
| KickCD | `core/Database.lua:641`; `core/Units.lua:161` (scope `a→b`); `settings/Spells.lua:342` (≠) | |
| LootHistory | `core/LootHistory.lua:92`; `modules/Attribution.lua:251,277,287` | |
| MultiMeters | `core/Database.lua:1311` | |
| PanelMaster | `core/Database.lua:131` | |
| PartyFrameEnhanced | `core/Database.lua:122`; `core/PartyFrameEnhanced.lua:343,363` | |
| PremadeGroupsFilterExtension | `core/PGFE.lua:86` | |
| PrettyChat | `core/Database.lua:184`; `core/PrettyChat.lua:135,143`; `modules/Override.lua:161` | |
| QuickComms | `core/QuickComms.lua:104` | |
| WhatGroup | `core/WhatGroup.lua:307,1276,1279`; `modules/Frame.lua:427,560,1116` | |

**Repos with nothing to change:** LibKa0s, AuraMaster, ConsumableMaster, DpsRace, KickCD, PanelMaster,
PartyFrameEnhanced, PGFE, QuickComms, WhatGroup and SkinTester have no unsafe character in display text. The
LibKa0s close-button `×` (`Core.lua:296`) is safe.

## 3. Test assertions that pin these strings

**For the section 2 changes (the ones that must change):**

- `BankLedger/tests/test_panel_filters.lua:922`: `"\nDatabase size: \226\137\136 "`, and its comment at `:919`.
- `BankLedger/tests/test_constants.lua:155-156`: DirectionGlyph ▲▼. Unchanged under the proposal.
- `LootHistory/tests/test_constants.lua:366`: asserts the DirGlyph value is multibyte (`#>=3`). ↔ still passes;
  ASCII `<>` would fail, so that test would need changing.
- `LootHistory/tests/test_browsertable.lua:931,944`: compare against `C.DirGlyph`, so they follow the constant.
- `LootHistory/tests/test_panel.lua:231` and `BankLedger/tests/test_panel_filters.lua:912,921`: find
  "Database size". Keep that substring.
- No test pins either footer's text: `test_skin_chrome.lua:139,189` checks only the color and the recorded paint.

**Only if the debug arrows change (option B):**

- `LibKa0sSkinTester/tests/test_debuglog.lua:440`
- `AbsorbTracker/tests/test_slashprofile.lua:315,327,346,373`
- `KickCD/tests/test_schema_store.lua:114`, `test_settings_log.lua:409`, `test_units.lua:354`
- `LootHistory/tests/test_profiles.lua:396`
- `MultiMeters/tests/test_database.lua:247`
- `PanelMaster/tests/test_debuglog.lua:470`
- `PrettyChat/tests/test_debuglog.lua:391,406,414,467`
- `WhatGroup/tests/test_debuglog.lua:446`

## 4. Proposed change

1. **LootHistory**, on the feature branch:
   - `modules/Browser.lua:591` becomes `("Database ~%s")`. This fixes image-19.
   - `settings/Panel.lua:149-150` becomes `"Database size: ~" .. FormatBytes .. "  (estimated)"`.
   - `core/Constants.lua:117` sets `MOVE = "\226\134\148"` (↔).
   - `modules/BrowserTable.lua:237` becomes `"Poor to Legendary"`.
   - Update the comments that cite `\226\137\136` (`modules/Browser.lua:587`, `settings/Panel.lua:148`) and the
     `⇄` in the `BrowserTable.lua:38` comment.
   - Add a test asserting that the footer text equals `"Database ~1.6 MB"` for a stubbed size, and that it contains
     no byte >= 0x80.
2. **BankLedger:**
   - `modules/Browser.lua:754` and `settings/Panel.lua:159` become `~`, with their comments (`:750`, `:157-158`).
   - `modules/LedgerTable.lua:70-71` drops the glyphs from the tooltip prose, for example "Deposit means it left your
     bags for the store; Withdraw means it came back out."
   - Update the assertion and comment at `tests/test_panel_filters.lua:919-922`.
3. **Guard against regressions** (recommended). Add a headless test to each of these two addons, or one kit-level
   helper in LibKa0s `tests/_kit` (e.g. `T.assertGlyphSafe(str)`) that checks against an allowlist: ASCII plus the
   safe set in section 1. Call it from the footer, panel and tooltip tests.
4. **Standard** (optional). Add a WowAddonStandards rule: "Display text in a skin face uses only characters every
   shipped face draws. Symbols use textures or the mono face." Back it with a coverage table that the font change
   regenerates.

## 5. Risks

- **The font override.** Under a Font override (any LSM face, `Skin.lua:748`), nothing outside ASCII is
  guaranteed. The safe set in section 1 is safe only for *shipped* faces.
- **A mono face change.** If any skin changes `font.mono` away from JetBrains Mono, these become boxes:
  DropWatcher's `▲ ≈ ▼ ⊘`, the LootHistory and BankLedger `▲▼`, and the debug arrows. Re-run this coverage check
  whenever the mono face changes. Item 7 (removing unused fonts) must keep JetBrains Mono.
- **The ↔ choice.** It relies on mono. If the lead wants pure ASCII, `<>` changes the Direction column's look and
  the multibyte test.
- **A cut-off footer.** `~` is narrower than `≈`, so it carries no risk of a cut-off footer.

## 6. Safe-character counts in display text, per repo

These are drawn by every shipped face, so no change is needed. Debug, error and test lines are excluded.

| Repo | — | … | · | × | – | other |
|---|---|---|---|---|---|---|
| LibKa0s | 39 | 1 | | | | é 1 |
| LibKa0sSkinTester | 23 | | | | | |
| AbsorbTracker | 29 | | | | | |
| AuraMaster | 175 | 11 | | | | |
| BankLedger | 20 | 5 | 6 | 12 | 1 | |
| ConsumableMaster | 71 | 3 | | | | NBSP 1 |
| DpsRace | 27 | 8 | 3 | 75 | | ± 9, › 1, • 1 |
| DropWatcher | 29 | 14 | 68 | | 6 | • 1 |
| KickCD | 45 | 1 | | | | |
| LootHistory | 30 | 6 | 8 | 8 | 1 | § 1 (`'§warband'` is a key, not text), NBSP 1 |
| MultiMeters | 92 | | 2 | | | ’ 3, › 1 |
| PanelMaster | 22 | 4 | | | | ° 4 |
| PartyFrameEnhanced | 41 | | 1 | | | |
| PGFE | 29 | 1 | | | | é ê ü 6 (realm names) |
| PrettyChat | 27 | | | | | NBSP 10, ’ 10, £ ¥ § (Blizzard GlobalStrings) |
| QuickComms | 22 | 18 | 5 | | | |
| WhatGroup | 41 | | | | | |

## 7. Open questions for the lead

1. **Is the target "every shipped face" or "pure ASCII everywhere" (option B)?**
   - Option A, recommended: change only the 7 display sites in section 2, about 6 lines in 2 repos.
   - Option B: also convert the ~1,400 safe characters (mostly `—`) and the debug arrows. That touches every repo
     and about 25 test pins, for no visible gain with shipped faces. It protects only Font-override users.
2. **The LootHistory MOVE glyph:** `↔` in mono (recommended, it keeps the look) or ASCII `<>`?
3. **The guard (section 4.3):** a kit helper in LibKa0s, or per-addon tests? I recommend the kit helper. It is
   library-level, so all addons can use it later, and it costs one revendor.
4. **Prototype has no Cyrillic, and it is Ka0s Default's face.** On a ruRU client, or with Cyrillic player names,
   body text in Ka0s Default will show boxes. It needs a `langmask = { "western" }` registration, as Atkinson has
   (`Media.lua:186-189`), so that LSM or the client falls back. Ask the fonts inventory owner (item 1-4 shipping) to
   set it. The PGFE Russian realm names (`defaults/Realms.lua:537-556`) are lookup keys and are not drawn.
5. **The BankLedger tooltip:** drop the glyph from the prose (recommended), or keep it and draw the tooltip line in
   mono? Mixing faces in a GameTooltip line is not possible without textures.
