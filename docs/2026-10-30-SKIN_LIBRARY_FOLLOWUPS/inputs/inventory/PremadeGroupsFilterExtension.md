# M0 inventory: PremadeGroupsFilterExtension

Read-only inventory for `docs/2026-10-30-SKIN_LIBRARY_FOLLOWUPS/00_PLAN.md` (rulings R-1..R-12). Taken
2026-10-30 at `master` 2fc7ae3. Paths are relative to `../PremadeGroupsFilterExtension` unless they
start with `LibKa0s/`, which means `../LibKa0s/LibKa0s/` (master ea1d92d). The vendored copies under
`libs/` and `tests/_kit/` are out of scope.

## 0. Bottom line

PGFE has **no HUD**, no `ResetToSkin` call, no close-button tint handling, no `q.*` stand-in, no custom
LibKa0s widget, and no `opts.stockDefault` caller. It does have **one large workaround, and it is the
whole of the R-2 question for this addon**: the attached panel is built **twice**. There is a never-painted
"metal" instance shown under Ka0s Default, and a skinned twin shown under every other skin. The addon's
own comment says it did this **because `opts.stockDefault` is honoured only in part**
(`modules/Panel.lua:24-44`, especially `:28-30`). Choosing between the two instances needs "which key
does this owner draw by", which is `Skin:__DrawsKey` and internal. PGFE therefore re-derives the answer
from public API in `NS.SkinDrawsDefault` (`core/SkinSetup.lua:381-390`). That is rollout follow-up 3,
which R-9 / LK-10 closes.

**The decision the lead must take (record it in `DECISIONS.md`):** does R-2, "Ka0s Default looks like
Ka0s Default everywhere", retire PGFE's metal instance? The metal look is an **owner-ratified addon
deviation**, not a library `stockDefault` call: `docs/ARCHITECTURE.md:478`, row
standalone-windows / library-stack-§8 / options-ui-§15, dated 2026-10-10 (owner). The plan already
expects "PGFE SKIN-11" to change (`00_PLAN.md`, XX-02 row), which points to option A.

- **Option A (recommended, follows R-2's wording and the plan's XX-02 row):** retire the metal instance.
  The panel is one frame, always painted through `NS.Skin`, and Ka0s Default shows the Ka0s look. A
  player who wants PGF's look picks WoW Default. This is a big PG-01: §1 lists the code, §3 the roughly 25
  tests and §4 the smoke checks. It also has to amend or retire the ratified deviation row
  (`docs/ARCHITECTURE.md:478`).
- **Option B:** keep the metal instance as an addon deviation that R-2 does not touch, because it is not
  a library option. PG-01 then only swaps `NS.SkinDrawsDefault` to the public `DrawsKey` (LK-10) and
  rewrites the two comments that cite `stockDefault`. SKIN-11 stays as it is.

Whichever option is chosen, two hazards for the LK implementers (§7) hit PGFE's skinned twin: LK-02 must
not drop `opts.stock` as a fade list, and LK-05 must not make `S.Text` stand down on a non-settings
window under the default Ignore settings panel.

## 1. Library-gap workarounds (per ruling)

| Ruling / item | What PGFE has | Cite | Change at M2 |
|---|---|---|---|
| R-1 / LK-01 (Ignore fonts on HUD) | **No HUD**, so no `NS.SkinFontsIgnored`-style patch. The skinned twin's strings go through the library: `S.Font(copyLabel)` and `S.Text(r, "disabled"/"body")` (`modules/Panel.lua:844-852`), and the title through `S.Text(title, "title")` (`:862-863`). The library's `P.font` already honours `ignoreFonts` for these. The rollout recorded PG-03 as "no HUD" (`../Ka0sAddonsCommonTasks/docs/2026-10-29-SKINNING_ROLLOUT/99_REPORT.md:44`). | proof grep §6 row 2 | None |
| R-2 / LK-02 (retire `stockDefault` / `stock`) | (a) **No `stockDefault` caller.** It appears only in two comments: `modules/Panel.lua:28-30` (the twin's rationale) and `core/SkinSetup.lua:381-382` (`NS.SkinDrawsDefault`'s doc). (b) **One `opts.stock` caller, used as a pure FADE LIST:** `S.Shell(f, { stock = { f.Bg, f.TopTileStreaks } })` on the skinned twin (`modules/Panel.lua:861`; comment `:855-858`). It fades PGF's template background and title streaks under every skin. It is not a stock-look request. (c) **The twin itself** (`modules/Panel.lua:24-44`, `:840-954`) is the addon-level stand-in for a working `stockDefault`. See §0 for options A and B. | `modules/Panel.lua:28-30,861`; `core/SkinSetup.lua:382` | **Option A:** delete the metal instance and the swap (list below). **Option B:** comment rewrites only. **Both:** keep `stock = {...}` at `:861` if LK-02 keeps `opts.stock` as the fade list (hazard H-1, §7). |
| R-3 / LK-03 (CloseButton tint) | No tint handling. The panel template's close button is **hidden** (`modules/Panel.lua:780`), and the min/max frame takes its place (`:781-782`). `NS.MakeCloseButton` is a pass-through that adds the owner (`core/CoreSetup.lua:92-94`) and has no caller in the addon's own code. The library's DebugLog console uses it. | proof grep §6 row 5 | None |
| R-4 / LK-04 (HUD font per skin) | No HUD font. Under option A, Ka0s Default's panel moves from Friz Quadrata (the metal instance's template fonts) to the library's Ka0s Default face through `S.Text`/`S.Font`. That comes from R-2, not R-4. | proof grep §6 row 2 | None |
| R-5 / LK-05 (`S.Text`, `WidgetsReorder` obey Scope) | **No hand-rolled Scope guard.** `S.Text` is called bare on the twin (`modules/Panel.lua:848-849,863`). No `WidgetsReorder` (`tests/loader.lua:35` only loads the vendored file for the harness). No `NS.SkinPanelEscape`-style guard: `NS.SkinColor`/`NS.SkinEscape` (`core/SkinSetup.lua:105-124`) are read only by the attached panel (`modules/Panel.lua:112,115,205,231`), which is a window and not a settings page. | — | None. See hazard H-2 (§7) |
| R-5 / LK-06 (custom widgets) | It consumes the library's DebugLog console and copy window (`core/DebugLogSetup.lua:83-122`), the Launcher (`core/LauncherSetup.lua`) and the first-run picker (`core/SkinSetup.lua:279-299`). **No custom widget of its own, and no Widgets/Toast/Sim/Perf consumption** (proof grep §6 row 4). | proof grep §6 row 4 | None in code. SKIN-19 and SKIN-30 may change if LK-06 restyles the console, copy window or launcher (§4) |
| R-6 / LK-07 (`ResetToSkin` `"@skin"`) | **No `ResetToSkin` call.** The only `"@skin"` is the degraded facade's `FROM_SKIN` constant and its `Resolve` mirror (`core/SkinSetup.lua:325,341-344`). That mirrors the library value and is not a guard. | proof grep §6 row 1 | None |
| R-7 / LK-08 (DragHandle `gtip.*`) | No DragHandle. The panel's own tooltip lines **already** take `gtip.value` / `gtip.title` (`modules/Panel.lua:107-118`; host copies at `core/SkinSetup.lua:101-102`). | — | None |
| R-8 / LK-09 (`q.*` exact) | No `q.*` read. The only quality-like literal is the unknown-realm tag `"|cff9d9d9d?|r"` (`modules/RegionTags.lua:50`). The rollout ruled it exception **E4** (`../Ka0sAddonsCommonTasks/docs/2026-10-29-SKINNING_ROLLOUT/inputs/inventory/PremadeGroupsFilterExtension.md:116`): it is drawn on Blizzard's Group Finder rows, it belongs to the region-tag palette, and no token matched (`q.poor` was 0.62 = `9e`). After LK-09, `q.poor` will be exactly `9d9d9d` (the client's), so a token **would** reproduce it. It is still a region tag and not an item quality, so E4 stands. Optional: the owner may ask for `q.poor`. | `modules/RegionTags.lua:50`; `LibKa0s/SkinDefs.lua:370` | None (E4 stands) |
| R-9 / LK-10 (public `DrawsKey`) | **The reach this ruling exists for.** `NS.SkinDrawsDefault()` rebuilds `__DrawsKey(owner) == DEFAULT` from `GetChoice`, `GetEUIStatus` and `GetSkin` (`core/SkinSetup.lua:381-390`), because `__DrawsKey` is internal (`LibKa0s/Skin.lua:752-759`; header `:87`). After LK-02 it is PGFE's **only** consumer (`inputs/inventory/lib-stock-close-picker.md:33`). Shipped code never calls `__DrawsKey`. Tests use it as an oracle (§3). Callers of `NS.SkinDrawsDefault`: `modules/Panel.lua:915` (`wantSkinned`), `modules/Diagnostics.lua:101` (the `drawsDefault=` line), the degraded arm `core/SkinSetup.lua:359`. | `core/SkinSetup.lua:381-390` | **Option B:** body becomes `return Skin:DrawsKey(addonName) == Skin.DEFAULT` (name per LK-10), behind a `type(Skin.DrawsKey) == "function"` guard that keeps the current derivation as the fallback (or no fallback, since the vendor gate pins the tag). **Option A:** `wantSkinned` goes. Keep `NS.SkinDrawsDefault` only for the diagnostics line (rebased on `DrawsKey`), or drop that line and SKIN-29's `drawsDefault` mention. |
| R-10 (standard: tab "Skin") | The tab already **renders** "Skin". The **key** stays `"Appearance"`: `NS.SkinPickerSpec` `tab = "Appearance"` (`core/SkinSetup.lua:246`), `SKIN_GROUP = "Appearance"` (`settings/Panel.lua:307`), comments at `core/SkinSetup.lua:220` and `settings/Panel.lua:295-296`. | — | None, unless WS-01 or an LK item renames the key (not planned) |
| R-11 / LK-11 (picker title) | The addon passes no title and no `strings` (`core/SkinSetup.lua:243-249`). The library composes "Choose a skin for " .. label from `RegisterOwner`'s `label = BRAND` = **"Ka0s Premade Groups Filter Extension"** (`core/SkinSetup.lua:85,375-379`). At 36 characters it is **the longest label in the roster** (`inputs/inventory/lib-stock-close-picker.md:256-260`), so it is the case LK-11's "never truncated" must be tested against. No addon test pins the title (§3). The smoke check does (SKIN-13, §4). | — | Smoke SKIN-13 wording. Optionally add a test asserting the label line shows `BRAND` in full (field per LK-11) |

### Option A: the code that goes or changes (`modules/Panel.lua` unless noted)

- Header block `:24-44` (THE SKIN: TWO INSTANCES): rewrite as "one frame, painted through `NS.Skin`".
- `FRAME_NAME` on the metal instance only (`:52`, `:885`). The single frame should keep the global name,
  because LAYER-1's `/dump` uses it (smoke `docs/smoke-tests.md:449-450`) and so does `tests/test_panel.lua:34,1149`.
- `ATTACH_RAISE = 3` (`:61-64`) and `raise` (`:895`): the metal border's overhang. The twin sits flush (0).
- `CHECK_SIZE` / `SKIN_CHECK_SIZE` / `f.checkSize` (`:67-72`, `:244`, `:256`, `:262`, `:300-302`, `:313`, `:320`, `:887`):
  a single 24px size, or keep the variables at one value.
- Metal header art: `HEADER_H`, `HEADER_SEAM`, the clipped border copies `buildHeaderHalf` / `buildHeaderArt` /
  `setHeaderOnly` (`:666-728`), the `RedButton-*` arrow art `setArrowArt` and its call (`:730-739`, `:785-789`),
  and `collapsedHeight`'s metal arm (`:751-756`). `buildHeaderClick` keeps `HEADER_SEAM` for its height (`:802`).
- `paintSkinned` (`:854-880`): becomes unconditional (`:909`).
- `buildFrame(dialog, skinned)` (`:882-911`), `wantSkinned` / `instance` / `clearFocus` / `choose` (`:913-943`),
  and the swap in `onLooksChanged` (`:945-954`): only `Panel.Refresh()` is left, because tokens are read at
  write time (`:42-44`). `Panel.Create` (`:960-970`) and `Panel.UpdateVisibility` (`:1005-1007`) lose `choose`.
- `Panel.stockFrame` / `Panel.skinFrame` fields: tests read them (§3).
- `core/SkinSetup.lua:30-31` (header line for `NS.SkinDrawsDefault`: "shows its never-painted metal instance")
  and `:381-390`.
- Degraded install (no library): the facade's primitives are no-ops (`core/SkinSetup.lua:329-337`), so the
  single frame keeps PGF's template art, which is the same pixels as today's metal instance. Only the
  collapse would lose the clipped header copies unless they are kept for the degraded arm. SKIN-31 needs
  a decision.

## 2. HUD face or outline the addon resolves itself (R-1)

**None.** PGFE never calls `S.Resolve`, `S.Token("hud.*")` or `FROM_SKIN` outside the degraded facade's
own mirror (`core/SkinSetup.lua:339-344`). The only facade reads in shipped code are `NS.Skin.Color`
(`core/SkinSetup.lua:110,120`), `NS.Skin.Token("title.height")` (`modules/Panel.lua:754`) and
`NS.Skin.OnLooksChanged` (`modules/Panel.lua:966`). The debug console's mono face `NS.FONT_MONO`
(`core/PGFE.lua:27-28`, `core/DebugLogSetup.lua:87`) is a descriptor input to the library's console and
not a HUD face. Proof: §6 row 2.

## 3. Tests that pin current behaviour

| Test | Cite | Pins | After the release |
|---|---|---|---|
| "eui: which instance shows is read from public API only, never the library's __DrawsKey" | `tests/test_skin_eui.lua:129-135` | That `core/SkinSetup.lua` never calls `Skin:__DrawsKey` | **R-9:** invert or replace it with "reads the public `DrawsKey`" (option B), or delete it with `wantSkinned` (option A). It stays green either way unless the swap reintroduces `__DrawsKey`. |
| "eui: the public answer matches the key the library draws by, in every state" | `tests/test_skin_eui.lua:137-158` (oracle `Skin:__DrawsKey` at `:142` and `:156`) | `NS.SkinDrawsDefault` == `__DrawsKey(owner) == DEFAULT` | **R-9:** move the oracle to the public name. It goes **red** if LK-10 drops the `__DrawsKey` alias, which LK-10 allows "only if a consumer still calls it". **This test is such a consumer.** Either keep the alias through PG-RV, or land PG-RV and PG-01 in one commit. |
| "eui: before EllesmereUI paints, the eui source wears the metal instance (Ka0s Default)" | `tests/test_skin_eui.lua:121-127` | Unpainted eui source shows `stockFrame` | Option A: rewrite as "shows the one frame on Ka0s Default". B: unchanged. |
| "eui: once EllesmereUI paints the owner, the skinned twin shows and goes to its facade" | `tests/test_skin_eui.lua:107-119` (`P.skinFrame`, `P.stockFrame` at `:112,118`) | Twin goes to EllesmereUI's facade; metal never does | Option A: drop the `stockFrame` half. |
| "eui: the twin folds to EllesmereUI's 25px shell bar" | `tests/test_skin_eui.lua:160-187` | `EUI_SHELL_HEADER_H` | Unchanged (field renames only) |
| "skin: under Ka0s Default the panel is the metal instance, and no primitive ever touched it" | `tests/test_skin.lua:61-73` | **The R-2 behaviour itself** | Option A: **inverts**: Ka0s Default paints the one frame through the facade. B: unchanged. |
| "skin: the colors the metal panel writes are Ka0s Default's exact pixels" | `tests/test_skin.lua:75-96` | Token values under Ka0s Default | Stays valid (colors are token reads). Rename it under A. |
| "skin: the panel's tooltip lines are the skin's tooltip colors..." | `tests/test_skin.lua:98-115` | `gtip.*` | Unchanged |
| "skin: another skin shows the twin...; the metal instance hides" / "back to Ka0s Default shows the untouched metal instance again" / "a swap carries the filter state..." / "a pick before the panel exists builds only the instance the skin wants" / "a pick while stood down builds nothing; the stand-up shows the skin's instance" | `tests/test_skin.lua:117-138`, `:140-153`, `:155-174`, `:176-183`, `:240-254` | The two-instance swap | Option A: delete or rewrite them as a "one frame repaints live" test. B: unchanged. |
| "skin: the twin's geometry: 24px check buttons..., flush under the dialog" | `tests/test_skin.lua:185-202` | 24px vs metal 32px, raise 0 vs 3, no `headerArt` | Option A: compares against `stockFrame`, so rewrite it as absolute geometry. |
| "skin: collapsed, the twin folds to the skin's title band" / "the twin writes the skin's colors..." | `tests/test_skin.lua:204-211`, `:213-238` | Twin behaviour | Unchanged (they become the only instance) |
| "skin: modules/Panel.lua types no color..." | `tests/test_skin.lua:256-` | No literals | Unchanged |
| test_panel metal-instance assertions (Ka0s Default is the default in every `test_panel` setup) | `tests/test_panel.lua:24-35` (name, raise 3 at `:33`), `:466-478` and `:480-490` (collapsed height 32), `:592-627` (header strip from two clipped border copies), `:629-637` (no NineSliceUtil), `:639-660` (header copies' level), `:688-698` (RedButton arrow atlases), `:791-806`, `:907-925`, `:992-1000` (32px box geometry), `:1143-1160` (named frame level) | The metal look under Ka0s Default | Option A: **all move** (height = `title.height`, no `headerArt`, page-button arrows, 24px boxes, raise 0). B: unchanged. |
| "layers: the panel's level band (L, header art L, chrome L+1, widgets L+2)" | `tests/test_layers.lua:68-80` (`f.headerArt` at `:75-76`) | Metal header art level | Option A: drop the header-art band. |
| "skin seam: the degraded facade answers every name the live facade carries" | `tests/test_skinsetup.lua:287-298`; host list `core/SkinSetup.lua:329-337` | Facade key parity | **Goes red if LK-06 or LK-10 adds a facade member** (for example a primitive per widget family, or `DrawsKey` on the facade). PG-01 then adds the name to the degraded list. |
| "skin seam: each host-copy skin token is the live library's Ka0s Default value" | `tests/test_skinsetup.lua:300-` ; `NS.SKIN_FALLBACK` `core/SkinSetup.lua:95-103` | 7 tokens (`title.text`, `text.*`, `gtip.title`, `gtip.value`) | Unchanged. LK-09 moves only `q.*`. It goes red only if a release moves one of these. |
| "skin picker: the spec names this owner, its seams, the General page's Skin tab, and no eye" | `tests/test_skin_picker.lua:58-72` (`tab == "Appearance"` at `:68`) | Tab key | Unchanged |
| Picker title | — | **No test pins "Choose a skin for ..."** (grep: `git grep -n "Choose a skin" -- tests` is empty) | Optional new test: the label line carries `BRAND` in full (R-11) |
| "skin seam: the tab's Ignore fonts reaches the library and the profile, one repaint" | `tests/test_skinsetup.lua:206-216` | Write seam only | Unchanged (no HUD) |
| `docs/test-cases.md` | `:400-413` (test_skin list), `:441-446` (eui list), `:558` (counts) | Test names and counts | Regenerate after the test edits |

## 4. Smoke checks and doc passages whose expectation changes

### Smoke (`docs/smoke-tests.md`)

| Check | Cite | Today | After |
|---|---|---|---|
| SKIN-13 the first-run picker | `:347-354` ("titled for Ka0s Premade Groups Filter Extension") | Old title | **R-11:** "titled **Choose a skin**, with *Ka0s Premade Groups Filter Extension* in full on its own line above the skin dropdown". This is the roster's longest label, so the check is the truncation check. |
| SKIN-11 Ka0s Default looks as before | `:329-338` | Metal panel, Friz Quadrata, red arrows, 32px boxes | Option A: **rewrite**. Ka0s Default shows the Ka0s look (Ka0s edge and background, page-button arrow, 24px boxes, the library's Ka0s Default face), and **WoW Default** is where the PGF-like look lives. B: unchanged, apart from noting that the settings tab strip changes if Ignore settings panel is off (LK-02 on `OptionsTabs.lua`, see the PanelMaster inventory §1 R-2). |
| SKIN-15 each skin live | `:361-369` ("swaps to its skinned twin"; "Back on Ka0s Default the metal panel returns untouched") | Swap | Option A: there is no swap. Every skin, Ka0s Default included, repaints the one panel live. Keep "no Blizzard background or title streaks showing through", which is H-1's in-client proof. |
| SKIN-20 fonts | `:390-395` ("Ka0s Default's metal panel keeps Friz Quadrata") | — | Option A: drop the parenthesis. R-4 does not touch it (no HUD). |
| SKIN-26 EllesmereUI off | `:417-420` ("the metal panel on Ka0s Default") | — | Option A: "the Ka0s Default panel" |
| SKIN-29 diagnostics | `:429-432` (`drawsDefault`) | — | Unchanged if the line stays (rebased on `DrawsKey`). Edit it if the line is dropped. |
| SKIN-31 degraded install | `:435-437` ("the attached panel is the metal panel") | — | Option A: true only if the degraded arm keeps the template art and the header copies (§1 option A list) |
| SKIN-19 console / SKIN-30 launcher | `:386-389`, `:433-434` | Library-painted | Change only if LK-06 restyles them. Note it in the check. |
| APPLY-14 collapse | `:176-185` (metal header strip, about 50px, "the strip's metal art") | — | Option A: the skin's title band |
| APPLY-22 title, flush | `:233-237` ("the two metal borders meet with no gap (tune `ATTACH_RAISE`)") | — | Option A: flush with no raise |
| LAYER-1 | `:448-455` (`/dump PremadeGroupsFilterExtensionPanel...`, "draws over PGF's bottom metal border") | — | Option A: the one frame must keep `FRAME_NAME` for the `/dump`. Reword "metal border". |
| Index row SKIN-11..32 | `:25` ("Ka0s Default unchanged") | — | Option A: reword |
| Pending sign-off | `:489-497` | — | Add the run's changed and new checks |
| Ignore fonts on HUD / HUD face under non-Ka0s skins | — | **None in this addon** (no HUD; the intro at `:326-327` says so) | None |

### Docs

| Doc | Cite | Change |
|---|---|---|
| `docs/ARCHITECTURE.md` | `:20-24` (metal under Ka0s Default, twin otherwise), `:152-154` (OnLooksChanged swaps instances), `:239` (twin), `:294-300` (EllesmereUI paint: twin vs metal; "built from public API ... never the library's `__DrawsKey`"), `:414` (Known limitations: twin), **`:478` the ratified deviation row** | A: rewrite all of them, and amend or retire the `:478` deviation's Ka0s Default clause (keep the attachment and visibility parts). B: rewrite only `:299-300` for the public `DrawsKey`. **Both:** `:31` vendored `v1.80.0` → `v1.81.0`. |
| `docs/module-map.md` | `:4` (v1.80.0), `:45` (`NS.SkinDrawsDefault`), `:68` (metal instance and twin) | Version (both). `:45`/`:68` under A. |
| `docs/schema.md` | `:17` ("under which the attached panel is PGF's metal look") | A |
| `docs/scope.md` | `:29` ("Ka0s Default keeps PGF's metal look") | A |
| `README.md` | `:55-58` ("Ka0s Default ... keeps the panel in Premade Groups Filter's own metal look") | A: "pick WoW Default for the game's look" |
| `docs/settings-panel.md` | `:68-75` (Skin tab, picker) | None (it names no picker title) |
| `docs/testing.md` | — | No skin passage (grep `-i "skin\|twin\|metal"` is empty) |
| `CLAUDE.md` | `:52` provenance `v1.80.0`; `:53` icons line | PG-RV rolls it |
| `modules/Panel.lua:28-30`, `core/SkinSetup.lua:30-31,381-385` (code comments citing `stockDefault` / `__DrawsKey`) | — | Both options: no longer true after LK-02 / LK-10 |

## 5. Current state

- Branch **`master`**, clean, `## master...origin/master` (in sync). HEAD **2fc7ae3** "Merge
  feat/2026-10-29-skinning-rollout". Only `master` exists locally and on origin. No run branch yet.
- Vendored LibKa0s: **v1.80.0**. Provenance at `CLAUDE.md:52` ("Bundles [LibKa0s](...) v1.80.0 (MIT).");
  icons line `CLAUDE.md:53` ("LibKa0s icons: clear, close, copy, settings.").
- Gate on master, run 2026-10-30:
  - `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` → `432 passed, 0 failed, 1 skipped, 433 total`,
    exit 0. The skip is the kit's "diagnostics contract: an addon that opts out ..." case, which the
    addon does not opt into.
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` → `Total: 0 warnings / 0 errors in 64 files`, exit 0.
  - 1500-line cap: largest own files are `tests/test_panel.lua` 1215 and `modules/Panel.lua` 1075. Under the cap.
- **Gate green.**

## 6. Proof greps (rows for `exceptions.tsv` where nothing changes)

Run from `../PremadeGroupsFilterExtension`. Exit 1 (no match) proves the claim.

| # | Claim | Command | Result |
|---|---|---|---|
| 1 | No `ResetToSkin` (R-6 / LK-07) | `git grep -n -E "ResetToSkin" -- core modules settings defaults locales` | no match (rc 1) |
| 2 | No HUD face or outline, no Ignore-fonts patch (R-1, R-4) | `git grep -n -E "hud\.(font\|outline)\|SkinFontsIgnored" -- core modules settings defaults locales` | no match (rc 1) |
| 3 | No `q.*` read (R-8 / LK-09) | `git grep -n -E '"q\.[a-z]+"' -- core modules settings defaults locales` | no match (rc 1). E4's literal at `modules/RegionTags.lua:50` stays by the rollout's ruling. |
| 4 | No custom widget consumption (R-5 / LK-06, LK-08) | `git grep -n -E "LibKa0s-(Widgets\|Toast\|Sim\|Perf)\|DragHandle\|Autocomplete\|LineChart\|Reorder" -- core modules settings defaults locales` | no match (rc 1) |
| 5 | No close-button tint handling (R-3 / LK-03) | `git grep -n -E "S\.CloseButton\|CloseButton.*(SetVertexColor\|Tint)" -- core modules settings defaults locales` | no match (rc 1) |
| 6 | No `stockDefault` caller (only comments) | `git grep -n "stockDefault" -- core modules settings defaults locales` | 2 comment hits: `core/SkinSetup.lua:382`, `modules/Panel.lua:29`. Both are edited by PG-01 in either option, so not an exception. |
| 7 | Shipped code never calls `__DrawsKey` | `git grep -n "__DrawsKey" -- core modules settings defaults locales` | no match (rc 1). Tests do: `tests/test_skin_eui.lua:133,142,156`. |

So for PGFE: **PG-RV** applies, **PG-01** applies (R-9's `DrawsKey` swap in both options, plus the
twin's retirement under A), and **PG-02** applies (SKIN-13 always, plus the option A rewrites). No PG
item is an exception. The rows above document the rulings that have nothing in this addon: R-1, R-3,
R-4, R-6, R-7, R-8.

## 7. Hazards for the LK implementers

- **H-1 (LK-02, `opts.stock`).** PGFE's twin passes `opts.stock` as a **fade list** under every skin
  (`modules/Panel.lua:861`). The library inventory recommends keeping it (`inputs/inventory/lib-stock-close-picker.md:57-85`).
  If LK-02 removes it, PGF's template `Bg` and `TopTileStreaks` show through the twin under every skin
  (SKIN-15's "no Blizzard background or title streaks showing through"). The harness cannot see it,
  because the mock's `PortraitFrameTemplate` has no `Bg` or `TopTileStreaks` (`tests/wow_mock.lua:323-326`).
  Unverified: whether `f.Bg` in `PortraitFrameTemplateMinimizable` is a Texture (faded today) or a Frame
  (silently dropped by `P.isTexture`, `LibKa0s/SkinPaint.lua:255`, the QC case). If LK-02 widens
  `opts.stock` to accept a Frame, PGFE gains the Bg fade for free in the second case.
- **H-2 (LK-05, `S.Text` and Scope).** PGFE's twin labels and title use `S.Text` on a **window**
  (`modules/Panel.lua:848-849,863`), and Ignore settings panel defaults **on** (`defaults/Profile.lua:51`).
  If LK-05 makes `S.Text` stand down whenever the owner ignores its settings panel, rather than only for
  text inside a settings page, the panel's labels lose the skin's colors under the default Scope. No PGFE
  test would catch it: `tests/test_skin.lua:213-238` reads colors through `NS.SkinColor`-written fields,
  and `paintTexts` goes through the live facade only for recorded strings. Add a PGFE test at M2:
  "with ignorePanel on, the twin's labels still take `text.body`".
- **H-3 (LK-10, alias).** `tests/test_skin_eui.lua:142,156` call `Skin:__DrawsKey`. If LK-10 drops the
  alias, PG-RV goes red until PG-01 moves the oracle. Land them in one commit, or keep the alias.
- **H-4 (LK-06 / LK-10, facade parity).** `tests/test_skinsetup.lua:287-298` holds the degraded facade's
  host list (`core/SkinSetup.lua:329-337`) to the live facade key for key. Any new facade member goes red
  there, and PG-01 adds the name.
