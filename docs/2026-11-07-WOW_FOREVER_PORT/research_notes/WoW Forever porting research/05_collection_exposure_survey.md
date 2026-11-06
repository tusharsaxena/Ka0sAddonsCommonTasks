# Collection exposure survey: what a WoW:F port would touch (local codebase research)

Method. I read the code read-only on 2026-11-07. Every repo was on `master` at its current HEAD. Paths are relative to
`/mnt/d/Profile/Users/Tushar/Documents/GIT/`, and the sources are local files cited as `path:line`. I also read two GitHub
issues through `gh api`. The owner's WoW:F install was listed read-only for corroboration (third-party addons only); nothing
there was changed. Counts are grep counts over non-comment lines of **production code**: each addon's `.lua`/`.xml`
excluding `libs/`, `tests/`, `docs/`, `_dev/`, `tools/`, `media/`, and PrettyChat's `GlobalStrings/` data dump. LibKa0s is
counted over its payload folder `LibKa0s/LibKa0s/`. A count is a call-site-line count, not a distinct-API count.

Naming trap for the report writer. In LibKa0s, **"WoW Forever" is also the name of a skin** (`LibKa0s/LibKa0s/SkinDefsOthers.lua:750-757`,
`LibKa0s/LibKa0s/SkinDefs.lua:3`, `LibKa0s/LibKa0s/Media.lua:151,288`). Nearly every "Forever" hit in LibKa0s and its tests is
the skin, not the client. The standard draws the distinction explicitly: *"The WoW Forever skin is a look usable on retail
… Running Ka0s addons on the WoW Forever client itself is not supported"* (`WowAddonStandards/standards/standards/open-evolutions.md:349-352`).

---

## Q1. TOC files, Interface lines, flavours, packager files, tag format

### Takeaway
Every roster addon ships **exactly one TOC**, `<Folder>.toc`. Its line 1 is the single value `## Interface: 120105`, and none of them
has a flavour line, a comma list, a per-flavour TOC or an `AllowLoadGameType`. Each addon has a `.pkgmeta` with no `enable-toc-creation`,
and no repo has a `.github/workflows`. Release tags are `X.Y.Z-release`. LibKa0s has no TOC and uses `vX.Y.Z` tags.

### Cited Findings
| Addon | TOC | `## Interface:` | Version | CurseForge ID | `.pkgmeta` | `Bindings.xml` | Newest tags |
|---|---|---|---|---|---|---|---|
| AbsorbTracker | `AbsorbTracker.toc` | `120105` (l.1) | 1.12.0 | 1450165 | yes (33 l.) | no | 1.12.0-release, 1.11.0-release |
| AuraMaster | `AuraMaster.toc` | `120105` | 1.1.0 | 1698345 | yes | no | 1.1.0-release |
| BankLedger | `BankLedger.toc` | `120105` | 1.3.0 | 1629058 | yes | yes | 1.3.0-release |
| ConsumableMaster | `ConsumableMaster.toc` | `120105` | 1.8.0 | 1522944 | yes | no | 1.8.0-release |
| DpsRace | `DpsRace.toc` | `120105` | 0.1.0 | none (unpublished) | yes | yes | no tags |
| DropWatcher | `DropWatcher.toc` | `120105` | 1.1.0 | 1748054 | yes | yes | 1.1.0-release |
| KickCD | `KickCD.toc` | `120105` | 1.5.0 | 1530802 | yes | no | 1.5.0-release |
| LibKa0sSkinTester | `LibKa0sSkinTester.toc` | `120105` | 0.1.0 | none | yes | yes | no tags |
| LootHistory | `LootHistory.toc` | `120105` | 1.5.0 | 1607560 | yes | yes | 1.5.0-release |
| MultiMeters | `MultiMeters.toc` | `120105` | 1.2.0 | 1690082 | yes | yes | 1.2.0-release |
| OutfitterReborn | `OutfitterReborn.toc` | `120105` | 1.1.0 | 1698220 | yes | yes | 1.0.0-release |
| PanelMaster | `PanelMaster.toc` | `120105` | 1.3.0 | 1642836 | yes | no | 1.3.0-release |
| PartyFrameEnhanced | `PartyFrameEnhanced.toc` | `120105` | 1.2.0 | 1698335 | yes | no | 1.2.0-release |
| PremadeGroupsFilterExtension | `PremadeGroupsFilterExtension.toc` | `120105` | 1.0.0 | 1736636 | yes | no | 1.0.0-release |
| PrettyChat | `PrettyChat.toc` | `120105` | 1.7.0 | 919766 | yes | no | 1.7.0-release |
| QuickComms | `QuickComms.toc` | `120105` | 1.0.0 | 1765410 | yes | yes | 1.0.0-release |
| WhatGroup | `WhatGroup.toc` | `120105` | 1.6.0 | 1489907 | yes | yes | 1.6.0-release |
| LibKa0s (library) | none | n/a | n/a | n/a | none | n/a | v1.91.0, v1.90.0, v1.89.0 |

- The roster is 17 addons plus LibKa0s, with WowAddonStandards and dev-copilot as tooling repos (`WowAddonStandards/standards/ADDONS.md:17-35,74-88`).
- The TOC header shape, using AbsorbTracker as the example: `## Interface: 120105`, Title, Notes, Author, Version, IconTexture, SavedVariables, `## OptionalDeps: Ace3, LibStub, … LibDBIcon-1.0, EllesmereUI`, `## Category-enUS`, `X-License`, `X-Standard`, `X-Curse-Project-ID`, then the vendored libs inside a `#@no-lib-strip@` block (`AbsorbTracker/AbsorbTracker.toc:1-20`). No addon carries `X-Flavor`, `X-Min-Interface`, `AllowLoadGameType` or `X-Wago-ID` (grep over every root TOC).
- `.pkgmeta` holds `package-as`, `enable-nolib-creation: no` and an `ignore:` list. It has no `enable-toc-creation` and no `externals:` (`AbsorbTracker/.pkgmeta:1-33`, and `package-as` in all 17). No repo has `.github/workflows` (ls of every root).
- The published CurseForge game versions in the journal are Retail only. Every file of every published addon is tagged `12.x`, apart from one PrettyChat file at `10.1.7`, and none is tagged with a WoW:F or Classic version (`Ka0sAddonsCommonTasks/journal/curseforge/*/files.json`, `gameVersions` field, aggregated). Note that the TOC says `120105` (12.1.5) while the newest uploads are tagged `12.1.0`.
- The client the TOCs target: the owner's install reports Retail `Product wow`, `Version 12.1.5.70783`, and WoW:F `Product wowf`, `Version 1.60.1.70790` (`/mnt/g/Games/Blizzard/World of Warcraft/.build.info`). The player report shows WoW:F as `interface=16001` (PartyFrameEnhanced#15, diagnostics line `client: version=1.60.1 build=70009 … interface=16001`).

### Inferences
- A WoW:F port starts from a clean slate. Nothing in the collection is multi-client today, so every TOC, the standard rules that forbid multi-client TOCs, and the tooling (Q6) all need a decision.
- The packager has never been asked for a second flavour. A CurseForge upload would also need the WoW:F game version selected on the project. That is outside this repo's data.

### Gaps
- I could not tell from local files whether the CurseForge projects allow WoW:F as a game flavour, or how the packager maps `16001` to a CurseForge game version. That needs web or CurseForge research.

---

## Q2. What the standard says today about flavours, Interface, Compat and WOW_PROJECT_ID

### Takeaway
The standard (v2.102.2, 2026-11-06) is **explicitly Retail-only**. Several MUST/MUST NOT rules forbid a single multi-value Interface
line, per-flavour TOCs, `enable-toc-creation`, `_Classic` splits and `WOW_PROJECT_ID` branching. The compat family is defined as
shimming *Retail patch* differences, "not across game flavors". WoW:F appears only as a recorded open evolution that points at LibKa0s#44.

### Cited Findings
- Current version: `# Ka0s WoW Addon Standard (v2.102.2, 2026-11-06)` (`WowAddonStandards/standards/STANDARDS.md:1`).
- toc-file-§3 is titled "Retail only — single Interface line": *"The collection targets **Retail (Mainline) only**. Classic/other flavors are out of scope"* (`WowAddonStandards/standards/standards/toc-file.md:57-59`).
  - It MUSTs a single TOC with a single `## Interface:` set to the latest Retail patch, and deliberately carries no literal (`toc-file.md:61`).
  - It forbids a comma-separated multi-flavor Interface list, per-flavor TOC files and `enable-toc-creation` fan-out (`toc-file.md:62`).
  - It forbids `_Mainline`/`_Classic` data splits (`toc-file.md:63`).
  - It forbids inline `if WOW_PROJECT_ID == ...` ladders. A cross-patch check is "a Retail-patch check", branched in the compat family behind a named flag (`toc-file.md:64`).
  - The README `[wow]` badge MUST show the same single Interface number (`toc-file.md:65`).
  - The template line is `## Interface: <latest Retail>            -- SINGLE number` (`toc-file.md:10`).
- compat: the family *"shims across **Retail patch** differences — not across game flavors"* (`WowAddonStandards/standards/standards/compat.md:5`). It also says *"MUST NOT branch on `WOW_PROJECT_ID` for game flavor (Retail only)"* (`compat.md:42`). The family is `core/Compat.lua` plus `core/Compat<Topic>.lua`, publishing into one `NS.Compat` (`compat.md:7-12`). The dead-fallback-rung rule is keyed to *"no client the addon's `## Interface` line admits"* (`compat.md:21`). Adding a WoW:F interface to that line would turn some deleted rungs back into live ones.
- Anti-patterns: #9 is *"`if WOW_PROJECT_ID == ...` game-flavor branching — Retail only"*, and #15 is *"Multi-flavor / Classic support (comma Interface lists, per-flavor TOCs, `_Classic` data splits, `enable-toc-creation` fan-out) — Retail only"* (`WowAddonStandards/standards/standards/anti-patterns.md:15,21`).
- packaging: *"MUST NOT use `enable-toc-creation` flavor fan-out — the addon is Retail-only with a single TOC"* (`WowAddonStandards/standards/standards/packaging.md:46`). CI is out of scope (`packaging.md:49`).
- versioning-git: *"MUST bump the single TOC `## Interface:` (and the matching README `[wow]` badge) each Retail patch via `dev-copilot:wow-bump-interface`"* (`WowAddonStandards/standards/standards/versioning-git.md:8`). The tag format `X.Y.Z-release` is not written in the standard's section files (grep for `-release` found only automated-test `--release X.Y.Z` mentions, `AUTOMATED_TESTS.md:22`). It is a convention visible in the tags.
- layout: `<AddonName>.toc -- single file, single Interface line (latest Retail)` and `Spells.lua / Data*.lua -- Retail data tables (no per-flavor suffix; Retail only)` (`WowAddonStandards/standards/standards/layout.md:11,29`).
- documentation: the badge placeholder `<Expansion>`/`<X.Y.Z>` is "the current Retail expansion name and … the client patch the TOC `## Interface:` encodes (e.g. `Midnight_12.0.7`)" (`WowAddonStandards/standards/standards/documentation.md:66,69`).
- client-quirks: the vendored quirks catalog expires against *"the retail interface number"* (`WowAddonStandards/standards/standards/client-quirks.md:31`), and each addon carries it as `docs/midnight-quirks.md` (`client-quirks.md:1`).
- events-frames-taint: the secret-values rules are framed as retail behaviour (`events-frames-taint.md:124`), and FrameXML citations point at Gethe/wow-ui-source's `live` branch, "retail" (`events-frames-taint.md:228`).
- The WoW:F mention: *"The WoW Forever client (recorded, not ruled)… `SetDesaturation` is missing there, which breaks every AceGUI checkbox, and the work is tracked in LibKa0s#44. Re-check when that issue moves."* (`WowAddonStandards/standards/standards/open-evolutions.md:349-352`). The harvest evidence lists LibKa0s#44 and PFE#15 (`WowAddonStandards/harvests/2026-11-06/03_EVIDENCE.md:1149,1247`).
- Grep found no `16001`, `WoW:F` or `WOW_PROJECT_CAMELOT` anywhere in the standard's section files.

### Inferences
- A port needs a **standard change first**: toc-file-§3, compat.md:5/42, packaging.md:46, versioning-git.md:8, anti-patterns #9/#15, layout.md:11/29 and the badge rule all have to be rewritten or carved out. This repo's rules route that to WowAddonStandards.
- Two shapes the current rules forbid would have to be chosen between: (a) one TOC with `## Interface: 120105, 16001`, which the standard forbids as "comma-separated multi-flavor", or (b) a `<Addon>_Forever.toc` / `_Camelot.toc` file beside the Retail TOC, which it forbids as "per-flavor TOC files". Both shapes are in use in the owner's WoW:F AddOns folder (Q7).

### Gaps
- The standard records no decision or rationale about *how* WoW:F would be admitted. It is "recorded, not ruled".

---

## Q3. LibKa0s's Compat layer, how addons consume it, and WOW_PROJECT_ID / GetBuildInfo

### Takeaway
`LibKa0s-Compat-1.0` (`LibKa0s/LibKa0s/Compat.lua`, 298 lines, MINOR 1) is a deliberately **narrow** set of Retail-patch ladders:
six spell and spec readers plus three secret-value guards. It has **no** flavour logic, **no** `SetDesaturation` shim and **no** `WOW_PROJECT_ID`
check. `LibKa0s-Env-1.0` reads `C_AddOns` only and has deleted the bare-global rung. Addons consume Compat through their own
`core/Compat.lua` (the `NS.Compat` seam) with library-absent stubs. No Ka0s-authored code references `WOW_PROJECT_ID`. `GetBuildInfo` is read
only for diagnostics, perf stamps and DpsRace's records.

### Cited Findings
- Compat's purpose and scope: two-rung ladders over APIs Blizzard moved, *"`C_Spell` in 11.0, `C_SpecializationInfo` in 12.0 — plus the three questions 12.0's secrets system forces"* (`LibKa0s/LibKa0s/Compat.lua:6-14`). The narrow-scope rationale and its rejection record are at `Compat.lua:16-34`. Its rules: bare globals read at call time, namespaced rung first, no pcall, exact arity (`Compat.lua:36-55`). Degradation and stub rules: readers answer the all-absent value, and guards MUST be re-implemented in host stubs (`Compat.lua:57-69`).
- Members: `IsSecret` (via `issecretvalue`, false when absent) `Compat.lua:96-112`; `CanAccess` (`canaccessvalue`) `:123-127`; `IsSafeKey` `:138-141`; `GetSpellInfo` (C_Spell, then legacy `GetSpellInfo` with the rank dropped) `:162-175`; `GetSpellName` `:194-210`; `GetSpellTexture` `:219-228`; `GetSpellCooldown` `:243-~265`; `GetSpecialization` (C_SpecializationInfo, then global) `~:270`; `GetSpecializationInfo` (passthrough) after that. MAJOR/MINOR is `"LibKa0s-Compat-1.0", 1` (`Compat.lua:84`).
- The legacy global rungs already present (`GetSpellInfo`, `GetSpellTexture`, `GetSpellCooldown`, `GetSpecialization`) are the kind a Classic-era API client would reach. The ladders were written for Retail deprecations, but they already degrade gracefully when a namespace is absent (`Compat.lua:169-173,224-226`).
- Env: `GetAddOnMetadata` answers `C_AddOns.GetAddOnMetadata` or nil. The bare global is "never read" since minor 2, under the dead-rung rule (`LibKa0s/LibKa0s/Env.lua:52-66`). `GetPlayerMapID` uses `C_Map.GetBestMapForUnit` (`Env.lua:91-96`), and `GetZone` uses `GetZoneText`/`GetSubZoneText` (`Env.lua:106-110`).
- `GetBuildInfo` in LibKa0s: the diagnostics header `pcall(GetBuildInfo)` prints `client: version=… build=… interface=…` (`LibKa0s/LibKa0s/DebugLogDiagnostics.lua:310-311`). That is the line that identified WoW:F in PFE#15. The perf record stamps the 4th return as the TOC (`LibKa0s/LibKa0s/Perf.lua:198-210`).
- `GetBuildInfo` in addons: DpsRace only, `DpsRace/modules/DummyList.lua:287` and `DpsRace/modules/Recorder.lua:281` (`ask(GetBuildInfo)`).
- `WOW_PROJECT_ID`: there are **zero** references in any addon's own code or in LibKa0s's payload (grep). The only references are in vendored **third-party** libs. AceGUI ColorPicker has `local INVERTED_ALPHA = (WOW_PROJECT_ID ~= WOW_PROJECT_MAINLINE)` (`PartyFrameEnhanced/libs/AceGUI-3.0/widgets/AceGUIWidget-ColorPicker.lua:16`), and LibDBIcon has `if WOW_PROJECT_ID == WOW_PROJECT_MAINLINE then` (`PartyFrameEnhanced/libs/LibDBIcon-1.0/LibDBIcon-1.0.lua:254`).
- `SetDesaturation`: **no** shim exists in LibKa0s or any addon. The vendored AceGUI CheckBox widget (`local Type, Version = "CheckBox", 26`, `AceGUIWidget-CheckBox.lua:4`; AceGUI MINOR 41, `AceGUI-3.0.lua:28`) calls the global at **six** sites: lines 100, 108, 110 (SetDisabled) and 122, 127, 130 (SetValue) (`PartyFrameEnhanced/libs/AceGUI-3.0/widgets/AceGUIWidget-CheckBox.lua`). All 17 addons vendor byte-identical copies (one md5 across 17 files). The PFE#15 errors cite line 130.
- How addons consume Compat (production code; `core/Compat*.lua` lines; files that resolve `LibKa0s-Compat-1.0`):

| Addon | Compat family | Lines | Resolves `LibKa0s-Compat-1.0` in |
|---|---|---|---|
| AbsorbTracker | none | 0 | none |
| AuraMaster | `core/Compat.lua` | 427 | Compat.lua, Secrets.lua |
| BankLedger | `core/Compat.lua` | 195 | none (hand shims only) |
| ConsumableMaster | `core/Compat.lua` | 97 | Compat.lua, DebugLogSetup.lua |
| DpsRace | `core/Compat.lua` | 149 | Compat.lua, Secrets.lua |
| DropWatcher | Compat + CompatCollect + CompatItem + CompatJournal + CompatWorld | 1645 | Compat.lua |
| KickCD | `core/Compat.lua` | 567 | Compat.lua |
| LibKa0sSkinTester | none | 0 | none |
| LootHistory | `core/Compat.lua` | 1001 | Compat.lua |
| MultiMeters | `core/Compat.lua` | 886 | Compat.lua, Secrets.lua, modules/Roster.lua |
| OutfitterReborn | `core/Compat.lua` | 956 | Compat.lua, Secrets.lua |
| PanelMaster | `core/Compat.lua` | 193 | none |
| PartyFrameEnhanced | `core/Compat.lua` | 223 | Compat.lua |
| PremadeGroupsFilterExtension | `core/Compat.lua` | 18 | Compat.lua |
| PrettyChat | none | 0 | none |
| QuickComms | `core/Compat.lua` | 390 | Compat.lua |
| WhatGroup | `core/Compat.lua` | 221 | Compat.lua |

- Every addon vendors LibKa0s **v1.91.0** (the provenance line in each `CLAUDE.md`, `Bundles [LibKa0s](…) v1.91.0`).

### Inferences
- A `SetDesaturation` fallback in LibKa0s would have to be a **global install** (`SetDesaturation = SetDesaturation or function(t, d) t:SetDesaturated(d) end`), loaded before AceGUI's CheckBox runs. That is a new kind of member, because Compat's rule is that it publishes a library table, not globals. It conflicts with Compat's "narrow" charter and with library-stack-§6-style rules on globals, so it would need a ruling. Questie on WoW:F does exactly this globally (Q7).
- Alternative evidence: upstream AceGUI **CheckBox widget version 27** replaces the global with `self.check:SetDesaturated(...)` (see Q7). AceGUI registers only the highest widget version (`if oldVersion and oldVersion >= Version then return end`, `PartyFrameEnhanced/libs/AceGUI-3.0/AceGUI-3.0.lua:553-554`). So (a) re-vendoring a current Ace3 would remove the defect without editing any vendored file, and (b) on a player's client where any other addon ships CheckBox v27, the Ka0s v26 copy is already overridden. That explains why some WoW:F users never see the bug, and why the CurseForge commenter fixed it by "updat[ing] the Ace3 Libraries" (Q7). The owner's note that the fix belongs in Compat predates this evidence, and the comparison is a decision for the plan.
- The Compat ladders are Retail-patch shaped. On a client whose API surface differs by flavour, the "first rung that EXISTS is authoritative" rule (`Compat.lua:44-46`) still works as feature detection. Any genuine semantic difference, though, would require a flag that the standard forbids today (compat.md:42).

### Gaps
- I did not verify which of Compat's namespaced rungs (`C_Spell`, `C_SpecializationInfo`) exist on WoW:F. That needs a WoW:F API reference or an in-client check.

---

## Q4. Retail-specific API exposure per addon and in LibKa0s

### Takeaway
The exposure is broad and uneven. A handful of addons are built *on* Midnight-only systems: MultiMeters and DpsRace (C_DamageMeter, death recap),
KickCD (C_CooldownViewer, C_CurveUtil), BankLedger and LootHistory (C_Bank, warband), PremadeGroupsFilterExtension and WhatGroup (C_LFGList, C_MythicPlus),
OutfitterReborn (C_EquipmentSet), and DropWatcher (C_LootHistory, C_EncounterJournal, C_TransmogCollection). Nearly every addon
also leans on the 12.0 secret-value system, and every addon leans on the Retail `Settings` panel, `BackdropTemplate` and `C_Timer` through LibKa0s. **No** Ka0s code uses
`COMBAT_LOG_EVENT_UNFILTERED`, `AddonCompartment` (only vendored LibDBIcon does), or `EditMode` beyond PartyFrameEnhanced.

### Cited Findings
Table A, pattern counts (non-comment lines, production code; LibKa0s = `LibKa0s/LibKa0s/`). Column patterns: Auras = `C_UnitAuras.|AuraUtil.|UnitAura(|UnitBuff(|UnitDebuff(`.
LootRoll = `C_LootHistory.|LOOT_HISTORY_UPDATE|START_LOOT_ROLL|LOOT_ROLLS_COMPLETE|ENCOUNTER_LOOT_RECEIVED|C_Loot.|GetLootRollItem|RollOnLoot`. BlizzSettings =
`Settings.OpenToCategory|Settings.Register*Category|…|SettingsPanel`. MenuUtil = `MenuUtil.|MenuResponse|Menu.ModifyMenu|CreateContextMenu|UIDropDownMenu|EasyMenu`.
EditMode = `EditModeManager|EDIT_MODE_|EditModeSystem`. TooltipDP = `TooltipDataProcessor|C_TooltipInfo`. SetAtlas = `SetAtlas|CreateAtlasMarkup|GetAtlasInfo`.
Secret = `issecretvalue|canaccessvalue|issecrettable|canaccesstable|IsSecret|CanAccess|C_Secrets`. Warband = `C_Bank.|Enum.BankType|AccountBank|ACCOUNT_BANK`.
Spec = `C_SpecializationInfo|GetSpecialization|GetSpecializationInfo`.

| Repo | LOC | C_AddOns | C_Spell | C_Item | C_Container | Auras | C_LFGList | LootRoll | C_ChatInfo | BlizzSettings | Compartment | MenuUtil | EditMode | TooltipDP | C_Timer | Backdrop | SetAtlas | CLEU | C_DamageMeter | Secret | Warband | Spec | GetBuildInfo/WOW_PROJECT | SetDesaturation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AbsorbTracker | 8700 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| AuraMaster | 28583 | 2 | 0 | 0 | 0 | 0* | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 12 | 2 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| BankLedger | 16875 | 3 | 0 | 6 | 2 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 3 | 9 | 0 | 0 | 0 | 0 | 11 | 0 | 0 | 0 |
| ConsumableMaster | 21384 | 2 | 15 | 25 | 2 | 0 | 0 | 0 | 0 | 12 | 0 | 0 | 0 | 4 | 7 | 4 | 4 | 0 | 0 | 4 | 0 | 8 | 0 | 0 |
| DpsRace | 29944 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 2 | 0 | 0 | 17 | 11 | 0 | 0 | 1 | 10 | 0 | 16 | 2 | 0 |
| DropWatcher | 43169 | 2 | 0 | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 3 | 21 | 7 | 0 | 0 | 0 | 75 | 0 | 3 | 0 | 0 |
| KickCD | 23530 | 2 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 6 | 3 | 4 | 0 | 0 | 15 | 0 | 5 | 0 | 0 |
| LibKa0sSkinTester | 5678 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LootHistory | 23826 | 2 | 0 | 23 | 5 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 2 | 7 | 8 | 9 | 0 | 0 | 0 | 12 | 0 | 0 | 0 |
| MultiMeters | 41551 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 2 | 0 | 0 | 4 | 7 | 7 | 0 | 8 | 39 | 0 | 5 | 0 | 0 |
| OutfitterReborn | 23907 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 6 | 0 | 3 | 0 | 2 | 4 | 5 | 0 | 0 | 0 | 16 | 0 | 15 | 0 | 0 |
| PanelMaster | 12866 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| PartyFrameEnhanced | 8861 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 2 | 0 | 5 | 2 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| PremadeGroupsFilterExtension | 6133 | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 |
| PrettyChat | 7460 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| QuickComms | 23191 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 2 | 8 | 4 | 0 | 0 | 12 | 0 | 5 | 0 | 0 |
| WhatGroup | 8087 | 2 | 2 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 1 | 2 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| **LibKa0s payload** | 43799 | 4 | 12 | 10 | 0 | 0 | 0 | 0 | 0 | 11 | 0 | 4 | 0 | 0 | 17 | 22 | 13 | 0 | 0 | 7 | 0 | 14 | 4 | 0 |

\* AuraMaster reaches auras as `_G.C_UnitAuras` (`AuraMaster/modules/Diagnostics.lua:82`), which the `C_UnitAuras.` pattern misses. Table B counts 3 mentions.
Zero-count caveat: the "BlizzSettings 0" for DropWatcher, PGFE and WhatGroup means only that the addon makes no *direct* call. Every addon registers its panel through `LibKa0s-Options-1.0` (`LibKa0s/LibKa0s/OptionsRegistry.lua:113,151-152`).

Table B, distinct `C_*` namespaces that are Midnight/Retail-era or system-specific (non-comment production lines, with an example):
- **C_DamageMeter**: MultiMeters 8 (`MultiMeters/core/Compat.lua:102`), DpsRace 1 (`DpsRace/modules/Meter.lua:42`).
- **C_DeathRecap / C_DeathInfo**: MultiMeters 4 / 5 (`MultiMeters/core/Compat.lua:234`, `:328`).
- **C_CurveUtil**: KickCD 18 (`KickCD/modules/Castbar.lua:599`), AuraMaster 3 (`AuraMaster/core/Compat.lua:143`), ConsumableMaster 2, PartyFrameEnhanced 1 (`PartyFrameEnhanced/core/Compat.lua:133`).
- **C_DurationUtil**: AuraMaster 1 (`AuraMaster/core/Compat.lua:256`), ConsumableMaster 2 (`ConsumableMaster/core/MacroDisplay.lua:121`), KickCD 1 (`KickCD/core/Compat.lua:323`).
- **C_CooldownViewer**: KickCD 4 (`KickCD/core/SpellInput.lua:165`).
- **C_RestrictedActions**: DropWatcher 1 (`DropWatcher/core/Compat.lua:252`), MultiMeters 2 (`MultiMeters/core/Secrets.lua:114`), OutfitterReborn 1 (`OutfitterReborn/modules/States.lua:162`), QuickComms 1 (`QuickComms/core/Compat.lua:197`).
- **C_Secrets**: AuraMaster 1 (`AuraMaster/core/Compat.lua:47`). **C_StringUtil**: AuraMaster 2, DpsRace 1, MultiMeters 5 (`MultiMeters/core/Compat.lua:516`). **C_Housing**: MultiMeters 1 (`MultiMeters/core/Compat.lua:727`), QuickComms 1 (`QuickComms/core/Compat.lua:157`). **C_DelvesUI**: MultiMeters 1 (`MultiMeters/core/Compat.lua:698`).
- **C_Bank (warband)**: BankLedger 5 (`BankLedger/core/Compat.lua:81`), LootHistory 1 (`LootHistory/core/Compat.lua:774`). The Warband column also counts `Enum.BankType` and `ACCOUNT_BANK` (`BankLedger/core/Constants.lua:124`, `LootHistory/core/Constants.lua:300`).
- **C_LFGList**: WhatGroup 6 (`WhatGroup/core/Compat.lua:159`), PGFE 2 (`PremadeGroupsFilterExtension/modules/RegionTags.lua:83`). **C_MythicPlus**: PGFE 3 (`PremadeGroupsFilterExtension/modules/Season.lua:38`). **C_ChallengeMode**: DropWatcher 3, LootHistory 2 (`LootHistory/core/Compat.lua:30`), PGFE 2, QuickComms 2 (`QuickComms/core/Compat.lua:91`).
- **Loot**: C_LootHistory in DropWatcher 1 (`DropWatcher/core/Compat.lua:426`). Loot-roll events in DropWatcher (`DropWatcher/modules/LootFeed.lua:1043-1044`). **C_EncounterJournal**: DropWatcher 3 (`DropWatcher/core/CompatJournal.lua:33`). **C_TransmogCollection**: DropWatcher 3 (`DropWatcher/core/Compat.lua:619`).
- **Outfits**: OutfitterReborn uses `C_EquipmentSet` 12 times (`OutfitterReborn/core/Compat.lua:677`) and has no `C_Transmog*` hits. Its other namespaces include C_PetJournal, C_AzeriteEmpoweredItem, C_ItemUpgrade and C_Minimap (namespace census).
- **C_TooltipInfo**: ConsumableMaster 4 (`ConsumableMaster/core/SlashDump.lua:136`), DropWatcher 3 (`DropWatcher/core/Compat.lua:148`), LootHistory 2 (`LootHistory/core/Compat.lua:309`), OutfitterReborn 1 (`OutfitterReborn/core/Compat.lua:532`).
- **C_UnitAuras**: AuraMaster 3, DpsRace 1 (`DpsRace/modules/Usage.lua:144`), OutfitterReborn 2 (`OutfitterReborn/modules/States.lua:222`).
- **C_Traits / C_ClassTalents**: DpsRace (`DpsRace/modules/Recorder.lua:223`). **C_SpecializationInfo**: ConsumableMaster 6, LibKa0s 8, OutfitterReborn 3, QuickComms 5, DpsRace 2.
- **EditMode**: PartyFrameEnhanced only (`PartyFrameEnhanced/core/Compat.lua:213`, `PartyFrameEnhanced/modules/Providers.lua:353`).
- **MenuUtil / new menu**: LibKa0s Launcher (`LibKa0s/LibKa0s/Launcher.lua:388,483-484`), DpsRace (`DpsRace/core/WidgetsSetup.lua:89,97`), MultiMeters (`MultiMeters/core/Compat.lua:578,582`), OutfitterReborn (`OutfitterReborn/core/WidgetsSetup.lua:175,222`), DropWatcher (`DropWatcher/core/Compat.lua:896`), PGFE (`PremadeGroupsFilterExtension/modules/Panel.lua:484`).
- **AddonCompartment**: no Ka0s code. Only vendored LibDBIcon reads it, guarded by `if AddonCompartmentFrame then` (`PartyFrameEnhanced/libs/LibDBIcon-1.0/LibDBIcon-1.0.lua:20,486,501`).
- **CLEU**: zero hits for `COMBAT_LOG_EVENT_UNFILTERED` / `CombatLogGetCurrentEventInfo` in every addon and in LibKa0s (scan, plus a direct grep of the AuraMaster, KickCD, MultiMeters, DpsRace and AbsorbTracker source dirs).
- **LibKa0s payload namespaces**: C_Timer 36, C_Spell 20, C_Item 18, C_SpecializationInfo 8, C_AddOns 7, C_Map 3, C_UI 3, C_CurrencyInfo 3, C_EventUtils 1, C_XMLUtil 1, C_Container 1, C_SpellBook 1, C_TradeSkillUI 1. The rest of the Retail surface it touches: `Settings`/`SettingsPanel` (`LibKa0s/.luacheckrc:21-24`; `OptionsRegistry.lua:113`), `BackdropTemplate` 22 (`Core.lua:163`, `Charts.lua:299`, `DebugLogWindow.lua:566`), `SetAtlas` 13 (`Options.lua:589`, `OptionsIdList.lua:729`, `OptionsNav.lua:112`) and `MenuUtil` (Launcher).
- **Keybinding XML**: a root `Bindings.xml` with `CLICK <Frame>:<Button>` bindings in a per-addon `category` exists in BankLedger, DpsRace, DropWatcher, LibKa0sSkinTester, LootHistory, MultiMeters, OutfitterReborn, QuickComms and WhatGroup. Example: `QuickComms/Bindings.xml:9-16`. LibKa0s's Keybindings tab drives the client's own binding API (`LibKa0s/LibKa0s/OptionsKeybinds.lua`; options-ui-§20).
- **Vendored libs** (identical set apart from opt-ins): Ace3 (AceAddon 13, AceDB 33, AceConfigDialog 92, AceGUI 41), CallbackHandler, LibStub, LibDataBroker-1.1, LibDBIcon-1.0 (minor 52), LibSharedMedia-3.0, plus LibCustomGlow-1.0 in DropWatcher, KickCD and QuickComms (`*/libs/` listing; `PartyFrameEnhanced/libs/*` headers).

### Inferences
- Tier the port by dependency. (1) *Shell-only* addons, where the risk is mostly LibKa0s and Ace: AbsorbTracker, PanelMaster, PrettyChat, LibKa0sSkinTester. (2) *Moderate*, with spells, items, auras and secrets: ConsumableMaster, AuraMaster, QuickComms, PartyFrameEnhanced, WhatGroup. (3) *Feature built on a Retail-only system*, where the addon's purpose may not exist on WoW:F: MultiMeters and DpsRace (C_DamageMeter), KickCD (C_CooldownViewer and C_CurveUtil castbars), BankLedger (warband bank), PGFE (M+ / LFGList filters), DropWatcher and LootHistory (loot history, journal and transmog), OutfitterReborn (equipment sets and talents). Whether each Tier 3 API exists on WoW:F is the decisive open question.
- The secret-value surface (`issecretvalue` and friends) is already written to degrade to "nothing is secret" when the globals are absent (`LibKa0s/LibKa0s/Compat.lua:96-100,123-127`). It is likely harmless on a client without 12.0 secrets.
- LibKa0s is the single point of failure: every addon's settings panel, launcher, skins and windows go through `Settings`, `BackdropTemplate`, `SetAtlas` atlas names, `MenuUtil` and `C_Timer`. A port should survey LibKa0s first, as LibKa0s#44 says.

### Gaps
- I could not determine from local code which of these APIs, events and atlases WoW:F ships. That needs FrameXML or API documentation for the `wowf` product, or an in-client `/dump` pass.
- The grep counts are call-site lines, not semantic usages. Several hits sit inside guarded ladders (`x and x.fn`) that already degrade.

---

## Q5. What the test kit and luacheck assume about the client; testing a second flavour headless

### Takeaway
Lint and tests assume one client. `.luacheckrc` is `std = "lua51"` with a hand-curated `read_globals` list of Retail globals.
The kit's mock is a single Retail-shaped WoW API, and AceGUI is a **fake**, so the real CheckBox widget, and with it the `SetDesaturation`
defect, is never executed headless. No flavour switch exists. A second flavour could be tested by a suite that removes or replaces globals,
because the loader resolves mocks before `_G` and Compat reads globals at call time.

### Cited Findings
- LibKa0s `.luacheckrc` (`std = "lua51"`, `LibKa0s/.luacheckrc:1`) lists Retail globals with reasons: `C_AddOns` ("never the bare globals"), `C_Map`, `C_Item`, `C_Timer`, `C_Spell`, `C_CurrencyInfo`, `C_Container`, `C_SpellBook`, `C_TradeSkillUI`, `BackdropTemplateMixin`, `GetBuildInfo` ("the client interface version a perf record stamps"), `Settings`, `SettingsPanel`, and the legacy `GetSpellInfo`/`GetSpellTexture`/`GetSpellCooldown`, `issecretvalue`, `canaccessvalue` (`LibKa0s/.luacheckrc:5-47`). An addon example is KickCD: `std = "lua51"`, `read_globals` at `:47`, `globals` at `:68` and per-file blocks (`KickCD/.luacheckrc:1-2,47,68,89-186`). `WOW_PROJECT_ID` and `SetDesaturation` are not declared anywhere (grep).
- The kit is one mock. *"The universal half of the WoW-API mock, and AceGUI's fake"* (`LibKa0s/testkit/README.md`, files table: `mock_base.lua`). Inside it, AceGUI widgets are *"inert data recorders rather than frames"* (`LibKa0s/testkit/mock_base.lua:464-468`), and the CheckBox check texture is a fake with only `SetTexture`/`SetVertexColor` (`mock_base.lua:472-479`).
- The loader resolves mocks before `_G`: `__index` checks `mocks[k]` and then `_G[k]` (`LibKa0s/testkit/loader.lua:12-23`), using `setfenv` (`loader.lua:72,91`). The kit deliberately does not stub `C_AddOns`, so suites can swap it to nil to drive fallback branches (`mock_base.lua:335-342`).
- Secrets: `testkit/secrets.lua` provides `Kit.secret`, `Kit.isSecret` and an opt-in `Kit.installSecretValue` that sets the global `issecretvalue`, and *"Nothing installs the global by default"* (`LibKa0s/testkit/README.md`, files table).
- The build stamp in LibKa0s's own tests is pinned to Retail: `M.GetBuildInfo = function() return "12.0.7", "60000", "Jul 31 2026", 120007 end` (`LibKa0s/tests/wow_mock.lua:73`), and the diagnostics test asserts `client: version=12.0.7 build=60000` (`LibKa0s/tests/test_debuglog_diagnostics.lua:92`).
- The Compat design rule enables rung removal in tests: *"The headless kit resolves a bare name through its mock first, so a suite can remove a rung after load and watch the ladder move"* (`LibKa0s/LibKa0s/Compat.lua:38-41`).
- Gate commands: `lua tests/run.lua` and `ka0s-bounded luacheck .`, plus the 1500-line file cap (`Ka0sAddonsCommonTasks/CLAUDE.md`, Verification). The kit carries `run-automated-tests.sh` (`LibKa0s/testkit/` listing).

### Inferences
- Headless WoW:F testing would need a **flavour profile** for the mock: a WoW:F `GetBuildInfo` (`1.60.1`, `16001`), `WOW_PROJECT_ID`, and removal of the Retail-only namespaces WoW:F lacks. It could ship as an opt-in `mock_*.lua` installer in the shape of `mock_bindings.lua` and `mock_layers.lua`, with suites run twice. The existing "swap global to nil" pattern is the mechanism.
- The SetDesaturation class of bug (a third-party lib calling a missing global) is **invisible** to the kit because AceGUI is faked. Catching it needs either a check that loads the real `libs/AceGUI-3.0/widgets/*.lua` against a stricter mock, or a static check for globals that vendored libs call but the target flavour lacks.
- luacheck's `read_globals` is a union list. luacheck cannot tell which flavour a global belongs to, so lint gives no flavour signal.

### Gaps
- I did not read every addon's `tests/mock_*.lua` extender. Some may hard-code more Retail behaviour than the base kit does.

---

## Q6. What dev-copilot's commands assume

### Takeaway
The installed plugin is **dev-copilot 2.7.1**. `wow-bump-interface` is Retail-only by design: it sets every Retail TOC's `## Interface:` to one
"Live Servers" value, skips TOCs whose suffix marks another flavour, and accepts a comma list only when one is passed explicitly. The review
agent's cross-addon "Interface uniformity" class treats more than one distinct Interface line as a finding. `wow-new-addon` scaffolds "Retail-only single
`## Interface:`".

### Cited Findings
- Installed: `dev-copilot@dev-copilot` version `2.7.1`, installPath `~/.claude/plugins/cache/dev-copilot/dev-copilot/2.7.1`, sha `021e2da…`, lastUpdated 2026-11-06 (`~/.claude/plugins/installed_plugins.json`). The dev-copilot source `CLAUDE.md` says "Current version: **2.7.1**" (`dev-copilot/CLAUDE.md:11`).
- `wow-bump-interface` (installed copy, `~/.claude/plugins/cache/dev-copilot/dev-copilot/2.7.1/commands/wow-bump-interface.md`):
  - Description: "Bump the ## Interface line … to the current Retail (Live Servers) interface number" (`:2`).
  - Argument: a 6-digit build. *"if it's a comma-separated list, accept it verbatim (some TOCs carry multiple)"* (`:18`).
  - Default target: the *Retail* Live value `(major*10000)+(minor*100)+patch`, asking the user if unsure (`:19-20`). A 5-digit `16001` would fail its "6-digit" check and prompt for confirmation (`:18`).
  - TOC discovery: top level only, *"the main TOC and any per-flavor Retail TOCs beside it (`Foo.toc`, `Foo_Mainline.toc`)"* (`:24`). *"If a TOC targets a non-Retail flavor (e.g. `_Vanilla`, `_Cata`, `_Wrath`), leave it alone and report it as skipped"* (`:27`). `_Forever` and `_Camelot` are not in its list.
  - Apply: *"Replace the line starting with `## Interface:` … with `## Interface: <target>`"* (`:33`). That overwrites the whole line, so a `120105, 16001` list collapses to the single Retail number unless the full list is passed.
  - It does not touch the README badge, although versioning-git.md:8 requires the badge in the same change.
- Review agent, cross-addon class 4 "`## Interface:` uniformity": `find "$a" -maxdepth 1 -name '*.toc' -exec grep -h '^## Interface:' {} + | … | sort -u`, *"Clean is a single line"* (`~/.claude/plugins/cache/dev-copilot/dev-copilot/2.7.1/profiles/wow/agent-review.md:443-451,494-500`). The TOC checklist flags *"Per-version TOCs (`Foo_Mainline.toc`, `Foo_Cata.toc`) drifted out of sync"* (`agent-review.md:659`).
- `wow-new-addon`: *"Retail-only single `## Interface:`"* (`…/2.7.1/commands/wow-new-addon.md:254`).
- `bump-version` (WoW profile): bumps `## Version:` in *"every `.toc` (including per-flavor variants: `*_Mainline.toc`, `*_Cata.toc`, etc.)"* (`…/2.7.1/profiles/wow/bump-version.md:148`), and checks that the season and patch match the TOC Interface (`:326`).
- Repo-kind detection: an addon is *"a root `*.toc` holding a line that starts `## Interface:`"* (`…/2.7.1/CLAUDE.md:40`; `scripts/detect_profile.py:23,80`). That is flavour-neutral.
- CurseForge journal: it records each file's `gameVersions` verbatim (`…/2.7.1/scripts/curseforge_journal.py:478`), so WoW:F uploads would show up without a code change.
- Grep of the installed tree for `WOW_PROJECT`, `16001`, `WoW:F` and `Forever` (client sense) found nothing.

### Inferences
- A port needs dev-copilot changes in `wow-bump-interface` (a two-number model, or a per-flavour TOC map including `_Forever`/`_Camelot`, plus WoW:F's 5-digit number), in the review agent's uniformity class (uniformity *per flavour*), in `wow-new-addon`, and possibly in `bump-version`'s badge and season logic. Per this repo's rules, those changes belong in `dev-copilot`, not here.

### Gaps
- I did not read every dev-copilot profile. Other commands (`wow-standards-audit`, `wow-revendor-*`) may embed the toc-file-§3 checks through the standard's AUDIT.md rather than in their own text.

---

## Q7. How the dev environment loads addons, and what is on the owner's WoW:F install

### Takeaway
The owner's client root is `G:\Games\Blizzard\World of Warcraft` (WSL `/mnt/g/...`). It has `_retail_`, `_forever_`, `_classic_`, `_classic_era_`
and `_anniversary_` product folders. `_retail_/Interface/AddOns/<Addon>` entries are **symlinks** to `GIT/<Addon>`, 16 of the 17 roster addons (AbsorbTracker is
absent). `_forever_/Interface/AddOns` holds 156 third-party addons and **no Ka0s addon**. Those third-party addons show the WoW:F conventions a port would copy:
`16001` in comma lists, `_Forever.toc`/`_Camelot.toc` files, `WOW_PROJECT_CAMELOT`, and AceGUI CheckBox v27 or a global `SetDesaturation` shim.

### Cited Findings
- Retail symlinks: `_retail_/Interface/AddOns/AuraMaster -> /mnt/d/Profile/Users/Tushar/Documents/GIT/AuraMaster`, and the same for BankLedger, ConsumableMaster, DpsRace, DropWatcher, KickCD, LibKa0sSkinTester, LootHistory, MultiMeters, OutfitterReborn, PanelMaster, PartyFrameEnhanced, PremadeGroupsFilterExtension, PrettyChat, QuickComms and WhatGroup. There is also a stale `PartyFramesEnhanced -> GIT/PartyFramesEnhanced`. No `AbsorbTracker` entry exists (`ls -la "/mnt/g/Games/Blizzard/World of Warcraft/_retail_/Interface/AddOns"`).
- Documented install paths: OutfitterReborn documents a Windows junction, `mklink /J "C:\Program Files (x86)\World of Warcraft\_retail_\Interface\AddOns\OutfitterReborn" "<path to this checkout>"`, and "A junction named `Outfitter` loads nothing" (`OutfitterReborn/DEPENDENCIES.md:63-67`). AuraMaster's log tool defaults to `/mnt/g/Games/Blizzard/World of Warcraft/_retail_/Logs/…` (`AuraMaster/DEPENDENCIES.md:130`). Owner memory records "the game loads GIT/AuraMaster via symlink, never test from a side worktree", with the live install `/mnt/g/Games/Blizzard/World of Warcraft/_retail_` and the account `ADD1KTED2KA0S` (`~/.claude/projects/…/memory/auramaster-spell-list-views.md:28-30`; `font-pickers-skin-faces.md:15`, which adds "Do not scan whole drives for it"). No CLAUDE.md documents a `_forever_` path (grep of every repo's `CLAUDE.md`/`DEPENDENCIES.md`).
- Product versions: `wow 12.1.5.70783`, `wow_classic 5.5.4.70631`, `wow_classic_era 1.15.9.70576`, `wow_anniversary 2.5.6.70577`, `wowf 1.60.1.70790` (`/mnt/g/Games/Blizzard/World of Warcraft/.build.info`).
- `_forever_` state: 156 AddOns entries with no Ka0s names, and no Ka0s SavedVariables under `_forever_/WTF/Account/ADD1KTED2KA0S/SavedVariables` (listing).
- WoW:F TOC conventions seen in the third-party addons in `_forever_/Interface/AddOns` (read-only). Single value: `AppelSwingsForever.toc: ## Interface: 16001`. Comma lists that include Retail: `Auctionator.toc: ## Interface: 120100, 120105, 16001, 50504, 38000, 20506, 11508, 11509`, `EllesmereUI.toc: ## Interface: 120000, 120001, 120005, 120007, 120100, 120105, 16001`, `DBM-Core.toc: ## Interface: 11509, 16001, 20506, …, 120105, 120107`. Suffixed TOCs: `AtlasLootClassic/AtlasLootClassic_Forever.toc` (`16001`), `GTFO/GTFO_Camelot.toc`, `EllesmereUIForeverEssentials/EllesmereUIForeverEssentials_Camelot.toc`.
- Project constant: `WOW_PROJECT_CAMELOT` is used 42 times by third-party code, often with a fallback literal: `WOW_PROJECT_ID == (_G.WOW_PROJECT_CAMELOT or 18)` (`_forever_/Interface/AddOns/AtlasLootClassic/Init.lua:93`), `local WOW_PROJECT_CAMELOT=WOW_PROJECT_CAMELOT or 18` (`…/Broker_Everything/shared.lua:127`). Auctionator treats it as Retail: `IsRetail = WOW_PROJECT_ID == WOW_PROJECT_MAINLINE or WOW_PROJECT_ID == WOW_PROJECT_CAMELOT, -- temporary fix assigning retail to mainline` (`…/Auctionator/Source/Constants/Main.lua:56`). The upstream AceGUI ColorPicker treats it as Mainline: `INVERTED_ALPHA = (WOW_PROJECT_ID ~= WOW_PROJECT_MAINLINE and WOW_PROJECT_ID ~= WOW_PROJECT_CAMELOT)` (`…/BlizzMove/Libs/AceGUI-3.0/widgets/AceGUIWidget-ColorPicker.lua:16`). The Ka0s-vendored copy lacks the CAMELOT clause (`PartyFrameEnhanced/libs/AceGUI-3.0/widgets/AceGUIWidget-ColorPicker.lua:16`).
- AceGUI CheckBox on WoW:F: of 15 copies, 3 are `Version 26` with 6 `SetDesaturation(` calls (AtlasLootClassic_Options, Spoken_Quests, and a nested NovaInstanceTracker copy). 12 are `Version 27`, which calls `self.check:SetDesaturated(true/false)` instead (`…/Bazooka_Options/libs/Ace3/AceGUI-3.0/widgets/AceGUIWidget-CheckBox.lua:100,108,110`; AceGUI MINOR still 41, `…/AceGUI-3.0.lua:28`).
- A global shim in the wild: Questie installs `SetDesaturation = SetDesaturation or QuestieCompat.SetDesaturation` on Forever, with the comment *"AceGUI checkboxes still call this global. Install before embedded libraries without replacing a native helper."* The shim body is `texture:SetDesaturated(desaturated)` (`…/Questie/Modules/QuestieCompat.lua:1305-1316`).
- Player reports: the PFE#15 body has `[PFE] settings row 'enabled' failed to render: …AceGUIWidget-CheckBox.lua:130: attempt to call a nil value`, and its diagnostics show `PartyFrameEnhanced v1.1.0`, `client: version=1.60.1 build=70009 date=Sep 23 2026 interface=16001`, `LibKa0s running: Core 8, Env 1, Compat 1, … Options 26`, and `EllesmereUI loaded=true` (GitHub tusharsaxena/PartyFrameEnhanced#15, opened 2026-09-27). In the CurseForge comment of 2026-10-03, a player says they *"got this working with the October patch of WoW:forever beta by changing the version in the .toc file (## Interface: 16001) and updated the Ace3 Libraries"*. The owner replied on 2026-10-10: *"I was planning to port this to Forever soon anyways, good to know its that easy"* (`Ka0sAddonsCommonTasks/journal/curseforge/PartyFrameEnhanced/comments.json`, ids 8493119, 8524823).
- LibKa0s#44 (open; `enhancement`, `state:triaged`, `severity:low`; created 2026-10-03) scopes three pieces of work: the TOC multi-client lines and the matching standard rule, a survey of every Blizzard global and API against WoW:F "so the gaps land in LibKa0s Compat once", and a per-addon smoke pass on the WoW:F client (GitHub tusharsaxena/LibKa0s#44).

### Inferences
- The dev loop for WoW:F would mirror Retail: add `_forever_/Interface/AddOns/<Addon> -> GIT/<Addon>` symlinks. With one checkout serving both clients, a single TOC listing both numbers (or a `_Forever.toc` beside the Retail TOC) loads from the same tree. The owner's memory warns against side worktrees for in-game tests.
- The PFE#15 report shows a 120105-era build loaded and mostly worked on WoW:F apart from checkboxes. The likely cause is that the player enabled out-of-date addons, but this is unconfirmed. Read with the CurseForge comment, the shell of at least one Tier 2 addon runs on WoW:F with only the Interface number and the Ace3 CheckBox changed.
- EllesmereUI declares 16001 and is the Ka0s skin provider's optional dependency (`AbsorbTracker/AbsorbTracker.toc:8`, `OptionalDeps … EllesmereUI`). The EUI skin path is therefore likely to be exercised on WoW:F as well.

### Gaps
- I did not establish from local data how the PFE#15 player loaded a `120105` TOC on a `16001` client, whether by "Load out of date AddOns" or by WoW:F accepting it.
- Third-party code on the owner's disk is not an authoritative WoW:F API reference. The `WOW_PROJECT_CAMELOT == 18` fallback literal and Auctionator's "assigning retail to mainline" comment are other authors' claims. They should be confirmed against Blizzard's WoW:F FrameXML or an in-client `/dump WOW_PROJECT_ID`.
