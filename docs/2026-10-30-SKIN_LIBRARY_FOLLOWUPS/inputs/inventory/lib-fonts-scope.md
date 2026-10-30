# M0 inventory: LK-01 (R-1, Ignore fonts reaches the HUD) and LK-05 (R-5, S.Text and ReorderList obey the Scope)

This was read-only, against LibKa0s `master` at `ea1d92d` (v1.80.0 merged), with a clean tree. Baseline:
`ka0s-bounded lua tests/run.lua` gives **3220 passed, 0 failed, 2 skipped (3222)**.

Library paths are relative to `../LibKa0s/`. Addon paths are relative to `GIT/`.

---

## 0. The two exceptions, and who asks them today

| What | Where |
|---|---|
| Storage: `o.ignorePanel` and `o.ignoreFonts` on the owner record | `LibKa0s/Skin.lua:618` |
| `Skin:GetIgnore(owner)` returns `panel, fonts`, or `false, false` when the owner is unregistered | `LibKa0s/Skin.lua:600-604` |
| `Skin:SetIgnore(owner, panel, fonts)`: nil keeps that half. On a change it calls `Repaint(owner)` and `notify(o)` (the OnLooksChanged listeners), unless a reload is pending | `LibKa0s/Skin.lua:611-624` |
| `Skin:__PanelSkinned(owner)` is `o ~= nil and not o.ignorePanel`, so it is **false for an unregistered owner** | `LibKa0s/Skin.lua:628-631` |
| `Skin:__FontsIgnored(owner)` is `o ~= nil and o.ignoreFonts == true` | `LibKa0s/Skin.lua:634-637` |

**Ignore fonts** is checked in exactly **one** place today:

- `P.font`, at `LibKa0s/SkinPaint.lua:539`: `if ... lib:__FontsIgnored(owner) then return P.unfont(rec, fs) end`. This covers
  every primitive that labels a string through `P.font`/`P.label`: `SkinPaint.lua:567,992`,
  `SkinPaintControls.lua:178,195,227,338`, `SkinPaintExtras.lua:98,326,333,342`, and the AceGUI rows
  (`SkinAce.lua:279,416,442,461,593`).

**Ignore settings panel** (`__PanelSkinned`) is checked in exactly **two** places today:

- `Skin:PaintAce`, at `LibKa0s/SkinAce.lua:802-806`.
- The Options chrome, through `lib.__chromeSkin`, at `LibKa0s/OptionsScroll.lua:259-265` (and
  `__chromeAway` at `:269-277`, which builds on it).

Nothing else in the library reads either exception. No token read (`Token`, `Color`, `Resolve`,
`__Tokens`, `BarStyle`) reads them, and no Widgets file reads them.

---

## 1. LK-01: every path that resolves a HUD face or outline

### 1.1 Engine paths (Skin.lua)

| # | Path | Site | What it does today |
|---|---|---|---|
| E1 | `Skin:Resolve(owner, kind, value, fromSkin)` | `Skin.lua:868-871` | `if value == FROM_SKIN or fromSkin == true then return self:Token(owner, kind) end; return value`. **It never asks `__FontsIgnored`.** |
| E2 | Facade `S.Resolve(kind, value, fromSkin)` | `Skin.lua:1019` | A trampoline to E1 |
| E3 | `Skin:Token(owner, name)` | `Skin.lua:811-813` | `return self:__Tokens(owner)[name]`, with no exception check |
| E4 | Facade `S.Token(name)` | `Skin.lua:1017` | A trampoline to E3 |
| E5 | `Skin:Color` / `S.Color` | `Skin.lua:816-820`, `:1018` | Reads E3, but only for tables, so a HUD string never comes back. Not affected |
| E6 | `__Tokens` = `withOwnTokens(withOverrides(base))` | `Skin.lua:804-807` | The whole table. `withOverrides` writes the **font override into `hud.font`** (`Skin.lua:727`). Every primitive reads `__Tokens` through `P.T` (`SkinPaint.lua:164`) |
| E7 | Owner tokens with `follow = "hud.font"` | `ownValue`, `Skin.lua:766-782` | Reads `t[def.follow]` from the `__Tokens`-level table, not through `Token`. No addon defines one today: `grep 'follow *= *"hud\.'` over all 15 addons and the Skin Tester finds nothing |
| E8 | `FROM_SKIN = "@skin"` | `Skin.lua:99` (facade `S.FROM_SKIN`, `:1015`) | Resolves only through E1 |
| E9 | `Skin.ResetToSkin` | `Skin.lua:892-911` | Writes companions or the sentinel. It is not a resolver (LK-07 owns it) |

Where the token values come from: Ka0s Default has `["hud.font"] = "Ka0s Oxanium SemiBold"` and
`["hud.outline"] = "OUTLINE"` (`SkinDefs.lua:307-308`). The schema line is at `SkinDefs.lua:156`, and the KEEP
fallback to Friz for the other skins is at `SkinDefs.lua:524-525` (LK-04 owns that). Under `eui`, `FONT_TOKENS` is
only `font.body`/`font.title` (`SkinEUI.lua:108`), so `hud.font` stays the Ka0s base value.

### 1.2 The paint getter (SkinPaintExtras.lua)

| # | Path | Site |
|---|---|---|
| G1 | `prim.BarStyle(owner)`, the facade `S.BarStyle()`, returns `font = P.media("font", T["hud.font"])`, `fontKey = T["hud.font"]`, `outline = T["hud.outline"]` | `SkinPaintExtras.lua:437-449` |

No addon calls `S.BarStyle()` (a grep over the 15 addons and the Skin Tester outside `libs/` finds nothing;
DpsRace's `Runs.BarStyle` at `DpsRace/modules/Results_Runs.lua:597` is its own function). Only two
library tests pin it: `tests/test_skin_override.lua:69-71` and `tests/test_skin_paint.lua:570-578`.

### 1.3 The composer's fromSkin companions and the font picker preview

| # | Path | Site |
|---|---|---|
| C1 | `FROM_SKIN.font = { token = "hud.font", label = "Use the skin's font", ... }` | `OptionsCompose.lua:330-332` |
| C2 | `skinValue(token)` calls `Skin:For(owner)` and then `S.Resolve(token, nil, true)` | `OptionsCompose.lua:515-521` |
| C3 | `governed(r, companion, token)` sets `r.disabledIf = companion` and `r.skinValue = fn(row)`. When the companion is true it answers C2's value | `OptionsCompose.lua:524-536` |
| C4 | `fromSkinRow` emits `<key>FromSkin` and governs the picker (and the size row for the icon family) | `OptionsCompose.lua:542-554`; FontGroup's call is at `:662` |
| C5 | The flow engine's `read(row)` shows `row.skinValue(row)` first when it answers non-nil, and the stored value otherwise | `OptionsWidgets.lua:422-427` |
| C6 | `disabledIf` is resolved by `isDisabled`/`bindDisabled` | `OptionsWidgets.lua:457-482` |
| C7 | A live refresh. `SetIgnore` calls `notify`, which fires the OnLooksChanged listener that re-renders the open pages one frame later (OptionsScroll minor 7) | `Skin.lua:619-622`; `OptionsScroll.lua:25-28`, `:434-457` |

The composer has **no outline companion**: `fontFlags` (`OptionsCompose.lua:653-656`) is never
governed. A host reaches `hud.outline` only through `S.Token("hud.outline")` or its own
`S.Resolve("hud.outline", ...)`. For example, ConsumableMaster uses
`ConsumableMaster/modules/MacroBarButton.lua:166`.

### 1.4 How the addons resolve it today, and their workarounds (for the XX-01 lists)

| Addon | Resolve site | Its own Ignore-fonts patch |
|---|---|---|
| AbsorbTracker | `core/Data.lua:138` (FOLLOWS `font = {"hud.font","fontFromSkin"}`), `NS.MediaKey` at `:145-157` | `:148` `if key == "font" and NS.SkinFontsIgnored() then return stored, false end`; the helper is at `core/SkinSetup.lua:329` |
| AuraMaster | `modules/Style.lua:57-65` (`Style.SkinKey`), `:1055` | `:60` `if token == "hud.font" and NS.SkinFontsIgnored() then return key end`; the helper is at `core/SkinSetup.lua:441-445` |
| ConsumableMaster | `modules/MacroBarButton.lua:153` (`S.Token("hud.font")`), `:166` (`S.Token("hud.outline")`), `:180` (`BB.Follow`) | `:147-149` restores the count font while ignored; the helper is at `core/SkinSetup.lua:539-543` |
| KickCD | `modules/IconGrid_Render.lua:861` (`NS.SkinResolve("hud.font", nil, true)`), `:890`; `modules/Castbar_Skin.lua:165`; `modules/UnitLabel.lua:95` | the helper is at `core/SkinSetup.lua:116` (check its use for fonts in M0's addon inventory) |
| PartyFrameEnhanced | `modules/Element.lua:119` | `core/SkinSetup.lua:370-376` (`NS.SkinIgnoresFonts`) |
| QuickComms | `modules/Pad_Render.lua:92` | its Ignore-fonts check is owned by the QC inventory (plan XX-02 names "the QuickComms Ignore-fonts check") |
| MultiMeters | `modules/Row.lua:780`, `Window.lua:835`, `Window_Header.lua:160,264`, `Tooltip.lua:305` (`NS.SkinMediaKey`, `media("font","hud.font","Friz Quadrata TT")`) | none found by grep. The MM inventory should confirm whether it patches |
| DpsRace | `modules/Hud_Appearance.lua:42` (`FOLLOWS font = "hud.font"`) | none found by grep. The DR inventory should confirm |

Every patch that exists implements the same rule: **while Ignore fonts is on, the stored pick wins
whatever the companion says, and a stored `"@skin"` sentinel answers nil** (stated explicitly at
`ConsumableMaster/modules/MacroBarButton.lua:170-172`). The library change below adopts that rule, so
every patch becomes redundant and keeps the same behaviour if left in place.

### 1.5 The proposed minimal change (LK-01)

**Skin.lua (bump minor 7 → 8).** Add one table and gate two members:

```lua
-- The HUD's two font tokens: "Ignore fonts" makes the stored value win for them (R-1).
local HUD_FONT = { ["hud.font"] = true, ["hud.outline"] = true }

local function hudFontIgnored(owner, name)
  return HUD_FONT[name] == true and lib:__FontsIgnored(owner)
end

function lib:Token(owner, name)
  if hudFontIgnored(owner, name) then return nil end      -- "the skin leaves it alone": the host's own stands
  return self:__Tokens(owner)[name]
end

function lib:Resolve(owner, kind, value, fromSkin)
  if hudFontIgnored(owner, kind) then                      -- the stored value wins (R-1)
    if value == self.FROM_SKIN then return nil end         -- a sentinel names no face of its own
    return value
  end
  if value == self.FROM_SKIN or fromSkin == true then return self:Token(owner, kind) end
  return value
end
```

- The Resolve gate is needed **as well as** the Token gate. Without it, `Resolve(kind, stored, true)`
  would call `Token`, get nil, and lose the stored pick.
- Token answering nil matches its documented contract, "nil for a token the skin leaves alone"
  (`Skin.lua:809-810`; `docs/api/Skin/version-7.15.11.5.9.2.4-docs.md:81`). Every caller already handles
  nil: `KickCD/modules/IconGrid_Render.lua:861` (`or ""`), `ConsumableMaster/modules/MacroBarButton.lua:154`
  (`type(face) ~= "string"` returns early, **without restoring**. CM's own `restoreCountFont`
  path at `:147` must therefore stay until it is re-vendored, or CM moves to `Resolve`), and MultiMeters
  `Tooltip.lua:305` (falls back to Friz Quadrata TT).
- Leave `__Tokens`/`P.T` unchanged. `P.font` already hands strings back through `__FontsIgnored`, and a
  gate in `__Tokens` would change every primitive's cache (`__overTok`, `__ownTok`) for no gain.
- `hud.fontSize` stays out of scope. R-1 names only the face and the outline.
- **The picker preview is fixed by the same change, with no OptionsCompose edit.** C2 calls
  `S.Resolve("hud.font", nil, true)`, which now answers nil while Ignore fonts is on, so C5's `read`
  shows the stored face. C7 already re-renders the open pages on `SetIgnore`, so the switch is live.
  The picker stays **disabled** (C3's `disabledIf` is the companion), and it shows the face that is actually
  drawn. Lifting the disable while fonts are ignored is a possible extra (a predicate `disabledIf`, which
  `OptionsWidgets.lua:459-463` supports). R-1 does not ask for it, so record it in DECISIONS.md and leave the
  companion's semantics alone.
- **BarStyle (G1, SkinPaintExtras.lua, bump minor 5 → 6, or fold into LK-05's bump).** For consistency, under
  `lib:__FontsIgnored(owner)` return `font = nil, fontKey = nil, outline = nil`, so the host's own setting
  stands. Use the same rule as `Token`, ideally by reading the two through `lib:Token(owner, ...)` instead of
  `T[...]`. There are no consumers, so the risk is nil. The two pinning tests (`test_skin_override.lua:69-71`,
  `test_skin_paint.lua:570-578`) run with Ignore fonts off, so they are unchanged.
- **Strings (optional, OptionsAppearance minor bump):** `IGNORE_FONTS_TIP` (`OptionsAppearance.lua:101-102`,
  "Keep every font in this addon as the game draws it...") and `FONT_TIP` (`:91-92`) could say that
  HUD text keeps the face and outline its own settings name. The tests read these via `S.IGNORE_FONTS` (no literal
  comparison found), so the change is low risk.
- **E7 gap (owner tokens following hud.font):** no consumer has one, so leave it unchanged and document it.

**Docs:** add new `docs/api/Skin/version-8.<SkinDefs>.<SkinPaint>.<Extras>.<Controls>.<EUI>.<Ace>-docs.md`
and a `members-*.json` (generated by `tools/gen-api-members.lua`, compared by `tests/test_versioning.lua`).
Rewrite the `Token` row (`docs/api/Skin/version-7.15.11.5.9.2.4-docs.md:81`), the `Resolve` row (`:83`), the
`SetIgnore` row (`:71`), the `SetOverride` row's "Ignore fonts wins" sentence (`:74`), and the FROM_SKIN
section (`:158-173`). Coordinate the version key with LK-02/03/04/07/09/10, which bump the same files: **one
minor per file for the whole release.**

### 1.6 LK-01 tests

Nothing in the suite pins "Ignore fonts does not reach the HUD", so **no existing test has to change**.
These tests sit next to the change and must stay green:

- `tests/test_skin.lua:618-630`: the Resolve contract with Ignore fonts off. It stays as it is.
- `tests/test_skin_override.lua:50-72`: the override reaches `hud.font` through Token and BarStyle, with Ignore fonts off.
- `tests/test_skin_override.lua:121-133`: Ignore fonts wins over a font override for `P.font`.
- `tests/test_options_compose_skin.lua:137-149`: `skinValue` shows `Skin:Token(OWNER,"hud.font")` while the companion is set (Ignore fonts off).
- `tests/test_options_appearance.lua:512-536`: Ignore fonts hands fonts back live.

New tests to add, each failing on today's code:

1. With `SetIgnore(owner, nil, true)`, `S.Resolve("hud.font", "Ka0s Inter", true)` answers `"Ka0s Inter"`, and
   the same holds for `"hud.outline"`, `"THICKOUTLINE"`, `true`.
2. With Ignore fonts on, `S.Resolve("hud.font", "@skin")` and `S.Resolve("hud.font", nil, true)` answer nil.
3. With Ignore fonts on, `S.Token("hud.font")` and `S.Token("hud.outline")` answer nil. Other tokens are unchanged:
   `font.body` (which P.font handles), `hud.fontSize`, and `bar.texture` through `Resolve(..., true)`.
4. With Ignore fonts on and a font override set, `Resolve("hud.font", stored, true)` is the stored value, not the override.
5. Off again, both answer the skin's value (live, with no re-register).
6. Composer: with a FontGroup `fromSkin`, the companion on and Ignore fonts on, `picker.skinValue(picker)` is nil and the
   rendered picker shows the stored face. After `SetIgnore(..., false)` it shows the skin's face (extend
   `test_options_compose_skin.lua:137`).
7. BarStyle under Ignore fonts: `font`, `fontKey` and `outline` are nil, and `texture` is unchanged.
8. An unregistered owner is unchanged (`__FontsIgnored` is false).

---

## 2. LK-05: S.Text and WidgetsReorder against the Scope

### 2.1 How the AceGUI path decides its scope (the model to reuse)

- `Skin:PaintAce(owner, widget)` at `SkinAce.lua:798-817`. It refuses an unregistered owner (`:801`). If
  `not self:__PanelSkinned(owner)`, it **gives back** a widget this owner painted (`restore(widget, held)`)
  and returns false (`:802-806`).
- The scope needs no argument because **every AceGUI widget is, by definition, a settings-panel
  widget**. The choke point is the Options instance's AceGUI proxy (`SkinAce.lua:879-917`,
  `__AttachSkinAce`), and `PaintAceTree` (`:847-853`) repeats the check per widget.
- Liveness comes from re-rendering, not from repainting in place (`SkinAce.lua:23-25`).
  `SetIgnore` → `notify` → the Options listener re-renders the open pages (`OptionsScroll.lua:25-28,
  434-457`). Release restores each row (`SkinAce.lua:18-22`), and re-acquire runs PaintAce, which now
  refuses.
- The Options chrome does the same through `lib.__chromeSkin(owner)` (`OptionsScroll.lua:259-265`), which
  returns a nil facade while the panel is ignored. `lib.__chromeUnpaint` (`:295-300`) hands back an
  already-painted target with `P.unpaint`.
- Fonts in both paths go through `P.font`, so **Ignore fonts is honoured automatically**.

### 2.2 S.Text: how it paints and why it ignores the Scope

- `prim.Text(owner, fs, role)` at `SkinPaintExtras.lua:316-327`: `P.track(owner, fs, "Text", role)` →
  `P.tint(rec, fs, T, token)` → `P.font(owner, rec, fs, TEXT_FONT[role] or "body")`.
- **Ignore fonts: S.Text already obeys it**, through `P.font` → `SkinPaint.lua:539` → `P.unfont`. The
  report line "S.Text ... ignore[s] the Ignore settings panel" is about the **panel** half only. Its
  color (`P.tint`, `SkinPaint.lua:396-413`) is always applied.
- **Ignore settings panel: S.Text never asks.** It has no scope signal. `S.Text` is a generic primitive,
  used heavily on **windows** (for example BankLedger `modules/Browser.lua:236,289,1108,1173,1178`,
  `InsightsWidgets.lua:460-928`, and DropWatcher in about 20 places: `modules/DropsStrip.lua:139`,
  `Window.lua:622`, `WindowTitleBar.lua:179-294`, ...), as well as on settings pages
  (`KickCD/settings/Spells.lua:542`, and ConsumableMaster's guarded `KCM.SkinPanelText`). The library
  cannot tell a panel string from a window string, so the scope must be **declared by the caller**.
  Gating S.Text unconditionally would wrongly unskin every window string, because Ignore settings panel
  defaults on in the hosts (R-2's owner answer).
- Replay: `Skin:Track` stores every vararg (`Skin.lua:928-946`, `rec.calls[prim] = { n = ..., ... }`), and
  `Repaint` replays them (`:966-977`, `:986-1000`), which `SetIgnore` calls (`:620`). A third argument to
  Text is therefore replayed for free, and a panel-scoped Text toggles live on SetIgnore **without** a
  page re-render.
- `Text` is a Ka0s extra and is **not** in EllesmereUI's native list (`SkinEUI.lua:83-86`, route `:284-287`),
  so it always runs `prim.Text`, even under `eui`. (`Font` and `White` are native and route to EllesmereUI.)

**What the addons compose today (to delete in XX-01):**
`ConsumableMaster/core/SkinSetup.lua:183-225`. Its comment is the gap statement, and it adds
`KCM.SkinPanelColor`, `KCM.SkinPanelEscape`, `KCM.SkinPanelOwner` and `KCM.SkinPanelText`. The last
**Untracks** the string and resets it to a template font object and a "stock" color: a hand-rolled
`P.unpaint`. Related escape helpers are `PanelMaster/core/SkinSetup.lua:131-141`
(`NS.SkinPanelEscape`) and `PrettyChat/core/SkinSetup.lua:130-139` (`NS.PanelEscape`). Those are color escapes
for markup, not S.Text, and they belong to LK-06 or the addon inventory: no S.Text change removes them.

### 2.3 WidgetsReorder: how it paints and why it ignores the Scope

- `skinPalette(owner)` at `WidgetsReorder.lua:56-69` calls `lib.__skinOf(owner)` (`Widgets.lua:118-124`,
  which checks only `Skin:IsOwner`) and then `Skin:Token(owner, ...)` for `list.box*`, `handle.rest`,
  `text.accent`, `list.dropLine` and `list.ghostBg`. **It never asks `__PanelSkinned`**, so a registered owner
  always gets the skin's palette.
- The palette is resolved once per controller (`WidgetsReorder.lua:537-551`) and used by `paintRowBox`
  (`:350-359`), the handle tints (`:617-634`, `:705-717`), the line (`:293`, color `:546`) and the ghost
  (`skinGhost` `:443-448`, `raiseGhost` `:456-475`). A controller lives for one render, so the next render
  after `SetIgnore` (C7) would pick up a scope-aware palette. No in-place repaint is needed.
- **Ignore fonts: moot.** ReorderList draws one string, the ghost's text, created with `GameFontNormal`
  (`WidgetsReorder.lua:159`) and **never given a skin face**. Only its color comes from the palette
  (`:470-471`). Nothing to gate. (R-5/LK-06's "skin every custom widget" may later add a face. If it does,
  it must go through the owner's `P.font`/`S.Text` so Ignore fonts applies.)
- **Every consumer is a settings page:** `ConsumableMaster/settings/Category.lua:747,974`,
  `settings/MacroBar.lua:1052`, `settings/StatPriority.lua:613`; `MultiMeters/settings/ColumnBlocks.lua:239`;
  `LootHistory/settings/Panel.lua:772` (through `core/WidgetsSetup.lua:198-206`). CM already passes
  `owner = KCM.SkinPanelOwner()` (`Category.lua:747-753`, helper `core/SkinSetup.lua:208-211`), which is nil
  while the panel is ignored.

### 2.4 The proposed minimal change (LK-05)

**A. S.Text: an opt-in panel scope (SkinPaintExtras minor bump, plus one helper in SkinPaint).**

- Signature: `S.Text(fs, role[, opts])` with `opts.panel = true`, meaning "this string is on the owner's
  settings panel". With no `opts`, Text paints exactly as it does today, so every window caller is untouched.
- A shared helper beside `P.keepStock` (`SkinPaint.lua:789-799`), so LK-06 can reuse it for every other
  primitive and widget:

  ```lua
  --- True when `opts.panel` puts the target on its owner's settings panel and that owner ignores its
  --- panel (Skin minor 5): everything the target wears from the library is given back (P.unpaint) and the
  --- caller paints nothing. The call stays recorded, so turning the exception off repaints it.
  function P.panelIgnored(owner, rec, frame, opts)
    if not (rec and type(opts) == "table" and opts.panel == true) then return false end
    local panel = type(lib.GetIgnore) == "function" and lib:GetIgnore(owner)   -- false for an unregistered owner
    if panel ~= true then return false end
    P.unpaint(rec, frame)
    return true
  end
  ```

  Use `GetIgnore`'s panel half, **not** `not __PanelSkinned`: the latter is true for an *unregistered*
  owner (`Skin.lua:628-631`), and an owner-less facade must keep reading Ka0s Default.
- `prim.Text` becomes `local rec = P.track(owner, fs, "Text", role, opts)`, then
  `if P.panelIgnored(owner, rec, fs, opts) then return end`, before the tint and the font. `P.unpaint`
  (`SkinPaint.lua:761-777`) gives back the prior color (`restoreColors "SetTextColor"`, which `P.tint`
  records since minor 8, `:402-407`) and the prior font (`P.unfont`). That is what CM's `SkinPanelText`
  hand-rolls, and it is better, because CM guesses the template face. Since `SetIgnore` → `Repaint` replays the recorded
  `opts`, the switch is live both ways.
- **LK-02 interaction:** keep `P.panelIgnored` independent of `P.keepStock`/`stockKept`, which LK-02 retires. Note
  that `P.unpaint` clears `rec.regions.stockKept` (`:776`), and that is harmless.
- Facade and VOCAB are unchanged: `Text` is already a trampoline (`Skin.lua:113`, `:1004-1009`), and an extra
  argument passes through.
- Optional, for LK-06: `Font`/`White` could take the same opts, but they are EllesmereUI-native
  (`SkinEUI.lua:83-86`), so the opts would also have to be stripped or handled on the EUI route
  (`stripAll`, `SkinEUI.lua:276`). Leave them to LK-06.

**B. ReorderList: panel-scoped by default (WidgetsReorder minor 2 → 3).**

- In `skinPalette(owner)` (`WidgetsReorder.lua:56-69`), after `Skin` is found, add:
  `if type(Skin.GetIgnore) == "function" and (Skin:GetIgnore(owner)) == true then return nil end`. With a nil palette,
  every reader falls back to minor 1's colors (the stock look), exactly as for an owner-less list. `skinGhost`
  already resets a ghost a skinned list painted (`:443-448`).
- Make it the **default** rather than opt-in, because every consumer is a settings page (§2.3), in line with
  PaintAce, which treats every AceGUI widget as panel. Offer `opts.scope = "window"` (or `panel = false`) as
  the escape for a future window host; none exists today. Document it in the Widgets API doc's *Skin owners*
  table (`docs/api/Widgets/version-16.2.6.4.4.1-docs.md:56-70`) and in the ReorderList `owner` option comment
  (`WidgetsReorder.lua:533-535`).
- Liveness: an Options re-render (C7) builds a new controller, so no listener is needed.
  `CM.SkinPanelOwner` then becomes redundant (XX-01), and MultiMeters and LootHistory start obeying the
  Scope with no change of their own. **This is a visible change for MM and LH:** under the default
  "Ignore settings panel" on, their Columns and reorder lists go back to minor-1 colors. That is the R-5
  intent. Flag it for their XX-02 smoke checks.

**C. Docs and versions.** New Skin API version doc rows for `Text(fs, role[, opts])` (current row
`docs/api/Skin/version-7.15.11.5.9.2.4-docs.md:891`) and for `SetIgnore` (`:71`, which lists the panel paths:
add S.Text with `opts.panel` and ReorderList). Add a new Widgets version doc plus `members-*.json`. Bump
`WidgetsReorder` 2→3 and `SkinPaintExtras`/`SkinPaint` (shared with the other LK items' bumps; one per file).

### 2.5 LK-05 tests

Existing tests that pin the current behaviour. **None asserts that the Scope is ignored**, so all stay green
under the proposal. They must still pass:

- `tests/test_skin_paint.lua:524-540`: `S.Text(fs, "heading")` colors and fonts (no opts).
- `tests/test_skin_owner_tokens.lua:231-242`: `S.Text` with token names (no opts).
- `tests/test_skin_eui.lua:176`, `:425`: `S.Text(fs, "accent")` under eui (no opts).
- `tests/test_widgets_skin.lua:354-359`: an owner-less ReorderList is minor 1's.
- `tests/test_widgets_skin.lua:361-376`: an owned ReorderList is drawn from the skin. **This relies on the
  library default `ignorePanel = false`** (`F.owner` registers without SetIgnore). It stays green, but it is
  the test closest to the change: if the panel default were ever flipped in the library, it would break.
- `tests/test_widgets_skin.lua` next test ("Ka0s Default draws the reorder list exactly as minor 1 did").
- `tests/test_skin_ace.lua:75-91`: the PaintAce panel scope, the model for the new tests.
- `tests/test_options_skin.lua:211-253` and `tests/test_options_appearance.lua:538-552,589-597`: chrome hand-back.
- `tests/test_widgets_reorder.lua`, `tests/test_widgets_reorderlist.lua`: owner-less gesture tests, untouched.

New tests, each failing on today's code:

1. `S.Text(fs, "heading", { panel = true })` with `SetIgnore(owner, true, nil)` leaves the prior color and font, and
   records the call. `SetIgnore(owner, false, nil)` paints it live (replay). On again, it is given back live.
2. `S.Text(fs, "heading")` (no opts) is unchanged by Ignore settings panel, so window strings keep the skin.
3. An unregistered owner with `{ panel = true }` still paints Ka0s Default (the `GetIgnore` rule, not `__PanelSkinned`).
4. Panel-scoped Text with Ignore fonts on and panel off keeps the skin's color and the string's own face.
5. ReorderList with a registered owner and `SetIgnore(owner, true)` draws minor-1 boxes, handle, line and ghost, and a
   ghost a skinned list painted earlier is put back.
6. ReorderList with `opts.scope = "window"` (if adopted) keeps the skin while the panel is ignored.

---

## 3. Summary for the implementer

| Item | Files (minor) | Change | Existing tests to change |
|---|---|---|---|
| LK-01 | `Skin.lua` (7→8); `SkinPaintExtras.lua` (BarStyle); optionally `OptionsAppearance.lua` strings | Gate `Token` and `Resolve` for `hud.font`/`hud.outline` on `__FontsIgnored` (stored value wins, sentinel → nil); BarStyle's font fields are nil under Ignore fonts; the picker preview follows with no composer edit | none |
| LK-05 | `SkinPaint.lua` (`P.panelIgnored`), `SkinPaintExtras.lua` (`Text` opts), `WidgetsReorder.lua` (2→3) | `S.Text(fs, role, { panel = true })` gives back while the owner's panel is ignored (replayed, live); ReorderList's palette is nil while the owner's panel is ignored (default), with an opt-out | none |

Addon workarounds that this makes redundant (owned by XX-01): AT `core/Data.lua:148`; AM `modules/Style.lua:60`;
CM `modules/MacroBarButton.lua:147-149` (only after CM reads through Resolve or Token-nil handles restore) and
`core/SkinSetup.lua:183-225` (`SkinPanelText`, `SkinPanelOwner`); PFE `core/SkinSetup.lua:370-376` plus its use in
`modules/Element.lua`; the matching helpers in KC, QC, PM and PC as their inventories confirm.
