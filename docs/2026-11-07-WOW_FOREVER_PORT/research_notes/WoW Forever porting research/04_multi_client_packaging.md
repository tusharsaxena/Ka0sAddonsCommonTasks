# Multi-client TOC, packaging and release: Retail (Mainline) + World of Warcraft: Forever (state as of 2026-11-07)

Scope note: Forever went live on 2026-11-04 as client 1.60.1, internal game type "Camelot". warcraft.wiki.gg blocks scripted raw fetches, so the wiki quotes below came through a summarising fetch tool. They are short fragments and paraphrases, not full verbatim copies. The BigWigs packager facts come from `release.sh` and `README.md` on its `master` branch, downloaded on 2026-11-07 (master = tag `v2.7.0` = floating tag `v2` = commit `01e8631`, dated 2026-11-05). Source URLs: https://github.com/BigWigsMods/packager/blob/master/release.sh and https://github.com/BigWigsMods/packager/blob/master/README.md.

Local context checked in this collection: `../AuraMaster/AuraMaster.toc` carries a single `## Interface: 120105`, plus `## X-Curse-Project-ID`. The repos have **no `.github/workflows`**, so Ka0s releases are evidently built by CurseForge's own tag-triggered packager, **not** by a BigWigs packager GitHub Action. That matters a lot below. The dev checkouts are symlinked only into `_retail_\Interface\AddOns` (see `../symlinks.txt`).

## 1. TOC loading rules per client: suffixed TOC files, precedence, multi-interface lines, out-of-date

### Takeaway
Forever belongs to the **Mainline family**. A Forever client therefore loads `_Forever.toc` / `_Camelot.toc` first, then `_Mainline.toc`, then the unsuffixed `AddOn.toc`. Both Retail and Forever honour a comma-separated `## Interface: 120105, 16001`. The simplest dual-client setup is the current single unsuffixed TOC with both numbers on the Interface line. Beware of one trap: an existing `_Mainline.toc` is **also** picked up by Forever.

### Cited Findings
- Game-type TOC suffixes: `_Standard` (Retail/Midnight), `_Forever` or `_Camelot` (Forever), `_Mists`, `_Cata`, `_Wrath`, `_TBC`, `_Vanilla`, `_Plunderstorm`/`_WoWLabs`, `_WoWHack`. Family suffixes: `_Mainline` covers standard, forever, camelot, plunderstorm and wowhack, and `_Classic` covers vanilla, tbc, wrath, cata and mists. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- Precedence: "The game first searches for TOC files with these suffixes". If none matches the client's game type or its aliases, the game falls back to `AddOnName.toc`. Family suffixes rank below game-type suffixes: with both `AddOnName_Standard.toc` and `AddOnName_Mainline.toc` present, Standard is used on the current expansion and Mainline on the other Mainline-family types. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- The TOC file name must match the folder name. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format); CurseForge also says that otherwise "the CurseForge validator may fail the upload or the addon will not be recognized by the Blizzard client". — [CurseForge support: Multi-TOC](https://support.curseforge.com/support/solutions/articles/9000209856-multi-toc-for-world-of-warcraft-addons) (modified 2024-02-28, does not mention Forever)
- Suffix history: Patch 9.1.0 added multiple TOC suffixes and 12.1.5 added the `_Standard` suffix. 1.60.1 "Added Camelot game type, Game variable value and TOC suffix, with Forever game type and TOC suffix alias". Footnote: "The Camelot value may be changed to Forever in the future." — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- One fan guide says the `_Forever` alias has been accepted since 8 October (beta), and that "`_Classic.toc` does not apply to Forever". — [ForeverMeta guide](https://forevermeta.me/en/guides/wow-forever-addons-interface) (secondary source)
- The comma-delimited Interface line has existed since Patch 10.2.7 ("Added support for comma-delimited Interface versions"). The wiki's example is `## Interface: 120105, 16001, 50504, 11509`, annotated as values "for retail, forever, classic, and classic era". The wiki also recommends comma-delimited versions or inline directives over suffixed TOCs where possible. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- Forever's interface value is `16001` (per-game-type table on the wiki). — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format). Wago's live game data lists Forever patch `1.60.1` only, with `supported_forever_patches: "1.60.1"`. — [Wago API /api/data/game](https://addons.wago.io/api/data/game)
- Out-of-date rule: "If an addon doesn't set an interface version that matches the client's, then it's classified as out-of-date." — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format). The BigWigs README says the same: "If you don't set an interface version that matches the game client, then the addon is flagged out-of-date." — [packager README](https://github.com/BigWigsMods/packager/blob/master/README.md)
- One player guide says an out-of-date addon "may not load at all", and that "Load out of date AddOns" forces loading of mismatched addons. — [Forever Mastery](https://forevermastery.com/en/guides/install-addons); [ForeverMeta](https://forevermeta.me/en/guides/wow-forever-addons-interface)
- A Classic Era addon (11509) does not load in Forever. — [ForeverMeta](https://forevermeta.me/en/guides/wow-forever-addons-interface)
- Real-world dual-client TOC: Horizon-Suite ships `## Interface: 120100, 16001` in one `HorizonSuite.toc`. — [Horizon-Suite #492](https://github.com/Tacit-Labs/Horizon-Suite/issues/492). GuildOS plans `## Interface: 20506, 16001` in one TOC, "no `_Camelot.toc` needed". — [guildos #20](https://github.com/danielcosta42/guildos/issues/20)
- The Retail interface number is ambiguous. The wiki example uses 120105 (12.1.5) and AuraMaster's TOC already has 120105. Wago's live Retail patch is `12.1.5`, but its patch list already contains `12.1.7`. — [Wago API](https://addons.wago.io/api/data/game). The wiki changelog has 12.1.7 entries (RegionalTextLocale), which suggests 12.1.7 exists, possibly only on the PTR. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)

### Inferences
- Recommended Ka0s shape: keep **one unsuffixed `AddOn.toc`** and change its line to `## Interface: 120105, 16001`. Both clients reach it through the fallback rule, and each one finds its own number, so neither shows the out-of-date flag. No suffixed files are needed.
- If a repo ever adds a `_Mainline.toc`, Forever will load it in preference to the unsuffixed file, because Forever belongs to the Mainline family. Use `_Standard.toc` (Retail only, 12.1.5+) and `_Forever.toc` when the two clients need different file lists. A client older than 12.1.5 does not know `_Standard`, but all live Retail clients are 12.1.5+.
- Prefer `_Forever` over `_Camelot` for the client, because the wiki flags Camelot as possibly renamed to Forever. But see section 3: the packager only recognises `_Camelot`. That conflict argues for avoiding suffixed TOCs altogether.
- "Forever-only later" just means dropping `120105` from the Interface line, leaving `## Interface: 16001`. Retail will then flag the addon out-of-date. To hide it from Retail entirely, add `## AllowLoadGameType: forever` as well (see section 2).

### Gaps
- No official Blizzard statement of what happens when an Interface value is unknown to a client (for example, 16001 seen by Retail). In practice a value simply fails to match and is ignored as long as another value matches. That is inference from the "classified as out-of-date" rule, not a quoted rule.
- The exact current behaviour of the "Load out-of-date AddOns" checkbox on Retail 12.x and Forever is not documented by a primary source I could reach.

## 2. AllowLoadGameType, ExcludeLoadGameType, inline file conditionals, variables, `Interface-<Type>` keys

### Takeaway
The client supports `## AllowLoadGameType:` and `## ExcludeLoadGameType:` (the latter since 12.0.0), plus `[AllowLoadGameType x]` / `[ExcludeLoadGameType x]` suffixes on file lines. The game types include `forever` and `camelot`, and the family `mainline`. The client does **not** understand `## Interface-Forever:`. That key is a BigWigs packager construct which the packager strips at build time.

### Cited Findings
- Directive: `## AllowLoadGameType: standard, classic`. It "Restricts loading this addon to *case-insensitive* game types or their families" and may appear multiple times. Values: `standard, forever, camelot, mists, cata, wrath, tbc, vanilla, plunderstorm, wowhack`. Families: `mainline, classic`. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- Warning: "If at least 1 game type is specified and none of the game types are recognized by the client, the condition will be satisfied". So pair it with ExcludeLoadGameType. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- `ExcludeLoadGameType` is the inverse and was added in 12.0.0. Example: `## ExcludeLoadGameType: vanilla, wrath`. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- 11.1.5 made AllowLoadGameType usable by insecure (third-party) addons and added file variables and inline directives for files. 12.0.7 added inline directives and variables for addon directives, and 12.1.7 "Prevented use of variables in addon directives". — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- Inline syntax is `[Directive]` / `[Directive Value]`, case-insensitive, several per line. "For reasons of compatibility, inline directives should generally only ever be used at the end of a line." Supported inline directives: AllowLoad, AllowLoadGameType, ExcludeLoadGameType, AllowLoadTextLocale, AllowLoadEnvironment, Bootstrap (12.1.0), LoadIntoEnvironment. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- Examples (the wiki's, also reproduced in the packager README):
  ```toc
  ## Interface: 11509, 20506, 30405, 38002, 40402, 50504, 120100, 16001
  ## Title: My Cool AddOn
  ## Title: My Cool AddOn in Classic [AllowLoadGameType classic]
  ## AllowLoadGameType: standard, classic
  ## ExcludeLoadGameType: titan, wrath
  [Family]\File.lua
  [Game]\File.lua
  Localization\[TextLocale].lua
  StandardOnly.lua [AllowLoadGameType standard]
  ForeverOnly.lua [AllowLoadGameType camelot][ExcludeLoadGameType standard, classic]
  ```
  — [packager README "Single TOC file"](https://github.com/BigWigsMods/packager/blob/master/README.md); [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- Variables: `[Family]` gives `Mainline`/`Classic`. `[Game]` gives `Standard`, `Vanilla`, `Camelot`, `TBC`, `Wrath`, `Mists` and so on, so on Forever it yields **`Camelot`**, not `Forever`. `[TextLocale]` exists, and `[RegionalTextLocale]` is supported only in Midnight 12.1.7 and Forever. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- The wiki's TOC page documents no `Interface-<flavor>` key. Its localized keys take the form `Title-frFR`. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- `## Interface-[Type]:` lines exist only for the BigWigs packager's TOC splitting. Example: `## Interface: 120100` / `## Interface-Classic: 11509` / `## Interface-Mists: 50504`. — [packager README](https://github.com/BigWigsMods/packager/blob/master/README.md). The packager deletes every `## Interface-` line from the packaged TOC (`sed ... -e '/^## Interface-/d'`, release.sh around line 1751). — [release.sh](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- One addon's issue states "`## Interface-Forever: 16001`" as a requirement. That only works through the BigWigs packager with `enable-toc-creation: yes`. — [WoW-Volume-Sliders #49](https://github.com/SheldonMichaels/WoW-Volume-Sliders/issues/49)

### Inferences
- Per-file gating in a shared TOC: `Compat\Forever.lua [AllowLoadGameType forever, camelot][ExcludeLoadGameType standard]`. List both names so that a future Camelot-to-Forever rename cannot break it, and add the Exclude so that a client which recognises neither name does not load the file. Do the same in reverse for Retail-only files: `RetailOnly.lua [AllowLoadGameType standard]`.
- `[Game]\File.lua` would need a folder named `Camelot\`, not `Forever\`. That is fragile across the possible rename, so prefer explicit inline directives.
- Forever-only addon: `## AllowLoadGameType: forever, camelot` with `## ExcludeLoadGameType: standard, classic`.
- Never commit `## Interface-Forever:` to a TOC that is shipped through CurseForge's own packager. The client ignores it, and it is unknown whether CurseForge's packager reads or strips it.

### Gaps
- I could not confirm whether the Forever client accepts `forever` as a game-type value in AllowLoadGameType or only as a TOC-suffix alias. The wiki lists `forever` among the values and the patch note says "Forever game type ... alias", which reads as accepted, but I found no tested report.

## 3. BigWigs packager: multiple TOCs, multi-interface lines, build keywords, Forever mapping, version in use

### Takeaway
The packager has supported Forever since PR #202 (merged 2026-09-17). Current `v2`/`v2.7.0` treats interface `16???` as game type `forever` and uploads it to CurseForge game-version type **88568** and to Wago's `forever` patches. It skips WoWInterface for Forever. One multi-interface TOC produces **one zip tagged for both Retail and Forever**. It recognises the `_Camelot.toc` suffix but **not `_Forever.toc`**. The keyword `@version-forever@` exists in the code but not in the README's keyword list.

### Cited Findings
- History: "Add WoW Forever support (#202)" `7391c8d` on 2026-09-17. "Allow Forever interface versions in `Mainline` toc files" `34709bd` and "Don't allow Forever interface versions in `Classic` toc files" `4f0b1df`, both 2026-10-07. Tags: `v2.6.1` = `e50a250` (2026-09-18), `v2.7.0` = `v2` = `01e8631` (2026-11-05). — [packager commits](https://github.com/BigWigsMods/packager/commits/master), [PR #202](https://github.com/BigWigsMods/packager/pull/202)
- PR #202 dropped Forever TOC-suffix detection before merge ("Please remove forever toc detection until we have solid confirmation on what they will change to"). `_Camelot` was evidently added later, because current master matches it. — [PR #202](https://github.com/BigWigsMods/packager/pull/202); [release.sh](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- Game-type aliases: `["forever"]="forever" ["camelot"]="forever"`, and `-g forever` / `-g camelot` are accepted. A `-g` x.y.z version with major 1 and minor `6[0-9]` maps to forever. — [release.sh, lines ~80 and ~305-325](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- Interface mapping: `toc_to_type` maps `16???) game_type="forever"`, alongside `11???` classic, `50???` mists, and default retail. — [release.sh ~line 212](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- Recognised TOC suffixes (regex): `[-_](Mainline|Classic|Vanilla|BCC|TBC|Wrath|WOTLKC|Cata|Mists|Camelot)\.toc`. **`Standard` and `Forever` are absent.** — [release.sh ~line 1187 and 1424](https://github.com/BigWigsMods/packager/blob/master/release.sh). Wago's own data does list `_Forever` / `-Forever` as Forever suffixes. — [Wago API](https://addons.wago.io/api/data/game)
- `_Mainline.toc` validation accepts both Retail and Forever interface values ("Special check for _Mainline (the 'modern' game family) to allow retail (standard) and forever versions"). `_Classic.toc` rejects Forever values. — [release.sh ~1240-1258](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- Multi-interface: "You can specify multiple interface versions delimited by commas." Example: `## Interface: 11509, 20506, 30405, 38002, 40402, 50504, 120100, 16001` "would mark an addon compatible with the latest version of all client flavors and Forever Beta". — [packager README](https://github.com/BigWigsMods/packager/blob/master/README.md). Since v2.3.1, "every interface value in every (non-external) TOC file will be included as a supported version when uploading". — [packager releases](https://github.com/bigwigsmods/packager/releases)
- "You only need to run a build once and the file will be tagged with the appropriate versions when uploaded." — [packager README](https://github.com/BigWigsMods/packager/blob/master/README.md)
- Build keywords: the README lists `retail`, `version-retail`, `version-classic`, `version-bcc`, `version-wrath`, `version-cata` and `version-mists`. The code additionally handles `version-forever` in Lua, XML and TOC filters (`lua_filter version-forever`, `toc_filter version-forever`), and its keyword-detection grep includes `forever`. — [README](https://github.com/BigWigsMods/packager/blob/master/README.md); [release.sh ~1918-1991](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- Caveat: "For builds with multiple game types, you won't be able to use build version keywords (e.g., `@version-retail@` ... `@end-version-retail@`) in Lua files ... you need to switch to plain old Lua control statements". In XML you must reorganise your includes into the TOC files. — [README](https://github.com/BigWigsMods/packager/blob/master/README.md)
- Splitting: with `## Interface-[Type]:` lines plus `-S` or `.pkgmeta` `enable-toc-creation: yes`, the packager creates one TOC per type. The forever type is written as `<pkg>_Camelot.toc` (`forever) new_file+="_Camelot.toc"`), and retail as `_Mainline.toc`. — [README](https://github.com/BigWigsMods/packager/blob/master/README.md); [release.sh ~2008-2014](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- CurseForge mapping: the packager fetches `$project_site/api/game/wow/versions` and selects by `gameVersionTypeID`: `classic 67408, bcc 73246, wrath 73713, cata 77522, mists 79434, titan 81212, forever 88568, default (retail) 517`. If a version name is missing, it falls back to the next lower one, then to the highest, and warns: "No CurseForge game version match for ..., using ...". The upload payload is `"gameVersions": [ids]` to `/api/projects/$slug/upload-file`. — [release.sh ~2889-2990](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- WoWInterface: `titan|forever` gives "WARNING: No WoWInterface game type match ... is not supported, ignoring". — [release.sh ~3026](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- File name: `{classic}` adds `-forever` only when a single game type is forced (`-g`) and the tag doesn't already contain it. A normal multi-type build has no game-type suffix. — [release.sh filename_filter ~153](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- Old pins break: GuildOS pinned the packager to `6d50adb` (2025-12-02), which "predates the flavor and does not recognize `forever` or `camelot`". — [guildos #20](https://github.com/danielcosta42/guildos/issues/20). Third-party commits from 2026-09-20 report that `-g forever` validation rejected a non-16xxx interface. — summarised from [PR #202 references](https://github.com/BigWigsMods/packager/pull/202)

### Inferences
- If Ka0s moves to the BigWigs GitHub Action, use `BigWigsMods/packager@v2`, which today includes Forever support and the Mainline/Forever validation. A pin older than `v2.6.1` lacks Forever, and one older than the 2026-10-07 commits mis-validates Forever numbers in `_Mainline.toc`.
- The safest packager-agnostic layout is one unsuffixed TOC with `## Interface: 120105, 16001`. It needs no splitting, no `_Camelot`/`_Forever` choice and no build keywords, and runtime gating happens in Lua or through inline TOC directives.
- Ka0s TOCs use `#@no-lib-strip@` today. That keyword is independent of game type and stays valid.

### Gaps
- **The key gap for Ka0s:** I found no primary documentation of how **CurseForge's own (tag/webhook) packager** reads a comma-separated Interface line, or whether it maps 16001 to the Forever flavour. That is the packager these repos appear to use, since none has a GitHub workflow. CurseForge's own multi-TOC article (2024) describes manual tagging and does not mention Forever or comma lists. A CurseForge ideas post says the API uses the Interface number in the main TOC to determine the game version, and that multi-flavour tagging was later allowed. — [CurseForge ideas CF-I-1832](https://curseforge-ideas.overwolf.com/ideas/CF-I-1832). The reports of other projects "tagged 12.0.0 to 12.1.0 plus 1.60.1" ("Retail +1") show that *some* packager maps every listed number. Their PR does not say which packager. — [NaowhForever #248](https://github.com/naowh-gaming/NaowhForever/pull/248). To verify: tag an alpha (`X.Y.Z-alpha`-style) build and check its game versions on the Files tab, or edit the file's tags manually after upload. CurseForge says "You can always edit your file tags if needed". — [CurseForge support](https://support.curseforge.com/support/solutions/articles/9000209856-multi-toc-for-world-of-warcraft-addons)

## 4. How CurseForge and Wago represent Forever, and tagging one file for several flavours

### Takeaway
On CurseForge, Forever is a separate game-version **type** (`gameVersionTypeID` 88568) with game version `1.60.1`. Retail is type 517. One file is multi-flavour by carrying game-version ids from several types. On Wago, Forever is the `forever` key with patch `1.60.1`, uploaded as `supported_forever_patches`.

### Cited Findings
- CurseForge type ids, as hard-coded in the packager: retail 517, classic 67408, bcc 73246, wrath 73713, cata 77522, mists 79434, titan 81212, forever 88568. — [release.sh](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- The Forever flavour filter is `gameVersionTypeId=88568`, in the same filter as Retail, Classic, TBC, Wrath, Cata, MoP and Titan Reforged. ClassicUI Forever and AtlasLoot Forever published Forever files on 2026-09-18. — [guildos #20](https://github.com/danielcosta42/guildos/issues/20). CurseForge file listings show 1.60.1 under the Forever flavour. — [WoW Forever Suite files](https://www.curseforge.com/wow/addons/wow-forever-suite/files/all)
- Multi-flavour file: the packager sends the union of version ids (`"gameVersions": [<retail id>, <forever id>]`) in a single upload. — [release.sh](https://github.com/BigWigsMods/packager/blob/master/release.sh). GuildOS's expected result is "One file, marked for both game versions". — [guildos #20](https://github.com/danielcosta42/guildos/issues/20)
- Listing extra Retail numbers makes CurseForge show the project as "Retail +1". Listing only `16001` makes it list "under WoW Forever only, not Retail". — [NaowhForever #248](https://github.com/naowh-gaming/NaowhForever/pull/248)
- An unknown game version can fail the upload. GuildOS dropped a hedge value `16000` because "A version Curse doesn't recognize fails the upload". — [guildos #20](https://github.com/danielcosta42/guildos/issues/20). The BigWigs packager instead falls back to the nearest version and warns. — [release.sh](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- Wago: the patches map has `"forever":["1.60.1"]`, the TOC suffixes are `"forever":["-Camelot","_Camelot","-Forever","_Forever"]`, and the live patch is `"supported_forever_patches":"1.60.1"`. — [Wago API](https://addons.wago.io/api/data/game). The packager posts `"supported_forever_patches": [...]`. — [release.sh upload_wago](https://github.com/BigWigsMods/packager/blob/master/release.sh)
- Users pick "Forever" in the CurseForge App version selector, or "Scan computer for games" if it is missing. WowUp 2.24.0 and the Wago App recognise Forever. — [ForeverMeta](https://forevermeta.me/en/guides/wow-forever-addons-interface)

### Inferences
- With one CurseForge project per addon, a release tagged for 12.1.5 and 1.60.1 is offered to both Retail and Forever users of the CurseForge App. No second project is needed. Going Forever-only later just means dropping 120105, and the project will then show under Forever only.
- Do not list speculative or unreleased interface numbers, such as a hypothetical 16002, before CurseForge knows the game version. Depending on the packager, they either fail the upload or are silently remapped.

### Gaps
- No official docs.curseforge.com page listing 88568 was retrieved. The id is corroborated only by the packager source and a third-party issue. The CurseForge Upload API's `/api/game/wow/versions` and `/api/game/version-types` endpoints need an author token, which was not available here.

## 5. Runtime flavour detection in Lua

### Takeaway
Forever reports `WOW_PROJECT_ID == 18` with the constant `WOW_PROJECT_CAMELOT`, which was added in 1.60.1. That constant is `nil` on clients that do not define it. The safe pattern compares against a locally defaulted constant or against the interface range from `GetBuildInfo()`. Never write `~= WOW_PROJECT_MAINLINE` to mean "Classic".

### Cited Findings
- Constants: `WOW_PROJECT_MAINLINE` 1, `WOW_PROJECT_CLASSIC` 2, `WOW_PROJECT_WOWLABS` 3, `WOW_PROJECT_BURNING_CRUSADE_CLASSIC` 5, `WOW_PROJECT_WRATH_CLASSIC` 11, `WOW_PROJECT_CATACLYSM_CLASSIC` 14, **`WOW_PROJECT_CAMELOT` 18 (World of Warcraft: Forever, ProjectConstants.lua 1.60.1)**, `WOW_PROJECT_MISTS_CLASSIC` 19. Patch 1.60.1 (2026-11-04): "Added `WOW_PROJECT_CAMELOT`." — [warcraft.wiki.gg WOW_PROJECT_ID](https://warcraft.wiki.gg/wiki/WOW_PROJECT_ID)
- The wiki's example branches `if WOW_PROJECT_ID == WOW_PROJECT_MAINLINE then -- midnight elseif WOW_PROJECT_ID == WOW_PROJECT_CAMELOT then -- forever ...`. — [warcraft.wiki.gg WOW_PROJECT_ID](https://warcraft.wiki.gg/wiki/WOW_PROJECT_ID)
- Real-world failure risk: Horizon-Suite classifies "any interface below 20000 that isn't a named Classic flavour" as Forever. It notes that if Forever had launched as `WOW_PROJECT_MAINLINE` at 20000 or above, Forever gates "would silently disable". Build 70170 "reportedly gave Forever project ID 18". — [Horizon-Suite #492](https://github.com/Tacit-Labs/Horizon-Suite/issues/492)
- Interface encoding: `%d%02d%02d` of the version gives 1.60.1 = 16001, and `/dump select(4, GetBuildInfo())` shows it in game. — [guildos #20](https://github.com/danielcosta42/guildos/issues/20); [search summary of forevermeta / endgametools](https://forevermeta.me/en/guides/wow-forever-addons-interface)
- The packager README points to Blizzard's constants for multi-type builds instead of build keywords. — [packager README](https://github.com/BigWigsMods/packager/blob/master/README.md)

### Inferences
- Safest pattern (works on every client and survives a Camelot-to-Forever rename of the constant):
  ```lua
  local PROJECT_FOREVER = WOW_PROJECT_CAMELOT or WOW_PROJECT_FOREVER or 18
  local PROJECT_RETAIL  = WOW_PROJECT_MAINLINE or 1
  local projectID = WOW_PROJECT_ID
  local IS_FOREVER = projectID == PROJECT_FOREVER
  local IS_RETAIL  = projectID == PROJECT_RETAIL
  -- belt and braces: interface range check
  local iface = select(4, GetBuildInfo())
  local IS_FOREVER_BY_IFACE = iface >= 16000 and iface < 17000
  ```
  The number 18 comes from the wiki table. `WOW_PROJECT_FOREVER` is hypothetical, a hedge against the rename the wiki footnote anticipates.
- Prefer **feature detection** (`if C_Something and C_Something.Func then`) over flavour checks wherever an API's presence is the real question. Flavour checks belong in a single LibKa0s/Compat module, never scattered through the code.
- Anti-pattern: `if WOW_PROJECT_ID ~= WOW_PROJECT_MAINLINE then --[[classic]] end` puts Forever (18) on the Classic path.

### Gaps
- I have not verified whether Forever also defines `WOW_PROJECT_MISTS_CLASSIC` and the other constants, or whether `C_GameRules`-style APIs expose the game type at runtime. No source covered this.

## 6. SavedVariables, AddOns folders and install paths for a shared repo

### Takeaway
Forever is a sibling client folder, `World of Warcraft\_forever_\`, with its own `Interface\AddOns` and its own `WTF`. One git checkout can be symlinked into both `_retail_` and `_forever_` AddOns folders. SavedVariables are fully separate per client, so no data is shared and no conflict arises, but neither do settings carry over.

### Cited Findings
- Launch path: `World of Warcraft\_forever_\Interface\AddOns` (client 1.60.1.70685). During beta it was `_classic_beta_`, and addons there are not read by Forever. "Each version of the game has its own subfolder there, with its own `Interface\AddOns`". WTF sits at `World of Warcraft\_forever_\WTF`, settings at `WTF\Account\<account>\SavedVariables`, written "on `/reload` or when you log out". — [Forever Mastery (updated 2026-11-04)](https://forevermastery.com/en/guides/install-addons)
- Same paths: "WoW Forever: `World of Warcraft/_forever_/Interface/AddOns/`" alongside Retail `_retail_`. — [WoW-Volume-Sliders #49](https://github.com/SheldonMichaels/WoW-Volume-Sliders/issues/49)
- SavedVariables types: `SavedVariables` lives in `WTF\[account]\SavedVariables\`, `SavedVariablesPerCharacter` per character and server, and `SavedVariablesMachine` is restricted. — [warcraft.wiki.gg TOC format](https://warcraft.wiki.gg/wiki/TOC_format)
- Beta bug: SavedVariables were written but not restored at startup. One guide says it was fixed from build 70009. — [Blizzard forum thread](https://us.forums.blizzard.com/en/wow/t/2356559); [ForeverMeta](https://forevermeta.me/en/guides/wow-forever-addons-interface). Community workaround addons exist, such as [ForeverSVBridge](https://www.curseforge.com/wow/addons/foreversvbridge).
- Current Ka0s dev setup: `mklink /d "G:\Games\Blizzard\World of Warcraft\_retail_\Interface\AddOns\<Addon>" "D:\...\GIT\<Addon>"` (local `../symlinks.txt`). The owner's memory notes that the game loads the GIT checkout through this symlink.

### Inferences
- For Forever dev testing, add a second junction per addon: `mklink /d "G:\Games\Blizzard\World of Warcraft\_forever_\Interface\AddOns\<Addon>" "D:\Profile\Users\Tushar\Documents\GIT\<Addon>"`. Both clients then read the same files. Only one client runs at a time, and each writes its own `WTF`, so there is no SavedVariables collision.
- A DB schema migration run on one client does not touch the other's SavedVariables. The same addon version can face different schema ages on the two clients, which is ordinary migration handling.
- A dev repo on the two clients cannot rely on TOC `## Version` filtering. Both clients load the exact same TOC, so the multi-interface line and inline directives are the only TOC-level switches.
- Keep the `.pkgmeta` `package-as` unchanged. One folder name serves both clients.

### Gaps
- No primary Blizzard source confirms the `_forever_` folder name. The evidence is two consistent secondary sources (one guide, one addon's issue). Whether the beta SavedVariables restore bug is fully fixed on the 1.60.1 live client is not confirmed by Blizzard.
