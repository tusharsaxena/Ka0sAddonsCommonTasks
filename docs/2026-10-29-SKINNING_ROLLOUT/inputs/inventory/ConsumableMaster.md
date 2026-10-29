# Inventory: ConsumableMaster (prefix CM)

Read-only inventory for M0 of `00_PLAN.md`. Repo `../ConsumableMaster`, branch `master`, clean, vendors
LibKa0s v1.77.0 (`CLAUDE.md`: "Bundles LibKa0s v1.77.0", "LibKa0s icons: clear, close, copy, help, info,
segment"). The reference library is LibKa0s v1.79.0 (`../LibKa0s` at 4e1ae41). Every file:line below is
in `../ConsumableMaster` unless a path says otherwise.

**In short.** CM draws one HUD, the **macro bar**: a container, up to 15 secure macro buttons, and a
secure hover **flyout** per button with a shaded indicator band. It also has a big settings surface: five
page files, four custom AceGUI widget types, and two raw-frame reorder lists. Its tool windows (debug
console, perf panel) and its Options pages already pass the folder name as `addonName`, so they follow
the owner as soon as it registers. The real work is in three places:
1. the HUD's backdrops, borders and label font, through `S.Resolve` and the R3 reset;
2. the settings widgets CM acquires itself, from AceGUI directly rather than through the proxy;
3. a handful of exact-value colors that no token holds.

There is no test mode and no Sim, Glow, chart, title bar or standalone window of CM's own.

---

## 1. Surfaces

The tokens named below are all from `LibKa0s/SkinDefs.lua`'s schema (minor 14). "KD" means the token's
Ka0s Default value. "exact" means KD equals the value CM types today.

### 1a. HUD: the macro bar (`modules/MacroBar.lua`, `modules/MacroBarButton.lua`, `modules/MacroBarFlyout.lua`)

| # | Surface | Built at | Typed today | Paints it (rung 1) |
|---|---|---|---|---|
| H1 | Bar container `KCMMacroBar` (BackdropTemplate, strata MEDIUM, `RegisterStateDriver(bar,"visibility")` at :462) | `modules/MacroBar.lua:222` | Backdrop `bgFile = WHITE8X8` (:49, :378). Edge = LSM border `macroBar.barBorderStyle`, size `barBorderSize` (:370-380). `SetBackdropColor(color(c.barBackdropColor, …, 0,0,0,0.5))` (:393). `SetBackdropBorderColor(color(c.barBorderColor, …, 0.25,0.25,0.25,1))` (:397) | Stays a host backdrop fed from the skin. Fill `S.Resolve("bar.bg", stored, barBackdropColorFromSkin)` (KD `{0,0,0,0.5}`, **exact**). Edge style `S.Resolve("bar.borderStyle", …)` (KD `"None"`). Size `bar.borderSize` (KD 1). Edge color `bar.border` (KD `{0,0,0,1}`). The literal fallbacks (:394, :398) become token reads. A primitive (`S.Panel`) would not fit: the bar's look is player settings first, skin second. |
| H2 | Unlock wash `KCMMacroBarWash` (child frame, LEVEL.WASH) | `modules/MacroBar.lua:243-251` | `wash.tex:SetColorTexture(1, 0.82, 0, 0.15)` (:249) | `menu.hover` is KD `{1,0.82,0,0.15}`, the **exact** value under a different role. See **D4**. |
| H3 | Drag handle strip (library `Widgets.DragHandle`, with close and help marks and three tooltips) | `modules/MacroBar.lua:275-338` | Nothing typed. The library draws it. | `spec.owner = addonName`. The strip takes `handle.bg`, `handle.edge`, `text.accent`, `icon.tint` and `icon.hot` (WidgetsDragHandle minor 6). |
| H4 | Slot button `KCMMacroBarButton<i>` (`SecureActionButtonTemplate`) | `modules/MacroBarButton.lua:391` | — | — |
| H4a | its backdrop fill (BACKGROUND texture) | `MacroBarButton.lua:403` | `SetColorTexture(swatch(cfg.buttonBackdropColor, …, {0,0,0,0.6}))` (:349, :299) | `S.Resolve(<token>, stored, buttonBackdropColorFromSkin)`. No HUD token holds `{0,0,0,0.6}` (`bar.bg` is 0.5), so the token choice is **D2**. |
| H4b | its border (BackdropTemplate child, LEVEL.BORDER, pushed out by `buttonBorderOffset`) | `MacroBarButton.lua:426`, painted `:320-335` | Edge = LSM `buttonBorderStyle` / `buttonBorderSize`. `SetBackdropBorderColor(swatch(cfg.buttonBorderColor, …, {1,1,1,1}))` (:332, :298) | Host backdrop again. Style `S.Resolve("bar.borderStyle", …)`, color `S.Resolve("icon.border", …)` (KD `{0,0,0,1}`). `S.IconBorder` does **not** fit: it draws only a flat N px edge with no LSM art and no offset (`SkinPaintControls.lua:575`). |
| H4c | its icon (macro icon) | `MacroBarButton.lua:406`, `:94` | game icon | Exception (rung 4). |
| H4d | Pushed / highlight art | `MacroBarButton.lua:409-412` | `UI-Quickslot-Depress`, `ButtonHilight-Square` (:38-39), ADD blend | Exception (rung 3: Blizzard action-button art), **D9**. |
| H4e | Cooldown swipe (`CooldownFrameTemplate`) | `MacroBarButton.lua:422` | Blizzard | Exception (rung 3). |
| H4f | Count text | `MacroBarButton.lua:434` | `NumberFontNormal` font object, color untouched | HUD text: face `S.BarStyle().font` (`hud.font`), outline `hud.outline`, keeping the font object's size. See **D6**. |
| H4g | Label text | `MacroBarButton.lua:438`, painted `:248-285` | `SetFont(LSM font labelFont, pts, labelFlags)` (:263). Shadow `SetShadowColor(0,0,0,1)` / offset (1,-1) (:271-276). `SetTextColor(SwatchColor(cfg.labelColor, …, 1,0.82,0,1))` (:281) | Face `S.Resolve("hud.font", labelFont, labelFontFromSkin)` (KD `"Ka0s Oxanium SemiBold"`). Color `S.Resolve("text.accent", labelColor, labelColorFromSkin)` (KD GOLD, **exact**). Flags stay the player's `labelFlags` (KD `hud.outline` = "OUTLINE", the same as CM's default). The size stays percent-of-button (geometry). The shadow color `(0,0,0,1)` has no token; it is a legibility constant, left as is (**D7**). |
| H5 | Flyout container `KCMMacroBarFlyout<i>` (`SecureHandlerEnterLeaveTemplate`, strata DIALOG) | `modules/MacroBarFlyout.lua:256` | — | — |
| H5a | flyout panel (BackdropTemplate child, LEVEL.PANEL) | `MacroBarFlyout.lua:278`, painted `:462-481` | `bgFile WHITE8X8` (:48). Edge = LSM `barBorderStyle` / `barBorderSize`. `SetBackdropColor(swatch(flyoutBackdropColor, …, {0,0,0,0.85}))` (:477, :443). `SetBackdropBorderColor(swatch(barBorderColor, …, {0.25,0.25,0.25,1}))` (:479, :444) | Fill: no HUD token holds 0.85 (`popup.bg` is `{0,0,0,0.92}`), see **D2**. Edge: the same tokens as H1's (`bar.borderStyle`, `bar.border`), because it shares the bar's settings. |
| H5b | flyout entry buttons (secure, pooled, max 16) | `MacroBarFlyout.lua:198-246` | Backdrop fill, border and icon zoom through the shared `BB.ApplyBorder` / `BB.ApplyBackdropTex` (the same values as H4a/H4b). Highlight `ButtonHilight-Square` (:49). Count `NumberFontNormal` (:227) | The same as H4a, H4b and H4f. |
| H5c | indicator band (`SecureHandlerEnterLeaveTemplate`) shade | `MacroBarFlyout.lua:286`, `:321`, painted `:517` | `SetColorTexture(swatch(flyoutShadeColor, …, {0,0,0,0.55}))`. The profile default is `{0,0,0,0.8}` | No exact token (`cover.dim` is `{0,0,0,0.6}`), see **D2**. |
| H5d | indicator arrow | `MacroBarFlyout.lua:324-325` | `ChatFrameExpandArrow` art, untinted | Blizzard art. `icon.arrow` (KD GOLD) would multiply it. See **D9**. |
| H6 | GameTooltip lines on slot and entry hover | `core/MacroDisplay.lua:197`, `:202` | `GameTooltip:SetText(name, 1, 0.82, 0)`, `AddLine(body, 1, 1, 1, true)` | `gtip.title` (KD GOLD, **exact**) and `gtip.value` (KD WHITE, **exact**). The frame is an exception (§7); only the lines take the skin. Item and spell tooltips (`SetItemByID` / `SetSpellByID`) are the client's. |

### 1b. Settings pages (Blizzard Settings canvases drawn by `LibKa0s-Options-1.0`)

The page chrome, the tab strips, the schema rows, the composer blocks, the banner, the landing and About
page, `H.Section`, `H.CustomCheckbox` (`SessionCheckbox`), the IdInput and IdList, and the combat cover
are all the library's. They follow the owner because `settings/OptionsSetup.lua:224` passes
`addonName = addonName`. Once the owner is registered, `Skin.__AttachSkinAce` wraps the instance's
`O.AceGUI`, so rows the library makes are painted. CM's own acquisitions call **`AceGUI:Create` on the
raw library** (`LibStub("AceGUI-3.0")`), so they bypass the proxy:

| # | Surface | Built at | Typed today | Paints it |
|---|---|---|---|---|
| S1 | Maintenance buttons (`H.Button` / `H.ButtonPair`): AceGUI `Button` + `SimpleGroup` | `settings/Panel.lua:640`, `:661`, `:672` | — | `Skin:PaintAce(owner, btn)`, or create through `H.AceGUI` (the proxy). `SimpleGroup` has no painter and stays transparent. |
| S2 | `H.Label` (AceGUI `Label`, `SetFontObject(GameFontHighlight)` for "medium") | `settings/Panel.lua:707-712` | font object | PaintAce. SkinAce's `hookLabelFont` re-records after SetFontObject. |
| S3 | Category page: `CheckBox` | `settings/Category.lua:405` | — | PaintAce. |
| S4 | Category / AddByID / StatPriority dropdowns | `settings/CategoryAddByID.lua:73`, `settings/StatPriority.lua:363` | — | PaintAce (`PAINT.Dropdown`). |
| S5 | Macro Bar page boundary rule (`Heading`) | `settings/MacroBar.lua:1022` | — | PaintAce (`PAINT.Heading`). |
| S6 | `SimpleGroup` rows | `settings/Category.lua:348`, `:595`; `settings/StatPriority.lua:381`, `:570`; `settings/MacroBar.lua:994` | — | Nothing (no painter, transparent). |
| S7 | **KCMIconButton** (custom AceGUI type, priority-row up/down/delete) | `modules/KCMIconButton.lua:100-140`, acquired `settings/Category.lua:357` | Hover swatch `SetColorTexture(1, 0.82, 0, 0.25)` (:120). Label disabled `SetTextColor(0.5,0.5,0.5)` (:90), enabled `(1,1,1)` (:94). Image disabled `SetVertexColor(0.5,0.5,0.5,0.5)` (:91), enabled `(1,1,1,1)` (:95). Label `GameFontHighlight` (:108) | Label `S.Color("text.disabled")` (KD `{0.5,0.5,0.5,1}`, **exact**) and `S.Color("text.highlight")` (KD WHITE, **exact**), face through `S.Text`. Hover swatch is **gap CM-G1**. Image dim is **gap CM-G4**. No library painter exists for a custom type, so the widget paints itself in `OnAcquire` / `SetDisabled` from `KCM.Skin` tokens. Only CM acquires this type, so its pool carries no cross-addon leak. |
| S8 | **KCMScoreButton** (info glyph) | `modules/KCMScoreButton.lua:85-92`, `settings/Category.lua:377` | Image dim `SetVertexColor(0.5,0.5,0.5,0.5)` / `(1,1,1,1)` (:76, :79) | **CM-G4**. Its tooltip text is S9. |
| S9 | Score tooltip body (through `H.AttachTooltip`, so GameTooltip lines) | `settings/Category.lua:137-150` | Escapes: `|cff888888` note (0.533), `|cffffffff` value, `|cffaaaaaa` summary (0.667) | `|cffffffff` becomes `gtip.value` (**exact**). The two grays are **gap CM-G3**. Token colors must be rendered to hex at format time (no literal escape). |
| S10 | **KCMItemRow** (candidate row) | `modules/KCMItemRow.lua:310-395`, `settings/Category.lua:389` | `label` `GameFontHighlight` (:344), `handTag` `GameFontNormalSmall` (:340). Alpha 0.4 when not applicable (:47, :254). Owned and not-owned ReadyCheck glyphs (:35-36), Favorites star (:37), crafting-quality atlas (:216), item and spell icon | `S.Text(label, "body")`... the closest exact role is `text.highlight` (WHITE, the GameFontHighlight color). `S.Text(handTag, "accent")` (GameFontNormal gold = `text.accent`, **exact**). The 0.4 alpha is a state, not chrome (**D8**). The glyphs, atlas and icons are exceptions (rung 4). |
| S11 | **KCMMacroDragIcon** | `modules/KCMMacroDragIcon.lua:91-115`, `settings/Category.lua:397` | `|cff999999` "Macro not created yet" (:82), `|cffffd100` "Drag to action bar" (:85). Highlight `ButtonHilight-Square` (:104) | `|cffffd100` becomes `text.accent` (**exact**). `|cff999999` (0.6) matches `sem.unknown` exactly, see **D5**. The highlight is Blizzard art (exception). |
| S12 | StatPriority stat rows (raw frames, privately pooled) | `settings/StatPriority.lua:450-505` | Label `GameFontNormal` (:482). `SetTextColor(1,0.82,0)` included / `(0.5,0.5,0.5)` excluded (:501, :503). Ghost `ghostTextColor = {1,0.82,0}` / `{0.5,0.5,0.5}` (:591). ReadyCheck glyphs (:108-109). Tooltip `AddLine(..., 1,1,1)` (:471-474) | `S.Text(label, "accent")` / `S.Text(label, "disabled")`: `text.accent` and `text.disabled`, both **exact**. Ghost colors from the same two tokens. Tooltip lines `gtip.value` (**exact**). Glyphs are rung 4 (ready/not-ready meaning). |
| S13 | Macro Bar page slot rows (raw frames, privately pooled) | `settings/MacroBar.lua:908-957` | The same as S12: `SetTextColor(1,0.82,0)` / `(0.5,0.5,0.5)` (:952, :954), ghost (:1012), tooltip `AddLine(..., 1,1,1)` (:898-901) | The same as S12. |
| S14 | Reorder lists ×4 (library `W.ReorderList`) | `settings/Category.lua:735`, `:957`; `settings/MacroBar.lua:1040`; `settings/StatPriority.lua:614` | — | Pass `owner = addonName` (WidgetsReorder minor 2: `list.box*`, `list.dropLine`, `list.ghostBg`, `handle.*`). |
| S15 | Warning labels inside `L[...]` keys (`H.Label`) | `settings/Category.lua:709`, `:712`, `:952`, `:1090`; `settings/StatPriority.lua:738` | `|cffff8800` (1, 0.533, 0) inside the locale key | **Gap CM-G2**. The color escape has to move out of the locale key, which renames five keys in `locales/enUS.lua`. |
| S16 | Profiles page (AceConfigDialog draws AceDBOptions into a `SimpleGroup`) | `settings/Profiles.lua:93`, `:145` | — | AceConfigDialog acquires its own widgets. `Skin:PaintAceTree(owner, container)` after each `dialog:Open` would reach them, see **D10**. |
| S17 | LSM30_Border / LSM30_Font pull-outs (Macro Bar page) | composer rows | — | Exception (§7). |
| S18 | Schema-error chat line | `settings/Panel.lua:318` | `|cffff0000` | Chat, exception **E-chat**. |

### 1c. Tool surfaces

| # | Surface | Where | Status |
|---|---|---|---|
| T1 | Debug console and its copy window | `core/DebugLogSetup.lua:165-275` (`addonName = addonName`, no `skin` and no `applySkin`) | Follows the owner with no code change (DebugLog 22.x resolves `core.__SkinFacade(addonName)` at call time). Log line colors become `log.ts`, `log.tag`, `log.text` and `log.count`. The close, copy and clear marks are already declared. |
| T2 | Perf panel | `core/PerfSetup.lua:79-130` (`addonName = addonName`) | Follows the owner (PerfPanel minor ≥10, `sem.step*`). |
| T3 | Sim panel | — | Not consumed. Nothing to do. |
| T4 | Test strip | — | None. CM has no test mode (the unlocked bar is the preview, options-ui-§15 exemption). |
| T5 | Copy windows other than the console's | — | None. |
| T6 | Launcher (LibDBIcon minimap button, broker, MenuUtil context menu) | `core/LauncherSetup.lua` | Exception (rung 3: LibDBIcon / Blizzard menu). No owner parameter in Launcher-1.0. |
| T7 | Static popups `KCM_CONFIRM_RESET`, `KCM_RESET_PRIORITIES`, `KCM_RESET_CATEGORY` | `settings/General.lua:146`, `:237`, `:419`; `settings/Category.lua:301` | Exception (§7). |
| T8 | First-run skin picker (new) | — | `O.SkinPicker` with `owner = addonName`, see §7 below and **D3**. |
| T9 | Appearance tab (new) | `settings/General.lua:426-430` `TAB_OPTS.tabs` | `O.AppearanceTab(spec)` appended **last**, after Maintenance. The General page has no Keybindings tab, so the strip reads Master controls, Maintenance, Appearance (3 of 8). |

### 1d. Chat output (not a surface the skin reaches)

`KCM.PREFIX = "|cff00ffff[CM]|r"` (`core/Constants.lua:18`); `core/SlashCommands.lua:345-346`, `:690`,
`:919`, `:938`, `:941`; `core/SlashDump.lua:113`, `:211`, `:251`, `:334-335`, `:412`, `:441`;
`settings/Slash.lua:425-444`; `core/DebugLogSetup.lua:83`. All of them are chat-frame text, see **E-chat**
and **D11**.

---

## 2. Library factories that take an owner

| Factory | Call site | Today | Owed |
|---|---|---|---|
| `Widgets.DragHandle(frame, spec)` | `modules/MacroBar.lua:275` | no `owner` | `owner = addonName` |
| `W.ReorderList(opts)` | `settings/Category.lua:735`, `:957`; `settings/MacroBar.lua:1040`; `settings/StatPriority.lua:614` | no `owner` | `owner = addonName` (and `list:AddRow` `ghostTextColor` from tokens, `StatPriority.lua:591`, `MacroBar.lua:1012`) |
| `LibKa0s-Options-1.0 :New` | `settings/OptionsSetup.lua:200` (`addonName = addonName`, :224) | ✓ already the folder | Nothing. The pages and the AceGUI proxy follow once registered. |
| `LibKa0s-DebugLog-1.0 :New` | `core/DebugLogSetup.lua:165` (`addonName`, :179) | ✓ | Nothing |
| `LibKa0s-Perf-1.0 :New` | `core/PerfSetup.lua:79` (`addonName`, :98) | ✓ | Nothing |
| `lib.MakeCloseButton(parent, onClick, addonName)` | `core/CoreSetup.lua:207-209` (`KCM.MakeCloseButton`, no host caller today) | ✓ passes the folder | Nothing |
| `Core.ApplySkin` | not called | — | — |
| `O.AppearanceTab` / `O.AppearanceRows`, `O.SkinPicker` | new | — | `spec.get` / `spec.set` = the write seam, `owner = addonName` |
| `H.MasterControls{ addonName = "Consumable Master" }` | `settings/General.lua:185` | a **display label**, not a skin owner | Leave it. Do not confuse it with the owner. |

---

## 3. HUD style settings (O2's one-time R3 reset)

The schema lives in `defaults/Profile.lua:126-247` (`macroBar.*`), and the rows in `settings/MacroBar.lua`
(`H.ColorPair` :265, :322, :589, :620; `H.BorderGroup` :283, :340; `H.FontGroup` :452). The migration runner
is `core/Database.lua:144-162` (`D.CURRENT_SCHEMA = 3`, :34). Its profile steps are gated on
`p.schemaVersion` and also run from `OnProfileChanged/Copied/Reset` (`core/ConsumableMaster.lua:618-620`).
The reset is a **v4 step** calling `Skin.ResetToSkin(p, keys)`.

`ResetToSkin` (`LibKa0s/Skin.lua:650`) does three things:
- **Color (table) keys:** sets `<key>FromSkin = true`.
- **Keys with a companion:** sets the companion to true.
- **Bool keys:** sets the key itself to true.
- **Any other key:** writes the `"@skin"` sentinel.

So the keys list must **not** carry number, enum or bool style keys. A sentinel would break their schema
validation, and a bool would be switched on.

| Key | Default | Token (KD) | How it follows the skin | In the R3 key list? |
|---|---|---|---|---|
| `macroBar.barBackdropColor` | `{0,0,0,0.5}` | `bar.bg` `{0,0,0,0.5}` (exact) | `S.Resolve("bar.bg", v, p.barBackdropColorFromSkin)`; companion via ResetToSkin | yes (needs a UI to turn it off: **CM-G5**) |
| `macroBar.barBorderStyle` | `"Blizzard Tooltip"` | `bar.borderStyle` `"None"` | `H.BorderGroup{ fromSkin = true }` emits `barBorderStyleFromSkin`. Draw with `S.Resolve` | yes |
| `macroBar.barBorderSize` | 4 | `bar.borderSize` 1 | no companion exists | **no** (**D1**) |
| `macroBar.barBorderColor` | `{0.25,0.25,0.25,1}` | `bar.border` `{0,0,0,1}` | `barBorderColorFromSkin` | yes (CM-G5) |
| `macroBar.buttonBackdropColor` | `{0,0,0,0.6}` | none exact (**D2**) | `buttonBackdropColorFromSkin` | owner call (D2) |
| `macroBar.buttonBorderStyle` | `"Blizzard Tooltip"` | `bar.borderStyle` `"None"` | BorderGroup `fromSkin = true` gives `buttonBorderStyleFromSkin` | yes |
| `macroBar.buttonBorderSize` | 4 | `bar.borderSize` 1 | none | **no** (D1) |
| `macroBar.buttonBorderOffset` | 2 | — (geometry) | — | no |
| `macroBar.buttonBorderColor` | `{1,1,1,1}` | `icon.border` `{0,0,0,1}` | `buttonBorderColorFromSkin` | yes (CM-G5) |
| `macroBar.labelFont` | `"Friz Quadrata TT"` | `hud.font` `"Ka0s Oxanium SemiBold"` | `H.FontGroup{ fromSkin = true }` gives `labelFontFromSkin` | yes |
| `macroBar.labelFlags` | `"OUTLINE"` | `hud.outline` `"OUTLINE"` | none, and an enum row | no (equal under KD anyway) |
| `macroBar.labelShadow` | false | (`font.shadow` is a body-text token, not HUD) | — | no (ResetToSkin would set it **true**) |
| `macroBar.labelColor` | `{1,0.82,0,1}` | `text.accent` GOLD (exact) | `labelColorFromSkin` | yes (CM-G5) |
| `macroBar.labelScale` | 25 (% of button) | — (geometry; `hud.fontSize` is points) | — | no |
| `macroBar.flyoutBackdropColor` | `{0,0,0,0.85}` | none exact (`popup.bg` 0.92) | `flyoutBackdropColorFromSkin` | owner call (D2) |
| `macroBar.flyoutShadeColor` | `{0,0,0,0.8}` | none exact (`cover.dim` 0.6) | `flyoutShadeColorFromSkin` | owner call (D2) |
| show toggles `barBackdrop`, `barBorder`, `buttonBackdrop`, `buttonBorder`, `flyoutBackdrop` | true | — | — | no (structure, not style) |
| `useClassColor*` (7 companions) | false | — | the class color wins over fromSkin when on (**D12**) | no |

Every new `*FromSkin` companion needs an AceDB default (false) in `defaults/Profile.lua`. Without one,
`ResetToSkin`'s `parent[leaf.."FromSkin"] ~= nil` test misses on a non-color key, and that key takes the
sentinel. The pin `tests/test_schema.lua:1075-1137` (the full schema dump) moves with them.

**What the reset does to a player on Ka0s Default.** O2 accepted the look change, but here it is in full.
Without labels, the bar loses its 4 px "Blizzard Tooltip" edges (KD `bar.borderStyle = "None"`). Its
button edges turn from white to black (`icon.border`). Its border color turns from gray to black. Its
labels move from Friz Quadrata to Oxanium. Only the bar fill and the label color are unchanged. This is
**D1**.

---

## 4. Exceptions

| Id | What | Rung | Reason |
|---|---|---|---|
| CM-E1 | StaticPopups `KCM_CONFIRM_RESET`, `KCM_RESET_PRIORITIES`, `KCM_RESET_CATEGORY` (`settings/General.lua:146`, `settings/Category.lua:301`) | 3 | skinning-§7: a StaticPopup is never restyled |
| CM-E2 | GameTooltip frame (item and spell tooltips `KCMItemRow.lua:375-383`, `core/MacroDisplay.lua`, the drag-handle tooltips) | 3 | §7: only the lines CM writes take tokens (H6, S9, S12, S13) |
| CM-E3 | LSM30_Border / LSM30_Font pull-outs and ColorPickerFrame (Macro Bar page swatches) | 3 | §7 |
| CM-E4 | Blizzard action-button art on the secure slots and flyout entries: `UI-Quickslot-Depress`, `ButtonHilight-Square`, `CooldownFrameTemplate` swipe (`MacroBarButton.lua:38-39`, `:409-422`; `MacroBarFlyout.lua:49`, `:212`, `:219`); `ButtonHilight-Square` on the drag icon (`KCMMacroDragIcon.lua:104`) | 3 | Blizzard templates and art on protected frames. Restyling the secure buttons' own art risks taint and is not "the addon's own overlay" |
| CM-E5 | SettingsPanel chrome, the sidebar and the AddOns category Enable checkbox | 3 | §7 |
| CM-E6 | Launcher: LibDBIcon minimap button and the MenuUtil context menu (`core/LauncherSetup.lua`) | 3 | third-party / Blizzard menu. Launcher-1.0 takes no owner |
| CM-E7 | Item, spell and macro icons (bar slots, flyout entries, `KCMItemRow` itemTex, drag icon) | 4 | game art |
| CM-E8 | Crafting-quality atlas (`KCMItemRow.lua:216`) | 4 | item-quality meaning |
| CM-E9 | ReadyCheck-Ready / NotReady glyphs (owned, shown, included) and the Favorites pick star (`KCMItemRow.lua:35-37`; `settings/MacroBar.lua:739-740`; `settings/StatPriority.lua:108-109`) | 4 | yes/no meaning carried by Blizzard art |
| CM-E10 | `useClassColor*` companions (class color) | 4 | class-color meaning (options-ui-§17) |
| E-chat | Every chat line: `KCM.PREFIX` cyan tag, the slash help, the `/cm dump` tags `[owned]`/`[on]`/`[off]`/`<-- pick`, debug ON/OFF, schema error | 3 | Text in Blizzard's chat frame, not a frame CM draws. The tag color is chat-output's brand rule. See D11 |

---

## 5. Gaps (rung 2)

Strict list. Each one holds a value that no existing token carries **exactly** (Ka0s Default must not
move), and each value is typed on a frame CM draws.

| Id | Component | Why no primitive or token fits | Proposed | Ka0s Default today |
|---|---|---|---|---|
| CM-G1 | KCMIconButton hover swatch (priority-row up/down/delete) | The gold hover fills sit at 0.10 (`list.hover`), 0.15 (`menu.hover`), 0.16 (`tab.rule`) and 0.18 (`list.sel`); none is 0.25. A token read with a typed alpha is itself #107 | token `btn.iconHover` (color, Buttons group): an icon button's hover fill | `{1, 0.82, 0, 0.25}`: `modules/KCMIconButton.lua:120` |
| CM-G2 | Warning text on the settings pages (no spec, empty list, no sub-categories, no categories) | `sem.warn` and `text.link` are `{1,0.5,0}`; the text draws `{1, 0x88/255, 0}` | token `text.warn` (color, Text group) | `|cffff8800` = `{1, 0.533, 0, 1}`: `settings/Category.lua:709`, `:712`, `:952`, `:1090`; `settings/StatPriority.lua:738` |
| CM-G3 | Two grays CM writes into GameTooltip lines (score explain tooltip) | `gtip.*` holds 0.5 (`muted`), 0.7 (`subtle`), 0.9 (`body`) and 1 (`value`). The text draws 0.533 and 0.667 (`cover.text` holds 0.667, but it belongs to the combat cover, not a tooltip) | tokens `gtip.note` and `gtip.summary` (color, Text group) | `|cff888888` = `{0.533,0.533,0.533,1}` (`settings/Category.lua:141`); `|cffaaaaaa` = `{0.667,0.667,0.667,1}` (`:147`) |
| CM-G4 | Disabled icon tint on CM's custom icon widgets | `icon.dim` is `{0.55,0.55,0.55,1}` (opaque); the widgets draw half-alpha 0.5 (AceGUI's stock Icon disabled look); no disabled-icon token | token `icon.disabled` (color, Lists and cards group) | `SetVertexColor(0.5, 0.5, 0.5, 0.5)`: `modules/KCMIconButton.lua:91`, `modules/KCMScoreButton.lua:76` |
| CM-G5 | A *follow the skin* companion row for **swatch** rows (`O.ColorPair`, and the color row inside `O.BorderGroup` / `O.FontGroup`) | `OptionsCompose`'s `FROM_SKIN` covers only `font`, `borderStyle` and `barTexture` (`LibKa0s/OptionsCompose.lua:323-330`). `Skin.ResetToSkin` sets `<colorKey>FromSkin = true` for a color, but no composer emits a row for it, so after the R3 reset the player cannot see or clear it, and a swatch pick would be ignored while `S.Resolve` answers the token | primitive-option: `fromSkin = true` on ColorPair, and on the color leaves of BorderGroup and FontGroup, emits `<key>FromSkin` (*Use the skin's color*) and disables the swatch while on, shown with `skinValue` | No visual today. The rows draw exactly as now while the companion is false |

Not gaps (rung 1, exact): `text.accent`, `text.disabled`, `text.highlight`, `gtip.title`, `gtip.value`
and `bar.bg` cover every other typed value. The unlock wash matches `menu.hover` exactly (D4). The drag
icon gray matches `sem.unknown` exactly (D5).

---

## 6. Doubtful calls for DECISIONS.md

| Id | Question | Recommendation |
|---|---|---|
| D1 | R3 reset on Ka0s Default changes the bar's look: the 4 px Blizzard Tooltip edges vanish (`bar.borderStyle "None"`), and the border and button-edge colors go black. Sizes (`barBorderSize`, `buttonBorderSize`) have no companion | Apply O2 as ruled: the reset covers the two border styles, `labelFont` and the color keys (with CM-G5). Leave sizes, flags, shadow and offset as the player's. Record the visible change in `06_SMOKE_TESTS.md`. If the owner wants the bar's look kept under Ka0s Default, the alternative is a library change to KD's `bar.*` values, which would move every addon |
| D2 | Button fill `{0,0,0,0.6}`, flyout fill `{0,0,0,0.85}` and indicator shade `{0,0,0,0.8}` have no HUD token | Keep them the player's (outside the R3 list). The fallback literals (`MacroBarButton.lua:299`, `MacroBarFlyout.lua:443-445`, `MacroBar.lua:394`, `:398`) become reads of the AceDB default rather than tokens. Not a rung-2 gap, because §6 names texture, border and font as the HUD style that follows |
| D3 | The picker's eye needs `onPreview`. CM has no test mode | Pass no `onPreview` (the picker draws the eye only for a function), declare only `settings` in `LibKa0s icons:`. Alternatively make `onPreview` show the bar unlocked, and declare `eye` too |
| D4 | The unlock wash `{1,0.82,0,0.15}` equals `menu.hover` | Use `menu.hover` unless the M0 consolidation finds the same move-hint wash in two or more HUD addons. In that case use a rung-2 `hud.unlockWash` with KD `{1,0.82,0,0.15}` |
| D5 | "Macro not created yet" `|cff999999` (0.6) equals `sem.unknown` | Use `sem.unknown` (a not-yet state, exact value) |
| D6 | The count text (`NumberFontNormal`) has no setting. Should it take `hud.font` and `hud.outline`? | Yes for face and outline, keeping the font object's size. It is HUD text (§6). Under KD this moves it from the client number font to Oxanium, which is acceptable under v1.79.0's "Ka0s Default looks different" |
| D7 | The label shadow color `(0,0,0,1)` and offset (1,-1) are typed | Keep them: a legibility constant behind the player's `labelShadow` toggle, the same in every skin. Not chrome |
| D8 | KCMItemRow's 0.4 alpha for a non-applicable row | Keep it: a state dimming, not a color |
| D9 | The flyout arrow (`ChatFrameExpandArrow`, untinted) | Tint it with `icon.arrow`. That is the token's job (in-client arrow art). Owner smoke-checks KD, because GOLD multiplies the yellow art. If it reads wrong, leave it untinted as CM-E4 |
| D10 | Profiles page (AceConfigDialog acquires its own widgets) | `Skin:PaintAceTree(owner, container)` after each `dialog:Open`. AceConfigDialog sets no per-widget OnRelease, so the restore chain holds |
| D11 | Chat colors (`[CM]` tag, slash help, dump tags) | An exception (E-chat). The chat frame is Blizzard's, and the tag color is chat-output's |
| D12 | Class color versus fromSkin precedence on a swatch with both companions | Class color wins when its companion is on (an explicit player pick). Otherwise fromSkin applies |
| D13 | CM-G1 alternative: test_widgets.lua:115-135 already removed the identical gold hover from the score button ("nothing else in the collection does this") | Owner's choice: remove KCMIconButton's hover too (closes CM-G1 with no token, but changes the KD look), or keep it with `btn.iconHover`. Recommend the token, since the run must not change KD unasked |
| D14 | CM's own AceGUI acquisitions: PaintAce at each site, or create through the proxy | Create through `H.AceGUI` (the proxy the Options instance carries once the owner is registered), one choke point. Custom types (S7, S8, S10, S11) have no painter, so they paint themselves from `KCM.Skin` |

---

## 7. Re-vendor v1.77.0 to v1.79.0 obligations (CM-RV)

- **Payload.** `git archive v1.79.0` both `libs/LibKa0s/` and `tests/_kit/`. New files: `Toast.lua`,
  `Skin.lua`, `SkinDefs.lua`, `SkinPaint.lua`, `SkinPaintExtras.lua`, `SkinPaintControls.lua`,
  `SkinEUI.lua`, `SkinAce.lua`, `WidgetsCopyWindow.lua`, `DebugLogWindow.lua`, `OptionsAppearance.lua`
  and `OptionsSkinPicker.lua` (XML 41 to 53 scripts). Also the Oxanium fonts and OFL text, and eight
  bar `.tga` files.
- **Options stub (`Kit.assertSurfaceParity`).** CM's Options parity is a **projection**:
  `tests/test_surface_parity.lua:272-317` lists `OPTIONS_SEAM` and `OPTIONS_LIVE_ONLY` from a grep of
  the `Helpers.` / `H.` members CM calls. When CM starts calling `H.AppearanceTab`, `H.AppearanceRows`,
  `H.SkinPicker` and `H.HideSkinPicker`, they join `OPTIONS_SEAM`. `AppearanceTab` is evaluated at
  **file load** inside `TAB_OPTS` (`settings/General.lua:426`), so the degraded arm of
  `settings/OptionsSetup.lua:349-380` must answer it (beside `MasterControls`, `ColorPair`, `FontGroup`
  and `BorderGroup`), returning a harmless entry or nil that `TAB_OPTS` tolerates. `AppearanceRows`,
  `SkinPicker` and `HideSkinPicker` are called at run time only. Either stub them as no-ops or list
  them live-only with the reason. Standard §3 says every stub answers `AppearanceTab` and
  `AppearanceRows`. Recommend stubbing all four.
- **`tests/test_libka0s.lua` MAJORS pins (:40-117).** Three file lists change:
  - **DebugLog:** add `"DebugLogWindow"` (paired `__windowMinor` / `__windowShellMinor`).
  - **Options:** add `"OptionsAppearance"` (`__appearanceMinor` / `__appearanceShellMinor`) and
    `"OptionsSkinPicker"` (`__pickerMinor` / `__pickerShellMinor`).
  - **Skin:** optionally add a `LibKa0s-Skin-1.0` entry, since CM now consumes it: files `Skin`,
    `SkinDefs`, `SkinPaint`, `SkinPaintExtras`, `SkinPaintControls`, `SkinEUI`, `SkinAce`.

  Without the first two, *no file registers under a major it does not belong to* goes red.
- **`tests/test_vendor_sync.lua`.** It reads the two `CLAUDE.md` lines. Roll `Bundles [LibKa0s] v1.77.0`
  to v1.79.0 (or v1.80.0 if M1 cuts it). Roll `LibKa0s icons: clear, close, copy, help, info, segment`
  to add **`settings`** (the picker's gear), plus **`eye`** only if D3 passes `onPreview`. Run
  `tools/prune-icons.lua` from the tag.
- **`tests/test_schema.lua:1075-1137`** (the full schema dump) gains the `skin.*` rows and every
  `*FromSkin` companion. `tests/test_settingsui.lua` pins the General page's row and tab counts on
  both arms. `tests/test_widgets.lua` pins the score button's source text.
- **TOC.** Add `EllesmereUI` to `## OptionalDeps` (§5). Add `core\SkinSetup.lua` after
  `core\CoreSetup.lua` and before `core\LauncherSetup.lua` / `core\DebugLogSetup.lua` and every module
  that builds a frame (it registers at file load). The comment "fifteen majors" (`ConsumableMaster.toc:50`)
  is stale: v1.79.0 has nineteen.
- **CLAUDE.md "Fourteen of its majors are consumed"** (`CLAUDE.md:81`) and
  **`docs/ARCHITECTURE.md:279`** become fifteen (Skin joins). `Pool`, `Glow`, `Sim` and `Toast` stay
  unconsumed.
- **v1.79.0's "Ka0s Default looks different"** reaches CM only after it registers. The smoke checks
  re-look at the bar labels and settings pages in Oxanium.
- README: the Tests badge count moves with the suite. Add font credits (Oxanium OFL plus the skins'
  faces, if the README credits shipped media).

---

## 8. Risks

- **Secure HUD frames.** The slot buttons and flyout entries are `SecureActionButtonTemplate`. The flyout
  and indicator are `SecureHandlerEnterLeaveTemplate`, and the bar carries a visibility state driver
  (`MacroBar.lua:462`), so the bar is protected in combat. Any facade primitive that creates holder
  frames or re-anchors on them must run **out of combat**. A skin switch is refused in combat
  (OptionsCombat), but `/cm` profile verbs, a Copy from another addon, or `OnLooksChanged` while
  fighting can still reach a repaint. CM's HUD repaint must route through `MacroBar.Update`'s existing
  combat deferral (`pendingUpdate`, PLAYER_REGEN_ENABLED) and never call primitives on these frames
  directly in combat. Prefer reading tokens in CM's own appliers (`BB.ApplyBorder`,
  `BB.ApplyBackdropTex`, `FO.ApplyBackdrop`) over facade primitives that track and replay on secure frames.
- **Pooled AceGUI widgets.** CM acquires stock `Button`, `Label`, `CheckBox`, `Dropdown` and `Heading`
  from the shared pool outside the proxy. Painting them without the SkinAce restore leaks a skin into
  other addons. Use the proxy or `Skin:PaintAce`, and never `SetCallback("OnRelease")` directly (none do
  today). The four custom types are CM-only pools, but they hold a mutable gold hover and colors, so
  repaint them in `OnAcquire` from the current skin, not once in `Constructor`.
- **Locale keys carry color escapes** (CM-G2): moving the color out renames five keys in
  `locales/enUS.lua`. `tests/test_locale.lua` will notice.
- **Perf, hot paths.** `BB.ApplyStyle` runs per button per layout pass (slider drags commit on change,
  `sliderCommit = "change"`). `S.Resolve` / `S.Token` are table reads, which is fine. Do not call
  `S.BarStyle()` per button per pass: it allocates a fresh table. Cache it per pass, or on `OnLooksChanged`.
  `KCM.SwatchColor` reuses a scratch table (`core/CoreSetup.lua:157`), and the token path should not
  allocate either. `tests/perf.lua` pins the walk.
- **R3 reset via `ResetToSkin`.** A wrong key (number, enum or bool) stores `"@skin"` or flips a toggle on.
  A missing AceDB default for a companion stores the sentinel into a string key. The step must also
  survive the profile-hook re-entry (`core/ConsumableMaster.lua:618-620`): stamp v4 only after it.
- **Brand-new profiles** have no stamp, so they start at v1 and meet the v4 reset too. That is the
  intended O2 behaviour (a fresh profile follows the skin), but the R3 step must not run before AceDB
  defaults exist.
- **Picker timing (O3).** `pickerSeen` defaults false on every profile, and CM is secure-HUD heavy. Hold
  the picker to `PLAYER_REGEN_ENABLED` like LootHistory (`../LootHistory/core/SkinSetup.lua:413-433`),
  and never show it while stood down (`KCM.Lifecycle`).
- **File cap.** `settings/MacroBar.lua` 1210, `settings/Category.lua` 1163 and `settings/Panel.lua` 1143
  lines. All are under 1500, but the skin rows, the companions and the AceGUI routing land mostly in
  MacroBar.lua and Category.lua. Put the Appearance and skin rows in a new `settings/Appearance.lua` (or
  in General.lua, 455 lines), and the HUD skin resolution in `core/SkinSetup.lua` or a small HUD
  helper, not in MacroBar.lua.
- **No reference adopter for the HUD reset.** LootHistory and the Skin Tester call no
  `ResetToSkin` / `fromSkin`, so CM-03 is the collection's first use of it. Expect library friction, the
  likely source of CM-G5.

---

## 9. Effort

**L.** A secure HUD with three backdrop and border appliers, plus the collection's first R3 reset (with
companions, and probably CM-G5 upstream). Six settings files (two over 1100 lines) with stock and
four custom AceGUI widget types. Five rung-2 gaps. The tool windows come nearly free.
