# C_FONT_METRICS: item 5, equal text width across skins

Read-only inventory. LibKa0s on `feat/2026-10-30-skin-library-followups` at `aefeba9` (v1.81.0). The
script is `plan-data/font_metrics.py` and its output is `plan-data/font_metrics.txt` (sections 1-8 are
cited as §n below). It runs as `<venv>/bin/python -I plan-data/font_metrics.py`. The system python3 has
no fontTools, so I used a scratch venv with fontTools 4.68, uharfbuzz and Pillow.

## 1. How sizes are consumed today

- **Body and title: one size token per skin per role, applied relatively.** `P.fontSize`
  (LibKa0s/SkinPaint.lua:523-532) returns `stock * skin[token] / KaosDefault[token]`. `FONT_ROLE`
  (SkinPaint.lua:457-461) maps body to `font.bodySize` and title to `font.titleSize`. Mono also maps to
  `font.bodySize`, but no caller uses the mono role, so it is latent. Each skin sets the two tokens
  through its mock entry's `fs` and `titleSize` (MOCK_MAP, SkinDefs.lua:457-458):
  - obsidian at :611
  - azeroth at :659
  - glass at :705
  - contrast at :757
  - ember at :806
  - wow at :861
  - midnight at :918
  - forever at :969

  The reference is Ka0s Default's 12 and 14 (SkinDefs.lua:279). Equalizing therefore means changing
  only those `fs`/`titleSize` numbers, and every window string scales with them.
- **A font override keeps the skin's sizes.** Skin.lua:679-681: an override replaces the face, and
  `font.mono` and every size stay the skin's (test_skin_override.lua:64). An overridden face is
  therefore not width-equalized.
- **HUD text does not take its size from the skin.**
  - `hud.fontSize` is 12 in every skin: SkinDefs.lua:336, pinned by test_skin_defs.lua:519.
  - Only `S.BarStyle().fontSize` (SkinPaintExtras.lua:476) and the Skin Tester's showroom
    (LibKa0sSkinTester/modules/ShowroomHud.lua:4) read it.
  - Each addon's HUD element stores its own `fontSize` (OptionsCompose FontGroup, :645-648, default 12).
  - "Use the skin's font" governs the face only (`FROM_SKIN.font`, OptionsCompose.lua:331, has no
    `sizeToken`).
  - The face sites that would need a size scale are in 8 addons:
    - AbsorbTracker core/Data.lua:138
    - AuraMaster modules/Style.lua:1052-1056 (`Style.FontKey`)
    - ConsumableMaster modules/MacroBarButton.lua:153-175
    - DpsRace modules/Hud_Appearance.lua:44
    - KickCD modules/Castbar_Skin.lua:165, IconGrid_Render.lua:864/894 and UnitLabel.lua:95
    - MultiMeters modules/Row.lua, Window_Header.lua and Tooltip.lua
    - PartyFrameEnhanced modules/Element.lua
    - QuickComms modules/Pad_Render.lua

## 2. How WoW sizes and lays out text (verified)

- `SetFont(path, h)` sets the **em** to `h` UI units. Every face in §1 has an upm of 1000, except Inter
  at 2048. Width is therefore the sum of advances divided by upm, times h.
- I measured ink widths of 5 strings in image-17 (Prototype), image-18 (Expressway) and image-28 (Fira
  Sans Medium), all at fs 12 (§6). A **linear** em layout cannot fit them: it leaves Expressway 4-5 px
  short (rms 2.3 px). Snapping **each glyph advance up to a whole pixel at 1.0 px per UI unit** fits all
  15 measurements with an rms of 0.78 px.
- So the owner's client pixel-snaps advances. Narrow faces gain the most from snapping: Expressway at
  12 renders about 2-5% narrower than Prototype, not the 6% that linear predicts. "Silvermoon City"
  measures 88 px in Expressway and 87 px in Prototype.
- Snapping depends on each player's effective pixel size. Every size below is therefore checked under 6
  layout models (§7, §8): linear; ceil at 1.0 (the owner's); round at 1.08; ceil at 1.25; round at 1.5;
  round at 1.875 (1440p with the UI scale off).
- **The owner's client replaces the Friz Quadrata file.** `_retail_/Fonts/FRIZQT__.TTF`, ARIALN,
  FRIENDS, MORPHEUS and skurri all have the same md5 as `Ka0s Prototype.ttf` (0483b4ee...).
  - In the owner's client, "WoW Default" and all of Blizzard's own text draw Prototype.
  - Real Friz Quadrata is not on disk, so WoW Default can only be measured as Prototype here.
- The corpus (font_metrics.py `BODY`/`TITLE`/`HUD`):
  - Body: every LootHistory tab, filter, header and row string in image-17, the footer and LibKa0s's
    settings labels.
  - Title: addon titles and section headings.
  - HUD: digits, short names and numbers.
- Widths are HarfBuzz-shaped, with kerning on.

## 3. Result: the table

The faces are the new ones: Ka0s Default Prototype, Obsidian Expressway, WoW Forever Fira Sans Medium
(body, title and HUD alike). The other skins keep their current faces, with HUD on HUD_FACE's heavier
weight (SkinDefs.lua:592-596).

- **Ratio** is the face's average advance per em divided by Prototype's (linear; §2).
- **Error** is the range of (width / Ka0s Default's width − 1) over the 6 layout models. A positive
  error means wider, which truncates first.

| Skin | Face | Now fs / ts / hud | Width ratio body / title / hud | Error at today's sizes with the new face (body) | **Proposed fs / ts / hud** | Body err % | Title err % | HUD err % |
|---|---|---|---|---|---|---|---|---|
| Ka0s Default | Prototype | 12 / 14 / 12 | 1 / 1 / 1 | 0 | **12 / 14 / 12** (baseline) | 0 | 0 | 0 |
| Obsidian | Expressway (the Bold cut) | 12 / 14 / 12 | 0.939 / 0.942 / 0.935 | −6.4..−4.8 | **12.5 / 14.5 / 13** | −2.9..−1.6 | −2.9..−0.3 | +0.9..+1.8 |
| Azeroth | Vollkorn / Vollkorn Bold | 13 / 14 / 12 | 0.987 / 1.075 / 1.066 | +4.5..+7.3 | **12 / 12.5 / 11** | −1.6..−0.1 | −4.0..−2.5 | −2.5..−0.2 |
| Glass | Nunito / Nunito SemiBold | 12.5 / 14 / 12 | 1.024 / 1.034 / 1.065 | +4.6..+7.4 | **11.5 / 13 / 11** | −2.6..−1.8 | −5.3..−2.8 | −3.6..−1.3 |
| High Contrast | Atkinson / Atkinson Bold | 13.5 / 15 / 12 | 0.992 / 1.074 / 1.074 | +10.5..+12.9 | **12 / 13 / 11** | −1.8..+0.3 | −1.5..+1.9 | −2.9..−0.6 |
| Ember | Bitter / Bitter Bold | 12 / 13.5 / 12 | 1.040 / 1.076 / 1.075 | +3.3..+4.6 | **11.5 / 12.5 / 11** | −1.3..+1.2 | −4.9..−2.4 | −2.2..+0.2 |
| WoW Default | Friz (Prototype on the owner's client) | 12 / 14 / 12 | 1 / 1 / 1 (owner's client only) | 0 | **12 / 14 / 12** (unchanged; see Q4) | 0 | 0 | 0 |
| WoW Midnight | Philosopher / Philosopher Bold | 12.5 / 14 / 12 | 0.959 / 1.012 / 1.006 | −1.2..+1.3 | **12.5 / 13.5 / 12** | −1.2..+1.3 | −4.2..−1.4 | −0.8..+1.2 |
| WoW Forever | Fira Sans Medium | 12 / 14 / 12 | 1.004 / 1.012 / 1.007 | −0.5..+0.6 | **12 / 13.5 / 12** | −0.5..+0.6 | −2.5..−0.7 | −0.3..+1.5 |

**Selection rule (§8 `REC`).** For each role I took the 0.5 step with the smallest worst-case error over
the 6 models. When that step ran more than 2% wide under any model, I stepped it down by 0.5. Wide is the
direction that truncates. Where that step-down happened, the step above was:

| Skin | Role | Step above | Its error % |
|---|---|---|---|
| Obsidian | body | 13 | +1.6..+2.5 |
| Obsidian | title | 15 | +0.7..+2.4 |
| Azeroth | title | 13 | −0.2..+2.4 |
| Glass | title | 13.5 | −0.7..+2.1 |
| Ember | title | 13 | −0.2..+3.0 |
| WoW Midnight | title | 14 | +0.7..+2.3 |
| Glass | HUD | 11.5 | +0.6..+2.1 |

**The owner's screenshot agrees.** image-20 (Azeroth at fs 13) truncates "Warband Withd..." and
"Sacrilege-Frostmour...", which matches its +4.5..+7.3% today.

**Per-string spread (§3).** Even when the averages match, single strings of 4 or more characters vary
about ±5-8%. "Clear" runs 7% wider in Expressway; digits run wide in Prototype, whose digits measure
0.53 em against Fira Medium's 0.49. No face size removes this spread.

**Vertical metrics (§8).** At the proposed sizes, the corpus ink spans 10.5 to 12.8 UI units (Ka0s
Default 12.2). That is well inside LootHistory's 18-unit rows (defaults/Profile.lua:50), so nothing
clips.

- Caps measure 8.0-8.65 units (baseline 8.6), and x-heights 5.5-6.8 (baseline 6.25).
- Equal width makes narrow faces look larger: Obsidian's x-height is 6.76.
- Wide faces look smaller: Azeroth's x-height is 5.50 and Glass's 5.57.

**Glyph coverage (§5).** Of the corpus characters, every face draws all of them. Among the symbols:

- U+2248 (≈, LootHistory's footer in image-19) is missing from **Expressway** and **Philosopher**.
- Arrows and ▲▼ are missing from most faces.
- ✓ (U+2713) is missing from all of them except Inter and JetBrains Mono.

These belong to the image-19 sweep.

## 4. Proposed change

The repo is **LibKa0s** (source `LibKa0s/LibKa0s/`). It then reaches every addon through the re-vendor.

1. **SkinDefs.lua.** Set `fs` and `titleSize` in the mock entries to the proposed values:
   - :611 obsidian: 12.5 / 14.5
   - :659 azeroth: 12 / 12.5
   - :705 glass: 11.5 / 13
   - :757 contrast: 12 / 13
   - :806 ember: 11.5 / 12.5
   - :918 midnight: 12.5 / 13.5
   - :969 forever: 12 / 13.5

   Keep :279 (12 / 14) and wow's :861 (12 / 14) as they are. Drop "larger type" from High Contrast's
   description (:755) and from the comment at :750-751. Record the change in the minor-history header
   with a `DEFS_MINOR` bump.
2. **HUD (needs the lead's decision, Q2).**
   - Add `HUD_SIZE` beside `HUD_FACE` (SkinDefs.lua:592-596): obsidian 13, azeroth 11, glass 11,
     contrast 11, ember 11, wow 12, midnight 12, forever 12.
   - Apply it in `register()` (:600-605) in the same way as `hud.font`.
   - Make `hud.fontSize` a **relative reference**, like `font.bodySize`.
   - Add the facade `S.HudFontSize(stock)` in SkinPaintExtras.lua next to `prim.BarStyle` (:468-479).
     It returns `P.fontSize(owner, "hud.fontSize", stock)`, or `stock` while the owner ignores fonts,
     and it is added to the Skin VOCAB.
   - Each of the 8 addons in §1 calls it where it resolves `hud.font` with fromSkin on, and only then.
     A player who picks their own face keeps their own size.
   - Every addon's `core/SkinSetup.lua` noop facade list gains `"HudFontSize"`. Their
     `tests/test_skinsetup.lua` pins that list key for key.
3. **Docs.** Update docs/api/Skin, which gets a new version file:
   - :344, the HUD size stays 12
   - :410-411 and :639, the token rows
   - :895-900, the "Sizes are relative" paragraph with its per-face list
   - :1166, High Contrast "a step larger"
4. **Tests (LibKa0s).**
   - test_skin_defs.lua:497: replace "High Contrast reads larger" with a pinned table of each skin's
     `{bodySize, titleSize, hud.fontSize}`.
   - Add a guard test: a `WIDTH` table of per-face average advance per em, copied from §1, with each
     skin's `size × adv` asserted within ±3% of Prototype's at Ka0s Default's sizes. It goes red when a
     face or size changes without re-measuring.
   - test_skin_defs.lua:519: change to `HUD_SIZE`.
   - test_skin_defs.lua:581 (the ±1.5 bound) still holds, because the largest deviation is 1.5.
   - test_skin_override.lua:423-425 (Ka0s Default stays 12) still holds.
   - Add a test for `S.HudFontSize`: it scales `stock` by skin over reference, and returns `stock` under
     Ignore fonts and for a stock of 0 or below.
   - Per addon: one HUD test for a fromSkin element at 12 under obsidian, which should get 13, and with
     fromSkin off, which should get 12.
5. **Smoke check (the owner's).** Open LootHistory in every skin and compare it with image-17.
   - The same cells should truncate: "Enchant Chest - Mark of the Worl…" and "Item Enhance…".
   - "Warband Withdraw" and "Sacrilege-Frostmourne" should not truncate.

## 5. Risks

- **Model uncertainty.** The sizes rest on a snapping model fitted to 15 strings at one UI scale.
  Outline (item 13) adds roughly the same amount to every glyph in every face, so it should barely move
  the ratios. The definitive measurement is the client's own `GetStringWidth`. A Skin Tester probe
  (`/skt widths`: each skin's corpus width over Ka0s Default's, through hidden FontStrings) would turn
  this into an in-game check (Q6).
- **WoW Default for everyone except the owner.** Real Friz Quadrata is unmeasured, so other players'
  WoW Default may be wider or narrower than Prototype.
- **Look.** Equal width trades away equal height: Azeroth and Glass read about 12% smaller in x-height,
  and Obsidian about 8% larger. High Contrast loses its larger type, which is its stated identity.
- **Overrides.** A Font override keeps the skin's sizes, so it is not equalized. The fix would be a
  per-face width factor in Media's `lib.FONTS`, applied in `P.fontSize`. It is not proposed now.
- **Licensing (items 2/3, flagged).**
  - Expressway's name table reads "(c) 2005 Typodermic. **Do not distribute**." The file is the Bold
    weight, "Expressway Rg Bold".
  - Prototype's reads "free for personal use, freely distributed with Prototype.txt".
  - Media.lua:163-166 records that Prototype was rejected earlier for this reason. The owner's "License
    should be fine" covers personal use. Expressway's notice forbids redistribution outright.
- **HUD sweep size.** The HUD change touches 8 addons plus 16 SkinSetup lists. It also changes
  `hud.fontSize`'s meaning, and the Skin Tester showroom's absolute use of it then shows the new
  per-skin sizes. That is intended.

## 6. Open questions for the lead

1. **Is the tolerance rule acceptable** (best fit, stepped down 0.5 when more than 2% wide)? *I
   recommend yes.* The alternative is the "step above" sizes in §3, which run up to 3% wider.
2. **HUD: equalize now** (relative `hud.fontSize` plus the `S.HudFontSize` sweep), or file an issue?
   *I recommend now, in the same run:* HUD faces already follow the skin by default, and item 11's
   anchor-width check needs final HUD sizes.
3. **High Contrast:** equalize to 12 / 13 / 11 and drop "larger type", or exempt it? Exempting it keeps
   it 10-16% wide, which truncates. *I recommend equalizing* (the owner's "every skin").
4. **WoW Default:** keep 12 / 14 / 12. The owner's client draws Prototype for it. *I recommend keeping
   it and filing an issue* to measure real FRIZQT__ from a client without the replacement, or from
   CASC, then retune.
5. **WoW Forever titles:** Fira Sans Medium, or the shipped SemiBold? Both give 13.5 (ratio 1.012 vs
   1.016), so the answer does not change the sizes. *I recommend Medium*, so the skin uses one face, as
   Ka0s Default and Obsidian do.
6. **Add the `/skt widths` in-client probe** to LibKa0sSkinTester? It is a permanent dev tool, not a
   temporary harness. *I recommend yes.* It is cheap, and it replaces the model with the client's own
   numbers before the sizes are frozen.
7. **Expressway's "Do not distribute" notice:** confirm with the owner before shipping, separately from
   Prototype's personal-use terms. *I recommend confirming explicitly.*
