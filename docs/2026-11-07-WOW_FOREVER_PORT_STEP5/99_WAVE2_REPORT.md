# Wave 2 execution record (2026-11-08)

Every wave-2 item has its commit on `feat/2026-11-08-forever-port-wave2`. Nothing is merged, tagged or version-bumped.
The three ports ran as one agent per repo; the lead reran each gate before accepting it.

| Item | Repo | Commit | Gate (rerun by the lead) |
|---|---|---|---|
| W2-PM-01 | PanelMaster | `e75f69c` | 1201 passed / 0 failed under `retail` and `forever`; luacheck 0/0; inventory matches; vendored LibKa0s = v1.94.0 |
| W2-PC-01 | PrettyChat | `04d48ba` | 694 / 0 under both; luacheck 0/0; inventory matches; vendored = v1.94.0 |
| W2-PF-01 | PartyFrameEnhanced | `2a6c47c` | 657 / 0 under both; luacheck 0/0; inventory matches; vendored = v1.94.0 |
| W2-STD-01 | WowAddonStandards | `941fa96` | `check-standard.sh` all passed |
| W2-REC | Ka0sAddonsCommonTasks | the plan (`788c324`) and this record | — |

With `16001` in each TOC, the kit's Forever missing-globals suite passed in all three with no allowlist entry.

## What each port found

- **PanelMaster.** The strata guard is `U.PanelStrata(f)` (`modules/Unlock.lua`). It answers the panel's stored
  strata, reads the frame only when that value is not secret, and otherwise uses the template's. All four unlock
  sites use it. PanelMaster now reaches LibKa0s Compat for `IsSecret`, so its adopted-majors count moves from eleven
  to twelve. The `skin.skin` schema row also held the literal default and now names the client's. It reads no
  character names.
- **PrettyChat.** One list serves both clients, by measurement. All 79 GLOBALNAMEs in `defaults/Defaults.lua` are in
  Forever's enUS GlobalStrings with the same text and placeholders as Retail's (Ketho/BlizzardInterfaceResources
  `forever` 1.60.1 (70532) and `live` 12.1.5 (70448), both 2026-10-22). These are the client's own UI string names,
  not clients-§5 seed data. A global missing from a client was already tolerated and tested (PC-R-07). Names pass
  through `%s` untouched.
- **PartyFrameEnhanced.** Its providers and Edit Mode reads match Forever's UI source (Gethe/wow-ui-source `forever`
  1.60.1 (70862) against `live` 12.1.5 (70783)): `PartyFrame`'s member frames and `UpdatePartyFrames`, `CompactPartyFrame`,
  `UseRaidStylePartyFrames` and `EditMode.Exit` are all present, and `PartyMemberFrame.lua` is byte-identical.
  Two fixes:
  - `modules/RangeFade.lua` no longer indexes its rank table with a possibly secret strata.
  - The target, pet and stand-in names go through `Compat.UnitCharacterName`, so they read "First Surname" on
    Forever. The target and pet labels already ended in an ellipsis. The stand-in's name now anchors at both ends.

## Found on the way

- The three inventories were stale by the kit-53 cases, as in wave 1, and are regenerated.
- PanelMaster's and PartyFrameEnhanced's strata guards cite the port's classification
  (`Enum.SecretAspect.FrameStrata`), not a client-quirks entry, because no repo has measured a secret strata in game.
  A measured case would make a quirk entry.

## Owed

- Owner smoke: `04_WAVE2_SMOKE.md`.
- The owner's go-ahead to merge the five branches (`/dev-copilot:finalize`).
