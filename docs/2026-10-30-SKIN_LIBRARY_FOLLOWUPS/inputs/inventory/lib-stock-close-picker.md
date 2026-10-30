# M0 inventory: LK-02 (retire the stock look), LK-03 (CloseButton tint), LK-11 (picker title)

Read-only inventory of LibKa0s `master` at `ea1d92d` (v1.80.0 merged; there is no
`feat/2026-10-30-skin-library-followups` branch in LibKa0s yet, and the tree is clean). Every path below is
relative to `/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/` unless it names another repo. Current
documents: Skin `docs/api/Skin/version-7.15.11.5.9.2.4-docs.md` (Status **Current**, :12) and Options
`docs/api/Options/version-34.4.35.4.6.10.3.13.8.3.2.5.3.1-docs.md` (Status **Current**, :14). Per
`docs/api/README.md:13-16` a version document is never edited once superseded, so each item below that
moves a minor writes a **new** version document and a README index row (`docs/api/README.md:200` is the
current Skin row).

---

## LK-02 (R-2): retire `opts.stockDefault` (and the "stock" look under Ka0s Default)

### 1. What the mechanism is

Three helpers in `LibKa0s/SkinPaint.lua` (minor 11, `:110`):

| Helper | Site | What it does |
|---|---|---|
| `P.stockRegions(frame, opts, getters)` | `SkinPaint.lua:244-259` | Lists the client's template art on `frame`: the getters (`STOCK_FADE_GETTERS`, `:149-150`, or `STOCK_GETTERS` `:147-148`), the template fields (`STOCK_KEYS`, `:151-153`), the `NineSlice` pieces (`:249-252`), **plus every Texture in `opts.stock`** (`:253-257`; a non-Texture entry, a Frame such as `win.Bg`, is silently dropped by `P.isTexture`, `:255`). |
| `P.hasStock(frame, opts)` | `SkinPaint.lua:261-265` | True when `stockRegions` with `STOCK_GETTERS` finds anything (so `opts.stock` counts). |
| `P.keepStock(owner, rec, frame, opts)` | `SkinPaint.lua:779-799` | **The retired behaviour.** When `opts.stockDefault == true` (`:791`) and `lib:__DrawsKey(owner) == lib.DEFAULT` (`:792`): `P.unpaint` the target (`:793`), set `rec.regions.stockKept = true` (`:794`), answer true so the caller paints nothing. Otherwise clears the mark (`:797`) and answers false. |
| `P.stockDefault(owner, rec, frame, opts)` | `SkinPaint.lua:801-809` | Two jobs in one: **(a)** marks `rec.regions.stock = true` when `P.hasStock` (`:807`), the mark Shell (`:982`) and CloseButton (`SkinPaintControls.lua:557`) read to decide whether to fade/draw a glyph; **(b)** returns `P.keepStock(...)` (`:808`). Only (b) retires; (a) must stay. |

The `stockKept` mark is consulted by:

- `P.hook` wrapper: `SkinPaint.lua:443` (`if r and not r.regions.stockKept then fn(...)`), so every hooked hover/enable/focus handler is inert while kept.
- `live(frame)`: `SkinPaintControls.lua:76-81`, used by Checkbox's `SetChecked` hook (`:286-289`) and CloseButton's `own` SetScripts (`:565-566`).
- Cleared by `P.unpaint` (`SkinPaint.lua:776`) and by `P.track` when the target was Untracked meanwhile (`SkinPaint.lua:821`).

`lib:__DrawsKey` (`Skin.lua:752-759`; header note `Skin.lua:87`) exists for `P.keepStock` alone (`SkinPaint.lua:792` is its only library caller; grep of `LibKa0s/*.lua`). After LK-02 the library no longer calls it, which LK-10 (R-9, make it public) should know: its sole remaining consumer is PGFE's re-implementation (`../PremadeGroupsFilterExtension/core/SkinSetup.lua:382`).

### 2. Every primitive and what it does under Ka0s Default today

| Primitive | Site | Option today | Under Ka0s Default with `stockDefault = true` | Without it |
|---|---|---|---|---|
| `Shell` | `SkinPaint.lua:971-993` (call `:975`; fade `:982`) | `P.stockDefault` | nothing painted, prior paint given back | marks stock, fades `stockRegions(frame, opts)` incl. `opts.stock` textures, paints |
| `Panel`, `Inset` | `SkinPaintExtras.lua:240-268` (call `:244`) | `P.stockDefault` | kept | paints the box. **Note:** Panel/Inset never fade anything; `opts.stock` only sets the mark, which neither reads. So `opts.stock` on Panel is a no-op today. |
| `TitleBar` | `SkinPaintExtras.lua:88-100` (call `:92`, `unjustify` `:74-81`) | `P.keepStock` | kept, alignment given back | paints |
| `FadeNineSlice` | `SkinPaintExtras.lua:288-299` (call `:294`) | `P.keepStock` | NineSlice left | fades the nine pieces |
| `FadeRegions` | `SkinPaintExtras.lua:272-286` | **none** (its varargs are frames, not opts, `:274`, `:278`) | fades every non-Ka0s texture under every skin, Ka0s Default included (`:273`) | same |
| `Button` | `SkinPaintControls.lua:162-187` (call `:166`; fade `:171`) | `P.stockDefault` | kept | fades `stockRegions(btn, opts)` (opts.stock honoured, `:171`), boxes |
| `EditBox` | `SkinPaintControls.lua:218-234` (call `:222`; fade `:224`) | `P.stockDefault` | kept | fades, boxes |
| `Checkbox` | `SkinPaintControls.lua:297-317` (comment `:301`) | **none** ("No stockDefault here (minor 2)") | always paints the square box | same. `opts.stock` IS read for the fade (`:303`, with `CHECK_GETTERS`). |
| `Dropdown` | `SkinPaintControls.lua:325-340` (call `:329`; fade `:331`) | `P.stockDefault` | kept | fades, boxes |
| `Slider` | `SkinPaintControls.lua:424-449` (call `:428`; fade `:431`) | `P.stockDefault` | kept | fades only when `slider.track` is set |
| `Tab` | `SkinPaintControls.lua:485-502` (call `:493`; fade `:495`) | `P.stockDefault` | kept | fades `stockRegions(tab, opts)`; **`opts.stock` is load-bearing here** (OptionsTabs' atlas slices, below) |
| `CloseButton` | `SkinPaintControls.lua:552-571` (call `:556`) | `P.stockDefault` | kept, hover inert | stock: fades art + draws "x" glyph (`:557-560`); tints (see LK-03) |
| `PageButton` | `SkinPaintControls.lua:579-595` (call `:582`, **no opts passed**: `P.stockDefault(owner, rec, btn)`; fade `:584` `P.stockRegions(btn)`; box `:585` `P.box(rec, btn, T, BTN)`) | `P.stockDefault` with nil opts, so never kept | n/a: the signature is `(owner, btn, dir)` (`:579`), so neither `stockDefault` nor `opts.stock` nor `noBorder`/`noBg` can reach it | paints |
| `Text`, `Font`, `White`, others | `SkinPaintExtras.lua:316+` | none | always paint | same |

The partial coverage (Checkbox, FadeRegions, Text/Font and PageButton cannot keep stock) is exactly what
`../PremadeGroupsFilterExtension/modules/Panel.lua:25-35` records as the reason PGFE built a twin frame.

### 3. `opts.stock` is TWO things: a stock-look companion and a fade list

The ruling says "`stockDefault` and `stock` go". The code shows `opts.stock` is not a stockDefault
companion: it is a **fade list** honoured under every skin, used by the library itself and by consumers
that never pass `stockDefault`.

Library callers of `opts.stock` (all through the chrome's `O.__chromePaint`):

- `LibKa0s/OptionsTabs.lua:495` `skin("Panel", panel, { stock = panel and panel.__ka0sHalves })` (halves made at `OptionsTabs.lua:401`). A no-op on Panel (see table); the halves are actually faded by `skin("FadeRegions", panel)` at `:494`. Comment `:492-493` ("faded away from Ka0s Default (and put back on it)") is stale since SkinPaint minor 6.
- `LibKa0s/OptionsTabs.lua:502-503` `skin("Tab", b, { ..., fill = art.fill, stock = { art.left, art.mid, art.right } })`. **Load-bearing:** Tab fades only getters/STOCK_KEYS/NineSlice plus `opts.stock` (`SkinPaint.lua:245-258`), so without `opts.stock` the three settings-strip atlas slices would show under every skin, including Ka0s Default. `FadeRegions` is not a drop-in: it would also fade `art.fill`, which Tab repaints as its backing (`SkinPaintControls.lua:453-464`; `P.fill` never resets alpha, `SkinPaint.lua:360-379`).
- Options doc row pinning it: `docs/api/Options/version-34.4.35.4.6.10.3.13.8.3.2.5.3.1-docs.md:146` ("the three client atlases are the stock it fades away from Ka0s Default"; "away from Ka0s Default" is stale wording too).

Test pinning the fade list: `tests/test_skin_paint_controls.lua:427-443` (`K.Tab(stock, { stock = { art } })`, asserts the art is faded under Ka0s Default, `:439`, and under glass, `:442`).

Consumer callers (for the addon inventories; not this reader's scope, listed so the lead sees the blast
radius of a literal retirement):

- `../PremadeGroupsFilterExtension/modules/Panel.lua:861` `S.Shell(f, { stock = { f.Bg, f.TopTileStreaks } })`, no stockDefault (a pure fade list).
- `../QuickComms/settings/ModalWindow.lua:95` `S.Shell(f, { stockDefault = true, stock = bgArt(chrome.bg) })`, where `bgArt` (`:81-90`) works around `opts.stock` dropping Frames by handing over the Bg frame's texture regions.
- `../LibKa0sSkinTester/modules/ShowroomOwner.lua:114` `paint("Shell", win, { stockDefault = true, stock = { child(win, "Bg") } })`.

**Recommendation (for DECISIONS.md):** retire **`opts.stockDefault` only** (the switch that keeps the
client's look under Ka0s Default). Keep **`opts.stock`** as the fade list it already is under every
skin. That fades more, so it matches R-2's "Ka0s Default looks like Ka0s Default everywhere". Optionally
widen it to accept a Frame and fade that frame's own texture regions (as QC's `bgArt` does), which makes the
LK-05 example `stock = { win.Bg }` work: Bg is a Frame in `SettingsFrameTemplate`/`FlatPanelBackgroundTemplate`
(`../QuickComms/settings/ModalWindow.lua:80-81`). If the lead reads R-2 literally and removes `opts.stock`,
`OptionsTabs.lua:502-503` must fade its slices another way, the Tab test at
`tests/test_skin_paint_controls.lua:436-442` changes, and PGFE's `Panel.lua:861` loses its Bg fade.
Either way, **`opts.stockCheck`** (Checkbox, `SkinPaintControls.lua:292-309`, and the EllesmereUI
allow-list `SkinEUI.lua:99`) is a different option (keep the client's check mark), and it **stays**.

### 4. The retirement: exact edits

`LibKa0s/SkinPaint.lua` (minor 11 → **12**; header note after `:109`):

- Delete `P.keepStock` (`:779-799`). Reduce `P.stockDefault` (`:801-809`) to the mark only. Either keep the name for sibling-file compatibility, answering false always (a SkinPaintControls/Extras copy of an older minor pairs only with its own shell minor, `SkinPaintControls.lua:23`, `SkinPaintExtras.lua:19`, so a rename is safe), or rename it `P.markStock(rec, frame, opts)` and have it return nothing. Keep `if P.hasStock(frame, opts) then rec.regions.stock = true end`.
- `P.hook` (`:441-444`): drop the `not r.regions.stockKept` guard (`:443`).
- `P.unpaint` (`:776`) and `P.track` (`:821`): drop the `stockKept` lines.
- `prim.Shell` (`:975`): call the mark and fall through. Doc comment `:968-970`: drop the stockDefault sentence.
- Header (`:29-33`, `:107-109`): record minor 12, "the stock look retired (R-2)".
- `P.isDefault` (`:169-173`) is unrelated (it always answers false, kept for OptionsScroll's `__chromeAway`, `OptionsScroll.lua:269-277`). Leave it.

`LibKa0s/SkinPaintExtras.lua` (minor 5 → **6**; header `:31-34`):

- `prim.TitleBar` (`:92`): delete the `P.keepStock` line. `unjustify` (`:74-81`) then has no caller; delete it. `justify` still saves/gives back alignment through `P.saved(rec,"justify")`. Check that `P.unpaint` restores `justify` priors: it does **not** today (`SkinPaint.lua:761-777` restores alpha/font/colors/backdrop only). So with `unjustify` gone, an unpainted TitleBar keeps the skin's `title.align`. Either keep `unjustify` and call it from an unpaint extension, or add `"justify"` to `P.unpaint`'s restores. **Recommendation:** add a justify restore to `P.unpaint`; it is a latent gap independent of R-2.
- `panel()` (`:244`) and `prim.FadeNineSlice` (`:294`): drop the keep branch (the mark stays for Panel; FadeNineSlice sets `rec.regions.stock = true` itself at `:295`).
- Doc comments `:85-87` (TitleBar) and `:288-290` (FadeNineSlice): drop the stockDefault sentences.

`LibKa0s/SkinPaintControls.lua` (minor 9 → **10**, shared with LK-03; header `:45-50`):

- `live()` (`:75-81`): drop the `stockKept` test (the doubled doc comment at `:75-76` can collapse to one).
- `Button` `:166`, `EditBox` `:222`, `Dropdown` `:329`, `Slider` `:428`, `Tab` `:493`, `CloseButton` `:556`, `PageButton` `:582`: replace `if P.stockDefault(...) then return end` with the mark call.
- **PageButton forwards its opts** (R-2): change to `prim.PageButton = function(owner, btn, dir, opts)` (`:579`), `opts = type(opts)=="table" and opts or {}`, then `P.track(owner, btn, "PageButton", dir, opts)` (`:581`) so a replay carries it, `P.stockRegions(btn, opts)` (`:584`) and `P.box(rec, btn, T, BTN, opts)` (`:585`, giving `noBorder`/`noBg`). EllesmereUI: `SkinEUI.lua:224-239` `strip` drops a table argument for a primitive with no `ALLOWED` entry (`:231-232`), so EllesmereUI's `PageButton(btn, dir)` receives `nil` as its third argument. That is safe, and no `ALLOWED` row is needed.
- Stale doc comments to fix in the same pass: Button `:158-159` ("Ka0s Default leaves a stock-template button stock"), `buttonOpts` `:103-104` (lists `stock`, fine if kept), Tab `:484`, CloseButton `:534` and `:546-551`, PageButton `:578`. All describe the pre-minor-6 rule.

`LibKa0s/Skin.lua`: header note `:87` and `__DrawsKey`'s doc `:752-755` mention stockDefault. LK-10 rewrites `__DrawsKey` anyway; drop the stockDefault wording there.

`LibKa0s/SkinEUI.lua`: nothing to change. `stockDefault` was never in `ALLOWED` (`:96-100`), so it was already stripped.

**Stale callers degrade, no error:** every primitive reads `opts` keys by name and nothing validates
unknown keys (e.g. `SkinPaint.lua:974`, `SkinPaintControls.lua:165` `buttonOpts`). Once the reads are
gone, `stockDefault = true` is ignored and the target paints the Ka0s look. No guard is needed. Add a
test that proves it.

### 5. Docs to correct (new Skin version document)

In the new Skin version doc (copy of `version-7.15.11.5.9.2.4-docs.md` with the new minors), fix these rows:

- `:14` Supersedes line: say the new version retires `opts.stockDefault`.
- `:750-755` "Stock art is faded under every skin ... The one exception is a caller's `opts.stockDefault`": drop the exception.
- `:833-836` "Ka0s Default is a skin like the others ... unless its caller asks with `opts.stockDefault`": drop the clause.
- `:880` **FadeRegions row: "Ka0s Default fades nothing and puts them back."** Stale since SkinPaint minor 6; the code fades under every skin (`SkinPaintExtras.lua:272-273`). Replace with "under every skin, Ka0s Default included".
- `:882` FadeNineSlice row, `:883` TitleBar row, `:910` CloseButton row: drop the stockDefault sentences.
- `:911` PageButton row: `PageButton(btn, dir, opts)`, with opts forwarded (`stock`, `noBg`, `noBorder`).
- `:908` Tab row and `:747` (`opts.stock` fade list): keep, or (if widened) say a Frame entry fades its texture regions.
- `:980-1022` the whole section **"Stock under Ka0s Default (`opts.stockDefault`)"**, including the LK-05 example `:991-995` (`S.Shell(win, { stockDefault = true, stock = { win.Bg } })`, which today fades nothing for Bg because Bg is a Frame, `SkinPaint.lua:255`): replace it with a short "Retired" note. Since v1.81.0 the option is ignored and the target paints the Ka0s look; a player who wants the client's look picks WoW Default (R-2).
- `:1453-1454`, `:1459-1460` (eui section: "`stockDefault`, ... is dropped"; "Ka0s Default's stock rule does not apply"): drop the stockDefault mentions.
- Elsewhere: `docs/api/README.md:200` (current row: "`opts.stockDefault` keeps a template-built window...") gets a new row, and the old one becomes Superseded. `docs/api/CONSUMERS.md:77` lists `opts.stockDefault` as a v1.80.0 surface, so add the retirement. `CHANGELOG.md:159-168`, `:192`, `:234` stay (history); the v1.81.0 entry records the retirement under "What a consumer owes".
- The Options doc (`version-34.4...13...-docs.md:146`, "away from Ka0s Default") and `:195-196` ("On Ka0s Default the proxy paints nothing ... the rows are stock AceGUI") are stale from SkinAce minor 2 / SkinPaint minor 6. They are not stockDefault, but they are the same stale "Ka0s Default is stock" wording. Correct them only if Options takes a new version doc anyway (LK-11 gives it one).

### 6. Tests

- `tests/test_skin_stock_default.lua` (238 lines; in the runner list at `tests/run.lua:85`) pins the retired behaviour throughout: header `:1-14`, `paint()` `:42-49`, `isStock()` `:51-68`, cases `:72` (Ka0s Default stays the client's), `:82` (switch back gives stock back), `:100` (TitleBar justification), `:111` (hooks inert), `:142` (mark cleared), `:160` (Slider/EditBox/Tab), `:187` (without the option), `:210` (eui fallback is stock), `:227` (fail-closed eui). **Rewrite** it as `test_skin_stock_retired.lua` (or rewrite it in place). The new cases:
  1. Under Ka0s Default, a SettingsFrameTemplate window painted with `{ stockDefault = true, stock = {...} }` on Shell, FadeNineSlice, TitleBar and CloseButton is painted exactly as one painted without the option: NineSlice faded, close art faded, "x" glyph shown, title recolored. Red on master.
  2. No error is raised for the stale key on every primitive that took it (`Shell, Panel, Inset, TitleBar, FadeNineSlice, Button, EditBox, Dropdown, Slider, Tab, CloseButton`).
  3. Hover hooks fire under Ka0s Default for such a target (the `:111` case inverted).
  4. PageButton's opts are forwarded: `S.PageButton(b, "up", { stock = { art } })` fades `art`, `{ noBorder = true }` draws no edge, and a `Skin:Repaint` replays with the opts. Red on master, because the 3rd arg is not read.
  5. The eui route (`:210-225`) keeps passing. `stockDefault` was always stripped (`SkinEUI.lua:96-100`), so the "fallback is stock" assertion flips to "fallback is painted".
- `tests/test_skin_paint_controls.lua:427-443` (Tab `opts.stock`) stays green if `opts.stock` is kept.
- `tests/test_skin_paint.lua:366` (FadeRegions) already pins "fades under every skin"; the doc row is what is stale.
- The SkinPaint, SkinPaintExtras and SkinPaintControls minor assertions (grep `MODULES.SkinPaint` in `tests/test_skin_paint*.lua` and `tests/majors.lua`), and the versioning test (`tests/test_versioning.lua`, which needs the new Skin doc and members JSON from `tools/gen-api-members.lua`, `docs/api/README.md:44-46`), move with the minors.

### 7. Not part of LK-02: the "Ignore settings panel" Scope (stays, default on)

The owner's per-addon exception is a separate mechanism, and R-2 leaves it in place (owner answer,
2026-10-30). Do not touch it:

- State: `o.ignorePanel` / `o.ignoreFonts`, set by `Skin:SetIgnore` (`Skin.lua:611-626`), read by `Skin:GetIgnore` (`:600-604`), asked through `lib:__PanelSkinned` (`Skin.lua:628-632`) and `lib:__FontsIgnored` (`:634-638`).
- Consumers of the panel half: the settings chrome, `OptionsScroll.lua:259-266` (`__chromeSkin`), `:295-331` (`__chromeUnpaint`/`__chromeRelease`/`__chromePaint`), and the AceGUI rows (`SkinAce.lua:802`).
- It hands a target back to the client's look **per owner, by the player's choice**, under every skin. `stockDefault` was a **per call, by the host** choice under Ka0s Default only. LK-05/LK-06 extend the Scope to custom widgets. LK-02 removes only the host switch.

---

## LK-03 (R-3): `S.CloseButton` does not save the art's prior tint

### 1. How it tints today

`LibKa0s/SkinPaintControls.lua:520-571`:

- `closeArt(btn, rec)` (`:520-526`): the art is `btn.icon` (Texture → `SetVertexColor`), else `btn.glyph` (FontString → `SetTextColor`), else the library's own glyph `rec.regions.glyph` (drawn by `closeGlyph`, `:537-543`, for a stock button only).
- **Rest tint** (`:561-563`): `art[method](art, rgb(c))` with `c = P.T(owner)["close.rest"]`. This is a **direct write**. It does not go through `P.tint` (`SkinPaint.lua:396-413`), so **no prior color is recorded** in `rec.regions.saved[method]`.
- **Hover** `closeHover` (`:528-532`): direct writes of `close.hot`/`close.rest`, also unrecorded. That is acceptable for a transient hover, provided the rest write records the prior.
- `opts.own` (`:564-567`): **SetScript**s OnEnter/OnLeave with closures gated by `live(self)` (`:76-81`), **replacing** the host's scripts. For `Core.MakeCloseButton` (`Core.lua:269-307`) those are Core's own CLOSE_REST/CLOSE_HOT scripts (`Core.lua:286-287` icon, `:293-294` glyph), and they are not saved. Without `own`: `P.hook` HookScript (`:569-570`).
- Stock button: `rec.regions.stock` (set by `P.stockDefault` → `P.hasStock`) causes the art to be faded (`:558`, alpha recorded by `P.fade`, `SkinPaint.lua:382-387`) and the "x" glyph to be drawn (an `__ours` region, hidden on unpaint, `SkinPaint.lua:772-774`).

### 2. What is saved and restored

| Property | Saved? | Restored by `P.unpaint` (`SkinPaint.lua:761-777`)? |
|---|---|---|
| Stock art alpha | yes (`P.fade`) | yes (`:763`) |
| Library glyph | n/a (ours) | hidden (`:772-774`) |
| **`btn.icon` vertex color / `btn.glyph` text color (the host's art)** | **no** (direct write, `:563`) | **no**: keeps the skin's `close.rest` |
| Host OnEnter/OnLeave under `own` | **no** (SetScript, `:565-566`) | **no**: after the record is gone, `live()` answers nil and the hover is dead |

`close.rest` and `close.hot` are non-nilable (`SkinDefs.lua:113`). Ka0s Default sets them (`SkinDefs.lua:220`)
and every skin derives from it (`SkinDefs.lua:19-20`), so the "token resolves to nil, put the prior back"
path of `P.tint` (`SkinPaint.lua:409-412`) never fires for a close button. Only `P.unpaint` matters.

### 3. When it unpaints

| Trigger | Site | Reaches a CloseButton? |
|---|---|---|
| Another owner paints the target | `P.track`, `SkinPaint.lua:815-816` | yes (a pooled or shared close button) |
| `opts.stockDefault` under Ka0s Default | `P.keepStock`, `SkinPaint.lua:792-793` | yes today. **This is the BL case in the rollout report (follow-up 6)**; it is removed by LK-02 |
| Entering EllesmereUI (give back NATIVE-primitive targets) | `SkinEUI.lua:337-353` (`CloseButton` is NATIVE, `SkinEUI.lua:83-86`) | yes |
| Ignore settings panel on a chrome target | `OptionsScroll.lua:295-300`, `:304-310`, `:316-331` | not today. No chrome path paints `CloseButton` (grep `__chromePaint(` in `Options*.lua`). It **will** once LK-05/LK-06 scope custom windows (the "scope that leaves it stock" of the plan's LK-03 row) |
| AceGUI release | `SkinAce.lua:637`, `:725` | no CloseButton on AceGUI parts |
| `Skin:Untrack` | `Skin.lua:949-955` | **restores nothing** (forgets only). After it, an `own` button's hover closures see `live()` == nil and do nothing |

### 4. The fix

In `LibKa0s/SkinPaintControls.lua` (minor 10, together with LK-02):

1. **Rest tint through `P.tint`.** Replace `:561-563` with
   `local art, method = closeArt(btn, rec); if art then P.tint(rec, art, P.T(owner), "close.rest", method) end`.
   `P.tint` records the art's own color the first time (`SkinPaint.lua:404-407`; the getter is derived
   from the method name: `GetVertexColor` / `GetTextColor`, both in the kit mocks,
   `tests/_kit/mock_paint.lua:130`, `:200`). `P.unpaint`'s `restoreColors(rec, "SetTextColor")` and
   `restoreColors(rec, "SetVertexColor")` (`SkinPaint.lua:766-767`) then give it back, and they clear the
   priors, so a later paint records afresh. `closeHover` (`:528-532`) can keep its direct writes: the prior
   is recorded once, before any hover.
2. **`own` buttons: save the host's hover pair and fall back to it.** Before the SetScripts at
   `:565-566`, record `btn:GetScript("OnEnter")` and `btn:GetScript("OnLeave")` once in `rec.regions`
   (e.g. `rec.regions.closeScripts`, only when nil, so a repaint never records the library's own
   closures). In the closures, when `live(self)` is nil, call the saved script. A button handed back
   (unpaint plus Untrack, or a record dropped) then hovers in Core's CLOSE_REST/CLOSE_HOT again, as it
   did before it was painted. The kit has `GetScript` (`tests/_kit/mock_base.lua:157`).
   *Alternative, if the lead prefers less code:* only fix (1), and document that an `own` button's
   hover follows its record.
3. Fix the doc comment `:545-551` (stale "left stock in Ka0s Default"; drop stockDefault; say the art's
   own tint is recorded and given back), and `:534` ("A stock close button away from Ka0s Default").

### 5. Tests (in `tests/test_skin_paint_controls.lua`, beside `:447-490`)

- **The art's own tint comes back.** Build a button with `b.icon` at vertex color (0.2, 0.4, 0.6) and
  run `S.CloseButton(b)` under `contrast`; assert `close.rest`. Then unpaint
  (`Skin.__P.unpaint(Skin.painted[b], b)`, or move it to another owner with `F.owner(Skin,"Other").CloseButton(b)`
  followed by an assertion on the first owner's give-back) and assert `0.2,0.4,0.6`. Red on master.
- The same with `b.glyph` (FontString, `SetTextColor`).
- **`own`:** `core.MakeCloseButton(parent, fn, OWNER)` for a registered owner (`Core.lua:303-304`), then
  unpaint and Untrack it, fire `OnEnter`, and assert Core's `CLOSE_HOT` (1, .3, .3). Red on master,
  because the hover is dead.
- **Keep green:** `:447-472` ("CloseButton on Ka0s Default is Core's close button, call for call"). Its
  tracer keeps only `SetTextColor` and `SetScript` lines (`:451-459`), so the extra `GetTextColor` read
  `P.tint` makes does not change it. Also keep `:476-490` (stock glyph under every skin).
- Consumer context: BankLedger's B:MakeCloseButton path (`../BankLedger/modules/Browser.lua:99`,
  `../BankLedger/tests/test_skin_windows.lua:226-290`) was the reporter (BL-A1). With LK-02 its
  stockDefault scenario is gone, and the save/restore still covers owner moves and the EllesmereUI entry.

---

## LK-11 (R-11): the first-run picker's title and the addon's name

### 1. Today

`LibKa0s/OptionsSkinPicker.lua` (Options file minor **1**, `:89`; attached by Options minor 34):

- Constants (`:120-126`): `WIDTH, PAD, TOP = 280, 12, 40`; `DD_H, ROW_H, ICON, BTN_H, APPLY_W = 26, 22, 24, 24, 80`; `BASE_H = TOP + DD_H + PAD + BTN_H + 10` (= 112); `SWATCH = 10`; `HEIGHT_SHARE = 0.75`.
- Words (`:105-118`): `TITLE_FOR = "Choose a skin for %s"` (`:106`). The header says PK-02 replaced the older `TITLE` with it (`:80-81`).
- `titleText(S, Skin, owner)` (`:240-245`): `string.format(S.TITLE_FOR, Skin:OwnerLabel(owner) or owner)` under pcall; when the format fails, the raw string.
- The title FontString, `buildChrome` (`:636-651`): `GameFontNormal`, anchored `TOPLEFT +28,-8` to `TOPRIGHT -28,-8` (`:638-639`), `SetWordWrap(false)` (`:640`). That leaves **224 px for one line, and the client truncates past it**: the owner's screenshots, every addon. The window skin is `core.ApplySkin(f, nil, P.owner)` (`:643`), which paints `frame.title` with the title role (Shell: `SkinPaint.lua:991-992`; Core colors it). The close control is `core.MakeCloseButton(f, hide, P.owner)` at `TOPRIGHT -6,-6` (`:644-649`).
- The title is set in `applySpec` (`:690`) on every show.
- The dropdown row is at `y = -TOP`: `anchorDropdown` (`:616-621`) is `TOPLEFT PAD,-TOP` with its right edge on the eye, or the gear (`:617`, `:620`). The gear is at `TOPRIGHT -PAD, -(TOP + (DD_H-ICON)/2)` (`:625`), and the eye sits left of the gear (`:627`).
- The list is at `-(TOP + DD_H + 2)` (`:588-589`). `layout()` sets the height to `BASE_H + listH + 2` while open (`:378-385`).
- Apply is `BOTTOMRIGHT -PAD,10` (`:630`); Apply to all runs from `BOTTOMLEFT PAD,10` to Apply's left (`:632-633`).
- Width: `f:SetSize(WIDTH, BASE_H)` at build (`:659`), never changed afterwards.
- Header prose: `:11-14` ("the title, "Choose a skin for <the addon's label>", and the close control").

The longest roster label is **"Ka0s Premade Groups Filter Extension"** (36 characters):
`../WowAddonStandards/standards/ADDONS.md:30`, registered as `label = BRAND`
(`../PremadeGroupsFilterExtension/core/SkinSetup.lua:85`, `:376`). The others are 13 to 27 characters
(e.g. "Ka0s Party Frame Enhanced", `../PartyFrameEnhanced/core/SkinSetup.lua:71`). `Skin:OwnerLabel`
is `Skin.lua:447-450`.

### 2. The change

1. **Words.** Replace `TITLE_FOR` with `TITLE = "Choose a skin"` in `lib.SKIN_PICKER_STRINGS` (`:105-106`).
   No addon passes `TITLE_FOR` in `spec.strings` (grep across the collection's `*.lua`, excluding
   `libs/`, finds only LibKa0s's own tests), so a stale override is simply an unused key: `mergeStrings`
   (`:228-238`) copies any string. Keeping `TITLE_FOR` as a retired key is unnecessary. The table is a
   documented lib-level surface (`docs/api/CONSUMERS.md:86`, Options doc `:2436-2442`), so the new doc
   records the key change.
2. **Title.** `applySpec` (`:690`): `f.title:SetText(S.TITLE)`. Delete `titleText` (`:240-245`).
3. **The addon's name on its own line above the dropdown.** In `buildChrome` (or a new
   `buildOwnerLine`), add a FontString, recommended field name **`frame.ownerLabel`** (addon tests will
   assert on it). Anchor it `TOPLEFT PAD, -TOP` to `TOPRIGHT -PAD, -TOP`, with
   `SetWordWrap(false)` and `JustifyH("LEFT")`, text `Skin:OwnerLabel(owner) or owner` set in
   `applySpec`. Paint it through the facade so it follows the skin: recommend
   `P.Sk.Text(f.ownerLabel, "heading")` (`SkinPaintExtras.lua:310-316`: the title face, `text.heading`)
   or `"body"`. The implementer's call goes in DECISIONS.md.
4. **Move the dropdown row down one line.** Add `LABEL_H` (about 18) and `DD_TOP = TOP + LABEL_H + 4`, and
   use `DD_TOP` wherever the dropdown row uses `TOP` today: `anchorDropdown` `:619`, gear `:625`, list
   `:588-589` (`DD_TOP + DD_H + 2`), and `BASE_H` `:122` (`DD_TOP + DD_H + PAD + BTN_H + 10`). The title
   stays at `-8`. The eye stays relative to the gear (`:627`).
5. **Never truncated: the window grows to fit.** Add `fit(p)`, called from `applySpec` (`:688-698`) and
   from the `OnLooksChanged` refresh (`:680-682`, since a skin switch changes the label's face and size;
   `Skin:SetIgnore`/`SetChoice` repaint before they notify, `Skin.lua:620-623`). It does:
   `local w = label.GetUnboundedStringWidth and label:GetUnboundedStringWidth() or label:GetStringWidth()`,
   then `f:SetWidth(math.max(WIDTH, math.ceil(w) + 2 * PAD))`. Use **GetUnboundedStringWidth**: with
   both side anchors set, `GetStringWidth` reports the width that fits, not the text's full width. Every
   other piece is anchored to both sides or to the right edge (title `:638-639`, dropdown `:619-620`, list
   `:588-589`, buttons `:625-633`), so they follow the width. The kit mocks answer 0 for both widths
   (`tests/_kit/mock_paint.lua:231`, `:233`), so a test must `rawset` the label's width getter, and the
   window stays 280 by default.
   *Alternative:* allow two lines (`SetWordWrap(true)`, with height grown by `GetStringHeight`). The plan
   (LK-11 row) says "the window grows to fit", so width growth is recommended.
6. **Header and minor.** OptionsSkinPicker minor 1 → **2** (`:89`, with a note after `:88`). Header
   `:11-14` describes the title line and the owner line. The Options version key becomes
   `34.4.35.4.6.10.3.13.8.3.2.5.3.2` (unless other Options files move in the same release). That needs a
   new Options version doc whose picker section (copied from `:2363-2375` and `:2436-2442` of the current
   doc) gives the title "Choose a skin" (`TITLE`), the owner line (`frame.ownerLabel`,
   `Skin:OwnerLabel(owner)` else the owner's name, one line, never truncated: the window widens from 280
   to fit it), and the dropdown below it.

### 3. Tests that pin the title (`tests/test_options_skin_picker.lua`)

| Line | Pins | Change |
|---|---|---|
| `:8` (header) | "titled "Choose a skin for <the addon's label>"" | reword |
| `:179` | `SKIN_PICKER_STRINGS.TITLE_FOR == "Choose a skin for %s"` | `TITLE == "Choose a skin"`, `TITLE_FOR == nil` |
| `:206-226` (`:208` red-under line, `:218` width 280, `:219` title) | title names the addon | title `"Choose a skin"`, `f.ownerLabel:GetText() == OWNER .. " Label"`, width still 280 for a short label. Red-under note: "TITLE_FOR put the addon in the title, where a long label was cut off (R-11)" |
| `:676`, `:686` | a repeat call's `strings.TITLE_FOR` reaches the title | use `strings.TITLE` (or assert on another word) |
| `:937-955` (`:943`, `:945`, `:951`, `:953-954`) | `TITLE_FOR` translation, non-formatting translation shown as is | `TITLE = "Skin waehlen"` → `f.title:GetText() == "Skin waehlen"`. The `"100% %d"` case (`:953-954`) loses its purpose (no format any more): drop it, or keep it as "shown verbatim" |
| `:301`, `:362` | the title repaints live (title.text color) | unchanged |
| `:255-260` | the window grows when the list opens (`GetHeight` comparison) | unchanged in shape; BASE_H grows |

New cases:

- **(a)** The owner line sits above the dropdown. Its anchor y is `-TOP` and the dropdown's TOPLEFT y is
  below it. Read `__pts` (the harness records anchors, `:41-58`).
- **(b)** A long label widens the window. Register an owner labeled
  `"Ka0s Premade Groups Filter Extension"`, `rawset` the owner line's `GetUnboundedStringWidth` to answer
  300, show the picker, and assert `f:GetWidth() == 324` (300 + 2*12) and that the title is still
  `"Choose a skin"`. Red on master.
- **(c)** A skin switch that changes the measured width refits it (via `OnLooksChanged`).

Addon tests and smoke checks that pin the old title (for the addon inventories; listed as pointers only):
`../AbsorbTracker/tests/test_skin_picker.lua:221`, `../BankLedger/tests/test_skin_picker.lua:275`,
`../KickCD/tests/test_skin_picker.lua:252`, PanelMaster (`inputs/inventory/PanelMaster.md:40,54,70`),
and the smoke rows in `../AbsorbTracker/docs/smoke-tests.md:192`,
`../BankLedger/docs/smoke-tests.md:1172`, `../ConsumableMaster/docs/smoke-tests.md:608`,
`../DpsRace/docs/smoke-tests.md:631`, `../DropWatcher/docs/smoke-tests.md:3051` and
`../KickCD/docs/smoke-tests.md:1389`, plus settings-panel docs (`../AbsorbTracker/docs/settings-panel.md:356`,
`../BankLedger/docs/settings-panel.md:129`, `../DpsRace/docs/settings-panel.md:115`).

---

## Summary for the lead

- **LK-02:** retire `opts.stockDefault` across 11 primitives (`P.keepStock`, the `stockKept` mark, the
  three guards). Keep `P.stockDefault`'s stock **mark**, which Shell and CloseButton need. **Decide
  `opts.stock`:** it is a fade list used under every skin by `OptionsTabs.lua:502-503` (load-bearing)
  and by PGFE/QC, so the recommendation is to keep it (and optionally accept Frames). PageButton gains
  `opts` (`SkinPaintControls.lua:579-585`). The FadeRegions doc row is stale since minor 6. The LK-05
  example's `stock = { win.Bg }` drops the Frame (`SkinPaint.lua:255`). Also add the TitleBar
  justification restore to `P.unpaint`. Minors: SkinPaint 12, SkinPaintExtras 6, SkinPaintControls 10;
  new Skin doc; `test_skin_stock_default.lua` rewritten.
- **LK-03:** the rest tint is a direct write (`SkinPaintControls.lua:561-563`). Route it through `P.tint`
  so `P.unpaint` restores the art's own color, and save and fall back to the host's hover scripts for
  `opts.own` (`:564-567`). Three red tests.
- **LK-11:** `TITLE = "Choose a skin"`, a new `frame.ownerLabel` line at `-TOP`, the dropdown row moved
  down by `LABEL_H` (four sites plus `BASE_H`), and the width grown to fit `GetUnboundedStringWidth`.
  OptionsSkinPicker minor 2; new Options doc; 6 test sites in `tests/test_options_skin_picker.lua` move
  and 3 cases are added.
