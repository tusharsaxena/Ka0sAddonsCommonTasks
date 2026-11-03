# Round 4 investigation (read-only workflow wf_f2e8c9bf-4fb, 2026-11-03)

## dropdown-close

### diagnosis

I read three images. Image 1 is the Skin Tester row. The two that close are "Dropdown (click: MenuFrame)" and "WowStyle1DropdownTemplate". The three that stay open are "AceGUI Dropdown, PaintAce", "Ka0sMedia_Font, PaintAce" and "Ka0sMedia_Statusbar, PaintAce". Images 2 and 3 belong to feedback item 2 and are only referenced for this area.

WHY THE TWO WORKING ONES CLOSE
- The plain "Dropdown" is LibKa0s's own Widgets dropdown, which uses a shared menu singleton. When it opens it registers GLOBAL_MOUSE_DOWN (LibKa0s/LibKa0s/Widgets.lua:544) and drops it on hide (Widgets.lua:486-487). Its handler `menu:__OutsideClick` (Widgets.lua:483-484, 496-501) does nothing if the press is over the menu or over the owning dropdown, and hides the menu otherwise. That is a listener, not a catcher, so the click still reaches what is under it (Widgets.lua:468-482). Tests are at tests/test_widgets.lua:693-745.
- WowStyle1DropdownTemplate uses Blizzard's Menu system, whose own menu manager closes the menu on GLOBAL_MOUSE_DOWN. That is client code, not in any repo.

WHY THE THREE ACEGUI ONES STAY OPEN
- All three are AceGUI-3.0's stock "Dropdown". Ka0sMedia_Font and Ka0sMedia_Statusbar are the stock Dropdown constructor registered under Ka0s type names (LibKa0s/LibKa0s/OptionsMedia.lua:15-21). AuraMaster's AuraMasterDropdown is built the same way (AuraMaster/settings/OptionsSetup.lua:73-104). So all of them share the stock "Dropdown-Pullout" behaviour.
- Stock AceGUI has no outside-click close of its own (vendored copy, for example LibKa0sSkinTester/libs/AceGUI-3.0/widgets/AceGUIWidget-DropDown.lua):
  - The pullout's Open is SetPoint, fixstrata TOOLTIP and Show (182-201), and its Close is Hide (204-207). There is no event, no blocker frame and no Escape handling.
  - The dropdown's button and button_cover OnClick both call Dropdown_TogglePullout (701, 710). On open it calls `AceGUI:SetFocus(self)` (383), and on a second click it closes and calls `AceGUI:ClearFocus()` (375-379).
  - The only other closers are the widget's ClearFocus, which runs pullout:Close (499-503), and Dropdown_OnHide (366-371).
  - Both depend on something calling `AceGUI:ClearFocus()` (AceGUI-3.0.lua:233-248). Only AceGUI's own containers and widgets do that: AceGUIContainer-Frame.lua:33,38,54,59,64 (the Frame container's mouse-down), TreeGroup :190,230, Button :20, and so on.
  - Neither the Blizzard Settings canvas nor the Skin Tester showroom window nor any Ka0s addon window is an AceGUI Frame. A press on their background, or on the world, never reaches ClearFocus, so the pullout stays open.
- LibKa0s's skin layer does not change this. SkinAce hookPullout (LibKa0s/LibKa0s/SkinAce.lua:695-714) post-hooks the pullout's Open, Close and Clear only to paint and restore. It is installed only from PAINT.Dropdown (SkinAce.lua:743-744), so an unpainted dropdown (settings panel with ignorePanel=true) never gets it. OptionsMedia only chains OnOpen (OptionsMedia.lua:347-357).
- The library already closes AceGUI pullouts in two narrow places, both through `AceGUI.FocusedWidget` and ClearFocus:
  - at combat start, for the instance's own pages: `O.__releaseOwnedFocus` (OptionsCombat.lua:243-262)
  - the skin picker's rows: dropFocus (OptionsSkinPicker.lua:519-529)
  Neither runs on a mouse press.

WHERE THESE WIDGETS APPEAR (every one goes through the stock Dropdown_TogglePullout, so one fix at the AceGUI focus seam covers them all)
- Schema "select" rows rendered by LibKa0s: makeDropdown (OptionsWidgets.lua:708-719, 877, 884). It picks Ka0sMedia_* for media rows and Dropdown otherwise, and this covers every addon's settings pages.
- LibKa0s's own rows: OptionsAppearance.lua:648, OptionsSkinPickerRows.lua:154, OptionsTabs.lua:1137.
- Direct AceGUI use in addons:
  - AbsorbTracker settings/UnitPanel.lua:194,223
  - AuraMaster settings/OptionsSetup.lua:102-104
  - BankLedger settings/Panel.lua:55
  - ConsumableMaster settings/CategoryAddByID.lua:73, StatPriority.lua:363, core/SkinSetup.lua:420
  - DropWatcher settings/PageEditors.lua:53,195
  - KickCD settings/Spells.lua:525, Spells_Header.lua:160, Spells_Rows.lua:249
  - LootHistory settings/Panel.lua:38
  - MultiMeters settings/Windows.lua:81
  - PanelMaster settings/PanelEditor.lua:16,540, PanelEditorTabs.lua:16,172,199,356
  - QuickComms settings/IconBrowser.lua:441,448, Groups.lua:140,440,649, Editors.lua:235
  - LibKa0sSkinTester modules/ShowroomControls.lua:85,101,112
- AceConfigDialog Profiles pages (AceDBOptions dropdowns) in AbsorbTracker settings/Profiles.lua:82, AuraMaster settings/Profiles.lua:49 and the other addons' Profiles pages. These come straight from AceGUI, not through O.AceGUI, which is why a fix inside the O.AceGUI proxy or SkinAce would miss them.
- All 16 vendored AceGUIWidget-DropDown.lua copies are the same code. 14 share one md5, and ConsumableMaster and PrettyChat differ only in the `$Id$` header line. AceGUI is minor 41 (AceGUI-3.0.lua:28).

### whereUsed

Every AceGUI Dropdown-family widget in the collection:
- Schema select and media rows on every addon's LibKa0s settings pages (OptionsWidgets.lua:708-719, 877, 884, with Ka0sMedia_* from OptionsMedia.lua).
- LibKa0s's own rows: OptionsAppearance.lua:648, OptionsSkinPickerRows.lua:154, OptionsTabs.lua:1137.
- AceConfigDialog Profiles pages, for example AbsorbTracker settings/Profiles.lua:82 and AuraMaster settings/Profiles.lua:49.
- Direct use in AbsorbTracker, AuraMaster (AuraMasterDropdown), BankLedger, ConsumableMaster, DropWatcher, KickCD, LootHistory, MultiMeters, PanelMaster, QuickComms (including the IconBrowser window) and LibKa0sSkinTester ShowroomControls.lua:85-112.
- All 16 addons vendor LibKa0s and an identical AceGUIWidget-DropDown.lua (widget version 36, AceGUI minor 41).

### proposal

THE FIX: one GLOBAL_MOUSE_DOWN listener at AceGUI's focus seam, in LibKa0s-Options-1.0
Add it to OptionsCombat.lua (263 lines, already home to AceGUI focus release) with a COMBAT minor bump, and call it wherever O.AceGUI is resolved (Options.lua:471 and OptionsRegistry.lua:208).

1. `lib.__armPulloutClose(AceGUI)` is process-wide and idempotent:
   - `if AceGUI and AceGUI.SetFocus ~= lib.__pulloutHooked then hooksecurefunc(AceGUI, "SetFocus", onFocus); lib.__pulloutHooked = AceGUI.SetFocus end`
   - Comparing against the stored wrapper means a later, newer AceGUI minor that redefines SetFocus gets re-hooked the next time any Ka0s addon's lib:New runs. Optionally re-check once on PLAYER_LOGIN.
   - Hooking a plain Lua table has no taint surface. AceGUI is insecure, and SkinAce already hooksecurefuncs AceGUI objects (SkinAce.lua:711-713).
2. `onFocus(_, w)`: if `type(rawget(w,"pullout"))=="table"` and `w.open`, register GLOBAL_MOUSE_DOWN on one shared hidden watcher frame (`lib.__pulloutWatch`, created on first use).
   - Every Dropdown, Ka0sMedia_* and AuraMasterDropdown calls `AceGUI:SetFocus(self)` right after its pullout opens (DropDown.lua:382-383). That covers the one code path all of them share.
   - EditBox and other focus users carry no pullout and are ignored.
3. Watcher OnEvent(GLOBAL_MOUSE_DOWN) reads `local w = AceGUI.FocusedWidget` at call time, not a captured widget:
   - If w is not an open dropdown (`not (w and w.open and w.pullout)`), unregister and return. This is the lazy unregister for a pullout closed by any other route: item pick, toggle, OnHide, combat.
   - If `w.pullout.frame:IsMouseOver()`, return. A press on a row, the scrollbar (the slider sits inside pullout.frame, DropDown.lua:299-330) or the multiselect Close row is not outside.
   - If `w.frame:IsMouseOver()`, return. This covers the owning dropdown's button and button_cover. Same reasoning as Widgets.lua:490-495: closing on the press would let the release's toggle reopen it.
   - Otherwise `pcall(AceGUI.ClearFocus, AceGUI)` and unregister. That runs w:ClearFocus, then pullout:Close, then OnPulloutClose (DropDown.lua:401-405, 499-503), the same path AceGUI's own Frame container uses. The OnClosed callback and SkinAce's Close hook (restorePullout) still fire.
   - The click is never swallowed. A press on a different dropdown closes this pullout, and that dropdown's release opens its own.
4. Combat: the pullout and the watcher are insecure non-protected frames, so Hide and RegisterEvent are fine in lockdown. The press is only listened to, never intercepted.
5. Cost: the event is registered only while a pullout is open, as Widgets.lua:476-480 rules. Outside that window there is one call per SetFocus.
6. Escape is not cheap to do correctly. AceGUI pullouts have no key handling. The options are:
   - a keyboard-propagating frame, which means SetPropagateKeyboardInput in combat
   - a named proxy frame in UISpecialFrames whose OnHide calls ClearFocus. On the Settings canvas the same Escape would also close SettingsPanel, which already closes the pullout through Dropdown_OnHide (DropDown.lua:366-371).
   The LibKa0s MenuFrame also has no Escape close (Widgets.lua:777-794, hosts call CloseMenu). Recommendation: leave Escape out of this item for parity, or add the UISpecialFrames proxy if the owner wants it.
7. Ship: new LibKa0s minor and tag, docs/api Options version doc, and CONSUMERS note. Then run /dev-copilot:wow-revendor-libka0s into all 16 vendoring addons. No addon code changes.

Rejected alternatives:
- Fix it in SkinAce hookPullout. That only reaches painted dropdowns and misses the settings panel under ignorePanel=true.
- Fix it in the O.AceGUI proxy. That misses AceConfigDialog's Profiles dropdowns and addons' raw AceGUI.
- Patch vendored AceGUI. It is a third-party lib in 16 copies.
- A full-screen catcher frame. The library already retired that because it swallows clicks (Widgets.lua:468-472).

### testsAndSmoke

HEADLESS: a new LibKa0s test, tests/test_options_pullout_close.lua.
- Use the real hooksecurefunc helper the skin fixture installs (tests/fixture_skin_ace.lua:405 realHook), because the kit's own is a no-op (tests/_kit/mock_base.lua:376).
- Use kit mock frames with `__mouseOver` and `IsEventRegistered` (mock_base.lua:238), following tests/test_widgets.lua:693-745.
- Build a fake AceGUI table with SetFocus, ClearFocus and FocusedWidget, as test_options_combat.lua:462-480 does, and a fake dropdown `{frame=F, pullout={frame=P, Close=...}, open=true, ClearFocus=...}`.

Cases:
(a) arm, then SetFocus on an open dropdown: GLOBAL_MOUSE_DOWN is registered.
(b) a press with the pullout frame moused over (row or scrollbar): no close, still registered.
(c) a press on the owner frame: no close.
(d) an outside press with any button (Left, Right, Button4): ClearFocus called once and the event unregistered.
(e) SetFocus on a non-dropdown (EditBox-like, no pullout): no registration.
(f) the pullout closed by another route (open=nil or FocusedWidget=nil), then a press: unregisters without calling ClearFocus.
(g) arming twice hooks once.
(h) replacing AceGUI.SetFocus to simulate an upgrade, then re-arming: hooked again.
(i) ClearFocus raising an error: pcall keeps the handler alive.
(j) a second dropdown's SetFocus while the first is open: one registration, and the press reads the current FocusedWidget.

Gate per LibKa0s CLAUDE.md: `ka0s-bounded lua tests/run.lua` plus `ka0s-bounded luacheck .`, with the file cap and CCN no higher than 15. Then the same gate in each re-vendored addon.

IN-CLIENT SMOKE (owner):
1. Skin Tester: open each of the AceGUI Dropdown, Ka0sMedia_Font and Ka0sMedia_Statusbar pickers, click the showroom background. It closes, and the click still lands.
2. Click the world. It closes.
3. Click a row. It picks.
4. Drag the pullout scrollbar on the font picker. It stays open.
5. Click the dropdown's own bar. It toggles closed and does not reopen.
6. With one open, click another dropdown. The first closes and the second opens.
7. Repeat on a settings page with Ignore settings panel ON (unpainted) and OFF, and on a Profiles page's dropdown.
8. Enter combat with one open. It still closes.

### repos

- LibKa0s
- AbsorbTracker
- AuraMaster
- BankLedger
- ConsumableMaster
- DpsRace
- DropWatcher
- KickCD
- LibKa0sSkinTester
- LootHistory
- MultiMeters
- PanelMaster
- PartyFrameEnhanced
- PremadeGroupsFilterExtension
- PrettyChat
- QuickComms
- WhatGroup

### files

- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsCombat.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/Options.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsRegistry.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/Widgets.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinAce.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsMedia.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsWidgets.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsSkinPicker.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/libs/AceGUI-3.0/widgets/AceGUIWidget-DropDown.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/libs/AceGUI-3.0/AceGUI-3.0.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/modules/ShowroomControls.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_widgets.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_options_combat.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/fixture_skin_ace.lua

### ownerQuestions

- Scope: AceGUI is shared by every addon in the client, so this close would also apply to other authors' AceGUI dropdowns (for example WeakAuras options). The library's combat close deliberately limits itself to its own pages (OptionsCombat.lua:243-249). Should an outside click close every AceGUI dropdown in the client, or only those under a Ka0s panel or window? The second option is a smaller change in behaviour but needs a frame-ancestry check, and AceConfigDialog Profiles dropdowns would then have to be matched by panel.
- Escape: should Escape also close an open AceGUI dropdown on its own? On the Settings canvas, Escape already closes the whole panel, which closes the dropdown with it. The LibKa0s Widgets dropdown has no Escape close today either. Adding one means a named UISpecialFrames proxy frame.

### challenge (holds=True)

- Re-hook guard: `AceGUI.SetFocus ~= lib.__pulloutHooked` also trips when a third-party addon (for example an ElvUI-style AceGUI skin) hooksecurefuncs SetFocus after us. The next lib:New would then hook a second time. That is harmless only because onFocus is idempotent (RegisterEvent twice is a no-op), so state that as a requirement. Better still, key the guard on the AceGUI minor (LibStub.minors['AceGUI-3.0']) or on a sentinel field, so ours is not re-hooked on top of someone else's wrapper.
- The pullout frame's strata is FULLSCREEN_DIALOG at construction (DropDown.lua:287) and is raised to TOOLTIP only by fixstrata in Open (198). The report's description is otherwise right. The slider is parented to scrollFrame, not directly to pullout.frame (DropDown.lua:302). Its anchors (TOPRIGHT -16 of a scrollFrame inset 6/12) and its -10 top hit-rect extension still fall inside pullout.frame's bounds, so `pullout.frame:IsMouseOver()` does cover the scrollbar as claimed.
- MISSED: Released-while-open path: a dropdown released or recycled from the pool (page rebuild, schema re-render) while open can leave AceGUI.FocusedWidget pointing at a pooled object. The lazy check `w.open and w.pullout` handles it only if Release/OnRelease clears `open` or closes the pullout first. Add a headless case for FocusedWidget being a released widget, next to case (f).
- MISSED: Dropdown_OnHide (DropDown.lua:366-371) closes the pullout but never clears AceGUI.FocusedWidget. When the host panel hides, the watcher stays registered until the next press, which then lazily unregisters. That is correct, but it is worth an explicit test, since this is the common Settings-close route.
- MISSED: Interaction with the existing narrow closers (O.__releaseOwnedFocus in OptionsCombat.lua:250-262 and OptionsSkinPicker.lua:519-529 dropFocus): both call ClearFocus, which leaves the watcher registered until the next press. That is harmless because of the lazy unregister, but the plan should say so and test it.
- MISSED: The SetFocus hook fires for a pullout whose open path runs during a press: Dropdown_TogglePullout runs on OnClick, which is the release. So the GLOBAL_MOUSE_DOWN that opened it has already fired before registration, and there is no self-close race. The report implies this but should state it, because it is why the scheme works without a frame-delay.

## tester-ignorepanel

### diagnosis

Images 2 and 3 show the three showroom AceGUI samples drawn stock: "AceGUI Dropdown, PaintAce (Scope: panel)", "Ka0sMedia_Font, PaintAce (Scope: panel)" and "Ka0sMedia_Statusbar, PaintAce (Scope: panel)". That is intended under the current default.

Where the default comes from:
- LibKa0sSkinTester/defaults/Profile.lua:15 sets `ignorePanel = true,  -- the Scope: leave this addon's settings pages the client's (default on)`.
- settings/Schema.lua:116-124 reads it in its row: `default = C.skin.ignorePanel`, onChange `NS.ApplySkinIgnore(v, nil)`.
- AceDB is built from the schema-derived defaults at core/LibKa0sSkinTester.lua:69-71.
- `NS.ApplySkinChoice()` with no argument (core/LibKa0sSkinTester.lua:45 and :99) calls `NS.ApplySkinIgnore()`, which reads `storedIgnore()` (core/SkinSetup.lua:113-117) and passes it to `Skin:SetIgnore` (core/SkinSetup.lua:219-225).
- LibKa0s itself holds no default. Skin.lua:543-576 only stores what the host hands it, and `__PanelSkinned` (Skin.lua:574-576) returns `not o.ignorePanel`.

Why the samples stay stock: SkinAce.lua minor 3 (LibKa0s/LibKa0s/SkinAce.lua:63-65) paints nothing through PaintAce while the owner ignores its panel. The samples go through plain `PaintAce`: modules/ShowroomControls.lua:82-89 and :105-117, plus the TreeGroup at modules/ShowroomOwner.lua:69-89. So flipping the tester's default is enough, with no code change, as the owner asked. It also flips the fourth "(Scope: panel)" sample, the Addon surfaces TreeGroup, so all four stay consistent.

The standard has a rule against this. WowAddonStandards/standards/standards/skinning.md (standard v2.97.0, STANDARDS.md:1):
- skinning-§3, line 48: "*Ignore settings panel* ... It **defaults to on** in every profile (owner ruling of 2026-10-30)." §3 is a MUST section (line 42).
- skinning-§9, line 139: "*Ignore settings panel* stays on by default (§3), and no flip, default or migration writes `skin.ignorePanel` or `skin.ignoreFonts`." §9 is a MUST (line 128).

So the change is a deviation and must be ratified. The tester's CLAUDE.md:13-20 says a deviation goes as a row in docs/ARCHITECTURE.md under `## Documented deviations` (line 121), shaped `| Rule | What differs | Why | Decided | Re-check trigger |`. Two rows exist there today (options-ui-§1, slash-commands-§7). audit-review-history.md:81-94 makes that register the only ratification an audit accepts.

No migration is needed. The owner's SavedVariables (/mnt/g/Games/Blizzard/World of Warcraft/_retail_/WTF/Account/ADD1KTED2KA0S/SavedVariables/LibKa0sSkinTester.lua) hold one profile, "Default", used by all 8 characters. Its `skin` table is just `{ pickerSeen = true }`. No `ignorePanel` key is stored: AceDB strips values equal to the default at logout (core/Database.lua:5-7). The new default therefore backfills on the next load and the owner sees it without a reset. A migration would also break skinning-§9's "no ... migration writes skin.ignorePanel", so writing none is correct. SCHEMA_VERSION stays at 2 (core/Database.lua:9).

Tests pinned to the old default (`T.enableAddon` uses the real defaults, tests/test_showroom_dropdowns.lua:32-41):
- tests/test_settings.lua:759 pins `skin.ignorePanel = bool|true|...`.
- tests/test_showroom_dropdowns.lua:89 asserts "stock while the Scope leaves the panel the client's (the default)".
- tests/test_showroom_owner.lua:142 asserts the same for the TreeGroup.
- tests/test_selector.lua:73-85 sets ignorePanel explicitly in its fixture, so it is unaffected.
- tests/test_settings_sample.lua:105-109 still passes (it sets the value to false), but its comment at :106 goes stale.
- The kit (tests/_kit) has no ignorePanel assertion.

Risk to note: per skinning-§3 line 46, "Copy to every Ka0s addon…" carries the Scope. If the tester's Skin tab copy is used, it pushes ignorePanel=false to every loaded addon. A copy from another addon into the tester writes true, and that stored value then overrides the new default.

Alternative, not proposed because the owner said no code changes: LibKa0s already has `Skin:__PaintAceWindow` (SkinAce.lua:66-69, minor 5) for AceGUI widgets a window holds. Calling it would paint the showroom samples under the Scope with no deviation. It would also remove the captions' purpose of showing the "Scope: panel" behaviour.

### whereUsed

There are four showroom samples captioned "(Scope: panel)":
- modules/ShowroomControls.lua:82 (AceGUI Dropdown)
- modules/ShowroomControls.lua:105, which builds both media pickers: Ka0sMedia_Font and Ka0sMedia_Statusbar
- modules/ShowroomOwner.lua:69 (TreeGroup)

All are repainted on every OnLooksChanged (ShowroomControls.lua:253, ShowroomOwner.lua:154). The same default also governs the tester's own settings pages, including the Sample controls page (settings/Profiles.lua:79 PaintAceTree, docs/settings-panel.md:29-31). tests/skin_surfaces.lua:26-29 leaves these four samples out of the kit's surface census as AceGUI stubs, so nothing changes there.

### proposal

All edits are in LibKa0sSkinTester on feat/2026-11-01-full-skinning, plus one ledger row. No LibKa0s or standard change, and no migration.

1. defaults/Profile.lua:15:
   `ignorePanel = true,  -- the Scope: leave this addon's settings pages the client's (default on)`
   becomes
   `ignorePanel = false, -- the Scope: OFF here, so the showroom's AceGUI samples and the settings pages wear the skin (accepted deviation from skinning-§3/§9, docs/ARCHITECTURE.md)`

2. docs/ARCHITECTURE.md, `## Documented deviations` table (after line 128), add:
   `| skinning-§3, skinning-§9 | **Ignore settings panel defaults to off** (`skin.ignorePanel = false`, defaults/Profile.lua). The standard has it on in every profile, so a settings panel stays stock until the player clears it. No migration writes it; a profile that stored true keeps it. | The tester is the skin showroom: its AceGUI Dropdown, Ka0sMedia_Font and Ka0sMedia_Statusbar samples and the TreeGroup go through PaintAce, which paints nothing while the panel is ignored, so by default they hid the very skin they exist to show. Owner ruling of 2026-11-03 (smoke round 4, item 2): "for the skin tester addon ONLY, set ignore settings panel = off - treat this as an accepted deviation". | 2026-11-03 | The standard letting a showroom/developer addon default the Scope off, or the showroom's AceGUI samples moving to a window paint (Skin:__PaintAceWindow), which ends the need |`

3. Tests, turned the other way round:
   - tests/test_settings.lua:759 becomes `"skin.ignorePanel = bool|false|nil|nil|nil|skin|false",`.
   - tests/test_showroom_dropdowns.lua:83-94 asserts `owned(mock, w)` at open ("painted by default: the tester's Scope leaves the panel skinned"), then `NS.ApplySkinIgnore(true, nil)` and asserts not owned ("handed back while the panel is ignored"), then `ApplySkinIgnore(false, nil)` and asserts owned again.
   - tests/test_showroom_dropdowns.lua:96-109: the pickers should be owned without the leading `ApplySkinIgnore(false, nil)`. Keep the hand-back step.
   - tests/test_showroom_owner.lua:137-149 gets the same inversion for the TreeGroup (`Skin.__ace[sec.tree].owner == OWNER` at open).
   - tests/test_settings_sample.lua:106-109: fix the comment. The `set skin.ignorePanel false` line becomes a no-op and can be dropped or kept as explicit.
   - Optionally add a red-under test that a fresh profile's `Skin:GetIgnore(OWNER)` returns false, false.

4. Doc ripple, replacing "a new profile has it on" with "off in this addon, a documented deviation":
   - docs/schema.md:18: the default column `true` becomes `false`.
   - docs/scope.md:31-33.
   - docs/settings-panel.md:29-31.
   - docs/smoke-tests.md:75-76 (PANEL-5: drop the untick step) and :81-84 (PANEL-6: "a fresh profile shows Ignore settings panel unticked and Ignore fonts unticked; the settings pages and the showroom wear the skin. Tick it → the settings pages and the four (Scope: panel) samples go back to the client's look at once"). Add a smoke check for item 2: open the showroom on the owner's existing profile with no reset; the three dropdowns in images 2 and 3 draw skinned under every skin.
   - The header comments in modules/ShowroomControls.lua:12-14 and modules/ShowroomOwner.lua:9-12 say "stock while the Scope leaves the panel the client's (the default)". Change "(the default)" to "(off by default in this addon)". These are comment-only edits.

5. Gate: `lua tests/run.lua` via /home/tushar/.claude/dev-copilot/bin/ka0s-bounded, plus `ka0s-bounded luacheck .`. Commit subject carries the round-4 item id.

### testsAndSmoke

Not run: this was a read-only step and nothing was edited.

Tests that will need inverting once the default flips:
- tests/test_settings.lua:759
- tests/test_showroom_dropdowns.lua:89 (and the flow at :90-93 and :102-108)
- tests/test_showroom_owner.lua:142 (and :143-148)

Smoke (the owner runs it):
- With no profile reset, open /st (the showroom). The three dropdowns in images 2 and 3, and the TreeGroup, draw skinned in Ka0s Default, Obsidian and Glass.
- General -> Skin shows Ignore settings panel unticked. Ticking it returns those four samples and the settings pages to stock live, and unticking skins them again.
- Other addons are unchanged: their Ignore settings panel is still ticked by default.

### repos

- LibKa0sSkinTester

### files

- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/defaults/Profile.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/settings/Schema.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/core/SkinSetup.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/core/Database.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/modules/ShowroomControls.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/modules/ShowroomOwner.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/docs/ARCHITECTURE.md
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/docs/schema.md
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/docs/scope.md
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/docs/settings-panel.md
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/docs/smoke-tests.md
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/tests/test_settings.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/tests/test_showroom_dropdowns.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/tests/test_showroom_owner.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/tests/test_settings_sample.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/Skin.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinAce.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/WowAddonStandards/standards/standards/skinning.md

### ownerQuestions

- Should the tester's Skin-tab 'Copy to every Ka0s addon...' keep carrying the Scope? With the tester defaulting ignorePanel off, one copy from the tester would turn Ignore settings panel off in every loaded addon. Choose between leaving it (it is the library's behaviour, skinning-§3) and remembering to copy from another addon.

### challenge (holds=True)

- The SavedVariables claim is out of date. The owner's file (/mnt/g/Games/Blizzard/World of Warcraft/_retail_/WTF/Account/ADD1KTED2KA0S/SavedVariables/LibKa0sSkinTester.lua, written 2026-11-03 11:28, seven minutes after the feedback screenshots at 11:21) holds profiles.Default.skin = { pickerSeen = true, ignorePanel = false }, not just { pickerSeen = true }. The owner has already unticked the box by hand since taking images 2 and 3. The conclusion still holds: no migration is needed. Once the default becomes false, AceDB strips that stored false at logout as equal to the default. The smoke check 'no reset' passes either way, but it does not prove the new default backfills on this profile, because the profile stores the value explicitly.
- Every other file:line claim checks out: defaults/Profile.lua:15, settings/Schema.lua:116-124, core/LibKa0sSkinTester.lua:45/69-71/99, core/SkinSetup.lua:113-117 and 219-225, core/Database.lua:5-9, LibKa0s Skin.lua:543-576 (GetIgnore/SetIgnore/__PanelSkinned), SkinAce.lua:63-69 (minor 3 and minor 5 __PaintAceWindow), skinning.md §3 line 48 and §9 line 139 (standard v2.97.0), the tester's CLAUDE.md deviation procedure, the ARCHITECTURE.md register with its two existing rows, and the tests at test_settings.lua:759, test_showroom_dropdowns.lua:89-108 and test_showroom_owner.lua:142-148.
- MISSED: The doc ripple list leaves out README.md:28. It says 'A new profile keeps the tester's own settings pages in the game's look, so untick Ignore settings panel on the Skin tab before you judge a skin there', which goes stale once the default flips.
- MISSED: There are more stale smoke steps in docs/smoke-tests.md than :75-84. These steps all tell the owner to 'untick/clear Ignore settings panel' as if it starts ticked: :102-107 (tooltip check), :119, :133, :139 (PANEL-15), :155, :284-287 (TreeGroup sample), :332-334, :373 (the three AceGUI dropdowns, which describes exactly item 2's 'client's stock look' default), and :534 PICKER-22. Each needs rewording, or the untick step becomes a no-op.
- MISSED: docs/data-flow.md:16-18 and docs/profiles.md:9 mention the Scope. Check them for 'default on' wording; data-flow's `/st set skin.ignorePanel false` example becomes a no-op on a fresh profile.
- MISSED: settings/Schema.lua:122's tooltip says 'Keep this addon's settings panel in the game's own look. The showroom still wears the skin.' It is already partly inaccurate, because the showroom's four '(Scope: panel)' PaintAce samples go stock while the box is ticked. Consider amending it alongside the change.
- MISSED: The proposal could not show that only the three named test files depend on the old default. Other suites run under the real defaults through T.enableAddon (e.g. tests/test_profiles.lua, test_settings_sample.lua and test_panel.lua, which paint settings pages through PaintAceTree). They may assume settings pages are stock by default, so run the full bounded suite after the flip rather than editing only the listed asserts. The kit's skin_switch.lua:292 saves and restores GetIgnore per surface, so it is default-agnostic.

## misaligned-element

### diagnosis

WHAT IT IS. Images 4-7 show the AceGUI "TreeGroup" sample in LibKa0sSkinTester's showroom, in the "Addon surfaces" section, in the cell captioned "TreeGroup via PaintAce (Scope: panel)". The tree is hard-coded as General (with child Skin), Strings, About, which matches the screenshots exactly: LibKa0sSkinTester/modules/ShowroomOwner.lua:68-90, with the tree at :73-77. It is not a real settings page of any addon. The left box is the TreeGroup's tree pane (treeframe) and the right box is its content pane ("border"). AceGUI-3.0/widgets/AceGUIContainer-TreeGroup.lua:641-643 and :685-686 build them as two BackdropTemplate frames sharing the widget's full height.

WHERE IT IS USED (the owner's question). In the whole collection, only two places acquire an AceGUI TreeGroup:
(1) This showroom sample, LibKa0sSkinTester/modules/ShowroomOwner.lua:72.
(2) PrettyChat's per-category string editor, PrettyChat/settings/Panel.lua:528. This is the real one: the string list on the left and the selected string's editor on the right.
No addon uses AceConfigDialog childGroups="tree" (a grep over every collection repo outside libs/tests/docs found nothing). LibKa0s's own settings nav rail only imitates the TreeGroup look and is not a TreeGroup (LibKa0s/LibKa0s/OptionsNav.lua:12-14). LibKa0s paints TreeGroups in PAINT.TreeGroup (LibKa0s/LibKa0s/SkinAce.lua:635), and in practice that serves PrettyChat. The sample exists to show that painter.

WHY IT IS BROKEN. This is a geometry bug in the sample, not a skin bug. That is why it looks the same in every skin and with Ignore settings panel both ON (4, 5: stock tooltip-edged boxes) and OFF (6, 7: painted nav.bg/nav.border boxes). Both boxes are only about 20 units tall: about 24 px at the capture's roughly 1.2 scale, against the intended 120. Meanwhile the row buttons, drawn during an earlier refresh, spill out below them. The chain:
- ShowroomOwner.lua:83 calls tree:SetHeight(120).
- That resizes the content frame, and AceGUI's ContentResize (AceGUI-3.0.lua:497-503, hooked at :518) runs DoLayout.
- The container keeps AceGUI's default "List" layout (AceGUI-3.0.lua:521). Its content holds no children, so the layout reports height 0 (AceGUI-3.0.lua:651).
- TreeGroup:LayoutFinished then runs `if self.noAutoHeight then return end; self:SetHeight((height or 0) + 20)` (AceGUIContainer-TreeGroup.lua:613-616) and collapses the widget to 20.
- The tree pane is anchored TOPLEFT+BOTTOMLEFT (:641-642) and the content pane TOPLEFT->tree TOPRIGHT, BOTTOMRIGHT (:685-686), so both boxes shrink to a 20-unit strip at the top.
- The tree's row buttons are anchored from the treeframe top (:481-489, :538-543) and are not clipped, so General/Skin/Strings/About hang below the boxes. That is the "misaligned" look.

PrettyChat hit exactly this bug and fixed it with tree:SetAutoAdjustHeight(false) (PrettyChat/settings/Panel.lua:529-541; its comment quotes the same LayoutFinished lines). The showroom sample never got that line. The real surface (PrettyChat) is therefore not affected. Only the SkinTester's demonstration of it is.

### whereUsed

The element in the screenshots is LibKa0sSkinTester's showroom sample only (modules/ShowroomOwner.lua:68-90, section "Addon surfaces", caption "TreeGroup via PaintAce (Scope: panel)"). The only real AceGUI TreeGroup in the collection is PrettyChat's category string list plus editor (PrettyChat/settings/Panel.lua:528). It already sets SetAutoAdjustHeight(false) at :541 and so does not collapse. No addon uses AceConfigDialog tree groups. LibKa0s's settings nav rail (OptionsNav.lua) only imitates the TreeGroup look. LibKa0s's PAINT.TreeGroup painter (SkinAce.lua:635) serves PrettyChat and this sample.

### proposal

Fix the sample in LibKa0sSkinTester. LibKa0s and AceGUI need no change.
1. In LibKa0sSkinTester/modules/ShowroomOwner.lua treeGroup(), add `if type(tree.SetAutoAdjustHeight) == "function" then tree:SetAutoAdjustHeight(false) end` right after AceGUI:Create("TreeGroup") (line 72), before SetTree, SetTreeWidth and SetHeight(120). This is the same one-line fix PrettyChat carries at settings/Panel.lua:541. The host then owns the height, and both panes stay 120 tall with the rows inside the tree pane.
2. Optional but recommended, so the right pane does not read as an empty broken box: give it content the way PrettyChat does. Call tree:SetLayout("Fill") and add one AceGUI Label child, e.g. "The General page", so the content pane shows something. The label is acquired through the same AceGUI, so PaintAce/PaintAceTree also paints it under the panel Scope.
3. Add a regression test in LibKa0sSkinTester/tests/test_showroom_owner.lua. It asserts the sample sets noAutoHeight (or calls SetAutoAdjustHeight(false)) before SetHeight, or it drives a LayoutFinished(nil, 0) on the built tree and asserts the height is still 120. It must be red without the fix.
4. Add a smoke line for the owner: open /st showroom, Addon surfaces, and check that the TreeGroup's two boxes are 120 tall with all four rows inside the left box, under every skin, with Ignore settings panel ON and OFF. Feedback item 2 flips the tester's ignorePanel default to off, so the painted case becomes the default view.
Also worth stating in the smoke file: PrettyChat's category string editor is the only live TreeGroup, and it already guards against this collapse.

### testsAndSmoke

Test: in LibKa0sSkinTester/tests/test_showroom_owner.lua, build the Addon surfaces section, fire the tree's LayoutFinished(nil, 0) (what List layout reports for empty content), and assert the tree height is still 120 (noAutoHeight true). It must be red before the fix. Gate: lua tests/run.lua and ka0s-bounded luacheck . in LibKa0sSkinTester. Smoke (owner, in-client): /st showroom, Addon surfaces, TreeGroup cell. Both boxes are full height (120) with General/Skin/Strings/About inside the left box, under each skin, with Ignore settings panel ON and OFF. Spot-check PrettyChat's category page (unchanged, already guarded).

### repos

- LibKa0sSkinTester

### files

- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/modules/ShowroomOwner.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/libs/AceGUI-3.0/widgets/AceGUIContainer-TreeGroup.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/libs/AceGUI-3.0/AceGUI-3.0.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/PrettyChat/settings/Panel.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinAce.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsNav.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/tests/test_showroom_owner.lua

### ownerQuestions

- Should the TreeGroup sample's right-hand pane show placeholder content (for example a label 'The General page') so it reads like a real settings page, or stay an empty content box once its height is fixed?

### challenge (holds=True)

- The proposed regression test works only in its first form. The kit's AceGUI is a stub with no widget parts (tests/skin_surfaces.lua:17, tests/_kit/mock_base.lua). It has no LayoutFinished and does not model the collapse to 20 units, so 'fire LayoutFinished(nil, 0) and assert the height is still 120' cannot run headless. The stub does record the call: SetAutoAdjustHeight(v) sets self.autoAdjustHeight (mock_base.lua:511). The test should therefore assert sec.tree.autoAdjustHeight == false, not noAutoHeight == true. That test goes red without the fix, because the field is nil until the sample calls the method.
- Small point: the stub has SetAutoAdjustHeight, so the proposed type() guard does not stop the headless assertion. The guard is fine, but the real AceGUI TreeGroup in libs always has the method, so the guard adds nothing.
- MISSED: The existing test 'addon surfaces: the TreeGroup follows the Scope's settings-panel half, live' (LibKa0sSkinTester/tests/test_showroom_owner.lua:137) is the natural place for the new assertion, or for a sibling test next to it. tests/skin_surfaces.lua:29 marks this sample ACE_STUB, so the geometry fix can only be checked by the owner's smoke test, never headless. The smoke line is the real proof.
- MISSED: Confirmed in the code: every central claim checks out. ShowroomOwner.lua:68-90 (Create at :72, the tree at :73-77, SetHeight(120) at :83, no SetAutoAdjustHeight). TreeGroup LayoutFinished at :613-616. treeframe TOPLEFT/BOTTOMLEFT at :641-642, border at :685-686. ContentResize at AceGUI-3.0.lua:497-503 and its hook at :518. The default List layout at :521. List's LayoutFinished(nil, height) at :651. PrettyChat's guard at settings/Panel.lua:541. A grep finds Create("TreeGroup") or childGroups="tree" outside libs/tests/docs only in ShowroomOwner.lua and PrettyChat/settings/Panel.lua. Images 4 and 6 show the 20-unit strips with the rows hanging below them, as described.

## skin-headers

### diagnosis

What the images show. In image 8 (Ka0s Default) the title band reads as the same near-black as the body. In images 9 (Azeroth) and 10 (Ember) the band is a distinct warm tone with a colored title.

Why Ka0s Default's header disappears:
- `title.bg` is black at 0.9 (SkinDefs.lua:487). The SF-L4 note at SkinDefs.lua:183-184 says it was moved there so the header would stand off the content.
- The window is `win.bg` {0.06,0.06,0.08,0.92} (SkinDefs.lua:340), which is #0F0F14 and already about the darkest a fill can be. Composited over black, the body is #0E0E12 and the band is #010102. That is 6.5% apart in a channel, so it passes the SF-L4 floor of 5% (tests/test_skin_defs.lua:736-748), but on screen it is black against near-black.
- The Showroom paints `title.bg` twice. S.Shell draws the top band at SkinPaint.lua:967-970, and S.TitleBar fills the bar's backdrop (SkinPaintExtras.lua:67,121; called from Showroom.lua:289-290). At alpha 0.9 the two layers stack to about 0.99 black.
- Every other skin does better in one of two ways. Six draw a header lighter than the body: Obsidian, Glass, High Contrast, Ember, WoW Default, WoW Midnight. Azeroth and WoW Forever go darker, but from a warm body light enough for the black band to show (#2B1D12 to #1A110A; #231C14 to #050505).

How a header is drawn, so a header change is a token change:
- Band fill: `title.bg`, or a vertical gradient when `title.bgTop` and `title.bgBottom` are both set (P.fill, SkinPaint.lua:398-416). It is drawn by:
  - S.Shell's top band: a BACKGROUND -5 texture inset by the border, `title.height` 30 tall (SkinPaint.lua:966-970). It is skipped under `opts.noTopBar`.
  - S.TitleBar: the bar's backdrop fill, or a region under its text. A gradient clears the flat fill and draws boxGradient (P.box, SkinPaint.lua:775-789; SkinPaintExtras.lua:67,113-128).
- Title text: `title.text` (tint, SkinPaintExtras.lua:126), the `font.title` face and `font.titleSize` (P.font 'title', SkinPaintExtras.lua:127; SkinPaint.lua:1050), and `title.align` (justify, SkinPaintExtras.lua:128).
- Window edge: `win.border`, `win.borderSize` and `win.borderStyle`, plus `win.inner` 1px inside it, drawn on the edge holder above the children (shellEdges, SkinPaint.lua:912-928).
- `divider` reaches only a window that has a `frame.divider` texture, through Core.ApplySkin's accents (SkinPaint.lua:882; Core.lua:118-121). The Showroom has none, so there is no line under its header.
- `title.rule` is the settings page header's rule only (OptionsScroll.lua:410). It is not the window's.
- Close button: `close.rest` and `close.hot` (SkinPaintControls.lua:750-795).
- So recoloring Ka0s Default's header means editing `title.bg` (and optionally `title.bgTop`/`title.bgBottom`) in the KA0S table at SkinDefs.lua:487. No paint code changes. It reaches every window using S.Shell or S.TitleBar: SkinSetup in all 16 addons, plus BankLedger, LootHistory, DropWatcher, MultiMeters, PGFE and QuickComms windows, and the Showroom.

Test constraints a new value must meet:
- tests/test_skin_defs.lua:736-748: the band, composited, must be at least 0.05 from the window in some channel. `divider` must be at least 0.10 from both the window and the band.
- Ka0s Default's divider is EDGE {0.24,0.24,0.27,0.85} (SkinDefs.lua:345), #36363D composited. That caps an opaque grey band at about #1E1E22. #2A2A30 or #232328 fail the rule check (0.052 and 0.084).
- Raising `divider` instead would break tests/test_skin.lua:207 (`divider` must equal Core.SKIN.divider, Core.lua:110) unless Core.SKIN moves too.
- Yellow bands pass easily because their blue channel sits far from the grey rule.
- tests/test_skin_paint.lua:135,480,497 read the token, not a literal, so they do not pin the value.
- Making the band opaque (alpha 1) also removes the double-paint darkening in the Showroom.

Per-skin resolved tokens: Ka0s Default merged with each skin, `false` dropped. I produced them by loading SkinDefs.lua and SkinDefsOthers.lua under a stub LibStub in lua5.1. Hex values; @a is alpha; 'grad a>b' is a vertical top-to-bottom gradient whose flat token is the blend.

```
{
 "ka0s": {"label":"Ka0s Default","src":"SkinDefs.lua:327-503","win.bg":"#0F0F14@0.92","win.border":"#000000 1px flat","win.inner":"#3D3D45@0.85","title.bg":"#000000@0.90","title.text":"#FFD100","title.align":"CENTER","title.height":30,"divider":"#3D3D45@0.85","foot.bg":"#0A0A0D@0.90","close.rest":"#B3B3B8","close.hot":"#FF4D4D","font.body/title":"Ka0s Prototype 12/14 OUTLINE","text.body":"#E6E6E6","text.muted":"#B3B3B8","text.heading":"#FFD100","text.accent":"#FFD100","btn.bg":"#1A1A1F@0.90","btn.border":"#3D3D45@0.90 1px flat","btn.text":"#FFFFFF","btn.hover":"#FFD100","btnPrimary.bg":"#332908@0.95","btnPrimary.border":"#FFD100@0.80","btnPrimary.text":"#FFD100","tab.bg":"grad #262626@.85>#1A1A1A@.85","tab.text":"#B3B3B8","tab.onBg":"#2E2E2E@0.90","tab.onText":"#FFD100","tab.onLine":"#FFD100","tab.border":"none","nav.selBg":"#4D80FF","list.header.bg":"#FFFFFF@0.04","list.header.text":"#FFD100","list.stripe":"#FFFFFF@0.03","list.hover":"#FFD100@0.10","list.sel":"#FFD100@0.18","input.bg":"#1A1A1F@0.90","input.border":"#3D3D45@0.90 1px flat","input.text":"#E6E6E6","input.placeholder":"#808080","input.focus":"#FFD100@0.90","dropdown":{"box":"input.*","arrow(icon.arrow)":"#FFD100","menu.bg":"#0F0F14@0.98","menu.border":"#000000","menu.hover":"#FFD100@0.15","menu.textSel":"#FFD100"},"check":"bg #1A1A1F@.9 border #3D3D45@.9 mark #FFD100","slider":"track #3D3D45@.9 fill #FFD100 thumb #E6E6E6","scroll":"track #3D3D45@.4 thumb #80808C@.85","bar":"Ka0s Default tex, fill #338CF2, bg #000000@.5, border None","icon.border":"#000000 Solid 1px","glow":"#FFD100"},
 "obsidian": {"label":"Obsidian","src":"SkinDefsOthers.lua:390-429","win.bg":"#0A0A0B","win.border":"#202024 1px flat","win.inner":"none","title.bg":"#1E1E22","title.text":"#2A86D1","title.align":"CENTER","divider":"#4A4A54","foot.bg":"#050506","close.rest":"#9B9BA4","font":"Ka0s Expressway 12/14.5","text.body":"#E8E8EC","text.muted":"#9B9BA4","text.heading":"#F2F2F4","text.accent":"#4DB8FF","btn.bg":"#141416","btn.border":"#2A2A30 1px","btn.text":"#E8E8EC","btn.hover":"#4DB8FF","btnPrimary":"bg #2A86D1 border #4DB8FF text #FFFFFF","tab":"bg clear, text #9B9BA4, on: bg clear text #F2F2F4 line #4DB8FF","nav.selBg":"#FFFFFF@0.06 bar #4DB8FF","list.header":"bg #101012 text #4DB8FF","list.stripe":"#FFFFFF@0.09","list.sel":"#4DB8FF@0.14","input":"bg #040405 border #26262B 1px text #E8E8EC ph #8A8A93 focus #4DB8FF","dropdown":"arrow #4DB8FF, menu #0A0A0B / #2C2C32, hover #4DB8FF@.15","check":"#040405 / #34343B / #4DB8FF","slider":"#202024 / #4DB8FF / #F2F2F4","scroll":"#1C1C20 / #4DB8FF@.9","bar":"Ka0s Matte, fill #4DB8FF, bg #141416@.8","icon.border":"#34343B Solid 1px","glow":"#4DB8FF"},
 "azeroth": {"label":"Azeroth","src":"SkinDefsOthers.lua:439-476","win.bg":"#2B1D12","win.border":"#6B4A22 1px flat","win.inner":"#8A6A36","title.bg":"#1A110A","title.text":"#F5C542","divider":"#6B4A22","foot.bg":"#1A110A","close.rest":"#F5C542","close.hot":"#FF6B4A","font":"Ka0s Open Sans Semibold 11 / Bold 12","text.body":"#E9DDBC","text.muted":"#B8A07A","text.heading":"#E2B659","text.accent":"#E2B659","btn.bg":"grad #5A3D1D>#3A2614","btn.border":"#24160A 1px","btn.text":"#F2E3BD","btn.hover":"#FFFFFF","btnPrimary":"grad #A3241A>#5E1009, border #E2B659, text #FFD866","tab":"bg #3A2614 text #CDB78A border #24160A; on bg #7A1A10 text #FFD866","nav.selBg":"#7A1A10","list.header":"bg #3A2614 text #E2B659","list.stripe":"#E9DDBC@0.11","list.sel":"#A3241A@0.35","input":"bg #1C130B border #6B4A22 text #E9DDBC ph #8E7A58 focus #E2B659","dropdown":"arrow #E2B659, menu #2B1D12 / #6B4A22 2px","check":"#1C130B / #8A6A36 / #E2B659","slider":"#5A3D1D / #C0392B / #E2B659","scroll":"#000000@.35 / #8A6A36","bar":"Ka0s Parchment, fill #C0392B, bg #1A110A@.8, border #6B4A22 Solid 1","icon.border":"#8A6A36 Solid 1px","glow":"#E2B659"},
 "glass": {"label":"Glass","src":"SkinDefsOthers.lua:484-529","win.bg":"#121622@0.88","win.border":"#FFFFFF@0.18 8px nine:Ka0s Glass (radius 8)","title.bg":"#FFFFFF@0.10","title.text":"#FFFFFF","divider":"#FFFFFF@0.22","foot.bg":"#FFFFFF@0.04","close.rest":"#C9CFDB","font":"Ka0s Avant Garde 11/13","text.body":"#F2F4F8","text.muted":"#C9CFDB","text.heading":"#FFFFFF","text.accent":"#B69CFF","btn.bg":"#FFFFFF@0.08","btn.border":"#FFFFFF@0.22 1px","btn.text":"#F2F4F8","btn.hover":"#B69CFF","btnPrimary":"bg #B69CFF border #B69CFF text #1A1033","tab":"bg clear text #C9CFDB; on bg #B69CFF@.10 text #FFFFFF line #B69CFF","nav.selBg":"#FFFFFF@0.12","list.header":"bg #FFFFFF@.06 text #B69CFF","list.stripe":"#FFFFFF@0.09","list.sel":"#B69CFF@0.24","input":"bg #000000@.30 border #FFFFFF@.18 text #F2F4F8 ph #B8BFCC focus #B69CFF","dropdown":"arrow #B69CFF, menu #121622@.92 nine:Ka0s Glass","check":"#000000@.3 / #FFFFFF@.3 / #B69CFF","slider":"#FFFFFF@.15 / #B69CFF / #FFFFFF","scroll":"#FFFFFF@.08 / #FFFFFF@.5","bar":"Ka0s Glass Bar (gloss), fill #B69CFF, bg #FFFFFF@.08","icon.border":"#FFFFFF@0.18 Solid 1px","glow":"#B69CFF"},
 "contrast": {"label":"High Contrast","src":"SkinDefsOthers.lua:536-583","win.bg":"#000000","win.border":"#FFFFFF 1px flat","title.bg":"#1F1F1F","title.text":"#FFE600","divider":"#FFFFFF","foot.bg":"#000000","close.rest":"#FFFFFF","close.hot":"#FF5050","font":"Ka0s Doris PP 10.5/12.5","text.body":"#FFFFFF","text.muted":"#E0E0E0","text.heading":"#FFE600","text.accent":"#FFE600","btn":"bg #000000 border #FFFFFF 1px text #FFFFFF hover #FFE600","btnPrimary":"bg #000000 border #FFE600 text #FFE600","tab":"bg #000000 text #FFFFFF border #FFFFFF; on text #FFE600 line #FFE600","nav.selBg":"#FFE600 (text #000000)","list.header":"bg #1A1A1A text #FFE600","list.stripe":"#222222","list.sel":"#000000 outline #FFE600","input":"bg #000000 border #FFFFFF text #FFFFFF ph #D0D0D0 focus #FFE600","dropdown":"arrow #FFE600, menu #000000 / #FFE600, hover #FFE600@.25","check":"#000000 / #FFFFFF / #FFE600","slider":"#FFFFFF / #FFE600 / #FFFFFF","scroll":"#262626 / #FFFFFF","bar":"Ka0s Solid, fill #FFE600, bg #1A1A1A@.85, border #FFFFFF Solid 1","icon.border":"#E0E0E0 Solid 1px","glow":"#FFE600"},
 "ember": {"label":"Ember","src":"SkinDefsOthers.lua:587-629","win.bg":"#1A0E0A@0.95","win.border":"#6A2E17 1px flat","win.inner":"#C98A3A@0.45","title.bg":"grad #3A1A0F>#24100A (blend #2F150D)","title.text":"#FFB45A","divider":"#6A2E17","foot.bg":"#000000@0.30","close.rest":"#C7A993","font":"Ka0s Emblem 11/12.5","text.body":"#F4E7DC","text.muted":"#C7A993","text.heading":"#FFB45A","text.accent":"#FF7A33","btn":"grad #4A2012>#2A120A border #8A3C1C text #FFCF9A hover #FF7A33","btnPrimary":"grad #E0662A>#A63D12 border #FF9A5A text #FFFFFF","tab":"bg #2A140C text #C7A993 border #5A2A16; on bg #4A2012 text #FFB45A line #FF7A33","nav.selBg":"#FF7A33@0.20 bar #FF7A33","list.header":"bg #FF7A33@.08 text #FFB45A","list.stripe":"#FFFFFF@0.09","list.sel":"#FF7A33@0.18","input":"bg #140A07 border #5A2A16 text #F4E7DC ph #A88A76 focus #FF7A33","dropdown":"arrow #FF7A33, menu #1A0E0A@.97 / #8A3C1C","check":"#140A07 / #8A3C1C / #FF7A33","slider":"#4A2416 / #FF7A33 / #FFCF9A","scroll":"#2E1810 / #FF7A33@.9","bar":"Ka0s Forge, fill #FF7A33, bg #140A07@.8","icon.border":"#6A2E17 Solid 1px","glow":"#FF7A33"},
 "wow": {"label":"WoW Default","src":"SkinDefsOthers.lua:643-692","win.bg":"#1E1C19 + tiled UI-DialogBox-Background-Dark","win.border":"#FFFFFF 32px nine:Blizzard Dialog","title.bg":"grad #4B4B4B>#252525 (blend #383838)","title.text":"#FFD100","divider":"#6E6E6E","foot.bg":"#000000@0.30","close.rest":"#D9D9D9","font":"Ka0s Ubuntu 12/13.5","text.body":"#FFFFFF","text.muted":"#B8B8B8","text.heading":"#FFD100","text.accent":"#FFD100","btn":"grad #B3200F>#640C05 border #1A0805 text #FFD100 hover #FFFFFF","btnPrimary":"grad #D42A16>#7E1007 border #E0B040 text #FFFFFF","tab":"UI-OptionsFrame-ActiveTab art, text #C9B048; on text #FFFFFF","nav.selBg":"#5A78DC@0.38","list.header":"bg #FFFFFF@.07 text #FFD100","list.stripe":"#FFFFFF@0.09","list.sel":"#FFD100@0.18","input":"bg #000000 border #7A7A7A bevelIn text #FFFFFF ph #9A9A9A focus #FFD100","dropdown":"arrow #FFD100, menu #1E1C19 nine:Blizzard Dialog 16","check":"UI-CheckBox-Up/-Check art (fallback #111111 / #FFD100)","slider":"#3A3A3A / #C9A24A / #C9A84A","scroll":"#000000 / #FFD100@.9","bar":"Blizzard, fill #C9A24A, bg #1E1C19@.7, border Blizzard Tooltip 2","icon.border":"#9A9A9A Solid 1px","glow":"#E0B040"},
 "midnight": {"label":"WoW Midnight","src":"SkinDefsOthers.lua:700-743","win.bg":"grad #171A2E>#0F1020","win.border":"#B08A3E 2px flat","win.inner":"#3D2F12","title.bg":"grad #2A2347>#17142B (blend #211C39)","title.text":"#F6D27A","divider":"#4A3D1E","foot.bg":"#000000@0.30","close.rest":"#F6D27A","font":"Ka0s Segoe UI Semibold 11.5 / Bold 13","text.body":"#F2EEF8","text.muted":"#B4AFC8","text.heading":"#F6D27A","text.accent":"#B48CFF","btn":"grad #3A2F6B>#1D1838 border #B08A3E text #F6D27A hover #FFFFFF","btnPrimary":"grad #7A5AD6>#3F2C86 border #F6D27A text #FFFFFF","tab":"bg #1A1730 text #B4AFC8 border #5A4A26; on bg #2C2550 text #F6D27A line #B48CFF","nav.selBg":"#B48CFF@0.25 bar #B48CFF","list.header":"bg #B48CFF@.08 text #F6D27A","list.stripe":"#FFFFFF@0.09","list.sel":"#B48CFF@0.20","input":"bg #08091A border #5A4A26 text #F2EEF8 ph #9A95B0 focus #B48CFF","dropdown":"arrow #B48CFF, menu grad / #B08A3E 2px","check":"#08091A / #B08A3E / #F6D27A","slider":"#2C2550 / #B48CFF / #F6D27A","scroll":"#22224A / #F6D27A@.9","bar":"Ka0s Satin, fill #B48CFF, bg #08091A@.8, border #B08A3E Solid 1","icon.border":"#5A4A26 Solid 1px","glow":"#B48CFF"},
 "forever": {"label":"WoW Forever","src":"SkinDefsOthers.lua:751-790","win.bg":"grad #2E251C>#18120D","win.border":"#3A3530 1px flat","title.bg":"#050505","title.text":"#FFFFFF","divider":"#48433D","foot.bg":"#050505","close.rest":"#FFFFFF","font":"Ka0s Fira Sans Medium 12 / SemiBold 13.5","text.body":"#FFFFFF","text.muted":"#A39E97","text.heading":"#F2B33D","text.accent":"#C9A07A","btn":"bg #1F1D1B border #48433D text #FFFFFF hover #C9A07A","btnPrimary":"bg #9C7A58 border #C9A07A text #FFFFFF","tab":"bg clear text #A39E97; on bg #000000@.4 text #FFFFFF line #C9A07A","nav.selBg":"#FFFFFF@0.07 bar #C9A07A","list.header":"bg #000000@.35 text #C9A07A","list.stripe":"#FFFFFF@0.10","list.sel":"#C9A07A@0.16","input":"bg #0A0908 border #3E3934 text #FFFFFF ph #8F8A83 focus #C9A07A","dropdown":"arrow #C9A07A, menu grad / #3A3530","check":"#0A0908 / #8A7A52 / #C9A07A","slider":"#3A3632 / #C9A07A / #C9A07A","scroll":"#0A0806 / #C9A07A","bar":"Ka0s Classic, fill #C9A07A, bg #0A0908@.8","icon.border":"#3A3530 Solid 1px","glow":"#C9A07A"}
}
```

Header against body, composited over black (band / body / channel gap / direction / title contrast ratio):

| Skin | Band | Body | Gap | Direction | Title CR |
|---|---|---|---|---|---|
| ka0s | #010102 | #0E0E12 | .065 | darker | 14.3 |
| obsidian | #1E1E22 | #0A0A0B | .090 | lighter | 4.3 |
| azeroth | #1A110A | #2B1D12 | .067 | darker | 11.5 |
| glass | #282B34 | #10131E | .094 | lighter | 14.2 |
| contrast | #1F1F1F | #000000 | .122 | lighter | 13.0 |
| ember | #2F150D | #190D0A | .087 | lighter | 9.7 |
| wow | #383838 | #1E1C19 | .122 | lighter | 8.0 |
| midnight | #211C39 | #131527 | .071 | lighter | 11.2 |
| forever | #050505 | #231C14 | .118 | darker | 20.4 |

### whereUsed

`title.bg`, `title.bgTop` and `title.bgBottom` are read by:
- S.Shell's top band (SkinPaint.lua:966-970)
- S.TitleBar (SkinPaintExtras.lua:67,113-128)
- the Shell `top` slot remap (SkinPaint.lua:994)
- SkinEUI flattening of the gradient pair (SkinEUI.lua:113)

TitleBar and Shell are reached from:
- every addon's core/SkinSetup.lua (AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, DpsRace, DropWatcher, KickCD, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PGFE, PrettyChat, QuickComms, LibKa0sSkinTester)
- BankLedger Browser/Export/SessionWindow, LootHistory Browser/Export, DropWatcher Window/WindowTitleBar, MultiMeters Export_Modal, PGFE Panel and QuickComms ModalWindow
- the Showroom (Showroom.lua:289-290)
- Core.ApplySkin's owner path (Core.lua:229)

The settings panel's page header uses `title.text` and `title.rule`, not `title.bg` (OptionsScroll.lua:384,410), so the header change does not touch the panel.

### proposal

Make Ka0s Default's band opaque and lighter than its body: one token edit at SkinDefs.lua:487. It needs no paint code change. Swatch 2 (#000000, SkinDefs.lua:510) can stay as the window edge, or become the new header color.

Candidates. Each is composited over the window and checked against the test_skin_defs.lua:736 rules. CR is gold #FFD100 title against the band.

1. **Dark yellow (recommended): #2B2306, opaque.**
   - Gap .113 from the body (#0E0E12); rule gap .217; CR 10.7. Passes.
   - It is an olive-gold band that ties to the gold title and primary button without competing with them. It is clearly distinct at a glance, about 1.7x Obsidian's gap.
   - Gradient variant, Ember/Midnight style: `title.bgTop` #3A2F0A, `title.bgBottom` #1F1905, with `title.bg` set to the blend #2C2408 (needed for the test and for any flat reader). Gap .119; passes.
2. **Stronger dark yellow: #332908, opaque.**
   - This is Ka0s Default's own `btnPrimary.bg` (0.2,0.16,0.03; SkinDefs.lua:370), so it is already on the palette.
   - Gap .145; CR 9.8. Passes.
   - Trade-off: a primary button sitting in a title bar would share the band's fill. Only its gold edge would still separate it.
3. **Grey, like Obsidian: #1E1E22, opaque (Obsidian's exact `title.bg`, SkinDefsOthers.lua:395).**
   - Gap .062; rule gap .107; CR 11.4. Passes, just barely.
   - This is the lightest grey the current `divider` (#3D3D45@.85, which composites to #36363D) allows. #232328 and #2A2A30 fail the rule check (.084 and .052).
   - A clearer grey, #2A2A30 (gap .115, CR 9.8), would also need a brighter `divider`, for example #55555F (rule gap .184). That in turn has to move Core.SKIN.divider (Core.lua:110), because tests/test_skin.lua:207 pins them equal. It would also brighten every Core.ApplySkin divider and the Widgets menu rule (Widgets.lua:446).

Optional extra separation: only through the settings-page `title.rule`, or a `frame.divider` texture on a window. The Showroom header has no rule today.

UX mockup inputs: the per-skin JSON in `data` holds every value the mockup needs. Mockup the header as a 30px band (`title.height`) inside the window edge, with a centered title in `font.title`/`titleSize` and the close glyph at the right in `close.rest`. Under it, show the body with:
- a button and a primary button,
- a tab strip (idle and selected),
- an input or dropdown with its `icon.arrow`,
- a table header plus a striped and a selected row,
- a checkbox and slider, a statusbar, and an icon with its border.

For each, use the listed tokens. Composite the alpha values over a dark world (about #1A1A2A), since the windows sit over the game. Draw Ka0s Default four times: today's band plus candidates 1, 2 and 3, so the owner can pick side by side. The 2026-10-25 page at LibKa0s/docs/skins/skins-mockup.html predates every retune and has an empty `classic` entry (line 54). Use it for layout only, not values.

### testsAndSmoke

Nothing was run under the test kit. I resolved the tokens by loading the two SkinDefs files under a stub LibStub (scratchpad dump.lua), and I computed the contrast figures in a Python copy of test_skin_defs.lua's over/apart/contrast helpers.

After the change:
- Run `ka0s-bounded lua tests/run.lua` in LibKa0s. test_skin_defs.lua:736 (band gap of at least .05, rule gap of at least .10) is the gate. Changing `divider` would also hit test_skin.lua:207.
- Consider tightening test_skin_defs.lua:744 for ka0s, for example requiring the band to be lighter than the body or at least .10 apart, so a near-black band cannot pass again.
- Owner smoke: open /skintester under Ka0s Default and compare the header with images 8 to 10. Also check one addon window, such as Loot History or Drop Watcher, which paint S.Shell plus S.TitleBar.

### repos

- LibKa0s
- LibKa0sSkinTester

### files

- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinDefs.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinDefsOthers.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaint.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaintExtras.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/Core.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_skin_defs.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_skin.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_skin_paint.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/docs/skins/skins-mockup.html
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/modules/Showroom.lua

### ownerQuestions

- Ka0s Default header: dark yellow #2B2306 (recommended), the stronger #332908 (equal to the primary button fill), or Obsidian's grey #1E1E22? A clearer grey such as #2A2A30 also means brightening Ka0s Default's divider (and Core.SKIN.divider) to about #55555F, which changes every Ka0s Default divider and menu rule. Accept that?
- Flat band or a subtle vertical gradient (e.g. #3A2F0A to #1F1905), as Ember, WoW Default and WoW Midnight draw?
- Should the Ka0s Default picker swatch (#000000, second of four) change to the new header color?

### challenge (holds=True)

- Several SkinDefs.lua line citations are wrong on the current branch head (fd57b83), although the values they cite are correct. Ka0s Default's `title.bg` {0,0,0,0.9} is at SkinDefs.lua:477, not 487. `win.bg` is at :318, not 340. `divider` = EDGE is at :321, with EDGE defined at :295, not 345. `btnPrimary.bg` is at :356, not 370. The SF-L4 note is at :190, not 183-184; lines 183-184 are a minor-25 note. The swatches line, :510, is correct.
- The double paint is specific to the Showroom, not general. The collection's convention is that a window whose title bar paints its own fill calls S.Shell with `{ noTopBar = true }`. BankLedger Browser/Export/SessionWindow, LootHistory Browser:1121, DropWatcher Window.lua:560 and WhatGroup FrameSkin all do this. DropWatcher test_skin_host.lua:247 and WhatGroup test_frame_skin.lua:280 pin it. The Showroom breaks the convention: it calls `R.Paint("Shell", f)` with no opts and then TitleBar on a bar that overlaps the band (Showroom.lua:289-290, bar anchored TOP and TITLE_H tall). So the suggested smoke check of LootHistory or DropWatcher 'which paint S.Shell plus S.TitleBar' compares against windows that paint the band only once.
- Because of that double paint, a skin with a translucent band looks different in the Showroom than its tokens say. Glass's `title.bg` is white at 0.10, but the Showroom draws it at about 0.19. A mockup built from the raw tokens will therefore not match what the owner sees in /skintester for Glass, or for Ka0s Default today. The real fix is to pass `noTopBar` in Showroom.lua, independent of the color choice. 'Make the band opaque' only hides the problem for Ka0s Default.
- MISSED: MultiMeters pins Ka0s Default's `title.bg`. MultiMeters/core/SkinSetup.lua:167 carries `["title.bg"] = {0,0,0,0.9}` in NS.SKIN_FALLBACK, and MultiMeters/tests/test_skinsetup.lua:335-350 requires every fallback entry to equal the live library's Ka0s Default value. Changing `title.bg` in LibKa0s turns MultiMeters' suite red after re-vendoring unless the fallback copy changes in the same sweep.
- MISSED: The change reaches beyond window title bars. MultiMeters' meter window header strip (Window_Header.lua:222-226, 446-455) draws `title.bg` with a flat SetColorTexture while `header.bgColorFromSkin` is on, so the in-combat meter HUD header would turn olive or grey under Ka0s Default. It also ignores `title.bgTop`/`title.bgBottom`, so the gradient variant needs a sensible flat `title.bg`, and that applies to MultiMeters too. The owner should be told before signing off.
- MISSED: WhatGroup is a roster addon and reads `title.bg` through modules/FrameSkin.lua (TitleBar plus a noTopBar Shell). It is missing from the whereUsed list. Its test tests/test_frame_skin.lua:280 and DropWatcher's tests/test_skin_host.lua:247 cover `title.bg` layering, so they belong in the post-change test run.
- MISSED: QuickComms `qc.bandBg` follows `title.bg` (QuickComms/core/SkinSetup.lua:153), but its Ka0s Default default is clear, so the Ka0s Default change does not reach the QuickComms pad headers. Worth stating so the owner does not expect it to.
- MISSED: The EllesmereUI source path (SkinEUI.lua:101 Shell `noTopBar`, :113 flattening) is not a registered skin, but the mockup roster should say whether 'eui' is shown. The old docs/skins/skins-mockup.html CARDS list includes it.

## icon-borders

### diagnosis

ROOT CAUSE: the drawing code works. The problem is the color token. S.IconBorder (LibKa0s/LibKa0s/SkinPaintControls.lua:923-934) calls drawIconEdge (:885-893). That draws a flat edge one physical pixel wide (P.px, SkinPaintExtras.lua:437-445) in P.edgeColor(T, "icon.border") (SkinPaintExtras.lua:517-522), and zooms the icon 0.07 (:902-913). Every skin goes through the same 1 px path, so the only per-skin input is the `icon.border` color. Two places set it:
- Ka0s Default: SkinDefs.lua:497, `["icon.border"] = { 0, 0, 0, 1 }`, pure black.
- The other skins: HUD_LOOK[key].icon in SkinDefsOthers.lua:289-305, copied into `icon.border` by register() at :373-375.

The outline sits between the window background (outside) and the icon art, whose own field is near-black (INV_Misc_QuestionMark, and most spell icons after the 0.07 zoom). It is only visible if it is lighter than both.

PIXEL EVIDENCE (sampled from the screenshots):
- img 19, Ka0s Default: outline pixels are 000000, the background is 04010f and the art field is 000000. Black on black, so it cannot be seen.
- img 20, Glass: outline 242424, background 0b0c22. That is white at 0.18 alpha over a translucent navy window. Barely there.
- img 21, Obsidian: outline 2b2b33, against 000000 on both sides. Visible, because Obsidian's window (#0A0A0B) and the art are both true black.

CURRENT icon.border PER SKIN (WCAG contrast of the composited edge against the window background, then against the black art field):
- Ka0s Default: 0,0,0,1 on win 0.06,0.06,0.08,0.92. 1.09 / 1.00. INVISIBLE.
- Obsidian: #34343b on #0A0A0B. 1.60 / 1.70. Visible (the owner's reference).
- Azeroth: #8a6a36 on #2B1D12. 3.26 / 4.20. Visible.
- Glass: white at 0.18 (GLASS_EDGE, SkinDefsOthers.lua:278, shared with Glass's window border at :488) on rgba(18,22,34,0.88). About 1.7 / 1.96 in theory, but in game the window is translucent over the world and it reads 242424 on 0b0c22. FAINT.
- High Contrast: #E0E0E0 on #000000. 15.9. Visible.
- Ember: #6a2e17 on rgba(26,14,10,0.95). 1.83 / 2.02. Weak. Not in the owner's screenshots, but the same risk.
- WoW Default: #9a9a9a on #1e1c19. 6.0 / 7.5. Visible.
- WoW Midnight: #5a4a26 on #171a2e. 2.0 / 2.4. Visible but dim.
- WoW Forever: FV_EDGE #3a3530 (shared with its window border, :756) on #2e251c. 1.24 against the background. NEARLY INVISIBLE outside the icon.

So Ka0s Default fails outright, Glass is faint, Forever is barely visible against its background, Ember is borderline and the rest are fine.

TOKEN IS SHARED (this makes it a product choice): `icon.border` is also the HUD icon edge color in every host that follows the skin:
- AuraMaster/modules/Style_Border.lua:202,209
- KickCD/modules/IconGrid_Render.lua:831 and Castbar_Skin.lua:105
- DropWatcher/modules/IconStyle.lua:125
- QuickComms/modules/IconStyle.lua:115
- DpsRace/modules/Results_Gear.lua:78

Over the bright game world, Ka0s Default's black HUD edge is visible and is the established Ka0s look. LibKa0s tests pin it:
- tests/test_skin_icon_border.lua:62 (`"0,0,0,1"`)
- tests/test_skin_host_gaps.lua:34, whose comment says "red under: Ka0s Default's look moving with the others"

IMAGE 22, THE DUPLICATE: the tester has three IconBorder call sites:
1. modules/ShowroomControls.lua:196-205, "SquareIcon (crop) + IconBorder"
2. modules/ShowroomOverlays.lua:150-157, "IconBorder, fromSkin", stored as body.framed. This is the TOP one in img 22, beside "ApplyBarFill", which is the next sample at :159.
3. modules/ShowroomOwner.lua:92-100, iconBorder(), "IconBorder, fromSkin", wired at :145 as `body.iconFrame = iconBorder(g, paint)`.

The third is the BOTTOM one in img 22. It is the next grid cell after cautionCallout (:57-66), whose title is "Waiting for the pull" (:59). It is the duplicate to remove; the Overlays one stays.

### whereUsed

S.IconBorder with fromSkin is called in LibKa0sSkinTester at:
- ShowroomControls.lua:205
- ShowroomOverlays.lua:156
- ShowroomOwner.lua:98 (the duplicate)

The `icon.border` token is also read directly as the HUD icon edge color by:
- AuraMaster/modules/Style_Border.lua:202,209
- KickCD/modules/IconGrid_Render.lua:831 and Castbar_Skin.lua:105
- DropWatcher/modules/IconStyle.lua:125
- QuickComms/modules/IconStyle.lua:115
- DpsRace/modules/Results_Gear.lua:78
- ConsumableMaster/DpsRace/QuickComms core/SkinSetup.lua (follow lists)

Changing a skin's `icon.border` under option A changes those HUD edges in that skin. P.edgeColor also serves FadeNineSlice's ring (SkinPaintExtras.lua:517), with a different first token, so that is unaffected.

### proposal

A. ICON BORDER COLORS (LibKa0s; the owner must choose the scope, see ownerQuestions). Proposed values were checked to be at least as visible as Obsidian's, which measures 1.6 against its background:
- Ka0s Default: {0,0,0,1} to #4d4d57, about {0.30,0.30,0.34,1}. Contrast about 2.3 against the background and 2.5 against the art. This is Ka0s Default's EDGE grey (SkinDefs.lua:295, #3d3d45) lifted one step, the same tone as Obsidian. Edit SkinDefs.lua:497 and its comment at :433-435.
- Glass: white at 0.18 to rgba(255,255,255,0.35), contrast about 3.2 / 3.6. Edit HUD_LOOK.glass.icon at SkinDefsOthers.lua:292 to a new literal. Do NOT change GLASS_EDGE, because Glass's window border uses it at :488.
- WoW Forever: #3a3530 to #5a5048, contrast 1.9 / 2.7. Edit HUD_LOOK.forever.icon at :303 to a literal, leaving FV_EDGE alone because the window border uses it at :756.
- Ember: #6a2e17 to #8a3c1c (its own bar.border), contrast 2.5 / 2.7. Edit :297.
- Optionally, WoW Midnight: #5a4a26 to #7a6532, contrast 3.0 / 3.7. Edit :301.
- Keep unchanged: Obsidian #34343b, Azeroth #8a6a36, High Contrast #E0E0E0, WoW Default #9a9a9a.

No change is needed to the 1 px or zoom code (SkinPaintControls.lua:885-913). Add a LibKa0s test asserting that, in every skin, `icon.border`'s luminance contrast is at least about 1.6 against `win.bg` composited over black, and at least about 1.6 against black. That replaces the black pin at tests/test_skin_icon_border.lua:62. Also update tests/test_skin_host_gaps.lua:34 if Ka0s Default changes.

If the owner wants Ka0s Default's HUD edge to stay black, use option B instead: a new token `icon.outline`, read first by drawIconEdge (`P.edgeColor(T, "icon.outline")` with `icon.border` as the fallback, SkinPaintControls.lua:887). It would take the values above, while `icon.border` and the HUD hosts stay as they are. Option A is simpler and stays consistent with Obsidian, which already draws grey HUD edges.

Either way, re-vendor LibKa0s into the hosts listed in the diagnosis, and those addons' HUD icon edges change color in the affected skins under option A.

B. IMAGE 22, TESTER (LibKa0sSkinTester):
- Delete iconBorder() at modules/ShowroomOwner.lua:92-100 and the line `body.iconFrame = iconBorder(g, paint)` at :145.
- Trim the header comment at :14-15. The ICON local at :23 is still used? No, check: it is used only by iconBorder, so remove it too, or luacheck will flag an unused variable.
- Keep ShowroomOverlays.lua:150-157 (top sample) and the Controls square.

Tests to update:
- tests/test_showroom.lua:258 and :273: `assertEqual(#asked, 3, ...)` and `assertEqual(#frames, 3, ...)` become 2, with the message "Controls' square and Overlays'".
- tests/test_showroom_owner.lua:79: drop "iconFrame" from the keys.
- tests/test_showroom_owner.lua:82: drop "IconBorder" from the used-names list. It is still used by Overlays, so it could stay, but the list is per-section intent.
- tests/test_showroom_owner.lua:150-165: delete the test "addon surfaces: the icon border draws a 1 px edge in icon.border, in every skin", or move its 1 px and token assertions onto Overlays' body.framed in test_showroom.lua near :240.
- Kit-generated cases "skin switch: addon: IconBorder, fromSkin changes" (with and without the Scope ignored) drop out automatically. They come from captions (tests/_kit/test_skin_switch.lua:81).

Docs to update:
- docs/test-cases.md:340 and :921-922. These are regenerated by the battery.
- docs/module-map.md:32: drop "an icon border through IconBorder's fromSkin".
- README.md:26: drop "an icon border" from the Addon surfaces list.
- docs/smoke-tests.md:205, SHOW-39: drop "the Addon surfaces icon border".

SHOW-17 (:266-280) is a passed record that mentions the Addon surfaces icon border. Leave its recorded text as history, or note the removal, per the tester's smoke-file convention.

New smoke check (owner-run, not marked passed): `/st show` in Ka0s Default, Glass, WoW Forever, Ember and Obsidian. The Overlays IconBorder sample and the Controls square each show a clearly visible 1 px outline, lighter than both the window and the icon's dark field. The Addon surfaces section shows no icon border, and the section after the caution callout goes straight to the TreeGroup.

### testsAndSmoke

LibKa0s tests:
- tests/test_skin_icon_border.lua:62 pins Ka0s Default icon.border to 0,0,0,1.
- tests/test_skin_host_gaps.lua:34 pins the same value.
- tests/test_skin_icon_border.lua:95, :116 and :151 and tests/test_skin_paint_controls.lua:645 compare against the token, not a literal, so they follow any change.

Tester tests:
- tests/test_showroom.lua:249-260 ("a5", count 3) and :262-278 ("R3-L3", count 3).
- tests/test_showroom_owner.lua:76-84 (keys and used names) and :150-165 (the addon-surfaces icon border test).
- Kit-generated "skin switch: addon: IconBorder, fromSkin changes" (and the Scope-ignored variant), from tests/_kit/test_skin_switch.lua:81.

Smoke checks:
- docs/smoke-tests.md:205, SHOW-39: names the Addon surfaces icon border. Still "not run".
- docs/smoke-tests.md:207, SHOW-41.
- docs/smoke-tests.md:270-279, SHOW-17: a passed record mentioning the addon icon border.
- docs/smoke-tests.md:399-401, SHOW-32: IconBorder sample.

Nothing was run: this was a read-only step and no tests were needed.

### repos

- LibKa0s
- LibKa0sSkinTester
- AuraMaster
- KickCD
- DropWatcher
- QuickComms
- DpsRace
- ConsumableMaster

### files

- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinDefs.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinDefsOthers.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaintControls.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaintExtras.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_skin_icon_border.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_skin_host_gaps.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/modules/ShowroomOwner.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/modules/ShowroomOverlays.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/modules/ShowroomControls.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/tests/test_showroom.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/tests/test_showroom_owner.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/docs/smoke-tests.md
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/docs/module-map.md
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/README.md

### ownerQuestions

- Ka0s Default's icon.border is also the HUD icon edge in AuraMaster, KickCD, DropWatcher, QuickComms and DpsRace (black today, which reads well over the game world). Should the visible grey outline (#4d4d57 proposed) replace that HUD edge too (option A: one token, consistent with Obsidian, whose HUD edges are already grey), or apply only to S.IconBorder outlines in windows through a new icon.outline token while the HUD stays black (option B)?
- Glass, WoW Forever and Ember have the same weak-outline problem, though only Glass was reported. Apply the proposed lifts (Glass white 0.35, Forever #5a5048, Ember #8a3c1c) to all three, or fix only Ka0s Default and Glass as reported?

### challenge (holds=True)

- LibKa0sSkinTester/modules/ShowroomOwner.lua: the ICON local is at line 24, not 23. Its only use is iconBorder() at :97, so removing it along with iconBorder() is correct, and luacheck would otherwise flag it as unused.
- All of the other file:line claims check out: SkinPaintControls.lua:885-893 (drawIconEdge), :902-913 (zoom), :923-934 (S.IconBorder); SkinPaintExtras.lua:437-445 (P.px), :517-522 (P.edgeColor); SkinDefs.lua:497 (black icon.border); SkinDefsOthers.lua:278 (GLASS_EDGE), :289-305 (HUD_LOOK), :373-375 (register copy), :488 (Glass winBorder), :756 (Forever winBorder FV_EDGE); the three tester call sites; the test pins at test_skin_icon_border.lua:62 and test_skin_host_gaps.lua:34; and the counts of 3 at test_showroom.lua:258/:273. Image 22 confirms the bottom sample sits next to the 'Waiting for the pull' caution card, as claimed.
- MISSED: S.SquareIcon (SkinPaintControls.lua:841-849) also draws its own flat 1 px edge in T['icon.border'], with no edgeColor fallback. Controls' 'SquareIcon (crop) + IconBorder' sample therefore carries two coincident icon.border edges, and option B (a new icon.outline token read only by drawIconEdge) would leave SquareIcon's edge black or faint underneath. Its doc comment ':839-840 (nil in Ka0s Default)' is also stale, because Ka0s Default sets it to black.
- MISSED: DpsRace/core/SkinSetup.lua:104 and QuickComms/core/SkinSetup.lua:229 hard-code ['icon.border'] = {0,0,0,1} as the degraded-facade default that mirrors Ka0s Default. Under option A these need to move to the new Ka0s Default grey, or the library-absent fallback drifts from Ka0s Default.
- MISSED: ConsumableMaster/core/SkinSetup.lua:147: cm.buttonBorder follows icon.border, so ConsumableMaster's button border changes color under option A. The report only mentions CM's 'follow lists' in passing.
- MISSED: S.BarStyle (SkinPaintExtras.lua:778) exposes iconBorder = T['icon.border'] to hosts. No host reads .iconBorder from it today (AuraMaster's am.iconBorder is its own frame), but it is part of the token's public surface.
- MISSED: SkinEUI.lua:118 PANEL_EDGES derives icon.border from the ElvUI panel color at half brightness. The ElvUI-theme path overrides the per-skin value, so the proposed HUD_LOOK lifts do nothing there. Worth noting so nobody expects EUI outlines to change.
- MISSED: test_skin_host_gaps.lua:432 and :459 compare against F.tok(... 'icon.border'), so they follow the change, but they are additional coverage of the token that the report did not list. test_skin_host_gaps.lua:20 lists icon.border among Ka0s Default's OWN values.

## dpsrace-ui

### diagnosis

All paths are relative to /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace, on branch feat/2026-11-01-full-skinning.

(a) Stat blocks, images 11 and 12. Every figure box draws its label and value pinned to the left edge.
- HUD tiles: `kpi()` at modules/Hud_States.lua:289-306 builds the box for the running pair (:897 "Damage" / "DPS · Live", image 11), the Stop!/waiting pairs (:1022, :1102) and the result card (:1249).
  - :294 `k.label:SetPoint("TOPLEFT", f, "TOPLEFT", 8, -7)`
  - :300 `k.value:SetPoint("BOTTOMLEFT", f, "BOTTOMLEFT", 8, KPI_PAD + ...)`
  - :303-304 put the caption row at BOTTOMLEFT/BOTTOMRIGHT. `Style.Text` defaults to LEFT justify (modules/Style.lua:329), and so does `Style.PlainText` (:390).
  - `placeKpi()` (~:700-711) only moves the frames, not the text.
- Results detail: `kpi()` at modules/Results_Detail.lua:443-452 uses the same pattern for Damage/DPS/Meter DPS/Delta (:472-473): label TOPLEFT +8,-7 (:448), value BOTTOMLEFT +8,5 (:450).
- New best badge (:475-485): the trophy is anchored LEFT of a frame (:479), and the text sits RIGHT of the trophy (:483). Layout (:918-932) puts the three boxes in thirds. Delta goes under column 1 (:926-928). The badge starts at column 2 and spans the rest of the width, `cw - third - KPI_GAP` (:929-931), so it reads as left-pinned.
- The boxes already span their slots, so the left-pinned content is what looks off-centre.

(b) Spacing on the idle body, image 13. The constants are at modules/Hud_States.lua:95-105:
- `PRESET_TOP, PRESET_H, PRESET_GAP = 14, 20, 6`
- `IDLE_TARGET_Y = 14 + 40 + 6 + 8 = 68`
- `IDLE_CARD_Y = 82`
- `IDLE_WARN_Y = IDLE_CARD_Y + 46 + 6 = 134`
- `BEST_CAPTION_H, BEST_CARD_H = 14, 38`
- `IDLE_BEST_Y = IDLE_WARN_Y + 28 = 162`
- `BEST_H = 14 + 38 + 6 = 58`
- `IDLE_ARM_Y = IDLE_BEST_Y + BEST_H = 220`

Resulting gaps:
- Race Length block ends at 60; Target caption at 68: an 8 px gap.
- Target card ends at 128; Your best caption at 162: a 34 px gap. The extra room is a 28 px slot that is always reserved for the amber warning line (`w.warn`, :554-556).
- Your best card ends at 214; Arm at 220: a 6 px gap, smaller than the block gap.

That warning (`targetWarning`, modules/Hud.lua:264-269) is set only when the target's category is "other" (unknown target or no target). With a cataloged dummy, as in image 13, the slot sits empty. Everything is placed once in `Builders.idle` (:551-560); `body.Update` (:586-602) never re-anchors.

Minimum height constraint:
- `States.MinContentHeight()` (:1365) computes `IDLE_ARM_Y + 24 + 4 + 14 + 4 + 20 = 286`.
- tests/test_hud_layout.lua:68 sets CHROME to 68, so content height = MIN_HEIGHT - 68 = 354 - 68 = 286. The idle stack is therefore at its limit: any layout that puts Arm below 220 raises `Hud.MIN_HEIGHT`, which is pinned to 354 at test_hud_best.lua:189 and test_hud_layout.lua:203.

(c) Caption, image 14. `captionText(v)` at modules/Hud_Best.lua:61-68 joins `L["Your best"]`, spec, `Dummies.Label(category)` and `Format.Length(length)` with " · ". The caption is set at :150.

(d) Card line two, image 15. `lineText(run)` at modules/Hud_Best.lua:70-79 builds date `%d %b` · `L["ilvl %s"]` · the top spell (`run.spells[1]` through `HudBreakdown.SpellName`, :76-77). It is set at :165. The `b.line` FontString is CAPTION, anchored on both sides and truncating (:125-127; test_hud_best.lua:198 pins `__wrap == false`).

Consumables are recorded per run as `run.usage` (modules/Usage.lua:1-30, record shape at :21-25):
- Shape: `{ v=1, used={ {itemID?, kind, slot?, times?, n, src} }, candidates, edited }`.
- `kind` is one of gear, potion, flask, food or other. `Usage.KIND_BY_SUBCLASS` (:46) maps subclass 1 to potion, 2/3 to flask and 5 to food. Everything else, such as augment runes and Healthstones, is "other".
- It is captured from three sources: an arm-time snapshot (gear on-use, bag consumables, auras), casts during the race, and bag-count drops at the result. Built by `Usage.Build` (:320-324). All values are plain (Secrets).
- Well Fed food is stored with no itemID: `{kind="food", src="buff"}` (:246).
- Sample and sim runs carry usage too (modules/MockRuns.lua:352-410: potion, flask and Well Fed).
- Runs stored before format 3 have no record.

Ready-made helpers in modules/Results_Usage.lua:
- `ResultsUsage.Entries(run)` (:62-75): the shown entries, gear first, with hidden items and old enchant entries removed (`Usage.Shown`); nil when nothing was recorded.
- `ResultsUsage.Name(e)` (:242-249): the item name, or "Well Fed".
- `ResultsUsage.Icon(e)` (:252-257): `C_Item.GetItemIconByID`, Spell_Misc_Food or a question mark.
- `ResultsUsage.InlineIcon(e)` (:260-262): `"|T<icon>:14:14|t"`.

These are runtime-only reads, so the load order (Results_Usage after Hud_Best, DpsRace.toc:148/178) is fine, as it already is for `NS.ResultsTable`.

(e) Arm button, image 16. `Best.ArmLabel(v)` at modules/Hud_Best.lua:52-59 returns `L["Arm Race \194\183 beat %s"]` whenever the board has a best. modules/Hud_States.lua:599 sets the button label from it on every idle update. The button is built with `L["Arm Race"]` at :558.

Locale strings (locales/enUS.lua):
- :110 `L["Arm Race"]`
- :112 `L["Your best"]`
- :113 `L["Arm Race \194\183 beat %s"]`
- :232 `L["ilvl %s"]`
- :913 `L["Well Fed"]`

Old behaviour is pinned by these tests:
- tests/test_hud_best.lua: :7-9 header; :84, :102 full caption; :133 caption has "0:30"; :145 caption has "Affliction"; :91 line has "Chaos Bolt"; :93 arm label "Arm Race · beat"; :187-189 IDLE_BEST_Y 162, ARM = BEST + BEST_H, MIN_HEIGHT 354.
- tests/test_hud_layout.lua:193-203: IDLE_BEST_Y 162, IDLE_ARM_Y 220, MIN_HEIGHT 354.
- tests/test_hud_tiles.lua:66-78: Stop!/waiting caption and value at BOTTOMLEFT x=8.
- tests/test_results_delta.lua:141-152: Delta box width equals Damage width; badge height KPI_H. These survive the change.
- tests/test_hud_window.lua:283 and tests/test_hud_element_tips.lua:55 expect "Arm Race". They survive.

Smoke checks and docs:
- docs/smoke-tests.md:830 (SM-DR-R3DR4) describes the long caption, "date · ilvl · top spell" and "Arm Race · beat <DPS>". :115 (R1) mentions the section.
- docs/module-map.md:68 and docs/testing.md:81 describe `ArmLabel` and the top spell.

### whereUsed

- `HudBest.ArmLabel` is called only at modules/Hud_States.lua:599.
- `captionText`, `lineText` and `tipOf` are used only inside Hud_Best.lua (:150, :152, :165).
- `States.IDLE_BEST_Y`, `BEST_H` and `IDLE_ARM_Y` are exported at Hud_States.lua:103-105. They are read by Hud_Best.lua:5/111, Hud_States `MinContentHeight` :1365, and tests test_hud_best.lua:187-188, test_hud_layout.lua:198-199 and test_hud_window.lua:373.
- HUD `kpi()`/`kpiPair()` are used by the running (:897), Stop! (:1022), waiting (:1102) and result card (:1249) bodies.
- Results_Detail `kpi()` is used at :472-473 for Damage, DPS, Meter DPS and Delta. The badge is at :475-485, laid out at :918-932, and toggled by `fillDelta` :700-707.
- `ResultsUsage.Entries`/`Icon`/`Name`/`InlineIcon` are already used by the Runs list's Used column (Results_Runs.lua:783) and its tips.
- The `run.usage` record is built in modules/Usage.lua and sampled in MockRuns.lua:352-410. The sim and test mode therefore show consumables on the Your best card.

### proposal

All paths are relative to DpsRace.

(a) Centre the text in every figure box.
- In Hud_States `kpi()` (:289-306):
  - Create the label with justify "CENTER" (`Style.Text(f, FONT.CAPTION, nil, "CENTER")`) and anchor it TOPLEFT (8,-7) and TOPRIGHT (-8,-7).
  - Create the value with "CENTER": `Style.PlainText(f, FONT.FIGURE, "CENTER")` for the running pair, `Style.Text(f, FONT.FIGURE, color, "CENTER")` otherwise. Anchor it BOTTOMLEFT (8,y) and BOTTOMRIGHT (-8,y).
  - Give the caption row (:302-304) CENTER justify on its existing two anchors.
  - Nothing is measured. Justify works on secret strings, so the running body's live values stay safe.
- In Results_Detail `kpi()` (:443-452), make the same change through `Tbl.Text(..., "CENTER")` with two-sided anchors.
- New best badge, in two parts:
  - Layout (:929-931): give it column 2's slot, `SetWidth(third)` at `third + KPI_GAP`, the same size as the Delta box beside it.
  - Build (:479-483): centre the pair without measuring. Anchor `badgeText` at the badge's CENTER, offset +(BADGE_ICON+6)/2. Anchor `badgeIcon` RIGHT to `badgeText`'s LEFT at -6.
- This covers all four HUD tile bodies (running, Stop!, waiting, result) and the Results detail, so every box reads the same.
- Tests:
  - Update test_hud_tiles.lua:66-78 to expect the caption and value spanning BOTTOMLEFT/BOTTOMRIGHT ±8 with `__justifyH == "CENTER"`, if the mock records justify. Otherwise assert both anchors.
  - Add a pin to test_results_delta.lua that the badge width equals the Delta box width.

(b) Even block spacing and extra room above Arm Race. Make the slots depend on whether the warning is shown, and keep Arm at or above 220 so `MIN_HEIGHT` stays 354.
- New constants (Hud_States :95-105):
  - `BLOCK_GAP = 8`, the existing gap between the presets and Target.
  - `ARM_GAP = 14`, the extra room above Arm Race.
  - `IDLE_WARN_Y = IDLE_CARD_Y + 46 + 4 = 132`.
  - Without a warning, `IDLE_BEST_Y_PLAIN = IDLE_CARD_Y + 46 + BLOCK_GAP = 136`.
  - With a warning, `IDLE_BEST_Y_WARNED = IDLE_WARN_Y + 28 = 160`. The warning reads as part of the Target block.
  - `BEST_BLOCK_H = BEST_CAPTION_H + BEST_CARD_H = 52`.
- Arm position:
  - Without a warning, Arm is at 136 + 52 + 14 = 202.
  - With a warning, Arm is at 160 + 52 + 8 = 220, because it is capped at the old `IDLE_ARM_Y` so the minimum height does not move.
  - Export `States.IDLE_ARM_Y = 220`, the deepest position, for `MinContentHeight`.
- New `HudBest.Place(b, y)`: clear points and re-anchor the caption and card (the code now in `Build` :114-119). `Build` calls it.
- In idle `body.Update` (:586-602), pick the Y from `v.warning ~= nil`. Call `NS.HudBest.Place(self.w.best, -y)` and re-anchor `w.arm` TOPLEFT/TOPRIGHT at `-armY`. Only do this when the slot changes (cache `self.slot`) to avoid re-anchoring every redraw.
- Tests:
  - test_hud_best.lua:187-189 and test_hud_layout.lua:198-199: assert the plain and warned Y values and that `MIN_HEIGHT` is still 354.
  - Add a test that targets GOLEM vs an unknown target and checks that the best caption's TOPLEFT y moves from -136 to -160 and Arm from -202 to -220.
  - Pin `IDLE_TARGET_Y - 60 == IDLE_BEST_Y_PLAIN - 128 == BLOCK_GAP`, so the gaps are equal.

(c) Caption reads "Your best".
- `captionText` (Hud_Best :61-68) becomes `return L["Your best"]`. Remove the DOT join and the spec, category and length parts.
- Move the board to the tooltip: in `tipOf` (:82-96) add the line `spec · Dummies.Label(category) · Format.Length(length)` under "Your best". This needs `v` passed in, `tipOf(run, v)` at :152. No new locale key is needed. The spec, category and length still swap live, so tests :133 and :145 move to the tooltip lines.
- test_hud_best.lua :84 and :102 assert the caption equals "Your best".

(d) Consumables instead of the top spell.
- `lineText(run)` (:70-79): keep date and ilvl, and drop the `run.spells[1]` part (:76-77).
- Add the consumables:
  ```lua
  local icons = {}
  for _, e in ipairs(NS.ResultsUsage.Entries(run) or {}) do
      if e.kind ~= "gear" then
          icons[#icons + 1] = "|T" .. tostring(NS.ResultsUsage.Icon(e)) .. ":12:12|t" .. ((tonumber(e.n) or 1) > 1 and ("x" .. e.n) or "")
      end
  end
  if #icons > 0 then parts[#parts + 1] = table.concat(icons, " ") end
  ```
  - The 12 px size matches the 10 px CAPTION line.
  - This covers potions, flasks, food (Well Fed) and other (augment runes, Healthstones), with gear left out.
  - Hidden items are excluded by `Entries`.
  - When nothing was used, or the run has no usage record, nothing is appended: the line is "01 Nov · ilvl 331.4" with no trailing dot.
  - The line already truncates (`__wrap` false).
- Tooltip: after the top-3 spells (:90-93), add one line per consumable, `ResultsUsage.InlineIcon(e) .. " " .. ResultsUsage.Name(e)`. This tells the player what the icons on the card are. No new locale key unless a heading is wanted (`L["Consumables"]`).
- Tests (test_hud_best.lua):
  - Change :91 to assert "Chaos Bolt" is absent from the line.
  - Store a run with `run.usage = { v=1, used={ {itemID=X, kind="potion", n=1, src="cast"}, {kind="food", n=1, src="buff"}, {itemID=G, kind="gear", slot=13, n=1, src="cast"} }, candidates={}, edited=false }`. Assert the line has the potion icon and Spell_Misc_Food but not the gear item's icon.
  - Add an empty-usage test: the line equals date · ilvl exactly.

(e) The button says "Arm Race".
- Delete `Best.ArmLabel` (Hud_Best :52-59) and its call at Hud_States :599. The label from `wideButton` at :558 (`L["Arm Race"]`) stays.
- Delete the locale key at enUS.lua:113 `L["Arm Race \194\183 beat %s"]`.
- Tests: test_hud_best.lua :93 becomes `assertEqual(w.arm.label.__text, "Arm Race")`; :9 header comment.

Docs and smoke:
- Rewrite docs/smoke-tests.md SM-DR-R3DR4 (:830). New expected result:
  - The caption reads just *Your best*.
  - The card shows *date · ilvl · consumable icons*, or date · ilvl alone with nothing after it when no consumable was used.
  - *Arm Race* is plain.
  - The hover adds the board line and the consumables.
  - The idle stack: 8 px between the three blocks, more above Arm Race, and the stack drops only when the amber warning shows.
- Add a new check for the centred figure boxes: the HUD running, Stop!, waiting and result tiles, plus the Results detail with Delta and New best. Use `/dr sim` and `/dr test result`.
- Update docs/module-map.md:68 (no `ArmLabel`; consumables, not top spell) and docs/testing.md:81.

Locale strings:
- Remove `"Arm Race \194\183 beat %s"`.
- Keep "Your best", "ilvl %s", "Well Fed" and "Arm Race".
- Optional new key: "Consumables", for the tooltip heading.

### testsAndSmoke

Nothing was run (this was a read-only step). Gate commands, per DpsRace/CLAUDE.md:
- `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua`
- `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded luacheck .`

Tests that pin the old behaviour and must change:
- tests/test_hud_best.lua: :84, :102 (full caption), :133, :145 (board in the caption), :91 (top spell "Chaos Bolt" on the line), :93 (arm label "Arm Race · beat"), :187-188 (IDLE_BEST_Y 162, ARM = BEST + BEST_H), and header comments :7-9.
- tests/test_hud_layout.lua:193-199: IDLE_BEST_Y 162 and IDLE_ARM_Y 220. Keep MIN_HEIGHT 354 (:203).
- tests/test_hud_tiles.lua:66-78: caption and value anchored BOTTOMLEFT x=8 on the Stop! and waiting tiles.

Tests that hold unchanged:
- test_results_delta.lua:141-152
- test_hud_window.lua:283 and :373
- test_hud_element_tips.lua:55

Smoke checks:
- Rewrite SM-DR-R3DR4 (docs/smoke-tests.md:830); its status is "Not run".
- R1 (:115) stays valid.
- Add a new check for the centred figure boxes, covering the HUD running, Stop!, waiting and result tiles and the Results detail: `/dr sim`, `/dr test result`, then Details.

The owner runs smoke in game. Nothing is marked passed.

### repos

- DpsRace

### files

- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Hud_Best.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Hud_States.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Detail.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Usage.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Usage.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Hud.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/locales/enUS.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/tests/test_hud_best.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/tests/test_hud_layout.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/tests/test_hud_tiles.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/tests/test_results_delta.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/docs/smoke-tests.md
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/docs/module-map.md
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/docs/testing.md

### ownerQuestions

- Results detail row 2 (image 12): the Delta box sits under Damage and the New best badge beside it, with the third column empty. Should only the contents of each block be centred, which is the proposal (the badge centred in a column-2 slot the size of the Delta box)? Or should the Delta + New best pair be centred as a group under the three boxes?
- Consumables on the Your best card: icons only, 12 px with 'x2' when used more than once and the names in the hover (proposed), or item names as text, which truncate at the HUD's minimum width? Should 'other'-kind items (augment runes, Healthstones) count as consumables alongside potions, flasks and Well Fed?
- The Your best tooltip still lists the top 3 damaging spells. Keep them, with the board line (spec · type · length) and the consumables added, or drop them too?

### challenge (holds=True)

- The test that pins MIN_HEIGHT at 354 is test_hud_layout.lua:202. Line :203 is a different check: it asserts MIN_HEIGHT - CHROME == MinContentHeight(). Line :201 also pins Arm's floor at 220 + 24 + 4 + 14 + 4 + 20. Line :189 in test_hud_best.lua is cited correctly.
- The idle stack sets the minimum height only because it ties for the largest of the three heights. MinContentHeight (Hud_States.lua:1365-1371) returns math.max(idle, running, result), and the test's 354 - 68 = 286 matches the idle value. So keeping Arm at or above 220 is the right constraint. Moving Arm lower would raise MIN_HEIGHT unless the change is offset elsewhere.
- Hud_Best.lua:167 is in the tooltip test, which lists 'Chaos Bolt', 'Incinerate' and 'Immolate' as the top-3 spells. If the owner keeps the top spells in the hover (open question 3), it survives unchanged. If they are dropped, it must change. The report's test list does not mention it.
- MISSED: The checked file:line claims hold on feat/2026-11-01-full-skinning. Constants :95-105 give TARGET 68, CARD 82, WARN 134, BEST 162, BEST_H 58 and ARM 220. CARD_HEIGHT is 46 (:425). Also checked: kpi() at :289-306, the idle Build and Update at :551-602 with ArmLabel at :599, Results_Detail kpi() at :443-452, the badge at :475-485 and its layout at :918-932, Hud_Best captionText, lineText and tipOf at :61-96, Results_Usage Entries, Name, Icon and InlineIcon, the Usage record shape, targetWarning (Hud.lua:264-269), and the locale key at enUS.lua:113, which exists only in enUS. The screenshots match the diagnosis: in 13 the Target-to-Your-best gap is visibly larger than the other gaps, and in 11 and 12 the text is left-pinned.
- MISSED: Two kinds of re-application leave the centring alone. Re-applying the HUD Appearance font (Hud_Appearance.ApplyFont, called from styleRunning :716-717) does not reset justify, and placeKpi (:690-700) moves only the frames. Centred justify therefore survives restyles. The mock records __justifyH (tests/mock_widgets.lua:166, tests/_kit/mock_paint.lua:224), so the proposed justify assertions can be written.
- MISSED: Tbl.Text is Style.Text (Results_Table.lua:90), so the 4th justify argument the Results_Detail change needs is available.
- MISSED: Scope note for item (a): the proposal also centres the Stop! and waiting tiles ('Damage Stopped' / 'In Combat', :1022/:1102), but the owner only showed the running tile (image 11) and the Results detail (image 12). That is a reasonable consistency extension, but it is beyond what the owner asked for. List it as such, or ask the owner.
- MISSED: Item (d), cost: ResultsUsage.Entries reads Usage.HiddenSet() and C_Item icons on every idle Update. Idle refreshes are event-driven through Hud.Refresh, so this is acceptable, but it is a new per-refresh read on the HUD.
- MISSED: The docs/smoke-tests.md SM-DR-R3DR4 row (:830) also says 'The presets and the Target card stay where they were'. That still holds under the proposal, but the rewrite should state that the Your best block moves up when no warning is shown.

## sims

### diagnosis

MULTIMETERS TODAY (image 18)
- Fights are data in MultiMeters/modules/SimScenario.lua:38-49 (shape `{ name, enemy, ticks, secondsPerTick, ends, deaths }`). The step label is built at SimScenario.lua:85, `L["Pull %s (%d ticks x %d s)"]:format(f.name, f.ticks, f.secondsPerTick)`.
- Meaning of "Pull Speaker Shadowcrown (10 ticks x 18 s)": the fight fires 10 meter ticks. Each tick adds 18 s of simulated segment time, because D.Tick calls World.Tick(w, fight.secondsPerTick) (SimDrivers.lua:93-100) and World.Tick adds `seconds` to seg.duration and to every member's damage (SimWorld.lua:298-308). So the segment models a 180 s boss. In wall-clock time it does NOT last 180 s:
  - D.Fight runs the pull and tick 1 at once, then books ticks 2..N with `sim:After(D.TICK * (k - 1), ...)` (SimDrivers.lua:154-168).
  - D.TICK is 0.5 s (SimDrivers.lua:33), so Speaker plays in (10-1)*0.5 = 4.5 s, Trash (6 x 4 s, which models 24 s) in 2.5 s, and the raid boss (12 x 25 s) in 5.5 s.
- What each tick fires: one DAMAGE_METER_CURRENT_SESSION_UPDATED (SimDrivers.lua:99). The pull also fires PLAYER_REGEN_DISABLED (:105-113), and the last tick fires PLAYER_REGEN_ENABLED plus one COMBAT_SESSION_UPDATED per stat (:118-131).
- Pacing: the host gate holds the next step while booked ticks remain. `Host.Gate` returns false with "The fight is still running." while w.pending > 0 (MultiMeters/modules/Sim.lua:133-137), and it is wired into the descriptor at Sim.lua:337. The library polls a closed gate every GATE_POLL = 0.25 s and plays the next step as soon as it opens (LibKa0s/LibKa0s/SimTimeline.lua:103, :307-312). So a fight step's wall time is roughly max(ticks-1)*0.5 s, rounded up to the next 0.25 s poll, regardless of sim.stepDelay. sim.stepDelay defaults to 1 (MultiMeters/defaults/Profile.lua:862).

DPSRACE TODAY (image 17)
- Steps: armed, start, buzzer (labelled "Combat ends" for endAt scenarios), result, results (DpsRace/modules/Sim.lua:154-164). Each step is a clock jump on the sample race (STEP_MOMENTS, Sim.lua:145-152):
  - start = SampleRace.Skip(0)
  - buzzer = SampleRace.Skip(StopAt())
- The descriptor has no `gate` (Sim.lua:180-202).
- The sample race's damage already exists. MockRuns.Plan builds every cast and hit from the class rotation across the race (MockRuns.lua:287-300, playRow :206-221). A Warlock gets about 70 hits in 30 s: Incinerate every 2.5 s, Chaos Bolt every 6 s, Wither 6 ticks, Infernal 14 ticks, imp Firebolt every 2 s (MockRotations.lua:83-93).
- The sim race length is MockRuns.LENGTH = 30 s (MockRuns.lua:26; stopAt = endAt or LENGTH, MockRuns.lua:590-591). It is NOT the 60 s `race.defaultLength` from the R3 addendum (defaults/Profile.lua:100; R3_ADDENDUM_DPSRACE.md:5). That 60 s is a real race's idle-body default and never reaches the sim.
- Why the race looks empty when stepped: with stepDelay 1 (DpsRace defaults/Profile.lua:218), Race starts puts the clock at 0. One second later, Buzzer runs Skip(30): `origin = GetTime() - t` (SampleRace.lua:254-260), and one Advance lands the other ~29 s of hits in a single beat (land/hear, SampleRace.lua:106-126, 184-191). So about 1 s of live damage plays, and the rest arrives in one jump.
- Knock-on (read from the code, not observed in game): live chart buckets are copied only by HUD reads within Slices.LATE = 1.0 s of their boundary (Slices.lua:27, :76-93). After a 29 s jump, buckets 2..29 are skipped as late, so the sim run's live and card chart (Hud_Chart.lua:359 reads Slices.Get) is mostly holes.
- A related latent bug: Casts.Start(origin) is captured at begin (SampleRace.lua:131), but hear() later stamps casts at `origin + c.t` (SampleRace.lua:109). Skip moves origin afterwards, so casts heard after a jump get times shifted by the jump on the live cast list (Casts.lua:102-106, centis :178-180).
- How the race clock works: clock() = GetTime() - origin (SampleRace.lua:66-69). A 0.05 s ticker calls Advance (Sim.lua:39, :115-126, :137). The buzzer fires by itself when the clock reaches stopAt (running(), SampleRace.lua:184-191). Elapsed, TimeLeft, SinceBuzzer and ReadLive all come from clock() (SampleRace.lua:73-98).
- The no-stepper path (no LibKa0s-Sim session) plays the 30 s race at real speed (Sim.lua:130-138, 227-235).

### whereUsed

MultiMeters:
- FIGHTS: SimScenario.lua:38-49, used by the timelines at :127-141.
- Fight label: SimScenario.lua:85.
- D.TICK booking: SimDrivers.lua:33 and :154-168.
- Gate: Sim.lua:133-137, wired at :337.

DpsRace:
- Steps: Sim.lua:145-164 (STEP_MOMENTS and timeline).
- Descriptor: Sim.lua:180-202, with no gate today.
- Sample race clock: SampleRace.lua:66-69 (clock), :234-273 (Unpark, Skip, SkipToResult), :184-191 (the natural buzzer).
- Plan: MockRuns.lua:26 (LENGTH = 30) and :287-300.
- Chart buckets: Slices.lua:27 and :76-93; Hud.lua:638-649 (scheduleSlice) and :685-692 (requestLive at live.hz = 4).

Library:
- Pacing: SimTimeline.lua:103 (GATE_POLL = 0.25), :283-312 (delayAfter, tick).

### proposal

A. MULTIMETERS: every fight step lasts 10 s, with more events
1. Keep D.TICK = 0.5 s (SimDrivers.lua:33). Raise each fight to 21 ticks: the pull plus tick 1 at 0 s, then 20 booked ticks at 0.5..10.0 s, so the step spans exactly (21-1)*0.5 = 10 s.
   - That is 2 meter updates per second: 21 DAMAGE_METER_CURRENT_SESSION_UPDATED instead of 6 or 10.
   - The gate already holds the next step until the last tick (Sim.lua:133-137), so no host or library change is needed.
   - Add a named constant, `Host.FIGHT_SECONDS = 10`, and a test that pins `(ticks-1)*D.TICK == FIGHT_SECONDS` for every FIGHTS entry.
2. Re-pick secondsPerTick so the simulated segment length stays near today's. It must be an integer, because the label uses %d.
   - dungeonTrash: 21 x 1 s (21 s; today 24 s)
   - dungeonBoss: 21 x 9 s (189 s; today 180 s)
   - raidBoss: 21 x 15 s (315 s; today 300 s)
   - wipeBoss: 21 x 6 s (126 s; today 120 s)
   - wipeRepull and zoneTrash: 21 x 1 s
3. Rescale the death ticks (SimScenario.lua:40-46) to the same relative point in the fight:
   - dungeonBoss: 7/10 becomes 15/21
   - raidBoss: 6 and 9 of 12 become 11 and 16 of 21
   - wipeBoss: 5, 6 and 8 of 8 become 13, 16 and 21 (the `all` death stays on the last tick)
4. Labels then read "Pull Trash (21 ticks x 1 s)" and "Pull Speaker Shadowcrown (21 ticks x 9 s)". No locale key changes (enUS.lua:1268).
5. Perf: 2 Hz meter events go through the engine's existing coalescing, and the e2e drain guard of 200 is ample (test_sim_e2e.lua:167-174).

B. DPSRACE: a new "Racing" step between Race starts and Buzzer, about 10 s, playing the whole race to its buzzer
1. Timeline (Sim.lua:154-164) becomes armed, start, race, buzzer, result, results.
   - New step `{ kind = "race", label = L["Racing (%d s of damage in %d s)"]:format(s.endAt or MockRuns.LENGTH, Sim.RACE_STEP_SECONDS) }`, giving "Racing (30 s of damage in 10 s)", or "(12 s ... )" for `died` and "(18 s ... )" for `incomplete`.
   - The label uses only scenario data, because the timeline is pure and can be built before prepare launches the sample (SimTimeline.lua:151-172).
   - New constant `Sim.RACE_STEP_SECONDS = 10`.
2. Recommended: compress the race clock during the step.
   - STEP_MOMENTS.race calls `NS.SampleRace.Pace((StopAt() - clock) / Sim.RACE_STEP_SECONDS)`. For newbest that is about 2.9x, because Race starts already ran about 1 s at 1x.
   - The race then plays every planned hit and cast in order, about 7 hits per wall second for a Warlock. The HUD countdown runs to 0:00 by itself, and the buzzer is the race's own (running(), SampleRace.lua:184-191). No jump happens, so the chart buckets fill.
   - SampleRace changes:
     - Replace `origin` in clock() with an anchor pair, so the clock is `anchor + (GetTime() - wallAt) * rate`, and rebase on every rate change.
     - Re-express Unpark, Skip and SkipToResult (SampleRace.lua:234-273) on the anchor.
     - Add Pace(rate) and Rate(), and reset rate to 1 in buzz() and endEarly() (SampleRace.lua:143-154), so Stop!, the tail, late casts and the quiet-before-read play at real speed.
     - Capture a fixed `zero` at begin() for Casts.Start(zero) and Hear(zero + c.t). This also fixes the existing Skip shift (SampleRace.lua:109, :131).
   - Hud scheduleSlice (Hud.lua:638-649) waits `(at - elapsed)` race seconds as wall time. Divide that by `race.Rate and race.Rate() or 1`, so boundary reads land in time under 3x. Without the fix, the 4 Hz reads (live.hz default 4, Profile.lua:120) still land within LATE while hits flow, but quiet stretches could leave holes.
   - Rate stays 1 everywhere else: test mode Hold, the no-stepper path and every existing test that Unparks and plays in real time.
3. Gate: add `gate = function() return Sim.Gate() end` to the descriptor (Sim.lua:180).
   - It is closed, with L["The race is still running."], while SampleRace.Rate() ~= 1 and the state is RUNNING.
   - So the Buzzer step plays within 0.25 s of the natural buzzer, and is then a marker: Skip(StopAt()) is a no-op because the clock is already at or past stopAt.
   - Consequence: a manual Step, or a click-ahead on Buzzer, Result card or Results window, now waits out the 10 s race step, exactly as MultiMeters' fight steps do (SimTimeline.lua:263-280, runTo :339-369).
4. Total wall time for newbest at stepDelay 1: armed, then 1 s, start, then 1 s, race (about 10 s), buzzer (0.25 s poll), then 1 s, result, then 1 s, results.
5. Simpler fallback (if the owner prefers no clock compression): the race step plays real time and the gate holds until the clock reaches start + 10 s; Buzzer then Skip(30)s as today. It is less code, but the 20 s jump keeps the chart holes and the HUD timer leaps from 0:20 to 0:00. Not recommended.

DOC RIPPLE
- DpsRace docs/smoke-tests.md:818 (SM-DR-SF15, passed on 2026-11-02) lists the old five steps. Add a new smoke row rather than edit the passed one.
- LibKa0s/docs/api/CONSUMERS.md:1146 (Sim `gate`, consumed by 3) would gain DpsRace. That table does not list DpsRace as a Sim consumer at all today (:1141-1150), which is a census gap to note.
- MultiMeters docs/ARCHITECTURE.md:61 needs no number change.

### testsAndSmoke

MULTIMETERS
- test_sim_drivers.lua uses its own FIGHT tables (:57, :152, :170), so it is unaffected while D.TICK stays 0.5.
- test_sim_e2e.lua checks death counts and roles (:308-310, :333, :359-362), not tick numbers, so the rescaled death ticks must keep the same counts and roles. The drain guard of 200 (:167-174) covers 20 bookings.
- New test (red under today's 6 and 10 ticks): every Host.FIGHTS entry has `(ticks-1)*D.TICK == 10`.
- New test: a dungeon boss step keeps the gate closed at 9.5 s and open at 10.25 s (the session gate test pattern, test_sim_session.lua:119).
- New test: each death tick is at or below its fight's tick count.
- Smoke: run `/mm sim dungeon` and Run. Pull Trash and Pull Speaker each take about 10 s, with numbers growing twice a second. The owner runs this smoke check.

DPSRACE, tests/test_sim.lua
- :331 and :379: change labels to "armed,start,race,buzzer,result,results".
- :380 and :383: change Steps()[3] to Steps()[4].
- :357-372 (the step-by-step test): after the race Step, f:advance(10.5) before the buzzer Step, and assert that a Step inside the window answers settling.
- New test: newbest's race step reaches "stopping" by itself within 10 s ± one beat, and not before 9.5 s. Same for died (endAt 12) and incomplete (endAt 18).
- New test: after the race step every chart bucket is filled. `Slices.Get("sim-newbest").filled == count` is red under today's Skip(30) jump.
- New test: the live cast list times equal the plan's casts' t under pace. This is red today after a Skip.
- New test: rate is back to 1 after the buzzer, so the tail and combat end take their scenario seconds of wall time (combatEnd 4.2 for newbest).
- New test: the gate is open whenever no race step is pacing.
- The existing real-time tests that Unpark (test_chart.lua:568/588, test_chart_icons.lua:582, test_countdown.lua:254-292, test_pace.lua:295, test_sample_parity.lua:28) must stay green unchanged, because they prove rate 1 is the default.

GATES AND SMOKE
- Green gate per repo: lua tests/run.lua, plus `ka0s-bounded luacheck .`.
- SampleRace.lua grows, so watch the CCN of clock(), Skip and SkipToResult.
- Smoke: add a new row next to SM-DR-SF15 (DpsRace docs/smoke-tests.md:818): `/dr sim`, Run, then watch the Racing step. The HUD timer runs 0:30 to 0:00 in about 10 s with steady damage, the buzzer fires on its own, and the chart is complete. The owner runs this smoke check.

### data

Wall time today, at D.TICK 0.5:
- Trash: 6 x 4 s, plays in 2.5 s (24 s simulated)
- Speaker: 10 x 18 s, plays in 4.5 s (180 s simulated)
- Raid: 12 x 25 s, plays in 5.5 s
- Wipe boss: 8 x 15 s, plays in 3.5 s
- Re-pull and zone trash: 4 or 5 x 4 s, plays in 1.5 to 2.0 s

Proposed: all fights 21 ticks, so 10.0 s. DpsRace's sim race is 30 s (MockRuns.LENGTH), not 60. With stepDelay 1 today, about 1 s of it plays live before Buzzer Skip(30) jumps about 29 s.

### repos

- MultiMeters
- DpsRace

### files

- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/modules/SimScenario.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/modules/SimDrivers.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/modules/Sim.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/tests/test_sim_e2e.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/tests/test_sim_drivers.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Sim.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/SampleRace.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/MockRuns.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Hud.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Slices.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Casts.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/locales/enUS.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/tests/test_sim.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/docs/smoke-tests.md
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SimTimeline.lua
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/docs/api/CONSUMERS.md

### ownerQuestions

- DpsRace Racing step: is it OK that the race plays fast (30 s of the race in about 10 s, so the HUD timer runs about 3x), so the buzzer comes by itself and the chart fills? Recommended. The alternative is 10 s at real speed and then a jump to the buzzer, which leaves the live chart with gaps and the timer leaping from 0:20 to 0:00.
- MultiMeters: should the 10 s length apply to every fight step in all four scenarios, including the raid boss, the wipe and its re-pull, and both trash pulls in `zone`? Or only to the dungeon's Pull Trash and Pull Speaker? Applying it to all of them makes /mm sim zone and /mm sim wipe about 20 s of fighting each.

### challenge (holds=True)

- Minor: in MultiMeters a fight step's wall time is not just (ticks-1)*0.5 rounded to the poll. After the fight step plays, the timeline first waits delayAfter (sim.stepDelay, default 1 s; SimTimeline.lua:283-312), then checks the gate, then re-polls every 0.25 s. So the step lasts max(stepDelay, (ticks-1)*0.5 rounded up to the next 0.25 s poll). At the default of 1 s the 10 s proposal is unaffected. At stepDelay values above 10 (the DpsRace row allows up to 10) the delay is what sets the step's length.
- The citation in LibKa0s/docs/api/CONSUMERS.md is already stale before this work. The `gate` row cites MultiMeters `modules/Sim.lua:325`, but the gate is wired at Sim.lua:337 today. Fix that line when adding DpsRace to the row.
- Every other file:line claim checks out: FIGHTS at SimScenario.lua:38-49, the label at :85, D.TICK = 0.5 at SimDrivers.lua:33, D.Fight booking at :154-168, Host.Gate at Sim.lua:133-137, GATE_POLL = 0.25, MockRuns.LENGTH = 30 with stopAt = endAt or LENGTH, STEP_MOMENTS and the timeline at DpsRace Sim.lua:145-164, no gate in the DpsRace descriptor, clock() = GetTime() - origin, Skip moving origin, Slices.LATE = 1.0, scheduleSlice waiting (at - elapsed) as wall time, live.hz 4, stepDelay 1 in both profiles, and the test lines at test_sim.lua:331/379/380/383. The latent cast-time shift is also real. Casts.Start(origin) is captured once in begin, but hear() stamps casts at the moved origin + c.t, so casts heard after Skip(30) come out about 29 s early on the live list.
- MISSED: MultiMeters docs/module-map.md:386 hard-codes the current numbers: 'Trash 6 x 4 s, Speaker Shadowcrown 10 x 18 s with a damage dealer dying at tick 7', 'Vexie ... 12 x 25 s', 'everyone dead by tick 8, ... a 4-tick re-pull'. All of them change under the 21-tick proposal. The doc ripple named only ARCHITECTURE.md:61 ('no change') and left this file out.
- MISSED: The new design goes against DpsRace's stated stepper contract in modules/Sim.lua:141-143: 'a click on a step jumps the clock to that moment (SampleRace.Skip), so the stepper skips the waits and never changes what the race does'. Compressing the clock and gating the next step reverses both halves of that. The comment, the SF-DR-8/SG-SIM wording, and docs/test-cases.md (the generated list, e.g. :1420) need updating along with the new tests.
- MISSED: No alternative was considered that avoids changing the clock. For example, a sim-only race length of about 10 to 12 s (MockRuns.LENGTH, or a per-scenario length) would give a real-time 10 s damage step with the natural buzzer and full chart buckets, and needs no rate or anchor rework in SampleRace. The catch is that the HUD would show a 0:10 race rather than 0:30. The owner should get this as a third option next to 'compress 3x' and 'real time, then jump'.
- MISSED: SampleRace.Hold (test mode) and SkipToResult (which does origin = origin - 0.5 in a loop) both work on `origin` directly. Moving to an anchor/rate clock must keep SkipToResult's 400-step loop and Hold's replay correct. Their existing tests (test_countdown, test_sample_parity, and the Hold-based chart tests) are the regression net, and the proposal named only the Unpark-based ones.
- MISSED: The proposed MultiMeters secondsPerTick of 1 for trash makes the label read 'Pull Trash (21 ticks x 1 s)'. Because the label forces whole seconds (%d), a reader can easily take that to be the wall-clock pacing, which is actually 0.5 s per tick. The owner may want the label to show wall duration instead, e.g. '(10 s)'. That changes a locale key (enUS.lua:1268) and the label on the passed SM rows.
