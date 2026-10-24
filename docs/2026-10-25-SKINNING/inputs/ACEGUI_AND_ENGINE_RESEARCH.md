# AceGUI anatomy and skin-engine research (input to the 2026-10-25 skinning bundle)

Research date 2026-10-25. Everything here was read in place; no repo was modified.

**Sources and abbreviations**

| Tag | Source |
|---|---|
| `AG` | `../LootHistory/libs/AceGUI-3.0/AceGUI-3.0.lua` (AceGUI-3.0 minor **41**, line 28) |
| `AGW/<file>` | `../LootHistory/libs/AceGUI-3.0/widgets/<file>` |
| `SMW/<file>` | `../AuraMaster/libs/AceGUI-3.0-SharedMediaWidgets/<file>`. AbsorbTracker, AuraMaster, ConsumableMaster, DpsRace, KickCD, MultiMeters, PanelMaster and PartyFrameEnhanced also vendor it. |
| `LK/<file>` | `../LibKa0s/LibKa0s/<file>` |
| `ASK/<file>` | `AddOns/AddOnSkins/<file>`. The installed copy's TOC says `## Interface: 110002`, so it is stale for 12.x. The license allows use only, with "all rights reserved": describe its techniques and do not copy them. |
| `EUI/<file>` | `AddOns/EllesmereUI*/<file>`. The license reserves all rights (`EllesmereUI/license.txt`), so this report describes its techniques only. |
| `ELV` | `https://github.com/tukui-org/ElvUI/blob/main/ElvUI/Game/Shared/Modules/Skins/Ace3.lua`. The bundle's prompt gave the old path `Skins/Libraries/Ace3.lua`, which now returns 404. |
| `BLZ/<file>` | `https://github.com/Gethe/wow-ui-source/blob/live/Interface/AddOns/<file>`, the `live` branch, last commit 2026-10-23 |

---

## 1. AceGUI widget anatomy and lifecycle

### 1.1 The pool and the lifecycle (all in `AG`)

- **One pool for the whole client.** `AceGUI.objPools[widgetType]` is a set keyed by widget object (`AG:88-123`). AceGUI is a LibStub library, so every addon in the client uses the same pools, Ka0s or not. A frame that AuraMaster released can be handed to WeakAuras' or Details' options on the next `Create`. The answer to "are widget frames shared across addons?" is **yes**.
- **Version discard.** `newWidget` drops a pooled object whose `AceGUIWidgetVersion` is older than the registered version and builds a fresh one (`AG:100-110`). Old objects are orphaned rather than recycled, but WoW frames are never garbage-collected, so they stay in memory.
- **`AceGUI:Create(type)`** (`AG:138-163`) takes an object from the pool or calls the constructor. It maps any legacy `Acquire`/`Release` fields to `OnAcquire`/`OnRelease`, calls `widget:OnAcquire()`, then sets the `"List"` layout.
- **`AceGUI:Release(widget)`** (`AG:172-206`) runs in this order:
  1. sets `isQueuedForRelease`;
  2. calls `PauseLayout`;
  3. calls `frame:Hide()`;
  4. calls **`widget:Fire("OnRelease")`** (line 177);
  5. calls `ReleaseChildren`;
  6. calls `widget:OnRelease()` if one is present;
  7. **wipes `userdata` and `events`**;
  8. clears the size fields;
  9. calls `ClearAllPoints`, `Hide` and `SetParent(UIParent)`;
  10. calls `delWidget`.

  An `OnRelease` *callback* therefore fires before the callbacks are wiped, which LibKa0s already relies on (`LK/OptionsWidgets.lua:338-361`). `events` holds **one slot per event name**, so a skin that calls `SetCallback("OnRelease")` replaces the consumer's own handler for that event, and the reverse is also true.
- **`RegisterAsWidget` / `RegisterAsContainer`** (`AG:511-535`) run **once per constructed object**, from the constructor and never on re-acquire. Each sets `frame.obj = widget` and the `WidgetBase` metatable. These two calls are the hook point that ElvUI and AddOnSkins use.
- **`RegisterWidgetType(name, ctor, ver)`** (`AG:549-558`) is process-global, and the highest version wins. `LK/Options.lua:265-330` (`__PatchLSM30Border`) already wraps a constructor this way and holds an idempotence sentinel.
- **Where OnAcquire/OnRelease live.** Most widgets copy a `methods` table onto the instance (`widget[method] = func`), and Dropdown assigns `self.OnRelease = OnRelease` directly. In both cases **the methods are instance fields**, so wrapping `widget.OnRelease` per instance is possible. LibKa0s already does this for ScrollFrame (`LK/OptionsScroll.lua:79-195`), restores the original on release and keeps a shared, not per-addon, marker. CheckBox, Slider, Button, Heading, ColorPicker, Icon, InlineGroup and SimpleGroup have **no `OnRelease`** (the line is commented out). `Release` tests `if widget.OnRelease`, so a wrapper that does not chain still works for them.

### 1.2 Per-widget anatomy (stock AceGUI minor 41)

| Widget (ver) | Fields / regions worth skinning | Stock art | Ref |
|---|---|---|---|
| CheckBox (26) | `frame` (Button), `checkbg` (ARTWORK), `check` (OVERLAY), `highlight` (HIGHLIGHT), `text`, `image`, `desc` (created lazily) | `checkbg`=130755 `UI-CheckBox-Up`, `check`=130751 `UI-CheckBox-Check`, `highlight`=130753. Radio mode switches all three to 130843 `UI-RadioButton` with texcoords. `SetDisabled` desaturates `check` and grays `text`. | `AGW/AceGUIWidget-CheckBox.lua:154-168, 241-283` |
| Slider (23) | `frame`, `label`, `slider` (Slider + BackdropTemplate), `lowtext`, `hightext`, `editbox` (EditBox + BackdropTemplate) | Slider backdrop `UI-SliderBar-Background/-Border`, thumb `UI-SliderBar-Button-Horizontal`. The editbox backdrop is `ChatFrameBackground`; its border is recolored on enter/leave (lines 113/117). | `AGW/AceGUIWidget-Slider.lua:200-208, 213-270` |
| EditBox (29) | `frame`, `editbox` (named `AceGUI-3.0EditBox<n>`, **InputBoxTemplate**), `label`, `button` (**UIPanelButtonTemplate** "OK") | The template's `Left/Middle/Right` (on live these are the atlases `common-search-border-*`) | `AGW/AceGUIWidget-EditBox.lua:217-251` |
| MultiLineEditBox (33) | `frame`, `label`, `button` (UIPanelButtonTemplate), `scrollBG` (BackdropTemplate), `scrollFrame` (**UIPanelScrollFrameTemplate**, named), `scrollBar`, `editBox` | backdrop + the template's scrollbar art | `AGW/AceGUIWidget-MultiLineEditBox.lua:284-357` |
| Button (24) | `frame` (named Button, **UIPanelButtonTemplate**), `text` | `Left/Middle/Right` `UI-Panel-Button-Up`. Blizzard's own OnMouseDown/Up/Disable **calls SetTexture** to swap Up/Down/Disabled (`BLZ/Blizzard_SharedXML/SecureUIPanelTemplates.lua:36-54`). | `AGW/AceGUIWidget-Button.lua:77-91` |
| Heading (20) | `frame`, `label` (GameFontNormal), `left`, `right` | 137057 `UI-Tooltip-Border` with a texcoord crop | `AGW/AceGUIWidget-Heading.lua:42-69` |
| Label (28) / InteractiveLabel (21) | `label`, `image`; InteractiveLabel adds `highlight` | **`OnAcquire` calls `SetFontObject()`**, so a Label resets its own font on re-acquire (`AGW/AceGUIWidget-Label.lua:81`). Heading and the others do not. | `AGW/...Label.lua:159-166`, `...InteractiveLabel.lua:78` |
| Icon (21) | `frame`, `label`, `image`, `highlight` | highlight 136580 | `AGW/AceGUIWidget-Icon.lua:99-125` |
| ColorPicker (28) | `frame`, `colorSwatch` (130939 `ChatFrameColorSwatch`), plus unnamed `texture` and `checkers` (188523), `text` | Opens Blizzard's **global `ColorPickerFrame`** and changes its strata, level and clamp on every open | `AGW/AceGUIWidget-ColorPicker.lua:33-119, 172-225` |
| Dropdown (36) | `frame`, `dropdown` (named `AceGUI30DropDown<n>`, **UIDropDownMenuTemplate**), `button` (`<name>Button`), `button_cover`, `text` (`<name>Text`), `label`, `pullout` | `_G[name.."Left/Middle/Right"]` from the legacy template | `AGW/AceGUIWidget-DropDown.lua:349-351, 645-711` |
| Dropdown-Pullout (5) | `frame` (named `AceGUI30Pullout<n>`, BackdropTemplate), a scroll frame, a slider (`AceGUI30PulloutScrollbar<n>`), item frames | backdrop. `Open()` fires `"OnOpen"` (`:182-200`). | `AGW/AceGUIWidget-DropDown.lua:36-38, 252-303` |
| Dropdown-Item-* | each item is a named Button (`AceGUI30DropDownItem<n>`) and an AceGUI widget in its own right | | `AGW/AceGUIWidget-DropDown-Items.lua:153, 240-470` |
| ScrollFrame (26) | `frame`, `scrollframe`, `scrollbar` (named `AceConfigDialogScrollFrame<n>ScrollBar`, **UIPanelScrollBarTemplate**), `scrollbg`, `content` | `UI-ScrollBar-Knob` and `UI-ScrollBar-ScrollUp/DownButton-*` (`BLZ/.../SecureScrollTemplates.xml:7-30`) | `AGW/AceGUIContainer-ScrollFrame.lua:167-199` |
| InlineGroup (22) | `frame`, `titletext`, `border` (BackdropTemplate `PaneBackdrop`, colors 0.1/0.5 and 0.4), `content` | backdrop | `AGW/AceGUIContainer-InlineGroup.lua:69-90` |
| SimpleGroup (20) | `frame`, `content`. No art. | | `AGW/AceGUIContainer-SimpleGroup.lua:49-57` |
| TabGroup (38) | `frame`, `titletext`, `border` (backdrop), `content`, `tabs[]` | Tabs are **plain Buttons created by `CreateTab`** (not AceGUI widgets). They are kept on the TabGroup instance and reused with it, and carry six `UI-OptionsFrame-(In)ActiveTab` textures plus a highlight. | `AGW/AceGUIContainer-TabGroup.lua:237-286, 493-516` |
| LSM30_* (13) | `frame` from `AGSMW:GetBaseFrame()`: `label`, `DLeft/DMiddle/DRight` (`Glues\CharacterCreate\CharacterCreate-LabelFrame`), `text`, `dropButton` (`UI-ChatIcon-ScrollDown-Up`). Border and Background add `displayButton` (backdrop). | The pop-up list frame comes from **a cache local to the AGSMW library**, `AGSMW:GetDropDownFrame()` / `ReturnDropDownFrame()`. It is shared by every addon and is not an AceGUI widget. | `SMW/prototypes.lua:50-121, 202-263`, `SMW/BackgroundWidget.lua:10-25` |

---

## 2. How ElvUI and AddOnSkins skin AceGUI, and a technique for per-addon skinning

### 2.1 AddOnSkins (`ASK/Skins/AddOns/Ace3.lua`)

- It **does nothing when ElvUI is loaded** (line 3).
- It replaces `AceGUI.RegisterAsWidget` and `RegisterAsContainer` with wrappers that switch on `widget.type`, skin the object, then call the original (lines 10-13, 204, 207-291). Skinning happens **once, at construction**, and is **permanent**: the skinned object goes back into the pool still skinned, so every addon that later acquires it gets the skin. That is the intent, because the skin is global.
- **Techniques:**
  - It wipes stock textures with `SetTexture('')`.
  - It **replaces the region's `SetTexture` method with a no-op** so that AceGUI's own `SetType` cannot restore the art (CheckBox, lines 24-51).
  - It uses `hooksecurefunc` on the instance methods `SetDesaturated` and `label.SetTextColor` to recolor.
  - It uses `HookScript('PostClick')` to skin the pull-out when it opens.
  - It wraps `widget.CreateTab` for TabGroup (lines 269-281).
- **Core primitives** (`ASK/Core/Skins.lua`):
  - `S:HandleButton` (920-958) clears the Normal, Highlight, Pushed and Disabled textures, applies `SetTemplate` (a backdrop) and hooks OnEnter, OnLeave, OnEnable and OnDisable. It is guarded by a `button.isSkinned` key **written onto the frame**.
  - `S:StripTextures` (432) uses `SetTexture('')` and `SetAtlas('')` across the frame's regions and the well-known children (`NineSlice`, `Inset`, `Border` and others; list at line 28).
  - `S:CleanTexture` (1620) supports three modes: kill, `SetAlpha(0)`, or clear.
- **AceGUI upgrades:** the hooks replace a field that a newer AceGUI minor redefines when it loads. AddOnSkins works around this by shipping its own up-to-date Ace3 (`ASK/Libs/Ace3/`) and by taking `LibStub('AceGUI-3.0')` at init (`ASK/Init.lua:29`).

### 2.2 ElvUI (`ELV`)

- **Hook point:** the same two `RegisterAs*` functions, but the hook survives upgrades. ElvUI calls `hooksecurefunc(LibStub, 'NewLibrary', ...)` (around line 711), and for each AceGUI minor that registers, `HookAce3` (608-631) clears `RegisterAsWidget/Container` and installs a **`__newindex` metamethod on the library table** (537-544, 563-596). When the new minor's file then assigns `RegisterAsWidget`, the metamethod stores a wrapper that runs `S.Ace3_RegisterAsWidget` first, gated by the `E.private.skins.ace3Enable` setting. Widgets built before ElvUI initialized are found by walking `UIParent:GetChildren()` for `.obj` (`EarlyAceWidgets`, lines 683-701).
- **Skinning happens once per construction and stays global.** Examples:
  - The checkbox gets a `CreateBackdrop` and its art is cleared. `checkbg.SetTexture`, `highlight.SetTexture` and `check.SetTexture` are set to `E.noop` (133-160).
  - Instance methods are hooked with `hooksecurefunc(widget,'SetDisabled'|'SetType')`, and the tab's `SetSelected` is hooked too.
  - The `-ElvUI` widget variants, such as `Dropdown-ElvUI` and `MultiLineEditBox-ElvUI` from `ElvUI_Libraries/.../Ace3-ElvUI/`, are new type names, so they do not collide with the stock types.
- **Neither addon restores anything on release, and neither tries to.** Both choose a global, permanent skin. The `= noop` overrides make a restore impossible without keeping the original method.

### 2.3 What our constraint rules out

Our constraint has four parts: skin per consumer addon, skin only widgets our pages acquire, restore the stock look on release, and coexist with ElvUI or AddOnSkins when they are installed. It rules out three things:

- **Hooking at construction.** Constructor time does not know who will acquire the widget.
- **Overriding methods with `noop`.** The override survives into the pool and cannot be undone.
- **Destructive `SetTexture('')`.** The original texture would have to be re-derived on restore.

### 2.4 Proposed technique: an overlay at acquire time, alpha restored at release

1. **Ownership at acquisition.** `OptionsWidgets` already creates every widget a page uses (`LK/OptionsWidgets.lua:167-1193`). Add one call, `Skin.Apply(owner, widget)`, right after each `O.AceGUI:Create(...)`. `owner` is the consumer descriptor (addon name). Skin state goes in a **weak-keyed external table** keyed by `widget.frame`, never in fields on the frame or the widget. Since ElvUI and AddOnSkins already write `isSkinned`, `backdrop` and similar keys, use a single namespaced table, not loose keys.
2. **Fade, do not destroy.**
   - Record each stock region's current alpha in the state table, then `SetAlpha(0)`.
   - Alpha survives later `SetTexture` and `Show` calls, which is what you need for:
     - the UIPanelButton Up/Down swap (`BLZ/.../SecureUIPanelTemplates.lua:44-54`);
     - AceGUI's CheckBox `SetType` (`AGW/...CheckBox.lua:154-168`);
     - TabGroup's select/deselect `Show`/`Hide` of the Left/Middle/Right textures.
   - **Do not use `SetTexture('')`**, and do not replace methods with noop.
3. **Overlays the skin owns.** Create child textures once per frame (fill, border edges, check glyph, hover) and keep them in state, so a frame that comes back from the pool reuses them. `Apply` shows them and paints them with the owner's tokens.
4. **Restore on release.**
   - Wrap `widget.OnRelease` per instance, following the precedent in `LK/OptionsScroll.lua:177-195`:
     - the wrapper first restores the stock state: region alphas, fonts (`SetFontObject` back to the object captured before the skin changed it), text colors, the backdrop colors the skin recolored, and anchors if any were moved (avoid moving anchors);
     - it hides the overlays and clears the owner entry;
     - it puts the original `OnRelease` back on the instance;
     - it then calls the original.
   - Do **not** use `SetCallback("OnRelease")`. It is a single slot shared with consumer code (the landing logo uses it) and would collide.
   - An alternative is one global `hooksecurefunc(AceGUI, "Release", post)` that looks the widget up in the state table. It runs after `delWidget`, which is safe because nothing acquires the widget in between, and it costs one hook rather than one per instance. However, a later AceGUI minor that loads after the hook is installed replaces `AceGUI.Release` (the file defines it at top level). Install it lazily on the first render, and re-check the function's identity on each page build.
5. **Idempotence and a shared marker.** Several Ka0s addons vendor LibKa0s, but LibStub gives all of them one `lib`. Keep the state table on the library (`lib.__skinState`, preserved across minor upgrades with `lib.__skinState = lib.__skinState or setmetatable({}, {__mode="k"})`), the same lesson as `LK/OptionsScroll.lua:81-83`.
6. **Coexisting with ElvUI/AddOnSkins.** When either is loaded, the widget is already globally skinned and some of its `SetTexture` methods are `noop`. Options:
   - **Detect and step aside.** If `frame.backdrop` or `isSkinned` is present, apply only the token-driven pieces such as fonts and colors.
   - **Expose a setting.** Offer "Defer to ElvUI/AddOnSkins", on by default when either addon is loaded.

   Never try to restore their art.

**Risks**

| Risk | Assessment and mitigation |
|---|---|
| AceGUI widget version bumps | Field names (`checkbg`, `check`, `slider`, `editbox`, `dropdown`, `button`, `pullout`, `scrollbar`, `border`, `colorSwatch`) have been stable for years, but any of them could disappear. Guard every field access. Keep a table of skinners keyed by type, record the `AceGUIWidgetVersion` it was written for, and fall back to stock (skip) when a field is missing. Objects discarded by a version bump are orphaned; a weak-keyed state table tolerates that. |
| Template art moves (Blizzard) | `InputBoxTemplate` already uses atlases on live (`common-search-border-left/middle/right`, `BLZ/Blizzard_SharedXML/Shared/InputBox/InputBoxTemplates.xml:43-70`). Fade by **parentKey, plus a sweep of `GetRegions()` that skips our own overlays**, not by texture path. |
| Dropdown pullout | It is a **separate pooled AceGUI object**, acquired in Dropdown `OnAcquire` and released in `OnRelease` (`AGW/AceGUIWidget-DropDown.lua:446-467`), so it shares the dropdown's lifetime. It can be skinned in the same `Apply` (`widget.pullout`). Its items are created per `SetList` and released on `Clear`, so skin them when the pull-out opens. Do not `SetCallback("OnOpen")`, because the Dropdown owns that slot (line 450). Use `hooksecurefunc(pullout, "Open", post)` **once per pullout object**, gated by an ownership check, because the hook outlives the owner. |
| LSM30 pop-up | `AGSMW:GetDropDownFrame()` returns frames from **a cache private to the library** (`SMW/prototypes.lua:202-263`), and `ReturnDropDownFrame` resets the backdrop. To skin it, do so in a post-hook on the widget's `ToggleDrop`/`SetList` and restore it on that widget's close and release. Lowest priority: restyle only the bar (`DLeft/DMiddle/DRight`, `dropButton`). LibKa0s already wraps `LSM30_Border` (`LK/Options.lua:304`), so any new wrapper must chain with it. |
| ColorPicker | The swatch is easy to skin (a border overlay). **`ColorPickerFrame` is a global Blizzard frame** used by Edit Mode and others. Leave it stock: AceGUI already changes its strata each time it opens. If it must be skinned, use external state, alpha only, skin it on open and restore it in `OnHide`. |
| TabGroup tabs | Tabs are reused with their TabGroup and are not separate widgets. Skin them inside the TabGroup's `Apply` (iterate `widget.tabs`), with a `CreateTab` post-hook gated by ownership. LibKa0s pages do not currently use TabGroup. |
| Font leakage | Only Label resets its font on acquire. Heading, CheckBox `text`, Slider `label`, `editbox` and the rest keep whatever font they were given, so a skinned font leaks to the next addon unless it is restored. |

---

## 3. Taint and combat constraints

| Concern | Finding |
|---|---|
| AceGUI frames | These are insecure addon frames, so skinning them taints nothing Blizzard depends on. Texture, alpha, font and color calls on them are allowed in combat. |
| The Settings canvas | Our canvas frame is ours. Do not touch `SettingsPanel` or its children. LibKa0s already parks rendering during combat and draws on `PLAYER_REGEN_ENABLED` (`LK/Options.lua:355-370, 1116`). A live repaint started while the panel is open in combat may restyle textures but must not `SetPoint`, `SetSize`, `SetParent` or `Show` anything Blizzard-owned. Run any re-layout through the existing combat park. |
| Writing keys onto Blizzard frames | Writing a key onto a Blizzard-created table or frame makes that key tainted. If secure code later reads it, the read can cause "action blocked". EUI's rule is "never write custom keys onto Blizzard frames; per-frame state lives in a weak-keyed external table" (`EUI/EllesmereUIBlizzardSkin/EllesmereUIBlizzardSkin_WindowEngine.lua:19-28, 38-45`). Follow it for every Blizzard-template frame we skin, and apply it to AceGUI frames too for uniformity. |
| `SetBackdrop` on templates | On retail, `BackdropTemplateMixin` is Lua (`BLZ/Blizzard_SharedXML/Backdrop.lua:159-439`). `SetBackdrop` creates piece textures and **writes fields** (`backdropInfo`, `Center`, `TopLeftCorner` and so on) onto the frame. That is fine on our own frames but taints a Blizzard frame, and it fails on frames that lack the mixin. For Blizzard templates, add our own child frame (BackdropTemplate) or textures instead, the pattern AddOnSkins calls `CreateBackdrop`. |
| NineSlice re-layout | `NineSliceUtil.ApplyLayout` (`BLZ/Blizzard_SharedXML/NineSlice.lua:160-184`) re-sets atlases and shows pieces again when Blizzard refreshes a frame's layout (PortraitFrameTemplate). Fade each named piece and the container alpha as well, since a re-layout cannot bring back a parent alpha of 0 (EUI `FadeNineSlice`, `...WindowEngine.lua:147-162`). Keep a re-strip registry for frames Blizzard repaints (`...WindowEngine.lua:164-226`). |
| Hide vs alpha | `Hide`, `SetParent` and `EnableMouse` on Blizzard frames can be protected or behavior-changing. Alpha is visual only. EUI uses only `HookScript` and `hooksecurefunc`, never `SetScript`, on Blizzard frames. |
| Method replacement | Assigning `frame.SetTexture = noop` (the ElvUI/AddOnSkins approach) writes a tainted key, cannot be undone cleanly and leaks through the pool. Avoid it. |
| 12.x secret values | EUI guards `fs:GetFont()` results with `issecretvalue` before reuse (`...WindowEngine.lua:443-452`) and wraps every skin pack in `pcall`. Do the same on any read of Blizzard-owned font strings. |
| Forbidden frames | Check `frame:IsForbidden()` before touching any frame that is not ours (EUI does so in every primitive). |

---

## 4. Live repaint engine design

### 4.1 How EUI does it

- **State:** per-frame state lives in `FFD`, a weak-keyed external table (`...WindowEngine.lua:38-45`). `CompleteSetup` separates "done" from "in progress" so a failed setup can be retried (`49-58`).
- **Primitives:** they create overlay textures once, record them in the frame's state entry (`d.bg`, `d.border`, `d.hover`, `d.arrow`, `d.underline`) and are idempotent through that entry (`Checkbox` 564-613, `Dropdown` 616-648, `ScrollBar` 714-740).
- **Registries:**
  - `_restrip[frame]` holds frames to fade again.
  - `_windowRestrips[winKey][frame]` holds the same per window; `WindowCallback` scopes registrations to the window being set up (174-198).
  - `_shells[winKey]` holds window shells.
  - `_skinnedTabs`, `_fillBars` and `_extUnderlines` hold accent-colored elements.
- **Repaint:**
  - `RefreshStyles()` (270-275) swaps shell variants by alpha (`bg` vs `modernBg`) and runs the `OnStylesChanged` callbacks.
  - `RefreshLooks()` (around 1506-1524) recolors underlines and bars from the live accent and runs the `OnLooksChanged` callbacks (`pcall` per callback). It is triggered by `EUI.RegAccent({type="callback"})`.
  - **Only colors and alphas change during a live repaint.** Switching between style families (off and on) requires a reload.
- **Third-party API:** `RegisterSkin(name, fn(S))`, `S.OnLooksChanged(fn)` for custom elements, and a promise that primitives cost "one table lookup" when re-applied (`EUI/EllesmereUI/SKINNING_API.md`).

### 4.2 Proposed engine for LibKa0s

```
state[frame]      (weak-keyed)
  = { owner, prim, skinId, regions = {name -> texture|fontstring},
      saved = {region -> alpha | fontObject | {r,g,b,a}} }
owners[owner]     = setmetatable({}, {__mode="k"})   -- frames currently skinned for this owner
skinOf[owner]     = skinId                           -- the per-addon choice
painters[prim]    = { create(frame, st), paint(frame, st, tokens), restore(frame, st) }
```

- **`Apply(owner, prim, frame)`**:
  1. `create` runs once per frame lifetime.
  2. `saved` captures the stock values.
  3. `paint` applies the tokens for `skinOf[owner]`.
  4. The frame is added to `owners[owner]`.
- **`Release(frame)`**: `restore`, hide the overlays, remove the frame from `owners[st.owner]`, clear `owner`. Keep the `regions` entry so the overlays are reused.
- **`SetSkin(owner, id)`**: resolve the tokens once, then call `paint` for each frame in `owners[owner]`. Other addons' frames are never visited.
- **Primitive families:** use about 10 painters covering Panel/Window, Button, Checkbox/Radio, Slider, EditBox, Dropdown(+Pullout), ScrollBar, Heading, InlineGroup border, Tab and Font. Map AceGUI types and Blizzard templates onto them so that a single `paint` serves AceGUI and template frames.
- **Fonts:** create **one FontObject per owner and role** (for example `LibKa0s_<Addon>_Body`, `_Heading`, `_Small`) with `CreateFont`. Give skinned font strings `SetFontObject(ownerFont)`. Switching skin then means calling `SetFont` and `SetShadow*` on 3-5 FontObjects, and every string that uses them updates. This also satisfies the 12.0.7 shadow rule (§6).
- **Unknown future skins:** primitives paint only from tokens, so adding a skin means adding a token table, not code.

**Cost model.** A full options page is about 50-150 widgets, about 3-6 overlay regions each.

| Step | Cost |
|---|---|
| First `Apply` | about 300-900 `CreateTexture` calls, done once per pooled frame per session |
| Re-acquire | 0 creates and about 10-20 C calls per widget (alphas plus paint) |
| `SetSkin` repaint | about 1-2k `SetColorTexture`/`SetVertexColor`/`SetAlpha` calls, about 1 ms or less, a one-off |
| Steady state | no OnUpdate handlers and no events. Hover uses HIGHLIGHT-layer textures, which cost nothing in Lua. |

Memory is a few hundred textures that stay with the pooled frames. Do not walk `GetRegions()` in a repaint loop; walk only during `create` and `restore`, and do it without allocating (EUI's `FadeTextures(select(...))` pattern, 126-145).

---

## 5. Textures and atlases for a "WoW Default" look; nine-slice options

All of the following are confirmed present on the `live` branch (12.x, commit of 2026-10-23). The legacy file paths go back to vanilla and still ship. I did not verify when each atlas was introduced; the `UI-Frame-Metal` NineSlice family predates Dragonflight. Check classic flavors separately.

| Use | Path / atlas | Ref |
|---|---|---|
| Dialog border / background | `Interface\DialogFrame\UI-DialogBox-Border`, `UI-DialogBox-Background`, `UI-DialogBox-Background-Dark`, `UI-DialogBox-Gold-Border` (`BACKDROP_DIALOG_32_32`, `BACKDROP_DARK_DIALOG_32_32`, `BACKDROP_GOLD_DIALOG_32_32`) | `BLZ/Blizzard_SharedXML/Backdrop.lua:17-51` |
| Tooltip border / background | `Interface\Tooltips\UI-Tooltip-Border` (fileID 137057, also AceGUI Heading), `UI-Tooltip-Background`. Atlas form: `Tooltip-NineSlice-Corner{TopLeft,TopRight,BottomLeft,BottomRight}`, `_Tooltip-NineSlice-EdgeTop/Bottom`, `!Tooltip-NineSlice-EdgeLeft/Right`, `Tooltip-NineSlice-Center` (`TooltipDefaultLayout`, `TooltipDefaultDarkLayout`) | `Backdrop.lua:108`; `.../Mainline/NineSliceLayouts.lua:257-282` |
| Slider | `Interface\Buttons\UI-SliderBar-Background`, `UI-SliderBar-Border` (`BACKDROP_SLIDER_8_8`), thumb `UI-SliderBar-Button-Horizontal`. Modern: `Minimal_SliderBar_Left/Right`, `_Minimal_SliderBar_Middle`, `Minimal_SliderBar_Button`, `Minimal_SliderBar_Button_Left/Right` | `Backdrop.lua:59-61`; `Mainline/SharedUIPanelTemplates.xml:330-341`; `Shared/Slider/MinimalSlider.xml:3-61` |
| Panel button | `Interface\Buttons\UI-Panel-Button-Up/-Down/-Disabled/-Disabled-Down/-Highlight` | `SecureUIPanelTemplates.xml:39-86`; `Mainline/SharedUIPanelTemplates.xml:3, 733-742` |
| Checkbox | `Interface\Buttons\UI-CheckBox-Up/-Down/-Highlight/-Check/-Check-Disabled`; radio `UI-RadioButton`. Modern: `checkbox-minimal`, `checkmark-minimal`, `checkmark-minimal-disabled`; radial `common-dropdown-tickradial`, `common-dropdown-icon-radialtick-yellow` | `Shared/Button/CheckButtonTemplates.xml:4-71` |
| Input box | Live `InputBoxTemplate`: `common-search-border-left/middle/right`. Large: `auctionhouse-ui-inputfield-left/middle/right` | `Shared/InputBox/InputBoxTemplates.xml:13-70` |
| Scroll bar (legacy) | `Interface\Buttons\UI-ScrollBar-Knob`, `UI-ScrollBar-ScrollUpButton-Up/Down/Disabled/Highlight` (and the matching `ScrollDownButton` set) | `SecureScrollTemplates.xml:7-30`; `SecureUIPanelTemplates.xml:10-13` |
| Dropdown (modern) | `common-dropdown-textholder`, `common-dropdown-a-button` (`WowStyle1DropdownTemplate`) | `Blizzard_Menu/Mainline/MenuTemplates.xml:3-15` |
| Tabs (legacy) | `Interface\OptionsFrame\UI-OptionsFrame-ActiveTab` / `-InActiveTab`, `PaperDollInfoFrame\UI-Character-Tab-Highlight` | `AGW/AceGUIContainer-TabGroup.lua:245-286` |
| Metal window frame (PortraitFrameTemplate) | `UI-Frame-PortraitMetal-CornerTopLeft`, `UI-Frame-Metal-CornerTopRight`, `-CornerTopRightDouble`, `-CornerBottomLeft`, `-CornerBottomRight`, `_UI-Frame-Metal-EdgeTop/Bottom`, `!UI-Frame-Metal-EdgeLeft/Right`; no-portrait variant `UI-Frame-Metal-CornerTopLeft` | `Mainline/NineSliceLayouts.lua:17-79` |
| Other metal families | `UI-Frame-SimpleMetal-*` (SimplePanelTemplate), `UI-Frame-GenericMetal-Corner/_EdgeTop/…` (GenericMetal), `UI-Frame-DiamondMetal-*` (`Dialog` layout), inset `UI-Frame-InnerTopLeft`… `_UI-Frame-InnerTopTile`… (InsetFrameTemplate) | `NineSliceLayouts.lua:4-16, 81-91, 145-167` |
| Swatch / checkers | `Interface\ChatFrame\ChatFrameColorSwatch` (130939), `Tileset\Generic\Checkers` (188523) | `AGW/AceGUIWidget-ColorPicker.lua:183, 198` |
| Flat fill | `Interface\Buttons\WHITE8X8` or `ChatFrame\ChatFrameBackground`, or simply `SetColorTexture` | AceGUI Slider `ManualBackdrop` (`AGW/...Slider.lua:207-208`) |

Atlas prefix convention: `_` marks a horizontally tiled piece and `!` a vertically tiled piece. Use `SetAtlas(name, useAtlasSize)` together with `SetHorizTile`/`SetVertTile` as NineSlice does.

**Nine-slice options for our own frames**

| Approach | Notes |
|---|---|
| `BackdropTemplate` + `SetBackdrop{bgFile, edgeFile, edgeSize, tile, tileSize, insets}` | Simplest for "WoW Default": pass `BACKDROP_DIALOG_32_32` or `BACKDROP_TOOLTIP`-style tables directly. The edge file must use the legacy 8-cell strip layout (the original backdrop format). Use it on our frames only (§3). |
| `NineSliceUtil.ApplyLayout(container, layoutTable)` / `ApplyLayoutByName(container, "Dialog")` / `NineSliceUtil.AddLayout(name, tbl)` | Atlas-based, with per-piece `layer`, `subLevel`, offsets and `mirrorLayout` (one corner art flipped four ways), and `DisableSharpening` (`NineSlice.lua:152-234`). The container needs `NineSlicePanelTemplate` or must be a plain frame given the pieces. The cleanest route to the metal frame look; custom atlases are not possible (addons cannot register atlases), so this suits **Blizzard** atlases only. |
| Custom TGA/PNG corners (Glass rounded) | Make 8 or 9 textures yourself: 4 corner textures at a fixed pixel size, 4 edges stretched or tiled with `SetTexCoord`, and a center. Alternatively, a single texture with **`SetTextureSliceMargins(l,t,r,b)` + `SetTextureSliceMode(Enum.UITextureSliceMode.Stretched/Tiled)`**, which the retail client supports natively (since 10.x; confirm on 12.x before relying on it). That draws a nine-slice from one file with one region and recolors with one `SetVertexColor`. Ship power-of-two TGA or PNG (for example 64×64 with an 8-12 px radius) in **white**, and tint per skin. Use `SetSnapToPixelGrid(false)` and `SetTexelSnappingBias(0)` on corners to avoid shimmer at fractional UI scales, which is also why Blizzard disables sharpening. |

---

## 6. Fonts

- **Shipping fonts.**
  - Put the TTF or OTF file inside the addon folder and reference it as `Interface\AddOns\<Folder>\...\X.ttf`.
  - The client only sees files that existed **at client start**, so a new font needs a full restart, not `/reload`.
  - `fs:SetFont(path, size, flags)` returns false if loading fails; fall back to `STANDARD_TEXT_FONT`.
  - Valid flags: `""`, `"OUTLINE"`, `"THICKOUTLINE"`, `"MONOCHROME"`, comma-combined, for example `"OUTLINE, MONOCHROME"`.
  - **The vendoring gotcha.** LibKa0s is vendored per consumer, so the winning LibStub copy must build its media path from **its own** load folder (`local folder = ...` at file scope, recorded when that copy wins the minor race), never from a hard-coded consumer name. If the winning copy's addon is disabled later in the session, its files are still on disk and stay valid.
- **FontObject vs SetFont.**
  - `CreateFont("Name")` and `obj:SetFont(...)` give a shared object. `fs:SetFontObject(obj)` makes the string inherit from it, and later changes to `obj` reach every string that inherits from it. That is the right tool for live repaint (§4.2).
  - Instance `SetFont` overrides only face, size and flags, and must be re-applied per string.
- **The 12.0.7 shadow change.** EUI documents that from 12.0.7 a runtime `FontString:SetShadowOffset/SetShadowColor` **no longer renders**: shadows render only when they come from a FontObject. Their fix:
  1. Keep two shared FontObjects, one with a 1,-1 black shadow and one with none.
  2. Call `SetFontObject(shadowObj)` **first**.
  3. Then call `SetFont` for the face; the inherited shadow survives `SetFont`.

  Sources: `EUI/EllesmereUI/EllesmereUI_Fonts.lua:430-445` and `EUI/EllesmereUIBlizzardSkin/EllesmereUIBlizzardSkin_WindowEngine.lua:447-449`. Per-owner FontObjects that carry their own shadow settings cover this.
- **Restore on release.** Capture `fs:GetFontObject()` before the change and set it back. Of the AceGUI widgets, only Label resets its own font (§1.2).
- **LSM registration.**
  - `LSM:Register("font", key, path, langmask)` (`../AbsorbTracker/libs/LibSharedMedia-3.0/LibSharedMedia-3.0.lua:239`).
  - The registry is process-global and the first registration of a key wins.
  - Use distinctive keys, for example "Ka0s Barlow", so we never shadow another addon's "Barlow" pointing at a different file.
  - Pass `LSM.LOCALE_BIT_western` (128, line 35) for Latin-only faces so ruRU, koKR and zh clients do not list them.
  - Do the registration once, guarded through the library state.
- **Glyph coverage.** Barlow and Inter include Cyrillic. Cinzel and Atkinson Hyperlegible are Latin-only. Ensure a fallback to the client font on koKR, zhCN, zhTW and ruRU.
- **Variable fonts.** I could not verify that WoW honors variable axes. Assume it renders only the default instance and ship **static** instances.

**Sizes** (Google Fonts repository `google/fonts/ofl/*`, from the GitHub API on 2026-10-25)

| Font | File | Bytes |
|---|---|---|
| Barlow | `Barlow-Regular.ttf` / `-Medium` / `-SemiBold` / `-Bold` | 104,068 / 103,536 / 108,348 / 108,220 |
| Barlow Condensed | `BarlowCondensed-Bold.ttf` (Regular is similar) | about 110 KB each. A copy in EllesmereUI is 97,960. |
| Barlow Semi Condensed | `BarlowSemiCondensed-Medium.ttf` (as shipped by StockClerk with its OFL.txt) | 163,992 |
| Cinzel | `Cinzel[wght].ttf`, variable only on Google Fonts; get static instances from github.com/NDISCOVER/Cinzel | 125,468 |
| Cinzel Decorative | `CinzelDecorative-Regular.ttf` / `-Bold` | 60,408 / 62,300 |
| Atkinson Hyperlegible | `AtkinsonHyperlegible-Regular.ttf` / `-Bold` | 54,348 / 55,256 |
| Atkinson Hyperlegible Next | `AtkinsonHyperlegibleNext[wght].ttf` (variable) | 114,552 |
| Inter | `Inter[opsz,wght].ttf`, variable only on Google Fonts | 876,576. Static `Inter-Regular.ttf` from github.com/rsms/inter releases is roughly 300-400 KB (not verified). |

A typical set of four faces with Regular and Bold each comes to about 0.6-0.9 MB with Inter and about 0.5 MB without it.

**OFL 1.1 licensing note.** All four fonts are SIL OFL 1.1. The headers seen in the `OFL.txt` files list no Reserved Font Name for Barlow, Cinzel, Atkinson Hyperlegible or Inter, but check the upstream repositories before modifying or subsetting a font.

- **Bundling:** fonts may be bundled and redistributed with software, including free and commercial addons. Each font's copyright line and the full `OFL.txt` must ship alongside it, for example `media/fonts/<Font>-OFL.txt` (StockClerk does this).
- **Selling:** a font may not be sold on its own.
- **Modified versions:** a modified version (a subset, for instance) must stay under the OFL and must not use any Reserved Font Name.
- **MIT addon:** the MIT license on our addons does not cover the fonts. Add a credits line to the README or DEPENDENCIES.

---

## 7. Summary for the spec

1. **Hook point:** use the acquire sites LibKa0s already owns in `OptionsWidgets`, not `RegisterAsWidget`. Pass the owner explicitly.
2. **Restore:** wrap `widget.OnRelease` per instance (the precedent is `OptionsScroll`). Do not use `SetCallback("OnRelease")`. Restore alphas, FontObjects, colors and recolored backdrops, and hide our overlays.
3. **Visuals:** fade stock art with `SetAlpha(0)` and put state in an external weak table. Draw our own overlay textures, created once per frame and reused. Never use `SetTexture('')`, noop overrides or keys on Blizzard frames.
4. **Repaint:** keep `owners[owner]` weak sets and per-owner FontObjects, and change only colors and alphas. A repaint is about 1 ms per page and has no steady-state cost.
5. **Leave stock:** `ColorPickerFrame`, the LSM30 pop-up list (phase 2) and anything on `SettingsPanel`. Defer to ElvUI or AddOnSkins when they have already skinned a widget.
6. **"WoW Default"** maps onto the Blizzard paths and atlases in §5. "Glass" uses shipped white TGA corners, preferably with `SetTextureSliceMargins`.
