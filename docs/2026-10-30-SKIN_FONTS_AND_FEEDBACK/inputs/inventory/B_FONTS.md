# Inventory B_FONTS: items 2, 3, 4, 7 and 13

Read-only inventory, 2026-10-30. Evidence is from the checkouts as they stand now. LibKa0s is at
`feat/2026-10-30-skin-library-followups` HEAD `aefeba9` (v1.81.0, not yet merged; master is `ea1d92d`).
The owner's answers say this run branches from master after that merge, so every line cited below
is the code this run starts from.

## 1. The source files (owner's SharedMedia_MyMedia)

Path: `/mnt/g/.../_retail_/Interface/AddOns/SharedMedia_MyMedia/font/`. `MyMedia.lua:21,29,34` registers them
as LSM `font` keys **`Ka0s Expressway`**, **`Ka0s Fira Sans Medium`** and **`Ka0s Prototype`**. The folder has
no license or readme file (no `Prototype.txt`).

Read with fontTools (`python3 -I`):

| File | SHA-256 | Family / style (name 1/2, 16/17) | OS/2 weight | Version | nameID 0 (copyright) | nameID 13/14 |
|---|---|---|---|---|---|---|
| Ka0s Prototype.ttf (29,592 B) | `ce7f544cfc3f02953f79d065bcd16c8cc0eb041f76fc987ae6adcc3b21005774` | Prototype / Regular | 400 | v2.0; 2001, vendor `MGBF` | "Copyright 2001, free for personal use, freely distributed with Prototype.txt" | none |
| Ka0s Expressway.ttf (99,820 B) | `06a2106170c2b5b736955cc749ed755f3757d103230645158f0bd5b5b91c386b` | Expressway Rg / Bold (typo: Expressway / Bold) | 700 | 2.100, Ray Larabie, vendor `TYPO` | "(c) 2005 Typodermic. Do not distribute. Report Piracy to piracy@typodermic.com. Visit www.typodermic.com"; nameID 7 "Expressway is a trademark of Typodermic" | none |
| Ka0s Fira Sans Medium.ttf (488,960 B) | `7e7acee3fda79ae2cc3ec899f14f7a5b9e988b27a88f31a81a8ad4cb870b8987` | Fira Sans Medium / Regular (typo: Fira Sans / Medium) | 500 | 4.301, bBox Type | "Digitized data copyright 2012-2018, The Mozilla Foundation and Telefonica S.A., bBox Type GmbH and Carrois Corporate GbR, with Reserved Font Name "Fira"" | "Licensed under the Open Font License, version 1.1 or later" / `http://scripts.sil.org/OFL` |

**Siblings for titles.** Prototype has one weight only. The pack holds only the Bold of Expressway. Fira
Sans has Light, Medium, Bold, Heavy and Condensed in the pack. The pack's `Ka0s Fira Sans Bold.ttf` is
4.203, a different build from the pack's Medium. LibKa0s already ships Fira Sans SemiBold 4.203, from
google/fonts at the pinned commit `e345593d` (`tools/artwork/fonts.py`, the firasans entry).

**Fira Sans Medium from google/fonts.** I fetched it at the same pinned commit `e345593d`:
`ofl/firasans/FiraSans-Medium.ttf`, SHA-256 `cbc1842cbed8c1d1146ba7c9db97d8f28c9bedfd25f41c5b0e1259ca48622328`,
457,248 B, version 4.203. It is the same build as the SemiBold LibKa0s already ships. 16 of the 95 ASCII
advances differ slightly from the owner's 4.301 copy. 4.203 also lacks ▲▼▶◀, which 4.301 has.

**Coverage (cmap):**

| | ASCII | Latin-1 | Latin Ext-A | Cyrillic (U+0400-045F) | Greek | Hangul/Han | Langmask that fits |
|---|---|---|---|---|---|---|---|
| Prototype | 95/95 | 93/96 (no ¼½¾) | 9/128 (Łł Œœ Šš Ÿ Žž: enough for fr/de/es/it/pt) | **0** | 3 | 0 | `{ "western" }` |
| Expressway | 95/95 | 93/96 (no ¤ ¬ soft hyphen) | 81/128 | **96/96** | 0 | 0 | `{ "western", "ruRU" }` |
| Fira Sans Medium (both builds) | 95/95 | 96/96 | 128/128 | 96/96 | 121 | 0 | `{ "western", "ruRU" }` |

Symbols that matter to item 5's character sweep:

- Prototype lacks → ← ↑ ↓ ▲ ▼ ▶ ◀ ✓ ✗ − (U+2212) €.
- Expressway lacks the arrows, the triangles, ✓ ✗ ∞ ≈ ≤ ≥ ‰.
- Fira 4.203 lacks ▲▼▶◀ ✓ ✗.
- All three draw – — ‘ ’ “ ” • … · × ° ±.
- **No face draws ✓ ✗ ▲ ▼ ▶ ◀**, so item 5 (and PGFE item 8's "up"/"down") should use icons or ASCII, not these.

## 2. The license question (items 2 and 3): lead must surface this to the owner

The owner said: "I am not making money off this addon so License should be fine." The files say otherwise
for two of the three:

- **Expressway**: the file itself says *"Do not distribute"*. Typodermic's license page says embedding in
  "software, apps, games" is excluded from the free Desktop EULA. It says explicit rights are needed for
  "PC or console games ... open-source software". It also excludes "Giving the font to ... another legal
  entity" ([typodermicfonts.com/license](https://typodermicfonts.com/license/)). Reported summaries of that
  page say an Application License is needed "whether your software is commercial or free". I could not
  confirm that exact quote on the page itself. Retailers sell Expressway's app license separately
  ([Fonthaus](https://www.fonthaus.com/fonts/Typodermic/Expressway/TPD50101),
  [Font Squirrel license](https://www.fontsquirrel.com/license/expressway)). Non-commercial use does not
  cure this. A CurseForge upload is a redistribution to every player.
- **Prototype**: "free for personal use, freely distributed with Prototype.txt". 1001fonts lists it as not
  free for commercial use, and the author is at mickeyavenue.com (recorded in
  `docs/2026-10-28-SKIN_OVERRIDES_AND_PICKER/SO06_KA0S_DEFAULT_MEDIA.md:26-29`). CurseForge pays authors,
  and the required `Prototype.txt` is not in the pack. The owner already ruled once against shipping it
  (SO06 "Update, 2026-10-28: free art instead", the source of Oxanium). This request reverses that ruling.
- **Fira Sans Medium**: SIL OFL 1.1. Shipping it unmodified is fine. Its Reserved Font Name "Fira" only
  binds a modified version, so the bytes must not be instanced or renamed.

**Options for the lead (recommendation: B, unless the owner re-confirms A after reading the two quotes above):**

- **A. Ship all three as asked.** Record the risk in the bundle. Each non-OFL file gets a license file that
  quotes its embedded notice verbatim. Expressway's would then read "Do not distribute" while being
  distributed.
- **B. Ship Fira Sans Medium; name Prototype and Expressway by LSM key without shipping them.** The skins
  set `font.body = "Ka0s Prototype"` and the rest, which the owner's pack (or any player's) resolves. A new
  per-face fallback in `lib.FONTS` (`fallback = "Ka0s Oxanium SemiBold"` for Prototype; an OFL face for
  Expressway) is drawn when LSM cannot resolve the key. Under B, Oxanium stays, and so does one OFL
  stand-in for Obsidian, so item 7's deletion list shrinks (section 6). Cost: players without the pack see
  the stand-in, and item 5's width baseline must be met by both faces.
- **C. Ship Fira, and find OFL look-alikes for Expressway and Prototype**, as SO-06 did with Oxanium.

The rest of this report details **A** (the owner's literal ask) and notes where B differs.

## 3. Fonts in LibKa0s today (every place)

**Catalog**, `LibKa0s/LibKa0s/Media.lua:168-195` (`lib.FONTS`), 17 entries:

- `JetBrains Mono`.
- `Ka0s Inter`, `Ka0s Inter SemiBold`.
- `Ka0s Nunito`, `Ka0s Nunito SemiBold`.
- `Ka0s Vollkorn`, `Ka0s Vollkorn Bold`.
- `Ka0s Bitter`, `Ka0s Bitter Bold`.
- `Ka0s Philosopher`, `Ka0s Philosopher Bold`.
- `Ka0s Fira Sans`, `Ka0s Fira Sans SemiBold`.
- `Ka0s Atkinson`, `Ka0s Atkinson Bold`.
- `Ka0s Oxanium SemiBold`, `Ka0s Oxanium Bold`.

The comment block at `Media.lua:139-166` names every family and says that all of them are OFL. `lib.Font`
is at `Media.lua:422-428`. `fontLangmask` and `RegisterLSM` are at `:453-557`. `registerOne` skips a key
LSM already holds (`:441`), so on the owner's client whichever copy registers first wins.

**Files**, `LibKa0s/LibKa0s/media/fonts/`: 17 TTFs plus 9 `<Family>-OFL.txt` files.

**Provenance**, `tools/artwork/fonts.py`: the docstring (`:1-45`) and `FAMILIES` (`:66-166`). Inter, Nunito,
Vollkorn, Bitter and Oxanium are instanced from variable fonts. Philosopher, Fira Sans and Atkinson are
copied. JetBrains Mono came from Mythic Meters and is not in fonts.py. The cache at
`tools/artwork/.cache/fonts/` also holds the retired alegreya, barlow and cinzel directories (not shipped).

**Skins**, `LibKa0s/LibKa0s/SkinDefs.lua`:

- Ka0s Default: `font.body` Oxanium SemiBold, `font.title` Oxanium Bold, `font.mono` JetBrains Mono,
  `font.outline ""`, `font.shadow true` (`:234-236`); sizes 12/14 (`:279`); `hud.font` Oxanium SemiBold,
  `hud.outline "OUTLINE"` (`:336-337`).
- `KEEP` = Friz for body and title, for WoW Default (`:557-558`).
- `HUD_FACE` per skin (`:593-597`): obsidian Inter SemiBold, forever Fira Sans SemiBold, and so on.
- Obsidian `font = "Ka0s Inter", tfont = "Ka0s Inter SemiBold"` (`:611`).
- Azeroth Vollkorn (`:659`), Glass Nunito (`:705`), High Contrast Atkinson (`:757`), Ember Bitter (`:806`),
  WoW Midnight Philosopher (`:918`).
- WoW Forever `font = "Ka0s Fira Sans", tfont = "Ka0s Fira Sans SemiBold"` (`:969`).
- The `DEFS_MINOR` history comments `:62-105` name faces.
- The header line `:17-18` ("Ka0s Default leaves every font token nil") has been stale since minor 8. Fix it
  in passing.
- The eui source (`SkinEUI.lua:108,314-315`) takes body and title from EllesmereUI and inherits `hud.font`
  from Ka0s Default, so it follows whatever Ka0s Default draws.

**Code comments that name Oxanium** (prose only): `Widgets.lua:83`, `WidgetsAutocomplete.lua:53`,
`WidgetsDragHandle.lua:63`, `WidgetsLineChart.lua:38`, `SimPanel.lua:76`, `PerfPanel.lua:19`,
`DebugLogWindow.lua:34`.

**Tooling**: `tools/skin_gallery.py:52-53` loads `Inter-SemiBold.ttf` for the gallery's labels and titles.
**It breaks if Inter is deleted.** Switch it to `FiraSans-SemiBold.ttf`.

**Docs**:

- `README.md:137` (Media row: "seventeen SIL OFL faces ... Oxanium") and `:138` (Skin row: "draws Oxanium").
- `README.md:327-329` (the tree).
- `README.md:444-466` (the credits: "all SIL OFL 1.1").
- `DEPENDENCIES.md:110,119` (fontTools instancing list).
- `docs/api/README.md:189,201` (version index).
- `docs/api/Media/version-9.1-docs.md` (current).
- `docs/api/Skin/version-8.16.12.6.10.2.4-docs.md` (current).
- `docs/api/CONSUMERS.md:104`.
- `docs/test-cases.md:494,497,652`.

Superseded `docs/api/*/version-*` files and `docs/automated-tests/*` are frozen; leave them.
`LibKa0s/LICENSE` (MIT) and `LibKa0s/LibKa0s/LICENSE` say nothing about fonts.

**LibKa0s tests that pin font names:**

- `tests/test_media.lua`:
  - `:197` licenses.
  - `:404` "13" ruRU faces.
  - `:437,480,505,525` count 17.
  - `:540-567` SKIN_FACES, INSTANCED, OXANIUM.
  - `:570` the count of 17.
  - `:611-629`: asserts **every** license file contains "SIL Open Font License, Version 1.1". That goes red
    for any non-OFL face.
  - `:631` uses `Ka0s Inter` as the RegisterLSM example.
- `tests/test_skin.lua:139-141`: Ka0s Default's three faces.
- `tests/test_skin_defs.lua:406,470-477,503-505,524-538`: per-skin faces, HUD_FACE, the "Oxanium stays
  Ka0s Default's" test.
- `tests/test_skin_override.lua:66,145,189,216-234,404-463`: Ka0s Default's Oxanium SemiBold as the
  expected skin face.
- `tests/test_options_appearance.lua:630`: "Skin's own (Ka0s Oxanium SemiBold)".
- `tests/test_options_chrome_skin.lua:33`.
- Arbitrary keys in a fake LSM: `Ka0s Inter` and `Ka0s Fira Sans` in `fixture_skin_ace.lua:31`,
  `test_options_appearance.lua:602-796`, `test_options_compose_skin.lua:142-216`,
  `test_options_skin_picker.lua:42,648,664`, `test_skin_override.lua:25-257`,
  `test_skin_owner_tokens.lua:161`. These do not depend on the catalog, so they stay green. Rename them to
  a shipped key for clarity.

## 4. Font keys in the addon repos (outside libs/)

Searched across every roster addon, LibKa0sSkinTester, WowAddonStandards and dev-copilot.

- **Shipped code, one site:** `QuickComms/core/SkinSetup.lua:160`, `NS.SKIN_FALLBACK["hud.font"] = "Ka0s
  Oxanium SemiBold"`. This is the degraded-arm copy of Ka0s Default. QuickComms' drift test holds it to the
  live library, so it goes red on the re-vendor. Change it to Ka0s Default's new HUD face.
- `AuraMaster/modules/FontPrimer.lua:17` names "Ka0s Prototype" in a comment, as the owner's pack face.
- **No addon default, schema value or migration names a skin face.** HUD `font` defaults are `Friz Quadrata
  TT` (from `OptionsCompose.lua:642`) or FROM_SKIN.
- **Addon tests that assert Ka0s Default's Oxanium** go red on the re-vendor:
  - `KickCD/tests/test_skin_hud.lua:126,235,239,267-293`.
  - `ConsumableMaster/tests/test_skin_hud.lua:21,151`.
  - `PartyFrameEnhanced/tests/test_skin_hud.lua:99,132,147,166`.
  - `QuickComms/tests/test_skin_hud.lua:23,32,146`.
  - `LibKa0sSkinTester/tests/test_showroom_hud.lua:53-99`: Obsidian's `Ka0s Inter SemiBold`, Ka0s Default's
    Oxanium; `:85` Ember's Bitter Bold stays.
  - `LibKa0sSkinTester/tests/test_mediasetup.lua:308-313`: "Ka0s Default's faces are Oxanium, and the
    vendored copy ships them".
  - `MultiMeters/tests/test_settings_pin.lua:118,130,172,195,223`: the sorted catalog list in five font
    pickers.
  - Prose and test names only, which stay green but go stale: `DpsRace/tests/test_skin_hud.lua:140` (the
    name only), `LootHistory/tests/test_libka0s.lua:886` (a comment).
- **Override strings in tests** (stored and read back; green either way, but stale names):
  - `WhatGroup/tests/test_skinsetup.lua:187-197` (`Ka0s Oxanium Bold`).
  - `PartyFrameEnhanced/tests/test_skinsetup.lua:155-201`.
  - `AuraMaster/tests/test_skinsetup.lua:255-342` ("Oxanium").
  - `PrettyChat/tests/test_skinsetup.lua:175-272` ("Oxanium").
- **Docs.** Every addon README's Credits section names Oxanium and Inter, for example
  `AbsorbTracker/README.md:144-155`. The 15 addon READMEs are AbsorbTracker, AuraMaster, BankLedger,
  ConsumableMaster, DpsRace, DropWatcher, KickCD, LootHistory, MultiMeters, PanelMaster,
  PartyFrameEnhanced, PremadeGroupsFilterExtension, PrettyChat, QuickComms and WhatGroup. Some also name
  the face in FAQ prose, for example `AbsorbTracker/README.md:86` ("the number in the Oxanium font").
  Living docs naming Oxanium: ARCHITECTURE.md in 13 addons, `KickCD/docs/schema.md`,
  `DpsRace/docs/settings-panel.md`, `ConsumableMaster/docs/macro-bar.md`,
  `QuickComms/docs/known-limitations.md`, `WhatGroup/docs/module-map.md`. Each `docs/smoke-tests.md` also
  names it. Those are records, so add new checks rather than rewrite old ones.
- **Standard**:
  - `WowAddonStandards/standards/standards/library-stack.md:428-433` still describes the v1.78.0 faces
    (Barlow, Cinzel, Atkinson, "Each ships ... SIL Open Font License 1.1"). It is already stale, and it
    breaks its own `:424` rule ("enumerate these, never hard-code a list").
  - `debug-logging.md:41-43`: JetBrains Mono is a MUST, so keep it.
- **SavedVariables** (both accounts, account and character files): **no stored `Ka0s Inter*`, `Ka0s
  Oxanium*` or `Ka0s Fira Sans` key anywhere.** `"Ka0s Prototype"` is stored by AuraMaster (137 times),
  KickCD (2) and MultiMeters (5), all from the owner's pack, and it keeps resolving.
- **No release ever shipped a skin face.** The last addon tags (`*-1.x.0-release`, 2026-10-09) carry only
  `JetBrainsMono-Regular.ttf` under `libs/LibKa0s/media/fonts/` (checked for LootHistory, AuraMaster,
  MultiMeters and KickCD). The skin faces exist only in unreleased dev builds.

**Is JetBrains Mono used? Yes. Keep it.** Ka0s Default's `font.mono` is used by the debug console, perf
and sim panels (`SkinPaint.lua:460`). It is also `AbsorbTracker/core/Constants.lua:30,35`, DpsRace's clocks
(`DpsRace/tests/test_skin_hud.lua:154`), and the MUST in `debug-logging.md:43`.

## 5. Proposed catalog and skin faces (option A)

**New `lib.FONTS` entries** (Media minor 10). Keys are the pack's own LSM names, so a player who runs the
pack gets one dropdown entry, and the owner's stored "Ka0s Prototype" resolves unchanged:

| Key | File | License file | langmask | Source |
|---|---|---|---|---|
| `Ka0s Prototype` | `Prototype-Regular.ttf` (byte copy) | `Prototype-LICENSE.txt` | `{ "western" }` | the pack, sha `ce7f544c…` |
| `Ka0s Expressway` | `Expressway-Bold.ttf` (byte copy) | `Expressway-LICENSE.txt` | `WEST_RU` | the pack, sha `06a21061…` |
| `Ka0s Fira Sans Medium` | `FiraSans-Medium.ttf` | `FiraSans-OFL.txt` (existing) | `WEST_RU` | google/fonts `e345593d`, sha `cbc1842c…` (recommended: matches the shipped SemiBold's 4.203 build and has a pinned provenance). Alternative: the pack's 4.301 bytes, sha `7e7acee3…` |

Add a `terms` field to every entry (`"OFL-1.1"`, `"personal-use"`, `"proprietary"`). Then the license test
can assert the OFL text only where `terms == "OFL-1.1"`, and the verbatim notice for the others.

The license files should hold:

- **Prototype-LICENSE.txt**: nameID 0 verbatim, the 1001fonts and mickeyavenue.com note, "Prototype.txt not
  available; the notice above is the font's only stated terms", and the owner's ruling with its date.
- **Expressway-LICENSE.txt**: nameIDs 0 and 7 verbatim, the Typodermic license URL, and the owner's ruling.

**Faces per skin** (SkinDefs minor 17):

| Skin | body (`font.body`) | titles (`font.title`) | HUD (`hud.font`) | Note |
|---|---|---|---|---|
| Ka0s Default (`KA0S`, `:234,336`) | Ka0s Prototype | Ka0s Prototype | Ka0s Prototype | One weight; titles differ by size (14 vs 12). The eui source inherits the HUD face. |
| Obsidian (`:611`, HUD_FACE `:594`) | Ka0s Expressway | Ka0s Expressway | Ka0s Expressway | Bold only, so body text reads heavy. Item 5 must size it (xAvgCharWidth 516 vs Prototype 447). |
| WoW Forever (`:969`, HUD_FACE `:596`) | Ka0s Fira Sans Medium | Ka0s Fira Sans SemiBold (kept) | **recommend** Ka0s Fira Sans SemiBold (kept, the R-4 rule: the HUD takes the heavier weight under OUTLINE) | Alternative: Medium everywhere if the owner meant "every Forever string". |

Also update the `SkinDefs.lua` header comments (`:17-18,62-105`, the per-skin blurbs `:608,963-964`) and the
`Media.lua:139-166` block. The comment that says the faces are all OFL becomes false.

## 6. Fonts no skin uses afterwards (item 7)

Under option A:

- **Delete**: `Ka0s Inter` and `Ka0s Inter SemiBold` (`Inter-Regular.ttf`, `Inter-SemiBold.ttf`,
  `Inter-OFL.txt`); `Ka0s Oxanium SemiBold` and `Ka0s Oxanium Bold` (`Oxanium-SemiBold.ttf`,
  `Oxanium-Bold.ttf`, `Oxanium-OFL.txt`); `Ka0s Fira Sans` (`FiraSans-Regular.ttf`; `FiraSans-OFL.txt`
  stays).
- **Keep**: JetBrains Mono, Nunito ×2, Vollkorn ×2, Bitter ×2, Philosopher ×2, Atkinson ×2, Fira Sans
  SemiBold.
- **Add**: Prototype, Expressway, Fira Sans Medium.
- **Result**: 15 faces (17 − 5 + 3). 12 of them reach ruRU (JetBrains, Expressway, Fira ×2, Nunito ×2,
  Vollkorn ×2, Bitter ×2, Philosopher ×2). Three are western only (Prototype, Atkinson ×2).

Under option B, keep Oxanium SemiBold (and Bold if it is the title fallback) as Prototype's stand-in, and
one OFL stand-in for Expressway. The current Inter SemiBold is the nearest one shipped.

**Migration of saved profiles naming a deleted key: none needed. Recommend no migration code.**

- No public release ever shipped these keys (section 4), and the owner's SavedVariables name none of them.
- A dev profile that still holds one is already covered:
  - A font override that LSM cannot resolve is dropped, so the skin's own face stands
    (`Skin.lua:738-743`, `withOverrides`). `GetOverride` still answers the stale name, and the Skin tab's
    dropdown shows it.
  - A HUD element's stored `font` goes to `LSM:Fetch`, which answers LSM's default face.
- If the lead wants belt and braces: a one-shot clear in `Skin:RegisterOwner` when `opts.media.font` is in a
  `RETIRED_FONTS` set. Item 1's "reset overrides on a skin change" also clears a stale override at the next
  skin pick.

## 7. Every place that must change (items 2, 3, 4 and 7)

**LibKa0s** (one item each, or one combined):

1. `media/fonts/`: add the 3 TTFs and 2 license files; delete the 5 TTFs and 2 OFL files listed in section 6.
2. `Media.lua`: `FONTS` (`:168-195`), the comment block (`:139-166`), a minor bump to 10, the `terms` field.
3. `tools/artwork/fonts.py`:
   - Drop the inter and oxanium families.
   - Add `FiraSans-Medium.ttf` to the firasans `files` and `ship` with its sha, and drop
     `FiraSans-Regular.ttf`.
   - Add a "local" source kind for Prototype and Expressway: a recorded source path in the owner's pack and
     its sha-256, verified, copied unchanged, the license file written from a template.
   - Rewrite the docstring ("all SIL OFL" stops being true) and the module docstring's "WHY THESE".
4. `SkinDefs.lua`: KA0S faces, Obsidian, Forever, HUD_FACE, the comments, a minor bump to 17.
5. `tools/skin_gallery.py:52-53`: switch from Inter to FiraSans-SemiBold.
6. Tests:
   - `test_media.lua`: counts 17→15 and 13→12, SKIN_FACES, INSTANCED (only Nunito, Vollkorn and Bitter
     remain), the conditional license test, a test that the non-OFL notice is verbatim, the
     RegisterLSM('X') example.
   - `test_skin.lua:139-141`, `test_skin_defs.lua` (faces, HUD_FACE, the `:524` test renamed to Prototype).
   - `test_skin_override.lua` and `test_options_appearance.lua:630`. Better still, read
     `Skin:ResolveSkin("ka0s")["font.body"]` into a local, so the next face change touches one line.
   - `test_options_chrome_skin.lua:33`, and the fake-LSM renames.
7. Docs:
   - README `:137,138,327-329,444-466`: a new "Fonts" credits block saying which faces are not OFL, and
     their terms.
   - `DEPENDENCIES.md:110,119`.
   - New `docs/api/Media/version-10-docs.md`, a new Skin docs version, `docs/api/README.md` rows,
     `CONSUMERS.md:104`, `docs/test-cases.md`, CHANGELOG.
8. Code comments that name Oxanium (section 3 list): replace them with "the body face".

**Every addon** (on the re-vendor):

- Fix the red tests listed in section 4.
- `QuickComms/core/SkinSetup.lua:160`.
- The README Credits (15 repos): drop Oxanium and Inter, add Prototype and Expressway with their terms, and
  Fira Sans Medium.
- The FAQ and ARCHITECTURE prose that names Oxanium.

**LibKa0sSkinTester**: `tests/test_showroom_hud.lua`, `tests/test_mediasetup.lua:308-313`, smoke-tests
additions. Its README has no font credits (checked).

**WowAddonStandards**:

- `library-stack.md:428-433`: stop naming faces (point at `FONTS`).
- Restate the license rule: "each face ships with a file recording its terms". Under A it can no longer say
  OFL. This is a standard decision.
- CHANGELOG and version bump.

## 8. Item 13: font outline

**Today:**

- **Window, panel and tool-window strings** go through `P.font` (`SkinPaint.lua:547-570`), which sets
  `flags = T["font.outline"] or ""` (`:563`). Every skin inherits Ka0s Default's `font.outline = ""`
  (`SkinDefs.lua:236`), so none is outlined. `ownerFont` caches one font object per owner, role, size and
  shadow, not per flags (`SkinPaint.lua:463-482`). It calls `SetFont` with the current flags each time.
- **HUD, the skin side**: `hud.outline = "OUTLINE"` in every skin (`SkinDefs.lua:337`). It is read by:
  - `S.BarStyle().outline` (`SkinPaintExtras.lua:471,477`).
  - `ConsumableMaster/modules/MacroBarButton.lua:166-167`, which falls back to OUTLINE on nil.
  - `LibKa0sSkinTester/modules/ShowroomHud.lua:49,57`.
  - `Skin:Resolve(owner, "hud.outline", ...)`.
- **HUD, the addon side**: every addon's HUD text uses its own stored `fontFlags` from the canonical
  FontGroup row (`OptionsCompose.lua:653-656`, default `"OUTLINE"`, values at `:116-123`). That row has
  **no** `FromSkin` companion; only `font`, `borderStyle` and `barTexture` follow the skin (`:330-337`).
  - Stored defaults: AuraMaster `defaults/Profile.lua:135` OUTLINE (the flag is mapped in `Style.lua:1054`),
    KickCD `defaults/Profile.lua:196` and `settings/*` OUTLINE, PFE OUTLINE, QuickComms
    `defaults/PadStyle.lua:38-103` OUTLINE, AbsorbTracker OUTLINE, DpsRace `""` (`defaults/Profile.lua:89-124`),
    MultiMeters `text.outline` and `header.outline` "NONE" (`core/Database.lua:991`, `modules/Row.lua:781`).
  - BankLedger and LootHistory hold the flags of their insight cards locally.
  - AbsorbTracker's `core/Data.lua:194` says outright that size and outline stay the player's.
- **Ignore fonts**:
  - `P.font` gives the string its own face back (`SkinPaint.lua:549`, `P.unfont` restores the saved
    flags).
  - `Token` answers nil, and `Resolve` the stored value, for `hud.font` and `hud.outline`
    (`Skin.lua:651-658,836-839,896-903`; `skinning.md:92`).

**Proposed design:**

- **Storage.**
  - A per-owner mode on the Skin registration: `o.outline` ∈ `"all" | "hud" | "off"`, default `"all"`.
  - New `Skin:GetOutline(owner)` and `Skin:SetOutline(owner, mode)`, which repaint and notify like
    `SetIgnore` (`Skin.lua:623`).
  - Seeded by `RegisterOwner` `opts.outline`.
  - Persisted through the host write seam: `WriteChoice`'s `media` table gains `outline`
    (`Skin.lua:474-484` normalizes it), so the call keeps its shape and "Copy to every Ka0s addon"
    (`OptionsAppearance.lua:237-241`) carries it.
  - Each addon adds `skin.outline = "all"` to its `defaults/Profile.lua` skin block. It also adds a
    skip-render schema row with values `all/hud/off`, which gives `/xx set skin.outline hud`, and stores and
    reads it in `core/SkinSetup.lua`. That is all 16 addons. Each addon's test that counts "the seven skin
    keys" moves to eight.
- **Resolution, in one place.** Apply the mode in `Skin.lua`'s overrides layer (`withOverrides`,
  `:738-755`; add the mode to its cache key). Let `flag = base["hud.outline"]` if it is non-empty, else
  `"OUTLINE"`:

  | Mode | `font.outline` | `hud.outline` |
  |---|---|---|
  | `all` | `flag` | `flag` |
  | `hud` | `""` | `flag` |
  | `off` | `""` | `""` |

  `ResolveSkin` stays raw for the picker. `P.font`, `BarStyle`, `Token` and every host reading `hud.outline`
  then follow with no code of their own. `ConsumableMaster:166` already treats `""` correctly.
- **The UI.** A dropdown in the Skin tab, "Font outline applies to" (All text / HUD text only / Off),
  placed in the Font and texture section (`OptionsAppearance.lua:465-473`) or under Scope (`:475-486`).
  It is disabled with a hint while Ignore fonts is on.
- **Interplay.**
  - **Ignore fonts wins.** It is already checked before tokens in `P.font` and `hudFontIgnored`, so no
    outline is applied to the addon's text.
  - **Ignore settings panel**: panel strings stay stock, so no outline there.
  - **A font override** is independent of the mode.
  - **Item 1's reset on a skin change** does not touch the mode; it is a preference, not an override.
- **Addon-stored `fontFlags`: recommend that the stored value wins.** It is an explicit per-element pick
  with no follow-the-skin companion, and this matches R-1, "the host's own setting stands". Consequence: Off
  and HUD-only do not remove the OUTLINE that AuraMaster, KickCD and the others store by default, so the
  setting mostly governs window text plus the HUD sites that read `hud.outline`. If the owner expects Off to
  strip every HUD outline, the fix is a `fontFlags` FromSkin family (`OptionsCompose.lua:340` pattern,
  token `hud.outline`, companion "Use the skin's outline"). That touches every FontGroup and every profile.
  Recommend filing it as a follow-up issue, not doing it in this run.
- **Tests (LibKa0s):**
  - `test_skin_override.lua` or a new `test_skin_outline.lua`: the mode table above; the default `all`;
    Ignore fonts wins; `WriteChoice` carries `media.outline`; copy-to-all carries it; `ResolveSkin` is
    unaffected; a `SetOutline` repaint re-flags a recorded string.
  - `test_options_appearance.lua`: the dropdown and its disabled state.
  - `test_skin_paint.lua`: `P.font` passes OUTLINE under `all`.
  - Per addon: the skin-key count and the write-seam round trip.

## 9. Risks

- **Licensing** (section 2): the biggest risk. The other font risks are smaller.
- **ruRU.** Ka0s Default is the default skin. With Prototype (no Cyrillic) a Russian client falls back to its
  own font, where today's Oxanium is western only too, so this is no regression. Under B, the fallback must
  also be western-masked.
- **Fira Sans Medium build.** If 4.203 ships from google, the owner's client may draw the pack's 4.301
  (whichever registers first, `Media.lua:441`). The widths differ slightly between what the owner sees and
  what players see. Use the pack's 4.301 bytes only if the owner wants exact parity.
- **OUTLINE widens strings.** OUTLINE as the default ("all") thickens strokes and adds width. **Item 5's
  width calibration must be measured with outline on**, so sequence item 13 before item 5's sizing.
- **The mono role.** Under "all", the debug console and perf tables (JetBrains Mono) also get OUTLINE, which
  can clog small digits.
- **Expressway** has only a Bold weight, so Obsidian has no lighter body.

## 10. Open questions for the lead

1. **The license option: A, B or C?** Recommend B. If the owner re-confirms A after reading the
   Typodermic and Prototype terms, record the ruling verbatim in the bundle and in each license file.
2. **The Fira Sans Medium source**: google 4.203 pinned or the pack's 4.301? Recommend google, to match the
   SemiBold build and keep provenance.
3. **WoW Forever titles and HUD**: SemiBold or Medium? Recommend SemiBold for both.
4. **Ka0s Default and Obsidian titles**: the same face as body, distinguished by size. There is no other
   weight, so accept it.
5. **Outline versus a stored `fontFlags`**: should the stored value win? Recommend yes, with a filed issue
   for a FromSkin companion on the flags.
6. **Does "All text" include the mono role?** Recommend yes for consistency, but this is low stakes.
7. **Where the outline is stored**: in `WriteChoice`'s `media` table, or in a new sixth argument?
   Recommend `media`.
8. **Migration for deleted keys**: none, or a one-shot clear? Recommend none.
