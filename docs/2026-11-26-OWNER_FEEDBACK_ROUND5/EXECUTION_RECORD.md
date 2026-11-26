# Execution record: owner feedback round 5 (2026-11-26)

All built, independently reviewed, fixed and merged on the owner's standing go-ahead ("merge everything as soon as
its ready to merge"). Branches (local and origin) and the `~/ka0s-scratch/r5` clones are deleted. No tags, no
version bumps.

| Repo | Merge | Items | Gate at merge |
|---|---|---|---|
| DropWatcher | e45bff8 | R5-DW-00..11 + 3 review fixes | Retail 2856/0, Forever 2885/0, luacheck 0/0 |
| RangeMaster | 0f80887 | R5-RM-01..04 + 2 review fixes | 885/0 both clients, luacheck 0/0 |
| CombatTrail | 341a654 | R5-CT-01..04 + 1 review fix | Retail 1851/0, Forever 1841/0, luacheck 0/0 |
| SkillMaster | b6ba05b | R5-SM-01..07 + 1 review fix | Forever 1028/0, luacheck 0/0 |
| SkillMaster | 85bbb72 | A1: R5-SM-08..12 + 4 review fixes | Forever 1064/0, luacheck 0/0 |

## Findings worth keeping

- **Tooltip C stack overflow (R5-DW-00).** Drop Watcher's Item post call computed the verdict, the verdict read Pawn,
  and Pawn's `PawnGetItemData` fills `PawnPrivateTooltip1` with `SetHyperlink`, which runs every Item post call
  again. ItemTree, SkillUpForever and AlreadyKnown appeared only as the deepest frame when the stack ran out. Fix:
  a re-entry guard. Not yet confirmed in game.
- **"Keep from 50"** meant the score needed for Keep: 50 or more is Keep, 20–49 Hold, under 20 Sell (a vendor buys
  it) or Toss. The panel now says that in words and the (?) help lists it from the scorer's constants.
- **Healer in Your band sets.** Expert and Ka0s presets created a Healer set for the friendly override once
  R4-RM-02 stopped seeding it into new profiles. Fixed: they use only a Healer set the player has. Existing sets
  are left, since nothing records who made them (the owner's SmokeTest5 profile keeps its Healer set).
- **CT 5/4 rows and Rows shown doing nothing.** One cause: the HUD's own SetSize echoed through OnSizeChanged was
  taken for a grip drag, whose rows outrank the setting; pixel snapping cost the fifth sequence row.
- **CT buffs/debuffs (R5-CT-03): open.** About 70 saved Forever fights hold about 1,170 CAST lines and only 5 buff
  gains, no debuffs. Suspects: aura fields secret in combat (the capture refuses secrets by design), and aura
  watching only starting at `CombatLog.Begin` (an aura landing at the pull is never a gain). Diagnostic shipped
  (`/ct diagnostics` lines `combat sequence aura …`); the fix needs the owner's numbers and a ruling on secrets.
- **SkillMaster joined windows** never built a grip (FB-SM-04 added it to lone frames only).
- **Owner decision owed:** R5-SM-05 documents a standard deviation (launcher-§6): `/sm toggle` opens all windows
  while the Show window entry and keybinding open Professions.

## Smoke

All owner smoke steps were given in chat at hand-off; the per-repo rows are in each repo's `docs/smoke-tests.md`
(DW ITEM-SEARCH-57..63, RM BANDS-41..44, CT R5-CT-SM1..4, SM SM-R5-1..12). None are marked passed.
