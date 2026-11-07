# Knowledge bases, reference tooling and ecosystem practice for WoW: Forever (as of 2026-11-07)

Method: live web fetches, plus direct reads of upstream GitHub repos through `gh api` (file contents, TOC files,
commit logs since 2026-09-01) on 2026-11-07. Where a repo file is quoted, the URL is the file on its default branch
at the time of reading. Code is quoted verbatim from those reads.

Basic facts that every later section relies on:
- Forever's internal codename is **Camelot**. Its TOC interface is **16001**, and its project constant is `WOW_PROJECT_CAMELOT = 18` — [warcraft.wiki.gg WOW_PROJECT_ID](https://warcraft.wiki.gg/wiki/WOW_PROJECT_ID); [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- It launched on 2026-11-04 as build `1.60.1.70790`, product `wowf`, installed in `_forever_`. The beta was `wow_classic_beta` — [BetterBags .claude/rules/camelot-forever.md](https://github.com/Cidan/BetterBags/blob/main/.claude/rules/camelot-forever.md). This is a third-party write-up, but it agrees with Gethe's `forever` branch head `1.60.1 (70790)`, committed 2026-11-04 ([Gethe/wow-ui-source forever](https://github.com/Gethe/wow-ui-source/tree/forever)).
- Forever "shares Mainline's UI architecture". It is one of two game types in the Mainline family (Camelot, then Standard), it has "the vast majority" of 12.1.5 APIs, and Midnight's secrets and addon-disarmament rules are active in it — [warcraft.wiki.gg Patch 1.60.1/API changes/notes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes/notes); [Icy Veins](https://www.icy-veins.com/wow-forever/news/addons-in-wow-forever-blizzard-devs-just-addressed-the-big-question/)

## Which knowledge bases cover Forever, what they offer, and how current they are

### Takeaway
The authoritative references are warcraft.wiki.gg (TOC format, WOW_PROJECT_ID and the Patch 1.60.1 API-change notes, which transcribe Blizzard's WoWUIDev Discord posts), Gethe/wow-ui-source and Ketho/BlizzardInterfaceResources (each has a live `forever` branch), and Blizzard's posts in the WoWUIDev Discord. Ketho's vscode-wow-api has no Forever support: its last commit is 2026-06-24. Blizzard publishes no official addon-developer documentation for Forever outside Discord and the beta forum posts.

### Cited Findings
- **warcraft.wiki.gg, WOW_PROJECT_ID.** The table lists `WOW_PROJECT_CAMELOT` = 18 as "World of Warcraft: Forever", added in Patch 1.60.1, next to MAINLINE 1, CLASSIC 2, WOWLABS 3, BCC 5, WRATH 11, CATA 14 and MISTS 19. The example if/elseif chain appears to use inverted `!=` tests, so verify it before copying. The page also sits in the "Potentially out-of-date content" category — [WOW_PROJECT_ID](https://warcraft.wiki.gg/wiki/WOW_PROJECT_ID)
- **warcraft.wiki.gg, TOC format.** This page is the best single reference.
  - Game types `forever`/`camelot` have the TOC suffixes `AddOnName_Forever.toc` and `AddOnName_Camelot.toc`.
  - The family suffix `_Mainline.toc` covers standard, forever, camelot, plunderstorm and wowhack. `_Classic.toc` covers vanilla through mists.
  - The page says "The Camelot value may be changed to Forever in the future."
  - It gives a multi-interface example, `## Interface: 120105, 16001, 50504, 11509`, captioned "retail, forever, classic, and classic era". Comma-separated interfaces have been supported since 10.2.7.
  - `AllowLoadGameType` and `ExcludeLoadGameType` accept `forever` and `camelot`. Warning: if the client recognises none of the listed game types, the condition is satisfied.
  - The Bootstrap directive and the RegionalTextLocale variable are "Only supported in: Midnight and Forever".
  - Forever 1.60.1 "Includes all Modern changes up to 12.1.5".
  - [TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- **warcraft.wiki.gg, Patch 1.60.1/API changes/notes.** The page was last edited 2026-10-17. Each entry links to a Discord post ("Forever 1.60.1 Beta Changes", "An Update On Secrets In WoW: Forever"), and the page names no author. Entries:
  - Beta 5, build 70425, 2026-10-16: GUID server and spawn IDs are obfuscated. The player, target and focus frames and the minimap header are reskinned, so addons that skin or anchor to them may need changes.
  - Beta 4, build 70291, 2026-10-08: "Forever" is accepted as an alias of Camelot in TOC suffixes, the `[Game]` variable and folder lookup. Lua `require` was renamed to `import`. `C_PvP.IsWarModeFeatureEnabled` returns false. There is a new `FrameStrata` secret aspect, under which `GetFrameStrata` can return a secret. Trial accounts can no longer send addon messages.
  - [API changes notes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes/notes)
- **warcraft.wiki.gg, API change summaries.** This index hosts the per-patch change pages, including the 1.60.1 one — [API change summaries](https://warcraft.wiki.gg/wiki/API_change_summaries). Unverified: whether individual API pages carry a per-flavour "Forever" availability tag. The TOC page tags sections "Only supported in: Midnight and Forever", which suggests the wiki's flavour templates now include Forever, but no API page was checked.
- **Gethe/wow-ui-source.** It has a `forever` branch next to `live`, `ptr`, `beta`, `classic*` and others. The head is `1.60.1 (70790)`, committed 2026-11-04, so it is current to the launch build — [Gethe/wow-ui-source forever branch](https://github.com/Gethe/wow-ui-source/tree/forever)
- **Ketho/BlizzardInterfaceResources.** It has a `forever` branch with `Resources/` holding the globals, API and event lists. The head is `1.60.1 (70532)`, committed 2026-10-21, about two weeks behind the launch build — [Ketho/BlizzardInterfaceResources forever](https://github.com/Ketho/BlizzardInterfaceResources/tree/forever)
- **Ketho/vscode-wow-api.** A code search for "forever" hits only `src/data/cvar.ts`. The latest commit is dated 2026-06-24 (`gh api repos/Ketho/vscode-wow-api/commits`), and no Forever flavour setting was found — [Ketho/vscode-wow-api](https://github.com/Ketho/vscode-wow-api)
- **Blizzard_ProjectConstants.** Blizzard added `Blizzard_ProjectConstants/Camelot/ProjectConstants.lua`, gated with `[AllowLoadGameType camelot]`. It sets `WOW_PROJECT_CAMELOT = 18` and `WOW_PROJECT_ID = WOW_PROJECT_CAMELOT`, and the global exists only on the camelot game type. Blizzard's own `GlueParent.lua` uses `WOW_PROJECT_CAMELOT or WOW_PROJECT_MAINLINE` — [BetterBags camelot-forever.md](https://github.com/Cidan/BetterBags/blob/main/.claude/rules/camelot-forever.md). This is a secondary account; the file is browsable on the [Gethe forever branch](https://github.com/Gethe/wow-ui-source/tree/forever).
- **Blizzard official channels.**
  - A Blizzard representative said in the WoW UI Discord that Forever shares Mainline's UI architecture and most 12.1.5 APIs — [Icy Veins](https://www.icy-veins.com/wow-forever/news/addons-in-wow-forever-blizzard-devs-just-addressed-the-big-question/)
  - Blizzard posted beta "development notes" on the US forums. The 09-24 notes enabled the Cooldown Manager for five classes — [Blizzard forum, dev notes 09-24](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-%E2%80%93-updated-september-24/2360696)
  - Blizzard also posted a known-issues thread — [Blizzard forum, known issues 09-17](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-known-issues-september-17/2352687) (both forum links are as cited by forever-addon-kit, not fetched)
  - No dedicated official Forever addon-developer page was found.
- **Community bug and research trackers.**
  - [ClassicWoWCommunity/forever-bugs](https://github.com/ClassicWoWCommunity/forever-bugs): "a place for WoW Forever bug reports and research", 202 open issues, last pushed 2026-10-01. Issue #74 traced the secure-snippet `loadstring_untainted` failure that was fixed in build 70009.
  - [Thunderz96/forever-addon-kit](https://github.com/Thunderz96/forever-addon-kit): measured findings and a captured API baseline. It is a beta snapshot, last updated 2026-09-24.
  - [imperial64/forever-addon-dev](https://github.com/imperial64/forever-addon-dev): cited by the kit, not fetched.
- **Community guide sites.** [wowforeverguides.com/addons/developers](https://wowforeverguides.com/addons/developers) and [/addons/patterns](https://wowforeverguides.com/addons/patterns) cover Interface 16001, secret values and the project ID. One of them reports that build 69913 returned `WOW_PROJECT_ID = 1` and a later probe on 70338 returned 18. These are secondary, SEO-style sites, so treat them as low authority.
- **The kit's saved-variables warning.** On the early beta the kit measured "Saved variables are never loaded (Blizzard bug)" — [forever-addon-kit README](https://github.com/Thunderz96/forever-addon-kit). Unverified whether this is fixed on the live client.

### Inferences
- For a port, treat warcraft.wiki.gg's TOC format page and the 1.60.1 API-change notes as normative, the Gethe `forever` branch as ground truth for FrameXML, and the BIR `forever` branch as the source for a global or API diff against `live`, after refreshing it to 70790.
- vscode-wow-api (LuaLS annotations) cannot yet tell Forever apart from Retail. Annotations will describe Retail 12.x, which mostly matches but will miss the Forever-only constants and the removed APIs.
- Beta-era community findings, such as the forever-addon-kit, predate builds 70170, 70291 and 70790. Several of them are now stale, notably "WOW_PROJECT_ID == WOW_PROJECT_MAINLINE" and "no addon site has a Forever flavour".

### Gaps
- Not checked: warcraft.wiki.gg API pages, for whether they carry per-flavour Forever tags. Wowpedia (Fandom), for Forever coverage. Townlong Yak and wago.tools, which the fetch budget did not reach (wago.tools likely lists `wowf` builds, unverified).
- I could not reach the WoWUIDev Discord. Its announcement content is only known through the wiki transcriptions.
- I found no posts in the Blizzard UI & Macro forum about Forever.

## How major multi-flavour addons and libraries detect Forever and branch on it

### Takeaway
Every project surveyed that supports Forever uses **flavour detection on `WOW_PROJECT_ID == WOW_PROJECT_CAMELOT`**, usually plus a derived "Modern = Retail or Forever" flag, inside the same repo as Retail. TOC strategy is split three ways: a multi-interface base TOC with `[AllowLoadGameType camelot]` per file (Ace3, BigWigs, Bartender4, Dominos, Masque); an `## Interface-Camelot:` line (Plater); or a separate `_Camelot.toc` (Details!, BetterBags). Retail-only gates such as `WOW_PROJECT_ID == WOW_PROJECT_MAINLINE` or `GetBuildInfo() >= 100000` broke on Forever.

### Cited Findings
**ElvUI** — flavour flags plus a Modern alias. [ElvUI/Game/Shared/General/Initialize.lua](https://github.com/tukui-org/ElvUI/blob/main/ElvUI/Game/Shared/General/Initialize.lua):
```lua
E.Forever = WOW_PROJECT_ID == WOW_PROJECT_CAMELOT
E.Retail = WOW_PROJECT_ID == WOW_PROJECT_MAINLINE

E.Modern = E.Retail or E.Forever
```
The vendored oUF in ElvUI ([ElvUI_Libraries/Game/Shared/oUF/init.lua](https://github.com/tukui-org/ElvUI/blob/main/ElvUI_Libraries/Game/Shared/oUF/init.lua)):
```lua
oUF.isForever = WOW_PROJECT_ID == WOW_PROJECT_CAMELOT
oUF.isRetail = WOW_PROJECT_ID == WOW_PROJECT_MAINLINE and not oUF.isForever
oUF.isModern = oUF.isRetail or oUF.isForever
```
Recent ElvUI commits: "DT: add ammo on forever" (2026-11-05), "Skins: Forever update" (2026-10-30) and "forever: skin fixes" (2026-10-16) — [ElvUI commits](https://github.com/tukui-org/ElvUI/commits)

**DBM** — a nil-safe fallback literal. [DBM-Core/modules/objects/GameVersion.lua](https://github.com/DeadlyBossMods/DeadlyBossMods/blob/master/DBM-Core/modules/objects/GameVersion.lua):
```lua
private.isMop = WOW_PROJECT_ID == (WOW_PROJECT_MISTS_CLASSIC or 19)
private.isForever = WOW_PROJECT_ID == (WOW_PROJECT_CAMELOT or 18)

function private:ReadPlayerName()
	return self.isForever and GetUnitName("player") or UnitName("player")
end
```
`.luarc.json` declares `WOW_PROJECT_CAMELOT` as a global. Recent commits include "Fix toc load directive for libspec so it actually loads in forever" (2026-10-29), "Fix isTanking on Forever" (2026-10-24), "Expand scope of secret based trash/boss alert systems to forever" (2026-10-15) and "fix range radar lua errors in forever" (2026-10-10) — [DBM commits](https://github.com/DeadlyBossMods/DeadlyBossMods/commits)

**BigWigs** — a TOC-variable load signal, not a runtime constant. `BigWigs.toc` has a single multi-interface line:
```
## Interface: 11508, 11509, 16001, 20505, 20506, 30405, 38002, 40402, 50503, 50504, 120100, 120105, 120107
```
It also loads `Init_[Game].lua`, which the client resolves per game type. `Init_Camelot.lua` is:
```lua
local _, tbl = ...
tbl.isForever = true
tbl.season = 0
```
`Loader.lua` then exports `public.isForever = tbl.isForever` and `public.isModern = tbl.isRetail or tbl.isForever`. A commit on 2026-11-05 changed `if isRetail then` to `if isRetail or isForever then` in the Bars plugin — [BigWigs.toc](https://github.com/BigWigsMods/BigWigs/blob/master/BigWigs.toc), [Loader.lua](https://github.com/BigWigsMods/BigWigs/blob/master/Loader.lua), [commit 6eb1eac](https://github.com/BigWigsMods/BigWigs/commit/6eb1eac)

**Bartender4** — a single multi-interface TOC, per-file game-type directives, and (still) an interface-range check. [Bartender4.toc](https://github.com/Nevcairiel/Bartender4/blob/master/Bartender4.toc):
```
## Interface: 120100,120105,11509,50504,20506,16001
Options\Presets.lua [AllowLoadGameType standard]
Options\PresetsForever.lua [AllowLoadGameType camelot, forever][ExcludeLoadGameType classic, standard]
Options\PresetsClassic.lua [AllowLoadGameType classic]
```
[GameTypes.lua](https://github.com/Nevcairiel/Bartender4/blob/master/GameTypes.lua):
```lua
local buildVersion = select(4, GetBuildInfo())
Bartender4.GameType.MainlineStandard = (WOW_PROJECT_ID == WOW_PROJECT_MAINLINE) and buildVersion > 120000
Bartender4.GameType.Forever          = buildVersion >= 16001 and buildVersion < 20000 -- TODO: clean this up once it gets its own project id
...
Bartender4.GameType.Mainline         = Bartender4.GameType.MainlineStandard or Bartender4.GameType.Forever
Bartender4.Features.Keyring    = (Bartender4.GameType.ClassicEra or Bartender4.GameType.ClassicBCC or Bartender4.GameType.Forever) and (KeyRingButton ~= nil)
```
The same file defines a capability layer (`Bartender4.Features.*`) on top of the game types, plus a safety metatable that errors on unknown game-type keys. The 2026-11-03 commit "Enable Totem bar in Wow Forever" switched a gate from `GameType.Mainline` to `GameType.MainlineStandard` — [commit 2ced21c](https://github.com/Nevcairiel/Bartender4/commit/2ced21c)

**Dominos** — maps the project ID to a game-type string. [Dominos/Dominos.lua](https://github.com/tullamods/Dominos/blob/main/Dominos/Dominos.lua):
```lua
elseif WOW_PROJECT_ID == WOW_PROJECT_CAMELOT then
    GAME_TYPE = 'forever'
```
Its TOC has `## Interface: 120107, 120105, 50504, 20506, 16001, 11509` and per-file `[AllowLoadGameType standard, camelot]` — [Dominos.toc](https://github.com/tullamods/Dominos/blob/main/Dominos/Dominos.toc)

**Ace3** — a multi-interface TOC and mostly feature detection.
- [Ace3.toc](https://github.com/WoWUIDev/Ace3/blob/master/Ace3.toc): `## Interface: 11508, 11509, 16001, 20505, 20506, 30405, 38002, 40402, 50503, 50504, 120100, 120105, 120107`
- [.luacheckrc](https://github.com/WoWUIDev/Ace3/blob/master/.luacheckrc) lists `WOW_PROJECT_CAMELOT`.
- AceDB detects the Forever realm and name model by capability, not by flavour ([AceDB-3.0.lua](https://github.com/WoWUIDev/Ace3/blob/master/AceDB-3.0/AceDB-3.0.lua)):
```lua
if RegionalUniqueNamesEnabled and RegionalUniqueNamesEnabled() then
	local isRP = C_GameRules.IsGameRuleActive(Enum.GameRule.RPRuleset)
	...
	local name, surname = UnitNameUnmodified("player")
	charKey = name .. " " .. surname
else
	realmKey = GetRealmName()
	charKey = UnitNameUnmodified("player") .. " - " .. realmKey
end
```
- Commits: "AceDB-3.0: Compatibility with WoW Forever" (2026-09-18), "Remove `realmKey` from `charKey` in WoW Forever as names are unique across all rulesets" (2026-09-25), "AceGUI-3.0: ColorPicker: Fix alpha being inverted in Forever" (2026-10-02), "AceDB-3.0: Recognize RP-PVP for Forever realms" (2026-10-28) — [Ace3 commits](https://github.com/WoWUIDev/Ace3/commits/master)
- Inference: **an addon that vendors AceDB must re-vendor, or its Forever SavedVariables key characters differently from Retail.**

**Details!** — a separate per-flavour TOC. The repo root has `Details.toc` (`## Interface: 120105`, `## Interface-Mists: 50504`) and `Details_Camelot.toc` (`## Interface: 16001`), plus _Cata, _Classic, _Mists, _TBC and _Wrath TOCs. Forever commits run from "First pass to making it work on forever" (2026-09-24) to "...removing last names on Forever" (2026-10-09) — [Details-Damage-Meter](https://github.com/Tercioo/Details-Damage-Meter)

**Plater** — per-flavour interface keys in one TOC, plus a packager keyword. [Plater.toc](https://github.com/Tercioo/Plater-Nameplates/blob/master/Plater.toc):
```
## Interface: 120105, 120107
## Interface-Mainline: 120105, 120107
## Interface-Mists: 50504
...
## Interface-Camelot: 16001
#@version-forever@
## Version: @project-version@-Forever
```
The commit "Camelot toc" is dated 2026-09-19 — [Plater commits](https://github.com/Tercioo/Plater-Nameplates/commits)

**Masque** — multi-interface. [Masque.toc](https://github.com/SFX-WoW/Masque/blob/master/Masque.toc): `## Interface: 11509, 16001, 20506, 30405, 38002, 40402, 50504, 120105`

**BetterBags** — the most thoroughly documented approach, with both signals and a nil-guard. [core/constants.lua](https://github.com/Cidan/BetterBags/blob/main/core/constants.lua):
```lua
local isCamelotProject = WOW_PROJECT_CAMELOT ~= nil and WOW_PROJECT_ID == WOW_PROJECT_CAMELOT
addon.isRetail = WOW_PROJECT_ID == WOW_PROJECT_MAINLINE or isCamelotProject
addon.isForever = addon.isForever == true or isCamelotProject
```
- The `~= nil` guard exists because in a test harness that defines no `WOW_PROJECT_*` globals, `nil == nil` is true and would flag every spec as Forever.
- `core/forever.lua` (`addon.isForever = true`) is listed only in `BetterBags_Camelot.toc`. It was the only signal before build 70170, when `WOW_PROJECT_ID` still equalled MAINLINE.
- The rule file says: "**Never** detect Camelot with `GetBuildInfo`/TOC version checks. The 16001 interface number is not a reliable discriminator."
- Root cause of the 70170 breakage: comparing against `WOW_PROJECT_MAINLINE` alone made `isRetail` false on Forever. The Classic branch then indexed `Enum.BagIndex.Bank`, which is nil on Forever, and the addon died at load. Forever also has 9+9 bank tabs where Retail has 6+5.
- The vendored LibUIDropDownMenu falls into none of its flavour modes on 70170+.
- Sources: [camelot-forever.md](https://github.com/Cidan/BetterBags/blob/main/.claude/rules/camelot-forever.md), [core/forever.lua](https://github.com/Cidan/BetterBags/blob/main/core/forever.lua)

**Others using `WOW_PROJECT_CAMELOT`** (from a GitHub code search): ConsolePort, Total RP 3, Questie (in its LibUIDropDownMenu), RealUI, GW2_UI, Clicked, RXPGuides, XLoot, SilverDragon (`Data/Forever/module.lua`), NDui, simc-addon, ToxiUI and LuckyoneUI — [GitHub code search "WOW_PROJECT_CAMELOT"](https://github.com/search?q=WOW_PROJECT_CAMELOT&type=code)

**No Forever support found:**
- **WeakAuras2**: TOCs only for Cata, Mists, TBC, Vanilla and Wrath, with no Mainline and no Camelot TOC, and no Forever commits since 2026-09 — [WeakAuras2](https://github.com/WeakAuras/WeakAuras2)
- **OmniCC**: `OmniCC/OmniCC.toc` has `## Interface: 110207, 50503, 38000, 20505, 11508` and no commits since 2026-09-01 — [OmniCC.toc](https://github.com/tullamods/OmniCC/blob/main/OmniCC/OmniCC.toc)

**The interface-check trap.** Almost every Retail addon tests `select(4, GetBuildInfo()) >= 100000` to mean "modern client". Forever answers 16001, so those addons take Classic code paths or refuse to start — [forever-addon-kit](https://github.com/Thunderz96/forever-addon-kit)

**Project-ID history.** On beta builds before 70170, `WOW_PROJECT_ID == WOW_PROJECT_MAINLINE`. From 70170 onward it is `WOW_PROJECT_CAMELOT` (18) — [BetterBags rule](https://github.com/Cidan/BetterBags/blob/main/.claude/rules/camelot-forever.md). The community guide reports 69913 returning 1 and 70338 returning 18 — [wowforeverguides patterns](https://wowforeverguides.com/addons/patterns). The two accounts agree.

### Inferences
- The common shape is a three-level model: game type (Retail/Forever/Classic), a derived family (`Modern = Retail or Forever`), and feature flags for the cases where Forever and Retail differ: keyring, totem bar, realm and name model, bank tabs, ammo, secrets.
- Code written as `isRetail = WOW_PROJECT_ID == WOW_PROJECT_MAINLINE` now excludes Forever. Every such gate has to be audited for whether it means "modern UI" (include Forever) or "Midnight Standard only" (exclude it).
- `WOW_PROJECT_CAMELOT` is nil on every non-Forever client. A comparison must guard for nil (BetterBags) or use a literal fallback, `(WOW_PROJECT_CAMELOT or 18)` (DBM), especially in headless tests.
- Bartender4's interface-range Forever check is an acknowledged TODO. It is not a pattern to copy.

### Gaps
- LibSharedMedia-3.0 and LibDBIcon-1.0 are developed on WowAce/CurseForge SVN and git, not on GitHub; the GitHub mirror found, wowace-clone, is stale at interface 80200. Their Forever status is unverified.
- WeakAuras' absence from Retail and Forever was observed from its TOC set, not confirmed against a project statement.
- For Ace3, LibStub, CallbackHandler and AceGUI, I did not verify which tagged release, as opposed to master, carries the Forever fixes.

## Prevailing best practice: feature detection versus flavour detection, and porting guides

### Takeaway
In practice the ecosystem uses **flavour detection for coarse routing** (which TOC and files load, the Modern versus Classic family) through `WOW_PROJECT_ID == WOW_PROJECT_CAMELOT` and TOC `[AllowLoadGameType]` directives, and **feature detection for specific capabilities** (`RegionalUniqueNamesEnabled`, `KeyRingButton ~= nil`, `C_GameRules`). Experienced authors explicitly reject interface-number checks. No canonical porting guide exists. The closest are community repos and the wiki's change notes.

### Cited Findings
- Bartender4 composes `Features.*` flags from the game type AND the existence of a frame, for example `... and (KeyRingButton ~= nil)` — [GameTypes.lua](https://github.com/Nevcairiel/Bartender4/blob/master/GameTypes.lua)
- AceDB branches on `RegionalUniqueNamesEnabled and RegionalUniqueNamesEnabled()`, not on the project ID — [AceDB-3.0.lua](https://github.com/WoWUIDev/Ace3/blob/master/AceDB-3.0/AceDB-3.0.lua)
- BetterBags says "Never detect Camelot with GetBuildInfo/TOC version checks" and sizes its bank tables from the enum instead of hard-coding them — [camelot-forever.md](https://github.com/Cidan/BetterBags/blob/main/.claude/rules/camelot-forever.md)
- The forever-addon-kit gives this porting advice:
  - "Port from your Retail code, not your Classic code."
  - Registering an unknown event throws, so wrap `RegisterEvent` in `pcall`.
  - `GetSpecialization` is absent and spec IDs are new (paladin = 1486).
  - `ReloadUI()` is protected.
  - Creature health is secret in combat.
  - Never test for `loadstring_untainted`; run a snippet instead.
  - Source: [forever-addon-kit](https://github.com/Thunderz96/forever-addon-kit). This is a beta snapshot from 2026-09-24, so re-verify each claim on live.
- Classic-era addons will not load. Authors must rebuild them against the Forever/Mainline API — [Icy Veins](https://www.icy-veins.com/wow-forever/news/addons-in-wow-forever-blizzard-devs-just-addressed-the-big-question/); [ForeverMeta guide](https://forevermeta.me/en/guides/wow-forever-addons-interface)
- Day-one porting reports agree that the Retail API is present on 16001 and the Classic globals are missing — [guildos #7](https://github.com/danielcosta42/guildos/issues/7), [#9](https://github.com/danielcosta42/guildos/issues/9) (as cited by forever-addon-kit)
- Community guide pages exist for Forever addon development. They are secondary and low authority — [wowforeverguides developers](https://wowforeverguides.com/addons/developers), [patterns](https://wowforeverguides.com/addons/patterns)

### Inferences
- For a Ka0s port, this split fits the collection: one compat predicate (`IsForever`, `IsModern`) in LibKa0s Compat, and capability shims for the specific gaps. The known one is `SetDesaturation`, per LibKa0s#44 in this workspace's memory.
- The `[AllowLoadGameType camelot, forever]` per-file directive is the cleanest way to ship Forever-only code without a runtime branch. Its "unrecognised type passes" rule means older clients load the file anyway, so pair it with `[ExcludeLoadGameType ...]` the way Bartender4 does.

### Gaps
- I found no r/wowaddons or Blizzard UI & Macro forum guide on porting Retail addons to Forever. Those sources were not reached within budget.

## How CurseForge, Wago and the BigWigs packager handle Forever

### Takeaway
The BigWigs packager (v2.7.0, released 2026-11-05) fully supports Forever:
- it maps 16xxx interfaces to the game type `forever`;
- it accepts `_Camelot.toc` and the `camelot` and `forever` aliases;
- it allows Forever interfaces in `_Mainline` TOCs but not in `_Classic` TOCs;
- it supports `@version-forever@` keywords;
- it uploads to CurseForge under gameVersionTypeID **88568**.

WoWInterface has no Forever type. CurseForge's app added a "Forever" flavour. Wago upload handling for Forever was not verified.

### Cited Findings
Packager source, all from [release.sh](https://github.com/BigWigsMods/packager/blob/master/release.sh):
- `declare -A game_flavor=( ... ["forever"]="forever" ["camelot"]="forever" )`
- `toc_to_type`: `16???) game_type="forever" ;;`. The `-g` option accepts `forever` and `camelot`.
- Recognised TOC suffixes include `Camelot`: `"$package_name"[-_](Mainline|Classic|Vanilla|BCC|TBC|Wrath|WOTLKC|Cata|Mists|Camelot)\.toc$`. A generated Forever TOC is named `_Camelot.toc`. Unverified whether a `_Forever.toc` suffix is recognised; it is absent from that regex.
- The Mainline family check allows both retail and forever interfaces: "Special check for _Mainline (the "modern" game family) to allow retail (standard) and forever versions". The interface prefix for forever is `16[0-9]`.
- Keyword filters `@version-forever@` and `@non-version-forever@` work in Lua, XML and TOC files.
- CurseForge upload mapping: `forever) game_id=88568 ;;`, next to classic 67408, bcc 73246, wrath 73713, cata 77522, mists 79434, titan 81212, and 517 for retail.
- WoWInterface: `titan|forever) echo "WARNING: No WoWInterface game type match ..."`, so Forever is skipped there.
- In the GitHub release metadata (`release.json`), the flavour is `forever`.

Packager commits ([commits](https://github.com/BigWigsMods/packager/commits/master)):
- "Allow Forever interface versions in `Mainline` toc files" (34709bd, 2026-10-07)
- "Don't allow Forever interface versions in `Classic` toc files" (4f0b1df, 2026-10-07)
- "Retry wowi and wago uploads" (01e8631, 2026-11-05)
- Releases: v2.7.0 (2026-11-05), v2.6.1 and v2.6.0 (2026-09-18).

The packager README's multi-interface example mentions "Forever Beta" and shows `ForeverOnly.lua [AllowLoadGameType camelot][ExcludeLoadGameType standard, classic]` — [packager README](https://github.com/BigWigsMods/packager/blob/master/README.md)

CurseForge:
- The app added support for the "Forever" beta flavour in release 1.321 — [CurseForge blog, app release notes 1.321](https://blog.curseforge.com/app-release-notes-1-321/) (from search results, not fetched)
- One French guide says the app recognises Forever installs from 1.324 — [playnews.gg](https://www.playnews.gg/guides/installer-un-addon-wow-forever-comment-faire-avec-curseforge-ou-a-la-main) (secondary)
- Authors either publish separate "-forever" files (for example Leatrix Plus) or declare 16001 in the Retail file — [playnews.gg](https://www.playnews.gg/guides/addons-wow-forever-lesquels-installer-et-lesquels-remplacent-ceux-de-classic) (secondary)

Status in September: as of 2026-09-18 no addon site had a Forever flavour, and the only reliable packaging signal was a separate `_Camelot.toc` — [forever-addon-kit](https://github.com/Thunderz96/forever-addon-kit). This has since been superseded by the packager's ID 88568 support.

### Inferences
- An addon built with the BigWigs packager and a single multi-interface TOC that includes 16001 will be tagged for both Retail (517) and Forever (88568) on CurseForge from one upload. No separate Forever file is required.
- The Ka0s CurseForge journal and the releases command will start seeing files with Forever game versions under type 88568. Its parser may need to recognise that type ID.

### Gaps
- No official CurseForge author documentation for Forever, and no `/api/game/wow/versions` entry for type 88568, was fetched; the ID comes only from packager source.
- Wago Addons: the packager builds `supported_${wago_type}_patches`, but whether `forever` maps to a Wago type was not traced (line ~3169 of release.sh), and no Wago documentation was found.
- Not checked: whether the packager recognises the `_Forever.toc` suffix alias, which the client has accepted since build 70291.

## Testing tools, mocks and API stubs for Forever

### Takeaway
No packaged Forever luacheck standard or mock library exists. Projects hand-add `WOW_PROJECT_CAMELOT` to their own `.luacheckrc` or `.luarc.json`. The raw material for a Forever global list is Ketho/BlizzardInterfaceResources' `forever` branch and Gethe's `forever` FrameXML. vscode-wow-api has no Forever flavour.

### Cited Findings
- `.luacheckrc` files that list `WOW_PROJECT_CAMELOT`: Ace3, BetterBags, GatherMate2, HandyNotes, HereBeDragons, Total RP 3, Plumber, Musician, LibDispel, SilverDragon, SimpleItemLevel and others — [GitHub code search](https://github.com/search?q=WOW_PROJECT_CAMELOT+path%3A.luacheckrc&type=code). DBM declares it in `.luarc.json` — [DBM .luarc.json](https://github.com/DeadlyBossMods/DeadlyBossMods/blob/master/.luarc.json)
- BetterBags has Forever-specific busted specs: `spec/core/forever_spec.lua` and `spec/core/constants_spec.lua`.
  - The specs check that the flag is set in the Camelot TOC and absent from the base TOC, and the load order.
  - Client flavour detection is exercised with Camelot's real `Enum.BagIndex`, on the 70170+ project ID, on pre-70170 mainline plus the TOC flag, and on live Retail and Classic Era.
  - It also warns that a harness with no `WOW_PROJECT_*` globals makes `nil == nil` true.
  - Source: [camelot-forever.md](https://github.com/Cidan/BetterBags/blob/main/.claude/rules/camelot-forever.md)
- [BlizzardInterfaceResources `forever` branch](https://github.com/Ketho/BlizzardInterfaceResources/tree/forever): `Resources/` holds the global, API, event and CVar lists as of 1.60.1 (70532). This is the usual source for luacheck global lists.
- forever-addon-kit ships a "captured API baseline" and porting tools. `tools/port_to_beta.py` rewrites `>= 100000` checks, and `tools/sv_bridge.py` is a saved-variables workaround — [forever-addon-kit](https://github.com/Thunderz96/forever-addon-kit). These are beta-era tools, so check whether they still apply.
- vscode-wow-api has no Forever flavour; its last commit is 2026-06-24 — [Ketho/vscode-wow-api](https://github.com/Ketho/vscode-wow-api)

### Inferences
- For Ka0s, the practical route is to diff BIR `forever` against `live` (the global functions and C_ namespaces), so the missing-on-Forever globals (such as `SetDesaturation` and `GetSpecialization`) can be listed. Then add `WOW_PROJECT_CAMELOT` to each `.luacheckrc`, and give the LibKa0s test kit a Forever environment preset (`WOW_PROJECT_ID = 18`, `WOW_PROJECT_CAMELOT = 18`, interface 16001) next to the Retail one. That last step is a design suggestion, not an existing tool.
- Headless tests must cover both "constant defined" and "constant nil" environments, because of the `nil == nil` trap.

### Gaps
- I found no published luacheck `std` for Forever and no Forever mock for WoWUnit or wow-mock style harnesses. Absence is not proven: the search covered GitHub code only.
- BIR's `forever` branch is at build 70532, not the launch build 70790, so a diff may miss late changes.
