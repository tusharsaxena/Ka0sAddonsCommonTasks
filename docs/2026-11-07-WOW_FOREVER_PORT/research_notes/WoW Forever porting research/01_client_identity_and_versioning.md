# WoW Forever: client identity and versioning (as of 2026-11-07)

Scope note: "WoW Forever" here means **World of Warcraft: Forever**, Blizzard's official product (internal codename
**Camelot**, community nickname "Classic+"). I found no competing private-server project with an interface number near
16001; every source that gives 16001 ties it to this Blizzard product. Two primary sources were checked directly on
2026-11-07: Blizzard's own patch server (`us.patch.battle.net:1119`) and the datamined Blizzard UI source in
Gethe/wow-ui-source's `forever` branch. Wiki pages and fan sites supply the rest, and are marked as such.

## 1. What WoW Forever is: owner, dates, relationship to Retail, content

### Takeaway
WoW: Forever is an official Blizzard product, set in vanilla-era Azeroth (levels 1-60), that launched on 2026-11-04.
It is **not** a fork of the Classic client. It runs on the **Mainline (Retail) client codebase** as a second "game
type" (Camelot) beside Midnight's "Standard", and shares "the vast majority of APIs available in 12.1.5". The owner's
note that it "uses basically the same client as Retail" is **broadly correct for the engine and API**. The gameplay,
content, many FrameXML files and the version numbering all differ from Retail.

### Cited Findings
- Blizzard's launch post says WoW: Forever is "now live" worldwide — [Blizzard News](https://news.blizzard.com/en-us/article/24315820/world-of-warcraft-forever-now-live). A community forum thread gives the launch time as 3:00 p.m. PST, 2026-11-04 — [US forums](https://us.forums.blizzard.com/en/wow/t/world-of-warcraft-forever-launch-time/2400905).
- Warcraft Wiki: revealed at BlizzCon 2026 (the cited Polygon article is dated 2026-09-12). Beta opened 2026-09-17, a stress test ran 2026-10-21, early name reservation opened 2026-10-27, and launch was 2026-11-04 (worldwide, 23:00 UTC). Internal development name "Camelot". Developer: Blizzard (part of Team 2). Platforms: Windows and macOS. Level cap 60 "indefinitely". "Has its roots in Classic" and "runs concurrently with both retail and Classic". Not in the same continuity as retail — [Warcraft Wiki: World of Warcraft: Forever](https://warcraft.wiki.gg/wiki/World_of_Warcraft:_Forever)
- Setting: after *Warcraft III Reforged: Forsaken Kingdom* and before Molten Core. Expanded Eastern Kingdoms and Kalimdor, 1,000+ new quests across levels 1-60, nine new 5-player dungeons (levels 13-60), and an account-wide horizontal "Legacy System". Included with an active WoW subscription or Game Time — [Blizzard: Return to Azeroth in WoW: Forever](http://worldofwarcraft.blizzard.com/en-us/news/24315643/return-to-azeroth-in-world-of-warcraft-forever)
- Content roadmap per the wiki: raids unlock 2026-12-09 (Barrow Deeps, Hyjal Summit, Onyxia's Lair), Hardcore mode in winter 2026/27, new raids and dungeons in spring 2027 and summer 2027 — [Warcraft Wiki](https://warcraft.wiki.gg/wiki/World_of_Warcraft:_Forever)
- Blizzard developer post "An Update On Secrets In WoW: Forever" (2026-09-15), as quoted on the wiki: "WoW Forever shares Mainline WoW's UI architecture, including the vast majority of APIs available in 12.1.5." Forever and Midnight are "two game types within the Mainline code family: Camelot (to be renamed before launch) and Standard." "The AuraContainer/AuraButton changes introduced in 12.1.0 will be available as well." — [Warcraft Wiki: Patch 1.60.1/API changes/notes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes/notes)
- Primary-source confirmation (datamined UI source, `forever` branch, checked 2026-11-07): Blizzard's TOCs use Mainline-family load conditions with Camelot-specific overrides. For example, `Blizzard_FrameXMLBase.toc` loads `[Game]\Constants.lua [AllowLoadGameType camelot]`, `[Family]\Constants.lua [ExcludeLoadGameType camelot]` and `Constants.lua [AllowLoadGameType mainline]`, and has `Mainline/`, `Camelot/`, `Cata/` and `Mists/` subfolders. Blizzard_TrainerUI loads `[Family]\Blizzard_TrainerUI_Camelot.lua [AllowLoadGameType camelot]`. Blizzard_FriendsFrame has separate `Mainline/` and `Camelot/` copies — [Gethe/wow-ui-source, forever branch](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_FrameXMLBase)
- The Forever API docs contain Camelot-specific constants and enums: `LevelConstsExposed_Camelot`, `LootConsts_Camelot`, `PetConsts_Camelot`, `QuestLogConstsMainlineCamelot`, TraitConfigType `CamelotCombat` = 4, and the new `C_GameRules.GetForeverExperiencePreset()`, which returns `Enum.ForeverExperiencePreset` (Classic = 0, Enhanced = 1) — [Gethe/wow-ui-source forever: Blizzard_APIDocumentationGenerated](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_APIDocumentationGenerated)
- A beta tester (2026-09-18) found retail-style APIs. The globals `GetItemInfo`, `GetSpellInfo`, `GetSpellBookItemName`, `GetNumTalentTabs`, `GetTalentInfo` and `GetNumSkillLines` are absent, with `C_Item`, `C_Spell` and `C_Traits` in their place — [wowforeverbuilds.com](https://wowforeverbuilds.com/news/what-the-wow-forever-beta-breaks-for-addons-secret-health-values-dead-secure-sni) (fan site; tested on beta build 1.60.1.69913)

### Inferences
- Forever is best treated as "a second Mainline game type", like Plunderstorm/WoWLabs. It is not a Classic flavour. Retail-API code (C_Item, C_Spell, Settings, secrets-aware code) is the right baseline. Classic-era API assumptions do not apply.
- The FrameXML is **not identical** to Retail. Blizzard ships Camelot-specific copies of some frames (FriendsFrame, TrainerUI, unit frames reskinned in beta 5). Addons that hook or skin Blizzard frames by name or structure need per-frame checks.

### Gaps
- No official Blizzard statement found on whether the Forever binary is the same executable build as Retail. The build numbers are interleaved but different (see section 2), so they are separate builds of one codebase.

## 2. Version, build and interface numbers; cadence

### Takeaway
Live Forever is **1.60.1, build 70790** (served on 2026-11-07), and its TOC interface number is **16001**. That
confirms the player report: 16001 is the 1.60.1 version written as an interface number. Live Retail is 12.1.5.70783,
interface 120105 (PTR 12.1.7 = 120107). Forever's interface number is therefore far below Retail's, so a Retail-only
`## Interface: 120105` TOC marks the addon "out of date" on Forever. The build-number series is shared with Retail
(70783 vs 70790). Every Forever build from beta to launch kept the version 1.60.1. No Forever patch beyond 1.60.1 has
been announced.

### Cited Findings
- Blizzard patch server, product **`wowf`**, queried 2026-11-07: `us|...|70790|1.60.1.70790|...` (same for eu). Product `wow` (Retail) returns `70783|12.1.5.70783`. `wow_camelot`, `wowf_beta` and `wowft` return no data — [us.patch.battle.net:1119/wowf/versions](http://us.patch.battle.net:1119/wowf/versions), [us.patch.battle.net:1119/wow/versions](http://us.patch.battle.net:1119/wow/versions)
- UI-source export history on the `forever` branch: 1.60.1 (70334) 2026-10-09, (70338) 10-10, (70374) 10-13, (70425) 10-16, (70450) 10-16, (70532) 10-22, (70707) 11-02, (70755) 11-03, (70790) 11-04. On 2026-11-02 the exporter's product was switched from `wow_classic_beta` to `wowf` ("Monitor wowf product") — [Gethe/wow-ui-source commits, forever](https://github.com/Gethe/wow-ui-source/commits/forever). Retail `live` exports over the same period: 12.1.5 (70575) 10-23, (70688) 10-31, (70783) 11-04 — [Gethe/wow-ui-source commits, live](https://github.com/Gethe/wow-ui-source/commits/live)
- The beta ran under the **`wow_classic_beta`** product (same commit as above). The forevermeta guide puts beta addons in `World of Warcraft\_classic_beta_\Interface\AddOns` — [forevermeta.me](https://forevermeta.me/en/guides/wow-forever-addons-interface) (fan guide, 2026-10-23)
- Warcraft Wiki TOC table: Midnight Standard 120105, Midnight Standard Test 120107, **Forever 16001**, Mists 50504, Cata 40402, Wrath (Titan Reforged) 38002, Wrath 30405, TBC 20506, Vanilla 11509 — [Warcraft Wiki: TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- Warcraft Wiki Public client builds: "Classic / Forever Beta" 1.60.1 (2026-10-20) and "Forever PTR" 1.60.1 (2026-11-03), with the numbers 16001 / 70532 / 70790. The table's columns appear mislabelled: 16001 is the interface and 70532/70790 are builds, which matches the patch server. Retail Live 12.1.5 (2026-11-03), Retail PTR 12.1.7 (2026-11-02) — [Warcraft Wiki: Public client builds](https://warcraft.wiki.gg/wiki/Public_client_builds)
- Earlier datamining: a build "Patch 1.60" codenamed Camelot moved from a dev server to a vendor server — [Wowhead](https://www.wowhead.com/classic/news/project-camelot-moves-from-dev-server-to-vendor-server-is-blizzard-planning-a-382310). A German report says builds 1.60.0 and 1.60.1 exist separately on the CDN — [PC Games](https://www.pcgames.de/World-of-Warcraft-Spiel-42971/News/WoW-Classic-Plus-Camelot-Build-2-1550516/) (dates not verified)
- Fan guides agree that Forever addons need a file marked for game version "1.60.1" (interface 16001), and that CurseForge has a "Forever" flavour filter — [forevermeta.me](https://forevermeta.me/en/guides/wow-forever-addons-interface), [wowforeveraddons.com](https://wowforeveraddons.com/articles/wow-forever-addons-folder)
- Beta change sets on the wiki: Beta 4 = build 70291 (2026-10-08), Beta 5 = build 70425 (2026-10-16) — [Warcraft Wiki: Patch 1.60.1/API changes/notes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes/notes)

### Inferences
- Interface encoding: 1.60.1 gives 1·10000 + 60·100 + 1 = **16001**, the same scheme as Retail (12.1.5 → 120105). The next Forever patch, if versioned 1.60.2 or 1.61.0, would be 16002 or 16100. That is speculative, since no such patch is announced.
- Forever shares the build-number counter with Retail and draws on the same codebase (Forever 70790 built on 2026-11-04, Retail 70783 the same day). Forever builds are likely to track Retail's mainline code drops. Retail API changes (12.1.7 and later) will probably reach Forever, but that cadence is unconfirmed.
- The content roadmap (raids on 2026-12-09, spring and summer 2027 content) implies client patches, but their version numbers are unknown.

### Gaps
- No Blizzard source states the cadence or versioning policy for future Forever patches.
- wago.tools/builds returned HTTP 403 to automated fetch, so it was not consulted.

## 3. WOW_PROJECT_ID, WOW_PROJECT_* constant and runtime detection

### Takeaway
**Conflicting and unresolved.** The Warcraft Wiki lists a new constant **`WOW_PROJECT_CAMELOT = 18`** ("Patch 1.60.1
(2026-11-04): Added"). A beta-era test (2026-09-18) reported that **`WOW_PROJECT_ID` returned 1 (= WOW_PROJECT_MAINLINE)**.
The datamined Forever Lua contains no `WOW_PROJECT_CAMELOT` and does not define `WOW_PROJECT_ID` for Mainline, so the
engine defines both and the source cannot settle it. Robust detection should not depend on `WOW_PROJECT_ID` alone. The
interface number from `GetBuildInfo()` (16001 against 12xxxx) is the one discriminator the evidence firmly supports.

### Cited Findings
- WOW_PROJECT table: 1 MAINLINE, 2 CLASSIC, 3 WOWLABS, 5 BURNING_CRUSADE_CLASSIC, 11 WRATH_CLASSIC, 14 CATACLYSM_CLASSIC, **18 WOW_PROJECT_CAMELOT ("World of Warcraft: Forever")**, 19 MISTS_CLASSIC. Note "Patch 1.60.1 (2026-11-04): Added WOW_PROJECT_CAMELOT." The page's last-edited date as fetched (2026-10-17) predates that note, which is an internal inconsistency — [Warcraft Wiki: WOW_PROJECT_ID](https://warcraft.wiki.gg/wiki/WOW_PROJECT_ID)
- Beta 1.60.1.69913: "`WOW_PROJECT_ID` is 1, the same as `WOW_PROJECT_MAINLINE`", so Classic-only guards return early. The article says a first draft claimed the ID was missing and a retest corrected it — [wowforeverbuilds.com](https://wowforeverbuilds.com/news/what-the-wow-forever-beta-breaks-for-addons-secret-health-values-dead-secure-sni)
- Datamined Forever Lua (build 70790): `WOW_PROJECT_*` assignments exist only in `Blizzard_FrameXMLBase/Mists/Constants.lua` and `Cata/Constants.lua` (MAINLINE=1 … MISTS_CLASSIC=19, no 18 listed there). No file references `WOW_PROJECT_CAMELOT` or `WOW_PROJECT_FOREVER`. The Camelot FriendsFrame compares `gameAccountInfo.wowProjectID` against `WOW_PROJECT_ID` — [Gethe/wow-ui-source forever](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_FriendsFrame/Camelot)
- `GetBuildInfo()` returns `buildVersion, buildNumber, buildDate, interfaceVersion, localizedVersion, buildInfo` — [BuildDocumentation.lua, forever branch](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_APIDocumentationGenerated/BuildDocumentation.lua). Given the patch server, Forever's values should be "1.60.1", "70790", and 16001 for interfaceVersion. That is inferred, not observed in game.
- Other in-game signals in the Forever API: `C_GameRules.GetForeverExperiencePreset()` (Classic = 0 / Enhanced = 1, nilable), `C_GameRules.GetActiveGameMode()` / `Enum.GameMode` (Blizzard code compares it with `.Plunderstorm` and `.Standard`), and `C_PvP.IsWarModeFeatureEnabled()`, which returns false on Forever (beta 4) — [forever GameRulesDocumentation.lua](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_APIDocumentationGenerated/GameRulesDocumentation.lua), [Patch 1.60.1/API changes/notes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes/notes)

### Inferences
- Possible reconciliation: in beta Forever ran under the classic-beta product and reported 1, and project 18 was introduced at launch (2026-11-04). This is unconfirmed. If live returns 1, any `WOW_PROJECT_ID == WOW_PROJECT_MAINLINE` check treats Forever as Retail. If it returns 18, every `== WOW_PROJECT_MAINLINE` gate excludes Forever.
- A defensive detection: `local isForever = (WOW_PROJECT_CAMELOT and WOW_PROJECT_ID == WOW_PROJECT_CAMELOT) or (select(4, GetBuildInfo()) < 20000 and C_GameRules and C_GameRules.GetForeverExperiencePreset ~= nil)`. This is a suggestion only, to be verified in game.

### Gaps
- The live value of `WOW_PROJECT_ID`, and whether `WOW_PROJECT_CAMELOT` exists as a global on live, needs an in-game check: `/dump WOW_PROJECT_ID, WOW_PROJECT_CAMELOT, GetBuildInfo()`. The owner should run it, and the result is the deciding evidence.
- The `Enum.GameMode` member values for Forever were not resolved from the docs.

## 4. Install folder, AddOns path, Battle.net product, SavedVariables

### Takeaway
Forever is its own Battle.net product (`wowf`), chosen from World of Warcraft's game-version dropdown. Fan guides agree
the live install folder is **`World of Warcraft\_forever_\`**, so addons go in `_forever_\Interface\AddOns`. During beta
it was `_classic_beta_`. Because each WoW flavour folder carries its own `WTF`, Forever's SavedVariables are separate
from Retail's. No Blizzard post confirms the folder name.

### Cited Findings
- Product code `wowf` on Blizzard's patch server, distinct from `wow` — [us.patch.battle.net:1119/wowf/versions](http://us.patch.battle.net:1119/wowf/versions)
- Path `World of Warcraft/_forever_/Interface/AddOns`, found by choosing Forever in the Battle.net version menu and then gear → Show in Explorer. The `Interface/AddOns` folders may need creating. The page itself notes Blizzard hasn't named the folder publicly — [wowforeveraddons.com](https://wowforeveraddons.com/articles/wow-forever-addons-folder); also [mobalytics](https://mobalytics.gg/wow-forever/profile/broog/guides/how-to-install-addons-wow-forever), [hardcorehelper](https://www.hardcorehelper.com/forever/guides/addons) (fan guides, via search summaries)
- To carry beta setups over, copy `Interface` and `WTF` from `_classic_beta_` into `_forever_` — search summary of [wowforeveraddons.com](https://wowforeveraddons.com/articles/wow-forever-addons-folder). Beta settings do not carry to live on their own — [forevermeta.me](https://forevermeta.me/en/guides/wow-forever-addons-interface)
- A claim that Forever "loads your addons and keybind settings from a previous WoW Beta" is disputed in the article's own comments — [Warcraft Tavern](https://www.warcrafttavern.com/forever/news/wow-forever-loads-your-retail-addons-keybinds/) (2026-09-17). Treat it as unreliable.
- Beta 4: "Forever is now accepted as an alias for Camelot in TOC file suffixes," and also in the `[Game]` variable and the game-type folder lookup — [Patch 1.60.1/API changes/notes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes/notes)

### Inferences
- An addon installed in `_retail_` is not seen by Forever. The owner (or CurseForge/Wago with the Forever flavour) must install into `_forever_`, and the owner's dev symlink setup needs a second link into `_forever_\Interface\AddOns`.
- SavedVariables live separately under `_forever_\WTF\...`, which is inferred from the per-flavour folder layout. No settings are shared with Retail.

### Gaps
- No Blizzard-authored confirmation of `_forever_`. The owner can verify it locally in seconds.

## 5. TOC suffix, multi-interface line, AllowLoadGameType

### Takeaway
Forever loads **`AddonName_Forever.toc`** or **`AddonName_Camelot.toc`** (game suffixes). It also belongs to the
**Mainline family**, so it falls back to `AddonName_Mainline.toc`, and then to the plain `AddonName.toc`. The
comma-separated `## Interface:` line (since 10.2.7) is supported, as in `## Interface: 120105, 16001`. `AllowLoadGameType`
accepts `forever` / `camelot`, and the family value `mainline` covers standard, forever, camelot, plunderstorm and
wowhack.

### Cited Findings
- Game suffixes: `_Standard`, `_Forever` / `_Camelot`, `_Mists`, `_Cata`, `_Wrath`, `_TBC`, `_Vanilla`, `_Plunderstorm` / `_WoWLabs`, `_WoWHack`. Family suffixes `_Mainline` and `_Classic` have lower priority than game suffixes (so `_Standard.toc` wins over `_Mainline.toc` on Midnight) — [Warcraft Wiki: TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- AllowLoadGameType values (case-insensitive): standard, forever, camelot, mists, cata, wrath, tbc, vanilla, plunderstorm, wowhack. Families: **mainline = standard, forever, camelot, plunderstorm, wowhack**; classic = vanilla, tbc, wrath, cata, mists. Repeated directives append. If none of the listed types is recognised, the condition is still satisfied, so pair it with ExcludeLoadGameType — [Warcraft Wiki: TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- The wiki's own example is `## Interface: 120105, 16001, 50504, 11509` ("for retail, forever, classic, and classic era"). Comma-delimited values arrived in 10.2.7, and a mismatch marks the addon out of date — [Warcraft Wiki: TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- Blizzard itself uses `[AllowLoadGameType camelot]`, `[ExcludeLoadGameType camelot]`, `[AllowLoadGameType mainline]` and the `[Game]` / `[Family]` path variables in its own Forever TOCs — [Blizzard_FrameXMLBase.toc, forever](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_FrameXMLBase/Blizzard_FrameXMLBase.toc)
- The `_Forever` suffix alias arrived in beta 4 (build 70291, 2026-10-08). `_Classic.toc` does not apply to Forever — [Patch 1.60.1/API changes/notes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes/notes), [forevermeta.me](https://forevermeta.me/en/guides/wow-forever-addons-interface)
- Beta 4 also renamed the TOC `require` functionality to `import` — [Patch 1.60.1/API changes/notes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes/notes)

### Inferences
- Simplest same-repo support: keep one TOC and set `## Interface: 120105, 16001`. Forever (Mainline family) loads a plain `Addon.toc` or `Addon_Mainline.toc`. A separate `Addon_Forever.toc` is needed only for a different file list.
- Inside a TOC, `[AllowLoadGameType forever]` / `[AllowLoadGameType standard]` per-file annotations allow Forever-only and Retail-only files from one TOC, the same way Blizzard does it. Whether addon TOCs honour per-file bracket conditions as Blizzard's do is assumed from the wiki's directive description, not tested.
- Watch out: an addon TOC that uses `## AllowLoadGameType: standard` to mean "Retail only" excludes Forever. One that uses `mainline` includes it.

### Gaps
- Not verified in game whether `_Standard.toc` is skipped on Forever. The wiki's game/family model implies it is.

## 6. Addon security model: secrets and the Midnight combat lockdown

### Takeaway
**Yes, Midnight's restrictions apply on Forever.** Blizzard said on 2026-09-15 that "the addon disarmament changes
introduced in Midnight, including secrets, will also be active in Forever". The beta confirmed secret UnitHealth and
UnitDetailedThreatSituation values, secret chat, and extra Forever-specific hardening (a secret FrameStrata aspect, and
obfuscated GUID server/spawn IDs). Forever addons must be written to the same secret-values rules as Retail 12.x.

### Cited Findings
- Blizzard quote (2026-09-15): "The addon disarmament changes introduced in Midnight, including secrets, will also be active in Forever." — [Warcraft Wiki: Patch 1.60.1/API changes/notes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes/notes)
- Beta 4 (70291) addon security: trial accounts cannot send addon messages. `SendChatMessage` "EMOTE" needs a hardware event outside instances. A fix closed a leak of minimap rotation values during encounters. A new **`FrameStrata` secret aspect** means `GetFrameStrata` returns a secret for such frames. Beta 5 (70425): the server-ID and spawn-ID parts of creature, vehicle, pet and gameobject GUIDs are obfuscated (stable within a session) to prevent layer comparison — [Patch 1.60.1/API changes/notes](https://warcraft.wiki.gg/wiki/Patch_1.60.1/API_changes/notes)
- Beta 1.60.1.69913: `UnitHealth` returns a secret number that addons cannot compare or do arithmetic with, which breaks third-party raid frames. `RestrictedExecution.lua` calls `loadstring_untainted`, which the beta lacked, so every secure snippet failed (action-bar paging, secure group headers, Clique). The article judged this a likely bug — [wowforeverbuilds.com](https://wowforeverbuilds.com/news/what-the-wow-forever-beta-breaks-for-addons-secret-health-values-dead-secure-sni) (fan site, 2026-09-18)
- The live-branch (70790) `RestrictedExecution.lua` still fetches `loadstring_untainted` (line 22) and calls it (line 79). Whether the engine now provides it is not determinable from the Lua — [RestrictedExecution.lua, forever](https://github.com/Gethe/wow-ui-source/blob/forever/Interface/AddOns/Blizzard_RestrictedAddOnEnvironment/RestrictedExecution.lua)
- The Forever API docs are secrets-annotated like Retail's (for example `SecretArguments = "AllowedWhenUntainted"`, and 228 Secret* annotations in UnitDocumentation.lua) — [forever Blizzard_APIDocumentationGenerated](https://github.com/Gethe/wow-ui-source/tree/forever/Interface/AddOns/Blizzard_APIDocumentationGenerated)
- Player thread (2026-10-06, Forever Beta forum): `UnitDetailedThreatSituation()` values are secret. It works for "nameplate1" but errors for party and raid units and for "player" from tainted code. No blue reply on page 1 — [EU forums](https://eu.forums.blizzard.com/en/wow/t/threat-is-a-secrethidden-value-in-addon-api-why/633885)
- Fan summaries say Forever addons cannot read the combat log, chat reaches addons as secrets, and addon communication is restricted — [wowforevertierlist.com](https://wowforevertierlist.com/addons/restrictions), [Icy Veins](https://www.icy-veins.com/wow-forever/news/addons-in-wow-forever-blizzard-devs-just-addressed-the-big-question/) (secondary; not verified against Blizzard text)
- Secret values were introduced in Patch 12.0.0 — [Warcraft Wiki: Secret Values](https://warcraft.wiki.gg/wiki/Secret_Values)

### Inferences
- Any Ka0s secrets-safe code paths (Midnight-era) apply unchanged on Forever. No "pre-secrets" code path should be revived for Forever.
- Forever may be **stricter** than Retail in places (FrameStrata secret aspect, GUID obfuscation). Code that reads `GetFrameStrata` on Blizzard frames or parses GUID server/spawn fields needs review.
- The owner's earlier finding that the `SetDesaturation` global is missing on WoW:F (LibKa0s#44) is consistent with the datamined source. `SetDesaturation` appears there only as a Model/ModelScene method, not as a Lua global. The global's status on Retail is outside this brief.

### Gaps
- No live-build (70790) report on whether secure snippets and `loadstring_untainted` work now. An in-game check is needed.
- No exhaustive list of APIs that differ between Forever 1.60.1 and Retail 12.1.5 was found (only "the vast majority" are shared).
