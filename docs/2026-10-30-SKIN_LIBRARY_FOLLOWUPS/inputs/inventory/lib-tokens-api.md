# M0 inventory: LK-04, LK-07, LK-09, LK-10 and the LK-90 release mechanics

Read-only inventory taken 2026-10-30 against LibKa0s `master` at `ea1d92d` (tag `v1.80.0` is the
newest; `git tag --sort=-v:refname`). Every LibKa0s path below is relative to
`/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/`; addon paths are relative to
`/mnt/d/Profile/Users/Tushar/Documents/GIT/`. Rulings are `00_PLAN.md:11-26` of this bundle.

Scope note: the user's relayed request (the first-run picker title "Choose a skin", the addon's name
on its own line above the dropdown) is R-11 / LK-11 (`00_PLAN.md:26,62`), which is outside this
report's four items. It is covered by `lib-stock-close-picker.md`.

---

## LK-04 (R-4): every skin gets its own HUD font

### The nine skins and their character

Every skin is registered in `LibKa0s/SkinDefs.lua`. Ka0s Default is the base table `KA0S`
(`SkinDefs.lua:208-372`, registered `:374-380`). The other eight go through
`register()` (`:557-563`), which calls `translate()` (`:528-546`) on a mockup table plus an `extra`
table. No skin sets `hud.font`, `hud.fontSize` or `hud.outline` itself. All eight inherit
`hud.fontSize = 12` and `hud.outline = "OUTLINE"` from Ka0s Default (`:307-308`).

| Key | Label, desc (cite) | Palette | Body / title face | Bar | HUD face today |
|---|---|---|---|---|---|
| `ka0s` | Ka0s Default, "Today's look: dark panels, hard 1px black edges, gold titles." (`:374-380`) | `#0f0f14`, black edges, `#3d3d45`, gold `#ffd100` (`:378`) | Ka0s Oxanium SemiBold / Ka0s Oxanium Bold (`:212`) | Ka0s Default (`:306`) | **Ka0s Oxanium SemiBold**, OUTLINE, 12 (`:307-308`) |
| `obsidian` | "True black and flat, hairline edges, one cool blue accent." (`:566`) | `#0a0a0b`, `#202024`, `#141416`, accent `#4db8ff` (`:567`) | Ka0s Inter / Ka0s Inter SemiBold, 12/14 (`:568`) | Ka0s Matte (`:569`) | Friz (KEEP) |
| `azeroth` | "Dark tooled leather, parchment text, gold and a red wax seal, Vollkorn type." (`:614`); reworked dark (`:606-611`) | leather `#2B1D12`, edge `#6b4a22`, gold `#E2B659`, wax `#8e1b10` (`:612-615`) | Ka0s Vollkorn / Ka0s Vollkorn Bold, 13/14 (`:616`) | Ka0s Parchment (`:617`) | Friz (KEEP) |
| `glass` | "Translucent frosted panels with rounded corners and a lilac accent." (`:660`); Nunito "rounded as its corners are" (`:653`) | `rgba(18,22,34,.88)`, white edges, lilac `#B69CFF`, blue `#5aa9ff` (`:661-668`) | Ka0s Nunito / Ka0s Nunito SemiBold, 12.5/14 (`:662`) | Ka0s Glass Bar (`:663`) | Friz (KEEP) |
| `contrast` | "Black and white with yellow focus, crisp 1px edges, larger type." (`:712`) | `#000000`, white `#FFFFFF`, `#1a1a1a`, yellow `#FFE600` (`:711-713`) | Ka0s Atkinson / Ka0s Atkinson Bold, 13.5/15 (`:714`) | Ka0s Solid (`:715`) | Friz (KEEP) |
| `ember` | "Charred browns lit by an orange accent, Bitter type." (`:761`); "a sturdy slab" (`:759`) | `#1a0e0a`, `#6a2e17`, `#c98a3a`, orange `#ff7a33` (`:762-769`) | Ka0s Bitter / Ka0s Bitter Bold, 12/13.5 (`:763`) | Ka0s Forge (`:764`) | Friz (KEEP) |
| `wow` | WoW Default, "The vanilla client: dialog-box border, red buttons, gold text." (`:816`) | `#1e1c19`, `#a8a8a8`, red `#640c05`, gold `#ffd100` (`:817-823`) | Friz Quadrata TT both, through KEEP; sets no face (`:813-814`, `:818`) | Blizzard, through KEEP (`:813-814`) | Friz (KEEP) |
| `midnight` | WoW Midnight, "Night blue and violet under a gold edge, centered Philosopher titles." (`:870`) | `#171a2e`, gold `#b08a3e`, `#2a2347`, violet `#b48cff` (`:869-877`) | Ka0s Philosopher / Ka0s Philosopher Bold, 12.5/14 (`:872`) | Ka0s Satin (`:873`) | Friz (KEEP) |
| `forever` | WoW Forever, "Warm charcoal, black title bars with centered white titles, tan accent." (`:921`); Fira Sans "crisp at small sizes" (`:918`) | charcoal `#2e251c`→`#18120d`, `#3a3530`, `#050505`, tan `#C9A07A` (`:919-928`) | Ka0s Fira Sans / Ka0s Fira Sans SemiBold, 12/14 (`:923`) | Ka0s Classic (`:924`) | Friz (KEEP) |

The family-uniqueness rule (one family per skin, body and titles alike; only Friz may be shared) is
pinned by `tests/test_skin_defs.lua:466-498`.

### The KEEP fallback that sends `hud.font` to Friz Quadrata

- `LibKa0s/SkinDefs.lua:521-525`:

  ```lua
  local FRIZ = "Friz Quadrata TT"
  local KEEP = { ["font.body"] = FRIZ, ["font.title"] = FRIZ, ["hud.font"] = FRIZ, ["bar.texture"] = "Blizzard" }
  ```

- It is applied last in `translate()`, `SkinDefs.lua:542-544`: `for name, v in pairs(KEEP) do if out[name] == nil then out[name] = v end end`.
  So a skin's own table always carries `hud.font = "Friz Quadrata TT"` unless its mockup or `extra`
  sets one. None does today.
- Why it exists: minor 14 moved Ka0s Default to Oxanium. Without KEEP, every derived skin would have
  inherited Oxanium through `ResolveSkin` (`SkinDefs.lua:80-87`, `:521-523`).
- After LK-04, KEEP's `font.body` / `font.title` still matter only to `wow`, which sets no face, and
  `bar.texture` only to `wow`, which sets no bar. Only the `hud.font` entry goes.
- The `eui` source does not use SkinDefs' KEEP. `SkinEUI.lua:321-329` derives from
  `ResolveSkin(lib.DEFAULT)`, and `FONT_TOKENS` covers only `font.body` and `font.title`
  (`SkinEUI.lua:108`, `:314-315`). So `hud.font` under eui stays Ka0s Default's Oxanium SemiBold. LK-04
  does not change that, and adds no token, so the eui source owes nothing new.
- The HUD readers: `SkinPaintExtras.lua:446-447` (`BarStyle`: `font = P.media("font", T["hud.font"])`,
  `outline = T["hud.outline"]`). `OptionsCompose.lua:331` makes FontGroup's *Use the skin's font*
  follow `hud.font`. `Skin.lua:727` makes a font override replace `hud.font`.

### Every font the library ships and registers (all SIL OFL 1.1)

The catalog is `lib.FONTS` at `LibKa0s/Media.lua:168-193` (Media minor 9, `Media.lua:56`). Files are
in `LibKa0s/media/fonts/`, each with its licence file beside it. Registration through LSM:
`Media.lua:541-542`. Per-face langmask: `Media.lua:157-161`, `:167`.

| LSM key | File | Licence file | Langmask | Cite |
|---|---|---|---|---|
| JetBrains Mono | JetBrainsMono-Regular.ttf | JetBrainsMono-OFL.txt | western, ruRU | `Media.lua:169-170` |
| Ka0s Inter | Inter-Regular.ttf | Inter-OFL.txt | western, ruRU | `:171` |
| Ka0s Inter SemiBold | Inter-SemiBold.ttf | Inter-OFL.txt | western, ruRU | `:172` |
| Ka0s Nunito | Nunito-Regular.ttf | Nunito-OFL.txt | western, ruRU | `:173` |
| Ka0s Nunito SemiBold | Nunito-SemiBold.ttf | Nunito-OFL.txt | western, ruRU | `:174` |
| Ka0s Vollkorn | Vollkorn-Regular.ttf | Vollkorn-OFL.txt | western, ruRU | `:175` |
| Ka0s Vollkorn Bold | Vollkorn-Bold.ttf | Vollkorn-OFL.txt | western, ruRU | `:176` |
| Ka0s Bitter | Bitter-Regular.ttf | Bitter-OFL.txt | western, ruRU | `:177` |
| Ka0s Bitter Bold | Bitter-Bold.ttf | Bitter-OFL.txt | western, ruRU | `:178` |
| Ka0s Philosopher | Philosopher-Regular.ttf | Philosopher-OFL.txt | western, ruRU | `:179-180` |
| Ka0s Philosopher Bold | Philosopher-Bold.ttf | Philosopher-OFL.txt | western, ruRU | `:181-182` |
| Ka0s Fira Sans | FiraSans-Regular.ttf | FiraSans-OFL.txt | western, ruRU | `:183` |
| Ka0s Fira Sans SemiBold | FiraSans-SemiBold.ttf | FiraSans-OFL.txt | western, ruRU | `:184-185` |
| Ka0s Atkinson | AtkinsonHyperlegible-Regular.ttf | AtkinsonHyperlegible-OFL.txt | western only | `:186-187` |
| Ka0s Atkinson Bold | AtkinsonHyperlegible-Bold.ttf | AtkinsonHyperlegible-OFL.txt | western only | `:188-189` |
| Ka0s Oxanium SemiBold | Oxanium-SemiBold.ttf | Oxanium-OFL.txt | western only | `:190-191` |
| Ka0s Oxanium Bold | Oxanium-Bold.ttf | Oxanium-OFL.txt | western only | `:192` |

- Every licence file states "licensed under the SIL Open Font License, Version 1.1". Checked with
  `head`/`grep` on each `media/fonts/*-OFL.txt`. Inter, Nunito, Vollkorn, Bitter and Oxanium are
  static cuts of upstream variable fonts made by `tools/artwork/fonts.py`, and their licence files
  record that (`Media.lua:153-155`).
- README credits: `README.md:444-469` (each family and weight, and the licence path). README module
  row: `README.md:137` ("seventeen SIL OFL faces").
- Friz Quadrata TT is **not** shipped. It is the client's own face, which LSM registers by default.
  `tests/test_skin_defs.lua:413-415` allows it by name.
- Stale comment, for information only: `Media.lua:149-153` still says "Ka0s Default and WoW Default
  draw the client's Friz Quadrata". That was true before Media minor 9 / SkinDefs minor 14. Changing
  it is a Media.lua change, which would need a Media minor bump (`docs/releasing.md:26-42`).
  **Recommendation: leave Media.lua alone.** LK-04 needs no new font.

### Recommended HUD face per non-Ka0s skin

Every pick below is a face the library already ships, so nothing needs a new file, licence or
credit. The README already credits every weight named (`README.md:444-469`). Two rules guide the
weights:

- **Same family as the skin's own text.** This keeps the family-per-skin rule
  (`test_skin_defs.lua:466-498`) and gives every skin a distinct HUD face.
- **The heavier shipped weight.** Ka0s Default's precedent is SemiBold for HUD text
  (`SkinDefs.lua:209-212`, `:307`). HUD text sits at 12px over moving bars under an OUTLINE, and a
  Regular weight's thin strokes close up under the outline.

| Skin | `hud.font` | `hud.outline` | Reason |
|---|---|---|---|
| Obsidian | `Ka0s Inter SemiBold` | OUTLINE (inherited) | Inter is a screen UI face. SemiBold matches Ka0s Default's HUD weight and Obsidian's own title weight. |
| Azeroth | `Ka0s Vollkorn Bold` | OUTLINE | Vollkorn Regular's serif hairlines vanish under an outline at 12px, and Bold is the only heavier weight shipped. |
| Glass | `Ka0s Nunito SemiBold` | OUTLINE | Rounded terminals match the rounded skin. SemiBold holds over the translucent glass bar. |
| High Contrast | `Ka0s Atkinson Bold` | OUTLINE | Atkinson Hyperlegible was designed for low-vision legibility, and Bold gives the most contrast. THICKOUTLINE was considered and rejected: it clogs the counters at 12px. |
| Ember | `Ka0s Bitter Bold` | OUTLINE | A slab serif's sturdy serifs survive the outline, and Bold suits the "sturdy slab" character (`:759`). |
| WoW Default | `Friz Quadrata TT`, set **explicitly** in the skin and not through KEEP | OUTLINE | This is the vanilla client's own HUD face, and the skin's whole point is the client look (`:805-814`). It is never shipped, so the library carries no licence for it. **Flag for DECISIONS.md:** R-4 says "OFL only". That rule governs faces the library ships, and Friz is the client's own. If the owner reads it as excluding Friz, no shipped OFL face resembles Friz, and one would have to be sourced and added (file, `*-OFL.txt`, `lib.FONTS` row, README credit, Media minor 10). |
| WoW Midnight | `Ka0s Philosopher Bold` | OUTLINE | Philosopher is the skin's display face, and its Regular is light. Bold matches the gold titles. |
| WoW Forever | `Ka0s Fira Sans SemiBold` | OUTLINE | Fira Sans is crisp at small sizes (`:918`), and SemiBold is the skin's title weight. |

If the owner prefers each skin's body weight instead, the Regular keys at `Media.lua:171-189` are the
alternative. Every one of them is also shipped. The library has no face that needs adding in either
case. `hud.fontSize` stays 12 (Ka0s Default's, inherited): the per-skin body sizes
(`font.bodySize`) are panel text, and moving HUD sizes would move addon layouts.

Langmask caveat: Atkinson is western only (`Media.lua:160`, `:186-189`). On a ruRU client LSM
refuses it, exactly as it already does for High Contrast's body face. Nothing new is introduced.

### What the implementer changes for LK-04

1. `SkinDefs.lua:525`: drop `["hud.font"] = FRIZ` from KEEP. Keep the other three entries.
2. Add a per-skin HUD face table beside `ICON_EDGE` (`SkinDefs.lua:548-555`), with the same shape.
   Apply it in `register()` the way `ICON_EDGE` is applied (`:559-561`): set
   `tokens["hud.font"]` when it is nil. Alternatively, put `["hud.font"]` in each skin's `extra`
   table. A table in one place is easier to review and test. WoW Default's entry is
   `"Friz Quadrata TT"`, written explicitly.
3. Write a SkinDefs header note for the new minor (SkinDefs 15 → **16**, `:94`). Correct the minor 14
   paragraph's KEEP sentence going forward (`:80-87`) and the KEEP comment (`:521-523`).
4. Tests:
   - `tests/test_skin_defs.lua:500-520` asserts `t["hud.font"] == own["hud.font"] or FRIZ`, with the
     label "keeps Friz Quadrata for HUD text". Rewrite it to pin each skin's chosen face. It must go
     red if `hud.font` is put back in KEEP: assert that every non-ka0s skin's resolved `hud.font`
     is its expected key and that only `wow` reads Friz.
   - `tests/test_skin_defs.lua:420-427` (`assertNamedFile`) checks only `^font%.` names, so
     `hud.font` is never checked for being shipped. Extend it to `hud.font`.
   - `tests/test_skin_paint.lua:577-578` (`wow.fontKey == "Friz Quadrata TT"`) stays green with an
     explicit Friz for WoW Default. Add a sibling assertion for one other skin (for example Obsidian's
     `BarStyle().fontKey == "Ka0s Inter SemiBold"`).
   - `tests/test_options_compose_skin.lua:145-147` is value-agnostic and unaffected.
5. Docs, in the new Skin document (copy `docs/api/Skin/version-7.15.11.5.9.2.4-docs.md`). Paragraphs
   and rows to correct:
   - `:308-312`: the KEEP paragraph, "Friz Quadrata TT for the three faces".
   - `:1052-1055`: *Inheritance*, "the four `KEEP` holds".
   - `:1126-1130`: the per-skin table's preamble, "the `KEEP` value `hud.font`".
   - `:1343`: the HUD row, eight times Friz today.
6. Addon fallout (M2, other readers' scope): AbsorbTracker `docs/smoke-tests.md:180` (SKIN-5,
   "Friz Quadrata on the others (no other skin names a HUD face)") and any skin-by-skin HUD smoke
   check change their expectation.

---

## LK-07 (R-6): `Skin.ResetToSkin` writes `"@skin"` into an absent bool companion

### Exact code

`LibKa0s/Skin.lua:886-911` (Skin minor 7, `Skin.lua:88`):

```lua
function lib.ResetToSkin(profile, keys, extra)
  if profile == lib then profile, keys = keys, extra end
  if type(profile) ~= "table" or type(keys) ~= "table" then return 0 end
  local n = 0
  for _, path in ipairs(keys) do
    local parent, leaf = walk(profile, tostring(path))
    if type(parent) == "table" then
      local v = parent[leaf]
      if type(v) == "table" or parent[leaf .. "FromSkin"] ~= nil then
        parent[leaf .. "FromSkin"] = true
      elseif type(v) == "boolean" then
        parent[leaf] = true
      else
        parent[leaf] = lib.FROM_SKIN        -- :905, the bug's landing site
      end
      n = n + 1
    end
  end
  return n
end
```

`walk` is at `Skin.lua:873-884`. It answers the parent table and the last segment, and nil when an
intermediate table is missing. The sentinel is `lib.FROM_SKIN = "@skin"` (`Skin.lua:99`).

### Why it happens

The branches decide by the **stored value's type and presence**:

- A companion named directly is recognized only when it already holds a boolean (`:902`).
- A pick's companion is recognized only when it is already stored (`:900`).

A raw profile out of `db.sv.profiles` holds only values that differ from the AceDB defaults, so a
companion new in this release, or one equal to its default, is **absent**. Then:

- **(a) A companion named directly and absent** (for example `"units.target.fontFromSkin"`) reaches
  `else` and gets `"@skin"`. `Resolve` reads the companion with `fromSkin == true` (`Skin.lua:868-870`),
  so a `"@skin"` companion **resolves as not following**. Meanwhile the settings checkbox shows a
  truthy value. This is R-6's case.
- **(b) A pick named while its companion is absent** (for example `"bars.barTexture"`) reaches `else`
  and gets `"@skin"` written into the LSM pick. The LSM picker and the CLI cannot render it
  (documented in `docs/api/Skin/version-7.15.11.5.9.2.4-docs.md:165-169`).

The header claim at `Skin.lua:63-65` ("so the sentinel never lands in a media pick or a bool") holds
only for stored companions. So does the doc at `version-7.15.11.5.9.2.4-docs.md:170-172` ("whether the
list names the pick ... or the companion itself") and the Members row at `:84`.

### Existing contract the fix must keep

- `tests/test_skin.lua:632-651`: a plain key with no companion takes the sentinel (`:641`, `p.barTexture == "@skin"`), and an **absent plain key takes the sentinel** (`:646`, `p.newKey == "@skin"`). A missing intermediate table is skipped (`:640`, `:648`). Both call forms work (`:649`).
- `tests/test_options_compose_skin.lua:189-200`: a stored companion is set via the pick (`:195-196`), a stored bool companion named directly is set to true (`:197`), a color gets its companion (`:198`), and a number with no companion takes the sentinel (`:199`).

Because of `:646`, the library cannot treat "absent" as "a companion" in general. The leaf's name is
the only signal it can use.

### The fix

A leaf whose name ends in `FromSkin` **is** a companion, by OptionsCompose's construction
(`OptionsCompose.lua:40-41`, `:546`: `companion = (picker.path or picker.field) .. "FromSkin"`). So set
it to `true` whether it is stored or not, and whatever it holds, which also repairs a `"@skin"` that an
earlier run wrote:

```lua
local v = parent[leaf]
if leaf:match("FromSkin$") then                      -- a companion named directly, stored or not
  parent[leaf] = true
elseif type(v) == "table" or parent[leaf .. "FromSkin"] ~= nil then
  parent[leaf .. "FromSkin"] = true
elseif type(v) == "boolean" then
  parent[leaf] = true
else
  parent[leaf] = lib.FROM_SKIN
end
```

`leaf` is always a string (`walk` builds it with `gmatch`).

- Form (b) is not R-6. The library cannot tell an absent pick that will get a companion from a plain
  key (`test_skin.lua:646`). After the fix, the documented way to turn a picker's companion on
  regardless of storage is to **name the companion**. Say this in the new doc's Members row and in the
  *FROM_SKIN* section. With that, every addon workaround below collapses to "name the companions".
- Skin minor 7 → **8** (shared with LK-10 and any other Skin.lua item this release). Add a header note
  after `Skin.lua:87`.
- New tests (red without the fix): in `tests/test_options_compose_skin.lua` beside `:189`, or in
  `tests/test_skin.lua` beside `:632`:
  - an absent `"b.fooFromSkin"` becomes `true` and never `"@skin"`;
  - a stored `"@skin"` in `"c.barTextureFromSkin"` becomes `true`;
  - `n` counts both;
  - `:641` and `:646` stay as they are.

### Consumers that worked around it (each deletable at its M2 XX-01)

Each guard names only stored companions, seeds them, or writes companions directly:

- AbsorbTracker `core/Database.lua:229-247`: names a companion only when `type(u[key]) == "boolean"`.
- AuraMaster `core/Database_Migrations.lua:948-994`: seeds `parent[companion] = false` before calling with the pick. Tests: `tests/test_skin_hud.lua:291`, `:317-340`.
- QuickComms `modules/Library_Migrate.lua:219-241`: names stored companions and writes absent ones true itself. Test: `tests/test_skin_hud.lua:321`.
- DpsRace `core/Database.lua:44-58`: the same comment and guard as AbsorbTracker.
- KickCD `core/Database_Migrations.lua:336-345` (and `:389-390`): only bool-reading companions are named. Test: `tests/test_skin_hud.lua:377`.
- ConsumableMaster `core/Database.lua:103-129`: "ResetToSkin decides by the companion's PRESENCE" (`:113`). Test: `tests/test_skin_hud.lua:339`.
- DropWatcher `core/Database.lua:216-233`: the same presence note at `:219`. Test: `tests/test_skin_hud.lua:205`.
- MultiMeters `core/Database.lua:1075-1107`: backfills false before the call.
- PartyFrameEnhanced `core/Database.lua:54-60`: never calls ResetToSkin for this reason.

Once an addon vendors Skin minor 8, LibStub picks a copy at least that new at runtime, so the guard
can go without a version check.

---

## LK-09 (R-8): the `q.*` tokens equal the client's quality colors exactly

### Ka0s Default's values today

`LibKa0s/SkinDefs.lua:369-371`, under the comment "The client's ITEM_QUALITY_COLORS, written out":

```lua
["q.poor"] = { 0.62, 0.62, 0.62, 1 }, ["q.common"] = WHITE, ["q.uncommon"] = { 0.12, 1, 0, 1 },
["q.rare"] = { 0, 0.44, 0.87, 1 }, ["q.epic"] = { 0.64, 0.21, 0.93, 1 }, ["q.legendary"] = { 1, 0.5, 0, 1 },
```

`WHITE` is `{ 1, 1, 1, 1 }` (`:190`). The schema has six nilable quality tokens, `q.poor`..`q.legendary`
(`SkinDefs.lua:161-162`). There is **no** artifact, heirloom or WoW Token token. Every addon maps
qualities 6-8 to the client's own color (BankLedger `core/SkinSetup.lua:239-241`, DropWatcher
`core/SkinSetup.lua:209-211`, LootHistory `core/SkinSetup.lua:237-239`).

Stale comment: `SkinDefs.lua:27-29` still says "the `q.*` tokens are nil in Ka0s Default, which reads
the client's ITEM_QUALITY_COLORS". Since minor 8 that is false (`:369-371`). Correct it in the same
change.

Who else inherits these values:

- Every skin derives from Ka0s Default. Only Glass (`:694`) and High Contrast (`:739`) override
  `q.epic`, `q.rare` and `q.uncommon` (through `MOCK_MAP` `:464`). So Obsidian, Azeroth, Ember, WoW
  Default, WoW Midnight and WoW Forever draw Ka0s Default's six, and Glass and High Contrast draw its
  `q.poor`, `q.common` and `q.legendary`.
- The `eui` source derives from Ka0s Default too (`SkinEUI.lua:323`).
- So LK-09 moves the quality colors under seven skins and eui as well. That is intended: they become
  the client's exact colors.

### The client's exact values, verified in the repos

| Quality | Hex | Bytes | Exact float (hex/255, 6 dp) | Lua to write | Today | Today's byte |
|---|---|---|---|---|---|---|
| poor (0) | 9d9d9d | 157,157,157 | 0.615686 ×3 | `{ 0x9d / 255, 0x9d / 255, 0x9d / 255, 1 }` | 0.62 ×3 | 9e (158.1) |
| common (1) | ffffff | 255,255,255 | 1, 1, 1 | `WHITE` (unchanged) | 1 | ff |
| uncommon (2) | 1eff00 | 30,255,0 | 0.117647, 1, 0 | `{ 0x1e / 255, 1, 0, 1 }` | 0.12, 1, 0 | 1f (30.6) |
| rare (3) | 0070dd | 0,112,221 | 0, 0.439216, 0.866667 | `{ 0, 0x70 / 255, 0xdd / 255, 1 }` | 0, 0.44, 0.87 | 70, de (221.85) |
| epic (4) | a335ee | 163,53,238 | 0.639216, 0.207843, 0.933333 | `{ 0xa3 / 255, 0x35 / 255, 0xee / 255, 1 }` | 0.64, 0.21, 0.93 | a3, 36 (53.55), ed (237.15) |
| legendary (5) | ff8000 | 255,128,0 | 1, 0.501961, 0 | `{ 1, 0x80 / 255, 0, 1 }` | 1, 0.5, 0 | 7f/80 (127.5) |
| artifact (6) | e6cc80 | 230,204,128 | 0.901961, 0.8, 0.501961 | no token | — | — |
| heirloom (7) | 00ccff | 0,204,255 | 0, 0.8, 1 | no token | — | — |
| WoW Token (8) | 00ccff | 0,204,255 | 0, 0.8, 1 | no token | — | — |

The floats were computed with `ka0s-bounded lua` (hex/255). Repo evidence for the hex values:

- LibKa0s `tests/wow_mock.lua:52-59`: `ITEM_QUALITY_COLORS` with the real `hex` for 0-8 ("Real hex values").
- BankLedger `tests/wow_mock.lua:602-606`: 0-8 including e6cc80 and 00ccff, with the note "Heirloom and WoW Token genuinely share 00ccff in the live client".
- BankLedger `core/Constants.lua:240-243`: `QUALITY_HEX_FALLBACK` 0-5.
- DropWatcher `tests/test_skin_chrome.lua:218`: epic `{ 163/255, 53/255, 238/255 }`.
- Item links across BankLedger, DropWatcher and ConsumableMaster tests carry `|cffa335ee`, `|cff0070dd` and `|cff9d9d9d` (for example BankLedger `tests/test_itemsetup.lua:91`).

Write the values in the `0xNN / 255` form that `SkinDefs.lua:231` (`log.ts`, `log.tag`) already uses.
The file's `hex()` helper is defined at `:407`, after `KA0S`, so it cannot be used at `:370-371`. Do
**not** read `ITEM_QUALITY_COLORS` at load: the client may not have filled it when `libs/` loads
(`LibKa0s/Item.lua:93-106`).

### Version and tests

- SkinDefs 15 → **16** (shared with LK-04).
- `tests/test_skin.lua:148` pins `{ 0.64, 0.21, 0.93, 1 }` with exact equality (`sameColor`, `:45-49`). It must move to `{ 163/255, 53/255, 238/255, 1 }`.
- Add a test that all six equal `wow_mock`'s `ITEM_QUALITY_COLORS[q].hex` byte for byte. That keeps the token and the mock from drifting apart, and goes red on today's values.
- Docs: the new Skin document's Semantic rows (`version-7.15.11.5.9.2.4-docs.md:643-648`) take the exact values. `:301` ("its `q.*` the client's quality colors written out") stays true.

### Addon fallout (M2, other readers' scope)

- DropWatcher `core/SkinSetup.lua:214-241` (`defaultQuality` and the `sameColor` compare that draws the client's color whenever the token equals the library's rounded default) becomes unnecessary, and so does the "rounded to two places" comment in `tests/test_skin_chrome.lua:215`.
- LootHistory `tests/test_skin_table.lua:199`, `:323` pin `rgba({ 0.64, 0.21, 0.93 })` at 3 dp (`:104-106`). 163/255 prints `0.639`, so both go **red** on re-vendor.
- DropWatcher `tests/test_icon_style.lua:163`, `:165` pin 0.64/0.21/0.93. Re-check them against its `QUALITY_COLORS` fixture and `sameColor` tolerance.
- BankLedger's `QualityColor` (`core/SkinSetup.lua:243-254`) has no workaround. Its draws move to the exact color.

---

## LK-10 (R-9): `Skin:__DrawsKey` becomes public

### What it computes

`LibKa0s/Skin.lua:752-759`:

```lua
function lib:__DrawsKey(owner)
  local _, key = baseOf(owner)
  return key
end
```

`baseOf` is at `Skin.lua:735-742`:

- `"eui"` when `lib.__euiTokens(owner)` answers a table. `__euiTokens` is `SkinEUI.lua:321-329` and
  answers only while `active(owner)`: EllesmereUI paints the owner, refused included, because the
  library then paints from the derived tokens (`Skin.lua:752-755`).
- Otherwise `effectiveKey(skin)` of `GetChoice(owner)`'s skin (`Skin.lua:214-217`): a registered skin
  key, else `lib.DEFAULT` (`"ka0s"`).
- An unregistered owner gets `"ka0s"` (GetChoice answers `"ka0s","ka0s"`, per the doc
  `version-7.15.11.5.9.2.4-docs.md:76`).

It was added at Skin minor 7 for `opts.stockDefault` (`Skin.lua:87`, CHANGELOG.md:170).

### Every caller (sibling repos grepped, `libs/` and `tests/_kit/` copies excluded)

- LibKa0s `LibKa0s/SkinPaint.lua:792`, in `P.keepStock` (`:789-799`), guarded `type(lib.__DrawsKey) == "function"`. This is the only runtime caller. **LK-02 retires `opts.stockDefault`, and with it `P.keepStock`**, so after LK-02 the library may have no internal caller left. Coordinate the order with LK-02.
- LibKa0s `tests/test_skin_stock_default.lua:237` (goes with LK-02's stockDefault tests).
- PremadeGroupsFilterExtension `tests/test_skin_eui.lua:129-134` is a source scan that forbids `Skin:__DrawsKey` in `core/SkinSetup.lua`. Its `:142` and `:156` call `Skin:__DrawsKey(OWNER)` on the vendored library, as the oracle for `NS.SkinDrawsDefault`.
- PremadeGroupsFilterExtension `core/SkinSetup.lua:381-390`, `NS.SkinDrawsDefault()`, rebuilds the answer from public API (`GetChoice`, `NS.SkinEUIPainted`, `GetSkin`). Its degraded arm is `:359`. Its callers are `modules/Panel.lua:915` (`wantSkinned`) and `modules/Diagnostics.lua:101`. This is the reach-around R-9 removes.
- Docs only: LibKa0s `CLAUDE.md:265`, `CHANGELOG.md:170`, `:206`, `docs/api/Skin/version-7.15.11.5.9.2.4-docs.md:1005`, `docs/automated-tests/RESULTS.md:220`, `docs/automated-tests/20261029-032426/ANALYSIS.md:94`, and PremadeGroupsFilterExtension `docs/test-cases.md:444`.

No other addon references it. The grep covered every `*.lua` and `*.md` under `GIT/`, excluding
`libs/`, `tests/_kit/`, worktrees and the non-collection directories.

### Public name and shape

The existing owner reads are a mix:

- `Get*` for stored state: `GetChoice`, `GetIgnore`, `GetOverride`, `GetEUIStatus` (`Skin.lua:475`, `:600`, `:643`, `SkinEUI.lua:512`).
- Bare questions: `PendingReload`, `IsOwner`, `OwnerLabel` (`Skin.lua:483`, `:433`, `:447`).

The value is derived, not stored, so a bare question fits. **Recommend `Skin:DrawsKey(owner)`**, the
name `00_PLAN.md:61` already proposes:

```lua
--- The key `owner` draws by (Skin minor 8, R-9): "eui" while EllesmereUI paints it (its derived
--- tokens; a refused EllesmereUI included, since the library then paints from them), else the skin key
--- it wears, `DEFAULT` for Ka0s Default, for an unknown key and for an `eui` owner before EllesmereUI
--- paints it. An unregistered owner answers DEFAULT.
function lib:DrawsKey(owner)
  local _, key = baseOf(owner)
  return key
end
--- Internal alias, kept one release for a copy or test that still names it. Retire at the next Skin minor.
lib.__DrawsKey = lib.DrawsKey
```

- Make it lib-level only, **not** a facade (`VOCAB`) member. Nine addons pin the facade against their
  host stubs (for example AbsorbTracker `tests/test_surface_parity.lua:358`, AuraMaster `:115`,
  BankLedger `:605`, DropWatcher `:206`, KickCD `:321`, LootHistory `:372`, ConsumableMaster
  `tests/test_skin.lua:79`, DpsRace `tests/test_skinsetup.lua:351`). A new facade member would turn
  all of them red.
- `Kit.publicMembers` skips `__`-prefixed keys (`tests/_kit/asserts.lua:217-231`). So `DrawsKey`
  appears in the regenerated `docs/api/Skin/members-<key>.json` and the alias does not.
- **Keep the alias.** PremadeGroupsFilterExtension's `tests/test_skin_eui.lua:142` and `:156` call
  `__DrawsKey` on the vendored copy. Its PG-RV commit (re-vendor) must stay green before PG-01 moves
  those to `DrawsKey` and swaps `NS.SkinDrawsDefault`'s body for
  `Skin:DrawsKey(addonName) == Skin.DEFAULT`, guarded by `type(Skin.DrawsKey) == "function"`. LK-10's
  rule ("alias only if a consumer still calls it") is met by that test. If LK-02 deletes
  `P.keepStock`, the alias has no library caller left.
- Docs:
  - new Skin document, Members table (`version-7.15.11.5.9.2.4-docs.md:62-104`): add a row near
    `GetChoice` / `PendingReload`;
  - the *What changed* section;
  - the `:1005` sentence goes or changes with LK-02;
  - `docs/api/CONSUMERS.md` (stamped v1.75.0, `:3`) records the new export as not measured, as v1.80.0
    did (CHANGELOG.md:213-215).
- Tests:
  - `DrawsKey` answers `"ka0s"` for an unregistered owner;
  - it answers the chosen skin key, `"ka0s"` for an unknown key, and `"eui"` once EllesmereUI paints;
  - `Skin.DrawsKey == Skin.__DrawsKey`.

  The pattern is `tests/test_skin_stock_default.lua:227-238`.
- Band: `Skin.lua` is 1044 lines. Its re-check trigger is "1150 lines, or the next Skin minor that
  adds to the owner-token block" (`CLAUDE.md:264-270`). LK-07 and LK-10 add about 10 lines and do not
  touch the owner-token block. LK-01 also edits Skin.lua, so re-measure at the close.

---

## LK-90: release mechanics for v1.81.0

### Command and order

- The procedure is `docs/releasing.md:15-260`. `CLAUDE.md:523` points there. The green gate is at
  `CLAUDE.md:546-551`:
  - `lua tests/run.lua`
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .`
- **Release run:** `tests/_kit/run-automated-tests.sh --release 1.81.0` (`docs/releasing.md:151-154`).
  It refuses a dirty tree and exits 2, so first run `git status --porcelain`, which must print nothing.
  Run it through the bounded runner per the workspace CLAUDE.md.
- Steps in order:
  1. Bump the minor of every changed file, once per release (`:26-42`). The v1.80.0 precedent is that
     several items share one bump per file (CHANGELOG.md:179-180).
  2. Write the CHANGELOG version block (`:64-69`). It may be headed `## v1.81.0 — unreleased` until the
     close.
  3. Write a new API document per moved major and the README row, then run
     `lua tools/gen-api-members.lua` (`:70-103`). `tests/test_versioning.lua` reddens on a missing doc
     or manifest at every commit. That is why v1.80.0 left "unreleased" intermediate documents (for
     example `version-7.14.11.5.9.2.3-docs.md`).
  4. Do the preview and simulation re-look (`:105-114`).
  5. Regenerate `docs/test-cases.md` with `lua tests/run.lua --list`, keeping CRLF (`:115-116`).
  6. Move the version pointers (`:117-144`): the releasing.md table `:7` (`v1.80.0`), the provenance
     template `:317` (`> Bundles [LibKa0s](...) v1.80.0 (MIT).`, read by
     `tests/test_versioning.lua:241`), and the README standards pointer `README.md:3` (v2.91.0, after
     WS-01).
  7. Make the first commit, then the release run, then `ANALYSIS.md` in the bundle, then the
     release-gate line and the re-look line in CHANGELOG, then the second commit, then the
     precondition checks off `manifest.json` (`:192-221`), then the **local** tag.

### CHANGELOG format (model: `CHANGELOG.md:13-242`, the v1.80.0 block)

- The heading is `## v1.81.0 — <date>`, followed by an opening paragraph: which run, which branch,
  which items, and that the tag stays local.
- The versions paragraph names each moved minor in bold with each major's version key, then "every
  other file still at its v1.80.0 minor, and **test kit revision 44**", the counts ("nineteen majors
  across fifty-three files"), and "no `NEEDS_*` floor rises". `tests/test_versioning.lua` enforces
  that it agrees with `lib.MODULES` (CHANGELOG.md:8-10).
- One `### <File> minor N: <what>` section per change.
- `### Docs and process` covers the standards pointer, the re-look answer, step 8 (the M2
  re-vendor), band files and consumers.
- `### What a consumer owes` follows; see the next section.
- Then the two fixed lines (releasing.md `:229-239`):
  ```text
  Release gate (`docs/automated-tests/<stamp>/`): lint pass, <w>/<e> in <files> files;
  tests pass, <total> tests, <failed> failed; complexity pass, <n> over CCN 15. Perf
  SKIPPED, not measured — no `tests/perf.lua` — so the gate covered three suites, not four.

  Preview and simulation re-look: <Current|Refreshed|Deferred|Not applicable> — <...>.
  ```
  **The re-look is likely applicable this time.** LK-06 skins the perf and sim panels and other
  Widgets files. If `SimPanel.lua`, `Sim.lua`, `SimTimeline.lua` or `Widgets.lua` (which defines
  `W.TestStrip`) moves, it is not "Not applicable" (`docs/releasing.md:105-114`, `:241`).

### "What a consumer owes" for this report's items

- **LK-04:** nothing to call. Under the eight non-Ka0s skins, a HUD text that follows the skin
  (`fromSkin` companion on, or `S.Resolve("hud.font", FROM_SKIN)`) draws the skin's own face instead
  of Friz Quadrata. A smoke check or test that pins Friz under another skin moves.
- **LK-07:** nothing. Naming a `<key>FromSkin` companion now sets it true whether it is stored or not,
  so the absent-companion guards may go. A guard that stays keeps working. Naming a pick whose
  companion is absent still writes the sentinel into the pick: name the companion instead.
- **LK-09:** nothing to call. `q.*` under Ka0s Default, every skin that does not override them, and
  eui now equal the client's colors byte for byte. A test that pins the rounded values (for example
  LootHistory `tests/test_skin_table.lua:199`, `:323`) moves, and a "token equals the rounded default,
  so use the client's" workaround (DropWatcher `core/SkinSetup.lua:214-241`) may go.
- **LK-10:** `Skin:DrawsKey(owner)` is new on the library table, not the facade, so no facade stub owes
  a member. `__DrawsKey` stays as an alias for this release. A host that calls `DrawsKey` guards on it
  (`type(Skin.DrawsKey) == "function"`) or relies on its own vendored v1.81.0 copy.

### Current minors of the files this report's items touch, and their targets

| File | Constant | Now (cite) | v1.81.0 | Items |
|---|---|---|---|---|
| `LibKa0s/Skin.lua` | `MINOR` | 7 (`Skin.lua:88`) | 8 | LK-07, LK-10 (and LK-01 if it edits Skin.lua) |
| `LibKa0s/SkinDefs.lua` | `DEFS_MINOR` | 15 (`SkinDefs.lua:94`) | 16 | LK-04, LK-09 |
| `LibKa0s/Media.lua` | `MINOR` | 9 (`Media.lua:56`) | unchanged | none (no new font) |

SkinDefs is paired on the shell's minor: it returns early only when `__defsMinor >= DEFS_MINOR` **and**
`__defsShellMinor == lib.MINOR` (`SkinDefs.lua:95-98`). So bumping Skin.lua to 8 and SkinDefs to 16
attaches cleanly. The pairing row is `tests/majors.lua:76-85`.

For the whole release, the other Skin files are: SkinPaint `PAINT_MINOR` 11 (`SkinPaint.lua:110`),
SkinPaintExtras `EXTRAS_MINOR` 5 (`:35`), SkinPaintControls `CONTROLS_MINOR` 9 (`:51`), SkinEUI
`EUI_MINOR` 2 (`:60`) and SkinAce `ACE_MINOR` 4 (`:67`). The Skin key today is **7.15.11.5.9.2.4**
(`docs/api/README.md:200`, `docs/api/Skin/version-7.15.11.5.9.2.4-docs.md:11`).

The files the other LK items may touch:

| File | Minor (cite) |
|---|---|
| `OptionsSkinPicker` `PICKER_MINOR` | 1 (`:89`) |
| `OptionsCompose` `COMPOSE_MINOR` | 13 (`:29`) |
| `OptionsAppearance` `APPEARANCE_MINOR` | 3 (`:55`) |
| `Options` | 34 (`:46`) |
| `Widgets` | 16 (`:87`) |
| `WidgetsDragHandle` `DRAG_MINOR` | 6 (`:56`) |
| `WidgetsReorder` `REORDER_MINOR` | 2 (`:33`) |
| `WidgetsAutocomplete` | 4 (`:59`) |
| `WidgetsCopyWindow` | 1 (`:22`) |
| `WidgetsLineChart` | 4 (`:42`) |
| `Toast` | 1 (`:53`) |
| `Launcher` | 5 (`:53`) |
| `DebugLog` | 22 (`:41`) |
| `DebugLogWindow` | 1 (`:38`) |
| `PerfPanel` | 10 (`:14`) |
| `SimPanel` | 7 (`:66`) |

The Options key is **34.4.35.4.6.10.3.13.8.3.2.5.3.1** (CHANGELOG.md:24-25). The test kit is
revision 44 (`testkit/framework.lua:20`). There are 19 majors (`grep -c 'major = "LibKa0s-' tests/majors.lua`)
and 53 `<Script` rows in `LibKa0s/LibKa0s.xml`.

### Other pointers the close moves

- `docs/releasing.md:536`: the Skin row of *Consumers*, which says what the release adds. Step 9's
  sweep is at `:252-260`.
- `docs/api/README.md`: a new row under `### LibKa0s-Skin-1.0` (`:196-200`); the old row goes to
  Superseded.
- `CLAUDE.md:264-270`: re-measure `Skin.lua` against the 1150 trigger.
- `docs/api/CONSUMERS.md:3`: keep the stamp or re-run the census; v1.80.0 kept it and noted the new
  exports as not measured.
