# Execution record

| Id | Commit | Retail | Forever | luacheck |
|---|---|---|---|---|
| R2P-CT | c1fffc9 | 1625 / 0 | 1615 / 0 | 0 / 0 |
| R2P-RM | 2a22697 | 795 / 0 | 795 / 0 | 0 / 0 |
| R2P-MM | f1b0d79 | 2658 / 0 | Retail only | 0 / 0 |
| R2P-CM | 4cd5cea | 1524 / 0 | 1524 / 0 | 0 / 0 |
| R2P-BL | fe82e41 | 1856 / 0 | 1835 / 0 | 0 / 0 |
| R2P-LH | 33cb9b4 | 2167 / 0 | 2147 / 0 | 0 / 0 |

Replay: each fixed addon booted with real AceDB on the owner's saved variables, both as they were before the R-2 run
and as they stand migrated. Every look equals the pre-run build's, except Bank Ledger's kept stripes, SD-CT-DEF's glow
and the five call-out hues, one 8-bit step off.

## Deviations and limits

- **The call-out hues.** LibKa0s-Callout draws an exact old default as the skin's sem.* and has no host opt-out, so
  Combat Trail's defaults sit 0.004 off. An opt-out in LibKa0s would retire the nudge (not filed yet).
- **A restore cannot tell** the retired step's write from a player's own tick beside the same default value. Both go off.
- **Multi Meters and Range Master** keep their schema stamps climbing (v29, v3) so a git-master install is repaired too.
- **The loot window** is covered by headless tests only. LOOT_CLOSED's timing on Forever is not yet seen in game.

## Forever probe (build 71037), as read

- Confirmed: Banker 8 and a bank readable at open; no account bank (R1); keyring in bags (R5); "First Surname" keys and
  mail names; coin text; 1792 and 3402 not account-wide; 13262 is Disenchant; default skin forever; Stormwind 1453.
- Corrected: base bank tab 48 slots; the self-loot sender is "First Surname".
- Bugs found: kill loot read Other (1.5 s stamp); one loot booked twice (a claim expiring while combat deferred the flush).
- Still open: dungeon, guild vault, group roll, trade, a key into the bank, bank right after a reload, the Retail pass.
- The probe sheets' Result lines are the owner's and are left empty.
