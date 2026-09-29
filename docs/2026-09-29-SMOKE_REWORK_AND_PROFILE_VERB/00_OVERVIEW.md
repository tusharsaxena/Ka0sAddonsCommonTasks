# Smoke-test rework and the `profile` verb (2026-09-29)

Two collection-wide items across the eleven Ka0s addons (AbsorbTracker, AuraMaster, BankLedger,
ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat,
WhatGroup), plus LibKa0s and the wow-addon plugin. Outfitter is not a Ka0s addon and is out of scope.

- **010** Rework every addon's `docs/smoke-tests.md`: simplify, dedupe, group by theme.
- **015** Add `/<prefix> profile <name>` to switch profiles quickly, in **all eleven** addons, adding
  profile support (and a Profiles settings page) where it does not exist today.

## Owner decisions (2026-09-29)

| # | Question | Decision |
|---|---|---|
| D1 | Where the verb's logic lives | **Shared in LibKa0s**: a new Slash minor with `CliProfile`; each addon registers its own `profile` verb and routes it there. |
| D2 | Which addons | **All eleven.** Profile support (callbacks, Profiles page, `docs/profiles.md`) is added to PrettyChat, WhatGroup, BankLedger and LootHistory. |
| D3 | Grammar | `profile <name>` switches to an **existing** profile only (exact case, surrounding quotes stripped, spaces allowed); an unknown name is refused with the list. Bare `profile` lists profiles, current marked. AbsorbTracker and PartyFrameEnhanced keep their sub-verbs. |
| D4 | Smoke history | **Evergreen only**: one deduplicated, theme-grouped suite; filled-in batch records dropped (git keeps them); unsigned owner checks kept under "Pending sign-off". |
| D5 | What a profile holds in BankLedger / LootHistory | **Settings only.** Recorded data (ledger, loot history, sessions) stays account-wide in `db.global`; settings move into the profile by a one-time migration into `Default`. BankLedger's `savedvariables-§2` deviation row is retired. |
| D6 | Settings that govern recorded data (BankLedger / LootHistory `retentionDays`, prune/purge rules) | **Stay account-wide** in `db.global`, outside every profile. A profile switch, copy or reset never prunes or deletes history. The Settings page marks retention as account-wide (tooltip) and `docs/profiles.md` lists it under what stays account-wide. (Decided 2026-09-29 after SP-BL-01 review found per-profile retention pruning shared history.) |

Execution guidelines (owner): resumable, checkpointed plan; work on a branch, commit incrementally; push
the branches to origin after major milestones; **no merge to master without the owner's go-ahead**;
ultracode (dynamic workflows).

## Standard position (research, 2026-09-29)

Neither item needs a standard change (Ka0s WoW Addon Standard v2.69.0):
- `docs/smoke-tests.md` internals are not prescribed (documentation-§3 only requires the file, the
  `docs/testing.md` link and the Verification-and-record row); it is a living doc, not a frozen bundle.
- A `profile` host verb is an addon-specific surface (slash-commands.md:7). It is not reserved, so it is
  **not** added to `lib.LIVE_VERBS`; each host widens its own `liveVerbs` (Slash.lua:110-112), which keeps
  hand-copied 13-verb pins in LootHistory, BankLedger, PanelMaster, PrettyChat and WhatGroup green.
- Rules the verb must honor: COMMANDS triple (§3), case-preserved rest, tagged printer and no trailing colon
  (§4), NS.L for host text (localization-§2), one switch log line from the profile handler
  (debug-logging-§10), open panel refreshed (options-ui.md:252), `tests/test_disabled.lua` pins it
  (slash-commands-§7), stub carries every `Cli*` member (slash-commands-§1, testing.md:171-191),
  `docs/profiles.md` once a profile control ships (documentation-§3 Tier 2).

Full research: `research/research.json` (standard, LibKa0s, plugin, 11 inventories, critic).

## Files

- `02_SPEC.md` the contract for every item.
- `03_EXECUTION_PLAN.md` milestones, order, gates, pushes.
- `items.tsv` the manifest; `checkpoints.tsv` the milestone record; `RESUME.md` + `resume-state.sh` resume.
- `smoke-maps/<Addon>.md` old-to-new coverage map per addon (M4).
- `99_REPORT.md` the execution record (M5).
