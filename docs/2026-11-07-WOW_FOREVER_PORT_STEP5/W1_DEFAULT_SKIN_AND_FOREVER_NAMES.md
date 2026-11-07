# Wave 1 addendum (2026-11-08): the default skin per client, and Forever's names

The owner's message after the wave-1 Forever smoke: "both absorbtracker and skintester work perfectly!", then two
rulings. Wave 1's plan (`01_WAVE1_PLAN.md`) is frozen, so this file records what followed. Everything is on
`feat/2026-11-07-forever-port-wave1`, committed and unpushed. Nothing is merged, and no tag is pushed.

## 1. The default skin per client

> "default skin in Retail should be Ka0d Default; default skin in Forever should be WoW Forever" (and note it in
> the standards)

| Item | Repo | Commit | Gate |
|---|---|---|---|
| W1-LK-01 | LibKa0s | `b1702bb`, tag `v1.94.0` **local** | 4265 passed / 0 failed under `retail` and `forever`; luacheck 0/0 |
| W1-AT-02 | AbsorbTracker | `fb0963c` | 1065 / 0 under both profiles; luacheck 0/0; inventory matches |
| W1-ST-02 | LibKa0sSkinTester | `f2e408a` | 899 / 0 under both profiles (2 new cases); luacheck 0/0; inventory matches |
| W1-STD-02 | WowAddonStandards | `087a8d1` (v2.104.0) | `check-standard.sh` all passed |

- **Library.** Skin minor 18 adds `Skin:DefaultSkin()`, which answers `CLIENT_DEFAULTS[Compat.ClientKey()]` (`retail = "ka0s"`,
  `forever = "forever"`) and falls back to Ka0s Default. A choice with no skin and an unregistered owner take it.
  `Skin.DEFAULT` stays `"ka0s"`, because it is the token base every skin lays over. Retail answers are unchanged.
- **Addons.** `NS.DEFAULT_SKIN` (`core/SkinSetup.lua`) feeds the profile default and the stand-in fallbacks. A stored
  choice is never rewritten. Tests pin the default per kit profile, and the cases that pin Ka0s Default's values
  choose it by name. The Skin Tester's harness boots on Ka0s Default unless `clientDefault` is set, and its new
  `tests/test_skin_default.lua` covers the client's default.
- **Standard.** skinning-§2 *The default skin is per client (MUST)*: name `Skin:DefaultSkin()`, never the literal or
  an addon's own client check. §3's reset and §4's WoW Forever bullet follow from it, and clients names the rule.
  The same release fixes the `libka0s-counts` erratum `99_WAVE1_REPORT.md` left open (seventy-two files).
- **Ripple.** Every other adopted addon adopts it with its own port (or its next LibKa0s re-vendor). Until then it
  is Retail-only and wears Ka0s Default anyway.
- **Smoke owed.** AbsorbTracker FOREVER-15 and Skin Tester FOREVER-13 cover a fresh profile on each client.

## 2. Forever's character names and realms

> all characters have a first name and last name, and the combination of both must be unique. This also means that
> spacing for elements where character name is displayed may not be sufficient. Also, realm name is vague identifier
> [...] Most players dont even know their realm, they just know ruleset. This doesnt affect the AbsorbTracker and
> SkinTester (except maybe profile name)

The screenshot shows a tooltip reading `CAMWOW AU1 Realm 2 PvP` over `Traxex Silentshot  16 Night Elf`.

- **Recorded** in the standard (v2.104.0, the same commit) as client-quirks-§5's first `Forever` entry. Names can
  contain a space and are unique only whole. Never split them on whitespace. Size every surface that shows a name,
  realm or profile key for the long form, and prefer the ruleset when a realm is shown for orientation. §6 adds an
  **open probe**: what `UnitName`, `GetUnitName(unit, true)`, `UnitFullName`, chat senders, `Ambiguate`,
  `GetRealmName` and `GetNormalizedRealmName` return on Forever. The probe is the owner's to run in game before a
  name-keyed addon is ported.
- **Wave 1.** No code change. The one exposure is the profile key (`Name - Realm`) on the Profiles page. Its earlier
  checks (AbsorbTracker FOREVER-8, Skin Tester FOREVER-7) passed in the owner's run.
- **Triage for later waves.** This is a first pass by grep, not a review: the files that call a name or realm API,
  and the sites that split a string on `-` or a space or take its first word. Some split sites are not names.
  Read each before porting the addon.

| Addon | Files calling name/realm APIs | Split / first-word sites |
|---|---|---|
| DropWatcher | 10 | 1 |
| MultiMeters | 7 | 5 |
| PartyFrameEnhanced | 4 | 1 |
| LootHistory | 2 | 3 |
| QuickComms | 2 | 3 |
| KickCD | 2 | 2 |
| DpsRace | 2 | 1 |
| BankLedger | 1 | 1 |
| OutfitterReborn | 1 | 1 |
| PanelMaster | 0 | 5 |
| PrettyChat | 0 | 3 (and chat sender rendering, by nature) |
| AuraMaster | 0 | 1 |
| ConsumableMaster | 0 | 0 |

## Owed

- Owner smoke: AbsorbTracker FOREVER-15, Skin Tester FOREVER-13, a Retail sanity pass, and the §6 name-API probe.
- The owner's go-ahead to push the branches and the `v1.94.0` tag, and to merge the five repos (LibKa0s joins this
  wave's four) with `/dev-copilot:finalize`.
