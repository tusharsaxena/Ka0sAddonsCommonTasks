# M0 inventory: QuickComms

This is a read-only inventory for the LibKa0s v1.81.0 follow-ups, rulings R-1 to R-11 of `../../00_PLAN.md`. The
scope is `/mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms`. The vendored `libs/` and `tests/_kit/` were read
for reference only. Paths are relative to the QuickComms repo root unless they start with `libs/`, which means
the vendored v1.80.0 copy. Everything was read on 2026-10-30 at master `c77daa1`.

## 0. Bottom line

QuickComms has **one real workaround** that the release retires and **one guard** that the release touches.
Everything else the rulings change reaches QuickComms through the library, with no code change:

- **R-2 (the big one): `settings/ModalWindow.lua:91-101`.** This is the only `stockDefault` / `stock` caller. It
  keeps the callout popup and the icon browser as Blizzard's `SettingsFrameTemplate` window under Ka0s Default
  (rollout X10, an owner-decided documented deviation). After R-2 both windows wear the **Ka0s Default window**
  under Ka0s Default. That is a visible change. It rewrites one test, a documented deviation row and about eight
  smoke checks or doc passages (section 4).
- **R-6: `modules/Library_Migrate.lua:219-241`.** The `followSkin` split hands ResetToSkin only the stored
  companions and writes absent ones itself. The step is shipped (schema step 10), so keep the code and reword
  the comment. Section 1d has the details.
- **R-1 reaches the HUD without a code change.** Every pad and dial face goes through
  `Skin.Resolve("hud.font", look.font, look.fontFromSkin == true)` (`modules/Pad_Render.lua:91-93`). No addon-side
  Ignore-fonts patch exists. Tests and docs gain the "Ignore fonts on, so the HUD shows the stored face" case.
- **R-11:** the picker's docs and smoke check name the old title. No test pins the title.
- **No code to change** for R-3, R-5's hand-rolled guards, R-7, R-8 or R-9. The proof greps are in section 6.

## 1. Workarounds of library gaps the release closes

### 1a. Own Ignore-fonts handling for HUD faces or outlines (R-1): none

- No `NS.SkinFontsIgnored`-style helper exists, and nothing reads the Ignore pair except the seam. `ignoreFonts`
  appears only in the path constant `core/SkinSetup.lua:91`, the write `core/SkinSetup.lua:239`, the read
  `core/SkinSetup.lua:260` (`storedIgnore`, which feeds `NS.ApplySkinIgnore` at `core/SkinSetup.lua:501-507`),
  the schema row `settings/SchemaRows.lua:112` and the default `defaults/Profile.lua:52`.
- No `hud.outline` read exists anywhere. A HUD block's outline is always the player's `fontFlags`, under rollout
  X4 ("only faces and border styles follow the skin", `modules/Pad_Render.lua:22-26`,
  `modules/Library_Migrate.lua:210-212`). So R-1's outline half changes nothing in QuickComms.

### 1b. `stockDefault` / `stock` callers (R-2): one site, four calls

`settings/ModalWindow.lua:93-101` (`skinTemplate`), called for the template window of both modals (the callout
popup and the icon browser share `MW.Build`):

| Line | Call | What it does today under Ka0s Default |
|---|---|---|
| `:95` | `S.Shell(f, { stockDefault = true, stock = bgArt(chrome.bg) })` | `P.stockDefault` keeps the window stock (`libs/LibKa0s/SkinPaint.lua:790-809, 975`). Under any other skin, Shell fades `opts.stock` (the template Bg frame's texture regions, gathered by `bgArt` at `settings/ModalWindow.lua:84-89`) and paints its fill. |
| `:96` | `S.FadeNineSlice(f, { stockDefault = true })` | `P.keepStock` leaves the NineSlice (`libs/LibKa0s/SkinPaintExtras.lua:289-299`). |
| `:98` | `S.TitleBar(chrome.nineSlice, { stockDefault = true, text = chrome.nineSlice.Text, noBg = true })` | stock title text, color and justify given back (`libs/LibKa0s/SkinPaintExtras.lua:84-98`). |
| `:100` | `S.CloseButton(chrome.close, { stockDefault = true })` | stock close X, hover inert (`libs/LibKa0s/SkinPaintControls.lua:549-557`). |

The supporting comments also go or change:
- `settings/ModalWindow.lua:17-26`: the THE SKIN header, "with `opts.stockDefault` on every call: under Ka0s
  Default it stays exactly Blizzard's settings window ... A live switch back to Ka0s Default gives the stock
  window back".
- `settings/ModalWindow.lua:81-83`: the `bgArt` rationale ("Shell's `opts.stock` takes textures only ...
  FadeRegions would fade them under Ka0s Default too: it takes no stockDefault").
- `settings/ModalWindow.lua:91-92`: "every call kept stock under Ka0s Default".
- `settings/IconBrowser.lua:50`: "(stock under Ka0s Default, X10)".
- `settings/IconBrowser.lua:125`: "X10: the browser keeps the stock settings window's look under Ka0s Default".
  Read its context: if it only justifies the texts keeping their font objects' faces, that rationale survives
  without the "stock under Ka0s Default" clause.

**What QC-01 must do.** Drop `stockDefault = true` from all four calls. The `stock = bgArt(chrome.bg)` argument
depends on LK-02's exact shape:
- If LK-02 retires **only `stockDefault`** and keeps Shell's `opts.stock` (the "regions to fade" list, a
  different thing from `stockDefault`), keep `stock = bgArt(...)`. The Bg art then fades under every skin, Ka0s
  Default included.
- If LK-02 also removes `opts.stock` from Shell, replace it with `S.FadeRegions(chrome.bg)`. FadeRegions fades
  under every skin, Ka0s Default included (`libs/LibKa0s/SkinPaintExtras.lua:274-286`). That is what is wanted
  once Ka0s Default is a skin like the others. The comment at `:81-83` then goes.
- **Library-side ask:** the plan's wording ("`stockDefault` and `stock` go") is ambiguous about Shell's region
  list. LK-02 should say which. QuickComms is the only addon known to pass Shell a `stock` region list, because
  the template Bg is a frame, not a texture.

**What the surface looks like under Ka0s Default afterwards.** The callout popup and the icon browser draw:
- the template's NineSlice faded;
- the Bg art faded under the Ka0s window fill and edge (`win.bg`, `win.border`, `win.inner`);
- the title "Ka0s Quick Comms" in the Ka0s title color and title font, Oxanium Bold (with the template's
  NineSlice title fs, `noBg` so no band);
- the close X faded to the library's "x" glyph in `close.rest` / `close.hot`, because `rec.regions.stock` is set
  by `P.hasStock` (`libs/LibKa0s/SkinPaintControls.lua:557-560`).

This is the same look the windows wear today under every other skin, in Ka0s Default's palette. The catcher's dim
(`qc.modalDim`) does not change. Under the default Scope (Ignore settings panel on), the page **inside** stays
stock AceGUI. The result is a Ka0s-chromed window around stock controls. The settings window behind it is also
stock (it is not skinned, ARCHITECTURE "Not skinned"). Under Ignore settings panel off, the inside follows the
skin too.

**Decision for the lead.** The owner ruled the stock look retired and the Ignore settings panel switch kept,
default on. One question is open: does the popup and browser **chrome** belong to the "settings panel" Scope?
They are editors opened only from the settings pages. Rollout X10 deliberately made them match the settings
window. Under R-2 they stop matching it under Ka0s Default.
- If the lead rules they follow the panel Scope (stay stock while Ignore settings panel is on), QC needs a
  Scope-aware read. No such public read exists today: `Skin:__PanelSkinned` is internal
  (`libs/LibKa0s/Skin.lua:626-630`).
- Otherwise, R-2 as written applies and the windows go Ka0s.

Either way, `docs/ARCHITECTURE.md:333`, the documented deviation decided by the owner, must be rewritten or
retired (section 4). If the lead cannot rule this from R-2, it is a candidate for `DECISIONS.md`.

### 1c. Hand-rolled Scope guards around `S.Text`, `WidgetsReorder` or other library widgets (R-5): none

- QuickComms never calls `S.Text`. The only `Text` definition is the degraded arm's stand-in at
  `core/SkinSetup.lua:445-449`. Proof: grep E in section 6.
- `W.ReorderList` at `settings/Editors.lua:405-417` passes `owner = addonName` (`:409`) with no guard. After LK-05
  its ghost and drop line are stock while Ignore settings panel is on, which is the default. **No code change.**
  The smoke expectations SKIN-3 and SKIN-10 change (section 4).
- The other library widgets QuickComms hosts, all owner-bound with no guard, are LK-06's list. Each one's Scope
  behaviour comes from the library:
  - `W.DragHandle`: the pad's drag strip. `core/WidgetsSetup.lua:21-27`, owner at `:25`, built at
    `modules/Pad.lua:310`.
  - `W.CopyWindow`: the icon browser's Wowhead link window. `core/WidgetsSetup.lua:34-38`, built at
    `settings/IconBrowser.lua:542`.
  - `W.Dropdown`: the Preview as window's dropdown. `modules/PreviewWindow.lua:158-160`, `owner = addonName`.
  - The DebugLog console and its Copy window (`core/DebugLogSetup.lua`, `addonName = addonName`).
  - The Perf panel (`core/PerfSetup.lua`).
  - The Launcher's minimap button, which ARCHITECTURE lists as "Not skinned" (`docs/ARCHITECTURE.md:254-256`).
  - QuickComms uses no Toast, LineChart, Autocomplete or Sim panel. Proof: the major list (section 6, F) wires
    Widgets in `core/WidgetsSetup.lua`, `modules/PreviewWindow.lua` and `settings/Editors.lua` only.
- **The Scope-adjacent seam that stays:** `NS.SkinPaintAce` / `NS.SkinPaintAceTree` (`core/SkinSetup.lua:486-494`).
  These are the documented way to paint an AceGUI widget the addon acquired itself. They are not a guard (the
  library's `PaintAce` consults the Scope itself), and nothing makes them unnecessary.

### 1d. ResetToSkin guards against the `"@skin"` sentinel (R-6): one, in a shipped step, so keep it

- `modules/Library_Migrate.lua:219-241` (`followSkin`) and `:248-257` (`Lib.MigrateFollowSkin`, schema step 10,
  registered at `core/Database.lua:41-44`).
- The guard is at `:233`. Only a companion the surface **stores** (`t[companion] ~= nil`) is named to
  `resetToSkin`, as its picker key (`header.font` and so on). An absent one is written `true` directly (`:236`).
- The rationale is in the comment at `:219-225`: "handed an absent companion, ResetToSkin cannot tell it is a
  bool and writes its "@skin" sentinel into the picker".
- The library cause is `libs/LibKa0s/Skin.lua:897-906`. A picker key whose value is a string and whose
  `<leaf>FromSkin` is nil falls to `parent[leaf] = lib.FROM_SKIN`.
- **QuickComms names the picker, not the companion.** Its case is therefore only closed if LK-07 makes
  ResetToSkin create the missing `<leaf>FromSkin` for a picker whose value is a string. That is broader than
  "leaves an absent bool companion a bool". AuraMaster raises the same point (`AuraMaster.md` 1.3).
- **Recommendation: keep the code.** Step 10 is shipped on master (merged 2026-10-29, `c77daa1`) and its `to = 10`
  stamp has already run for anyone on master, and steps are not rewritten. Reword the comment at `:219-225` to
  record that the split predates LK-07 (and, if LK-07 does cover picker keys, that it is now redundant but
  harmless). The no-library arm (`:236` when `resetToSkin` is nil) stays either way.
- `core/Database.lua:41-43`, the step comment, needs no change.

### 1e. Reach into `Skin:__DrawsKey` or other internals (R-9): none

- QuickComms reaches no `__`-prefixed Skin member. `__DrawsKey` is used only by the library's own `P.keepStock`
  (`libs/LibKa0s/SkinPaint.lua:792`), which QuickComms triggers through `stockDefault`. That use goes away with
  1b. Proof: grep A in section 6.
- **Surface parity:** if LK-10 adds a public name to the **owner facade** (`S.DrawsKey` or similar), it reaches
  QuickComms in two places. The degraded facade must answer it, because `tests/test_skinsetup.lua:394-404`
  (`T.assertSurfaceParity(live.Skin, degraded.Skin, ...)`) fails otherwise. The degraded vocabulary list is
  `core/SkinSetup.lua:424-432`, with the special members at `:434-452`. The same applies to any new facade name
  from LK-01 to LK-11. If the name is added only on the `Skin` major object (`Skin:DrawsKey(owner)`), nothing
  changes in QuickComms.

### 1f. Close-button tint handling (R-3): none

- QuickComms saves and restores no close-art tint. Proof: grep D in section 6.
- Close controls: the modal template's X (`settings/ModalWindow.lua:100`, see 1b) and `NS.MakeCloseButton` (the
  library's own, `opts.own`). `NS.MakeCloseButton` is used by the fallback modal (`settings/ModalWindow.lua:127`)
  and the Preview window (`modules/PreviewWindow.lua:213`). LK-03 changes what an unpaint restores. QuickComms
  needs no change.

### 1g. Literal tooltip and quality colors standing in for `gtip.*` / `q.*` (R-7, R-8): none

- Every tooltip line QuickComms writes already reads `gtip.*`:
  - `settings/CalloutPopup.lua:207-208`;
  - `settings/Groups_When.lua:321`;
  - `settings/Groups.lua:259`;
  - `settings/IconBrowser.lua:236-239`;
  - `modules/PreviewWindow.lua:98, 125`;
  - `modules/Pad_Render.lua:71` (`tip = rgba("gtip.value")`).
- No `q.*` token is read. Proof: grep B in section 6. `NS.SKIN_FALLBACK` (`core/SkinSetup.lua:128-160`) holds no
  `q.*` entry, so LK-09's value change cannot redden `tests/test_skinsetup.lua:409-423`.
- **R-7 still changes what QuickComms shows.** The pad drag strip's tooltip is the library's DragHandle tooltip
  (`modules/Pad.lua:324`, `tooltip = { title = ..., body = ... }`). Its colors are literals today: gold title,
  white body, 0.6 gray footer (`libs/LibKa0s/WidgetsDragHandle.lua:335-341`). After LK-08 they take `gtip.*`.
  Under Ka0s Default the title stays gold (`gtip.title` = GOLD). The body follows `gtip.body`
  (`libs/LibKa0s/SkinDefs.lua:226`, `BODY`) and may move from pure white to Ka0s Default's body gray, depending on
  which `gtip.*` token LK-08 maps it to. SKIN-3 lists "the drag strip" as looking as before. If LK-08 moves the
  Ka0s Default body pixel, SKIN-3 needs a carve-out.

## 2. Where QuickComms resolves a HUD face itself

Nowhere outside the library's `Resolve`. **After LK-01 the stored value wins with no QuickComms change:**

- `modules/Pad_Render.lua:89-93`: `R.FontKey(look)` is `Skin.Resolve("hud.font", look.font, look.fontFromSkin == true)`.
  This is the one face read. Its consumers:
  - `R.LabelFont` (`:381-387`, `NS.MediaFetch("font", R.FontKey(look))`), used for the pad header, the section
    titles and the buttons;
  - the look signature (`:484-485`);
  - the dial ring title and slice labels, through `NS.PadRender.ApplyFont` (`modules/Dial_Render.lua:477, 580`).
- `modules/Pad_Render.lua:97-99`: `R.BorderKey` is `Skin.Resolve("bar.borderStyle", ...)`. That is a border, not
  a font, so R-1 does not touch it.
- `modules/IconStyle.lua:108-110`: `S.Resolve("icon.borderStyle" / "icon.borderSize")`. Also not a font.
- **The repaint already happens:** `Skin:SetIgnore` repaints and fires OnLooksChanged
  (`libs/LibKa0s/Skin.lua:611-624`). QuickComms' listener (`modules/Pad_Render.lua:83-86`) moves `looksGen` and
  asks `Surfaces` for one rebuild. Toggling Ignore fonts therefore redraws the pads and dials live, held to the
  end of combat in combat.
- **What the player sees after R-1, with Ignore fonts on.** Every followed HUD face is the block's stored
  `font`. By default that is "Friz Quadrata TT" (`defaults/PadStyle.lua:38, 51, 72, 90, 103`; schema rows in
  `docs/schema.md:40-49`), or the player's own pick. This holds under every skin, including the font override
  (`skin.font`), assuming LK-01 lets the stored value beat the override too. Colors, sizes, flags and shadows
  are unchanged (they were never the skin's).
- **The degraded arm:** `core/SkinSetup.lua:436-439` has no Ignore state without the library, so it stays as it
  is.
- **Unaffected by R-1:**
  - the dial hub's stale, LOCKDOWN and TEST labels keep their font-object faces (rollout report, "QuickComms dial
    hub labels");
  - the icon browser's count, status, hint and name lines keep their font objects' faces under every skin
    (`tests/test_skin_windows.lua:520`, X10).
- **The composer pickers** (`settings/SchemaMembers.lua:405-414`, `blockSpec` with `fromSkin = true`, and
  `settings/SchemaIcons.lua:148`) are the library's OptionsCompose. LK-01's "the picker previews the stored face
  while Ignore fonts is on" reaches them with no QuickComms change.

## 3. Tests that pin current behaviour

| Test (path:line) | What it pins | Change under v1.81.0 |
|---|---|---|
| `tests/test_skin_windows.lua:345-361` "the modal window's template chrome is stock under Ka0s Default, every call" | `opts.stockDefault == true` on Shell, FadeNineSlice, TitleBar and CloseButton (`:353-360`) | **Rewrite (R-2):** assert the four calls carry no `stockDefault`, and that under Ka0s Default the window is painted (e.g. the close X recorded with a glyph, the NineSlice faded). |
| `tests/test_skin_windows.lua:363-382` "the modal window's Bg is the client's under Ka0s Default and faded under a skin" | the Bg art alpha is 1 under Ka0s Default (`:372`), 0 under OTHER (`:376`), and 1 again on the switch back (`:378`) | **Rewrite (R-2):** alpha 0 under Ka0s Default and under OTHER. The "red under" comment (`:374-375`) names the `stock` / FadeRegions choice made in 1b. |
| `tests/test_skin_windows.lua:7` (file header) | "the modal window's template chrome kept stock under Ka0s Default" | Reword. |
| `tests/test_skin_hud.lua:109-121` "a pad's labels, titles and header take hud.font while they follow, the pick when not" | OXANIUM while following, ARIAL off | Keep. **Add** an R-1 case: `Skin:SetIgnore(OWNER, nil, true)` makes a following label draw its stored face (Friz Quadrata, or the set pick) while `fontFromSkin` stays true. Untick returns OXANIUM. |
| `tests/test_skin_hud.lua:123-129` "a following face takes the Skin tab's font override" | the override reaches a followed face | Keep. Optionally add "Ignore fonts beats the override on the HUD" once LK-01 fixes that contract. |
| `tests/test_skin_hud.lua:166-179` "a dial's slice labels and ring title take hud.font while they follow" | the dial is OXANIUM | Add the same R-1 case for a dial label, or fold it into the pad case. |
| `tests/test_skin_hud.lua:232-248` "a skin switch repaints the chrome and the faces" | `FontKey == ResolveSkin(OTHER)["hud.font"]` (`:246`) | It reads the library's value, so it stays green when R-4 gives OTHER its own `hud.font`. No change, but it now exercises a real face rather than the KEEP fallback. |
| `tests/test_skin_hud.lua:317-326` step 10, `:321` "red under: ... ResetToSkin handed an absent companion ("@skin" lands in the picker)" | the `followSkin` split (1d) | Keep the assertions. Reword `:321` if the comment at `Library_Migrate.lua:219-225` is reworded. |
| `tests/test_skin_hud.lua:328-333` "without the library step 10 writes the companions itself" | the no-library arm | No change. |
| `tests/test_skinsetup.lua:311-321` "the tab's Ignore fonts reaches the library and the profile, one repaint" | `counts.looks == 1` | No change expected. If LK-01 adds a second notify on an Ignore-fonts toggle, `:320` goes red. That is a library regression, not a QuickComms change. |
| `tests/test_skinsetup.lua:274-281` "/qc set reaches an exception" | the GetIgnore pair | No change. |
| `tests/test_skinsetup.lua:394-404` "the degraded facade answers every name the live facade carries" | facade parity | **Goes red** if v1.81.0 adds any facade name (1e). Add the name to `core/SkinSetup.lua:424-432` (a no-op) or as a special member. |
| `tests/test_skinsetup.lua:409-423` "each host-copy skin token is the live library's Ka0s Default value" | `NS.SKIN_FALLBACK` equals the library's `ResolveSkin("ka0s")` | Red only if v1.81.0 changes a Ka0s Default value QuickComms copies. R-4 changes the eight other skins only, and R-8's `q.*` tokens are not copied. **Expected: no change.** Run it after the re-vendor. |
| `tests/test_skinsetup.lua:197-225` "the drag strip, the Preview dropdown and the reorder list are handed the owner" | owner wiring | No change. |
| `tests/test_skin_tools.lua:61-68` "under the default Scope (Ignore settings panel) a page widget stays stock" | the AceGUI proxy honours the Scope | No change. If LK-05/LK-06 add Scope behaviour for ReorderList, a sibling case for the reorder ghost under the default Scope can join it (optional). |
| `tests/test_skin_tools.lua:195-224` the debug console, its copy window and the perf panel are "painted for this owner" | `Skin.painted[f].owner == OWNER` | **Check after LK-06.** If the tool windows come under the panel Scope and stand down while it is on, the record may be absent under the default Scope, and these go red. The fix is to set `skin.ignorePanel` false in the case, or to assert the owner binding (descriptor `addonName`) without the record. |
| `tests/test_skin_picker.lua:69-82` "the spec names this owner ... General's Skin tab" | `spec.tab == "Appearance"` (`:80`), the tab **key** | No change. R-10 renames the label only, and the key stays "Appearance" (`libs/LibKa0s/OptionsAppearance.lua:3, 47`). No QuickComms test asserts the picker's title text. Proof: `grep -n 'Choose a skin\|BRAND\|Quick Comms' tests/test_skin_picker.lua` returns nothing. |
| `tests/test_vendor_sync.lua` (kit `tests/_kit/vendor_sync.lua`) | the vendored tag equals the CLAUDE.md provenance line | Moves with QC-RV: the provenance becomes v1.81.0. |

`docs/test-cases.md` is generated (`docs/test-cases.md:9`). The renamed cases at `:1318-1319` (the two
modal-window titles) and any new R-1 case change on regeneration, not by hand.

## 4. Smoke checks and doc passages whose expectation changes

### Ignore fonts on the HUD (R-1)

- `docs/smoke-tests.md:1726-1728` **SKIN-12**: "the windows' and the settings pages' text goes back to the
  game's face". It is silent on the HUD, and that silence is the documented current behaviour the rollout report
  cites (`2026-10-29-SKINNING_ROLLOUT/99_REPORT.md:65-66`). Rewrite: with Ignore fonts on, every pad and dial
  label whose *Use the skin's font* is ticked draws its own stored face (Friz Quadrata by default) live, its
  colors, size and flags unchanged; untick Ignore fonts and the skin's face returns. The composer's Font picker
  previews the stored face while Ignore fonts is on (LK-01).
- `docs/smoke-tests.md:1719-1724` **SKIN-11**: "every pad and dial label whose *Use the skin's font* is ticked
  takes [the override]". Add "(unless Ignore fonts is on, SKIN-12)".
- `docs/ARCHITECTURE.md:219-227` (The HUD): add one sentence that Ignore fonts keeps the stored face on a
  following block.
- `docs/settings-panel.md:95` (the Scope row): optionally gloss Ignore fonts as covering the pads and dials too.

### The stock look (R-2)

- `docs/smoke-tests.md:1646-1658` **SKIN-3**: "the callout popup and the icon browser (Blizzard's settings window
  exactly, its dim behind; X10) ... looks as before". Move this to the list of expected changes: under Ka0s
  Default they wear the Ka0s window. Also re-check "the drag strip and the reorder lists" (LK-05/LK-06) and the
  drag-strip tooltip (R-7, 1g).
- `docs/smoke-tests.md:1694-1702` **SKIN-8**: "under **Ka0s Default** both are Blizzard's settings window, as
  before ... Back to **Ka0s Default** → Blizzard's window comes back exactly ... Fail: a skinned frame left on
  Ka0s Default". Rewrite: Ka0s Default is the Ka0s window. The stock look is the **WoW Default** skin.
- `docs/smoke-tests.md:1739-1742` **SKIN-14**: "(the popup is Blizzard's settings window under Ka0s Default)".
  Rewrite to "the Ka0s window".
- `docs/smoke-tests.md:452-462` **EDIT-13**: "On **Ka0s Default** ... both are Blizzard's settings window, as
  before". Rewrite.
- `docs/smoke-tests.md:404-412` **EDIT-9** and `:464-470` **EDIT-14**: "looks like the settings window itself:
  the same background and border ... Blizzard's close X". These predate the rollout and passed on 2026-10-21. They
  now hold only under WoW Default, or not at all. Amend each with "(amended: under Ka0s Default the window is the
  Ka0s window, R-2)".
- `docs/ARCHITECTURE.md:233-236` (The windows): "keep Blizzard's `SettingsFrameTemplate` under Ka0s Default ...
  (X10, `opts.stockDefault`...)". Rewrite.
- `docs/ARCHITECTURE.md:333`, documented deviation `standalone-windows`, "The window edge": "Blizzard's
  `SettingsFrameTemplate` ... under Ka0s Default ... painted ... with `opts.stockDefault` (LibKa0s LK-05), so it
  stays the client's under Ka0s Default". Rewrite or retire this. The window is still **built** from the
  template, which the deviation covers, but under Ka0s Default it no longer looks like the client's. Its
  "decided by the owner" basis is superseded by R-2, so cite R-2.
- `docs/ARCHITECTURE.md:332`, deviation `standalone-windows` / `library-stack-§8` (the template's own close X):
  still accurate, since the X is still the template's button. Its rationale "to match the settings window
  exactly" no longer holds under Ka0s Default. Reword the rationale.
- `docs/settings-panel.md:383-386`: "(painted with `opts.stockDefault`, so Ka0s Default keeps the settings
  window exactly; DECISIONS X10)". Rewrite.
- `docs/settings-panel.md:391` and `:470`, the ASCII layouts: "window   Blizzard's settings window, titled Ka0s
  Quick Comms". Reword to "the settings template's window, in the skin".
- `docs/settings-panel.md:375` and `:462` ("Blizzard's `SettingsFrameTemplate`") describe the construction, which
  still holds. Keep them.
- `docs/module-map.md:134`, the `tests/test_skin_windows.lua` row: "the modal window's template chrome kept stock
  under Ka0s Default with `stockDefault` on every call, its Bg art faded under another skin and given back".
  Rewrite.
- `docs/module-map.md:72, 75` and `docs/taint.md:135` describe the template as the build. No change.

### The picker title (R-11)

- `docs/smoke-tests.md:1754-1760` **SKIN-17**: "a small window titled **Choose a skin for Ka0s Quick Comms** ...
  Fail: ... a title that does not name Ka0s Quick Comms". Rewrite: titled **Choose a skin**, with "Ka0s Quick
  Comms" on its own line above the dropdown, not cut off. Fail: a truncated name, or no name.
- `docs/settings-panel.md:109-110`: "a small window titled *Choose a skin for Ka0s Quick Comms*". Rewrite the
  same way.
- `docs/ARCHITECTURE.md:240-247` (the first-run picker) does not quote the title. No change.

### HUD face under non-Ka0s skins (R-4)

- `docs/smoke-tests.md:1668-1677` **SKIN-5**: "(Oxanium SemiBold on Ka0s Default, Friz Quadrata on the others:
  no other skin names a HUD face)" at `:1671`. Rewrite: each skin's own HUD face, named per skin from LK-04's
  `DECISIONS.md`.
- `docs/smoke-tests.md:1595-1599` **LOC-1**, the pads' fonts note: "Ka0s Default's Oxanium SemiBold, Friz
  Quadrata under the other skins". Rewrite the same way. The locale caveat ("LibKa0s registers a face only for
  the locales it can draw") stays.
- `README.md:145-157`, the font credits: if LK-04 registers a face the library did not ship before, add its
  credit here. If every HUD face is one of the eight families already listed, no change.
- `docs/known-limitations.md:170-174` and `docs/ARCHITECTURE.md:228-232` talk about Ka0s Default only. No change.
- `docs/schema.md:40-49`: the stored `font` defaults ("Friz Quadrata TT") are the player's picks, not the skin's.
  No change.

### Pending sign-off and version pins

- `docs/smoke-tests.md:1826-1831`: the "Owed: the skinning rollout" paragraph. The rewritten checks (SKIN-3,
  SKIN-5, SKIN-8, SKIN-11, SKIN-12, SKIN-14, SKIN-17, EDIT-9, EDIT-13, EDIT-14 and LOC-1) join a new "Owed: the
  library follow-ups (v1.81.0)" line.
- The v1.80.0 version pins that QC-RV moves to v1.81.0:
  - `CLAUDE.md:44`;
  - `docs/ARCHITECTURE.md:51`;
  - `docs/known-limitations.md:203, 205`;
  - `docs/module-map.md:4`.
- `docs/testing.md`: no Ignore-fonts, stock-look or picker-title passage. The skin suites are listed generically
  at `docs/testing.md:70`. **No change** unless a new suite file is added.

## 5. Current state and gate

- Branch `master`, tracking `origin/master`, **clean**: `git status -sb` shows `## master...origin/master` and
  nothing else. HEAD is `c77daa1` ("Merge feat/2026-10-29-skinning-rollout"). The only branch is `master`, with
  no feature branch left.
- Vendored LibKa0s: `CLAUDE.md:44`, "Bundles [LibKa0s](https://github.com/tusharsaxena/LibKa0s) v1.80.0 (MIT)."
  `CLAUDE.md:45` reads "LibKa0s icons: all (icon browser)." Skin major `LibKa0s-Skin-1.0` minor 7
  (`libs/LibKa0s/Skin.lua:88`).
- The latest re-vendor bundle is `docs/revendor/2026-10-24-v1.77.0`. Like the other addons, QuickComms has no
  bundle for v1.80.0 (rollout report "Not done").
- Gate, run on master on 2026-10-30:
  - `cd /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms && ~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua`
    tail:
    ```
    1254 passed, 0 failed, 1 skipped, 1255 total (16 shards)
    ```
    exit 0.
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` tail:
    ```
    Total: 0 warnings / 0 errors in 143 files
    ```
    exit 0.
  - The 1500-line cap is enforced inside the suite (kit `test_layout_cap`) and is green. The largest files
    touched here are well under it: `settings/ModalWindow.lua` 225, `core/SkinSetup.lua` 547,
    `modules/Pad_Render.lua` 681, `tests/test_skin_windows.lua` 572.
  - **Gate green.** The totals match the rollout's recorded 1254/0/1 (`99_REPORT.md:46`).

## 6. Nothing to change (exceptions.tsv candidates, each with its proof)

All commands run from the QuickComms root. Each one returned **nothing** on `c77daa1`.

| Ruling / item | Claim | Proof command |
|---|---|---|
| A: R-9 / LK-10 | no `__DrawsKey` or `DrawsKey` reach | `grep -rn '__DrawsKey\|DrawsKey' core modules settings defaults tests/*.lua` |
| B: R-8 / LK-09 | no `q.*` token read or copied | `grep -rnE '"q\.[a-z]+"' core modules settings defaults tests/*.lua` |
| C: R-1 / LK-01, R-5 / LK-05 | no hand-rolled Ignore or Scope read outside the seam and the schema row | `grep -rnE 'GetIgnore\|__PanelSkinned\|__FontsIgnored\|ignorePanel\|ignoreFonts' core modules settings \| grep -v 'core/SkinSetup.lua:91\|SchemaRows'` |
| D: R-3 / LK-03 | no close-art tint handling | `grep -rniE 'close.*(SetVertexColor\|SetTextColor\|Desaturat)\|(SetVertexColor\|SetTextColor).*close' core modules settings` |
| E: R-5 / LK-05 | no `S.Text` call outside the degraded stand-in | `grep -rnE '(Skin\|S)\.Text\(' core modules settings \| grep -v 'core/SkinSetup.lua:445'` |
| R-1 outline half | no `hud.outline` read | `grep -rn 'hud\.outline' core modules settings defaults tests/*.lua docs/*.md` |
| R-7 / LK-08 | no literal color passed to a tooltip line | `grep -rnE '(AddLine\|AddDoubleLine\|SetText)\([^)]*[ ,][01](\.[0-9]+)?\s*[,)]' core modules settings` (every tooltip call passes a token-derived variable or nil) |
| F: LK-06 widget reach | the Widgets major is used in three files only | `grep -rlo 'LibKa0s-Widgets-1.0' core modules settings` returns `core/WidgetsSetup.lua`, `modules/PreviewWindow.lua`, `settings/Editors.lua` |
| R-10 / WS-01 | the picker spec uses the tab **key**, which does not change | `grep -n 'tab = "Appearance"' core/SkinSetup.lua` returns `:322` only, the key, which stays "Appearance" (`libs/LibKa0s/OptionsAppearance.lua:3`) |

The R-7 grep catches numeric literals only. The listed
tooltip writers (1g) were read by hand: `settings/CalloutPopup.lua:203-210`, `settings/Groups_When.lua:321`,
`settings/IconBrowser.lua:236-239`, `modules/PreviewWindow.lua:98, 125` and `modules/Pad_Render.lua:71`. Each
passes a `gtip.*` token.

## 7. Items for QuickComms (summary for the implementer)

- **QC-RV:** re-vendor from `v1.81.0` (`git archive` of the tag), prune icons (`all`), and roll `CLAUDE.md:44` and
  the four version pins (section 4). Add any new facade name to the degraded arm (`core/SkinSetup.lua:424-452`)
  so `tests/test_skinsetup.lua:394` stays green.
- **QC-01:**
  - drop `stockDefault` from `settings/ModalWindow.lua:95-100`, and handle `stock = bgArt(...)` according to
    LK-02's shape (1b);
  - rewrite the comments at `settings/ModalWindow.lua:17-26, 81-83, 91-92` and `settings/IconBrowser.lua:50, 125`;
  - reword `modules/Library_Migrate.lua:219-225` (1d);
  - rewrite `tests/test_skin_windows.lua:345-382`;
  - add the R-1 HUD cases to `tests/test_skin_hud.lua`;
  - re-check `tests/test_skin_tools.lua:195-224` against LK-06.
- **QC-02:** the smoke checks SKIN-3, SKIN-5, SKIN-8, SKIN-11, SKIN-12, SKIN-14, SKIN-17, EDIT-9, EDIT-13,
  EDIT-14 and LOC-1, and the owed paragraph; `docs/ARCHITECTURE.md:219-236, 332-333`;
  `docs/settings-panel.md:95, 109-110, 383-391, 470`; `docs/module-map.md:134`; `README.md` credits only if
  LK-04 adds a face.
- **Lead decisions:**
  - (a) Does LK-02 also retire Shell's `opts.stock` region list? (1b)
  - (b) Do the modal windows' chrome fall under the Ignore settings panel Scope, or wear Ka0s under Ka0s Default
    as R-2 reads? (1b)
  - (c) Does LK-07 cover a picker key with an absent companion? (1d)
