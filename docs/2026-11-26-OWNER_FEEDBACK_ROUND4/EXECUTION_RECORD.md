# Execution record

Workflows:
- `wf_4b563bc8-f13`: the recon.
- `wf_9c6b1326-97b`: the build, one review per repo, and fixes.
- `wf_fa874d8b-300`: R4-DW-11, the verdict panel (addendum A1), with its review and fix.

Builders worked in `~/ka0s-scratch/r4/<Repo>`. Nothing is merged: every branch waits on the owner's go-ahead.

## Branch heads (pushed), lead re-gate 2026-11-26

| Repo | Head | Retail | Forever | luacheck | seeds | perf |
|---|---|---|---|---|---|---|
| LibKa0s | 0272c7dd (tag v1.118.0 local) | 5263/0 | 5263/0 | 0/0 (394) | 18 | n/a |
| DropWatcher | acc4f1e | 2854/0/140 | 2877/0/115 | 0/0 (305) | 33 | green both |
| CombatTrail | fca5bd4 | 1842/0/1 | 1832/0/1 | 0/0 (220) | 37 | green both |
| RangeMaster | 95b8461 | 881/0/1 | 881/0/1 | 0/0 (119) | 23 | green both |

## What happened in the run

- **The LibKa0s step was derailed.** The R4-LK-01 builder read a mid-run owner message (closing SkillMaster issues) as its
  brief and stopped without doing anything. The Drop Watcher fix pass then built R4-LK-01 (`c06c772c`, release record
  `0272c7dd`, local tag v1.118.0), R4-DW-00 and R4-DW-02. Every manifest item now has its commit.
- **Built out of order.** R4-DW-01, 03, 04 and 05 were built before R4-DW-00, because none of them needs the new icon.

### Review fixes

- **CombatTrail:**
  - a HUD the pull opened fades after a fight with no hit;
  - a width of 260 the player chose is kept;
  - the texts say the HUD opens at the pull.
- **RangeMaster:**
  - "Use for this character" moves the containers the v5 upgrade pinned;
  - a Devourer's new profile holds Caster 40 alone;
  - deleting your own set lands on your class set or a generic one, never another class's.
- **Drop Watcher:**
  - the badge doc;
  - less allocation on a rich first hover;
  - the separator kept one pixel tall after a scale change;
  - Mining is teal, not near-white.
- **R4-DW-11:**
  - the panel follows a gear change as the tooltip's badge does;
  - an item you only wear doesn't count;
  - a "still loading" breakdown is worked out again.

### Calls made during the build

- **R4-CT-08:** with `openOnPull` on by default, the HUD opens at combat entry, before the first hit. Until then it shows
  the last fight's card or the pre-fight look.
- **R4-RM-01:** the assignment is written back, which reverses round 3's spec call C3 ("not written back"), as the recon
  proposed.
- **R4-DW-03:**
  - the bundle `docs/seed-research/2026-11-26-forever-recipes-gathering` is pinned to build 1.60.1.70938;
  - Mining's smelting recipes now show under ores.
- **R4-DW-11:**
  - each cap or bound that moves the sum is its own line, so the lines always add up to the score;
  - the panel's and the tooltip's wording of the same part differ on purpose: the panel itemises, the tooltip summarises.
    The review's nit on this was rejected.

## The live tooltip overflow (outside the plan)

On 2026-11-26 the owner reported C stack overflows in item tooltip post calls (SkillUpForever, ItemTree, Drop Watcher). They
come from AlreadyKnown's merchant scan and from opening the character panel.

- **Timeline:** the first one was saved at 10:21, after round 3 merged at 09:04. The other addons are unchanged since 25
  Nov.
- **Suspect:** round 3's separator. It hooks `OnSizeChanged` and reads `GetTop` and `GetBottom` while the tooltip is being
  filled. It also calls `Show()` mid-fill.
- **Round 4's separator (R4-DW-06)** is anchored, has no `OnSizeChanged` hook and no geometry reads, and calls `Show()` only
  when the client is not filling the tooltip.
- **Bisect:** the owner was asked to run `/dw set itemSearch.tooltip.header false` then `/reload`, and report.

## Smoke owed (owner)

- Drop Watcher: ITEM-SEARCH-47 to 56. The new dash icon needs a full client restart.
- CombatTrail: R4-CT-SM1 to SM9, plus the amended SM-CT-LG22 and LG27.
- RangeMaster: BANDS-31 to 40.

## Merged (2026-11-26)

The owner said: "Go ahead and merge everything so i can test in game".

- No master had moved since its branch was cut, so each `--no-ff` merge tree is identical to the gated branch head.
- **Pushed masters:**
  - LibKa0s 4dbc1636, with the tag v1.118.0 pushed;
  - Drop Watcher c9c1441;
  - Combat Trail d26a82c;
  - RangeMaster a7b86f3;
  - Skill Master a53f4ef, its windows run merged in the same push.
- The round's feature branches were deleted locally and on origin, and the scratch clones were removed.
