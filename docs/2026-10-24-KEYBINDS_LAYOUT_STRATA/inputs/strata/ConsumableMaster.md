# ConsumableMaster — frame strata analysis

Scope: item 030. Read from `../ConsumableMaster` on 2026-10-24: every `CreateFrame` / `SetFrameStrata` /
`SetFrameLevel` / texture draw layer in `core/`, `modules/`, `settings/`, plus the vendored LibKa0s files that
build frames for this addon (`WidgetsDragHandle.lua`, `DebugLog.lua`, `PerfPanel.lua`, `Widgets.lua`,
`WidgetsReorder.lua`, `OptionsIds.lua`, `Launcher.lua`). Also read: `docs/macro-bar.md` (Buttons layer table
:70-95, indicator level :190).

The addon's on-screen surface is one HUD bar (the macro bar), its per-slot flyouts, and the drag handle. Every
other window is the library's or Blizzard's.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Macro bar `KCMMacroBar` | modules/MacroBar.lua:221-225 | UIParent | **MEDIUM, explicit** | inherited (UIParent + 1) | not toplevel / **clamped** | movable, BackdropTemplate (bar background + border drawn on the bar itself, :363-383). Secure visibility driver :446-447. |
| Unlock wash `bar.moveHint` | modules/MacroBar.lua:238-241 | bar (texture) | bar's | bar's own level, layer OVERLAY | — | 15% gold `SetColorTexture`. As a texture on the bar it draws **under every child button**, so it shows only in padding and spacing gaps. Shown by applyLock :406. |
| Drag handle `KCMMacroBarHandle` | LibKa0s WidgetsDragHandle.lua:653 (spec built at MacroBar.lua:265-332; anchored :334) | bar | inherited MEDIUM | inherited (bar + 1) | not clamped itself; it sits outside the clamped bar's rect, so it can be pushed off-screen at the top edge | Above the bar's top edge (`BOTTOM` to `TOP`, gap `HANDLE_GAP`), so it doesn't overlap the slots. Children: help mark (WidgetsDragHandle.lua:394) and close mark (:447), both at the default child level (handle + 1). Neither sets a level explicitly. |
| Bar slot button `KCMMacroBarButton<i>` | modules/MacroBarButton.lua:389-390 | bar | inherited MEDIUM | inherited (bar + 1) | — | SecureActionButtonTemplate. Textures: `backdropTex` BACKGROUND :401, `icon` ARTWORK :404, pushed + highlight (ADD) :407-410. |
| Slot cooldown | modules/MacroBarButton.lua:412-413 | button | inherited | **inherited, button + 1** (the default for a child) | — | CooldownFrameTemplate swipe over the icon. |
| Slot border | modules/MacroBarButton.lua:419-421 | button | inherited | **explicit relative, button + 2** | — | BackdropTemplate, LSM edge, offset outward by `buttonBorderOffset`. |
| Slot text overlay (count, label) | modules/MacroBarButton.lua:423-434 | button | inherited | **explicit relative, button + 3** | — | Fontstrings at OVERLAY. Outside-placed labels (labelPlacement OUTSIDE) extend past the button. |
| Flyout indicator `KCMMacroBarFlyout<i>Indicator` | modules/MacroBarFlyout.lua:270-309, level set :500 | button | inherited MEDIUM | **explicit relative, button + 1**, set again on every `applyIndicator` | — | SecureHandlerEnterLeaveTemplate. Motion-only mouse. `shade` ARTWORK :305, `arrow` OVERLAY :308. **Same level as the slot cooldown.** |
| Flyout container `KCMMacroBarFlyout<i>` | modules/MacroBarFlyout.lua:248-251, strata :551 | **button** | **DIALOG, explicit**, set on every `FO.Apply` (not at Create) | inherited | not toplevel / **not clamped** | SecureHandlerEnterLeaveTemplate, mouse-enabled. Comment: "above the bar, and above other bars". |
| Flyout panel `flyout.bg` | modules/MacroBarFlyout.lua:262-264 | flyout | inherited DIALOG | **explicit, = flyout's level** | — | BackdropTemplate. Its border uses the *bar's* border settings (:463). |
| Flyout entry `...Entry<n>` | modules/MacroBarFlyout.lua:195-196 | flyout | inherited DIALOG | inherited (flyout + 1) | — | SecureActionButtonTemplate. `backdropTex` BACKGROUND :203, `icon` ARTWORK :206, highlight :209-211. |
| Entry cooldown | modules/MacroBarFlyout.lua:213-214 | entry | inherited | **inherited, entry + 1** | — | |
| Entry text overlay (count) | modules/MacroBarFlyout.lua:216-220 | entry | inherited | **explicit relative, entry + 2** | — | |
| Entry border | modules/MacroBarFlyout.lua:222-223 | entry | inherited | **explicit relative, entry + 1** | — | **Same level as the entry cooldown**, and one below its text. The slot button's order is cooldown < border < text, at +1 / +2 / +3. |
| Game tooltip on slot / entry | core/MacroDisplay.lua:155, :230 (`SetOwner(owner,"ANCHOR_RIGHT")`) | Blizzard GameTooltip | TOOLTIP (Blizzard) | — | — | Gated by `macroBar.tooltips` (slot: MacroBarButton.lua:436-440; entry: MacroBarFlyout.lua:225-229). |
| Game tooltip in the settings lists (item rows, Buttons-tab glyph, Stat Priority glyph) | modules/KCMItemRow.lua:375, settings/MacroBar.lua:870, settings/StatPriority.lua:470 | GameTooltip | TOOLTIP (Blizzard) | — | — | Draws over the HIGH Settings panel. No addon-side strata. Missing from the first inventory. |
| Drag-handle tooltips (strip, ?, X) | modules/MacroBar.lua:190-206 (`MB.PlaceTooltipBeside`) | GameTooltip | TOOLTIP | — | — | Placed beside the strip, owned by the library at `ANCHOR_NONE`. |
| Confirm popups `KCM_CONFIRM_RESET`, `KCM_RESET_PRIORITIES`, `KCM_RESET_CATEGORY` | core/SlashCommands.lua:55, settings/General.lua:146, settings/Category.lua:298 | StaticPopup (Blizzard) | **DIALOG** (Blizzard StaticPopup) | Blizzard | toplevel (Blizzard) | Raised from the settings panel and from `/cm resetall`. |
| Debug console `<name>DebugWindow` | LibKa0s DebugLog.lua:536-539 (via core/DebugLogSetup.lua) | UIParent | **DIALOG, explicit (library)** | inherited; buttons + 1 (:337) | clamped | debug-logging standard mandates DIALOG. Toggled by Master controls > Debug console. |
| Debug copy frame | LibKa0s Widgets.lua:653-656 | UIParent | **FULLSCREEN, explicit (library)** | inherited | clamped | Sits above the DIALOG console that opened it. |
| Perf panel `<name>PerfPanel` | LibKa0s PerfPanel.lua:186-189 (via core/PerfSetup.lua) | UIParent | **DIALOG, explicit (library)** | inherited | clamped | `/cm perf`. |
| Minimap button | LibDBIcon (core/LauncherSetup.lua) | Minimap | LibDBIcon's (MEDIUM) | LibDBIcon's | — | Right-click opens Blizzard `MenuUtil` context menu (Launcher.lua:385-395), which handles its own strata. |
| Settings canvases (General, Macros, Stat Priority, Macro Bar, Profiles) | settings/*.lua `H.CreatePanel` | Blizzard SettingsPanel | inherited (SettingsPanel is HIGH) | library-managed (OptionsTabs.lua:375, :714; Options.lua:589 cover) | Blizzard | All AceGUI. |
| Custom AceGUI widgets `KCMIconButton`, `KCMItemRow`, `KCMMacroDragIcon`, `KCMScoreButton` | modules/KCMIconButton.lua:101, KCMItemRow.lua:311, KCMMacroDragIcon.lua:92, KCMScoreButton.lua:85 | created on UIParent, reparented by AceGUI | inherited from their container once parented | inherited | — | Created on UIParent (MEDIUM) and live only inside the settings panel. |
| Pooled list rows (Buttons tab, Stat Priority) | settings/MacroBar.lua:881-902, settings/StatPriority.lua:450-475 | AceGUI SimpleGroup | inherited | inherited; glyph button child + 1 | — | Hidden attics on UIParent: MacroBar.lua:845, StatPriority.lua:415. |
| Reorder chrome (box, insertion line, carried copy) | LibKa0s WidgetsReorder.lua:601, :255, :107 | row / list ancestor / UIParent | box and line inherited; **ghost TOOLTIP explicit** | box = row − 1, line = + 20 | — | Library-owned; used by Macros, Stat Priority and Buttons lists. |
| Add-by-ID suggestion list | LibKa0s OptionsIds.lua:996-998 | UIParent | **FULLSCREEN_DIALOG, explicit (library)** | inherited | clamped | Above the Settings panel. |
| Bootstrap event frame | settings/Panel.lua:1133 | none | — | — | — | Not visual. |

## Problems

| id | where | problem |
|---|---|---|
| CON-S01 | modules/MacroBarFlyout.lua:551 | **The flyout's DIALOG strata is undocumented beyond a one-line comment.** The goal in the comment ("above the bar, and above other bars") needs only one tier above MEDIUM. At DIALOG the flyout shares a strata with Blizzard's StaticPopups (including this addon's own reset confirmations), the game menu, the debug console and the perf panel, so which one draws on top comes down to frame level. The flyout's level is low (it is a child of a slot button, about bar + 2), and the popups and windows are toplevel or raised, so in practice they win. It also draws **above the Blizzard Settings panel (HIGH)** when its strip crosses it, which can only happen when part of the bar is visible beside the panel. This is a consistency finding, not an observed bug: DIALOG is the *safe* choice for a hover popup, because it is always visible where it opens. |
| CON-S02 | modules/MacroBarFlyout.lua:551 vs :248 | The strata is set on **every `FO.Apply`** (each refresh) rather than once when the frame is built, so the frame's strata between Create and the first Apply is the inherited MEDIUM. It's harmless today (hidden until applied), but it is the only property in the file set per refresh rather than at construction, and it hides the decision inside a layout function. |
| CON-S03 | modules/MacroBarButton.lua:412, modules/MacroBarFlyout.lua:500 | **The flyout indicator band ties with the cooldown swipe at button + 1.** The two are sibling frames at the same level, so their draw order isn't fixed: the swipe may cover the band and arrow during a cooldown, or not. `docs/macro-bar.md:190` documents "+1, above the icon, below the border", but never considers the cooldown, which is also +1. |
| CON-S04 | modules/MacroBarFlyout.lua:213, :216-223 | **Flyout entries use a different level scheme from bar slots.** On entries the border is at +1 (a tie with the cooldown) and the text at +2. On slots it is cooldown +1, border +2, text +3, so the slot's border is guaranteed above the swipe and the entry's is not. Within one addon the same element class (a bordered icon button) layers two ways. |
| CON-S05 | modules/MacroBar.lua:238-241 | **The unlock wash sits under the thing it washes.** `moveHint` is an OVERLAY *texture on the bar frame*, and every slot button is a *child frame*, so the wash draws beneath all buttons. It is visible only in padding and spacing gaps, and invisible on a bar with zero spacing and padding. `docs/macro-bar.md:362` calls it "the gold wash over the bar". |
| CON-S06 | modules/MacroBarButton.lua:419-425, modules/MacroBarFlyout.lua:218, :223, :264, :500 | **Levels are hardcoded offsets scattered over two files** (+1, +2, +3, +1, +2, +0), with no shared table naming the bands. That is how CON-S03 and CON-S04 crept in. |
| CON-S07 | modules/MacroBarFlyout.lua:248-264 | The flyout is **not clamped to screen**, while the bar is (MacroBar.lua:223). A bar docked at a screen edge with *Flyout side* pointing outward opens a flyout partly or fully off-screen. `SetClampedToScreen` is allowed out of combat at construction, and FO.Create already refuses in combat. |
| CON-S08 | modules/MacroBarButton.lua:423-434 vs LibKa0s WidgetsDragHandle.lua:653 | Outside-placed **button labels** (bar + 1 + 3) draw above the **drag handle** (bar + 1) when *Label position* is a top anchor with *Placement: Outside*. The label then overlaps the handle strip while unlocked. This is a minor collision between the bar's own elements, and the handle is the more important of the two while unlocked. |
| CON-S09 | modules/MacroBarFlyout.lua:264 | `flyout.bg` is pinned to the **same level as its parent**. That works only because the container draws nothing itself. If the container ever gains a texture, the two tie. A named band (bg = container + 0, entries = container + 1) would record the intent instead of relying on it. |
| CON-S10 | modules/KCMIconButton.lua:101 and siblings | The custom AceGUI widgets are created on **UIParent** (MEDIUM) and reparented on acquire. That's correct under AceGUI, but a widget acquired and shown before it is parented would flash at MEDIUM behind the HIGH settings panel. Not observed. Noted for the guidance only, no change proposed. |

## Proposed strata map

One HUD tier for the bar, one tier up for its transient popup, and library/Blizzard tiers above that. Level bands
are relative to the owning frame and are named in one table (see CON-Z05).

| tier | strata | element class | level band |
|---|---|---|---|
| HUD | **MEDIUM** (explicit on the bar only; everything else inherits) | bar frame (background + border on the bar itself) | base L (inherited) |
| | | slot buttons, drag handle | L + 1 (default child) |
| | | in-button band, per slot: icon/backdrop | button + 0 |
| | | cooldown swipe | button + 1 |
| | | flyout indicator (band + arrow) | button + 2 |
| | | border | button + 3 |
| | | text overlay (count, label) | button + 4 |
| | | unlock wash (mouse-disabled child frame) | L + 1 + 6, above every slot band, so it truly washes the bar; drag handle raised to the same top band so outside labels never cover it |
| HUD popup | **one tier above the bar, set once at Create**: HIGH if Blizzard's SpellFlyout is HIGH or lower, else DIALOG unchanged (Z01) | flyout container | base F |
| | | flyout panel `bg` | F + 0 |
| | | flyout entries | F + 1, same in-button band as slots: cooldown + 1, border + 3, text + 4 (no indicator) |
| Blizzard window | HIGH | Blizzard Settings panel and its AceGUI canvases | Blizzard-managed |
| Modal / tool windows | DIALOG | StaticPopups (Blizzard), debug console, perf panel (library) | library / Blizzard |
| Above modal | FULLSCREEN / FULLSCREEN_DIALOG | debug copy frame, Add-by-ID suggestion list, library menus | library |
| Cursor | TOOLTIP | GameTooltip, reorder carried copy | library / Blizzard |

The open question for the HUD popup tier is DIALOG (today) versus HIGH versus MEDIUM-with-a-high-level. At HIGH
the flyout shares a strata with the Blizzard Settings panel and the other HIGH windows. Its frame level is low
(a child of a slot button), and the Settings panel is toplevel at a higher level, so where the two overlap the
flyout opens **underneath** the panel. That is an invisible strip the player is hovering, with entries the panel
covers. Under MEDIUM at bar level + 20, a flyout can fall under another addon's MEDIUM bar at a higher level. At
DIALOG it is always visible, and popups and tool windows still win by level. **HIGH is only an improvement if
Blizzard's own action-button flyout (`SpellFlyout`) is HIGH or lower.** Check it in-client
(`/dump SpellFlyout:GetFrameStrata()`). If it is DIALOG, the flyout already matches Blizzard and Z01 should be
dropped (see CON-Z01).

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| CON-Z01 | modules/MacroBarFlyout.lua:551: `flyout:SetFrameStrata("DIALOG")` → `"HIGH"` | One tier above the HUD bar meets the stated goal (above other bars) without sharing DIALOG with StaticPopups, the debug console and the perf panel, and without drawing over the Settings panel's content by default. **Risk:** at HIGH a flyout whose strip crosses the open Settings panel opens *under* it (the flyout's level is low, the panel is toplevel), so the player hovers an indicator and sees nothing. Verify `SpellFlyout:GetFrameStrata()` in-client first; keep DIALOG if Blizzard's flyout uses it. | 45% |
| CON-Z02 | Move that `SetFrameStrata` call from `FO.Apply` (:551) into `FO.Create`, right after the frame is built (:251) | A construction property is set once at construction, so the frame never exists at the wrong strata. Entries created later by `layoutEntries` inherit it from the container. Create already refuses in combat (:241), so the protected-frame write is safe. | 85% |
| CON-Z03 | modules/MacroBarFlyout.lua:500: indicator `button + 1` → `button + 2`. modules/MacroBarButton.lua:421: border `+2` → `+3`. MacroBarButton.lua:425: overlay `+3` → `+4`. Update `docs/macro-bar.md:75-80, :190`. | Fixes the indicator/cooldown tie. The arrow stays readable over a running swipe, and border and text stay on top. | 70% |
| CON-Z04 | modules/MacroBarFlyout.lua:223: entry border `+1` → `+3`. :218: entry overlay `+2` → `+4` (the same values as the slots after Z03) | One layering scheme for every bordered icon button the addon draws, and the entry border clears the swipe. | 85% |
| CON-Z05 | Add one level-band table, e.g. `KCM.MacroBarLayout.LEVEL = { COOLDOWN = 1, INDICATOR = 2, BORDER = 3, OVERLAY = 4, WASH = 6 }` (core/MacroBarLayout.lua, which both files already read), and replace every literal offset in MacroBarButton.lua:419-425, MacroBarFlyout.lua:218/223/500. Cooldowns get an explicit `SetFrameLevel(level + LEVEL.COOLDOWN)` instead of relying on the child default. | Named bands stop the next tie from creeping in, and a test can pin the order (cooldown < indicator < border < overlay) without depending on the mock. | 75% |
| CON-Z06 | modules/MacroBar.lua:238-241: host the unlock wash on a child frame (`CreateFrame("Frame", nil, frame)`, `SetAllPoints`, `EnableMouse(false)`, level = bar level + 1 + `LEVEL.WASH`) instead of a texture on the bar. applyLock (:406) shows and hides that frame. | The wash covers the buttons as documented, so an unlocked bar reads as unlocked even with 0 spacing and 0 padding. Mouse-disabled, so drag-swap and the handle still work. (Owner to confirm the look: a wash over the icons is more visible than the current gap-only tint, and it also tints the labels, counts and borders, which sit below the wash band.) Built in `buildBar`, out of combat. Showing and hiding an unprotected child frame is allowed in combat. | 50% |
| CON-Z07 | modules/MacroBarFlyout.lua:248-251 (`FO.Create`): add `flyout:SetClampedToScreen(true)` | Same clamp policy as the bar, so a flyout opened from a bar at a screen edge stays on screen. Out-of-combat only, which Create already guarantees. Check that the secure hover snippet's `IsUnderMouse` test still holds when clamping shifts the strip away from the button (`flyoutGap` already allows a gap). **Risk:** a clamp can shift the strip back over its own slot button, and while the flyout is open its entries would then swallow clicks meant for the macro under them. | 50% |
| CON-Z08 | modules/MacroBar.lua:~334 (after the handle is built): raise the drag handle to bar level + 1 + `LEVEL.WASH` (or `LEVEL.OVERLAY + 1`) | The handle wins over outside-placed labels while unlocked, which is the only time it shows. **Risk:** the library has already built the help and close marks at handle + 1 by then, and the host would be re-levelling a library widget after construction. If the client does not carry the children up with the parent, the marks draw *under* the strip and vanish. Prefer a `frameLevel` option on LibKa0s `DragHandle` (an upstream change), or verify in-client with `/fstack` before taking the host-side route. | 45% |
| CON-Z09 | modules/MacroBarFlyout.lua:264: keep `bg` at the container's level, and write it as `flyout:GetFrameLevel() + 0` with a `LEVEL.PANEL = 0` entry in the Z05 table | Documents the intent. No visible change. | 50% |

No change proposed for library-owned frames (debug console, perf panel, copy frame, suggestion list, reorder ghost),
StaticPopups, or the settings widgets (CON-S10). Their tiers are already distinct from the addon's after Z01.

## Notes for the upstream guidance

- **One explicit strata per root, everything else inherits.** The bar sets MEDIUM once and nothing under it sets
  a strata. That is the right pattern. The one break (the flyout) is a child that re-strata'd itself
  to escape its parent. The rule could say: a HUD addon picks one strata for its display root, and its
  transient popups (flyouts, menus) go exactly **one tier up**, set **once at construction**, never per refresh.
- **Name the level bands.** An icon button with cooldown, overlay indicator, border and text has a fixed z-order.
  Codify it (icon 0 < cooldown 1 < indicator 2 < border 3 < text 4) as a shared constant, perhaps in
  LibKa0s-Core next to `SKIN`, so KickCD, AuraMaster and ConsumableMaster layer their buttons identically.
  Two schemes in one addon (CON-S04) is the failure this prevents.
- **Never leave a sibling tie for a meaningful order.** Child frames default to parent + 1, so any explicit
  `+1` sibling of a cooldown is a tie. The guidance should say: give the cooldown an explicit level too, and no
  two siblings that overlap share a level.
- **Overlays are frames, not parent textures.** A "wash over the whole display" drawn as a texture on a
  container sits under the container's children. An overlay that must cover children has to be a
  mouse-disabled child frame above their band.
- **DIALOG is for windows and modals, not HUD popups.** The debug console and perf panel are DIALOG by
  debug-logging's rule, and StaticPopups are DIALOG. A HUD flyout at DIALOG competes with all of them.
  Reserve DIALOG for windows the player opens deliberately.
- **Clamp popups the way you clamp their root.** A clamped bar with an unclamped flyout is inconsistent.
- **A popup tier needs a Blizzard reference point.** Pick a HUD popup's strata by what Blizzard's equivalent uses
  (SpellFlyout for action-button flyouts), not by reasoning about which windows it should beat. A HUD popup's
  level is low, so dropping it to the strata of a toplevel window puts it under that window, not beside it.
- **Library-chosen strata are part of the addon's map.** The inventory should list the tiers LibKa0s picks on
  the addon's behalf (DIALOG console, FULLSCREEN copy, FULLSCREEN_DIALOG suggestions, TOOLTIP ghost), so an
  addon's own choices can be checked against them.

## Review

Independent review, 2026-10-24, against `../ConsumableMaster` at `80943b2`, read-only. Every `CreateFrame`,
`SetFrameStrata`, `SetFrameLevel`, `SetToplevel` and `SetClampedToScreen` in `core/`, `modules/` and `settings/`
was grepped and re-read. There is no `SetToplevel` anywhere in the addon, and `core/` creates no frames. What
changed in this file, and why:

- **Inventory.** The drag handle's line references are corrected (spec :265-332, anchor :334). Its marks carry no
  explicit level, and it is not itself clamped. A row is added for the GameTooltips the settings lists raise
  (KCMItemRow.lua:375, MacroBar.lua:870, StatPriority.lua:470), which the first pass missed. The slot and entry
  tooltip gates now cite their lines. Everything else checked out, including the cooldown/indicator tie at
  button + 1, the entry border/cooldown tie, the bar texture wash under its child buttons, the per-Apply DIALOG
  call, and the unclamped flyout.
- **CON-S01 softened.** The flyout's low frame level means StaticPopups and tool windows already win within
  DIALOG. DIALOG drawing over the Settings panel is the safe behaviour for a hover popup, not a defect.
- **CON-Z01 60% -> 45%, with a corrected risk.** The first pass said a HIGH flyout would draw over the Settings
  panel until the panel was clicked. The reverse is true: the flyout's level is low and the panel is toplevel,
  so at HIGH the flyout opens under the panel, invisible. The strata map and the open-question paragraph now
  make Z01 conditional on Blizzard's SpellFlyout strata, which must be checked in-client.
- **CON-Z06 60% -> 50%.** The wash would also tint the labels, counts and borders. The look is the owner's call.
- **CON-Z07 55% -> 50%.** A clamp can push the strip back over its own button, and while open it would then
  swallow that button's clicks.
- **CON-Z08 55% -> 45%.** Re-levelling a library widget after its children are built risks hiding its help and
  close marks. A LibKa0s `DragHandle` `frameLevel` option is the safer route.
- **Z02, Z03, Z04, Z05 and Z09 confirmed.** Nothing in them affects combat-protected frames: every write runs at
  construction or inside `FO.Apply`, both out of combat. Nothing affects dropdowns, menus or the Settings panel.
  The cooldown frame takes no mouse, so moving the indicator above it keeps hover working.
- **Upstream guidance.** One bullet added: choose a HUD popup's strata from Blizzard's equivalent, because a
  low-level popup dropped into a toplevel window's strata ends up under that window.
