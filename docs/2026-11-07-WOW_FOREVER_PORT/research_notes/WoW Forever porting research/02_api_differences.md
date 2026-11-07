# Lua and UI API differences: WoW: Forever (Camelot, 1.60.1, Interface 16001) vs Retail (Mainline 12.1.5)

Research date: 2026-11-07. Evidence tiers used below:

- **[DIFF]** means I confirmed it myself by diffing Blizzard's shipped UI source or Ketho's per-flavour dumps (method below).
- **[SOURCE]** means a primary or near-primary page states it: warcraft.wiki.gg API-change pages, Ace3 commits, or Blizzard code that authors quote.
- **[REPORTED]** means an addon author or user reported it in a PR, issue or doc. It is not independently verified.
- **[SPECULATIVE]** means it is my inference or an unverified claim.

**Method for [DIFF] items.**
- I shallow-cloned `Gethe/wow-ui-source` branches `forever` (head commit "1.60.1 (70790)", 2026-11-04) and `live` (head "12.1.5 (70783)", 2026-11-04) — https://github.com/Gethe/wow-ui-source/tree/forever and https://github.com/Gethe/wow-ui-source/tree/live.
- I downloaded `Ketho/BlizzardInterfaceResources` `Resources/*.lua` from branches `forever` (head "1.60.1 (70532)", 2026-10-21) and `live` (head "12.1.5 (70448)", 2026-10-22) — https://github.com/Ketho/BlizzardInterfaceResources/tree/forever and https://github.com/Ketho/BlizzardInterfaceResources/tree/live. I set-diffed GlobalAPI, Events, Templates, FrameXML, Mixins, WidgetAPI and AtlasInfo.
- The live client is build 70790. It went live 2026-11-04 ("launched 2026-11-04 as build `1.60.1.70790`, product `wowf`, installed in `_forever_`") — https://github.com/Cidan/BetterBags/blob/HEAD/.claude/rules/camelot-forever.md

---

## Q1. Which globals, C_ namespaces and functions exist on one client but not the other? Is there a published diff?

### Takeaway
At the C API level, Forever is a near-superset of Retail 12.1.5. The Ketho dumps show 181 global functions on Forever only and just 7 on Retail only. Every C_ namespace an Ace3/LibKa0s addon normally touches has the same function count on both clients.

The real porting hazards sit elsewhere:
- functions Retail already removed, such as `SetDesaturation`, which Retail 12.1.0 removed too;
- deprecation shims gated to the `standard` game type, such as `GetSpecialization`;
- version-number and project-ID detection.

There is a published diff: warcraft.wiki.gg "Patch 1.60.1/API changes", which compares 12.1.5 (69952) with 1.60.1 (70205).

### Cited Findings

**Published diffs and data sources**
- **[SOURCE] The wiki publishes a diff.** warcraft.wiki.gg has a Forever API diff page with the heading "12.1.5 (69952) → 1.60.1 (70205) Oct 2 2026". It counts Global API +176 / −10 and FrameXML +471 / −1041. It states that the Midnight addon "disarmament changes… including secrets, will also be active in Forever." — [Patch 1.60.1/API changes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes)
- **[DIFF] Ketho's resources carry a `forever` branch.** They track 1.60.1 builds, so per-flavour global lists exist — [BlizzardInterfaceResources forever](https://github.com/Ketho/BlizzardInterfaceResources/tree/forever)
- **[DIFF] Gethe wow-ui-source has a `forever` branch** alongside `live`, `ptr`, `beta`, `classic*` and others. It is updated per build (70755 on 2026-11-03, 70790 on 2026-11-04) — [Gethe forever](https://github.com/Gethe/wow-ui-source/tree/forever)

**Ketho dump counts and differences**
- **[DIFF] Ketho set-diff counts, forever (70532) vs live (70448):**
  - GlobalAPI: 7087 vs 6913 (181 Forever-only, 7 Live-only)
  - Events: 1814 vs 1784 (33 Forever-only, 3 Live-only)
  - Templates: 6016 vs 5683 (401 / 68)
  - FrameXML globals: 5782 vs 6366 (473 Forever-only, 1057 Live-only)
  - Mixins: 3531 vs 3287 (268 / 24)
  - WidgetAPI: 1058 vs 1051 (7 Forever-only, 0 Live-only)

  Source: [forever GlobalAPI.lua](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/GlobalAPI.lua), [live GlobalAPI.lua](https://github.com/Ketho/BlizzardInterfaceResources/blob/live/Resources/GlobalAPI.lua)
- **[DIFF] The 7 Live-only globals are** `AbandonSkill`, `BNSetBlocked`, `C_PaperDollInfo.CanCursorCanGoInSlot`, `C_TransmogOutfitInfo.GetWeaponOptionsForSlot`, `C_TransmogOutfitInfo.SetViewedWeaponOptionForSlot`, `GetPetFoodTypes` and `SetBarSlotFromIntro`. Most were moved into namespaces on Forever:
  - `C_SkillInfo.AbandonSkill`
  - `C_BattleNet.SetBlocked`
  - `C_PaperDollInfo.CursorCanGoInSlot`
  - `C_TransmogOutfitInfo.GetOptionsForSlot` / `SetViewedOptionForSlot`
  - `C_PetInfo.GetPetFoodTypes`
  - `C_SpellBook.SetBarSlotFromIntro`

  Source: [Ketho forever GlobalAPI](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/GlobalAPI.lua)
- **[DIFF] Forever-only globals (selection relevant to addons):**
  - Game rules: `C_GameRules.GetForeverExperiencePreset`, `C_GameRules.IsHardcoreActive`, `C_GameRules.IsSelfFoundAllowed`
  - Swing timer: `C_SwingTimer.EnableRangeCheck`, `C_SwingTimer.IsTargetWithinSwingRange`
  - Skills: `C_SkillInfo.GetNumSkillLines` / `GetSkillLineInfo` / `GetSkillLineInfoByID`
  - Pets: `C_PetInfo.GetPetHappiness` / `GetPetLoyalty` / `GetPetTrainingPoints`, `C_StableInfo.*`
  - Specs: `C_SpecializationInfo.GetAllClassIDs` / `SetActiveSpecGroup` / `HasPlayerEarnedATalentPoint`
  - Traits: `C_Traits.GetGroupCurrencyInfo` / `GetMaxAvailableTraitCurrency`
  - Bank: `C_Bank.ShouldUsePlayerBagsInBank`, `C_Bank.FetchMaxNumBankTabs`, `ReagentsFromBankAllowed`
  - Spells and items: `C_Spell.GetItemCooldown`, `C_Spell.CancelItemTempEnchantment`, `C_Item.GetWeaponEnchantInfo`, `C_Item.DeleteItem`
  - Other C_ functions: `C_LFGListRoles.GetRoles` / `SetRoles`, `C_QuestLog.IsEliteQuest`, `C_CVar.SetTempCVar`
  - Plain globals: `UnitUsesAmmo`, `UnitResistance`, `UnitDefenseSkill`, `RegionalUniqueNamesEnabled`, `UIReload`, `ToggleSit`, `IsCursorVisible`
  - Gamepad: `C_GamepadUI.*` and `C_GamepadTargeting.*`

  Source: [Ketho forever GlobalAPI](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/GlobalAPI.lua)
- **[DIFF] Namespace counts in Ketho GlobalAPI, forever / live:**

  | Namespace | Forever | Live |
  |---|---|---|
  | C_AddOns | 29 | 29 |
  | C_Timer | 4 | 4 |
  | C_Container | 47 | 47 |
  | C_UnitAuras | 38 | 38 |
  | C_TooltipInfo | 82 | 82 |
  | C_LFGList | 88 | 88 |
  | C_LootHistory | 5 | 5 |
  | C_DamageMeter | 8 | 8 |
  | C_CooldownViewer | 7 | 7 |
  | C_ChallengeMode | 29 | 29 |
  | C_MythicPlus | 21 | 21 |
  | C_ClassTalents | 31 | 31 |
  | C_TransmogOutfitInfo | 67 | 67 |
  | C_Housing | 62 | 62 |
  | C_EncounterTimeline | 34 | 34 |
  | C_CombatLog | 11 | 11 |
  | C_Secrets | 27 | 27 |
  | C_EncodingUtil | 10 | 10 |
  | C_Spell | 71 | 65 |
  | C_Item | 121 | 118 |
  | C_Bank | 26 | 23 |
  | C_SpecializationInfo | 31 | 26 |
  | C_GameRules | 29 | 22 |
  | C_EditMode | 12 | 11 |
  | C_SwingTimer | 2 | 0 |

  Neither client has `C_Seasons` or `C_Engraving`. Source: [Ketho forever](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/GlobalAPI.lua) / [live](https://github.com/Ketho/BlizzardInterfaceResources/blob/live/Resources/GlobalAPI.lua)
- **[DIFF] WidgetAPI.** The 7 Forever-only widget methods are `FocusEnter`, `FocusExit`, `MouseDown`, `MouseUp`, `SetModelByUnitCreatureDisplayID`, `SetUsingSoftCursor` and `UpdateMouseoverAtPoint`, which are gamepad and soft-cursor related. No widget method is missing on Forever. `Texture:SetDesaturation` and `SetDesaturated` exist on both — [Ketho forever WidgetAPI](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/WidgetAPI.lua)

**SetDesaturation**
- **[SOURCE] Retail removed the global `SetDesaturation` in 12.1.0, so this gap is not specific to Forever.** It appears in the FrameXML "Removed" list of Patch 12.1.0 (link target `townlong-yak.com/framexml/12.0.7/go/SetDesaturation`) — [Patch 12.1.0/API changes](https://warcraft.wiki.gg/wiki/Patch_12.1.0/API_changes)
- **[SOURCE] Ace3 fixed it upstream on 2026-06-20** in commit 6229eda9, "AceGUI-3.0/widgets/AceGUIWidget-CheckBox: Fix setting desaturation on WoW 12.1". It raised CheckBox from 26 to 27 and replaced `SetDesaturation(check, x)` with `check:SetDesaturated(x)`. It shipped in Ace3 tag Release-r1403 — [Ace3 commit 6229eda9](https://github.com/WoWUIDev/Ace3/commit/6229eda9)
- **[DIFF] Neither the forever nor the live source defines `function SetDesaturation`.** The only remaining hits are the `Texture:SetDesaturation` method docs — [Gethe live](https://github.com/Gethe/wow-ui-source/tree/live) / [forever](https://github.com/Gethe/wow-ui-source/tree/forever)
- **[DIFF] The owner's vendored copy is CheckBox Version 26, which still calls the global** (`AuraMaster/libs/AceGUI-3.0/widgets/AceGUIWidget-CheckBox.lua:4,100-130`, local file).

**Retail-era removals Forever shares**

Forever is a 12.1.5 fork, so every removal Retail made in 11.x and 12.x applies there too.
- **[REPORTED]** The removed globals, with their replacements:
  - `GetSpellInfo` → `C_Spell.GetSpellInfo` (returns a table)
  - `GetItemInfo` / `GetItemInfoInstant` → `C_Item.*`
  - `UnitAura` → `C_UnitAuras.*`
  - `GetContainerItemInfo` → `C_Container.*`
  - `IsAddOnLoaded` / `GetAddOnMetadata` → `C_AddOns.*`
  - `GetMouseFocus` → `GetMouseFoci()`
  - `EasyMenu` → `MenuUtil`
  - `GetQuestLogTitle` → `C_QuestLog`
  - `CombatLogGetCurrentEventInfo` has no replacement

  Source: [ForeverPlusPlus docs/forever-api.md](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md)
- **[REPORTED]** More removals: `GetItemQualityColor`, `GetDetailedItemLevelInfo` and `GetItemIcon` moved to `C_Item.*`. `InterfaceOptionsFrame_OpenToCategory` became `Settings.OpenToCategory`. `NUM_ITEM_QUALITIES` is undefined. `MouseIsOver` is gone, so use `Region:IsMouseOver()` — [Auctioneer-Forever README](https://github.com/NoobyGains/Auctioneer-Forever). Retail 12.1.0 also lists `MouseIsOver` as removed — [Patch 12.1.0/API changes](https://warcraft.wiki.gg/wiki/Patch_12.1.0/API_changes)
- **[REPORTED]** `GetItemSpell`, `GetItemInfoInstant`, `IsSpellKnown`, `IsSpellKnownOrOverridesKnown` and `ActionButton_ShowOverlayGlow` / `HideOverlayGlow` were nil on Forever and needed `C_Item` / `C_SpellBook` wrappers — [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1)
- **[REPORTED]** The global `GetItemStats` is gone. `C_Item.GetItemStats` returns `ITEM_MOD_*` keys. `CHAT_TIMESTAMP_FORMAT` gave way to `ChatFrameUtil.GetTimestampFormat()` (unverified) — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md)
- **[REPORTED]** `EquipmentManager_UnpackLocation` is absent; only `EquipmentManager_GetLocationData`, the Midnight API, exists — [BetterBags camelot-forever.md §6](https://github.com/Cidan/BetterBags/blob/HEAD/.claude/rules/camelot-forever.md)

**Deprecation shims**
- **[DIFF] The specialization shim does not load on Forever.** `Blizzard_DeprecatedSpecialization.toc` has `## AllowLoadGameType: classic, standard`, and `standard` is Retail only. The shim defines `GetSpecialization`, `GetSpecializationInfo`, `GetActiveSpecGroup`, `GetNumSpecializationsForClassID`, `GetSpecializationMasterySpells` and `GetTalentInfo`. On Forever, call `C_SpecializationInfo.*` directly — [forever Blizzard_DeprecatedSpecialization](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_DeprecatedSpecialization)
- **[DIFF] The other `Blizzard_Deprecated*` shims load the same way on both clients**, and they still sit behind `GetCVarBool("loadDeprecationFallbacks")`. Forever adds `Blizzard_DeprecatedTransmog` — [forever Blizzard_DeprecatedCombatLog](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_DeprecatedCombatLog/Deprecated_CombatLog.lua)
- **[REPORTED] Contradiction.** ForeverPlusPlus reports in game that `GetSpecializationInfo(1)` on a Warrior returned the class name, and that Forever spec IDs differ from Retail (Warrior 1491) — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md). This conflicts with the shim's TOC gating unless the CVar or another path defines the global; see Gaps. Separately, wowforeverguides lists `GetSpellInfo`, `GetItemInfo`, `GetSpellBookItemName`, `GetNumTalentTabs`, `GetTalentInfo` and `GetNumSkillLines` as missing on build 69913 — [wowforeverguides developers](https://wowforeverguides.com/addons/developers)

**Project constants and Lua environment**
- **[DIFF] Project constants.** `WOW_PROJECT_CAMELOT = 18` and `WOW_PROJECT_ID = WOW_PROJECT_CAMELOT` are defined only in `Blizzard_ProjectConstants/Camelot/ProjectConstants.lua`, which is loaded through `[AllowLoadGameType camelot]`. `WOW_PROJECT_CAMELOT` is nil on Retail — [forever ProjectConstants](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_ProjectConstants)
- **[REPORTED] Before build 70170 (or 70205), `WOW_PROJECT_ID` was 1, the Mainline value** — [BetterBags](https://github.com/Cidan/BetterBags/blob/HEAD/.claude/rules/camelot-forever.md), [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1)
- **[REPORTED] The Lua environment is standard WoW Lua 5.1:** no `require`, `io` or `os`, and the `bit` library is available — [wowforeverguides developers](https://wowforeverguides.com/addons/developers)

### Inferences
- **[SPECULATIVE] The owner's checkbox failure is probably latent on Retail too.** `SetDesaturation` left Retail in 12.1.0, and the vendored CheckBox is v26. AceGUI keeps the highest registered widget version, so Retail likely works only because another installed addon ships CheckBox v27 or newer. The fix is the same everywhere: re-vendor Ace3 r1403 or newer, or add a LibKa0s Compat global shim.
- Ketho's GlobalAPI list does not list `SetDesaturation` on either branch, because it is a FrameXML function and not a C function. A "globals missing on Forever" audit must therefore use both GlobalAPI.lua and FrameXML.lua, and both have blind spots for functions Retail removed.
- Forever is newer than Retail 12.1.5 in places. For example, it adds the `FrameStrata` secret aspect (see Q3). Retail will probably converge on Forever in 12.2, so features found on Forever only may be Retail's next step.

### Gaps
- I could not reconcile the `GetSpecializationInfo` in-game report with the shim's `classic, standard` TOC gate. Someone needs to test it in the client: `/dump GetSpecializationInfo`.
- I did not read the full 263k-character wiki diff (only the first 100k). Its Removed lists for globals and events may name more items.

---

## Q2. Which FrameXML/SharedXML pieces differ (templates, Settings, compartment, Edit Mode, menus, tooltips, fonts, atlases, keybindings)?

### Takeaway
The shared UI frameworks an Ace3/LibKa0s addon builds on are all present on Forever with the same entry points:
- Settings
- `MenuUtil` / `Menu`
- `UIDropDownMenu`
- `TooltipDataProcessor`
- `BackdropTemplate`
- `UIPanelButtonTemplate`
- `AddonCompartmentFrame`
- `EditModeManagerFrame`
- `SettingsPanel`

The differences are skinning. Camelot has overrides for NineSlice, UIPanelTemplates and Menu.xml, so frame chrome is re-drawn, and gamepad "SmartNavigation" hooks are added. Several whole Blizzard UI addons are not loaded, or are swapped for other frames: the group finder, Encounter Journal, Challenges/M+ UI, PvP UI, Garrison, Housing and the Expansion landing page.

### Cited Findings

**How Forever selects files**
- **[DIFF] Forever's game type is `camelot` and it loads the `[Family]` = Mainline files.** TOC file lines use `[AllowLoadGameType camelot]` / `[ExcludeLoadGameType classic, camelot]` and `[Game]\...` overrides. For example, `Blizzard_UIPanelTemplates.toc` loads `[Family]\UIPanelTemplatesOverrides.xml [ExcludeLoadGameType classic, camelot]` and `[Game]\UIPanelTemplatesOverrides.xml [AllowLoadGameType camelot]` — [forever Blizzard_UIPanelTemplates](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_UIPanelTemplates)
- **[DIFF] The game-type tokens behave like this:** `mainline` includes camelot, `standard` is Retail only, and `classic` does not include camelot. In the forever tree, `AllowLoadGameType` values are `standard` ×29, `mainline` ×26, `standard, camelot` ×11 and `camelot` ×7 — [Gethe forever](https://github.com/Gethe/wow-ui-source/tree/forever). This matches in-game testing: "camelot and mainline load; standard and classic don't" — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md)
- **[DIFF] These Blizzard addon folders contain a `Camelot/` override folder:** SharedXML, UIPanelTemplates, Menu, Settings_Shared, FrameXMLBase, FrameXML, EditMode, Minimap, MicroMenu, ActionBar, UnitFrame, NamePlates, ChatFrame, ChatFrameBase, UnitPopup, ObjectiveTracker, PlayerSpells, SharedTalentUI, Professions, ProfessionsBook, ProfessionsTemplates, AuctionHouseUI, Collections, Communities, FriendsFrame, UIPanels_Game (CharacterFrame, BankFrame), MainMenuBarBagButtons, QueueStatusFrame, StatusTrackingBar, DamageMeter, TokenUI, StableUI, TimeManager, Calendar, WorldMap and others — [Gethe forever AddOns](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns)

**Frameworks present on both clients**
- **[DIFF] Settings API.** `Settings.RegisterCanvasLayoutCategory`, `Settings.RegisterVerticalLayoutCategory`, `Settings.RegisterAddOnCategory` and `Settings.OpenToCategory` are each defined once on both. `Blizzard_Settings_Shared` differs in 16 files, mostly gamepad SmartNavigation, plus `Camelot/NewDefinitions.lua`, `AudioOverrides.lua`, `LanguagesOverrides.lua` and `Blizzard_Settings_PreferredPlaySettings.lua` — [forever Blizzard_Settings_Shared](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_Settings_Shared)
- **[REPORTED] `Settings.OpenToCategory` "errors on Midnight and Forever"** when called from a debug-frame button, so one addon switched to AceConfigDialog — [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1). Auctioneer-Forever uses `Settings.OpenToCategory` successfully — [Auctioneer-Forever](https://github.com/NoobyGains/Auctioneer-Forever). The two reports conflict, probably because of taint or the call context.
- **[DIFF] Addon compartment.** `AddonCompartmentFrame` is a `DropdownButton` with `mixin="AddonCompartmentMixin"`, parented to `MinimapCluster`. It is defined in both `Blizzard_Minimap/Mainline/AddonCompartment.xml` and `Blizzard_Minimap/Camelot/AddonCompartment.xml`, and the Camelot Minimap.lua re-anchors it to `GameTimeFrame` — [forever Blizzard_Minimap](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_Minimap)
- **[DIFF] Menus.** `MenuUtil` (`CreateContextMenu`, `CreateCheckbox`, `CreateRadio`, …) exists on both. `Blizzard_Menu` differs in DropdownButton.lua, Menu.lua, MenuTemplates.lua and MenuUtil.lua, and has a Camelot `Menu.xml`. The legacy `UIDropDownMenu_Initialize` / `UIDropDownMenu_AddButton` exist on both. Forever's `UIDropDownMenu.lua` adds only `SmartNavigation:OnDropDownShown(listFrame)`. `EasyMenu` is defined on neither — [forever Blizzard_Menu](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_Menu), [forever UIDropDownMenu.lua](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_SharedXML/Mainline/UIDropDownMenu.lua)
- **[DIFF] Templates and tooltips.** `BackdropTemplate`, `UIPanelButtonTemplate`, `UICheckButtonTemplate`, `SettingsCheckboxTemplate` and `TooltipDataProcessor` exist on both. Forever adds `CheckboxWithLabelTemplate` (inherits `MinimalCheckboxArtTemplate`) in `Shared/Button/CheckButtonTemplates.xml` — [forever CheckButtonTemplates.xml](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_SharedXML/Shared/Button/CheckButtonTemplates.xml)

**Skinning and layout**
- **[REPORTED] `DefaultPanelFlatTemplate` / `ButtonFrameTemplateNoPortrait` render badly on Camelot.** The NineSlice header art is taller (`Blizzard_SharedXML/Camelot/NineSliceLayoutOverrides.lua`), and Blizzard added a Camelot-only `NineSliceUtil.UpdateCornerCropping`. BetterBags switched to `TooltipBorderedFrameTemplate` — [BetterBags §5](https://github.com/Cidan/BetterBags/blob/HEAD/.claude/rules/camelot-forever.md)
- **[DIFF] Edit Mode.** `EditModeManagerFrame` exists on both, and there is a `Blizzard_EditMode/Camelot/` folder. `Enum.EditModeSystem` on Forever adds `MainActionBarEndCap`, `GroupFinder`, `SwingTimer` and `GamepadMainActionBar` to Retail's list. `C_EditMode.GetEditModeDefaultLayout` is Forever-only — [forever EditModeManagerConstants docs](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_APIDocumentationGenerated)
- **[REPORTED] LibEditMode (MINOR 18) loads on Forever** — [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1)
- **[DIFF] Keybindings.** `Blizzard_Settings_Shared/Blizzard_Keybindings.lua` differs only in whitespace and in gamepad SmartNavigation hooks, so the `Bindings.xml` / `BINDING_HEADER_*` model is unchanged. The forever tree has no separate KeyBinding UI addon, and Retail has none either — [forever Blizzard_Keybindings.lua](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_Settings_Shared/Blizzard_Keybindings.lua)
- **[DIFF] Fonts.** `Blizzard_Fonts_Shared/Shared/GameFonts.xml` on Forever adds font families such as `NumberFont_GameLarge` (FRIZQT__ 14). There were no removals in the part I inspected — [forever GameFonts.xml](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_Fonts_Shared/Shared/GameFonts.xml)
- **[DIFF] Atlases.** Ketho AtlasInfo has about 19,683 names on forever and about 17,611 on live. About 618 names are Live-only: housing, `common-icon-*` (for example `common-icon-copy`, `common-icon-delete`, `common-icon-plus`), `common-dropdown-expand-button`, `UI-RaidFrames-AntCorners`, `128-RedButton-*` and talents. About 2,690 are Forever-only. All 11 atlas names that LibKa0s's own Lua uses exist on Forever (checked locally against the forever list) — [Ketho forever AtlasInfo](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/AtlasInfo.lua)

**Blizzard UI addons absent or swapped on Forever**
- **[DIFF] Group finder.**
  - `Blizzard_GroupFinder` (PVEFrame, LFGListFrame, GroupFinderFrame) has `## ExcludeLoadGameType: camelot`.
  - `Blizzard_GroupFinder_VanillaStyle` (`AllowLoadGameType: classic, camelot`, LoadOnDemand) defines `LFGParentFrame`, `LFGBrowseFrame`, `LFGListingFrame` and `LFGWhoListFrame` instead.

  Source: [forever Blizzard_GroupFinder_VanillaStyle](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_GroupFinder_VanillaStyle)
- **[DIFF] Other addons not loaded on Forever** (TOC gate value in brackets):
  - `Blizzard_EncounterJournal` (standard, classic)
  - `Blizzard_ChallengesUI` (standard, mists)
  - `Blizzard_PVPUI` (excludes camelot)
  - `Blizzard_GarrisonUI` (excludes camelot)
  - `Blizzard_EncounterTimeline`, `Blizzard_EncounterWarnings`, `Blizzard_ExpansionLandingPage`, all `Blizzard_Housing*`, `Blizzard_DelvesToast`, `Blizzard_AccountStore`, `Blizzard_ClassTrial` (all standard)

  Source: [Gethe forever AddOns](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns)
- **[DIFF] Forever-only addons:** `Blizzard_SwingTimer`, `Blizzard_LegacySystem`, `Blizzard_Statistics`, `Blizzard_LegacyChallengeTracker` and the `Blizzard_Gamepad*` set (all camelot), plus `Blizzard_StatusTrackingBar`. Retail-only addons absent from the forever tree are `Blizzard_TalentUI`, `Blizzard_ReforgingUI`, `Blizzard_LevelUpDisplay` and `Blizzard_DeclensionFrameGlue` — [Gethe forever AddOns](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns)
- **[DIFF] Forever uses Camelot variants of these Blizzard frames:** `CharacterFrame`, `BankFrame`, `PlayerSpellsFrame`, `ProfessionsFrame` and `MicroMenu`. Forever also has a classic-style `SpellBookFrame` file set, which Retail lacks — [Gethe forever](https://github.com/Gethe/wow-ui-source/tree/forever)
- **[REPORTED] The Friends window is `SocialUIFrame`, not `FriendsFrame`** — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md)

**Tooltip and colour picker behaviour**
- **[REPORTED] `GameTooltip:SetText(text, r, g, b, a, wrap)` rejects `true` in the alpha slot** ("outside of expected range"). Old AceConfigDialog and TreeGroup passed a boolean there; Ace3 r1403 fixes it — [bestaround-revisited PR #6](https://github.com/puppysnuff/wow-wikr-bestaroundrevisited/pull/6), [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1)
- **[SOURCE] The colour picker treats alpha as non-inverted on Forever, as on Mainline.** Ace3 ColorPicker v29 (2026-10-02) changed `INVERTED_ALPHA = (WOW_PROJECT_ID ~= WOW_PROJECT_MAINLINE and WOW_PROJECT_ID ~= WOW_PROJECT_CAMELOT)` ("Fix alpha being inverted in Forever"). The owner's vendored ColorPicker is v28, which inverts alpha on Forever — [Ace3 commit e37c055f](https://github.com/WoWUIDev/Ace3/commit/e37c055f)

### Inferences
- An addon that hooks or skins `PVEFrame` / `LFGListFrame` / `LFGListSearchPanel_*` will find those frames unloaded on Forever. PremadeGroupsFilterExtension is the obvious Ka0s candidate. The `C_LFGList` C API is still there (88 functions on both), plus the new `C_LFGListRoles`.
- Sizing that relies on the chrome metrics of `ButtonFrameTemplate` / `DefaultPanelFlatTemplate` / `PortraitFrameTemplate` is at risk, because Camelot re-draws the NineSlice. Fully custom-skinned frames are lower risk, and LibKa0s's skin system mostly falls in that group.

### Gaps
- I did not diff the Ka0s addons' full template-inheritance list against Forever Templates.lua. A per-addon `grep inherits=` check against `f_Templates.txt` is the next step.
- I did not see in-client behaviour of `Settings.RegisterAddOnCategory` subcategories on the Camelot SettingsPanel skin.

---

## Q3. Do Midnight 12.0 restrictions (secret values, combat-log and aura restrictions, C_DamageMeter) exist on Forever? What differs in security and taint?

### Takeaway
Yes. The whole secret-value system is on Forever with the same annotations as Retail, and Forever is slightly stricter:
- it adds a `FrameStrata` secret aspect, which makes `GetFrameStrata` return a secret;
- it has a few more `SecretWhenUnitStatsRestricted` / `SecretWhenUnitIdentityRestricted` annotations;
- it marks `C_DamageMeter` `specIconID` as secret where Retail marks it `NeverSecret`.

`COMBAT_LOG_EVENT_UNFILTERED` still exists as an event, but addons receive nothing useful from it.

### Cited Findings
- **[DIFF] Secret annotation counts in the generated API docs, live / forever:**

  | Annotation | Live | Forever |
  |---|---|---|
  | `SecretArguments` | 3867 | 3952 |
  | `Secret` | 950 | 965 |
  | `SecretWhenUnitStatsRestricted` | 50 | 63 |
  | `SecretWhenUnitIdentityRestricted` | 32 | 35 |
  | `SecretWhenUnitAuraRestricted` | 22 | 23 |
  | `SecretWhenUnitSpellCastRestricted` | 21 | 21 |
  | `SecretWhenCooldownsRestricted` | 15 | 15 |
  | `ConditionalSecret` | 20 | 20 |

  Source: [forever APIDocumentationGenerated](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_APIDocumentationGenerated)
- **[DIFF] `UnitHealth` is annotated the same way on Forever** (`SecretReturns = true`, `SecretArguments = "AllowedWhenUntainted"`, unit type `UnitTokenPvPRestrictedForAddOns`) — [forever UnitDocumentation.lua](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_APIDocumentationGenerated/UnitDocumentation.lua)
- **[DIFF] Forever-only `Enum.SecretAspect.FrameStrata` (16777216):** `GetFrameStrata` has `SecretReturnsForAspect = { Enum.SecretAspect.FrameStrata }`, and live has neither — [forever SecretAspectConstantsDocumentation.lua](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_APIDocumentationGenerated/SecretAspectConstantsDocumentation.lua). The wiki agrees: "A new FrameStrata secret aspect was added, and GetFrameStrata now returns a secret value for frames with it" — [Patch 1.60.1/API changes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes)
- **[DIFF] The secret-handling helpers exist on both:** `issecretvalue`, `issecrettable`, `canaccessvalue`, `secretwrap`, `scrub` and `C_Secrets.*` (27 functions). Both clients also have `C_CurveUtil`, `C_DurationUtil` and `C_RestrictedActions` — [Ketho forever GlobalAPI](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/GlobalAPI.lua)
- **[DIFF] The combat log looks identical in source on both clients.** `C_CombatLog` has 11 functions, including `IsCombatLogRestricted`. `COMBAT_LOG_EVENT_UNFILTERED` is documented with `HasRestrictions = true`, `SynchronousEvent = true` and `CallbackEvent = true`. `CombatLogGetCurrentEventInfo` survives only as a deprecation alias for `C_CombatLog.GetCurrentEventInfo` behind `loadDeprecationFallbacks` — [forever CombatLogDocumentation.lua](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_APIDocumentationGenerated/CombatLogDocumentation.lua), [forever Deprecated_CombatLog.lua](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_DeprecatedCombatLog/Deprecated_CombatLog.lua)
- **[REPORTED] In practice:**
  - `COMBAT_LOG_EVENT_UNFILTERED` never fires for addons — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md)
  - Forever never delivers `SPELL_AURA_APPLIED` to addons, so authors moved to `UNIT_AURA` — [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1)
  - `CombatLogGetCurrentEventInfo` is unavailable — [wowforeverguides](https://wowforeverguides.com/addons/developers)
- **[REPORTED] Values seen as secret in game:**
  - the player's mana, out of combat (2026-11-05)
  - the player's own buffs, where reading a secret aura in combat throws (2026-10-14)
  - nameplate aura rows, which are restricted regions
  - friendly health on name-only plates

  Also, `Cooldown:SetCooldown` rejects secret numbers — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md). Unit names may be secret strings, and `UnitCanAttack` / `UnitExists` may return secret booleans — [wowforeverguides](https://wowforeverguides.com/addons/developers)
- **[DIFF] Damage meter and cooldown manager.** `C_DamageMeter` (8 functions) and `DAMAGE_METER_COMBAT_SESSION_UPDATED` exist on Forever. `Blizzard_DamageMeter` and `Blizzard_CooldownViewer` load on camelot (`AllowLoadGameType: standard, camelot`). In `DamageMeterDocumentation.lua` the `specIconID` field is `NeverSecret = true` on live but `SecretValue = true` on forever — [forever DamageMeterDocumentation.lua](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_APIDocumentationGenerated/DamageMeterDocumentation.lua)
- **[DIFF] The restricted (secure-snippet) environment loads on Forever.** `Blizzard_RestrictedAddOnEnvironment.toc` is `AllowLoadGameType: classic, standard, camelot` on forever, against `classic, standard` on live — [forever Blizzard_RestrictedAddOnEnvironment](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_RestrictedAddOnEnvironment)
- **[REPORTED] On early build 69913, secure snippets failed to compile** (`loadstring_untainted` missing), which broke click-casting and action-bar paging. The same report says to avoid `ChatFrame_OpenChat`, `ChatEdit_ActivateChat` and `C_SuperTrack.SetSuperTrackedUserWaypoint` — [wowforeverguides](https://wowforeverguides.com/addons/developers)
- **[REPORTED] Forbidden or tainting actions:**
  - `PickupInventoryItem` is forbidden to addons (build 70338)
  - `C_RecentAllies.TryRequestRecentAlliesData` is forbidden
  - opening Blizzard windows such as the character frame from addon code taints them

  Source: [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md)
- **[SOURCE] Blizzard's own statement, as relayed by others:** "WoW Forever shares Mainline WoW's UI architecture, including the vast majority of APIs available in 12.1.5" (Blizzard representative on the WoW UI Discord, via Wowhead and Icy Veins) — [endgametools](https://endgametools.com/en/wow-forever/news/wow-forever-addons)
- **[REPORTED] GUID server and spawn IDs for creatures, vehicles, pets and game objects are obfuscated** to prevent layer comparison — [Patch 1.60.1/API changes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes)

### Inferences
- An addon that already passes Retail 12.x secret-value testing will mostly pass on Forever. The extra risks are `GetFrameStrata` returning a secret, which matters to Ka0s strata and layout code that reads strata to compare or save it, and a few more unit stats becoming secret.
- I found no Forever-specific taint model. It is the Midnight model, plus whatever Camelot frames are protected.

### Gaps
- Nothing I found says which secret predicates are active outside combat on Forever versus Retail; that depends on server-side game rules. Only in-client testing can answer it.
- I have no source on whether `loadstring_untainted` was restored after build 69913. The RestrictedAddOnEnvironment TOC now allowing camelot suggests it was, but I have not verified that.

---

## Q4. Which events differ?

### Takeaway
The event sets are nearly identical: 33 events are Forever-only and 3 are Retail-only. Every event the question names exists on both clients:
- `COMBAT_LOG_EVENT_UNFILTERED`
- `ENCOUNTER_START` / `ENCOUNTER_END`
- `START_LOOT_ROLL`
- `LOOT_HISTORY_UPDATE_DROP` / `LOOT_HISTORY_UPDATE_ENCOUNTER`
- `CHAT_MSG_LOOT`
- `UNIT_AURA`
- `ADDON_RESTRICTION_STATE_CHANGED`

What differs is payload restriction (CLEU is effectively dead for addons), not whether the event exists.

### Cited Findings
- **[DIFF] All of these appear in the Forever Ketho Events list:** `ADDON_RESTRICTION_STATE_CHANGED`, `CHAT_MSG_LOOT`, `COMBAT_LOG_EVENT`, `COMBAT_LOG_EVENT_UNFILTERED`, `DAMAGE_METER_COMBAT_SESSION_UPDATED`, `ENCOUNTER_START`, `ENCOUNTER_END`, `LOOT_HISTORY_UPDATE_DROP`, `LOOT_HISTORY_UPDATE_ENCOUNTER`, `START_LOOT_ROLL` and `UNIT_AURA` — [Ketho forever Events.lua](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/Events.lua)
- **[DIFF] The 3 Live-only events** are `EXTERNAL_EVENT_LAUNCH_URL_FAILED`, `PET_SPELL_POWER_UPDATE` and `VIEWED_TRANSMOG_OUTFIT_SLOT_WEAPON_OPTION_CHANGED`. Forever has `VIEWED_TRANSMOG_OUTFIT_SLOT_OPTION_CHANGED` and `EXTERNAL_EVENT_LAUNCH_URL_RESULT` instead — [Ketho live Events.lua](https://github.com/Ketho/BlizzardInterfaceResources/blob/live/Resources/Events.lua)
- **[DIFF] The 33 Forever-only events include:**
  - combat and pets: `PLAYER_SWING`, `PLAYER_SWING_RANGE_UPDATE`, `UNIT_HAPPINESS`, `UNIT_PET_TRAINING_POINTS`, `PET_STATS_UPDATE`
  - chat and collections: `CHAT_MSG_COLLECTED_APPEARANCE`
  - game rules and world: `GAME_RULES_CHANGED`, `DIEL_CYCLE_CHANGED`
  - group finder: `LFG_LIST_ROLE_UPDATE`, `LFG_LIST_SHOW_SEARCH`
  - mail: `MAIL_OPEN_ALL_CANCELED`, `SECURE_TRANSFER_CONFIRM_TAKE_MAIL_MONEY`
  - PvP: `PLAYER_PVP_FLAG_CHANGED`
  - shard transfer: `SHARD_TRANSFER`, `SHARD_TRANSFER_IMMINENT`, `SHARD_TRANSFER_CANCELLED`
  - input: `GLOBAL_REGION_MOUSE_DOWN` / `UP`, `INPUT_DEVICE_INTERFACE_TRANSITION`, the gamepad stance and possess events
  - voice chat: the voice-provider and Discord events
  - BlizzCon: `BC_26_*`

  Source: [Ketho forever Events.lua](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/Events.lua)
- **[REPORTED] `COMBAT_LOG_EVENT_UNFILTERED` never fires for addons** — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md). **[REPORTED]** One port registers CLEU only inside a pcall and only where `CombatLogGetCurrentEventInfo` exists — [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1)
- **[REPORTED] `COMBAT_LOG_EVENT_UNFILTERED` "throws an error on Midnight"** (Retail), so the behaviour matches — [wowforeverguides](https://wowforeverguides.com/addons/developers)

### Inferences
- Ka0s Drop Watcher and LootHistory rely on `START_LOOT_ROLL`, `LOOT_HISTORY_*`, `CHAT_MSG_LOOT` and `C_LootHistory`. These exist with the same function count. The Camelot loot rules are a separate question: Forever has `LootConsts_Camelot`, and the Mainline `LootConsts.MasterLootQualityThreshold` constant is absent from the shared docs. See Q5.

### Gaps
- I did not compare event payload signatures (arguments) between the clients. Only name sets were diffed. Payload differences, for example a secret argument on `CHAT_MSG_*` (`SecretInChatMessagingLockdown`: 99 live vs 100 forever), need a per-event doc diff.

---

## Q5. Which game-system differences affect addons?

### Takeaway
Forever is a Retail engine running Wrath-era-style game rules. Systems that differ:
- **Talents:** trait config `CamelotCombat`, spec IDs that differ from Retail, and a talent-tree layout of trait groups as tabs.
- **Bank:** 9 character + 9 account tab enums, but no Warband bank in practice, plus a keyring at bag −1.
- **Group finder:** the Vanilla-style UI, not PVEFrame.
- **Missing UIs:** no Encounter Journal, no M+ Challenges UI, no PvP UI, no Housing or Garrison.
- **Character identity:** a regional unique name plus surname, keyed by ruleset rather than realm.
- **Added systems:** pet happiness and loyalty, ammo, a swing timer.

### Cited Findings

**Talents and specs**
- **[DIFF] The talent system adds Camelot-specific types:** `Enum.TraitConfigType.CamelotCombat` and `GenericTraitFrameLayoutOptions.CamelotLegacy` appear in the forever source, and there is a Camelot `Blizzard_PlayerSpells/Camelot/Blizzard_PlayerSpellsFrame.xml` — [Gethe forever](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_PlayerSpells)
- **[REPORTED] Spec IDs differ from Retail** (Warrior 1491), and talent points live in a `CamelotCombat` config (type 4) with trait groups as tabs — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md). **[REPORTED]** LibDualSpec-1.0 v1.35.0 uses talent-group profiles on Forever — [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1)

**Bank and bags**
- **[REPORTED] Bank tabs.** `Enum.BagIndex` has `CharacterBankTab_1..9` (bag IDs 6..14) and `AccountBankTab_1..9` (15..23), where Retail has 6 + 5, and there is no `Enum.BagIndex.Bank`. There is no Warband bank in practice, even though the enum declares one. `Keyring = -1` is a working keyring. `BankPanel.Header` and `BankPanel.AutoDepositFrame` do not exist. `C_Bank.FetchPurchasedBankTabData`, `BankPanel:SetBankType` and `BankPanelPurchaseButtonScriptTemplate` behave as on Retail — [BetterBags §2–§4, §7](https://github.com/Cidan/BetterBags/blob/HEAD/.claude/rules/camelot-forever.md)
- **[DIFF] Forever-only bank globals:** `C_Bank.ShouldUsePlayerBagsInBank`, `C_Bank.FetchMaxNumBankTabs`, `C_Bank.BankBagTypeAndIDToInvSlot` and `ReagentsFromBankAllowed`. There is also a Camelot `BankFrame.xml` — [Ketho forever GlobalAPI](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/GlobalAPI.lua)

**Group finder and Mythic+**
- **[DIFF] Group finder.** The Vanilla-style LFG UI is used (see Q2), with Forever-only `C_LFGListRoles.*` and the events `LFG_LIST_ROLE_UPDATE` / `LFG_LIST_SHOW_SEARCH`. `C_LFGList` keeps 88 functions — [forever Blizzard_GroupFinder_VanillaStyle](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_GroupFinder_VanillaStyle)
- **[DIFF] Mythic+.** `C_ChallengeMode` (29) and `C_MythicPlus` (21) exist, but `Blizzard_ChallengesUI` does not load on camelot. `Blizzard_LegacyChallengeTracker` is camelot-only — [Gethe forever AddOns](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns). **[REPORTED]** Retail-only namespaces such as `C_MythicPlus`, `C_Housing` and `C_LFGList` "exist, but their content may be off" (untested) — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md)

**Encounter Journal and game rules**
- **[REPORTED] The beta game rules `EncounterJournalDisabled`, `DisableCampsites` and `TransmogEnabled = 0` are reported active.** `C_GameRules.IsGameRuleActive` drives ruleset profiles — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md). **[DIFF]** `Blizzard_EncounterJournal` does not load on camelot — [Gethe forever](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_EncounterJournal)

**Character identity and saved data**
- **[SOURCE] Names are unique per region, carry a surname, and are keyed by ruleset.**
  - AceDB-3.0 now builds keys differently when `RegionalUniqueNamesEnabled()` (Forever-only) is true. `realmKey` becomes "Hardcore", "RP-PvP", "RP", "PvP" or "PvE" from `C_GameRules.IsGameRuleActive(Enum.GameRule.*Ruleset)`, and `charKey = name .. " " .. tostring(surname)` with no realm suffix, using `UnitNameUnmodified`.
  - These changes ran from AceDB MINOR 36 (2026-09-18) to 40 (2026-10-28). The owner's vendored AceDB is MINOR 33.

  Source: [Ace3 commit 1e98fc00](https://github.com/WoWUIDev/Ace3/commit/1e98fc00), [afabc91e](https://github.com/WoWUIDev/Ace3/commit/afabc91e), [ac3d1225](https://github.com/WoWUIDev/Ace3/commit/ac3d1225)
- **[REPORTED] `UnitName` returns a surname as its second value.** One ruleset realm spans several realm IDs in GUIDs, so data should be keyed by realm name — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md). DBM reads the player name with `GetUnitName("player")` on Forever and `UnitName("player")` elsewhere — [DBM GameVersion.lua](https://github.com/DeadlyBossMods/DeadlyBossMods/blob/HEAD/DBM-Core/modules/objects/GameVersion.lua)

**Auction house, professions, transmog and Wrath-era systems**
- **[DIFF] Auction house.** `Blizzard_AuctionHouseUI` loads (mainline) with Camelot overrides. `C_AuctionHouse` has 86 functions on Forever against 85 on Retail; the extra one is `GetItemKeySampleLink`. `C_WowTokenUI.ShouldDisplayInAuctionHouse` is Forever-only — [Ketho forever GlobalAPI](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/GlobalAPI.lua). **[REPORTED]** The first `SearchForItemKeys` call with new keys returned empty rows — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md)
- **[DIFF] Professions.** `Blizzard_Professions` (mainline) has a Camelot `ProfessionsFrame`. `C_TradeSkillUI` has 146 functions against 145 (`CanTradeSkillShowCraftingUI` added). **[REPORTED]** Classic `GetNumCrafts` / `GetNumTradeSkills` are absent — [Auctioneer-Forever](https://github.com/NoobyGains/Auctioneer-Forever)
- **[DIFF] Transmog and outfits.** `C_TransmogOutfitInfo` has 67 functions on both, but the weapon-option functions are renamed. `Blizzard_DeprecatedTransmog` exists on Forever only — [Ketho forever GlobalAPI](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/GlobalAPI.lua)
- **[DIFF] Wrath-era systems Forever adds:**
  - pet happiness, loyalty and training points: `C_PetInfo`, `UNIT_HAPPINESS`
  - ammo: `UnitUsesAmmo`, `C_PaperDollInfo.AmmoNeeded`
  - classic stat functions such as `GetArmorPenetration`, `GetHealthRegenFromSpirit` and `GetManaRegenFromSpirit`
  - a swing timer: `C_SwingTimer`, `PLAYER_SWING`
  - skills: `C_SkillInfo`
  - quest timers: `C_QuestLog.GetQuestTimers`

  Source: [Ketho forever GlobalAPI](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/GlobalAPI.lua)
- **[REPORTED] Hit and similar gear stats are ratings that tooltips show as a percentage** (unverified) — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md)

### Inferences
- **[SPECULATIVE] AceDB profile keys differ on Forever.** Ka0s addons that use AceDB character, realm or faction-realm profile keys will produce different keys on Forever once AceDB is MINOR 36 or newer. On the vendored MINOR 33 they will use `GetRealmName()` plus `UnitName`, which may collide or change when a surname is present.
- Any Ka0s code that hard-codes bank tab counts, Warband bank (`Enum.BankType.Account`) or `Enum.BagIndex.Bank` needs enum-driven sizing.

### Gaps
- The loot-system rules (master loot, personal loot, need/greed) on Camelot are not documented. I found only `LootConsts_Camelot` in source and did not read its values.

---

## Q6. Known breakages reported by authors, and how Ace3, LibStub, LibSharedMedia, LibDBIcon/LDB and AceGUI handle Forever

### Takeaway
Ace3 upstream (WoWUIDev/Ace3) supports Forever actively. The relevant releases and commits:
- **r1403 (2026-08-12):** CheckBox v27 (the `SetDesaturation` fix) and the tooltip alpha fix.
- **ColorPicker v29 (2026-10-02):** recognises `WOW_PROJECT_CAMELOT`.
- **AceDB MINOR 36–40 (2026-09-18 to 2026-10-28):** Forever character and realm keys.

The failures authors report fall into four groups:
- 16001 being read as "Classic";
- `WOW_PROJECT_ID ~= WOW_PROJECT_MAINLINE` checks;
- TOC suffix selection;
- old vendored Ace3.

### Cited Findings

**Ace3 and AceGUI**
- **[SOURCE] Ace3 commits related to Forever, newest first** — [Ace3 commits](https://github.com/WoWUIDev/Ace3/commits/master):
  - 2026-10-28 ac3d1225 "AceDB-3.0: Recognize RP-PVP for Forever realms"
  - 2026-10-02 e37c055f "AceGUI-3.0: ColorPicker: Fix alpha being inverted in Forever"
  - 2026-09-25 afabc91e / 5e2e0d3b / a2e7e286 / b1c72f24: AceDB Forever naming
  - 2026-09-18 1e98fc00 "AceDB-3.0: Compatibility with WoW Forever"
  - 2026-08-26 a29b0caa "AceGUIWidget-Heading: Support secret text"
  - 2026-08-05 d96aeae0 "Ignore secret values in ChatThrottleLib hooks"
  - 2026-06-20 6229eda9, the CheckBox desaturation fix
- **[REPORTED] Addons hit by old AceGUI copies:** RangeDisplay, Mechanic and BarShelf. Which copy's error appears depends on which addon loads its AceGUI first — [search summary of wowace RangeDisplay and others](https://www.wowace.com/projects/range-display)
- **[REPORTED] Re-vendoring Ace3 r1403 fixed the CheckBox `SetDesaturation` error and the `GameTooltip:SetText` alpha error on the 1.60 client** — [bestaround-revisited PR #6](https://github.com/puppysnuff/wow-wikr-bestaroundrevisited/pull/6), [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1)

**LibSharedMedia, LibDualSpec, LibEditMode, LibDBIcon and LibDataBroker**
- **[REPORTED] LibSharedMedia-3.0 v12.1.0 replaced its `WOW_PROJECT_ID == WOW_PROJECT_MAINLINE` check with `C_UIFileAsset.IsKnownFile`.** The old check treated Forever as Classic. `C_UIFileAsset.IsKnownFile` exists on both clients — [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1), [Ketho forever GlobalAPI](https://github.com/Ketho/BlizzardInterfaceResources/blob/forever/Resources/GlobalAPI.lua). The owner's vendored LSM is MINOR 12000001 and contains no project check (local file).
- **[REPORTED] LibDualSpec-1.0 v1.35.0 and LibEditMode MINOR 18 work on Forever** — [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1)
- **[DIFF] LibDBIcon has its compartment target on Forever.** It captures `AddonCompartmentFrame` as an upvalue, and that frame exists on Forever (Camelot variant) — [forever Blizzard_Minimap](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_Minimap). I found no Forever-specific LibDBIcon or LibDataBroker change, and no source reporting breakage.
- **[REPORTED] LibUIDropDownMenu detects Forever as `projectID == WOW_PROJECT_MAINLINE` with a 1.x interface,** so from build 70170 it matches none of its flavour modes; an upstream fix is needed — [BetterBags §1](https://github.com/Cidan/BetterBags/blob/HEAD/.claude/rules/camelot-forever.md)

**Flavour detection and TOC loading**
- **[REPORTED] Treating 16001 as "Classic" breaks addons.** Enchantrix did so and then called `GetNumCrafts` / `GetNumTradeSkills` — [Auctioneer-Forever](https://github.com/NoobyGains/Auctioneer-Forever). CDTL3 added `isForever` / `retailAPI` gates for the same reason — [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1). BetterBags sent Forever down the pre-Midnight `EquipmentManager_UnpackLocation` path because the TOC number is below 120000 — [BetterBags §6](https://github.com/Cidan/BetterBags/blob/HEAD/.claude/rules/camelot-forever.md)
- **[REPORTED] `isRetail = (WOW_PROJECT_ID == WOW_PROJECT_MAINLINE)` went false after build 70170 and crashed BetterBags** at load ("table index is nil"). The recommended detection is `isCamelot = WOW_PROJECT_CAMELOT ~= nil and WOW_PROJECT_ID == WOW_PROJECT_CAMELOT`, with retail code paths taken when the project is Mainline or Camelot — [BetterBags §1](https://github.com/Cidan/BetterBags/blob/HEAD/.claude/rules/camelot-forever.md). DBM uses `WOW_PROJECT_ID == (WOW_PROJECT_CAMELOT or 18)` — [DBM GameVersion.lua](https://github.com/DeadlyBossMods/DeadlyBossMods/blob/HEAD/DBM-Core/modules/objects/GameVersion.lua)
- **[REPORTED] TOC suffix selection:**
  - Forever loads `_Camelot.toc` over `_Mainline.toc`. One author found no fallback to `_Mainline`, and another reported that the precedence changed between builds — [cdtl3-dev PR #1](https://github.com/Nelnamara/cdtl3-dev/pull/1), [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md)
  - **[SOURCE]** `_Forever` is accepted as an alias of `_Camelot` (TOC suffix, `[Game]` variable, folder lookup), and a `forever` TOC game type was added — [Patch 1.60.1/API changes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes)
- **[REPORTED] SavedVariables were written but not read back on 2026-09-23;** this was fixed by 2026-09-24 — [ForeverPlusPlus](https://github.com/xIGBClutchIx/ForeverPlusPlus/blob/main/docs/forever-api.md). **[REPORTED]** Addon and interface settings reset after a full restart (open since 2026-09-18) — [endgametools](https://endgametools.com/en/wow-forever/news/wow-forever-addons)

**Large addons and other projects using `WOW_PROJECT_CAMELOT`**
- **[REPORTED] Status of large addons as of 2026-11-06:**
  - Questie: Forever support since 12.0.1 (`Questie_Camelot.toc`)
  - DBM: since 12.1.10
  - Details!: Forever work since 2026-09-24
  - Leatrix Plus, Auctionator, TomTom and Bartender4: Forever files
  - WeakAuras: no Forever version (5.22.1)

  Source: [endgametools](https://endgametools.com/en/wow-forever/news/wow-forever-addons)
- **[DIFF] GitHub code search shows `WOW_PROJECT_CAMELOT` in:** Ace3, ElvUI (Initialize.lua, oUF init, LibActionButton, its ColorPicker fork), DBM, Details, Dominos, GW2_UI, RealUI, Total RP 3, SpartanUI, HereBeDragons and GatherMate2 (`.luacheckrc`), Questie (LibUIDropDownMenu), XLoot, RaiderIO, Clicked, ConsolePort, KethoDoc and simc-addon — [GitHub code search](https://github.com/search?q=WOW_PROJECT_CAMELOT&type=code)

### Inferences
- The Ka0s vendored stack (AceGUI CheckBox v26, ColorPicker v28, AceDB MINOR 33) predates every Ace3 Forever fix. Re-vendoring Ace3 at or after commit ac3d1225 (2026-10-28) is the cheapest single fix. LibKa0s Compat should own flavour detection, using the `WOW_PROJECT_CAMELOT ~= nil` guard, and should never branch on the 16001 number.

### Gaps
- No Ace3 release tag after Release-r1403 contains the AceDB and ColorPicker Forever fixes; they are on master only. Check before re-vendoring whether a tagged release exists.
- I found no public WoWUIDev Discord summary and no Blizzard UI & Macro forum thread that lists API differences.
- The ElvUI, Plater and BigWigs Forever changes were not read in detail.
