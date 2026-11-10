# QuickComms on Forever, emote callouts, LibKa0s Role, SkinTester panel

Dated 2026-11-10. The owner's words and every answer are in `inputs/owner-rulings.md` (R1..R8 are the owner's,
C1..C6 are Claude's calls). This is step 5 of the Forever port (`../2026-11-07-WOW_FOREVER_PORT_STEP5/`), group 4,
for QuickComms only, plus QuickComms#15 and two SkinTester changes.

## 1. Why

- QuickComms is next in the port. One codebase serves both clients (build-for-retail-and-forever).
- #15 "Support emotes": callouts that emote instead of chat, on both clients.
- Skin Tester: the Sample controls page is redundant with the showroom, and its settings panel should keep the
  game's look. Only the showroom window is skinned.

## 2. What Forever is, for this addon (measured 2026-11-10)

Sources: Gethe/wow-ui-source `forever` "1.60.1 (70862)" and `live` "12.1.5 (70783)", Ketho/BlizzardInterfaceResources
`forever` (session scratchpad clones, not in any repo).

- Forever's talents are `Blizzard_PlayerSpells/Camelot/ClassTalents`: one C_Traits tree per class whose **groups are
  the classic talent trees**. `C_Traits.GetGroupDisplayInfoByTreeID(treeID)` lists the groups and
  `C_Traits.GetGroupCurrencyInfo(configID, groupIDs)` gives the points spent in each. Dual spec exists
  (`C_SpecializationInfo.GetActiveSpecGroup`, `GetCombatConfigIDForSpecGroup`).
- `GetSpecializationRole`, `GetSpecializationRoleByID`, `GetSpecializationInfoForClassID`,
  `GetNumSpecializationsForClassID` and `UnitGroupRolesAssigned` exist on Forever. One spec per class.
- The emote lists (`EmoteList`, `TextEmoteSpeechList` in `ChatEmoteConstants.lua`) are identical on both clients, and
  Forever's GlobalStrings carry `EMOTEn_TOKEN` / `EMOTEn_CMD1` pairs (`/oom`, `/incoming`, `/charge`, `/point`...).
- Forever has secret values (the CharacterFrame taint rule), so the secure send path stays (R4).
- Names: "First Last", the ruleset as the realm key (client-quirks-§5). `UnitFullName`'s second value is a surname.

## 3. LibKa0s: a Role module (R3, R5)

A new library `LibKa0s-Role-1.0` (file `LibKa0s/Role.lua`, in `LibKa0s.xml`), framework-free like Compat, with
docs under `docs/api/` and tests under both kit profiles. Ships in **LibKa0s v1.95.0**. It reads the client and
answers; it owns no SavedVariables, and the host passes its per-character store.

API (names are the builder's to refine, the behavior is fixed):

- `Role:Spec()` returns `specID, name` (plain or nil, secret-safe through Compat).
- `Role:SpecsForClass(classFile)` returns the class's spec ids from the client
  (`GetNumSpecializationsForClassID`/`GetSpecializationInfoForClassID`), so Forever needs no spec seed (C2).
- `Role:Resolve(store)` returns `role, source`, role one of `TANK` / `HEALER` / `DAMAGER` or nil, source one of
  `override`, `assigned`, `talents`, `spec`, `saved`. Order (C1):
  1. `store.override`, the player's own pick, when set.
  2. The group-assigned role (`UnitGroupRolesAssigned("player")`, not `NONE`).
  3. Forever only: the talent group with the most points spent in the active spec group, through a per-class seed
     `TALENT_GROUP_ROLE[classFile][groupIndex]` (classic tree order: Warrior Arms/Fury/Protection =
     DAMAGER/DAMAGER/TANK, Paladin Holy/Protection/Retribution = HEALER/TANK/DAMAGER, Priest Disc/Holy/Shadow =
     HEALER/HEALER/DAMAGER, Shaman Elemental/Enhancement/Restoration = DAMAGER/DAMAGER/HEALER, Druid
     Balance/Feral/Restoration = DAMAGER/DAMAGER/HEALER; Hunter, Rogue, Mage, Warlock all DAMAGER). A tie or zero
     points falls through. The seed is MATCHED, NOT CONFIRMED: the group order is confirmed by the probe (§5.4).
  4. The spec API's role (`GetSpecializationInfo`'s role; on Retail this is the normal answer).
  5. `store.last`, the last resolved role, so a read at login before the client answers still has one.
  Every resolved answer (not `saved`) is written to `store.last` with the spec id.
- `Role:SetOverride(store, role|nil)`.
- `Role:Groups()` (Forever) returns the talent groups with their name, id and points, for diagnostics and the probe.

The standard gets one line in the clients section: spec and role reads go through LibKa0s Role (a minor bump of the
standard, not an addon version).

## 4. QuickComms on Forever

Everything below is gated through `Compat.IsForever()` / `ClientKey()` and per-client seed lists (clients-§5),
never interface numbers. Retail behavior does not change except where §6 says so.

### 4.1 The port items (as waves 1 and 2)

Re-vendor LibKa0s v1.95.0 and roll the provenance line. `NS.DEFAULT_SKIN = Skin:DefaultSkin()`. TOC
`## Interface: 120105, 16001`. README badge and opening line ("Retail and WoW Forever"). DEPENDENCIES. The per-client
feature table in `docs/ARCHITECTURE.md`. Both kit profiles in the gate (`CLAUDE.md`, `docs/testing.md`). A WoW
Forever section in `docs/smoke-tests.md`. A regenerated `docs/test-cases.md`. The 2 strata reads are guarded with
`IsSecret` (the PanelMaster pattern).

### 4.2 Content kinds (R1, C3)

| Kind | Retail | Forever |
|---|---|---|
| openWorld, dungeon, raid | yes | yes |
| battleground | yes | yes, Forever BG list |
| mythicPlus, delve, scenario, arena, housing | yes | hidden: not offered in the When editor, not in Preview as..., built-ins not seeded |

Classify stays the same on both clients. A hidden kind is only hidden from the UI and the seeds, so a profile copied
from Retail still loads. The key-level and difficulty rows are hidden on Forever. `{dungeon}` (M+ only) is left out
of the token list on Forever.

### 4.3 Place lists (R1, R2)

Per client in `defaults/GameIds*.lua`, picked once by `ClientKey()`:

- Forever `DUNGEONS` and `RAIDS` (the season lists, used by Preview as...): the classic-era dungeons and raids
  Forever runs. Raids are a **new Forever list** (R1): Molten Core 409, Onyxia's Lair 249, Blackwing Lair 469,
  Zul'Gurub 309, Ruins of Ahn'Qiraj 509, Temple of Ahn'Qiraj 531, Naxxramas 533, by their Retail map ids.
- Forever `INSTANCES`: the classic-era subset of the Retail list.
- Forever battlegrounds: the classic BGs (Warsong Gulch, Arathi Basin, Alterac Valley) with the ids the Retail BG
  built-ins already use for them, and their objective callouts reused from those built-ins.
- Every Forever id is **MATCHED, NOT CONFIRMED**. The header says so, and the probe (§4.5) plus smoke confirm them.
  A test pins that each Forever id has a row in the Retail map table.

### 4.4 Identity, spec and role (R3, R5)

- `Compat.PlayerIdentity` reads the character key through LibKa0s `Compat.CharacterKey()` (no more
  `UnitFullName`, whose second value is a surname on Forever). `SenderIsPlayer` and `PlayerName` go through the
  library's name helpers, and the character row in the When editor shows and matches the long form.
- The spec and role come from LibKa0s Role. The store is `db.char.role`.
- The When editor's spec row offers `Role:SpecsForClass` on both clients (Retail's `GameIds.SPECS` seed stays as
  the stand-in fallback and for tests).
- A new **Role** dropdown on the General page: Automatic (default) / Tank / Healer / Damage, writing the override,
  with a tooltip that names where Automatic got its answer ("from your talents: Protection"). Both clients.
- `/qc why` and diagnostics print the role and its source.

### 4.5 The probe (R2, C4)

`/qc probe` (both clients, out of combat) records into `QuickCommsDB.global.probes`, keyed by client and
timestamp, and prints a summary: `GetInstanceInfo()` in full (name, type, difficulty id and name, max players,
instance id), `IsInInstance`, the classified content kind, the talent groups (`Role:Groups()`), the resolved role
and source, and the emote tokens the client has. `/qc probe clear` empties it. Claude reads the file after the owner
logs out to confirm the seeds.

### 4.6 Not changing

The send engine, the throttle, the dropped-line note, the dial, the pads, the skin, the channel set (instance chat
and raid warning exist on Forever; smart channels resolve as today).

## 5. Emote callouts (QuickComms#15, both clients)

### 5.1 Two kinds (R6)

- **Custom emote**: a new channel kind `emote`, prefix `/e`, chat type `EMOTE`. Text and tokens work as for any
  channel. It goes in `Channels.KINDS` and the channel dropdown as "Emote". The echo is `CHAT_MSG_EMOTE`.
- **Game emote**: a callout field `emote = "<TOKEN>"` (e.g. `POINT`, `OOM`) instead of text. Its channel is
  `gameEmote`. The bake builds the line from the client's own localized command for that token (the `EMOTEn_TOKEN`
  to `EMOTEn_CMD1` map, built once), never from user text, so the "text may not start with /" rule stays intact
  for user text. An unknown token bakes nothing and the callout shows as unavailable, with the reason. Game emotes
  act on your target as the game does. The echo is `CHAT_MSG_TEXT_EMOTE` (the client's own line); voice emotes
  also play their sound.
- One action per callout (R7). A game emote never carries text.

### 5.2 The editor

The callout editor's channel list gains Emote and Game emote. Picking Game emote replaces the text box with an
emote picker: a searchable list of the client's emotes, the speech ones (`TextEmoteSpeechList`) first and marked
as voice, then the animated ones (`EmoteList`), then the rest. The name defaults to the emote's command
("/point"). The icon works as now.

### 5.3 The seed (R6)

A new built-in group **Emotes**, active in the open world in any group size (`when = { content = { openWorld =
true } }`), placed after the existing World group. Seeded callouts, one list for both clients (C5):

- Voice: /incoming, /charge, /attacktarget, /openfire, /oom, /healme, /helpme, /flee, /wait, /follow.
- Social: /wave, /hello, /thank, /cheer, /bow, /point, /dance, /ready, /lol, /bye.

Each seeded token must exist in both clients' GlobalStrings, and a test pins that. The group is ordinary: edit it,
delete it, Restore built-in groups brings it back. A schema step adds it to existing profiles once (the
Library_Migrate pattern), without touching anything the player edited.

### 5.4 Edges

- Preview and test mode print "would emote /point" (or the /e text) and send nothing.
- The throttle and the dim apply to emotes exactly as to chat.
- A game emote in a group that is copied to another place keeps its token.

## 6. Follow-up issues (R7)

Filed on tusharsaxena/QuickComms, `enhancement`, `state:untriaged`, spaced out:

1. A callout can combine actions on one press: a chat line, an emote, a ping and a raid target marker.
2. Ping callouts: use the ping system (`C_Ping`; Forever ships `Blizzard_PingUI`, to be confirmed on the client).
3. Raid target marker callouts: set a marker on your target as part of a callout.

## 7. Skin Tester (R8)

- Remove the Sample controls page: `settings/Panel.lua`'s page, `settings/Schema.lua`'s `sample` rows, their store
  defaults (kept harmlessly or cleaned by a schema step, the builder's call), tests, `docs/settings-panel.md` and
  any README mention.
- `skin.ignorePanel` defaults to **on** and the toggle stays. Its tooltip changes from "Off by default in this addon"
  to on by default. The documented deviation in `docs/ARCHITECTURE.md` ("`ignorePanel = false`") is removed, and
  the `keepScope` comment in `core/SkinSetup.lua` is reworded. A stored `false` from a player who changed it stays
  theirs. The showroom's panel samples follow the option, as today.

## 8. Anti-goals

- No second code path for Forever sending. No Classic flavor. No version bumps, tags pushed or merges without the
  owner.
- No Forever seed presented as confirmed before the owner's probe and smoke.
- No new SavedVariables global.
- Never split names on whitespace. Never open a Blizzard panel from addon code on Forever.

## 9. Left to the builder

Exact function names, file splits under the 1500-line cap, locale keys, the emote picker's widget (a LibKa0s
dropdown or autocomplete), the schema step numbers, and how the When editor hides rows per client.
