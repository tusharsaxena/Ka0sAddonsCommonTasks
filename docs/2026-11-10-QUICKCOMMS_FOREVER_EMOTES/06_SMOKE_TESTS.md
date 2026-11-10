# Smoke run sheet (QFE-SMOKE)

The owner runs these in game. Every check below is **owed** until the owner records its result here. Claude
never marks one passed. Each check's full steps and expected result are in the owning repo's
`docs/smoke-tests.md`, under the id given. This sheet is the order to run them in and the place for the results.

## Before you start

- Every repo is on `feat/2026-11-10-quickcomms-forever-emotes`, in the folder the game loads: QuickComms,
  LibKa0sSkinTester, DpsRace.
- **Restart the client fully** (not `/reload`) on both clients, so the new TOC lines and files are read.
- For the Forever checks, QuickComms must be linked into the Forever AddOns folder. The setup is in
  QuickComms' smoke-tests.md, section *WoW Forever*.
- After the Forever pass, send the Forever `QuickComms.lua` SavedVariables file. Its `global.probes` table is
  what confirms the Forever dungeon and raid ids and the talent-group order (FOREVER-16, FOREVER-22, LibKa0s
  `TALENT_GROUP_ROLE`).

## 1. Retail

| # | Check | Where | Result |
|---|---|---|---|
| 1 | ROLE-1, ROLE-2, ROLE-3: the Role row, group role over spec, Character and Specialization rows | QuickComms | pass (owner, 2026-11-10) |
| 2 | EMOTE-1, EMOTE-3: custom `/e` and a game emote callout | QuickComms | pass (owner, 2026-11-10) |
| 3 | EMOTE-4, EMOTE-5: the emote picker (order, voice marks, name rule), preview, throttle, unknown token | QuickComms | pass (owner, 2026-11-10) |
| 4 | EMOTE-7, EMOTE-8: the Emotes set in the open world, gone in a dungeon; an existing profile gains it once, after Solo | QuickComms | pass (owner, 2026-11-10) |
| 5 | EMOTE-2, EMOTE-6: an emote and a game emote on a raid boss. **Record what the game does**, since the lock is set as for Say but not confirmed | QuickComms | pass (owner, 2026-11-10) |
| 6 | FOREVER-23: `/qc probe` on Retail (talent groups `none`), `probe clear`, `/qc help` lists probe | QuickComms | pass (owner, 2026-11-10) |
| 7 | Regression sweep: a pad and a dial send in the open world and in a dungeon; Mythic+ and Arena sets still seed on a fresh Retail profile | QuickComms | pass (owner, 2026-11-10) |
| 8 | PANEL-21, PANEL-6: on a fresh profile only the showroom window wears the skin; the *Ignore settings panel* box is ticked, works live, and an untick survives a full restart | LibKa0sSkinTester | pass (owner, 2026-11-10) |
| 9 | The Sample controls page is gone from the Skin Tester settings; PANEL-17 (a dropdown closes on an outside press) on the Skin tab | LibKa0sSkinTester | pass (owner, 2026-11-10) |
| 10 | DPS Race still loads and runs on Retail as before | DpsRace | pass (owner, 2026-11-10) |

Note for row 8: profiles that never touched the box now show it ticked, because the old default (off) was
never saved. Your own profile is one of them.

## 2. WoW Forever

| # | Check | Where | Result |
|---|---|---|---|
| 11 | FOREVER-1 to FOREVER-11: AddOns list, clean load, panel and launcher, default skin, secure send, dial and strata guards, bindings, profiles across a restart, diagnostics `client:` line, enable/disable | QuickComms | pass (owner, 2026-11-10) |
| 12 | FOREVER-12, FOREVER-13, FOREVER-15: the When editor offers only Open world, Dungeon, Raid and Battleground; *Preview as...* lists the Forever places; `{dungeon}` and `{key}` are not in the token help | QuickComms | pass (owner, 2026-11-10) |
| 13 | FOREVER-14, FOREVER-24: a fresh profile seeds Dungeon, Raid, Solo, Emotes and the three battlegrounds; the Dungeon set matches dungeons alone (no Mythic+) | QuickComms | pass (owner, 2026-11-10) |
| 14 | FOREVER-17: a profile copied from Retail loads and still matches | QuickComms | pass (owner, 2026-11-10) |
| 15 | FOREVER-18, FOREVER-19: Automatic reads the talent tree on a hybrid (warrior, paladin or druid); the Role pick overrides it and Automatic comes back. **Also swap dual spec** and check the role is read again | QuickComms | pass (owner, 2026-11-10) |
| 16 | FOREVER-20, FOREVER-21: the Character row and `{me}` use "First Surname"; your own lines count as yours | QuickComms | pass (owner, 2026-11-10) |
| 17 | FOREVER-16, FOREVER-22: `/qc why` and `/qc probe` in every dungeon, raid and battleground you can reach, plus the open world | QuickComms | pass (owner, 2026-11-10) |
| 18 | EMOTE-1, EMOTE-3, EMOTE-7 on Forever: custom `/e`, a game emote, the Emotes set in the open world. Check that the *Shout* emote sends `/holler` | QuickComms | pass (owner, 2026-11-10) |
| 19 | DPS Race is **not** listed in the Forever AddOns list (it is Retail-only, ruling R9) | DpsRace | pass (owner, 2026-11-10) |
| 20 | PANEL-21 on Forever: only the showroom window wears the skin; FOREVER-5 now runs on the General page's checkboxes | LibKa0sSkinTester | pass (owner, 2026-11-10) |

## Results

Record each result in the table above (pass, or what went wrong) and in the owning repo's smoke-tests.md.
Failures become fix items on this branch before finalize.

On 2026-11-10 the owner reported every check on this sheet passed (rows 1 to 20), after the run was finalized.
The Forever ids run (QuickComms#21) rewrote FOREVER-13 and FOREVER-16 and added FOREVER-25, which passed with
them. Its ids record named all 45 shipped Forever ids as the client does; the group finder hid 15 of them
from the character, every one an activity with a player condition. The results are on each check's `Result:`
line in QuickComms' and LibKa0sSkinTester's smoke-tests.md.

## After the smoke

On the owner's go-ahead: `/dev-copilot:finalize` in dependency order: LibKa0s, LibKa0sSkinTester, QuickComms,
DpsRace, WowAddonStandards, Ka0sAddonsCommonTasks. Then push the v1.95.0 tag and delete this run's branches,
stashes and worktrees.
